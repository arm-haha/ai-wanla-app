import unittest
from nailpop import *
from fixtures import *

class T(unittest.TestCase):
    def setUp(self):
        self.scan = hand_scan(MIND_PHOTO)
        self.tone = undertone(MIND["quiz"], MIND["skin_rgb"])
        self.grid = try_on_grid(self.scan, self.tone["undertone"], "wedding", MIND["budget_thb"])

    # 1) Hand Snap + detection
    def test_mind_shape_length(self):
        self.assertEqual((self.scan["shape"], self.scan["length"]), ("squoval", "medium"))
        self.assertEqual(self.scan["nail_count"], 5)

    def test_mind_quality(self):
        q = self.scan["quality"]
        self.assertEqual(q["score"], 84)
        self.assertTrue(q["ok"])
        self.assertEqual(q["tips_th"], [])

    def test_shape_rules(self):
        self.assertEqual(classify_shape(0.8, 0.5, 10, 5, 10), "stiletto")
        self.assertEqual(classify_shape(0.5, 0.7, 10, 5, 10), "almond")
        self.assertEqual(classify_shape(0.5, 0.2, 10, 5, 10), "coffin")
        self.assertEqual(classify_shape(0.0, 0.1, 10, 1, 10), "square")
        self.assertEqual(classify_shape(0.1, 0.8, 10, 1, 10), "round")
        self.assertEqual(classify_shape(0.1, 0.8, 12, 3, 10), "oval")

    def test_length_rules(self):
        self.assertEqual([classify_length(x) for x in (0.5, 1.5, 3.9, 4.0)], ["short", "medium", "medium", "long"])

    def test_bad_width(self):
        with self.assertRaises(ValueError):
            classify_shape(0.1, 0.1, 10, 1, 0)

    def test_low_quality_tips(self):
        s = hand_scan(PHOTOS[3])
        self.assertFalse(s["quality"]["ok"])
        self.assertEqual(s["nail_count"], 4)
        self.assertTrue(len(s["quality"]["tips_th"]) >= 2)

    def test_pipeline_relight_deskew(self):
        st = pipeline_steps(PHOTOS[2])
        self.assertEqual(st[0], "hand_detect")
        self.assertIn("relight", st)
        self.assertIn("deskew", st)
        self.assertEqual(st[-1], "fit_rank")

    def test_pipeline_mind_clean(self):
        self.assertNotIn("relight", pipeline_steps(MIND_PHOTO))

    # 3) Skin tone
    def test_mind_warm(self):
        self.assertEqual(self.tone["undertone"], "warm")
        self.assertEqual(self.tone["depth"], "medium")

    def test_fern_cool_por_neutral(self):
        self.assertEqual(undertone(PEOPLE[1]["quiz"], PEOPLE[1]["skin_rgb"])["undertone"], "cool")
        self.assertEqual(undertone(PEOPLE[2]["quiz"], PEOPLE[2]["skin_rgb"])["undertone"], "neutral")

    def test_joy_deep_warm(self):
        u = undertone(PEOPLE[3]["quiz"], PEOPLE[3]["skin_rgb"])
        self.assertEqual((u["undertone"], u["depth"]), ("warm", "deep"))

    def test_shades(self):
        r = shade_recommend("warm")
        self.assertEqual(len(r["best"]), 5)
        self.assertIn("#C0603F", [x["hex"] for x in r["best"]])
        with self.assertRaises(KeyError):
            shade_recommend("olive")

    # 2) Try-on grid
    def test_grid_9(self):
        self.assertEqual(self.grid["count"], 9)
        self.assertEqual([t["slot"] for t in self.grid["tiles"]][:3], ["r1c1", "r1c2", "r1c3"])

    def test_grid_top_pick(self):
        t = self.grid["tiles"][0]
        self.assertEqual((t["design_id"], t["fit_score"]), ("d01", 100))

    def test_grid_sorted(self):
        sc = [t["fit_score"] for t in self.grid["tiles"]]
        self.assertEqual(sc, sorted(sc, reverse=True))

    def test_grid_n_bounds(self):
        with self.assertRaises(ValueError):
            try_on_grid(self.scan, "warm", n=10)

    def test_fit_max_100(self):
        for d in DESIGNS:
            self.assertLessEqual(fit_score(d, self.scan, "warm", "wedding", 900)[0], 100)

    # Price + 4) Salon card
    def test_price_gel_art1(self):
        p = price_estimate("gel", 1, "medium")
        self.assertEqual((p["min_thb"], p["max_thb"]), (450, 850))

    def test_price_long_removal_province(self):
        p = price_estimate("gel", 0, "long", "province", removal=True)
        self.assertEqual((p["min_thb"], p["max_thb"]), (470, 810))

    def test_price_extension_no_long_surcharge(self):
        p = price_estimate("extension", 3, "long")
        self.assertEqual((p["min_thb"], p["max_thb"]), (1300, 2400))

    def test_salon_card(self):
        c = salon_card("มายด์", "d01", self.scan)
        self.assertEqual((c["price_min_thb"], c["price_max_thb"]), (450, 850))
        self.assertIn("เหลี่ยมมน", c["note_th"])
        self.assertTrue(c["line_share_url"].startswith("https://line.me/R/share?text="))
        self.assertIn("ภาพจำลอง", c["share_text_th"])

    # 5) Friend vote
    def test_vote_mind(self):
        v = friend_vote(self.grid, MIND_VOTES)
        self.assertEqual((v["winner"], v["winner_pct"], v["total"]), ("d01", 60, 10))

    def test_vote_tie_rank(self):
        v = friend_vote(self.grid, ["d02", "d01"])
        self.assertEqual(v["winner"], "d01")

    def test_vote_invalid_empty(self):
        v = friend_vote(self.grid, ["zz"])
        self.assertEqual((v["winner"], v["invalid"]), (None, 1))

    def test_vote_link(self):
        self.assertEqual(vote_link("g01", ["d01", "d02", "d05"])["expires_hours"], 48)
        with self.assertRaises(ValueError):
            vote_link("g01", ["d01"])

    # 6) Diary + reminder
    def test_gel_reminder(self):
        r = care_reminder("2026-11-09", "gel")
        self.assertEqual((r["check_date"], r["due_date"], r["remove_by"]), ("2026-11-23", "2026-11-30", "2026-12-07"))

    def test_reminder_status(self):
        r = care_reminder("2026-11-09", "gel")
        self.assertEqual(reminder_status(r, "2026-11-12")["status"], "ok")
        self.assertEqual(reminder_status(r, "2026-11-25")["status"], "check")
        self.assertEqual(reminder_status(r, "2026-11-30")["status"], "due")
        self.assertEqual(reminder_status(r, "2026-12-10")["status"], "overdue")

    def test_diary_stats(self):
        es = [diary_entry(*e) for e in DIARY]
        st = diary_stats(es)
        self.assertEqual((st["count"], st["total_thb"], st["avg_thb"]), (3, 1490, 497))
        with self.assertRaises(ValueError):
            diary_entry("x", "2026-11-09", "d01", "gel", 1, 6)

    # 7) Occasion
    def test_occasion_songkran(self):
        p = occasion_preset("songkran")
        self.assertIn("d08", p["design_ids"])
        self.assertEqual(p["label_th"], "สงกรานต์")

    def test_occasion_unknown(self):
        with self.assertRaises(KeyError):
            occasion_preset("halloween")

    # 8) DIY
    def test_diy_gel_art1(self):
        g = diy_guide("d01")
        self.assertTrue(g["diy_ok"])
        self.assertIn("gel_cure", [s["key"] for s in g["steps"]])
        self.assertEqual(g["total_min"], 48)

    def test_diy_blocked_extension(self):
        self.assertFalse(diy_guide("d13")["diy_ok"])

    # Safety / quota / share
    def test_health_guard(self):
        self.assertEqual(health_guard({"redness": True})["level"], "stop")
        self.assertEqual(health_guard({"lifting": True})["level"], "warn")
        self.assertEqual(health_guard({})["level"], "ok")

    def test_quota(self):
        self.assertEqual(quota(2, 3), {"allowed": 1, "left_after": 0, "paywall": True})
        self.assertFalse(quota(0, 9, pro=True)["paywall"])

    def test_share_card(self):
        c = share_card("มายด์", "d01", 100, 60)
        self.assertIn("60%", c["headline_th"])
        self.assertIn("AI preview", c["watermark"])

if __name__ == "__main__":
    unittest.main(verbosity=1)
