import unittest
from hairmirror import *
from fixtures import *
class T(unittest.TestCase):
    def test_round(self): self.assertEqual(face_shape(MEAS)["shape"], "round")
    def test_oblong(self): self.assertEqual(face_shape({"face_length": 24, "forehead_w": 14, "cheek_w": 15, "jaw_w": 13})["shape"], "oblong")
    def test_heart(self): self.assertEqual(face_shape({"face_length": 20, "forehead_w": 15.5, "cheek_w": 15, "jaw_w": 12})["shape"], "heart")
    def test_diamond(self): self.assertEqual(face_shape({"face_length": 20, "forehead_w": 13, "cheek_w": 15, "jaw_w": 13})["shape"], "diamond")
    def test_square(self): self.assertEqual(face_shape({"face_length": 18, "forehead_w": 14.5, "cheek_w": 15, "jaw_w": 14.5})["shape"], "square")
    def test_oval(self): self.assertEqual(face_shape({"face_length": 20, "forehead_w": 14.5, "cheek_w": 15, "jaw_w": 13})["shape"], "oval")
    def test_bad_meas(self):
        with self.assertRaises(ValueError): face_shape({"face_length": 0, "forehead_w": 1, "cheek_w": 1, "jaw_w": 1})
    def test_upkeep(self): self.assertEqual(monthly_upkeep(STYLES[0]), 270.83)
    def test_top_two(self):
        r = rank_styles(STYLES, PROFILE, "round", 2); self.assertEqual([x["style_id"] for x in r], ["french_crop", "two_block"]); self.assertEqual(r[0]["score"], 100)
    def test_budget_penalty(self):
        r = style_match(STYLES[1], PROFILE, "round"); self.assertEqual(r["score"], 55); self.assertEqual(r["verdict"], "เสี่ยง")
    def test_wolf(self): self.assertEqual(style_match(STYLES[5], PROFILE, "round")["score"], 20)
    def test_poll(self):
        p = poll_tally(POLL, VOTES); self.assertEqual(p["total_votes"], 7); self.assertEqual(p["winner"], "two_block"); self.assertEqual(p["rows"][0]["pct"], 71.43)
    def test_poll_tie(self): self.assertTrue(poll_tally(["a", "b"], [{"voter": "x", "option": "a"}, {"voter": "y", "option": "b"}])["tie"])
    def test_poll_empty(self): p = poll_tally(["a"], []); self.assertIsNone(p["winner"]); self.assertFalse(p["tie"])
    def test_bleach(self): c = color_check(2, 6, "cool", "milk_tea"); self.assertTrue(c["needs_bleach"]); self.assertEqual(c["est_cost_thb"], 2300)
    def test_no_bleach(self): self.assertFalse(color_check(2, 4, "warm", "chocolate")["needs_bleach"])
    def test_tone_mismatch(self): self.assertFalse(color_check(3, 4, "warm", "ash")["tone_fit"])
    def test_barber(self):
        b = barber_card(STYLES[0], ZONES); self.assertEqual(b["zones"][0]["zone"], "top"); self.assertEqual(b["zones"][0]["length_mm"], 70); self.assertEqual(b["top_to_side_ratio"], 10.0)
    def test_grow(self): g = grow_out(6, 12); self.assertEqual(g["months"], 4.8); self.assertEqual(g["weeks"], 21)
    def test_grow_trim(self): self.assertTrue(grow_out(12, 6)["trim_needed"])
    def test_year(self): self.assertEqual(year_cost(STYLES[0])["year_thb"], 3249.96)
    def test_reminder(self): self.assertEqual(cut_reminder("2026-11-02", 4)["next_cut_date"], "2026-11-30")
if __name__ == "__main__": unittest.main()
