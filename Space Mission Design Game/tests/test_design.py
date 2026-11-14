"""Trade-off behavior and energy/data conservation, not snapshots of UI output."""
from dataclasses import replace
import sys
from pathlib import Path
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from game.domain.design import Design,DesignSession,evaluate,load_catalog,feasible_designs


class DesignTests(unittest.TestCase):
    def setUp(self):
        self.catalog=load_catalog()

    def test_sensor_upgrade_creates_linked_power_and_data_constraints(self):
        base=evaluate(self.catalog,Design())
        upgraded=evaluate(self.catalog,Design(sensor='advanced'))
        self.assertTrue(base.passed)
        self.assertGreater(upgraded.values['quality'],base.values['quality'])
        for key in ('mass_kg','cost_credits','peak_power_w','expected_data_mb'):
            self.assertGreater(upgraded.values[key],base.values[key])
        self.assertEqual({check.code for check in upgraded.failures},{'power','delivery'})

    def test_fixing_one_system_does_not_hide_other_failures(self):
        design=Design(sensor='advanced',power='extended')
        result=evaluate(self.catalog,design)
        self.assertGreater(result.values['power_margin_w'],0)
        self.assertIn('mass',{check.code for check in result.failures})
        design=replace(design,launcher='heavy')
        self.assertEqual({check.code for check in evaluate(self.catalog,design).failures},{'delivery'})
        self.assertTrue(evaluate(self.catalog,replace(design,radio='fast')).passed)

    def test_multiple_sensor_designs_can_pass_the_preview(self):
        valid=list(feasible_designs(self.catalog))
        self.assertGreaterEqual(len(valid),2)
        self.assertTrue(any(item.sensor=='basic' for item in valid))
        self.assertTrue(any(item.sensor=='advanced' for item in valid))

    def test_energy_and_data_are_conserved_for_all_combinations(self):
        from itertools import product
        categories=self.catalog['categories']
        for options in product(*(category['options'] for category in categories)):
            design=Design(**{cat['id']:option['id'] for cat,option in zip(categories,options)})
            value=evaluate(self.catalog,design).values
            with self.subTest(design=design):
                self.assertAlmostEqual(value['generated_mb'],value['delivered_mb']+value['stored_mb']+value['overflow_mb'])
                self.assertAlmostEqual(value['battery_capacity_wh']+value['solar_energy_wh'],
                                       value['final_battery_wh']+value['used_energy_wh']+value['curtailed_energy_wh'])
                self.assertGreaterEqual(value['min_battery_wh'],0)
                self.assertLessEqual(value['final_battery_wh'],value['battery_capacity_wh']+.00001)

    def test_eclipse_and_launch_orbit_constraints_are_visible(self):
        result=evaluate(self.catalog,Design(orbit='wide'))
        codes={check.code for check in result.failures}
        self.assertIn('energy',codes)
        self.assertIn('orbit',codes)
        self.assertIn('delivery',codes)

    def test_expensive_combination_exceeds_budget(self):
        result=evaluate(self.catalog,Design('advanced','extended','fast','wide','heavy'))
        self.assertIn('budget',{check.code for check in result.failures})

    def test_undo_and_reset_restore_all_metrics(self):
        session=DesignSession(self.catalog)
        original=session.preview
        session.choose('sensor','advanced')
        changed=session.preview
        self.assertTrue(session.undo())
        self.assertEqual(session.preview,original)
        session.choose('sensor','advanced')
        session.reset()
        self.assertEqual(session.preview,original)
        session.undo()
        self.assertEqual(session.preview,changed)

    def test_storage_overflow_fails_even_with_fast_radio(self):
        self.catalog['scenario']['storage_mb']=100
        result=evaluate(self.catalog,Design(radio='fast'))
        self.assertIn('storage',{check.code for check in result.failures})
        self.assertGreater(result.values['overflow_mb'],0)


if __name__=='__main__': unittest.main()
