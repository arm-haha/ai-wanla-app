import unittest
from snaplingo import *
from fixtures import *

TAO_ANSWERS = ["kettle", "kettle", "spoon"]  # cup wrong → 2/3

class T(unittest.TestCase):
    def setUp(self):
        self.scene = parse_scene(KITCHEN)
        self.labs = labels(self.scene["keys"])
        self.quiz = mini_quiz(self.scene["keys"], "en", answers=TAO_ANSWERS)
        self.prog = progress(3, self.quiz, TODAY)

    def test_kitchen_quality(self):
        self.assertEqual(self.scene["quality"]["score"], 89)
        self.assertTrue(self.scene["ok"])
        self.assertEqual(self.scene["keys"], ["kettle", "cup", "spoon"])

    def test_labels(self):
        self.assertEqual(self.labs["count"], 3)
        self.assertIn("3 คำ", self.labs["headline_th"])
        k = self.labs["cards"][0]
        self.assertEqual(k["name_en"], "kettle")
        self.assertEqual(k["name_zh"], "水壶")
        self.assertIn("เคท-เทิล", k["en_line_th"])
        self.assertIn("สุ่ย-หู", k["zh_line_th"])

    def test_flashcards_en(self):
        f = flashcards(self.scene["keys"], "en")
        self.assertEqual(f["count"], 3)
        self.assertEqual(f["cards"][0]["front_th"], "กาต้มน้ำ")
        self.assertIn("kettle", f["cards"][0]["back"])
        self.assertEqual(f["cards"][0]["say_th"], "เคท-เทิล")

    def test_flashcards_zh(self):
        f = flashcards(["kettle"], "zh")
        self.assertIn("水壶", f["cards"][0]["back"])
        self.assertEqual(f["cards"][0]["say_th"], "สุ่ย-หู")

    def test_quiz_score(self):
        self.assertEqual((self.quiz["right"], self.quiz["score_pct"]), (2, 67))
        self.assertIn("2/3", self.quiz["headline_th"])
        self.assertFalse(self.quiz["questions"][1]["correct"])
        self.assertTrue(self.quiz["questions"][0]["correct"])

    def test_quiz_unanswered(self):
        q = mini_quiz(self.scene["keys"], "en")
        self.assertEqual(q["answered"], 0)
        self.assertEqual(q["score_pct"], 0)
        self.assertIsNone(q["questions"][0]["correct"])

    def test_progress_streak_4(self):
        self.assertTrue(self.prog["passed"])
        self.assertEqual(self.prog["streak"], 4)
        self.assertEqual(self.prog["rewards"], [])
        self.assertIn("4 วัน", self.prog["headline_th"])

    def test_star_reward_at_3(self):
        p = progress(2, self.quiz, TODAY)
        self.assertEqual(p["streak"], 3)
        self.assertEqual(p["rewards"][0]["key"], "star")

    def test_fail_resets(self):
        bad = mini_quiz(self.scene["keys"], "en", answers=["cup", "cup", "cup"])
        self.assertEqual(bad["right"], 1)
        p = progress(4, bad, TODAY)
        self.assertFalse(p["passed"])
        self.assertEqual(p["streak"], 0)

    def test_progress_requires_answers(self):
        with self.assertRaises(ValueError):
            progress(1, mini_quiz(self.scene["keys"], "en"))

    def test_bad_quality(self):
        q = parse_scene(BAD_SHOT)["quality"]
        self.assertEqual(q["score"], 43)
        self.assertFalse(q["ok"])
        self.assertGreaterEqual(len(q["tips_th"]), 3)

    def test_empty(self):
        e = parse_scene(EMPTY_SHOT)
        self.assertFalse(e["ok"])
        self.assertEqual(e["quality"]["score"], 54)
        self.assertEqual(e["keys"], [])

    def test_lowconf_drops_kettle(self):
        s = parse_scene(LOWCONF_SHOT)
        self.assertEqual(s["keys"], ["cup"])
        self.assertTrue(s["ok"])

    def test_bad_input(self):
        with self.assertRaises(ValueError):
            scan_quality(1.2, 0, 0, 1)

    def test_unknown_word(self):
        with self.assertRaisesRegex(ValueError, "unknown word"):
            label_card("spaceship")

    def test_bad_lang(self):
        with self.assertRaises(ValueError):
            flashcards(["cup"], "jp")
        with self.assertRaises(ValueError):
            mini_quiz(["cup"], "jp")

    def test_empty_quiz(self):
        with self.assertRaises(ValueError):
            mini_quiz([], "en")

    def test_room_scene(self):
        s = parse_scene(ROOM)
        self.assertEqual(s["keys"], ["chair", "book"])
        self.assertEqual(s["quality"]["score"], 90)

    def test_library_16(self):
        self.assertEqual(len(WORDS), 16)
        ids = [w["id"] for w in WORDS.values()]
        self.assertEqual(len(ids), len(set(ids)))

    def test_quiz_choices_unique(self):
        for q in self.quiz["questions"]:
            keys = [c["key"] for c in q["choices"]]
            self.assertEqual(len(keys), len(set(keys)))
            self.assertEqual(sum(1 for c in q["choices"] if c["correct"]), 1)
            self.assertEqual(len(q["choices"]), 3)

    def test_share(self):
        s = share_card("พี่แอน", "น้องเต้า", self.labs, self.prog)
        self.assertEqual(s["count"], 3)
        self.assertEqual(s["streak"], 4)
        self.assertIn("LINGO", s["cta_th"])
        self.assertTrue(s["hook_th"].startswith("ถ่ายของรอบบ้าน"))
        self.assertEqual(s["layout"], "lingo_card")

    def test_quota(self):
        self.assertEqual(quota(1, 1), {"allowed": 1, "left_after": 1, "paywall": False})
        self.assertEqual(quota(3, 1), {"allowed": 0, "left_after": 0, "paywall": True})
        self.assertEqual(quota(0, 5, pro=True)["paywall"], False)

    def test_safety(self):
        self.assertEqual(safety_guard()["level"], "ok")
        self.assertEqual(safety_guard(True, True)["level"], "warn")
        self.assertEqual(safety_guard(True, False)["level"], "stop")
        self.assertIn("ไม่ใช่หลักสูตร", safety_guard()["message_th"])

    def test_cup_pronunciation(self):
        c = label_card("cup")
        self.assertEqual(c["th_en"], "คัพ")
        self.assertEqual(c["pinyin"], "bēizi")

    def test_spoon_zh(self):
        self.assertEqual(label_card("spoon")["name_zh"], "勺子")

    def test_zh_quiz(self):
        q = mini_quiz(["kettle"], "zh", answers=["kettle"])
        self.assertEqual(q["right"], 1)
        self.assertEqual(q["questions"][0]["choices"][0]["text"], "水壶")

    def test_rewards_7(self):
        p = progress(6, self.quiz, TODAY)
        self.assertEqual(p["rewards"][0]["key"], "sun")

    def test_rewards_14_30(self):
        self.assertEqual(progress(13, self.quiz)["rewards"][0]["key"], "rainbow")
        self.assertEqual(progress(29, self.quiz)["rewards"][0]["key"], "trophy")

    def test_share_no_prog(self):
        s = share_card("พี่แอน", "น้องเต้า", self.labs, None)
        self.assertEqual(s["streak"], 0)

    def test_watermark(self):
        self.assertIn("curriculum", WATERMARK)

    def test_duplicate_det_unique_keys(self):
        sh = dict(KITCHEN, detections=KITCHEN["detections"]+KITCHEN["detections"])
        self.assertEqual(parse_scene(sh)["keys"], ["kettle", "cup", "spoon"])

    def test_unknown_key_ignored(self):
        sh = dict(KITCHEN, detections=KITCHEN["detections"]+[{"key":"spaceship","value":True,"confidence":0.99}])
        self.assertEqual(parse_scene(sh)["keys"], ["kettle", "cup", "spoon"])

    def test_flashcard_order(self):
        f = flashcards(["spoon", "kettle"], "en")
        self.assertEqual([c["key"] for c in f["cards"]], ["spoon", "kettle"])

    def test_quiz_prompt_th(self):
        self.assertIn("ภาษาอังกฤษ", self.quiz["questions"][0]["prompt_th"])
        self.assertIn("กาต้มน้ำ", self.quiz["questions"][0]["prompt_th"])

    def test_perfect_score(self):
        q = mini_quiz(["cup"], "en", answers=["cup"])
        self.assertEqual(q["score_pct"], 100)
        self.assertTrue(progress(0, q)["passed"])

    def test_boundary_50(self):
        q = mini_quiz(["kettle", "cup"], "en", answers=["kettle", "kettle"])
        self.assertEqual(q["score_pct"], 50)
        self.assertTrue(progress(0, q)["passed"])

    def test_below_50(self):
        q = mini_quiz(["kettle", "cup", "spoon"], "en", answers=["cup", "cup", "cup"])
        self.assertEqual(q["score_pct"], 33)
        self.assertFalse(progress(0, q)["passed"])

    def test_topics(self):
        self.assertEqual(WORDS["kettle"]["topic"], "kitchen")
        self.assertEqual(WORDS["chair"]["topic"], "room")

    def test_message(self):
        self.assertIn("3 ชิ้น", self.scene["message_th"])

    def test_choice_position_varies(self):
        pos=[]
        for q in mini_quiz(["kettle","cup","spoon"], "en")["questions"]:
            pos.append(next(i for i,c in enumerate(q["choices"]) if c["correct"]))
        self.assertEqual(len(set(pos)), 3)  # 0,1,2

    def test_fridge_and_book_cards(self):
        self.assertEqual(label_card("fridge")["name_zh"], "冰箱")
        self.assertEqual(label_card("book")["name_en"], "book")

if __name__ == "__main__":
    unittest.main()
