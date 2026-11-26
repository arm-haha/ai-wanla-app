import unittest
from partypop import *
from fixtures import *

R = room_from_scan(SCAN)
B = budget_split(BUDGET, ADULTS, KIDS)
P = deco_plan(R, THEME, B["decor"], ADULTS + KIDS)
M = menu_plan("suki", ADULTS, KIDS, HOURS)
S = shopping_list(P, M, B)


class T(unittest.TestCase):
    def test_tables(self):
        self.assertEqual((len(THEMES), len(DECOR), len(MENU_STYLES), len(GAMES), len(FOOD)), (6, 12, 3, 10, 13))
        self.assertEqual(set(DRESS), set(THEMES))
        for k, (th, en, pal) in THEMES.items():
            self.assertEqual(len(pal), 6)
        self.assertAlmostEqual(sum(DECO_SHARE.values()), 1.0)
        for k, v in DECOR.items():
            self.assertTrue(v[5] == "*" or all(t in THEMES for t in v[5].split(",")), k)

    def test_room_area_recomputed(self):
        self.assertEqual((R["area_m2"], R["wall_m"], R["tables"]), (15.12, 4.2, 1))
        with self.assertRaises(ValueError):
            room_from_scan(dict(SCAN, width_m=0.5))

    def test_capacity_fixture_mingle(self):
        c = capacity(R, ADULTS, KIDS)
        self.assertEqual((c["seated_max"], c["standing_max"], c["status"], c["flag"]), (8, 17, "mingle", None))

    def test_capacity_levels(self):
        self.assertEqual(capacity(R, 6)["status"], "comfy")
        small = room_from_scan(SCAN_SMALL)
        c = capacity(small, 12)
        self.assertEqual((c["status"], c["flag"]), ("over", "over_capacity"))
        self.assertIn("เกินพื้นที่ 4 คน", c["tip_th"])

    def test_budget_split_sums(self):
        self.assertEqual((B["decor"], B["food"], B["drinks"], B["games_gifts"], B["reserve"]), (1000, 2000, 480, 320, 200))
        for tot in (999, 1500, 4000, 12345):
            b = budget_split(tot, 5, 2)
            self.assertEqual(sum(b[k] for k in DECO_SHARE), tot)

    def test_budget_per_head_and_potluck(self):
        self.assertEqual((B["per_head"], B["food_per_guest"], B["potluck"]), (333, 185.2, False))
        low = budget_split(1500, ADULTS, KIDS)
        self.assertTrue(low["potluck"]); self.assertIn("Potluck", low["tip_th"])
        with self.assertRaises(ValueError):
            budget_split(0, 3)

    def test_deco_fits_budget(self):
        self.assertEqual((P["spent"], P["left"]), (950, 50))
        self.assertLessEqual(P["spent"], P["budget"])
        self.assertEqual([i["key"] for i in P["items"]], ["garland", "balloons", "lights", "backdrop", "number_balloons", "tablecloth"])
        self.assertEqual(P["skipped"], ["hats", "props", "led_candles"])

    def test_deco_quantities(self):
        q = {i["key"]: i["packs"] for i in P["items"]}
        self.assertEqual((q["garland"], q["balloons"], q["lights"]), (3, 2, 2))   # 4.2 m wall, 15.12 m², 7.8 m of lights
        self.assertTrue(all(i["no_nails"] for i in P["items"]))
        self.assertEqual(sum(i["cost"] for i in P["items"]), P["spent"])

    def test_deco_theme_specific(self):
        xm = deco_plan(R, "cozy_xmas", 5000, 12)
        keys = [i["key"] for i in xm["items"]]
        self.assertIn("mini_tree", keys); self.assertNotIn("number_balloons", keys); self.assertNotIn("disco_ball", keys)
        self.assertIn("disco_ball", [i["key"] for i in deco_plan(R, "neon_disco", 5000, 12)["items"]])
        self.assertIn("paper_lanterns", [i["key"] for i in deco_plan(R, "thai_fair", 5000, 12)["items"]])
        with self.assertRaises(ValueError):
            deco_plan(R, "galaxy", 1000, 5)

    def test_deco_zero_budget(self):
        z = deco_plan(R, THEME, 0, 12)
        self.assertEqual((z["items"], z["spent"]), ([], 0))

    def test_render_prompt_guard(self):
        rp = render_prompt(R, P)
        self.assertTrue(rp["keep_layout"])
        for f in ("text", "faces", "logos", "brands", "fireworks indoors"):
            self.assertIn(f, rp["forbid"])
        self.assertIn("ธงราว", rp["items_th"])

    def test_menu_fixture(self):
        self.assertEqual((M["guest_eq"], M["total"]), (10.8, 1882))
        it = {i["key"]: i for i in M["items"]}
        self.assertEqual((it["meat"]["buy_qty"], it["ice"]["buy_qty"], it["dessert"]["packs"], it["water"]["buy_qty"]), (2.0, 9.0, 11, 12.0))

    def test_menu_buy_covers_need(self):
        for st in MENU_STYLES:
            for a, k, h in ((9, 3, 5.5), (20, 0, 4), (4, 4, 3)):
                for i in menu_plan(st, a, k, h)["items"]:
                    self.assertGreaterEqual(i["buy_qty"] + 1e-9, i["need"], (st, i["key"]))

    def test_menu_scales_with_hours_and_kids(self):
        self.assertLess(menu_plan("suki", 9, 0, 3)["total"], menu_plan("suki", 9, 0, 8)["total"])
        self.assertLess(menu_plan("buffet", 6, 6)["guest_eq"], menu_plan("buffet", 12, 0)["guest_eq"])
        with self.assertRaises(ValueError):
            menu_plan("bbq", 5)
        with self.assertRaises(ValueError):
            menu_plan("suki", 5, 0, 20)

    def test_menu_allergy_flag(self):
        m = menu_plan("suki", 5, 0, 4, ["กุ้ง", "ถั่ว", "กุ้ง"])
        self.assertEqual((m["allergy_labels"], m["flag"]), (["กุ้ง", "ถั่ว"], "food_allergy"))
        self.assertIsNone(M["flag"])

    def test_shopping_list_totals(self):
        self.assertEqual((S["total"], S["fits"], S["over_by"]), (2832, True, 0))
        self.assertEqual(S["total"], P["spent"] + M["total"])
        self.assertEqual(sum(x["cost"] for x in S["sections"]), S["total"])
        self.assertEqual(len(S["rows"]), len(P["items"]) + len(M["items"]))
        self.assertFalse(any(r["checked"] for r in S["rows"]))

    def test_shopping_over_budget(self):
        b = budget_split(1800, ADULTS, KIDS)
        s = shopping_list(deco_plan(R, THEME, b["decor"], 12), M, b)
        self.assertFalse(s["fits"]); self.assertGreater(s["over_by"], 0)

    def test_trim_menu(self):
        self.assertEqual(trim_menu("suki", ADULTS, KIDS, HOURS, 2480), {"style": "suki", "total": 1882, "potluck_dishes": 0, "changed": False})
        t = trim_menu("suki", ADULTS, KIDS, HOURS, 1500)
        self.assertEqual((t["style"], t["changed"]), ("buffet", True))
        t2 = trim_menu("suki", ADULTS, KIDS, HOURS, 800)
        self.assertEqual((t2["style"], t2["potluck_dishes"]), ("suki", 8))

    def test_timeline_new_year(self):
        tl = timeline(START, END, alcohol=True)
        keys = [t["key"] for t in tl["tasks"]]
        self.assertEqual(keys[0], "invite"); self.assertEqual(keys[-1], "home")
        at = {t["key"]: t["at"] for t in tl["tasks"]}
        self.assertEqual((at["invite"], at["countdown"], at["gift_swap"], at["decorate"]), ("2026-12-24T19:00", "2026-12-31T23:59", "2027-01-01T00:10", "2026-12-30T19:00"))
        self.assertEqual(tl["flag"], "noise_late")
        self.assertIn("ไม่ดื่มแล้วขับ", tl["tasks"][-1]["text_th"])
        self.assertEqual([t["at"] for t in tl["tasks"]], sorted(t["at"] for t in tl["tasks"]))

    def test_timeline_office_daytime(self):
        tl = timeline("2026-12-26T17:00", "2026-12-26T21:00")
        keys = [t["key"] for t in tl["tasks"]]
        self.assertNotIn("countdown", keys); self.assertIn("gift_swap", keys)
        self.assertIsNone(tl["flag"]); self.assertNotIn("ไม่ดื่มแล้วขับ", tl["tasks"][-1]["text_th"])
        with self.assertRaises(ValueError):
            timeline(END, START)

    def test_games_family_with_kids(self):
        g = game_plan(12, "family", 3, 60)
        self.assertLessEqual(g["minutes"], 60); self.assertEqual(g["minutes"], 55)
        self.assertTrue(all(x["kid_ok"] for x in g["games"]))
        self.assertFalse(g["drinking_games"])

    def test_games_office(self):
        g = game_plan(30, "office", 0, 60)
        keys = [x["key"] for x in g["games"]]
        self.assertNotIn("musical_chairs", keys); self.assertNotIn("pass_parcel", keys)
        self.assertTrue(all(GAME[k][3] <= 30 <= GAME[k][4] for k in keys))
        with self.assertRaises(ValueError):
            game_plan(10, "casino")

    def test_gift_swap_valid(self):
        gs = gift_swap(GUESTS, 2027, 300, COUPLES)
        givers = [p["giver"] for p in gs["pairs"]]; recv = [p["receiver"] for p in gs["pairs"]]
        self.assertEqual(sorted(givers), sorted(GUESTS)); self.assertEqual(sorted(recv), sorted(GUESTS))
        for p in gs["pairs"]:
            self.assertNotEqual(p["giver"], p["receiver"])
            self.assertNotIn(frozenset((p["giver"], p["receiver"])), {frozenset(c) for c in COUPLES})
            self.assertRegex(p["code"], "^[0-9A-F]{4}$")

    def test_gift_swap_deterministic(self):
        self.assertEqual(gift_swap(GUESTS, 2027, 300, COUPLES), gift_swap(GUESTS, 2027, 300, COUPLES))
        self.assertNotEqual(gift_swap(GUESTS, 1)["pairs"], gift_swap(GUESTS, 2)["pairs"])

    def test_gift_swap_errors(self):
        with self.assertRaises(ValueError):
            gift_swap(["a", "b"], 1)
        with self.assertRaises(ValueError):
            gift_swap(["a", "a", "b"], 1)
        with self.assertRaises(ValueError):
            gift_swap(["a", "b", "c"], 1, exclude=[("a", "b"), ("b", "c")])   # impossible

    def test_invite_public_hides_address(self):
        iv = invite("แพร", START, THEME, "คอนโดริมน้ำ นนทบุรี", "ห้อง 1205")
        self.assertEqual((iv["date_th"], iv["time_th"], iv["rsvp_by"], iv["address_th"], iv["address_hidden"]),
                         ("31 ธ.ค. 2569", "19:00 น.", "2026-12-28", None, True))
        self.assertEqual(invite("แพร", START, THEME, "x", "ห้อง 1205", public=False)["address_th"], "ห้อง 1205")

    def test_cost_split(self):
        c = cost_split(S["total"], ADULTS, KIDS, P["spent"])
        self.assertEqual((c["each"], c["collected"], c["extra"], c["kids_free"]), (210, 1890, 8, 3))
        self.assertGreaterEqual(c["collected"], c["total"] - c["host_pays"])
        with self.assertRaises(ValueError):
            cost_split(100, 0)

    def test_countdown(self):
        self.assertEqual(countdown("2026-12-25"), {"date": "2026-12-25", "days_to_new_year": 7, "be_year": 2570, "weekday_th": "วันศุกร์"})
        self.assertEqual(countdown("2026-12-31")["days_to_new_year"], 1)

    def test_party_flags(self):
        self.assertEqual(party_flags(kids=3, alcohol=True, driving_guests=2, end_after_midnight=True),
                         ["alcohol_minor", "drink_drive", "noise_late"])
        self.assertEqual(party_flags(), [])
        self.assertEqual(party_flags(fire_items=["sparkler"], kids_under3=1), ["indoor_fire", "small_kids_balloons"])

    def test_guard_levels(self):
        self.assertTrue(safety_guard("alcohol_minor")["block"])
        self.assertFalse(safety_guard("indoor_fire")["block"])
        self.assertEqual(safety_guard()["level"], "ok")
        self.assertIn("LED", safety_guard("indoor_fire")["message_th"])

    def test_privacy_check(self):
        self.assertEqual(privacy_check()["level"], "ok")
        self.assertEqual(privacy_check(["alcohol_minor"])["allowed"], False)
        k = privacy_check([], 11)
        self.assertEqual((k["level"], k["share_allowed"]), ("warn", False))
        self.assertTrue(privacy_check([], 11, True)["share_allowed"])

    def test_share_card(self):
        c = share_card("before_after")
        self.assertTrue(c["faces_blurred"] and c["address_hidden"]); self.assertEqual(c["watermark"], WATERMARK)
        with self.assertRaises(ValueError):
            share_card("story")

    def test_reel_plan(self):
        for sec in (15, 20, 24, 30):
            r = reel_plan(sec)
            self.assertEqual(r["shots"][-1]["end"], sec); self.assertEqual(r["shots"][0]["start"], 0)
            for a, b in zip(r["shots"], r["shots"][1:]):
                self.assertEqual(a["end"], b["start"])
        self.assertIn("PARTY", reel_plan()["shots"][-1]["caption_th"])
        with self.assertRaises(ValueError):
            reel_plan(40)

    def test_quota(self):
        self.assertEqual(quota(2), {"plan": "free", "renders_per_day": 3, "used": 2, "left": 1, "blocked": False})
        self.assertTrue(quota(3)["blocked"]); self.assertFalse(quota(3, "plus")["blocked"])

    def test_no_shaming_or_brands_in_text(self):
        txt = " ".join(str(v) for v in list(DECOR.values()) + list(FOOD.values()) + GAMES + list(GUARD.values()))
        for bad in ("เบียร์", "เหล้า", "drinking game", "กินเหล้า"):
            self.assertNotIn(bad, txt)


if __name__ == "__main__":
    unittest.main(verbosity=1)
