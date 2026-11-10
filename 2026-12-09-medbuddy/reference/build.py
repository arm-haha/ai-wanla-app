"""Generate ../schemas.json + ../examples.json and validate every example."""
import json, os, jsonschema
from medbuddy import *
from fixtures import *

S = "https://json-schema.org/draft/2020-12/schema"
s = {"type": "string"}
b = {"type": "boolean"}
u = {"type": "number", "minimum": 0, "maximum": 1}
i0 = {"type": "integer", "minimum": 0}
i1 = {"type": "integer", "minimum": 1}
pct = {"type": "integer", "minimum": 0, "maximum": 100}
slot = {"enum": list(SLOTS)}
food = {"enum": list(FOOD)}
nullint = {"type": ["integer", "null"], "minimum": 0}

def obj(req, props, **kw):
    return {"type": "object", "required": req, "properties": props, "additionalProperties": False, **kw}

def arr(i, **kw):
    return {"type": "array", "items": i, **kw}

defs = {
 "Person": obj(["id", "name_th", "age"], {
    "id": {"type": "string", "pattern": "^[up][0-9]{2}$"}, "name_th": s, "name_en": s, "age": i1,
    "city_th": s, "relation_th": s, "clinic_th": s, "doctor_th": s, "visit_date": s}),
 "LabelPhoto": obj(["id", "px_w", "px_h", "glare", "blur", "crop"], {
    "id": {"type": "string", "pattern": "^p[0-9]{2}$"}, "px_w": i1, "px_h": i1, "glare": u, "blur": u, "crop": u}),
 "ScanQuality": obj(["score", "ok", "tips_th"], {"score": pct, "ok": b, "tips_th": arr(s)}),
 "PhotoScan": obj(["photo_id", "quality"], {"photo_id": s, "quality": {"$ref": "#/$defs/ScanQuality"}}),
 "Pipeline": obj(["photo_id", "steps"], {"photo_id": s, "steps": arr(s, minItems=1)}),
 "LibraryItem": obj(["id", "name", "kind_th", "form_th", "disclaimer_th"], {
    "id": {"type": "string", "pattern": "^m[0-9]{2}$"}, "name": s, "kind_th": s, "form_th": s, "disclaimer_th": s}),
 "ParsedLabel": obj(["name", "strength_th", "dose_th", "slots", "food", "food_th", "qty", "confidence", "needs_confirm", "message_th", "disclaimer_th"], {
    "name": s, "strength_th": s, "dose_th": s, "slots": arr(slot, minItems=1), "food": food, "food_th": s,
    "qty": i0, "daily_units": nullint, "confidence": u, "needs_confirm": b,
    "prn_max_per_day": nullint, "message_th": s, "disclaimer_th": s}),
 "ScheduleItem": obj(["name", "strength_th", "dose_th", "food_th"], {"name": s, "strength_th": s, "dose_th": s, "food_th": s}),
 "ScheduleSlot": obj(["slot", "slot_th", "items", "count"], {
    "slot": slot, "slot_th": s, "items": arr({"$ref": "#/$defs/ScheduleItem"}), "count": i0}),
 "Schedule": obj(["slots", "med_count", "slot_count", "headline_th", "disclaimer_th"], {
    "slots": arr({"$ref": "#/$defs/ScheduleSlot"}, minItems=1), "med_count": i1, "slot_count": i1, "headline_th": s, "disclaimer_th": s}),
 "Refill": obj(["name", "qty", "status", "prn", "message_th", "disclaimer_th"], {
    "name": s, "qty": i0, "daily_units": nullint, "days_left": nullint, "due_date": {"type": ["string", "null"]},
    "status": {"enum": ["ok", "soon", "due", "ask"]}, "prn": b, "message_th": s, "disclaimer_th": s}),
 "MissedGuide": obj(["slot", "slot_th", "steps_th", "headline_th", "disclaimer_th"], {
    "slot": slot, "slot_th": s, "steps_th": arr(s, minItems=3), "headline_th": s, "disclaimer_th": s}),
 "InteractionFlag": obj(["level", "med_count", "message_th", "disclaimer_th"], {
    "level": {"enum": ["ok", "ask"]}, "med_count": i0, "message_th": s, "disclaimer_th": s}),
 "VisitCard": obj(["patient_th", "clinic_th", "doctor_th", "visit_date", "meds", "med_count", "headline_th", "disclaimer_th"], {
    "patient_th": s, "clinic_th": s, "doctor_th": s, "visit_date": s, "meds": arr(s, minItems=1),
    "med_count": i1, "note_th": s, "headline_th": s, "disclaimer_th": s}),
 "CaregiverShare": obj(["caregiver_th", "patient_th", "date", "pending_slots_th", "slot_count", "headline_th", "cta_th", "disclaimer_th"], {
    "caregiver_th": s, "patient_th": s, "date": s, "pending_slots_th": arr(s), "slot_count": i0,
    "headline_th": s, "cta_th": s, "disclaimer_th": s}),
 "ShareCard": obj(["title_th", "headline_th", "hook_th", "med_count", "layout", "sizes", "watermark", "cta_th", "disclaimer_th"], {
    "title_th": s, "headline_th": s, "hook_th": s, "med_count": i1,
    "layout": {"enum": ["schedule_card"]}, "sizes": arr({"enum": ["1080x1350", "1080x1920", "1080x1080"]}),
    "watermark": s, "cta_th": s, "disclaimer_th": s}),
 "Quota": obj(["allowed", "left_after", "paywall"], {"allowed": i0, "left_after": {"type": ["integer", "null"], "minimum": 0}, "paywall": b}),
 "SafetyGuard": obj(["level", "message_th"], {"level": {"enum": ["ok", "warn", "stop"]}, "message_th": s}),
}
schema = {"$schema": S, "$id": "https://example.com/medbuddy.schema.json", "title": "MedBuddy", "$defs": defs}

def ref(n):
    return {"$ref": f"#/$defs/{n}", "$defs": defs}

ex = []
def add(n, v, note=""):
    ex.append({"def": n, "note": note, "value": v})

add("Person", {k: NON[k] for k in ("id", "name_th", "name_en", "age", "city_th", "relation_th")}, "non")
add("Person", {k: WANDEE[k] for k in ("id", "name_th", "name_en", "age", "city_th", "clinic_th", "doctor_th", "visit_date")}, "wandee")

for ph in PHOTOS:
    add("LabelPhoto", ph, ph["id"])
    add("PhotoScan", photo_scan(ph), ph["id"])
    add("Pipeline", {"photo_id": ph["id"], "steps": pipeline_steps(ph, [PRIL_RAW, MET_RAW, PAIN_RAW])}, ph["id"])
add("Pipeline", {"photo_id": "p01", "steps": pipeline_steps(PHOTOS[0], [LOW_RAW])}, "low conf")
add("ScanQuality", scan_quality(0.62, 0.48, 0.55), "bad")

for name in LIBRARY:
    add("LibraryItem", library_info(name), name)

for lab, note in ((PRIL, "pril"), (MET, "met"), (PAIN, "pain"), (LOW, "low")):
    add("ParsedLabel", lab, note)

sch = schedule(MEDS)
add("Schedule", sch, "three meds")
for sl in sch["slots"]:
    add("ScheduleSlot", sl, sl["slot"])
    for it in sl["items"]:
        add("ScheduleItem", it, it["name"] + " " + sl["slot"])

for med, st in ((PRIL, TODAY), (MET, TODAY), (PAIN, TODAY)):
    add("Refill", refill(med, st, TODAY), med["name"])
add("Refill", refill(parse_label(dict(PRIL_RAW, qty=0)), TODAY, TODAY), "due")
add("Refill", refill(parse_label(dict(PRIL_RAW, qty=40)), TODAY, TODAY), "ok 40")

for sl in SLOTS:
    add("MissedGuide", missed_dose_guide(sl), sl)

add("InteractionFlag", interaction_flag(MEDS), "three")
add("InteractionFlag", interaction_flag([PRIL]), "one")
add("VisitCard", visit_card(WANDEE["name_th"], MEDS, WANDEE["clinic_th"], WANDEE["doctor_th"], WANDEE["visit_date"], "นำซองยาจริงไปด้วย"), "visit")
add("CaregiverShare", caregiver_share(NON["name_th"], WANDEE["name_th"], sch, TODAY), "share")
add("ShareCard", share_card("คุณวันดี", 3, sch["headline_th"]), "card")
add("Quota", quota(1, 1), "free")
add("Quota", quota(3, 1), "exhausted")
add("Quota", quota(2, 2), "partial")
add("Quota", quota(0, 5, pro=True), "pro")
add("SafetyGuard", safety_guard(True), "ok")
add("SafetyGuard", safety_guard(False), "stop")

# extra labels for depth
cough = parse_label({"name": "FictoCough", "strength_th": "5 ml", "dose_th": "วันละ 3 ครั้ง หลังอาหาร",
                     "slots": ["morning", "noon", "evening"], "food": "after_food", "qty": 30, "daily_units": 3, "confidence": 0.86})
vit = parse_label({"name": "FictoVit", "strength_th": "1 เม็ด", "dose_th": "วันละ 1 เม็ด เช้า",
                   "slots": ["morning"], "food": "with_food", "qty": 60, "daily_units": 1, "confidence": 0.95})
add("ParsedLabel", cough, "cough")
add("ParsedLabel", vit, "vit")
add("Schedule", schedule([cough, vit]), "cough+vit")
add("Refill", refill(cough, TODAY, TODAY), "cough refill")
add("Refill", refill(vit, TODAY, TODAY), "vit refill")
add("VisitCard", visit_card("คุณวันดี", [cough, vit], "Ficto Clinic", "นพ.วันชัย (สมมติ)", "2026-12-16"), "visit 2")


# extra confirm-edge and qty sweep
for conf in (0.2, 0.59, 0.6, 0.75, 0.99):
    add("ParsedLabel", parse_label(dict(PRIL_RAW, confidence=conf)), f"conf {conf}")
for qty in (1, 7, 13, 15, 28, 90):
    lab = parse_label(dict(MET_RAW, qty=qty))
    add("ParsedLabel", lab, f"met qty {qty}")
    add("Refill", refill(lab, TODAY, TODAY), f"met refill {qty}")
for qty in (5, 10, 11, 20):
    lab = parse_label(dict(PAIN_RAW, qty=qty))
    add("Refill", refill(lab, TODAY, TODAY), f"pain {qty}")
add("Schedule", schedule([PRIL]), "pril only")
add("Schedule", schedule([PRIL, MET]), "pril+met")
add("CaregiverShare", caregiver_share("พี่นนท์", "คุณวันดี", schedule([PRIL, MET]), TODAY), "two slots")
add("ShareCard", share_card("คุณวันดี", 1, "ตารางกินยา 1 รายการ"), "one")
add("InteractionFlag", interaction_flag([PRIL, MET]), "two")
for e in ex:
    jsonschema.validate(e["value"], ref(e["def"]))

d = os.path.dirname(os.path.abspath(__file__)) + "/.."
json.dump(schema, open(d + "/schemas.json", "w"), ensure_ascii=False, indent=1)
json.dump({"examples": ex}, open(d + "/examples.json", "w"), ensure_ascii=False, indent=1)
print(len(defs), "defs,", len(ex), "examples, all valid")
