import unittest
from specstry import *
from fixtures import *

class T(unittest.TestCase):
    def setUp(self):
        self.scan = face_scan(GALE_PHOTO)
        self.tryon = overlay_tryon(GALE_PHOTO, GALE_FRAME, GALE_LIFE)
        self.size = size_check(62, 136, GALE_FRAME)
        self.price = price_range(GALE_FRAME, "bkk", "single")

    def test_gale_shape(self):
        sh = self.scan["face"]
        self.assertEqual(sh["shape"], "oval")
        self.assertEqual(sh["shape_th"], "หน้าไข่")
        self.assertEqual(sh["length_to_width"], 1.36)

    def test_all_shapes(self):
        self.assertEqual(face_scan(PHOTOS[1])["face"]["shape"], "round")
        self.assertEqual(face_scan(PHOTOS[2])["face"]["shape"], "square")
        self.assertEqual(face_scan(PHOTOS[3])["face"]["shape"], "heart")
        self.assertEqual(face_scan(PHOTOS[4])["face"]["shape"], "oblong")
        self.assertEqual(face_scan(PHOTOS[5])["face"]["shape"], "diamond")

    def test_gale_quality(self):
        q = self.scan["quality"]
        self.assertEqual(q["score"], 88)
        self.assertTrue(q["ok"])
        self.assertTrue(self.scan["ok"])

    def test_quality_tips(self):
        s = face_scan(PHOTOS[6])
        self.assertEqual(s["quality"]["score"], 49)
        self.assertFalse(s["quality"]["ok"])
        self.assertTrue(s["uncertain"])
        self.assertIsNone(s["face"])
        self.assertGreaterEqual(len(s["quality"]["tips_th"]), 3)

    def test_bad_quality_input(self):
        with self.assertRaises(ValueError):
            scan_quality(1.2, 0, 0, 1, 1)

    def test_bad_measures(self):
        with self.assertRaises(ValueError):
            face_shape(0, 10, 10, 10)

    def test_pipeline(self):
        self.assertEqual(pipeline_steps(GALE_PHOTO),
                         ["face_detect", "shape_classify", "pd_estimate", "frame_tryon", "size_check", "optician_card"])
        st = pipeline_steps(PHOTOS[6])
        self.assertIn("deglare", st)
        self.assertIn("deskew", st)

    def test_library(self):
        self.assertEqual(len(FRAMES), 12)
        self.assertEqual(len(FACE_SHAPES), 6)
        self.assertEqual(len(LENS_TYPES), 5)
        for fr in FRAMES.values():
            self.assertGreater(frame_front_width(fr), 100)

    def test_pd_typical(self):
        p = pd_status(62)
        self.assertEqual(p["verdict"], "typical")

    def test_pd_check_and_range(self):
        self.assertEqual(pd_status(54)["verdict"], "check")
        self.assertEqual(pd_status(50)["verdict"], "out_of_range")
        with self.assertRaises(ValueError):
            pd_status(0)

    def test_gale_size(self):
        s = self.size
        self.assertEqual(s["verdict"], "ok")
        self.assertEqual(s["frame_front_mm"], 132)
        self.assertEqual(s["delta_mm"], -4)
        self.assertEqual(s["pd_verdict"], "typical")
        self.assertEqual(s["centres_mm"], 68)
        self.assertEqual(s["center_offset_mm"], 6)

    def test_too_narrow_wide(self):
        self.assertEqual(size_check(62, 136, "f10")["verdict"], "too_narrow")
        self.assertEqual(size_check(62, 136, "f11")["verdict"], "too_wide")

    def test_gale_tryon(self):
        t = self.tryon
        self.assertEqual(t["frame_id"], "f01")
        self.assertEqual(t["face_shape"], "oval")
        self.assertEqual(t["fit_score"], 96)
        self.assertEqual(t["size_verdict"], "ok")
        self.assertIn("ไม่ใช่การตรวจสายตา", t["disclaimer_th"])

    def test_grid_ranking(self):
        g = tryon_grid(GALE_PHOTO, GALE_GRID, "office")
        ranks = [(x["frame_id"], x["fit_score"]) for x in g["ranked"]]
        self.assertEqual(ranks[0][0], g["top_id"])
        self.assertEqual(ranks[0], ("f02", 98))
        self.assertIn(("f01", 96), ranks)
        self.assertEqual(ranks[-1][0], "f10")

    def test_compare_grid(self):
        c = compare_grid(GALE_PHOTO, ["f01", "f07", "f02"], "office")
        self.assertEqual(c["count"], 3)
        with self.assertRaises(ValueError):
            compare_grid(GALE_PHOTO, ["f01"], "office")

    def test_tryon_needs_face(self):
        with self.assertRaises(ValueError):
            overlay_tryon(PHOTOS[6], "f01")

    def test_gale_price(self):
        p = self.price
        self.assertEqual((p["mid_thb"], p["min_thb"], p["max_thb"]), (3100, 2500, 4200))

    def test_gale_quote_fair(self):
        q = quote_check(3200, "f01", "bkk", "single")
        self.assertEqual(q["verdict"], "fair")
        self.assertGreaterEqual(len(q["questions_th"]), 4)

    def test_quote_bands(self):
        self.assertEqual(quote_check(1800, "f01", "bkk")["verdict"], "low")
        self.assertEqual(quote_check(3900, "f01", "bkk")["verdict"], "high")
        self.assertEqual(quote_check(8000, "f01", "bkk")["verdict"], "very_high")

    def test_province_cheaper(self):
        self.assertLess(price_range("f01", "province")["mid_thb"], price_range("f01", "bkk")["mid_thb"])

    def test_lens_advice(self):
        a = lens_advice("progressive", 26, "office")
        self.assertTrue(a["warnings_th"])
        b = lens_advice("blue_light", 26, "office")
        self.assertTrue(any("พักสายตา" in w for w in b["warnings_th"]))

    def test_optician_card(self):
        card = optician_card(GALE, self.scan, self.tryon, self.price, self.size, GALE_NOTE)
        self.assertEqual(card["lens_width"], 48)
        self.assertEqual(card["bridge"], 20)
        self.assertEqual(card["pd_mm"], 62)
        self.assertTrue(card["line_share_url"].startswith("https://line.me/R/share?text="))
        self.assertIn("เกล", card["name_th"])

    def test_share_quota_diary(self):
        c = share_card(GALE["name_th"], self.tryon)
        self.assertIn("หน้าไข่", c["headline_th"])
        self.assertEqual(quota(1, 1)["left_after"], 1)
        self.assertTrue(quota(3, 1)["paywall"])
        self.assertFalse(quota(0, 5, pro=True)["paywall"])
        entries = [diary_entry(*e) for e in DIARY]
        s = diary_stats(entries)
        self.assertEqual(s["count"], 3)
        self.assertEqual(s["total_thb"], 5200)
        self.assertEqual(s["avg_thb"], 5200)
        self.assertEqual(diary_stats([])["count"], 0)

    def test_safety_guard(self):
        self.assertEqual(safety_guard(True)["level"], "ok")
        self.assertEqual(safety_guard(False)["level"], "stop")

    def test_frame_info(self):
        info = frame_info("f01")
        self.assertEqual(info["front_mm"], 132)
        self.assertEqual(info["material_th"], "โลหะ")
        with self.assertRaises(ValueError):
            frame_info("f99")

    def test_unknowns(self):
        with self.assertRaises(ValueError):
            price_range("f01", "mars")
        with self.assertRaises(ValueError):
            overlay_tryon(GALE_PHOTO, "f01", "space")
        with self.assertRaises(ValueError):
            diary_entry("e9", "u01", "2026-01-01", "f01", "", 0, "lost")

    def test_contrast_cool_silver(self):
        self.assertGreater(contrast_score("cool", "silver"), contrast_score("warm", "silver"))


    def test_odd_pd_photo(self):
        s = size_check(PHOTOS[7]["pd_mm"], 136, "f01")
        self.assertEqual(s["pd_verdict"], "out_of_range")

    def test_tourist_more(self):
        self.assertGreater(price_range("f01", "tourist")["mid_thb"], price_range("f01", "bkk")["mid_thb"])

    def test_progressive_costs_more(self):
        self.assertGreater(price_range("f01", "bkk", "progressive")["mid_thb"], price_range("f01", "bkk", "single")["mid_thb"])

    def test_grid_bounds(self):
        with self.assertRaises(ValueError):
            tryon_grid(GALE_PHOTO, [], "office")
        with self.assertRaises(ValueError):
            tryon_grid(GALE_PHOTO, ["f01"]*10, "office")

    def test_fit_breakdown(self):
        f = fit_score("oval", "f01", self.size, "cool", "office")
        self.assertEqual((f["face_pts"], f["size_pts"], f["lifestyle_pts"], f["score"]), (40, 30, 15, 96))

    def test_fit_mismatch_shape(self):
        f = fit_score("round", "f08", size_check(64, 136, "f08"), "warm", "fashion")
        self.assertEqual(f["face_pts"], 18)  # f08 best_shapes square/heart/diamond

    def test_shape_advice_present(self):
        for key in FACE_SHAPES:
            # trigger via known photos or constructed
            pass
        self.assertIn("เหลี่ยม", face_shape(160, 134, 136, 132)["advice_th"])
        self.assertIn("กลม", face_shape(168, 138, 140, 138)["advice_th"])

    def test_endpiece_constant(self):
        self.assertEqual(ENDPIECE_EACH, 8)
        self.assertEqual(frame_front_width(FRAMES["f05"]), 136)

    def test_single_grid(self):
        g = tryon_grid(GALE_PHOTO, ["f01"], "office")
        self.assertEqual(g["top_id"], "f01")
        self.assertEqual(g["count"], 1)

    def test_lens_unknown(self):
        with self.assertRaises(ValueError):
            lens_advice("bifocal", 40, "office")

    def test_unknown_frame_size(self):
        with self.assertRaises(ValueError):
            size_check(62, 136, "fx")
        with self.assertRaises(ValueError):
            size_check(62, 0, "f01")

    def test_quote_negative(self):
        with self.assertRaises(ValueError):
            quote_check(-1, "f01", "bkk")

    def test_share_cta(self):
        self.assertIn("SPECS", share_card("น้องเกล", self.tryon)["cta_th"])

    def test_low_conf_message(self):
        ident = identify_face(PHOTOS[6])
        self.assertFalse(ident["ok"])
        self.assertIn("ถ่ายใหม่", ident["message_th"])

if __name__ == "__main__":
    unittest.main()
