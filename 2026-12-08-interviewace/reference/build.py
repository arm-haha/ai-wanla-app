"""Generate ../schemas.json + ../examples.json and validate every example."""
import json, os, jsonschema
from interviewace import *
from fixtures import *

S = "https://json-schema.org/draft/2020-12/schema"
s = {"type": "string"}
b = {"type": "boolean"}
i0 = {"type": "integer", "minimum": 0}
i1 = {"type": "integer", "minimum": 1}
pct = {"type": "integer", "minimum": 0, "maximum": 100}
role = {"enum": list(ROLES)}
nullint = {"type": ["integer", "null"], "minimum": 0}

def obj(req, props, **kw):
    return {"type": "object", "required": req, "properties": props, "additionalProperties": False, **kw}

def arr(i, **kw):
    return {"type": "array", "items": i, **kw}

defs = {
 "Person": obj(["id", "name_th", "age", "role"], {
    "id": {"type": "string", "pattern": "^u[0-9]{2}$"}, "name_th": s, "name_en": s, "age": i1,
    "city_th": s, "role": role, "job_th": s, "company_th": s, "duration_sec": i0, "question_index": i0}),
 "RoleInfo": obj(["id", "role", "name_th", "name_en", "seniority", "questions", "count"], {
    "id": {"type": "string", "pattern": "^r[0-9]{2}$"}, "role": role, "name_th": s, "name_en": s,
    "seniority": {"enum": ["entry", "junior", "mid"]}, "questions": arr(s, minItems=1), "count": i1}),
 "QuestionCard": obj(["role", "index", "prompt_th", "role_th", "ideal_sec", "ideal_words"], {
    "role": role, "index": i0, "prompt_th": s, "role_th": s, "ideal_sec": i1, "ideal_words": i1}),
 "FillerCount": obj(["counts", "total", "word_count", "ratio", "label_th"], {
    "counts": obj(list(FILLERS), {f: i0 for f in FILLERS}),
    "total": i0, "word_count": i1, "ratio": {"type": "number", "minimum": 0}, "label_th": s}),
 "StarFlags": obj(["S", "T", "A", "R"], {"S": b, "T": b, "A": b, "R": b}),
 "AnswerScore": obj(["overall", "structure", "clarity", "length", "star", "band_th", "word_count", "filler_total", "filler_ratio", "star_flags", "headline_th", "disclaimer_th"], {
    "overall": pct, "structure": pct, "clarity": pct, "length": pct, "star": pct,
    "band_th": {"enum": ["พร้อมมาก", "พร้อมปานกลาง", "ต้องซ้อมอีก"]},
    "word_count": i1, "filler_total": i0, "filler_ratio": {"type": "number", "minimum": 0},
    "star_flags": {"$ref": "#/$defs/StarFlags"}, "duration_sec": nullint, "headline_th": s, "disclaimer_th": s}),
 "StarRewrite": obj(["situation_th", "task_th", "action_th", "result_th", "text_th", "char_count", "tip_th"], {
    "situation_th": s, "task_th": s, "action_th": s, "result_th": s, "text_th": s, "char_count": i0, "tip_th": s}),
 "ConfidenceReport": obj(["name_th", "role_th", "overall", "band_th", "structure", "clarity", "length", "star", "tips_th", "headline_th", "disclaimer_th"], {
    "name_th": s, "role_th": s, "overall": pct, "band_th": s, "structure": pct, "clarity": pct,
    "length": pct, "star": pct, "tips_th": arr(s, minItems=1), "headline_th": s, "disclaimer_th": s}),
 "Drill": obj(["focus", "task_th", "minutes"], {"focus": {"enum": ["star", "clarity", "length", "structure"]}, "task_th": s, "minutes": i1}),
 "ShareCard": obj(["title_th", "headline_th", "hook_th", "role_th", "overall", "layout", "sizes", "watermark", "cta_th", "disclaimer_th"], {
    "title_th": s, "headline_th": s, "hook_th": s, "role_th": s, "overall": pct,
    "layout": {"enum": ["score_report"]}, "sizes": arr({"enum": ["1080x1350", "1080x1920", "1080x1080"]}),
    "watermark": s, "cta_th": s, "disclaimer_th": s}),
 "Quota": obj(["allowed", "left_after", "paywall"], {"allowed": i0, "left_after": {"type": ["integer", "null"], "minimum": 0}, "paywall": b}),
 "SafetyGuard": obj(["level", "message_th"], {"level": {"enum": ["ok", "warn", "stop"]}, "message_th": s}),
}
schema = {"$schema": S, "$id": "https://example.com/interviewace.schema.json", "title": "InterviewAce", "$defs": defs}

def ref(n):
    return {"$ref": f"#/$defs/{n}", "$defs": defs}

ex = []
def add(n, v, note=""):
    ex.append({"def": n, "note": note, "value": v})

for p in PEOPLE:
    slim = {k: p[k] for k in ("id", "name_th", "name_en", "age", "city_th", "role", "job_th", "company_th", "duration_sec", "question_index")}
    add("Person", slim, p["name_th"])

for r in ROLE_IDS:
    add("RoleInfo", role_info(r), r)
    for i in range(4):
        add("QuestionCard", question_card(r, i), f"{r}-{i}")

add("FillerCount", filler_count(GUN_TRANSCRIPT), "gun")
add("FillerCount", filler_count(PIN["transcript"]), "pin")
add("FillerCount", filler_count("อ่า เอ่อ แบบ คือ ก็ ทดสอบ"), "all fillers")
add("StarFlags", star_flags(GUN_TRANSCRIPT), "gun missing R")
add("StarFlags", star_flags(PIN["transcript"]), "pin full")
add("StarFlags", star_flags("สวัสดี ครับ"), "none")

gun = score_answer(GUN_TRANSCRIPT, 35)
pin = score_answer(PIN["transcript"], 75)
add("AnswerScore", gun, "gun 72")
add("AnswerScore", pin, "pin")
add("AnswerScore", score_answer(GUN_TRANSCRIPT, None), "gun no duration")
add("AnswerScore", score_answer("สวัสดี ครับ ผม ชื่อ กันต์", 10), "short")
add("StarRewrite", star_rewrite(GUN_STAR["situation"], GUN_STAR["task"], GUN_STAR["action"], GUN_STAR["result"]), "gun")
add("StarRewrite", star_rewrite("เคยทำโครงงานกลุ่ม", "แบ่งงานและนัดประชุม", "จัดตารางส่งงาน", "ส่งได้ตามกำหนดและได้เกรด A"), "pin style")
add("ConfidenceReport", confidence_report(gun, "น้องกันต์", "งานการตลาด"), "gun")
add("ConfidenceReport", confidence_report(pin, "น้องปิน", "จบใหม่ / ยังไม่มีประสบการณ์งาน"), "pin")
for f in ("star", "clarity", "length", "structure"):
    add("Drill", drill(f), f)
add("ShareCard", share_card("น้องกันต์", 72, "พร้อมปานกลาง", "งานการตลาด"), "gun")
add("ShareCard", share_card("น้องปิน", pin["overall"], pin["band_th"], "จบใหม่ / ยังไม่มีประสบการณ์งาน"), "pin")
add("Quota", quota(1, 1), "free")
add("Quota", quota(3, 1), "exhausted")
add("Quota", quota(2, 2), "partial")
add("Quota", quota(0, 5, pro=True), "pro")
add("SafetyGuard", safety_guard(True), "ok")
add("SafetyGuard", safety_guard(False), "stop")

# extra scores for depth
for dur in (45, 60, 75, 90):
    add("AnswerScore", score_answer(GUN_TRANSCRIPT, dur), f"gun {dur}s")
for role_k, idx in (("engineer", 1), ("nurse", 2), ("teacher", 0), ("sales", 3)):
    add("QuestionCard", question_card(role_k, idx), f"extra {role_k}")


samples = [
    "ตอนนั้น ฉัน ต้อง พูด ใน ที่ ประชุม งานที่ คือ นำเสนอ แผน ฉันจึง ซ้อม กับ เพื่อน ผลคือ ได้ ไฟเขียว",
    "อ่า ผม อยาก ได้ งาน นี้ แบบ มาก เอ่อ เพราะ ชอบ ทีม",
    "ครั้งหนึ่ง ฉัน รับ ฟีดแบก หน้าที่ คือ แก้ งาน ฉันจึง ปรับ สไลด์ ทั้ง ชุด ได้ยอด ชม จาก ผู้จัดการ",
    "ช่วงนั้น เดดไลน์ ใกล้ ได้รับมอบ ให้ ช่วย ทีม เลยลงมือ เขียน เอกสาร เสร็จตาม เวลา ที่ กำหนด ไว้",
]
for i, tx in enumerate(samples):
    add("AnswerScore", score_answer(tx, 50+i*5), f"sample {i}")
    add("FillerCount", filler_count(tx), f"fill {i}")
    add("StarFlags", star_flags(tx), f"flags {i}")
    add("ConfidenceReport", confidence_report(score_answer(tx, 50+i*5), "ผู้ซ้อม", "งานทั่วไป"), f"rep {i}")
for e in ex:
    jsonschema.validate(e["value"], ref(e["def"]))

d = os.path.dirname(os.path.abspath(__file__)) + "/.."
json.dump(schema, open(d + "/schemas.json", "w"), ensure_ascii=False, indent=1)
json.dump({"examples": ex}, open(d + "/examples.json", "w"), ensure_ascii=False, indent=1)
print(len(defs), "defs,", len(ex), "examples, all valid")
