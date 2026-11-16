"""OS window policy, wide-screen projection and rejected native mouse requests."""
import unittest
from types import SimpleNamespace
from panda3d.core import WindowProperties
from game.presentation.desktop import startup_window,projection,PointerCapture,DesktopDisplay

class FakeWindow:
    def __init__(self,relative=False,warp=True):
        self.props=WindowProperties();self.props.set_size(1280,720);self.props.set_origin(30,40)
        self.props.set_mouse_mode(WindowProperties.M_absolute)
        self.relative=relative;self.warp=warp;self.point=(640,360);self.moves=[];self.requests=[]
    def get_x_size(self):return self.props.get_x_size()
    def get_y_size(self):return self.props.get_y_size()
    def get_properties(self):return self.props
    def request_properties(self,p):
        self.requests.append(p)
        # Emulate X11 rejecting M_relative when XF86-DGA is absent.
        if p.has_mouse_mode() and p.get_mouse_mode()==WindowProperties.M_relative and not self.relative:return
        self.props.add_properties(p)
    def get_pointer(self,i):return SimpleNamespace(get_x=lambda:self.point[0],get_y=lambda:self.point[1])
    def move_pointer(self,i,x,y):
        self.moves.append((x,y))
        if self.warp:self.point=(x,y)
        return self.warp

class DesktopTests(unittest.TestCase):
    def test_linux_default_is_titled_and_windows_fullscreen_is_preserved(self):
        self.assertEqual(startup_window('linux'),{'size':(1280,720),'fullscreen':False,'borderless':False})
        self.assertTrue(startup_window('win32')['fullscreen'])
        self.assertFalse(startup_window('win32',windowed=True)['fullscreen'])
        self.assertFalse(startup_window('linux',fullscreen=True)['fullscreen'])

    def test_ultrawide_projection_preserves_vertical_view(self):
        standard=projection(1600,900);wide=projection(2560,974);square=projection(900,900)
        self.assertAlmostEqual(standard[0],75)
        self.assertAlmostEqual(wide[1],standard[1]);self.assertAlmostEqual(square[1],standard[1])
        self.assertGreater(wide[0],standard[0])

    def test_unavailable_dga_falls_back_to_actual_client_pixel_center(self):
        win=FakeWindow();look=PointerCapture(win)
        self.assertEqual(look.sample(),(0,0));self.assertEqual(look.sample(),(0,0))
        self.assertEqual(look.mode,'warp');self.assertEqual(win.moves[-1],(640,360))
        win.point=(700,330);dx,dy=look.sample()
        self.assertAlmostEqual(dx,60/720);self.assertAlmostEqual(dy,30/720)
        self.assertEqual(win.point,(640,360))
        look.release();self.assertFalse(win.props.get_cursor_hidden())
        look.sample();self.assertEqual(look.mode,'warp')

    def test_relative_input_uses_displacement_without_recentering(self):
        win=FakeWindow(relative=True);look=PointerCapture(win)
        look.sample();look.sample();win.point=(650,350)
        dx,dy=look.sample();self.assertAlmostEqual(dx,10/720);self.assertAlmostEqual(dy,10/720)
        self.assertEqual(win.moves,[])

    def test_failed_warp_has_a_visible_right_drag_fallback(self):
        win=FakeWindow(warp=False);look=PointerCapture(win)
        look.sample();look.sample();self.assertEqual(look.mode,'drag')
        self.assertFalse(win.props.get_cursor_hidden())
        look.sample(dragging=False);win.point=(500,300);look.sample(dragging=True)
        win.point=(520,290);dx,dy=look.sample(dragging=True)
        self.assertAlmostEqual(dx,20/720);self.assertAlmostEqual(dy,10/720)
        self.assertEqual(look.sample(dragging=False),(0,0))

    def test_resize_and_focus_release_discard_stale_pointer_jumps(self):
        win=FakeWindow();look=PointerCapture(win,'warp');look.sample();look.sample()
        p=WindowProperties();p.set_size(2560,974);win.request_properties(p)
        win.point=(10,10);self.assertEqual(look.sample(),(0,0));self.assertEqual(win.moves[-1],(1280,487))
        look.release();win.point=(2100,600);self.assertEqual(look.sample(),(0,0));self.assertEqual(look.sample(),(0,0))

    def test_linux_desktop_fullscreen_never_requests_exclusive_mode(self):
        win=FakeWindow()
        monitor=SimpleNamespace(width=2560,height=974,x=0,y=0)
        controller=DesktopDisplay(SimpleNamespace(win=win),SimpleNamespace(main_monitor=monitor),None,linux=True)
        controller.toggle();self.assertFalse(win.props.get_fullscreen());self.assertTrue(win.props.get_undecorated())
        self.assertEqual((win.get_x_size(),win.get_y_size()),(2560,974))
        controller.toggle();self.assertFalse(win.props.get_undecorated())
        self.assertEqual((win.get_x_size(),win.get_y_size()),(1280,720))

if __name__=='__main__':unittest.main()
