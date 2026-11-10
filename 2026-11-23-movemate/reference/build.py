"""Generate ../schemas.json + ../examples.json and validate every example."""
import json, os, jsonschema
from movemate import *
from fixtures import *

S = "https://json-schema.org/draft/2020-12/schema"
s = {"type": "string"}
b = {"type": "boolean"}
i0 = {"type": "integer", "minimum": 0}
i1 = {"type": "integer", "minimum": 1}
pct = {"type": "integer", "minimum": 0, "maximum": 100}
room = {"enum": list(ROOMS)}
date = {"type": "string", "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}$"}

def obj(req, props, **kw):
    return {"type": "object", "required": req, "properties": props, "additionalProperties": False, **kw}

def arr(i, **kw):
    return {"type": "array", "items": i, **kw}

defs = {
 "Person": obj(["id", "name_th", "age", "move_date"], {
    "id": {"type": "string", "pattern": "^u[0-9]{2}$"}, "name_th": s, "name_en": s, "age": i1,
    "city_th": s, "goal_th": s, "move_date": date, "region": {"enum": list(REGION_VAN)},
    "van_type": {"enum": list(VAN_TYPES)}, "van_hour": {"type": "integer", "minimum": 0, "maximum": 23}}),
 "CheckItem": obj(["key", "text_th", "packed"], {"key": s, "text_th": s, "packed": b}),
 "RoomChecklist": obj(["room", "name_th", "items", "count", "packed", "progress"], {
    "room": room, "name_th": s, "items": arr({"$ref": "#/$defs/CheckItem"}), "count": i0, "packed": i0, "progress": pct}),
 "Box": obj(["code", "short_th", "room", "room_th", "contents_th", "item_count", "fragile", "photo_id", "on_device", "qr_payload", "label_th"], {
    "code": {"type": "string", "pattern": "^B[0-9]{2}$"}, "short_th": s, "room": room, "room_th": s,
    "contents_th": arr(s, minItems=1), "item_count": i1, "fragile": b, "photo_id": {"type": ["string", "null"]},
    "on_device": b, "qr_payload": {"type": "string", "pattern": "^movemate://box/B[0-9]{2}$"}, "label_th": s}),
 "BoxLabel": obj(["code", "short_th", "label_th", "qr_payload", "room_th", "fragile", "photo_id", "on_device", "sizes"], {
    "code": s, "short_th": s, "label_th": s, "qr_payload": s, "room_th": s, "fragile": b,
    "photo_id": {"type": ["string", "null"]}, "on_device": b, "sizes": arr(s, minItems=1)}),
 "FindHit": obj(["code", "short_th", "room", "room_th", "matched_th", "fragile", "photo_id"], {
    "code": s, "short_th": s, "room": room, "room_th": s, "matched_th": arr(s), "fragile": b,
    "photo_id": {"type": ["string", "null"]}}),
 "FindResult": obj(["query", "hits", "count"], {"query": s, "hits": arr({"$ref": "#/$defs/FindHit"}), "count": i0}),
 "InventoryStats": obj(["box_count", "item_count", "fragile_count", "rooms", "with_photo"], {
    "box_count": i0, "item_count": i0, "fragile_count": i0, "rooms": arr(room), "with_photo": i0}),
 "TimelineStep": obj(["n", "key", "time", "text_th", "owner_th"], {"n": i1, "key": s, "time": {"type": "string", "pattern": "^[0-9]{2}:[0-9]{2}$"}, "text_th": s, "owner_th": s}),
 "Timeline": obj(["move_date", "dow", "van_hour", "rooms", "steps", "step_count"], {
    "move_date": date, "dow": s, "van_hour": {"type": "integer", "minimum": 0, "maximum": 23},
    "rooms": arr(room, minItems=1), "steps": arr({"$ref": "#/$defs/TimelineStep"}, minItems=1), "step_count": i1}),
 "UtilityItem": obj(["key", "label_th", "hint_th", "value_th", "status"], {
    "key": s, "label_th": s, "hint_th": s, "value_th": {"type": ["string", "null"]}, "status": {"enum": ["done", "pending"]}}),
 "UtilityList": obj(["items", "count", "pending", "missing"], {
    "items": arr({"$ref": "#/$defs/UtilityItem"}, minItems=1), "count": i1, "pending": i0, "missing": arr(s)}),
 "CostEstimate": obj(["n_boxes", "van_type", "region", "van_thb", "boxes_thb", "tape_thb", "total_thb", "disclaimer_th"], {
    "n_boxes": i0, "van_type": {"enum": list(VAN_TYPES)}, "region": {"enum": list(REGION_VAN)},
    "van_thb": i0, "boxes_thb": i0, "tape_thb": i0, "total_thb": i0, "disclaimer_th": s}),
 "ShareCard": obj(["title_th", "headline_th", "hook_th", "box_count", "item_count", "total_thb", "layout", "sizes", "watermark", "cta_th"], {
    "title_th": s, "headline_th": s, "hook_th": s, "box_count": i0, "item_count": i0, "total_thb": i0,
    "layout": {"enum": ["move_card"]}, "sizes": arr({"enum": ["1080x1350", "1080x1920", "1080x1080"]}),
    "watermark": s, "cta_th": s}),
 "Quota": obj(["allowed", "left_after", "paywall"], {"allowed": i0, "left_after": {"type": ["integer", "null"], "minimum": 0}, "paywall": b}),
 "SafetyGuard": obj(["level", "message_th"], {"level": {"enum": ["ok", "warn", "stop"]}, "message_th": s}),
}
schema = {"$schema": S, "$id": "https://example.com/movemate.schema.json", "title": "MoveMate", "$defs": defs}

def ref(n):
    return {"$ref": f"#/$defs/{n}", "$defs": defs}

ex=[]
def add(n,v,note=""):
    ex.append({"def": n, "note": note, "value": v})

add("Person", AM, "am")
add("Person", BEE, "bee")
boxes=[make_box(f"B{n:02d}", room, contents, fragile, photo) for n,room,contents,fragile,photo in AM_BOX_SPECS]
for b in boxes:
    add("Box", b, b["code"])
    add("BoxLabel", box_label(b), b["code"])
for r in ROOMS:
    cl=room_checklist(r)
    add("RoomChecklist", cl, r+" empty")
    packed=AM_PACKED.get(r, [])
    add("RoomChecklist", apply_checks(cl, packed), r+" checked")
    for it in apply_checks(cl, packed)["items"][:1]:
        add("CheckItem", it, r)
add("InventoryStats", inventory_stats(boxes), "am")
add("InventoryStats", inventory_stats([]), "empty")
for q in ("ที่ชาร์จ", "จาน", "HDMI", "เปียโน", "B07", "MM-B04"):
    add("FindResult", find_item(q, boxes), q)
    fr=find_item(q, boxes)
    for h in fr["hits"]:
        add("FindHit", h, q+" "+h["code"])
tl=moving_timeline(MOVE_DATE, VAN_HOUR, ["kitchen","bedroom","living","bathroom","balcony"])
add("Timeline", tl, "am sat")
for st in tl["steps"]:
    add("TimelineStep", st, st["key"])
add("Timeline", moving_timeline("2026-12-05", 9, ["living"]), "bee early")
add("UtilityList", utility_list(AM_UTILS), "am")
add("UtilityList", utility_list({}), "fresh")
for it in utility_list(AM_UTILS)["items"]:
    add("UtilityItem", it, it["key"])
for n, vt, rg, note in ((10,"pickup","bkk","am"), (10,"pickup","province","bee"), (10,"small_truck","bkk","truck"), (0,"pickup","bkk","zero")):
    add("CostEstimate", cost_estimate(n, vt, rg), note)
add("ShareCard", share_card("พี่แอม", MOVE_DATE, inventory_stats(boxes), cost_estimate(10,"pickup")), "am")
add("Quota", quota(1,1), "free")
add("Quota", quota(3,1), "exhausted")
add("Quota", quota(0,5,pro=True), "pro")
add("SafetyGuard", safety_guard(), "ok")
add("SafetyGuard", safety_guard(True), "valuables")
add("SafetyGuard", safety_guard(False, False), "photos off device")

for e in ex:
    jsonschema.validate(e["value"], ref(e["def"]))
d=os.path.dirname(os.path.abspath(__file__))+"/.."
json.dump(schema, open(d+"/schemas.json","w"), ensure_ascii=False, indent=1)
json.dump({"examples": ex}, open(d+"/examples.json","w"), ensure_ascii=False, indent=1)
print(len(defs), "defs,", len(ex), "examples, all valid")
