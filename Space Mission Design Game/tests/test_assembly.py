import unittest
from game.domain.assembly import Assembly,ROLES,CATEGORIES,PLAYER_IDS,assignments,owned,feedback
from game.domain.design import DesignSession
from game.domain.navigation import Pose
from game.domain.locomotion import Locomotion,Volume

class AssemblyTests(unittest.TestCase):
    def test_balanced_roles_all_counts(self):
        for n,counts in ((1,[4]),(2,[2,2]),(3,[2,1,1]),(4,[1,1,1,1])):
            players=PLAYER_IDS[:n];roles=assignments(players)
            self.assertEqual([len(rs) for rs in roles.values()],counts)
            self.assertEqual(sorted(r for rs in roles.values() for r in rs),sorted(ROLES))
            self.assertEqual(set.union(*(owned(p,players) for p in players)),set(CATEGORIES))

    def test_mission_unavailable_and_workshop_sequence(self):
        a=Assembly();s=DesignSession()
        with self.assertRaises(ValueError):a.select_mission('coming-soon')
        with self.assertRaises(ValueError):a.confirm(s,'sensor','engineer')
        a.select_mission('flood-watch')
        with self.assertRaises(ValueError):a.confirm(s,'power','engineer')

    def integrated(self,players=PLAYER_IDS[:1]):
        a=Assembly();s=DesignSession();a.select_mission('flood-watch')
        for c in CATEGORIES:
            p=next(p for p in players if c in owned(p,players))
            a.confirm(s,c,p);a.submit(s,c,p,players)
        return a,s

    def test_all_player_counts_integrate_without_missing_roles(self):
        for n in range(1,5):
            a,s=self.integrated(PLAYER_IDS[:n])
            self.assertTrue(a.validate(s,PLAYER_IDS[:n]));self.assertTrue(a.ready(s))

    def test_duplicate_and_wrong_owner_rejected(self):
        a,s=self.integrated(PLAYER_IDS[:2])
        with self.assertRaises(ValueError):a.submit(s,'sensor','operations',PLAYER_IDS[:2])
        with self.assertRaises(ValueError):a.submit(s,'sensor','engineer',PLAYER_IDS[:2])

    def test_correction_preserves_unaffected_submissions_and_requires_resubmission(self):
        a,s=self.integrated();a.validate(s,PLAYER_IDS[:1])
        s.choose('sensor','advanced');a.changed(s)
        self.assertNotIn('sensor',a.submitted);self.assertEqual(len(a.submitted),4);self.assertFalse(a.ready(s))
        a.confirm(s,'sensor','engineer');a.submit(s,'sensor','engineer',PLAYER_IDS[:1])
        self.assertFalse(a.validate(s,PLAYER_IDS[:1]))
        self.assertTrue(any(not r['passed'] for r in a.validation))
        for c,o in [('power','extended'),('radio','fast'),('launcher','heavy')]:
            s.choose(c,o);a.changed(s);a.confirm(s,c,'engineer');a.submit(s,c,'engineer',PLAYER_IDS[:1])
        self.assertTrue(a.validate(s,PLAYER_IDS[:1]))

    def test_save_restore_conservative_and_feedback_uses_existing_checks(self):
        a,s=self.integrated();a.validate(s,PLAYER_IDS[:1]);b=Assembly();b.restore(a.snapshot(s,PLAYER_IDS[:1]),s)
        self.assertEqual(b.confirmed,a.confirmed);self.assertFalse(b.submitted);self.assertFalse(b.ready(s))
        self.assertEqual([r['explanation'] for r in feedback(s,PLAYER_IDS[:2])],[c.explanation for c in s.preview.checks])

class LocomotionTests(unittest.TestCase):
    def test_jump_gravity_and_no_air_jump(self):
        m=Locomotion();p=Pose();self.assertTrue(m.jump());self.assertFalse(m.jump())
        heights=[]
        for _ in range(100):m.tick(.02,p,[]);heights.append(m.y)
        self.assertGreater(max(heights),.8);self.assertEqual(m.y,0);self.assertTrue(m.grounded)

    def test_crouch_clearance_and_modal_freeze(self):
        m=Locomotion();p=Pose(51,9);beam=Volume(51,9,1,3.4,1.1,4)
        m.tick(.05,p,[beam],True);self.assertTrue(m.crouch);self.assertFalse(m.blockers([beam]))
        m.tick(.05,p,[beam],False);self.assertTrue(m.crouch)
        m.tick(.05,Pose(53,9),[beam],False);self.assertFalse(m.crouch)
        self.assertIn(beam,m.blockers([beam]))
        m.jump();m.tick(.1,p,[],frozen=True);self.assertEqual(m.y,0)

    def test_raised_crossing_landing_and_walking_off(self):
        m=Locomotion();p=Pose(37,9);step=Volume(37,9,1.2,3.4,0,.45)
        m.jump()
        for _ in range(50):m.tick(.02,p,[step])
        self.assertAlmostEqual(m.y,.45);self.assertTrue(m.grounded)
        for _ in range(50):m.tick(.02,Pose(39,9),[step])
        self.assertEqual(m.y,0)
