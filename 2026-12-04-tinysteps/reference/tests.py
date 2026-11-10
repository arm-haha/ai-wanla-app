import unittest
from tinysteps import *
from fixtures import *

class T(unittest.TestCase):
    def setUp(self):
        self.scan = photo_scan(PHU_PHOTO)
        self.months = age_months(PHU["birth"], TODAY)
        self.card = milestone_card(PHU["name_th"], self.months, "sit", PHU_PHOTO["id"])
        self.growth = growth_entry(self.months, PHU["weight_kg"], PHU["height_cm"])
        self.consent = consent_guard(True, True, 31, True)

    def test_phu_quality(self):
        q = self.scan["quality"]
        self.assertEqual(q["score"], 90)
        self.assertTrue(q["ok"])
        self.assertEqual(q["tips_th"], [])

    def test_quality_tips(self):
        s = photo_scan(PHOTOS[2])
        self.assertEqual(s["quality"]["score"], 46)
        self.assertFalse(s["quality"]["ok"])
        self.assertGreaterEqual(len(s["quality"]["tips_th"]), 3)

    def test_bad_quality(self):
        with self.assertRaises(ValueError):
            scan_quality(1.2, 0, 0)

    def test_pipeline(self):
        self.assertEqual(pipeline_steps(PHU_PHOTO),
                         ["photo", "age_months", "milestone_card", "caption"])
        self.assertIn("deglare", pipeline_steps(PHOTOS[2]))
        self.assertIn("recrop", pipeline_steps(PHOTOS[2]))

    def test_age_eight(self):
        self.assertEqual(self.months, 8)
        self.assertEqual(age_months("2026-04-04", "2026-12-03"), 7)

    def test_age_zero_and_bad(self):
        self.assertEqual(age_months("2026-12-04", TODAY), 0)
        with self.assertRaises(ValueError):
            age_months("2026-12-05", TODAY)

    def test_card_title(self):
        self.assertEqual(self.card["title_th"], "เดือนที่ 8 · นั่งทรงตัวได้")
        self.assertEqual(self.card["headline_th"], "น้องภู · เดือนที่ 8 · นั่งทรงตัวได้")
        self.assertEqual(self.card["caption_th"], "เดือนนี้เพิ่งนั่งทรงตัวได้ เก็บช่วงนี้ไว้ในอัลบั้มนะ")

    def test_growth_in_band(self):
        self.assertEqual(self.growth["weight_pos"], "in")
        self.assertEqual(self.growth["height_pos"], "in")
        self.assertEqual(self.growth["band"]["weight_mid_kg"], 8.4)
        self.assertEqual(self.growth["band"]["height_mid_cm"], 70.0)
        self.assertIn("ไม่ใช่เกณฑ์แพทย์", self.growth["band"]["disclaimer_th"])

    def test_growth_below_above(self):
        g = growth_entry(8, 6.0, 76.0)
        self.assertEqual(g["weight_pos"], "below")
        self.assertEqual(g["height_pos"], "above")
        self.assertIn("ต่ำกว่าแถบตัวอย่าง", g["weight_label_th"])
        self.assertIn("สูงกว่าแถบตัวอย่าง", g["height_label_th"])
        self.assertNotIn(" Delayed", g["weight_label_th"])

    def test_growth_bad(self):
        with self.assertRaises(ValueError):
            growth_entry(8, 0, 70)
        with self.assertRaises(ValueError):
            example_band(40)

    def test_firsts_library(self):
        self.assertEqual(len(FIRSTS), 8)
        self.assertEqual(len(set(v["id"] for v in FIRSTS.values())), 8)
        info = first_info("sit")
        self.assertEqual(info["example_month"], 8)
        self.assertEqual((info["range_lo"], info["range_hi"]), (6, 9))

    def test_unknown_first(self):
        with self.assertRaises(ValueError):
            first_info("drive")

    def test_log_first_in_and_out(self):
        ok = log_first("sit", 8, "นั่งเล่นได้นานขึ้น")
        self.assertEqual(ok["flag"], "in_example")
        late = log_first("sit", 14)
        self.assertEqual(late["flag"], "outside_example")
        self.assertIn("ปรึกษาแพทย์", late["tip_th"])
        self.assertNotIn("พัฒนาการล่าช้า", late["tip_th"])

    def test_timeline(self):
        entries = [log_first(k, m, n) for k, m, n in PHU_FIRSTS]
        tl = timeline(entries)
        self.assertEqual(tl["count"], 3)
        self.assertEqual([e["kind"] for e in tl["entries"]], ["smile", "roll", "sit"])

    def test_timeline_empty(self):
        with self.assertRaises(ValueError):
            timeline([])

    def test_captions(self):
        qs = captions("sit", "น้องภู", 2)
        self.assertEqual(qs[0]["text_th"], "เดือนนี้เพิ่งนั่งทรงตัวได้ เก็บช่วงนี้ไว้ในอัลบั้มนะ")
        self.assertEqual(len(qs), 2)
        with self.assertRaises(ValueError):
            captions("fly", "น้องภู")

    def test_month_ideas(self):
        ideas = month_ideas(8)
        self.assertEqual(len(ideas["ideas_th"]), 2)
        self.assertIn("หมอนค้ำ", ideas["ideas_th"][0])
        self.assertIn("ไม่ใช่แบบฝึกแพทย์", ideas["disclaimer_th"])
        self.assertEqual(len(month_ideas(3)["ideas_th"]), 2)

    def test_collage_eight(self):
        c = collage("อัลบั้มน้องภู 8 เดือน", PHU_COLLAGE)
        self.assertEqual(c["count"], 8)
        self.assertEqual((c["cols"], c["rows"]), (3, 3))

    def test_collage_four(self):
        c = collage("สี่เดือนแรก", PHU_COLLAGE[:4])
        self.assertEqual((c["cols"], c["rows"]), (2, 2))
        with self.assertRaises(ValueError):
            collage("x", [])

    def test_print_sheet(self):
        s = print_sheet("น้องภู", 8, self.card["caption_th"], "portrait_a4")
        self.assertEqual(s["bleed_mm"], 3)
        self.assertIn("A4", s["sizes"])
        self.assertTrue(print_sheet("น้องภู", 8, "x", "book_20")["label_th"].startswith("หน้าอัลบั้ม"))
        with self.assertRaises(ValueError):
            print_sheet("น้องภู", 8, "x", "poster")

    def test_share(self):
        s = share_card("น้องภู", 8, "sit", self.card["caption_th"])
        self.assertEqual(s["headline_th"], "เดือนที่ 8 · นั่งทรงตัวได้")
        self.assertIn("STEPS", s["cta_th"])
        self.assertIn("ไม่ medical" if False else "ไม่ใช่คำแนะนำทางการแพทย์", s["disclaimer_th"])

    def test_quota(self):
        self.assertEqual(quota(1, 1), {"allowed": 1, "left_after": 1, "paywall": False})
        self.assertEqual(quota(3, 1), {"allowed": 0, "left_after": 0, "paywall": True})
        self.assertEqual(quota(0, 5, pro=True)["paywall"], False)

    def test_consent_ok(self):
        self.assertTrue(self.consent["ok"])
        self.assertEqual(self.consent["blocks_th"], [])

    def test_consent_blocks(self):
        self.assertFalse(consent_guard(False, True, 31)["ok"])
        self.assertFalse(consent_guard(True, False, 31)["ok"])
        self.assertFalse(consent_guard(True, True, 16)["ok"])
        self.assertFalse(consent_guard(True, True, None)["ok"])
        self.assertFalse(consent_guard(True, True, 31, False)["ok"])
        self.assertTrue(any("ลูกตนเอง" in b for b in consent_guard(False, True, 31)["blocks_th"]))

    def test_safety_guard(self):
        self.assertEqual(safety_guard(True)["level"], "ok")
        self.assertEqual(safety_guard(False)["level"], "stop")
        self.assertIn("ไม่ใช่คำแนะนำทางการแพทย์", safety_guard()["message_th"])

    def test_nan_age_12(self):
        self.assertEqual(age_months(NAN["child"]["birth"], TODAY), 12)
        g = growth_entry(12, 9.8, 76.0)
        # mid w=3.2+7.8=11.0, mid h=50+30=80; 9.8 and 76 are in (9.5-12.5, 76-84)
        self.assertEqual(g["weight_pos"], "in")
        self.assertEqual(g["height_pos"], "in")

    def test_band_month_zero(self):
        b = example_band(0)
        self.assertEqual(b["weight_mid_kg"], 3.2)
        self.assertEqual(b["height_mid_cm"], 50.0)

    def test_ideas_bounds(self):
        with self.assertRaises(ValueError):
            month_ideas(-1)

    def test_scan_child_id(self):
        self.assertEqual(self.scan["photo_id"], "p01")
        self.assertEqual(self.scan["child_id"], "c01")

    def test_wave_and_walk_info(self):
        self.assertEqual(first_info("wave")["name_th"], "โบกมือ")
        self.assertEqual(first_info("walk")["range_hi"], 18)

    def test_caption_cycle(self):
        qs = captions("smile", "น้องภู", 3)
        self.assertEqual(len(qs), 3)
        self.assertEqual(qs[0]["n"], 1)

    def test_no_diagnosis_wording(self):
        text = " ".join([
            SAFETY_DISCLAIMER_TH,
            log_first("walk", 20)["tip_th"],
            growth_entry(8, 6.0, 70)["weight_label_th"],
        ])
        for banned in ("วินิจฉัย", "โรค", "แคระแกร็น", "อ้วน", "พัฒนาการล่าช้า"):
            self.assertNotIn(banned, text)


    def test_print_collage_layout(self):
        self.assertEqual(print_sheet("น้องภู", 8, "x", "collage_a4")["layout"], "collage_a4")

    def test_share_sizes(self):
        s = share_card("น้องภู", 8, "sit", "x")
        self.assertEqual(s["layout"], "milestone_card")
        self.assertIn("1080x1350", s["sizes"])

    def test_log_early_sit(self):
        e = log_first("sit", 5)
        self.assertEqual(e["flag"], "outside_example")

    def test_consent_message(self):
        self.assertIn("ผ่านการตรวจยินยอม", self.consent["message_th"])

    def test_month_ideas_12(self):
        self.assertIn("หนังสือภาพ", month_ideas(12)["ideas_th"][0])

    def test_timeline_order_ties(self):
        entries = [log_first("wave", 10), log_first("stand", 10)]
        tl = timeline(entries)
        self.assertEqual([e["kind"] for e in tl["entries"]], ["stand", "wave"])

    def test_card_sizes(self):
        self.assertIn("1080x1350", self.card["sizes"])
        self.assertEqual(self.card["kind"], "sit")
        self.assertEqual(self.card["month"], 8)

    def test_growth_mid_exact(self):
        g = growth_entry(0, 3.2, 50.0)
        self.assertEqual(g["weight_pos"], "in")
        self.assertEqual(g["height_pos"], "in")

    def test_people_fiction(self):
        self.assertEqual(MEY["name_th"], "พี่เมย")
        self.assertEqual(PHU["name_th"], "น้องภู")
        self.assertTrue(MEY["own_child"])


if __name__ == "__main__":
    unittest.main()
