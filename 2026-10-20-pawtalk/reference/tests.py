"""Run: python3 tests.py — locks the demo numbers the Reel shows."""
from datetime import date
import pawtalk as P, fixtures as X
ON = date.fromisoformat(X.TODAY); PETS = {p["id"]: p for p in X.PETS}
M = {k: P.read_mood(PETS[k]["species"], s["cues"], s["at"], PETS[k]["meal_times"]) for k, s in X.SNAPS.items()}
def t_cat_moods(): assert [(m["mood"], m["points"], m["pct"]) for m in M["cat1"]["moods"]] == [("hungry", 8, 62), ("annoyed", 3, 23), ("needy", 2, 15)]
def t_meal_bonus(): assert M["cat1"]["meal_bonus"] and M["cat1"]["minutes_to_meal"] == 25
def t_no_meal_bonus_far(): assert not P.read_mood("cat", ["staring_at_bowl"], "12:00", ["07:30", "19:00"])["meal_bonus"]
def t_cat_vibe(): assert M["cat1"]["vibe_score"] == 38 and M["cat1"]["vibe_label"] == "ระวังนะ"
def t_cat_after(): r = P.read_mood("cat", X.CAT_AFTER["cues"], X.CAT_AFTER["at"], PETS["cat1"]["meal_times"]); assert (r["top_mood"], r["vibe_score"]) == ("chill", 96)
def t_dog(): assert (M["dog1"]["top_mood"], M["dog1"]["moods"][0]["pct"], M["dog1"]["vibe_score"]) == ("playful", 54, 87)
def t_pct_sum():
    for m in M.values(): assert sum(x["pct"] for x in m["moods"]) == 100
def t_cue_canonical(): assert P.read_mood("cat", ["tail_flick", "staring_at_bowl", "tail_flick"])["cues"] == ["tail_flick", "staring_at_bowl"]
def t_bad_cue():
    try: P.read_mood("cat", ["play_bow"]); assert False
    except ValueError: pass
def t_scared_hint(): r = P.read_mood("cat", ["ears_flat", "tail_puffed", "hiss"]); assert r["top_mood"] == "scared" and r["safety_hint"]
def t_tie_priority(): assert P.read_mood("dog", ["whale_eye"])["top_mood"] == "scared"
def t_bubble(): b = P.thought_bubble(PETS["cat1"], M["cat1"], "boss", X.OWNER, X.TODAY); assert b["text_th"] == "ทาสสส อีก 25 นาทีข้าวต้องมา ช้า 1 วิหักเงินเดือน" and b["badge_th"] == "🍗 หิว 62%"
def t_bubble_deterministic(): assert P.bubble_index("cat1", X.TODAY, "hungry", "boss") == P.bubble_index("cat1", X.TODAY, "hungry", "boss") == 0
def t_persona_flip(): assert [P.thought_bubble(PETS["cat1"], M["cat1"], p, X.OWNER, X.TODAY)["template_index"] for p in P.PERSONAS] == [0, 0, 2]
def t_duet(): d = P.duet(PETS["cat1"], M["cat1"], PETS["dog1"], M["dog1"], "boss", "sweet", X.OWNER, X.TODAY); assert [l["pet_id"] for l in d] == ["cat1", "dog1", "cat1"] and d[2]["text_th"] == "ชามว่างคือการดูหมิ่นข้า"
def t_care_order(): assert [r["task_id"] for r in P.care_board(X.CARE, ON)] == ["t1", "t5", "t6", "t2", "t4", "t3"]
def t_care_deworm(): r = P.care_board(X.CARE, ON)[0]; assert (r["status"], r["days_left"], r["due_on"]) == ("overdue", -7, "2026-10-13")
def t_health_watch(): assert P.health_check(PETS["cat1"], X.HEALTH["cat1"])["level"] == "watch"
def t_health_red(): h = P.health_check(PETS["cat1"], X.HEALTH_RED["cat1"]); assert h["level"] == "emergency" and h["show_vet_finder"]
def t_health_species_guard():
    try: P.health_check(PETS["dog1"], ["straining_no_urine"]); assert False
    except ValueError: pass
def t_health_young_escalate(): assert P.health_check(dict(PETS["cat1"], age_years=0.3), ["sneeze_mild"])["level"] == "soon"
def t_food(): f = P.food_plan(PETS["cat1"], 380, 2); d = P.food_plan(PETS["dog1"], 350, 2); assert (f["kcal_per_day"], f["grams_per_day"], f["grams_per_meal"], d["kcal_per_day"], d["grams_per_day"]) == (260, 68, 34, 582, 166)
def t_age(): assert (P.human_age(PETS["cat1"])["human_years"], P.human_age(PETS["dog1"])["human_years"]) == (28, 24)
def t_progress():
    log = X.LOG + [{"on": X.TODAY, "kind": "snap", "pet_id": k, "mood": M[k]["top_mood"]} for k in PETS]
    assert P.progress(log, ON) == {"xp": 205, "level": 3, "streak_days": 7}
def t_wrapped():
    log = X.LOG + [{"on": X.TODAY, "kind": "snap", "pet_id": "cat1", "mood": "hungry"}]
    w = P.wrapped(log, "cat1", "2026-10"); assert (w["top_mood"], w["mood_counts"]["hungry"], w["snaps"], w["grumpiest_weekday"], w["happy_pct"]) == ("hungry", 6, 13, "Wed", 23)
if __name__ == "__main__":
    ts = [(k, v) for k, v in dict(globals()).items() if k.startswith("t_")]
    for k, f in ts: f(); print("ok", k)
    print(f"{len(ts)} tests passed")
