"""Generate ../schemas.json + ../examples.json and validate every example."""
import json, os, jsonschema
from roomglow import *
from fixtures import *
S = "https://json-schema.org/draft/2020-12/schema"
n0 = {"type": "number", "minimum": 0}; s = {"type": "string"}; b = {"type": "boolean"}; u = {"type": "number", "minimum": 0, "maximum": 1}
style = {"enum": list(STYLES_TH)}; rtype = {"enum": list(LUX)}
cat = {"enum": ["declutter", "wall", "furniture", "textile", "light", "decor", "plant"]}
def obj(req, props, **kw): return {"type": "object", "required": req, "properties": props, **kw}
def arr(i): return {"type": "array", "items": i}
defs = {
 "Room": obj(["name", "room_type", "width_m", "length_m", "height_m", "renter", "budget_thb"], {"name": s, "room_type": rtype,
   "width_m": {"type": "number", "exclusiveMinimum": 0}, "length_m": {"type": "number", "exclusiveMinimum": 0}, "height_m": {"type": "number", "exclusiveMinimum": 0},
   "doors": {"type": "integer", "minimum": 0}, "windows": {"type": "integer", "minimum": 0}, "renter": b, "budget_thb": n0, "existing_lm": n0}),
 "RoomScanExtract": obj(["room_found", "room_type", "scores", "items_seen", "wall_color_hex", "confidence", "retake_reason_th"], {"room_found": b,
   "room_type": {"enum": list(LUX) + [None]}, "scores": obj(["light", "clutter", "harmony", "cohesion"], {"light": u, "clutter": u, "harmony": u, "cohesion": u}),
   "items_seen": arr(obj(["label_th", "kind"], {"label_th": s, "kind": {"enum": ["furniture", "textile", "light", "clutter", "decor", "window", "door"]},
   "bbox": arr({"type": "number"})})), "wall_color_hex": {"type": ["string", "null"], "pattern": "^#[0-9A-Fa-f]{6}$"},
   "est_size_m": obj([], {"width": {"type": ["number", "null"]}, "length": {"type": ["number", "null"]}}), "confidence": u, "retake_reason_th": {"type": ["string", "null"]}}),
 "GlowScore": obj(["before", "after", "delta"], {"before": {"type": "integer", "minimum": 0, "maximum": 100}, "after": {"type": "integer", "minimum": 0, "maximum": 100}, "delta": {"type": "integer"}}),
 "CatalogItem": obj(["id", "name_th", "category", "price_thb", "impact", "renter_safe", "styles", "minutes"], {"id": {"type": "string", "pattern": "^[a-z0-9_]+$"},
   "name_th": s, "category": cat, "price_thb": {"type": "number", "exclusiveMinimum": 0}, "impact": {"type": "integer", "minimum": 1, "maximum": 10},
   "renter_safe": b, "styles": arr({"enum": list(STYLES_TH) + ["any"]}), "minutes": n0, "boost": {"type": "object", "additionalProperties": u},
   "shop_query_th": s}),
 "RestyleRequest": obj(["style", "source_photo", "prompt"], {"style": style, "source_photo": s, "prompt": s, "keep_layout": b, "item_ids": arr(s), "seed": {"type": "integer"}}),
 "RestyleResult": obj(["style", "image_url", "layout_ok", "status"], {"style": style, "image_url": {"type": ["string", "null"]}, "layout_ok": b,
   "status": {"enum": ["ok", "retry", "blocked"]}, "note_th": {"type": ["string", "null"]}}),
 "ShoppingPlan": obj(["style", "budget_thb", "spent_thb", "left_thb", "impact", "items", "budget_used_pct"], {"style": style, "budget_thb": n0, "spent_thb": n0,
   "left_thb": n0, "impact": {"type": "integer", "minimum": 0}, "items": arr(s), "excluded_not_renter_safe": arr(s), "budget_used_pct": {"type": "number", "minimum": 0, "maximum": 100}}),
 "PaintEstimate": obj(["liters", "cans", "cost_thb"], {"liters": n0, "cans": {"type": "integer", "minimum": 0}, "cost_thb": n0}),
 "WallpaperEstimate": obj(["rolls", "cost_thb"], {"rolls": {"type": "integer", "minimum": 0}, "cost_thb": n0}),
 "LightPlan": obj(["lumens_needed", "existing_lm", "gap_lm", "bulbs_800lm", "kelvin", "tip_th"], {"lumens_needed": {"type": "integer", "minimum": 0}, "existing_lm": n0,
   "gap_lm": n0, "bulbs_800lm": {"type": "integer", "minimum": 0}, "kelvin": {"enum": [2700, 3000, 4000]}, "tip_th": s}),
 "Palette": obj(["style", "colors"], {"style": style, "colors": arr(obj(["hex", "role"], {"hex": {"type": "string", "pattern": "^#[0-9A-Fa-f]{6}$"},
   "role": {"enum": ["base", "secondary", "accent", "wood", "metal"]}, "name_th": s}))}),
 "DeclutterItem": obj(["name", "action"], {"name": s, "action": {"enum": ["keep", "sell", "donate", "toss"]}, "resale_thb": n0}),
 "DeclutterResult": obj(["counts", "resale_thb", "removed"], {"counts": obj(["keep", "sell", "donate", "toss"], {k: {"type": "integer", "minimum": 0} for k in ["keep", "sell", "donate", "toss"]}),
   "resale_thb": n0, "removed": {"type": "integer", "minimum": 0}}),
 "WeekendPlan": obj(["steps", "total_minutes", "total_hours"], {"steps": arr(obj(["item", "name_th", "minutes", "cum_minutes"], {"item": s, "name_th": s, "minutes": n0, "cum_minutes": n0})),
   "total_minutes": n0, "total_hours": n0}),
 "Vote": obj(["voter", "option"], {"voter": {"type": "string", "minLength": 1}, "option": s}),
 "PollResult": obj(["total_votes", "rows", "winner", "tie"], {"total_votes": {"type": "integer", "minimum": 0},
   "rows": arr(obj(["option", "votes", "pct"], {"option": s, "votes": {"type": "integer", "minimum": 0}, "pct": {"type": "number", "minimum": 0, "maximum": 100}})),
   "winner": {"type": ["string", "null"]}, "tie": b}),
 "ShareCard": obj(["kind", "title_th", "big_stat", "sub_th"], {"kind": {"enum": ["style_grid", "before_after", "budget_receipt", "poll", "glow_score"]},
   "title_th": s, "big_stat": s, "sub_th": s, "disclaimer_th": s}),
}
schema = {"$schema": S, "$id": "roomglow.schemas.json", "title": "RoomGlow schemas", "$defs": defs}
DIS = "ภาพแต่งห้องสร้างด้วย AI ราคาเป็นตัวอย่าง เช็กราคาจริงก่อนซื้อ"
K = shopping_plan(CATALOG, 3000, "korean"); PK = [c for c in CATALOG if c["id"] in K["items"]]
before = glow_score(SCAN); after = score_after(SCAN, PK, True)
A = floor_area(ROOM["width_m"], ROOM["length_m"]); W = wall_area(ROOM["width_m"], ROOM["length_m"], ROOM["height_m"])
ex = {
 "Room": [ROOM, {"name": "โอ๊ต", "room_type": "studio", "width_m": 4.5, "length_m": 6.0, "height_m": 2.7, "doors": 1, "windows": 2, "renter": False, "budget_thb": 10000, "existing_lm": 1500}],
 "RoomScanExtract": [
  {"room_found": True, "room_type": "bedroom", "scores": SCAN, "items_seen": [{"label_th": "เตียง 5 ฟุต", "kind": "furniture", "bbox": [0.1, 0.45, 0.7, 0.95]},
    {"label_th": "กองเสื้อบนเก้าอี้", "kind": "clutter", "bbox": [0.72, 0.4, 0.9, 0.8]}, {"label_th": "หลอดไฟเพดานขาวดวงเดียว", "kind": "light"}],
   "wall_color_hex": "#E8E4DA", "est_size_m": {"width": 3.2, "length": 4.0}, "confidence": 0.86, "retake_reason_th": None},
  {"room_found": True, "room_type": None, "scores": {"light": 0.1, "clutter": 0.5, "harmony": 0.5, "cohesion": 0.5}, "items_seen": [], "wall_color_hex": None,
   "est_size_m": {"width": None, "length": None}, "confidence": 0.31, "retake_reason_th": "มืดเกินไป เปิดไฟแล้วถ่ายจากมุมห้องให้เห็นผนัง 2 ด้าน"},
  {"room_found": False, "room_type": None, "scores": {"light": 0, "clutter": 0, "harmony": 0, "cohesion": 0}, "items_seen": [], "wall_color_hex": None,
   "est_size_m": {}, "confidence": 0.0, "retake_reason_th": "ไม่เจอห้อง ถ่ายจากมุมห้องแนวนอน"}],
 "GlowScore": [{"before": before, "after": after, "delta": after - before}],
 "CatalogItem": CATALOG,
 "RestyleRequest": [{"style": "korean", "source_photo": "local://room-001.jpg", "prompt": "แต่งห้องนี้สไตล์เกาหลีคลีน คงผนัง หน้าต่าง ประตู เตียง ตำแหน่งเดิม ...", "keep_layout": True, "item_ids": K["items"], "seed": 7}],
 "RestyleResult": [{"style": "korean", "image_url": "local://restyle-korean.jpg", "layout_ok": True, "status": "ok", "note_th": None},
                   {"style": "boho", "image_url": None, "layout_ok": False, "status": "retry", "note_th": "หน้าต่างย้ายที่ กำลังสร้างใหม่"}],
 "ShoppingPlan": [K] + [shopping_plan(CATALOG, 3000, st) for st in ["muji", "cozy"]] + [shopping_plan(CATALOG, 1000, "korean"), shopping_plan(CATALOG, 3000, "korean", False)],
 "PaintEstimate": [paint_estimate(W)],
 "WallpaperEstimate": [wallpaper_rolls(ROOM["width_m"] * ROOM["height_m"])],
 "LightPlan": [light_plan(A, "bedroom", 800, "korean"), light_plan(A, "bedroom", 800, "cozy"), light_plan(A, "bedroom", 2500, "muji")],
 "Palette": [{"style": "korean", "colors": [{"hex": "#F7F4EE", "role": "base", "name_th": "ขาวนม"}, {"hex": "#E6DCCB", "role": "secondary", "name_th": "เบจ"},
   {"hex": "#C8B6A6", "role": "accent", "name_th": "โกโก้นม"}, {"hex": "#D9C3A5", "role": "wood", "name_th": "ไม้โอ๊คอ่อน"}]},
  {"style": "industrial", "colors": [{"hex": "#3A3A3A", "role": "base", "name_th": "ปูนเปลือย"}, {"hex": "#8C8C8C", "role": "secondary"}, {"hex": "#B5651D", "role": "accent", "name_th": "สนิมทองแดง"}, {"hex": "#222222", "role": "metal"}]}],
 "DeclutterItem": DECLUTTER,
 "DeclutterResult": [declutter(DECLUTTER)],
 "WeekendPlan": [weekend_plan(K["items"], CATALOG)],
 "Vote": VOTES,
 "PollResult": [poll_tally(POLL, VOTES), poll_tally(["a", "b"], [{"voter": "x", "option": "a"}, {"voter": "y", "option": "b"}])],
 "ShareCard": [
  {"kind": "style_grid", "title_th": "ห้องเดียว 6 ลุค", "big_stat": "6 สไตล์", "sub_th": "ห้องนอนคอนโด 12.8 ตร.ม.", "disclaimer_th": DIS},
  {"kind": "before_after", "title_th": "ก่อน/หลัง เกาหลีคลีน", "big_stat": f"{before} → {after}", "sub_th": "Glow Score เพิ่ม 46 คะแนน ไม่เจาะผนัง", "disclaimer_th": DIS},
  {"kind": "budget_receipt", "title_th": "ใบเสร็จแต่งห้อง", "big_stat": "฿3,000", "sub_th": "6 ชิ้น · ทำเสร็จ ~2 ชม.", "disclaimer_th": DIS},
  {"kind": "poll", "title_th": "เพื่อนเลือกลุคให้", "big_stat": "67%", "sub_th": "4 จาก 6 โหวตเกาหลีคลีน", "disclaimer_th": DIS},
  {"kind": "glow_score", "title_th": "ห้องฉันได้กี่คะแนน", "big_stat": f"{before}/100", "sub_th": "แสงน้อย ของรก สีไม่เข้ากัน", "disclaimer_th": DIS}],
}
here = os.path.dirname(os.path.abspath(__file__))
json.dump(schema, open(os.path.join(here, "..", "schemas.json"), "w"), ensure_ascii=False, indent=1)
json.dump(ex, open(os.path.join(here, "..", "examples.json"), "w"), ensure_ascii=False, indent=1)
n = 0
for k, items in ex.items():
    sub = {"$schema": S, "$defs": defs, "$ref": f"#/$defs/{k}"}
    for it in items: jsonschema.validate(it, sub); n += 1
print(f"{len(defs)} defs, {n} examples valid")
print(json.dumps(ex["WeekendPlan"], ensure_ascii=False))
