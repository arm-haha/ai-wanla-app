import unittest
from handfont import *
from fixtures import *


class T(unittest.TestCase):
    def test_sets_sizes(self):
        self.assertEqual((len(TH_CONS), len(TH_TONE), len(LAT_UPPER), len(TH_DIGITS)), (44, 4, 26, 10))

    def test_template_quick(self):
        self.assertEqual(len(template_chars("thai_quick")), 72)
        self.assertEqual(template_sheet("thai_quick")["pages"], 1)

    def test_template_bilingual_pages(self):
        t = template_sheet("bilingual")
        self.assertEqual((t["cells"], t["pages"]), (161, 3))

    def test_template_unknown(self):
        with self.assertRaises(ValueError):
            template_chars("klingon")

    def test_scan_ok(self):
        self.assertEqual(sheet_scan(PHOTOS[0])["quality"], {"score": 94, "ok": True, "tips_th": []})

    def test_scan_mid(self):
        q = sheet_scan(PHOTOS[1])["quality"]
        self.assertEqual((q["score"], q["ok"], len(q["tips_th"])), (58, False, 2))

    def test_scan_bad_and_range(self):
        self.assertEqual(len(sheet_scan(PHOTOS[2])["quality"]["tips_th"]), 4)
        with self.assertRaises(ValueError):
            scan_quality(1.2, 0, 0, 1)

    def test_glyph_status(self):
        st = lambda **k: glyph_check(dict(char="ก", **k))["status"]
        self.assertEqual(st(ink=0.0, touches_border=False, extra_blobs=0), "empty")
        self.assertEqual(st(ink=0.02, touches_border=False, extra_blobs=0), "too_faint")
        self.assertEqual(st(ink=0.1, touches_border=True, extra_blobs=0), "overflow")
        self.assertEqual(st(ink=0.1, touches_border=False, extra_blobs=3), "messy")
        self.assertEqual(st(ink=0.5, touches_border=False, extra_blobs=0), "messy")
        self.assertEqual(st(ink=0.1, touches_border=False, extra_blobs=0), "ok")

    def test_coverage_demo(self):
        self.assertEqual((COV["usable"], COV["percent"], COV["missing"], COV["can_build"]), (69, 96, ["ฃ", "ฬ", "ๆ"], True))

    def test_coverage_blocks_build(self):
        half = [glyph_check(dict(c, ink=0.0)) if i % 2 else glyph_check(c) for i, c in enumerate(CELLS)]
        cv = coverage("thai_quick", half)
        self.assertFalse(cv["can_build"])
        b = font_build(PEOPLE[0], "thai_quick", cv, STYLE)
        self.assertEqual((b["ok"], b["size_kb"]), (False, 0))

    def test_build_demo(self):
        self.assertEqual((BUILD["family"], BUILD["glyphs"], BUILD["alternates"], BUILD["size_kb"]), ("HandFont-Mint", 69, 138, 256))

    def test_build_formats(self):
        self.assertLess(font_build(PEOPLE[0], "thai_quick", COV, STYLE, "woff2")["size_kb"], BUILD["size_kb"])
        with self.assertRaises(ValueError):
            font_build(PEOPLE[0], "thai_quick", COV, STYLE, "exe")

    def test_font_name_sanitised(self):
        self.assertEqual(font_name("bai toey!!"), "HandFont-Baitoey")
        self.assertEqual(font_name("***"), "HandFont-Me")

    def test_clusters(self):
        c = clusters("ที่นี่")
        self.assertEqual([x["base"] for x in c], ["ท", "น"])
        self.assertEqual(c[0]["marks"], ["\u0e35", "\u0e48"])

    def test_tone_low_without_upper(self):
        m = mark_placement("ก", ["\u0e48"])["marks"][0]
        self.assertEqual((m["dx"], m["dy"]), (0, 0))

    def test_tone_high_with_upper(self):
        m = mark_placement("ท", ["\u0e35", "\u0e48"])["marks"][1]
        self.assertEqual(m["dy"], 18)

    def test_ascender_shift(self):
        m = mark_placement("ป", ["\u0e35"])["marks"][0]
        self.assertEqual(m["dx"], -12)

    def test_descender_lower_vowel(self):
        self.assertEqual(mark_placement("ฎ", ["\u0e38"])["marks"][0]["dy"], -10)
        self.assertTrue(mark_placement("ญ", ["\u0e38"])["cut_descender"])
        self.assertFalse(mark_placement("ญ", ["\u0e48"])["cut_descender"])

    def test_style(self):
        s = style_params("bold", -5, "clean")
        self.assertEqual((s["stroke"], s["alternates"], s["baseline_jitter"]), (7, 1, 0))
        with self.assertRaises(ValueError):
            style_params(slant=30)
        with self.assertRaises(ValueError):
            style_params(weight="heavy")

    def test_alternates_cycle(self):
        self.assertEqual(pick_alternates("aaaa b", 3), [0, 1, 2, 0, 0, 0])

    def test_preview_thai(self):
        p = text_preview(MSG, STYLE)
        self.assertEqual((p["line_count"], p["lines"][0]), (2, "สุขสันต์วันครูนะคะ"))

    def test_preview_english_wrap(self):
        p = text_preview("Happy birthday my dear friend see you soon", STYLE, max_width_mm=60)
        self.assertEqual(p["line_count"], 3)

    def test_card_teacher(self):
        c = card_layout("teacher", MSG)
        self.assertEqual((c["fits"], c["font_pt"], c["ink_hex"]), (True, 28, "#1F3FBF"))

    def test_card_too_long(self):
        c = card_layout("shop_note", "ขอบคุณ" * 20)
        self.assertEqual((c["fits"], c["font_pt"]), (False, 18))
        with self.assertRaises(ValueError):
            card_layout("birthday", "hi", paper="gold")

    def test_sticker(self):
        s = sticker_export("555 ขำมาก")
        self.assertTrue(s["transparent"]); self.assertEqual(s["height_px"], 360)

    def test_practice_sheet(self):
        self.assertEqual(practice_sheet("กขค")["guide_lines"], 4)
        self.assertEqual(practice_sheet("abc", 3, "copy")["opacity"], 0.0)
        with self.assertRaises(ValueError):
            practice_sheet("ก", 20)

    def test_practice_score(self):
        p = practice_score(SAMPLES)
        self.assertEqual((p["score"], p["grade"], p["focus"]), (83, "B", "spacing_var"))
        with self.assertRaises(ValueError):
            practice_score([])

    def test_diary(self):
        d = diary_summary(DIARY, "2026-12-22")
        self.assertEqual((d["fonts_built"], d["practice_streak"], d["improvement"], d["latest_version"]), (2, 3, 11, 2))

    def test_diary_streak_broken(self):
        self.assertEqual(diary_summary(DIARY, "2026-12-24")["practice_streak"], 0)

    def test_reel(self):
        r = reel_plan("HandFont-Mint", 24)
        self.assertEqual((len(r["shots"]), r["shots"][-1]["end"]), (6, 24.0))
        with self.assertRaises(ValueError):
            reel_plan("x", 40)

    def test_quota(self):
        self.assertEqual(quota(2)["blocked"], True)
        self.assertEqual(quota(5, "plus")["left"], 15)

    def test_consent_ok(self):
        c = consent_check(27, True)
        self.assertEqual((c["allowed"], c["level"], c["flags"]), (True, "ok", []))

    def test_consent_child(self):
        self.assertFalse(consent_check(11, True)["allowed"])
        self.assertTrue(consent_check(11, True, parent_ok=True)["allowed"])

    def test_consent_stops(self):
        c = consent_check(30, False, signature=True, purpose="forgery")
        self.assertEqual(c["flags"], ["not_own_handwriting", "signature_detected", "document_forgery"])
        self.assertEqual(c["level"], "stop")

    def test_consent_resale_warn(self):
        c = consent_check(33, True, purpose="resale")
        self.assertEqual((c["allowed"], c["level"]), (True, "warn"))

    def test_guard_all(self):
        for f in GUARD:
            g = safety_guard(f)
            self.assertEqual(g["block"], g["level"] == "stop")

    def test_share(self):
        self.assertEqual(share_card("HandFont-Mint", MSG)["size"], "1080x1350")
        with self.assertRaises(ValueError):
            share_card("x", "y", "poster")


if __name__ == "__main__":
    unittest.main(verbosity=1)
