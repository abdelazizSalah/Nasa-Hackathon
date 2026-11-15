import unittest
from game.domain.design import DesignSession
from game.domain.assembly import Assembly,CATEGORIES
from game.domain.guidance import next_step,progress_text
from game.domain.facility_layout import station_position
from game.domain.navigation import Pose,Obstacle,advance
import test_four_player as network_tests

class GuidedFlowTests(unittest.TestCase):
    def test_one_unique_bench_per_object(self):
        self.assertEqual(len({station_position(c) for c in CATEGORIES}),6)
        self.assertNotEqual(station_position('orbit'),station_position('launcher'))

    def test_both_fuel_options_have_positive_prices(self):
        s=DesignSession();cat=next(c for c in s.catalog['categories'] if c['id']=='fuel')
        self.assertEqual({o['id']:o['cost_eur'] for o in cat['options']},{'solid':2000,'liquid':5000})
        self.assertEqual(s.preview.values['cost_eur'],91000)

    def test_guidance_explains_pick_place_approval_launch_and_completion(self):
        s=DesignSession();a=Assembly();players={'engineer':{'name':'Host'}}
        self.assertEqual(next_step(a.snapshot(s,players),s,players)['action'],'SELECT MISSION')
        a.select_mission('flood-watch',s)
        for c in CATEGORIES:
            g=next_step(a.snapshot(s,players),s,players)
            self.assertEqual(g['target'],station_position(c));a.collect(s,c,getattr(s.design,c),'engineer',players)
        for c in CATEGORIES:
            self.assertIn('PLACE',next_step(a.snapshot(s,players),s,players)['action'])
            a.submit(s,c,'engineer',players)
        self.assertIn('APPROVE',next_step(a.snapshot(s,players),s,players)['action'])
        a.validate(s,players)
        self.assertEqual(next_step(a.snapshot(s,players),s,players)['action'],'LAUNCH NOW')
        self.assertIn('15/15',progress_text(a.snapshot(s,players),True))

    def test_sprint_is_faster_and_does_not_tunnel_through_walls(self):
        p=Pose(0,0,0);walk=advance(p,1,0,.1,[]);run=advance(p,1,0,.1,[],speed=5.4)
        self.assertAlmostEqual(run.z/walk.z,1.8)
        blocker=Obstacle(0,.7,3,.1)
        for _ in range(20):p=advance(p,1,0,.1,[blocker],speed=5.4)
        self.assertLess(p.z,.4)
        self.assertEqual(advance(p,1,0,.1,[],frozen=True,speed=5.4),p)

class HostLaunchTests(unittest.TestCase):
    def test_host_can_launch_approved_crew_from_tablet_without_a_proximity_trap(self):
        helper=network_tests.FourPlayerTests();self.addCleanup(helper.doCleanups)
        server,clients=helper.crew(2);helper.prepare(server,clients)
        host=clients['engineer'];helper.act(host,'pose',x=0,z=-4.5,yaw=0)
        helper.act(host,'launch')
        result=helper.state(host,lambda d:d['result'] is not None)
        self.assertTrue(result['result']['passed'])
        for client in clients.values():helper.act(client,'finished',flight_id=result['flight_id'])
        helper.state(host,lambda d:not d['busy'])
