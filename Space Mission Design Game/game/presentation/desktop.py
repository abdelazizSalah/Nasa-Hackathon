"""Desktop-safe Linux window sizing, resize-aware projection and native mouse fallback."""
import math
from panda3d.core import WindowProperties

def startup_window(platform,windowed=False,fullscreen=False):
    # A normal titled window remains discoverable in GNOME/VM task switching.
    desktop=platform.startswith('linux')
    full=fullscreen or (not windowed and not desktop)
    return {'size':(1280,720) if desktop or windowed else None,
            'fullscreen':full and not desktop,'borderless':full and not desktop}

def projection(width,height):
    aspect=max(1,width)/max(1,height)
    vertical=2*math.atan(math.tan(math.radians(75)/2)/(16/9))
    horizontal=2*math.atan(math.tan(vertical/2)*aspect)
    return math.degrees(horizontal),math.degrees(vertical)

class DesktopDisplay:
    def __init__(self,app,window,camera,linux=False):
        self.app=app;self.window=window;self.camera=camera;self.linux=linux
        self.fullscreen=bool(window.fullscreen) if not linux else False
        self.restore=None;self.previous_size=None
    def toggle(self):self.set_fullscreen(not self.fullscreen)
    def set_fullscreen(self,value):
        if value==self.fullscreen:return
        if not self.linux:
            self.window.fullscreen=value
        else:
            # Desktop-sized window: no exclusive mode, XRandR switch or override-redirect.
            p=WindowProperties();p.set_fullscreen(False);p.set_undecorated(value)
            if value:
                current=self.app.win.get_properties()
                self.restore=(current.get_x_size(),current.get_y_size(),current.get_x_origin(),current.get_y_origin())
                monitor=self.window.main_monitor
                width=int(monitor.width) if monitor else self.app.pipe.get_display_width()
                height=int(monitor.height) if monitor else self.app.pipe.get_display_height()
                p.set_size(max(640,width),max(480,height))
                p.set_origin(int(monitor.x) if monitor else 0,int(monitor.y) if monitor else 0)
            elif self.restore:
                w,h,x,y=self.restore;p.set_size(w,h);p.set_origin(x,y)
            self.app.win.request_properties(p)
        self.fullscreen=value
    def update(self):
        size=(self.app.win.get_x_size(),self.app.win.get_y_size())
        if min(size)<=0 or size==self.previous_size:return
        self.previous_size=size
        self.camera.lens.set_aspect_ratio(size[0]/size[1])
        self.camera.lens.set_fov(*projection(*size))

class PointerCapture:
    """Try native relative input, then actual-client-pixel recentering, then right-drag."""
    def __init__(self,win,requested='auto'):
        self.win=win;self.requested=requested;self.active=False;self.mode=None
        self.previous=None;self.size=None;self.relative_available=None
    def properties(self,mode,hidden):
        p=WindowProperties();p.set_mouse_mode(mode);p.set_cursor_hidden(hidden)
        self.win.request_properties(p)
    def release(self):
        if self.active:self.properties(WindowProperties.M_absolute,False)
        self.active=False;self.mode=None;self.previous=None;self.size=None
    def sample(self,dragging=False):
        if not self.active:
            self.active=True;self.previous=None
            self.mode=('warp' if self.relative_available is False else 'relative-pending') if self.requested=='auto' else self.requested
            self.properties(WindowProperties.M_relative if self.mode=='relative-pending' else WindowProperties.M_absolute,self.mode!='drag')
            return 0,0
        pointer=self.win.get_pointer(0);point=(pointer.get_x(),pointer.get_y())
        size=(self.win.get_x_size(),self.win.get_y_size())
        if min(size)<=0:return 0,0
        center=(size[0]//2,size[1]//2)
        if self.mode=='relative-pending':
            if self.win.get_properties().get_mouse_mode()==WindowProperties.M_relative:
                self.mode='relative';self.previous=point
                self.relative_available=True
            else:
                self.relative_available=False
                self.mode='warp';self.properties(WindowProperties.M_absolute,True)
                if not self.win.move_pointer(0,*center):
                    self.mode='drag';self.properties(WindowProperties.M_absolute,False)
                self.previous=None
            self.size=size;return 0,0
        if size!=self.size:
            self.size=size;self.previous=point
            if self.mode=='warp':self.win.move_pointer(0,*center)
            return 0,0
        if self.mode=='drag' and not dragging:
            self.previous=None;return 0,0
        if self.mode=='warp':
            dx,dy=point[0]-center[0],point[1]-center[1]
            if not self.win.move_pointer(0,*center):
                self.mode='drag';self.properties(WindowProperties.M_absolute,False);self.previous=None
                return 0,0
        else:
            previous=self.previous;self.previous=point
            if previous is None:return 0,0
            dx,dy=point[0]-previous[0],point[1]-previous[1]
        # Discard stale warps/large jumps from focus or monitor transitions.
        if abs(dx)>size[0]*.45 or abs(dy)>size[1]*.45:return 0,0
        return dx/size[1],-dy/size[1]
