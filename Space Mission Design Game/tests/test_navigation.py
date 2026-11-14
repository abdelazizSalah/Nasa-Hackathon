"""Behavior checks for walls, doors, camera directions, and frozen reading mode."""
import sys
from pathlib import Path
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from game.domain.navigation import Pose,Obstacle,advance


class NavigationTests(unittest.TestCase):
    def test_strafe_is_relative_to_heading_and_diagonal_speed_is_limited(self):
        import math
        right=advance(Pose(0,0,0),0,0,.1,[],strafe=1)
        self.assertAlmostEqual(right.x,.3)
        self.assertAlmostEqual(right.yaw,0)
        rotated=advance(Pose(0,0,90),0,0,.1,[],strafe=1)
        self.assertAlmostEqual(rotated.z,-.3)
        diagonal=advance(Pose(0,0,0),1,0,.1,[],strafe=1)
        self.assertAlmostEqual(math.hypot(diagonal.x,diagonal.z),.3)

    def walk(self,pose,obstacles):
        for _ in range(100): pose=advance(pose,1,0,.02,obstacles)
        return pose

    def test_closed_door_blocks_but_open_door_allows_passage(self):
        start=Pose(0,3,0)
        closed=self.walk(start,[Obstacle(0,5,3.2,.24)])
        opened=self.walk(start,[])
        self.assertLess(closed.z,4.61)
        self.assertGreater(opened.z,5.5)

    def test_paused_panel_freezes_both_position_and_turn(self):
        pose=Pose(1,3,45)
        self.assertEqual(advance(pose,1,1,.1,[],frozen=True),pose)

    def test_turning_changes_forward_direction(self):
        result=advance(Pose(0,0,90),1,0,.1,[])
        self.assertAlmostEqual(result.x,.3)
        self.assertAlmostEqual(result.z,0)

    def test_motion_does_not_tunnel_through_thin_wall(self):
        wall=Obstacle(0,0,10,.05)
        result=advance(Pose(0,-.4),1,0,10,[wall])
        self.assertLess(result.z,-.3)

    def test_wall_allows_sliding_parallel_to_surface(self):
        wall=Obstacle(0,0,10,.2)
        pose=Pose(0,-.39,45)
        for _ in range(20): pose=advance(pose,1,0,.05,[wall])
        self.assertGreater(pose.x,1)
        self.assertLess(pose.z,-.37)


if __name__=='__main__': unittest.main()
