import unittest
from labellens import *
from fixtures import *
class T(unittest.TestCase):
    def test_totals(self): self.assertEqual(pack_totals(GREENTEA)["sugar_g"], 40)
    def test_totals_bad(self):
        with self.assertRaises(ValueError): pack_totals({**GREENTEA, "servings_per_pack": 0})
    def test_spoons(self): self.assertEqual(sugar_spoons(40), 10.0); self.assertEqual(sugar_spoons(0), 0)
    def test_light_drink(self): self.assertEqual(traffic_light(GREENTEA)["sugar_g"], AMBER)
    def test_light_solid_red(self):
        tl = traffic_light(CHIPS); self.assertEqual((tl["fat_g"], tl["sodium_mg"]), (RED, RED))
    def test_grade_sweet(self): self.assertEqual(grade(GREENTEA)["grade"], "C"); self.assertEqual(grade(GREENTEA)["score"], 50)
    def test_grade_zero(self): self.assertEqual(grade(GREENTEA0)["grade"], "A")
    def test_grade_noodle(self): self.assertEqual(grade(NOODLE)["grade"], "E")
    def test_daily_pct(self): self.assertEqual(daily_pct(pack_totals(GREENTEA))["sugar_g"], 167)
    def test_walk(self): self.assertEqual(walk_off(180), 45)
    def test_allergen(self):
        self.assertEqual(allergen_hits(CHIPS["ingredients_th"], ["milk"])["hits"][0]["allergen"], "milk")
        self.assertTrue(allergen_hits(GREENTEA0["ingredients_th"], ["milk", "shrimp"])["safe"])
    def test_additives(self):
        d = decode_additives(["621", "ins 102", "E999"])
        self.assertEqual([x["code"] for x in d], ["E621", "E102", "E999"]); self.assertEqual(d[2]["level"], "unknown")
    def test_battle(self):
        b = battle(GREENTEA, GREENTEA0); self.assertEqual((b["winner"], b["sugar_diff_tsp"], b["price_diff_thb"]), ("greentea_zero", 10.0, 0))
    def test_battle_tie(self): self.assertEqual(battle(GREENTEA_LITE, GREENTEA_LITE)["winner"], "tie")
    def test_budget(self):
        b = budget_day(DAY); self.assertEqual((b["sugar_tsp"], b["pct"]["sugar_g"], b["over"]), (15.0, 250, ["sugar_g"]))
    def test_budget_empty(self): self.assertEqual(budget_day([])["items"], 0)
    def test_swap(self):
        s = swap_suggest(GREENTEA, CANDIDATES); self.assertEqual((s["to"], s["score_gain"], s["sugar_saved_tsp"]), ("greentea_zero", 50, 10.0))
    def test_swap_none(self): self.assertIsNone(swap_suggest(GREENTEA0, CANDIDATES))
    def test_streak(self): self.assertEqual(week_streak(WEEK), {"streak": 6, "badge": "หวานน้อย 3 วัน"})
if __name__ == "__main__": unittest.main(verbosity=1)
