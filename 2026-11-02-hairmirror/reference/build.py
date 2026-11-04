"""Generate ../schemas.json + ../examples.json and validate every example."""
import json, os, jsonschema
from hairmirror import *
from fixtures import *
S = "https://json-schema.org/draft/2020-12/schema"
n0 = {"type": "number", "minimum": 0}; s = {"type": "string"}; b = {"type": "boolean"}
shape = {"enum": SHAPES}; htype = {"enum": ["straight", "wavy", "curly", "coily"]}
def obj(req, props, **kw): return {"type": "object", "required": req, "properties": props, **kw}
def arr(i): return {"type": "array", "items": i}
defs = {
 "Profile": obj(["name", "hair_type", "max_daily_minutes", "budget_month_thb"], {"name": s, "age": {"type": "integer", "minimum": 13},
   "hair_type": htype, "thickness": {"enum": ["fine", "medium", "thick"]}, "current_length_cm": n0, "max_daily_minutes": n0,
   "budget_month_thb": n0, "gender_style": {"enum": ["masc", "femme", "any"]}}),
 "FaceLandmarkExtract": obj(["face_found", "face_length", "forehead_w", "cheek_w", "jaw_w", "confidence", "retake_reason_th"],
   {"face_found": b, "face_length": {"type": ["number", "null"]}, "forehead_w": {"type": ["number", "null"]}, "cheek_w": {"type": ["number", "null"]},
    "jaw_w": {"type": ["number", "null"]}, "hairline_visible": b, "current_hair": obj([], {"type": htype, "length_cm": {"type": ["number", "null"]},
    "natural_level": {"type": ["integer", "null"], "minimum": 1, "maximum": 10}}), "confidence": {"type": "number", "minimum": 0, "maximum": 1},
    "retake_reason_th": {"type": ["string", "null"]}}),
 "FaceShape": obj(["shape", "shape_th", "length_to_width", "jaw_to_cheek", "forehead_to_cheek"], {"shape": shape, "shape_th": s,
   "length_to_width": n0, "jaw_to_cheek": n0, "forehead_to_cheek": n0}),
 "Style": obj(["id", "name_th", "length", "suits", "hair_types", "daily_minutes", "salon_cost_thb", "maintenance_weeks", "barber_phrase_th"],
   {"id": {"type": "string", "pattern": "^[a-z0-9_]+$"}, "name_th": s, "length": {"enum": ["short", "medium", "long"]}, "suits": arr(shape),
    "hair_types": arr(htype), "daily_minutes": n0, "salon_cost_thb": n0, "maintenance_weeks": {"type": "number", "exclusiveMinimum": 0},
    "neutral_ok": b, "barber_phrase_th": s, "dont_th": arr(s)}),
 "TryOnRequest": obj(["style_id", "source_photo", "prompt"], {"style_id": s, "source_photo": s, "prompt": s, "keep_identity": b,
   "seed": {"type": "integer"}}),
 "TryOnResult": obj(["style_id", "image_url", "identity_ok", "status"], {"style_id": s, "image_url": {"type": ["string", "null"]},
   "identity_ok": b, "status": {"enum": ["ok", "retry", "blocked"]}, "note_th": {"type": ["string", "null"]}}),
 "StyleMatch": obj(["style_id", "score", "face_fit", "upkeep_month_thb", "verdict", "reasons_th"], {"style_id": s,
   "score": {"type": "integer", "minimum": 0, "maximum": 100}, "face_fit": b, "upkeep_month_thb": n0, "verdict": {"enum": ["ปัง", "ลองได้", "เสี่ยง"]},
   "reasons_th": arr(s)}),
 "BarberCard": obj(["style_id", "name_th", "zones", "say_to_barber_th"], {"style_id": s, "name_th": s,
   "zones": arr(obj(["zone", "length_mm"], {"zone": {"enum": ["top", "fringe", "sides", "back", "neckline"]}, "length_mm": n0, "note_th": s})),
   "top_to_side_ratio": {"type": ["number", "null"]}, "say_to_barber_th": s, "dont_th": arr(s)}),
 "Vote": obj(["voter", "option"], {"voter": {"type": "string", "minLength": 1}, "option": s}),
 "PollResult": obj(["total_votes", "rows", "winner", "tie"], {"total_votes": {"type": "integer", "minimum": 0},
   "rows": arr(obj(["option", "votes", "pct"], {"option": s, "votes": {"type": "integer", "minimum": 0}, "pct": {"type": "number", "minimum": 0, "maximum": 100}})),
   "winner": {"type": ["string", "null"]}, "tie": b}),
 "ColorCheck": obj(["lift_levels", "needs_bleach", "bleach_sessions", "tone_fit", "est_cost_thb", "target_th", "warning_th"],
   {"lift_levels": {"type": "integer", "minimum": 0}, "needs_bleach": b, "bleach_sessions": {"type": "integer", "minimum": 0}, "tone_fit": b,
    "est_cost_thb": n0, "target_th": s, "warning_th": s}),
 "GrowOut": obj(["months", "weeks", "trim_needed", "assumption_th"], {"months": n0, "weeks": {"type": "integer", "minimum": 0}, "trim_needed": b, "assumption_th": s}),
 "CutLog": obj(["date", "style_id"], {"date": {"type": "string", "format": "date"}, "style_id": s, "salon": s, "price_thb": n0,
   "photo": b, "rating": {"type": "integer", "minimum": 1, "maximum": 5}, "note_th": s}),
 "CutReminder": obj(["next_cut_date", "maintenance_weeks"], {"next_cut_date": {"type": "string", "format": "date"}, "maintenance_weeks": n0}),
 "YearCost": obj(["month_thb", "year_thb"], {"month_thb": n0, "year_thb": n0}),
 "ShareCard": obj(["kind", "title_th", "big_stat", "sub_th"], {"kind": {"enum": ["try_on_grid", "before_after", "poll", "barber_card", "face_shape"]},
   "title_th": s, "big_stat": s, "sub_th": s, "disclaimer_th": s}),
}
schema = {"$schema": S, "$id": "hairmirror.schemas.json", "title": "HairMirror schemas", "$defs": defs}
DIS = "ภาพลองทรงสร้างด้วย AI ผลจริงขึ้นกับสภาพผมและฝีมือช่าง"
fs = face_shape(MEAS); top = rank_styles(STYLES, PROFILE, fs["shape"], 9); poll = poll_tally(POLL, VOTES); card = barber_card(STYLES[0], ZONES)
ex = {
 "Profile": [PROFILE, {"name": "พลอย", "hair_type": "wavy", "thickness": "medium", "current_length_cm": 30, "max_daily_minutes": 10, "budget_month_thb": 500, "gender_style": "femme"}],
 "FaceLandmarkExtract": [
  {"face_found": True, **MEAS, "hairline_visible": True, "current_hair": {"type": "straight", "length_cm": 6, "natural_level": 2}, "confidence": 0.91, "retake_reason_th": None},
  {"face_found": True, "face_length": None, "forehead_w": None, "cheek_w": 15.0, "jaw_w": None, "hairline_visible": False, "current_hair": {"type": "straight", "length_cm": None, "natural_level": None}, "confidence": 0.34, "retake_reason_th": "หมวก/หน้าม้าบังหน้าผาก ลองเปิดหน้าผากแล้วถ่ายใหม่"},
  {"face_found": False, "face_length": None, "forehead_w": None, "cheek_w": None, "jaw_w": None, "hairline_visible": False, "current_hair": {}, "confidence": 0.0, "retake_reason_th": "ไม่เจอใบหน้า ถ่ายหน้าตรงในที่สว่าง"}],
 "FaceShape": [fs] + [face_shape(m) for m in [{"face_length": 24, "forehead_w": 14, "cheek_w": 15, "jaw_w": 13}, {"face_length": 20, "forehead_w": 15.5, "cheek_w": 15, "jaw_w": 12}, {"face_length": 18, "forehead_w": 14.5, "cheek_w": 15, "jaw_w": 14.5}]],
 "Style": STYLES,
 "TryOnRequest": [{"style_id": "two_block", "source_photo": "local://selfie-001.jpg", "prompt": "เปลี่ยนเฉพาะทรงผมเป็น two-block textured ...", "keep_identity": True, "seed": 42}],
 "TryOnResult": [{"style_id": "two_block", "image_url": "local://tryon-two_block.jpg", "identity_ok": True, "status": "ok", "note_th": None},
                 {"style_id": "mullet", "image_url": None, "identity_ok": False, "status": "retry", "note_th": "หน้าเพี้ยน กำลังสร้างใหม่"}],
 "StyleMatch": top,
 "BarberCard": [card],
 "Vote": VOTES,
 "PollResult": [poll, poll_tally(["a", "b"], [{"voter": "x", "option": "a"}, {"voter": "y", "option": "b"}])],
 "ColorCheck": [color_check(2, 6, "cool", "milk_tea"), color_check(2, 4, "warm", "chocolate"), color_check(3, 4, "warm", "ash")],
 "GrowOut": [grow_out(6, 12), grow_out(12, 6)],
 "CutLog": [{"date": "2026-11-02", "style_id": "two_block", "salon": "ร้านตัดผมหน้าปากซอย", "price_thb": 250, "photo": True, "rating": 5, "note_th": "ช่างทำตามการ์ดเป๊ะ"}],
 "CutReminder": [cut_reminder("2026-11-02", 4)],
 "YearCost": [year_cost(STYLES[0]), year_cost(STYLES[2], 50)],
 "ShareCard": [
  {"kind": "try_on_grid", "title_th": "ลอง 9 ทรงใน 30 วิ", "big_stat": "9 ทรง", "sub_th": "หน้ากลม · ผมตรงหนา", "disclaimer_th": DIS},
  {"kind": "before_after", "title_th": "ก่อน/หลัง ทูบล็อก", "big_stat": "100/100", "sub_th": "เข้ากับหน้ากลม ค่าดูแล ~฿271/เดือน", "disclaimer_th": DIS},
  {"kind": "poll", "title_th": "เพื่อนเลือกให้แล้ว", "big_stat": "71%", "sub_th": "5 จาก 7 โหวตทูบล็อก", "disclaimer_th": DIS},
  {"kind": "barber_card", "title_th": "ยื่นให้ช่างเลย", "big_stat": "ข้าง 6 มิล · บน 7 ซม.", "sub_th": STYLES[0]["barber_phrase_th"], "disclaimer_th": DIS},
  {"kind": "face_shape", "title_th": "หน้าฉันทรงอะไร", "big_stat": "หน้ากลม", "sub_th": "ยาว/กว้าง 1.22 · กราม/โหนก 0.86", "disclaimer_th": DIS}],
}
here = os.path.dirname(os.path.abspath(__file__))
json.dump(schema, open(os.path.join(here, "..", "schemas.json"), "w"), ensure_ascii=False, indent=1)
json.dump(ex, open(os.path.join(here, "..", "examples.json"), "w"), ensure_ascii=False, indent=1)
n = 0
for k, items in ex.items():
    sub = {"$schema": S, "$defs": defs, "$ref": f"#/$defs/{k}"}
    for it in items: jsonschema.validate(it, sub); n += 1
print(f"{len(defs)} defs, {n} examples valid")
