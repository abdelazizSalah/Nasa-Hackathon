"""Component views extracted from the existing spacecraft; no second satellite model."""
from ursina import Entity, Text, color, destroy, Mesh
from game.presentation.spacecraft import Spacecraft
from game.presentation.materials import surface
from ursina.shaders import basic_lighting_shader
import math

def cylinder_mesh():
    """Capped tank mesh with explicit UVs/normals, without optional numpy."""
    vertices=[];normals=[];uvs=[]
    for i in range(16):
        a=i*math.tau/16;b=(i+1)*math.tau/16
        points=[(.5*math.cos(t),y,.5*math.sin(t)) for t,y in [(a,-.5),(a,.5),(b,.5),(b,-.5)]]
        for j in (0,1,2,0,2,3):
            x,y,z=points[j];vertices.append((x,y,z));normals.append((x*2,0,z*2));uvs.append(((i+(j>=2))/16,y+.5))
        for y,order in [(-.5,(a,b)),(.5,(b,a))]:
            for p in [(0,y,0)]+[(.5*math.cos(t),y,.5*math.sin(t)) for t in order]:
                vertices.append(p);normals.append((0,y*2,0));uvs.append((p[0]+.5,p[2]+.5))
    return Mesh(vertices=vertices,normals=normals,uvs=uvs)

CYLINDER=cylinder_mesh()

def stacked_inventory(state,player):
    inventory=list(state['inventory'].get(player,[]))
    base=state['carried'].get(player)
    return ([base]+[c for c in inventory if c!=base]) if base in inventory else inventory

class Part(Entity):
    def __init__(self,category,design,**kwargs):
        super().__init__(**kwargs)
        self.category=category
        def part(position,scale,tint,model='cube',texture=None,rotation=(0,0,0)):
            if model=='cylinder':model=CYLINDER
            return Entity(parent=self,model=model,position=position,scale=scale,color=tint,texture=texture,rotation=rotation,shader=basic_lighting_shader)
        if category=='sensor':
            advanced=design.sensor=='advanced';tint=color.orange if advanced else color.cyan
            part((0,0,0),(.62,.50,.45),tint,texture=surface('brushed-metal'))
            part((0,0,-.28),(.38,.38,.18),color.rgb32(15,30,50),'sphere')
            part((0,0,-.38),(.24,.24,.07),color.azure,'sphere')
            if advanced:part((.24,.18,-.24),(.12,.12,.12),color.yellow,'sphere')
        elif category=='power':
            craft=Spacecraft(self);craft.apply(design);craft.root.rotation=(0,0,0)
            for child in craft.root.children:child.enabled=False
            for _,wing in craft.arrays:
                wing.enabled=True;wing.texture=surface('solar-cells');wing.color=color.white
            part((0,0,0),(.45,.12,.4),color.orange,texture=surface('thermal-foil'))
        elif category=='radio':
            fast=design.radio=='fast';tint=color.violet if fast else color.azure
            part((0,-.16,0),(.50,.24,.38),tint,texture=surface('brushed-metal'))
            part((0,.06,0),(.08,.40,.08),color.light_gray,'cylinder')
            part((0,.25,0),(.65 if fast else .45,.15,.65 if fast else .45),color.white,'sphere',rotation=(45,0,0))
            part((0,.37,-.12),(.06,.20,.06),tint,'cylinder')
        elif category=='orbit':
            part((0,0,0),(.60,.60,.60),color.azure,'sphere')
            for i in range(28):
                a=i*math.tau/28
                part((.48*math.cos(a),.15*math.sin(a),.48*math.sin(a)),(.035,.035,.035),color.cyan,'sphere')
        elif category=='launcher':
            tint=color.orange if design.launcher=='heavy' else color.white
            part((0,-.05,0),(.30,.75,.30),tint,'cylinder',surface('brushed-metal'))
            part((0,.40,0),(.30,.30,.30),color.red,'sphere')
            for side in (-1,1):part((side*.23,-.3,0),(.22,.25,.12),color.red,rotation=(0,0,side*25))
        elif category=='fuel':
            liquid=design.fuel=='liquid'
            for x in ((-.18,.18) if liquid else (0,)):
                part((x,0,0),(.26 if liquid else .42,.70,.26 if liquid else .42),color.azure if liquid else color.orange,'cylinder',surface('brushed-metal'))
                part((x,.35,0),(.26 if liquid else .42,.13,.26 if liquid else .42),color.cyan if liquid else color.red,'sphere')
            if liquid:part((0,-.27,0),(.5,.07,.07),color.light_gray)


def set_carried(parent,categories,design,local=False):
    categories=[categories] if isinstance(categories,str) else list(categories or [])
    key=tuple((category,getattr(design,category)) for category in categories)
    if getattr(parent,'part_key',None)==key:return
    old=getattr(parent,'held_part',None)
    if old:old.enabled=False;destroy(old)
    parent.part_key=key;parent.held_part=None
    parent.held_parts=[]
    if categories:
        parent.held_part=Entity(parent=parent,position=(.43,-.30,.9) if local else (.45,.74,.28))
        size=(.17 if len(categories)<=3 else .12) if local else (.35 if len(categories)<=3 else .23)
        heights={'sensor':.55,'power':.14,'radio':.80,'orbit':.60,'launcher':1.10,'fuel':.85}
        y=0;previous_height=None
        for i,category in enumerate(categories):
            height=heights[category]*size
            if previous_height is not None:y+=(previous_height+height)/2+(.025 if local else .04)
            part=Part(category,design,parent=parent.held_part,y=y,scale=size,rotation=(0,-15,0))
            parent.held_parts.append(part)
            previous_height=height
        Entity(parent=parent.held_part,model='sphere',position=(0,-.04,0),scale=.055 if local else .13,color=color.light_gray)
