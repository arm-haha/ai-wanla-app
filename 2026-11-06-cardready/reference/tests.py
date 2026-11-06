import unittest
from cardready import *
from fixtures import *

class T(unittest.TestCase):
    def test_1inch_px(self):
        s = size_spec("1_inch")
        self.assertEqual((s["px_w"], s["px_h"], s["mm_w"], s["mm_h"]), (295, 413, 25.0, 35.0))

    def test_passport_px(self):
        s = size_spec("passport")
        self.assertEqual((s["px_w"], s["px_h"]), (413, 531))

    def test_all_presets(self):
        keys = [p["key"] for p in list_size_presets()]
        self.assertEqual(keys, ["1_inch", "2_inch", "passport", "visa", "job_th"])

    def test_unknown_size(self):
        with self.assertRaises(KeyError):
            size_spec("3_inch")

    def test_bg_white(self):
        self.assertEqual(resolve_bg_safe("white")["hex"], "#FFFFFF")

    def test_bg_gov_blue(self):
        b = resolve_bg_safe("gov_blue")
        self.assertEqual(b["hex"], "#1E4D8C")
        self.assertFalse(b["custom"])

    def test_bg_custom_hex(self):
        b = resolve_bg_safe("#a1b2c3")
        self.assertTrue(b["custom"])
        self.assertEqual(b["hex"], "#A1B2C3")

    def test_bg_bad_hex(self):
        with self.assertRaises(ValueError):
            resolve_bg_safe("#gg0000")

    def test_mint_pass_score_92(self):
        sc, lv, th = pass_score(MINT_SELFIE["mess"], soft_light_on=True, bg_removed=True, size_ok=True)
        self.assertEqual(sc, 92)
        self.assertEqual(lv, "pass")
        self.assertEqual(th, "ผ่าน")

    def test_pass_fail_raw_mess(self):
        sc, lv, _ = pass_score(MINT_SELFIE["mess"], soft_light_on=False, bg_removed=False, size_ok=False)
        self.assertLess(sc, 50)
        self.assertEqual(lv, "fail")

    def test_mess_clamped(self):
        sc, _, _ = pass_score({k: 5 for k in MESS_W}, soft_light_on=False, bg_removed=False, size_ok=False)
        self.assertEqual(sc, 0)

    def test_id_crop_mint(self):
        m = MINT_SELFIE
        box = id_crop_box(m["px_w"], m["px_h"], m["face"]["cx"], m["face"]["cy"], m["face"]["h"], "1_inch")
        self.assertEqual(box["out_px_w"], 295)
        self.assertEqual(box["out_px_h"], 413)
        self.assertLess(box["x0"], box["x1"])
        self.assertLess(box["y0"], box["y1"])
        self.assertGreaterEqual(box["x0"], 0)
        self.assertLessEqual(box["x1"], m["px_w"])

    def test_soft_light_clamped(self):
        p = soft_light_plan(0.9, blemish=0.9)
        self.assertEqual(p["strength"], SOFT_LIGHT_MAX)
        self.assertEqual(p["blemish_calm"], BLEMISH_MAX)
        self.assertFalse(p["reshape"])
        self.assertFalse(p["plastic_beauty"])
        self.assertIn("face_reshape", p["blocked"])

    def test_soft_light_zero(self):
        p = soft_light_plan(0)
        self.assertEqual(p["strength"], 0.0)

    def test_print_sheet_mint_8(self):
        lay = print_sheet_layout("1_inch", 8)
        self.assertEqual(lay["copies_placed"], 8)
        self.assertTrue(lay["cut_guides"])
        self.assertTrue(lay["dpi_check"]["ok"])
        self.assertEqual(lay["dpi_check"]["dpi"], 300)
        self.assertEqual(len(lay["positions"]), 8)

    def test_print_sheet_capacity(self):
        lay = print_sheet_layout("2_inch", 24)
        self.assertLessEqual(lay["copies_placed"], lay["capacity"])
        self.assertEqual(lay["copies_requested"], 24)

    def test_print_sheet_bad_copies(self):
        with self.assertRaises(ValueError):
            print_sheet_layout("1_inch", 0)

    def test_doc_checklist_mint_job(self):
        c = doc_checklist("job_th", MINT_SIGNALS)
        self.assertEqual(c["meter"], 100)
        self.assertEqual(c["level"], "pass")
        self.assertEqual(c["preferred_size"], "1_inch")
        self.assertIn("ไม่ใช่การรับรอง", c["disclaimer_th"])

    def test_doc_checklist_partial(self):
        sig = dict(MINT_SIGNALS); sig["formal_wear"] = False
        c = doc_checklist("job_th", sig)
        self.assertEqual(c["passed"], 5)
        self.assertEqual(c["total"], 6)
        self.assertEqual(c["meter"], 83)
        self.assertEqual(c["level"], "pass")

    def test_doc_checklist_fail(self):
        c = doc_checklist("passport", {})
        self.assertEqual(c["meter"], 0)
        self.assertEqual(c["level"], "fail")

    def test_export_pack(self):
        e = export_pack(["jpg", "png"], "1_inch", include_print_pdf=True)
        self.assertEqual(e["count"], 3)
        self.assertEqual(e["files"][0]["px_w"], 295)
        self.assertTrue(e["files"][1]["bg_alpha"])
        self.assertEqual(e["files"][2]["format"], "pdf")

    def test_export_bad_format(self):
        with self.assertRaises(ValueError):
            export_pack(["gif"], "1_inch")

    def test_share_card(self):
        c = share_card("น้องมิ้นท์", "1_inch", 92, "ขาว")
        self.assertIn("Pass 92", c["headline_th"])
        self.assertIn("3 วินาที", c["hook_th"])
        self.assertEqual(c["pass_score"], 92)

    def test_quota_free(self):
        self.assertEqual(quota(3, 4), {"allowed": 2, "left_after": 0, "paywall": True})

    def test_quota_pro(self):
        self.assertFalse(quota(99, 10, pro=True)["paywall"])

    def test_history_on_device(self):
        h = history_entry("s01", "1_inch", "white", 92, NOW)
        self.assertTrue(h["on_device"])
        self.assertEqual(h["bg"]["hex"], "#FFFFFF")

    def test_batch_family(self):
        b = batch_profiles(FAMILY_BATCH)
        self.assertEqual(b["count"], 3)

    def test_batch_max(self):
        with self.assertRaises(ValueError):
            batch_profiles([{"id": f"x{i}", "name_th": "ก", "relation_th": "ข"} for i in range(9)])

    def test_pipeline_mint(self):
        steps = pipeline_steps(MINT_SELFIE["mess"], soft_light_on=True)
        self.assertEqual(steps[0], "face_detect")
        self.assertIn("deskew", steps)
        self.assertIn("bg_remove", steps)
        self.assertIn("soft_light", steps)
        self.assertIn("color_cast_fix", steps)

    def test_dpi_check_exact(self):
        d = dpi_check(295, 413, 25.0, 35.0, min_dpi=300)
        self.assertTrue(d["ok"])
        self.assertEqual(d["dpi"], 300)

    def test_mm_to_px(self):
        self.assertEqual(mm_to_px(25.4, 300), 300)

if __name__ == "__main__":
    unittest.main(verbosity=1)
