import unittest
from dreamboard import *
from fixtures import *

P = [progress(g, LOGS[g["id"]], MID) for g in GOALS]


class T(unittest.TestCase):
    def test_tables(self):
        self.assertEqual((len(CATEGORIES), len(UNITS), len(THEMES), len(DEVICES), len(WORDS)), (10, 8, 6, 3, 10))
        self.assertEqual(set(WORDS), set(CAT_KEYS))
        for k, (name, pal) in THEMES.items():
            self.assertEqual(len(pal), 6)

    def test_smart_good_goal(self):
        self.assertEqual(smart_check(G_MONEY, 25000), {"score": 100, "specific": True, "measurable": True, "achievable": True, "relevant": True,
                                                       "timed": True, "per_month": 5000.0, "flag": None, "tips_th": []})

    def test_smart_all_fixture_goals_pass(self):
        self.assertEqual([smart_check(g, USER["monthly_income"])["score"] for g in GOALS], [100] * 5)

    def test_smart_vague(self):
        r = smart_check(G_VAGUE)
        self.assertEqual((r["score"], r["specific"], r["measurable"], r["timed"], len(r["tips_th"])), (20, False, False, False, 3))
        self.assertIn("อยากรวย", r["tips_th"][0])

    def test_crash_diet_flagged(self):
        r = smart_check(G_CRASH)
        self.assertEqual((r["score"], r["achievable"], r["flag"]), (80, False, "extreme_diet"))
        self.assertTrue(safety_guard(r["flag"])["block"])

    def test_safe_replan(self):
        g = safe_replan(G_CRASH)
        self.assertEqual((g["deadline"], g["target_value"]), ("2027-05-21", 10))
        self.assertTrue(smart_check(g)["achievable"])
        with self.assertRaises(ValueError):
            safe_replan(G_MONEY)

    def test_saving_vs_income(self):
        self.assertFalse(smart_check(G_HUGE, 25000)["achievable"])
        self.assertTrue(smart_check(G_HUGE, 60000)["achievable"])
        self.assertTrue(smart_check(G_HUGE)["achievable"])      # no income given → not judged

    def test_months_between(self):
        self.assertEqual((months_between(Y0, Y1), months_between(Y0, "2027-06-30"), months_between("2026-12-24", "2027-01-05")), (12, 6, 2))
        with self.assertRaises(ValueError):
            months_between(Y1, Y0)

    def test_roadmap_money_ramp(self):
        r = roadmap(G_MONEY)["milestones"]
        self.assertEqual(len(r), 12)
        self.assertEqual([m["target"] for m in r[:3]], [3500, 7300, 11300])
        self.assertEqual((r[-1]["target"], r[-1]["pct"], r[0]["label_th"], r[-1]["label_th"]), (60000, 100, "ม.ค. 70", "ธ.ค. 70"))
        deltas = [m["delta"] for m in r]
        self.assertLess(deltas[0], deltas[-1])                     # starts small, grows later

    def test_roadmap_monotonic_and_sums(self):
        for g in GOALS:
            r = roadmap(g)["milestones"]
            t = [m["target"] for m in r]
            self.assertEqual(t, sorted(t))
            self.assertAlmostEqual(sum(m["delta"] for m in r), delta(g), places=2)

    def test_roadmap_steps(self):
        self.assertEqual([m["target"] for m in roadmap(G_WEIGHT)["milestones"]], [0.5, 1.5, 2.5, 3.5, 4.5, 6])
        self.assertEqual([m["target"] for m in roadmap(G_BOOK)["milestones"]][:6], [1, 3, 5, 6, 8, 10])

    def test_weekly_habit_money(self):
        self.assertEqual(weekly_habit(G_MONEY), {"goal_id": "g1", "weeks": 53, "per_week": 1150, "unit": "THB",
                                                 "text_th": "เก็บสัปดาห์ละ 1,150 บาท (วันละ ~165 บาท)"})

    def test_weekly_habit_other_units(self):
        self.assertEqual(weekly_habit(G_WEIGHT)["text_th"], "ลดสัปดาห์ละ 0.3 กก. ≈ กินน้อยลง/ขยับมากขึ้น ~350 kcal ต่อวัน")
        self.assertEqual(weekly_habit(G_BOOK)["text_th"], "อ่านวันละ ~17 หน้า (เล่มละ ~250 หน้า)")
        self.assertEqual(weekly_habit(G_RUN)["per_week"], 6)
        self.assertEqual(weekly_habit(G_TRIP)["text_th"], "วางแผนทริปทุก ~13 สัปดาห์")

    def test_weekly_habit_never_unsafe(self):
        self.assertLessEqual(weekly_habit(safe_replan(G_CRASH))["per_week"], SAFE_KG_PER_WEEK)

    def test_layout_iphone_five(self):
        L = layout(GOALS)
        self.assertEqual((L["w"], L["h"], L["safe_top"], L["safe_bottom"], len(L["tiles"])), (1179, 2556, 817, 2300, 5))
        self.assertEqual(L["tiles"][0], {"goal_id": "g1", "x": 48, "y": 865, "w": 525, "h": 441, "color": "#FF9A62", "category": "money"})
        self.assertEqual(L["tiles"][4]["w"], 1083)                 # odd last tile spans full width

    def test_layout_never_under_clock(self):
        for dev in DEVICES:
            for n in range(1, 7):
                L = layout((GOALS * 2)[:n], "midnight", dev)
                for t in L["tiles"]:
                    self.assertGreaterEqual(t["y"], L["safe_top"])
                    self.assertLessEqual(t["y"] + t["h"], L["safe_bottom"])
                    self.assertLessEqual(t["x"] + t["w"], L["w"])

    def test_layout_no_overlap(self):
        for dev in DEVICES:
            ts = layout((GOALS * 2)[:6], "pastel", dev)["tiles"]
            for i in range(len(ts)):
                for j in range(i + 1, len(ts)):
                    self.assertFalse(overlaps(ts[i], ts[j]))

    def test_layout_desktop_keeps_icons_free(self):
        L = layout(GOALS[:4], "nature", "desktop")
        self.assertEqual(min(t["x"] for t in L["tiles"]), 806)
        self.assertEqual(layout(GOALS, "nature", "desktop")["tiles"][2]["x"], 1538)   # 5 goals → 3 columns

    def test_layout_errors(self):
        with self.assertRaises(ValueError):
            layout([])
        with self.assertRaises(ValueError):
            layout(GOALS * 2)
        with self.assertRaises(ValueError):
            layout(GOALS, "neon")

    def test_word_of_year(self):
        self.assertEqual(word_of_year(GOALS), {"category": "health", "word_th": "แข็งแรง", "word_en": "Strong", "line_th": "คำประจำปี 2570 ของฉัน: แข็งแรง"})
        self.assertEqual(word_of_year([G_MONEY, G_BOOK])["word_th"], "มั่นคง")     # tie → first goal

    def test_countdown(self):
        self.assertEqual(countdown("2026-12-24"), {"date": "2026-12-24", "days_to_new_year": 8, "days_passed": 357, "year_pct": 98})
        self.assertEqual(countdown("2027-01-01")["days_passed"], 0)

    def test_streak(self):
        self.assertEqual(streak(CHECKINS, "2027-02-07"), {"weeks": 6, "this_week_done": True, "badge_th": None, "next_badge_at": 12})
        self.assertEqual(streak(CHECKINS, "2027-02-10")["weeks"], 6)       # this week not yet → last week still counts
        self.assertEqual(streak(CHECKINS, "2027-02-16")["weeks"], 0)       # a whole week missed

    def test_streak_badge(self):
        self.assertEqual(streak(CHECKINS[:4], "2027-01-24")["badge_th"], "เริ่มต้นแล้ว")
        self.assertEqual(streak([], "2027-01-24"), {"weeks": 0, "this_week_done": False, "badge_th": None, "next_badge_at": 4})

    def test_expected_at(self):
        self.assertEqual(expected_at(G_MONEY, "2027-03-15"), 9235.48)
        self.assertEqual((expected_at(G_MONEY, "2026-12-24"), expected_at(G_MONEY, "2028-01-02")), (0, 60000))

    def test_progress_mid_year(self):
        self.assertEqual([p["status"] for p in P], ["behind", "on_track", "behind", "ahead", "behind"])
        self.assertEqual([p["pct"] for p in P], [38, 92, 25, 55, 25])
        self.assertEqual(P[0], {"goal_id": "g1", "done": 22500, "expected": 25100.0, "pct": 38, "status": "behind", "glow": 1,
                                "message_th": "ช้ากว่าแผนนิดหน่อย ไม่เป็นไร สัปดาห์นี้ลองก้าวเล็ก ๆ อีกครั้ง"})

    def test_progress_ignores_future_logs(self):
        self.assertEqual(progress(G_MONEY, LOGS["g1"], "2027-03-15")["done"], 6500)

    def test_progress_done_capped(self):
        p = progress(G_TRIP, [{"date": "2027-03-01", "amount": 5}], "2027-03-02")
        self.assertEqual((p["pct"], p["status"], p["glow"]), (100, "done", 5))

    def test_messages_never_shame(self):
        for p in P:
            for bad in ("ล้มเหลว", "แย่", "ขี้เกียจ"):
                self.assertNotIn(bad, p["message_th"])

    def test_board_glow(self):
        self.assertEqual(board_glow(P)["overall_pct"], 47)
        self.assertEqual((board_glow(P)["level"], board_glow(P)["lit_tiles"]), (2, 5))

    def test_review(self):
        r = review(GOALS, P, "mid_year")
        self.assertEqual((r["title_th"], r["goals_done"], r["overall_pct"], r["best_goal_id"]), ("ทบทวนครึ่งปี", 0, 47, "g2"))
        with self.assertRaises(ValueError):
            review(GOALS, P, "weekly")

    def test_buddy_card_hides_money_and_weight(self):
        c = buddy_card("คุณมิ้นท์", "คุณโบ๊ท", GOALS)
        self.assertEqual([i["amount_hidden"] for i in c["items"]], [True, True, False, False, False])
        self.assertEqual(c["items"][0]["title_th"], "เงิน")
        self.assertEqual(buddy_card("a", "b", GOALS, private=False)["items"][0]["title_th"], G_MONEY["title_th"])

    def test_share_card(self):
        s = share_card("board", 2, "แข็งแรง")
        self.assertEqual((s["size"], s["amounts_hidden_default"], s["faces_blurred"]), ("1080x1350", True, True))
        with self.assertRaises(ValueError):
            share_card("story")

    def test_reel_plan(self):
        r = reel_plan(24)
        self.assertEqual((len(r["shots"]), r["shots"][0]["end"], r["shots"][-1]["end"]), (7, 3.1, 24.0))
        for a, b in zip(r["shots"], r["shots"][1:]):
            self.assertEqual(a["end"], b["start"])
        with self.assertRaises(ValueError):
            reel_plan(45)

    def test_quota(self):
        self.assertEqual(quota(3), {"plan": "free", "boards_per_day": 3, "used": 3, "left": 0, "blocked": True})
        self.assertFalse(quota(3, "plus")["blocked"])

    def test_guard_levels(self):
        self.assertEqual(safety_guard("self_harm")["level"], "stop")
        self.assertIn("1323", safety_guard("self_harm")["message_th"])
        self.assertEqual(safety_guard("gambling"), {"flag": "gambling", "level": "warn", "message_th": GUARD["gambling"][1], "block": False})
        self.assertFalse(safety_guard()["block"])

    def test_privacy_minor_needs_parent(self):
        self.assertEqual(privacy_check([], TEEN["age"])["share_allowed"], False)
        self.assertEqual(privacy_check([], TEEN["age"], True)["share_allowed"], True)
        self.assertEqual(privacy_check([], TEEN["age"])["flags"], ["minor"])

    def test_privacy_stop_wins(self):
        r = privacy_check(["gambling", "self_harm"])
        self.assertEqual((r["allowed"], r["level"], r["share_allowed"], len(r["messages_th"])), (False, "stop", False, 2))
        self.assertEqual(privacy_check()["level"], "ok")


if __name__ == "__main__":
    unittest.main(verbosity=1)
