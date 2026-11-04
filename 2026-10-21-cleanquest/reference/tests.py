"""Run: python3 tests.py — locks the demo numbers the Reel shows."""
from datetime import date
import cleanquest as C, fixtures as X
ON = date.fromisoformat(X.TODAY)
B, A = C.mess_score(X.BEFORE), C.mess_score(X.AFTER)
FIRE = C.quest_plan(X.BEFORE, "fire")
def t_before(): assert (B["clean_score"], B["mess_points"], B["label_th"], B["est_minutes"]) == (12, 88, "ห้องวิกฤต 🚨", 38)
def t_after(): assert (A["clean_score"], A["label_th"]) == (94, "ห้องโชว์ ✨")
def t_pins_sorted(): assert [p["id"] for p in B["hotspots"]][:3] == ["clothes_pile", "trash_floor", "dishes_cups"]
def t_worst_zone_tie(): assert B["zone_points"] == {"bed": 30, "desk": 30, "floor": 28} and B["worst_zone"] == "bed"
def t_floor_zero(): assert C.mess_score([{"id": "clothes_pile", "severity": 3}, {"id": "trash_floor", "severity": 3}, {"id": "dishes_cups", "severity": 3}, {"id": "desk_clutter", "severity": 3}])["clean_score"] == 0
def t_empty_room(): r = C.mess_score([]); assert (r["clean_score"], r["worst_zone"]) == (100, None)
def t_dedupe(): assert C.mess_score([{"id": "bed_unmade", "severity": 1}, {"id": "bed_unmade", "severity": 3}])["mess_points"] == 6
def t_bad_hotspot():
    try: C.mess_score([{"id": "ghost", "severity": 1}]); assert False
    except ValueError: pass
def t_bad_severity():
    try: C.mess_score([{"id": "bed_unmade", "severity": 4}]); assert False
    except ValueError: pass
def t_fire_order(): assert [q["hotspot"] for q in FIRE["quests"]] == ["snack_wrappers", "trash_floor", "bed_unmade", "dishes_cups", "clothes_pile", "boxes_parcels", "desk_clutter", "cables_mess"]
def t_fire_sprints(): assert [s["minutes"] for s in FIRE["sprints"]] == [14, 12, 12] and FIRE["total_minutes"] == 38
def t_fire_scores(): assert [q["score_after"] for q in FIRE["quests"]] == [20, 40, 46, 56, 80, 88, 96, 100]
def t_sprint_cap():
    for s in FIRE["sprints"]: assert s["minutes"] <= C.SPRINT_MIN or len(s["quest_ids"]) == 1
def t_lazy(): p = C.quest_plan(X.BEFORE, "lazy"); assert [q["hotspot"] for q in p["quests"]] == ["snack_wrappers", "bed_unmade"] and p["score_after"] == 26 and p["total_minutes"] <= 5
def t_normal(): p = C.quest_plan(X.BEFORE, "normal"); assert (p["total_minutes"], p["score_after"], len(p["quests"])) == (14, 56, 4)
def t_quick_win(): assert [q["quick_win"] for q in FIRE["quests"]][:3] == [True, False, True]
def t_timer_mid(): t = C.timer_tick(FIRE, ["q1", "q2", "q3"], 600); assert (t["live_score"], t["next_quest"], t["sprint"], t["remaining_sec"]) == (46, "q4", 1, 1680)
def t_timer_done(): t = C.timer_tick(FIRE, [q["id"] for q in FIRE["quests"]], 2400); assert t["finished"] and t["live_score"] == 100 and t["remaining_sec"] == 0
def t_glow(): g = C.glow_up(B, A, 38, 8, X.NAME); assert (g["delta"], g["title_th"], g["headline_th"]) == (82, "ห้องเกิดใหม่ 🦋", "ห้องฟ้า 12 → 94 ใน 38 นาที")
def t_declutter(): assert [C.declutter(i)["decision"] for i in X.ITEMS] == ["sell", "keep", "trash", "donate", "keep"]
def t_listing(): d = C.declutter(X.ITEMS[0]); assert d["resale_thb"] == 770 and "฿770" in d["listing_th"]
def t_split(): assert [(s["person"], s["minutes"], s["quest_ids"]) for s in C.chore_split(FIRE["quests"], X.ROOMMATES)] == [("ฟ้า", 20, ["q5", "q6", "q1", "q3"]), ("มุก", 18, ["q2", "q7", "q4", "q8"])]
def t_progress_before(): assert C.progress(X.LOG + [{"on": X.TODAY, "kind": "scan"}], ON) == {"xp": 150, "level": 2, "streak_days": 7}
def t_reset(): assert C.weekly_reset(X.SESSIONS, ON) == {"next_reset": "2026-10-25", "days_left": 4, "done_this_week": False}
def t_wrapped():
    s = X.SESSIONS + [{"on": X.TODAY, "before": 12, "after": 94, "minutes": 38, "hotspots": [h["id"] for h in X.BEFORE]}]
    w = C.wrapped(s, "2026-10"); assert (w["sessions"], w["minutes"], w["avg_delta"], w["best_delta"], w["top_hotspot"]) == (4, 85, 44, 82, "clothes_pile")
if __name__ == "__main__":
    ts = [(k, v) for k, v in dict(globals()).items() if k.startswith("t_")]
    for k, f in ts: f(); print("ok", k)
    print(f"{len(ts)} tests passed")
