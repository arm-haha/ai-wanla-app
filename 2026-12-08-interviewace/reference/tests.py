import unittest
from interviewace import *
from fixtures import *

class T(unittest.TestCase):
    def setUp(self):
        self.score = score_answer(GUN_TRANSCRIPT, GUN["duration_sec"])
        self.q = question_card(GUN["role"], GUN["question_index"])
        self.report = confidence_report(self.score, GUN["name_th"], "งานการตลาด")

    def test_gun_overall_72(self):
        self.assertEqual(self.score["overall"], 72)
        self.assertEqual(self.score["structure"], 80)
        self.assertEqual(self.score["clarity"], 62)
        self.assertEqual(self.score["length"], 72)
        self.assertEqual(self.score["star"], 75)
        self.assertEqual(self.score["band_th"], "พร้อมปานกลาง")
        self.assertEqual(self.score["headline_th"], "คะแนนรวม 72 · พร้อมปานกลาง")

    def test_gun_words_fillers(self):
        f = filler_count(GUN_TRANSCRIPT)
        self.assertEqual(f["word_count"], 95)
        self.assertEqual(f["total"], 9)
        self.assertEqual(f["counts"]["อ่า"], 3)
        self.assertEqual(f["counts"]["เอ่อ"], 2)
        self.assertEqual(f["counts"]["แบบ"], 4)
        self.assertEqual(f["ratio"], 0.0947)

    def test_gun_star_flags(self):
        flags = star_flags(GUN_TRANSCRIPT)
        self.assertEqual(flags, {"S": True, "T": True, "A": True, "R": False})
        self.assertEqual(star_score(flags), 75)

    def test_question_card(self):
        self.assertEqual(self.q["prompt_th"], "เล่าตอนที่ต้องทำงานเป็นทีมแล้วมีปัญหา")
        self.assertEqual(self.q["role_th"], "งานการตลาด")
        self.assertEqual(self.q["ideal_sec"], 75)

    def test_roles_library(self):
        self.assertEqual(len(ROLES), 6)
        self.assertEqual(len(set(v["id"] for v in ROLES.values())), 6)
        for r in ROLE_IDS:
            info = role_info(r)
            self.assertEqual(info["count"], 4)
            self.assertEqual(len(info["questions"]), 4)

    def test_unknown_role(self):
        with self.assertRaises(ValueError):
            role_info("astronaut")
        with self.assertRaises(ValueError):
            question_card("marketing", 9)

    def test_empty_transcript(self):
        with self.assertRaises(ValueError):
            filler_count("  ")
        with self.assertRaises(ValueError):
            word_count("")

    def test_length_peak(self):
        self.assertEqual(length_score(100, 75), 100)
        self.assertEqual(length_score(95, 35), 72)
        with self.assertRaises(ValueError):
            length_score(100, -1)

    def test_clarity_formula(self):
        self.assertEqual(clarity_score(0), 100)
        self.assertEqual(clarity_score(0.0947), 62)
        self.assertEqual(clarity_score(1), 0)

    def test_star_rewrite(self):
        r = star_rewrite(GUN_STAR["situation"], GUN_STAR["task"], GUN_STAR["action"], GUN_STAR["result"])
        self.assertTrue(r["text_th"].startswith("สถานการณ์:"))
        self.assertIn("ผลลัพธ์:", r["text_th"])
        self.assertIn("สองชั่วโมง", r["result_th"])
        self.assertEqual(r["char_count"], len(r["text_th"]))

    def test_star_rewrite_incomplete(self):
        with self.assertRaises(ValueError):
            star_rewrite("s", "t", "a", "  ")

    def test_report_tips(self):
        self.assertEqual(self.report["overall"], 72)
        self.assertTrue(any("ผลลัพธ์" in t for t in self.report["tips_th"]))
        self.assertTrue(any("คำเติม" in t for t in self.report["tips_th"]))
        self.assertIn("ไม่ใช่การรับรองว่าจะได้งาน", self.report["disclaimer_th"])

    def test_pin_full_star(self):
        s = score_answer(PIN["transcript"], 75)
        self.assertEqual(s["star"], 100)
        self.assertEqual(s["star_flags"], {"S": True, "T": True, "A": True, "R": True})
        self.assertGreaterEqual(s["overall"], 65)

    def test_drill(self):
        self.assertIn("สี่ประโยค", drill("star")["task_th"])
        self.assertEqual(drill("clarity")["minutes"], 5)
        with self.assertRaises(ValueError):
            drill("luck")

    def test_share(self):
        s = share_card("น้องกันต์", 72, "พร้อมปานกลาง", "งานการตลาด")
        self.assertIn("ACE", s["cta_th"])
        self.assertEqual(s["headline_th"], "คะแนนรวม 72 · พร้อมปานกลาง")

    def test_quota(self):
        self.assertEqual(quota(1, 1), {"allowed": 1, "left_after": 1, "paywall": False})
        self.assertEqual(quota(3, 1), {"allowed": 0, "left_after": 0, "paywall": True})
        self.assertEqual(quota(0, 5, pro=True)["paywall"], False)

    def test_safety(self):
        self.assertEqual(safety_guard(True)["level"], "ok")
        self.assertEqual(safety_guard(False)["level"], "stop")
        self.assertIn("ไม่ใช่การรับรองว่าจะได้งาน", safety_guard()["message_th"])

    def test_bands(self):
        # reuse length/clarity extremes via a short all-star text? just check thresholds on overall helper
        self.assertEqual(score_answer(PIN["transcript"], 75)["band_th"] in ("พร้อมมาก", "พร้อมปานกลาง", "ต้องซ้อมอีก"), True)

    def test_engineer_question(self):
        q = question_card("engineer", 0)
        self.assertIn("บั๊ก", q["prompt_th"])

    def test_fresh_grad_count(self):
        self.assertEqual(role_info("fresh_grad")["seniority"], "entry")

    def test_structure_short(self):
        # 10 words all STAR-less
        t = "ฉัน ชอบ งาน นี้ มาก จริง ๆ นะ ครับ ผม ดี"
        self.assertEqual(star_flags(t), {"S": False, "T": False, "A": False, "R": False})
        self.assertEqual(star_score(star_flags(t)), 0)
        self.assertLess(structure_score(star_flags(t), 10), 40)

    def test_no_job_guarantee_wording(self):
        text = SAFETY_DISCLAIMER_TH + self.score["disclaimer_th"]
        self.assertNotIn("รับประกันว่าได้งาน", text)
        self.assertIn("ไม่ใช่การรับรองว่าจะได้งาน", text)

    def test_gun_duration(self):
        self.assertEqual(self.score["duration_sec"], 35)

    def test_tokenize_split(self):
        self.assertEqual(tokenize("อ่า เอ่อ แบบ"), ["อ่า", "เอ่อ", "แบบ"])

    def test_report_name(self):
        self.assertEqual(self.report["name_th"], "น้องกันต์")
        self.assertEqual(self.report["role_th"], "งานการตลาด")

    def test_share_sizes(self):
        s = share_card("น้องกันต์", 72, "พร้อมปานกลาง", "งานการตลาด")
        self.assertEqual(s["layout"], "score_report")
        self.assertIn("1080x1350", s["sizes"])

    def test_question_index_zero(self):
        self.assertEqual(question_card("sales", 0)["index"], 0)
        self.assertEqual(question_card("nurse", 3)["index"], 3)

    def test_high_score_tips(self):
        # pin has full STAR; tips may still mention length
        s = score_answer(PIN["transcript"], 75)
        r = confidence_report(s, "น้องปิน", "จบใหม่ / ยังไม่มีประสบการณ์งาน")
        self.assertTrue(len(r["tips_th"]) >= 1)

    def test_filler_label(self):
        self.assertEqual(filler_count(GUN_TRANSCRIPT)["label_th"], "คำเติม 9 จาก 95 คำ")

    def test_people(self):
        self.assertEqual(GUN["company_th"], "Ficto Media")
        self.assertEqual(GUN["name_th"], "น้องกันต์")

    def test_all_roles_have_unique_questions(self):
        allq = [q for r in ROLES.values() for q in r["questions"]]
        self.assertEqual(len(allq), len(set(allq)))
        self.assertEqual(len(allq), 24)


    def test_teacher_role(self):
        self.assertIn("เด็กไม่เข้าใจ", role_info("teacher")["questions"][0])

    def test_length_without_duration(self):
        self.assertEqual(length_score(100), 100)
        self.assertEqual(length_score(80), 70)

    def test_star_score_partial(self):
        self.assertEqual(star_score({"S": True, "T": True, "A": False, "R": False}), 50)

    def test_rewrite_tip(self):
        r = star_rewrite(*GUN_STAR.values()) if False else star_rewrite(GUN_STAR["situation"], GUN_STAR["task"], GUN_STAR["action"], GUN_STAR["result"])
        self.assertIn("วัดได้", r["tip_th"])

    def test_drill_length(self):
        self.assertIn("75 วินาที", drill("length")["task_th"])

    def test_gun_word_count_fn(self):
        self.assertEqual(word_count(GUN_TRANSCRIPT), 95)

    def test_band_thresholds_low(self):
        t = "สวัสดี ครับ ผม ชื่อ กันต์"
        self.assertEqual(score_answer(t, 10)["band_th"], "ต้องซ้อมอีก")

    def test_quota_partial(self):
        self.assertEqual(quota(2, 2), {"allowed": 1, "left_after": 0, "paywall": True})

    def test_sales_role_name(self):
        self.assertEqual(role_info("sales")["name_th"], "งานขาย")

    def test_disclaimer_on_score(self):
        self.assertIn("ค่าตัวอย่าง", self.score["disclaimer_th"])


if __name__ == "__main__":
    unittest.main()
