"""Original Phase 1 renderer proof, retained independently from hub navigation."""
import math
from ursina import Entity, Text, DirectionalLight, AmbientLight, color, camera, application
from ursina.shaders import lit_with_shadows_shader


class EngineCheck:
    def __init__(self):
        self.elapsed=0.
        camera.position=(0,2,-13)
        camera.look_at((0,0,0))
        DirectionalLight(shadows=False).look_at((1,-1,1))
        AmbientLight(color=color.rgba(.3,.3,.4,1))
        self.earth=Entity(model='sphere',color=color.rgb32(27,111,181),scale=3,shader=lit_with_shadows_shader)
        for i in range(96):
            a=i*math.tau/96
            Entity(model='sphere',color=color.rgb32(50,206,216),scale=.025,position=(3.3*math.cos(a),.5*math.sin(a),3.3*math.sin(a)))
        self.satellite=Entity(model='cube',color=color.light_gray,scale=(.25,.2,.2))
        for x in (-.4,.4):
            Entity(parent=self.satellite,model='cube',color=color.rgb32(31,91,172),position=(x,0,0),scale=(2.3,.12,1.8))
        Text('MISSION FORGE',position=(-.75,.42),scale=2,color=color.rgb32(77,219,224))
        Text('PHASE 1 / ENGINE CHECK',position=(-.75,.34))
        Text('Standalone graphics proof\nGMAT runs separately. ESC closes this window.',position=(-.75,-.33),scale=.9)

    def tick(self,dt):
        self.elapsed+=dt
        self.earth.rotation_y+=dt*9
        a=self.elapsed*.5
        self.satellite.position=(3.3*math.cos(a),.5*math.sin(a),3.3*math.sin(a))

    def handle_input(self,key):
        if key=='escape': application.quit()

    def evidence(self):
        return {'scene':'phase1_engine_check'}
