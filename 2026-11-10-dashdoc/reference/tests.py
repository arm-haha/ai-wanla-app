import unittest
from dashdoc import *
from fixtures import *

class T(unittest.TestCase):
    def setUp(self):
        self.scan = light_scan(OAT_PHOTO)
        self.v = drive_verdict(self.scan["lights"], OAT_SYMPTOMS)

    # 1) Light Scan
    def test_oat_lights(self):
        self.assertEqual([l["symbol"] for l in self.scan["lights"]], ["check_engine", "tpms"])
        self.assertEqual(self.scan["uncertain"], ["service_due"])
        self.assertEqual(self.scan["light_count"], 2)

    def test_oat_quality(self):
        q = self.scan["quality"]
        self.assertEqual(q["score"], 86)
        self.assertTrue(q["ok"])
        self.assertEqual(q["tips_th"], [])

    def test_quality_tips(self):
        s = light_scan(PHOTOS[3])
        self.assertEqual(s["quality"]["score"], 54)
        self.assertFalse(s["quality"]["ok"])
        self.assertGreaterEqual(len(s["quality"]["tips_th"]), 2)

    def test_no_lights(self):
        s = light_scan(PHOTOS[7])
        self.assertFalse(s["quality"]["ok"])
        self.assertEqual(s["light_count"], 0)
        self.assertIn("ไม่เจอไฟเตือน", " ".join(s["quality"]["tips_th"]))

    def test_bad_quality_input(self):
        with self.assertRaises(ValueError):
            scan_quality(1.5, 0, 0, 1)

    def test_unknown_symbol(self):
        with self.assertRaises(ValueError):
            identify_lights({"id": "x", "detections": [{"symbol": "ufo", "color_seen": "red", "confidence": 1}]})

    def test_pipeline(self):
        self.assertEqual(pipeline_steps(OAT_PHOTO), ["panel_detect", "symbol_classify", "color_check", "urgency", "price_range"])
        st = pipeline_steps(PHOTOS[3])
        self.assertIn("deglare", st)
        self.assertIn("deskew", st)

    def test_library(self):
        self.assertEqual(len(LIGHTS), 17)
        self.assertEqual(len(set(v["id"] for v in LIGHTS.values())), 17)
        for k, v in LIGHTS.items():
            for f in v["fixes"]:
                self.assertIn(f, FIXES)
            for c in v["checks"]:
                self.assertIn(c, CHECK_TEXT)

    # 2) Urgency + verdict
    def test_oat_verdict(self):
        v = self.v
        self.assertEqual((v["level"], v["score"]), ("yellow", 48))
        self.assertEqual((v["can_drive"], v["max_km"], v["max_speed_kmh"], v["within_days"]), (True, 50, 80, 1))
        self.assertIn("~50 กม.", v["headline_th"])

    def test_red_oil(self):
        v = drive_verdict(light_scan(PHOTOS[1])["lights"])
        self.assertEqual((v["level"], v["can_drive"], v["max_km"]), ("red", False, 0))
        self.assertEqual(v["score"], 85)

    def test_flashing_escalates(self):
        s = light_scan(PHOTOS[5])
        self.assertEqual(s["lights"][0]["severity"], "red")
        self.assertEqual(drive_verdict(s["lights"])["score"], 92)

    def test_color_red_escalates_yellow(self):
        l = light_scan(PHOTOS[6])["lights"][0]
        self.assertEqual(l["severity"], "red")

    def test_symptom_escalates(self):
        v = drive_verdict(self.scan["lights"], ["smoke", "burning_smell"])
        self.assertEqual(v["level"], "red")
        self.assertEqual(v["score"], 80)

    def test_minor_belt_green(self):
        s = light_scan(PHOTOS[4])
        self.assertTrue(all(l["severity"] == "green" for l in s["lights"] if l["symbol"] == "seat_belt"))
        v = drive_verdict(s["lights"])
        self.assertEqual(v["level"], "green")
        self.assertIsNone(v["max_km"])

    def test_two_red(self):
        v = drive_verdict(light_scan(PHOTOS[2])["lights"])
        self.assertEqual(v["level"], "red")
        self.assertEqual(v["score"], 85)

    def test_score_cap(self):
        lights = light_scan(PHOTOS[5])["lights"]
        self.assertEqual(urgency_score(lights, ["smoke", "knocking", "fluid_leak", "overheating", "power_loss", "brake_soft"]), 100)

    def test_empty_lights(self):
        with self.assertRaises(ValueError):
            drive_verdict([])
        self.assertEqual(urgency_score([]), 0)

    def test_levels(self):
        self.assertEqual([level_of(x) for x in (0, 29, 30, 69, 70)], ["green", "green", "yellow", "yellow", "red"])

    # 3) Do-this-now
    def test_steps_yellow(self):
        st = do_now_steps("yellow", ["check_engine", "tpms"])
        keys = [s["key"] for s in st]
        self.assertEqual(keys[:2], ["slow", "avoid_night_highway"])
        self.assertIn("gas_cap", keys)
        self.assertIn("tire_visual", keys)
        self.assertEqual(keys[-1], "go_garage")
        self.assertEqual([s["n"] for s in st], list(range(1, len(st) + 1)))

    def test_steps_red(self):
        keys = [s["key"] for s in do_now_steps("red", ["oil_pressure"])]
        self.assertEqual(keys[0], "hazard")
        self.assertIn("oil_level", keys)
        self.assertEqual(keys[-1], "call_help")

    # 4) Fair price
    def test_price_range_eco_bkk(self):
        r = price_range("f03")
        self.assertEqual((r["min_thb"], r["max_thb"]), (1200, 5500))

    def test_price_range_mult(self):
        r = price_range("f07", "province", "suv_pickup")
        self.assertEqual((r["min_thb"], r["max_thb"]), (2050, 5150))

    def test_likely_fixes(self):
        f = likely_fixes(["check_engine", "tpms"], limit=5)
        self.assertEqual([x["fix_id"] for x in f], ["f18", "f01", "f02", "f03", "f04"])

    def test_quote_verdicts(self):
        self.assertEqual(quote_check("f03", 4200)["verdict"], "fair")
        self.assertEqual(quote_check("f03", 6000)["verdict"], "high")
        self.assertEqual(quote_check("f03", 9000)["verdict"], "very_high")
        self.assertEqual(quote_check("f03", 500)["verdict"], "low")

    def test_quote_questions_negative(self):
        self.assertGreaterEqual(len(quote_check("f05", 3000)["questions_th"]), 2)
        with self.assertRaises(ValueError):
            quote_check("f05", -1)

    # 5) Mechanic card
    def test_card(self):
        fx = likely_fixes(["check_engine", "tpms"])
        c = mechanic_card(OAT, OAT_CAR, self.v, ["check_engine", "tpms"], OAT_SYMPTOMS, fx)
        self.assertTrue(c["line_share_url"].startswith("https://line.me/R/share?text="))
        self.assertIn("87,450", c["note_th"])
        self.assertEqual((c["budget_min_thb"], c["budget_max_thb"]), (300 + 0, 800 + 150))
        self.assertEqual(c["level"], "yellow")

    def test_card_symptoms(self):
        c = mechanic_card(OAT, OAT_CAR, self.v, ["tpms"], ["shaking"], [], "ขอเช็กด่วน")
        self.assertIn("รถสั่นมาก", c["note_th"])
        self.assertIn("ขอเช็กด่วน", c["note_th"])

    # 6) Diary
    def test_next_due_oil(self):
        e = service_entry(*SERVICE_LOG[0])
        n = next_due(e)
        self.assertEqual((n["due_km"], n["due_date"]), (86900, "2026-10-18"))

    def test_status_oil_overdue(self):
        r = reminder_status(service_entry(*SERVICE_LOG[0]), OAT_CAR["odometer_km"], TODAY)
        self.assertEqual(r["status"], "overdue")
        self.assertEqual(r["km_left"], -550)
        self.assertEqual(r["days_left"], -23)

    def test_status_tax_soon(self):
        r = reminder_status(service_entry(*SERVICE_LOG[4]), 87450, TODAY)
        self.assertEqual(r["status"], "soon")
        self.assertEqual(r["days_left"], 25)
        self.assertIsNone(r["km_left"])

    def test_status_battery_ok(self):
        r = reminder_status(service_entry(*SERVICE_LOG[2]), 87450, TODAY)
        self.assertEqual(r["status"], "ok")
        self.assertEqual(r["due_date"], "2028-03-02")

    def test_status_due(self):
        e = service_entry("x", "c01", "2026-06-01", 80000, "air_filter", 300, "อู่")
        self.assertEqual(reminder_status(e, 99700, "2026-07-01")["status"], "due")

    def test_month_end(self):
        e = service_entry("x", "c01", "2026-08-31", 1, "engine_oil", 1, "อู่")
        self.assertEqual(next_due(e)["due_date"], "2027-02-28")

    def test_bad_item(self):
        with self.assertRaises(ValueError):
            service_entry("x", "c01", "2026-01-01", 1, "wash", 1, "x")

    def test_diary_stats(self):
        st = diary_stats([service_entry(*e) for e in SERVICE_LOG])
        self.assertEqual((st["count"], st["total_thb"], st["avg_thb"], st["last_odometer_km"]), (5, 15595, 3119, 76900))
        self.assertEqual(st["top_item"], "act")
        self.assertEqual(diary_stats([])["count"], 0)

    # 7) Emergency kit
    def test_kit_placeholders(self):
        k = emergency_kit({})
        self.assertEqual(k["missing"], ["insurer", "tow", "garage"])
        self.assertEqual(len(k["contacts"]), 6)

    def test_kit_filled(self):
        k = emergency_kit({"insurer_hotline": "<เบอร์ในกรมธรรม์>", "insurer_th": "FictoInsure", "garage_phone": "081-000-0000"})
        self.assertEqual(k["missing"], ["tow"])
        self.assertIn("FictoInsure", [c for c in k["contacts"] if c["key"] == "insurer"][0]["label_th"])

    def test_guides(self):
        g = guide("jump_start")
        self.assertEqual(len(g["steps"]), 5)
        self.assertEqual(guide("flat_tire")["steps"][0]["n"], 1)
        self.assertEqual(set(emergency_kit({})["guides"]), set(GUIDES))

    # 8) Share + quota + safety
    def test_share(self):
        s = share_card("พี่โอ๊ต", ["check_engine", "tpms"], self.v)
        self.assertEqual(s["headline_th"], "ขับต่อได้ ~50 กม.")
        self.assertIn("Check engine + Low tire pressure", s["cta_th"])

    def test_quota(self):
        self.assertEqual(quota(1, 1), {"allowed": 1, "left_after": 1, "paywall": False})
        self.assertEqual(quota(3, 1), {"allowed": 0, "left_after": 0, "paywall": True})
        self.assertEqual(quota(0, 5, pro=True)["paywall"], False)

    def test_safety_guard(self):
        self.assertEqual(safety_guard("red")["level"], "stop")
        self.assertIn("ไม่ใช่ช่าง", safety_guard("green")["message_th"])
        self.assertEqual(safety_guard("yellow")["level"], "warn")

if __name__ == "__main__":
    unittest.main()
