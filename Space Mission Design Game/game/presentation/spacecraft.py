"""Procedural spacecraft shared by the design bay and its panel preview."""
from ursina import Entity, color
from ursina.shaders import basic_lighting_shader


class Spacecraft:
    def __init__(self, parent, position=(0,0,0), scale=1):
        self.root = Entity(parent=parent, position=position, scale=scale, rotation=(12,-25,0))
        self.part((0,0,0),(.8,.65,.6),color.rgb32(198,215,224))
        self.part((0,.36,0),(.65,.1,.5),color.rgb32(193,148,63))
        self.arrays=[]
        for side in (-1,1):
            self.part((side*.57,0,0),(.4,.06,.06),color.light_gray)
            wing=self.part((side*.95,0,0),(.75,.045,.9),color.rgb32(28,92,161))
            for z in (-.3,0,.3):
                Entity(parent=wing, model='cube', position=(0,-.57,z),scale=(.94,.1,.012),color=color.rgb32(80,169,221))
            self.arrays.append((side,wing))
        self.sensor=self.part((0,-.1,-.42),(.35,.35,.25),color.rgb32(53,177,188),'sphere')
        self.radio=self.part((.3,.52,.1),(.35,.12,.35),color.rgb32(229,235,243),'sphere')

    def part(self, position, scale, tint, model='cube'):
        return Entity(parent=self.root,model=model,position=position,scale=scale,color=tint,shader=basic_lighting_shader)

    def apply(self, design):
        extended=design.power=='extended'
        for side,wing in self.arrays:
            wing.x=side*(1.15 if extended else .95)
            wing.scale=(1.15 if extended else .75,.045,1.2 if extended else .9)
        advanced=design.sensor=='advanced'
        self.sensor.scale=(.52,.52,.35) if advanced else (.35,.35,.25)
        self.sensor.color=color.rgb32(255,190,89) if advanced else color.rgb32(53,177,188)
        self.radio.scale=(.55,.16,.55) if design.radio=='fast' else (.35,.12,.35)
