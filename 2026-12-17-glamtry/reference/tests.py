import unittest
from glamtry import *
from fixtures import *


class T(unittest.TestCase):
    def test_scan_ok(self):
        q = selfie_scan(PHOTOS[0])["quality"]
        self.assertEqual((q["score"], q["ok"], q["tips_th"]), (92, True, []))

    def test_scan_filter_penalty(self):
        q = selfie_scan(PHOTOS[1])["quality"]
        self.assertEqual((q["score"], q["ok"], len(q["tips_th"])), (53, False, 2))

    def test_scan_bad(self):
        q = selfie_scan(PHOTOS[2])["quality"]
        self.assertEqual((q["score"], len(q["tips_th"])), (38, 3))
        with self.assertRaises(ValueError):
            scan_quality(1.5, 0, 0)

    def test_consent_ok(self):
        self.assertEqual((CONSENT["allowed"], CONSENT["level"], CONSENT["flags"]), (True, "ok", []))

    def test_consent_under_13(self):
        c = consent_check(12, True)
        self.assertEqual((c["allowed"], c["flags"]), (False, ["under_13"]))

    def test_consent_not_own_and_celebrity(self):
        c = consent_check(25, False, celebrity_match=True)
        self.assertEqual((c["allowed"], c["flags"]), (False, ["not_own_photo", "celebrity"]))

    def test_consent_multiple_faces_warn(self):
        c = consent_check(20, True, faces=3)
        self.assertEqual((c["allowed"], c["level"]), (True, "warn"))

    def test_consent_no_face_and_whitening(self):
        self.assertFalse(consent_check(20, True, faces=0)["allowed"])
        self.assertIn("whitening_request", consent_check(20, True, whitening_request=True)["flags"])

    def test_shade_demo(self):
        self.assertEqual((SHADE["depth"], SHADE["undertone"], SHADE["shade_code"], SHADE["confidence"]), ("light", "warm", "2W", 0.85))
        self.assertTrue(SHADE["is_estimate"])

    def test_shade_variety(self):
        cases = {(240, 215, 200): "1C", (205, 170, 150): "2N", (180, 150, 95): "3W", (150, 110, 85): "4N", (110, 75, 60): "5N", (200, 190, 150): "2O"}
        for rgb, code in cases.items():
            self.assertEqual(shade_match(rgb)["shade_code"], code, rgb)

    def test_shade_low_light_conf(self):
        s = shade_match((205, 170, 150), 40)
        self.assertLess(s["confidence"], 0.6)
        self.assertIn("ถ่ายใหม่", s["tip_th"])

    def test_shade_bad(self):
        with self.assertRaises(ValueError):
            shade_match((300, 10, 10))
        with self.assertRaises(ValueError):
            shade_match((10, 10))

    def test_six_looks(self):
        self.assertEqual([s["look"] for s in LOOKS6], ["natural", "korean_glass", "thai_bride", "party_glam", "office", "y2k"])

    def test_spec_prompt_guardrails(self):
        for w in ("no skin whitening", "no face slimming", "no celebrity likeness", "own selfie"):
            self.assertIn(w, SPEC["image_prompt"])
        self.assertEqual(SPEC["title_th"], "เกาหลีผิวฉ่ำ · 15 นาที")

    def test_palette_undertone_shift(self):
        self.assertEqual(look_palette("korean_glass", "neutral")["lip_hex"], "#E06A7A")
        self.assertEqual(SPEC["palette"]["lip_hex"], "#E06C71")
        self.assertNotEqual(look_palette("office", "cool")["lip_hex"], look_palette("office", "warm")["lip_hex"])

    def test_intensity(self):
        self.assertLess(look_palette("y2k", intensity="soft")["opacity"], look_palette("y2k", intensity="full")["opacity"])
        with self.assertRaises(ValueError):
            look_palette("y2k", intensity="extreme")

    def test_look_bad(self):
        with self.assertRaises(ValueError):
            look_spec("goth", "light", "warm")
        with self.assertRaises(ValueError):
            look_spec("natural", "pale", "warm")

    def test_tutorial_demo(self):
        self.assertEqual((len(TUT["steps"]), TUT["total_minutes"], TUT["simplified"]), (7, 14, False))
        self.assertEqual(TUT["steps"][0]["n"], 1)

    def test_tutorial_simplified_for_beginner(self):
        t = tutorial("party_glam", skill=1)
        self.assertTrue(t["simplified"])
        self.assertNotIn("false_lashes", [s["item"] for s in t["steps"]])

    def test_tutorial_colors(self):
        lip = [s for s in TUT["steps"] if s["area"] == "lip"][0]
        self.assertEqual(lip["color_hex"], SPEC["palette"]["lip_hex"])

    def test_kit_demo(self):
        self.assertEqual((KIT["low_baht"], KIT["high_baht"], KIT["save_vs_premium_baht"]), (584, 1284, 11516))
        self.assertEqual(KIT["skipped_owned"], ["concealer"])

    def test_kit_tiers_order(self):
        for lk in LOOKS:
            self.assertLess(budget_kit(lk, "budget")["high_baht"], budget_kit(lk, "mid")["low_baht"] * 2)
            self.assertLess(budget_kit(lk, "mid")["high_baht"], budget_kit(lk, "premium")["high_baht"])

    def test_kit_bride_premium(self):
        self.assertEqual(budget_kit("thai_bride", "premium")["high_baht"], 23300)
        self.assertEqual((budget_kit("natural")["low_baht"], budget_kit("natural")["high_baht"]), (415, 925))

    def test_kit_no_brands(self):
        self.assertIn("ไม่ได้อ้างอิงแบรนด์", KIT["disclaimer_th"])
        with self.assertRaises(ValueError):
            budget_kit("natural", "luxury")

    def test_occasion_demo(self):
        self.assertEqual((PLAN["days_left"], PLAN["look"], len(PLAN["timeline"])), (10, "korean_glass", 3))
        self.assertIn("setting_spray", PLAN["touch_up_kit"])
        self.assertIsNone(PLAN["warning_th"])

    def test_occasion_last_minute(self):
        p = occasion_plan("interview", TODAY, TODAY, hot_humid=False)
        self.assertEqual((p["look"], p["touch_up_kit"], len(p["timeline"])), ("office", [], 1))
        self.assertIsNotNone(p["warning_th"])

    def test_occasion_bad(self):
        with self.assertRaises(ValueError):
            occasion_plan("party", "2026-12-01", TODAY)
        with self.assertRaises(ValueError):
            occasion_plan("funeral_party", "2026-12-20", TODAY)

    def test_patch_demo(self):
        self.assertEqual(PATCH["level"], "warn")
        self.assertTrue(any("24–48" in s for s in PATCH["steps_th"]))
        self.assertIn("ไม่ใช่คำแนะนำทางการแพทย์", PATCH["note_th"])

    def test_patch_info_and_allergy(self):
        self.assertEqual(patch_test(["lip_tint"])["level"], "info")
        p = patch_test(["lipstick"], known_allergies=("น้ำหอม",))
        self.assertEqual(p["level"], "warn"); self.assertIn("น้ำหอม", p["steps_th"][-1])

    def test_reel(self):
        self.assertEqual(REEL["shots"][-1]["to_s"], 20)
        self.assertEqual([s["kind"] for s in REEL["shots"]], ["before", "scan", "swipe", "compare", "cta"])
        self.assertIn("GLAM", REEL["shots"][-1]["text_th"])
        with self.assertRaises(ValueError):
            reel_plan(SPEC, 45)

    def test_reel_contiguous(self):
        r = reel_plan(SPEC, 30)
        for a, b in zip(r["shots"], r["shots"][1:]):
            self.assertEqual(a["to_s"], b["from_s"])

    def test_diary(self):
        d = diary_summary(DIARY, "2027-01-05")
        self.assertEqual((d["looks_saved"], d["top_look"], d["spend_baht"]), (2, "korean_glass", 388))
        self.assertEqual(d["replace_soon"][0], {"item": "mascara", "replace_by": "2027-03-19", "days_left": 73})

    def test_diary_bad(self):
        with self.assertRaises(ValueError):
            diary_summary([], TODAY)
        with self.assertRaises(ValueError):
            diary_summary([{"date": TODAY, "kind": "sell"}], TODAY)

    def test_share(self):
        c = share_card(SPEC, "เซลฟี่เดียว ลองแต่งหน้าก่อนซื้อ")
        self.assertEqual(c["layout"], "selfie_before_after")
        self.assertIn("GLAM", c["cta_th"])

    def test_quota(self):
        self.assertEqual(quota(0), {"allowed": 1, "left_after": 2, "paywall": False})
        self.assertTrue(quota(3)["paywall"])
        self.assertIsNone(quota(9, pro=True)["left_after"])

    def test_guard(self):
        self.assertEqual(safety_guard()["level"], "ok")
        for f in ("not_own_photo", "celebrity", "under_13", "whitening_request"):
            self.assertEqual(safety_guard(f)["level"], "stop", f)
        with self.assertRaises(ValueError):
            safety_guard("x")

    def test_tables_complete(self):
        self.assertEqual(len(LOOKS), 6)
        for k, lk in LOOKS.items():
            for c in ("lip", "blush", "eye"):
                self.assertRegex(lk[c], r"^#[0-9A-F]{6}$", k)
            for i in lk["items"]:
                self.assertIn(i, ITEMS, k); self.assertIn(i, ("blotting_paper",) + tuple(ITEMS))
        for k, v in ITEMS.items():
            for t in TIERS:
                self.assertLess(v[t][0], v[t][1], k)


if __name__ == "__main__":
    unittest.main(verbosity=1)
