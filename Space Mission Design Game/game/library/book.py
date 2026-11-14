"""Reusable hardcover geometry with an independently hinged front cover."""
from ursina import Entity, Text, color, load_texture
from game.library.art import ASSETS

class Book(Entity):
    def __init__(self,book,**kwargs):
        super().__init__(**kwargs)
        tint=color.hex(book['color'])
        self.pages=Entity(parent=self,model='cube',scale=(.94,.96,.15),color=color.rgb32(223,219,196))
        Entity(parent=self,model='cube',z=.095,scale=(1,1.03,.035),color=tint)
        Entity(parent=self,model='cube',x=-.48,scale=(.05,1.03,.22),color=tint)
        Text(book['short'],parent=self,position=(-.513,0,0),rotation=(0,-90,90),
             origin=(0,0),scale=1.6,color=color.white)
        self.hinge=Entity(parent=self,x=-.5,z=-.1)
        Entity(parent=self.hinge,model='cube',x=.5,scale=(1,1.03,.035),color=tint)
        self.cover=Entity(parent=self.hinge,model='quad',position=(.5,0,-.023),scale=(1,1),
                          texture=load_texture(f'cover-{book["id"]}.png', folder=ASSETS),collider='box')
        if self.cover.texture is None:
            Text(book['short'],parent=self.cover,origin=(0,0),scale=4,color=color.white,wordwrap=10)
        self.cover.on_click=lambda:getattr(self,'choose',lambda:None)()
        self.cover.on_mouse_enter=lambda:self.hover(True)
        self.cover.on_mouse_exit=lambda:self.hover(False)
        self.hovered_book=False
    def hover(self,active):
        self.hovered_book=active
        self.cover.color=color.rgb32(255,244,211) if active else color.white
        callback=getattr(self,'on_hover',None)
        if callback:callback(active)
