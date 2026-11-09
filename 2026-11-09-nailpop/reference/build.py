"""Generate ../schemas.json + ../examples.json and validate every example."""
import json, os, jsonschema
from nailpop import *
from fixtures import *

S = "https://json-schema.org/draft/2020-12/schema"
s = {"type": "string"}
b = {"type": "boolean"}
n0 = {"type": "number", "minimum": 0}
u = {"type": "number", "minimum": 0, "maximum": 1}
i0 = {"type": "integer", "minimum": 0}
i1 = {"type": "integer", "minimum": 1}
pct = {"type": "integer", "minimum": 0, "maximum": 100}
hexc = {"type": "string", "pattern": "^#[0-9A-F]{6}$"}
date = {"type": "string", "format": "date", "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}$"}

def obj(req, props, **kw):
    return {"type": "object", "required": req, "properties": props, "additionalProperties": False, **kw}

def arr(i, **kw):
    return {"type": "array", "items": i, **kw}

shape = {"enum": list(SHAPES)}
length = {"enum": LENGTH_ORDER}
tone = {"enum": list(UNDERTONES)}
tech = {"enum": list(TECHNIQUES)}
occ = {"enum": list(OCCASIONS)}
finger = {"enum": FINGERS}
did = {"type": "string", "pattern": "^d[0-9]{2}$"}
shade = obj(["name_th", "hex"], {"name_th": s, "hex": hexc})

defs = {
 "Person": obj(["id", "name_th", "age", "occasion", "budget_thb", "region", "quiz", "skin_rgb"], {
    "id": {"type": "string", "pattern": "^u[0-9]{2}$"}, "name_th": s, "name_en": s, "age": i1, "city_th": s, "goal_th": s,
    "occasion": occ, "budget_thb": i0, "region": {"enum": list(REGION_MULT)},
    "quiz": {"$ref": "#/$defs/UndertoneQuiz"}, "skin_rgb": arr({"type": "integer", "minimum": 0, "maximum": 255}, minItems=3, maxItems=3)}),
 "UndertoneQuiz": obj(["vein", "jewelry", "sun"], {
    "vein": {"enum": ["green", "blue", "mixed"]}, "jewelry": {"enum": ["gold", "silver", "both"]}, "sun": {"enum": ["tan", "burn", "both"]}}),
 "NailMeasure": obj(["finger", "width_mm", "bed_len_mm", "free_edge_mm", "taper", "corner_round"], {
    "finger": finger, "width_mm": {"type": "number", "exclusiveMinimum": 0}, "bed_len_mm": n0, "free_edge_mm": n0, "taper": u, "corner_round": u}),
 "HandPhoto": obj(["id", "hand", "px_w", "px_h", "lighting", "blur", "tilt", "nails"], {
    "id": {"type": "string", "pattern": "^h[0-9]{2}$"}, "hand": {"enum": ["left", "right"]}, "px_w": i1, "px_h": i1,
    "lighting": u, "blur": u, "tilt": u, "nails": arr({"$ref": "#/$defs/NailMeasure"}, minItems=1, maxItems=5)}),
 "NailDetect": obj(["finger", "shape", "shape_th", "length", "length_th", "width_mm", "total_len_mm"], {
    "finger": finger, "shape": shape, "shape_th": s, "length": length, "length_th": s, "width_mm": n0, "total_len_mm": n0}),
 "ScanQuality": obj(["score", "ok", "tips_th"], {"score": pct, "ok": b, "tips_th": arr(s)}),
 "HandScan": obj(["photo_id", "hand", "nail_count", "nails", "shape", "shape_th", "length", "length_th", "quality"], {
    "photo_id": s, "hand": {"enum": ["left", "right"]}, "nail_count": {"type": "integer", "minimum": 1, "maximum": 5},
    "nails": arr({"$ref": "#/$defs/NailDetect"}), "shape": shape, "shape_th": s, "length": length, "length_th": s,
    "quality": {"$ref": "#/$defs/ScanQuality"}}),
 "UndertoneResult": obj(["undertone", "undertone_th", "depth", "points", "rgb_hint", "confidence"], {
    "undertone": tone, "undertone_th": s, "depth": {"enum": ["light", "medium", "tan", "deep"]},
    "points": obj(["warm", "cool"], {"warm": i0, "cool": i0}), "rgb_hint": tone, "confidence": u}),
 "ShadeRec": obj(["undertone", "depth", "best", "avoid", "note_th"], {
    "undertone": tone, "depth": s, "best": arr(shade, minItems=1), "avoid": arr(shade), "note_th": s}),
 "Design": obj(["id", "name_th", "name_en", "technique", "finish", "art", "colors", "tones", "occasions", "len_min", "shapes"], {
    "id": did, "name_th": s, "name_en": s, "technique": tech, "finish": {"enum": FINISHES},
    "art": {"type": "integer", "minimum": 0, "maximum": 3}, "colors": arr(hexc, minItems=1), "tones": arr(tone, minItems=1),
    "occasions": arr(occ), "len_min": length, "shapes": arr(shape, minItems=1)}),
 "PriceEstimate": obj(["technique", "art_level", "length", "region", "removal", "min_thb", "max_thb", "disclaimer_th"], {
    "technique": tech, "art_level": {"type": "integer", "minimum": 0, "maximum": 3}, "length": length,
    "region": {"enum": list(REGION_MULT)}, "removal": b, "min_thb": i0, "max_thb": i0, "disclaimer_th": s}),
 "TryOnTile": obj(["rank", "slot", "design_id", "name_th", "colors", "finish", "technique", "fit_score", "price_min_thb", "price_max_thb", "why_th", "render"], {
    "rank": {"type": "integer", "minimum": 1, "maximum": 9}, "slot": {"type": "string", "pattern": "^r[1-3]c[1-3]$"},
    "design_id": did, "name_th": s, "colors": arr(hexc), "finish": {"enum": FINISHES}, "technique": tech, "fit_score": pct,
    "price_min_thb": i0, "price_max_thb": i0, "why_th": s, "render": {"const": "overlay_on_real_nails"}}),
 "TryOnGrid": obj(["photo_id", "undertone", "occasion", "budget_thb", "count", "tiles", "watermark"], {
    "photo_id": s, "undertone": tone, "occasion": {"enum": list(OCCASIONS) + [None]},
    "budget_thb": {"type": ["integer", "null"], "minimum": 0}, "count": {"type": "integer", "minimum": 1, "maximum": 9},
    "tiles": arr({"$ref": "#/$defs/TryOnTile"}, minItems=1, maxItems=9), "watermark": s}),
 "SalonCard": obj(["title_th", "name_th", "design_id", "design_name_th", "shape", "shape_th", "length", "length_th", "technique", "technique_th",
                   "colors", "price_min_thb", "price_max_thb", "note_th", "share_text_th", "line_share_url", "disclaimer_th"], {
    "title_th": s, "name_th": s, "design_id": did, "design_name_th": s, "shape": shape, "shape_th": s, "length": length, "length_th": s,
    "technique": tech, "technique_th": s, "colors": arr(hexc), "price_min_thb": i0, "price_max_thb": i0, "note_th": s,
    "share_text_th": s, "line_share_url": {"type": "string", "pattern": "^https://line\\.me/R/share\\?text="}, "disclaimer_th": s}),
 "VoteLink": obj(["grid_id", "options", "url", "expires_hours", "anonymous"], {
    "grid_id": s, "options": arr(did, minItems=2, maxItems=4), "url": {"type": "string", "pattern": "^https://"}, "expires_hours": i1, "anonymous": b}),
 "VoteResult": obj(["total", "invalid", "winner", "winner_pct", "results"], {
    "total": i0, "invalid": i0, "winner": {"type": ["string", "null"]}, "winner_pct": pct,
    "results": arr(obj(["design_id", "votes", "pct"], {"design_id": did, "votes": i1, "pct": pct}))}),
 "CareReminder": obj(["technique", "done_date", "check_date", "due_date", "remove_by", "message_th"], {
    "technique": tech, "done_date": date, "check_date": date, "due_date": date, "remove_by": date, "message_th": s}),
 "ReminderStatus": obj(["status", "days_since", "days_to_due"], {
    "status": {"enum": ["ok", "check", "due", "overdue"]}, "days_since": {"type": "integer"}, "days_to_due": {"type": "integer"}}),
 "DiaryEntry": obj(["id", "date", "design_id", "technique", "price_thb", "rating", "salon_th", "on_device", "reminder"], {
    "id": s, "date": date, "design_id": did, "technique": tech, "price_thb": i0, "rating": {"type": "integer", "minimum": 1, "maximum": 5},
    "salon_th": s, "on_device": b, "reminder": {"$ref": "#/$defs/CareReminder"}}),
 "DiaryStats": obj(["count", "total_thb", "avg_thb", "avg_rating", "favorite_design"], {
    "count": i0, "total_thb": i0, "avg_thb": i0, "avg_rating": {"type": "number", "minimum": 0, "maximum": 5},
    "favorite_design": {"type": ["string", "null"]}}),
 "OccasionPreset": obj(["key", "label_th", "tip_th", "palette", "max_length", "design_ids"], {
    "key": occ, "label_th": s, "tip_th": s, "palette": arr(hexc, minItems=1), "max_length": length, "design_ids": arr(did)}),
 "DiyGuide": obj(["design_id", "diy_ok", "steps", "total_min", "tools_th", "note_th"], {
    "design_id": did, "diy_ok": b, "total_min": i0, "tools_th": arr(s), "note_th": s,
    "steps": arr(obj(["n", "key", "text_th", "minutes"], {"n": i1, "key": {"enum": list(DIY_STEPS)}, "text_th": s, "minutes": i1}))}),
 "HealthGuard": obj(["level", "flags", "message_th"], {
    "level": {"enum": ["ok", "warn", "stop"]}, "flags": arr({"enum": ["lifting", "redness", "swelling", "pain", "discoloration", "fungus_suspect"]}), "message_th": s}),
 "ShareCard": obj(["title_th", "headline_th", "hook_th", "design_id", "fit_score", "layout", "sizes", "watermark", "cta_th"], {
    "title_th": s, "headline_th": s, "hook_th": s, "design_id": did, "fit_score": pct, "layout": {"enum": ["before_after_grid", "single"]},
    "sizes": arr({"enum": ["1080x1350", "1080x1920", "1080x1080"]}), "watermark": s, "cta_th": s}),
 "Quota": obj(["allowed", "left_after", "paywall"], {
    "allowed": i0, "left_after": {"type": ["integer", "null"], "minimum": 0}, "paywall": b}),
 "Pipeline": obj(["photo_id", "steps"], {"photo_id": s, "steps": arr(s, minItems=1)}),
}

schema = {"$schema": S, "$id": "https://example.com/nailpop.schema.json", "title": "NailPop", "$defs": defs}

def ref(n):
    return {"$ref": f"#/$defs/{n}", "$defs": defs}

ex = []
def add(n, v, note=""):
    ex.append({"def": n, "note": note, "value": v})

for p in PEOPLE:
    add("Person", p, p["name_th"])
    add("UndertoneResult", undertone(p["quiz"], p["skin_rgb"]), p["id"])
for ph in PHOTOS:
    add("HandPhoto", ph, ph["id"])
    sc = hand_scan(ph)
    add("HandScan", sc, ph["id"])
    add("Pipeline", {"photo_id": ph["id"], "steps": pipeline_steps(ph)}, ph["id"])
add("NailMeasure", MIND_PHOTO["nails"][0], "mind thumb")
add("NailDetect", detect_nail(MIND_PHOTO["nails"][0]), "mind thumb")
add("NailDetect", detect_nail(PHOTOS[2]["nails"][0]), "almond long")
add("ScanQuality", scan_quality(0.3, 0.6, 0.5, 3), "bad photo")
for t in UNDERTONES:
    add("ShadeRec", shade_recommend(t), t)
add("ShadeRec", shade_recommend("warm", "deep"), "joy deep")
for d in DESIGNS[:5] + [DESIGN_BY_ID["d13"]]:
    add("Design", d, d["name_en"])
add("PriceEstimate", price_estimate("gel", 1, "medium"), "mind d01")
add("PriceEstimate", price_estimate("gel", 0, "long", "province", True), "long+removal province")
add("PriceEstimate", price_estimate("extension", 3, "long", "tourist"), "chrome extension tourist")

mscan = hand_scan(MIND_PHOTO)
mtone = undertone(MIND["quiz"], MIND["skin_rgb"])["undertone"]
grid = try_on_grid(mscan, mtone, "wedding", MIND["budget_thb"])
add("TryOnGrid", grid, "mind wedding 9")
add("TryOnTile", grid["tiles"][0], "mind top pick")
fern = PEOPLE[1]
fscan = hand_scan(PHOTOS[1])
add("TryOnGrid", try_on_grid(fscan, "cool", "office", fern["budget_thb"], "province"), "fern office")
add("TryOnGrid", try_on_grid(hand_scan(PHOTOS[2]), "neutral", None, None, n=4), "por no occasion 4")
add("SalonCard", salon_card("มายด์", "d01", mscan, extra_note_th="ขอโทนไม่ฉูดฉาด จันทร์ต้องเข้าออฟฟิศ"), "mind")
add("SalonCard", salon_card("คุณจอย", "d09", hand_scan(PHOTOS[2]), "province", True), "joy krathong")
add("VoteLink", vote_link("g01", ["d01", "d02", "d05"]), "mind vote")
add("VoteResult", friend_vote(grid, MIND_VOTES), "mind 10 friends")
add("VoteResult", friend_vote(grid, []), "no votes yet")
entries = [diary_entry(*e) for e in DIARY]
for e in entries:
    add("DiaryEntry", e, e["id"])
add("DiaryStats", diary_stats(entries), "mind diary")
rem = care_reminder("2026-11-09", "gel")
add("CareReminder", rem, "mind gel")
add("CareReminder", care_reminder("2026-11-09", "regular"), "regular")
add("CareReminder", care_reminder("2026-11-09", "extension"), "extension")
add("ReminderStatus", reminder_status(rem, "2026-11-25"), "check")
add("ReminderStatus", reminder_status(rem, "2026-12-10"), "overdue")
for k in OCCASIONS:
    add("OccasionPreset", occasion_preset(k), k)
add("DiyGuide", diy_guide("d01"), "mind diy")
add("DiyGuide", diy_guide("d08"), "songkran art2")
add("DiyGuide", diy_guide("d13"), "blocked")
add("HealthGuard", health_guard({}), "ok")
add("HealthGuard", health_guard({"lifting": True}), "warn")
add("HealthGuard", health_guard({"redness": True, "lifting": True}), "stop")
add("ShareCard", share_card("มายด์", "d01", 100, 60), "mind share")
add("Quota", quota(1, 1), "free")
add("Quota", quota(3, 1), "exhausted")
add("Quota", quota(0, 5, pro=True), "pro")

for e in ex:
    jsonschema.validate(e["value"], ref(e["def"]))

d = os.path.dirname(os.path.abspath(__file__)) + "/.."
json.dump(schema, open(d + "/schemas.json", "w"), ensure_ascii=False, indent=1)
json.dump({"examples": ex}, open(d + "/examples.json", "w"), ensure_ascii=False, indent=1)
print(len(defs), "defs,", len(ex), "examples, all valid")
