"""One scale transform for panel content AND hitboxes, recalculated after resize."""
from ursina import Entity, window

def panel_scale(aspect):return min(1,max(.1,(aspect-.08)/1.46))

class ResponsivePanel(Entity):
    def __init__(self,width=1.46,**kwargs):
        self.reference_width=width
        super().__init__(**kwargs)
        self.update()
    def update(self):
        self.scale=min(1,max(.1,(float(window.aspect_ratio)-.08)/self.reference_width))
        dim=getattr(self,'dimmer',None)
        if dim:dim.scale=(max(4,window.aspect_ratio/self.scale_x),max(3,1/self.scale_y))
