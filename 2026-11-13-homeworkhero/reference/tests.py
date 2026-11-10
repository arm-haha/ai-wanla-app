import unittest
from homeworkhero import *
from fixtures import *

class T(unittest.TestCase):
    def setUp(self):
        self.scan = homework_scan(NOON_PHOTO)
        self.hints3 = step_hints("percent_discount", NOON_FIELDS, 3)

    def test_noon_scan(self):
        s = self.scan
        self.assertEqual(s["template"], "percent_discount")
        self.assertEqual(s["subject"], "math")
        self.assertEqual(s["level"], "p4")
        self.assertEqual(s["level_th"], "ประถมศึกษาปีที่ 4")
        self.assertTrue(s["ok"])

    def test_noon_quality(self):
        q = self.scan["quality"]
        self.assertEqual(q["score"], 89)
        self.assertTrue(q["ok"])
        self.assertEqual(q["tips_th"], [])

    def test_quality_tips(self):
        s = homework_scan(PHOTOS[6])
        self.assertFalse(s["ok"])
        self.assertTrue(s["uncertain"])
        self.assertGreaterEqual(len(s["quality"]["tips_th"]), 3)

    def test_bad_quality_input(self):
        with self.assertRaises(ValueError):
            scan_quality(1.2, 0, 0, 1)

    def test_unknown_template(self):
        with self.assertRaises(ValueError):
            identify_problem({"template": "calculus", "confidence": 1, "fields": {}})

    def test_pipeline(self):
        self.assertEqual(pipeline_steps(NOON_PHOTO),
                         ["page_detect", "ocr_block", "template_match", "hint_tree", "parent_script", "practice"])
        self.assertIn("deglare", pipeline_steps(PHOTOS[6]))
        self.assertIn("deskew", pipeline_steps(PHOTOS[6]))

    def test_library(self):
        self.assertEqual(len(TEMPLATES), 10)
        self.assertEqual(len(LEVELS), 12)
        self.assertEqual(len(level_catalog()), 12)

    def test_hint_levels(self):
        h2 = step_hints("percent_discount", NOON_FIELDS, 2)
        self.assertEqual(len(h2["hints"]), 2)
        self.assertEqual(len(self.hints3["hints"]), 3)
        self.assertIn("____", self.hints3["hints"][2]["text_th"])
        with self.assertRaises(ValueError):
            step_hints("percent_discount", NOON_FIELDS, 4)

    def test_hints_do_not_leak_noon_answer(self):
        texts = " ".join(h["text_th"] for h in self.hints3["hints"][:2])
        self.assertNotIn("600", texts)
        self.assertNotIn("200", texts)
        # hint 3 has blanks, still no final 600
        self.assertNotIn("600", self.hints3["hints"][2]["text_th"])

    def test_all_templates_hints_safe(self):
        samples = {
            "percent_discount": {"price": 800, "percent": 25},
            "area_rect": {"length": 10, "width": 4, "unit": "เมตร"},
            "fraction_of": {"whole": 24, "num": 1, "den": 3},
            "unit_rate": {"total": 120, "qty": 5},
            "average": {"values": [8, 10, 12]},
            "decimal_add": {"a": 1.25, "b": 2.5},
            "thai_word_choice": {"sentence": "แม่____ข้าวให้ลูก", "answer": "ตัก", "choices": ["ตัก", "ริน"]},
            "water_cycle": {"clue": "น้ำในทะเลกลายเป็นไอเมื่อโดนความร้อน", "answer": "การระเหย"},
            "eng_tense": {"sentence": "They ____ football yesterday.", "time_word": "yesterday", "answer": "played", "choices": ["play", "played"]},
            "linear_eq": {"a": 2, "b": 3, "c": 11},
        }
        for tid, fields in samples.items():
            # step_hints itself raises if hint 1-2 leak
            step_hints(tid, fields, 2)

    def test_parent_script(self):
        p = parent_script("percent_discount", NOON_FIELDS)
        self.assertGreaterEqual(len(p["steps"]), 3)
        self.assertIn("อย่าทำข้อให้ลูก", p["intro_th"])
        self.assertTrue(p["mistakes_th"])

    def test_parent_reveal_gated(self):
        r = parent_reveal("percent_discount", NOON_FIELDS)
        self.assertTrue(r["gated"])
        self.assertEqual(r["audience"], "parent")
        self.assertEqual(r["answer"]["pay"], 600)
        self.assertEqual(r["answer"]["discount"], 200)

    def test_similar_practice_different_numbers(self):
        pr = similar_practice("percent_discount", 0, 3)
        self.assertEqual(pr["count"], 3)
        self.assertNotEqual(pr["items"][0]["fields"], NOON_FIELDS)
        self.assertIn("answer_key", pr["items"][0])
        self.assertEqual(pr["items"][0]["answer_key"]["pay"], 960)

    def test_area_and_linear(self):
        self.assertEqual(parent_reveal("area_rect", PHOTOS[1]["fields"])["answer"]["area"], 40)
        self.assertEqual(parent_reveal("linear_eq", PHOTOS[4]["fields"])["answer"]["x"], 4)
        self.assertEqual(parent_reveal("fraction_of", PHOTOS[2]["fields"])["answer"]["value"], 8)

    def test_common_mistakes(self):
        m = common_mistakes("percent_discount")
        self.assertGreaterEqual(len(m["mistakes_th"]), 2)

    def test_timebox(self):
        t = timebox(20, 7, 1)
        self.assertEqual((t["left_minutes"], t["encourage_th"]), (13, "เก่งมากที่พยายามเอง"))
        t2 = timebox(20, 20, 3)
        self.assertEqual(t2["left_minutes"], 0)
        self.assertIn("พัก", t2["encourage_th"])
        with self.assertRaises(ValueError):
            timebox(0, 0, 0)

    def test_progress(self):
        entries = [progress_entry(*e) for e in PROGRESS]
        s = progress_stats(entries)
        self.assertEqual(s["count"], 3)
        self.assertEqual(s["solved"], 2)
        self.assertEqual(s["avg_hints"], 1.67)
        self.assertEqual(s["top_template"], "percent_discount")
        self.assertEqual(progress_stats([])["count"], 0)

    def test_teacher_note(self):
        card = teacher_note(NOON, self.scan, 2, NOON_NOTE)
        self.assertTrue(card["line_share_url"].startswith("https://line.me/R/share?text="))
        self.assertEqual(card["hints_used"], 2)
        self.assertEqual(card["level_th"], "ประถมศึกษาปีที่ 4")

    def test_share_quota_safety(self):
        c = share_card(NOON["name_th"], self.scan)
        self.assertIn("HINT", c["cta_th"])
        self.assertIn("ไม่บอกคำตอบ", c["hook_th"])
        self.assertEqual(quota(1, 1)["left_after"], 1)
        self.assertTrue(quota(3, 1)["paywall"])
        self.assertEqual(safety_guard(False)["level"], "ok")
        self.assertEqual(safety_guard(True)["level"], "warn")

    def test_template_info(self):
        info = template_info("percent_discount")
        self.assertEqual(info["id"], "t01")
        self.assertEqual(info["level"], "p4")
        with self.assertRaises(ValueError):
            template_info("foo")

    def test_missing_fields(self):
        with self.assertRaises(ValueError):
            step_hints("percent_discount", {"price": 800}, 1)

    def test_other_subjects_scan(self):
        self.assertEqual(homework_scan(PHOTOS[3])["subject"], "eng")
        self.assertEqual(homework_scan(PHOTOS[5])["subject"], "sci")
        self.assertEqual(homework_scan(PHOTOS[4])["level"], "m2")

    def test_decimal_and_tense_answers(self):
        self.assertEqual(parent_reveal("decimal_add", PHOTOS[7]["fields"])["answer"]["sum"], 3.75)
        self.assertEqual(parent_reveal("eng_tense", PHOTOS[3]["fields"])["answer"]["verb"], "played")

    def test_unit_rate_and_average(self):
        self.assertEqual(parent_reveal("unit_rate", {"total": 120, "qty": 5})["answer"]["rate"], 24)
        self.assertEqual(parent_reveal("average", {"values": [8, 10, 12]})["answer"]["average"], 10)

    def test_water_and_thai(self):
        self.assertEqual(parent_reveal("water_cycle", PHOTOS[5]["fields"])["answer"]["process"], "การระเหย")
        self.assertIn("ตัก", parent_reveal("thai_word_choice", {"sentence": "แม่____ข้าวให้ลูก", "answer": "ตัก", "choices": ["ตัก"]})["display_th"])

    def test_encourage_more_hints(self):
        self.assertIn("คำใบ้", timebox(20, 5, 2)["encourage_th"])

    def test_progress_bad(self):
        with self.assertRaises(ValueError):
            progress_entry("e9", "c01", "2026-01-01", "percent_discount", -1, 0, True)

    def test_quota_pro(self):
        self.assertEqual(quota(0, 5, pro=True), {"allowed": 5, "left_after": None, "paywall": False})

    def test_hint_has_source_numbers_only_at_3(self):
        t3 = self.hints3["hints"][2]["text_th"]
        self.assertIn("800", t3)
        self.assertIn("25", t3)


    def test_similar_other_templates(self):
        for tid in ("area_rect", "linear_eq", "eng_tense"):
            pr = similar_practice(tid, 1, 2)
            self.assertEqual(pr["count"], 2)
            self.assertIn("____", pr["items"][0]["method_th"])

    def test_all_level_labels(self):
        self.assertEqual(LEVEL_TH["p1"], "ประถมศึกษาปีที่ 1")
        self.assertEqual(LEVEL_TH["m6"], "มัธยมศึกษาปีที่ 6")

    def test_share_sizes(self):
        c = share_card(NOON["name_th"], self.scan)
        self.assertIn("1080x1350", c["sizes"])
        self.assertEqual(c["layout"], "hint_session")

    def test_parent_script_area(self):
        p = parent_script("area_rect", PHOTOS[1]["fields"])
        self.assertTrue(any("พื้นที่" in s["text_th"] or "รอบรูป" in s["text_th"] for s in p["steps"]))

    def test_scan_subjects_thai_math(self):
        self.assertEqual(homework_scan(PHOTOS[1])["subject_th"], "คณิตศาสตร์")
        self.assertEqual(homework_scan(PHOTOS[7])["template"], "decimal_add")

    def test_low_conf_message(self):
        ident = identify_problem(PHOTOS[6])
        self.assertFalse(ident["ok"])
        self.assertIn("ถ่ายใหม่", ident["message_th"])

    def test_hint_upto_one(self):
        h = step_hints("percent_discount", NOON_FIELDS, 1)
        self.assertEqual(len(h["hints"]), 1)
        self.assertFalse(h["hints"][0]["reveals_answer"])

    def test_average_similar_changes(self):
        a = similar_practice("average", 0, 3)
        vals = [tuple(it["fields"]["values"]) for it in a["items"]]
        self.assertEqual(len(set(vals)), 3)

    def test_safety_text(self):
        self.assertIn("ไม่บอกคำตอบ", safety_guard(False)["message_th"])

    def test_template_fields(self):
        self.assertEqual(template_info("linear_eq")["fields"], ["a", "b", "c"])

    def test_progress_last_date(self):
        entries = [progress_entry(*e) for e in PROGRESS]
        self.assertEqual(progress_stats(entries)["last_date"], "2026-11-13")

    def test_common_mistakes_unknown(self):
        with self.assertRaises(ValueError):
            common_mistakes("foo")

if __name__ == "__main__":
    unittest.main()
