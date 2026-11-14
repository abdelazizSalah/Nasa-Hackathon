"""Bounded newline-JSON TCP protocol. Socket threads never touch Ursina objects."""
from dataclasses import asdict
import hashlib
import json
import math
from pathlib import Path
import queue
import secrets
import socket
import socketserver
import threading
from concurrent.futures import ThreadPoolExecutor

from game.domain.design import DesignSession
from game.domain.campaign import Campaign
from game.domain.assembly import Assembly, PLAYER_IDS, assignments, owned, feedback
from game.domain.operations import simulate
from game.orbit.provider import trajectory

MAX_PACKET=1024*1024
ROOT=Path(__file__).resolve().parents[2]

def fingerprint():
    content=json.dumps(json.loads((ROOT/'content/design_catalog.json').read_text(encoding='utf-8')),sort_keys=True)
    content+='room-workflow-v2'+(ROOT/'game/domain/assembly.py').read_text(encoding='utf-8')
    content+=json.dumps(json.loads((ROOT/'content/missions.json').read_text(encoding='utf-8')),sort_keys=True)
    content+=(ROOT/'game/domain/facility_layout.py').read_text(encoding='utf-8')
    content+=''.join((ROOT/'game/domain'/name).read_text(encoding='utf-8') for name in ('design.py','campaign.py','operations.py'))
    return hashlib.sha256(content.encode('utf-8')).hexdigest()

def packet(data):
    encoded=(json.dumps(data,allow_nan=False,separators=(',',':'))+'\n').encode()
    if len(encoded)>MAX_PACKET: raise ValueError('Packet exceeds limit')
    return encoded

class Room:
    def __init__(self,code=None):
        self.code=code or str(secrets.randbelow(900000)+100000)
        self.lock=threading.RLock(); self.peers={}; self.players={}; self.histories={}
        self.session=DesignSession(); self.campaign=Campaign(); self.cards=set(); self.assembly=Assembly()
        self.mode='cached'; self.targeted=True; self.revision=0; self.flight_id=0; self.result=None
        self.busy=False; self.awaiting=set(); self.generation=0
        self.door_open=False
        self.save_path=ROOT/'runtime/crew-save.json'
        self.pool=ThreadPoolExecutor(max_workers=1)

    def state(self):
        return {'kind':'state','revision':self.revision,'design':asdict(self.session.design),
                'stage':self.campaign.stage,'approved':self.campaign.approved,'cards':sorted(self.cards),
                'last_result':self.campaign.last_result,'previous_result':self.campaign.previous_result,
                'mode':self.mode,'targeted':self.targeted,'busy':self.busy,'undo':{r:bool(v) for r,v in self.histories.items()},
                'flight_id':self.flight_id,'result':self.result,'door_open':self.door_open,
                'assembly':self.assembly.snapshot(self.session,self.players),'players':self.players}

    def broadcast(self,data):
        for peer in list(self.peers.values()):
            peer.send(data)

    def changed(self):
        self.revision+=1; self.broadcast(self.state())

    def attach(self,peer,hello):
        with self.lock:
            if not isinstance(hello,dict):raise ValueError('Expected a handshake object')
            if hello.get('version')!=2 or hello.get('catalog')!=fingerprint(): raise ValueError('Different game/content version. Use the same checkout on both laptops.')
            if not secrets.compare_digest(str(hello.get('code','')),self.code): raise ValueError('Incorrect room code')
            role=hello.get('role')
            if role=='engineer':
                if role in self.peers:raise ValueError('Host slot occupied.')
            else:
                if 'engineer' not in self.peers:raise ValueError('Wait for the host to connect first.')
                role=next((p for p in PLAYER_IDS[1:] if p not in self.peers),None)
                if role is None:raise ValueError('Room full (four players).')
            if role=='engineer' and peer.client_address[0] not in ('127.0.0.1','::1'): raise ValueError('Engineer slot belongs to the host')
            name=''.join(c for c in str(hello.get('name','Player')) if c.isalnum() or c in ' _-')[:24] or 'Player'
            peer.role=role; self.peers[role]=peer; self.histories[role]=[]
            if self.busy and self.result is not None:self.awaiting.add(role)
            self.players[role]={'name':name,'x':0.,'z':-4.5 if role=='engineer' else -.8,'yaw':0. if role=='engineer' else 180.,'task':'Exploring','y':0.,'crouch':False}
            if self.assembly.validation:self.assembly.validation=feedback(self.session,self.players)
            peer.send({'kind':'welcome','role':role,'spawn':self.players[role]})
            self.broadcast(self.state()); self.broadcast({'kind':'players','players':self.players})

    def detach(self,peer):
        with self.lock:
            role=getattr(peer,'role',None)
            if self.peers.get(role) is not peer:return
            self.peers.pop(role); self.players.pop(role,None); self.awaiting.discard(role)
            if self.assembly.validation:self.assembly.validation=feedback(self.session,self.players)
            if not self.awaiting and self.result is not None: self.busy=False
            self.broadcast({'kind':'players','players':self.players}); self.changed()

    def action(self,role,data):
        with self.lock:
            if not isinstance(data,dict):raise ValueError('Expected a command object')
            action=data.get('action')
            if action=='pose':
                values=[float(data[k]) for k in ('x','z','yaw')]
                if not all(math.isfinite(v) for v in values) or not -7<=values[0]<=80 or not -7<=values[1]<=14: raise ValueError('Invalid player pose')
                y=float(data.get('y',0))
                if not math.isfinite(y) or not 0<=y<=5:raise ValueError('Invalid vertical pose')
                self.players[role].update(y=y,crouch=bool(data.get('crouch',False)),x=values[0],z=values[1],yaw=values[2]%360,
                    task=str(data.get('task','Exploring')) if data.get('task') in ('Exploring','Learning','Designing','Mission control','In flight') else 'Exploring')
                self.broadcast({'kind':'players','players':self.players}); return
            if action=='finished':
                if data.get('flight_id')==self.flight_id:
                    self.awaiting.discard(role)
                    if not self.awaiting: self.busy=False; self.changed()
                return
            if action=='read':
                valid={c['id'] for c in json.loads((ROOT/'content/learning_cards.json').read_text())['cards']}
                if data.get('card') not in valid: raise ValueError('Unknown learning card')
                self.cards.add(data['card']); self.changed(); return
            if action=='door':
                opening=not self.door_open
                if not opening and any(abs(p['z']-5)<1 and abs(p['x'])<2 for p in self.players.values()):
                    raise ValueError('A crew member is in the doorway. Step clear before closing.')
                self.door_open=opening; self.changed(); return
            if self.busy: raise ValueError('Crew launch in progress; finish playback before editing.')
            if 'engineer' not in self.peers:raise ValueError('Host disconnected. Wait for the host or leave the session to continue solo.')
            if action=='mission':
                if role!='engineer':raise ValueError('Only the host selects the mission.')
                self.assembly.select_mission(data.get('mission'));self.cards.add('purpose')
            elif action=='confirm':
                category=data.get('category')
                if category not in owned(role,self.players):raise ValueError('That subsystem belongs to your teammate.')
                from game.domain.facility_layout import station_position
                x,z=station_position(category,role,self.players)
                p=self.players[role]
                if math.hypot(p['x']-x,p['z']-z)>3.2:raise ValueError('Approach your assigned workshop table first.')
                self.assembly.confirm(self.session,category,role)
            elif action=='carry':
                self.assembly.carry(self.session,role,self.players,data.get('category'))
            elif action=='submit':
                category=data.get('category');p=self.players[role]
                from game.domain.facility_layout import integration_target
                x,z=integration_target(category)
                if math.hypot(p['x']-x,p['z']-z)>3.2:raise ValueError('Approach the integration placement location first.')
                self.assembly.submit(self.session,category,role,self.players)
            elif action=='validate':
                if role!='engineer':raise ValueError('Only the host finalizes validation.')
                p=self.players[role]
                if math.hypot(p['x']-72,p['z']-6.5)>3.2:raise ValueError('Approach the integration validation console first.')
                if self.assembly.validate(self.session,self.players):
                    while self.campaign.stage<4:
                        old=self.campaign.stage
                        self.campaign.advance(self.session,self.cards)
                        if self.campaign.stage==old:break
            elif action=='choose':
                category=data.get('category'); option=data.get('option')
                if category not in owned(role,self.players): raise ValueError('That subsystem belongs to your teammate.')
                old=getattr(self.session.design,category)
                if self.session.choose(category,option):
                    self.histories[role].append((category,old,option)); self.histories[role]=self.histories[role][-30:]
                    self.campaign.changed();self.assembly.changed(self.session)
            elif action=='undo':
                if self.histories[role]:
                    category,old,new=self.histories[role].pop()
                    if category not in owned(role,self.players):raise ValueError('Role ownership changed; choose explicitly at your current station.')
                    if getattr(self.session.design,category)!=new: raise ValueError('That selection changed; choose the desired option explicitly.')
                    self.session.choose(category,old); self.campaign.changed();self.assembly.changed(self.session)
            elif action=='reset_design':
                for category in owned(role,self.players): self.session.choose(category,self.session.catalog['defaults'][category])
                self.histories[role]=[]; self.campaign.changed();self.assembly.changed(self.session)
            elif action=='advance':
                owner=self.stage_owner()
                if owner!=role: raise ValueError('Current task belongs to '+str(owner or 'operations')+'.')
                if self.campaign.stage==3 and not self.assembly.ready(self.session):raise ValueError('Submit all contributions and validate in the integration room first.')
                message=self.campaign.advance(self.session,self.cards)
                self.peers[role].send({'kind':'notice','message':message})
            elif action in ('plan','source'):
                if 'flight' not in assignments(self.players).get(role,[]): raise ValueError('Mission & Flight Dynamics controls the plan and orbit source.')
                if action=='plan': self.targeted=not self.targeted
                else:self.mode='live' if self.mode=='cached' else 'cached'
            elif action in ('save','load','new'):
                if role!='engineer': raise ValueError('The host manages shared saves and new missions.')
                path=self.save_path
                if action=='save':
                    self.campaign.save(path,self.session,self.cards)
                    saved=json.loads(path.read_text()); saved.update(crew_mode=self.mode,crew_targeted=self.targeted,assembly=self.assembly.snapshot(self.session,self.players))
                    temporary=path.with_suffix('.tmp'); temporary.write_text(json.dumps(saved,indent=2)); temporary.replace(path)
                elif action=='load':
                    saved=json.loads(path.read_text()); self.cards=self.campaign.load(path,self.session)
                    self.mode=saved.get('crew_mode','cached'); self.targeted=saved.get('crew_targeted',True)
                    if self.mode not in ('cached','live'): self.mode='cached'
                    self.targeted=bool(self.targeted)
                    self.assembly.restore(saved.get('assembly'),self.session)
                    self.campaign.changed()
                    self.result=None; self.histories={r:[] for r in self.peers}
                else:
                    self.session=DesignSession(); self.campaign=Campaign(); self.cards=set(); self.assembly=Assembly(); self.result=None
                    self.histories={r:[] for r in self.peers}
                self.peers[role].send({'kind':'notice','message':{'save':'Shared mission saved on the host.','load':'Shared mission restored on both laptops.','new':'New shared mission started.'}[action]})
            elif action=='launch':
                if 'flight' not in assignments(self.players).get(role,[]):raise ValueError('Mission & Flight Dynamics initiates launch.')
                p=self.players[role]
                if math.hypot(p['x']-76,p['z']-6.5)>3.2:raise ValueError('Approach the launch-readiness console first.')
                if not self.assembly.ready(self.session):raise ValueError('Complete physical integration and host validation before launch.')
                if self.campaign.stage<4 or self.campaign.approved!=asdict(self.session.design): raise ValueError('Complete shared readiness first.')
                self.busy=True; self.result=None; self.generation+=1
                self.pool.submit(self.run_flight,self.session.design,self.targeted,self.mode,self.generation)
            else: raise ValueError('Unknown crew command')
            self.changed()

    def stage_owner(self):
        roles=assignments(self.players)
        desired='flight' if self.campaign.stage in (0,2) else 'science'
        return 'engineer' if self.campaign.stage==3 else next((p for p,rs in roles.items() if desired in rs),None)

    def run_flight(self,design,targeted,mode,generation):
        try:
            rows,provenance,meta=trajectory(design.orbit,mode=='live')
            result=simulate(self.session.catalog,design,rows,targeted)
            result.update(design=asdict(design),provenance=provenance,input_hash=meta['input_hash'],plan='targeted' if targeted else 'continuous')
            with self.lock:
                if generation!=self.generation:return
                self.result=result; self.flight_id+=1; self.awaiting=set(self.peers)
                c=self.campaign; c.previous_result=c.last_result; c.last_result={k:v for k,v in result.items() if k!='frames'}
                if result['passed']:c.stage=5
                if not self.awaiting:self.busy=False
                self.changed()
        except Exception as exc:
            with self.lock:
                self.busy=False; self.broadcast({'kind':'notice','message':'Host orbit run failed: '+str(exc)}); self.changed()

class Handler(socketserver.StreamRequestHandler):
    def setup(self):
        super().setup(); self.send_lock=threading.Lock(); self.role=None
    def send(self,data):
        try:
            with self.send_lock:self.request.sendall(packet(data))
        except OSError:pass
    def handle(self):
        try:
            self.request.settimeout(8)
            line=self.rfile.readline(MAX_PACKET+1)
            if len(line)>MAX_PACKET or not line.endswith(b'\n'):return
            self.server.room.attach(self,json.loads(line)); self.request.settimeout(10)
            while True:
                line=self.rfile.readline(MAX_PACKET+1)
                if not line or len(line)>MAX_PACKET or not line.endswith(b'\n'):break
                try:self.server.room.action(self.role,json.loads(line))
                except (ValueError,KeyError,TypeError,StopIteration,OSError) as e:self.send({'kind':'notice','message':str(e)})
        except (OSError,ValueError,KeyError,TypeError) as e:self.send({'kind':'error','message':str(e)})
        finally:self.server.room.detach(self)

class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address=True; daemon_threads=True; block_on_close=False
    def __init__(self,address,code=None):
        self.room=Room(code); super().__init__(address,Handler)
        self.thread=threading.Thread(target=self.serve_forever,daemon=True); self.thread.start()
    def stop(self):
        with self.room.lock:
            peers=list(self.room.peers.values())
        for peer in peers:
            try:peer.request.shutdown(socket.SHUT_RDWR); peer.request.close()
            except OSError:pass
        self.shutdown(); self.server_close(); self.room.pool.shutdown(wait=False,cancel_futures=True)

class Client:
    def __init__(self,address,code,name,role):
        self.events=queue.Queue(maxsize=128); self.send_lock=threading.Lock(); self.closed=False
        self.socket=socket.create_connection(address,timeout=3)
        self.socket.settimeout(10)
        self.outgoing=queue.Queue(maxsize=32)
        self.send({'version':2,'catalog':fingerprint(),'code':code,'name':name,'role':role})
        self.writer=threading.Thread(target=self.write,daemon=True); self.writer.start()
        self.thread=threading.Thread(target=self.read,daemon=True); self.thread.start()
    def send(self,data):
        if self.closed:raise ConnectionError('Disconnected. Press N to leave or reconnect.')
        try:self.outgoing.put_nowait(packet(data))
        except queue.Full:raise ConnectionError('Connection is too slow; leave and reconnect.')
    def write(self):
        try:
            while not self.closed:
                try:encoded=self.outgoing.get(timeout=.2)
                except queue.Empty:continue
                with self.send_lock:self.socket.sendall(encoded)
        except OSError:
            self.close()
    def read(self):
        try:
            with self.socket.makefile('rb') as stream:
                while not self.closed:
                    line=stream.readline(MAX_PACKET+1)
                    if not line:break
                    if len(line)>MAX_PACKET or not line.endswith(b'\n'):raise ValueError('Invalid server packet')
                    data=json.loads(line)
                    try:self.events.put(data,timeout=1)
                    except queue.Full:raise ValueError('Network queue full')
        except (OSError,ValueError) as e:
            try:self.events.put_nowait({'kind':'error','message':str(e)})
            except queue.Full:pass
        finally:
            self.closed=True
            try:self.events.put_nowait({'kind':'disconnected'})
            except queue.Full:pass
    def close(self):
        self.closed=True
        try:self.socket.shutdown(socket.SHUT_RDWR)
        except OSError:pass
        self.socket.close()
