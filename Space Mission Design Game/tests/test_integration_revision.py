"""Retrieval and mission-owned EUR budget rules, including real TCP authority."""
from unittest import TestCase
from unittest.mock import patch
from game.domain.assembly import Assembly,CATEGORIES
from game.domain.design import DesignSession,evaluate,Design,load_catalog
from game.domain.economy import missions,eur
import test_four_player as multiplayer_tests
from test_lan import receive

class EuroBudgetTests(TestCase):
    def test_catalog_prices_and_mission_are_single_euro_sources(self):
        catalog=load_catalog();mission=next(m for m in missions() if m['id']=='flood-watch')
        self.assertEqual(catalog['scenario']['budget_eur'],mission['budget_eur'])
        self.assertEqual(mission['currency'],'EUR')
        for category in catalog['categories']:
            for option in category['options']:
                self.assertGreater(option.get('cost_eur',option.get('ground_cost_eur',0)),0)
        self.assertEqual(evaluate(catalog,Design()).values['cost_eur'],89000)
        costly=evaluate(catalog,Design('advanced','extended','fast','wide','heavy'))
        self.assertEqual(costly.values['cost_eur'],148000)
        check=next(c for c in costly.checks if c.code=='budget')
        self.assertFalse(check.passed);self.assertIn('€148,000',check.explanation);self.assertIn('€145,000',check.explanation)

    def test_mission_budget_boundary_recalculates_and_blocks_collection(self):
        s=DesignSession();a=Assembly();definition=dict(next(m for m in missions() if m['available']))
        definition['budget_eur']=89000
        with patch('game.domain.economy.missions',return_value=[definition]):a.select_mission('flood-watch',s)
        self.assertTrue(next(c.passed for c in s.preview.checks if c.code=='budget'))
        a.confirm(s,'sensor','engineer')
        definition['budget_eur']=88999
        with patch('game.domain.economy.missions',return_value=[definition]):a.select_mission('flood-watch',s)
        self.assertFalse(next(c.passed for c in s.preview.checks if c.code=='budget'))
        with self.assertRaisesRegex(ValueError,'budget'):a.confirm(s,'sensor','engineer')
        self.assertIn('budget',[r['code'] for r in a.snapshot(s,['engineer'])['issues']])

    def test_remove_restores_inventory_preserves_other_parts_and_invalidates_approval(self):
        s=DesignSession();a=Assembly();a.select_mission('flood-watch',s)
        for c in CATEGORIES:a.confirm(s,c,'engineer');a.submit(s,c,'engineer',['engineer'])
        self.assertTrue(a.validate(s,['engineer']))
        a.remove(s,'sensor','engineer',['engineer'])
        self.assertEqual(len(a.submitted),4);self.assertEqual(a.inventory(s,'engineer',['engineer']),['sensor'])
        self.assertFalse(a.ready(s));self.assertIsNone(a.approved)
        with self.assertRaises(ValueError):a.remove(s,'sensor','engineer',['engineer'])
        a.submit(s,'sensor','engineer',['engineer']);self.assertTrue(a.validate(s,['engineer']))

class RetrievalNetworkTests(TestCase):
    def test_owner_and_proximity_checked_and_retrieval_synchronized(self):
        helper=multiplayer_tests.FourPlayerTests();self.addCleanup(helper.doCleanups)
        server,clients=helper.crew(2);helper.prepare(server,clients)
        host=clients['engineer'];friend=clients['operations']
        helper.act(friend,'pose',x=70,z=7,yaw=0);helper.act(friend,'remove',category='sensor')
        receive(friend,lambda d:d.get('kind')=='notice' and 'teammate' in d['message'])
        helper.act(host,'pose',x=0,z=0,yaw=0);helper.act(host,'remove',category='sensor')
        receive(host,lambda d:d.get('kind')=='notice' and 'Approach' in d['message'])
        helper.act(host,'pose',x=70,z=7,yaw=0);helper.act(host,'remove',category='sensor')
        state=helper.state(friend,lambda d:'sensor' not in d['assembly']['submitted'])
        self.assertFalse(state['assembly']['ready']);self.assertEqual(state['stage'],1)
        self.assertIn('sensor',state['assembly']['inventory']['engineer']);self.assertEqual(len(state['assembly']['submitted']),4)
