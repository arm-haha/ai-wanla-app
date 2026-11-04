import unittest
from menumate import *
from fixtures import *

class T(unittest.TestCase):
    def test_rate(self):
        self.assertEqual(to_thb(980, RATE), 225)
        with self.assertRaises(ValueError): to_thb(1, 0)
    def test_allergy_avoid(self):
        self.assertEqual(flag_item(MENU[2], PREFS)["level"], AVOID)
    def test_spice_warn(self):
        self.assertEqual(flag_item(MENU[1], PREFS)["level"], WARN)
    def test_low_conf_warn(self):
        self.assertEqual(flag_item(MENU[6], PREFS)["level"], WARN)
    def test_safe(self):
        self.assertEqual(flag_item(MENU[0], PREFS)["level"], SAFE)
    def test_halal(self):
        self.assertEqual(flag_item(MENU[0], {"diets":["halal"]})["level"], AVOID)
    def test_vegetarian_drink_ok(self):
        self.assertEqual(flag_item(MENU[7], {"diets":["vegetarian"]})["level"], SAFE)
    def test_order(self):
        o = build_order(MENU, BUDGET, PARTY, PREFS)
        self.assertEqual(o["pick_ids"], ["m1","m4","s1","s2"])
        self.assertEqual(o["total_local"], 2830)
        self.assertEqual(o["left_local"], 170)
        self.assertTrue(o["mains_covered"])
    def test_order_excludes_unsafe(self):
        o = build_order(MENU, BUDGET, PARTY, PREFS)
        self.assertNotIn("m3", o["pick_ids"]); self.assertNotIn("m2", o["pick_ids"])
    def test_order_tight_budget(self):
        o = build_order(MENU, 1000, 2, PREFS)
        self.assertEqual(o["pick_ids"][0], "m1"); self.assertFalse(o["mains_covered"])
    def test_party_error(self):
        with self.assertRaises(ValueError): build_order(MENU, 1000, 0, PREFS)
    def test_point_card(self):
        o = build_order(MENU, BUDGET, PARTY, PREFS)
        c = point_card(MENU, o, "ja", "エビアレルギーがあります")
        self.assertEqual(c["header"], "こちらをお願いします")
        self.assertEqual(c["lines"][0]["line"], "豚骨ラーメン × 1個")
        self.assertEqual(len(c["lines"]), 4)
    def test_bill_extra(self):
        o = build_order(MENU, BUDGET, PARTY, PREFS)
        items = [i for i in MENU if i["id"] in o["pick_ids"]]
        b = bill_check(items, RECEIPT)
        self.assertEqual(b["extra_lines"], ["ライス"]); self.assertEqual(b["gap"], 200)
        self.assertFalse(b["ok"])
    def test_bill_ok(self):
        items = [MENU[0]]
        self.assertTrue(bill_check(items, [{"name":"豚骨ラーメン","amount":980}])["ok"])
    def test_bill_tax(self):
        b = bill_check([MENU[0]], [{"name":"豚骨ラーメン","amount":980}], tax_rate=0.1)
        self.assertEqual(b["expected_total"], 1078)
    def test_split(self):
        self.assertEqual(split_even(2830, 2, RATE), {"per_person_local":1415.0,"per_person_thb":325})
    def test_wrapped(self):
        w = trip_wrapped(MEALS, RATE)
        self.assertEqual((w["meals"], w["dishes_tried"], w["allergy_dodged"], w["spent_local"], w["spent_thb"], w["biggest_meal_city"]), (3,12,3,8930,2054,"Kyoto"))
if __name__ == "__main__": unittest.main()
