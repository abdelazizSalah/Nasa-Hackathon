"""Frame-rate-independent mouse displacement to camera orientation."""
from dataclasses import replace

def mouse_look(pose,pitch,dx,dy,sensitivity=120):
    return replace(pose,yaw=(pose.yaw+dx*sensitivity)%360),max(-85,min(85,pitch-dy*sensitivity))
