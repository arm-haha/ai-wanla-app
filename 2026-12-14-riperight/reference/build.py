"""Generate ../schemas.json + ../examples.json and validate every example."""
import json, os, jsonschema
from riperight import *
from fixtures import *

S = "https://json-schema.org/draft/2020-12/schema"
s = {"type": "string"}; b = {"type": "boolean"}
u = {"type": "number", "minimum": 0, "maximum": 1}
i0 = {"type": "integer", "minimum": 0}; i1 = {"type": "integer", "minimum": 1}
pct = {"type": "integer", "minimum": 0, "maximum": 100}
fruit = {"enum": list(FRUITS)}; stage = {"enum": ["unripe", "almost", "perfect", "overripe"]}
date = {"type": "string", "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}$"}
month = {"type": "integer", "minimum": 1, "maximum": 12}

def obj(req, props, **kw):
    return {"type": "object", "required": req, "properties": props, "additionalProperties": False, **kw}
def arr(i, **kw):
    return {"type": "array", "items": i, **kw}
R = lambda n: {"$ref": f"#/$defs/{n}"}

defs = {
 "Person": obj(["id", "name_th", "age"], {"id": {"type": "string", "pattern": "^u[0-9]{2}$"}, "name_th": s, "name_en": s, "age": i1, "city_th": s}),
 "FruitPhoto": obj(["id", "fruit", "px_w", "px_h", "glare", "blur", "crop"], {"id": {"type": "string", "pattern": "^p[0-9]{2}$"}, "fruit": fruit, "px_w": i1, "px_h": i1, "glare": u, "blur": u, "crop": u}),
 "ScanQuality": obj(["score", "ok", "tips_th"], {"score": pct, "ok": b, "tips_th": arr(s)}),
 "FruitScan": obj(["photo_id", "fruit", "quality"], {"photo_id": s, "fruit": fruit, "quality": R("ScanQuality")}),
 "AiCueExtract": obj(["fruit", "color", "spots", "confidence", "mold_seen"], {"fruit": fruit, "color": u, "spots": u, "confidence": u, "mold_seen": b, "notes_th": s}),
 "RipenessInput": obj(["fruit", "color", "spots"], {"fruit": fruit, "color": u, "spots": u, "firmness": {"enum": list(FIRMNESS)}, "aroma": {"enum": list(AROMA)}, "knock": u}),
 "RipenessResult": obj(["fruit", "fruit_th", "index", "score", "stage", "stage_th", "ripens_after_pick", "days_to_perfect", "eat_within_days", "cues_used", "confidence", "headline_th", "disclaimer_th"], {
    "fruit": fruit, "fruit_th": s, "index": u, "score": pct, "stage": stage, "stage_th": s, "ripens_after_pick": b, "days_to_perfect": i0, "eat_within_days": i0,
    "cues_used": arr({"enum": ["color", "spots", "firmness", "aroma", "knock"]}, minItems=2), "confidence": u, "headline_th": s, "disclaimer_th": s}),
 "KnockInput": obj(["fruit", "hz", "decay_ms"], {"fruit": {"enum": ["watermelon", "durian"]}, "hz": {"type": "number", "minimum": 30, "maximum": 600}, "decay_ms": {"type": "number", "minimum": 10, "maximum": 2000}}),
 "KnockResult": obj(["fruit", "hz", "decay_ms", "verdict", "verdict_th", "cue", "tip_th"], {"fruit": {"enum": ["watermelon", "durian"]}, "hz": {"type": "number"}, "decay_ms": {"type": "number"},
    "verdict": {"enum": ["unripe", "almost", "ripe", "overripe"]}, "verdict_th": s, "cue": u, "tip_th": s}),
 "PriceInput": obj(["fruit", "total_baht", "kg", "month"], {"fruit": fruit, "total_baht": {"type": "number", "exclusiveMinimum": 0}, "kg": {"type": "number", "exclusiveMinimum": 0}, "month": month}),
 "PriceCheck": obj(["fruit", "per_kg", "ref_low", "ref_high", "in_season", "verdict", "verdict_th", "diff_from_mid_pct", "disclaimer_th"], {"fruit": fruit, "per_kg": {"type": "number"}, "ref_low": i1, "ref_high": i1, "in_season": b,
    "verdict": {"enum": ["suspicious_low", "cheap", "fair", "pricey", "very_pricey"]}, "verdict_th": s, "diff_from_mid_pct": {"type": "integer"}, "disclaimer_th": s}),
 "StoragePlan": obj(["fruit", "goal", "where", "speed_factor", "steps_th"], {"fruit": fruit, "goal": {"enum": ["speed_up", "keep", "slow_down"]}, "where": {"enum": ["counter", "paper_bag", "fridge"]},
    "speed_factor": {"type": "number", "exclusiveMinimum": 0}, "steps_th": arr(s, minItems=1)}),
 "BasketItem": obj(["label", "fruit", "days_to_perfect", "eat_within_days"], {"label": s, "fruit": fruit, "days_to_perfect": i0, "eat_within_days": i0}),
 "EatDay": obj(["date", "eat", "waiting", "past_best"], {"date": date, "eat": arr(s), "waiting": arr(s), "past_best": arr(s)}),
 "EatPlan": obj(["start", "days", "eat_first", "headline_th"], {"start": date, "days": arr(R("EatDay"), minItems=1), "eat_first": s, "headline_th": s}),
 "PickCheck": obj(["fruit", "questions_th", "answers", "yes", "verdict", "verdict_th"], {"fruit": fruit, "questions_th": arr(s, minItems=4, maxItems=4), "answers": arr(b, minItems=4, maxItems=4),
    "yes": {"type": "integer", "minimum": 0, "maximum": 4}, "verdict": {"enum": ["pick", "maybe", "skip"]}, "verdict_th": s}),
 "SeasonCalendar": obj(["month", "fruits", "fruits_th", "tip_th"], {"month": month, "fruits": arr(fruit), "fruits_th": arr(s), "tip_th": s}),
 "DiaryEntry": obj(["date", "fruit", "predicted", "result", "paid_baht"], {"date": date, "fruit": fruit, "predicted": stage, "result": {"enum": ["just_right", "too_raw", "too_ripe"]}, "paid_baht": i0}),
 "DiarySummary": obj(["count", "accuracy_pct", "spent_baht", "top_fruit", "headline_th"], {"count": i1, "accuracy_pct": pct, "spent_baht": i0, "top_fruit": fruit, "headline_th": s}),
 "ShareCard": obj(["title_th", "hook_th", "layout", "sizes", "watermark", "cta_th", "disclaimer_th"], {"title_th": s, "hook_th": s, "layout": {"enum": ["fruit_meter"]},
    "sizes": arr({"enum": ["1080x1350", "1080x1920", "1080x1080"]}), "watermark": s, "cta_th": s, "disclaimer_th": s}),
 "Quota": obj(["allowed", "left_after", "paywall"], {"allowed": i0, "left_after": {"type": ["integer", "null"], "minimum": 0}, "paywall": b}),
 "SafetyGuard": obj(["level", "message_th"], {"level": {"enum": ["ok", "warn", "stop"]}, "message_th": s}),
}
schema = {"$schema": S, "$id": "https://example.com/riperight.schema.json", "title": "RipeRight", "$defs": defs}
def ref(n):
    return {"$ref": f"#/$defs/{n}", "$defs": defs}

ex = []
def add(n, v, note=""):
    ex.append({"def": n, "note": note, "value": v})

for p in PEOPLE: add("Person", p, p["name_en"])
for ph in PHOTOS: add("FruitPhoto", ph, ph["id"]); add("FruitScan", fruit_scan(ph), ph["id"])
add("ScanQuality", scan_quality(0.2, 0.2, 0.2), "mid")
add("AiCueExtract", {"fruit": "avocado", "color": 0.40, "spots": 0.05, "confidence": 0.88, "mold_seen": False, "notes_th": "เปลือกเริ่มเข้ม ยังมีสีเขียวมาก"}, "avocado")
add("AiCueExtract", {"fruit": "banana", "color": 0.95, "spots": 0.70, "confidence": 0.93, "mold_seen": False}, "banana spotted")
add("AiCueExtract", {"fruit": "papaya", "color": 0.7, "spots": 0.3, "confidence": 0.62, "mold_seen": True, "notes_th": "เห็นจุดฟูขาวที่ขั้ว"}, "mold")
inputs = [("avocado", 0.40, 0.05, "firm", None, None), ("mango", 0.85, 0.10, "yielding", "strong", None), ("banana", 0.95, 0.70, None, None, None),
          ("watermelon", 0.60, 0.05, None, None, 0.75), ("watermelon", 0.60, 0.05, None, None, None), ("durian", 0.5, 0.1, "yielding", "strong", 0.75),
          ("papaya", 0.3, 0.0, "hard", None, None), ("pineapple", 0.7, 0.1, "firm", "faint", None), ("mangosteen", 0.9, 0.1, "yielding", None, None),
          ("avocado", 0.8, 0.2, "soft", None, None), ("mango", 0.1, 0.0, "hard", "none", None), ("banana", 0.6, 0.1, "firm", None, None)]
for fr, c, sp, fi, ar, kn in inputs:
    inp = {"fruit": fr, "color": c, "spots": sp}
    for k, v in (("firmness", fi), ("aroma", ar), ("knock", kn)):
        if v is not None: inp[k] = v
    r = ripeness(fr, c, sp, fi, ar, kn); note = f"{fr} {r['stage']}"
    add("RipenessInput", inp, note); add("RipenessResult", r, note)
    for g in ("speed_up", "keep", "slow_down"): add("StoragePlan", storage_plan(fr, r["stage"], g), f"{note} {g}")
for fr, hz, dm in (("watermelon", 120, 180), ("watermelon", 300, 100), ("watermelon", 100, 90), ("watermelon", 70, 50), ("durian", 100, 150), ("durian", 75, 200)):
    add("KnockInput", {"fruit": fr, "hz": hz, "decay_ms": dm}, f"{fr} {hz}Hz"); add("KnockResult", knock_test(fr, hz, dm), f"{fr} {hz}Hz")
for fr, t, kg, m in (("watermelon", 80, 3.2, 12), ("watermelon", 160, 3.0, 12), ("durian", 900, 3.0, 12), ("durian", 450, 3.0, 5), ("mango", 30, 1.0, 4), ("avocado", 120, 0.8, 12), ("mangosteen", 15, 1.0, 6), ("banana", 35, 1.0, 12)):
    add("PriceInput", {"fruit": fr, "total_baht": t, "kg": kg, "month": m}, f"{fr} {t}"); add("PriceCheck", price_check(fr, t, kg, m), f"{fr} {t}")
for it in BASKET: add("BasketItem", it, it["label"])
add("EatPlan", eat_plan(BASKET, TODAY), "demo basket")
for d in eat_plan(BASKET, TODAY)["days"]: add("EatDay", d, d["date"])
add("EatPlan", eat_plan([basket_item("กล้วย", BANANA), basket_item("มะละกอ", ripeness("papaya", 0.3, 0.0, "hard"))], TODAY, 7), "banana+papaya 7d")
for fr, a in (("watermelon", [True, True, True, False]), ("durian", [True, False, True, False]), ("mango", [False, False, True, False]), ("pineapple", [True, True, True, True])):
    add("PickCheck", pick_check(fr, a), fr)
for m in (1, 4, 6, 9, 12): add("SeasonCalendar", season_calendar(m), str(m))
for d in DIARY: add("DiaryEntry", d, d["fruit"])
add("DiarySummary", diary_summary(DIARY), "tom")
add("ShareCard", share_card(AVO, "ถ่ายปุ๊บ รู้เลยกินได้วันไหน"), "demo")
for a in ((0,), (4,), (5,), (9, 5, True)): add("Quota", quota(*a), str(a))
for f in (None, "mold", "durian_alcohol", "not_fruit"): add("SafetyGuard", safety_guard(f), str(f))

for x in ex: jsonschema.validate(x["value"], ref(x["def"]))
d = os.path.dirname(os.path.abspath(__file__)) + "/.."
json.dump(schema, open(d + "/schemas.json", "w"), ensure_ascii=False, indent=1)
json.dump({"examples": ex}, open(d + "/examples.json", "w"), ensure_ascii=False, indent=1)
print(len(defs), "defs,", len(ex), "examples, all valid")
