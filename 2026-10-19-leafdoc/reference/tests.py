"""Run: python3 tests.py — locks the demo numbers the Reel shows."""
from datetime import date
import leaf as L, fixtures as X
ON = date.fromisoformat(X.TODAY); P = {p["id"]: p for p in X.PLANTS}
DX = {k: L.diagnose(P[k], c["symptoms"], c["ctx"], ON) for k, c in X.CHECKUPS.items()}
def t_scores(): assert {k: v["health_score"] for k, v in DX.items()} == {"p1": 55, "p2": 70, "p3": 100}
def t_grades(): assert [DX[k]["grade"] for k in ("p1", "p2", "p3")] == ["sick", "fussy", "thriving"]
def t_p1_causes(): assert [(c["cause_id"], c["points"], c["confidence_pct"]) for c in DX["p1"]["causes"]] == [("overwater", 11, 50), ("low_humidity", 6, 27), ("root_rot", 5, 23)]
def t_pct_sum_100():
    for d in DX.values():
        if d["causes"]: assert sum(c["confidence_pct"] for c in d["causes"]) == 100
def t_p2_underwater(): assert (DX["p2"]["top_cause"], DX["p2"]["causes"][0]["confidence_pct"]) == ("underwater", 61)
def t_healthy(): assert DX["p3"]["causes"] == [] and DX["p3"]["top_cause"] is None
def t_symptom_order_canonical(): assert L.diagnose(P["p1"], ["brown_tips", "drooping"], X.CHECKUPS["p1"]["ctx"], ON)["symptoms"] == ["brown_tips", "drooping"]
def t_water():
    w = {k: L.water_status(p, ON) for k, p in P.items()}
    assert {k: (v["interval_days"], v["status"], v["due_on"]) for k, v in w.items()} == {"p1": (12, "ok", "2026-10-29"), "p2": (8, "overdue", "2026-10-15"), "p3": (13, "ok", "2026-10-23")}
    assert w["p2"]["next_dates"][0] == X.TODAY and w["p2"]["status_th"] == "เลยกำหนด 4 วัน"
def t_seasons(): assert [L.season_of(date(2026, m, 1)) for m in (4, 10, 12)] == ["hot", "rainy", "cool"]
def t_half_up(): assert L.rnd(2.5) == 3 and L.rnd(0.5) == 1 and L.water_interval("fern", "direct", "terracotta", date(2026, 4, 1)) == 1
def t_plan():
    p = L.rescue_plan(DX["p1"], X.TODAY)
    assert p["title_th"] == "แผนชุบชีวิต 7 วัน: รดน้ำมากไป" and len(p["days"]) == 7 and p["recheck_on"] == "2026-10-26" and "อากาศแห้ง" in p["days"][2]["extra_th"]
    assert L.plan_progress(p, X.PLAN_DONE_DAYS) == {"done": 3, "of": 7, "pct": 43}
def t_glow():
    a = X.P1_AFTER; d2 = L.diagnose(dict(P["p1"], light=a["ctx"]["light"]), a["symptoms"], a["ctx"], date.fromisoformat(a["on"]))
    g = L.glow_up(DX["p1"], d2, a["new_leaves"]); assert (g["before_score"], g["after_score"], g["delta"], g["days"]) == (55, 94, 39, 14)
def t_light():
    assert [L.lux_from_luma(s["mean_luma"]) for s in X.LUMA_SAMPLES] == [640, 2560, 20480]
    assert L.light_reading(20480)["fits"] == ["cactus"] and "cactus" not in L.light_reading(640)["fits"]
def t_pets(): assert L.pet_check("monstera")["pet_toxic"] and not L.pet_check("spider")["pet_toxic"] and not L.pet_check("monstera")["verified"]
def t_room_match(): assert [(m["species"], m["fit"]) for m in L.room_match(X.ROOM_QUIZ)] == [("spider", 100), ("fern", 50), ("pothos", 40)]
def t_room_no_pets(): assert L.room_match({"light": "low", "ac_room": False, "pets": False, "forgetful": True})[0]["species"] == "snake"
def t_streak(): assert L.care_streak(X.CARE_DAYS, X.TODAY) == 5 and L.care_streak(X.CARE_DAYS, "2026-10-20") == 0
def t_wrapped():
    log = X.LOG + [{"on": X.TODAY, "kind": "checkup", "plant_id": k, "top_cause": d["top_cause"], "delta": 0} for k, d in DX.items()]
    w = L.plant_wrapped(log, "2026-10"); assert (w["waterings"], w["on_time_pct"], w["checkups"], w["top_cause"]) == (6, 50, 3, "overwater")
def t_jungle(): assert L.jungle_level(3, 3, 3) == {"xp": 105, "level": 2, "title_th": "สายเขียวฝึกหัด", "next_at": 250}
def t_score_floor(): assert L.diagnose(P["p1"], list(L.SYMPTOMS), X.CHECKUPS["p1"]["ctx"], ON)["health_score"] == 5
if __name__ == "__main__":
    ts = [(k, v) for k, v in dict(globals()).items() if k.startswith("t_")]
    for k, f in ts: f()
    print(f"{len(ts)} tests passed")
