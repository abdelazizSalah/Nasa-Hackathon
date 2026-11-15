"""Resize/hitbox, live preview, one-click workflow and success-recipe graphics QA."""
import sys,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from panda3d.core import loadPrcFileData,Filename,CollisionTraverser,CollisionNode,CollisionHandlerQueue,CollisionRay
loadPrcFileData('','audio-library-name null\nnotify-level-device error')
from ursina import Ursina,Button,camera,window,application,mouse
from game.presentation.hub import Hub
from game.domain.assembly import CATEGORIES
from game.domain.navigation import Pose

app=Ursina(size=(1280,800),borderless=False,development_mode=False,editor_ui_enabled=False)
h=Hub();f=h.facility;out=ROOT/'runtime/workstation-upgrade';out.mkdir(parents=True,exist_ok=True);checks=[]
def frame(name=None):
    for _ in range(4):h.tick(.016);app.taskMgr.step();app.graphicsEngine.render_frame()
    if name:assert app.win.save_screenshot(Filename.from_os_specific(str(out/f'{name}.png')))
def descendants(root):
    for child in root.children:
        yield child
        yield from descendants(child)
def buttons():return [e for e in descendants(h.panel) if isinstance(e,Button)]
def click(label):
    button=next(b for b in buttons() if b.text==label)
    # Use the same lens and collision path as Ursina's mouse picker at the visual center.
    point=button.get_pos(camera.ui);ray=CollisionRay()
    ray.set_from_lens(camera._ui_lens_node,point.x*2/window.aspect_ratio,point.y*2)
    node=CollisionNode('ui-resize-check');node.addSolid(ray);node.set_into_collide_mask(0)
    path=h.panel.get_parent().get_parent().attach_new_node(node)
    path.reparent_to(__import__('ursina').scene.ui_camera)
    handler=CollisionHandlerQueue();traverser=CollisionTraverser();traverser.addCollider(path,handler);traverser.traverse(camera.ui)
    handler.sort_entries();assert handler.get_num_entries()>0,label
    hit=handler.get_entry(0).get_into_node_path().parent.getPythonTag('Entity');path.remove_node()
    assert hit==button,(label,hit)
    button.on_click();frame()
def close():
    if h.panel:h.close_panel()

h.show_spawn_instructions();frame('01-spawn-controls');assert h.modal=='controls' and not mouse.locked
click('START EXPLORING');assert h.modal is None
f.action('mission',mission='flood-watch');close()
for c in CATEGORIES:
    f.open_station(c)
    label=next(o['label'] for cat in h.design_session.catalog['categories'] if cat['id']==c for o in cat['options'] if o['id']==getattr(h.design_session.design,c))
    assert not any('CONFIRM' in b.text for b in buttons())
    click('SELECT & PICK '+label.upper());assert c in f.state['confirmed']
    before=f.preview.root.rotation_y;h.tick(.1);assert f.preview.root.rotation_y>before
    if c=='sensor':
        for i,size in enumerate(((1600,900),(900,900),(1280,720))):
            window.size=size;frame()
            click('SELECT & PICK BASIC');frame(f'02-resize-{i}')
        if sys.platform=='win32':
            import ctypes
            handle=app.win.get_window_handle().get_int_handle()
            ctypes.windll.user32.ShowWindow(handle,3)  # Native maximize, not a simulated aspect change.
            frame();click('SELECT & PICK BASIC');frame('02-native-maximized')
            ctypes.windll.user32.ShowWindow(handle,9);frame()
    frame('03-'+c);close()
checks+=['spawn instructions with usable start button','six one-click selections/collections','same rotating model in all workstation dialogs',
         'visual-center collision hits correct buttons after wide/narrow resize and dialog refresh']
f.open_station('fuel');click('SHOW CHECKS');frame('04-fuel-checks');close()
for c in CATEGORIES:
    f.action('submit',category=c)
f.action('validate');assert f.state['ready'];close()
h.pose=Pose(76,6.5,0);h.mission.mode='cached';h.mission.targeted=True
h.mission.launch();h.mission.future.result(timeout=30);h.mission.tick(0)
result=h.mission.flight['result'];assert result['passed'];h.mission.finish_flight();frame('05-success')
checks+=['all six contributions required and validated','documented default recipe succeeds using cached targeted simulation']
(out/'report.json').write_text(json.dumps({'status':'passed','checks':checks,'recipe_result':{k:v for k,v in result.items() if k!='frames'},
 'preview':h.design_session.preview.values},indent=2),encoding='utf-8')
print('PASS:', '; '.join(checks),flush=True)
mouse.locked=False;application.quit()
