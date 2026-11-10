import unittest
from medbuddy import *
from fixtures import *

class T(unittest.TestCase):
    def setUp(self):
        self.scan = photo_scan(PHOTOS[0])
        self.sch = schedule(MEDS)
        self.flag = interaction_flag(MEDS)

    def test_scan_quality(self):
        q = self.scan["quality"]
        self.assertEqual(q["score"], 90)
        self.assertTrue(q["ok"])
        self.assertEqual(q["tips_th"], [])

    def test_quality_tips(self):
        s = photo_scan(PHOTOS[3])
        self.assertEqual(s["quality"]["score"], 46)
        self.assertFalse(s["quality"]["ok"])
        self.assertGreaterEqual(len(s["quality"]["tips_th"]), 3)

    def test_bad_quality(self):
        with self.assertRaises(ValueError):
            scan_quality(2, 0, 0)

    def test_parse_ok(self):
        self.assertFalse(PRIL["needs_confirm"])
        self.assertEqual(PRIL["food_th"], "หลังอาหาร")
        self.assertEqual(PRIL["name"], "FictoPril")
        self.assertIn("ยืนยัน", PRIL["message_th"])

    def test_low_conf_must_confirm(self):
        self.assertTrue(LOW["needs_confirm"])
        self.assertIn("ห้ามบันทึกขนาดยาที่ยังไม่ชัด", LOW["message_th"])
        with self.assertRaises(ValueError):
            schedule([LOW])

    def test_parse_bad(self):
        with self.assertRaises(ValueError):
            parse_label(dict(PRIL_RAW, food="midnight"))
        with self.assertRaises(ValueError):
            parse_label(dict(PRIL_RAW, slots=["brunch"]))
        with self.assertRaises(ValueError):
            parse_label(dict(PRIL_RAW, qty=-1))
        with self.assertRaises(ValueError):
            parse_label(dict(PRIL_RAW, confidence=1.2))

    def test_schedule_demo(self):
        self.assertEqual(self.sch["med_count"], 3)
        slots = {s["slot"]: s["count"] for s in self.sch["slots"]}
        self.assertEqual(slots["morning"], 2)
        self.assertEqual(slots["evening"], 1)
        self.assertEqual(slots["as_needed"], 1)
        self.assertNotIn("noon", slots)
        self.assertEqual(self.sch["headline_th"], "ตารางกินยา 3 รายการ")

    def test_schedule_empty(self):
        with self.assertRaises(ValueError):
            schedule([])

    def test_refill_pril_met_pain(self):
        r = refill(PRIL, TODAY, TODAY)
        self.assertEqual((r["days_left"], r["due_date"], r["status"]), (14, "2026-12-23", "soon"))
        r2 = refill(MET, TODAY, TODAY)
        self.assertEqual((r2["days_left"], r2["due_date"], r2["status"]), (10, "2026-12-19", "soon"))
        r3 = refill(PAIN, TODAY, TODAY)
        self.assertTrue(r3["prn"])
        self.assertEqual(r3["status"], "ask")
        self.assertIsNone(r3["days_left"])
        self.assertIn("ห้ามเพิ่มขนาดเอง", r3["message_th"])

    def test_refill_due_and_ok(self):
        short = parse_label(dict(PRIL_RAW, qty=0))
        self.assertEqual(refill(short, TODAY, TODAY)["status"], "due")
        plenty = parse_label(dict(PRIL_RAW, qty=40))
        self.assertEqual(refill(plenty, TODAY, TODAY)["status"], "ok")  # 40 days

    def test_missed_dose_never_double(self):
        g = missed_dose_guide("morning")
        text = " ".join(g["steps_th"]) + g["headline_th"]
        self.assertIn("อย่ากินเพิ่มเป็นสองเท่า", text)
        self.assertIn("โทรถามเภสัชกร", text)
        self.assertNotIn("กินเพิ่มได้", text)
        with self.assertRaises(ValueError):
            missed_dose_guide("sunset")

    def test_interaction_flag(self):
        self.assertEqual(self.flag["level"], "ask")
        self.assertIn("ห้ามเพิ่ม", self.flag["message_th"])
        one = interaction_flag([PRIL])
        self.assertEqual(one["level"], "ok")

    def test_visit_card(self):
        v = visit_card(WANDEE["name_th"], MEDS, WANDEE["clinic_th"], WANDEE["doctor_th"], WANDEE["visit_date"])
        self.assertEqual(v["med_count"], 3)
        self.assertIn("FictoPril", v["meds"][0])
        self.assertIn("ไม่ใช่ใบสั่งยา", v["disclaimer_th"])
        with self.assertRaises(ValueError):
            visit_card("x", [], "c", "d", TODAY)

    def test_caregiver_share(self):
        sh = caregiver_share(NON["name_th"], WANDEE["name_th"], self.sch, TODAY)
        self.assertEqual(sh["slot_count"], 2)  # morning + evening, not prn
        self.assertIn("คุณวันดี", sh["headline_th"])

    def test_library(self):
        self.assertEqual(len(LIBRARY), 5)
        self.assertEqual(len(set(v["id"] for v in LIBRARY.values())), 5)
        info = library_info("FictoPril")
        self.assertIn("สมมติ", info["disclaimer_th"])
        with self.assertRaises(ValueError):
            library_info("Paracetamol")  # no real drug names in the library

    def test_pipeline(self):
        steps = pipeline_steps(PHOTOS[0], [PRIL_RAW, MET_RAW, PAIN_RAW])
        self.assertEqual(steps[:2], ["label_photo", "parse_label"])
        self.assertIn("safety", steps)
        self.assertNotIn("ask_user_confirm", steps)
        low_steps = pipeline_steps(PHOTOS[0], [LOW_RAW])
        self.assertIn("ask_user_confirm", low_steps)
        bad = pipeline_steps(PHOTOS[3], [PRIL_RAW])
        self.assertIn("deglare", bad)
        self.assertIn("recrop", bad)

    def test_share(self):
        s = share_card("คุณวันดี", 3, self.sch["headline_th"])
        self.assertIn("MED", s["cta_th"])
        self.assertEqual(s["headline_th"], "ตารางกินยา 3 รายการ")

    def test_quota(self):
        self.assertEqual(quota(1, 1), {"allowed": 1, "left_after": 1, "paywall": False})
        self.assertEqual(quota(3, 1), {"allowed": 0, "left_after": 0, "paywall": True})
        self.assertEqual(quota(0, 5, pro=True)["paywall"], False)

    def test_safety(self):
        self.assertEqual(safety_guard(True)["level"], "ok")
        self.assertEqual(safety_guard(False)["level"], "stop")
        self.assertIn("ห้ามเปลี่ยนขนาดยาเอง", safety_guard()["message_th"])

    def test_no_dose_change_language(self):
        texts = [
            SAFETY_DISCLAIMER_TH,
            missed_dose_guide("evening")["headline_th"],
            refill(PAIN, TODAY, TODAY)["message_th"],
            self.flag["message_th"],
        ]
        blob = " ".join(texts)
        for banned in ("กินสองเท่า", "เพิ่มขนาดได้", "ลดยาได้เอง", "หยุดยาได้เลย"):
            self.assertNotIn(banned, blob)

    def test_people_fictional(self):
        self.assertEqual(NON["name_th"], "พี่นนท์")
        self.assertEqual(WANDEE["clinic_th"], "Ficto Clinic")
        self.assertTrue(all(m["name"].startswith("Ficto") for m in MEDS))

    def test_food_labels(self):
        self.assertEqual(FOOD["after_food"], "หลังอาหาร")
        self.assertEqual(PAIN["food_th"], "ไม่ระบุมื้อ")

    def test_refill_scheduled_needs_daily(self):
        bad = dict(PRIL)
        bad["daily_units"] = 0
        bad["slots"] = ["morning"]
        with self.assertRaises(ValueError):
            refill(bad, TODAY, TODAY)

    def test_share_sizes(self):
        s = share_card("คุณวันดี", 3, "x")
        self.assertEqual(s["layout"], "schedule_card")
        self.assertIn("1080x1350", s["sizes"])

    def test_visit_date(self):
        v = visit_card(WANDEE["name_th"], MEDS, WANDEE["clinic_th"], WANDEE["doctor_th"], WANDEE["visit_date"])
        self.assertEqual(v["visit_date"], "2026-12-16")
        self.assertIn("นพ.วันชัย", v["doctor_th"])

    def test_soon_threshold(self):
        self.assertEqual(SOON_DAYS, 14)
        self.assertEqual(refill_status(14, 14), "soon")
        self.assertEqual(refill_status(15, 15), "ok")
        self.assertEqual(refill_status(0, 0), "due")

    def test_parse_missing_field(self):
        raw = dict(PRIL_RAW)
        raw.pop("dose_th")
        with self.assertRaises(ValueError):
            parse_label(raw)

    def test_slots_thai(self):
        self.assertEqual(SLOTS["bedtime"], "ก่อนนอน")

    def test_caregiver_excludes_prn_from_pending(self):
        sh = caregiver_share("พี่นนท์", "คุณวันดี", self.sch, TODAY)
        self.assertNotIn("เมื่อปวด / เมื่อมีอาการ", sh["pending_slots_th"])

    def test_min_conf(self):
        edge = parse_label(dict(PRIL_RAW, confidence=0.59))
        self.assertTrue(edge["needs_confirm"])
        ok = parse_label(dict(PRIL_RAW, confidence=0.6))
        self.assertFalse(ok["needs_confirm"])

    def test_disclaimer_everywhere(self):
        for obj in (PRIL, self.sch, self.flag, safety_guard()):
            self.assertIn("ไม่ใช่เภสัชกร", obj["disclaimer_th"] if "disclaimer_th" in obj else obj["message_th"])


    def test_pipeline_photo_id(self):
        self.assertEqual(self.scan["photo_id"], "p01")

    def test_library_forms(self):
        self.assertEqual(library_info("FictoCough")["form_th"], "น้ำ")
        self.assertEqual(library_info("FictoVit")["kind_th"], "ตัวอย่างวิตามินในแอป")

    def test_missed_all_slots(self):
        for sl in SLOTS:
            g = missed_dose_guide(sl)
            self.assertTrue(g["steps_th"][0].startswith("อย่ากินเพิ่ม"))

    def test_quota_partial(self):
        self.assertEqual(quota(2, 2)["paywall"], True)
        self.assertEqual(quota(2, 2)["allowed"], 1)

    def test_share_watermark(self):
        self.assertIn("never change doses", share_card("คุณวันดี", 3, "x")["watermark"])

    def test_schedule_item_fields(self):
        morning = next(s for s in self.sch["slots"] if s["slot"] == "morning")
        names = {i["name"] for i in morning["items"]}
        self.assertEqual(names, {"FictoPril", "FictoMet"})

    def test_pain_max(self):
        self.assertEqual(PAIN["prn_max_per_day"], 3)

    def test_non_relation(self):
        self.assertEqual(NON["relation_th"], "ลูก")
        self.assertEqual(NON["age"], 36)

    def test_refill_message_pril(self):
        self.assertIn("2026-12-23", refill(PRIL, TODAY, TODAY)["message_th"])

    def test_safety_stop_message(self):
        self.assertIn("ยืนยันกับซองยา", safety_guard(False)["message_th"])


if __name__ == "__main__":
    unittest.main()
