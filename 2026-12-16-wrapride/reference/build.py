"""Generate ../schemas.json + ../examples.json and validate every example."""
import json, os, jsonschema
from wrapride import *
from fixtures import *

S = "https://json-schema.org/draft/2020-12/schema"
s = {"type": "string"}; b = {"type": "boolean"}
u = {"type": "number", "minimum": 0, "maximum": 1}
i0 = {"type": "integer", "minimum": 0}; i1 = {"type": "integer", "minimum": 1}
pct = {"type": "integer", "minimum": 0, "maximum": 100}
hexc = {"type": "string", "pattern": "^#[0-9A-F]{6}$"}
date = {"type": "string", "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}$"}
veh = {"enum": list(VEHICLES)}; col = {"enum": list(COLORS)}; fin = {"enum": list(FINISHES)}; cov = {"enum": list(COVERAGE)}
fam = {"enum": sorted({c["family"] for c in COLORS.values()})}

def obj(req, props, **kw):
    return {"type": "object", "required": req, "properties": props, "additionalProperties": False, **kw}
def arr(i, **kw):
    return {"type": "array", "items": i, **kw}
R = lambda n: {"$ref": f"#/$defs/{n}"}
nul = lambda x: {"anyOf": [x, {"type": "null"}]}

defs = {
 "Person": obj(["id", "name_th", "age", "vehicle"], {"id": {"type": "string", "pattern": "^u[0-9]{2}$"}, "name_th": s, "name_en": s, "age": i1, "city_th": s, "vehicle": veh}),
 "VehiclePhoto": obj(["id", "px_w", "px_h", "glare", "blur", "crop"], {"id": {"type": "string", "pattern": "^p[0-9]{2}$"}, "px_w": i1, "px_h": i1, "glare": u, "blur": u, "crop": u}),
 "ScanQuality": obj(["score", "ok", "tips_th"], {"score": pct, "ok": b, "tips_th": arr(s)}),
 "VehicleScan": obj(["photo_id", "quality"], {"photo_id": s, "quality": R("ScanQuality")}),
 "AiVehicleExtract": obj(["is_vehicle", "vehicle", "original_family", "angle", "plate_visible", "confidence"], {"is_vehicle": b, "vehicle": nul(veh), "original_family": nul(fam),
    "angle": {"enum": ["front_45", "side", "rear_45", "front", "rear", "unknown"]}, "plate_visible": b, "confidence": u, "notes_th": s}),
 "FinishSwatch": obj(["color", "finish", "base_hex", "highlight_hex", "shadow_hex", "label_th"], {"color": col, "finish": fin, "base_hex": hexc, "highlight_hex": hexc, "shadow_hex": hexc, "shift_hex": hexc, "label_th": s}),
 "WrapSpec": obj(["vehicle", "color", "finish", "coverage", "accent_color", "swatch", "main_color_change", "image_prompt", "title_th", "disclaimer_th"], {"vehicle": veh, "color": col, "finish": fin,
    "coverage": cov, "accent_color": nul(col), "swatch": R("FinishSwatch"), "main_color_change": b, "image_prompt": s, "title_th": s, "disclaimer_th": s}),
 "RimStickerSpec": obj(["vehicle", "rim_style", "rim_color", "rim_inch", "stickers", "blocked_areas", "ok", "image_prompt", "note_th"], {"vehicle": veh, "rim_style": nul({"enum": list(RIM_STYLES)}),
    "rim_color": nul({"enum": list(RIM_COLORS)}), "rim_inch": i1, "stickers": arr({"enum": list(STICKERS)}, maxItems=3), "blocked_areas": arr({"enum": list(FORBIDDEN_AREAS)}), "ok": b, "image_prompt": s, "note_th": s}),
 "PriceCheck": obj(["vehicle", "job", "low_baht", "high_baht", "quote_baht", "verdict", "verdict_th", "disclaimer_th"], {"vehicle": veh, "job": {"enum": ["wrap", "paint", "rims", "stickers"]},
    "low_baht": i0, "high_baht": i0, "quote_baht": nul({"type": "number", "minimum": 1}), "verdict": {"enum": ["no_quote", "suspicious_low", "fair", "high", "too_high"]}, "verdict_th": s, "disclaimer_th": s}),
 "ShopBrief": obj(["to_th", "from_name_th", "lines_th", "text_th", "attach", "cta_th"], {"to_th": s, "from_name_th": s, "lines_th": arr(s, minItems=3), "text_th": s,
    "attach": arr({"enum": ["before_photo", "mockup_4x5", "swatch"]}), "cta_th": s}),
 "LegalItem": obj(["code", "level", "text_th"], {"code": {"enum": ["dlt_color", "insurance", "reflective", "lights_plate"]}, "level": {"enum": ["info", "warn", "action"]}, "text_th": s}),
 "LegalCheck": obj(["level", "items", "note_th"], {"level": {"enum": ["info", "warn", "action"]}, "items": arr(R("LegalItem"), minItems=1), "note_th": s}),
 "ReelShot": obj(["from_s", "to_s", "kind", "text_th"], {"from_s": i0, "to_s": i1, "kind": {"enum": ["before", "scan", "swipe", "compare", "cta"]}, "text_th": s}),
 "ReelPlan": obj(["seconds", "ratio", "music_bpm", "shots", "watermark"], {"seconds": {"type": "integer", "minimum": 15, "maximum": 30}, "ratio": {"enum": ["9:16"]}, "music_bpm": i1,
    "shots": arr(R("ReelShot"), minItems=5, maxItems=5), "watermark": s}),
 "DiaryEntry": obj(["date", "kind"], {"date": date, "kind": {"enum": ["wash", "wrap", "service", "rim", "photo", "tire"]}, "cost_baht": i0, "note_th": s}),
 "DiarySummary": obj(["entries", "wrap_age_days", "next_wash", "spend_baht", "care_tip_th", "headline_th"], {"entries": i1, "wrap_age_days": nul(i0), "next_wash": date, "spend_baht": i0, "care_tip_th": s, "headline_th": s}),
 "ShareCard": obj(["title_th", "hook_th", "layout", "sizes", "watermark", "cta_th", "disclaimer_th"], {"title_th": s, "hook_th": s, "layout": {"enum": ["car_before_after"]},
    "sizes": arr({"enum": ["1080x1350", "1080x1920", "1080x1080"]}), "watermark": s, "cta_th": s, "disclaimer_th": s}),
 "Quota": obj(["allowed", "left_after", "paywall"], {"allowed": i0, "left_after": {"type": ["integer", "null"], "minimum": 0}, "paywall": b}),
 "SafetyGuard": obj(["level", "message_th"], {"level": {"enum": ["ok", "warn", "stop"]}, "message_th": s}),
}
schema = {"$schema": S, "$id": "https://example.com/wrapride.schema.json", "title": "WrapRide", "$defs": defs}
def ref(n):
    return {"$ref": f"#/$defs/{n}", "$defs": defs}

ex = []
def add(n, v, note=""):
    ex.append({"def": n, "note": note, "value": v})

for p in PEOPLE: add("Person", p, p["name_en"])
for ph in PHOTOS: add("VehiclePhoto", ph, ph["id"]); add("VehicleScan", vehicle_scan(ph), ph["id"])
add("ScanQuality", scan_quality(0.2, 0.2, 0.2), "mid")
add("AiVehicleExtract", {"is_vehicle": True, "vehicle": "eco_car", "original_family": "white", "angle": "front_45", "plate_visible": True, "confidence": 0.88, "notes_th": "รถอีโคคาร์สีขาว มุมเฉียงหน้า"}, "demo")
add("AiVehicleExtract", {"is_vehicle": True, "vehicle": "scooter", "original_family": "black", "angle": "side", "plate_visible": False, "confidence": 0.81}, "scooter")
add("AiVehicleExtract", {"is_vehicle": False, "vehicle": None, "original_family": None, "angle": "unknown", "plate_visible": False, "confidence": 0.93, "notes_th": "รูปนี้เป็นจักรยาน"}, "not vehicle")
for c in COLORS:
    for f in FINISHES:
        add("FinishSwatch", finish_swatch(c, f), f"{c} {f}")
combos = [("eco_car", "mint_green", "matte", "two_tone", "deep_black", "white"), ("sedan", "midnight_blue", "satin", "full", None, "grey"),
          ("suv", "army_green", "matte", "full", None, "white"), ("pickup", "sunset_orange", "gloss", "stripes", None, "white"),
          ("big_bike", "candy_red", "gloss", "full", None, "black"), ("scooter", "lavender", "gloss", "full", None, "black"),
          ("sedan", "cement_grey", "chrome", "full", None, "grey"), ("eco_car", "hot_pink", "color_shift", "roof", None, "white"),
          ("suv", "pearl_white", "satin", "two_tone", "champagne_gold", "white")]
specs = []
for v, c, f, cv, a, fm in combos:
    sp = wrap_spec(v, c, f, cv, a, fm); specs.append(sp); note = f"{v} {c} {f} {cv}"
    add("WrapSpec", sp, note); add("LegalCheck", legal_check(sp), note)
    add("PriceCheck", price_check(v, "wrap", f, cv), note)
for it in LEGAL["items"]: add("LegalItem", it, it["code"])
for r in (RIMS, rim_sticker_spec("pickup", "deep_dish", "bronze", ["hood_stripes", "kanok"]), rim_sticker_spec("scooter", "mesh", "gold", ["race_number"]),
          rim_sticker_spec("sedan", stickers=["checker"], areas=["door", "headlight", "plate"]), rim_sticker_spec("suv", "multi_spoke", "gunmetal")):
    add("RimStickerSpec", r, r["vehicle"])
add("PriceCheck", PRICE, "demo quote 24k")
add("PriceCheck", RIM_PRICE, "demo rims")
for v, j, q, kw in (("sedan", "wrap", 12000, {}), ("sedan", "wrap", 44000, {}), ("scooter", "wrap", 9000, {}), ("sedan", "paint", 38000, {}),
                    ("big_bike", "rims", None, {}), ("eco_car", "stickers", 2500, {"stickers": 2})):
    add("PriceCheck", price_check(v, j, quote_baht=q, **kw), f"{v} {j} {q}")
add("ShopBrief", BRIEF, "demo")
add("ShopBrief", shop_brief(PEOPLE[1], specs[5], rim_sticker_spec("scooter", "mesh", "gold"), price_check("scooter", "wrap")), "scooter")
add("ReelPlan", REEL, "20s")
add("ReelPlan", reel_plan(specs[4], 15), "15s bike")
add("ReelPlan", reel_plan(specs[1], 30), "30s sedan")
for sh in REEL["shots"]: add("ReelShot", sh, sh["kind"])
for d in DIARY: add("DiaryEntry", d, d["kind"])
add("DiarySummary", diary_summary(DIARY, TODAY), "ton")
add("DiarySummary", diary_summary([{"date": "2026-11-01", "kind": "wash", "cost_baht": 120}, {"date": "2026-12-01", "kind": "service", "cost_baht": 1890}], TODAY), "no wrap")
add("ShareCard", share_card(SPEC, "เบื่อสีรถเดิม? ลองสีใหม่ใน 10 วิ"), "demo")
add("ShareCard", share_card(specs[5], "สกู๊ตเตอร์สีเดิม ๆ → ม่วงลาเวนเดอร์"), "scooter")
for a in ((0,), (4,), (5,), (9, 5, True)): add("Quota", quota(*a), str(a))
for f in (None, "plate_visible", "covers_lights", "not_vehicle", "someone_elses_car", "brand_logo"): add("SafetyGuard", safety_guard(f), str(f))

for x in ex: jsonschema.validate(x["value"], ref(x["def"]))
d = os.path.dirname(os.path.abspath(__file__)) + "/.."
json.dump(schema, open(d + "/schemas.json", "w"), ensure_ascii=False, indent=1)
json.dump({"examples": ex}, open(d + "/examples.json", "w"), ensure_ascii=False, indent=1)
print(len(defs), "defs,", len(ex), "examples, all valid")
