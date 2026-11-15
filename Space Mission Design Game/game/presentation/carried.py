"""Component views extracted from the existing spacecraft; no second satellite model."""
from ursina import Entity, Text, color, destroy
from game.presentation.spacecraft import Spacecraft

def stacked_inventory(state,player):
    inventory=list(state['inventory'].get(player,[]))
    base=state['carried'].get(player)
    return ([base]+[c for c in inventory if c!=base]) if base in inventory else inventory

class Part(Entity):
    def __init__(self,category,design,**kwargs):
        super().__init__(**kwargs)
        self.category=category
        if category in ('orbit','launcher','fuel'):
            Entity(parent=self,model='cube',scale=(.8,.12,.6),color=color.rgb32(33,94,117))
            Text(('ORBIT' if category=='orbit' else 'FUEL: '+design.fuel.upper() if category=='fuel' else 'LAUNCH')+' PLAN',parent=self,position=(-.33,.08,-.27),rotation_x=90,scale=1.1,color=color.cyan)
        else:
            craft=Spacecraft(self);craft.apply(design);craft.root.rotation=(0,0,0)
            for child in craft.root.children:child.enabled=False
            if category=='sensor':craft.sensor.enabled=True;craft.sensor.position=(0,0,0)
            elif category=='radio':craft.radio.enabled=True;craft.radio.position=(0,0,0)
            else:
                # The same array geometry, sized by the actual selected power package.
                for _,wing in craft.arrays:wing.enabled=True

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
        size=.17 if local else .35
        heights={'sensor':.52 if design.sensor=='advanced' else .35,'power':.045,
                 'radio':.16 if design.radio=='fast' else .12,'orbit':.12,'launcher':.12,'fuel':.12}
        y=0;previous_height=None
        for i,category in enumerate(categories):
            height=heights[category]*size
            if previous_height is not None:y+=(previous_height+height)/2+(.025 if local else .04)
            part=Part(category,design,parent=parent.held_part,y=y,scale=size,rotation=(0,-15,0))
            parent.held_parts.append(part)
            previous_height=height
        Entity(parent=parent.held_part,model='sphere',position=(0,-.04,0),scale=.055 if local else .13,color=color.light_gray)
