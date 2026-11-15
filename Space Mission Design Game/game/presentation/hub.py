"""Walkable hub, Learning Lab, and reversible spacecraft design console."""
import json
import math
from pathlib import Path
import random
import textwrap
import webbrowser

from ursina import (Entity, Text, Button, DirectionalLight, AmbientLight, camera,
                    color, held_keys, mouse, application, scene, destroy)
from ursina.shaders import unlit_shader
from ursina.prefabs.slider import Slider
from game.domain.navigation import Pose, Obstacle, advance
from game.domain.look import mouse_look
from game.presentation.responsive import ResponsivePanel
from game.presentation.materials import surface
from game.presentation.material_lighting import material_shader
from game.presentation.planet import earth
from game.domain.design import DesignSession
from game.domain.economy import eur
from game.presentation.spacecraft import Spacecraft
from game.presentation.design_panel import DesignPanel

from game.paths import ROOT,RUNTIME
CYAN = color.rgb32(64, 216, 222)
WHITE = color.rgb32(226, 237, 246)
MUTED = color.rgb32(151, 176, 198)
NAVY = color.rgb32(12, 23, 39)
AMBER = color.rgb32(255, 190, 89)


class Hub:
    def __init__(self):
        self.cards = json.loads((ROOT / 'content/learning_cards.json').read_text(encoding='utf-8'))['cards']
        self.settings_path=RUNTIME/'player_settings.json'
        self.sprint_speed=5.4
        try:
            value=float(json.loads(self.settings_path.read_text(encoding='utf-8'))['sprint_speed'])
            if math.isfinite(value):self.sprint_speed=max(3,min(60,value))
        except (OSError,ValueError,TypeError,KeyError):pass
        self.pose = Pose()
        from game.domain.locomotion import Locomotion
        self.locomotion=Locomotion()
        self.pitch = 0.
        self._look_ready=False
        self.spawn_help_pending=False
        self.focused = True
        self.elapsed = 0.
        self.frames = 0
        self.obstacles = []
        self.door_open = False
        self.door_progress = 0.
        self.modal = None
        self.panel = None
        self.card_index = 0
        self.read_cards = set()
        self.notice = ''
        self.notice_until = 0
        self.events = []
        self.targets = []
        self.design_session = DesignSession()
        self.design_panel = None
        from game.presentation.mission import MissionUI
        self.mission=MissionUI(self)
        self._world()
        self._hud()
        from game.presentation.crew import Crew
        self.network=Crew(self)
        from game.presentation.facility import Facility
        self.facility=Facility(self)
        camera.fov = 75
        mouse.locked = True
        self._sync_camera()

    def show_spawn_instructions(self):
        self.facility.open_help(welcome=True)

    def box(self, position, scale, tint=color.rgb32(38,55,72), solid=False, shader=True, **kwargs):
        if shader and 'texture' not in kwargs:
            material='deck-plate' if position[1]<0 and scale[1]<.5 else 'wall-panels' if scale[1]>2 and max(scale[0],scale[2])>2 else 'equipment-panel'
            kwargs['texture']=surface(material)
        entity = Entity(model='cube', position=position, scale=scale, color=tint,
                        shader=material_shader if shader else unlit_shader, **kwargs)
        if shader and min(scale)>.05:entity.texture_scale=(max(1,max(scale[0],scale[2])/2),max(1,scale[1]/2))
        if solid:
            self.obstacles.append(Obstacle(position[0], position[2], scale[0], scale[2]))
        return entity

    def label(self, text, position, scale=.8, tint=WHITE, **kwargs):
        return Text(text, parent=scene, position=position, scale=scale*40, color=tint,
                    origin=(0,0), **kwargs)

    def _world(self):
        AmbientLight(color=color.rgba(.55, .6, .72, 1))
        DirectionalLight(shadows=False).look_at((1, -2, 1))
        self.box((0,-.15,3.5), (14,.3,21), color.rgb32(19,31,45))
        for z in range(-6,15,2):
            self.box((0,.008,z), (13.7,.012,.025), color.rgb32(37,59,76), shader=False)
        for x in range(-6,7,2):
            self.box((x,.008,3.5), (.025,.012,20.7), color.rgb32(37,59,76), shader=False)
        for x in (-7,7):
            if x==7:
                # Approved narrow Library exit; the original spawn-side wall is identical.
                self.box((x,2,.15),(.35,4,14.3),solid=True)
                self.box((x,2,12.35),(.35,4,3.3),solid=True)
                self.box((x,3.7,9),(.35,.6,3.4))
            else:self.box((x,2,3.5), (.35,4,21), solid=True)
            self.box((x * .97,.1,3.5), (.04,.045,20.5), CYAN, shader=False)
            for z in (-5,1,7,13):
                self.box((x*.96,2,z), (.18,4,.2), color.rgb32(38,60,78))
        for z in (-7,14):
            self.box((0,2,z), (14,4,.35), solid=True)
        for x in (-4.3,4.3):
            self.box((x,2,5), (5.4,4,.35), solid=True)
        self.box((0,3.7,5), (3.3,.6,.35))
        for x in (-1.72,1.72):
            self.box((x,1.6,4.76), (.15,3.2,.1), CYAN, shader=False)
        self.box((0,3.25,4.76), (3.6,.13,.1), CYAN, shader=False)
        self.door = self.box((0,1.6,5), (3.2,3.2,.24), color.rgb32(39,70,87))
        # Door decoration follows the sliding leaf, rather than remaining in the opening.
        for entity_x in (-.2,.2):
            Entity(parent=self.door, model='cube', position=(entity_x,0,-.53), scale=(.008,.8,.02), color=CYAN)
        self.label('LEARNING LAB', (0,3.47,4.68), .23, CYAN)
        self.label('01 / OPEN THE DOOR  -  EXPLORE THE IDEAS', (0,3.03,4.7), .08)
        for z in (-3,-1,1,3,6.5,8.5,10.5):
            self.box((0,.018,z), (.12,.014,.7), CYAN, shader=False)
        for z in (-5,2,9,13):
            self.box((0,3.95,z), (13.8,.08,.25), color.rgb32(39,61,79))
            self.box((0,3.89,z), (6,.02,.06), CYAN, shader=False)

        # Hub's hologram and base; the walkway stays clear.
        self.box((-3.8,.4,.2), (2.5,.8,2.5), solid=True)
        self.box((-3.8,.82,.2), (2.4,.04,2.4), CYAN, shader=False)
        self.earth = earth(position=(-3.8,2,.2), scale=1.9)
        for i in range(72):
            a = i * math.tau/72
            Entity(model='sphere', position=(-3.8+1.5*math.cos(a),2+.25*math.sin(a),.2+1.5*math.sin(a)), scale=.025,color=CYAN)
        self.label('EARTH OBSERVATION', (-3.8,1.1,-1.09), .12, CYAN)
        self.label('OUR MISSION: USEFUL FLOOD DATA', (-3.8,.55,-1.09), .075)

        self.box((4.2,.6,.8), (3,1.2,1.6), solid=True)
        self.box((4.2,1.3,1.05), (2.8,.8,.12), color.rgb32(18,53,68))
        self.label('SPACECRAFT DESIGN', (4.2,1.45,.95), .13, CYAN)
        self.label('E / CONFIGURE SPACECRAFT', (4.2,1.1,.95), .08, MUTED)
        self.spacecraft=Spacecraft(scene,position=(4.2,2.55,.8),scale=.65)
        self.spacecraft.apply(self.design_session.design)
        self.targets.append(('design',(4.2,0,-.3)))

        from game.library.view import world_shelves
        world_shelves(self)
        self.box((0,.6,10.5), (2.7,1.2,1.0), solid=True)
        self.box((0,1.22,10.5), (2.6,.05,.95), color.rgb32(18,70,85), shader=False)
        self.box((0,1.25,10.02), (2.4,.025,.025), CYAN, shader=False)
        self.label('E / OPEN BOOK LIBRARY', (0,.85,9.97), .12, CYAN)
        self.targets.append(('library',(0,0,9.5)))
        self.label('LEARN  >  DESIGN  >  VERIFY', (0,2.7,-6.78), .19, CYAN, rotation_y=180)
        self.label('W/S MOVE   A/D STRAFE   MOUSE LOOK   SHIFT RUN   E USE', (0,2.2,-6.77), .11, rotation_y=180)
        rng=random.Random(17)
        for _ in range(70):
            Entity(model='sphere', position=(rng.uniform(-35,35),rng.uniform(6,22),rng.uniform(-25,35)), scale=rng.uniform(.02,.06), color=MUTED)

    def _hud(self):
        self.hud = ResponsivePanel(parent=camera.ui,width=1.6)
        Entity(parent=self.hud, model='quad', position=(0,.40), scale=(1.6,.20), color=color.rgba32(5,13,24,240))
        Text('MISSION FORGE', parent=self.hud, position=(-.76,.475), scale=1.05, color=CYAN)
        self.location = Text('MISSION CONTROL', parent=self.hud, position=(.38,.465), scale=.7, color=MUTED)
        self.task = Text('EXPLORE / Open the Learning Lab ahead', parent=self.hud, position=(-.76,.425), scale=.72)
        Entity(parent=self.hud, model='quad', y=-.445, scale=(1.6,.11), color=color.rgba32(5,13,24,235))
        Text('W/S  Walk   A/D  Strafe   Mouse  Look   SHIFT Run   SPACE Jump   ALT Crouch   E  Use   I  Parts   N  Crew', parent=self.hud,
             position=(-.76,-.422), scale=.69, color=MUTED)
        self.progress=Text('',parent=self.hud,position=(-.76,.35),scale=.60,color=WHITE)
        self.resources=Text('',parent=self.hud,position=(-.76,-.463),scale=.58,color=CYAN)
        self.refresh_resources()
        self.prompt = Text('', parent=self.hud, origin=(0,0), position=(0,-.355), scale=.9, color=CYAN)
        self.reticle = Text('+', parent=self.hud, origin=(0,0), position=(0,0), scale=.65,color=CYAN)

    def _sync_camera(self):
        camera.position=(self.pose.x,self.locomotion.eye,self.pose.z)
        camera.rotation=(self.pitch,self.pose.yaw,0)

    def _update_mouse_look(self):
        if self.modal is not None or not self.focused:
            if mouse.locked:mouse.locked=False
            self._look_ready=False
            return
        if not mouse.locked:
            mouse.locked=True
            self._look_ready=False
            return
        if not self._look_ready:
            # Ignore recentering/old cursor motion when returning from UI or Alt-Tab.
            self._look_ready=True
            return
        self.pose,self.pitch=mouse_look(self.pose,self.pitch,mouse.velocity.x,mouse.velocity.y)

    def nearby(self):
        candidates = [('door',(0,0,5)),*self.targets]
        fx, fz = math.sin(math.radians(self.pose.yaw)), math.cos(math.radians(self.pose.yaw))
        result=[]
        for name,(x,_,z) in candidates:
            dx,dz=x-self.pose.x,z-self.pose.z
            distance=math.hypot(dx,dz)
            if distance<2.45 and (distance<.6 or (dx*fx+dz*fz)/distance>0.25):
                result.append((distance,name))
        return min(result)[1] if result else None

    def tick(self, dt):
        self.network.tick(dt)
        self.mission.tick(dt)
        if self.mission.flight is not None: return
        self.elapsed += dt
        self.frames += 1
        self.earth.rotation_y += dt*8
        self.earth.clouds.rotation_y += dt*1.2
        self.spacecraft.root.rotation_y += dt*8
        if self.modal=='design' and self.design_panel is not None:
            self.design_panel.model.root.rotation_y += dt*12
        target = 1. if self.door_open else 0.
        self.door_progress += max(-dt*1.5,min(dt*1.5,target-self.door_progress))
        self.door.x = self.door_progress*3.5
        blockers = self.obstacles + ([Obstacle(0,5,3.2,.24)] if self.door_progress<.98 else [])
        frozen=self.modal is not None or not self.focused
        self._update_mouse_look()
        self.locomotion.tick(dt,self.pose,self.facility.volumes,
                             held_keys['left alt'] or held_keys['right alt'] or held_keys['alt'],frozen)
        blockers+=self.facility.table_obstacles+self.locomotion.blockers(self.facility.volumes)
        speed=.65 if self.locomotion.crouch else 1
        self.pose=advance(self.pose,(held_keys['w']-held_keys['s'])*speed,
                          held_keys['right arrow']-held_keys['left arrow'],dt,blockers,
                          frozen=self.modal is not None or not self.focused,
                          strafe=(held_keys['d']-held_keys['a'])*speed,
                          speed=self.sprint_speed if (held_keys['shift'] or held_keys['left shift'] or held_keys['right shift']) and not self.locomotion.crouch else 3)
        self._sync_camera()
        self.location.text = 'ENGINEERING WING' if self.pose.x>7 else 'LEARNING LAB' if self.pose.z>5.3 else 'MISSION CONTROL'
        if self.design_session.history:
            passed=sum(check.passed for check in self.design_session.preview.checks)
            self.task.text=f'DESIGN / {passed}/8 preview checks pass  |  Learn in the Lab or revise in the bay'
        else:
            self.task.text=f'EXPLORE / {len(self.read_cards)}/10 concepts opened  |  Design bay on your right'
        if self.mission.campaign.stage:
            stage=self.mission.campaign.stage
            self.task.text=f'MISSION / {min(stage+1,5)}/5  |  '+('Complete - M to review or retry' if stage==5 else 'M opens current objective and saves')
        self.reticle.enabled = self.modal is None
        if self.modal:
            self.prompt.text=''
        elif self.elapsed<self.notice_until:
            self.prompt.text=self.notice
        else:
            self.prompt.text={'door': 'E / Close Lab door' if self.door_open else 'E / Open Learning Lab',
                              'library':'E / Open aerospace books','design':'E / Engineering workshop directory'}.get(self.nearby(),'Learning Lab ahead / Spacecraft design bay on the right')

        self.facility.tick(dt)
        if self.spawn_help_pending:
            self.spawn_help_pending=False;self.facility.open_help(welcome=True)

    def toast(self,text):
        self.notice=text
        self.notice_until=self.elapsed+3

    def handle_input(self,key):
        if key=='n' and self.modal is None:
            self.network.open(); return
        if self.modal=='flight':
            if key in ('escape','enter'): self.mission.finish_flight()
            return
        if key=='m' and self.modal is None:
            self.mission.open(); return
        if self.modal == 'design':
            if key=='escape': self.close_panel()
            else: self.design_panel.handle_input(key)
            return
        if self.modal == 'learning':
            self.library.handle_input(key)
            return
        if self.modal=='submission' and key in ('e','left arrow','right arrow'):
            self.facility.handle_plan_input(key);return
        if self.modal:
            if key in ('escape','enter'): self.close_panel()
            return
        if key=='space':
            if self.focused:self.locomotion.jump()
        elif key=='i':self.facility.open_inventory()
        elif key=='escape':
            self.open_pause()
        elif key=='e':
            facility_target=self.facility.nearby()
            if facility_target:self.facility.interact(facility_target);return
            target=self.nearby()
            if target=='door':
                if self.network.active:
                    self.network.send('door'); return
                if self.door_open and abs(self.pose.z-5)<1 and abs(self.pose.x)<2:
                    self.toast('Step clear of the doorway before closing it.')
                    return
                self.door_open=not self.door_open
                self.events.append('door_opened' if self.door_open else 'door_closed')
            elif target=='library': self.open_library()
            elif target=='design': self.facility.open_directory()

    def panel_base(self,kind,title,subtitle):
        if self.panel is not None:self.close_panel()
        self.modal=kind
        self.hud.enabled=False
        mouse.locked=False
        self._look_ready=False
        self.panel=ResponsivePanel(parent=camera.ui)
        self.panel_dim=Entity(parent=self.panel, model='quad', scale=(4,3), z=.1, color=color.rgba32(2,7,14,215), collider='box')
        self.panel.dimmer=self.panel_dim
        self.panel_background=Entity(parent=self.panel, model='quad', scale=(1.46,.82), color=NAVY)
        Entity(parent=self.panel, model='quad', position=(0,.397,-.01), scale=(1.46,.012),color=CYAN)
        Text(title,parent=self.panel,position=(-.67,.365,-.02),scale=1.3,color=CYAN)
        Text(subtitle,parent=self.panel,position=(-.67,.31,-.02),scale=.73,color=MUTED)
        self.close_button = Button('CLOSE / ESC',parent=self.panel,position=(.57,.35,-.03),scale=(.22,.055),color=color.rgb32(31,59,77),text_size=.7,on_click=self.close_panel)

    def open_library(self):
        from game.library.view import LibraryController
        self.panel_base('learning','AEROSPACE FIELD LIBRARY','Choose a physical book / 12 volumes / offline lessons and original diagrams')
        self.library=LibraryController(self)
        self.close_button.on_click=self.library.exit
        self.select_card(self.card_index)
        self.events.append('library_opened')

    def select_card(self,index):
        self.card_index=index
        # Preserve the ten original concept receipts and their existing network protocol.
        # The two additional books never add campaign requirements or network messages.
        if 0 <= index < len(self.cards):
            card=self.cards[index]
            self.read_cards.add(card['id'])
            if self.network.active:self.network.send('read',card=card['id'])
            self.events.append('card:'+card['id'])
        self.library.select(index)

    def open_source(self):
        self.library.references(0)

    def open_pause(self):
        self.panel_base('pause','MISSION PAUSED','Explore the hub at your own pace.')
        Text('W / S          Walk forward and backward\nA / D          Step sideways\nMOUSE          Look in every direction\nLEFT / RIGHT   Optional keyboard turning\nSHIFT          Run\nSPACE          Jump / ALT: Crouch\nE              Open a nearby door or console\nESC            Close reading panels / pause\n\nThe mouse is free in menus; close this panel to look around.',parent=self.panel,
             position=(-.61,.20,-.04),scale=.95,color=WHITE)
        Button('RESUME / ENTER',parent=self.panel,position=(-.33,-.27,-.04),scale=(.55,.07),color=color.rgb32(26,96,110),text_size=.85,on_click=self.close_panel)
        Button('EXIT GAME',parent=self.panel,position=(.33,-.27,-.04),scale=(.55,.07),color=color.rgb32(52,61,76),text_size=.85,on_click=application.quit)
        Button('SETTINGS / RUN SPEED',parent=self.panel,position=(0,-.17,-.04),scale=(.70,.06),color=color.rgb32(26,96,110),text_size=.85,on_click=self.open_settings)

    def open_settings(self):
        self.panel_base('settings','SETTINGS','Personal controls / saved on this laptop')
        Text('SHIFT / RUN SPEED',parent=self.panel,position=(-.60,.20,-.04),scale=1.1,color=CYAN)
        value=Text('',parent=self.panel,position=(-.60,.135,-.04),scale=.95,color=WHITE)
        def change():
            self.sprint_speed=round(max(3,min(60,self.sprint_slider.value)),1)
            value.text=f'{self.sprint_speed:g} m/s  /  {self.sprint_speed/3:.1f}x walking speed'
        self.sprint_slider=Slider(min=3,max=60,default=self.sprint_speed,step=.1,dynamic=True,
                                 parent=self.panel,position=(-.55,.035,-.06),scale=2,
                                 height=.025,bar_color=color.rgb32(45,80,103),on_value_changed=change)
        self.sprint_slider.knob.color=CYAN
        change()
        Text('3 m/s / WALK',parent=self.panel,position=(-.55,-.055,-.04),scale=.7,color=MUTED)
        Text('60 m/s / TURBO',parent=self.panel,position=(.25,-.055,-.04),scale=.7,color=AMBER)
        Text('Hold Shift while moving to use this speed. Walking stays at 3 m/s.\nMaximum is 20x walking speed; walls and tables still block movement.\nYour choice is saved when you close Settings.',parent=self.panel,
             position=(-.60,-.13,-.04),scale=.73,color=WHITE)
        Button('RESET / 5.4 m/s',parent=self.panel,position=(-.33,-.29,-.04),scale=(.55,.07),color=color.rgb32(52,61,76),text_size=.85,
               on_click=lambda:setattr(self.sprint_slider,'value',5.4))
        Button('SAVE & RESUME',parent=self.panel,position=(.33,-.29,-.04),scale=(.55,.07),color=color.rgb32(26,96,110),text_size=.85,on_click=self.close_panel)

    def open_design(self):
        self.panel_base('design','SPACECRAFT DESIGN','Flood Watch / trade study / all numbers are teaching assumptions')
        self.design_panel=DesignPanel(self.panel,self.design_session,self.design_changed,
                                      self.network if self.network.active else None)
        self.events.append('design_opened')

    def design_changed(self):
        if hasattr(self,'facility'):self.facility.changed()
        self.mission.campaign.changed()
        self.spacecraft.apply(self.design_session.design)
        self.refresh_resources()
        self.events.append('design_changed')

    def refresh_resources(self):
        value=self.design_session.preview.values
        budget=self.design_session.catalog['scenario']['budget_eur']
        self.resources.text=(f"PREVIEW   Budget {eur(value['cost_eur'])}/{eur(budget)}   |   "
                             f"Mass {value['mass_kg']:g}/{value['launch_capacity_kg']:g} kg   |   "
                             f"Power margin {value['power_margin_w']:+g} W   |   "
                             f"Data {value['delivered_mb']:.0f}/{value['expected_data_mb']:.0f} MB")

    def close_panel(self):
        if self.mission.flight is not None:
            self.mission.finish_flight(); return
        if self.modal=='learning':self.library.dispose()
        if self.modal=='settings':
            try:
                self.settings_path.parent.mkdir(parents=True,exist_ok=True)
                self.settings_path.write_text(json.dumps({'sprint_speed':self.sprint_speed}),encoding='utf-8')
            except OSError:self.toast('Run speed applied for this session; settings could not be saved.')
        self.events.append('panel_closed')
        self.panel.enabled=False
        destroy(self.panel)
        self.panel=None
        self.modal=None
        self.hud.enabled=True
        self.design_panel=None
        mouse.locked=bool(self.focused)
        self._look_ready=False

    def evidence(self):
        from dataclasses import asdict
        return {'scene':'phase3_hub','player':{'x':self.pose.x,'z':self.pose.z,'yaw':self.pose.yaw},
                'door_open':self.door_open,'cards_opened':sorted(self.read_cards),'events':self.events[-100:],
                'design':asdict(self.design_session.design),'preview_passed':self.design_session.preview.passed}
