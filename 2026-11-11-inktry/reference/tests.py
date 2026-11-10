import unittest
from inktry import *
from fixtures import *

class T(unittest.TestCase):
    def setUp(self):
        self.scan = skin_scan(MINT_PHOTO)
        self.tryon = overlay_tryon(MINT_PHOTO, MINT_DESIGN, MINT_PLACEMENT, MINT_SIZE, MINT_MODE)
        self.price = price_range(MINT_SIZE, "fine_line", "bkk", MINT_MODE, MINT_PLACEMENT)
        self.age5 = aging_preview("fine_line", MINT_MODE, MINT_PLACEMENT, 5, MINT_SIZE)

    # 1) Skin scan + placement
    def test_mint_scan(self):
        self.assertEqual([p["placement"] for p in self.scan["placements"]], ["inner_forearm"])
        self.assertEqual(self.scan["uncertain"], ["wrist"])
        self.assertEqual(self.scan["placement_count"], 1)
        self.assertEqual(self.scan["undertone"], "warm")

    def test_mint_quality(self):
        q = self.scan["quality"]
        self.assertEqual(q["score"], 88)
        self.assertTrue(q["ok"])
        self.assertEqual(q["tips_th"], [])

    def test_quality_tips(self):
        s = skin_scan(PHOTOS[3])
        self.assertEqual(s["quality"]["score"], 58)
        self.assertFalse(s["quality"]["ok"])
        self.assertGreaterEqual(len(s["quality"]["tips_th"]), 2)

    def test_no_skin(self):
        s = skin_scan(PHOTOS[6])
        self.assertFalse(s["quality"]["ok"])
        self.assertEqual(s["placement_count"], 0)
        self.assertTrue(any("ผิว" in t for t in s["quality"]["tips_th"]))

    def test_bad_quality_input(self):
        with self.assertRaises(ValueError):
            scan_quality(1.5, 0, 0, 1)

    def test_unknown_placement(self):
        with self.assertRaises(ValueError):
            identify_placement({"id": "x", "detections": [{"placement": "forehead", "confidence": 1}]})

    def test_pipeline(self):
        self.assertEqual(pipeline_steps(MINT_PHOTO),
                         ["skin_detect", "placement_classify", "overlay", "size_check", "aging_preview", "artist_card"])
        st = pipeline_steps(PHOTOS[3])
        self.assertIn("deglare", st)
        self.assertIn("deskew", st)

    def test_library_counts(self):
        self.assertEqual(len(PLACEMENTS), 15)
        self.assertEqual(len(STYLES), 10)
        self.assertEqual(len(DESIGNS), 12)
        self.assertEqual(len(set(v["id"] for v in PLACEMENTS.values())), 15)
        self.assertEqual(len(set(v["id"] for v in STYLES.values())), 10)

    # 2) Size + try-on
    def test_mint_size(self):
        c = size_check(MINT_PLACEMENT, MINT_SIZE)
        self.assertEqual((c["band"], c["band_th"], c["verdict"]), ("small", "เล็ก", "ok"))
        self.assertEqual((c["min_cm"], c["max_cm"]), (4, 18))
        self.assertTrue(c["in_range"])

    def test_too_small_and_big(self):
        self.assertEqual(size_check("inner_forearm", 3)["verdict"], "too_small")
        self.assertEqual(size_check("wrist", 12)["verdict"], "too_big")
        self.assertEqual(size_check("finger", 2)["verdict"], "ok")

    def test_size_zero(self):
        with self.assertRaises(ValueError):
            size_check("wrist", 0)

    def test_mint_tryon(self):
        t = self.tryon
        self.assertEqual(t["design_id"], "d01")
        self.assertEqual(t["style"], "fine_line")
        self.assertEqual(t["contrast"], 80)
        self.assertEqual(t["size_verdict"], "ok")
        self.assertTrue(t["placement_matched"])
        self.assertIn("ภาพจำลอง", t["disclaimer_th"])

    def test_blackwork_rejects_color(self):
        with self.assertRaises(ValueError):
            overlay_tryon(PHOTOS[2], "d09", "upper_arm", 12, "color")

    def test_watercolor_rejects_bw(self):
        with self.assertRaises(ValueError):
            overlay_tryon(MINT_PHOTO, "d07", "inner_forearm", 8, "bw")

    def test_min_charge_tiny(self):
        p = price_range(2, "minimal", "province", "bw", "behind_ear")
        self.assertEqual(p["min_thb"], 1500)
        self.assertGreaterEqual(p["mid_thb"], 1500)

    def test_wrist_wrap_note(self):
        c = size_check("wrist", 5)
        self.assertIn("โค้ง", c["wrap_th"])
        c2 = size_check("inner_forearm", 8)
        self.assertIn("เรียบ", c2["wrap_th"])

    def test_unknown_flag(self):
        with self.assertRaises(ValueError):
            safety_from_flags(["laser"], 28)

    # 3) Color vs BW
    def test_mint_variants(self):
        v = color_variants("d01", "warm", "inner_forearm", 8)
        self.assertEqual(v["best_mode"], "bw")
        self.assertEqual([x["color_mode"] for x in v["variants"]], ["bw", "color"])
        self.assertEqual(v["variants"][0]["contrast"], 80)
        self.assertEqual(v["variants"][1]["contrast"], 76)
        self.assertTrue(v["variants"][0]["recommended"])

    def test_contrast_cool_color(self):
        self.assertGreater(contrast_score("cool", "color", "floral"), contrast_score("warm", "color", "floral"))

    # 4) Aging preview
    def test_mint_aging(self):
        a1 = aging_preview("fine_line", "bw", "inner_forearm", 1, 8)
        a5 = self.age5
        a10 = aging_preview("fine_line", "bw", "inner_forearm", 10, 8)
        self.assertEqual((a1["fade_pct"], a1["spread_mm"], a1["sharpness_left"]), (12, 0.2, 88))
        self.assertEqual((a5["fade_pct"], a5["spread_mm"], a5["sharpness_left"]), (60, 0.98, 40))
        self.assertEqual((a10["fade_pct"], a10["spread_mm"], a10["sharpness_left"]), (90, 1.95, 10))
        self.assertIn("ซีด", a5["look_th"])

    def test_hand_fades_faster(self):
        arm = aging_preview("fine_line", "bw", "inner_forearm", 5, 8)
        hand = aging_preview("fine_line", "bw", "hand", 5, 8)
        self.assertGreater(hand["fade_pct"], arm["fade_pct"])
        self.assertEqual(hand["fade_pct"], 90)

    def test_color_fades_faster(self):
        bw = aging_preview("fine_line", "bw", "inner_forearm", 5, 8)
        col = aging_preview("fine_line", "color", "inner_forearm", 5, 8)
        self.assertGreater(col["fade_pct"], bw["fade_pct"])

    def test_aging_bad_years(self):
        with self.assertRaises(ValueError):
            aging_preview("fine_line", "bw", "inner_forearm", 0, 8)

    # 5) Pain + aftercare
    def test_pain_forearm(self):
        g = pain_guide("inner_forearm")
        self.assertEqual((g["pain"], g["level"], g["heal_days"]), (4, "low", 14))

    def test_pain_ribs_high(self):
        g = pain_guide("ribs")
        self.assertEqual((g["pain"], g["level"]), (8, "high"))

    def test_aftercare_steps(self):
        g = aftercare_guide()
        self.assertEqual(len(g["steps"]), 6)
        self.assertEqual(g["steps"][0]["n"], 1)

    # 6) Price + quote
    def test_mint_price(self):
        p = self.price
        self.assertEqual((p["mid_thb"], p["min_thb"], p["max_thb"]), (3200, 2550, 4500))

    def test_mint_quote_fair(self):
        q = quote_check(3500, 8, "fine_line", "bkk", "bw", "inner_forearm")
        self.assertEqual(q["verdict"], "fair")
        self.assertGreaterEqual(len(q["questions_th"]), 5)

    def test_quote_bands(self):
        self.assertEqual(quote_check(1800, 8, "fine_line", "bkk", "bw")["verdict"], "low")
        self.assertEqual(quote_check(4300, 8, "fine_line", "bkk", "bw")["verdict"], "high")
        self.assertEqual(quote_check(8000, 8, "fine_line", "bkk", "bw")["verdict"], "very_high")

    def test_province_cheaper(self):
        bkk = price_range(8, "fine_line", "bkk", "bw")
        prov = price_range(8, "fine_line", "province", "bw")
        self.assertLess(prov["mid_thb"], bkk["mid_thb"])

    def test_tourist_color_more(self):
        p = price_range(16, "traditional", "tourist", "color", "upper_arm")
        self.assertGreaterEqual(p["min_thb"], 1500)
        self.assertGreater(p["max_thb"], p["min_thb"])

    # 7) Artist card
    def test_artist_card(self):
        card = artist_card(MINT, self.tryon, self.price, self.age5, MINT_FLAGS, MINT_NOTE)
        self.assertTrue(card["can_book"])
        self.assertEqual(card["budget_min_thb"], 2550)
        self.assertEqual(card["aging_5y_fade_pct"], 60)
        self.assertTrue(card["line_share_url"].startswith("https://line.me/R/share?text="))
        self.assertIn("มิ้นต์", card["line_share_url"] + card["name_th"])

    def test_keloid_blocks_booking(self):
        rec = safety_from_flags(["keloid"], 33)
        self.assertEqual(rec["level"], "red")
        self.assertFalse(rec["can_book"])
        card = artist_card(PEOPLE[3], self.tryon, self.price, self.age5, ["keloid"])
        self.assertFalse(card["can_book"])

    def test_under_18(self):
        rec = safety_from_flags([], 16)
        self.assertEqual(rec["level"], "red")
        self.assertFalse(rec["can_book"])

    def test_blood_thinner_warn(self):
        rec = safety_from_flags(["blood_thinner"], 41)
        self.assertEqual(rec["level"], "yellow")
        self.assertTrue(rec["can_book"])

    # 8) Share, quota, diary, safety
    def test_share_card(self):
        c = share_card(MINT["name_th"], self.tryon, self.age5)
        self.assertEqual(c["layout"], "tryon_result")
        self.assertIn("1080x1350", c["sizes"])
        self.assertIn("60%", c["hook_th"])

    def test_quota(self):
        self.assertEqual(quota(1, 1), {"allowed": 1, "left_after": 1, "paywall": False})
        self.assertEqual(quota(3, 1), {"allowed": 0, "left_after": 0, "paywall": True})
        self.assertEqual(quota(0, 5, pro=True), {"allowed": 5, "left_after": None, "paywall": False})

    def test_diary_stats(self):
        entries = [diary_entry(*e) for e in DIARY]
        s = diary_stats(entries)
        self.assertEqual(s["count"], 3)
        self.assertEqual(s["total_thb"], 2200)
        self.assertEqual(s["avg_thb"], 2200)
        self.assertEqual(s["last_date"], "2026-11-20")
        empty = diary_stats([])
        self.assertEqual(empty["count"], 0)

    def test_safety_guard(self):
        self.assertEqual(safety_guard("red")["level"], "stop")
        self.assertEqual(safety_guard("yellow")["level"], "warn")
        self.assertEqual(safety_guard("green")["level"], "ok")

    def test_design_and_placement_info(self):
        d = design_info("d01")
        self.assertEqual(d["style"], "fine_line")
        self.assertTrue(d["bw_ok"])
        p = placement_info("hand")
        self.assertEqual(p["id"], "pl13")
        with self.assertRaises(ValueError):
            design_info("d99")

    def test_unknown_style_region(self):
        with self.assertRaises(ValueError):
            price_range(8, "tribal", "bkk", "bw")
        with self.assertRaises(ValueError):
            price_range(8, "fine_line", "mars", "bw")

if __name__ == "__main__":
    unittest.main()
