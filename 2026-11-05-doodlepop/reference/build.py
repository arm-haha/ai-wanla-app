"""Generate ../schemas.json + ../examples.json and validate every example."""
import json, os, jsonschema
from doodlepop import *
from fixtures import *
S = "https://json-schema.org/draft/2020-12/schema"
s = {"type": "string"}; b = {"type": "boolean"}; u = {"type": "number", "minimum": 0, "maximum": 1}
i0 = {"type": "integer", "minimum": 0}; i1 = {"type": "integer", "minimum": 1}; n0 = {"type": "number", "minimum": 0}
date = {"type": "string", "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}$"}
ALLP = PRESETS + ["hop", "wiggle"]; preset = {"enum": ALLP}
def obj(req, props, **kw): return {"type": "object", "required": req, "properties": props, "additionalProperties": False, **kw}
def arr(i, **kw): return {"type": "array", "items": i, **kw}
scan = obj(list(SCAN_W), {k: u for k in SCAN_W})
parts = obj(list(BONES), {k: {"type": "integer", "minimum": 0, "maximum": 8} for k in BONES})
STEP = ["perspective", "deshadow", "remove_paper", "sharpen_lines", "fill_gaps", "cutout"]
SUBJ = ["animal", "person", "robot", "vehicle", "house", "monster", "plant", "other"]
defs = {
 "Kid": obj(["id", "name_th", "birth", "avatar"], {"id": {"type": "string", "pattern": "^k[0-9]{2,}$"}, "name_th": s, "birth": date, "avatar": s}),
 "Drawing": obj(["id", "kid_id", "title_th", "subject", "drawn_on", "px_w", "px_h", "colors", "strokes", "parts", "scan"], {
   "id": {"type": "string", "pattern": "^d[0-9]{2,}$"}, "kid_id": s, "title_th": s, "subject": {"enum": SUBJ}, "drawn_on": date,
   "px_w": i1, "px_h": i1, "colors": {"type": "integer", "minimum": 1, "maximum": 24}, "strokes": i0, "parts": parts, "scan": scan}),
 "ScanExtract": obj(["drawing_found", "corners", "scan", "subject", "title_guess_th", "parts", "colors", "has_child_face", "has_text", "retake_reason_th"], {
   "drawing_found": b, "corners": {"type": ["array", "null"], "items": arr({"type": "number"}, minItems=2, maxItems=2), "minItems": 4, "maxItems": 4},
   "scan": scan, "subject": {"enum": SUBJ}, "title_guess_th": s, "parts": parts, "colors": i0, "has_child_face": b, "has_text": b,
   "retake_reason_th": {"type": ["string", "null"]}}),
 "ScanReport": obj(["drawing_id", "score", "level", "level_th", "steps", "retake_reason_th"], {"drawing_id": s, "score": {"type": "integer", "minimum": 0, "maximum": 100},
   "level": {"enum": [l[1] for l in SCAN_LEVELS]}, "level_th": s, "steps": arr({"enum": STEP}, uniqueItems=True), "retake_reason_th": {"type": ["string", "null"]}}),
 "Rig": obj(["drawing_id", "bones", "presets", "fallbacks", "needs_manual_pins"], {"drawing_id": s, "bones": i0, "presets": arr(preset, minItems=6, maxItems=6),
   "fallbacks": {"type": "object", "propertyNames": {"enum": list(FALLBACK)}, "additionalProperties": preset}, "needs_manual_pins": b}),
 "AnimationClip": obj(["preset", "label_th", "duration_s", "fps", "frames", "loop"], {"preset": preset, "label_th": s, "duration_s": n0, "fps": {"enum": [12, 24, 30]}, "frames": i1, "loop": b}),
 "ExportSpec": obj(["format", "w", "h", "fps", "duration_s", "loops", "frames", "music", "watermark"], {"format": {"enum": list(EXPORTS)}, "w": i1, "h": i1, "fps": i1,
   "duration_s": n0, "loops": i1, "frames": i1, "music": b, "watermark": {"const": WATERMARK}}),
 "Story": obj(["kid_id", "characters", "title_th", "age", "plan", "pages", "tts_voice", "safety"], {"kid_id": s, "characters": arr(s, minItems=1, maxItems=3), "title_th": s,
   "age": {"type": "integer", "minimum": 2, "maximum": 12},
   "plan": obj(["pages", "words_per_page", "total_words", "narration_s"], {"pages": {"type": "integer", "minimum": 4, "maximum": 6}, "words_per_page": i1, "total_words": i1, "narration_s": i0}),
   "pages": arr(obj(["n", "text_th", "drawing_ids", "pose"], {"n": i1, "text_th": s, "drawing_ids": arr(s, minItems=1), "pose": preset}), minItems=4, maxItems=6),
   "tts_voice": {"enum": ["th_female_warm", "th_male_warm", "parent_recorded"]}, "safety": obj(["no_scary", "no_brands", "ends_calm"], {"no_scary": b, "no_brands": b, "ends_calm": b})}),
 "YearRecap": obj(["kid_id", "year", "count", "top_subject", "avg_colors", "first_detail", "last_detail", "growth_pct", "headline_th"], {"kid_id": s, "year": {"type": "integer", "minimum": 2000},
   "count": i1, "top_subject": {"enum": SUBJ}, "avg_colors": n0, "first_detail": i0, "last_detail": i0, "growth_pct": {"type": ["integer", "null"]}, "headline_th": s}),
 "StickerPack": obj(["title_th", "count", "size", "stickers"], {"title_th": s, "count": {"enum": STICKER_COUNTS}, "size": arr(i1, minItems=2, maxItems=2),
   "stickers": arr(obj(["drawing_id", "preset", "text_th"], {"drawing_id": s, "preset": preset, "text_th": s}), minItems=8, maxItems=40)}),
 "ColoringPage": obj(["drawing_id", "age", "line_px", "paper", "regions"], {"drawing_id": s, "age": {"type": "integer", "minimum": 2, "maximum": 12}, "line_px": {"enum": [4, 6, 8]},
   "paper": {"enum": ["A4", "A5"]}, "regions": i1}),
 "DrawPrompt": obj(["date", "prompt_th", "repeat_window_days"], {"date": date, "prompt_th": {"enum": DRAW_PROMPTS}, "repeat_window_days": {"const": PROMPT_NO_REPEAT_DAYS}}),
 "ShareLink": obj(["expires_on", "view_only", "allow_download", "strip_location", "indexable"], {"expires_on": date, "view_only": b, "allow_download": b, "strip_location": {"const": True}, "indexable": {"const": False}}),
 "PrintCheck": obj(["product", "dpi", "need_dpi", "ok"], {"product": {"enum": list(PRODUCTS)}, "dpi": i0, "need_dpi": i1, "ok": b}),
 "ParentGate": obj(["action", "needs_parent", "allowed"], {"action": {"enum": sorted(PARENT_ONLY | {"animate", "story", "color", "draw_prompt", "gallery_view"})}, "needs_parent": b, "allowed": b}),
 "Quota": obj(["kind", "allowed", "left_after", "paywall"], {"kind": {"enum": ["animate", "story"]}, "allowed": i0, "left_after": {"type": ["integer", "null"], "minimum": 0}, "paywall": b}),
 "ShareCard": obj(["title_th", "headline_th", "preset", "watermark", "cta_th", "shows_child_face"], {"title_th": s, "headline_th": s, "preset": preset, "watermark": {"const": WATERMARK}, "cta_th": s, "shows_child_face": {"const": False}}),
}
schema = {"$schema": S, "$id": "https://example.com/doodlepop.schema.json", "title": "DoodlePop", "$defs": defs}
def ref(name): return {"$schema": S, "$defs": defs, "$ref": "#/$defs/" + name}
ex = []
def add(d, v, note=""): ex.append({"def": d, "note": note, "value": v})
for k in KIDS: add("Kid", k)
for d in DRAWINGS: add("Drawing", d, d["title_th"])
D06 = DRAWINGS[5]
add("ScanExtract", {"drawing_found": True, "corners": [[0.08, 0.06], [0.93, 0.05], [0.95, 0.94], [0.06, 0.95]], "scan": D06["scan"],
    "subject": "animal", "title_guess_th": "ไดโนเสาร์สีชมพูใส่มงกุฎ", "parts": D06["parts"], "colors": 6, "has_child_face": False, "has_text": True, "retake_reason_th": None}, "d06 demo")
add("ScanExtract", {"drawing_found": True, "corners": None, "scan": DRAWINGS[4]["scan"], "subject": "animal", "title_guess_th": "ปลาวาฬ", "parts": DRAWINGS[4]["parts"], "colors": 4,
    "has_child_face": False, "has_text": False, "retake_reason_th": retake_reason(DRAWINGS[4]["scan"])}, "cut off -> retake")
add("ScanExtract", {"drawing_found": False, "corners": None, "scan": {"shadow": 0, "blur": 0, "tilt": 0, "crop_cut": 0}, "subject": "other", "title_guess_th": "", "parts": {k: 0 for k in BONES},
    "colors": 0, "has_child_face": True, "has_text": False, "retake_reason_th": "ไม่เจอรูปวาดในภาพ ถ่ายเฉพาะกระดาษนะ (ภาพนี้มีหน้าเด็ก ระบบไม่เก็บ)"}, "child face, no drawing")
for d in DRAWINGS:
    sc, lv, th = scan_score(d["scan"])
    add("ScanReport", {"drawing_id": d["id"], "score": sc, "level": lv, "level_th": th, "steps": cleanup_steps(d["scan"]), "retake_reason_th": retake_reason(d["scan"])})
for d in DRAWINGS: add("Rig", {"drawing_id": d["id"], **rig(d["parts"])})
for p in ALLP: add("AnimationClip", clip(p))
add("AnimationClip", clip("dance", fps=30, loops=2), "reel loop")
add("ExportSpec", export_spec("reel_mp4", 15, 4.0), "dance reel"); add("ExportSpec", export_spec("square_mp4", 8, 2.0)); add("ExportSpec", export_spec("gif", 10, 4.0), "gif capped 6s")
plan = story_plan(5, 3)
pages = ["กาลครั้งหนึ่ง ไดโนชมพูใส่มงกุฎตื่นเช้ามา อยากหาเพื่อนเล่นที่สวนหลังบ้าน", "ไดโนเจอแมวส้มนอนอาบแดด แมวส้มบอกว่า ไปด้วยกันสิ เดี๋ยวพาไปหาช้าง",
         "ช้างกำลังพ่นน้ำเล่นสงกรานต์ ทั้งสามหัวเราะคิกคัก เปียกกันไปหมดเลย", "พระอาทิตย์เริ่มตก ทั้งสามช่วยกันเก็บดอกไม้ไปให้คุณแม่ของไดโน",
         "คืนนั้นไดโนชมพูนอนหลับฝันดี กอดมงกุฎไว้แน่น พรุ่งนี้จะเล่นกับเพื่อนอีก ราตรีสวัสดิ์"]
poses = ["wave", "walk", "dance", "jump", "sleep"]; ids = [["d06"], ["d06", "d01"], ["d06", "d01", "d03"], ["d06", "d01", "d03"], ["d06"]]
add("Story", {"kid_id": "k01", "characters": ["d06", "d01", "d03"], "title_th": "ไดโนชมพูกับเพื่อนรัก", "age": 5, "plan": plan,
    "pages": [{"n": i + 1, "text_th": t, "drawing_ids": ids[i], "pose": poses[i]} for i, t in enumerate(pages)], "tts_voice": "th_female_warm",
    "safety": {"no_scary": True, "no_brands": True, "ends_calm": True}}, "demo bedtime story (text shortened)")
add("Story", {"kid_id": "k02", "characters": ["d04"], "title_th": "หุ่นยนต์ไฟฟ้าช่วยเมือง", "age": 8, "plan": story_plan(8, 1),
    "pages": [{"n": i + 1, "text_th": f"(ตัวอย่างหน้า {i + 1})", "drawing_ids": ["d04"], "pose": p} for i, p in enumerate(["wave", "walk", "jump", "spin", "dance", "sleep"])],
    "tts_voice": "parent_recorded", "safety": {"no_scary": True, "no_brands": True, "ends_calm": True}}, "age 8, 6 pages")
for y in (2025, 2026): add("YearRecap", year_recap(DRAWINGS, KIDS[0], y))
add("YearRecap", year_recap(DRAWINGS, KIDS[1], 2026), "single drawing")
add("StickerPack", {"title_th": "ไดโนชมพูของใบเตย", "count": 8, "size": list(fit_box(2480, 3300)), "stickers": sticker_pack(["d06", "d02"], PRESETS, 8)})
for a in (3, 5, 8): add("ColoringPage", {"drawing_id": "d06", "age": a, "line_px": coloring_line_px(a), "paper": "A4", "regions": 14})
add("DrawPrompt", {"date": TODAY, "prompt_th": daily_prompt(TODAY, PROMPT_HISTORY), "repeat_window_days": PROMPT_NO_REPEAT_DAYS})
add("ShareLink", share_link(TODAY), "grandparents 7 days"); add("ShareLink", share_link(TODAY, 30, True), "30 days + download")
for pr in PRODUCTS: add("PrintCheck", print_check(2480, 3300, pr))
add("PrintCheck", print_check(1240, 1650, "tshirt"), "low-res photo")
for a, un in [("animate", False), ("export_video", False), ("export_video", True), ("grandparent_link", True), ("print_order", False)]: add("ParentGate", parent_gate(a, un))
add("Quota", quota("animate", 2, 3), "free, 2 used"); add("Quota", quota("story", 0, 1)); add("Quota", quota("animate", 9, 4, pro=True), "pro")
add("ShareCard", share_card(DRAWINGS[5], KIDS[0], age_at(KIDS[0]["birth"], "2026-11-04")["label_th"], "dance"))
for e in ex: jsonschema.validate(e["value"], ref(e["def"]))
d = os.path.dirname(os.path.abspath(__file__)) + "/.."
json.dump(schema, open(d + "/schemas.json", "w"), ensure_ascii=False, indent=1)
json.dump({"examples": ex}, open(d + "/examples.json", "w"), ensure_ascii=False, indent=1)
print(len(defs), "defs,", len(ex), "examples, all valid")
