"""Generate ../schemas.json + ../examples.json and validate every example."""
import json, os, jsonschema
from cardready import *
from fixtures import *

S = "https://json-schema.org/draft/2020-12/schema"
s = {"type": "string"}
b = {"type": "boolean"}
n0 = {"type": "number", "minimum": 0}
u = {"type": "number", "minimum": 0, "maximum": 1}
i0 = {"type": "integer", "minimum": 0}
i1 = {"type": "integer", "minimum": 1}

def obj(req, props, **kw):
    return {"type": "object", "required": req, "properties": props, "additionalProperties": False, **kw}

def arr(i, **kw):
    return {"type": "array", "items": i, **kw}

mess = obj(list(MESS_W), {k: u for k in MESS_W})
face = obj(["cx", "cy", "h", "eyes_open", "neutral", "front"], {
    "cx": u, "cy": u, "h": u, "eyes_open": b, "neutral": b, "front": b,
})
size_keys = {"enum": list(SIZE_PRESETS.keys())}
bg_presets = {"enum": list(BG_PRESETS.keys()) + ["custom"]}
doc_enum = {"enum": DOC_TYPES}
pass_lv = {"enum": [l[1] for l in PASS_LEVELS]}

defs = {
 "Selfie": obj(
    ["id", "name_th", "age", "doc_type", "px_w", "px_h", "face", "mess", "target_size", "target_bg"],
    {"id": {"type": "string", "pattern": "^s[0-9]{2,}$"}, "name_th": s, "name_en": s, "age": i1,
     "city_th": s, "purpose_th": s, "doc_type": doc_enum,
     "px_w": i1, "px_h": i1, "face": {"$ref": "#/$defs/FaceBox"}, "mess": mess,
     "target_size": size_keys, "target_bg": s, "soft_light": b, "print_copies": i1}),
 "FaceBox": face,
 "SizeSpec": obj(["key", "label_th", "mm_w", "mm_h", "dpi", "px_w", "px_h", "docs"], {
    "key": size_keys, "label_th": s, "mm_w": n0, "mm_h": n0, "dpi": i1, "px_w": i1, "px_h": i1,
    "docs": arr(doc_enum)}),
 "BgChoice": obj(["preset", "hex", "label_th", "custom"], {
    "preset": bg_presets, "hex": {"type": "string", "pattern": "^#[0-9A-F]{6}$"},
    "label_th": s, "custom": b}),
 "CropBox": obj(["x0", "y0", "x1", "y1", "out_px_w", "out_px_h", "size_key", "aspect"], {
    "x0": i0, "y0": i0, "x1": i1, "y1": i1, "out_px_w": i1, "out_px_h": i1,
    "size_key": size_keys, "aspect": n0}),
 "PassReport": obj(["selfie_id", "score", "level", "level_th"], {
    "selfie_id": s, "score": {"type": "integer", "minimum": 0, "maximum": 100},
    "level": pass_lv, "level_th": s}),
 "SoftLightPlan": obj(["strength", "blemish_calm", "even_lighting", "reshape", "plastic_beauty", "whitelist", "blocked"], {
    "strength": u, "blemish_calm": u, "even_lighting": b, "reshape": {"const": False},
    "plastic_beauty": {"const": False}, "whitelist": arr(s), "blocked": arr(s)}),
 "DpiCheck": obj(["dpi", "ok", "min_dpi"], {"dpi": i0, "ok": b, "min_dpi": i1}),
 "PrintSheet": obj(
    ["size_key", "copies_requested", "copies_placed", "capacity", "rows", "cols",
     "margin_mm", "gap_mm", "a4_px_w", "a4_px_h", "cut_guides", "dpi_check", "positions"],
    {"size_key": size_keys, "copies_requested": i1, "copies_placed": i0, "capacity": i1,
     "rows": i1, "cols": i1, "margin_mm": n0, "gap_mm": n0, "a4_px_w": i1, "a4_px_h": i1,
     "cut_guides": b, "dpi_check": {"$ref": "#/$defs/DpiCheck"},
     "positions": arr(obj(["index", "x_mm", "y_mm", "w_mm", "h_mm"], {
        "index": i1, "x_mm": n0, "y_mm": n0, "w_mm": n0, "h_mm": n0}))}),
 "CheckItem": obj(["id", "label_th", "pass"], {"id": s, "label_th": s, "pass": b}),
 "DocChecklist": obj(
    ["doc_type", "label_th", "preferred_size", "preferred_bg", "items", "passed", "total", "meter", "level", "disclaimer_th"],
    {"doc_type": doc_enum, "label_th": s, "preferred_size": size_keys, "preferred_bg": s,
     "items": arr({"$ref": "#/$defs/CheckItem"}), "passed": i0, "total": i1,
     "meter": {"type": "integer", "minimum": 0, "maximum": 100},
     "level": {"enum": ["pass", "warn", "fail"]}, "disclaimer_th": s}),
 "ExportPack": obj(["files", "watermark", "count"], {
    "files": arr(obj(["format", "filename", "px_w", "px_h", "dpi", "bg_alpha"], {
        "format": {"enum": ["jpg", "png", "pdf"]}, "filename": s, "px_w": i1, "px_h": i1,
        "dpi": i1, "bg_alpha": b})),
    "watermark": s, "count": i0}),
 "ShareCard": obj(["title_th", "headline_th", "hook_th", "badges", "watermark", "cta_th", "size_label_th", "pass_score"], {
    "title_th": s, "headline_th": s, "hook_th": s, "badges": arr(s), "watermark": s,
    "cta_th": s, "size_label_th": s, "pass_score": {"type": "integer", "minimum": 0, "maximum": 100}}),
 "HistoryEntry": obj(["photo_id", "size_key", "bg", "pass_score", "created_at", "on_device"], {
    "photo_id": s, "size_key": size_keys, "bg": {"$ref": "#/$defs/BgChoice"},
    "pass_score": {"type": "integer", "minimum": 0, "maximum": 100},
    "created_at": s, "on_device": {"const": True}}),
 "BatchProfiles": obj(["count", "members", "note_th"], {
    "count": i0,
    "members": arr(obj(["id", "name_th", "relation_th"], {"id": s, "name_th": s, "relation_th": s})),
    "note_th": s}),
 "Quota": obj(["allowed", "left_after", "paywall"], {
    "allowed": i0, "left_after": {"type": ["integer", "null"], "minimum": 0}, "paywall": b}),
 "Pipeline": obj(["selfie_id", "steps"], {"selfie_id": s, "steps": arr(s, minItems=1)}),
}

schema = {"$schema": S, "$id": "https://example.com/cardready.schema.json", "title": "CardReady", "$defs": defs}

def ref(n):
    return {"$ref": f"#/$defs/{n}", "$defs": defs}

ex = []
def add(n, v, note=""):
    ex.append({"def": n, "note": note, "value": v})

# Selfies + FaceBox + PassReport + Crop + Pipeline for each
for sl in SELFIES:
    face_v = sl["face"]
    add("Selfie", {k: sl[k] for k in sl if k in (
        "id", "name_th", "name_en", "age", "city_th", "purpose_th", "doc_type",
        "px_w", "px_h", "face", "mess", "target_size", "target_bg", "soft_light", "print_copies")}, sl["name_th"])
    add("FaceBox", face_v, sl["id"])
    sc, lv, th = pass_score(sl["mess"], soft_light_on=sl.get("soft_light", True), bg_removed=True, size_ok=True)
    add("PassReport", {"selfie_id": sl["id"], "score": sc, "level": lv, "level_th": th}, f"{sl['id']} after")
    sc0, lv0, th0 = pass_score(sl["mess"], soft_light_on=False, bg_removed=False, size_ok=False)
    add("PassReport", {"selfie_id": sl["id"], "score": sc0, "level": lv0, "level_th": th0}, f"{sl['id']} raw")
    box = id_crop_box(sl["px_w"], sl["px_h"], face_v["cx"], face_v["cy"], face_v["h"], sl["target_size"])
    add("CropBox", box, sl["id"])
    add("Pipeline", {"selfie_id": sl["id"], "steps": pipeline_steps(sl["mess"], sl.get("soft_light", True))}, sl["id"])

# Size presets
for p in list_size_presets():
    add("SizeSpec", p, p["key"])

# BG choices
for k in BG_PRESETS:
    add("BgChoice", resolve_bg_safe(k), k)
add("BgChoice", resolve_bg_safe("#E8F3FF"), "custom sky")

# Soft light
add("SoftLightPlan", soft_light_plan(0.30, 0.15), "mint default")
add("SoftLightPlan", soft_light_plan(0.9, 0.9), "clamped")

# Dpi
add("DpiCheck", dpi_check(295, 413, 25.0, 35.0), "1 inch @300")
add("DpiCheck", dpi_check(150, 210, 25.0, 35.0, min_dpi=300), "too low")

# Print sheets
add("PrintSheet", print_sheet_layout("1_inch", 8), "mint 8 copies")
add("PrintSheet", print_sheet_layout("passport", 4), "passport 4")
add("PrintSheet", print_sheet_layout("2_inch", 6), "2 inch 6")

# Checklists
add("DocChecklist", doc_checklist("job_th", MINT_SIGNALS), "mint job pass")
add("DocChecklist", doc_checklist("passport", {
    "face_front": True, "eyes_open": True, "neutral": True, "even_light": True,
    "bg_plain": True, "no_hat": True, "no_glasses_tint": True, "head_ratio": True, "ears_visible": False,
}), "passport warn ears")
add("DocChecklist", doc_checklist("national_id", {
    "face_front": True, "eyes_open": True, "neutral": True, "even_light": False,
    "bg_plain": False, "no_hat": True, "no_glasses_tint": True, "head_ratio": True,
}), "national_id partial")
add("DocChecklist", doc_checklist("student", {
    "face_front": True, "eyes_open": True, "neutral": False, "even_light": True,
    "bg_plain": True, "no_hat": True,
}), "student smile")
add("DocChecklist", doc_checklist("visa", {}), "visa empty fail")

# Export / share / history / batch / quota
add("ExportPack", export_pack(["jpg", "png"], "1_inch", True), "mint export")
add("ExportPack", export_pack(["jpg"], "passport", False), "passport jpg only")
add("ShareCard", share_card("น้องมิ้นท์", "1_inch", 92, "ขาว"), "mint share")
add("ShareCard", share_card("คุณก้อง", "passport", 88, "ขาว"), "kong share")
add("HistoryEntry", history_entry("s01", "1_inch", "white", 92, NOW), "mint vault")
add("HistoryEntry", history_entry("s02", "passport", "white", 88, NOW), "kong vault")
add("HistoryEntry", history_entry("s03", "1_inch", "gov_blue", 70, NOW), "fai vault")
add("BatchProfiles", batch_profiles(FAMILY_BATCH), "mint family")
add("Quota", quota(2, 3), "free day")
add("Quota", quota(5, 1), "exhausted")
add("Quota", quota(0, 5, pro=True), "pro")

for e in ex:
    jsonschema.validate(e["value"], ref(e["def"]))

d = os.path.dirname(os.path.abspath(__file__)) + "/.."
json.dump(schema, open(d + "/schemas.json", "w"), ensure_ascii=False, indent=1)
json.dump({"examples": ex}, open(d + "/examples.json", "w"), ensure_ascii=False, indent=1)
print(len(defs), "defs,", len(ex), "examples, all valid")
