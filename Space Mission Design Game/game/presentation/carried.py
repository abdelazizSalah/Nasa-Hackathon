"""Component views extracted from the existing spacecraft; no second satellite model."""
from ursina import Entity, Text, color, destroy
from game.presentation.spacecraft import Spacecraft

class Part(Entity):
    def __init__(self,category,design,**kwargs):
        super().__init__(**kwargs)
        self.category=category
        if category in ('orbit','launcher'):
            Entity(parent=self,model='cube',scale=(.8,.12,.6),color=color.rgb32(33,94,117))
            Text(('ORBIT' if category=='orbit' else 'LAUNCH')+' PLAN',parent=self,position=(-.33,.08,-.27),rotation_x=90,scale=1.1,color=color.cyan)
        else:
            craft=Spacecraft(self);craft.apply(design);craft.root.rotation=(0,0,0)
            for child in craft.root.children:child.enabled=False
            if category=='sensor':craft.sensor.enabled=True;craft.sensor.position=(0,0,0)
            elif category=='radio':craft.radio.enabled=True;craft.radio.position=(0,0,0)
            else:
                # The same array geometry, sized by the actual selected power package.
                for _,wing in craft.arrays:wing.enabled=True

def set_carried(parent,category,design,local=False):
    key=(category,getattr(design,category)) if category else None
    if getattr(parent,'part_key',None)==key:return
    old=getattr(parent,'held_part',None)
    if old:old.enabled=False;destroy(old)
    parent.part_key=key;parent.held_part=None
    if category:
        parent.held_part=Part(category,design,parent=parent,position=(.43,-.30,.9) if local else (.45,.85,.28),
                              scale=.17 if local else .35,rotation=(0,-15,0))
        Entity(parent=parent.held_part,model='sphere',position=(0,-.22,0),scale=.25,color=color.light_gray)
