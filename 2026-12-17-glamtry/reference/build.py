"""Generate ../schemas.json + ../examples.json and validate every example."""
import json, os, jsonschema
from glamtry import *
from fixtures import *

S = "https://json-schema.org/draft/2020-12/schema"
s = {"type": "string"}; b = {"type": "boolean"}
u = {"type": "number", "minimum": 0, "maximum": 1}
i0 = {"type": "integer", "minimum": 0}; i1 = {"type": "integer", "minimum": 1}
pct = {"type": "integer", "minimum": 0, "maximum": 100}
hexc = {"type": "string", "pattern": "^#[0-9A-F]{6}$"}
date = {"type": "string", "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}$"}
look = {"enum": list(LOOKS)}; tone = {"enum": list(UNDERTONES)}; dep = {"enum": list(DEPTHS)}; inten = {"enum": list(INTENSITY)}
item = {"enum": list(ITEMS)}; tier = {"enum": list(TIERS)}; flag = {"enum": [k for k in GUARD if k]}

def obj(req, props, **kw):
    return {"type": "object", "required": req, "properties": props, "additionalProperties": False, **kw}
def arr(i, **kw):
    return {"type": "array", "items": i, **kw}
R = lambda n: {"$ref": f"#/$defs/{n}"}
nul = lambda x: {"anyOf": [x, {"type": "null"}]}

defs = {
 "Person": obj(["id", "name_th", "age", "skill"], {"id": {"type": "string", "pattern": "^u[0-9]{2}$"}, "name_th": s, "name_en": s, "age": {"type": "integer", "minimum": 13}, "city_th": s, "skill": {"type": "integer", "minimum": 1, "maximum": 3}}),
 "SelfiePhoto": obj(["id", "light", "blur", "tilt"], {"id": {"type": "string", "pattern": "^p[0-9]{2}$"}, "light": u, "blur": u, "tilt": u, "filter_on": b}),
 "ScanQuality": obj(["score", "ok", "tips_th"], {"score": pct, "ok": b, "tips_th": arr(s)}),
 "SelfieScan": obj(["photo_id", "quality"], {"photo_id": s, "quality": R("ScanQuality")}),
 "AiFaceExtract": obj(["is_face", "faces", "cheek_rgb", "eye_shape", "filter_detected", "celebrity_like", "confidence"], {"is_face": b, "faces": i0,
    "cheek_rgb": nul(arr({"type": "integer", "minimum": 0, "maximum": 255}, minItems=3, maxItems=3)), "eye_shape": {"enum": ["monolid", "hooded", "double", "round", "almond", "unknown"]},
    "filter_detected": b, "celebrity_like": b, "confidence": u, "notes_th": s}),
 "ConsentCheck": obj(["allowed", "level", "flags", "messages_th"], {"allowed": b, "level": {"enum": ["ok", "warn", "stop"]}, "flags": arr(flag), "messages_th": arr(s, minItems=1)}),
 "ShadeMatch": obj(["skin_hex", "depth", "undertone", "shade_code", "label_th", "lip_suggestions_hex", "confidence", "is_estimate", "tip_th", "disclaimer_th"], {"skin_hex": hexc, "depth": dep,
    "undertone": tone, "shade_code": {"type": "string", "pattern": "^[1-5][CNWO]$"}, "label_th": s, "lip_suggestions_hex": arr(hexc, minItems=3, maxItems=3), "confidence": u,
    "is_estimate": {"const": True}, "tip_th": s, "disclaimer_th": s}),
 "LookPalette": obj(["look", "undertone", "intensity", "lip_hex", "blush_hex", "eye_hex", "liner_hex", "opacity", "finish"], {"look": look, "undertone": tone, "intensity": inten,
    "lip_hex": hexc, "blush_hex": hexc, "eye_hex": hexc, "liner_hex": nul(hexc), "opacity": u, "finish": {"enum": ["satin", "dewy", "matte", "glossy"]}}),
 "LookSpec": obj(["look", "depth", "undertone", "intensity", "palette", "minutes", "skill", "image_prompt", "title_th", "disclaimer_th"], {"look": look, "depth": dep, "undertone": tone,
    "intensity": inten, "palette": R("LookPalette"), "minutes": i1, "skill": {"type": "integer", "minimum": 1, "maximum": 3}, "image_prompt": s, "title_th": s, "disclaimer_th": s}),
 "TutorialStep": obj(["n", "item", "area", "item_th", "tip_th", "color_hex", "minutes"], {"n": i1, "item": item, "area": {"enum": ["base", "brow", "eye", "cheek", "lip", "finish"]},
    "item_th": s, "tip_th": s, "color_hex": nul(hexc), "minutes": i1}),
 "Tutorial": obj(["look", "steps", "total_minutes", "simplified", "note_th"], {"look": look, "steps": arr(R("TutorialStep"), minItems=1), "total_minutes": i1, "simplified": b, "note_th": s}),
 "KitItem": obj(["item", "item_th", "tier", "low_baht", "high_baht"], {"item": item, "item_th": s, "tier": tier, "low_baht": i1, "high_baht": i1}),
 "BudgetKit": obj(["look", "tier", "tier_th", "items", "skipped_owned", "low_baht", "high_baht", "save_vs_premium_baht", "dupe_tip_th", "disclaimer_th"], {"look": look, "tier": tier, "tier_th": s,
    "items": arr(R("KitItem")), "skipped_owned": arr(item), "low_baht": i0, "high_baht": i0, "save_vs_premium_baht": i0, "dupe_tip_th": s, "disclaimer_th": s}),
 "OccasionPlan": obj(["event", "event_th", "event_date", "days_left", "look", "hours_worn", "touch_up_kit", "timeline", "warning_th"], {"event": {"enum": list(EVENTS)}, "event_th": s,
    "event_date": date, "days_left": i0, "look": look, "hours_worn": i1, "touch_up_kit": arr({"enum": ["setting_spray", "blotting_paper", "touch_up_lip"]}),
    "timeline": arr(obj(["days_before", "task_th"], {"days_before": i0, "task_th": s}), minItems=1), "warning_th": nul(s)}),
 "PatchTest": obj(["level", "items", "steps_th", "note_th"], {"level": {"enum": ["info", "warn"]}, "items": arr(item), "steps_th": arr(s, minItems=3), "note_th": s}),
 "ReelShot": obj(["from_s", "to_s", "kind", "text_th"], {"from_s": i0, "to_s": i1, "kind": {"enum": ["before", "scan", "swipe", "compare", "cta"]}, "text_th": s}),
 "ReelPlan": obj(["seconds", "ratio", "music_bpm", "shots", "watermark"], {"seconds": {"type": "integer", "minimum": 15, "maximum": 30}, "ratio": {"enum": ["9:16"]}, "music_bpm": i1,
    "shots": arr(R("ReelShot"), minItems=5, maxItems=5), "watermark": s}),
 "DiaryEntry": obj(["date", "kind"], {"date": date, "kind": {"enum": ["try", "wear", "buy", "open", "photo"]}, "look": look, "item": item, "cost_baht": i0, "note_th": s}),
 "DiarySummary": obj(["entries", "looks_saved", "top_look", "spend_baht", "replace_soon", "headline_th", "note_th"], {"entries": i1, "looks_saved": i0, "top_look": nul(look), "spend_baht": i0,
    "replace_soon": arr(obj(["item", "replace_by", "days_left"], {"item": item, "replace_by": date, "days_left": {"type": "integer"}})), "headline_th": s, "note_th": s}),
 "ShareCard": obj(["title_th", "hook_th", "layout", "sizes", "watermark", "cta_th", "disclaimer_th"], {"title_th": s, "hook_th": s, "layout": {"enum": ["selfie_before_after", "six_look_grid"]},
    "sizes": arr({"enum": ["1080x1350", "1080x1920", "1080x1080"]}), "watermark": s, "cta_th": s, "disclaimer_th": s}),
 "Quota": obj(["allowed", "left_after", "paywall"], {"allowed": i0, "left_after": {"type": ["integer", "null"], "minimum": 0}, "paywall": b}),
 "SafetyGuard": obj(["level", "message_th"], {"level": {"enum": ["ok", "warn", "stop"]}, "message_th": s}),
}
schema = {"$schema": S, "$id": "https://example.com/glamtry.schema.json", "title": "GlamTry", "$defs": defs}
def ref(n):
    return {"$ref": f"#/$defs/{n}", "$defs": defs}

ex = []
def add(n, v, note=""):
    ex.append({"def": n, "note": note, "value": v})

for p in PEOPLE: add("Person", p, p["name_en"])
for ph in PHOTOS: add("SelfiePhoto", ph, ph["id"]); add("SelfieScan", selfie_scan(ph), ph["id"])
add("ScanQuality", scan_quality(0.7, 0.2, 0.2), "mid")
add("AiFaceExtract", {"is_face": True, "faces": 1, "cheek_rgb": [214, 170, 140], "eye_shape": "hooded", "filter_detected": False, "celebrity_like": False, "confidence": 0.91, "notes_th": "หน้าตรง แสงหน้าต่าง"}, "demo Fern")
add("AiFaceExtract", {"is_face": True, "faces": 3, "cheek_rgb": [180, 150, 95], "eye_shape": "monolid", "filter_detected": True, "celebrity_like": False, "confidence": 0.72}, "group + filter")
add("AiFaceExtract", {"is_face": False, "faces": 0, "cheek_rgb": None, "eye_shape": "unknown", "filter_detected": False, "celebrity_like": False, "confidence": 0.95, "notes_th": "รูปนี้เป็นตุ๊กตา"}, "no face")
for a in ((24, True), (12, True), (25, False, 1, True), (20, True, 3), (20, True, 0), (19, True, 1, False, True)):
    add("ConsentCheck", consent_check(*a), str(a))
for rgb, q in (((214, 170, 140), 94), ((240, 215, 200), 90), ((205, 170, 150), 88), ((180, 150, 95), 85), ((150, 110, 85), 92), ((110, 75, 60), 90), ((200, 190, 150), 80), ((205, 170, 150), 40)):
    add("ShadeMatch", shade_match(rgb, q), f"{rgb} q{q}")
for lk in LOOKS:
    for t in UNDERTONES:
        add("LookPalette", look_palette(lk, t), f"{lk} {t}")
for sp in LOOKS6: add("LookSpec", sp, f"demo {sp['look']}")
for lk, d, t, i in (("natural", "deep", "neutral", "soft"), ("thai_bride", "tan", "warm", "full"), ("y2k", "fair", "cool", "full"), ("office", "medium", "olive", "medium")):
    add("LookSpec", look_spec(lk, d, t, i), f"{lk} {d} {t} {i}")
for lk in LOOKS:
    tu = tutorial(lk, "warm"); add("Tutorial", tu, lk)
add("Tutorial", tutorial("party_glam", skill=1), "party simplified")
for st in TUT["steps"]: add("TutorialStep", st, st["item"])
for lk in LOOKS:
    for tr in TIERS:
        add("BudgetKit", budget_kit(lk, tr), f"{lk} {tr}")
add("BudgetKit", KIT, "demo owned concealer")
for it in KIT["items"]: add("KitItem", it, it["item"])
add("OccasionPlan", PLAN, "demo wedding guest")
for ev, dt, o, h in (("own_wedding", "2027-02-14", True, True), ("interview", TODAY, False, False), ("concert", "2026-12-31", True, True), ("office_day", "2026-12-18", False, True)):
    add("OccasionPlan", occasion_plan(ev, dt, TODAY, o, h), ev)
add("PatchTest", PATCH, "demo"); add("PatchTest", patch_test(["lip_tint"]), "info"); add("PatchTest", patch_test(["lipstick"], known_allergies=("น้ำหอม",)), "allergy")
add("ReelPlan", REEL, "20s"); add("ReelPlan", reel_plan(LOOKS6[2], 15), "15s bride"); add("ReelPlan", reel_plan(LOOKS6[5], 30), "30s y2k")
for sh in REEL["shots"]: add("ReelShot", sh, sh["kind"])
for dd in DIARY: add("DiaryEntry", dd, dd["kind"])
add("DiarySummary", diary_summary(DIARY, "2027-01-05"), "fern")
add("DiarySummary", diary_summary([{"date": "2026-12-17", "kind": "photo"}], TODAY), "empty-ish")
add("ShareCard", share_card(SPEC, "เซลฟี่เดียว ลองแต่งหน้าก่อนซื้อ"), "demo")
sc = share_card(LOOKS6[0], "6 ลุคจากเซลฟี่เดียว"); sc["layout"] = "six_look_grid"; add("ShareCard", sc, "grid")
for a in ((0,), (2,), (3,), (9, 3, True)): add("Quota", quota(*a), str(a))
for f in GUARD: add("SafetyGuard", safety_guard(f), str(f))

for x in ex: jsonschema.validate(x["value"], ref(x["def"]))
d = os.path.dirname(os.path.abspath(__file__)) + "/.."
json.dump(schema, open(d + "/schemas.json", "w"), ensure_ascii=False, indent=1)
json.dump({"examples": ex}, open(d + "/examples.json", "w"), ensure_ascii=False, indent=1)
print(len(defs), "defs,", len(ex), "examples, all valid")
