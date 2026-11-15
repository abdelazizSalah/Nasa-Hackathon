"""Rendered checks for E retrieval, red room screen, stacked inventory and EUR choices."""
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from panda3d.core import loadPrcFileData,Filename
loadPrcFileData('','audio-library-name null\nnotify-level-device error')
from ursina import Ursina,application,window,color
from game.presentation.hub import Hub
from game.domain.navigation import Pose
from game.domain.assembly import CATEGORIES
from game.domain.facility_layout import integration_target

app=Ursina(size=(1440,900),borderless=False,development_mode=False,editor_ui_enabled=False)
window.color=color.rgb32(6,12,25);h=Hub();f=h.facility
out=ROOT/'runtime/integration-revision';out.mkdir(parents=True,exist_ok=True);checks=[]
def close():
    if h.panel:h.close_panel()
def view(x,z,yaw=0):h.pose=Pose(x,z,yaw);h._sync_camera()
def shot(name):
    h.tick(0)
    for _ in range(3):app.taskMgr.step();app.graphicsEngine.render_frame()
    assert app.win.save_screenshot(Filename.from_os_specific(str(out/f'{name}.png')))
def check(value,message):assert value,message;checks.append(message)

f.action('mission',mission='flood-watch');close()
for c in CATEGORIES:f.action('confirm',category=c)
h.tick(0);view(68,9.5);shot('01-five-parts-stack')
check(len(f.local_hand.held_parts)==len(CATEGORIES),'All six owned choices are visible in one vertical stack')
check(all(a.y<b.y for a,b in zip(f.local_hand.held_parts,f.local_hand.held_parts[1:])),'Carried parts occupy increasing, separate heights')
for c in CATEGORIES:
    x,z=integration_target(c);view(x,z-1);f.action('submit',category=c)
view(72,6.5);f.action('validate');check(f.state['ready'],'Initial integration approved')
view(70,7);h.handle_input('e');h.tick(0)
check('sensor' not in f.state['submitted'] and not f.state['ready'],'E retrieves a placed sensor and clears approval')
check(len(f.local_hand.held_parts)==1,'Retrieved sensor returns visibly to the carrying stack')
shot('02-retrieved-part');h.handle_input('e')
check('sensor' in f.state['submitted'],'Second E resubmits the retrieved part')
view(76,10.4);h.handle_input('e');check(h.modal=='submission','E opens the plan desk')
h.handle_input('e');check('orbit' not in f.state['submitted'],'E also retrieves the selected planning tablet')
h.handle_input('e');check('orbit' in f.state['submitted'],'E resubmits the selected planning tablet');close()
f.action('choose',category='sensor',option='advanced');close();view(68,9.5)
shot('03-red-engineering-screen')
check(f.integration_sign.color==color.rgb32(255,70,85),'Engineering failures turn the room display red')
check('REVISE / PEAK POWER' in f.integration_details.text,'Room screen includes actual failed requirements')
for c,o in [('power','extended'),('radio','fast'),('launcher','heavy')]:f.action('choose',category=c,option=o)
f.action('choose',category='orbit',option='wide');close();view(68,9.5);shot('04-over-budget-screen')
check(f.state['cost_eur']==150000 and f.state['budget_eur']==145000,'Mission budget and selected prices total correctly in EUR')
check('OVER BUDGET: €5,000' in f.integration_budget.text,'Room screen names the exact budget overrun')
f.action('confirm',category='sensor');check('budget' in f.message.lower(),'Overspend prevents collection')
f.open_station('orbit');shot('05-priced-orbit-choices');close()
(out/'report.json').write_text(json.dumps({'status':'passed','checks':checks,'method':'scripted Windows graphical checks; real Wi-Fi remains manual'},indent=2))
print(f'PASS: {len(checks)} integration revision checks; screenshots: {out}',flush=True)
application.quit()
