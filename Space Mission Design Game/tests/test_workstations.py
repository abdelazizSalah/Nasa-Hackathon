from dataclasses import asdict
import unittest
from game.domain.assembly import Assembly,CATEGORIES
from game.domain.design import DesignSession,Design,evaluate
from game.domain.campaign import Campaign
from game.domain.facility_layout import station_position

class WorkstationTests(unittest.TestCase):
    def test_one_action_selects_and_collects_default_and_upgrade(self):
        s=DesignSession();a=Assembly();a.select_mission('flood-watch',s)
        self.assertFalse(a.collect(s,'sensor','basic','engineer',['engineer']))
        self.assertEqual(a.inventory(s,'engineer',['engineer']),['sensor'])
        self.assertTrue(a.collect(s,'sensor','advanced','engineer',['engineer']))
        self.assertEqual(a.confirmed['sensor'],'advanced');self.assertEqual(s.design.sensor,'advanced')

    def test_rejected_collection_never_partially_changes_selection(self):
        s=DesignSession();a=Assembly();a.select_mission('flood-watch',s)
        before=asdict(s.design)
        with self.assertRaises(ValueError):a.collect(s,'power','extended','engineer',['engineer'])
        self.assertEqual(asdict(s.design),before);self.assertFalse(a.confirmed)
        with self.assertRaises(ValueError):a.collect(s,'sensor','advanced','operations',['engineer','operations'])
        self.assertEqual(asdict(s.design),before)

    def test_fuel_is_required_owned_by_flight_and_changes_only_cost(self):
        s=DesignSession();a=Assembly();a.select_mission('flood-watch',s)
        for c in CATEGORIES[:-1]:a.collect(s,c,getattr(s.design,c),'engineer',['engineer']);a.submit(s,c,'engineer',['engineer'])
        with self.assertRaises(ValueError):a.validate(s,['engineer'])
        before=s.preview.values
        a.collect(s,'fuel','liquid','engineer',['engineer']);after=s.preview.values
        self.assertEqual(after['cost_eur']-before['cost_eur'],3000)
        for k in before:
            if not k.endswith('eur'):self.assertEqual(before[k],after[k],k)
        a.submit(s,'fuel','engineer',['engineer']);self.assertTrue(a.validate(s,['engineer']))
        self.assertEqual(station_position('fuel','engineer',['engineer']),(58,6.2))

    def test_cannot_bypass_budget_with_atomic_choice(self):
        s=DesignSession();a=Assembly();a.select_mission('flood-watch',s)
        for c in CATEGORIES:a.collect(s,c,getattr(s.design,c),'engineer',['engineer'])
        s.catalog['scenario']['budget_eur']=90000
        with self.assertRaises(ValueError):a.collect(s,'fuel','liquid','engineer',['engineer'])
        self.assertEqual(s.design.fuel,'solid');self.assertEqual(a.confirmed['fuel'],'solid')

    def test_both_propellant_choices_have_nasa_sources_and_qualitative_traits(self):
        s=DesignSession();cat=next(c for c in s.catalog['categories'] if c['id']=='fuel')
        self.assertTrue(cat['source_url'].startswith('https://www1.grc.nasa.gov/'))
        self.assertEqual({o['id'] for o in cat['options']},{'solid','liquid'})
        self.assertTrue(all('control' in o and 'storage' in o for o in cat['options']))
