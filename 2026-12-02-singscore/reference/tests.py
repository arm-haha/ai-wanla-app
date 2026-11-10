import unittest
from singscore import *
from fixtures import *

class T(unittest.TestCase):
    def setUp(self):
        self.tom = score_take(TOM_TAKE)
        self.nina = score_take(NINA_TAKE)
        self.key = key_finder(TOM_TAKE["notes"], TOM_TAKE["exercise"])

    def test_tom_scores(self):
        self.assertEqual((self.tom["pitch"], self.tom["timing"], self.tom["combined"]), (82, 74, 79))
        self.assertEqual(self.tom["band"], "good")
        self.assertIn("79", self.tom["headline_th"])
        self.assertTrue(self.tom["ok"])

    def test_nina_scores(self):
        self.assertEqual((self.nina["pitch"], self.nina["timing"], self.nina["combined"]), (75, 68, 72))

    def test_pitch_formula(self):
        self.assertEqual(pitch_score(36), 82)
        self.assertEqual(pitch_score(0), 100)
        self.assertEqual(pitch_score(200), 0)

    def test_timing_formula(self):
        self.assertEqual(timing_score(52), 74)
        self.assertEqual(timing_score(0), 100)
        self.assertEqual(timing_score(200), 0)

    def test_combined_formula(self):
        self.assertEqual(combined_score(82, 74), 79)

    def test_negative_rejected(self):
        with self.assertRaises(ValueError):
            pitch_score(-1)
        with self.assertRaises(ValueError):
            timing_score(-1)

    def test_missing_values(self):
        with self.assertRaises(ValueError):
            pitch_score(None)

    def test_lowconf(self):
        r = score_take(LOWCONF_TAKE)
        self.assertFalse(r["ok"])
        self.assertIsNone(r["combined"])
        self.assertIn("ไม่ชัด", r["message_th"])

    def test_bands(self):
        self.assertEqual(score_take({"mean_cents_off": 10, "mean_ms_off": 10, "confidence": 0.95})["band"], "great")
        self.assertEqual(score_take({"mean_cents_off": 80, "mean_ms_off": 80, "confidence": 0.95})["band"], "ok")
        self.assertEqual(score_take({"mean_cents_off": 120, "mean_ms_off": 120, "confidence": 0.95})["band"], "try_again")

    def test_key_from_exercise(self):
        self.assertEqual((self.key["tonic"], self.key["mode"]), ("C", "major"))
        self.assertEqual(self.key["source"], "exercise")
        self.assertIn("ScaleRun" if False else "สเกลรัน", self.key["name_th"])
        self.assertIn("C major", self.key["headline_th"])

    def test_key_from_notes(self):
        k = key_finder(TOM_TAKE["notes"])
        self.assertEqual((k["tonic"], k["mode"], k["source"]), ("C", "major", "notes"))
        self.assertEqual(k["hit"], 8)

    def test_unknown_exercise(self):
        with self.assertRaisesRegex(ValueError, "unknown exercise"):
            key_finder(["C"], "happy_birthday")

    def test_no_notes(self):
        with self.assertRaisesRegex(ValueError, "no notes"):
            key_finder(["Q"])

    def test_warmups(self):
        w = warmups()
        self.assertEqual(w["count"], 4)
        self.assertEqual(w["total_sec"], 100)
        self.assertEqual(w["items"][0]["key"], "lip_trill")
        self.assertIn("ลิปทริลล์", w["headline_th"] + w["items"][0]["name_th"])

    def test_warmup_subset(self):
        w = warmups(["lip_trill", "hum_five"])
        self.assertEqual(w["total_sec"], 50)
        self.assertEqual(w["count"], 2)

    def test_unknown_warmup(self):
        with self.assertRaisesRegex(ValueError, "unknown warmup"):
            warmups(["opera_scream"])

    def test_duet_tom_wins(self):
        d = duet_battle("พี่ต้อม", self.tom["combined"], "น้องนีน่า", self.nina["combined"])
        self.assertEqual(d["verdict"], "a")
        self.assertEqual(d["winner"], "พี่ต้อม")
        self.assertEqual(d["margin"], 7)
        self.assertIn("นำ 7", d["headline_th"])

    def test_duet_tie(self):
        d = duet_battle("พี่ต้อม", 80, "น้องนีน่า", 80)
        self.assertEqual(d["verdict"], "tie")
        self.assertIsNone(d["winner"])
        self.assertEqual(d["margin"], 0)

    def test_duet_b_wins(self):
        d = duet_battle("พี่ต้อม", 60, "น้องนีน่า", 88)
        self.assertEqual((d["verdict"], d["winner"]), ("b", "น้องนีน่า"))

    def test_duet_missing(self):
        with self.assertRaises(ValueError):
            duet_battle("a", 80, "b", None)

    def test_log(self):
        log = practice_log([], TODAY, "scale_run_c", 79, "ok")
        log = practice_log(log["rows"], TODAY, "vowel_hold", 90, "easy")
        self.assertEqual(log["count"], 2)
        self.assertEqual(log["best"], 90)
        self.assertIn("90", log["headline_th"])

    def test_log_errors(self):
        with self.assertRaises(ValueError):
            practice_log([], TODAY, "scale_run_c", 79, "pain")
        with self.assertRaises(ValueError):
            practice_log([], TODAY, "let_it_go", 79, "ok")

    def test_share(self):
        s = share_card("พี่ต้อม", self.tom, self.key)
        self.assertEqual(s["combined"], 79)
        self.assertEqual(s["pitch"], 82)
        self.assertIn("SING", s["cta_th"])
        self.assertTrue(s["hook_th"].startswith("ร้องคาราโอเกะให้คะแนน"))
        self.assertEqual(s["layout"], "sing_card")
        self.assertIn("C major", s["key_th"])

    def test_share_no_key(self):
        self.assertIsNone(share_card("พี่ต้อม", self.tom, None)["key_th"])

    def test_quota(self):
        self.assertEqual(quota(1, 1), {"allowed": 1, "left_after": 1, "paywall": False})
        self.assertEqual(quota(3, 1), {"allowed": 0, "left_after": 0, "paywall": True})
        self.assertEqual(quota(0, 5, pro=True)["paywall"], False)

    def test_safety(self):
        self.assertEqual(safety_guard()["level"], "ok")
        self.assertEqual(safety_guard(sore_throat=True)["level"], "stop")
        self.assertEqual(safety_guard(strain=True)["level"], "stop")
        self.assertIn("ไม่มีเนื้อเพลงลิขสิทธิ์", safety_guard()["message_th"])

    def test_bee_great(self):
        r = score_take(BEE_TAKE)
        self.assertEqual(r["combined"], 90)
        self.assertEqual(r["band"], "great")

    def test_g_scale_key(self):
        k = key_finder(EXERCISES["scale_run_g"]["notes"], "scale_run_g")
        self.assertEqual(k["tonic"], "G")

    def test_library(self):
        self.assertEqual(len(EXERCISES), 6)
        self.assertEqual(len(WARMUPS), 4)
        ids = [e["id"] for e in EXERCISES.values()]
        self.assertEqual(len(ids), len(set(ids)))

    def test_no_copyrighted_titles(self):
        blob = " ".join(e["name_en"]+" "+e["name_th"] for e in EXERCISES.values())
        for banned in ("Let It Go", "My Heart Will Go On", "Despacito", "Shape of You", "รักไม่ยอมเปลี่ยนแปลง"):
            self.assertNotIn(banned, blob)

    def test_watermark(self):
        self.assertIn("no bundled lyrics", WATERMARK)

    def test_boundary_good(self):
        # combined 70 exactly → good: pitch 70 timing 70
        r = score_take({"mean_cents_off": 60, "mean_ms_off": 60, "confidence": 0.9})
        self.assertEqual(r["combined"], 70)
        self.assertEqual(r["band"], "good")

    def test_boundary_ok(self):
        r = score_take({"mean_cents_off": 100, "mean_ms_off": 100, "confidence": 0.9})
        self.assertEqual(r["combined"], 50)
        self.assertEqual(r["band"], "ok")

    def test_f_scale_notes(self):
        self.assertEqual(EXERCISES["scale_run_f"]["notes"][0], "F")
        self.assertIn("Bb", EXERCISES["scale_run_f"]["notes"])

    def test_warmup_ids_unique(self):
        ids = [w["id"] for w in WARMUPS.values()]
        self.assertEqual(len(ids), len(set(ids)))

    def test_message_good(self):
        self.assertIn("เกลาเสียง", self.tom["message_th"])

    def test_log_single(self):
        log = practice_log([], TODAY, "hum_fifth", 64, "hard")
        self.assertEqual(log["rows"][0]["name_th"], "ฮัมช่วงห้า")
        self.assertEqual(log["best"], 64)

    def test_hum_fifth_key(self):
        k = key_finder(["C","G","C"], "hum_fifth")
        self.assertEqual(k["mode"], "fifth")

    def test_vowel_hold_tonic(self):
        self.assertEqual(EXERCISES["vowel_hold"]["tonic"], "A")

    def test_share_timing(self):
        self.assertEqual(share_card("พี่ต้อม", self.tom, self.key)["timing"], 74)

    def test_disclaimer_on_score(self):
        self.assertIn("ไม่ใช่ครูสอนร้อง", self.tom["disclaimer_th"])

if __name__ == "__main__":
    unittest.main()
