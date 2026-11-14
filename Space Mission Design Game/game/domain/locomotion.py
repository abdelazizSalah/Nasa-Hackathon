"""Vertical capsule clearance layered over the existing horizontal navigator."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Volume:
    x:float
    z:float
    width:float
    depth:float
    bottom:float
    top:float
    def contains(self,x,z,radius=.28):
        return abs(x-self.x)<self.width/2+radius and abs(z-self.z)<self.depth/2+radius

class Locomotion:
    standing=1.8
    crouched=.95
    def __init__(self):
        self.y=0.;self.velocity=0.;self.crouch=False;self.grounded=True
    @property
    def height(self):return self.crouched if self.crouch else self.standing
    @property
    def eye(self):return self.y+(self.height-.1)
    def blockers(self,volumes):
        return [v for v in volumes if self.y<v.top-.01 and self.y+self.height>v.bottom+.01]
    def jump(self):
        if self.grounded:self.velocity=5.2;self.grounded=False;return True
        return False
    def tick(self,dt,pose,volumes,want_crouch=False,frozen=False):
        if frozen:return
        dt=max(0,min(dt,.1))
        overhead=any(v.contains(pose.x,pose.z) and v.bottom<self.y+self.standing and v.top>self.y+self.crouched for v in volumes)
        self.crouch=bool(want_crouch or overhead)
        floor=max([0.]+[v.top for v in volumes if v.contains(pose.x,pose.z) and v.top<=self.y+.025])
        if self.grounded and self.y>floor+.03:self.grounded=False
        if not self.grounded:
            old=self.y;self.velocity-=12*dt;new=old+self.velocity*dt
            if self.velocity>0:
                ceilings=[v.bottom-self.height for v in volumes if v.contains(pose.x,pose.z) and old+self.height<=v.bottom+.01 and new+self.height>v.bottom]
                if ceilings:new=min(ceilings);self.velocity=0
            floors=[0.]+[v.top for v in volumes if v.contains(pose.x,pose.z) and new<=v.top<=old+.025]
            if self.velocity<=0 and new<=max(floors):new=max(floors);self.velocity=0;self.grounded=True
            self.y=max(0,new)
