import unittest
from riperight import *
from fixtures import *


class T(unittest.TestCase):
    def test_scan_ok(self):
        q = fruit_scan(PHOTOS[0])["quality"]
        self.assertEqual((q["score"], q["ok"], q["tips_th"]), (94, True, []))

    def test_scan_bad(self):
        q = fruit_scan(PHOTOS[2])["quality"]
        self.assertEqual((q["score"], q["ok"], len(q["tips_th"])), (49, False, 3))

    def test_scan_range(self):
        with self.assertRaises(ValueError):
            scan_quality(1.2, 0, 0)

    def test_weights_sum_to_one(self):
        for f in FRUITS:
            self.assertAlmostEqual(sum(FRUITS[f]["w"]), 1.0, places=6, msg=f)

    def test_avocado_demo_waits(self):
        self.assertEqual((AVO["stage"], AVO["days_to_perfect"], AVO["eat_within_days"], AVO["score"]), ("unripe", 3, 5, 32))
        self.assertIn("3 วัน", AVO["headline_th"])

    def test_mango_perfect(self):
        self.assertEqual((MANGO["stage"], MANGO["score"], MANGO["eat_within_days"]), ("perfect", 75, 2))
        self.assertEqual(MANGO["confidence"], 0.95)

    def test_banana_spots_overripe(self):
        self.assertEqual(BANANA["stage"], "overripe")
        self.assertEqual(BANANA["eat_within_days"], 0)
        self.assertIn("สมูทตี้", BANANA["headline_th"])

    def test_heavy_spots_force_overripe(self):
        self.assertEqual(ripeness("mango", 0.2, 0.65, "firm")["stage"], "overripe")

    def test_missing_cues_renormalised(self):
        a = ripeness("mango", 0.5, 0.0)
        self.assertEqual(a["index"], round((0.45 * 0.5) / 0.55, 3))
        self.assertEqual(a["cues_used"], ["color", "spots"])

    def test_knock_ripe_demo(self):
        self.assertEqual((MELON_KNOCK["verdict"], MELON_KNOCK["cue"]), ("ripe", 0.75))
        self.assertEqual((MELON["stage"], MELON["score"]), ("perfect", 66))

    def test_knock_adds_certainty(self):
        self.assertEqual(MELON_NOKNOCK["stage"], "almost")
        self.assertIn("knock", MELON["cues_used"])
        self.assertGreater(MELON["confidence"], MELON_NOKNOCK["confidence"])

    def test_watermelon_does_not_ripen_after_pick(self):
        self.assertFalse(MELON_NOKNOCK["ripens_after_pick"])
        self.assertEqual((MELON_NOKNOCK["days_to_perfect"], MELON_NOKNOCK["eat_within_days"]), (0, 0))
        self.assertIn("เลือกลูกอื่น", MELON_NOKNOCK["headline_th"])

    def test_knock_verdicts(self):
        self.assertEqual(knock_test("watermelon", 300, 100)["verdict"], "unripe")
        self.assertEqual(knock_test("watermelon", 100, 90)["verdict"], "almost")
        self.assertEqual(knock_test("watermelon", 70, 50)["verdict"], "overripe")
        self.assertEqual(knock_test("durian", 75, 200)["verdict"], "ripe")

    def test_knock_only_some_fruits(self):
        with self.assertRaises(ValueError):
            knock_test("mango", 120, 100)
        with self.assertRaises(ValueError):
            ripeness("mango", 0.5, 0.1, knock=0.5)

    def test_knock_range(self):
        with self.assertRaises(ValueError):
            knock_test("watermelon", 5, 100)

    def test_ripeness_bad_inputs(self):
        for a in (("kiwi", 0.5, 0.1), ("mango", 1.5, 0.1), ("mango", 0.5, 0.1, "squishy"), ("mango", 0.5, 0.1, None, "stinky"), ("mango", True, 0.1)):
            with self.assertRaises(ValueError):
                ripeness(*a)

    def test_every_fruit_monotonic_with_color(self):
        for f in FRUITS:
            lo, hi = ripeness(f, 0.1, 0.0)["index"], ripeness(f, 0.9, 0.0)["index"]
            self.assertLess(lo, hi, f)

    def test_price_demo_fair(self):
        p = price_check("watermelon", 80, 3.2, MONTH)
        self.assertEqual((p["per_kg"], p["verdict"], p["in_season"], p["diff_from_mid_pct"]), (25.0, "fair", True, 11))

    def test_price_off_season(self):
        p = price_check("durian", 900, 3.0, 12)
        self.assertEqual((p["in_season"], p["ref_low"], p["ref_high"], p["verdict"]), (False, 168, 252, "pricey"))
        self.assertEqual(price_check("durian", 450, 3.0, 5)["verdict"], "fair")

    def test_price_verdict_ladder(self):
        v = [price_check("watermelon", x, 1, 12)["verdict"] for x in (8, 12, 20, 35, 50)]
        self.assertEqual(v, ["suspicious_low", "cheap", "fair", "pricey", "very_pricey"])

    def test_price_bad(self):
        with self.assertRaises(ValueError):
            price_check("watermelon", 0, 1, 12)
        with self.assertRaises(ValueError):
            price_check("watermelon", 50, 1, 13)

    def test_storage_speed_up(self):
        s = storage_plan("avocado", "unripe", "speed_up")
        self.assertEqual((s["where"], s["speed_factor"]), ("paper_bag", 0.7))
        self.assertIn("กล้วย", s["steps_th"][0])

    def test_storage_banana_no_fridge(self):
        s = storage_plan("banana", "almost", "slow_down")
        self.assertEqual(s["where"], "counter")
        self.assertIn("ห้ามแช่ตู้เย็น", s["steps_th"][0])

    def test_storage_fridge_when_ripe(self):
        self.assertEqual(storage_plan("mango", "perfect", "slow_down")["where"], "fridge")
        self.assertEqual(storage_plan("mango", "unripe", "slow_down")["where"], "counter")

    def test_storage_watermelon_no_speedup(self):
        self.assertIn("ไม่สุกต่อ", storage_plan("watermelon", "almost", "speed_up")["steps_th"][0])

    def test_eat_plan_demo(self):
        p = eat_plan(BASKET, TODAY)
        self.assertEqual(p["eat_first"], "มะม่วง")
        self.assertEqual(p["days"][0]["eat"], ["มะม่วง", "แตงโม"])
        self.assertEqual(p["days"][0]["waiting"], ["อะโวคาโด"])
        self.assertEqual((p["days"][3]["date"], p["days"][3]["eat"]), ("2026-12-17", ["อะโวคาโด"]))

    def test_eat_plan_bad(self):
        with self.assertRaises(ValueError):
            eat_plan([], TODAY)
        with self.assertRaises(ValueError):
            eat_plan(BASKET, TODAY, 30)

    def test_pick_check(self):
        self.assertEqual(pick_check("watermelon", [True, True, True, False])["verdict"], "pick")
        self.assertEqual(pick_check("durian", [True, False, True, False])["verdict"], "maybe")
        self.assertEqual(pick_check("mango", [False, False, True, False])["verdict"], "skip")
        with self.assertRaises(ValueError):
            pick_check("mango", [True, True])

    def test_every_fruit_has_checklist(self):
        for f in FRUITS:
            self.assertEqual(len(CHECKLISTS[f]), 4)

    def test_season_december(self):
        c = season_calendar(12)
        self.assertEqual(c["fruits"], ["banana", "watermelon", "papaya", "pineapple"])
        self.assertIn("แตงโม", c["fruits_th"])
        self.assertIn("durian", season_calendar(5)["fruits"])

    def test_diary(self):
        s = diary_summary(DIARY)
        self.assertEqual((s["count"], s["accuracy_pct"], s["spent_baht"], s["top_fruit"]), (4, 75, 405, "avocado"))
        with self.assertRaises(ValueError):
            diary_summary([])

    def test_share(self):
        c = share_card(AVO, "ถ่ายปุ๊บ รู้เลยกินได้วันไหน")
        self.assertEqual(c["layout"], "fruit_meter")
        self.assertIn("อะโวคาโด", c["title_th"])
        self.assertIn("RIPE", c["cta_th"])

    def test_quota(self):
        self.assertEqual(quota(0), {"allowed": 1, "left_after": 4, "paywall": False})
        self.assertTrue(quota(5)["paywall"])
        self.assertIsNone(quota(9, pro=True)["left_after"])

    def test_guard(self):
        self.assertEqual(safety_guard()["level"], "ok")
        self.assertEqual(safety_guard("mold")["level"], "stop")
        self.assertEqual(safety_guard("durian_alcohol")["level"], "warn")
        with self.assertRaises(ValueError):
            safety_guard("unknown")

    def test_disclaimer_everywhere(self):
        for f in FRUITS:
            self.assertIn("ไม่ใช่การรับรอง", ripeness(f, 0.5, 0.1)["disclaimer_th"])


if __name__ == "__main__":
    unittest.main(verbosity=1)
