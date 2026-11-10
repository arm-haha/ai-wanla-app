"""Generate ../schemas.json + ../examples.json and validate every example."""
import json, os, jsonschema
from dashdoc import *
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
sym = {"enum": list(LIGHTS)}
level = {"enum": list(LEVELS)}
color = {"enum": COLORS}
nullint = {"type": ["integer", "null"], "minimum": 0}

def obj(req, props, **kw):
    return {"type": "object", "required": req, "properties": props, "additionalProperties": False, **kw}

def arr(i, **kw):
    return {"type": "array", "items": i, **kw}

fixid = {"type": "string", "pattern": "^f[0-9]{2}$"}
defs = {
 "Car": obj(["id", "model_th", "year", "fuel", "car_class", "odometer_km"], {
    "id": {"type": "string", "pattern": "^c[0-9]{2}$"}, "model_th": s, "year": {"type": "integer", "minimum": 1990, "maximum": 2100},
    "fuel": {"enum": FUELS}, "car_class": {"enum": list(CAR_CLASSES)}, "odometer_km": i0}),
 "Person": obj(["id", "name_th", "age", "region", "car"], {
    "id": {"type": "string", "pattern": "^u[0-9]{2}$"}, "name_th": s, "name_en": s, "age": i1, "city_th": s, "goal_th": s,
    "region": {"enum": list(REGION_MULT)}, "car": {"$ref": "#/$defs/Car"}}),
 "Detection": obj(["symbol", "color_seen", "confidence"], {"symbol": sym, "color_seen": color, "confidence": u, "flashing": b}),
 "DashPhoto": obj(["id", "px_w", "px_h", "glare", "blur", "tilt", "detections"], {
    "id": {"type": "string", "pattern": "^p[0-9]{2}$"}, "px_w": i1, "px_h": i1, "glare": u, "blur": u, "tilt": u,
    "detections": arr({"$ref": "#/$defs/Detection"})}),
 "ScanQuality": obj(["score", "ok", "tips_th"], {"score": pct, "ok": b, "tips_th": arr(s)}),
 "IdentifiedLight": obj(["symbol", "name_th", "name_en", "color_seen", "flashing", "confidence", "severity"], {
    "symbol": sym, "name_th": s, "name_en": s, "color_seen": color, "flashing": b, "confidence": u, "severity": level}),
 "LightScan": obj(["photo_id", "quality", "lights", "uncertain", "light_count"], {
    "photo_id": s, "quality": {"$ref": "#/$defs/ScanQuality"}, "lights": arr({"$ref": "#/$defs/IdentifiedLight"}),
    "uncertain": arr(sym), "light_count": i0}),
 "Pipeline": obj(["photo_id", "steps"], {"photo_id": s, "steps": arr(s, minItems=1)}),
 "LightInfo": obj(["id", "symbol", "name_th", "name_en", "color", "meaning_th", "drive_km", "drive_days", "max_speed", "checks", "fixes"], {
    "id": {"type": "string", "pattern": "^w[0-9]{2}$"}, "symbol": sym, "name_th": s, "name_en": s, "color": color, "meaning_th": s,
    "drive_km": nullint, "drive_days": nullint, "max_speed": nullint, "checks": arr({"enum": list(CHECK_TEXT)}), "fixes": arr(fixid)}),
 "Verdict": obj(["level", "score", "can_drive", "max_km", "max_speed_kmh", "within_days", "headline_th", "answer_th", "reasons_th"], {
    "level": level, "score": pct, "can_drive": b, "max_km": nullint, "max_speed_kmh": nullint, "within_days": nullint,
    "headline_th": s, "answer_th": s, "reasons_th": arr(s)}),
 "DoNowSteps": arr(obj(["n", "key", "text_th"], {"n": i1, "key": s, "text_th": s}), minItems=1),
 "FixPrice": obj(["fix_id", "name_th", "min_thb", "max_thb"], {"fix_id": fixid, "name_th": s, "min_thb": i0, "max_thb": i0, "for_symbol": sym}),
 "QuoteCheck": obj(["fix_id", "quote_thb", "min_thb", "max_thb", "verdict", "message_th", "questions_th", "disclaimer_th"], {
    "fix_id": fixid, "quote_thb": i0, "min_thb": i0, "max_thb": i0, "verdict": {"enum": ["low", "fair", "high", "very_high"]},
    "message_th": s, "questions_th": arr(s, minItems=1), "disclaimer_th": s}),
 "MechanicCard": obj(["title_th", "name_th", "car_model_th", "odometer_km", "symbols", "symptoms", "level", "budget_min_thb", "budget_max_thb",
                      "note_th", "line_share_url", "disclaimer_th"], {
    "title_th": s, "name_th": s, "car_model_th": s, "odometer_km": i0, "symbols": arr(sym, minItems=1), "symptoms": arr({"enum": list(SYMPTOMS)}),
    "level": level, "budget_min_thb": i0, "budget_max_thb": i0, "note_th": s,
    "line_share_url": {"type": "string", "pattern": "^https://line\\.me/R/share\\?text="}, "disclaimer_th": s}),
 "ServiceEntry": obj(["id", "car_id", "date", "odometer_km", "item", "cost_thb", "shop_th", "on_device"], {
    "id": s, "car_id": s, "date": date, "odometer_km": i0, "item": {"enum": list(SERVICE_ITEMS)}, "cost_thb": i0, "shop_th": s, "on_device": b}),
 "NextDue": obj(["item", "label_th", "due_km", "due_date"], {"item": {"enum": list(SERVICE_ITEMS)}, "label_th": s, "due_km": nullint, "due_date": date}),
 "ReminderStatus": obj(["item", "label_th", "status", "days_left", "km_left", "due_km", "due_date"], {
    "item": {"enum": list(SERVICE_ITEMS)}, "label_th": s, "status": {"enum": ["ok", "soon", "due", "overdue"]}, "days_left": {"type": "integer"},
    "km_left": {"type": ["integer", "null"]}, "due_km": nullint, "due_date": date}),
 "DiaryStats": obj(["count", "total_thb", "avg_thb", "last_odometer_km", "top_item"], {
    "count": i0, "total_thb": i0, "avg_thb": i0, "last_odometer_km": nullint, "top_item": {"type": ["string", "null"]}}),
 "Hotline": obj(["key", "label_th", "number", "kind", "note_th"], {
    "key": {"enum": ["police", "highway_police", "medical", "insurer", "tow", "garage"]}, "label_th": s, "number": {"type": ["string", "null"]},
    "kind": {"enum": ["public", "placeholder", "user"]}, "note_th": s}),
 "EmergencyKit": obj(["contacts", "missing", "kit_items_th", "guides"], {
    "contacts": arr({"$ref": "#/$defs/Hotline"}, minItems=1), "missing": arr(s), "kit_items_th": arr(s), "guides": arr(s)}),
 "Guide": obj(["key", "title_th", "tools_th", "steps", "disclaimer_th"], {
    "key": {"enum": list(GUIDES)}, "title_th": s, "tools_th": arr(s),
    "steps": arr(obj(["n", "text_th"], {"n": i1, "text_th": s}), minItems=1), "disclaimer_th": s}),
 "ShareCard": obj(["title_th", "headline_th", "hook_th", "symbols", "level", "score", "layout", "sizes", "watermark", "cta_th"], {
    "title_th": s, "headline_th": s, "hook_th": s, "symbols": arr(sym), "level": level, "score": pct, "layout": {"enum": ["scan_result"]},
    "sizes": arr({"enum": ["1080x1350", "1080x1920", "1080x1080"]}), "watermark": s, "cta_th": s}),
 "Quota": obj(["allowed", "left_after", "paywall"], {"allowed": i0, "left_after": {"type": ["integer", "null"], "minimum": 0}, "paywall": b}),
 "SafetyGuard": obj(["level", "message_th"], {"level": {"enum": ["ok", "warn", "stop"]}, "message_th": s}),
}
schema = {"$schema": S, "$id": "https://example.com/dashdoc.schema.json", "title": "DashDoc", "$defs": defs}

def ref(n):
    return {"$ref": f"#/$defs/{n}", "$defs": defs}

ex = []
def add(n, v, note=""):
    ex.append({"def": n, "note": note, "value": v})

for p in PEOPLE:
    add("Person", p, p["name_th"])
    add("Car", p["car"], p["car"]["id"])
for ph in PHOTOS:
    add("DashPhoto", ph, ph["id"])
    add("LightScan", light_scan(ph), ph["id"])
    add("Pipeline", {"photo_id": ph["id"], "steps": pipeline_steps(ph)}, ph["id"])
add("Detection", OAT_PHOTO["detections"][0], "oat check engine")
add("ScanQuality", scan_quality(0.3, 0.6, 0.5, 3), "bad photo")
add("IdentifiedLight", light_scan(OAT_PHOTO)["lights"][0], "oat top")
for k in ["check_engine", "oil_pressure", "coolant_temp", "tpms", "abs", "dpf", "high_beam", "seat_belt"]:
    v = LIGHTS[k]
    add("LightInfo", {"id": v["id"], "symbol": k, "name_th": v["name_th"], "name_en": v["name_en"], "color": v["color"], "meaning_th": v["meaning_th"],
                      "drive_km": v["drive_km"], "drive_days": v["drive_days"], "max_speed": v["max_speed"], "checks": v["checks"], "fixes": v["fixes"]}, k)

oat_lights = light_scan(OAT_PHOTO)["lights"]
oat_syms = [l["symbol"] for l in oat_lights]
ov = drive_verdict(oat_lights, OAT_SYMPTOMS)
add("Verdict", ov, "oat yellow ~50km")
add("Verdict", drive_verdict(light_scan(PHOTOS[1])["lights"]), "muk red oil")
add("Verdict", drive_verdict(light_scan(PHOTOS[2])["lights"]), "somchai overheating")
add("Verdict", drive_verdict(light_scan(PHOTOS[3])["lights"]), "nan battery")
add("Verdict", drive_verdict(light_scan(PHOTOS[4])["lights"]), "beam all info")
add("Verdict", drive_verdict(light_scan(PHOTOS[5])["lights"]), "flashing check engine")
add("Verdict", drive_verdict(oat_lights, ["smoke", "burning_smell"]), "oat + smoke escalates")
add("DoNowSteps", do_now_steps("yellow", oat_syms), "oat")
add("DoNowSteps", do_now_steps("red", ["oil_pressure"]), "muk")
add("DoNowSteps", do_now_steps("red", ["coolant_temp"]), "somchai")
add("DoNowSteps", do_now_steps("green", ["washer"]), "beam")

fixes = likely_fixes(oat_syms, OAT["region"], OAT_CAR["car_class"])
for f in fixes:
    add("FixPrice", f, "oat " + f["fix_id"])
add("FixPrice", price_range("f07", "tourist", "sedan"), "nan battery tourist sedan")
add("FixPrice", price_range("f12", "province", "suv_pickup"), "somchai radiator province pickup")
for fid, q in OAT_QUOTES:
    add("QuoteCheck", quote_check(fid, q, "bkk", "eco"), f"oat {fid} quote {q}")
add("QuoteCheck", quote_check("f03", 9000), "very high")
add("QuoteCheck", quote_check("f07", 900), "low")
add("MechanicCard", mechanic_card(OAT, OAT_CAR, ov, oat_syms, OAT_SYMPTOMS, fixes, "ไม่มีเสียงผิดปกติ เครื่องเดินเรียบ"), "oat")
mp = PEOPLE[1]
add("MechanicCard", mechanic_card(mp, mp["car"], drive_verdict(light_scan(PHOTOS[1])["lights"]), ["oil_pressure"], ["knocking"],
                                  likely_fixes(["oil_pressure"], "province", "eco")), "muk")
entries = [service_entry(*e) for e in SERVICE_LOG]
for e in entries:
    add("ServiceEntry", e, e["id"])
    add("NextDue", next_due(e), e["id"])
    add("ReminderStatus", reminder_status(e, OAT_CAR["odometer_km"], TODAY), e["id"])
add("DiaryStats", diary_stats(entries), "oat diary")
add("DiaryStats", diary_stats([]), "empty")
add("EmergencyKit", emergency_kit({}), "fresh install")
add("EmergencyKit", emergency_kit({"insurer_hotline": "<เบอร์ในกรมธรรม์>", "insurer_th": "FictoInsure", "garage_phone": "081-000-0000"}), "filled")
for g in GUIDES:
    add("Guide", guide(g), g)
add("ShareCard", share_card("พี่โอ๊ต", oat_syms, ov), "oat")
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
