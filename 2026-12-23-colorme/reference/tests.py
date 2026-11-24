import unittest
from colorme import *
from fixtures import *


class T(unittest.TestCase):
    def test_tables(self):
        self.assertEqual((len(CRAYONS), len(LEVELS), len(THEMES), A4_PX), (13, 4, 14, (2480, 3508)))

    def test_levels_cover_all_ages(self):
        self.assertEqual([level_for_age(a) for a in (3, 5, 6, 8, 9, 12, 13, 99)], ["tiny", "tiny", "kid", "kid", "big", "big", "calm", "calm"])
        with self.assertRaises(ValueError):
            level_for_age(2)

    def test_photo_check(self):
        self.assertEqual(photo_check(0.9, 0.85, 0.6, 0.3), {"score": 78, "ok": True, "tips_th": []})
        bad = photo_check(0.4, 0.3, 0.2, 0.8)
        self.assertEqual((bad["score"], bad["ok"], len(bad["tips_th"])), (29, False, 4))
        with self.assertRaises(ValueError):
            photo_check(1.2, 1, 1, 0)

    def test_nearest(self):
        self.assertEqual(nearest((250, 140, 45)), "orange")
        self.assertEqual(nearest((0, 0, 0)), "black")
        self.assertEqual(nearest((250, 140, 45), ["red", "blue"]), "red")

    def test_despeckle_removes_lonely_cell(self):
        g = [["sky"] * 3 for _ in range(3)]; g[1][1] = "purple"
        self.assertEqual(despeckle(g)[1][1], "sky")
        g[1][2] = "purple"   # two together are a real detail, keep
        self.assertEqual(despeckle(g)[1][1], "purple")

    def test_palette_ignores_dust(self):
        self.assertEqual(pick_palette(PIC, 7), ["red", "orange", "yellow", "lime", "green", "sky", "brown"])
        self.assertNotIn("purple", pick_palette(PIC, 12))

    def test_regions_connectivity(self):
        g = [["red", "sky", "red"], ["sky", "sky", "sky"], ["red", "sky", "red"]]
        regs, lab = regions(g)
        self.assertEqual(len(regs), 5)   # 4-connected: diagonal reds are separate
        self.assertEqual(regs[1]["area"], 5)
        self.assertEqual(lab[2][2], 5)

    def test_merge_small(self):
        g = [["sky"] * 4 for _ in range(4)]; g[0][0] = "red"; g[2][2] = g[2][3] = "yellow"
        m = merge_small(g, 2)
        self.assertEqual(m[0][0], "sky")
        self.assertEqual(m[2][2], "yellow")
        self.assertEqual(len(regions(merge_small(g, 3))[0]), 1)

    def test_merge_keeps_single_region(self):
        self.assertEqual(merge_small([["sky"]], 10), [["sky"]])

    def test_outline(self):
        g = [["sky", "red"], ["sky", "sky"]]
        self.assertEqual(outline(g), {(0, 0), (0, 1)})

    def test_page_kid(self):
        p = page_public(PAGE_KID)
        self.assertEqual((p["level"], p["colors"], p["regions"], p["line_px"], p["show_numbers"]), ("kid", 6, 8, 5, True))
        self.assertEqual([l["key"] for l in p["legend"]], ["red", "orange", "yellow", "lime", "sky", "brown"])
        self.assertEqual([l["num"] for l in p["legend"]], [1, 2, 3, 4, 5, 6])
        self.assertEqual(p["edge_ratio"], 0.217)

    def test_page_tiny_is_simple(self):
        p = page_public(PAGE_TINY)
        self.assertEqual((p["regions"], p["colors"], p["line_px"], p["show_numbers"], p["labels"]), (4, 4, 8, False, []))

    def test_detail_grows_with_age(self):
        r = [PAGE_TINY["regions"], PAGE_KID["regions"], PAGE_BIG["regions"], PAGE_CALM["regions"]]
        self.assertEqual(r, sorted(r))
        self.assertEqual(r, [4, 8, 19, 19])

    def test_calm_thin_lines_more_dots(self):
        self.assertEqual((PAGE_CALM["line_px"], PAGE_TINY["line_px"]), (2, 8))
        self.assertEqual((LEVELS["calm"]["dots"], LEVELS["tiny"]["dots"]), (80, 10))

    def test_eyes_only_for_older(self):
        self.assertNotIn("black", [l["key"] for l in PAGE_KID["legend"]])
        self.assertIn("black", [l["key"] for l in PAGE_BIG["legend"]])

    def test_regions_within_level_limit(self):
        for p in (PAGE_TINY, PAGE_KID, PAGE_BIG, PAGE_CALM):
            self.assertLessEqual(p["regions"], LEVELS[p["level"]]["max_regions"])

    def test_auto_simplify(self):
        stripes = [[(230, 57, 70) if (x // 2) % 2 else (120, 190, 240) for x in range(40)] for _ in range(30)]  # 20 tall stripes
        p = make_page(stripes, 4)
        self.assertEqual(p["regions"], 1)
        self.assertGreaterEqual(p["simplify_passes"], 1)

    def test_lineart_has_no_numbers(self):
        self.assertEqual((PAGE_LINE["show_numbers"], PAGE_LINE["labels"]), (False, []))
        with self.assertRaises(ValueError):
            make_page(PIC, 6, "watercolor")

    def test_labels_inside_region(self):
        regs, lab = regions(PAGE_KID["grid"])
        for l in PAGE_KID["labels"]:
            self.assertEqual(lab[l["y"]][l["x"]], l["region"])
        self.assertEqual((PAGE_KID["labels"][2]["x"], PAGE_KID["labels"][2]["y"]), (12, 10))   # cat head centre

    def test_label_numbers_match_legend(self):
        num = {l["key"]: l["num"] for l in PAGE_KID["legend"]}
        regs, _ = regions(PAGE_KID["grid"])
        for l in PAGE_KID["labels"]:
            self.assertEqual(l["num"], num[regs[l["region"] - 1]["color"]])

    def test_dots(self):
        d = dot_to_dot(CAT_OUTLINE, 6)
        self.assertEqual((len(d["dots"]), d["perimeter"], d["spacing"]), (20, 280.8, 14.0))
        self.assertEqual(d["dots"][0], {"num": 1, "x": 30.0, "y": 20.0})
        self.assertEqual(len(dot_to_dot(CAT_OUTLINE, 36)["dots"]), 80)
        with self.assertRaises(ValueError):
            dot_to_dot([(0, 0), (1, 1)], 6)

    def test_booklet(self):
        b = booklet([PAGE_KID, PAGE_TINY, PAGE_BIG], "น้องข้าวปั้น")
        self.assertEqual((b["title_th"], b["pages"], b["sheets_double_sided"], b["ink_pct"]), ("สมุดระบายสีของน้องข้าวปั้น", 4, 2, 6.3))
        with self.assertRaises(ValueError):
            booklet([PAGE_KID] * 13, "x")

    def test_ink_saver(self):
        a, b = booklet([PAGE_KID], "x"), booklet([PAGE_KID], "x", True)
        self.assertLess(b["ink_pct"], a["ink_pct"])
        self.assertEqual(b["line_px"], 2)

    def test_progress_done(self):
        self.assertEqual(progress_check(PAGE_KID, SCAN_DONE), {"coverage_pct": 100, "in_lines_pct": 100, "match_pct": 100, "stars": 3,
                         "favorite": "sky", "praise_th": "เสร็จแล้ว! ผลงานศิลปินตัวจริง ชอบสีฟ้าที่เลือกจัง", "done": True})

    def test_progress_half_wrong_colours_still_kind(self):
        p = progress_check(PAGE_KID, SCAN_HALF)
        self.assertEqual((p["coverage_pct"], p["match_pct"], p["stars"], p["done"]), (50, 75, 2, False))

    def test_progress_min_one_star(self):
        p = progress_check(PAGE_KID, SCAN_START)
        self.assertEqual(p["stars"], 1)
        blank = [[None] * PAGE_KID["w"] for _ in range(PAGE_KID["h"])]
        self.assertEqual((progress_check(PAGE_KID, blank)["stars"], progress_check(PAGE_KID, blank)["favorite"]), (1, None))

    def test_progress_over_the_line(self):
        self.assertEqual(progress_check(PAGE_KID, scan_of(PAGE_KID, 1.0, spill=30))["in_lines_pct"], 96)

    def test_progress_lineart_no_match(self):
        self.assertIsNone(progress_check(PAGE_LINE, scan_of(PAGE_LINE, 1.0))["match_pct"])

    def test_quest_streak_and_sticker(self):
        self.assertEqual(quest(TODAY, HISTORY), {"date": "2026-12-23", "theme_th": "วิวหน้าบ้าน", "streak": 3, "done_today": True, "new_sticker": "ดินสอสีทอง"})
        self.assertEqual(quest("2026-12-24", HISTORY)["streak"], 3)    # yesterday still counts
        self.assertEqual(quest("2026-12-25", HISTORY)["streak"], 0)

    def test_quest_theme_rotates(self):
        self.assertEqual(len({quest("2026-12-%02d" % d, [])["theme_th"] for d in range(1, 15)}), 14)

    def test_gallery(self):
        g = gallery_summary(GALLERY, "2026-12")
        self.assertEqual((g["pages"], g["stars"], g["favorite_th"], g["art_book_ready"]), (8, 20, "ส้ม", True))
        self.assertIn("3", gallery_summary(GALLERY[:5], "2026-12")["note_th"])
        self.assertEqual(gallery_summary(GALLERY, "2026-11")["favorite_th"], None)

    def test_share_card(self):
        c = share_card(PAGE_KID, progress_check(PAGE_KID, SCAN_DONE))
        self.assertEqual((c["child_face_hidden"], c["stars"], c["size"]), (True, 3, "1080x1350"))
        with self.assertRaises(ValueError):
            share_card(PAGE_KID, layout="poster")

    def test_reel(self):
        r = reel_plan(24)
        self.assertEqual((len(r["shots"]), r["shots"][-1]["end"], r["shots"][0]["kind"]), (6, 24, "hook"))
        with self.assertRaises(ValueError):
            reel_plan(45)

    def test_quota(self):
        self.assertEqual(quota(5), {"plan": "free", "pages_per_day": 5, "used": 5, "left": 0, "blocked": True})
        self.assertFalse(quota(10, "plus")["blocked"])

    def test_privacy(self):
        self.assertTrue(privacy_check(True, True)["share_allowed"])
        w = privacy_check(False, True, ("copyright_character",))
        self.assertEqual((w["level"], w["allowed"], w["share_allowed"]), ("warn", True, False))
        s = privacy_check(True, True, ("id_document",))
        self.assertEqual((s["allowed"], s["level"]), (False, "stop"))

    def test_guard(self):
        self.assertTrue(safety_guard("nudity")["block"])
        self.assertTrue(safety_guard("under_3")["block"])
        self.assertFalse(safety_guard("screen_time")["block"])
        self.assertEqual(safety_guard()["level"], "ok")


if __name__ == "__main__":
    unittest.main(verbosity=1)
