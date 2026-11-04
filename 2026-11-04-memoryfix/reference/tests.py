import unittest
from memoryfix import *
from fixtures import *
P = {p["id"]: p for p in PHOTOS}
class T(unittest.TestCase):
    def test_damage_p01(self): self.assertEqual(damage_score(P["p01"]["scan"]), (52, "heavy", "หนัก"))
    def test_damage_p02(self): self.assertEqual(damage_score(P["p02"]["scan"])[0], 66)
    def test_damage_p04_light(self): self.assertEqual(damage_score(P["p04"]["scan"])[1], "light")
    def test_damage_zero(self): self.assertEqual(damage_score({}), (0, "light", "เบา"))
    def test_damage_max(self): self.assertEqual(damage_score({k: 1 for k in DAMAGE_W})[1], "severe")
    def test_damage_clamped(self): self.assertEqual(damage_score({"tears": 5})[0], 25)
    def test_plan_p01(self):
        p = P["p01"]; self.assertEqual(restore_plan(p["scan"], p["is_bw"], p["faces"], 900, skewed=True, deglare_needed=True),
            ["perspective", "deglare", "repair", "denoise", "face_enhance", "sharpen", "upscale"])
    def test_plan_p02_colorize(self): self.assertIn("colorize", restore_plan(P["p02"]["scan"], True, 2, 700))
    def test_plan_no_color_if_opt_out(self): self.assertNotIn("colorize", restore_plan(P["p02"]["scan"], True, 2, 700, want_color=False))
    def test_plan_p04_minimal(self): self.assertEqual(restore_plan(P["p04"]["scan"], False, 1, 1000), ["face_enhance", "sharpen", "upscale"])
    def test_upscale(self): self.assertEqual((upscale_factor(700), upscale_factor(900), upscale_factor(2000), upscale_factor(300)), (4, 2, 1, 4))
    def test_print_p02_raw(self): o = print_options(700, 980); self.assertFalse(o["4x6"]["ok"]); self.assertEqual(o["4x6"]["dpi"], 163)
    def test_print_after_upscale(self): o = print_options(2800, 3920); self.assertTrue(o["8x10"]["ok"]); self.assertTrue(o["A4"]["ok"])
    def test_print_p03(self): o = print_options(2400, 1600); self.assertTrue(o["5x7"]["ok"]); self.assertTrue(o["8x10"]["ok"]); self.assertFalse(o["A4"]["ok"])
    def test_timeline(self):
        t = timeline(PHOTOS); self.assertEqual([g["decade"] for g in t], [1960, 1980, 1990, None]); self.assertEqual(t[2]["ids"], ["p03", "p04"])
    def test_timeline_label(self): self.assertEqual(timeline(PHOTOS)[0]["label_th"], "ยุค 2503s (ค.ศ. 1960s)")
    def test_people(self): self.assertEqual(list(people_index(PHOTOS).items())[0], ("แม่", ["p01", "p03"]))
    def test_then_now(self): self.assertEqual(then_now_caption("แม่", 1989, 2026), "แม่ ปี 2532 → 2569 (37 ปี)")
    def test_quota_free(self): self.assertEqual(quota(2, 3), {"allowed": 1, "left_after": 0, "paywall": True})
    def test_quota_pro(self): self.assertFalse(quota(10, 5, pro=True)["paywall"])
    def test_motion(self):
        self.assertFalse(motion_allowed("minor", True)); self.assertTrue(motion_allowed("deceased", True)); self.assertFalse(motion_allowed("living", False))
    def test_share(self): c = share_card("ตายายวันแต่งงาน", 66, 64, ["repair", "colorize", "sharpen"]); self.assertEqual(c["badges"], ["repair", "colorize"]); self.assertIn("64 ปี", c["headline_th"])
if __name__ == "__main__": unittest.main(verbosity=1)
