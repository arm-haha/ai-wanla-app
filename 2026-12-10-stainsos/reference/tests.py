import unittest
from stainsos import *
from fixtures import *


class T(unittest.TestCase):
    def setUp(self):
        self.risk = risk_meter(TEA)
        self.plan = rescue_plan(TEA, PRAE_KIT)

    def test_scan_ok(self):
        q = photo_scan(PHOTOS[0])["quality"]
        self.assertEqual((q["score"], q["ok"], q["tips_th"]), (91, True, []))

    def test_scan_bad_tips(self):
        q = photo_scan(PHOTOS[3])["quality"]
        self.assertEqual(q["score"], 46)
        self.assertFalse(q["ok"])
        self.assertEqual(len(q["tips_th"]), 3)

    def test_scan_range(self):
        with self.assertRaises(ValueError):
            scan_quality(1.5, 0, 0)

    def test_parse_demo(self):
        self.assertFalse(TEA["needs_confirm"])
        self.assertEqual(TEA["cls"], "tannin")
        self.assertIn("ชาไทย", TEA["message_th"])

    def test_low_conf_blocks_plan(self):
        self.assertTrue(LOW["needs_confirm"])
        self.assertIn("ห้ามเริ่ม", LOW["message_th"])
        with self.assertRaises(ValueError):
            rescue_plan(LOW, PRAE_KIT)

    def test_parse_bad(self):
        for bad in (dict(TEA_RAW, stain="glitter"), dict(TEA_RAW, fabric="leather"), dict(TEA_RAW, color="pink"),
                    dict(TEA_RAW, size_cm=0), dict(TEA_RAW, age_hours=-1), dict(TEA_RAW, confidence=1.1)):
            with self.assertRaises(ValueError):
                parse_stain(bad)

    def test_risk_demo(self):
        self.assertEqual((self.risk["score"], self.risk["level"], self.risk["expected_fade_pct"]), (50, "medium", 70))
        self.assertFalse(self.risk["dry_clean"])

    def test_risk_curry_hard(self):
        r = risk_meter(CURRY)
        self.assertEqual((r["score"], r["level"], r["dry_clean"]), (75, "hard", False))

    def test_risk_silk_pro(self):
        r = risk_meter(INK_SILK)
        self.assertEqual((r["score"], r["level"]), (100, "pro"))
        self.assertTrue(r["dry_clean"])

    def test_age_steps(self):
        scores = [risk_meter(parse_stain(dict(TEA_RAW, age_hours=h)))["score"] for h in (0.5, 2, 10, 48, 100)]
        self.assertEqual(scores, [45, 50, 57, 65, 75])

    def test_size_and_color(self):
        self.assertEqual(risk_meter(parse_stain(dict(TEA_RAW, size_cm=8)))["score"], 55)
        self.assertEqual(risk_meter(parse_stain(dict(TEA_RAW, size_cm=11)))["score"], 60)
        self.assertEqual(risk_meter(parse_stain(dict(TEA_RAW, color="colored")))["score"], 55)

    def test_delicate_threshold(self):
        r = risk_meter(parse_stain(dict(TEA_RAW, fabric="rayon", age_hours=0.5)))  # 45+15=60
        self.assertEqual(r["score"], 60)
        self.assertTrue(r["dry_clean"])
        r2 = risk_meter(parse_stain(dict(TEA_RAW, stain="mud", fabric="rayon", age_hours=0.5)))  # 45
        self.assertFalse(r2["dry_clean"])

    def test_fade_bounds(self):
        self.assertEqual(risk_meter(parse_stain(dict(TEA_RAW, stain="mud", age_hours=0)))["expected_fade_pct"], 82)
        self.assertEqual(risk_meter(INK_SILK)["expected_fade_pct"], 40)

    def test_plan_demo(self):
        self.assertEqual(self.plan["step_count"], 5)
        self.assertEqual(self.plan["total_minutes"], 36)
        self.assertEqual(self.plan["items_used"], ["dish_soap", "oxygen_bleach", "water"])
        self.assertEqual(self.plan["shopping_list"], [])

    def test_plan_first_step_blot(self):
        self.assertIn("ห้ามขยี้", self.plan["steps"][0]["action_th"])
        self.assertIn("อบ", self.plan["steps"][-1]["action_th"])

    def test_substitute_vinegar(self):
        p = rescue_plan(TEA, ["dish_soap", "white_vinegar"])
        soak = [s for s in p["steps"] if s["item"] == "oxygen_bleach"][0]
        self.assertTrue(soak["missing"])
        self.assertEqual(soak["substitute"], "white_vinegar")
        self.assertEqual(p["shopping_list"], [])

    def test_shopping_list(self):
        p = rescue_plan(TEA, [])
        self.assertEqual(p["shopping_list"], ["dish_soap", "oxygen_bleach"])

    def test_ink_sanitizer_sub(self):
        p = rescue_plan(parse_stain(dict(INK_SILK_RAW, fabric="cotton", age_hours=0.5)), ["hand_sanitizer", "dish_soap"])
        self.assertIn("hand_sanitizer", p["items_used"])
        self.assertEqual(p["shopping_list"], [])

    def test_oil_cornstarch_sub(self):
        p = rescue_plan(parse_stain(dict(TEA_RAW, stain="oil")), ["cornstarch", "dish_soap"])
        self.assertIn("cornstarch", p["items_used"])

    def test_curry_sun_step(self):
        p = rescue_plan(CURRY, PRAE_KIT)
        self.assertTrue(any("ตากแดด" in s["action_th"] for s in p["steps"]))
        self.assertTrue(any("ตะเข็บ" in w for w in p["warnings_th"]))

    def test_blood_cold_warning(self):
        p = rescue_plan(BLOOD, PRAE_KIT)
        self.assertTrue(any("ห้ามใช้น้ำร้อน" in w for w in p["warnings_th"]))
        self.assertIn("น้ำเย็น", p["steps"][1]["action_th"])

    def test_dry_clean_plan(self):
        p = rescue_plan(INK_SILK, PRAE_KIT)
        self.assertTrue(p["dry_clean"])
        self.assertEqual(p["step_count"], 3)
        self.assertIn("ซักแห้ง", p["steps"][-1]["action_th"])

    def test_delicate_no_oxygen(self):
        p = rescue_plan(parse_stain(dict(TEA_RAW, stain="mud", fabric="silk", age_hours=0.5, size_cm=2)), PRAE_KIT)
        self.assertNotIn("oxygen_bleach", [s["item"] for s in p["steps"]])

    def test_mud_needs_brush(self):
        p = rescue_plan(MUD, PRAE_KIT)
        self.assertEqual(p["shopping_list"], ["brush"])
        self.assertEqual(p["total_minutes"], 37)

    def test_plan_never_chlorine(self):
        for raw in (TEA_RAW, CURRY_RAW, BLOOD_RAW, MUD_RAW, INK_SILK_RAW):
            p = rescue_plan(parse_stain(raw), list(ITEMS))
            self.assertNotIn("chlorine_bleach", p["items_used"])
            self.assertEqual(safety_check(p["items_used"])["level"], "ok")

    def test_safety_danger(self):
        s = safety_check(["chlorine_bleach", "white_vinegar", "dish_soap"])
        self.assertEqual(s["level"], "danger")
        self.assertIn("ก๊าซคลอรีน", s["message_th"])

    def test_safety_multi(self):
        s = safety_check(["chlorine_bleach", "ammonia", "alcohol"])
        self.assertEqual(len(s["pairs"]), 2)
        self.assertEqual(len(safety_check(["hydrogen_peroxide", "white_vinegar"])["pairs"]), 1)

    def test_safety_ok(self):
        self.assertEqual(safety_check(PRAE_KIT)["level"], "ok")

    def test_care_label_shirt(self):
        c = care_label(SHIRT_LABEL)
        self.assertEqual((c["max_wash_c"], c["bleach"], c["dryer_ok"], c["dry_clean_only"]), (40, "oxygen_only", True, False))

    def test_care_label_silk(self):
        c = care_label(SILK_LABEL)
        self.assertEqual((c["max_wash_c"], c["bleach"], c["dryer_ok"]), (30, "none", False))

    def test_care_label_bad(self):
        with self.assertRaises(ValueError):
            care_label([])
        with self.assertRaises(ValueError):
            care_label(["wash_95"])

    def test_dry_clean_only(self):
        self.assertTrue(care_label(["no_wash", "dry_clean"])["dry_clean_only"])

    def test_plan_fits_label(self):
        self.assertTrue(plan_fits_label(self.plan, care_label(SHIRT_LABEL))["ok"])
        f = plan_fits_label(self.plan, care_label(["wash_30", "no_bleach"]))
        self.assertFalse(f["ok"])
        self.assertIn("ข้ามขั้นแช่ผงฟอก", f["issues_th"][0])

    def test_kit_check(self):
        k = kit_check(PRAE_KIT)
        self.assertEqual((k["ready_count"], k["total"]), (6, 8))
        self.assertNotIn("ink", k["ready_for"])
        self.assertEqual(k["headline_th"], "ชุดในบ้านพร้อมรับมือ 6/8 คราบ")

    def test_kit_full(self):
        self.assertEqual(kit_check(PRAE_KIT + ["alcohol", "brush"])["ready_count"], 8)

    def test_diary(self):
        d = diary_summary(DIARY)
        self.assertEqual((d["removed"], d["faded"], d["success_rate_pct"], d["saved_baht"]), (3, 1, 60, 1770))
        self.assertIn("฿1,770", d["headline_th"])
        with self.assertRaises(ValueError):
            diary_summary([])

    def test_share_card(self):
        c = share_card("เสื้อนักศึกษาขาว", "ชาไทย", 70)
        self.assertIn("70%", c["hook_th"])
        self.assertIn("STAIN", c["cta_th"])
        self.assertEqual(c["watermark"], WATERMARK)

    def test_quota(self):
        self.assertEqual(quota(0, 1), {"allowed": 1, "left_after": 2, "paywall": False})
        self.assertEqual(quota(3, 1), {"allowed": 0, "left_after": 0, "paywall": True})
        self.assertEqual(quota(9, 5, pro=True)["paywall"], False)
        with self.assertRaises(ValueError):
            quota(-1, 1)

    def test_pipeline(self):
        self.assertEqual(pipeline_steps(PHOTOS[0], TEA), ["stain_photo", "parse_stain", "risk_meter", "rescue_plan", "safety_check"])
        self.assertIn("deglare", pipeline_steps(PHOTOS[3], TEA))
        self.assertEqual(pipeline_steps(PHOTOS[0], LOW)[-1], "ask_user_confirm")

    def test_safety_guard(self):
        self.assertEqual(safety_guard()["level"], "ok")
        self.assertEqual(safety_guard("danger")["level"], "stop")
        self.assertIn("ทดสอบมุมด้านใน", DISCLAIMER_TH)


if __name__ == "__main__":
    unittest.main(verbosity=1)
