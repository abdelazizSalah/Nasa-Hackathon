"""Flat-floor navigation and wall collision, independent of the renderer."""
from dataclasses import dataclass
import math


@dataclass(frozen=True)
class Obstacle:
    x: float
    z: float
    width: float
    depth: float

    def contains(self, x, z, radius=.28):
        return abs(x - self.x) < self.width / 2 + radius and abs(z - self.z) < self.depth / 2 + radius


@dataclass(frozen=True)
class Pose:
    x: float = 0
    z: float = -4.5
    yaw: float = 0


def advance(pose, forward, turn, dt, obstacles, frozen=False, strafe=0):
    if frozen:
        return pose
    dt = max(0, min(dt, .1))  # Prevent jumps when focus/graphics stall.
    yaw = (pose.yaw + turn * 75 * dt) % 360
    length = max(1, math.hypot(forward, strafe))
    forward, strafe = forward / length, strafe / length
    amount = math.hypot(forward, strafe) * 3 * dt
    steps = max(1, math.ceil(abs(amount) / .08))
    dx = (math.sin(math.radians(yaw))*forward + math.cos(math.radians(yaw))*strafe) * 3 * dt / steps
    dz = (math.cos(math.radians(yaw))*forward - math.sin(math.radians(yaw))*strafe) * 3 * dt / steps
    x, z = pose.x, pose.z
    for _ in range(steps):
        if not any(item.contains(x + dx, z) for item in obstacles):
            x += dx
        if not any(item.contains(x, z + dz) for item in obstacles):
            z += dz
    return Pose(x, z, yaw)
