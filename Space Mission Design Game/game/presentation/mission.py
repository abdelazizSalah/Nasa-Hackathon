"""Campaign tablet, non-blocking orbit work, launch presentation and mission debrief."""
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict
import json
import math
from pathlib import Path
import textwrap
from ursina import Entity,Text,Button,camera,color,destroy,scene
from game.domain.campaign import Campaign,MISSIONS
from game.domain.operations import simulate
from game.domain.economy import eur
from game.orbit.provider import trajectory
from ursina.shaders import basic_lighting_shader

ROOT=Path(__file__).resolve().parents[2]
CYAN=color.rgb32(64,216,222); AMBER=color.rgb32(255,190,89)

class MissionUI:
    def crew_action(self,action):
        network=getattr(self.hub,'network',None)
        if network is not None and network.active:
            network.send(action); return True
        return False
    def __init__(self,hub):
        self.hub=hub; self.campaign=Campaign(); self.pool=ThreadPoolExecutor(max_workers=1)
        self.future=None; self.mode='cached'; self.targeted=True; self.flight=None
        self.message='Deliver at least 60 MB of useful flood observations. Keep power and storage healthy.'
        self.save_path=ROOT/'runtime/campaign.json'

    def open(self):
        h=self.hub
        if h.panel is not None: h.close_panel()
        h.panel_base('mission','MISSION CONTROL','Flood Watch / consecutive objectives / M opens this tablet')
        p=h.panel; stage=self.campaign.stage
        net=getattr(h,'network',None); crew=net is not None and net.active
        role=net.role if crew else None
        if crew:
            Text('CREW / '+str(role)+' / '+str(len(net.players))+'/4 connected',parent=p,position=(.12,.27,-.04),scale=.6,color=CYAN)
        for i,title in enumerate(MISSIONS):
            mark='DONE' if i<stage else 'NOW' if i==stage else 'LOCKED'
            Text(f'{i+1}. {mark} / {title}',parent=p,position=(-.65,.22-i*.045,-.04),scale=.76,color=CYAN if i<=stage else color.gray)
        Text('\n'.join(textwrap.wrap(self.message,104)),parent=p,position=(-.65,-.035,-.04),scale=.72)
        owner=h.facility.stage_owner()
        Button('COMPLETE CURRENT TASK',parent=p,position=(-.34,-.16,-.04),scale=(.61,.055),text_size=.7,
               disabled=crew and (owner!=role or net.busy),on_click=self.advance)
        Button('LAUNCH & OPERATE',parent=p,position=(.34,-.16,-.04),scale=(.61,.055),text_size=.7,
               disabled=stage<4 or not h.facility.state['ready'] or self.future is not None or not h.facility.flight_owner() or (crew and net.busy),on_click=self.launch)
        Button('SOURCE: '+self.mode.upper(),parent=p,position=(-.34,-.235,-.04),scale=(.61,.055),text_size=.7,disabled=crew and (not h.facility.flight_owner() or net.busy),on_click=self.toggle_source)
        Button('PLAN: '+('TARGETED' if self.targeted else 'CONTINUOUS'),parent=p,position=(.34,-.235,-.04),scale=(.61,.055),text_size=.7,disabled=crew and (not h.facility.flight_owner() or net.busy),on_click=self.toggle_plan)
        for x,label,fn in [(-.48,'SAVE',self.save),(0,'LOAD',self.load),(.48,'NEW MISSION',self.reset)]:
            Button(label,parent=p,position=(x,-.31,-.04),scale=(.4,.05),text_size=.7,disabled=crew and (role!='engineer' or net.busy),on_click=fn)
        Text('Cached GMAT works offline. Live GMAT uses your local installation.\nTargeted stops imaging after 120 MB; Continuous risks storage overload.',parent=p,position=(-.65,-.355,-.04),scale=.6,color=color.light_gray)

    def advance(self):
        if self.crew_action('advance'):return
        if self.campaign.stage==3 and not self.hub.facility.state['ready']:
            self.message='Submit all contributions and validate at the integration room first.';self.open();return
        self.message=self.campaign.advance(self.hub.design_session,self.hub.read_cards); self.open()
    def toggle_source(self):
        if self.crew_action('source'):return
        self.mode='live' if self.mode=='cached' else 'cached'; self.open()
    def toggle_plan(self):
        if self.crew_action('plan'):return
        self.targeted=not self.targeted; self.open()
    def save(self):
        if self.crew_action('save'):return
        try:
            self.campaign.save(self.save_path,self.hub.design_session,self.hub.read_cards)
            data=json.loads(self.save_path.read_text(encoding='utf-8'))
            data['assembly']=self.hub.facility.state
            temp=self.save_path.with_suffix('.tmp');temp.write_text(json.dumps(data,indent=2),encoding='utf-8');temp.replace(self.save_path)
            self.message='Mission saved locally.'
        except (OSError,ValueError) as e: self.message='Save failed: '+str(e)
        self.open()
    def load(self):
        if self.crew_action('load'):return
        try:
            self.hub.read_cards=self.campaign.load(self.save_path,self.hub.design_session)
            self.hub.spacecraft.apply(self.hub.design_session.design); self.hub.refresh_resources()
            self.hub.facility.solo.restore(json.loads(self.save_path.read_text(encoding='utf-8')).get('assembly'),self.hub.design_session)
            self.campaign.changed()
            self.message='Saved mission restored. Resubmit contributions for fresh integration approval.'
        except (OSError,ValueError,KeyError,TypeError,StopIteration) as e: self.message='Load failed: '+str(e)
        self.open()
    def reset(self):
        if self.crew_action('new'):return
        from game.domain.assembly import Assembly
        self.hub.facility.solo=Assembly()
        self.campaign=Campaign(); self.hub.design_session.reset(); self.hub.design_changed()
        self.message='New mission started. Learning cards remain accessible.'; self.open()

    def launch(self):
        if self.crew_action('launch'):return
        session=self.hub.design_session
        if not self.hub.facility.state['ready'] or math.hypot(self.hub.pose.x-76,self.hub.pose.z-6.5)>3.2:
            self.message='Complete integration approval and approach the launch-readiness console.';self.open();return
        if self.campaign.stage<4 or self.campaign.approved!=asdict(session.design):
            self.message='Pass readiness for this exact configuration first.'; self.open(); return
        design=session.design; targeted=self.targeted; mode=self.mode
        self.pending_campaign=self.campaign
        def work():
            rows,provenance,meta=trajectory(design.orbit,mode=='live')
            result=simulate(session.catalog,design,rows,targeted)
            result.update(provenance=provenance,input_hash=meta['input_hash'],plan='targeted' if targeted else 'continuous')
            result['design']=asdict(design)
            return result
        self.future=self.pool.submit(work)
        self.message='Preparing trajectory... The game stays responsive. Failure will be shown without a hidden fallback.'
        self.open()

    def tick(self,dt):
        if self.future is not None and self.future.done():
            future=self.future; self.future=None
            try:
                result=future.result()
                if (self.campaign is not self.pending_campaign or self.campaign.stage<4
                    or self.campaign.approved!=result['design']
                    or result['design']!=asdict(self.hub.design_session.design)):
                    raise ValueError('Mission or design changed during orbit preparation. Rerun readiness.')
                self.start_flight(result)
            except Exception as e:
                self.message='Orbit preparation failed: '+str(e)+'. Choose Cached explicitly or fix GMAT and retry.'
                self.open()
        if self.flight is None: return
        f=self.flight; f['elapsed']+=dt; t=f['elapsed']
        if t<7:
            self.telemetry.text=f'LAUNCH GALLERY / T-{max(0,3-int(t))}\n'+('Liftoff!' if t>3 else 'Readiness approved. Spectators in position.')
            self.rocket.y=max(0,t-3)**2
        else:
            self.rocket.enabled=False; self.earth.enabled=True; self.sat.enabled=True
            for person in self.people: person.enabled=False
            frames=f['result']['frames']; index=min(len(frames)-1,int((t-7)*15)); row=frames[index]
            x,y,z=row['position']; self.sat.position=(100+x/6378*2,z/6378*2+2,y/6378*2)
            from ursina import Vec3
            station=Vec3(100+2*math.cos(7.292115e-5*row['t']),2,2*math.sin(7.292115e-5*row['t']))
            self.station.position=station
            self.station.enabled=True
            self.beam.enabled=row['contact']
            self.beam.position=(self.sat.position+station)/2
            self.beam.look_at(station)
            self.beam.scale=(.02,.02,(self.sat.position-station).length())
            self.telemetry.text=(f"{f['result']['provenance']} / {row['t']/60:.0f} simulated min\n"
                                 f"Battery {row['battery_wh']:.1f} Wh | Storage {row['storage_mb']:.0f} MB\n"
                                 f"Delivered {row['delivered_mb']:.0f}/60 MB | "
                                 f"{'ECLIPSE' if row['eclipse'] else 'SUNLIGHT'} | {'CONTACT' if row['contact'] else 'NO CONTACT'}")
            if index==len(frames)-1: self.finish_flight()

    def start_flight(self,result):
        h=self.hub
        if h.panel: h.close_panel()
        h.panel_base('flight','LAUNCH & OPERATIONS','A short cinematic, then trajectory-driven telemetry. Skip goes to the calculated result.')
        self.flight={'result':result,'elapsed':0}
        self.world=Entity(parent=scene)
        self.rocket=Entity(parent=self.world,model='cube',position=(100,0,0),scale=(.4,2,.4),color=color.white)
        Entity(parent=self.rocket,model='sphere',y=.6,scale=(1,.35,1),color=color.red)
        for side in (-1,1): Entity(parent=self.rocket,model='cube',position=(side*.7,-.35,0),scale=(.7,.25,.2),color=color.red)
        Entity(parent=self.rocket,model='sphere',y=-.65,scale=(.6,.7,.6),color=AMBER)
        self.earth=Entity(parent=self.world,model='sphere',position=(100,2,0),scale=4,color=color.azure,shader=basic_lighting_shader,enabled=False)
        self.sat=Entity(parent=self.world,model='cube',scale=.15,color=AMBER,enabled=False)
        self.station=Entity(parent=self.world,model='sphere',scale=.08,color=CYAN,enabled=False)
        self.beam=Entity(parent=self.world,model='cube',color=CYAN,enabled=False)
        self.orbit_dots=[]
        for row in result['frames'][:105:2]:
            x,y,z=row['position']
            self.orbit_dots.append(Entity(parent=self.world,model='sphere',position=(100+x/6378*2,z/6378*2+2,y/6378*2),scale=.025,color=CYAN))
        self.people=[Entity(parent=self.world,model='cube',position=(98+i*.8,-.5,-2),scale=(.2,.6,.2),color=CYAN) for i in range(6)]
        # Keep the center transparent so the launch/orbit world remains visible.
        h.panel_dim.enabled=False
        h.panel_background.enabled=False
        h.hud.enabled=False
        self.telemetry=Text('',parent=h.panel,position=(-.65,-.15,-.04),scale=.85,color=CYAN)
        Button('SKIP TO RESULT',parent=h.panel,position=(0,-.34,-.05),scale=(.5,.06),text_size=.8,on_click=self.finish_flight)
        camera.position=(100,3,-11); camera.look_at((100,2,0))

    def finish_flight(self):
        if self.flight is None:return
        result=self.flight['result']; self.flight=None; destroy(self.world)
        self.hub.hud.enabled=True
        summary={k:v for k,v in result.items() if k!='frames'}
        values=self.hub.design_session.preview.values
        summary.update(cost_eur=values['cost_eur'],mass_kg=values['mass_kg'],quality=values['quality'])
        c=self.campaign
        network=getattr(self.hub,'network',None)
        if network is not None and network.active:
            network.send('finished',flight_id=network.seen_flight)
        else:
            c.previous_result=c.last_result; c.last_result=summary
            if result['passed']: c.stage=5
        (ROOT/'runtime/mission-report.json').write_text(json.dumps(summary,indent=2))
        h=self.hub
        if h.panel: h.close_panel()
        h.panel_base('report','MISSION SUCCESS' if result['passed'] else 'MISSION NEEDS REVISION',result['provenance'])
        previous=c.previous_result
        text=(f"Useful data delivered: {result['delivered_mb']:.0f} / 60 MB\n"
              f"Storage loss: {result['lost_mb']:.0f} MB\nUnserved energy: {result['unserved_wh']:.2f} Wh\n\n"
              f"Design: {values['mass_kg']:g} kg / {eur(values['cost_eur'])} / science grade {values['quality']}\n\n"
              + '\n'.join(textwrap.wrap(result['reason'],74))
              + (f"\n\nPrevious attempt: {previous['delivered_mb']:.0f} MB delivered." if previous else '')
              + '\n\nReport saved locally. Press M after closing to review or retry.')
        Text(text,parent=h.panel,position=(-.63,.20,-.04),scale=.85)
