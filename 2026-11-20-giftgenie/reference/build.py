"""Generate ../schemas.json + ../examples.json and validate every example."""
import json, os, jsonschema
from giftgenie import *
from fixtures import *

S = "https://json-schema.org/draft/2020-12/schema"
s = {"type": "string"}
b = {"type": "boolean"}
i0 = {"type": "integer", "minimum": 0}
i1 = {"type": "integer", "minimum": 1}
pct = {"type": "integer", "minimum": 0, "maximum": 100}
rel = {"enum": RELS}
age = {"enum": AGE_BANDS}
vibe = {"enum": VIBES}
hobby = {"enum": HOBBIES}
occ = {"enum": OCCASIONS}
tone = {"enum": TONES}
date = {"type": "string", "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}$"}

def obj(req, props, **kw):
    return {"type": "object", "required": req, "properties": props, "additionalProperties": False, **kw}

def arr(i, **kw):
    return {"type": "array", "items": i, **kw}

defs = {
 "Person": obj(["id", "name_th", "age"], {
    "id": {"type": "string", "pattern": "^u[0-9]{2}$"}, "name_th": s, "name_en": s, "age": i1, "city_th": s, "goal_th": s}),
 "Quiz": obj(["relationship", "age_band", "vibe", "hobbies", "occasion", "budget_thb", "receiver_name_th", "is_minor"], {
    "relationship": rel, "age_band": age, "vibe": vibe, "hobbies": arr(hobby, minItems=1), "occasion": occ,
    "budget_thb": i0, "receiver_name_th": s, "is_minor": b}),
 "GiftInfo": obj(["id", "name_th", "name_en", "min", "max", "mid", "rel", "age", "vibe", "hobby", "occasions", "adult_only", "why_th"], {
    "id": {"type": "string", "pattern": "^g[0-9]{2}$"}, "name_th": s, "name_en": s, "min": i0, "max": i0, "mid": i0,
    "rel": arr(rel), "age": arr(age), "vibe": arr(vibe), "hobby": arr(hobby), "occasions": arr(occ),
    "adult_only": b, "why_th": s}),
 "GiftPick": obj(["gift_id", "name_th", "name_en", "min_thb", "max_thb", "mid_thb", "score", "why_th", "adult_only", "disclaimer_th"], {
    "gift_id": s, "name_th": s, "name_en": s, "min_thb": i0, "max_thb": i0, "mid_thb": i0, "score": pct,
    "why_th": s, "adult_only": b, "disclaimer_th": s}),
 "BudgetPicks": obj(["receiver_name_th", "budget_thb", "picks", "count", "filtered_out"], {
    "receiver_name_th": s, "budget_thb": i0, "picks": arr({"$ref": "#/$defs/GiftPick"}), "count": i0, "filtered_out": i0}),
 "SwapPicks": obj(["picks", "count"], {"picks": arr({"$ref": "#/$defs/GiftPick"}), "count": i0}),
 "CardMessage": obj(["n", "occasion", "tone", "receiver_name_th", "text_th"], {
    "n": i1, "occasion": occ, "tone": tone, "receiver_name_th": s, "text_th": s}),
 "WrapIdeas": obj(["band", "budget_thb", "ideas_th", "tip_th", "disclaimer_th"], {
    "band": {"enum": ["low", "mid", "high", "luxe"]}, "budget_thb": i0, "ideas_th": arr(s, minItems=1), "tip_th": s, "disclaimer_th": s}),
 "ReminderStatus": obj(["event_date", "today", "days_left", "status"], {
    "event_date": date, "today": date, "days_left": {"type": "integer"}, "status": {"enum": ["past", "due", "soon", "ok"]}}),
 "OccasionEvent": obj(["id", "receiver_name_th", "occasion", "event_date", "budget_thb", "days_left", "status"], {
    "id": s, "receiver_name_th": s, "occasion": occ, "event_date": date, "budget_thb": i0,
    "days_left": {"type": "integer"}, "status": {"enum": ["past", "due", "soon", "ok"]}}),
 "CalendarStats": obj(["count", "due", "soon", "next_id"], {
    "count": i0, "due": i0, "soon": i0, "next_id": {"type": ["string", "null"]}}),
 "ShareCard": obj(["title_th", "headline_th", "hook_th", "budget_thb", "score", "message_th", "layout", "sizes", "watermark", "cta_th"], {
    "title_th": s, "headline_th": s, "hook_th": s, "budget_thb": i0, "score": pct, "message_th": s,
    "layout": {"enum": ["gift_card"]}, "sizes": arr({"enum": ["1080x1350", "1080x1920", "1080x1080"]}),
    "watermark": s, "cta_th": s}),
 "Quota": obj(["allowed", "left_after", "paywall"], {"allowed": i0, "left_after": {"type": ["integer", "null"], "minimum": 0}, "paywall": b}),
 "SafetyGuard": obj(["level", "message_th"], {"level": {"enum": ["ok", "warn", "stop"]}, "message_th": s}),
}
schema = {"$schema": S, "$id": "https://example.com/giftgenie.schema.json", "title": "GiftGenie", "$defs": defs}

def ref(n):
    return {"$ref": f"#/$defs/{n}", "$defs": defs}

ex = []
def add(n, v, note=""):
    ex.append({"def": n, "note": note, "value": v})

for p in PEOPLE:
    add("Person", p, p["name_th"])
for key, raw in QUIZZES.items():
    q = persona_quiz(**raw)
    add("Quiz", q, key)
    bp = budget_picks(q)
    add("BudgetPicks", bp, key)
    for pk in bp["picks"]:
        add("GiftPick", pk, f"{key} {pk['gift_id']}")
    add("SwapPicks", already_has_swap(q, [bp["picks"][0]["gift_id"]] if bp["picks"] else []), key)

for gid, g in GIFTS.items():
    add("GiftInfo", {"id": gid, **g}, gid)

for occ, tn, who in (("birthday", "sweet", "ต้น"), ("birthday", "funny", "ต้น"), ("thank_you", "formal", "คุณสุรีย์"),
                     ("thank_you", "short", "คุณสุรีย์"), ("housewarming", "sweet", "เจ"), ("condolence", "formal", "คุณสุรีย์"),
                     ("new_job", "funny", "เจ"), ("anniversary", "sweet", "ต้น"), ("just_because", "short", "ต้น")):
    for m in card_messages(occ, tn, who, 2):
        add("CardMessage", m, f"{who} {occ} {tn} {m['n']}")

for bgt, note in ((400, "low"), (1500, "mid"), (2000, "high"), (5000, "luxe"), (500, "low edge"), (3000, "high edge")):
    add("WrapIdeas", wrap_ideas(bgt), note)

for e in EVENTS:
    ev = occasion_event(*e, TODAY)
    add("OccasionEvent", ev, ev["id"])
    add("ReminderStatus", reminder_status(e[3], TODAY), ev["id"])
evs = [occasion_event(*e, TODAY) for e in EVENTS]
add("CalendarStats", calendar_stats(evs), "bim cal")
add("CalendarStats", calendar_stats([]), "empty")

q = persona_quiz(**BIM_QUIZ)
top = budget_picks(q)["picks"][0]
msg = card_messages("birthday", "sweet", "ต้น", 1)[0]["text_th"]
add("ShareCard", share_card(q, top, msg), "bim")
add("ShareCard", share_card(q, None, ""), "empty")
add("Quota", quota(1, 1), "free")
add("Quota", quota(3, 1), "exhausted")
add("Quota", quota(0, 5, pro=True), "pro")
add("SafetyGuard", safety_guard(False), "adult")
add("SafetyGuard", safety_guard(True), "minor")
add("SafetyGuard", safety_guard(True, True), "minor adult item")

for e in ex:
    jsonschema.validate(e["value"], ref(e["def"]))

d = os.path.dirname(os.path.abspath(__file__)) + "/.."
json.dump(schema, open(d + "/schemas.json", "w"), ensure_ascii=False, indent=1)
json.dump({"examples": ex}, open(d + "/examples.json", "w"), ensure_ascii=False, indent=1)
print(len(defs), "defs,", len(ex), "examples, all valid")
