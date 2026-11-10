"""Generate ../schemas.json + ../examples.json and validate every example."""
import json, os, jsonschema
from sellsnap import *
from fixtures import *

S = "https://json-schema.org/draft/2020-12/schema"
s = {"type": "string"}
b = {"type": "boolean"}
u = {"type": "number", "minimum": 0, "maximum": 1}
n0 = {"type": "number", "minimum": 0}
i0 = {"type": "integer", "minimum": 0}
i1 = {"type": "integer", "minimum": 1}
pct = {"type": "integer", "minimum": 0, "maximum": 100}

def obj(req, props, **kw):
    return {"type": "object", "required": req, "properties": props, "additionalProperties": False, **kw}

def arr(i, **kw):
    return {"type": "array", "items": i, **kw}

defs = {
 "Person": obj(["id", "name_th", "age"], {
    "id": {"type": "string", "pattern": "^u[0-9]{2}$"}, "name_th": s, "name_en": s, "age": i1, "city_th": s, "goal_th": s}),
 "Detection": obj(["key", "value", "confidence"], {"key": s, "value": True, "confidence": u}),
 "ItemPhoto": obj(["id", "px_w", "px_h", "glare", "blur", "crop", "detections"], {
    "id": {"type": "string", "pattern": "^s[0-9]{2}$"}, "px_w": i1, "px_h": i1, "glare": u, "blur": u, "crop": u,
    "detections": arr({"$ref": "#/$defs/Detection"})}),
 "ScanQuality": obj(["score", "ok", "tips_th"], {"score": pct, "ok": b, "tips_th": arr(s)}),
 "ItemScan": obj(["shot_id", "quality", "ok", "category", "item_th", "color_th", "brand_th", "defect_th", "message_th"], {
    "shot_id": s, "quality": {"$ref": "#/$defs/ScanQuality"}, "ok": b,
    "category": {"type": ["string", "null"]}, "item_th": {"type": ["string", "null"]},
    "color_th": {"type": ["string", "null"]}, "brand_th": {"type": ["string", "null"]},
    "defect_th": {"type": ["string", "null"]}, "message_th": s},
    # category_name_th only when ok
    **{}),
 "ConditionGrade": obj(["ok", "condition", "grade", "name_th", "message_th"], {
    "ok": b, "condition": {"type": ["string", "null"]}, "grade": {"type": ["string", "null"]},
    "name_th": {"type": ["string", "null"]}, "message_th": s}),
 "PriceRange": obj(["min_thb", "max_thb", "mid_thb", "category", "condition", "grade", "headline_th", "disclaimer_th"], {
    "min_thb": i0, "max_thb": i0, "mid_thb": i0, "category": s, "condition": s, "grade": s,
    "headline_th": s, "disclaimer_th": s}),
 "Listing": obj(["title_th", "description_th", "item_th", "condition", "grade", "min_thb", "max_thb", "ask_thb", "headline_th"], {
    "title_th": s, "description_th": s, "item_th": s, "condition": s, "grade": s,
    "min_thb": i0, "max_thb": i0, "ask_thb": i0, "headline_th": s}),
 "PhotoTips": obj(["keys", "tips_th", "count", "headline_th"], {
    "keys": arr(s), "tips_th": arr(s), "count": i0, "headline_th": s}),
 "ReplyTemplate": obj(["id", "key", "name_th", "text_th"], {"id": s, "key": s, "name_th": s, "text_th": s}),
 "ReplyKit": obj(["ask_thb", "templates", "count"], {"ask_thb": i0, "templates": arr({"$ref": "#/$defs/ReplyTemplate"}), "count": i0}),
 "LogRow": obj(["id", "status", "ask_thb", "sold_thb", "date", "title_th"], {
    "id": s, "status": {"enum": ["for_sale", "reserved", "sold"]}, "ask_thb": i0,
    "sold_thb": {"type": ["integer", "null"], "minimum": 0}, "date": {"type": ["string", "null"]}, "title_th": s}),
 "SoldLog": obj(["rows", "sold_count", "open_count", "reserved_count", "total_sold_thb", "headline_th"], {
    "rows": arr({"$ref": "#/$defs/LogRow"}), "sold_count": i0, "open_count": i0, "reserved_count": i0,
    "total_sold_thb": i0, "headline_th": s}),
 "ShareCard": obj(["title_th", "headline_th", "hook_th", "min_thb", "max_thb", "ask_thb", "grade", "layout", "sizes", "watermark", "cta_th"], {
    "title_th": s, "headline_th": s, "hook_th": s, "min_thb": i0, "max_thb": i0, "ask_thb": i0, "grade": s,
    "layout": {"enum": ["listing_card"]}, "sizes": arr({"enum": ["1080x1350", "1080x1920", "1080x1080"]}),
    "watermark": s, "cta_th": s}),
 "Quota": obj(["allowed", "left_after", "paywall"], {"allowed": i0, "left_after": {"type": ["integer", "null"], "minimum": 0}, "paywall": b}),
 "SafetyGuard": obj(["level", "message_th"], {"level": {"enum": ["ok", "warn", "stop"]}, "message_th": s}),
}
# ItemScan may include category_name_th
defs["ItemScan"]["properties"]["category_name_th"] = s
schema = {"$schema": S, "$id": "https://example.com/sellsnap.schema.json", "title": "SellSnap", "$defs": defs}

def ref(n):
    return {"$ref": f"#/$defs/{n}", "$defs": defs}

ex=[]
def add(n,v,note=""):
    ex.append({"def": n, "note": note, "value": v})

for p in PEOPLE:
    add("Person", p, p["name_th"])
shots=[BOSS_SHOT, NID_SHOT, SOM_SHOT, WEAR_SHOT, BAD_SHOT, EMPTY_SHOT, LOWCONF_SHOT]
for sh in shots:
    add("ItemPhoto", sh, sh["id"])
    add("ItemScan", parse_item(sh), sh["id"])
    add("ScanQuality", scan_quality(sh["glare"], sh["blur"], sh["crop"], len(sh["detections"])), sh["id"])
    add("ConditionGrade", condition_grade(sh), sh["id"])
    for d in sh["detections"][:2]:
        add("Detection", d, sh["id"]+" "+d["key"])

item=parse_item(BOSS_SHOT); cond=condition_grade(BOSS_SHOT); price=price_range(item, cond)
post=listing(item, cond, price, extra_note="มารับเองแถวลาดพร้าว")
add("PriceRange", price, "boss lamp good")
add("Listing", post, "boss")
for sh, note in ((NID_SHOT, "nid bag"), (SOM_SHOT, "som book")):
    it, cd = parse_item(sh), condition_grade(sh)
    pr = price_range(it, cd)
    add("PriceRange", pr, note)
    add("Listing", listing(it, cd, pr), note)
add("PhotoTips", photo_tips(BOSS_SHOT), "boss missing extras")
add("PhotoTips", photo_tips(BOSS_SHOT, True, True, 3), "complete")
add("PhotoTips", photo_tips(BAD_SHOT, True, True, 3), "bad quality")
rk=reply_templates(price)
add("ReplyKit", rk, "all")
for t in rk["templates"]:
    add("ReplyTemplate", t, t["key"])
add("ReplyKit", reply_templates(price, kinds=["sold", "meetup"]), "subset")
inv=[dict(r) for r in INVENTORY]
for r in inv:
    add("LogRow", r, r["id"])
add("SoldLog", sold_log([dict(r) for r in INVENTORY], "sell", "l01", sold_thb=550, date="2026-11-26"), "sell lamp")
add("SoldLog", sold_log([dict(r) for r in INVENTORY], "reserve", "l02"), "reserve bag")
add("SoldLog", sold_log([dict(r) for r in INVENTORY], "relist", "l03"), "relist book")
# extra category/condition price examples
for cat, condk in (("chair","good"),("electronics","good"),("clothes","like_new"),("kitchen","fair"),("toy","poor"),("other","good"),("lamp","for_parts"),("bag","like_new")):
    it=dict(item, ok=True, category=cat, item_th=cat, color_th=None, brand_th=None, defect_th=None, category_name_th=cat)
    cd=dict(cond, ok=True, condition=condk, grade=CONDITIONS[condk]["grade"], name_th=CONDITIONS[condk]["name_th"])
    pr=price_range(it, cd)
    add("PriceRange", pr, cat+" "+condk)
    add("Listing", listing(it, cd, pr), cat+" "+condk)
add("ShareCard", share_card("พี่บอส", post, price), "boss")
add("Quota", quota(1,1), "free")
add("Quota", quota(3,1), "exhausted")
add("Quota", quota(0,5,pro=True), "pro")
add("SafetyGuard", safety_guard(), "ok")
add("SafetyGuard", safety_guard(True, False), "stop")
add("SafetyGuard", safety_guard(True, True), "warn prepay")
add("SafetyGuard", safety_guard(False, False), "warn meetup")

for e in ex:
    jsonschema.validate(e["value"], ref(e["def"]))
d=os.path.dirname(os.path.abspath(__file__))+"/.."
json.dump(schema, open(d+"/schemas.json","w"), ensure_ascii=False, indent=1)
json.dump({"examples": ex}, open(d+"/examples.json","w"), ensure_ascii=False, indent=1)
print(len(defs), "defs,", len(ex), "examples, all valid")
