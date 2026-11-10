"""Generate ../schemas.json + ../examples.json and validate every example."""
import json, os, jsonschema
from tripstitch import *
from fixtures import *

S = "https://json-schema.org/draft/2020-12/schema"
s = {"type": "string"}
b = {"type": "boolean"}
u = {"type": "number", "minimum": 0, "maximum": 1}
i0 = {"type": "integer", "minimum": 0}
i1 = {"type": "integer", "minimum": 1}
pct = {"type": "integer", "minimum": 0, "maximum": 100}
typ = {"enum": TYPES}
src = {"enum": SOURCES}
slot = {"enum": SLOTS}
climate = {"enum": CLIMATES}
hour = {"type": ["integer", "null"], "minimum": 0, "maximum": 24}
nullint = {"type": ["integer", "null"], "minimum": 0}

def obj(req, props, **kw):
    return {"type": "object", "required": req, "properties": props, "additionalProperties": False, **kw}

def arr(i, **kw):
    return {"type": "array", "items": i, **kw}

defs = {
 "Person": obj(["id", "name_th", "age", "dest_th", "start_date", "nights", "pax", "budget_thb"], {
    "id": {"type": "string", "pattern": "^u[0-9]{2}$"}, "name_th": s, "name_en": s, "age": i1,
    "city_th": s, "goal_th": s, "dest_th": s, "start_date": {"type": "string", "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}$"},
    "nights": i1, "pax": i1, "budget_thb": i0, "climates": arr(climate)}),
 "Detection": obj(["id", "name_th", "area", "type", "confidence"], {
    "id": s, "name_th": s, "name_en": s, "area": s, "type": typ, "confidence": u, "source": src,
    "open_hour": hour, "close_hour": hour, "closed_dow": arr({"type": "integer", "minimum": 0, "maximum": 6}),
    "ticket_thb": i0, "note_th": s}),
 "Screenshot": obj(["id", "px_w", "px_h", "glare", "blur", "crop", "detections"], {
    "id": {"type": "string", "pattern": "^s[0-9]{2}$"}, "px_w": i1, "px_h": i1, "glare": u, "blur": u, "crop": u,
    "detections": arr({"$ref": "#/$defs/Detection"})}),
 "ScanQuality": obj(["score", "ok", "tips_th", "place_hint_count"], {"score": pct, "ok": b, "tips_th": arr(s), "place_hint_count": i0}),
 "Place": obj(["id", "name_th", "name_en", "area", "type", "source", "confidence", "open_hour", "close_hour", "closed_dow", "ticket_thb", "note_th"], {
    "id": s, "name_th": s, "name_en": s, "area": s, "type": typ, "source": src, "confidence": u,
    "open_hour": hour, "close_hour": hour, "closed_dow": arr({"type": "integer", "minimum": 0, "maximum": 6}),
    "ticket_thb": i0, "note_th": s}),
 "Extract": obj(["shot_id", "quality", "places", "uncertain", "place_count"], {
    "shot_id": s, "quality": {"$ref": "#/$defs/ScanQuality"}, "places": arr({"$ref": "#/$defs/Place"}),
    "uncertain": arr(s), "place_count": i0}),
 "Pipeline": obj(["shot_id", "steps"], {"shot_id": s, "steps": arr(s, minItems=1)}),
 "Stitch": obj(["shot_ids", "places", "place_count", "uncertain", "areas"], {
    "shot_ids": arr(s, minItems=1), "places": arr({"$ref": "#/$defs/Place"}), "place_count": i0,
    "uncertain": arr(s), "areas": arr(s)}),
 "Stop": obj(["n", "place_id", "name_th", "area", "type", "slot", "travel_min"], {
    "n": i1, "place_id": s, "name_th": s, "area": s, "type": typ, "slot": slot, "travel_min": i0,
    "open_hour": hour, "close_hour": hour}),
 "DayPlan": obj(["day", "date", "dow", "stops", "stop_count", "areas", "total_travel_min"], {
    "day": i1, "date": {"type": "string", "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}$"}, "dow": s,
    "stops": arr({"$ref": "#/$defs/Stop"}), "stop_count": i0, "areas": arr(s), "total_travel_min": i0}),
 "TripPlan": obj(["start_date", "nights", "days", "pax", "itinerary", "place_count"], {
    "start_date": s, "nights": i1, "days": i1, "pax": i1,
    "itinerary": arr({"$ref": "#/$defs/DayPlan"}, minItems=1), "place_count": i1}),
 "ClosedWarning": obj(["day", "date", "place_id", "name_th", "message_th"], {
    "day": i1, "date": s, "place_id": s, "name_th": s, "message_th": s}),
 "RainPlan": obj(["tips_th", "indoor_alts", "disclaimer_th"], {
    "tips_th": arr(s, minItems=1),
    "indoor_alts": arr(obj(["name_th", "area", "type"], {"name_th": s, "area": s, "type": typ})),
    "disclaimer_th": s}),
 "BudgetLine": obj(["key", "label_th", "thb"], {"key": s, "label_th": s, "thb": i0}),
 "BudgetSplit": obj(["budget_thb", "planned_thb", "buffer_thb", "total_thb", "per_pax_thb", "pax", "nights", "lines", "verdict", "message_th", "disclaimer_th"], {
    "budget_thb": i0, "planned_thb": i0, "buffer_thb": i0, "total_thb": i0, "per_pax_thb": i0,
    "pax": i1, "nights": i1, "lines": arr({"$ref": "#/$defs/BudgetLine"}, minItems=1),
    "verdict": {"enum": ["unknown", "under", "fit", "tight", "over"]}, "message_th": s, "disclaimer_th": s}),
 "PackItem": obj(["key", "text_th", "group"], {"key": s, "text_th": s, "group": {"enum": ["clothes", "weather", "activity", "essentials"]}}),
 "PackingList": obj(["nights", "days", "climates", "count", "items"], {
    "nights": i1, "days": i1, "climates": arr(climate), "count": i0, "items": arr({"$ref": "#/$defs/PackItem"})}),
 "ShareCard": obj(["title_th", "headline_th", "hook_th", "days_th", "total_thb", "verdict", "layout", "sizes", "watermark", "offline", "cta_th"], {
    "title_th": s, "headline_th": s, "hook_th": s, "days_th": s, "total_thb": i0,
    "verdict": {"enum": ["unknown", "under", "fit", "tight", "over"]},
    "layout": {"enum": ["trip_card"]}, "sizes": arr({"enum": ["1080x1350", "1080x1920", "1080x1080"]}),
    "watermark": s, "offline": b, "cta_th": s}),
 "Quota": obj(["allowed", "left_after", "paywall"], {"allowed": i0, "left_after": {"type": ["integer", "null"], "minimum": 0}, "paywall": b}),
 "SafetyGuard": obj(["level", "message_th"], {"level": {"enum": ["ok", "warn", "stop"]}, "message_th": s}),
}
schema = {"$schema": S, "$id": "https://example.com/tripstitch.schema.json", "title": "TripStitch", "$defs": defs}

def ref(n):
    return {"$ref": f"#/$defs/{n}", "$defs": defs}

ex = []
def add(n, v, note=""):
    ex.append({"def": n, "note": note, "value": v})

for p in PEOPLE:
    add("Person", p, p["name_th"])

for sh in KAO_SHOTS + NINA_SHOTS + PHU_SHOTS + MUK_SHOTS + [EMPTY_SHOT]:
    add("Screenshot", sh, sh["id"])
    r = extract_places(sh)
    add("Extract", r, sh["id"])
    add("Pipeline", {"shot_id": sh["id"], "steps": pipeline_steps(sh)}, sh["id"])

add("Detection", P_BEAN, "fictobean")
add("ScanQuality", scan_quality(0.66, 0.50, 0.52, 1), "bad shot")
add("Place", extract_places(KAO_SHOTS[0])["places"][0], "bean")

st_k = stitch_places(KAO_SHOTS)
st_n = stitch_places(NINA_SHOTS)
st_p = stitch_places(PHU_SHOTS)
add("Stitch", st_k, "kao")
add("Stitch", st_n, "nina")
add("Stitch", st_p, "phu")

plan_k = plan_days(st_k["places"], KAO["start_date"], KAO["nights"], KAO["pax"])
plan_n = plan_days(st_n["places"], NINA["start_date"], NINA["nights"], NINA["pax"])
plan_p = plan_days(st_p["places"], PHU["start_date"], PHU["nights"], PHU["pax"])
plan_tue = plan_days(st_k["places"], "2026-12-05", 3, 2)
for plan, note in ((plan_k, "kao"), (plan_n, "nina"), (plan_p, "phu"), (plan_tue, "tue start")):
    add("TripPlan", plan, note)
    for d in plan["itinerary"]:
        add("DayPlan", d, f"{note} day {d['day']}")
        for st in d["stops"]:
            add("Stop", st, f"{note} {st['place_id']}")

for w in closed_warnings(plan_tue, st_k["places"]):
    add("ClosedWarning", w, w["name_th"])
add("RainPlan", rain_plan(plan_k, st_k["places"]), "kao rain")

for places, nights, pax, budget, stay, note in (
    (st_k["places"], 3, 2, 8000, None, "kao fit"),
    (st_k["places"], 3, 2, 12000, None, "kao under"),
    (st_k["places"], 3, 2, 7200, None, "kao tight"),
    (st_k["places"], 3, 2, 4000, None, "kao over"),
    (st_k["places"], 3, 2, 0, None, "kao no budget"),
    (NINA_PLACES, 1, 1, 2500, None, "nina over"),
    (PHU_PLACES, 2, 4, 9000, None, "phu fit"),
    (st_k["places"], 3, 2, 8000, 0, "kao no stay"),
):
    b = budget_split(places, nights, pax, budget, stay)
    add("BudgetSplit", b, note)
    for ln in b["lines"]:
        add("BudgetLine", ln, f"{note} {ln['key']}")

for nights, clim, types, note in (
    (3, KAO["climates"], [p["type"] for p in st_k["places"]], "kao"),
    (1, ["hot"], ["cafe"], "nina hot"),
    (2, ["cold", "rain_possible"], ["market", "viewpoint", "cafe"], "phu"),
):
    pk = packing_list(nights, clim, types)
    add("PackingList", pk, note)
    add("PackItem", pk["items"][0], note + " first")

add("ShareCard", share_card("ทริปพี่เก้า", "เชียงใหม่", plan_k, budget_split(st_k["places"], 3, 2, 8000)), "kao")
add("ShareCard", share_card("ทริปพี่ภู", "เชียงคาน", plan_p, budget_split(PHU_PLACES, 2, 4, 9000)), "phu")
add("Quota", quota(1, 1), "free")
add("Quota", quota(3, 1), "exhausted")
add("Quota", quota(0, 5, pro=True), "pro")
add("SafetyGuard", safety_guard(True, 0), "ok")
add("SafetyGuard", safety_guard(True, 1), "warn closed")
add("SafetyGuard", safety_guard(False), "no places")

for e in ex:
    jsonschema.validate(e["value"], ref(e["def"]))

d = os.path.dirname(os.path.abspath(__file__)) + "/.."
json.dump(schema, open(d + "/schemas.json", "w"), ensure_ascii=False, indent=1)
json.dump({"examples": ex}, open(d + "/examples.json", "w"), ensure_ascii=False, indent=1)
print(len(defs), "defs,", len(ex), "examples, all valid")
