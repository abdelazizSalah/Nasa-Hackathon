"""Fullscreen, navigation, themed room and one-click readiness/launch render checks."""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from panda3d.core import loadPrcFileData,Filename
loadPrcFileData('','audio-library-name null\nnotify-level-device error')
from ursina import Ursina,window,application,Button,held_keys,mouse,Vec3
from game.presentation.hub import Hub
from game.domain.navigation import Pose
from game.domain.assembly import CATEGORIES
from game.domain.facility_layout import station_position

app=Ursina(fullscreen=True,borderless=True,size=None,development_mode=False,editor_ui_enabled=False)
h=Hub();f=h.facility;out=ROOT/'runtime/clarity-upgrade';out.mkdir(parents=True,exist_ok=True);checks=[]
def check(value,name):assert value,name;checks.append(name)
def frame(name=None):
    mouse.velocity=Vec3(0,0,0)
    for _ in range(4):h.tick(.016);app.taskMgr.step();app.graphicsEngine.render_frame()
    if name:assert app.win.save_screenshot(Filename.from_os_specific(str(out/f'{name}.png')))
def pose(x,z,yaw=0):h.pose=Pose(x,z,yaw);h.pitch=0;h._sync_camera()
def close():
    if h.panel:h.close_panel()
def children(root):
    for c in root.children:yield c;yield from children(c)
def click(text,wait=True):
    b=next(c for c in children(h.panel) if isinstance(c,Button) and c.text==text)
    assert not b.disabled,text;b.on_click()
    if wait:frame()

h.show_spawn_instructions();frame('01-fullscreen-controls')
check(window.fullscreen and app.win.get_x_size()>=1280,'Game starts fullscreen')
click('START EXPLORING');check(h.hud.enabled,'HUD returns when modal closes')
check(len(f.table_obstacles)==6,'Six benches / one engineering category per bench')
check(abs(f.fuel_sign.rotation_y-180)<.1 and f.fuel_sign.z>6.2,'Fuel label faces the central walkway')
pose(12,8,90);held_keys['w']=1;h.tick(.1);walk=h.pose.x-12
pose(12,8,90);held_keys['shift']=1;h.tick(.1);run=h.pose.x-12
held_keys['w']=held_keys['shift']=0
check(abs(run/walk-h.sprint_speed/3)<.01,'Shift uses the configured run speed')
for name,x,z,yaw in [('payload',16,8,0),('power',30,8,0),('radio',44,8,0),('planning',58,9,0),('fuel-facing',58,9,180)]:
    pose(x,z,yaw);frame('02-'+name)
f.action('mission',mission='flood-watch')
for c in CATEGORIES:
    f.open_station(c)
    label=next(o['label'] for cat in h.design_session.catalog['categories'] if cat['id']==c for o in cat['options'] if o['id']==getattr(h.design_session.design,c))
    click('SELECT & PICK '+label.upper());frame('03-dialog-'+c);close()
check(h.design_session.preview.values['cost_eur']==91000,'Solid fuel is priced in the final EUR 91,000 total')
pose(68,9.5);frame('04-carried-shapes')
for c in CATEGORIES:f.action('submit',category=c)
frame('05-progress-to-approval')
pose(0,-4.5);h.mission.open();frame('06-clear-approval-action')
click('HOST: VALIDATE & APPROVE')
check(f.state['ready'] and h.mission.campaign.stage==4,'Readiness is approved directly from the explicit host button')
frame('07-green-launch')
click('LAUNCH NOW',wait=False);check(h.mission.future is not None,'Launch request immediately enters preparing state')
frame('08-visible-preparation')
if h.mission.future is not None:h.mission.future.result(timeout=30);h.mission.tick(0)
check(h.mission.flight is not None,'Launch automatically starts without another click or location restriction')
h.mission.finish_flight();frame('09-mission-result')
check(h.mission.campaign.stage==5,'New approval/launch flow retains successful science outcome')
close();frame('10-completed-progress')
check('15/15' in h.progress.text,'HUD visibly completes all progress milestones')
(out/'report.json').write_text(json.dumps({'status':'passed','checks':checks,'window_size':list(app.win.get_size()),
    'limits':'Scripted Windows rendering; separate physical laptops and Arch remain manual.'},indent=2),encoding='utf-8')
print('PASS:', '; '.join(checks),flush=True)
mouse.locked=False;application.quit()
