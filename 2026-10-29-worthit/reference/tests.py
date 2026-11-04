import unittest
from worthit import *
from fixtures import *
class T(unittest.TestCase):
    def test_wage(self): self.assertEqual(hourly_wage(25000), 142.05)
    def test_wage_bad(self):
        with self.assertRaises(ValueError): hourly_wage(0)
    def test_bag_hours(self):
        w = work_time(3990, PROFILE); self.assertEqual(w["hours"], 28.1); self.assertEqual(w["work_days"], 3.5); self.assertEqual(w["pct_of_month"], 16.0)
    def test_label(self): self.assertEqual(work_time(3990, PROFILE)["label_th"], "ต้องทำงาน 28 ชม. 5 นาที")
    def test_latte(self): self.assertEqual(work_time(75, PROFILE)["hours"], 0.5)
    def test_fmt_round(self): self.assertEqual(fmt_hours(1.999), "2 ชม.")
    def test_cpu_sneaker(self): c = cost_per_use(2890, 12, 12); self.assertEqual(c["per_use_thb"], 20.07); self.assertEqual(c["tier"], "amber")
    def test_cpu_bag(self): c = cost_per_use(3990, 2, 12); self.assertEqual(c["per_use_thb"], 166.25); self.assertEqual(c["tier"], "red")
    def test_cpu_zero(self): self.assertEqual(cost_per_use(500, 0, 12)["tier"], "red")
    def test_verdict_bag(self): v = verdict(BAG_ANS, "red", 16.0); self.assertEqual((v["score"], v["verdict"]), (5, "skip"))
    def test_verdict_sneaker(self): v = verdict(SNEAKER_ANS, "amber", 11.6); self.assertEqual((v["score"], v["verdict"]), (95, "buy"))
    def test_verdict_phone(self): v = verdict(PHONE_ANS, "green", 131.6); self.assertEqual((v["score"], v["verdict"]), (30, "skip"))
    def test_verdict_missing(self):
        with self.assertRaises(ValueError): verdict({"need": True}, "green", 1)
    def test_cooloff(self):
        self.assertEqual(cooloff_hours(75, 0.3), 0); self.assertEqual(cooloff_hours(3990, 16.0), 24); self.assertEqual(cooloff_hours(32900, 131.6), 72)
    def test_cooloff_status(self):
        s = cooloff_status("2026-10-29T08:00:00+07:00", 24, "2026-10-29T20:00:00+07:00"); self.assertEqual(s["hours_left"], 12.0); self.assertFalse(s["unlocked"])
        self.assertTrue(cooloff_status("2026-10-29T08:00:00+07:00", 24, "2026-10-30T09:00:00+07:00")["unlocked"])
    def test_jar(self): j = skip_jar(SKIPS, 15000); self.assertEqual((j["saved_thb"], j["goal_pct"], j["reached"]), (6870, 45.8, False))
    def test_jar_reached(self): self.assertTrue(skip_jar([{"price_thb": 20000}], 15000)["reached"])
    def test_report(self):
        r = month_report(DECISIONS, PROFILE); self.assertEqual((r["skipped"], r["saved_thb"], r["hours_saved"], r["biggest_skip"]), (3, 6870, 48.4, "กระเป๋าสะพายข้าง"))
    def test_report_empty(self): self.assertIsNone(month_report([], PROFILE)["biggest_skip"])
    def test_minutes_only(self): self.assertEqual(work_time(75, PROFILE)["label_th"], "ต้องทำงาน 32 นาที")
    def test_habit(self): h = habit_cost(75, 5, PROFILE); self.assertEqual((h["per_month_thb"], h["per_year_thb"], h["hours_per_month"], h["hours_per_year"]), (1625.0, 19500, 11.4, 137.3))
if __name__ == "__main__": unittest.main()
