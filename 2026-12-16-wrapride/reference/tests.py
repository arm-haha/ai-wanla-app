import unittest
from wrapride import *
from fixtures import *


class T(unittest.TestCase):
    def test_scan_ok(self):
        q = vehicle_scan(PHOTOS[0])["quality"]
        self.assertEqual((q["score"], q["ok"], q["tips_th"]), (94, True, []))

    def test_scan_bad(self):
        q = vehicle_scan(PHOTOS[2])["quality"]
        self.assertEqual((q["score"], q["ok"], len(q["tips_th"])), (49, False, 3))

    def test_scan_range(self):
        with self.assertRaises(ValueError):
            scan_quality(0, 1.2, 0)

    def test_swatch_matte(self):
        sw = finish_swatch("mint_green", "matte")
        self.assertEqual((sw["base_hex"], sw["highlight_hex"], sw["shadow_hex"]), ("#7FD1AE", "#8ED7B8", "#66A78B"))

    def test_swatch_gloss_brighter_than_matte(self):
        g = int(finish_swatch("candy_red", "gloss")["highlight_hex"][1:3], 16)
        m = int(finish_swatch("candy_red", "matte")["highlight_hex"][1:3], 16)
        self.assertGreater(g, m)

    def test_swatch_color_shift(self):
        self.assertIn("shift_hex", finish_swatch("sky_blue", "color_shift"))
        self.assertNotIn("shift_hex", finish_swatch("sky_blue", "gloss"))

    def test_swatch_bad(self):
        with self.assertRaises(ValueError):
            finish_swatch("rainbow", "gloss")
        with self.assertRaises(ValueError):
            finish_swatch("mint_green", "glitter")

    def test_wrap_spec_demo(self):
        self.assertEqual(SPEC["title_th"], "อีโคคาร์ เขียวมิ้นต์ ด้าน + ดำ")
        self.assertTrue(SPEC["main_color_change"])
        for w in ("headlights", "licence plate", "no logos"):
            self.assertIn(w, SPEC["image_prompt"])

    def test_two_tone_default_accent(self):
        self.assertEqual(wrap_spec("sedan", "candy_red", "gloss", "two_tone")["accent_color"], "deep_black")

    def test_same_family_no_main_change(self):
        self.assertFalse(wrap_spec("sedan", "pearl_white", "gloss", "full", original_family="white")["main_color_change"])

    def test_partial_no_main_change(self):
        self.assertFalse(wrap_spec("sedan", "deep_black", "gloss", "roof")["main_color_change"])

    def test_wrap_spec_bad(self):
        with self.assertRaises(ValueError):
            wrap_spec("tank", "mint_green", "matte")
        with self.assertRaises(ValueError):
            wrap_spec("sedan", "mint_green", "matte", "wheels")

    def test_rims_demo(self):
        self.assertEqual((RIMS["rim_inch"], RIMS["ok"], RIMS["stickers"]), (15, True, ["side_stripe"]))

    def test_rims_block_lights(self):
        r = rim_sticker_spec("sedan", stickers=["checker"], areas=["door", "headlight", "plate"])
        self.assertEqual((r["ok"], r["blocked_areas"]), (False, ["headlight", "plate"]))

    def test_rims_max_stickers(self):
        with self.assertRaises(ValueError):
            rim_sticker_spec("sedan", stickers=["kanok", "checker", "pinstripe", "side_stripe"])

    def test_price_demo_fair(self):
        self.assertEqual((PRICE["low_baht"], PRICE["high_baht"], PRICE["verdict"]), (19000, 38000, "fair"))

    def test_price_scooter_full(self):
        p = price_check("scooter", "wrap")
        self.assertEqual((p["low_baht"], p["high_baht"], p["verdict"]), (2500, 6000, "no_quote"))

    def test_price_chrome_more(self):
        self.assertGreater(price_check("sedan", "wrap", "chrome")["low_baht"], price_check("sedan", "wrap", "gloss")["high_baht"])

    def test_price_roof_cheaper(self):
        self.assertLess(price_check("suv", "wrap", coverage="roof")["high_baht"], price_check("suv", "wrap")["low_baht"])

    def test_price_verdicts(self):
        self.assertEqual(price_check("sedan", "wrap", quote_baht=12000)["verdict"], "suspicious_low")
        self.assertEqual(price_check("sedan", "wrap", quote_baht=44000)["verdict"], "high")
        self.assertEqual(price_check("scooter", "wrap", quote_baht=9000)["verdict"], "too_high")

    def test_price_rims(self):
        self.assertEqual((RIM_PRICE["low_baht"], RIM_PRICE["high_baht"]), (9000, 27000))
        self.assertEqual(price_check("big_bike", "rims")["low_baht"], 2000)

    def test_price_stickers(self):
        p = price_check("eco_car", "stickers", stickers=2)
        self.assertEqual((p["low_baht"], p["high_baht"]), (1800, 4800))

    def test_price_paint_vs_wrap(self):
        self.assertGreater(price_check("sedan", "paint")["high_baht"], price_check("sedan", "wrap")["high_baht"])

    def test_price_bad(self):
        with self.assertRaises(ValueError):
            price_check("sedan", "tint")
        with self.assertRaises(ValueError):
            price_check("sedan", "wrap", quote_baht=-5)

    def test_brief(self):
        self.assertIn("#7FD1AE", BRIEF["text_th"])
        self.assertIn("15\" 5 ก้าน สีดำ", BRIEF["text_th"])
        self.assertIn("฿19,000–฿38,000", BRIEF["text_th"])
        self.assertTrue(any("ไม่ติดทับไฟ" in l for l in BRIEF["lines_th"]))

    def test_legal_main_change(self):
        self.assertEqual(LEGAL["level"], "action")
        self.assertEqual([i["code"] for i in LEGAL["items"]], ["dlt_color", "insurance", "lights_plate"])
        self.assertIn("กรมการขนส่งทางบก", LEGAL["items"][0]["text_th"])

    def test_legal_partial_info(self):
        self.assertEqual(legal_check(wrap_spec("sedan", "deep_black", "gloss", "roof"))["level"], "info")

    def test_legal_chrome_warn(self):
        l = legal_check(wrap_spec("sedan", "cement_grey", "chrome", "full", original_family="grey"))
        self.assertEqual(l["level"], "warn")
        self.assertIn("reflective", [i["code"] for i in l["items"]])

    def test_legal_no_numbers(self):
        for i in LEGAL["items"]:
            self.assertFalse(any(ch.isdigit() for ch in i["text_th"]), i["code"])

    def test_reel(self):
        self.assertEqual(REEL["shots"][-1]["to_s"], 20)
        self.assertEqual([s["kind"] for s in REEL["shots"]], ["before", "scan", "swipe", "compare", "cta"])
        self.assertIn("WRAP", REEL["shots"][-1]["text_th"])
        with self.assertRaises(ValueError):
            reel_plan(SPEC, 60)

    def test_reel_contiguous(self):
        r = reel_plan(SPEC, 30)
        for a, b in zip(r["shots"], r["shots"][1:]):
            self.assertEqual(a["to_s"], b["from_s"])

    def test_diary(self):
        d = diary_summary(DIARY, TODAY)
        self.assertEqual((d["wrap_age_days"], d["next_wash"], d["spend_baht"]), (6, "2026-12-28", 38650))
        self.assertIn("สัปดาห์แรก", d["care_tip_th"])

    def test_diary_bad(self):
        with self.assertRaises(ValueError):
            diary_summary([], TODAY)
        with self.assertRaises(ValueError):
            diary_summary([{"date": TODAY, "kind": "race"}], TODAY)

    def test_share(self):
        c = share_card(SPEC, "เบื่อสีรถเดิม? ลองสีใหม่ใน 10 วิ")
        self.assertEqual(c["layout"], "car_before_after")
        self.assertIn("WRAP", c["cta_th"])

    def test_quota(self):
        self.assertEqual(quota(0), {"allowed": 1, "left_after": 4, "paywall": False})
        self.assertTrue(quota(5)["paywall"])
        self.assertIsNone(quota(9, pro=True)["left_after"])

    def test_guard(self):
        self.assertEqual(safety_guard()["level"], "ok")
        self.assertEqual(safety_guard("covers_lights")["level"], "stop")
        self.assertEqual(safety_guard("plate_visible")["level"], "warn")
        with self.assertRaises(ValueError):
            safety_guard("x")

    def test_tables_complete(self):
        for k, v in VEHICLES.items():
            for f in ("wrap", "paint"):
                self.assertLess(v[f][0], v[f][1], k)
        for k, c in COLORS.items():
            self.assertRegex(c["hex"], r"^#[0-9A-F]{6}$", k)
        self.assertGreaterEqual(len(COLORS), 12)


if __name__ == "__main__":
    unittest.main(verbosity=1)
