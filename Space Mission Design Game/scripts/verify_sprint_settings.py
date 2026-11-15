"""Render Settings and exercise the actual Shift speed, persistence and collision."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from panda3d.core import loadPrcFileData,Filename
loadPrcFileData('','audio-library-name null\nnotify-level-device error')
from ursina import Ursina,application,held_keys,window,mouse
from game.presentation.hub import Hub
from game.domain.navigation import Pose,Obstacle,advance

app=Ursina(size=(1280,800),borderless=False,development_mode=False,editor_ui_enabled=False)
settings=ROOT/'runtime/player_settings.json'
backup=settings.read_bytes() if settings.exists() else None
out=ROOT/'runtime/sprint-settings';out.mkdir(parents=True,exist_ok=True)
h=Hub()
def frame(name):
    for _ in range(5):h.tick(.016);app.taskMgr.step();app.graphicsEngine.render_frame()
    app.win.save_screenshot(Filename.from_os_specific(str(out/(name+'.png'))))

try:
    h.open_pause();frame('01-pause-entry')
    h.open_settings();h.sprint_slider.value=60
    assert h.sprint_speed==60
    frame('02-turbo')
    window.size=(900,900);frame('03-narrow')
    h.close_panel()
    assert '60' in settings.read_text()
    h.sprint_speed=5.4;h.open_settings()
    h.sprint_slider.value=60;h.close_panel()
    # Actual Hub movement at maximum; use a clear segment of the wing walkway.
    h.pose=Pose(20,9,90);held_keys['w']=held_keys['shift']=1
    h.tick(.1);assert abs(h.pose.x-26)<.001
    held_keys['shift']=0;h.tick(.1);assert abs(h.pose.x-26.3)<.001
    held_keys['w']=0
    # A thin blocker remains solid even when a frame spans several metres.
    p=advance(Pose(0,0),1,0,.1,[Obstacle(0,1,3,.1)],speed=60)
    assert p.z<.7,p
    h.open_settings();h.sprint_slider.value=5.4
    assert h.sprint_speed==5.4
    frame('04-default');h.close_panel()
    print('PASS: Settings UI, 60 m/s maximum, 20x actual Shift speed, walking unchanged, narrow resize, saved preference, reset, no wall tunneling',flush=True)
finally:
    held_keys['w']=held_keys['shift']=0
    if backup is None:settings.unlink(missing_ok=True)
    else:settings.write_bytes(backup)
    mouse.locked=False;application.quit()
