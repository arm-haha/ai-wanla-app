import unittest
from brickbuddy import *
from fixtures import *


class T(unittest.TestCase):
    def test_catalogue_sizes(self):
        self.assertEqual((len(PARTS), len(COLORS), len(BUILDS), len(CHALLENGES)), (14, 12, 14, 7))

    def test_every_build_uses_known_parts(self):
        for b in BUILDS.values():
            self.assertTrue(set(b["need"]) <= set(PARTS))

    def test_scan_ok(self):
        self.assertEqual(pile_scan(PHOTOS[0])["quality"], {"score": 90, "ok": True, "tips_th": []})

    def test_scan_mid(self):
        q = pile_scan(PHOTOS[1])["quality"]
        self.assertEqual((q["score"], q["ok"], len(q["tips_th"])), (63, False, 2))

    def test_scan_bad_and_range(self):
        self.assertEqual(len(pile_scan(PHOTOS[2])["quality"]["tips_th"]), 4)
        with self.assertRaises(ValueError):
            scan_quality(1.2, 0, 0, 0)

    def test_grid_cell(self):
        self.assertEqual((grid_cell(0, 0), grid_cell(1, 1), grid_cell(0.5, 0.5)), ("A1", "F4", "D3"))
        with self.assertRaises(ValueError):
            grid_cell(-0.1, 0.5)

    def test_inventory_totals(self):
        self.assertEqual((INV["total"], INV["studs"], INV["kinds"]), (61, 183, 12))

    def test_inventory_drops_low_confidence(self):
        self.assertNotIn("window", INV["by_part"])
        self.assertEqual(INV["by_color"].get("green"), 7)

    def test_inventory_top_colors(self):
        self.assertEqual(INV["top_colors"], ["yellow", "blue", "red"])

    def test_inventory_unknown(self):
        with self.assertRaises(ValueError):
            inventory([{"part": "spaceship", "color": "red", "count": 1}])

    def test_match_exact(self):
        m = match_build("duck", INV)
        self.assertEqual((m["match_pct"], m["can_build"], m["substitutions"]), (100, True, []))

    def test_match_missing_window(self):
        m = match_build("house", INV)
        self.assertEqual((m["can_build"], m["missing"], m["match_pct"]), (False, {"window": 1}, 94))

    def test_substitution_1x4(self):
        m = match_build("dino", INV)
        self.assertTrue(m["can_build"])
        self.assertEqual(m["substitutions"], [{"need": "brick_1x4", "use": "brick_1x2", "per": 2, "count": 2}])

    def test_substitution_partial(self):
        m = match_build("ny_2027", INV)
        self.assertEqual((m["match_pct"], m["missing"]), (87, {"brick_1x2": 2, "brick_1x1": 2}))

    def test_exact_before_substitute(self):
        inv = inventory([{"part": "brick_2x2", "color": "red", "count": 2}])
        m = match_build("duck", inv)  # needs 1×2x4 + 2×2x2: the 2x2s must go to the 2x2 slots, not stand in for the 2x4
        self.assertEqual(m["missing"].get("brick_2x4"), 1)
        self.assertNotIn("brick_2x2", m["missing"])

    def test_suggest_order_and_count(self):
        self.assertEqual([i["build"] for i in IDEAS], ["duck", "snowman", "race_car", "boat", "robot", "rocket"])

    def test_suggest_respects_age(self):
        ids = [m["build"] for m in suggest_builds(INV, 4, 60, top=20)]
        self.assertNotIn("dino", ids)
        self.assertTrue(all(BUILDS[i]["age"] <= 4 for i in ids))

    def test_suggest_respects_time(self):
        self.assertTrue(all(m["minutes"] <= 6 for m in suggest_builds(INV, 10, 6, top=20)))

    def test_buildable_count(self):
        self.assertEqual(sum(match_build(b, INV)["can_build"] for b in BUILDS), 11)

    def test_assign_colors_duck(self):
        self.assertEqual(COLORS_DUCK["roles"], {"main": "yellow", "accent": "red"})

    def test_assign_colors_tree_green(self):
        self.assertEqual(assign_colors("xmas_tree", PILE + [{"part": "brick_2x2", "color": "green", "count": 1}])["roles"]["main"], "green")

    def test_steps_duck(self):
        self.assertEqual(STEPS_DUCK["step_count"], 5)
        self.assertEqual(STEPS_DUCK["steps"][0]["part"], "brick_2x4")
        self.assertIsNone(STEPS_DUCK["steps"][-1]["color"])  # eyes keep their own colour

    def test_steps_base_first_and_split(self):
        st = build_steps("house", assign_colors("house", PILE))["steps"]
        self.assertEqual(st[0]["part"], "plate_2x4")
        self.assertTrue(all(s["count"] <= 4 for s in st if PARTS[s["part"]][3] == "brick"))

    def test_find_piece(self):
        self.assertEqual(find_piece(PILE, "brick_2x4", "red")["cells"], ["A1", "D3"])
        self.assertFalse(find_piece(PILE, "brick_2x4", "pink")["found"])

    def test_sort_color(self):
        sp = sort_plan(INV, 4)
        self.assertEqual(sum(b["count"] for b in sp["boxes"]), 61)
        self.assertLessEqual(sp["balance_gap"], 4)

    def test_sort_size_and_errors(self):
        self.assertEqual(sort_plan(INV, 3, "size")["boxes"][0]["groups"], ["S"])
        with self.assertRaises(ValueError):
            sort_plan(INV, 1)
        with self.assertRaises(ValueError):
            sort_plan(INV, 3, "taste")

    def test_stability_levels(self):
        self.assertEqual(stability(6, 8, 100)["level"], "solid")
        self.assertEqual(stability(12, 4, 50)["level"], "will_fall")
        self.assertEqual(stability(6, 4, 40)["level"], "wobbly")

    def test_challenge_rotates(self):
        self.assertEqual(daily_challenge("2026-11-23")["theme"], "vehicle")
        self.assertNotEqual(daily_challenge("2026-11-23")["theme"], daily_challenge("2026-11-24")["theme"])

    def test_challenge_new_year_window(self):
        self.assertEqual(daily_challenge("2026-12-21")["theme"], "seasonal")
        self.assertEqual(daily_challenge("2027-01-02")["theme"], "seasonal")

    def test_creation_score(self):
        c = creation_score(7, 3, 0.9, 5, True, 10)
        self.assertEqual((c["points"], c["stars"], c["badges"]), (62, 4, ["symmetry_star", "challenge_done"]))

    def test_creation_never_zero(self):
        c = creation_score(0, 0, 0, 0, False)
        self.assertEqual((c["points"], c["stars"]), (5, 1))

    def test_creation_over_limit(self):
        c = creation_score(40, 6, 0.5, 12, True, 30)
        self.assertTrue(c["over_limit"])
        self.assertNotIn("challenge_done", c["badges"])

    def test_diary(self):
        d = diary_summary(DIARY, TODAY)
        self.assertEqual((d["builds"], d["streak"], d["pieces_used"], d["best_stars"]), (3, 3, 33, 4))

    def test_reel_and_quota(self):
        r = reel_plan("เป็ดน้อย", 24)
        self.assertEqual((len(r["shots"]), r["shots"][-1]["end"]), (6, 24))
        with self.assertRaises(ValueError):
            reel_plan("x", 40)
        self.assertTrue(quota(3)["blocked"])
        self.assertFalse(quota(3, "plus")["blocked"])

    def test_age_check(self):
        self.assertEqual(age_check(2, True)["level"], "stop")
        self.assertEqual(age_check(7, False)["flags"], ["under_13_no_parent"])
        self.assertTrue(age_check(7, True)["allowed"])
        self.assertEqual(age_check(30, found=("magnet",))["level"], "stop")
        self.assertEqual(age_check(30, found=("coin", "face"))["level"], "warn")

    def test_guard(self):
        self.assertTrue(safety_guard("official_set_copy")["block"])
        self.assertFalse(safety_guard("face_in_photo")["block"])
        self.assertIn("1669", safety_guard("swallowed_part")["message_th"])


if __name__ == "__main__":
    unittest.main(verbosity=1)
