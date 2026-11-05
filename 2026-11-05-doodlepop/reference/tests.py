import unittest
from doodlepop import *
from fixtures import *
D = {d["id"]: d for d in DRAWINGS}; K = {k["id"]: k for k in KIDS}
class T(unittest.TestCase):
    def test_scan_d06(self): self.assertEqual(scan_score(D["d06"]["scan"]), (82, "great", "ชัดมาก"))
    def test_scan_d01_ok(self): self.assertEqual(scan_score(D["d01"]["scan"]), (74, "ok", "ใช้ได้"))
    def test_scan_d05_retake(self): self.assertEqual(scan_score(D["d05"]["scan"])[1], "retake"); self.assertIn("ตัดขอบ", retake_reason(D["d05"]["scan"]))
    def test_scan_perfect(self): self.assertEqual(scan_score({}), (100, "great", "ชัดมาก")); self.assertIsNone(retake_reason({}))
    def test_scan_clamped(self): self.assertEqual(scan_score({"blur": 9})[0], 65)
    def test_cleanup_d06(self): self.assertEqual(cleanup_steps(D["d06"]["scan"]), ["perspective", "deshadow", "remove_paper", "fill_gaps", "cutout"])
    def test_cleanup_minimal(self): self.assertEqual(cleanup_steps(D["d04"]["scan"]), ["remove_paper", "fill_gaps", "cutout"])
    def test_rig_dino_all_six(self): r = rig(D["d06"]["parts"]); self.assertEqual(r["presets"], PRESETS); self.assertEqual(r["bones"], 12); self.assertEqual(r["fallbacks"], {})
    def test_rig_whale_fallbacks(self): r = rig(D["d05"]["parts"]); self.assertEqual(r["fallbacks"], {"wave": "wiggle", "walk": "hop"}); self.assertEqual(len(r["presets"]), 6)
    def test_rig_no_body(self): self.assertTrue(rig({"head": 1})["needs_manual_pins"])
    def test_clip_dance(self): self.assertEqual(clip("dance")["frames"], 96)
    def test_export_reel(self): e = export_spec("reel_mp4", 15, 4.0); self.assertEqual((e["w"], e["h"], e["loops"], e["frames"]), (1080, 1920, 4, 450)); self.assertEqual(e["watermark"], WATERMARK)
    def test_export_gif_capped(self): e = export_spec("gif", 10, 4.0); self.assertEqual((e["duration_s"], e["frames"], e["music"]), (6, 72, False))
    def test_story_age5(self): self.assertEqual(story_plan(5, 3), {"pages": 5, "words_per_page": 40, "total_words": 200, "narration_s": 125})
    def test_story_ages(self): self.assertEqual((story_plan(3, 1)["pages"], story_plan(8, 2)["pages"]), (4, 6))
    def test_story_too_many(self): self.assertRaises(ValueError, story_plan, 5, 4)
    def test_age(self): self.assertEqual(age_at("2021-06-15", "2026-11-04")["label_th"], "5 ขวบ 4 เดือน"); self.assertEqual(age_at("2021-06-15", "2026-06-14")["years"], 4)
    def test_gallery(self): self.assertEqual(gallery(DRAWINGS, "k01"), ["d06", "d05", "d03", "d02", "d01"])
    def test_recap_2026(self): r = year_recap(DRAWINGS, K["k01"], 2026); self.assertEqual((r["count"], r["first_detail"], r["last_detail"], r["growth_pct"]), (3, 76, 96, 26))
    def test_recap_empty(self): self.assertIsNone(year_recap(DRAWINGS, K["k02"], 2025))
    def test_sticker(self):
        self.assertEqual(fit_box(2480, 3300), (240, 320)); self.assertEqual(len(sticker_pack(["d06", "d02"], PRESETS, 8)), 8); self.assertRaises(ValueError, sticker_pack, ["d06"], PRESETS, 10)
    def test_daily_prompt_no_repeat(self): self.assertEqual(daily_prompt(TODAY, PROMPT_HISTORY), "เพื่อนจากดาวอังคาร"); self.assertNotIn(daily_prompt("2026-11-04", [("2026-11-04", "เพื่อนจากดาวอังคาร")]), ["เพื่อนจากดาวอังคาร"])
    def test_share_link(self): l = share_link(TODAY); self.assertEqual(l["expires_on"], "2026-11-12"); self.assertTrue(l["view_only"] and l["strip_location"])
    def test_print(self):
        self.assertTrue(print_check(2480, 3300, "poster_a4")["ok"]); self.assertFalse(print_check(1240, 1650, "tshirt")["ok"]); self.assertEqual(print_check(2480, 3300, "mug")["dpi"], 419)
    def test_parent_gate(self):
        self.assertFalse(parent_gate("export_video", False)["allowed"]); self.assertTrue(parent_gate("animate", False)["allowed"]); self.assertTrue(parent_gate("grandparent_link", True)["allowed"])
    def test_quota(self): self.assertEqual(quota("animate", 2, 3), {"kind": "animate", "allowed": 1, "left_after": 0, "paywall": True}); self.assertTrue(quota("story", 1, 1)["paywall"])
    def test_share_card(self): c = share_card(D["d06"], K["k01"], "5 ขวบ 4 เดือน", "dance"); self.assertIn("เต้น", c["headline_th"]); self.assertFalse(c["shows_child_face"])
if __name__ == "__main__": unittest.main(verbosity=1)
