import unittest
from giftgenie import *
from fixtures import *

class T(unittest.TestCase):
    def setUp(self):
        self.q = persona_quiz(**BIM_QUIZ)
        self.picks = budget_picks(self.q)

    def test_bim_quiz(self):
        self.assertEqual(self.q["relationship"], "partner")
        self.assertFalse(self.q["is_minor"])
        self.assertEqual(self.q["hobbies"], ["cafe", "fashion"])

    def test_hobby_dedupe(self):
        q = persona_quiz("friend", "25-34", "cozy", ["cafe", "cafe", "books"], "birthday", 1000, "เอ")
        self.assertEqual(q["hobbies"], ["cafe", "books"])

    def test_bad_quiz(self):
        with self.assertRaises(ValueError):
            persona_quiz("pet", "25-34", "cozy", ["cafe"], "birthday", 1000, "x")
        with self.assertRaises(ValueError):
            persona_quiz("partner", "25-34", "cozy", ["surfing"], "birthday", 1000, "x")
        with self.assertRaises(ValueError):
            persona_quiz("partner", "25-34", "cozy", ["cafe"], "birthday", -1, "x")
        with self.assertRaises(ValueError):
            persona_quiz("partner", "25-34", "cozy", [], "birthday", 1000, "x")

    def test_bim_top_shirt(self):
        top = self.picks["picks"][0]
        self.assertEqual((top["gift_id"], top["score"], top["mid_thb"]), ("g01", 100, 890))
        self.assertEqual(top["name_th"], "เสื้อโอเวอร์ไซส์ FictoSoft")
        self.assertEqual(self.picks["count"], 5)

    def test_bim_order(self):
        self.assertEqual([p["gift_id"] for p in self.picks["picks"]], ["g01", "g13", "g02", "g06", "g05"])

    def test_shirt_score_parts(self):
        self.assertEqual(gift_score(GIFTS["g01"], self.q), 100)
        self.assertEqual(gift_score(GIFTS["g02"], self.q), 90)
        self.assertEqual(gift_score(GIFTS["g01"], dict(self.q, budget_thb=500)), 0)

    def test_library(self):
        self.assertEqual(len(GIFTS), 16)
        self.assertEqual(len(set(GIFTS)), 16)
        for g in GIFTS.values():
            self.assertTrue(g["min"] <= g["mid"] <= g["max"])

    def test_child_blocks_alcohol(self):
        q = persona_quiz(**GAI_QUIZ)
        self.assertTrue(q["is_minor"])
        self.assertEqual(gift_score(GIFTS["g15"], q), 0)
        ids = [p["gift_id"] for p in budget_picks(q)["picks"]]
        self.assertNotIn("g15", ids)
        self.assertEqual(ids[0], "g16")
        self.assertEqual(budget_picks(q)["picks"][0]["score"], 100)

    def test_nan_housewarming(self):
        ids = [p["gift_id"] for p in budget_picks(persona_quiz(**NAN_QUIZ))["picks"]]
        self.assertEqual(ids[0], "g11")
        self.assertIn("g07", ids)

    def test_swap(self):
        s = already_has_swap(self.q, ["g01"])
        self.assertEqual(s["picks"][0]["gift_id"], "g13")
        self.assertTrue(all(p["gift_id"] != "g01" for p in s["picks"]))
        self.assertEqual(s["count"], 3)

    def test_messages_bim(self):
        ms = card_messages("birthday", "sweet", "ต้น", 2)
        self.assertEqual(ms[0]["text_th"], "สุขสันต์วันเกิดนะ ขอให้ปีนี้มีวันที่สบายใจมากกว่าเดิม")
        self.assertEqual(ms[0]["n"], 1)

    def test_message_tones(self):
        self.assertEqual(card_messages("thank_you", "short", "คุณสุรีย์", 1)[0]["tone"], "short")
        with self.assertRaises(ValueError):
            card_messages("birthday", "angry", "ต้น")
        with self.assertRaises(ValueError):
            card_messages("wedding", "sweet", "ต้น")

    def test_wrap_bands(self):
        self.assertEqual(wrap_ideas(400)["band"], "low")
        self.assertEqual(wrap_ideas(1500)["band"], "mid")
        self.assertEqual(wrap_ideas(2000)["band"], "high")
        self.assertEqual(wrap_ideas(5000)["band"], "luxe")
        self.assertIn("ดอกไม้แห้ง", wrap_ideas(1500)["ideas_th"][0])
        with self.assertRaises(ValueError):
            wrap_ideas(-5)

    def test_event_statuses(self):
        ev = [occasion_event(*e, TODAY) for e in EVENTS]
        self.assertEqual([e["status"] for e in ev], ["soon", "due", "ok", "past"])
        self.assertEqual(ev[0]["days_left"], 18)
        self.assertEqual(ev[1]["days_left"], 5)
        self.assertEqual(ev[3]["days_left"], -2)

    def test_calendar_stats(self):
        ev = [occasion_event(*e, TODAY) for e in EVENTS]
        st = calendar_stats(ev)
        self.assertEqual((st["count"], st["due"], st["soon"], st["next_id"]), (4, 1, 1, "e02"))
        self.assertEqual(calendar_stats([])["count"], 0)

    def test_bad_occasion_event(self):
        with self.assertRaises(ValueError):
            occasion_event("e", "x", "wedding", "2026-12-01", 100, TODAY)

    def test_share(self):
        msg = card_messages("birthday", "sweet", "ต้น", 1)[0]["text_th"]
        s = share_card(self.q, self.picks["picks"][0], msg)
        self.assertIn("เสื้อโอเวอร์ไซส์", s["headline_th"])
        self.assertIn("฿1,500", s["cta_th"])
        self.assertEqual(s["score"], 100)

    def test_share_empty(self):
        s = share_card(self.q, None, "")
        self.assertIn("ยังไม่มีไอเดีย", s["headline_th"])

    def test_quota(self):
        self.assertEqual(quota(1, 1), {"allowed": 1, "left_after": 1, "paywall": False})
        self.assertEqual(quota(3, 1), {"allowed": 0, "left_after": 0, "paywall": True})
        self.assertEqual(quota(0, 5, pro=True)["paywall"], False)

    def test_safety(self):
        self.assertEqual(safety_guard(False)["level"], "ok")
        self.assertEqual(safety_guard(True)["level"], "warn")
        self.assertEqual(safety_guard(True, True)["level"], "stop")
        self.assertIn("ไม่ใช่ร้านค้า", safety_guard(False)["message_th"])

    def test_ot_colleague(self):
        p = budget_picks(persona_quiz(**OT_QUIZ))
        self.assertTrue(all(x["mid_thb"] <= 800 for x in p["picks"]))
        self.assertGreaterEqual(p["count"], 3)

    def test_boundaries(self):
        self.assertEqual(reminder_status("2026-11-27", TODAY)["status"], "due")  # 7 days
        self.assertEqual(reminder_status("2026-11-28", TODAY)["status"], "soon")
        self.assertEqual(reminder_status("2026-12-11", TODAY)["status"], "soon")  # 21
        self.assertEqual(reminder_status("2026-12-12", TODAY)["status"], "ok")
        self.assertEqual(wrap_ideas(500)["band"], "low")
        self.assertEqual(wrap_ideas(501)["band"], "mid")
        self.assertEqual(wrap_ideas(3000)["band"], "high")
        self.assertEqual(wrap_ideas(3001)["band"], "luxe")


    def test_bim_cafe_card_third(self):
        self.assertEqual(self.picks["picks"][2]["gift_id"], "g02")
        self.assertEqual(self.picks["picks"][2]["mid_thb"], 650)

    def test_filtered_out_low_budget(self):
        q = persona_quiz("partner", "25-34", "cozy", ["cafe"], "birthday", 300, "ต้น")
        p = budget_picks(q)
        self.assertTrue(all(x["mid_thb"] <= 300 for x in p["picks"]))
        self.assertGreater(p["filtered_out"], 0)

    def test_message_count(self):
        self.assertEqual(len(card_messages("birthday", "funny", "ต้น", 2)), 2)

    def test_wrap_count(self):
        self.assertEqual(len(wrap_ideas(1500)["ideas_th"]), 3)

    def test_minor_quiz_band(self):
        self.assertTrue(persona_quiz("kid", "13-17", "playful", ["games"], "birthday", 500, "นิด")["is_minor"])
        self.assertFalse(persona_quiz("friend", "18-24", "playful", ["games"], "birthday", 500, "นิด")["is_minor"])

    def test_unknown_vibe(self):
        with self.assertRaises(ValueError):
            persona_quiz("partner", "25-34", "edgy", ["cafe"], "birthday", 1000, "x")
        with self.assertRaises(ValueError):
            persona_quiz("partner", "99", "cozy", ["cafe"], "birthday", 1000, "x")

    def test_calendar_empty_next(self):
        self.assertIsNone(calendar_stats([])["next_id"])

    def test_event_due_label(self):
        e = occasion_event("e02", "แม่", "birthday", "2026-11-25", 1000, TODAY)
        self.assertEqual(e["status"], "due")
        self.assertEqual(e["receiver_name_th"], "แม่")

    def test_share_hook(self):
        msg = card_messages("birthday", "sweet", "ต้น", 1)[0]["text_th"]
        s = share_card(self.q, self.picks["picks"][0], msg)
        self.assertEqual(s["hook_th"], "คิดของขวัญไม่ออก ตอบ 5 ข้อได้ไอเดียตามงบ")
        self.assertEqual(s["layout"], "gift_card")

    def test_wine_ok_for_adult(self):
        self.assertGreater(gift_score(GIFTS["g15"], self.q), 0)

    def test_safety_copy_minor(self):
        self.assertIn("แอลกอฮอล์", safety_guard(True)["message_th"])

    def test_picks_disclaimer(self):
        self.assertIn("ไม่ใช่ราคาร้านจริง", self.picks["picks"][0]["disclaimer_th"])

    def test_same_day_due(self):
        self.assertEqual(reminder_status(TODAY, TODAY)["status"], "due")
        self.assertEqual(reminder_status(TODAY, TODAY)["days_left"], 0)

    def test_budget_picks_limit(self):
        self.assertEqual(budget_picks(self.q, limit=3)["count"], 3)

    def test_gift_count_stable(self):
        self.assertIn("g16", GIFTS)
        self.assertTrue(GIFTS["g15"]["adult_only"])
        self.assertFalse(GIFTS["g16"]["adult_only"])

    def test_formal_condolence(self):
        t = card_messages("condolence", "formal", "คุณสุรีย์", 1)[0]["text_th"]
        self.assertTrue("เสียใจ" in t or "กำลังใจ" in t)

    def test_high_wrap_tip(self):
        self.assertIn("ห่อเองที่บ้าน", wrap_ideas(2000)["tip_th"])

    def test_ot_no_overspend(self):
        q = persona_quiz(**OT_QUIZ)
        self.assertEqual(q["budget_thb"], 800)
        self.assertLessEqual(max(p["mid_thb"] for p in budget_picks(q)["picks"]), 800)

    def test_soon_window(self):
        self.assertEqual(reminder_status("2026-12-08", TODAY)["status"], "soon")

if __name__ == "__main__":
    unittest.main()
