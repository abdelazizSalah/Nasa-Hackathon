import sys
from pathlib import Path
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from game.domain.campaign import Campaign
from game.domain.design import DesignSession
from game.orbit.provider import trajectory
from game.domain.operations import geometry,simulate

class CampaignTests(unittest.TestCase):
    def test_gates_saves_and_revalidation(self):
        c=Campaign(); s=DesignSession()
        c.advance(s,set()); self.assertEqual(c.stage,0)
        for _ in range(4): c.advance(s,{'purpose'})
        self.assertEqual(c.stage,4)
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'save.json'; c.save(path,s,{'purpose'})
            other=Campaign(); self.assertEqual(other.load(path,s),{'purpose'}); self.assertEqual(other.stage,4)
        s.choose('sensor','advanced'); c.changed(); self.assertEqual(c.stage,1); self.assertIsNone(c.approved)

    def test_geometry_and_cache_provenance(self):
        a,_,meta=trajectory('regional',False); b,_,other=trajectory('wide',False)
        self.assertNotEqual(meta['input_hash'],other['input_hash'])
        self.assertNotEqual(a[50][2:5],b[50][2:5])
        self.assertTrue(geometry(a[0])['contact'])
        self.assertTrue(any(geometry(row)['eclipse'] for row in a))
        # Independent horizon condition: station-satellite vector above local tangent.
        row=a[0]; self.assertGreater(row[2]-6378.137,0)

    def test_operational_plan_changes_outcome_and_balances_data(self):
        rows,_,_=trajectory('regional',False); s=DesignSession()
        targeted=simulate(s.catalog,s.design,rows,True); continuous=simulate(s.catalog,s.design,rows,False)
        self.assertTrue(targeted['passed']); self.assertFalse(continuous['passed'])
        self.assertAlmostEqual(targeted['generated_mb'],120)
        self.assertGreater(continuous['lost_mb'],0)

if __name__=='__main__': unittest.main()
