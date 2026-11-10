import unittest
from stickerme import *
from fixtures import *

def _scan(shot):
    q = scan_quality(shot["glare"], shot["blur"], shot["crop"], shot["face_conf"], shot["face_frac"])
    return {"shot_id": shot["id"], "quality": q, "ok": q["ok"], "face_conf": shot["face_conf"],
            "face_frac": shot["face_frac"]}

class T(unittest.TestCase):
    def setUp(self):
        self.scan = _scan(JANE_SELFIE)
        self.consent = consent_guard(**JANE_CONSENT)
        self.pack = make_pack(self.scan, "chibi", self.consent)
        self.export = export_spec(self.pack)

    def test_jane_quality(self):
        self.assertEqual(self.scan["quality"]["score"], 91)
        self.assertTrue(self.scan["ok"])
        self.assertEqual(self.scan["quality"]["tips_th"], [])

    def test_jane_pack_count(self):
        self.assertEqual(self.pack["count"], 16)
        self.assertEqual(self.pack["style"], "chibi")
        self.assertEqual(self.pack["style_name_th"], "จิ๋วหัวโต")
        self.assertEqual(len(self.pack["stickers"]), 16)

    def test_jane_headline(self):
        self.assertIn("จิ๋วหัวโต", self.pack["headline_th"])
        self.assertIn("16 ใบ", self.pack["headline_th"])
        self.assertIn("8 ใบ", self.pack["headline_th"])

    def test_jane_bubbles(self):
        self.assertEqual(self.pack["with_text"], 8)
        texts = [s["text_th"] for s in self.pack["stickers"] if s["text_th"]]
        self.assertIn("เข้าใจแล้ว", texts)
        self.assertIn("รักนะ", texts)

    def test_jane_sticker_size(self):
        for s in self.pack["stickers"]:
            self.assertEqual((s["w"], s["h"]), (370, 320))
            self.assertTrue(s["transparent"])
            self.assertEqual(s["format"], "png")

    def test_export_ready(self):
        self.assertTrue(self.export["ready"])
        self.assertEqual((self.export["passed"], self.export["total"]), (6, 6))
        self.assertIn("Creators Studio", self.export["headline_th"])

    def test_export_sizes(self):
        self.assertEqual((self.export["sticker_w"], self.export["sticker_h"]), (370, 320))
        self.assertEqual((self.pack["main"]["w"], self.pack["main"]["h"]), (240, 240))
        self.assertEqual((self.pack["tab"]["w"], self.pack["tab"]["h"]), (96, 74))
        self.assertEqual(self.export["max_kb_per_sticker"], 1000)

    def test_consent_ok(self):
        self.assertEqual(self.consent["level"], "ok")
        self.assertEqual(self.consent["code"], "ok")

    def test_consent_other_stop(self):
        c = consent_guard(**OTHER_CONSENT)
        self.assertEqual(c["level"], "stop")
        self.assertEqual(c["code"], "other_person")
        self.assertIn("คนอื่น", c["message_th"])

    def test_consent_no_own_face(self):
        c = consent_guard(own_face=False)
        self.assertEqual((c["level"], c["code"]), ("stop", "no_consent"))

    def test_consent_minor_no_guardian(self):
        c = consent_guard(**MIN_CONSENT_NO)
        self.assertEqual((c["level"], c["code"]), ("stop", "minor_no_guardian"))

    def test_consent_minor_with_guardian_warn(self):
        c = consent_guard(**MIN_CONSENT_YES)
        self.assertEqual((c["level"], c["code"]), ("warn", "minor_with_guardian"))
        pack = make_pack(_scan(MIN_SELFIE), "comic", c, emotions=DEFAULT_SET_16[:8], count=8, bubble_map={})
        self.assertEqual(pack["count"], 8)
        self.assertEqual(pack["consent_code"], "minor_with_guardian")

    def test_consent_celebrity(self):
        c = consent_guard(own_face=True, celebrity_likeness=True)
        self.assertEqual((c["level"], c["code"]), ("stop", "celebrity"))

    def test_pack_blocked_without_consent(self):
        with self.assertRaisesRegex(ValueError, "consent blocked"):
            make_pack(self.scan, "chibi", consent_guard(**OTHER_CONSENT))

    def test_pack_requires_ok_scan(self):
        with self.assertRaises(ValueError):
            make_pack(_scan(BAD_SHOT), "chibi", self.consent)

    def test_bad_quality(self):
        q = _scan(BAD_SHOT)["quality"]
        self.assertEqual(q["score"], 39)
        self.assertFalse(q["ok"])
        self.assertGreaterEqual(len(q["tips_th"]), 3)

    def test_empty_and_lowconf(self):
        e = _scan(EMPTY_SHOT)
        self.assertFalse(e["ok"])
        self.assertEqual(e["quality"]["score"], 42)
        self.assertIn("ไม่มั่นใจว่าเป็นใบหน้า", " ".join(e["quality"]["tips_th"]))
        low = _scan(LOWCONF_SHOT)
        self.assertFalse(low["ok"])
        self.assertEqual(low["quality"]["score"], 56)

    def test_bad_input_scan(self):
        with self.assertRaises(ValueError):
            scan_quality(1.2, 0, 0, 1, 1)

    def test_bubble_ok(self):
        self.assertTrue(bubble_check("กินข้าวยัง?")["ok"])
        self.assertEqual(bubble_check("รักนะ")["chars"], 5)

    def test_bubble_too_long(self):
        r = bubble_check("ข้อความนี้ยาวเกินกว่าที่จะใส่บนสติกเกอร์ใบเล็ก")
        self.assertFalse(r["ok"])
        self.assertIn("ยาวเกิน", r["message_th"])

    def test_bubble_empty(self):
        self.assertFalse(bubble_check("   ")["ok"])

    def test_unknown_emotion(self):
        with self.assertRaisesRegex(ValueError, "unknown emotion"):
            make_pack(self.scan, "chibi", self.consent, emotions=["happy"] * 8 + ["not_real"] + ["ok"] * 7)

    def test_unknown_style(self):
        with self.assertRaisesRegex(ValueError, "unknown style"):
            make_pack(self.scan, "oilpaint", self.consent)

    def test_unknown_bubble(self):
        with self.assertRaisesRegex(ValueError, "unknown bubble"):
            make_pack(self.scan, "chibi", self.consent, bubble_map={"happy": "not_a_bubble"})

    def test_count_must_be_allowed(self):
        with self.assertRaisesRegex(ValueError, "count must be"):
            make_pack(self.scan, "chibi", self.consent, emotions=DEFAULT_SET_16[:10], count=10)

    def test_emotion_count_mismatch(self):
        with self.assertRaisesRegex(ValueError, "emotion count"):
            make_pack(self.scan, "chibi", self.consent, emotions=DEFAULT_SET_16[:8], count=16)

    def test_duplicate_emotion(self):
        with self.assertRaisesRegex(ValueError, "duplicate emotion"):
            make_pack(self.scan, "chibi", self.consent, emotions=["happy"] * 8, count=8, bubble_map={})

    def test_pack_8(self):
        p = make_pack(_scan(BECK_SELFIE), "pop", self.consent,
                      emotions=DEFAULT_SET_16[:8], count=8, bubble_map={"happy": "got_it"})
        self.assertEqual(p["count"], 8)
        self.assertEqual(p["style"], "pop")
        self.assertEqual(p["with_text"], 1)
        self.assertTrue(export_spec(p)["ready"])

    def test_chat_preview(self):
        prev = chat_preview(self.pack)
        self.assertEqual(prev["layout"], "chat_mock")
        self.assertEqual(prev["count"], 4)
        self.assertTrue(prev["items"][0]["text_th"])

    def test_share_card(self):
        s = share_card("น้องเจน", self.pack, self.export)
        self.assertIn("16 ใบ", s["headline_th"])
        self.assertEqual(s["count"], 16)
        self.assertTrue(s["export_ready"])
        self.assertEqual(s["layout"], "sticker_card")
        self.assertIn("STICKER", s["cta_th"])
        self.assertTrue(s["hook_th"].startswith("เซลฟี่เดียว"))

    def test_quota(self):
        self.assertEqual(quota(1, 1), {"allowed": 1, "left_after": 1, "paywall": False})
        self.assertEqual(quota(3, 1), {"allowed": 0, "left_after": 0, "paywall": True})
        self.assertEqual(quota(0, 5, pro=True)["paywall"], False)

    def test_safety_guard(self):
        self.assertEqual(safety_guard()["level"], "ok")
        self.assertEqual(safety_guard(consent_guard(**OTHER_CONSENT))["level"], "stop")
        self.assertIn("ใบหน้าของตนเอง", safety_guard()["message_th"])

    def test_style_library_8(self):
        lib = style_library()
        self.assertEqual(len(lib), 8)
        self.assertEqual(len({x["id"] for x in lib}), 8)

    def test_emotion_library_24(self):
        lib = emotion_library()
        self.assertEqual(len(lib), 24)
        self.assertEqual(lib[0]["key"], "happy")

    def test_custom_textmake_sticker(self):
        s = make_sticker("happy", "chibi", 370, 320, custom_text="สวัสดี")
        self.assertEqual(s["text_th"], "สวัสดี")
        self.assertEqual(s["bubble_id"], "custom")
        with self.assertRaises(ValueError):
            make_sticker("happy", "chibi", 370, 320, custom_text="ข้อความยาวมากจนใส่ไม่ได้อีกแล้ว")

    def test_default_bubble_first_eight(self):
        keys = [s["emotion"] for s in self.pack["stickers"][:8]]
        self.assertEqual(keys, DEFAULT_SET_16[:8])
        self.assertTrue(all(s["text_th"] for s in self.pack["stickers"][:8]))
        self.assertTrue(all(s["text_th"] is None for s in self.pack["stickers"][8:]))

    def test_export_count_fail(self):
        broken = dict(self.pack, count=10)
        ex = export_spec(broken)
        self.assertFalse(ex["ready"])
        self.assertFalse([c for c in ex["checks"] if c["key"] == "count"][0]["ok"])

    def test_watermark(self):
        self.assertIn("not a LINE product", self.pack["watermark"])
        self.assertIn("LINE", SAFETY_DISCLAIMER_TH)

    def test_beck_quality(self):
        self.assertEqual(_scan(BECK_SELFIE)["quality"]["score"], 85)

    def test_share_saved_fields(self):
        s = share_card("น้องเจน", self.pack, self.export)
        self.assertEqual(s["with_text"], 8)
        self.assertEqual(s["style"], "chibi")

    def test_line_spec_constants(self):
        self.assertEqual(LINE_SPEC["allowed_counts"], (8, 16, 24))
        self.assertEqual(len(DEFAULT_SET_16), 16)
        self.assertEqual(len(BUBBLES), 8)

if __name__ == "__main__":
    unittest.main()
