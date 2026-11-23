import math
import unittest
from sizesure import *
from fixtures import *


class T(unittest.TestCase):
    def test_tables(self):
        self.assertEqual((len(SHOES), len(GENERIC), len(KINDS), A4_CM), (17, 5, 3, (21.0, 29.7)))

    def test_photo_ok(self):
        p = PHOTOS[0]
        self.assertEqual(photo_check(p["light"], 1, 1, "fitted", 1), {"score": 97, "ok": True, "tips_th": []})

    def test_photo_mid_and_bad(self):
        self.assertEqual(photo_check(0.7, 1, 0, "normal", 0)["score"], 56)
        self.assertEqual(len(photo_check(0.4, 0, 0, "bulky", 0)["tips_th"]), 5)
        with self.assertRaises(ValueError):
            photo_check(0.5, 1, 1, "spacesuit", 1)

    def test_ellipse_circle(self):
        self.assertAlmostEqual(ellipse_circ(10, 10), math.pi * 10, places=6)

    def test_ellipse_flat(self):
        self.assertAlmostEqual(ellipse_circ(30, 22), 82.17, places=1)

    def test_measure_praew(self):
        self.assertEqual(M_PRAEW["cm"], {"chest": 84.6, "waist": 68.0, "hip": 93.6, "shoulder": 37.0, "inseam": 72.0, "sleeve": 54.0})
        self.assertEqual((M_PRAEW["margin_cm"], M_PRAEW["warnings"]), (2.0, []))

    def test_measure_a4_mismatch_and_loose(self):
        self.assertEqual(M_OAT["warnings"], ["scale_mismatch", "loose_clothes"])
        self.assertEqual(M_OAT["margin_cm"], 5.0)
        self.assertIn("9%", M_OAT["scale_note_th"])

    def test_measure_height_range(self):
        with self.assertRaises(ValueError):
            measure_body(AI_PRAEW, 260)

    def test_loose_clothes_subtract(self):
        loose = measure_body(dict(AI_PRAEW, clothing="loose"), 160)
        self.assertAlmostEqual(M_PRAEW["cm"]["waist"] - loose["cm"]["waist"], 5.0, places=1)

    def test_override_tape(self):
        m = override(M_PRAEW, {"chest": 85, "waist": 68.5, "hip": 94})
        self.assertEqual((m["source"], m["margin_cm"], m["cm"]["chest"]), ("tape", 1.0, 85))
        self.assertEqual(override(M_PRAEW, {"waist": 69})["source"], "mixed")
        with self.assertRaises(ValueError):
            override(M_PRAEW, {"neck": 33})

    def test_inch(self):
        self.assertEqual(to_inch(68.58), 27.0)

    def test_chart_flat_inch(self):
        self.assertEqual(N_SHIRT["rows"][1]["cm"]["chest"], [91.4, 91.4])   # 18" flat → ×2 ×2.54
        self.assertEqual(N_SHIRT["rows"][1]["cm"]["length"], [58.4, 58.4])  # length is not doubled
        self.assertTrue(N_SHIRT["converted"])
        self.assertEqual(N_SHIRT["kind"], "garment")

    def test_chart_body_cm(self):
        self.assertEqual((N_DRESS["kind"], N_DRESS["converted"], N_DRESS["rows"][0]["cm"]["hip"]), ("body", False, [88, 92]))

    def test_chart_bad_unit(self):
        with self.assertRaises(ValueError):
            normalize_chart({"unit": "feet", "method": "body", "rows": []})

    def test_rec_shirt(self):
        self.assertEqual((REC_SHIRT["best"], REC_SHIRT["second"], REC_SHIRT["confidence"]), ("M", "L", "high"))
        self.assertEqual(REC_SHIRT["fit"][0]["ease_cm"], 6.8)

    def test_rec_shirt_slim_vs_oversize(self):
        self.assertEqual(recommend(M_PRAEW, N_SHIRT, "top", "oversize")["best"], "XL")
        self.assertEqual(recommend(M_PRAEW, N_SHIRT, "top", "slim")["best"], "S")

    def test_rec_dress_between(self):
        self.assertEqual((REC_DRESS["best"], REC_DRESS["second"], REC_DRESS["between_sizes"]), ("M", "S", True))
        self.assertIn("คับที่สะโพก", REC_DRESS["advice_th"])

    def test_rec_jeans_stretch(self):
        self.assertEqual((REC_JEANS["best"], REC_JEANS["advice_th"]), ("27", "แนะนำไซซ์ 27 พอดีทุกจุดที่วัด"))
        self.assertIn("คับที่สะโพก", recommend(M_PRAEW, N_JEANS, "bottom", "slim", "none")["advice_th"])

    def test_rec_low_confidence(self):
        gen = {"kind": "body", "rows": [{"label": k, "cm": v} for k, v in GENERIC.items()]}
        self.assertEqual(recommend(M_OAT, gen, "top")["confidence"], "low")

    def test_rec_errors(self):
        with self.assertRaises(ValueError):
            recommend(M_PRAEW, N_SHIRT, "hat")
        with self.assertRaises(ValueError):
            recommend(M_PRAEW, {"kind": "body", "rows": [{"label": "F", "cm": {"length": [60, 60]}}]})

    def test_shoe(self):
        self.assertEqual((SHOE["foot_cm"], SHOE["shoe_cm"], SHOE["eu"], SHOE["width"]), (23.5, 24.0, 38, "regular"))

    def test_shoe_wide_and_kid(self):
        self.assertEqual(shoe_size(1080, 1188, 450)["width"], "wide")
        self.assertIsNotNone(shoe_size(700, 1188)["note_th"])
        with self.assertRaises(ValueError):
            shoe_size(2000, 1188)

    def test_passport(self):
        self.assertEqual((PP_PRAEW["top"], PP_PRAEW["jeans_waist_in"], PP_PRAEW["shoe_eu"], PP_PRAEW["share_numbers"]), ("S", 27, 38, False))

    def test_gift(self):
        self.assertEqual(gift_pick(PP_PRAEW)["size"], "S")
        self.assertEqual(gift_pick(PP_PRAEW, "top", "oversize")["size"], "M")
        self.assertEqual(gift_pick(PP_PRAEW, "shoes")["shoe_eu"], 38)

    def test_return_risk(self):
        self.assertEqual(return_risk(REC_SHIRT, True)["level"], "low")
        self.assertEqual(return_risk(REC_DRESS, False, "runs_small")["level"], "high")

    def test_log(self):
        lg = log_summary(LOG, TODAY)
        self.assertEqual((lg["entries"], lg["change_cm"]["waist"], lg["remeasure"]), (2, -1.0, False))
        self.assertEqual(log_summary(LOG, TODAY, hide_numbers=True)["change_cm"], {})
        self.assertTrue(log_summary(LOG[:1], TODAY)["remeasure"])

    def test_share_no_numbers(self):
        self.assertFalse(share_card(PP_PRAEW)["shows_numbers"])
        with self.assertRaises(ValueError):
            share_card(PP_PRAEW, "body_photo")

    def test_reel_quota(self):
        r = reel_plan(24)
        self.assertEqual((len(r["shots"]), r["shots"][-1]["end"]), (6, 24))
        self.assertTrue(quota(3)["blocked"])
        self.assertEqual(quota(1)["left"], 2)

    def test_privacy(self):
        self.assertEqual(privacy_check(15, True)["flags"], ["minor_photo"])
        self.assertFalse(privacy_check(15, True)["allowed"])
        self.assertTrue(privacy_check(15, True)["manual_entry_ok"])
        self.assertFalse(privacy_check(30, False)["allowed"])
        self.assertFalse(privacy_check(30, True, ("nudity",))["allowed"])
        self.assertEqual(privacy_check(30, True, ("loose_clothes",))["level"], "warn")
        self.assertEqual(privacy_check(28, True)["level"], "ok")

    def test_measure_without_a4(self):
        m = measure_body(dict(AI_PRAEW, a4_px=None), 160)
        self.assertEqual((m["cm"], m["scale_note_th"]), (M_PRAEW["cm"], None))

    def test_generic_chart_contiguous(self):
        rows = list(GENERIC.values())
        for a, b in zip(rows, rows[1:]):
            self.assertEqual(b["chest"][0] - a["chest"][1], 1)

    def test_chart_range_values(self):
        n = normalize_chart({"unit": "inch", "method": "body", "rows": [{"label": "M", "values": {"waist": [27, 29]}}]})
        self.assertEqual(n["rows"][0]["cm"]["waist"], [68.6, 73.7])

    def test_shoe_rounds_up_half(self):
        self.assertEqual(shoe_size(1000, 1188)["shoe_cm"], 25.5)   # 25.0 cm foot + 0.5 toe room

    def test_fit_labels_only_known(self):
        for r in (REC_SHIRT, REC_DRESS, REC_JEANS):
            self.assertTrue(all(a["label"] in ("good", "tight", "loose") for a in r["fit"]))

    def test_guard(self):
        self.assertTrue(safety_guard("body_shaming")["block"])
        self.assertFalse(safety_guard("medical_use")["block"])
        self.assertEqual(safety_guard()["level"], "ok")


if __name__ == "__main__":
    unittest.main(verbosity=1)
