import unittest
from parkpin import *
from fixtures import *

class T(unittest.TestCase):
    def setUp(self):
        self.scan = pin_scan(JAY_PHOTO)
        self.fee = fee_estimate("fictomall_bangna", PARKED, NOW)
        self.pin = save_pin("pin01", "u01", JAY_PHOTO, PARKED, JAY_HINT)
        self.walk = walkback_guide(JAY_PHOTO, JAY_HINT)

    def test_jay_scan(self):
        s = self.scan
        self.assertEqual((s["floor"], s["zone"], s["pillar"], s["color_th"]), ("B2", "C", "C-14", "เขียว"))
        self.assertTrue(s["ok"])
        self.assertFalse(s["has_plate"])

    def test_jay_quality(self):
        q = self.scan["quality"]
        self.assertEqual(q["score"], 88)
        self.assertTrue(q["ok"])

    def test_quality_tips(self):
        s = pin_scan(PHOTOS[6])
        self.assertFalse(s["quality"]["ok"])
        self.assertTrue(s["uncertain"])
        self.assertGreaterEqual(len(s["quality"]["tips_th"]), 3)

    def test_bad_quality(self):
        with self.assertRaises(ValueError):
            scan_quality(2, 0, 0, 1)

    def test_unknowns(self):
        with self.assertRaises(ValueError):
            identify_pin({**JAY_PHOTO, "floor": "Z9", "confidence": 1})
        with self.assertRaises(ValueError):
            fee_estimate("not_a_mall", PARKED, NOW)

    def test_pipeline(self):
        self.assertEqual(pipeline_steps(JAY_PHOTO),
                         ["sign_detect", "floor_read", "zone_color", "pin_save", "fee_timer", "walkback"])
        self.assertIn("deglare", pipeline_steps(PHOTOS[6]))
        self.assertIn("plate_blur", pipeline_steps(PHOTOS[7]))

    def test_library(self):
        self.assertEqual(len(MALLS), 4)
        self.assertEqual(len(FLOOR_KINDS), 11)
        self.assertEqual(mall_info("fictomall_bangna")["per_hour_thb"], 20)

    def test_jay_fee(self):
        f = self.fee
        self.assertEqual((f["minutes"], f["hours_billed"], f["fee_thb"]), (150, 3, 60))
        self.assertEqual((f["next_jump_min"], f["next_fee_thb"]), (45, 80))

    def test_grace(self):
        f = fee_estimate("fictomall_bangna", PARKED, "2026-11-17T14:30:00")
        self.assertEqual((f["minutes"], f["fee_thb"], f["next_jump_min"]), (10, 0, 5))

    def test_cap(self):
        f = fee_estimate("fictomall_bangna", "2026-11-17T00:00:00", "2026-11-17T20:00:00")
        self.assertEqual(f["fee_thb"], 200)

    def test_time_order(self):
        with self.assertRaises(ValueError):
            elapsed_minutes(NOW, PARKED)

    def test_close_ok_and_soon(self):
        c = close_reminder("fictomall_bangna", NOW)
        self.assertEqual(c["status"], "ok")
        self.assertEqual(c["minutes_left"], 310)
        c2 = close_reminder("fictomall_bangna", "2026-11-17T21:40:00")
        self.assertEqual(c2["status"], "soon")
        c3 = close_reminder("fictomall_bangna", "2026-11-17T22:10:00")
        self.assertEqual(c3["status"], "after_close")

    def test_walkback(self):
        w = self.walk
        self.assertEqual(w["steps"][1]["text_th"], "ขึ้น/ลงไปชั้น B2")
        self.assertTrue(any("C-14" in s["text_th"] for s in w["steps"]))
        self.assertTrue(any("เขียว" in s["text_th"] for s in w["steps"]))

    def test_no_plate_storage(self):
        with self.assertRaises(ValueError):
            save_pin("x", "u01", JAY_PHOTO, PARKED, plate_note="กก 1234")
        p = save_pin("pin08", "u01", PHOTOS[7], PARKED, JAY_HINT)
        self.assertTrue(p["needs_plate_blur"])

    def test_lost_car(self):
        lost = lost_car(self.pin, NOW, JAY_PHOTO)
        self.assertEqual(lost["fee_thb"], 60)
        self.assertIn("C-14", lost["message_th"])
        self.assertEqual(lost["minutes"], 150)

    def test_family_share(self):
        card = family_share(JAY, self.pin, self.fee, self.walk, JAY_NOTE)
        self.assertTrue(card["line_share_url"].startswith("https://line.me/R/share?text="))
        self.assertEqual(card["fee_thb"], 60)
        self.assertIn("B2", card["floor"])

    def test_share_quota_safety(self):
        c = share_card(JAY["name_th"], self.pin, self.fee)
        self.assertIn("PARK", c["cta_th"])
        self.assertIn("60", c["hook_th"])
        self.assertEqual(quota(1, 1)["left_after"], 1)
        self.assertTrue(quota(3, 1)["paywall"])
        self.assertEqual(safety_guard(False)["level"], "ok")
        self.assertEqual(safety_guard(True)["level"], "warn")

    def test_history(self):
        pins = [save_pin(*e[:2], e[2], e[3], e[4]) for e in HISTORY]
        s = history_stats(pins)
        self.assertEqual(s["count"], 2)
        self.assertEqual(s["malls"], 2)
        self.assertIn(s["top_mall"], {"fictomall_bangna", "fictoplex_siri"})
        self.assertEqual(s["last_parked_at"], PARKED)
        self.assertEqual(history_stats([])["count"], 0)

    def test_airport_rate(self):
        f = fee_estimate("fictopark_airport", "2026-11-17T10:00:00", "2026-11-17T12:00:00")
        self.assertEqual(f["per_hour_thb"], 40)
        self.assertGreater(f["fee_thb"], 0)

    def test_unknown_color(self):
        with self.assertRaises(ValueError):
            identify_pin({**JAY_PHOTO, "color": "neon", "confidence": 1})

    def test_quota_pro(self):
        self.assertFalse(quota(0, 4, pro=True)["paywall"])

    def test_chiangmai_grace_30(self):
        f = fee_estimate("fictoworld_chiangmai", "2026-11-17T14:00:00", "2026-11-17T14:20:00")
        self.assertEqual(f["fee_thb"], 0)

    def test_disclaimer(self):
        self.assertIn("ป้ายทะเบียน", SAFETY_DISCLAIMER_TH)
        self.assertIn("ไม่ใช่ราคาห้างจริง", self.fee["disclaimer_th"])

    def test_walk_landmark(self):
        self.assertIn("ศูนย์อาหาร", self.walk["steps"][0]["text_th"])

    def test_pin_fields(self):
        self.assertEqual(self.pin["pillar"], "C-14")
        self.assertTrue(self.pin["on_device"])

    def test_share_layout(self):
        self.assertEqual(share_card("พี่เจ", self.pin, self.fee)["layout"], "pin_card")

    def test_minutes_exact(self):
        self.assertEqual(elapsed_minutes(PARKED, NOW), 150)

    def test_plate_photo_warn(self):
        s = pin_scan(PHOTOS[7])
        self.assertTrue(s["has_plate"])
        self.assertEqual(safety_guard(s["has_plate"])["level"], "warn")

    def test_siri_close(self):
        c = close_reminder("fictoplex_siri", "2026-11-17T21:00:00")
        self.assertEqual(c["minutes_left"], 30)
        self.assertEqual(c["status"], "soon")

    def test_bad_mall_info(self):
        with self.assertRaises(ValueError):
            mall_info("x")


    def test_other_floors(self):
        self.assertEqual(pin_scan(PHOTOS[1])["floor"], "3F")
        self.assertEqual(pin_scan(PHOTOS[3])["floor"], "rooftop")
        self.assertEqual(pin_scan(PHOTOS[5])["floor"], "G")

    def test_lost_ticket_field(self):
        self.assertEqual(self.fee["lost_ticket_thb"], 300)

    def test_next_jump_grace(self):
        f = fee_estimate("fictomall_bangna", PARKED, "2026-11-17T14:30:00")
        self.assertEqual(f["next_fee_thb"], 20)

    def test_family_steps_count(self):
        card = family_share(JAY, self.pin, self.fee, self.walk, JAY_NOTE)
        self.assertEqual(card["steps_count"], len(self.walk["steps"]))

    def test_pipeline_clean(self):
        self.assertNotIn("plate_blur", pipeline_steps(JAY_PHOTO))

    def test_colors_thai(self):
        self.assertEqual(COLOR_TH["red"], "แดง")
        self.assertEqual(pin_scan(PHOTOS[4])["color_th"], "แดง")

    def test_share_sizes(self):
        self.assertIn("1080x1350", share_card("พี่เจ", self.pin, self.fee)["sizes"])

    def test_close_disclaimer(self):
        self.assertIn("ค่าตัวอย่าง", close_reminder("fictomall_bangna", NOW)["disclaimer_th"])

    def test_hours_billed_grace(self):
        self.assertEqual(fee_estimate("fictomall_bangna", PARKED, "2026-11-17T14:30:00")["hours_billed"], 0)

    def test_walk_step_numbers(self):
        ns = [s["n"] for s in self.walk["steps"]]
        self.assertEqual(ns, list(range(1, len(ns)+1)))

    def test_save_hint(self):
        self.assertEqual(self.pin["hint_th"], JAY_HINT)

if __name__ == "__main__":
    unittest.main()
