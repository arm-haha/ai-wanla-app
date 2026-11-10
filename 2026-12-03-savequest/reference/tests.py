import unittest
from savequest import *
from fixtures import *

class T(unittest.TestCase):
    def setUp(self):
        self.scan = photo_scan(MINT_PHOTO)
        self.jar = jar_fill(MINT["saved_thb"], MINT["goal_thb"])
        self.ms = milestones(MINT["saved_thb"], MINT["goal_thb"])
        self.st = streak(MINT_DATES, TODAY)

    # 1) Photo scan
    def test_mint_quality(self):
        q = self.scan["quality"]
        self.assertEqual(q["score"], 90)
        self.assertTrue(q["ok"])
        self.assertEqual(q["tips_th"], [])

    def test_quality_tips(self):
        s = photo_scan(PHOTOS[3])
        self.assertEqual(s["quality"]["score"], 46)
        self.assertFalse(s["quality"]["ok"])
        self.assertGreaterEqual(len(s["quality"]["tips_th"]), 3)

    def test_bad_quality_input(self):
        with self.assertRaises(ValueError):
            scan_quality(1.5, 0, 0)

    def test_pipeline(self):
        self.assertEqual(pipeline_steps(MINT_PHOTO),
                         ["goal_photo", "jar_fill", "plan", "challenge", "milestone"])
        st = pipeline_steps(PHOTOS[3])
        self.assertIn("deglare", st)
        self.assertIn("recrop", st)

    # 2) Jar fill (wow)
    def test_mint_jar(self):
        self.assertEqual(self.jar["pct"], 42)
        self.assertEqual(self.jar["remaining_thb"], 26100)
        self.assertEqual(self.jar["level"], "growing")
        self.assertEqual(self.jar["headline_th"], "กระปุกโตถึง 42%")

    def test_bee_halfway(self):
        j = jar_fill(BEE["saved_thb"], BEE["goal_thb"])
        self.assertEqual(j["pct"], 75)
        self.assertEqual(j["level"], "almost")

    def test_arm_almost(self):
        j = jar_fill(ARM["saved_thb"], ARM["goal_thb"])
        self.assertEqual((j["pct"], j["level"]), (80, "almost"))

    def test_full_and_empty(self):
        self.assertEqual(jar_fill(0, 45000)["level"], "empty")
        self.assertEqual(jar_fill(45000, 45000)["level"], "full")
        self.assertEqual(jar_fill(50000, 45000)["pct"], 100)
        self.assertEqual(jar_fill(4050, 45000)["level"], "empty")  # 9%
        self.assertEqual(jar_fill(22500, 45000)["level"], "halfway")

    def test_bad_jar(self):
        with self.assertRaises(ValueError):
            jar_fill(10, 0)
        with self.assertRaises(ValueError):
            jar_fill(-1, 100)

    def test_mint_milestones(self):
        self.assertEqual(self.ms["reached"], [25])
        self.assertEqual(self.ms["next_mark"], 50)
        self.assertEqual(self.ms["need_thb"], 3600)
        self.assertIn("3,600", self.ms["message_th"])

    def test_milestone_done(self):
        m = milestones(45000, 45000)
        self.assertEqual(m["next_mark"], None)
        self.assertIn("ถึงเป้า", m["message_th"])

    # 3) 52-week + random plans
    def test_week52_mint(self):
        p = week52_plan(18, 100)
        self.assertEqual(p["amount_thb"], 1800)
        self.assertEqual(p["cumulative_thb"], 17100)
        self.assertEqual(p["plan_total_thb"], 137800)
        self.assertEqual(p["kind"], "week52")

    def test_week52_fit(self):
        self.assertEqual(week52_fit_base(45000), 33)
        self.assertEqual(week52_total(33), 45474)
        self.assertGreaterEqual(week52_total(week52_fit_base(45000)), 45000)

    def test_week52_bounds(self):
        with self.assertRaises(ValueError):
            week52_amount(0, 100)
        with self.assertRaises(ValueError):
            week52_amount(53, 100)
        with self.assertRaises(ValueError):
            week52_amount(1, 0)

    def test_random_plan_mint(self):
        p = random_plan(18, 100, "u01-2026")
        self.assertEqual(p["multiplier"], 38)
        self.assertEqual(p["amount_thb"], 3800)
        self.assertEqual(p["cumulative_thb"], 50200)
        self.assertEqual(p["kind"], "random")

    def test_random_order_stable(self):
        a = random_week_order("u01-2026")
        b = random_week_order("u01-2026")
        self.assertEqual(a, b)
        self.assertEqual(sorted(a), list(range(1, 53)))
        self.assertNotEqual(a, random_week_order("u02-2026"))

    def test_random_bounds(self):
        with self.assertRaises(ValueError):
            random_plan(0, 100, "x")

    # 4) Challenges + streaks
    def test_daily_challenge_mint(self):
        c = daily_challenge(TODAY, "u01")
        self.assertEqual(c["id"], "c03")
        self.assertEqual(c["name_th"], "งดเดลิเวอรี่")
        self.assertEqual(c["save_thb"], 120)
        self.assertTrue(c["suggested"])

    def test_complete_skip_cafe(self):
        self.assertEqual(MINT_CHALLENGE["save_thb"], 85)
        self.assertEqual(MINT_CHALLENGE["xp"], 10)
        self.assertTrue(MINT_CHALLENGE["done"])
        self.assertIn("งดกาแฟร้าน", MINT_CHALLENGE["message_th"])

    def test_unknown_challenge(self):
        with self.assertRaises(ValueError):
            complete_challenge("lottery", TODAY)

    def test_mint_streak_12(self):
        self.assertEqual(self.st["days"], 12)
        self.assertEqual(self.st["frozen_used"], 0)
        self.assertTrue(self.st["today_saved"])
        self.assertEqual(self.st["badge_th"], "ไฟลุก")

    def test_bee_streak_with_freeze(self):
        s = streak(BEE_DATES, TODAY, BEE_FROZEN)
        self.assertEqual(s["days"], 7)
        self.assertEqual(s["frozen_used"], 1)
        self.assertTrue(s["today_saved"])

    def test_streak_broken(self):
        s = streak(["2026-11-01"], TODAY)
        self.assertEqual(s["days"], 0)
        self.assertEqual(s["badge_th"], "ยังไม่เริ่ม")

    def test_streak_yesterday_only(self):
        s = streak(["2026-12-02"], TODAY)
        self.assertEqual(s["days"], 1)
        self.assertFalse(s["today_saved"])
        self.assertEqual(s["badge_th"], "กำลังเริ่ม")

    # 5) Library, round-up, team
    def test_library(self):
        self.assertEqual(len(GOALS), 7)
        self.assertEqual(len(set(v["id"] for v in GOALS.values())), 7)
        info = goal_info("japan_trip")
        self.assertEqual(info["name_th"], "เที่ยวญี่ปุ่น")
        self.assertEqual(info["sample_thb"], 45000)
        self.assertEqual(len(CHALLENGES), 8)

    def test_unknown_goal(self):
        with self.assertRaises(ValueError):
            goal_info("yacht")

    def test_round_up(self):
        self.assertEqual(round_up(87, 10), {"amount_thb": 87, "step_thb": 10, "extra_thb": 3, "rounded_thb": 90})
        self.assertEqual(round_up(90, 10)["extra_thb"], 0)
        self.assertEqual(round_up(87, 50)["extra_thb"], 13)
        with self.assertRaises(ValueError):
            round_up(-1, 10)
        with self.assertRaises(ValueError):
            round_up(10, 0)

    def test_team_jar(self):
        t = team_jar(45000, MINT_TEAM)
        self.assertEqual(t["saved_thb"], 24000)
        self.assertEqual(t["pct"], 53)
        self.assertEqual(t["level"], "halfway")
        self.assertEqual(t["member_count"], 3)
        self.assertEqual(t["members"][0]["pct"], 42)

    def test_team_empty_or_bad(self):
        with self.assertRaises(ValueError):
            team_jar(45000, [])
        with self.assertRaises(ValueError):
            team_jar(45000, [{"name_th": "x", "amount_thb": -1}])

    # 6) Share, quota, safety
    def test_share(self):
        s = share_card("น้องมิ้น", "เที่ยวญี่ปุ่น", 42, 12)
        self.assertEqual(s["headline_th"], "เที่ยวญี่ปุ่น · กระปุกโตถึง 42%")
        self.assertIn("SAVE", s["cta_th"])
        self.assertIn("12", s["cta_th"])

    def test_quota(self):
        self.assertEqual(quota(1, 1), {"allowed": 1, "left_after": 1, "paywall": False})
        self.assertEqual(quota(3, 1), {"allowed": 0, "left_after": 0, "paywall": True})
        self.assertEqual(quota(0, 5, pro=True)["paywall"], False)

    def test_safety_guard(self):
        self.assertEqual(safety_guard(True)["level"], "ok")
        self.assertEqual(safety_guard(False)["level"], "stop")
        self.assertIn("ไม่ใช่บัญชีธนาคาร", safety_guard()["message_th"])

    def test_mint_dates_len(self):
        self.assertEqual(len(MINT_DATES), 12)
        self.assertEqual(MINT_DATES[0], "2026-11-22")
        self.assertEqual(MINT_DATES[-1], TODAY)

    def test_week52_week1(self):
        self.assertEqual(week52_amount(1, 100), 100)
        self.assertEqual(week52_cumulative(1, 100), 100)
        self.assertEqual(week52_plan(1, 50)["amount_thb"], 50)

    def test_levels_edges(self):
        self.assertEqual(jar_level(9), ("empty", "แทบยังไม่เริ่ม"))
        self.assertEqual(jar_level(10)[0], "growing")
        self.assertEqual(jar_level(49)[0], "growing")
        self.assertEqual(jar_level(50)[0], "halfway")
        self.assertEqual(jar_level(74)[0], "halfway")
        self.assertEqual(jar_level(75)[0], "almost")
        self.assertEqual(jar_level(99)[0], "almost")
        self.assertEqual(jar_level(100)[0], "full")

    def test_challenge_bank_ids_unique(self):
        self.assertEqual(len(set(v["id"] for v in CHALLENGES.values())), 8)
        self.assertTrue(all(c["save_thb"] > 0 for c in CHALLENGES.values()))


    def test_photo_goal_id(self):
        self.assertEqual(self.scan["photo_id"], "p01")
        self.assertEqual(self.scan["goal_id"], "japan_trip")

    def test_week52_bee_base50(self):
        p = week52_plan(26, 50)
        self.assertEqual(p["amount_thb"], 1300)
        self.assertEqual(p["cumulative_thb"], 17550)

    def test_daily_challenge_stable(self):
        self.assertEqual(daily_challenge(TODAY, "u01"), daily_challenge(TODAY, "u01"))
        self.assertNotEqual(daily_challenge(TODAY, "u01")["id"], daily_challenge(TODAY, "u02")["id"])

    def test_team_headline(self):
        t = team_jar(45000, MINT_TEAM)
        self.assertEqual(t["headline_th"], "กระปุกร่วม โตถึง 53%")
        self.assertEqual(t["remaining_thb"], 21000)

    def test_share_sizes(self):
        s = share_card("น้องมิ้น", "เที่ยวญี่ปุ่น", 42, 12)
        self.assertEqual(s["layout"], "jar_milestone")
        self.assertIn("1080x1350", s["sizes"])
        self.assertIn("not a bank", s["watermark"])


if __name__ == "__main__":
    unittest.main()
