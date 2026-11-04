"""Generate ../schemas.json + ../examples.json and validate every example."""
import json, os, jsonschema
from memoryfix import *
from fixtures import *
S = "https://json-schema.org/draft/2020-12/schema"
s = {"type": "string"}; b = {"type": "boolean"}; n0 = {"type": "number", "minimum": 0}; u = {"type": "number", "minimum": 0, "maximum": 1}
i0 = {"type": "integer", "minimum": 0}; yr = {"type": ["integer", "null"], "minimum": 1850, "maximum": 2030}
step = {"enum": STEPS}; lvl = {"enum": [l[1] for l in LEVELS]}
def obj(req, props, **kw): return {"type": "object", "required": req, "properties": props, "additionalProperties": False, **kw}
def arr(i, **kw): return {"type": "array", "items": i, **kw}
dmg = obj(list(DAMAGE_W), {k: u for k in DAMAGE_W})
defs = {
 "Photo": obj(["id", "title_th", "year_est", "is_bw", "px_w", "px_h", "faces", "people", "scan", "skewed", "glare"], {"id": {"type": "string", "pattern": "^p[0-9]{2,}$"},
   "title_th": s, "year_est": yr, "is_bw": b, "px_w": {"type": "integer", "minimum": 1}, "px_h": {"type": "integer", "minimum": 1}, "faces": i0,
   "people": arr(s), "scan": dmg, "skewed": b, "glare": b}),
 "ScanExtract": obj(["photo_found", "corners", "glare", "is_bw", "faces", "damage", "year_est", "year_confidence", "era_clues_th", "retake_reason_th"], {
   "photo_found": b, "corners": {"type": ["array", "null"], "items": arr({"type": "number"}, minItems=2, maxItems=2), "minItems": 4, "maxItems": 4},
   "glare": b, "is_bw": b, "faces": i0, "damage": dmg, "year_est": yr, "year_confidence": u, "era_clues_th": arr(s), "retake_reason_th": {"type": ["string", "null"]}}),
 "DamageReport": obj(["photo_id", "score", "level", "level_th"], {"photo_id": s, "score": {"type": "integer", "minimum": 0, "maximum": 100}, "level": lvl, "level_th": s}),
 "RestorePlan": obj(["photo_id", "steps", "upscale_factor"], {"photo_id": s, "steps": arr(step, uniqueItems=True), "upscale_factor": {"enum": [1, 2, 4]}}),
 "RestoreJob": obj(["photo_id", "status", "steps_done", "before_url", "after_url"], {"photo_id": s, "status": {"enum": ["queued", "running", "done", "failed", "blocked"]},
   "steps_done": arr(step), "before_url": s, "after_url": {"type": ["string", "null"]}, "identity_check": {"enum": ["pass", "fail", "skipped"]}, "note_th": {"type": ["string", "null"]}}),
 "PrintOption": obj(["dpi", "ok"], {"dpi": i0, "ok": b}),
 "PrintOptions": {"type": "object", "propertyNames": {"enum": list(PRINT_SIZES)}, "additionalProperties": {"$ref": "#/$defs/PrintOption"}},
 "TimelineGroup": obj(["decade", "label_th", "ids"], {"decade": {"type": ["integer", "null"]}, "label_th": s, "ids": arr(s)}),
 "PeopleIndex": {"type": "object", "additionalProperties": arr(s)},
 "ThenNow": obj(["person", "then_photo_id", "now_photo_url", "caption_th"], {"person": s, "then_photo_id": s, "now_photo_url": s, "caption_th": s}),
 "VoiceStory": obj(["photo_id", "audio_url", "duration_s", "transcript_th"], {"photo_id": s, "audio_url": s, "duration_s": {"type": "number", "minimum": 0, "maximum": 180},
   "transcript_th": s, "teller": s}),
 "MotionRequest": obj(["photo_id", "person_status", "consent", "allowed"], {"photo_id": s, "person_status": {"enum": ["deceased", "living", "minor"]}, "consent": b, "allowed": b}),
 "Quota": obj(["allowed", "left_after", "paywall"], {"allowed": i0, "left_after": {"type": ["integer", "null"], "minimum": 0}, "paywall": b}),
 "ShareCard": obj(["title_th", "headline_th", "badges", "watermark", "cta_th"], {"title_th": s, "headline_th": s, "badges": arr(step), "watermark": {"const": "AI restored · MemoryFix"}, "cta_th": s}),
}
schema = {"$schema": S, "$id": "https://example.com/memoryfix.schema.json", "title": "MemoryFix", "$defs": defs}
def ref(n): return {"$ref": f"#/$defs/{n}", "$defs": defs}
ex = []
def add(n, v, note=""): ex.append({"def": n, "note": note, "value": v})
for p in PHOTOS:
    add("Photo", p, p["title_th"]); sc, lv, th = damage_score(p["scan"]); add("DamageReport", {"photo_id": p["id"], "score": sc, "level": lv, "level_th": th})
    short = min(p["px_w"], p["px_h"]); add("RestorePlan", {"photo_id": p["id"], "steps": restore_plan(p["scan"], p["is_bw"], p["faces"], short, skewed=p["skewed"], deglare_needed=p["glare"]), "upscale_factor": upscale_factor(short)})
    f = upscale_factor(short); add("PrintOptions", print_options(p["px_w"] * f, p["px_h"] * f), f"{p['id']} after x{f}")
add("PrintOptions", print_options(700, 980), "p02 raw scan before upscale")
add("ScanExtract", {"photo_found": True, "corners": [[0.08, 0.06], [0.93, 0.05], [0.95, 0.94], [0.06, 0.96]], "glare": False, "is_bw": True, "faces": 2,
   "damage": P2 if (P2 := PHOTOS[1]["scan"]) else None, "year_est": 1962, "year_confidence": 0.55, "era_clues_th": ["ชุดไทยแต่งงานทรงยุคก่อน", "ขอบรูปหยัก", "ฟิล์มขาวดำ"], "retake_reason_th": None})
add("ScanExtract", {"photo_found": False, "corners": None, "glare": True, "is_bw": False, "faces": 0, "damage": {k: 0 for k in DAMAGE_W}, "year_est": None, "year_confidence": 0,
   "era_clues_th": [], "retake_reason_th": "แสงสะท้อนบังรูป ลองเอียงมือถือ 15° หรือปิดไฟเพดาน"}, "retake")
add("RestoreJob", {"photo_id": "p02", "status": "done", "steps_done": ["repair", "denoise", "face_enhance", "sharpen", "colorize", "upscale"], "before_url": "local://p02_before.jpg",
   "after_url": "local://p02_after.jpg", "identity_check": "pass", "note_th": None})
add("RestoreJob", {"photo_id": "p01", "status": "failed", "steps_done": ["perspective", "deglare", "repair"], "before_url": "local://p01_before.jpg", "after_url": None,
   "identity_check": "fail", "note_th": "หน้าเปลี่ยนเกินไป ใช้ผลแบบไม่เสริมหน้าแทน"}, "identity guard")
for g in timeline(PHOTOS): add("TimelineGroup", g)
add("PeopleIndex", people_index(PHOTOS))
add("ThenNow", {"person": "แม่", "then_photo_id": "p01", "now_photo_url": "local://mom_2026.jpg", "caption_th": then_now_caption("แม่", 1989, NOW_YEAR)})
add("VoiceStory", {"photo_id": "p02", "audio_url": "local://p02_story.m4a", "duration_s": 74, "transcript_th": "(ตัวอย่าง) ยายเล่าว่าวันนั้นฝนตกทั้งวัน แต่ตาก็ยังมาตรงเวลา", "teller": "แม่"})
for st, c in [("deceased", True), ("living", False), ("minor", True)]:
    add("MotionRequest", {"photo_id": "p02", "person_status": st, "consent": c, "allowed": motion_allowed(st, c)})
add("Quota", quota(2, 3), "free day, 2 used"); add("Quota", quota(0, 1)); add("Quota", quota(10, 5, pro=True), "pro")
add("ShareCard", share_card("ตายายวันแต่งงาน", 66, NOW_YEAR - 1962, ["repair", "denoise", "face_enhance", "sharpen", "colorize", "upscale"]))
for e in ex: jsonschema.validate(e["value"], ref(e["def"]))
d = os.path.dirname(os.path.abspath(__file__)) + "/.."
json.dump(schema, open(d + "/schemas.json", "w"), ensure_ascii=False, indent=1)
json.dump({"examples": ex}, open(d + "/examples.json", "w"), ensure_ascii=False, indent=1)
print(len(defs), "defs,", len(ex), "examples, all valid")
