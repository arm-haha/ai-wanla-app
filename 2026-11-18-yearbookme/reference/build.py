"""Generate ../schemas.json + ../examples.json and validate every example."""
import json, os, jsonschema
from yearbookme import *
from fixtures import *

S = "https://json-schema.org/draft/2020-12/schema"
s = {"type": "string"}
b = {"type": "boolean"}
u = {"type": "number", "minimum": 0, "maximum": 1}
i0 = {"type": "integer", "minimum": 0}
i1 = {"type": "integer", "minimum": 1}
pct = {"type": "integer", "minimum": 0, "maximum": 100}
era = {"enum": list(ERAS)}
tone = {"enum": TONES}
role = {"enum": list(ROLES)}
nullint = {"type": ["integer", "null"], "minimum": 0}

def obj(req, props, **kw):
    return {"type": "object", "required": req, "properties": props, "additionalProperties": False, **kw}

def arr(i, **kw):
    return {"type": "array", "items": i, **kw}

defs = {
 "Person": obj(["id", "name_th", "age", "own_photo", "consent_confirmed"], {
    "id": {"type": "string", "pattern": "^u[0-9]{2}$"}, "name_th": s, "name_en": s, "nickname_th": s,
    "age": i1, "city_th": s, "goal_th": s, "own_photo": b, "consent_confirmed": b, "guardian_ok": b,
    "all_consented": b, "celebrity_likely": b, "consented": b, "role": role}),
 "Detection": obj(["label", "confidence"], {
    "label": s, "confidence": u, "own_face": b, "celebrity_likely": b, "age_apparent": {"type": ["integer", "null"], "minimum": 0}}),
 "SelfiePhoto": obj(["id", "px_w", "px_h", "glare", "blur", "crop", "detections"], {
    "id": {"type": "string", "pattern": "^p[0-9]{2}$"}, "px_w": i1, "px_h": i1, "glare": u, "blur": u, "crop": u,
    "detections": arr({"$ref": "#/$defs/Detection"})}),
 "ScanQuality": obj(["score", "ok", "tips_th", "face_count"], {"score": pct, "ok": b, "tips_th": arr(s), "face_count": i0}),
 "IdentifiedFace": obj(["label", "confidence", "own_face", "celebrity_likely"], {
    "label": s, "confidence": u, "own_face": b, "celebrity_likely": b, "age_apparent": {"type": ["integer", "null"], "minimum": 0}}),
 "PhotoScan": obj(["photo_id", "quality", "faces", "uncertain", "face_count"], {
    "photo_id": s, "quality": {"$ref": "#/$defs/ScanQuality"}, "faces": arr({"$ref": "#/$defs/IdentifiedFace"}),
    "uncertain": arr(s), "face_count": i0}),
 "Pipeline": obj(["photo_id", "steps"], {"photo_id": s, "steps": arr(s, minItems=1)}),
 "ConsentGuard": obj(["ok", "level", "reasons_th", "blocks_th", "message_th", "face_count", "disclaimer_th"], {
    "ok": b, "level": {"enum": ["ok", "block"]}, "reasons_th": arr(s), "blocks_th": arr(s),
    "message_th": s, "face_count": i0, "disclaimer_th": s}),
 "EraInfo": obj(["id", "era", "name_th", "name_en", "year_label", "grade_th", "palette", "typography", "props_th", "hair_th", "clothes_th"], {
    "id": {"type": "string", "pattern": "^e[0-9a-z]{2}$"}, "era": era, "name_th": s, "name_en": s, "year_label": s,
    "grade_th": s, "palette": arr(s, minItems=1), "typography": s, "props_th": arr(s), "hair_th": s, "clothes_th": s}),
 "StyleRender": obj(["photo_id", "era", "name_th", "name_en", "year_label", "score", "badge_th", "grade_th",
                    "palette", "typography", "grain", "flash", "frame", "props_th", "hair_th", "clothes_th", "headline_th", "hook_th"], {
    "photo_id": s, "era": era, "name_th": s, "name_en": s, "year_label": s, "score": pct, "badge_th": s, "grade_th": s,
    "palette": arr(s), "typography": s, "grain": u, "flash": u, "frame": s, "props_th": arr(s),
    "hair_th": s, "clothes_th": s, "headline_th": s, "hook_th": s}),
 "EraStudio": obj(["photo_id", "name_th", "top_era", "top_score", "renders", "count"], {
    "photo_id": s, "name_th": s, "top_era": era, "top_score": pct,
    "renders": arr({"$ref": "#/$defs/StyleRender"}, minItems=3, maxItems=3), "count": i1}),
 "PropKit": obj(["era", "name_th", "props_th", "frame", "tip_th"], {
    "era": era, "name_th": s, "props_th": arr(s, minItems=1), "frame": s, "tip_th": s}),
 "CaptionQuote": obj(["n", "era", "tone", "text_th", "for_name_th"], {
    "n": i1, "era": era, "tone": tone, "text_th": s, "for_name_th": s}),
 "Autograph": obj(["from_name_th", "to_name_th", "era", "tone", "text_th", "char_count"], {
    "from_name_th": s, "to_name_th": s, "era": era, "tone": tone, "text_th": s, "char_count": i0}),
 "MemberSlot": obj(["id", "name_th", "name_en", "nickname_th", "role", "role_th", "era", "score", "headline_th", "consented"], {
    "id": s, "name_th": s, "name_en": s, "nickname_th": s, "role": role, "role_th": s, "era": era,
    "score": pct, "headline_th": s, "consented": b}),
 "YearbookPage": obj(["title_th", "school_th", "year", "era", "year_label", "frame", "palette", "members", "member_count", "cols", "rows", "disclaimer_th"], {
    "title_th": s, "school_th": s, "year": {"type": "integer", "minimum": 1900, "maximum": 2100}, "era": era,
    "year_label": s, "frame": s, "palette": arr(s), "members": arr({"$ref": "#/$defs/MemberSlot"}, minItems=1),
    "member_count": i1, "cols": i1, "rows": i1, "disclaimer_th": s}),
 "PrintSheet": obj(["name_th", "era", "year_label", "quote_th", "layout", "label_th", "sizes", "bleed_mm", "watermark", "cta_th"], {
    "name_th": s, "era": era, "year_label": s, "quote_th": s, "layout": {"enum": ["portrait_a4", "four_up", "sticker"]},
    "label_th": s, "sizes": arr(s, minItems=1), "bleed_mm": i0, "watermark": s, "cta_th": s}),
 "ShareCard": obj(["title_th", "headline_th", "hook_th", "era", "score", "quote_th", "layout", "sizes", "watermark", "cta_th"], {
    "title_th": s, "headline_th": s, "hook_th": s, "era": era, "score": pct, "quote_th": s,
    "layout": {"enum": ["era_portrait"]}, "sizes": arr({"enum": ["1080x1350", "1080x1920", "1080x1080"]}),
    "watermark": s, "cta_th": s}),
 "Quota": obj(["allowed", "left_after", "paywall"], {"allowed": i0, "left_after": {"type": ["integer", "null"], "minimum": 0}, "paywall": b}),
 "SafetyGuard": obj(["level", "message_th"], {"level": {"enum": ["ok", "warn", "stop"]}, "message_th": s}),
}
schema = {"$schema": S, "$id": "https://example.com/yearbookme.schema.json", "title": "YearbookMe", "$defs": defs}

def ref(n):
    return {"$ref": f"#/$defs/{n}", "$defs": defs}

ex = []
def add(n, v, note=""):
    ex.append({"def": n, "note": note, "value": v})

for p in PEOPLE:
    slim = {k: p[k] for k in ("id", "name_th", "name_en", "nickname_th", "age", "city_th", "goal_th",
                              "own_photo", "consent_confirmed", "guardian_ok", "all_consented",
                              "celebrity_likely", "consented", "role")}
    add("Person", slim, p["name_th"])

for ph in PHOTOS:
    add("SelfiePhoto", ph, ph["id"])
    add("PhotoScan", photo_scan(ph), ph["id"])
    add("Pipeline", {"photo_id": ph["id"], "steps": pipeline_steps(ph)}, ph["id"])

add("Detection", MIND_PHOTO["detections"][0], "mind face")
add("ScanQuality", scan_quality(0.62, 0.48, 0.55, 1), "bad photo")
add("IdentifiedFace", photo_scan(MIND_PHOTO)["faces"][0], "mind")

add("ConsentGuard", consent_guard(MIND_PHOTO, MIND_PROFILE), "mind ok")
add("ConsentGuard", consent_guard(MIND_PHOTO, dict(MIND_PROFILE, own_photo=False)), "not own")
add("ConsentGuard", consent_guard(PHOTOS[7], dict(MIND_PROFILE, all_consented=False)), "group no consent")
add("ConsentGuard", consent_guard(PHOTOS[8], dict(MIND_PROFILE, own_photo=False, celebrity_likely=True)), "celeb")
add("ConsentGuard", consent_guard(PRAE["photo"], dict(age=16, own_photo=True, consent_confirmed=True,
                                                     guardian_ok=False, all_consented=True, celebrity_likely=False)), "teen no guardian")
add("ConsentGuard", consent_guard(PRAE["photo"], {k: PRAE[k] for k in MIND_PROFILE}), "teen with guardian")

for e in ERA_IDS:
    add("EraInfo", era_info(e), e)
    add("PropKit", prop_kit(e), e)

for person in (MIND, FERN, TANG):
    studio = era_studio(person["photo"], person["traits"], person["name_th"])
    add("EraStudio", studio, person["name_th"])
    for r in studio["renders"]:
        add("StyleRender", r, f"{person['name_th']} {r['era']}")

for era_k, tone_k, who in (("90s", "sweet", "น้องมายด์"), ("80s", "funny", "พี่เฟิร์น"), ("y2k", "proud", "น้องตัง"),
                           ("90s", "nostalgic", "พี่เกรซ"), ("80s", "sweet", "น้องแพร")):
    for q in caption_quotes(era_k, tone_k, who, 2):
        add("CaptionQuote", q, f"{who} {era_k} {tone_k} {q['n']}")

add("Autograph", autograph("พี่เฟิร์น", "น้องมายด์", "90s", "sweet"), "fern to mind")
add("Autograph", autograph("น้องตัง", "พี่เกรซ", "y2k", "funny"), "tang to grace")

slots90 = [member_slot(p, "90s", p["traits"], p["role"]) for p in (MIND, FERN, TANG, GRACE)]
for sl in slots90:
    add("MemberSlot", sl, sl["name_th"])
add("YearbookPage", yearbook_page("หน้ารุ่นจำลอง 2026", "Ficto University", 2026, "90s", slots90), "four friends")
slots5 = [member_slot(p, "90s", p["traits"], p["role"]) for p in PEOPLE]
add("YearbookPage", yearbook_page("รุ่นทดลอง", "Ficto", 2026, "90s", slots5), "five grid")

q_mind = caption_quotes("90s", "sweet", "น้องมายด์", 1)[0]["text_th"]
add("PrintSheet", print_sheet("น้องมายด์", "90s", q_mind, "portrait_a4"), "a4")
add("PrintSheet", print_sheet("น้องมายด์", "90s", q_mind, "four_up"), "four up")
add("PrintSheet", print_sheet("น้องตัง", "y2k", "โกลว์นี้เก็บไว้", "sticker"), "sticker")
add("ShareCard", share_card("น้องมายด์", "90s", 88, q_mind), "mind 90s")
add("ShareCard", share_card("พี่เฟิร์น", "80s", 78, caption_quotes("80s", "funny", "พี่เฟิร์น", 1)[0]["text_th"]), "fern 80s")
add("Quota", quota(1, 1), "free")
add("Quota", quota(3, 1), "exhausted")
add("Quota", quota(0, 5, pro=True), "pro")
add("SafetyGuard", safety_guard(True, 22), "adult ok")
add("SafetyGuard", safety_guard(False, 22), "no consent")
add("SafetyGuard", safety_guard(True, 16), "teen warn")
add("SafetyGuard", safety_guard(True, 11), "child stop")

for e in ex:
    jsonschema.validate(e["value"], ref(e["def"]))

d = os.path.dirname(os.path.abspath(__file__)) + "/.."
json.dump(schema, open(d + "/schemas.json", "w"), ensure_ascii=False, indent=1)
json.dump({"examples": ex}, open(d + "/examples.json", "w"), ensure_ascii=False, indent=1)
print(len(defs), "defs,", len(ex), "examples, all valid")
