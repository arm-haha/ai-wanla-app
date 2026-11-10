import unittest
from fitdeck import *
from fixtures import *

class T(unittest.TestCase):
    def setUp(self):
        self.gear = parse_gear(GIFT_SHOT)
        self.plan = make_plan(self.gear, "beginner")
        self.timers = timer_cards(self.plan)

    def test_gift_quality(self):
        self.assertEqual(self.gear["quality"]["score"], 90)
        self.assertTrue(self.gear["ok"])
        self.assertEqual(self.gear["weight_kg"], 4)
        self.assertIn("yoga_mat", self.gear["keys"])
        self.assertIn("4 กก.", self.gear["message_th"])

    def test_gift_plan(self):
        self.assertEqual([m["key"] for m in self.plan["moves"]],
                         ["march_warm", "goblet_squat", "knee_push", "glute_bridge", "dumbbell_row", "dead_bug", "stretch_close"])
        self.assertEqual(self.plan["total_sec"], 1200)
        self.assertEqual(self.plan["total_min"], 20.0)
        self.assertEqual(self.plan["count"], 7)
        self.assertIn("20 นาที", self.plan["headline_th"])
        self.assertEqual(self.plan["level"], "beginner")

    def test_timers(self):
        self.assertEqual(self.timers["total_sec"], 1200)
        self.assertEqual(self.timers["cards"][0]["start_sec"], 0)
        self.assertEqual(self.timers["cards"][-1]["end_sec"], 1200)
        self.assertEqual(self.timers["cards"][1]["start_sec"], 120)
        self.assertIn("สกวอตถือดัมเบิล", self.timers["cards"][1]["cue_th"])

    def test_bee_plan(self):
        p = make_plan(parse_gear(BEE_SHOT), "beginner")
        self.assertEqual(p["total_sec"], 1200)
        keys = [m["key"] for m in p["moves"]]
        self.assertEqual(len(keys), len(set(keys)))
        self.assertIn("chair_sit", keys)
        self.assertIn("wall_push", keys)
        self.assertNotIn("goblet_squat", keys)

    def test_ton_intermediate(self):
        p = make_plan(parse_gear(TON_SHOT), "intermediate")
        self.assertEqual(p["total_sec"], 1200)
        keys = [m["key"] for m in p["moves"]]
        self.assertIn("jump_rope", keys)
        self.assertIn("band_row", keys)
        self.assertNotIn("goblet_squat", keys)

    def test_lowconf_drops_dumbbell(self):
        g = parse_gear(LOWCONF_SHOT)
        self.assertIn("yoga_mat", g["keys"])
        self.assertNotIn("dumbbell", g["keys"])
        p = make_plan(g, "beginner")
        self.assertNotIn("goblet_squat", [m["key"] for m in p["moves"]])
        self.assertIn("knee_push", [m["key"] for m in p["moves"]])

    def test_bad_quality(self):
        g = parse_gear(BAD_SHOT)
        self.assertEqual(g["quality"]["score"], 43)
        self.assertFalse(g["ok"])
        with self.assertRaises(ValueError):
            make_plan(g)

    def test_empty(self):
        g = parse_gear(EMPTY_SHOT)
        self.assertFalse(g["ok"])
        self.assertEqual(g["quality"]["score"], 54)
        self.assertEqual(g["keys"], ["bodyweight"])

    def test_bad_input(self):
        with self.assertRaises(ValueError):
            scan_quality(1.2, 0, 0, 1)

    def test_unknown_level(self):
        with self.assertRaisesRegex(ValueError, "unknown level"):
            make_plan(self.gear, "elite")

    def test_log_complete(self):
        log = log_session([], TODAY, self.plan, 7, "ok")
        self.assertEqual(log["finished_sessions"], 1)
        self.assertFalse(log["rows"][0]["stopped"])
        self.assertEqual(log["rows"][0]["total_sec"], 1200)

    def test_log_stop(self):
        log = log_session([], TODAY, self.plan, 2, "stop")
        self.assertTrue(log["rows"][0]["stopped"])
        self.assertEqual(log["finished_sessions"], 0)
        self.assertEqual(log["rows"][0]["total_sec"], 120 + 180)

    def test_log_accumulate(self):
        log = log_session([], TODAY, self.plan, 7, "easy")
        log = log_session(log["rows"], "2026-12-02", self.plan, 7, "hard")
        self.assertEqual(log["count"], 2)
        self.assertEqual(log["finished_sessions"], 2)

    def test_log_errors(self):
        with self.assertRaises(ValueError):
            log_session([], TODAY, self.plan, 8, "ok")
        with self.assertRaises(ValueError):
            log_session([], TODAY, self.plan, 3, "pain")

    def test_share(self):
        s = share_card("พี่กิ๊ฟ", self.plan)
        self.assertEqual(s["total_min"], 20.0)
        self.assertEqual(s["count"], 7)
        self.assertIn("FIT", s["cta_th"])
        self.assertTrue(s["hook_th"].startswith("ถ่ายอุปกรณ์ที่มี"))
        self.assertEqual(s["layout"], "fit_card")

    def test_quota(self):
        self.assertEqual(quota(1, 1), {"allowed": 1, "left_after": 1, "paywall": False})
        self.assertEqual(quota(3, 1), {"allowed": 0, "left_after": 0, "paywall": True})
        self.assertEqual(quota(0, 5, pro=True)["paywall"], False)

    def test_safety(self):
        self.assertEqual(safety_guard()["level"], "ok")
        self.assertEqual(safety_guard(pain=True)["level"], "stop")
        self.assertEqual(safety_guard(dizzy=True)["level"], "stop")
        self.assertEqual(safety_guard(cleared=False)["level"], "warn")
        self.assertIn("ไม่ใช่เทรนเนอร์", safety_guard()["message_th"])

    def test_move_numbers(self):
        self.assertEqual([m["n"] for m in self.plan["moves"]], list(range(1, 8)))

    def test_safety_on_moves(self):
        squat = self.plan["moves"][1]
        self.assertIn("หลังตรง", squat["safety_th"])

    def test_bee_quality(self):
        self.assertEqual(parse_gear(BEE_SHOT)["quality"]["score"], 89)

    def test_ton_quality(self):
        self.assertEqual(parse_gear(TON_SHOT)["quality"]["score"], 90)

    def test_library(self):
        self.assertGreaterEqual(len(EXERCISES), 14)
        ids = [e["id"] for e in EXERCISES.values()]
        self.assertEqual(len(ids), len(set(ids)))

    def test_need_subset(self):
        self.assertEqual(EXERCISES["goblet_squat"]["need"], {"dumbbell"})
        self.assertEqual(EXERCISES["march_warm"]["need"], set())

    def test_watermark(self):
        self.assertIn("not a trainer", WATERMARK)

    def test_gift_count_gear(self):
        self.assertEqual(self.gear["count"], 2)

    def test_plan_disclaimer(self):
        self.assertIn("แพทย์", self.plan["disclaimer_th"])

    def test_timer_monotonic(self):
        starts = [c["start_sec"] for c in self.timers["cards"]]
        self.assertEqual(starts, sorted(starts))

    def test_intermediate_gift(self):
        p = make_plan(self.gear, "intermediate")
        self.assertEqual(p["total_sec"], 1200)
        self.assertIn("overhead_press", [m["key"] for m in p["moves"]])

    def test_bodyweight_forced(self):
        g = dict(parse_gear(EMPTY_SHOT), ok=True)
        p = make_plan(g, "beginner")
        self.assertGreaterEqual(p["count"], 5)
        self.assertIn("body_squat", [m["key"] for m in p["moves"]])
        self.assertNotIn("goblet_squat", [m["key"] for m in p["moves"]])

    def test_share_level(self):
        self.assertEqual(share_card("พี่กิ๊ฟ", self.plan)["level"], "beginner")

    def test_first_move_warm(self):
        self.assertEqual(self.plan["moves"][0]["name_th"], "เดินยกเข่าอุ่นเครื่อง")

    def test_last_move_stretch(self):
        self.assertEqual(self.plan["moves"][-1]["key"], "stretch_close")

    def test_minutes_field(self):
        self.assertEqual(self.plan["moves"][0]["minutes"], 2.0)
        self.assertEqual(self.plan["moves"][1]["minutes"], 3.0)

    def test_log_headline(self):
        self.assertIn("1 ครั้ง", log_session([], TODAY, self.plan, 7)["headline_th"])

    def test_equipment_names(self):
        self.assertEqual(EQUIPMENT["yoga_mat"]["name_th"], "เสื่อโยคะ")

    def test_feeling_hard_still_finished(self):
        log = log_session([], TODAY, self.plan, 7, "hard")
        self.assertFalse(log["rows"][0]["stopped"])

    def test_partial_not_stop_feeling_still_stopped(self):
        log = log_session([], TODAY, self.plan, 5, "ok")
        self.assertTrue(log["rows"][0]["stopped"])

    def test_muscles_on_squat(self):
        self.assertIn("legs", self.plan["moves"][1]["muscles"])

    def test_bee_no_mat_moves(self):
        keys=[m["key"] for m in make_plan(parse_gear(BEE_SHOT),"beginner")["moves"]]
        self.assertNotIn("knee_push", keys)
        self.assertNotIn("dead_bug", keys)

    def test_target_constant(self):
        self.assertEqual(TARGET_SEC, 1200)

    def test_weight_none_bee(self):
        self.assertIsNone(parse_gear(BEE_SHOT)["weight_kg"])

if __name__ == "__main__":
    unittest.main()
