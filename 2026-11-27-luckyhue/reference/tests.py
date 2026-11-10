import unittest
from luckyhue import *
from fixtures import *

class T(unittest.TestCase):
    def setUp(self):
        self.lucky = lucky_color("friday", TODAY)
        self.closet = parse_closet(MAY_CLOSET)
        self.mix = outfit_mix(self.closet, self.lucky, pick=MAY_PICK)

    def test_may_birthday(self):
        self.assertEqual(weekday_from_date(MAY_BIRTH), "friday")
        self.assertEqual(weekday_from_date(TODAY), "friday")

    def test_may_color(self):
        self.assertEqual(self.lucky["color_th"], "ฟ้า")
        self.assertEqual(self.lucky["hex"], "#38BDF8")
        self.assertTrue(self.lucky["today_is_birth_day"])
        self.assertIn("วันศุกร์", self.lucky["headline_th"])
        self.assertIn("ฟ้า", self.lucky["headline_th"])

    def test_may_quality(self):
        self.assertEqual(self.closet["quality"]["score"], 88)
        self.assertTrue(self.closet["ok"])
        self.assertEqual(self.closet["count"], 5)

    def test_may_mix(self):
        self.assertEqual(self.mix["verdict"], "match")
        self.assertEqual((self.mix["lucky_n"], self.mix["neutral_n"], self.mix["other_n"]), (1, 2, 0))
        self.assertEqual(self.mix["score"], 67)
        self.assertIn("แมตช์สีฟ้า", self.mix["headline_th"])
        self.assertEqual([i["id"] for i in self.mix["items"]], MAY_PICK)

    def test_auto_mix(self):
        m = outfit_mix(self.closet, self.lucky)
        self.assertEqual(m["count"], 4)
        self.assertEqual(m["score"], 62)
        self.assertEqual(m["verdict"], "match")

    def test_clash(self):
        m = outfit_mix(self.closet, self.lucky, pick=CLASH_PICK)
        self.assertEqual(m["verdict"], "clash")
        self.assertEqual(m["score"], 50)
        self.assertEqual(m["other_n"], 1)

    def test_no_match(self):
        m = outfit_mix(self.closet, lucky_color("sunday"), pick=["i01", "i03"])
        self.assertEqual(m["verdict"], "no_match")
        self.assertEqual(m["lucky_n"], 0)
        self.assertEqual(m["score"], 50)  # two neutrals: 100*(0+0.5*2)/2

    def test_unknown_item(self):
        with self.assertRaisesRegex(ValueError, "unknown item"):
            outfit_mix(self.closet, self.lucky, pick=["i99"])

    def test_closet_not_ok(self):
        with self.assertRaises(ValueError):
            outfit_mix(parse_closet(EMPTY_SHOT), self.lucky)

    def test_bad_quality(self):
        q = parse_closet(BAD_SHOT)["quality"]
        self.assertEqual(q["score"], 43)
        self.assertFalse(q["ok"])
        self.assertGreaterEqual(len(q["tips_th"]), 3)

    def test_empty(self):
        e = parse_closet(EMPTY_SHOT)
        self.assertFalse(e["ok"])
        self.assertEqual(e["quality"]["score"], 54)
        self.assertIn("ยังไม่เจอเสื้อผ้า", " ".join(e["quality"]["tips_th"]))

    def test_bad_input(self):
        with self.assertRaises(ValueError):
            scan_quality(1.2, 0, 0, 1)

    def test_unknown_weekday(self):
        with self.assertRaisesRegex(ValueError, "unknown weekday"):
            lucky_color("funday")

    def test_bow_sunday(self):
        self.assertEqual(BOW["birth_weekday"], "sunday")
        c = lucky_color(BOW["birth_weekday"])
        self.assertEqual((c["color_th"], c["hex"]), ("แดง", "#DC2626"))

    def test_ken_wednesday(self):
        self.assertEqual(KEN["birth_weekday"], "wednesday")
        day = lucky_color("wednesday")
        night = lucky_color("wednesday", use_wednesday_night=True)
        self.assertEqual(day["color_th"], "เขียว")
        self.assertEqual(night["color_th"], "แสด")
        self.assertTrue(night["night_mode"])
        self.assertFalse(day["night_mode"])

    def test_all_seven_colors(self):
        self.assertEqual(len(WEEKDAYS), 7)
        seen=set()
        for k in WEEKDAYS:
            c=lucky_color(k)
            seen.add(c["hex"])
            self.assertTrue(c["headline_th"].startswith("สีมงคล"))
        self.assertEqual(len(seen), 7)

    def test_wallpaper(self):
        w = wallpaper(self.lucky)
        self.assertEqual(w["size"], "1080x1920")
        self.assertEqual(w["hex"], "#38BDF8")
        self.assertEqual(w["palette"][0], "#38BDF8")
        self.assertIn("วอลเปเปอร์สีฟ้า", w["title_th"])
        self.assertIn("สบาย", w["blessing_th"])

    def test_wallpaper_sizes(self):
        self.assertEqual(wallpaper(self.lucky, "1080x1080")["size"], "1080x1080")
        with self.assertRaises(ValueError):
            wallpaper(self.lucky, "640x640")

    def test_calendar(self):
        cal = weekly_calendar(TODAY, "friday")
        self.assertEqual(cal["start_iso"], "2026-11-23")
        self.assertEqual(cal["count"], 7)
        self.assertEqual(cal["days"][0]["weekday"], "monday")
        self.assertTrue(cal["days"][4]["is_birth_day"])  # Friday
        self.assertEqual(sum(1 for d in cal["days"] if d["is_birth_day"]), 1)
        self.assertIn("วันศุกร์", cal["headline_th"])

    def test_calendar_midweek_start(self):
        # Wednesday 25 Nov still snaps to Monday 23
        self.assertEqual(weekly_calendar("2026-11-25", "friday")["start_iso"], "2026-11-23")

    def test_share(self):
        s = share_card("พี่เมย์", self.lucky, self.mix)
        self.assertEqual(s["color_th"], "ฟ้า")
        self.assertEqual(s["outfit_score"], 67)
        self.assertIn("HUE", s["cta_th"])
        self.assertTrue(s["hook_th"].startswith("สีมงคลประจำวัน"))
        self.assertEqual(s["layout"], "hue_card")

    def test_quota(self):
        self.assertEqual(quota(1, 1), {"allowed": 1, "left_after": 1, "paywall": False})
        self.assertEqual(quota(3, 1), {"allowed": 0, "left_after": 0, "paywall": True})
        self.assertEqual(quota(0, 5, pro=True)["paywall"], False)

    def test_safety(self):
        self.assertEqual(safety_guard()["level"], "ok")
        self.assertEqual(safety_guard(True)["level"], "warn")
        self.assertIn("ไม่ใช่หมอดู", safety_guard()["message_th"])

    def test_navy_friday_is_lucky(self):
        closet = {"ok": True, "items": [{"id": "n1", "name_th": "เสื้อกรม", "category": "top", "color_key": "navy", "color_th": "กรม"}]}
        m = outfit_mix(closet, self.lucky, pick=["n1"])
        self.assertEqual(m["lucky_n"], 1)
        self.assertEqual(m["neutral_n"], 0)
        self.assertEqual(m["score"], 100)

    def test_navy_monday_is_neutral(self):
        closet = {"ok": True, "items": [{"id": "n1", "name_th": "เสื้อกรม", "category": "top", "color_key": "navy", "color_th": "กรม"}]}
        m = outfit_mix(closet, lucky_color("monday"), pick=["n1"])
        self.assertEqual(m["verdict"], "no_match")
        self.assertEqual(m["neutral_n"], 1)

    def test_unknown_category(self):
        sh = dict(MAY_CLOSET, items=[{"id": "x", "name_th": "หมวก", "category": "hat", "color_key": "blue", "color_th": "ฟ้า"}])
        with self.assertRaisesRegex(ValueError, "unknown category"):
            parse_closet(sh)

    def test_today_not_birthday(self):
        c = lucky_color("monday", TODAY)
        self.assertFalse(c["today_is_birth_day"])
        self.assertTrue(c["is_birth_day"])

    def test_watermark(self):
        self.assertIn("for fun", WATERMARK)
        self.assertIn("วันพุธ", SAFETY_DISCLAIMER_TH)

    def test_library_ids_unique(self):
        ids = [v["id"] for v in WEEKDAYS.values()]
        self.assertEqual(len(ids), len(set(ids)))

    def test_may_message(self):
        self.assertIn("5 ชิ้น", self.closet["message_th"])

    def test_blessing_friday(self):
        self.assertIn("สบาย", self.lucky["blessing_th"])

    def test_share_none_mix(self):
        s = share_card("พี่เมย์", self.lucky, None)
        self.assertIsNone(s["outfit_score"])

    def test_monday_yellow(self):
        self.assertEqual(lucky_color("monday")["color_th"], "เหลือง")

    def test_saturday_purple(self):
        self.assertEqual(lucky_color("saturday")["hex"], "#7C3AED")

    def test_thursday_orange(self):
        self.assertEqual(lucky_color("thursday")["color_th"], "ส้ม")

    def test_tuesday_pink(self):
        self.assertEqual(lucky_color("tuesday")["color_th"], "ชมพู")

    def test_wallpaper_palette_len(self):
        self.assertEqual(len(wallpaper(self.lucky)["palette"]), 3)

    def test_mix_hex(self):
        self.assertEqual(self.mix["hex"], "#38BDF8")

    def test_calendar_days_hex(self):
        cal=weekly_calendar(TODAY,"sunday")
        self.assertEqual(cal["days"][6]["hex"], "#DC2626")
        self.assertTrue(cal["days"][6]["is_birth_day"])

    def test_empty_mix_score_zero_items_guard(self):
        # only possible if pick is empty list
        m=outfit_mix(self.closet, self.lucky, pick=[])
        self.assertEqual(m["count"], 0)
        self.assertEqual(m["score"], 0)
        self.assertEqual(m["verdict"], "no_match")

    def test_bow_wallpaper_red(self):
        w=wallpaper(lucky_color("sunday"), "1170x2532")
        self.assertEqual(w["size"], "1170x2532")
        self.assertEqual(w["color_th"], "แดง")

if __name__ == "__main__":
    unittest.main()
