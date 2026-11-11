"""Generate ../schemas.json + ../examples.json and validate every example."""
import json, os, jsonschema
from stainsos import *
from fixtures import *

S = "https://json-schema.org/draft/2020-12/schema"
s = {"type": "string"}; b = {"type": "boolean"}
u = {"type": "number", "minimum": 0, "maximum": 1}
n0 = {"type": "number", "minimum": 0}
i0 = {"type": "integer", "minimum": 0}; i1 = {"type": "integer", "minimum": 1}
pct = {"type": "integer", "minimum": 0, "maximum": 100}
stain = {"enum": list(STAINS)}; fabric = {"enum": list(FABRICS)}; item = {"enum": list(ITEMS)}
cls = {"enum": ["tannin", "oil", "oil_pigment", "protein", "ink", "dirt"]}

def obj(req, props, **kw):
    return {"type": "object", "required": req, "properties": props, "additionalProperties": False, **kw}
def arr(i, **kw):
    return {"type": "array", "items": i, **kw}
R = lambda n: {"$ref": f"#/$defs/{n}"}

defs = {
 "Person": obj(["id", "name_th", "age"], {"id": {"type": "string", "pattern": "^u[0-9]{2}$"}, "name_th": s, "name_en": s, "age": i1, "city_th": s}),
 "StainPhoto": obj(["id", "px_w", "px_h", "glare", "blur", "crop"], {"id": {"type": "string", "pattern": "^p[0-9]{2}$"}, "px_w": i1, "px_h": i1, "glare": u, "blur": u, "crop": u}),
 "ScanQuality": obj(["score", "ok", "tips_th"], {"score": pct, "ok": b, "tips_th": arr(s)}),
 "PhotoScan": obj(["photo_id", "quality"], {"photo_id": s, "quality": R("ScanQuality")}),
 "Pipeline": obj(["photo_id", "steps"], {"photo_id": s, "steps": arr(s, minItems=1)}),
 "StainRaw": obj(["stain", "fabric", "color", "age_hours", "size_cm", "confidence"], {"stain": stain, "fabric": fabric, "color": {"enum": ["white", "colored"]}, "age_hours": n0, "size_cm": {"type": "number", "exclusiveMinimum": 0}, "confidence": u}),
 "ParsedStain": obj(["stain", "stain_th", "cls", "fabric", "fabric_th", "color", "age_hours", "size_cm", "confidence", "needs_confirm", "message_th"], {
    "stain": stain, "stain_th": s, "cls": cls, "fabric": fabric, "fabric_th": s, "color": {"enum": ["white", "colored"]},
    "age_hours": n0, "size_cm": n0, "confidence": u, "needs_confirm": b, "message_th": s}),
 "RiskMeter": obj(["score", "level", "level_th", "dry_clean", "expected_fade_pct", "act_within_th", "disclaimer_th"], {
    "score": pct, "level": {"enum": ["easy", "medium", "hard", "pro"]}, "level_th": s, "dry_clean": b,
    "expected_fade_pct": pct, "act_within_th": s, "disclaimer_th": s}),
 "RescueStep": obj(["order", "action_th", "item", "minutes", "missing", "substitute"], {
    "order": i1, "action_th": s, "item": {"anyOf": [item, {"type": "null"}]}, "minutes": i0, "missing": b,
    "substitute": {"anyOf": [item, {"type": "null"}]}}),
 "RescuePlan": obj(["stain", "fabric", "risk_level", "dry_clean", "steps", "step_count", "total_minutes", "items_used", "shopping_list", "warnings_th", "disclaimer_th"], {
    "stain": stain, "fabric": fabric, "risk_level": {"enum": ["easy", "medium", "hard", "pro"]}, "dry_clean": b,
    "steps": arr(R("RescueStep"), minItems=1), "step_count": i1, "total_minutes": i0, "items_used": arr(item),
    "shopping_list": arr(item), "warnings_th": arr(s), "disclaimer_th": s}),
 "SafetyPair": obj(["a", "b", "why_th"], {"a": item, "b": item, "why_th": s}),
 "SafetyCheck": obj(["level", "pairs", "message_th"], {"level": {"enum": ["ok", "danger"]}, "pairs": arr(R("SafetyPair")), "message_th": s}),
 "CareLabel": obj(["codes", "lines_th", "max_wash_c", "bleach", "dryer_ok", "dry_clean_only"], {
    "codes": arr({"enum": list(CARE)}, minItems=1), "lines_th": arr(s, minItems=1), "max_wash_c": {"type": ["integer", "null"], "minimum": 0},
    "bleach": {"enum": ["any", "oxygen_only", "none"]}, "dryer_ok": b, "dry_clean_only": b}),
 "LabelFit": obj(["ok", "issues_th"], {"ok": b, "issues_th": arr(s)}),
 "KitCheck": obj(["kit", "ready_for", "ready_count", "total", "headline_th"], {"kit": arr(item), "ready_for": arr(stain), "ready_count": i0, "total": i1, "headline_th": s}),
 "DiaryEntry": obj(["date", "item_th", "stain", "result", "value_baht"], {"date": s, "item_th": s, "stain": stain, "result": {"enum": ["removed", "faded", "stuck"]}, "value_baht": i0}),
 "DiarySummary": obj(["count", "removed", "faded", "success_rate_pct", "saved_baht", "headline_th", "disclaimer_th"], {
    "count": i1, "removed": i0, "faded": i0, "success_rate_pct": pct, "saved_baht": i0, "headline_th": s, "disclaimer_th": s}),
 "ShareCard": obj(["title_th", "headline_th", "hook_th", "layout", "sizes", "watermark", "cta_th", "disclaimer_th"], {
    "title_th": s, "headline_th": s, "hook_th": s, "layout": {"enum": ["before_after"]},
    "sizes": arr({"enum": ["1080x1350", "1080x1920", "1080x1080"]}), "watermark": s, "cta_th": s, "disclaimer_th": s}),
 "Quota": obj(["allowed", "left_after", "paywall"], {"allowed": i0, "left_after": {"type": ["integer", "null"], "minimum": 0}, "paywall": b}),
 "SafetyGuard": obj(["level", "message_th"], {"level": {"enum": ["ok", "stop"]}, "message_th": s}),
 "AiStainExtract": obj(["stain", "fabric", "color", "age_hours", "size_cm", "confidence"], {"stain": stain, "fabric": fabric, "color": {"enum": ["white", "colored"]}, "age_hours": n0, "size_cm": n0, "confidence": u, "notes_th": s}),
}
schema = {"$schema": S, "$id": "https://example.com/stainsos.schema.json", "title": "StainSOS", "$defs": defs}
def ref(n):
    return {"$ref": f"#/$defs/{n}", "$defs": defs}

ex = []
def add(n, v, note=""):
    ex.append({"def": n, "note": note, "value": v})

for p in PEOPLE:
    add("Person", p, p["name_en"])
for ph in PHOTOS:
    add("StainPhoto", ph, ph["id"]); add("PhotoScan", photo_scan(ph), ph["id"]); add("Pipeline", {"photo_id": ph["id"], "steps": pipeline_steps(ph, TEA)}, ph["id"])
add("Pipeline", {"photo_id": "p01", "steps": pipeline_steps(PHOTOS[0], LOW)}, "low conf")
raws = [("tea", TEA_RAW), ("curry", CURRY_RAW), ("ink silk", INK_SILK_RAW), ("blood", BLOOD_RAW), ("mud", MUD_RAW), ("low", LOW_RAW)]
for note, raw in raws:
    add("StainRaw", raw, note); add("AiStainExtract", dict(raw, notes_th="ตัวอย่างผลจาก vision"), note)
    p = parse_stain(raw); add("ParsedStain", p, note); add("RiskMeter", risk_meter(p), note)
    if not p["needs_confirm"]:
        pl = rescue_plan(p, PRAE_KIT); add("RescuePlan", pl, note)
        for st in pl["steps"]:
            add("RescueStep", st, f"{note} step {st['order']}")
for k in STAINS:  # every stain on white cotton, fresh
    p = parse_stain({"stain": k, "fabric": "cotton", "color": "white", "age_hours": 0.5, "size_cm": 3, "confidence": 0.9})
    add("RiskMeter", risk_meter(p), k + " fresh"); add("RescuePlan", rescue_plan(p, PRAE_KIT + ["alcohol", "brush"]), k + " full kit")
for f in FABRICS:
    add("RiskMeter", risk_meter(parse_stain(dict(TEA_RAW, fabric=f))), "tea on " + f)
add("RescuePlan", rescue_plan(TEA, ["dish_soap", "white_vinegar"]), "vinegar substitute")
add("RescuePlan", rescue_plan(TEA, []), "empty kit → shopping")
for kit, note in ((PRAE_KIT, "prae"), (["chlorine_bleach", "white_vinegar"], "danger"), (["chlorine_bleach", "ammonia", "alcohol"], "danger x2"), (["hydrogen_peroxide", "white_vinegar"], "peroxide+vinegar")):
    add("SafetyCheck", safety_check(kit), note)
for codes, note in ((SHIRT_LABEL, "shirt"), (SILK_LABEL, "silk"), (["no_wash", "dry_clean"], "dry clean only"), (["wash_60", "tumble_low"], "towel")):
    add("CareLabel", care_label(codes), note)
add("LabelFit", plan_fits_label(rescue_plan(TEA, PRAE_KIT), care_label(SHIRT_LABEL)), "fits")
add("LabelFit", plan_fits_label(rescue_plan(TEA, PRAE_KIT), care_label(["wash_30", "no_bleach"])), "no bleach")
add("KitCheck", kit_check(PRAE_KIT), "prae"); add("KitCheck", kit_check(PRAE_KIT + ["alcohol", "brush"]), "full"); add("KitCheck", kit_check([]), "empty")
for e in DIARY:
    add("DiaryEntry", e, e["item_th"])
add("DiarySummary", diary_summary(DIARY), "prae diary")
add("ShareCard", share_card("เสื้อนักศึกษาขาว", "ชาไทย", 70), "demo")
add("ShareCard", share_card("กางเกงยีนส์", "โคลน", 70), "mud")
for a in ((0, 1), (2, 1), (3, 1), (1, 5), (9, 5, True)):
    add("Quota", quota(*a), str(a))
add("SafetyGuard", safety_guard(), "ok"); add("SafetyGuard", safety_guard("danger"), "stop")
add("ScanQuality", scan_quality(0.62, 0.48, 0.55), "bad")

for e in ex:
    jsonschema.validate(e["value"], ref(e["def"]))
d = os.path.dirname(os.path.abspath(__file__)) + "/.."
json.dump(schema, open(d + "/schemas.json", "w"), ensure_ascii=False, indent=1)
json.dump({"examples": ex}, open(d + "/examples.json", "w"), ensure_ascii=False, indent=1)
print(len(defs), "defs,", len(ex), "examples, all valid")
