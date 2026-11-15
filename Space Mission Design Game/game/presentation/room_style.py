"""Lightweight themed rooms with explicit task and role signage."""
from ursina import Entity,color
from game.presentation.materials import surface

THEMES={
 'sensor':('PAYLOAD / OPTICS',(55,215,226),(15,49,61),'SCIENCE & PAYLOAD','E at the camera bench -> SELECT & PICK one imager.','Next: POWER SYSTEMS / amber room'),
 'power':('POWER / ENERGY',(255,195,68),(62,46,20),'POWER & SPACECRAFT SYSTEMS','E at the solar/battery bench -> pick a power package.','Next: COMMUNICATIONS / violet room'),
 'radio':('COMMUNICATIONS / DATA',(194,144,255),(43,28,63),'COMMUNICATIONS & DATA','E at the antenna bench -> pick a radio.','Next: MISSION PLANNING / blue room'),
 'orbit':('MISSION PLANNING',(100,164,255),(22,39,67),'MISSION & FLIGHT DYNAMICS','Pick ONE option at EACH table: ORBIT, LAUNCHER, FUEL.','Next: INTEGRATION / green room'),
 'integration':('INTEGRATION / READINESS',(97,239,172),(23,51,41),'HOST APPROVES / EVERYONE PLACES','E places or retrieves parts; submit all SIX contributions.','Then: HOST APPROVE READINESS -> M -> LAUNCH NOW')}

def decorate(facility,x,key):
    h=facility.hub;_,rgb,wall,role,task,next_=THEMES[key];accent=color.rgb32(*rgb)
    panel=h.box((x,2.25,13.89),(12,2.9,.04),color.rgb32(*wall),shader=False,texture=surface('wall-panels'))
    panel.texture_scale=(6,1.5)
    facility.label('ROLE: '+role,(x,2.78,13.77),.105,accent)
    facility.label(task,(x,2.40,13.76),.10,color.white)
    facility.label(next_,(x,2.04,13.75),.085,accent)
    for side in (-1,1):
        h.box((x+side*6.4,2,9),(.13,3.8,.13),accent,shader=False)
    for z in (4.25,13.75):
        h.box((x,.025,z),(13.4,.035,.18),accent,shader=False)
    if key=='power':
        for i in range(4):h.box((x-4.8,1.2+i*.32,13.6),(1,.18,.12),accent,shader=False)
    elif key=='radio':
        h.box((x-4.8,1.45,13.45),(.15,1.3,.15),accent)
        Entity(model='sphere',position=(x-4.8,2.1,13.35),scale=(.9,.18,.9),rotation_x=65,color=color.white,texture=surface('brushed-metal'))
    elif key=='sensor':
        Entity(model='sphere',position=(x-4.8,1.8,13.48),scale=(1,1,.15),color=color.light_gray,texture=surface('brushed-metal'))
        Entity(model='sphere',position=(x-4.8,1.8,13.36),scale=(.65,.65,.16),color=color.white,texture=surface('optical-glass'))
    elif key=='integration':
        h.box((x,.035,7.6),(6.5,.04,.22),color.white,shader=False,texture=surface('hazard-stripes'))

def texture_spacecraft(craft):
    craft.root.children[0].texture=surface('equipment-panel')
    for _,wing in craft.arrays:
        wing.texture=surface('solar-cells');wing.color=color.white
