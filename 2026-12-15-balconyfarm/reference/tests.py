import unittest
from balconyfarm import *
from fixtures import *


class T(unittest.TestCase):
    def test_scan_ok(self):
        q = balcony_scan(PHOTOS[0])["quality"]
        self.assertEqual((q["score"], q["ok"], q["tips_th"]), (94, True, []))

    def test_scan_bad(self):
        q = balcony_scan(PHOTOS[2])["quality"]
        self.assertEqual((q["score"], q["ok"], len(q["tips_th"])), (49, False, 3))

    def test_scan_range(self):
        with self.assertRaises(ValueError):
            scan_quality(0, -0.1, 0)

    def test_sun_demo(self):
        self.assertEqual((SUN["sun_hours"], SUN["light"], SUN["hot_afternoon"]), (3.8, "partial", False))
        self.assertIn("3.8 ชม.", SUN["headline_th"])

    def test_sun_south_open_full(self):
        self.assertEqual(sun_estimate("s", 0, 0, 20)["light"], "full")

    def test_sun_north_shade(self):
        e = sun_estimate("n", 0.5, 1.5, 3)
        self.assertEqual((e["sun_hours"], e["light"]), (0.8, "shade"))

    def test_high_floor_less_blocked(self):
        self.assertGreater(sun_estimate("e", 0.5, 0, 15)["sun_hours"], sun_estimate("e", 0.5, 0, 4)["sun_hours"])

    def test_west_hot(self):
        self.assertTrue(sun_estimate("w", 0, 0, 5)["hot_afternoon"])

    def test_sun_bad(self):
        for a in (("up", 0, 0, 1), ("s", 2, 0, 1), ("s", 0, 5, 1), ("s", 0, 0, 0)):
            with self.assertRaises(ValueError):
                sun_estimate(*a)

    def test_season(self):
        self.assertEqual([season(m) for m in (1, 4, 8, 11)], ["cool", "hot", "rainy", "cool"])

    def test_plant_fit_levels(self):
        self.assertEqual(plant_fit("horapha", 3.8, 12)["score"], 100)
        self.assertEqual(plant_fit("kaprao", 3.8, 12)["light_fit"], 0.5)
        self.assertEqual(plant_fit("cherry_tomato", 2.0, 12)["score"], 30)
        self.assertFalse(plant_fit("coriander", 4, 5)["in_season"])

    def test_picks_demo(self):
        self.assertEqual(GARDEN, ["lettuce", "coriander", "horapha", "mint", "spring_onion"])
        self.assertTrue(PICKS["headline_th"].startswith("แนะนำ ผักสลัด"))

    def test_picks_full_sun(self):
        g = [p["plant"] for p in plant_picks(sun_estimate("s", 0, 0, 20), 12)["picks"]]
        self.assertIn("cherry_tomato", g)
        self.assertNotIn("pandan", g)

    def test_picks_shade_only_shade_plants(self):
        g = [p["plant"] for p in plant_picks(sun_estimate("n", 0.5, 1.5, 3), 7)["picks"]]
        self.assertIn("pandan", g)
        self.assertNotIn("chili", g)

    def test_picks_exclude(self):
        g = [p["plant"] for p in plant_picks(SUN, MONTH, exclude=("lettuce",))["picks"]]
        self.assertNotIn("lettuce", g)

    def test_layout_demo(self):
        self.assertEqual((len(LAYOUT["pots"]), LAYOUT["skipped"], LAYOUT["total_wet_kg"], LAYOUT["load_kg_m2"], LAYOUT["load_status"]), (5, [], 23, 16.0, "ok"))
        self.assertEqual(LAYOUT["usable_depth_m"], 0.6)

    def test_layout_no_overlap_and_inside(self):
        W = int(LAYOUT["width_m"] * 100); D = int(LAYOUT["usable_depth_m"] * 100)
        for p in LAYOUT["pots"]:
            self.assertLessEqual(p["x_cm"] + p["pot_cm"], W)
            self.assertLessEqual(p["y_cm"] + p["pot_cm"], D)
        xs = sorted((p["y_cm"], p["x_cm"], p["x_cm"] + p["pot_cm"]) for p in LAYOUT["pots"])
        for a, b in zip(xs, xs[1:]):
            if a[0] == b[0]: self.assertLessEqual(a[2], b[1])

    def test_layout_skips_when_full(self):
        l = layout(1.5, 1.0, ["kaffir_lime", "chili", "lemongrass", "cherry_tomato", "kaprao"])
        self.assertEqual((l["skipped"], l["load_status"]), (["kaprao"], "warn"))

    def test_layout_overload(self):
        self.assertEqual(layout(1.2, 1.0, ["kaffir_lime"] * 3)["load_status"], "over")

    def test_layout_bad(self):
        with self.assertRaises(ValueError):
            layout(2, 0.7, ["mint"])
        with self.assertRaises(ValueError):
            layout(2, 1.2, [])
        with self.assertRaises(ValueError):
            layout(2, 1.2, ["rose"])

    def test_water_demo(self):
        w = water_plan(GARDEN, MONTH, "se", TODAY, SUN["sun_hours"])
        self.assertEqual(set(w["every_days"].values()), {2})
        self.assertEqual(len(w["days"][0]["water"]), 5)
        self.assertEqual(w["days"][1]["water"], [])
        self.assertEqual(w["season"], "cool")

    def test_water_hot_west_daily(self):
        w = water_plan(["chili"], 4, "w", TODAY, 6)
        self.assertEqual(w["every_days"]["chili"], 1)
        self.assertEqual(water_plan(["chili"], 8, "e", TODAY, 6)["every_days"]["chili"], 3)

    def test_harvest_demo(self):
        h = harvest_plan(GARDEN, TODAY)
        self.assertEqual((h["first_up"], h["items"][0]["first_harvest"], h["saves_baht_month"]), ("สะระแหน่", "2027-01-14", 260))

    def test_shopping_demo(self):
        s = shopping_list(GARDEN)
        self.assertEqual((s["total_baht"], s["soil_total_l"], s["payback_months"]), (397, 29, 1.5))

    def test_shopping_groups_duplicates(self):
        s = shopping_list(["kaprao", "kaprao", "chili"])
        self.assertEqual(s["items"][0]["pots"], 2)
        self.assertEqual(len(s["items"]), 2)

    def test_mockup_prompt_safe(self):
        m = mockup_spec(SUN, PICKS)
        self.assertIn("inside the railing", m["image_prompt"])
        self.assertIn("no people", m["image_prompt"])
        with self.assertRaises(ValueError):
            mockup_spec(SUN, PICKS, "gold")

    def test_diary(self):
        d = diary_summary(DIARY, TODAY)
        self.assertEqual((d["entries"], d["streak_days"], d["harvest_g"], d["saved_baht"]), (5, 3, 125, 15))
        with self.assertRaises(ValueError):
            diary_summary([], TODAY)

    def test_share(self):
        c = share_card(SUN, PICKS, "ระเบียงโล่ง ๆ กลายเป็นสวนผักใน 10 วิ")
        self.assertEqual(c["layout"], "balcony_before_after")
        self.assertIn("FARM", c["cta_th"])
        self.assertIn("5 อย่าง", c["title_th"])

    def test_quota(self):
        self.assertEqual(quota(0), {"allowed": 1, "left_after": 2, "paywall": False})
        self.assertTrue(quota(3)["paywall"])
        self.assertIsNone(quota(9, pro=True)["left_after"])

    def test_guard(self):
        self.assertEqual(safety_guard()["level"], "ok")
        self.assertEqual(safety_guard("railing")["level"], "stop")
        self.assertEqual(safety_guard("overload")["level"], "warn")
        with self.assertRaises(ValueError):
            safety_guard("x")

    def test_every_plant_complete(self):
        for k, p in PLANTS.items():
            self.assertLess(p["sun"][0], p["sun"][1], k)
            self.assertTrue(p["months"], k)
            for f in ("pot_cm", "kg", "water", "harvest", "save"):
                self.assertGreater(p[f], 0, k)


if __name__ == "__main__":
    unittest.main(verbosity=1)
