"""Native rendered resize/focus/cursor checks; Linux desktop policy exercised on this host."""
from pathlib import Path
import sys,json
from types import SimpleNamespace
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from panda3d.core import loadPrcFileData,Filename,WindowProperties
loadPrcFileData('','load-display pandagl\naudio-library-name null\nnotify-level-device error')
from ursina import Ursina,window,camera,application,held_keys,mouse
from game.presentation.hub import Hub
from game.presentation.desktop import DesktopDisplay

app=Ursina(size=(1280,720),fullscreen=False,borderless=False,development_mode=False,editor_ui_enabled=False)
h=Hub(mouse_mode='warp');display=DesktopDisplay(app,window,camera,linux=True)
# Drive the same client-pixel API deterministically without moving the user's OS cursor.
class PointerFeed:
    def __init__(self,win):self.win=win;self.point=(win.get_x_size()//2,win.get_y_size()//2)
    def get_pointer(self,index):return SimpleNamespace(get_x=lambda:self.point[0],get_y=lambda:self.point[1])
    def move_pointer(self,index,x,y):self.point=(x,y);return True
    def __getattr__(self,name):return getattr(self.win,name)
feed=PointerFeed(app.win);h.desktop_mouse.win=feed
out=ROOT/'runtime/desktop-recovery';out.mkdir(parents=True,exist_ok=True);checks=[]
def frame(name=None):
    for _ in range(4):h.tick(.016);display.update();app.taskMgr.step();app.graphicsEngine.render_frame()
    if name:app.win.save_screenshot(Filename.from_os_specific(str(out/f'{name}.png')))
def check(value,name):assert value,name;checks.append(name)
try:
    frame('01-normal-window')
    center=(app.win.get_x_size()//2,app.win.get_y_size()//2)
    old_yaw=h.pose.yaw;old_pitch=h.pitch
    feed.point=(center[0]+40,center[1]-20);h.tick(.016)
    check(h.pose.yaw!=old_yaw and h.pitch<old_pitch,'Controlled client-pixel displacement turns actual Hub camera on both axes')
    h.set_focus(False);pose,pitch=h.pose,h.pitch;held_keys['w']=1;frame()
    check(h.pose==pose and h.pitch==pitch and not h.desktop_mouse.active,'Focus loss releases capture and freezes movement')
    held_keys['w']=0;h.set_focus(True);frame('02-click-to-resume')
    check(h.pose==pose and h.pitch==pitch and h._focus_click_required,'Focus return waits for click and ignores stale motion')
    h.handle_input('left mouse down');frame()
    check(not h._focus_click_required and h.desktop_mouse.active,'Click resumes native mouse capture')
    h.open_pause();frame();check(not h.desktop_mouse.active,'Menus release cursor for UI interaction')
    h.close_panel();frame()
    vfov=[]
    for name,size in [('standard',(1280,720)),('ultrawide',(2560,974)),('square',(900,900))]:
        window.size=size;frame('03-'+name);vfov.append(camera.lens.get_vfov())
        check(abs(camera.lens.get_aspect_ratio()-app.win.get_x_size()/app.win.get_y_size())<.001,'Projection matches actual '+name+' client dimensions')
    check(max(vfov)-min(vfov)<.001,'Vertical field of view stays stable instead of zooming on wide VM displays')
    display.toggle();frame('04-desktop-sized');check(not app.win.get_properties().get_fullscreen(),'Desktop-sized mode keeps native exclusive fullscreen disabled')
    display.toggle();frame('05-restored');check(not app.win.get_properties().get_undecorated(),'Returning from desktop mode restores the title bar')
    (out/'report.json').write_text(json.dumps({'status':'passed','host':sys.platform,'checks':checks,
        'limits':'Controlled pointer samples/focus transitions and native host rendering; physical GNOME/VM mouse and Alt-Tab still require Ubuntu acceptance.'},indent=2))
    print('PASS:', '; '.join(checks),flush=True)
finally:
    h.release_mouse();mouse.locked=False
application.quit()
