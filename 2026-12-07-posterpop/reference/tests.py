import unittest
from posterpop import *
from fixtures import *

class T(unittest.TestCase):
    def setUp(self):
        self.brand = brand_kit(JAY_BRAND["name_th"], JAY_BRAND["colors"])
        self.qr = qr_block(JAY_BRIEF["qr_url"])
        self.layout = auto_layout(
            JAY_BRIEF["template"], JAY_BRIEF["size_id"], JAY_BRIEF["title"], JAY_BRIEF["subtitle"],
            JAY_BRIEF["details"], JAY_BRIEF["date_th"], JAY_BRIEF["place_th"], JAY_BRIEF["cta_th"],
            self.brand, self.qr,
        )

    def test_jay_contrast(self):
        self.assertEqual(self.brand["contrast"]["ratio"], 11.09)
        self.assertTrue(self.brand["contrast"]["ok"])
        self.assertEqual(self.brand["contrast"]["level_th"], "ผ่าน AA")

    def test_jay_layout(self):
        self.assertEqual(self.layout["title_px"], 72)
        self.assertEqual((self.layout["w"], self.layout["h"]), (1080, 1350))
        self.assertTrue(self.layout["ok_contrast"])
        self.assertEqual(self.layout["headline_th"], "โปรศุกร์ 1 แถม 1")
        self.assertEqual(self.layout["template"], "sale")

    def test_title_sizes(self):
        self.assertEqual(title_size("โปร 1 แถม 1", 1080), 96)  # 11 chars
        self.assertEqual(title_size("โปรศุกร์ 1 แถม 1", 1080), 72)
        self.assertEqual(title_size("abcdefghijklmnopqrst", 1080), 72)
        self.assertEqual(title_size("abcdefghijklmnopqrstu", 1080), 56)
        self.assertEqual(title_size("x" * 33, 1080), 44)

    def test_bad_color(self):
        with self.assertRaises(ValueError):
            contrast_ratio("red", "#fff")
        with self.assertRaises(ValueError):
            brand_kit("x", ["#FFFFFF"])

    def test_contrast_fail(self):
        c = contrast_check("#F8F1E3", "#F8F1E3", "body")
        self.assertFalse(c["ok"])
        self.assertEqual(c["ratio"], 1.0)
        self.assertIn("ปรับสี", c["tip_th"])

    def test_large_vs_body(self):
        # mid grey on white may pass large but fail body
        c_lg = contrast_check("#8A8A8A", "#FFFFFF", "large")
        c_bd = contrast_check("#8A8A8A", "#FFFFFF", "body")
        self.assertTrue(c_lg["ok"])
        self.assertFalse(c_bd["ok"])

    def test_templates(self):
        self.assertEqual(len(TEMPLATES), 3)
        self.assertEqual(len(set(v["id"] for v in TEMPLATES.values())), 3)
        self.assertEqual(template_info("sale")["name_th"], "โปรลดราคา")
        self.assertIn("grid", template_info("menu")["zones"])
        with self.assertRaises(ValueError):
            template_info("wedding")

    def test_sizes(self):
        self.assertEqual(len(SIZES), 6)
        self.assertEqual(size_info("a4")["w"], 2480)
        self.assertEqual(size_info("ig_story")["h"], 1920)
        self.assertEqual(size_info("a3")["kind"], "print")
        with self.assertRaises(ValueError):
            size_info("tabloid")

    def test_qr(self):
        self.assertEqual(self.qr["size_px"], 220)
        self.assertEqual(self.qr["position"], "footer_right")
        q = qr_block("https://example.com", "footer_center")
        self.assertEqual(q["position"], "footer_center")
        with self.assertRaises(ValueError):
            qr_block("", "footer_right")
        with self.assertRaises(ValueError):
            qr_block("https://x.com", "hero")

    def test_menu_grid(self):
        g = menu_grid(JAY_MENU)
        self.assertEqual(g["count"], 4)
        self.assertEqual(g["cols"], 1)
        self.assertEqual(g["rows"][0]["price_label_th"], "฿85")
        wide = menu_grid(JAY_MENU + JAY_MENU + JAY_MENU[:1])
        self.assertEqual(wide["count"], 9)
        self.assertEqual(wide["cols"], 2)
        with self.assertRaises(ValueError):
            menu_grid([])
        with self.assertRaises(ValueError):
            menu_grid([{"name_th": "x", "price_thb": -1}])

    def test_event_layout(self):
        brand = brand_kit(MORN_BRAND["name_th"], MORN_BRAND["colors"])
        lay = auto_layout("event", "fb_post", MORN_BRIEF["title"], MORN_BRIEF["subtitle"],
                          MORN_BRIEF["details"], MORN_BRIEF["date_th"], MORN_BRIEF["place_th"],
                          MORN_BRIEF["cta_th"], brand, qr_block(MORN_BRIEF["qr_url"]))
        self.assertEqual(lay["template"], "event")
        self.assertTrue(lay["ok_contrast"])
        self.assertGreaterEqual(brand["contrast"]["ratio"], 4.5)

    def test_zones_sale(self):
        ids = [z["id"] for z in self.layout["zones"]]
        self.assertEqual(ids, TEMPLATES["sale"]["zones"])
        self.assertEqual(self.layout["zones"][0]["y"], 0.08)

    def test_pipeline(self):
        self.assertEqual(pipeline_steps("sale"),
                         ["brief", "template_sale", "brand_kit", "auto_layout", "qr", "export"])
        st = pipeline_steps("menu", has_qr=False, contrast_ok=False)
        self.assertIn("contrast_fix", st)
        self.assertNotIn("qr", st)
        with self.assertRaises(ValueError):
            pipeline_steps("flyer")

    def test_share(self):
        s = share_card("พี่เจ", "โปรศุกร์ 1 แถม 1", "sale", "ig_portrait")
        self.assertIn("POSTER", s["cta_th"])
        self.assertEqual(s["headline_th"], "โปรศุกร์ 1 แถม 1")

    def test_quota(self):
        self.assertEqual(quota(1, 1), {"allowed": 1, "left_after": 1, "paywall": False})
        self.assertEqual(quota(3, 1), {"allowed": 0, "left_after": 0, "paywall": True})
        self.assertEqual(quota(0, 5, pro=True)["paywall"], False)

    def test_safety(self):
        self.assertEqual(safety_guard(True)["level"], "ok")
        self.assertEqual(safety_guard(False)["level"], "stop")
        self.assertIn("ไม่ใช่โรงพิมพ์", safety_guard()["message_th"])

    def test_a4_layout(self):
        lay = auto_layout("sale", "a4", JAY_BRIEF["title"], JAY_BRIEF["subtitle"], JAY_BRIEF["details"],
                          JAY_BRIEF["date_th"], JAY_BRIEF["place_th"], JAY_BRIEF["cta_th"], self.brand, self.qr)
        self.assertEqual(lay["h"], 3508)
        self.assertEqual(lay["title_px"], 72)

    def test_brand_fonts(self):
        self.assertEqual(self.brand["heading_font"], "Kanit")
        self.assertEqual(self.brand["body_font"], "Sarabun")

    def test_menu_layout_zones(self):
        lay = auto_layout("menu", "a4", "เมนู Ficto Café", "", "", "", "", "", self.brand, None)
        self.assertEqual([z["id"] for z in lay["zones"]], TEMPLATES["menu"]["zones"])

    def test_hex_roundtrip(self):
        self.assertEqual(contrast_ratio("#000000", "#FFFFFF"), 21.0)
        self.assertEqual(contrast_ratio("#FFFFFF", "#000000"), 21.0)

    def test_people(self):
        self.assertEqual(JAY["shop_th"], "Ficto Café")
        self.assertEqual(JAY["name_th"], "พี่เจ")

    def test_disclaimer_on_layout(self):
        self.assertIn("สิทธิ์", self.layout["disclaimer_th"])

    def test_size_labels(self):
        self.assertIn("A4", size_info("a4")["label_th"])
        self.assertIn("สตอรี่", size_info("ig_story")["label_th"])

    def test_title_scale_small_canvas(self):
        self.assertEqual(title_size("โปร 1 แถม 1", 540), 48)

    def test_unique_size_ids(self):
        self.assertEqual(len(set(v["id"] for v in SIZES.values())), 6)

    def test_offer_zone_taller(self):
        offer = next(z for z in self.layout["zones"] if z["id"] == "offer")
        self.assertEqual(offer["h"], 0.14)

    def test_bad_auto_template(self):
        with self.assertRaises(ValueError):
            auto_layout("wedding", "a4", "x", "", "", "", "", "", self.brand)

    def test_share_sizes(self):
        s = share_card("พี่เจ", "โปรศุกร์ 1 แถม 1", "sale", "ig_portrait")
        self.assertEqual(s["layout"], "poster_preview")
        self.assertIn("1080x1350", s["sizes"])

    def test_jay_body_contrast_ok(self):
        self.assertTrue(self.layout["body_contrast"]["ok"])
        self.assertEqual(self.layout["body_contrast"]["ratio"], 11.09)

    def test_menu_first_item(self):
        self.assertEqual(JAY_MENU[0]["name_th"], "ลาเต้ Ficto")

    def test_qr_on_layout(self):
        self.assertEqual(self.layout["qr"]["url"], JAY_BRIEF["qr_url"])

    def test_fonts_default(self):
        self.assertEqual(FONTS["heading"], "Kanit")


    def test_event_title_size(self):
        self.assertEqual(title_size("ตลาดนัดยามเย็น", 1080), 72)

    def test_a3_kind(self):
        self.assertEqual(size_info("a3")["h"], 4961)

    def test_pipeline_event(self):
        self.assertIn("template_event", pipeline_steps("event"))

    def test_brand_tip(self):
        self.assertIn("ผ่าน AA", self.brand["tip_th"])

    def test_low_contrast_hex(self):
        self.assertEqual(contrast_check("#777777", "#888888", "large")["ok"], False)

    def test_menu_price_zero(self):
        g = menu_grid([{"name_th": "น้ำเปล่า", "price_thb": 0}])
        self.assertEqual(g["rows"][0]["price_label_th"], "฿0")

    def test_layout_fonts(self):
        self.assertEqual(self.layout["heading_font"], "Kanit")
        self.assertEqual(self.layout["body_font"], "Sarabun")

    def test_jay_brief_place(self):
        self.assertEqual(self.layout["place_th"], "ซอยสุขใจ 12")
        self.assertEqual(self.layout["cta_th"], "มาร้านได้เลย")

    def test_ig_square(self):
        self.assertEqual(size_info("ig_square")["w"], size_info("ig_square")["h"])


if __name__ == "__main__":
    unittest.main()
