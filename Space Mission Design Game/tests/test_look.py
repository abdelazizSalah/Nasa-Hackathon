import unittest
from game.domain.look import mouse_look
from game.domain.navigation import Pose

class MouseLookTests(unittest.TestCase):
    def test_both_axes_and_position_preserved(self):
        pose,pitch=mouse_look(Pose(2,3,0),0,.1,.1)
        self.assertEqual((pose.x,pose.z),(2,3));self.assertEqual(pose.yaw,12);self.assertEqual(pitch,-12)
        pose,pitch=mouse_look(pose,pitch,-.2,-.2)
        self.assertEqual(pose.yaw,348);self.assertEqual(pitch,12)

    def test_pitch_limits_and_displacement_independent_of_frame_count(self):
        self.assertEqual(mouse_look(Pose(),0,0,99)[1],-85)
        self.assertEqual(mouse_look(Pose(),0,0,-99)[1],85)
        one,pitch=mouse_look(Pose(),0,.2,.2)
        many=Pose();p=0
        for _ in range(10):many,p=mouse_look(many,p,.02,.02)
        self.assertAlmostEqual(one.yaw,many.yaw);self.assertAlmostEqual(pitch,p)
