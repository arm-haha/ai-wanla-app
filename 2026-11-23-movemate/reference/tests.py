import unittest
from movemate import *
from fixtures import *

def am_boxes():
    return [make_box(f"B{n:02d}", room, contents, fragile, photo) for n,room,contents,fragile,photo in AM_BOX_SPECS]

class T(unittest.TestCase):
    def setUp(self):
        self.boxes = am_boxes()
        self.stats = inventory_stats(self.boxes)
        self.cost = cost_estimate(10, "pickup", "bkk")

    def test_kitchen_progress(self):
        p = apply_checks(room_checklist("kitchen"), AM_PACKED["kitchen"])
        self.assertEqual((p["packed"], p["count"], p["progress"]), (4, 5, 80))
        self.assertFalse(p["items"][-1]["packed"])

    def test_bedroom_progress(self):
        p = apply_checks(room_checklist("bedroom"), AM_PACKED["bedroom"])
        self.assertEqual(p["progress"], 40)

    def test_empty_progress(self):
        p = apply_checks(room_checklist("bathroom"), [])
        self.assertEqual(p["progress"], 0)

    def test_unknown_room(self):
        with self.assertRaises(ValueError):
            room_checklist("garage")

    def test_library(self):
        self.assertEqual(len(ROOMS), 6)
        self.assertEqual(len(UTILITIES), 7)

    def test_box_charger(self):
        b = self.boxes[3]
        self.assertEqual(b["short_th"], "MM-B04")
        self.assertEqual(b["qr_payload"], "movemate://box/B04")
        self.assertTrue(b["on_device"])
        self.assertEqual(b["room_th"], "ห้องนอน")

    def test_fragile_label(self):
        self.assertIn("เปราะบาง", self.boxes[0]["label_th"])
        self.assertTrue(self.boxes[0]["fragile"])
        self.assertEqual(box_label(self.boxes[0])["fragile"], True)

    def test_bad_box(self):
        with self.assertRaises(ValueError):
            make_box("X1", "kitchen", ["จาน"])
        with self.assertRaises(ValueError):
            make_box("B01", "kitchen", [])
        with self.assertRaises(ValueError):
            make_box("B01", "garage", ["x"])

    def test_stats(self):
        self.assertEqual((self.stats["box_count"], self.stats["item_count"], self.stats["fragile_count"], self.stats["with_photo"]), (10, 26, 2, 8))
        self.assertEqual(inventory_stats([])["box_count"], 0)

    def test_find_charger(self):
        r = find_item("ที่ชาร์จ", self.boxes)
        self.assertEqual(r["count"], 1)
        self.assertEqual(r["hits"][0]["code"], "B04")
        self.assertEqual(r["hits"][0]["matched_th"], ["ที่ชาร์จมือถือ"])

    def test_find_dishes(self):
        r = find_item("จาน", self.boxes)
        self.assertEqual(r["hits"][0]["code"], "B01")
        self.assertTrue(r["hits"][0]["fragile"])

    def test_find_hdmi(self):
        self.assertEqual(find_item("HDMI", self.boxes)["hits"][0]["code"], "B08")

    def test_find_none_and_empty(self):
        self.assertEqual(find_item("เปียโน", self.boxes)["count"], 0)
        with self.assertRaises(ValueError):
            find_item("  ", self.boxes)

    def test_find_by_code(self):
        r = find_item("B07", self.boxes)
        self.assertEqual(r["count"], 1)
        self.assertEqual(r["hits"][0]["room"], "balcony")

    def test_timeline(self):
        tl = moving_timeline(MOVE_DATE, VAN_HOUR, ["kitchen", "bedroom"])
        self.assertEqual(tl["dow"], "saturday")
        self.assertEqual(tl["step_count"], 8)
        self.assertEqual(tl["steps"][0]["time"], "07:00")
        self.assertEqual(tl["steps"][3]["time"], "12:00")
        self.assertEqual([s["n"] for s in tl["steps"]], list(range(1, 9)))

    def test_timeline_bad(self):
        with self.assertRaises(ValueError):
            moving_timeline(MOVE_DATE, 12, [])
        with self.assertRaises(ValueError):
            moving_timeline(MOVE_DATE, 3, ["kitchen"])

    def test_utilities(self):
        u = utility_list(AM_UTILS)
        self.assertEqual(u["count"], 7)
        self.assertEqual(u["pending"], 4)
        self.assertEqual(u["missing"], ["internet", "parcel", "keys", "waste"])
        self.assertEqual(utility_list({})["pending"], 7)

    def test_cost_am(self):
        c = self.cost
        self.assertEqual((c["van_thb"], c["boxes_thb"], c["tape_thb"], c["total_thb"]), (2800, 150, 80, 3030))

    def test_cost_mult(self):
        self.assertEqual(cost_estimate(10, "pickup", "province")["van_thb"], 2400)
        self.assertEqual(cost_estimate(10, "small_truck")["total_thb"], 4430)
        self.assertEqual(cost_estimate(0, "pickup")["tape_thb"], 0)

    def test_bad_cost(self):
        with self.assertRaises(ValueError):
            cost_estimate(-1, "pickup")
        with self.assertRaises(ValueError):
            cost_estimate(2, "jet")

    def test_share(self):
        s = share_card("พี่แอม", MOVE_DATE, self.stats, self.cost)
        self.assertIn("10 กล่อง", s["headline_th"])
        self.assertIn("฿3,030", s["cta_th"])
        self.assertEqual(s["item_count"], 26)

    def test_quota(self):
        self.assertEqual(quota(1, 1), {"allowed": 1, "left_after": 1, "paywall": False})
        self.assertEqual(quota(3, 1), {"allowed": 0, "left_after": 0, "paywall": True})
        self.assertEqual(quota(0, 5, pro=True)["paywall"], False)

    def test_safety(self):
        self.assertEqual(safety_guard()["level"], "ok")
        self.assertEqual(safety_guard(True)["level"], "stop")
        self.assertEqual(safety_guard(False, False)["level"], "warn")
        self.assertIn("ไม่ใช่บริษัทขนย้าย", safety_guard()["message_th"])

    def test_label_sizes(self):
        self.assertEqual(box_label(self.boxes[3])["sizes"], ["70x50mm", "90x60mm"])

    def test_all_rooms_listed(self):
        for r in ROOMS:
            self.assertGreaterEqual(room_checklist(r)["count"], 3)

    def test_timeline_early_van(self):
        tl = moving_timeline("2026-12-05", 9, ["living"])
        self.assertEqual(tl["steps"][0]["time"], "06:00")  # max(6, 9-5)
        self.assertEqual(tl["dow"], "saturday")

    def test_misc_box(self):
        self.assertEqual(self.boxes[8]["room"], "misc")
        self.assertIsNone(self.boxes[8]["photo_id"])

    def test_cost_mid_truck(self):
        self.assertEqual(cost_estimate(10, "mid_truck")["van_thb"], 6500)

    def test_find_mm_prefix(self):
        r = find_item("MM-B04", self.boxes)
        self.assertEqual(r["count"], 1)

    def test_utility_done(self):
        done = [i["key"] for i in utility_list(AM_UTILS)["items"] if i["status"]=="done"]
        self.assertEqual(done, ["electricity", "water", "address"])

    def test_share_hook(self):
        self.assertEqual(share_card("พี่แอม", MOVE_DATE, self.stats, self.cost)["hook_th"], "ย้ายบ้านไม่ป่วน")

    def test_box_item_count(self):
        self.assertEqual(self.boxes[3]["item_count"], 4)

    def test_unknown_region(self):
        with self.assertRaises(ValueError):
            cost_estimate(2, "pickup", "mars")


    def test_rooms_in_stats(self):
        self.assertEqual(self.stats["rooms"], ["balcony", "bathroom", "bedroom", "kitchen", "living", "misc"])

    def test_find_case_code(self):
        self.assertEqual(find_item("b04", self.boxes)["count"], 1)

    def test_van_hour_bounds(self):
        moving_timeline(MOVE_DATE, 5, ["kitchen"])
        moving_timeline(MOVE_DATE, 18, ["kitchen"])
        with self.assertRaises(ValueError):
            moving_timeline(MOVE_DATE, 19, ["kitchen"])

    def test_empty_inventory_rooms(self):
        self.assertEqual(inventory_stats([])["rooms"], [])

    def test_bathroom_unpacked(self):
        self.assertEqual(apply_checks(room_checklist("bathroom"), AM_PACKED["bathroom"])["packed"], 0)

    def test_qr_unique(self):
        payloads=[b["qr_payload"] for b in self.boxes]
        self.assertEqual(len(payloads), len(set(payloads)))

    def test_share_layout(self):
        s=share_card("พี่แอม", MOVE_DATE, self.stats, self.cost)
        self.assertEqual(s["layout"], "move_card")
        self.assertEqual(s["box_count"], 10)

    def test_utility_hints(self):
        hints=" ".join(i["hint_th"] for i in utility_list({})["items"])
        self.assertIn("มิเตอร์", hints)

if __name__ == "__main__":
    unittest.main()
