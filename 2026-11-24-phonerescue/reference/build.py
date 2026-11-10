"""Generate ../schemas.json + ../examples.json and validate every example."""
import json, os, jsonschema
from phonerescue import *
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
    "id": {"type": "string", "pattern": "^u[0-9]{2}$"}, "name_th": s, "name_en": s, "age": i1, "city_th": s, "goal_th": s, "device_th": s}),
 "Detection": obj(["key", "value", "confidence"], {"key": s, "value": True, "confidence": u}),
 "Screenshot": obj(["id", "px_w", "px_h", "glare", "blur", "crop", "detections"], {
    "id": {"type": "string", "pattern": "^s[0-9]{2}$"}, "px_w": i1, "px_h": i1, "glare": u, "blur": u, "crop": u,
    "detections": arr({"$ref": "#/$defs/Detection"})}),
 "ScanQuality": obj(["score", "ok", "tips_th"], {"score": pct, "ok": b, "tips_th": arr(s)}),
 "StorageScan": obj(["shot_id", "quality", "ok", "used_gb", "total_gb", "free_gb", "percent", "breakdown", "message_th"], {
    "shot_id": s, "quality": {"$ref": "#/$defs/ScanQuality"}, "ok": b,
    "used_gb": {"type": ["number", "null"], "minimum": 0}, "total_gb": {"type": ["number", "null"], "minimum": 0},
    "free_gb": {"type": ["number", "null"]}, "percent": {"type": ["integer", "null"], "minimum": 0, "maximum": 100},
    "breakdown": {"type": "object", "additionalProperties": n0}, "message_th": s}),
 "BatteryScan": obj(["shot_id", "quality", "ok", "health_pct", "screen_on_h", "last_charge_h", "brightness_pct", "background_refresh", "low_power", "message_th"], {
    "shot_id": s, "quality": {"$ref": "#/$defs/ScanQuality"}, "ok": b,
    "health_pct": {"type": ["integer", "null"], "minimum": 0, "maximum": 100},
    "screen_on_h": {"type": ["number", "null"], "minimum": 0},
    "last_charge_h": {"type": ["number", "null"], "minimum": 0},
    "brightness_pct": {"type": ["number", "null"], "minimum": 0, "maximum": 100},
    "background_refresh": {"type": ["boolean", "null"]}, "low_power": {"type": ["boolean", "null"]}, "message_th": s}),
 "Pipeline": obj(["shot_id", "steps"], {"shot_id": s, "steps": arr(s, minItems=1)}),
 "CleanupAction": obj(["id", "key", "name_th", "gb", "priority", "how_th", "n"], {
    "id": s, "key": s, "name_th": s, "gb": n0, "priority": i1, "how_th": s, "n": i1}),
 "CleanupPlan": obj(["used_gb", "total_gb", "free_gb", "saved_gb", "after_used_gb", "after_free_gb", "actions", "count", "headline_th"], {
    "used_gb": n0, "total_gb": n0, "free_gb": n0, "saved_gb": n0, "after_used_gb": n0, "after_free_gb": n0,
    "actions": arr({"$ref": "#/$defs/CleanupAction"}), "count": i0, "headline_th": s}),
 "GuideStep": obj(["n", "text_th"], {"n": i1, "text_th": s}),
 "DuplicateGuide": obj(["title_th", "steps", "disclaimer_th"], {
    "title_th": s, "steps": arr({"$ref": "#/$defs/GuideStep"}, minItems=1), "disclaimer_th": s}),
 "BatteryTips": obj(["health_pct", "keys", "tips_th", "count", "headline_th"], {
    "health_pct": pct, "keys": arr(s), "tips_th": arr(s), "count": i0, "headline_th": s}),
 "RepairCheck": obj(["verdict", "message_th", "health_pct", "free_gb", "battery_min_thb", "battery_max_thb", "phone_min_thb", "phone_max_thb", "disclaimer_th"], {
    "verdict": {"enum": ["cleanup", "cleanup_then_watch", "repair_battery", "replace_or_repair", "watch"]},
    "message_th": s, "health_pct": pct, "free_gb": n0, "battery_min_thb": i0, "battery_max_thb": i0,
    "phone_min_thb": i0, "phone_max_thb": i0, "disclaimer_th": s}),
 "ShareCard": obj(["title_th", "headline_th", "hook_th", "used_gb", "total_gb", "saved_gb", "health_pct", "layout", "sizes", "watermark", "cta_th"], {
    "title_th": s, "headline_th": s, "hook_th": s, "used_gb": n0, "total_gb": n0, "saved_gb": n0,
    "health_pct": {"type": ["integer", "null"], "minimum": 0, "maximum": 100},
    "layout": {"enum": ["rescue_card"]}, "sizes": arr({"enum": ["1080x1350", "1080x1920", "1080x1080"]}),
    "watermark": s, "cta_th": s}),
 "Quota": obj(["allowed", "left_after", "paywall"], {"allowed": i0, "left_after": {"type": ["integer", "null"], "minimum": 0}, "paywall": b}),
 "SafetyGuard": obj(["level", "message_th"], {"level": {"enum": ["ok", "warn", "stop"]}, "message_th": s}),
}
schema = {"$schema": S, "$id": "https://example.com/phonerescue.schema.json", "title": "PhoneRescue", "$defs": defs}

def ref(n):
    return {"$ref": f"#/$defs/{n}", "$defs": defs}

ex=[]
def add(n,v,note=""):
    ex.append({"def": n, "note": note, "value": v})

for p in PEOPLE:
    add("Person", p, p["name_th"])
shots=[POR_STORAGE, POR_BATTERY, MUK_STORAGE, MUK_BATTERY, OLD_STORAGE, OLD_BATTERY, BAD_SHOT, EMPTY_SHOT, LOWCONF_SHOT]
for sh in shots:
    add("Screenshot", sh, sh["id"])
    add("Pipeline", {"shot_id": sh["id"], "steps": pipeline_steps(sh)}, sh["id"])
    if any("used_gb" in (d.get("key") or "") or "total_gb" in (d.get("key") or "") for d in sh["detections"]) or sh["id"] in ("s08","s09"):
        add("StorageScan", parse_storage(sh), sh["id"])
    if any("health" in (d.get("key") or "") for d in sh["detections"]) or sh is EMPTY_SHOT:
        add("BatteryScan", parse_battery(sh), sh["id"])
    add("ScanQuality", scan_quality(sh["glare"], sh["blur"], sh["crop"], len(sh["detections"])), sh["id"])
    for d in sh["detections"][:2]:
        add("Detection", d, sh["id"]+" "+d["key"])

st=parse_storage(POR_STORAGE); bt=parse_battery(POR_BATTERY); plan=cleanup_plan(st)
add("CleanupPlan", plan, "por")
for a in plan["actions"]:
    add("CleanupAction", a, a["key"])
add("CleanupPlan", cleanup_plan(st, include=["duplicates", "cache"]), "subset")
g=duplicate_guide(); add("DuplicateGuide", g, "guide")
for stt in g["steps"]:
    add("GuideStep", stt, str(stt["n"]))
for shot, note in ((POR_BATTERY,"por"), (MUK_BATTERY,"muk"), (OLD_BATTERY,"old")):
    add("BatteryTips", battery_tips(parse_battery(shot)), note)
add("RepairCheck", repair_or_replace(st, bt), "por cleanup")
add("RepairCheck", repair_or_replace(parse_storage(MUK_STORAGE), parse_battery(MUK_BATTERY)), "muk repair")
add("RepairCheck", repair_or_replace(parse_storage(OLD_STORAGE), parse_battery(OLD_BATTERY)), "old replace")
add("RepairCheck", repair_or_replace(dict(st, free_gb=20, used_gb=108), dict(bt, health_pct=90)), "watch")
add("RepairCheck", repair_or_replace(dict(st, free_gb=2), dict(bt, health_pct=82)), "cleanup then watch")
add("ShareCard", share_card("น้องปอ", st, plan, bt), "por")
add("Quota", quota(1,1), "free")
add("Quota", quota(3,1), "exhausted")
add("Quota", quota(0,5,pro=True), "pro")
add("SafetyGuard", safety_guard(), "ok")
add("SafetyGuard", safety_guard(True, False), "reset no backup")
add("SafetyGuard", safety_guard(True, True), "reset backed up")

for e in ex:
    jsonschema.validate(e["value"], ref(e["def"]))
d=os.path.dirname(os.path.abspath(__file__))+"/.."
json.dump(schema, open(d+"/schemas.json","w"), ensure_ascii=False, indent=1)
json.dump({"examples": ex}, open(d+"/examples.json","w"), ensure_ascii=False, indent=1)
print(len(defs), "defs,", len(ex), "examples, all valid")
