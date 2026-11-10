import unittest
from sellsnap import *
from fixtures import *
from fixtures import _shot, _d, INVENTORY
# helpers _shot, _d, TODAY are in fixtures

class T(unittest.TestCase):
    def setUp(self):
        self.item = parse_item(BOSS_SHOT)
        self.cond = condition_grade(BOSS_SHOT)
        self.price = price_range(self.item, self.cond)
        self.post = listing(self.item, self.cond, self.price, extra_note="มารับเองแถวลาดพร้าว")

    def test_boss_quality(self):
        self.assertEqual(self.item["quality"]["score"], 90)
        self.assertTrue(self.item["ok"])
        self.assertEqual(self.item["quality"]["tips_th"], [])

    def test_boss_item(self):
        self.assertEqual(self.item["category"], "lamp")
        self.assertEqual(self.item["item_th"], "โคมไฟตั้งโต๊ะ")
        self.assertEqual(self.item["color_th"], "ครีม")
        self.assertIn("โคมไฟตั้งโต๊ะ", self.item["message_th"])

    def test_boss_condition(self):
        self.assertEqual((self.cond["condition"], self.cond["grade"]), ("good", "B"))
        self.assertEqual(self.cond["name_th"], "สภาพดี")

    def test_boss_price(self):
        self.assertEqual((self.price["min_thb"], self.price["max_thb"], self.price["mid_thb"]), (450, 750, 600))
        self.assertIn("450", self.price["headline_th"])
        self.assertIn("750", self.price["headline_th"])
        self.assertIn("ค่าตัวอย่าง", self.price["disclaimer_th"])

    def test_boss_listing(self):
        self.assertEqual(self.post["title_th"], "โคมไฟตั้งโต๊ะ สีครีม สภาพดี")
        self.assertIn("รอยขีดเล็กที่ฐาน", self.post["description_th"])
        self.assertIn("ลาดพร้าว", self.post["description_th"])
        self.assertNotIn("สภาพสภาพ", self.post["description_th"])
        self.assertEqual(self.post["ask_thb"], 600)
        self.assertEqual(self.post["grade"], "B")

    def test_photo_tips_boss(self):
        t = photo_tips(BOSS_SHOT, has_defect_shot=False, has_scale_shot=False, n_angles=1)
        self.assertEqual(t["count"], 3)
        self.assertIn("need_defect", t["keys"])
        self.assertIn("need_scale", t["keys"])
        self.assertIn("need_all", t["keys"])

    def test_photo_tips_complete(self):
        t = photo_tips(BOSS_SHOT, has_defect_shot=True, has_scale_shot=True, n_angles=3)
        self.assertEqual(t["count"], 0)
        self.assertIn("รูปครบ", t["headline_th"])

    def test_replies(self):
        r = reply_templates(self.price)
        self.assertEqual(r["count"], 5)
        self.assertEqual(r["ask_thb"], 570)
        self.assertIn("570", r["templates"][0]["text_th"])
        keys = [t["key"] for t in r["templates"]]
        self.assertEqual(keys, ["bargain", "meetup", "reserved", "sold", "scam_guard"])

    def test_reply_subset(self):
        r = reply_templates(self.price, kinds=["sold", "meetup"])
        self.assertEqual(r["count"], 2)
        self.assertEqual(r["templates"][0]["key"], "sold")

    def test_unknown_template(self):
        with self.assertRaisesRegex(ValueError, "unknown template"):
            reply_templates(self.price, kinds=["insult"])

    def test_nid_price(self):
        item, cond = parse_item(NID_SHOT), condition_grade(NID_SHOT)
        p = price_range(item, cond)
        self.assertEqual((p["min_thb"], p["max_thb"], p["mid_thb"]), (200, 400, 300))
        self.assertEqual(cond["grade"], "C")

    def test_som_like_new(self):
        item, cond = parse_item(SOM_SHOT), condition_grade(SOM_SHOT)
        p = price_range(item, cond)
        self.assertEqual(cond["condition"], "like_new")
        self.assertEqual((p["min_thb"], p["max_thb"]), (80, 250))

    def test_wear_inference(self):
        c = condition_grade(WEAR_SHOT)
        self.assertEqual((c["condition"], c["grade"]), ("poor", "D"))

    def test_wear_boundaries(self):
        def shot(w):
            return {"id": "s99", "px_w": 1, "px_h": 1, "glare": 0, "blur": 0, "crop": 0,
                    "detections": [{"key": "wear", "value": w, "confidence": 0.9}]}
        self.assertEqual(condition_grade(shot(0.15))["condition"], "like_new")
        self.assertEqual(condition_grade(shot(0.16))["condition"], "good")
        self.assertEqual(condition_grade(shot(0.40))["condition"], "good")
        self.assertEqual(condition_grade(shot(0.41))["condition"], "fair")
        self.assertEqual(condition_grade(shot(0.65))["condition"], "fair")
        self.assertEqual(condition_grade(shot(0.66))["condition"], "poor")
        self.assertEqual(condition_grade(shot(0.85))["condition"], "poor")
        self.assertEqual(condition_grade(shot(0.86))["condition"], "for_parts")

    def test_missing_condition(self):
        sh = _shot("s08", 0.1, 0.1, 0.1, [_d("category", "lamp", 0.9)])
        c = condition_grade(sh)
        self.assertFalse(c["ok"])

    def test_bad_quality(self):
        q = parse_item(BAD_SHOT)["quality"]
        self.assertEqual(q["score"], 43)
        self.assertFalse(q["ok"])
        self.assertGreaterEqual(len(q["tips_th"]), 3)

    def test_empty_and_lowconf(self):
        e = parse_item(EMPTY_SHOT)
        self.assertFalse(e["ok"])
        self.assertEqual(e["quality"]["score"], 54)
        self.assertIn("ยังไม่เจอสินค้า", " ".join(e["quality"]["tips_th"]))
        low = parse_item(LOWCONF_SHOT)
        self.assertFalse(low["ok"])
        self.assertIsNone(low["category"])
        self.assertEqual(low["item_th"], "โคมไฟตั้งโต๊ะ")

    def test_bad_input(self):
        with self.assertRaises(ValueError):
            scan_quality(1.2, 0, 0, 1)

    def test_price_requires_ok(self):
        with self.assertRaises(ValueError):
            price_range(parse_item(EMPTY_SHOT), self.cond)
        with self.assertRaises(ValueError):
            listing(parse_item(EMPTY_SHOT), self.cond, self.price)

    def test_sold_log_sell(self):
        inv = [dict(r) for r in INVENTORY]
        log = sold_log(inv, "sell", "l01", sold_thb=550, date="2026-11-26")
        self.assertEqual(log["sold_count"], 2)
        self.assertEqual(log["total_sold_thb"], 630)
        self.assertEqual(log["open_count"], 1)
        self.assertIn("2 ชิ้น", log["headline_th"])

    def test_sold_log_reserve(self):
        inv = [dict(r) for r in INVENTORY]
        log = sold_log(inv, "reserve", "l02")
        self.assertEqual(log["reserved_count"], 1)
        self.assertEqual(log["open_count"], 1)

    def test_sold_log_relist(self):
        inv = [dict(r) for r in INVENTORY]
        log = sold_log(inv, "relist", "l03")
        self.assertEqual(log["sold_count"], 0)
        self.assertEqual(log["open_count"], 3)

    def test_sold_log_errors(self):
        inv = [dict(r) for r in INVENTORY]
        with self.assertRaisesRegex(ValueError, "unknown listing"):
            sold_log(inv, "sell", "l99", sold_thb=1)
        with self.assertRaisesRegex(ValueError, "already sold"):
            sold_log(inv, "reserve", "l03")
        with self.assertRaisesRegex(ValueError, "sold_thb"):
            sold_log(inv, "sell", "l01")
        with self.assertRaisesRegex(ValueError, "unknown action"):
            sold_log(inv, "delete", "l01")

    def test_share(self):
        s = share_card("พี่บอส", self.post, self.price)
        self.assertEqual(s["ask_thb"], 600)
        self.assertEqual(s["grade"], "B")
        self.assertIn("SELL", s["cta_th"])
        self.assertTrue(s["hook_th"].startswith("ถ่ายของมือสอง"))
        self.assertEqual(s["layout"], "listing_card")

    def test_quota(self):
        self.assertEqual(quota(1, 1), {"allowed": 1, "left_after": 1, "paywall": False})
        self.assertEqual(quota(3, 1), {"allowed": 0, "left_after": 0, "paywall": True})
        self.assertEqual(quota(0, 5, pro=True)["paywall"], False)

    def test_safety(self):
        self.assertEqual(safety_guard()["level"], "ok")
        self.assertEqual(safety_guard(True, False)["level"], "stop")
        self.assertEqual(safety_guard(True, True)["level"], "warn")
        self.assertEqual(safety_guard(False, False)["level"], "warn")
        self.assertIn("ไม่ใช่ตลาดกลาง", safety_guard()["message_th"])

    def test_title_trim(self):
        item = dict(self.item, item_th="โคมไฟตั้งโต๊ะวินเทจลายดอกไม้พร้อมโคมแก้วฝ้า", color_th="ครีมอ่อนมาก")
        t = listing(item, self.cond, self.price)["title_th"]
        self.assertLessEqual(len(t), 60)
        self.assertTrue(t.endswith("…"))

    def test_nid_quality(self):
        self.assertEqual(parse_item(NID_SHOT)["quality"]["score"], 86)

    def test_som_quality(self):
        self.assertEqual(parse_item(SOM_SHOT)["quality"]["score"], 90)

    def test_categories(self):
        self.assertEqual(len(CATEGORIES), 9)
        self.assertEqual(len(CONDITIONS), 5)
        self.assertEqual(len(PRICES), 9 * 5)

    def test_bad_photo_tips_include_quality(self):
        t = photo_tips(BAD_SHOT, has_defect_shot=True, has_scale_shot=True, n_angles=3)
        self.assertIn("glare", t["keys"])
        self.assertIn("blur", t["keys"])
        self.assertIn("crop", t["keys"])

    def test_library_ids_unique(self):
        ids = [c["id"] for c in CATEGORIES.values()]
        self.assertEqual(len(ids), len(set(ids)))

    def test_price_chair_good(self):
        item = dict(self.item, ok=True, category="chair")
        cond = dict(self.cond, ok=True, condition="good", grade="B")
        self.assertEqual(price_range(item, cond)["mid_thb"], 700)

    def test_watermark(self):
        self.assertIn("not a live price", WATERMARK)

    def test_listing_requires_condition(self):
        with self.assertRaises(ValueError):
            listing(self.item, {"ok": False}, self.price)

    def test_empty_tips_no_item(self):
        t = photo_tips(EMPTY_SHOT, has_defect_shot=True, has_scale_shot=True, n_angles=3)
        self.assertIn("no_item", t["keys"])

    def test_electronics_fair(self):
        item = dict(self.item, ok=True, category="electronics")
        cond = dict(self.cond, ok=True, condition="fair", grade="C")
        self.assertEqual(price_range(item, cond)["mid_thb"], 600)

    def test_for_parts_lamp(self):
        item = dict(self.item, ok=True, category="lamp")
        cond = {"ok": True, "condition": "for_parts", "grade": "E", "name_th": "ขายซาก/อะไหล่"}
        p = price_range(item, cond)
        self.assertEqual((p["min_thb"], p["max_thb"]), (50, 120))

    def test_share_range(self):
        s = share_card("พี่บอส", self.post, self.price)
        self.assertEqual((s["min_thb"], s["max_thb"]), (450, 750))

    def test_inventory_not_mutated_on_copy(self):
        # sold_log should not change other rows' identity incorrectly
        inv = [dict(r) for r in INVENTORY]
        sold_log(inv, "reserve", "l01")
        self.assertEqual(INVENTORY[0]["status"], "for_sale")

    def test_nid_listing_title(self):
        item, cond = parse_item(NID_SHOT), condition_grade(NID_SHOT)
        post = listing(item, cond, price_range(item, cond))
        self.assertEqual(post["title_th"], "กระเป๋าผ้า สีกรม ใช้งานได้ มีรอย")
        self.assertEqual(post["ask_thb"], 300)

if __name__ == "__main__":
    unittest.main()
