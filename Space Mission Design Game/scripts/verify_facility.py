"""Graphical single-player acceptance: real UI/domain actions and traversal."""
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from panda3d.core import loadPrcFileData,Filename
loadPrcFileData('','audio-library-name null\nnotify-level-device error')
from ursina import Ursina,application,held_keys,window,color
from game.presentation.hub import Hub
from game.domain.navigation import Pose
from game.domain.assembly import CATEGORIES
from game.domain.facility_layout import station_position,integration_target

app=Ursina(size=(1440,900),borderless=False,development_mode=False,editor_ui_enabled=False)
window.color=color.rgb32(6,12,25)
h=Hub();f=h.facility;out=ROOT/'runtime/facility-review';out.mkdir(parents=True,exist_ok=True)
checks=[]
def check(value,name):
    assert value,name
    checks.append(name)
def shot(name):
    h.tick(0)
    for _ in range(3):app.taskMgr.step();app.graphicsEngine.render_frame()
    assert app.win.save_screenshot(Filename.from_os_specific(str(out/f'{name}.png')))
def place(x,z,yaw=0):h.pose=Pose(x,z,yaw);h.locomotion.y=0;h.locomotion.velocity=0;h.locomotion.grounded=True;h._sync_camera()
def close():
    if h.panel:h.close_panel()
def walk(frames):
    held_keys['w']=1
    for _ in range(frames):h.tick(.03)
    held_keys['w']=0

shot('01-spawn')
f.open_missions();shot('02-mission-select')
f.action('mission',mission='coming-soon');check(f.state['mission'] is None,'Future mission rejected')
f.action('mission',mission='flood-watch');check(f.state['mission']=='flood-watch','Existing Flood Watch selected')
close();place(6,9,90);walk(70);check(h.pose.x>11,'Approved Library doorway and first workshop are traversable')
place(16,7.7);shot('03-payload-room');f.open_station('sensor');shot('04-station')
f.action('choose',category='sensor',option='advanced');f.action('confirm',category='sensor');close();h.tick(.03)
check(f.local_hand.held_part is not None,'Confirmed physical component visible in hand')
shot('05-carried-payload')
for c in CATEGORIES[1:]:
    x,z=station_position(c,'engineer',f.players);place(x,z-1)
    f.open_station(c);f.action('confirm',category=c);close()
check(len(f.state['confirmed'])==len(CATEGORIES),'Single player confirms all four roles and six choices')
place(35.5,9,90);walk(20);check(h.pose.x<36.2,'Raised crossing blocks walking')
h.handle_input('space');walk(35);check(h.pose.x>37.9,'Jump crosses raised cable passage')
for _ in range(40):h.tick(.03)
check(h.locomotion.y==0,'Gravity returns player to floor')
place(49.5,9,90);walk(20);check(h.pose.x<50.3,'Low beam blocks standing player')
held_keys['left alt']=1;walk(16);held_keys['left alt']=0;h.tick(.03)
check(h.locomotion.crouch,'Cannot stand up while under beam')
held_keys['left alt']=1;walk(35);held_keys['left alt']=0;h.tick(.03)
check(h.pose.x>52 and not h.locomotion.crouch,'Crouch passage clears and standing restores')
place(72,6.5);shot('06-integration')
for c in CATEGORIES:
    x,z=integration_target(c);place(x,z-1);f.action('submit',category=c)
check(len(f.state['submitted'])==len(CATEGORIES),'Every component and all three plan choices submit once')
place(72,6.5);f.open_validation();f.action('validate');check(not f.state['ready'],'Invalid selected design fails original checks')
shot('07-validation-failed');close()
for c,o in [('power','extended'),('radio','fast'),('launcher','heavy')]:
    x,z=station_position(c,'engineer',f.players);place(x,z-1)
    f.open_station(c);f.action('choose',category=c,option=o);f.action('confirm',category=c);close()
    x,z=integration_target(c);place(x,z-1);f.action('submit',category=c)
place(72,6.5);f.open_validation();f.action('validate')
check(f.state['ready'] and h.mission.campaign.stage==4,'Correction, resubmission and validation approve exact design')
shot('08-validation-approved');close();place(72,6.0);shot('09-complete-satellite')
angle=h.spacecraft.root.rotation_y;h.tick(.1)
check(h.spacecraft.root.rotation_y>angle,'Original spacecraft keeps original eight-degree/second rotation')
place(76,6.5);h.mission.launch();h.mission.future.result(timeout=30);h.mission.tick(0)
check(h.mission.flight is not None,'Approved design enters original trajectory and launch workflow')
h.mission.finish_flight();check(h.mission.campaign.stage==5,'Original mission delivery result succeeds')
shot('10-mission-result');close()
place(-5,7.3);f.open_help();shot('11-controls');close()
h.open_library();book=h.library;book.open_book(0,0);book.advance(.55)
before=h.locomotion.y;h.handle_input('space');h.tick(.03)
check(h.locomotion.y==before and book.state=='reading','Library captures controls without movement interference')
h.close_panel();shot('12-library-preserved')
(out/'report.json').write_text(json.dumps({'status':'passed','checks':checks,'method':'scripted graphical acceptance on Windows; physical Wi-Fi remains manual'},indent=2))
print(f'PASS: {len(checks)} facility graphical checks; evidence: {out}',flush=True)
application.quit()
