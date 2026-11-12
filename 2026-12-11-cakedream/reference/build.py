"""Generate ../schemas.json + ../examples.json and validate every example."""
import json, os, jsonschema
from cakedream import *
from fixtures import *

S = "https://json-schema.org/draft/2020-12/schema"
s = {"type": "string"}; b = {"type": "boolean"}
u = {"type": "number", "minimum": 0, "maximum": 1}
i0 = {"type": "integer", "minimum": 0}; i1 = {"type": "integer", "minimum": 1}
pct = {"type": "integer", "minimum": 0, "maximum": 100}
lb = {"enum": sorted(SIZES)}; theme = {"enum": list(THEMES)}; flavor = {"enum": list(FLAVORS)}; alg = {"enum": list(ALLERGENS)}
date = {"type": "string", "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}$"}
hexc = {"type": "string", "pattern": "^#[0-9A-F]{6}$"}

def obj(req, props, **kw):
    return {"type": "object", "required": req, "properties": props, "additionalProperties": False, **kw}
def arr(i, **kw):
    return {"type": "array", "items": i, **kw}
R = lambda n: {"$ref": f"#/$defs/{n}"}

defs = {
 "Person": obj(["id", "name_th", "age"], {"id": {"type": "string", "pattern": "^u[0-9]{2}$"}, "name_th": s, "name_en": s, "age": i1, "city_th": s}),
 "RefPhoto": obj(["id", "px_w", "px_h", "glare", "blur", "crop"], {"id": {"type": "string", "pattern": "^p[0-9]{2}$"}, "px_w": i1, "px_h": i1, "glare": u, "blur": u, "crop": u}),
 "ScanQuality": obj(["score", "ok", "tips_th"], {"score": pct, "ok": b, "tips_th": arr(s)}),
 "RefScan": obj(["photo_id", "quality"], {"photo_id": s, "quality": R("ScanQuality")}),
 "GuestInput": obj(["adults", "kids", "appetite", "leftovers"], {"adults": i0, "kids": i0, "appetite": {"enum": ["light", "normal", "dessert_lovers"]}, "leftovers": b}),
 "Servings": obj(["guests", "adults", "kids", "servings_needed", "pounds", "shape", "diameter_in", "servings_capacity", "headline_th"], {
    "guests": i1, "adults": i0, "kids": i0, "servings_needed": i1, "pounds": lb, "shape": {"enum": ["round", "tier2", "tier3"]},
    "diameter_in": i1, "servings_capacity": i1, "headline_th": s}),
 "MessageFit": obj(["text", "glyphs", "limit_per_line", "lines", "fits", "tip_th"], {"text": s, "glyphs": i1, "limit_per_line": i1, "lines": {"enum": [1, 2]}, "fits": b, "tip_th": s}),
 "DesignRequest": obj(["theme", "flavor", "pounds", "message"], {"theme": theme, "flavor": flavor, "pounds": lb, "message": s, "extra_toppers": {"type": "integer", "minimum": 0, "maximum": 5}}),
 "DesignSpec": obj(["theme", "theme_th", "flavor", "flavor_th", "pounds", "shape", "diameter_in", "palette", "toppers_th", "extra_toppers", "complexity", "message", "image_prompt", "disclaimer_th"], {
    "theme": theme, "theme_th": s, "flavor": flavor, "flavor_th": s, "pounds": lb, "shape": {"enum": ["round", "tier2", "tier3"]}, "diameter_in": i1,
    "palette": arr(hexc, minItems=2), "toppers_th": arr(s, minItems=1), "extra_toppers": i0, "complexity": {"enum": [1, 2, 3, 4]},
    "message": R("MessageFit"), "image_prompt": s, "disclaimer_th": s}),
 "PriceEstimate": obj(["region", "low", "mid", "high", "per_serving", "disclaimer_th"], {"region": {"enum": list(REGION_MULT)}, "low": i1, "mid": i1, "high": i1, "per_serving": i1, "disclaimer_th": s}),
 "FairPrice": obj(["quote", "verdict", "verdict_th", "diff_from_mid_pct"], {"quote": {"type": "number", "exclusiveMinimum": 0},
    "verdict": {"enum": ["suspicious_low", "cheap", "fair", "pricey", "very_pricey"]}, "verdict_th": s, "diff_from_mid_pct": {"type": "integer"}}),
 "AllergyCheck": obj(["level", "hits", "alternatives", "message_th"], {"level": {"enum": ["ok", "warn", "stop"]}, "hits": arr(alg), "alternatives": arr(flavor), "message_th": s}),
 "Ingredient": obj(["item", "item_th", "qty", "unit", "cost_baht"], {"item": s, "item_th": s, "qty": i1, "unit": {"enum": ["กรัม", "ฟอง"]}, "cost_baht": i0}),
 "DiyRecipe": obj(["pounds", "flavor", "ingredients", "total_cost_baht", "bake_minutes", "oven_c", "steps_th"], {
    "pounds": lb, "flavor": flavor, "ingredients": arr(R("Ingredient"), minItems=1), "total_cost_baht": i0, "bake_minutes": i1, "oven_c": i1, "steps_th": arr(s, minItems=1)}),
 "OrderDeadline": obj(["party_date", "order_by", "days_left", "status", "message_th"], {"party_date": date, "order_by": date, "days_left": {"type": "integer"}, "status": {"enum": ["ok", "last_call", "too_late"]}, "message_th": s}),
 "OrderCard": obj(["to", "from_th", "lines_th", "attach", "share_text", "disclaimer_th"], {"to": s, "from_th": s, "lines_th": arr(s, minItems=5), "attach": arr(s), "share_text": s, "disclaimer_th": s}),
 "DiaryEntry": obj(["date", "theme", "paid_baht", "stars"], {"date": date, "theme": theme, "paid_baht": i0, "stars": {"type": "integer", "minimum": 1, "maximum": 5}}),
 "DiarySummary": obj(["count", "spent_baht", "avg_stars", "top_theme", "headline_th"], {"count": i1, "spent_baht": i0, "avg_stars": {"type": "number", "minimum": 1, "maximum": 5}, "top_theme": theme, "headline_th": s}),
 "ShareCard": obj(["title_th", "hook_th", "layout", "sizes", "watermark", "cta_th", "disclaimer_th"], {"title_th": s, "hook_th": s, "layout": {"enum": ["idea_to_mockup"]},
    "sizes": arr({"enum": ["1080x1350", "1080x1920", "1080x1080"]}), "watermark": s, "cta_th": s, "disclaimer_th": s}),
 "Quota": obj(["allowed", "left_after", "paywall"], {"allowed": i0, "left_after": {"type": ["integer", "null"], "minimum": 0}, "paywall": b}),
 "SafetyGuard": obj(["level", "message_th"], {"level": {"enum": ["ok", "stop"]}, "message_th": s}),
 "AiIdeaExtract": obj(["theme", "flavor", "message", "confidence"], {"theme": theme, "flavor": flavor, "message": s, "confidence": u, "colors": arr(hexc), "notes_th": s}),
}
schema = {"$schema": S, "$id": "https://example.com/cakedream.schema.json", "title": "CakeDream", "$defs": defs}
def ref(n):
    return {"$ref": f"#/$defs/{n}", "$defs": defs}

ex = []
def add(n, v, note=""):
    ex.append({"def": n, "note": note, "value": v})

for p in PEOPLE: add("Person", p, p["name_en"])
for ph in PHOTOS: add("RefPhoto", ph, ph["id"]); add("RefScan", ref_scan(ph), ph["id"])
add("ScanQuality", scan_quality(0.2, 0.2, 0.2), "mid")
for g in ((8, 10, "normal", False), (8, 10, "dessert_lovers", False), (8, 10, "normal", True), (4, 2, "light", False), (30, 0, "normal", False), (50, 0, "normal", False), (2, 0, "normal", False)):
    add("GuestInput", dict(zip(("adults", "kids", "appetite", "leftovers"), g)), str(g)); add("Servings", serving_calc(*g), str(g))
for t, n in (("HBD น้องภูมิ 5 ขวบ", 2), ("สุขสันต์วันเกิดคุณแม่ที่รักที่สุดในโลก", 1), ("ก" * 40, 0.5), ("Happy 60th ลุงชัย", 3), ("รักนะ", 1)):
    add("MessageFit", message_fit(t, n), t[:12])
reqs = [("dinosaur", "vanilla_chiffon", 2, "HBD น้องภูมิ 5 ขวบ", 0), ("unicorn", "strawberry", 1.5, "Happy 6th Mali", 1), ("korean_minimal", "thai_tea", 1, "รักนะ", 0),
        ("princess", "chocolate", 5, "Happy 60", 3), ("gold_luxury", "chocolate", 3, "Happy 60th ลุงชัย", 0), ("floral", "pandan_coconut", 2, "ขอบคุณแม่", 2),
        ("football", "eggless_choc", 1, "Fah 22", 0), ("cartoon_bear", "almond_crunch", 0.5, "Bear", 0)]
for r in reqs:
    note = f"{r[0]} {r[2]}lb"; add("DesignRequest", dict(zip(("theme", "flavor", "pounds", "message", "extra_toppers"), r)), note)
    d = design_spec(*r); add("DesignSpec", d, note)
    for reg in REGION_MULT: add("PriceEstimate", price_estimate(d, reg), note + " " + reg)
e = price_estimate(DINO)
for q in (700, 1000, 1250, 1500, 2000, 2600): add("FairPrice", fair_price(e, q), str(q))
for f, a in (("vanilla_chiffon", []), ("vanilla_chiffon", ["nuts"]), ("almond_crunch", ["nuts"]), ("chocolate", ["egg"]), ("pandan_coconut", ["dairy"]), ("strawberry", ["egg", "dairy"])):
    add("AllergyCheck", allergy_guard(f, a), f + str(a))
for p in (0.5, 1, 2, 3):
    r = diy_recipe(p, "vanilla_chiffon"); add("DiyRecipe", r, f"{p}lb")
    for i in r["ingredients"]: add("Ingredient", i, f"{p}lb {i['item']}")
for pd, cx in ((PARTY, 3), ("2026-12-14", 3), ("2026-12-12", 4), ("2026-12-25", 1)): add("OrderDeadline", order_deadline(pd, cx, TODAY), pd)
add("OrderCard", order_card(PEOPLE[0], DINO, GUESTS, e, allergy_guard("vanilla_chiffon", []), order_deadline(PARTY, 3, TODAY)), "demo")
add("OrderCard", order_card(PEOPLE[1], design_spec("unicorn", "chocolate", 1, "Nan"), serving_calc(5, 0), price_estimate(design_spec("unicorn", "chocolate", 1, "Nan")),
                            allergy_guard("chocolate", ["egg"]), order_deadline(PARTY, 3, TODAY)), "allergy")
for d in DIARY: add("DiaryEntry", d, d["theme"])
add("DiarySummary", diary_summary(DIARY), "puk")
add("ShareCard", share_card(DINO, "จากไอเดีย เป็นภาพเค้กใน 10 วิ"), "demo")
for a in ((0,), (2,), (3,), (9, 3, True)): add("Quota", quota(*a), str(a))
for f in (None, "real_brand", "nuts"): add("SafetyGuard", safety_guard(f), str(f))
add("AiIdeaExtract", {"theme": "dinosaur", "flavor": "vanilla_chiffon", "message": "HBD น้องภูมิ 5 ขวบ", "confidence": 0.91, "colors": ["#7CC36B", "#F4D35E"], "notes_th": "ตัวอย่างผลจากเสียง/ข้อความ"}, "voice")
add("AiIdeaExtract", {"theme": "unicorn", "flavor": "strawberry", "message": "Happy 6th Mali", "confidence": 0.58, "notes_th": "ไม่แน่ใจรส ให้ผู้ใช้ยืนยัน"}, "low conf")

for x in ex: jsonschema.validate(x["value"], ref(x["def"]))
d = os.path.dirname(os.path.abspath(__file__)) + "/.."
json.dump(schema, open(d + "/schemas.json", "w"), ensure_ascii=False, indent=1)
json.dump({"examples": ex}, open(d + "/examples.json", "w"), ensure_ascii=False, indent=1)
print(len(defs), "defs,", len(ex), "examples, all valid")
