"""Generate ../schemas.json + ../examples.json and validate every example."""
import json, os, jsonschema
from savequest import *
from fixtures import *

S = "https://json-schema.org/draft/2020-12/schema"
s = {"type": "string"}
b = {"type": "boolean"}
u = {"type": "number", "minimum": 0, "maximum": 1}
i0 = {"type": "integer", "minimum": 0}
i1 = {"type": "integer", "minimum": 1}
pct = {"type": "integer", "minimum": 0, "maximum": 100}
goal = {"enum": list(GOALS)}
chal = {"enum": list(CHALLENGES)}
nullint = {"type": ["integer", "null"], "minimum": 0}

def obj(req, props, **kw):
    return {"type": "object", "required": req, "properties": props, "additionalProperties": False, **kw}

def arr(i, **kw):
    return {"type": "array", "items": i, **kw}

defs = {
 "Person": obj(["id", "name_th", "age", "goal_id", "goal_thb", "saved_thb"], {
    "id": {"type": "string", "pattern": "^u[0-9]{2}$"}, "name_th": s, "name_en": s, "age": i1,
    "city_th": s, "goal_id": goal, "goal_th": s, "goal_thb": i1, "saved_thb": i0,
    "start": s, "deadline": s, "week": i1, "base_thb": i1, "seed": s}),
 "GoalPhoto": obj(["id", "px_w", "px_h", "glare", "blur", "crop", "goal_id"], {
    "id": {"type": "string", "pattern": "^p[0-9]{2}$"}, "px_w": i1, "px_h": i1,
    "glare": u, "blur": u, "crop": u, "goal_id": goal}),
 "ScanQuality": obj(["score", "ok", "tips_th"], {"score": pct, "ok": b, "tips_th": arr(s)}),
 "PhotoScan": obj(["photo_id", "quality"], {
    "photo_id": s, "quality": {"$ref": "#/$defs/ScanQuality"}, "goal_id": goal}),
 "Pipeline": obj(["photo_id", "steps"], {"photo_id": s, "steps": arr(s, minItems=1)}),
 "GoalInfo": obj(["id", "goal_id", "name_th", "name_en", "icon", "hint_th", "sample_thb"], {
    "id": {"type": "string", "pattern": "^g[0-9]{2}$"}, "goal_id": goal, "name_th": s, "name_en": s,
    "icon": s, "hint_th": s, "sample_thb": i1}),
 "JarFill": obj(["saved_thb", "goal_thb", "remaining_thb", "pct", "level", "label_th", "headline_th"], {
    "saved_thb": i0, "goal_thb": i1, "remaining_thb": i0, "pct": pct,
    "level": {"enum": ["empty", "growing", "halfway", "almost", "full"]},
    "label_th": s, "headline_th": s}),
 "Milestones": obj(["pct", "reached", "next_mark", "message_th"], {
    "pct": pct, "reached": arr({"enum": list(MARKS)}), "next_mark": {"type": ["integer", "null"], "enum": [25, 50, 75, 100, None]},
    "next_amount_thb": nullint, "need_thb": nullint, "message_th": s}),
 "Week52Plan": obj(["kind", "week", "base_thb", "amount_thb", "cumulative_thb", "plan_total_thb", "label_th"], {
    "kind": {"const": "week52"}, "week": {"type": "integer", "minimum": 1, "maximum": 52},
    "base_thb": i1, "amount_thb": i1, "cumulative_thb": i0, "plan_total_thb": i1, "label_th": s}),
 "RandomPlan": obj(["kind", "week", "base_thb", "seed", "multiplier", "amount_thb", "cumulative_thb", "plan_total_thb", "label_th"], {
    "kind": {"const": "random"}, "week": {"type": "integer", "minimum": 1, "maximum": 52},
    "base_thb": i1, "seed": s, "multiplier": {"type": "integer", "minimum": 1, "maximum": 52},
    "amount_thb": i1, "cumulative_thb": i0, "plan_total_thb": i1, "label_th": s}),
 "Challenge": obj(["id", "name_th", "save_thb", "xp", "hint_th"], {
    "id": {"type": "string", "pattern": "^c[0-9]{2}$"}, "name_th": s, "save_thb": i1, "xp": i1, "hint_th": s,
    "date": s, "suggested": b, "challenge_id": chal}),
 "CompletedChallenge": obj(["id", "challenge_id", "name_th", "save_thb", "xp", "date", "done", "message_th"], {
    "id": s, "challenge_id": chal, "name_th": s, "save_thb": i1, "xp": i1, "date": s, "done": b, "message_th": s}),
 "Streak": obj(["days", "frozen_used", "badge_th", "today_saved", "message_th"], {
    "days": i0, "frozen_used": i0, "badge_th": s, "today_saved": b, "message_th": s}),
 "RoundUp": obj(["amount_thb", "step_thb", "extra_thb", "rounded_thb"], {
    "amount_thb": i0, "step_thb": i1, "extra_thb": i0, "rounded_thb": i0}),
 "TeamShare": obj(["name_th", "amount_thb", "pct"], {"name_th": s, "amount_thb": i0, "pct": pct}),
 "TeamJar": obj(["goal_thb", "saved_thb", "remaining_thb", "pct", "level", "members", "member_count", "headline_th"], {
    "goal_thb": i1, "saved_thb": i0, "remaining_thb": i0, "pct": pct,
    "level": {"enum": ["empty", "growing", "halfway", "almost", "full"]},
    "members": arr({"$ref": "#/$defs/TeamShare"}, minItems=1), "member_count": i1, "headline_th": s}),
 "ShareCard": obj(["title_th", "headline_th", "hook_th", "pct", "streak_days", "layout", "sizes", "watermark", "cta_th"], {
    "title_th": s, "headline_th": s, "hook_th": s, "pct": pct, "streak_days": i0,
    "layout": {"enum": ["jar_milestone"]},
    "sizes": arr({"enum": ["1080x1350", "1080x1920", "1080x1080"]}),
    "watermark": s, "cta_th": s}),
 "Quota": obj(["allowed", "left_after", "paywall"], {
    "allowed": i0, "left_after": {"type": ["integer", "null"], "minimum": 0}, "paywall": b}),
 "SafetyGuard": obj(["level", "message_th"], {"level": {"enum": ["ok", "warn", "stop"]}, "message_th": s}),
}
schema = {"$schema": S, "$id": "https://example.com/savequest.schema.json", "title": "SaveQuest", "$defs": defs}

def ref(n):
    return {"$ref": f"#/$defs/{n}", "$defs": defs}

ex = []
def add(n, v, note=""):
    ex.append({"def": n, "note": note, "value": v})

for p in PEOPLE:
    slim = {k: p[k] for k in ("id", "name_th", "name_en", "age", "city_th", "goal_id", "goal_th",
                              "goal_thb", "saved_thb", "start", "deadline", "week", "base_thb", "seed")}
    add("Person", slim, p["name_th"])

for ph in PHOTOS:
    add("GoalPhoto", ph, ph["id"])
    add("PhotoScan", photo_scan(ph), ph["id"])
    add("Pipeline", {"photo_id": ph["id"], "steps": pipeline_steps(ph)}, ph["id"])

add("ScanQuality", scan_quality(0.62, 0.48, 0.55), "bad photo")

for gid in GOAL_IDS:
    add("GoalInfo", goal_info(gid), gid)

for person in PEOPLE:
    add("JarFill", jar_fill(person["saved_thb"], person["goal_thb"]), person["name_th"])
    add("Milestones", milestones(person["saved_thb"], person["goal_thb"]), person["name_th"])
    add("Week52Plan", week52_plan(person["week"], person["base_thb"]), person["name_th"])
    add("RandomPlan", random_plan(person["week"], person["base_thb"], person["seed"]), person["name_th"])

add("JarFill", jar_fill(0, 45000), "empty")
add("JarFill", jar_fill(45000, 45000), "full")
add("Milestones", milestones(45000, 45000), "done")
add("Week52Plan", week52_plan(1, 100), "week 1")
add("Week52Plan", week52_plan(52, 100), "week 52")

add("Challenge", daily_challenge(TODAY, "u01"), "mint today")
add("Challenge", daily_challenge(TODAY, "u02"), "bee today")
for cid, day in (("skip_cafe", TODAY), ("cook_home", "2026-12-02"), ("no_delivery", TODAY),
                 ("walk_not_grab", "2026-12-01"), ("pack_water", "2026-11-30"),
                 ("no_snack", "2026-11-29"), ("unsubscribe", "2026-11-28"), ("market_not_mall", "2026-11-27")):
    add("CompletedChallenge", complete_challenge(cid, day), cid)

add("Streak", streak(MINT_DATES, TODAY), "mint 12")
add("Streak", streak(BEE_DATES, TODAY, BEE_FROZEN), "bee freeze")
add("Streak", streak(["2026-12-02"], TODAY), "yesterday only")
add("Streak", streak(["2026-11-01"], TODAY), "broken")

add("RoundUp", round_up(87, 10), "87 to 90")
add("RoundUp", round_up(90, 10), "exact")
add("RoundUp", round_up(87, 50), "to 50")
add("TeamShare", team_jar(45000, MINT_TEAM)["members"][0], "mint share")
add("TeamJar", team_jar(45000, MINT_TEAM), "three friends")
add("ShareCard", share_card("น้องมิ้น", "เที่ยวญี่ปุ่น", 42, 12), "mint 42")
add("ShareCard", share_card("พี่บี", "กองฉุกเฉิน 3 เดือน", 75, 7), "bee 75")
add("Quota", quota(1, 1), "free")
add("Quota", quota(3, 1), "exhausted")
add("Quota", quota(0, 5, pro=True), "pro")
add("SafetyGuard", safety_guard(True), "ok")
add("SafetyGuard", safety_guard(False), "stop")

# extra edge / library examples to deepen the pack
for saved, goal, note in ((0, 8000, "concert empty"), (800, 8000, "concert 10"),
                          (2000, 8000, "concert 25"), (4000, 8000, "concert 50"),
                          (6000, 8000, "concert 75"), (7900, 8000, "concert almost"),
                          (11250, 45000, "mint 25"), (33750, 45000, "mint 75")):
    add("JarFill", jar_fill(saved, goal), note)
    add("Milestones", milestones(saved, goal), note)

for week in (2, 10, 26, 40, 51):
    add("Week52Plan", week52_plan(week, 100), f"w{week} base100")
    add("RandomPlan", random_plan(week, 100, "u01-2026"), f"rand w{week}")

for cid in CHALLENGE_IDS:
    c = {**CHALLENGES[cid], "date": TODAY, "suggested": False, "challenge_id": cid}
    add("Challenge", c, f"bank {cid}")

add("RoundUp", round_up(1, 10), "1 to 10")
add("RoundUp", round_up(149, 100), "sub to 200")
add("TeamJar", team_jar(30000, [{"name_th": "พี่บี", "amount_thb": 22500}, {"name_th": "น้องมิ้น", "amount_thb": 3000}]), "bee lead")


for e in ex:
    jsonschema.validate(e["value"], ref(e["def"]))

d = os.path.dirname(os.path.abspath(__file__)) + "/.."
json.dump(schema, open(d + "/schemas.json", "w"), ensure_ascii=False, indent=1)
json.dump({"examples": ex}, open(d + "/examples.json", "w"), ensure_ascii=False, indent=1)
print(len(defs), "defs,", len(ex), "examples, all valid")
