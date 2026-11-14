"""Connected workshops and integration UI around existing mission/design services."""
from dataclasses import asdict
import json
import math
import textwrap
from ursina import Entity, Text, Button, color, destroy, camera, scene
from game.domain.assembly import Assembly, ROLES, CATEGORIES, assignments, owned, missions
from game.domain.facility_layout import ROOMS, station_position, integration_target
from game.domain.locomotion import Volume
from game.domain.navigation import Obstacle
from game.presentation.carried import Part, set_carried

CYAN=color.rgb32(64,216,222)
AMBER=color.rgb32(255,190,89)
MUTED=color.rgb32(155,180,199)

class Facility:
    def __init__(self,hub):
        self.hub=hub;self.solo=Assembly();self.shared=None;self.signature=None;self.table_obstacles=[]
        self.tables=Entity();self.placements=Entity();self.local_hand=Entity(parent=camera)
        self.volumes=[];self.elapsed=0;self.detail_category='sensor';self.feedback_page=0;self.message=''
        self.build()
        self.refresh_world()

    @property
    def player(self):return self.hub.network.role if self.hub.network.active else 'engineer'
    @property
    def players(self):return self.hub.network.players if self.hub.network.active else {'engineer':{'name':'You'}}
    @property
    def state(self):
        return self.shared if self.hub.network.active and self.shared else self.solo.snapshot(self.hub.design_session,self.players)
    def can(self,category):return category in owned(self.player,self.players)
    def host(self):return not self.hub.network.active or self.player=='engineer'
    def flight_owner(self):return 'flight' in assignments(self.players).get(self.player,[])
    def stage_owner(self):
        stage=self.hub.mission.campaign.stage
        if stage==3:return 'engineer'
        role='flight' if stage in (0,2) else 'science'
        return next((p for p,rs in assignments(self.players).items() if role in rs),None)

    def label(self,text,position,size=.09,tint=CYAN,parent=None):
        return Text(text,parent=parent if parent is not None else scene,position=position,scale=size*40,color=tint,origin=(0,0),rotation_y=0)

    def build(self):
        h=self.hub
        # The original orbit display and all original spawn-room geometry stay in place.
        screen=h.box((-5.55,1.65,-.92),(1.5,1.0,.10),color.rgb32(15,47,64),shader=False,collider='box')
        screen.on_click=lambda:self.open_missions() if h.modal is None and math.hypot(h.pose.x+5.55,h.pose.z+.92)<3 else None
        self.mission_sign=self.label('MISSION SELECT\nFlood Watch / available',(-5.55,1.85,-.99),.068)
        self.label('Mission 02 / COMING SOON',(-5.55,1.45,-.99),.052,MUTED)
        h.targets.append(('mission-select',(-5.55,0,-1.8)))
        h.box((8,-.15,9),(2,.3,3.4))
        for z in (7.3,10.7):h.box((8,2,z),(2,4,.2),solid=True)
        for title,x,categories in (*ROOMS,('Satellite Integration',72,())):
            h.box((x,-.15,9),(14,.3,10),color.rgb32(19,31,45))
            for z in (4,14):h.box((x,2,z),(14,4,.25),solid=True)
            for boundary in (x-7,):
                for z,depth in ((5.6,3.2),(12.4,3.2)):h.box((boundary,2,z),(.25,4,depth),solid=True)
                h.box((boundary,3.7,9),(.25,.6,3.4))
                for z in (7.3,10.7):h.box((boundary-.16,1.7,z),(.05,3.4,.06),CYAN,shader=False)
            self.label(title.upper(),(x,3.25,13.82),.16)
            self.label('BACK / SELECT / CONFIGURE / COLLECT / NEXT: INTEGRATE',(x,2.83,13.80),.069,MUTED)
            for xx in range(x-6,x+7,2):h.box((xx,.012,9),(.6,.02,.08),CYAN,shader=False)
            for xx in range(x-6,x+7,2):
                h.box((xx,.006,9),(.018,.01,9.6),color.rgb32(34,53,67),shader=False)
            for zz in range(5,14,2):
                h.box((x,.008,zz),(13.6,.01,.018),color.rgb32(34,53,67),shader=False)
            for xx in (x-6.6,x+6.6):
                h.box((xx,2,13.8),(.14,3.8,.14),color.rgb32(40,66,83))
                h.box((xx,2.8,13.67),(.025,1.2,.025),CYAN,shader=False)
            h.box((x,3.9,9),(8,.06,.12),CYAN,shader=False)
            self.volumes.append(Volume(x,9,14,10,4,4.3))
        h.box((79,2,9),(.25,4,10),solid=True)
        # Both traversal features fit the connecting apertures; walking never bypasses validation.
        h.box((37,.225,9),(1.2,.45,3.4),color.rgb32(207,143,59))
        self.volumes.append(Volume(37,9,1.2,3.4,0,.45))
        self.label('RAISED CABLE CROSSING / SPACE TO JUMP',(34,1.2,13.78),.085,AMBER)
        h.box((51,2.55,9),(1.0,2.9,3.4),color.rgb32(125,107,52))
        self.volumes.append(Volume(51,9,1,3.4,1.1,4))
        self.label('LOW SERVICE PASSAGE / HOLD ALT',(48,1.2,13.78),.085,AMBER)
        h.box((72,.6,9),(6,1.2,2),solid=True)
        h.box((72,1.22,9),(6.1,.06,2.1),color.rgb32(24,83,96),shader=False)
        h.spacecraft.root.position=(72,2.55,9) # Same object, scale, styling and Hub rotation.
        for category in ('sensor','power','radio'):
            x,z=integration_target(category)
            h.box((x,1.27,z+.35),(1.35,.035,.6),color.rgb32(47,82,95),shader=False)
            self.label(category.upper(),(x,1.05,z-.02),.075)
            h.targets.append(('place:'+category,(x,0,z-1)))
        h.box((76,.55,11.5),(1.8,1.1,1),solid=True)
        self.label('MISSION PLAN\nORBIT + LAUNCHER',(76,1.5,11.1),.08)
        h.targets.append(('plan-submit',(76,0,10.4)))
        self.integration_sign=self.label('',(72,2.2,13.8),.10)
        h.targets.append(('validate',(72,0,6.5)))
        h.targets.append(('launch-console',(76,0,6.5)))
        self.label('E / HOST VALIDATION',(72,.5,7.92),.095)
        h.box((76,.55,5.2),(1.8,1.1,1),solid=True)
        self.label('LAUNCH READINESS\nE / MISSION CONTROL',(76,1.5,5.1),.08)
        self.help=Entity(model='sphere',position=(-5,1.7,8.3),scale=.4,color=CYAN,collider='sphere')
        Text('?',parent=self.help,position=(0,0,-.6),origin=(0,0),scale=20,color=color.white)
        self.help.on_click=lambda:self.open_help() if h.modal is None and math.hypot(h.pose.x+5,h.pose.z-8.3)<3 else None
        h.targets.append(('controls-help',(-5,0,8.3)))

    def receive(self,data):self.shared=data;self.signature=None

    def changed(self):
        if not self.hub.network.active:self.solo.changed(self.hub.design_session)
        self.signature=None

    def action(self,action,**fields):
        h=self.hub
        self.message=''
        if h.network.active:h.network.send(action,**fields);return
        s=h.design_session;c=fields.get('category')
        try:
            if action=='mission':self.solo.select_mission(fields['mission']);h.read_cards.add('purpose')
            elif action=='choose':
                if s.choose(c,fields['option']):h.design_changed()
            elif action=='confirm':self.solo.confirm(s,c,self.player)
            elif action=='carry':self.solo.carry(s,self.player,self.players,c)
            elif action=='submit':self.solo.submit(s,c,self.player,self.players)
            elif action=='validate':
                if self.solo.validate(s,self.players):
                    while h.mission.campaign.stage<4:
                        old=h.mission.campaign.stage
                        h.mission.campaign.advance(s,h.read_cards)
                        if old==h.mission.campaign.stage:break
            self.signature=None
            self.refresh_modal()
        except ValueError as exc:
            h.toast(str(exc));self.message=str(exc);self.refresh_modal()

    def refresh_world(self):
        state=self.state;h=self.hub;s=h.design_session
        destroy(self.tables);self.tables=Entity();self.table_obstacles=[]
        for title,center,categories in ROOMS:
            for player,p in self.players.items():
                x,z=station_position(categories[0],player,self.players)
                active=bool(set(categories)&owned(player,self.players))
                Entity(parent=self.tables,model='cube',position=(x,.5,z),scale=(2.3,1,1.2),color=color.rgb32(35,57,73))
                self.table_obstacles.append(Obstacle(x,z,2.3,1.2))
                ready=all(state['confirmed'].get(c)==getattr(s.design,c) for c in categories)
                tint=CYAN if active and ready else AMBER if active else MUTED
                Entity(parent=self.tables,model='cube',position=(x,1.04,z),scale=(2.4,.06,1.25),color=color.rgb32(24,80,91) if active else color.rgb32(44,53,60))
                roles=', '.join(ROLES[r][0] for r in assignments(self.players)[player])
                lines=f'{player} / {p["name"]}\n'+' / '.join(assignments(self.players)[player])+'\n'+ (' / '.join(categories) if active else 'Observe / other workshops')
                lines+='\n'+ ('CONFIRMED' if ready and active else 'AWAITING CONFIRMATION' if active else 'INFORMATION ONLY')
                self.label(lines,(x,1.6,z-.65),.065,tint,self.tables)
                if active:
                    for i,c in enumerate(categories):
                        Part(c,s.design,parent=self.tables,position=(x+(.4*i),1.18,z),scale=.27)
                    self.label('Choices: '+' / '.join(getattr(s.design,c) for c in categories),(x,.73,z-.66),.055,MUTED,self.tables)
        destroy(self.placements);self.placements=Entity()
        for c,item in state['submitted'].items():
            x,z=integration_target(c)
            if c in ('orbit','launcher'):x+=-.4 if c=='orbit' else .4
            part=Part(c,s.design,parent=self.placements,position=(x,1.6,z+.35),scale=.4)
            part.destination_y=1.2 if c in ('orbit','launcher') else 1.45
            self.label(c+' / '+item['by'],(x,1.65,z+.1),.05,CYAN,self.placements)
        ready_roles=sum(all(c in state['submitted'] for c in cs) for _,cs in ROLES.values())
        waiting=[r for r,(_,cs) in ROLES.items() if not all(c in state['submitted'] for c in cs)]
        self.integration_sign.text=f'{ready_roles} OF 4 ENGINEERING ROLES SUBMITTED\n'+('SPACECRAFT DESIGN APPROVED' if state['ready'] else 'Waiting: '+', '.join(waiting) if waiting else 'READY FOR HOST VALIDATION')
        self.mission_sign.text='MISSION SELECT\n'+('Flood Watch / SELECTED' if state['mission'] else 'Flood Watch / available')

    def tick(self,dt):
        self.elapsed+=dt;self.help.y=1.7+.07*math.sin(self.elapsed*1.6)
        state=self.state
        signature=json.dumps((state,asdict(self.hub.design_session.design),{p:v['name'] for p,v in self.players.items()}),sort_keys=True)
        if signature!=self.signature:self.signature=signature;self.refresh_world()
        category=state['carried'].get(self.player)
        set_carried(self.local_hand,category,self.hub.design_session.design,True)
        self.local_hand.enabled=self.hub.modal is None
        for part in self.placements.children:
            if hasattr(part,'destination_y'):part.y=max(part.destination_y,part.y-dt*.5)
        if self.hub.modal is None:
            nearby=self.nearby()
            if nearby:self.hub.prompt.text='E / '+self.hint(nearby)
        if self.hub.mission.campaign.stage<5:
            missing=[c for c in CATEGORIES if c not in state['confirmed']]
            if not state['mission']:message='SELECT / Use the mission screen beside the Earth display'
            elif missing:
                title,_,_=next(room for room in ROOMS if missing[0] in room[2])
                message='CONFIGURE / '+title+' / Confirm '+missing[0]+' at its assigned workstation'
            elif len(state['submitted'])<5:message=f'INTEGRATE / {len(state["submitted"])}/5 contributions submitted / I opens your carried inventory'
            elif not state['ready']:message='VALIDATE / Approach the central integration console / host approval required'
            else:message='APPROVED / Walk to Launch Readiness and launch with the flight engineer'
            self.hub.task.text=message

    def nearby(self):
        h=self.hub
        for _,_,categories in ROOMS:
            for player in self.players:
                x,z=station_position(categories[0],player,self.players)
                if math.hypot(h.pose.x-x,h.pose.z-z)<2.5:return 'station:'+player+':'+categories[0]
        target=h.nearby()
        return target if target in ('mission-select','controls-help','validate','plan-submit','launch-console') or (target or '').startswith('place:') else None

    def hint(self,target):
        if target.startswith('station:'):return 'Inspect workstation / '+target.split(':')[1]
        if target.startswith('place:'):return 'Place '+target.split(':')[1]
        return {'mission-select':'Select mission','controls-help':'Controls / SPACE jump / ALT crouch','validate':'Integration and host validation',
                'plan-submit':'Submit orbit / launcher plan','launch-console':'Launch & Mission Control'}[target]

    def interact(self,target):
        if target.startswith('station:'):
            _,player,category=target.split(':');self.open_station(category,player)
        elif target.startswith('place:'):
            category=target.split(':')[1];self.action('submit',category=category)
        elif target=='plan-submit':self.open_submission()
        elif target=='mission-select':self.open_missions()
        elif target=='controls-help':self.open_help()
        elif target=='validate':self.open_validation()
        elif target=='launch-console':self.hub.mission.open()

    def panel(self,kind,title,subtitle):
        if self.hub.panel:self.hub.close_panel()
        self.hub.panel_base(kind,title,subtitle)
        if self.message:self.txt(self.message,-.64,-.38,.60,AMBER,width=115)
        return self.hub.panel
    def txt(self,text,x,y,size=.75,tint=color.white,width=95):
        return Text('\n'.join(textwrap.wrap(text,width)),parent=self.hub.panel,position=(x,y,-.05),scale=size,color=tint)
    def btn(self,label,x,y,width,fn,disabled=False):
        return Button(label,parent=self.hub.panel,position=(x,y,-.06),scale=(width,.05),text_size=.65,color=color.rgb32(28,80,94) if not disabled else color.rgb32(47,51,59),
                      disabled=disabled,**({'on_click':fn} if not disabled else {}))

    def open_missions(self):
        self.panel('missions','MISSION SELECT','Choose Flood Watch to begin / only the host selects the shared crew mission')
        for i,m in enumerate(missions()):
            y=.20-i*.23;self.txt(m['name']+(' / SELECTED' if self.state['mission']==m['id'] else ''),-.64,y,1,CYAN if m['available'] else MUTED)
            self.txt(m['description'],-.64,y-.055,.76,MUTED)
            self.btn('SELECT MISSION' if m['available'] else 'COMING SOON',.40,y-.13,.42,lambda mid=m['id']:self.action('mission',mission=mid),not m['available'] or not self.host())

    def open_directory(self):
        self.panel('directory','ENGINEERING WORKSHOP DIRECTORY','Walk through the Learning Lab right-hand doorway to the connected engineering wing.')
        for i,(title,x,categories) in enumerate(ROOMS):
            self.txt(f'{i+1}. {title} / '+', '.join(categories),-.63,.20-i*.085,.9,CYAN)
        self.txt('Then: Satellite Integration > Host Validation > Launch Readiness.\nSPACE jumps the raised crossing; hold ALT under the service beam.',-.63,-.18,.78,MUTED)

    def open_station(self,category,player=None):
        self.detail_category=category;self.station_player=player or self.player
        self.panel('workshop','ENGINEERING WORKSTATION',self.station_player+' / '+', '.join(ROLES[r][0] for r in assignments(self.players).get(self.station_player,[])))
        s=self.hub.design_session;cat=next(c for c in s.catalog['categories'] if c['id']==category)
        self.txt(cat['label'].upper(),-.64,.24,1,CYAN)
        allowed=self.station_player==self.player and self.can(category) and not self.hub.network.busy
        for i,option in enumerate(cat['options']):
            x=-.63+i*.65;chosen=option['id']==getattr(s.design,category)
            self.txt(option['name']+(' / SELECTED' if chosen else ''),x,.17,.88,CYAN if chosen else color.white,width=41)
            self.txt(option['description'],x,.10,.73,MUTED,width=46)
            specs=' / '.join(f'{k.replace("_"," ")}: {v}' for k,v in option.items() if k not in ('id','label','name','description'))
            self.txt(specs,x,-.015,.67,color.white,width=49)
            self.btn('SELECT '+option['label'].upper(),x+.27,-.16,.52,lambda c=category,o=option['id']:self.action('choose',category=c,option=o),not allowed)
        self.btn('CONFIRM & COLLECT',-.30,-.26,.60,lambda:self.action('confirm',category=category),not allowed)
        if category in ('orbit','launcher'):
            other='launcher' if category=='orbit' else 'orbit'
            self.btn('VIEW '+other.upper(),.36,-.26,.50,lambda:self.open_station(other,self.station_player))
        state=self.state;status='Confirmed / carry to integration' if state['confirmed'].get(category)==getattr(s.design,category) else 'Awaiting explicit confirmation'
        self.txt(status+' / Return through earlier rooms at any time.',-.64,-.34,.66,MUTED)

    def open_submission(self):
        self.panel('submission','MISSION PLAN SUBMISSION','Orbit and launcher are planning choices, not hardware inside the satellite.')
        for i,c in enumerate(('orbit','launcher')):
            self.txt(c.upper()+' / '+getattr(self.hub.design_session.design,c),-.63,.20-i*.18,.95,CYAN)
            self.btn('SUBMIT '+c.upper(),.35,.14-i*.18,.52,lambda category=c:self.action('submit',category=category),not self.can(c) or c in self.state['submitted'])
        self.txt('Each contribution is tied to the current confirmed selection.',-.63,-.27,.75,MUTED)

    def open_validation(self,page=0):
        self.feedback_page=page
        self.panel('validation','SATELLITE INTEGRATION / VALIDATION','Engineering checks / host approval / return to the workshops to revise and resubmit')
        state=self.state
        reports=sorted(state['validation'],key=lambda r:r['passed'])
        failures=sum(not r['passed'] for r in reports)
        title='SPACECRAFT DESIGN APPROVED' if state['ready'] else f'VALIDATION NEEDS REVISION / {failures} failed checks' if failures else f'{len(state["submitted"])}/5 choices submitted / host validation required'
        self.txt(title,-.63,.235,1,CYAN if not failures else AMBER)
        if reports:
            report=reports[page%len(reports)]
            self.txt(('PASS / ' if report['passed'] else 'REVISE / ')+report['label'],-.63,.17,.95,CYAN if report['passed'] else AMBER)
            self.txt(report['explanation'],-.63,.105,.80,color.white,width=100)
            self.txt('Responsible roles: '+', '.join(ROLES[r][0] for r in report['roles']),-.63,.015,.72,MUTED,width=102)
            self.txt('Current owners: '+', '.join(report['players'])+' / Stations: '+', '.join(report['categories']),-.63,-.055,.71,MUTED)
            self.txt(report['advice'],-.63,-.115,.77,AMBER,width=100)
            self.btn('PREV CHECK',-.43,-.20,.30,lambda:self.open_validation(page-1))
            self.btn('NEXT CHECK',-.05,-.20,.30,lambda:self.open_validation(page+1))
        else:
            self.txt('Submit payload, power and radio at their marked locations. Submit orbit and launcher at the mission-plan station. Every role must contribute before validation.',-.63,.12,.86,MUTED,width=95)
        self.btn('RUN HOST VALIDATION',-.34,-.29,.60,lambda:self.action('validate'),not self.host() or len(state['submitted'])<5 or self.hub.network.busy)
        self.btn('MISSION CONTROL',.34,-.29,.60,self.hub.mission.open,not state['ready'])

    def open_help(self):
        self.panel('controls','FLIGHT DECK CONTROLS','Keyboard navigation / mouse stays free for books and consoles')
        lines=['[ W / S ]  Walk forward / backward','[ A / D ]  Strafe left / right','[ LEFT / RIGHT ARROWS ]  Turn camera left / right',
               '[ SPACE ]  Jump (grounded only)','[ LEFT / RIGHT ALT ]  Hold to crouch','[ E ]  Use a nearby door, station or placement location',
               '[ I ]  Open carried-parts inventory','[ LEFT MOUSE ]  Select covers and interface buttons',
               '[ M ]  Mission tablet    [ N ]  LAN crew','[ ESC ]  Close menu / book / pause; mouse remains free']
        for i,line in enumerate(lines):self.txt(line,-.63,.23-i*.05,.76,CYAN if i in (3,4) else color.white)

    def open_inventory(self):
        self.panel('inventory','CARRIED PARTS / YOUR ROLES',self.player+' / '+', '.join(ROLES[r][0] for r in assignments(self.players).get(self.player,[])))
        inventory=self.state['inventory'].get(self.player,[])
        for i,c in enumerate(inventory):
            self.txt(c.upper()+' / '+getattr(self.hub.design_session.design,c),-.63,.2-i*.09,.85,CYAN)
            self.btn('CARRY',.42,.19-i*.09,.28,lambda category=c:self.action('carry',category=category))
        if not inventory:self.txt('No unsubmitted confirmed parts. Confirm choices at your assigned workshop.',-.63,.16,.8,MUTED)

    def refresh_modal(self):
        modal=self.hub.modal
        if modal=='workshop':self.open_station(self.detail_category,self.station_player)
        elif modal=='validation':self.open_validation(self.feedback_page)
        elif modal=='missions':self.open_missions()
        elif modal=='submission':self.open_submission()
        elif modal=='inventory':self.open_inventory()
