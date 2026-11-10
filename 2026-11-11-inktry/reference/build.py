"""Generate ../schemas.json + ../examples.json and validate every example."""
import json, os, jsonschema
from inktry import *
from fixtures import *

S = "https://json-schema.org/draft/2020-12/schema"
s = {"type": "string"}
b = {"type": "boolean"}
n0 = {"type": "number", "minimum": 0}
u = {"type": "number", "minimum": 0, "maximum": 1}
i0 = {"type": "integer", "minimum": 0}
i1 = {"type": "integer", "minimum": 1}
pct = {"type": "integer", "minimum": 0, "maximum": 100}
date = {"type": "string", "format": "date", "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}$"}
pl = {"enum": list(PLACEMENTS)}
st = {"enum": list(STYLES)}
mode = {"enum": COLOR_MODES}
region = {"enum": list(REGION_MULT)}
under = {"enum": UNDERTONES}
level = {"enum": list(LEVELS)}
did = {"enum": list(DESIGNS)}
side = {"enum": ["left", "right", "unknown"]}
flag = {"enum": list(CONTRA)}

def obj(req, props, **kw):
    return {"type": "object", "required": req, "properties": props, "additionalProperties": False, **kw}

def arr(i, **kw):
    return {"type": "array", "items": i, **kw}

defs = {
 "Person": obj(["id", "name_th", "age", "region"], {
    "id": {"type": "string", "pattern": "^u[0-9]{2}$"}, "name_th": s, "name_en": s, "age": i1,
    "city_th": s, "goal_th": s, "region": region}),
 "Detection": obj(["placement", "confidence"], {"placement": pl, "confidence": u, "side": side}),
 "SkinPhoto": obj(["id", "px_w", "px_h", "glare", "blur", "tilt", "skin_visible", "undertone", "detections"], {
    "id": {"type": "string", "pattern": "^p[0-9]{2}$"}, "px_w": i1, "px_h": i1, "glare": u, "blur": u, "tilt": u,
    "skin_visible": u, "undertone": under, "detections": arr({"$ref": "#/$defs/Detection"})}),
 "ScanQuality": obj(["score", "ok", "tips_th"], {"score": pct, "ok": b, "tips_th": arr(s)}),
 "IdentifiedPlacement": obj(["placement", "name_th", "name_en", "confidence"], {
    "placement": pl, "name_th": s, "name_en": s, "confidence": u, "side": side}),
 "SkinScan": obj(["photo_id", "quality", "placements", "uncertain", "placement_count", "undertone"], {
    "photo_id": s, "quality": {"$ref": "#/$defs/ScanQuality"}, "placements": arr({"$ref": "#/$defs/IdentifiedPlacement"}),
    "uncertain": arr(pl), "placement_count": i0, "undertone": under}),
 "Pipeline": obj(["photo_id", "steps"], {"photo_id": s, "steps": arr(s, minItems=1)}),
 "PlacementInfo": obj(["id", "placement", "name_th", "name_en", "pain", "heal_days", "min_cm", "max_cm", "notes_th"], {
    "id": {"type": "string", "pattern": "^pl[0-9]{2}$"}, "placement": pl, "name_th": s, "name_en": s,
    "pain": {"type": "integer", "minimum": 0, "maximum": 10}, "heal_days": i1, "min_cm": n0, "max_cm": n0, "notes_th": s}),
 "DesignInfo": obj(["id", "name_th", "name_en", "style", "style_th", "default_mode", "tags", "color_ok", "bw_ok", "notes_th"], {
    "id": did, "name_th": s, "name_en": s, "style": st, "style_th": s, "default_mode": mode, "tags": arr(s),
    "color_ok": b, "bw_ok": b, "notes_th": s}),
 "SizeCheck": obj(["placement", "size_cm", "band", "band_th", "min_cm", "max_cm", "in_range", "verdict", "message_th", "wrap_th"], {
    "placement": pl, "size_cm": n0, "band": {"enum": ["tiny", "small", "medium", "large", "xl"]}, "band_th": s,
    "min_cm": n0, "max_cm": n0, "in_range": b, "verdict": {"enum": ["ok", "too_small", "too_big"]},
    "message_th": s, "wrap_th": s}),
 "ColorVariant": obj(["design_id", "style", "color_mode", "label_th", "contrast", "recommended"], {
    "design_id": did, "style": st, "color_mode": mode, "label_th": s, "contrast": pct, "recommended": b}),
 "ColorVariants": obj(["design_id", "name_th", "style", "undertone", "placement", "size_cm", "variants", "best_mode"], {
    "design_id": did, "name_th": s, "style": st, "undertone": under, "placement": pl, "size_cm": n0,
    "variants": arr({"$ref": "#/$defs/ColorVariant"}, minItems=1), "best_mode": mode}),
 "TryOn": obj(["photo_id", "design_id", "name_th", "placement", "placement_th", "size_cm", "style", "color_mode",
               "contrast", "size_verdict", "placement_matched", "quality", "watermark", "disclaimer_th"], {
    "photo_id": s, "design_id": did, "name_th": s, "placement": pl, "placement_th": s, "size_cm": n0, "style": st,
    "color_mode": mode, "contrast": pct, "size_verdict": {"enum": ["ok", "too_small", "too_big"]},
    "placement_matched": b, "quality": {"$ref": "#/$defs/ScanQuality"}, "watermark": s, "disclaimer_th": s}),
 "AgingPreview": obj(["style", "color_mode", "placement", "years", "size_cm", "fade_pct", "spread_mm", "sharpness_left", "look_th", "care_th", "disclaimer_th"], {
    "style": st, "color_mode": mode, "placement": pl, "years": i1, "size_cm": n0, "fade_pct": pct, "spread_mm": n0,
    "sharpness_left": pct, "look_th": s, "care_th": s, "disclaimer_th": s}),
 "PainGuide": obj(["placement", "name_th", "pain", "pain_max", "level", "heal_days", "tip_th", "notes_th", "disclaimer_th"], {
    "placement": pl, "name_th": s, "pain": {"type": "integer", "minimum": 0, "maximum": 10}, "pain_max": {"const": 10},
    "level": {"enum": ["low", "medium", "high"]}, "heal_days": i1, "tip_th": s, "notes_th": s, "disclaimer_th": s}),
 "AftercareGuide": obj(["title_th", "days", "steps", "disclaimer_th"], {
    "title_th": s, "days": i1, "steps": arr(obj(["n", "text_th"], {"n": i1, "text_th": s}), minItems=1), "disclaimer_th": s}),
 "PriceRange": obj(["style", "placement", "size_cm", "region", "color_mode", "mid_thb", "min_thb", "max_thb", "currency", "name_th", "disclaimer_th"], {
    "style": st, "placement": pl, "size_cm": n0, "region": region, "color_mode": mode, "mid_thb": i0, "min_thb": i0,
    "max_thb": i0, "currency": {"const": "THB"}, "name_th": s, "disclaimer_th": s}),
 "QuoteCheck": obj(["quote_thb", "min_thb", "max_thb", "mid_thb", "verdict", "message_th", "questions_th", "disclaimer_th"], {
    "quote_thb": i0, "min_thb": i0, "max_thb": i0, "mid_thb": i0,
    "verdict": {"enum": ["low", "fair", "high", "very_high"]}, "message_th": s,
    "questions_th": arr(s, minItems=1), "disclaimer_th": s}),
 "SafetyFlags": obj(["level", "can_book", "flags", "reasons_th", "disclaimer_th"], {
    "level": level, "can_book": b, "flags": arr(flag, minItems=1), "reasons_th": arr(s, minItems=1), "disclaimer_th": s}),
 "ArtistCard": obj(["title_th", "name_th", "design_th", "style", "color_mode", "placement", "placement_th", "size_cm",
                    "budget_min_thb", "budget_max_thb", "aging_5y_fade_pct", "note_th", "questions_th",
                    "line_share_url", "can_book", "disclaimer_th"], {
    "title_th": s, "name_th": s, "design_th": s, "style": st, "color_mode": mode, "placement": pl, "placement_th": s,
    "size_cm": n0, "budget_min_thb": i0, "budget_max_thb": i0, "aging_5y_fade_pct": pct, "note_th": s,
    "questions_th": arr(s), "line_share_url": {"type": "string", "pattern": "^https://line\\.me/R/share\\?text="},
    "can_book": b, "disclaimer_th": s}),
 "DiaryEntry": obj(["id", "person_id", "date", "design_id", "placement", "size_cm", "status", "shop_th", "cost_thb", "on_device"], {
    "id": s, "person_id": s, "date": date, "design_id": did, "placement": pl, "size_cm": n0,
    "status": {"enum": ["wishlist", "booked", "done", "touch_up"]}, "shop_th": s, "cost_thb": i0, "on_device": b}),
 "DiaryStats": obj(["count", "total_thb", "avg_thb", "last_date", "top_placement"], {
    "count": i0, "total_thb": i0, "avg_thb": i0, "last_date": {"type": ["string", "null"]},
    "top_placement": {"type": ["string", "null"]}}),
 "ShareCard": obj(["title_th", "headline_th", "hook_th", "placement", "style", "color_mode", "layout", "sizes", "watermark", "cta_th"], {
    "title_th": s, "headline_th": s, "hook_th": s, "placement": pl, "style": st, "color_mode": mode,
    "layout": {"enum": ["tryon_result"]}, "sizes": arr({"enum": ["1080x1350", "1080x1920", "1080x1080"]}),
    "watermark": s, "cta_th": s}),
 "Quota": obj(["allowed", "left_after", "paywall"], {
    "allowed": i0, "left_after": {"type": ["integer", "null"], "minimum": 0}, "paywall": b}),
 "SafetyGuard": obj(["level", "message_th"], {"level": {"enum": ["ok", "warn", "stop"]}, "message_th": s}),
}
schema = {"$schema": S, "$id": "https://example.com/inktry.schema.json", "title": "InkTry", "$defs": defs}

def ref(n):
    return {"$ref": f"#/$defs/{n}", "$defs": defs}

ex = []
def add(n, v, note=""):
    ex.append({"def": n, "note": note, "value": v})

for p in PEOPLE:
    add("Person", p, p["name_th"])
for ph in PHOTOS:
    add("SkinPhoto", ph, ph["id"])
    add("SkinScan", skin_scan(ph), ph["id"])
    add("Pipeline", {"photo_id": ph["id"], "steps": pipeline_steps(ph)}, ph["id"])

for k in ("inner_forearm", "wrist", "upper_arm", "ribs", "hand", "finger", "behind_ear", "ankle", "back", "nape", "shoulder", "collarbone", "calf"):
    add("PlacementInfo", placement_info(k), k)
for did_ in ("d01", "d02", "d05", "d07", "d08", "d09", "d10"):
    add("DesignInfo", design_info(did_), did_)

add("SizeCheck", size_check("inner_forearm", 8), "mint ok")
add("SizeCheck", size_check("inner_forearm", 3), "too small")
add("SizeCheck", size_check("wrist", 12), "too big")
add("SizeCheck", size_check("finger", 2), "finger ok")

add("ColorVariants", color_variants("d01", "warm", "inner_forearm", 8), "mint")
add("ColorVariants", color_variants("d02", "cool", "upper_arm", 14), "peony")
add("ColorVariants", color_variants("d09", "neutral", "calf", 10), "blackwork bw only")

t_mint = overlay_tryon(MINT_PHOTO, "d01", "inner_forearm", 8, "bw")
add("TryOn", t_mint, "mint olive")
add("TryOn", overlay_tryon(PHOTOS[1], "d11", "wrist", 5, "bw"), "petch vine")
add("TryOn", overlay_tryon(PHOTOS[2], "d05", "upper_arm", 16, "color"), "ekk dragon")
add("TryOn", overlay_tryon(PHOTOS[4], "d08", "hand", 6, "bw"), "ta cat")

for y in (1, 5, 10):
    add("AgingPreview", aging_preview("fine_line", "bw", "inner_forearm", y, 8), f"mint {y}y")
add("AgingPreview", aging_preview("fine_line", "bw", "hand", 5, 8), "hand fades")
add("AgingPreview", aging_preview("watercolor", "color", "inner_forearm", 5, 8), "watercolor color")
add("AgingPreview", aging_preview("traditional", "color", "upper_arm", 10, 16), "traditional 10y")

for k in ("inner_forearm", "ribs", "hand", "ankle", "thigh"):
    add("PainGuide", pain_guide(k), k)
add("AftercareGuide", aftercare_guide(), "standard")

pr_mint = price_range(8, "fine_line", "bkk", "bw", "inner_forearm")
add("PriceRange", pr_mint, "mint")
add("PriceRange", price_range(8, "fine_line", "province", "bw"), "province")
add("PriceRange", price_range(16, "traditional", "tourist", "color", "upper_arm"), "tourist dragon")
add("PriceRange", price_range(2, "minimal", "province", "bw", "behind_ear"), "min charge")
add("QuoteCheck", quote_check(3500, 8, "fine_line", "bkk", "bw"), "mint fair")
add("QuoteCheck", quote_check(1800, 8, "fine_line", "bkk", "bw"), "low")
add("QuoteCheck", quote_check(4300, 8, "fine_line", "bkk", "bw"), "high")
add("QuoteCheck", quote_check(8000, 8, "fine_line", "bkk", "bw"), "very high")

add("SafetyFlags", safety_from_flags(["none"], 28), "mint")
add("SafetyFlags", safety_from_flags(["keloid"], 33), "fah keloid")
add("SafetyFlags", safety_from_flags([], 16), "under 18")
add("SafetyFlags", safety_from_flags(["blood_thinner"], 41), "warn")

age5 = aging_preview("fine_line", "bw", "inner_forearm", 5, 8)
add("ArtistCard", artist_card(MINT, t_mint, pr_mint, age5, ["none"], MINT_NOTE), "mint")
add("ArtistCard", artist_card(PEOPLE[3], t_mint, pr_mint, age5, ["keloid"], "เคยเป็นคีลอยด์"), "fah blocked")

entries = [diary_entry(*e) for e in DIARY]
for e in entries:
    add("DiaryEntry", e, e["id"])
add("DiaryStats", diary_stats(entries), "mint diary")
add("DiaryStats", diary_stats([]), "empty")
add("ShareCard", share_card(MINT["name_th"], t_mint, age5), "mint")
add("Quota", quota(1, 1), "free")
add("Quota", quota(3, 1), "exhausted")
add("Quota", quota(0, 5, pro=True), "pro")
for lv in ("green", "yellow", "red"):
    add("SafetyGuard", safety_guard(lv), lv)

for e in ex:
    jsonschema.validate(e["value"], ref(e["def"]))

d = os.path.dirname(os.path.abspath(__file__)) + "/.."
json.dump(schema, open(d + "/schemas.json", "w"), ensure_ascii=False, indent=1)
json.dump({"examples": ex}, open(d + "/examples.json", "w"), ensure_ascii=False, indent=1)
print(len(defs), "defs,", len(ex), "examples, all valid")
