import unittest
from fixmate import *
from fixtures import *
class T(unittest.TestCase):
    def test_gate_ok(self): self.assertEqual(safety_gate(FAUCET)["level"], OK)
    def test_gate_stop(self):
        g = safety_gate(OUTLET); self.assertEqual(g["level"], STOP); self.assertFalse(g["allow_diy"])
    def test_gate_caution_lowconf(self):
        g = safety_gate(AIRCON); self.assertEqual(g["level"], CAUTION); self.assertEqual(len(g["reasons"]), 2)
    def test_cost(self):
        c = diy_cost(FAUCET_PARTS, FAUCET_TOOLS, OWNED)
        self.assertEqual((c["parts_thb"], c["tools_thb"], c["total_thb"]), (25, 120, 145))
    def test_cost_all_owned(self):
        self.assertEqual(diy_cost(FAUCET_PARTS, FAUCET_TOOLS, ["screwdriver","adj_wrench"])["total_thb"], 25)
    def test_verdict_diy(self):
        v = verdict(FAUCET, FAUCET_PARTS, FAUCET_TOOLS, OWNED, 500)
        self.assertEqual((v["verdict"], v["save_thb"]), ("diy", 355))
    def test_verdict_stop(self):
        v = verdict(OUTLET, [], [], OWNED, 400); self.assertEqual((v["verdict"], v["save_thb"]), ("call_pro", 0))
    def test_verdict_too_expensive(self):
        self.assertEqual(verdict(FAUCET, FAUCET_PARTS, FAUCET_TOOLS, OWNED, 100)["verdict"], "call_pro")
    def test_verdict_bad_quote(self):
        with self.assertRaises(ValueError): verdict(FAUCET, [], [], OWNED, 0)
    def test_drip(self):
        self.assertEqual(drip_waste(60), {"liters_month":130,"buckets_10l":13})
        self.assertEqual(drip_waste(0)["liters_month"], 0)
    def test_progress(self):
        p = step_progress(FAUCET_STEPS, {"s1","s2"})
        self.assertEqual((p["pct"], p["minutes_left"], p["next_step"]), (40, 15, "s3"))
    def test_progress_done(self):
        self.assertEqual(step_progress(FAUCET_STEPS, {s["id"] for s in FAUCET_STEPS})["next_step"], None)
    def test_care(self):
        c = care_schedule(CARE, TODAY)
        self.assertEqual(c[0]["id"], "ac_filter"); self.assertEqual(c[0]["overdue_days"], 17)
        self.assertEqual(next(x for x in c if x["id"]=="ac_service")["overdue_days"], 0)
        self.assertEqual(next(x for x in c if x["id"]=="ac_service")["due_in_days"], 32)
    def test_tally(self):
        f = [{"verdict":"diy","status":"fixed","save_thb":355,"minutes":20},
             {"verdict":"diy","status":"fixed","save_thb":480,"minutes":15},
             {"verdict":"call_pro","status":"fixed","save_thb":0,"minutes":0}]
        t = savings_tally(f); self.assertEqual((t["fixes"], t["saved_thb"], t["badge"]), (2, 835, "มือใหม่ซ่อมเป็น"))
    def test_toilet(self):
        self.assertEqual(verdict(TOILET, TOILET_PARTS, [], OWNED, 600)["save_thb"], 480)
    def test_low_conf_needs_photo(self):
        v = verdict(AIRCON, [], [], OWNED, 800); self.assertEqual((v["verdict"], v["save_thb"]), ("need_photo", 0))
    def test_msg(self):
        m = pro_message(OUTLET, "ห้องนอน คอนโดชั้น 12", 2); self.assertIn("ปลั๊กไฟมีรอยไหม้", m); self.assertIn("2 รูป", m)
if __name__ == "__main__": unittest.main(verbosity=1)
