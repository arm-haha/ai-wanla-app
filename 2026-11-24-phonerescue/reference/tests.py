import unittest
from phonerescue import *
from fixtures import *

class T(unittest.TestCase):
    def setUp(self):
        self.st = parse_storage(POR_STORAGE)
        self.bt = parse_battery(POR_BATTERY)
        self.plan = cleanup_plan(self.st)

    def test_por_storage(self):
        self.assertEqual((self.st["used_gb"], self.st["total_gb"], self.st["free_gb"], self.st["percent"]), (127, 128, 1, 99))
        self.assertEqual(self.st["breakdown"]["photos_gb"], 84)
        self.assertTrue(self.st["ok"])

    def test_por_quality(self):
        self.assertEqual(self.st["quality"]["score"], 90)
        self.assertEqual(self.st["quality"]["tips_th"], [])

    def test_por_battery(self):
        self.assertEqual(self.bt["health_pct"], 86)
        self.assertEqual(self.bt["brightness_pct"], 80)
        self.assertTrue(self.bt["background_refresh"])
        self.assertFalse(self.bt["low_power"])

    def test_cleanup_saved(self):
        self.assertEqual(self.plan["saved_gb"], 16.8)
        self.assertEqual((self.plan["after_used_gb"], self.plan["after_free_gb"]), (110.2, 17.8))
        self.assertIn("16.8 GB", self.plan["headline_th"])
        self.assertEqual([a["key"] for a in self.plan["actions"]], ["duplicates", "screenshots", "chat_backup", "unused_apps", "cache"])

    def test_cleanup_priority_numbers(self):
        self.assertEqual([a["n"] for a in self.plan["actions"]], list(range(1, 6)))
        self.assertEqual(self.plan["actions"][0]["gb"], 6.2)

    def test_subset_plan(self):
        p = cleanup_plan(self.st, include=["duplicates", "cache"])
        self.assertEqual(p["saved_gb"], 7.3)
        self.assertEqual(p["count"], 2)

    def test_plan_requires_ok(self):
        with self.assertRaises(ValueError):
            cleanup_plan(parse_storage(EMPTY_SHOT))
        with self.assertRaises(ValueError):
            cleanup_plan(self.st, include=["factory_reset"])

    def test_duplicate_guide(self):
        g = duplicate_guide()
        self.assertEqual(len(g["steps"]), 5)
        self.assertEqual(g["steps"][0]["n"], 1)
        self.assertIn("สำรอง", g["steps"][0]["text_th"])

    def test_por_tips(self):
        t = battery_tips(self.bt)
        self.assertEqual(t["count"], 5)
        self.assertEqual(t["keys"][0], "health_ok")
        self.assertIn("brightness", t["keys"])
        self.assertIn("86%", t["headline_th"])

    def test_muk_tips_no_brightness(self):
        t = battery_tips(parse_battery(MUK_BATTERY))
        self.assertEqual(t["keys"][0], "health_low")  # 76% is below 80
        self.assertNotIn("brightness", t["keys"])
        self.assertNotIn("background", t["keys"])

    def test_old_tips(self):
        t = battery_tips(parse_battery(OLD_BATTERY))
        self.assertEqual(t["keys"][0], "health_low")

    def test_repair_por(self):
        r = repair_or_replace(self.st, self.bt)
        self.assertEqual(r["verdict"], "cleanup")
        self.assertEqual((r["battery_min_thb"], r["battery_max_thb"]), (1900, 3500))
        self.assertEqual((r["phone_min_thb"], r["phone_max_thb"]), (12900, 19900))

    def test_repair_muk(self):
        self.assertEqual(repair_or_replace(parse_storage(MUK_STORAGE), parse_battery(MUK_BATTERY))["verdict"], "repair_battery")

    def test_repair_old(self):
        self.assertEqual(repair_or_replace(parse_storage(OLD_STORAGE), parse_battery(OLD_BATTERY))["verdict"], "replace_or_repair")

    def test_watch_healthy_free(self):
        st = dict(self.st, free_gb=20, used_gb=108)
        bt = dict(self.bt, health_pct=90)
        self.assertEqual(repair_or_replace(st, bt)["verdict"], "watch")

    def test_cleanup_then_watch(self):
        st = dict(self.st, free_gb=2)
        bt = dict(self.bt, health_pct=82)
        self.assertEqual(repair_or_replace(st, bt)["verdict"], "cleanup_then_watch")

    def test_quality_tips(self):
        q = parse_storage(BAD_SHOT)["quality"]
        self.assertEqual(q["score"], 43)
        self.assertFalse(q["ok"])
        self.assertGreaterEqual(len(q["tips_th"]), 3)

    def test_empty_and_lowconf(self):
        e = parse_storage(EMPTY_SHOT)
        self.assertFalse(e["ok"])
        self.assertIn("ไม่เจอตัวเลข", " ".join(e["quality"]["tips_th"]))
        low = parse_storage(LOWCONF_SHOT)
        self.assertIsNone(low["used_gb"])
        self.assertEqual(low["total_gb"], 128)

    def test_bad_input(self):
        with self.assertRaises(ValueError):
            scan_quality(1.2, 0, 0, 1)

    def test_pipeline(self):
        self.assertEqual(pipeline_steps(POR_STORAGE), ["screen_detect", "ocr_storage", "cleanup_plan"])
        self.assertEqual(pipeline_steps(POR_BATTERY), ["screen_detect", "ocr_battery", "battery_tips", "repair_check"])
        self.assertIn("deglare", pipeline_steps(BAD_SHOT))
        self.assertEqual(pipeline_steps(EMPTY_SHOT)[-1], "need_settings_page")

    def test_share(self):
        s = share_card("น้องปอ", self.st, self.plan, self.bt)
        self.assertIn("16.8 GB", s["headline_th"])
        self.assertEqual(s["health_pct"], 86)
        self.assertIn("PHONE", s["cta_th"])

    def test_quota(self):
        self.assertEqual(quota(1, 1), {"allowed": 1, "left_after": 1, "paywall": False})
        self.assertEqual(quota(3, 1), {"allowed": 0, "left_after": 0, "paywall": True})
        self.assertEqual(quota(0, 5, pro=True)["paywall"], False)

    def test_safety(self):
        self.assertEqual(safety_guard()["level"], "ok")
        self.assertEqual(safety_guard(True, False)["level"], "stop")
        self.assertEqual(safety_guard(True, True)["level"], "warn")
        self.assertIn("สำรองข้อมูล", safety_guard()["message_th"])

    def test_battery_missing(self):
        b = parse_battery(EMPTY_SHOT)
        self.assertFalse(b["ok"])
        with self.assertRaises(ValueError):
            battery_tips(b)

    def test_message_copy(self):
        self.assertIn("เหลือ 1 GB", self.st["message_th"])

    def test_library(self):
        self.assertEqual(len(CLEANUP), 5)
        self.assertEqual(round(sum(c["gb"] for c in CLEANUP.values()), 1), 16.8)

    def test_repair_needs_both(self):
        with self.assertRaises(ValueError):
            repair_or_replace(parse_storage(EMPTY_SHOT), self.bt)

    def test_guide_disclaimer(self):
        self.assertIn("สำรองก่อนลบ", duplicate_guide()["disclaimer_th"])

    def test_muk_storage_free(self):
        self.assertEqual(parse_storage(MUK_STORAGE)["free_gb"], 86)

    def test_share_hook(self):
        s = share_card("น้องปอ", self.st, self.plan, self.bt)
        self.assertEqual(s["layout"], "rescue_card")
        self.assertTrue(s["hook_th"].startswith("มือถือเต็ม"))

    def test_percent_rounding(self):
        self.assertEqual(parse_storage(OLD_STORAGE)["percent"], 47)  # 30/64

    def test_actions_unique_ids(self):
        ids = [c["id"] for c in CLEANUP.values()]
        self.assertEqual(len(ids), len(set(ids)))

    def test_low_power_false_tip(self):
        self.assertIn("low_power", battery_tips(self.bt)["keys"])
        self.assertNotIn("low_power", battery_tips(parse_battery(MUK_BATTERY))["keys"])

    def test_cleanup_after_not_negative(self):
        tiny = dict(self.st, used_gb=2, free_gb=126)
        p = cleanup_plan(tiny)
        self.assertEqual(p["after_used_gb"], 0)
        self.assertEqual(p["after_free_gb"], 128)


    def test_health_watch_boundary(self):
        bt=dict(self.bt, health_pct=80, brightness_pct=40, background_refresh=False, low_power=True, screen_on_h=3)
        self.assertEqual(battery_tips(bt)["keys"], ["health_watch"])

    def test_health_ok_boundary(self):
        bt=dict(self.bt, health_pct=85, brightness_pct=40, background_refresh=False, low_power=True, screen_on_h=3)
        self.assertEqual(battery_tips(bt)["keys"], ["health_ok"])

    def test_share_saved(self):
        self.assertEqual(share_card("น้องปอ", self.st, self.plan, self.bt)["saved_gb"], 16.8)

    def test_old_free(self):
        self.assertEqual(parse_storage(OLD_STORAGE)["free_gb"], 34)

    def test_battery_quality_por(self):
        self.assertTrue(self.bt["quality"]["ok"])
        self.assertGreaterEqual(self.bt["quality"]["score"], 80)

    def test_breakdown_sum(self):
        b=self.st["breakdown"]
        self.assertEqual(b["photos_gb"]+b["apps_gb"]+b["system_gb"]+b["other_gb"], 127)

    def test_unknown_action_message(self):
        with self.assertRaisesRegex(ValueError, "unknown action"):
            cleanup_plan(self.st, include=["factory_reset"])

if __name__ == "__main__":
    unittest.main()
