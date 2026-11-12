import unittest
from cakedream import *
from fixtures import *


class T(unittest.TestCase):
    def test_scan_ok(self):
        q = ref_scan(PHOTOS[0])["quality"]
        self.assertEqual((q["score"], q["ok"], q["tips_th"]), (94, True, []))

    def test_scan_bad(self):
        q = ref_scan(PHOTOS[2])["quality"]
        self.assertEqual((q["score"], q["ok"], len(q["tips_th"])), (49, False, 3))

    def test_scan_range(self):
        with self.assertRaises(ValueError):
            scan_quality(1.2, 0, 0)

    def test_servings_demo(self):
        self.assertEqual((GUESTS["servings_needed"], GUESTS["pounds"], GUESTS["diameter_in"]), (14, 2, 8))
        self.assertIn("18 คน", GUESTS["headline_th"])

    def test_servings_appetite(self):
        self.assertEqual(serving_calc(8, 10, "dessert_lovers")["pounds"], 3)
        self.assertEqual(serving_calc(8, 10, "light")["pounds"], 2)
        self.assertEqual(serving_calc(8, 10, leftovers=True)["pounds"], 3)
        self.assertEqual(serving_calc(4, 2, "light")["pounds"], 1)

    def test_servings_tiers(self):
        self.assertEqual(serving_calc(30, 0)["shape"], "tier2")
        self.assertEqual(serving_calc(50, 0)["shape"], "tier3")
        with self.assertRaises(ValueError):
            serving_calc(80, 0)

    def test_servings_bad(self):
        for a in ((0, 0), (-1, 3), (2, 2, "huge")):
            with self.assertRaises(ValueError):
                serving_calc(*a)

    def test_glyphs_thai(self):
        self.assertEqual(glyphs("น้องภูมิ"), 5)
        self.assertEqual(glyphs("HBD"), 3)

    def test_message_fit_demo(self):
        m = DINO["message"]
        self.assertEqual((m["glyphs"], m["limit_per_line"], m["lines"], m["fits"]), (13, 20, 1, True))

    def test_message_two_lines(self):
        m = message_fit("สุขสันต์วันเกิดคุณแม่ที่รักที่สุดในโลก", 1)
        self.assertEqual((m["limit_per_line"], m["lines"]), (15, 2))

    def test_message_too_long(self):
        m = message_fit("ก" * 40, 0.5)
        self.assertFalse(m["fits"])
        self.assertIn("ตัดให้เหลือ", m["tip_th"])

    def test_message_empty(self):
        with self.assertRaises(ValueError):
            message_fit("  ", 2)

    def test_design_demo(self):
        self.assertEqual((DINO["complexity"], DINO["diameter_in"], DINO["theme_th"]), (3, 8, "ไดโนเสาร์"))
        self.assertIn("8-inch dinosaur", DINO["image_prompt"])
        self.assertIn("no logos", DINO["image_prompt"])

    def test_design_complexity_caps(self):
        d = design_spec("princess", "chocolate", 5, "Happy 60", 3)
        self.assertEqual(d["complexity"], 4)
        self.assertIn("2-tier", d["image_prompt"])
        self.assertEqual(design_spec("korean_minimal", "thai_tea", 1, "รักนะ")["complexity"], 1)

    def test_design_bad(self):
        for a in (("robot", "chocolate", 1, "x"), ("unicorn", "durian", 1, "x"), ("unicorn", "chocolate", 7, "x"), ("unicorn", "chocolate", 1, "x", 9)):
            with self.assertRaises(ValueError):
                design_spec(*a)

    def test_price_demo(self):
        e = price_estimate(DINO)
        self.assertEqual((e["low"], e["mid"], e["high"], e["per_serving"]), (1100, 1300, 1620, 93))

    def test_price_region(self):
        self.assertLess(price_estimate(DINO, "province")["mid"], price_estimate(DINO, "metro")["mid"])
        with self.assertRaises(ValueError):
            price_estimate(DINO, "mars")

    def test_fair_demo(self):
        f = fair_price(price_estimate(DINO), 1250)
        self.assertEqual((f["verdict"], f["diff_from_mid_pct"]), ("fair", -4))

    def test_fair_ladder(self):
        e = price_estimate(DINO)
        got = [fair_price(e, q)["verdict"] for q in (700, 1000, 1500, 2000, 2600)]
        self.assertEqual(got, ["suspicious_low", "cheap", "fair", "pricey", "very_pricey"])
        with self.assertRaises(ValueError):
            fair_price(e, 0)

    def test_allergy_ok(self):
        a = allergy_guard("vanilla_chiffon", ["nuts"])
        self.assertEqual((a["level"], a["hits"]), ("ok", []))

    def test_allergy_nuts_stop(self):
        a = allergy_guard("almond_crunch", ["nuts"])
        self.assertEqual(a["level"], "stop")
        self.assertNotIn("almond_crunch", a["alternatives"])

    def test_allergy_egg_warn(self):
        a = allergy_guard("chocolate", ["egg"])
        self.assertEqual((a["level"], a["alternatives"]), ("warn", ["eggless_choc"]))

    def test_allergy_bad(self):
        with self.assertRaises(ValueError):
            allergy_guard("chocolate", ["shellfish"])

    def test_deadline_demo(self):
        d = order_deadline(PARTY, 3, TODAY)
        self.assertEqual((d["order_by"], d["days_left"], d["status"]), ("2026-12-16", 5, "ok"))

    def test_deadline_last_call_and_late(self):
        self.assertEqual(order_deadline("2026-12-14", 3, TODAY)["status"], "last_call")
        self.assertEqual(order_deadline("2026-12-12", 4, TODAY)["status"], "too_late")

    def test_diy_demo(self):
        r = diy_recipe(2, "vanilla_chiffon")
        self.assertEqual((r["total_cost_baht"], r["bake_minutes"]), (151, 43))
        self.assertEqual([i["qty"] for i in r["ingredients"]][:3], [180, 220, 8])

    def test_diy_half(self):
        self.assertEqual(diy_recipe(0.5, "vanilla_chiffon")["bake_minutes"], 25)
        with self.assertRaises(ValueError):
            diy_recipe(2, "chocolate")

    def test_order_card(self):
        c = order_card(PEOPLE[0], DINO, GUESTS, price_estimate(DINO), allergy_guard("vanilla_chiffon", []), order_deadline(PARTY, 3, TODAY))
        self.assertIn("HBD น้องภูมิ 5 ขวบ", c["share_text"])
        self.assertIn("฿1,100–1,620", c["share_text"])
        self.assertEqual(len(c["lines_th"]), 7)

    def test_order_card_allergy_line(self):
        c = order_card(PEOPLE[1], design_spec("unicorn", "chocolate", 1, "Nan"), serving_calc(5, 0), price_estimate(DINO),
                       allergy_guard("chocolate", ["egg"]), order_deadline(PARTY, 3, TODAY))
        self.assertIn("⚠️", c["lines_th"][-1])

    def test_diary(self):
        s = diary_summary(DIARY)
        self.assertEqual((s["count"], s["spent_baht"], s["avg_stars"], s["top_theme"]), (3, 3000, 4.7, "football"))
        with self.assertRaises(ValueError):
            diary_summary([])

    def test_share(self):
        c = share_card(DINO, "จากไอเดีย เป็นภาพเค้กใน 10 วิ")
        self.assertEqual(c["layout"], "idea_to_mockup")
        self.assertIn("ไดโนเสาร์", c["title_th"])

    def test_quota(self):
        self.assertEqual(quota(0), {"allowed": 1, "left_after": 2, "paywall": False})
        self.assertTrue(quota(3)["paywall"])
        self.assertIsNone(quota(9, pro=True)["left_after"])

    def test_guard(self):
        self.assertEqual(safety_guard()["level"], "ok")
        self.assertEqual(safety_guard("real_brand")["level"], "stop")
        self.assertIn("ถั่ว", safety_guard("nuts")["message_th"])

    def test_every_theme_prices(self):
        for t in THEMES:
            e = price_estimate(design_spec(t, "vanilla_chiffon", 1, "HBD"))
            self.assertTrue(e["low"] < e["mid"] < e["high"])

    def test_every_size_capacity_monotonic(self):
        caps = [SIZES[k][2] for k in sorted(SIZES)]
        self.assertEqual(caps, sorted(caps))


if __name__ == "__main__":
    unittest.main(verbosity=1)
