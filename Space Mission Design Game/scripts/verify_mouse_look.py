"""Scripted graphical mouse input/context checks; no desktop input injection."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from panda3d.core import loadPrcFileData
loadPrcFileData('','audio-library-name null\nnotify-level-device error')
from ursina import Ursina,mouse,Vec3,application,camera
from game.presentation.hub import Hub

app=Ursina(size=(1280,800),borderless=False,development_mode=False,editor_ui_enabled=False)
h=Hub()
# This harness injects Ursina velocity to exercise the legacy path on any OS.
# Native pointer/focus/projection paths have verify_desktop_recovery.py instead.
if h.desktop_mouse:
    h.desktop_mouse.release();h.desktop_mouse=None;mouse.locked=True
def move(dx,dy):
    mouse.velocity=Vec3(dx,dy,0);h.tick(.016)
move(0,0);move(.1,.1)
assert abs(h.pose.yaw-12)<.001 and abs(h.pitch+12)<.001
assert abs(camera.rotation_x+12)<.001
h.open_library();pose,pitch=h.pose,h.pitch;move(.2,.2)
assert not mouse.locked and h.pose==pose and h.pitch==pitch
h.library.open_book(0,0);h.library.advance(.55);move(.2,.2)
assert h.library.state=='reading' and h.pose==pose and h.pitch==pitch
h.close_panel();assert mouse.locked
move(.3,.3);assert h.pose==pose and h.pitch==pitch
move(-.1,-.1);assert abs(h.pose.yaw)<.001 and abs(h.pitch)<.001
h.focused=False;move(.5,.5)
assert not mouse.locked and abs(h.pose.yaw)<.001
h.focused=True;move(.5,.5);move(.5,.5)
assert abs(h.pose.yaw)<.001
move(.1,0);assert abs(h.pose.yaw-12)<.001
h.open_pause();assert not mouse.locked
h.close_panel();mouse.velocity=Vec3(0,0,0)
print('PASS: both mouse axes, camera sync, library/book capture, cursor restore, focus loss and no recenter jump',flush=True)
mouse.locked=False
application.quit()
