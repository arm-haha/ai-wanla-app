"""Generate ../schemas.json + ../examples.json and validate every example."""
import json, os, jsonschema
from tinysteps import *
from fixtures import *

S = "https://json-schema.org/draft/2020-12/schema"
s = {"type": "string"}
b = {"type": "boolean"}
u = {"type": "number", "minimum": 0, "maximum": 1}
i0 = {"type": "integer", "minimum": 0}
i1 = {"type": "integer", "minimum": 1}
pct = {"type": "integer", "minimum": 0, "maximum": 100}
kind = {"enum": list(FIRSTS)}
pos = {"enum": ["below", "in", "above"]}
nullint = {"type": ["integer", "null"], "minimum": 0}

def obj(req, props, **kw):
    return {"type": "object", "required": req, "properties": props, "additionalProperties": False, **kw}

def arr(i, **kw):
    return {"type": "array", "items": i, **kw}

defs = {
 "Person": obj(["id", "name_th", "age", "own_child", "parent_confirmed"], {
    "id": {"type": "string", "pattern": "^u[0-9]{2}$"}, "name_th": s, "name_en": s, "age": i1,
    "city_th": s, "relation_th": s, "own_child": b, "parent_confirmed": b, "all_guardians_ok": b}),
 "Child": obj(["id", "name_th", "birth", "weight_kg", "height_cm"], {
    "id": {"type": "string", "pattern": "^c[0-9]{2}$"}, "name_th": s, "name_en": s, "birth": s,
    "weight_kg": {"type": "number", "exclusiveMinimum": 0}, "height_cm": {"type": "number", "exclusiveMinimum": 0}}),
 "MilestonePhoto": obj(["id", "px_w", "px_h", "glare", "blur", "crop", "child_id"], {
    "id": {"type": "string", "pattern": "^p[0-9]{2}$"}, "px_w": i1, "px_h": i1,
    "glare": u, "blur": u, "crop": u, "child_id": s}),
 "ScanQuality": obj(["score", "ok", "tips_th"], {"score": pct, "ok": b, "tips_th": arr(s)}),
 "PhotoScan": obj(["photo_id", "quality"], {"photo_id": s, "quality": {"$ref": "#/$defs/ScanQuality"}, "child_id": s}),
 "Pipeline": obj(["photo_id", "steps"], {"photo_id": s, "steps": arr(s, minItems=1)}),
 "ExampleBand": obj(["month", "weight_lo_kg", "weight_mid_kg", "weight_hi_kg", "height_lo_cm", "height_mid_cm", "height_hi_cm", "disclaimer_th"], {
    "month": i0, "weight_lo_kg": {"type": "number"}, "weight_mid_kg": {"type": "number"}, "weight_hi_kg": {"type": "number"},
    "height_lo_cm": {"type": "number"}, "height_mid_cm": {"type": "number"}, "height_hi_cm": {"type": "number"}, "disclaimer_th": s}),
 "GrowthEntry": obj(["month", "weight_kg", "height_cm", "weight_pos", "height_pos", "weight_label_th", "height_label_th", "band", "disclaimer_th"], {
    "month": i0, "weight_kg": {"type": "number"}, "height_cm": {"type": "number"},
    "weight_pos": pos, "height_pos": pos, "weight_label_th": s, "height_label_th": s,
    "band": {"$ref": "#/$defs/ExampleBand"}, "disclaimer_th": s}),
 "FirstInfo": obj(["id", "kind", "name_th", "example_month", "range_lo", "range_hi", "disclaimer_th"], {
    "id": {"type": "string", "pattern": "^f[0-9]{2}$"}, "kind": kind, "name_th": s,
    "example_month": i0, "range_lo": i0, "range_hi": i0, "disclaimer_th": s}),
 "LoggedFirst": obj(["id", "kind", "name_th", "logged_month", "flag", "tip_th"], {
    "id": s, "kind": kind, "name_th": s, "example_month": i0, "range_lo": i0, "range_hi": i0,
    "disclaimer_th": s, "logged_month": i0, "flag": {"enum": ["in_example", "outside_example"]},
    "tip_th": s, "note_th": s}),
 "Timeline": obj(["count", "entries", "disclaimer_th"], {
    "count": i1, "entries": arr({"$ref": "#/$defs/LoggedFirst"}, minItems=1), "disclaimer_th": s}),
 "Caption": obj(["n", "kind", "for_name_th", "text_th"], {"n": i1, "kind": kind, "for_name_th": s, "text_th": s}),
 "MilestoneCard": obj(["photo_id", "name_th", "month", "kind", "title_th", "caption_th", "layout", "sizes", "watermark", "disclaimer_th", "headline_th"], {
    "photo_id": s, "name_th": s, "month": i0, "kind": kind, "title_th": s, "caption_th": s,
    "layout": {"enum": ["month_card"]}, "sizes": arr(s, minItems=1), "watermark": s, "disclaimer_th": s, "headline_th": s}),
 "MonthIdeas": obj(["month", "ideas_th", "disclaimer_th"], {"month": i0, "ideas_th": arr(s, minItems=1), "disclaimer_th": s}),
 "CollageSlot": obj(["photo_id", "month", "label_th"], {"photo_id": s, "month": i1, "label_th": s}),
 "Collage": obj(["title_th", "slots", "count", "cols", "rows", "disclaimer_th", "layout"], {
    "title_th": s, "slots": arr({"$ref": "#/$defs/CollageSlot"}, minItems=1),
    "count": i1, "cols": i1, "rows": i1, "disclaimer_th": s, "layout": {"enum": ["monthly_grid"]}}),
 "PrintSheet": obj(["name_th", "month", "caption_th", "layout", "label_th", "sizes", "bleed_mm", "watermark"], {
    "name_th": s, "month": i0, "caption_th": s, "layout": {"enum": ["portrait_a4", "book_20", "collage_a4"]},
    "label_th": s, "sizes": arr(s), "bleed_mm": i0, "watermark": s}),
 "ShareCard": obj(["title_th", "headline_th", "hook_th", "caption_th", "month", "kind", "layout", "sizes", "watermark", "cta_th", "disclaimer_th"], {
    "title_th": s, "headline_th": s, "hook_th": s, "caption_th": s, "month": i0, "kind": kind,
    "layout": {"enum": ["milestone_card"]}, "sizes": arr({"enum": ["1080x1350", "1080x1920", "1080x1080"]}),
    "watermark": s, "cta_th": s, "disclaimer_th": s}),
 "ConsentGuard": obj(["ok", "level", "blocks_th", "message_th", "disclaimer_th"], {
    "ok": b, "level": {"enum": ["ok", "block"]}, "blocks_th": arr(s), "message_th": s, "disclaimer_th": s}),
 "Quota": obj(["allowed", "left_after", "paywall"], {"allowed": i0, "left_after": {"type": ["integer", "null"], "minimum": 0}, "paywall": b}),
 "SafetyGuard": obj(["level", "message_th"], {"level": {"enum": ["ok", "warn", "stop"]}, "message_th": s}),
}
schema = {"$schema": S, "$id": "https://example.com/tinysteps.schema.json", "title": "TinySteps", "$defs": defs}

def ref(n):
    return {"$ref": f"#/$defs/{n}", "$defs": defs}

ex = []
def add(n, v, note=""):
    ex.append({"def": n, "note": note, "value": v})

for p in PEOPLE:
    slim = {k: p[k] for k in ("id", "name_th", "name_en", "age", "city_th", "relation_th", "own_child", "parent_confirmed", "all_guardians_ok")}
    add("Person", slim, p["name_th"])
    ch = p["child"]
    add("Child", {k: ch[k] for k in ("id", "name_th", "name_en", "birth", "weight_kg", "height_cm")}, ch["name_th"])

for ph in PHOTOS:
    add("MilestonePhoto", ph, ph["id"])
    add("PhotoScan", photo_scan(ph), ph["id"])
    add("Pipeline", {"photo_id": ph["id"], "steps": pipeline_steps(ph)}, ph["id"])
add("ScanQuality", scan_quality(0.62, 0.48, 0.55), "bad")

for m in (0, 1, 8, 12, 24, 36):
    add("ExampleBand", example_band(m), f"m{m}")
add("GrowthEntry", growth_entry(8, 8.4, 70.0), "phu in")
add("GrowthEntry", growth_entry(8, 6.0, 76.0), "below/above")
add("GrowthEntry", growth_entry(12, 9.8, 76.0), "phai")
add("GrowthEntry", growth_entry(0, 3.2, 50.0), "newborn mid")

for k in FIRST_IDS:
    add("FirstInfo", first_info(k), k)
    add("LoggedFirst", log_first(k, FIRSTS[k]["example_month"]), f"{k} in")

add("LoggedFirst", log_first("sit", 14, "นอกช่วงตัวอย่าง"), "sit outside")
add("LoggedFirst", log_first("walk", 20), "walk outside")
entries = [log_first(k, m, n) for k, m, n in PHU_FIRSTS]
add("Timeline", timeline(entries), "phu three")
add("Timeline", timeline([log_first("wave", 10), log_first("stand", 10)]), "tie")

for k, who in (("sit", "น้องภู"), ("smile", "น้องภู"), ("roll", "น้องไผ่"), ("word", "น้องไผ่"), ("walk", "น้องภู")):
    for q in captions(k, who, 2):
        add("Caption", q, f"{who} {k} {q['n']}")

add("MilestoneCard", milestone_card("น้องภู", 8, "sit", "p01"), "phu sit")
add("MilestoneCard", milestone_card("น้องไผ่", 12, "word", "p02"), "phai word")
for m in (1, 8, 12, 3):
    add("MonthIdeas", month_ideas(m), f"ideas {m}")
for sl in PHU_COLLAGE:
    add("CollageSlot", sl, sl["photo_id"])
add("Collage", collage("อัลบั้มน้องภู 8 เดือน", PHU_COLLAGE), "8 months")
add("Collage", collage("สี่เดือนแรก", PHU_COLLAGE[:4]), "four")
cap = captions("sit", "น้องภู", 1)[0]["text_th"]
add("PrintSheet", print_sheet("น้องภู", 8, cap, "portrait_a4"), "a4")
add("PrintSheet", print_sheet("น้องภู", 8, cap, "book_20"), "book")
add("PrintSheet", print_sheet("น้องภู", 8, cap, "collage_a4"), "collage")
add("ShareCard", share_card("น้องภู", 8, "sit", cap), "phu")
add("ShareCard", share_card("น้องไผ่", 12, "word", captions("word", "น้องไผ่", 1)[0]["text_th"]), "phai")
add("ConsentGuard", consent_guard(True, True, 31, True), "ok")
add("ConsentGuard", consent_guard(False, True, 31), "not own")
add("ConsentGuard", consent_guard(True, False, 31), "no confirm")
add("ConsentGuard", consent_guard(True, True, 16), "teen parent")
add("ConsentGuard", consent_guard(True, True, None), "no age")
add("Quota", quota(1, 1), "free")
add("Quota", quota(3, 1), "exhausted")
add("Quota", quota(0, 5, pro=True), "pro")
add("SafetyGuard", safety_guard(True), "ok")
add("SafetyGuard", safety_guard(False), "stop")

for e in ex:
    jsonschema.validate(e["value"], ref(e["def"]))

d = os.path.dirname(os.path.abspath(__file__)) + "/.."
json.dump(schema, open(d + "/schemas.json", "w"), ensure_ascii=False, indent=1)
json.dump({"examples": ex}, open(d + "/examples.json", "w"), ensure_ascii=False, indent=1)
print(len(defs), "defs,", len(ex), "examples, all valid")
