import unittest
from wattwise import *
from fixtures import *
class T(unittest.TestCase):
    def test_kwh(self): self.assertEqual(kwh_month(1000, 8), 240.0)
    def test_kwh_day(self): self.assertEqual(kwh_month(kwh_per_day=1.2), 36.0)
    def test_kwh_bad(self):
        with self.assertRaises(ValueError): kwh_month(100, 25)
    def test_ac_cost(self): c = appliance_cost(APPS[0], RATE); self.assertEqual((c["cost_month_thb"], c["tier"], c["cost_per_hour_thb"]), (1008.0, "red", 4.2))
    def test_heater(self): self.assertEqual(appliance_cost(APPS[2], RATE)["cost_per_hour_thb"], 14.7)
    def test_rate_bad(self):
        with self.assertRaises(ValueError): appliance_cost(APPS[0], 0)
    def test_breakdown(self):
        b = bill_breakdown(BILL, APPS, RATE)
        self.assertEqual((b["estimated_kwh"], b["unexplained_kwh"], b["unexplained_pct"], b["top_appliance_id"]), (353.25, 86.75, 19.72, "ac"))
        self.assertEqual(b["slices"][0]["pct"], 54.55)
    def test_breakdown_over(self): self.assertTrue(bill_breakdown({"units_kwh": 100, "total_thb": 420}, APPS, RATE)["over_estimated"])
    def test_ac_sim(self): a = ac_temp_sim(1008, 25, 27); self.assertEqual((a["new_cost_thb"], a["save_month_thb"], a["save_year_thb"]), (816.48, 191.52, 2298.24))
    def test_ac_lower(self): self.assertLess(ac_temp_sim(1008, 26, 24)["save_month_thb"], 0)
    def test_ac_bad(self):
        with self.assertRaises(ValueError): ac_temp_sim(1000, 10, 25)
    def test_standby(self): s = standby_leak(STANDBY, RATE); self.assertEqual((s["total_standby_watt"], s["cost_month_thb"], s["cost_year_thb"], s["worst_id"]), (20, 60.48, 725.76, "router"))
    def test_standby_empty(self): self.assertIsNone(standby_leak([], RATE)["worst_id"])
    def test_goal(self):
        g = goal_track(READINGS, 1500, RATE, "2026-10-15")
        self.assertEqual((g["used_kwh"], g["per_day_kwh"], g["projected_thb"], g["on_track"], g["gap_thb"], g["budget_per_day_kwh"]), (182.7, 13.05, 1699.11, False, 199.11, 11.52))
    def test_goal_ok(self): self.assertTrue(goal_track(READINGS, 1800, RATE, "2026-10-15")["on_track"])
    def test_goal_backwards(self):
        with self.assertRaises(ValueError): goal_track([{"date": "2026-10-01", "meter_kwh": 10}, {"date": "2026-10-02", "meter_kwh": 5}], 1000, RATE, "2026-10-02")
    def test_split(self): s = room_split(1848, ROOMS); self.assertEqual([x["thb"] for x in s], [1092.0, 756.0])
    def test_split_sum(self): s = room_split(1000, [{"name": "a", "kwh": 1}, {"name": "b", "kwh": 1}, {"name": "c", "kwh": 1}]); self.assertAlmostEqual(sum(x["thb"] for x in s), 1000, places=2)
    def test_payback(self): p = swap_payback(1000, 700, 8, 15900, RATE); self.assertEqual((p["save_month_thb"], p["payback_months"]), (302.4, 52.58))
    def test_payback_none(self): self.assertIsNone(swap_payback(60, 60, 5, 200, RATE)["payback_months"])
if __name__ == "__main__": unittest.main()
