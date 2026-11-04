import unittest
from roomglow import *
from fixtures import *
K = shopping_plan(CATALOG, 3000, "korean")
PK = [c for c in CATALOG if c["id"] in K["items"]]
class T(unittest.TestCase):
    def test_floor(self): self.assertEqual(floor_area(3.2, 4.0), 12.8)
    def test_floor_bad(self):
        with self.assertRaises(ValueError): floor_area(0, 4)
    def test_wall(self): self.assertEqual(wall_area(3.2, 4.0, 2.6), 34.14)
    def test_paint(self): self.assertEqual(paint_estimate(34.14), {"liters": 6.83, "cans": 3, "cost_thb": 1950})
    def test_wallpaper(self): self.assertEqual(wallpaper_rolls(3.2 * 2.6)["rolls"], 2)
    def test_lumens(self): self.assertEqual(lumens_needed(12.8, "bedroom")["lumens"], 1920)
    def test_light_gap(self): l = light_plan(12.8, "bedroom", 800, "cozy"); self.assertEqual(l["gap_lm"], 1120); self.assertEqual(l["bulbs_800lm"], 2); self.assertEqual(l["kelvin"], 2700)
    def test_light_ok(self): self.assertEqual(light_plan(12.8, "bedroom", 2500, "muji")["bulbs_800lm"], 0)
    def test_glow_before(self): self.assertEqual(glow_score(SCAN), 32)
    def test_glow_bad(self):
        with self.assertRaises(ValueError): glow_score({"light": 2, "clutter": 0, "harmony": 0, "cohesion": 0})
    def test_glow_after(self): self.assertEqual(score_after(SCAN, PK, True), 78)
    def test_plan_budget(self): self.assertEqual(K["spent_thb"], 3000); self.assertEqual(K["impact"], 44); self.assertEqual(len(K["items"]), 6)
    def test_renter_excludes(self): self.assertNotIn("paint_wall", K["items"]); self.assertEqual(K["excluded_not_renter_safe"], ["paint_wall", "shelf_drill"])
    def test_owner_mode(self): self.assertIn("shelf_drill", shopping_plan(CATALOG, 3000, "korean", False)["items"])
    def test_small_budget(self): p = shopping_plan(CATALOG, 1000, "korean"); self.assertEqual(p["spent_thb"], 930); self.assertLessEqual(p["spent_thb"], 1000)
    def test_zero_budget(self): self.assertEqual(shopping_plan(CATALOG, 0, "korean")["items"], [])
    def test_style_filter(self): self.assertNotIn("rug_round", shopping_plan(CATALOG, 3000, "muji")["items"])
    def test_declutter(self): d = declutter(DECLUTTER); self.assertEqual(d["resale_thb"], 750); self.assertEqual(d["removed"], 4)
    def test_weekend(self): w = weekend_plan(K["items"], CATALOG); self.assertEqual(w["steps"][0]["item"], "storage_box"); self.assertEqual(w["total_minutes"], 125)
    def test_poll(self): p = poll_tally(POLL, VOTES); self.assertEqual(p["total_votes"], 6); self.assertEqual(p["winner"], "korean"); self.assertEqual(p["rows"][0]["pct"], 66.67)
    def test_poll_tie(self): self.assertTrue(poll_tally(["a", "b"], [{"voter": "x", "option": "a"}, {"voter": "y", "option": "b"}])["tie"])
    def test_poll_empty(self): self.assertIsNone(poll_tally(["a"], [])["winner"])
if __name__ == "__main__": unittest.main()
