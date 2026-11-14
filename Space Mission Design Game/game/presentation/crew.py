"""LAN lobby, main-thread state application, and interpolated remote astronauts."""
from dataclasses import asdict
import ipaddress
import queue
import socket
import textwrap
from ursina import Entity,Text,Button,InputField,scene,color,destroy
from game.network.lan import Server,Client,OWNED
from game.domain.design import Design
from game.domain.navigation import Pose

CYAN=color.rgb32(64,216,222)

class Crew:
    def __init__(self,hub):
        self.hub=hub; self.server=None; self.client=None; self.role=None; self.busy=False
        self.avatars={}; self.players={}; self.timer=0.; self.seen_flight=0; self.revision=-1
        self.message='Solo / N: play together on Wi-Fi'; self.code=''; self.port=8765
        self.status=Text(self.message,parent=hub.hud,position=(-.76,.386),scale=.55,color=CYAN)
    @property
    def active(self):return self.client is not None
    def send(self,action,**fields):
        try:self.client.send({'action':action,**fields})
        except (OSError,ValueError) as exc:self.message='Disconnected: '+str(exc); self.hub.toast(self.message)
    def owned(self,category):return not self.active or category in OWNED.get(self.role,set())
    def open(self):
        h=self.hub
        if h.modal=='flight':h.toast('Finish playback before changing crew sessions.'); return
        if h.panel is not None:h.close_panel()
        h.panel_base('crew','PLAY TOGETHER / SAME WI-FI','Two laptops / one shared mission / N opens this panel')
        p=h.panel
        Text('Host: Spacecraft Engineer / sensor, power, launch hardware\nFriend: Science & Operations / orbit, radio, plan, launch\nBoth players learn, walk independently, and see each other.',parent=p,position=(-.64,.24,-.04),scale=.75)
        Text('\n'.join(textwrap.wrap(self.message,100)),parent=p,position=(-.64,.10,-.04),scale=.67,color=CYAN)
        if self.active:
            if self.server:
                try:ips=', '.join(socket.gethostbyname_ex(socket.gethostname())[2])
                except OSError:ips='Check your Wi-Fi adapter IPv4 address in network settings'
                Text(f'Host address: {ips}\nPort: {self.port} / Room code: {self.code}\nShare your Wi-Fi IPv4 address and room code with your friend.',parent=p,position=(-.64,.02,-.04),scale=.72)
            Button('LEAVE SESSION',parent=p,position=(0,-.24,-.04),scale=(.6,.07),on_click=self.leave)
            return
        Text('Your name',parent=p,position=(-.64,.02,-.04),scale=.7)
        name=InputField(parent=p,position=(-.17,.00,-.05),scale=(.55,.045),default_value='Player',limit_content_to='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 _-',character_limit=24)
        Text('Host IPv4',parent=p,position=(-.64,-.065,-.04),scale=.7)
        address=InputField(parent=p,position=(-.17,-.09,-.05),scale=(.55,.045),default_value='192.168.1.10',character_limit=15)
        Text('Room code',parent=p,position=(-.64,-.155,-.04),scale=.7)
        code=InputField(parent=p,position=(-.17,-.18,-.05),scale=(.55,.045),default_value='',limit_content_to='0123456789',character_limit=6)
        Button('HOST NEW CREW MISSION',parent=p,position=(-.33,-.29,-.04),scale=(.61,.06),text_size=.7,on_click=lambda:self.host(name.text))
        Button('JOIN FRIEND',parent=p,position=(.33,-.29,-.04),scale=(.61,.06),text_size=.7,on_click=lambda:self.join(address.text,code.text,name.text))
        Text('Hosting starts a new shared mission; your solo save is untouched.\nAllow the host through the private-network firewall if your OS asks.',parent=p,position=(-.64,-.35,-.04),scale=.6)
    def host(self,name):
        try:
            self.server=Server(('0.0.0.0',self.port)); self.code=self.server.room.code
            self.client=Client(('127.0.0.1',self.port),self.code,name,'engineer')
            self.message='Hosting / room '+self.code+' / waiting for your friend'; self.open()
        except (OSError,ValueError) as exc:
            if self.server:self.server.stop(); self.server=None
            self.message='Could not host: '+str(exc); self.open()
    def join(self,address,code,name):
        try:
            ip=ipaddress.ip_address(address.strip())
            if ip.version!=4 or ip.is_multicast or ip.is_unspecified or str(ip)=='255.255.255.255':raise ValueError('Use the host Wi-Fi IPv4 address')
            self.client=Client((str(ip),self.port),code.strip(),name,'operations')
            self.message='Connecting to '+str(ip)+'...'; self.open()
        except (OSError,ValueError) as exc:self.message='Could not join: '+str(exc); self.open()
    def leave(self):
        if self.hub.mission.flight is not None:self.hub.mission.finish_flight()
        if self.client:self.client.close()
        if self.server:self.server.stop()
        self.client=None; self.server=None; self.role=None; self.busy=False
        self.hub.design_session.history=[]
        self.revision=-1; self.seen_flight=0; self.code=''
        for avatar in self.avatars.values():destroy(avatar)
        self.avatars={}; self.players={}; self.message='Solo / retained last shared design / N: crew'
        self.open()
    def tick(self,dt):
        if not self.active:return
        while True:
            try:data=self.client.events.get_nowait()
            except queue.Empty:break
            kind=data.get('kind')
            if kind=='welcome':
                self.role=data['role']; p=data['spawn']; self.hub.pose=Pose(p['x'],p['z'],p['yaw'])
                self.message='Connected as '+self.role+' / N: crew details'
                if self.hub.modal=='crew':self.open()
            elif kind=='players':
                membership=set(self.players)!=set(data['players'])
                self.players=data['players']
                if membership and self.hub.modal=='crew':self.open()
            elif kind=='state':self.apply(data)
            elif kind in ('error','notice'):
                self.message=data.get('message','Connection error'); self.hub.toast(self.message)
                if self.hub.modal=='mission':self.hub.mission.message=self.message; self.hub.mission.open()
            elif kind=='disconnected':
                self.players={}; self.message='DISCONNECTED / N to leave and reconnect'; self.hub.toast(self.message)
        self.timer+=dt
        if self.client.closed:
            self.players={}
            if not self.message.startswith('DISCONNECTED'):
                self.message='DISCONNECTED / '+self.message+' / N to leave and reconnect'
        if self.timer>=.1 and not self.client.closed and self.role:
            self.timer=0; p=self.hub.pose
            task={'learning':'Learning','design':'Designing','flight':'In flight','mission':'Mission control'}.get(self.hub.modal,'Exploring')
            self.send('pose',x=p.x,z=p.z,yaw=p.yaw,task=task)
        connected=set(self.players)-{self.role}
        for role in set(self.avatars)-connected:destroy(self.avatars.pop(role))
        for role in connected:
            p=self.players[role]
            if role not in self.avatars:
                root=Entity(parent=scene,position=(p['x'],0,p['z']))
                tint=CYAN if role=='engineer' else color.orange
                Entity(parent=root,model='cube',position=(0,.75,0),scale=(.5,1.2,.35),color=tint)
                Entity(parent=root,model='sphere',position=(0,1.55,0),scale=.48,color=color.light_gray)
                Entity(parent=root,model='cube',position=(0,1.55,.23),scale=(.32,.18,.04),color=color.azure)
                root.label=Text('',parent=root,position=(0,2.05,0),scale=1.5,origin=(0,0),billboard=True,color=tint)
                self.avatars[role]=root
            root=self.avatars[role]; factor=min(1,dt*12)
            root.enabled=self.hub.modal is None
            root.x+=(p['x']-root.x)*factor; root.z+=(p['z']-root.z)*factor
            root.rotation_y+=((p['yaw']-root.rotation_y+180)%360-180)*factor
            root.label.text=p['name']+'\n'+role+' / '+p['task']
        names=', '.join(p['name'] for p in self.players.values())
        self.status.text=self.message+' | '+names
    def apply(self,data):
        if data['revision']<self.revision:return
        self.revision=data['revision']; h=self.hub; s=h.design_session
        h.door_open=data['door_open']
        design=Design(**data['design'])
        changed=design!=s.design
        s.history=[s.design] if data.get('undo',{}).get(self.role) else []
        if changed:s._apply(design,'Crew selection updated by the host.'); h.spacecraft.apply(design); h.refresh_resources()
        c=h.mission.campaign; c.stage=data['stage']; c.approved=data['approved']
        c.last_result=data['last_result']; c.previous_result=data['previous_result']
        h.read_cards=set(data['cards']); h.mission.mode=data['mode']; h.mission.targeted=data['targeted']; self.busy=data['busy']
        if h.modal=='design':h.design_panel.refresh()
        elif h.modal=='mission':h.mission.open()
        if data['result'] is not None and data['flight_id']>self.seen_flight:
            self.seen_flight=data['flight_id']
            if data['busy']:h.mission.start_flight(data['result'])
