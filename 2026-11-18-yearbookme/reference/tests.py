import unittest
from yearbookme import *
from fixtures import *

class T(unittest.TestCase):
    def setUp(self):
        self.scan = photo_scan(MIND_PHOTO)
        self.studio = era_studio(MIND_PHOTO, MIND_TRAITS, MIND["name_th"])
        self.consent = consent_guard(MIND_PHOTO, MIND_PROFILE)

    # 1) Photo scan
    def test_mind_scan(self):
        self.assertEqual(self.scan["face_count"], 1)
        self.assertEqual(self.scan["uncertain"], [])
        self.assertTrue(self.scan["faces"][0]["own_face"])

    def test_mind_quality(self):
        q = self.scan["quality"]
        self.assertEqual(q["score"], 88)
        self.assertTrue(q["ok"])
        self.assertEqual(q["tips_th"], [])

    def test_quality_tips(self):
        s = photo_scan(PHOTOS[5])
        self.assertEqual(s["quality"]["score"], 46)
        self.assertFalse(s["quality"]["ok"])
        self.assertGreaterEqual(len(s["quality"]["tips_th"]), 3)

    def test_no_face(self):
        s = photo_scan(PHOTOS[6])
        self.assertFalse(s["quality"]["ok"])
        self.assertEqual(s["face_count"], 0)
        self.assertIn("ไม่เจอใบหน้า", " ".join(s["quality"]["tips_th"]))

    def test_low_conf_uncertain(self):
        s = photo_scan(PHOTOS[9])
        self.assertEqual(s["uncertain"], ["blur-face"])
        self.assertEqual(s["face_count"], 0)

    def test_bad_quality_input(self):
        with self.assertRaises(ValueError):
            scan_quality(1.5, 0, 0, 1)

    def test_pipeline(self):
        self.assertEqual(pipeline_steps(MIND_PHOTO),
                         ["face_detect", "consent_check", "era_score", "style_render", "caption"])
        st = pipeline_steps(PHOTOS[5])
        self.assertIn("deglare", st)
        self.assertIn("recrop", st)

    # 2) Consent guard
    def test_mind_consent_ok(self):
        self.assertTrue(self.consent["ok"])
        self.assertEqual(self.consent["level"], "ok")
        self.assertEqual(self.consent["blocks_th"], [])

    def test_not_own_photo(self):
        p = dict(MIND_PROFILE, own_photo=False)
        g = consent_guard(MIND_PHOTO, p)
        self.assertFalse(g["ok"])
        self.assertTrue(any("รูปของตนเอง" in b for b in g["blocks_th"]))

    def test_no_confirm(self):
        p = dict(MIND_PROFILE, consent_confirmed=False)
        self.assertFalse(consent_guard(MIND_PHOTO, p)["ok"])

    def test_celebrity_blocked(self):
        g = consent_guard(PHOTOS[8], dict(MIND_PROFILE, own_photo=False, celebrity_likely=True))
        self.assertFalse(g["ok"])
        self.assertTrue(any("สาธารณะ" in b for b in g["blocks_th"]))

    def test_other_faces_need_consent(self):
        g = consent_guard(PHOTOS[7], dict(MIND_PROFILE, all_consented=False))
        self.assertFalse(g["ok"])
        self.assertTrue(any("ยินยอมจากทุกคน" in b for b in g["blocks_th"]))

    def test_other_faces_ok_when_all_consent(self):
        g = consent_guard(PHOTOS[7], dict(MIND_PROFILE, all_consented=True))
        self.assertTrue(g["ok"])

    def test_child_blocked(self):
        g = consent_guard(MIND_PHOTO, dict(MIND_PROFILE, age=11, guardian_ok=True))
        self.assertFalse(g["ok"])
        self.assertTrue(any("13" in b for b in g["blocks_th"]))

    def test_teen_needs_guardian(self):
        g = consent_guard(PRAE["photo"], dict(age=16, own_photo=True, consent_confirmed=True,
                                             guardian_ok=False, all_consented=True, celebrity_likely=False))
        self.assertFalse(g["ok"])
        g2 = consent_guard(PRAE["photo"], {k: PRAE[k] for k in MIND_PROFILE})
        self.assertTrue(g2["ok"])

    # 3) Era studio (wow)
    def test_mind_scores(self):
        self.assertEqual(era_score(MIND_TRAITS, "80s"), 39)
        self.assertEqual(era_score(MIND_TRAITS, "90s"), 88)
        self.assertEqual(era_score(MIND_TRAITS, "y2k"), 47)

    def test_mind_studio_top_90s(self):
        self.assertEqual((self.studio["top_era"], self.studio["top_score"]), ("90s", 88))
        self.assertEqual(self.studio["count"], 3)
        self.assertEqual(self.studio["renders"][0]["badge_th"], "เข้าสุด")
        self.assertEqual(self.studio["renders"][0]["year_label"], "Class of '97")

    def test_fern_top_80s(self):
        s = era_studio(FERN_PHOTO, FERN_TRAITS, FERN["name_th"])
        self.assertEqual((s["top_era"], s["top_score"]), ("80s", 78))

    def test_tang_top_y2k(self):
        s = era_studio(TANG_PHOTO, TANG_TRAITS, TANG["name_th"])
        self.assertEqual((s["top_era"], s["top_score"]), ("y2k", 85))

    def test_unknown_era(self):
        with self.assertRaises(ValueError):
            era_score(MIND_TRAITS, "70s")

    def test_library(self):
        self.assertEqual(len(ERAS), 3)
        self.assertEqual(len(set(v["id"] for v in ERAS.values())), 3)
        for e in ERA_IDS:
            info = era_info(e)
            self.assertEqual(info["era"], e)
            self.assertEqual(len(info["props_th"]), 4)
            kit = prop_kit(e)
            self.assertEqual(kit["props_th"], info["props_th"])

    # 4) Quotes + autograph
    def test_mind_quote(self):
        qs = caption_quotes("90s", "sweet", "น้องมายด์", 2)
        self.assertEqual(qs[0]["text_th"], "เพื่อนที่ขาดไม่ได้ของรุ่นนี้ — ไว้เจอกันอีกสิบปีนะ")
        self.assertEqual(qs[0]["n"], 1)
        self.assertEqual(len(qs), 2)

    def test_quote_tones_and_cycle(self):
        qs = caption_quotes("80s", "funny", "พี่เฟิร์น", 5)
        self.assertEqual(len(qs), 5)
        self.assertEqual(qs[0]["tone"], "funny")

    def test_bad_tone(self):
        with self.assertRaises(ValueError):
            caption_quotes("90s", "angry", "น้องมายด์")

    def test_autograph(self):
        a = autograph("พี่เฟิร์น", "น้องมายด์", "90s", "sweet")
        self.assertIn("เพื่อนที่ขาดไม่ได้ของรุ่นนี้", a["text_th"])
        self.assertIn("พี่เฟิร์น", a["text_th"])
        self.assertEqual(a["char_count"], 76)

    # 5) Group yearbook page
    def test_page(self):
        slots = [member_slot(p, "90s", p["traits"], p["role"]) for p in (MIND, FERN, TANG, GRACE)]
        page = yearbook_page("หน้ารุ่นจำลอง 2026", "Ficto University", 2026, "90s", slots)
        self.assertEqual(page["member_count"], 4)
        self.assertEqual((page["cols"], page["rows"]), (2, 2))
        self.assertEqual(page["year_label"], "Class of '97")
        self.assertTrue(all(s["consented"] for s in page["members"]))
        self.assertEqual(page["members"][0]["role_th"], "เพื่อนที่ขาดไม่ได้")

    def test_page_needs_consent(self):
        slots = [member_slot(MIND, "90s", MIND_TRAITS, MIND["role"])]
        slots[0]["consented"] = False
        with self.assertRaises(ValueError):
            yearbook_page("x", "y", 2026, "90s", slots)

    def test_page_empty(self):
        with self.assertRaises(ValueError):
            yearbook_page("x", "y", 2026, "90s", [])

    def test_bad_role(self):
        with self.assertRaises(ValueError):
            member_slot(MIND, "90s", MIND_TRAITS, "valedictorian")

    def test_five_members_grid(self):
        slots = [member_slot(p, "90s", p["traits"], p["role"]) for p in PEOPLE]
        page = yearbook_page("รุ่นทดลอง", "Ficto", 2026, "90s", slots)
        self.assertEqual((page["cols"], page["rows"]), (3, 2))

    # 6) Print + share + quota + safety
    def test_print_sheet(self):
        q = caption_quotes("90s", "sweet", "น้องมายด์", 1)[0]["text_th"]
        s = print_sheet("น้องมายด์", "90s", q, "portrait_a4")
        self.assertEqual(s["year_label"], "Class of '97")
        self.assertEqual(s["bleed_mm"], 3)
        self.assertIn("A4", s["sizes"])

    def test_print_layouts(self):
        self.assertEqual(print_sheet("น้องมายด์", "y2k", "x", "four_up")["layout"], "four_up")
        self.assertEqual(print_sheet("น้องมายด์", "80s", "x", "sticker")["label_th"].startswith("สติกเกอร์"), True)
        with self.assertRaises(ValueError):
            print_sheet("น้องมายด์", "90s", "x", "poster")

    def test_share(self):
        q = caption_quotes("90s", "sweet", "น้องมายด์", 1)[0]["text_th"]
        s = share_card("น้องมายด์", "90s", 88, q)
        self.assertEqual(s["headline_th"], "Class of '97 · ยุค 90s")
        self.assertIn("YEARBOOK", s["cta_th"])
        self.assertIn("88", s["cta_th"])

    def test_quota(self):
        self.assertEqual(quota(1, 1), {"allowed": 1, "left_after": 1, "paywall": False})
        self.assertEqual(quota(3, 1), {"allowed": 0, "left_after": 0, "paywall": True})
        self.assertEqual(quota(0, 5, pro=True)["paywall"], False)

    def test_safety_guard(self):
        self.assertEqual(safety_guard(True, 22)["level"], "ok")
        self.assertEqual(safety_guard(False, 22)["level"], "stop")
        self.assertEqual(safety_guard(True, 16)["level"], "warn")
        self.assertEqual(safety_guard(True, 11)["level"], "stop")
        self.assertIn("รูปคนอื่น", safety_guard(True)["message_th"])


    def test_badges(self):
        r = {x["era"]: x["badge_th"] for x in self.studio["renders"]}
        self.assertEqual(r["90s"], "เข้าสุด")
        self.assertEqual(r["80s"], "ลุคทดลอง")
        self.assertEqual(style_render(GRACE["photo"], "90s", GRACE["traits"], GRACE["name_th"])["badge_th"], "ใช้ได้ดี")

    def test_style_render_hook(self):
        r = style_render(MIND_PHOTO, "90s", MIND_TRAITS, "น้องมายด์")
        self.assertEqual(r["headline_th"], "น้องมายด์ · Class of '97")
        self.assertEqual(r["hook_th"], "เซลฟี่เดียว กลายเป็นรูปรุ่นยุค 90s")
        self.assertEqual(r["frame"], "white_yearbook")

    def test_two_face_tip(self):
        s = photo_scan(PHOTOS[7])
        self.assertEqual(s["face_count"], 2)
        self.assertTrue(any("หลายใบหน้า" in t for t in s["quality"]["tips_th"]))

    def test_missing_age(self):
        p = dict(MIND_PROFILE)
        p.pop("age")
        g = consent_guard(MIND_PHOTO, p)
        self.assertFalse(g["ok"])
        self.assertTrue(any("อายุ" in b for b in g["blocks_th"]))

    def test_era_info_bad(self):
        with self.assertRaises(ValueError):
            era_info("70s")

    def test_member_score_matches(self):
        sl = member_slot(MIND, "90s", MIND_TRAITS, "most_likely_friend")
        self.assertEqual(sl["score"], 88)
        self.assertEqual(sl["nickname_th"], "มายด์")

if __name__ == "__main__":
    unittest.main()
