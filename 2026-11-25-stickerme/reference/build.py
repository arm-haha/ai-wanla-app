"""Generate ../schemas.json + ../examples.json and validate every example."""
import json, os, jsonschema
from stickerme import *
from fixtures import *

def _scan(shot):
    q = scan_quality(shot["glare"], shot["blur"], shot["crop"], shot["face_conf"], shot["face_frac"])
    return {"shot_id": shot["id"], "quality": q, "ok": q["ok"], "face_conf": shot["face_conf"],
            "face_frac": shot["face_frac"], "message_th": "เจอใบหน้า พร้อมสร้างชุด" if q["ok"] else "ถ่ายใหม่: " + " · ".join(q["tips_th"])}

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
    "id": {"type": "string", "pattern": "^u[0-9]{2}$"}, "name_th": s, "name_en": s, "age": i1, "city_th": s, "goal_th": s, "style": s}),
 "Detection": obj(["key", "value", "confidence"], {"key": s, "value": True, "confidence": u}),
 "Selfie": obj(["id", "px_w", "px_h", "glare", "blur", "crop", "face_conf", "face_frac", "detections"], {
    "id": {"type": "string", "pattern": "^s[0-9]{2}$"}, "px_w": i1, "px_h": i1, "glare": u, "blur": u, "crop": u,
    "face_conf": u, "face_frac": u, "detections": arr({"$ref": "#/$defs/Detection"})}),
 "ScanQuality": obj(["score", "ok", "tips_th"], {"score": pct, "ok": b, "tips_th": arr(s)}),
 "FaceScan": obj(["shot_id", "quality", "ok", "face_conf", "face_frac", "message_th"], {
    "shot_id": s, "quality": {"$ref": "#/$defs/ScanQuality"}, "ok": b, "face_conf": u, "face_frac": u, "message_th": s}),
 "ConsentGuard": obj(["level", "code", "message_th"], {
    "level": {"enum": ["ok", "warn", "stop"]}, "code": s, "message_th": s}),
 "BubbleCheck": obj(["ok", "text_th", "chars", "max_chars", "message_th"], {
    "ok": b, "text_th": s, "chars": i0, "max_chars": i1, "message_th": s}),
 "Sticker": obj(["emotion", "emotion_id", "name_th", "style", "style_id", "w", "h", "format", "transparent", "bubble_id", "text_th", "watermark"], {
    "emotion": s, "emotion_id": s, "name_th": s, "style": s, "style_id": s, "w": i1, "h": i1,
    "format": {"enum": ["png"]}, "transparent": b,
    "bubble_id": {"type": ["string", "null"]}, "text_th": {"type": ["string", "null"]}, "watermark": s}),
 "ExportAsset": obj(["w", "h", "format"], {"w": i1, "h": i1, "format": s}),
 "StickerPack": obj(["style", "style_name_th", "count", "with_text", "stickers", "main", "tab", "headline_th", "watermark", "consent_code"], {
    "style": s, "style_name_th": s, "count": i1, "with_text": i0,
    "stickers": arr({"$ref": "#/$defs/Sticker"}),
    "main": {"$ref": "#/$defs/ExportAsset"}, "tab": {"$ref": "#/$defs/ExportAsset"},
    "headline_th": s, "watermark": s, "consent_code": s}),
 "SpecCheck": obj(["key", "ok", "detail_th"], {"key": s, "ok": b, "detail_th": s}),
 "ExportSpec": obj(["ready", "passed", "total", "checks", "sticker_w", "sticker_h", "main_w", "main_h", "tab_w", "tab_h", "max_kb_per_sticker", "headline_th", "disclaimer_th"], {
    "ready": b, "passed": i0, "total": i1, "checks": arr({"$ref": "#/$defs/SpecCheck"}),
    "sticker_w": i1, "sticker_h": i1, "main_w": i1, "main_h": i1, "tab_w": i1, "tab_h": i1,
    "max_kb_per_sticker": i1, "headline_th": s, "disclaimer_th": s}),
 "ChatItem": obj(["name_th", "text_th"], {"name_th": s, "text_th": {"type": ["string", "null"]}}),
 "ChatPreview": obj(["layout", "style", "items", "count", "watermark"], {
    "layout": {"enum": ["chat_mock"]}, "style": s, "items": arr({"$ref": "#/$defs/ChatItem"}), "count": i0, "watermark": s}),
 "StyleInfo": obj(["key", "id", "name_th", "name_en", "outline"], {"key": s, "id": s, "name_th": s, "name_en": s, "outline": b}),
 "EmotionInfo": obj(["key", "id", "name_th", "name_en", "priority"], {"key": s, "id": s, "name_th": s, "name_en": s, "priority": i1}),
 "ShareCard": obj(["title_th", "headline_th", "hook_th", "style", "count", "with_text", "export_ready", "layout", "sizes", "watermark", "cta_th"], {
    "title_th": s, "headline_th": s, "hook_th": s, "style": s, "count": i1, "with_text": i0, "export_ready": b,
    "layout": {"enum": ["sticker_card"]}, "sizes": arr({"enum": ["1080x1350", "1080x1920", "1080x1080"]}),
    "watermark": s, "cta_th": s}),
 "Quota": obj(["allowed", "left_after", "paywall"], {"allowed": i0, "left_after": {"type": ["integer", "null"], "minimum": 0}, "paywall": b}),
 "SafetyGuard": obj(["level", "message_th"], {"level": {"enum": ["ok", "warn", "stop"]}, "message_th": s}),
}
schema = {"$schema": S, "$id": "https://example.com/stickerme.schema.json", "title": "StickerMe", "$defs": defs}

def ref(n):
    return {"$ref": f"#/$defs/{n}", "$defs": defs}

ex=[]
def add(n,v,note=""):
    ex.append({"def": n, "note": note, "value": v})

for p in PEOPLE:
    add("Person", p, p["name_th"])
shots=[JANE_SELFIE, BECK_SELFIE, MIN_SELFIE, BAD_SHOT, EMPTY_SHOT, LOWCONF_SHOT]
for sh in shots:
    add("Selfie", sh, sh["id"])
    add("FaceScan", _scan(sh), sh["id"])
    add("ScanQuality", scan_quality(sh["glare"], sh["blur"], sh["crop"], sh["face_conf"], sh["face_frac"]), sh["id"])
    for d in sh["detections"][:2]:
        add("Detection", d, sh["id"]+" "+d["key"])

for note, kwargs in (
    ("jane ok", JANE_CONSENT),
    ("other", OTHER_CONSENT),
    ("no consent", {"own_face": False}),
    ("minor no", MIN_CONSENT_NO),
    ("minor yes", MIN_CONSENT_YES),
    ("celebrity", {"own_face": True, "celebrity_likeness": True}),
):
    add("ConsentGuard", consent_guard(**kwargs), note)

for t, note in (("เข้าใจแล้ว", "ok"), ("", "empty"), ("ข้อความนี้ยาวเกินกว่าที่จะใส่บนสติกเกอร์ใบเล็ก", "long"), ("กินข้าวยัง?", "eaten")):
    add("BubbleCheck", bubble_check(t), note)

jane_scan=_scan(JANE_SELFIE); jane_c=consent_guard(**JANE_CONSENT)
pack=make_pack(jane_scan, "chibi", jane_c)
add("StickerPack", pack, "jane 16")
for st in pack["stickers"][:4] + pack["stickers"][8:10]:
    add("Sticker", st, st["emotion"])
add("ExportAsset", pack["main"], "main")
add("ExportAsset", pack["tab"], "tab")
exs=export_spec(pack)
add("ExportSpec", exs, "ready")
for c in exs["checks"]:
    add("SpecCheck", c, c["key"])
add("ExportSpec", export_spec(dict(pack, count=10)), "count fail")
pack8=make_pack(_scan(BECK_SELFIE), "pop", jane_c, emotions=DEFAULT_SET_16[:8], count=8, bubble_map={"happy": "got_it"})
add("StickerPack", pack8, "beck 8")
add("ExportSpec", export_spec(pack8), "beck ready")
min_c=consent_guard(**MIN_CONSENT_YES)
add("StickerPack", make_pack(_scan(MIN_SELFIE), "comic", min_c, emotions=DEFAULT_SET_16[:8], count=8, bubble_map={}), "min 8 guardian")
prev=chat_preview(pack)
add("ChatPreview", prev, "jane")
for it in prev["items"]:
    add("ChatItem", it, it["name_th"])
for st in style_library():
    add("StyleInfo", st, st["key"])
for emo in emotion_library()[:8]:
    add("EmotionInfo", emo, emo["key"])
add("ShareCard", share_card("น้องเจน", pack, exs), "jane")
add("Quota", quota(1,1), "free")
add("Quota", quota(3,1), "exhausted")
add("Quota", quota(0,5,pro=True), "pro")
add("SafetyGuard", safety_guard(), "ok")
add("SafetyGuard", safety_guard(consent_guard(**OTHER_CONSENT)), "stop")
add("SafetyGuard", safety_guard(consent_guard(**MIN_CONSENT_YES)), "warn")

for e in ex:
    jsonschema.validate(e["value"], ref(e["def"]))
d=os.path.dirname(os.path.abspath(__file__))+"/.."
json.dump(schema, open(d+"/schemas.json","w"), ensure_ascii=False, indent=1)
json.dump({"examples": ex}, open(d+"/examples.json","w"), ensure_ascii=False, indent=1)
print(len(defs), "defs,", len(ex), "examples, all valid")
