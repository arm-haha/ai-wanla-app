import unittest
from tripstitch import *
from fixtures import *

class T(unittest.TestCase):
    def setUp(self):
        self.st = stitch_places(KAO_SHOTS)
        self.plan = plan_days(self.st["places"], KAO["start_date"], KAO["nights"], KAO["pax"])
        self.budget = budget_split(self.st["places"], KAO["nights"], KAO["pax"], KAO["budget_thb"])

    # 1) Screenshot extract
    def test_kao_first_quality(self):
        q = extract_places(KAO_SHOTS[0])["quality"]
        self.assertEqual(q["score"], 90)
        self.assertTrue(q["ok"])
        self.assertEqual(q["tips_th"], [])

    def test_uncertain_low_conf(self):
        r = extract_places(KAO_SHOTS[4])
        self.assertEqual(r["uncertain"], ["จุดชมวิวไม่ชัด"])
        self.assertEqual(r["place_count"], 1)
        self.assertEqual(r["places"][0]["id"], "pl05")

    def test_quality_tips(self):
        q = extract_places(MUK_SHOTS[0])["quality"]
        self.assertEqual(q["score"], 44)
        self.assertFalse(q["ok"])
        self.assertGreaterEqual(len(q["tips_th"]), 3)

    def test_no_places(self):
        r = extract_places(EMPTY_SHOT)
        self.assertFalse(r["quality"]["ok"])
        self.assertEqual(r["place_count"], 0)
        self.assertIn("ไม่เจอชื่อสถานที่", " ".join(r["quality"]["tips_th"]))

    def test_bad_quality_input(self):
        with self.assertRaises(ValueError):
            scan_quality(1.2, 0, 0, 1)

    def test_unknown_type(self):
        sh = dict(KAO_SHOTS[0], detections=[{**P_BEAN, "type": "zoo"}])
        with self.assertRaises(ValueError):
            extract_places(sh)

    def test_pipeline(self):
        self.assertEqual(pipeline_steps(KAO_SHOTS[0]),
                         ["screen_detect", "ocr_name", "area_match", "dedupe", "day_plan", "budget"])
        st = pipeline_steps(MUK_SHOTS[0])
        self.assertIn("deglare", st)
        self.assertIn("recrop", st)

    # 2) Stitch
    def test_stitch_kao(self):
        self.assertEqual(self.st["place_count"], 6)
        self.assertEqual(self.st["areas"], ["doi_suthep", "mae_rim", "nimman", "old_city"])
        self.assertEqual(self.st["uncertain"], ["จุดชมวิวไม่ชัด"])
        self.assertEqual({p["id"] for p in self.st["places"]}, {"pl01", "pl02", "pl03", "pl04", "pl05", "pl06"})

    def test_stitch_dedupes(self):
        dup = stitch_places([KAO_SHOTS[0], KAO_SHOTS[0]])
        self.assertEqual(dup["place_count"], 1)

    # 3) Day-by-day route (wow)
    def test_kao_plan_shape(self):
        self.assertEqual((self.plan["days"], self.plan["nights"], self.plan["pax"]), (4, 3, 2))
        self.assertEqual([d["date"] for d in self.plan["itinerary"]],
                         ["2026-12-03", "2026-12-04", "2026-12-05", "2026-12-06"])

    def test_kao_day_areas(self):
        self.assertEqual([d["areas"] for d in self.plan["itinerary"]],
                         [["nimman"], ["old_city"], ["doi_suthep"], ["mae_rim"]])

    def test_kao_slots(self):
        d1 = [(s["slot"], s["name_th"]) for s in self.plan["itinerary"][0]["stops"]]
        self.assertEqual(d1, [("morning", "คาเฟ่ FictoBean"), ("afternoon", "ร้านข้าวซอย FictoSoi")])
        d2 = [s["slot"] for s in self.plan["itinerary"][1]["stops"]]
        self.assertEqual(d2, ["afternoon", "evening"])
        self.assertEqual(self.plan["itinerary"][2]["stops"][0]["name_th"], "วัดพระธาตุดอยสุเทพ")
        self.assertEqual(self.plan["itinerary"][3]["stops"][0]["name_th"], "คาเฟ่ FictoHill")

    def test_travel_times(self):
        self.assertEqual(self.plan["itinerary"][0]["total_travel_min"], 10)
        self.assertEqual(self.plan["itinerary"][1]["stops"][0]["travel_min"], 15)
        self.assertEqual(travel_min("nimman", "nimman"), 10)
        self.assertEqual(travel_min("nimman", "doi_suthep"), 40)
        self.assertEqual(travel_min("nowhere", "else"), 40)

    def test_plan_empty_and_nights(self):
        with self.assertRaises(ValueError):
            plan_days([], "2026-12-03", 3)
        with self.assertRaises(ValueError):
            plan_days(self.st["places"], "2026-12-03", 0)

    def test_closed_warning(self):
        plan = plan_days(self.st["places"], "2026-12-05", 3, 2)  # day 4 = Tuesday
        self.assertEqual(plan["itinerary"][3]["dow"], "tuesday")
        w = closed_warnings(plan, self.st["places"])
        self.assertEqual(len(w), 1)
        self.assertEqual(w[0]["name_th"], "คาเฟ่ FictoHill")
        self.assertEqual(closed_warnings(self.plan, self.st["places"]), [])

    def test_rain_plan(self):
        r = rain_plan(self.plan, self.st["places"])
        self.assertGreaterEqual(len(r["indoor_alts"]), 3)
        self.assertTrue(any("ฝน" in t for t in r["tips_th"]))

    # 4) Budget
    def test_kao_budget(self):
        b = self.budget
        self.assertEqual([l["thb"] for l in b["lines"]], [2700, 2400, 600, 100, 1000, 1000])
        self.assertEqual((b["planned_thb"], b["buffer_thb"], b["total_thb"], b["per_pax_thb"]), (6800, 1000, 7800, 3900))
        self.assertEqual(b["verdict"], "fit")

    def test_budget_verdicts(self):
        places = self.st["places"]
        self.assertEqual(budget_split(places, 3, 2, 12000)["verdict"], "under")
        self.assertEqual(budget_split(places, 3, 2, 8000)["verdict"], "fit")
        self.assertEqual(budget_split(places, 3, 2, 7200)["verdict"], "tight")
        self.assertEqual(budget_split(places, 3, 2, 4000)["verdict"], "over")

    def test_nina_over(self):
        b = budget_split(NINA_PLACES, 1, 1, 2500)
        self.assertEqual((b["planned_thb"], b["total_thb"], b["verdict"]), (2600, 2900, "over"))

    def test_custom_stay(self):
        b = budget_split(self.st["places"], 3, 2, 8000, stay_thb=0)
        self.assertEqual(b["lines"][0]["thb"], 0)
        self.assertEqual(b["planned_thb"], 4100)

    def test_bad_budget(self):
        with self.assertRaises(ValueError):
            budget_split(self.st["places"], 3, 0, 8000)

    # 5) Packing
    def test_kao_pack(self):
        pk = packing_list(3, KAO["climates"], [p["type"] for p in self.st["places"]])
        self.assertEqual(pk["days"], 4)
        self.assertEqual(pk["count"], 15)
        texts = " ".join(i["text_th"] for i in pk["items"])
        self.assertIn("เสื้อคลุมบาง", texts)
        self.assertIn("ชุดสุภาพ", texts)
        self.assertIn("ร่มพับ", texts)

    def test_hot_pack(self):
        pk = packing_list(1, ["hot"], ["cafe"])
        texts = " ".join(i["text_th"] for i in pk["items"])
        self.assertIn("ครีมกันแดด", texts)
        self.assertEqual(pk["days"], 2)

    def test_bad_climate(self):
        with self.assertRaises(ValueError):
            packing_list(2, ["snow"], ["cafe"])
        with self.assertRaises(ValueError):
            packing_list(0, ["hot"], ["cafe"])

    # 6) Share + quota + safety
    def test_share(self):
        s = share_card("ทริปพี่เก้า", "เชียงใหม่", self.plan, self.budget)
        self.assertTrue(s["offline"])
        self.assertIn("฿7,800", s["cta_th"])
        self.assertIn("วันที่ 1 2 จุด", s["days_th"])
        self.assertEqual(s["verdict"], "fit")

    def test_quota(self):
        self.assertEqual(quota(1, 1), {"allowed": 1, "left_after": 1, "paywall": False})
        self.assertEqual(quota(3, 1), {"allowed": 0, "left_after": 0, "paywall": True})
        self.assertEqual(quota(0, 5, pro=True)["paywall"], False)

    def test_safety_guard(self):
        self.assertEqual(safety_guard(True, 0)["level"], "ok")
        self.assertEqual(safety_guard(True, 1)["level"], "warn")
        self.assertEqual(safety_guard(False)["level"], "warn")
        self.assertIn("ไม่ใช่ข้อมูลเวลาเปิด-ปิด", safety_guard(True)["message_th"])

    def test_nina_plan_days(self):
        st = stitch_places(NINA_SHOTS)
        plan = plan_days(st["places"], NINA["start_date"], NINA["nights"], 1)
        self.assertEqual(plan["days"], 2)
        self.assertEqual(sum(d["stop_count"] for d in plan["itinerary"]), 3)


    def test_phu_budget_fit(self):
        b = budget_split(PHU_PLACES, 2, 4, 9000)
        self.assertEqual((b["planned_thb"], b["buffer_thb"], b["total_thb"], b["verdict"]), (7570, 1100, 8670, "fit"))

    def test_suthep_ticket(self):
        suthep = [p for p in self.st["places"] if p["id"] == "pl05"][0]
        self.assertEqual(suthep["ticket_thb"], 50)
        self.assertEqual(suthep["type"], "temple")

    def test_hill_closed_tuesday(self):
        hill = [p for p in self.st["places"] if p["id"] == "pl06"][0]
        self.assertEqual(hill["closed_dow"], [1])

    def test_stop_numbers(self):
        for d in self.plan["itinerary"]:
            self.assertEqual([s["n"] for s in d["stops"]], list(range(1, d["stop_count"] + 1)))

    def test_kao_dows(self):
        self.assertEqual([d["dow"] for d in self.plan["itinerary"]],
                         ["thursday", "friday", "saturday", "sunday"])

    def test_budget_zero(self):
        self.assertEqual(budget_split(self.st["places"], 3, 2, 0)["verdict"], "unknown")

    def test_share_hook(self):
        s = share_card("ทริปพี่เก้า", "เชียงใหม่", self.plan, self.budget)
        self.assertEqual(s["hook_th"], "แคปจอที่เที่ยวเก็บไว้ กลายเป็นทริปพร้อมเที่ยว")
        self.assertEqual(s["layout"], "trip_card")

    def test_stitch_nina(self):
        st = stitch_places(NINA_SHOTS)
        self.assertEqual(st["place_count"], 3)
        self.assertEqual(sorted(st["areas"]), ["silom", "thonglor"])

    def test_extract_bean_fields(self):
        r = extract_places(KAO_SHOTS[0])["places"][0]
        self.assertEqual(r["name_th"], "คาเฟ่ FictoBean")
        self.assertEqual((r["open_hour"], r["close_hour"], r["area"]), (8, 18, "nimman"))

    def test_pack_groups(self):
        pk = packing_list(3, KAO["climates"], [p["type"] for p in self.st["places"]])
        groups = {i["group"] for i in pk["items"]}
        self.assertEqual(groups, {"clothes", "weather", "activity", "essentials"})

    def test_warning_message(self):
        w = closed_warnings(plan_days(self.st["places"], "2026-12-05", 3, 2), self.st["places"])
        self.assertIn("ปิดวันนั้น", w[0]["message_th"])

    def test_empty_pipeline(self):
        self.assertEqual(pipeline_steps(EMPTY_SHOT)[0], "screen_detect")
        self.assertNotIn("deglare", pipeline_steps(EMPTY_SHOT))

    def test_safety_copy(self):
        self.assertIn("ห้ามแชร์ตำแหน่งบ้าน", safety_guard(True)["message_th"])

if __name__ == "__main__":
    unittest.main()
