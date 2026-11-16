"""Generate ../schemas.json + ../examples.json and validate every example."""
import json, os, jsonschema
from balconyfarm import *
from fixtures import *

S = "https://json-schema.org/draft/2020-12/schema"
s = {"type": "string"}; b = {"type": "boolean"}
u = {"type": "number", "minimum": 0, "maximum": 1}
i0 = {"type": "integer", "minimum": 0}; i1 = {"type": "integer", "minimum": 1}
pct = {"type": "integer", "minimum": 0, "maximum": 100}
plant = {"enum": list(PLANTS)}; facing = {"enum": list(FACING)}; light = {"enum": list(LIGHT_TH)}
date = {"type": "string", "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}$"}
month = {"type": "integer", "minimum": 1, "maximum": 12}

def obj(req, props, **kw):
    return {"type": "object", "required": req, "properties": props, "additionalProperties": False, **kw}
def arr(i, **kw):
    return {"type": "array", "items": i, **kw}
R = lambda n: {"$ref": f"#/$defs/{n}"}

defs = {
 "Person": obj(["id", "name_th", "age"], {"id": {"type": "string", "pattern": "^u[0-9]{2}$"}, "name_th": s, "name_en": s, "age": i1, "city_th": s}),
 "BalconyPhoto": obj(["id", "px_w", "px_h", "glare", "blur", "crop"], {"id": {"type": "string", "pattern": "^p[0-9]{2}$"}, "px_w": i1, "px_h": i1, "glare": u, "blur": u, "crop": u}),
 "ScanQuality": obj(["score", "ok", "tips_th"], {"score": pct, "ok": b, "tips_th": arr(s)}),
 "BalconyScan": obj(["photo_id", "quality"], {"photo_id": s, "quality": R("ScanQuality")}),
 "AiBalconyExtract": obj(["is_balcony", "obstruction", "overhang_m", "width_m", "depth_m", "confidence"], {"is_balcony": b, "obstruction": u, "overhang_m": {"type": "number", "minimum": 0, "maximum": 3},
    "width_m": {"type": "number", "minimum": 0}, "depth_m": {"type": "number", "minimum": 0}, "railing": {"enum": ["glass", "metal_bars", "concrete_wall"]}, "confidence": u, "notes_th": s}),
 "SunInput": obj(["facing", "obstruction", "overhang_m", "floor"], {"facing": facing, "obstruction": u, "overhang_m": {"type": "number", "minimum": 0, "maximum": 3}, "floor": {"type": "integer", "minimum": 1, "maximum": 80}}),
 "SunEstimate": obj(["facing", "facing_th", "sun_hours", "light", "light_th", "hot_afternoon", "note_th", "headline_th"], {"facing": facing, "facing_th": s,
    "sun_hours": {"type": "number", "minimum": 0, "maximum": 12}, "light": light, "light_th": s, "hot_afternoon": b, "note_th": s, "headline_th": s}),
 "PlantFit": obj(["plant", "plant_th", "score", "light_fit", "in_season", "why_th"], {"plant": plant, "plant_th": s, "score": pct, "light_fit": {"enum": [0.0, 0.5, 1.0]}, "in_season": b, "why_th": s}),
 "PlantPicks": obj(["sun_hours", "light", "month", "picks", "headline_th"], {"sun_hours": {"type": "number"}, "light": light, "month": month, "picks": arr(R("PlantFit"), minItems=1), "headline_th": s}),
 "PotPlacement": obj(["plant", "x_cm", "y_cm", "pot_cm"], {"plant": plant, "x_cm": i0, "y_cm": i0, "pot_cm": i1}),
 "Layout": obj(["width_m", "depth_m", "usable_depth_m", "walkway_m", "pots", "skipped", "total_wet_kg", "load_kg_m2", "load_limit_kg_m2", "load_status", "load_th"], {
    "width_m": {"type": "number"}, "depth_m": {"type": "number"}, "usable_depth_m": {"type": "number"}, "walkway_m": {"type": "number"}, "pots": arr(R("PotPlacement")), "skipped": arr(plant),
    "total_wet_kg": i0, "load_kg_m2": {"type": "number", "minimum": 0}, "load_limit_kg_m2": i1, "load_status": {"enum": ["ok", "warn", "over"]}, "load_th": s}),
 "WaterDay": obj(["date", "water"], {"date": date, "water": arr(plant)}),
 "WaterPlan": obj(["season", "every_days", "days", "tip_th"], {"season": {"enum": ["hot", "rainy", "cool"]}, "every_days": {"type": "object", "propertyNames": plant, "additionalProperties": i1},
    "days": arr(R("WaterDay"), minItems=1), "tip_th": s}),
 "HarvestItem": obj(["plant", "plant_th", "first_harvest", "days"], {"plant": plant, "plant_th": s, "first_harvest": date, "days": i1}),
 "HarvestPlan": obj(["planted", "items", "first_up", "saves_baht_month", "headline_th"], {"planted": date, "items": arr(R("HarvestItem"), minItems=1), "first_up": s, "saves_baht_month": i0, "headline_th": s}),
 "ShoppingItem": obj(["plant", "plant_th", "pots", "pot_cm", "soil_l", "cost_baht"], {"plant": plant, "plant_th": s, "pots": i1, "pot_cm": i1, "soil_l": i1, "cost_baht": i1}),
 "ShoppingList": obj(["items", "soil_total_l", "total_baht", "payback_months", "disclaimer_th"], {"items": arr(R("ShoppingItem"), minItems=1), "soil_total_l": i1, "total_baht": i1,
    "payback_months": {"type": "number", "minimum": 0}, "disclaimer_th": s}),
 "MockupSpec": obj(["style", "plants", "image_prompt", "disclaimer_th"], {"style": {"enum": ["tropical_cafe", "minimal_white", "thai_retro"]}, "plants": arr(plant, minItems=1), "image_prompt": s, "disclaimer_th": s}),
 "DiaryEntry": obj(["date", "plant", "action"], {"date": date, "plant": plant, "action": {"enum": ["water", "harvest", "photo", "fertilize"]}, "grams": i0}),
 "DiarySummary": obj(["entries", "streak_days", "harvest_g", "saved_baht", "headline_th"], {"entries": i1, "streak_days": i0, "harvest_g": i0, "saved_baht": i0, "headline_th": s}),
 "ShareCard": obj(["title_th", "hook_th", "layout", "sizes", "watermark", "cta_th", "disclaimer_th"], {"title_th": s, "hook_th": s, "layout": {"enum": ["balcony_before_after"]},
    "sizes": arr({"enum": ["1080x1350", "1080x1920", "1080x1080"]}), "watermark": s, "cta_th": s, "disclaimer_th": s}),
 "Quota": obj(["allowed", "left_after", "paywall"], {"allowed": i0, "left_after": {"type": ["integer", "null"], "minimum": 0}, "paywall": b}),
 "SafetyGuard": obj(["level", "message_th"], {"level": {"enum": ["ok", "warn", "stop"]}, "message_th": s}),
}
schema = {"$schema": S, "$id": "https://example.com/balconyfarm.schema.json", "title": "BalconyFarm", "$defs": defs}
def ref(n):
    return {"$ref": f"#/$defs/{n}", "$defs": defs}

ex = []
def add(n, v, note=""):
    ex.append({"def": n, "note": note, "value": v})

for p in PEOPLE: add("Person", p, p["name_en"])
for ph in PHOTOS: add("BalconyPhoto", ph, ph["id"]); add("BalconyScan", balcony_scan(ph), ph["id"])
add("ScanQuality", scan_quality(0.2, 0.2, 0.2), "mid")
add("AiBalconyExtract", {"is_balcony": True, "obstruction": 0.3, "overhang_m": 1.0, "width_m": 2.4, "depth_m": 1.2, "railing": "glass", "confidence": 0.84, "notes_th": "ตึกฝั่งตรงข้ามบังบางส่วน"}, "demo")
add("AiBalconyExtract", {"is_balcony": False, "obstruction": 0, "overhang_m": 0, "width_m": 0, "depth_m": 0, "confidence": 0.9, "notes_th": "รูปนี้เป็นห้องนั่งเล่น"}, "not balcony")
suns = [("se", 0.3, 1.0, 12, 12), ("s", 0.0, 0.0, 20, 1), ("w", 0.1, 0.5, 5, 4), ("n", 0.5, 1.5, 3, 7), ("e", 0.2, 0.8, 8, 9), ("sw", 0.4, 0.3, 25, 12), ("ne", 0.0, 0.5, 15, 2)]
for f, o, oh, fl, mo in suns:
    note = f"{f} floor {fl}"
    add("SunInput", {"facing": f, "obstruction": o, "overhang_m": oh, "floor": fl}, note)
    se = sun_estimate(f, o, oh, fl); add("SunEstimate", se, note)
    pk = plant_picks(se, mo); add("PlantPicks", pk, f"{note} m{mo}")
    for x in pk["picks"]: add("PlantFit", x, f"{note} {x['plant']}")
    gl = [x["plant"] for x in pk["picks"]]
    add("WaterPlan", water_plan(gl, mo, f, TODAY, se["sun_hours"]), note)
    add("MockupSpec", mockup_spec(se, pk, ["tropical_cafe", "minimal_white", "thai_retro"][len(ex) % 3]), note)
add("Layout", LAYOUT, "demo 2.4x1.2")
for pl in LAYOUT["pots"]: add("PotPlacement", pl, pl["plant"])
add("Layout", layout(1.5, 1.0, ["kaffir_lime", "chili", "lemongrass", "cherry_tomato", "kaprao"]), "heavy small")
add("Layout", layout(1.2, 1.0, ["kaffir_lime", "kaffir_lime", "kaffir_lime"]), "over")
wp = water_plan(GARDEN, MONTH, "se", TODAY, SUN["sun_hours"])
for d in wp["days"]: add("WaterDay", d, d["date"])
hp = harvest_plan(GARDEN, TODAY); add("HarvestPlan", hp, "demo")
for it in hp["items"]: add("HarvestItem", it, it["plant"])
add("HarvestPlan", harvest_plan(["kaprao", "chili", "morning_glory"], "2026-04-01"), "sunny")
sl = shopping_list(GARDEN); add("ShoppingList", sl, "demo")
for it in sl["items"]: add("ShoppingItem", it, it["plant"])
add("ShoppingList", shopping_list(["kaprao", "kaprao", "chili", "kaffir_lime"]), "sunny")
for d in DIARY: add("DiaryEntry", d, d["plant"])
add("DiarySummary", diary_summary(DIARY, TODAY), "keng")
add("ShareCard", share_card(SUN, PICKS, "ระเบียงโล่ง ๆ กลายเป็นสวนผักใน 10 วิ"), "demo")
for a in ((0,), (2,), (3,), (9, 3, True)): add("Quota", quota(*a), str(a))
for f in (None, "railing", "overload", "pesticide", "not_balcony"): add("SafetyGuard", safety_guard(f), str(f))

for x in ex: jsonschema.validate(x["value"], ref(x["def"]))
d = os.path.dirname(os.path.abspath(__file__)) + "/.."
json.dump(schema, open(d + "/schemas.json", "w"), ensure_ascii=False, indent=1)
json.dump({"examples": ex}, open(d + "/examples.json", "w"), ensure_ascii=False, indent=1)
print(len(defs), "defs,", len(ex), "examples, all valid")
