"""Generate ../schemas.json + ../examples.json and validate every example."""
import json, os, jsonschema
from brickbuddy import *
from fixtures import *

S = "https://json-schema.org/draft/2020-12/schema"
s = {"type": "string"}; b = {"type": "boolean"}; ns = {"type": ["string", "null"]}
u = {"type": "number", "minimum": 0, "maximum": 1}; num = {"type": "number"}
i0 = {"type": "integer", "minimum": 0}; i1 = {"type": "integer", "minimum": 1}
pct = {"type": "integer", "minimum": 0, "maximum": 100}
hexc = {"type": "string", "pattern": "^#[0-9A-F]{6}$"}
date = {"type": "string", "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}$"}
cell = {"type": "string", "pattern": "^[A-F][1-4]$"}
arr = lambda x, **k: dict({"type": "array", "items": x}, **k)
R = lambda n: {"$ref": "#/$defs/" + n}


def obj(props, req=None, extra=False):
    return {"type": "object", "required": req if req is not None else list(props), "properties": props, "additionalProperties": extra}


part = {"enum": list(PARTS)}; color = {"enum": list(COLORS)}; build = {"enum": list(BUILDS)}
countmap = {"type": "object", "propertyNames": {"enum": list(PARTS)}, "additionalProperties": i1}
defs = {
    "Person": obj({"id": s, "name_th": s, "name_en": s, "age": {"type": "integer", "minimum": 1, "maximum": 110}, "city_th": s, "role_th": s}),
    "PilePhoto": obj({"id": s, "light": u, "blur": u, "spread": u, "overlap": u}),
    "ScanQuality": obj({"score": pct, "ok": b, "tips_th": arr(s)}),
    "PileScan": obj({"photo_id": s, "quality": R("ScanQuality")}),
    "PieceDetection": obj({"part": part, "color": color, "count": i1, "confidence": u, "positions": arr(arr(u, minItems=2, maxItems=2))}, ["part", "color", "count"]),
    "AiPileScan": obj({"photo_id": s, "pieces": arr(R("PieceDetection")), "hazards": arr({"enum": ["battery", "magnet", "coin", "face", "sharp"]}),
                       "connected_clumps": i0, "confidence": u, "notes_th": s}, ["photo_id", "pieces", "hazards", "confidence"]),
    "Inventory": obj({"total": i0, "studs": i0, "by_part": countmap, "by_color": {"type": "object", "propertyNames": {"enum": list(COLORS)}, "additionalProperties": i1},
                      "top_colors": arr(color, maxItems=3), "kinds": i0}),
    "BuildIdea": obj({"id": build, "name_th": s, "category": {"enum": sorted({x["cat"] for x in BUILDS.values()})}, "minutes": i1,
                      "level": {"enum": [1, 2, 3]}, "age_min": i1, "need": countmap}),
    "Substitution": obj({"need": part, "use": part, "per": i1, "count": i1}),
    "BuildMatch": obj({"build": build, "name_th": s, "category": s, "minutes": i1, "level": {"enum": [1, 2, 3]}, "match_pct": pct, "can_build": b,
                       "missing": countmap, "substitutions": arr(R("Substitution")), "pieces": i1}),
    "ColorAssignment": obj({"build": build, "roles": {"type": "object", "propertyNames": {"enum": ["main", "accent", "base", "detail"]}, "additionalProperties": color},
                            "hex": {"type": "object", "additionalProperties": hexc}}),
    "BuildStep": obj({"n": i1, "part": part, "name_th": s, "color": {"enum": list(COLORS) + [None]}, "count": i1, "tip_th": s}),
    "BuildSteps": obj({"build": build, "steps": arr(R("BuildStep"), minItems=1), "step_count": i1, "minutes": i1}),
    "FindIt": obj({"part": part, "color": color, "found": b, "cells": arr(cell), "hint_th": s}),
    "SortPlan": obj({"by": {"enum": ["color", "size"]}, "bins": {"type": "integer", "minimum": 2, "maximum": 12},
                     "boxes": arr(obj({"box": i1, "groups": arr(s), "count": i0})), "balance_gap": i0}),
    "Stability": obj({"layers": i1, "base_studs": i1, "stagger_pct": pct, "score": pct, "level": {"enum": ["solid", "wobbly", "will_fall"]}, "tip_th": s}),
    "DailyChallenge": obj({"date": date, "theme": {"enum": [c[0] for c in CHALLENGES]}, "title_th": s, "max_pieces": i1, "minutes": i1, "badge": s}),
    "CreationScore": obj({"points": pct, "stars": {"type": "integer", "minimum": 1, "maximum": 5}, "badges": arr({"enum": ["rainbow", "symmetry_star", "sky_high", "challenge_done"]}),
                          "over_limit": b, "cheer_th": s}),
    "DiaryEntry": obj({"date": date, "kind": {"enum": ["build", "challenge", "sort"]}, "build": build, "pieces": i0, "stars": {"type": "integer", "minimum": 1, "maximum": 5},
                       "badges": arr(s)}, ["date", "kind"]),
    "DiarySummary": obj({"today": date, "builds": i0, "challenges": i0, "pieces_used": i0, "streak": i0, "best_stars": {"type": "integer", "minimum": 0, "maximum": 5}, "badges": arr(s)}),
    "ReelShot": obj({"kind": {"enum": [k for k, _ in REEL_SHOTS]}, "start": {"type": "number", "minimum": 0}, "end": num, "caption_th": s}),
    "ReelPlan": obj({"build": s, "seconds": {"type": "integer", "minimum": 15, "maximum": 30}, "ratio": {"const": "9:16"}, "bpm": i1,
                     "shots": arr(R("ReelShot"), minItems=3), "watermark": s}),
    "ShareCard": obj({"name_th": s, "stars": {"type": "integer", "minimum": 1, "maximum": 5}, "layout": {"enum": ["before_after", "steps_grid", "badge"]},
                      "size": {"const": "1080x1350"}, "watermark": s, "badge_th": s}),
    "Quota": obj({"plan": {"enum": ["free", "plus"]}, "scans_per_day": i1, "used": i0, "left": i0, "blocked": b}),
    "AgeCheck": obj({"allowed": b, "level": {"enum": ["ok", "warn", "stop"]}, "flags": arr({"enum": [k for k in GUARD if k]}), "messages_th": arr(s, minItems=1)}),
    "SafetyGuard": obj({"flag": {"type": ["string", "null"]}, "level": {"enum": ["ok", "warn", "stop"]}, "message_th": s, "block": b}),
}
schema = {"$schema": S, "$id": "https://github.com/arm-haha/ai-wanla-app/2026-12-21-brickbuddy/schemas.json", "title": "BrickBuddy", "$defs": defs}
ref = lambda n: {"$schema": S, "$defs": defs, "$ref": "#/$defs/" + n}

ex = []
add = lambda d, v, note="": ex.append({"def": d, "note": note, "value": v})
for p in PEOPLE: add("Person", p, p["name_en"])
for ph in PHOTOS: add("PilePhoto", ph, ph["id"]); add("PileScan", pile_scan(ph), ph["id"])
for a in ((0.95, 0.0, 1.0, 0.0), (0.5, 0.4, 0.4, 0.5), (0.7, 0.1, 0.9, 0.2)): add("ScanQuality", scan_quality(*a), str(a))
for p in PILE: add("PieceDetection", p, p["part"] + "/" + p["color"])
add("AiPileScan", {"photo_id": "p01", "pieces": PILE, "hazards": [], "connected_clumps": 1, "confidence": 0.88, "notes_th": "กองเกลี่ยดี มีชิ้นต่อติดกัน 1 กอง"}, "phum")
add("AiPileScan", {"photo_id": "p03", "pieces": PILE[:3], "hazards": ["coin", "magnet"], "connected_clumps": 6, "confidence": 0.42}, "messy + magnet")
add("Inventory", INV, "phum")
add("Inventory", inventory(PILE[:4]), "small pile")
add("Inventory", inventory([]), "empty")
for bid, bd in BUILDS.items():
    add("BuildIdea", {"id": bid, "name_th": bd["th"], "category": bd["cat"], "minutes": bd["min"], "level": bd["level"], "age_min": bd["age"], "need": bd["need"]}, bid)
for bid in BUILDS: add("BuildMatch", match_build(bid, INV), bid)
add("BuildMatch", match_build("castle_tower", inventory(PILE[:4])), "castle small pile")
for m in IDEAS:
    for sb in m["substitutions"]: add("Substitution", sb, m["build"])
for bid in ("dino", "xmas_tree", "ny_2027"):
    for sb in match_build(bid, INV)["substitutions"]: add("Substitution", sb, bid)
for bid in ("duck", "snowman", "race_car", "house", "xmas_tree", "robot"): add("ColorAssignment", assign_colors(bid, PILE), bid)
for bid in ("duck", "snowman", "race_car", "rocket"): add("BuildSteps", build_steps(bid, assign_colors(bid, PILE)), bid)
for st in STEPS_DUCK["steps"]: add("BuildStep", st, "duck")
for pa, co in (("brick_2x4", "red"), ("slope_2x2", "red"), ("wheel", "black"), ("eye_1x1", "white"), ("brick_2x4", "pink"), ("window", "trans_clear")):
    add("FindIt", find_piece(PILE, pa, co), pa + "/" + co)
for a in ((4, "color"), (3, "color"), (3, "size"), (6, "color")): add("SortPlan", sort_plan(INV, *a), str(a))
for a in ((6, 8, 100), (12, 4, 50), (6, 4, 40), (20, 2, 0), (10, 16, 80)): add("Stability", stability(*a), str(a))
for d in ("2026-11-23", "2026-11-24", "2026-11-25", "2026-11-26", "2026-12-21", "2027-01-02"): add("DailyChallenge", daily_challenge(d), d)
for a in ((7, 3, 0.9, 5, True, 10), (40, 6, 0.5, 12, True, 30), (0, 0, 0, 0, False, None), (16, 5, 0.85, 10, True, 30), (12, 2, 0.3, 3, False, None)):
    add("CreationScore", creation_score(*a), str(a))
for e in DIARY: add("DiaryEntry", e, e["kind"])
for d in ("2026-12-20", "2026-12-21", "2026-12-23"): add("DiarySummary", diary_summary(DIARY, d), d)
for sec in (15, 20, 30): add("ReelPlan", reel_plan("เป็ดน้อย", sec), str(sec))
for sh in reel_plan("เป็ดน้อย", 24)["shots"]: add("ReelShot", sh, sh["kind"])
for lay in ("before_after", "steps_grid", "badge"): add("ShareCard", share_card("เป็ดน้อย", 4, lay), lay)
for a in ((0,), (2,), (3,), (12, "plus")): add("Quota", quota(*a), str(a))
for a, kw in ((7, {}), (7, {"parent_ok": True}), (2, {"parent_ok": True}), (36, {"found": ("magnet",)}), (29, {"found": ("coin", "face")}), (4, {"parent_ok": True})):
    add("AgeCheck", age_check(a, **kw), f"{a} {kw}")
for f in GUARD: add("SafetyGuard", safety_guard(f), str(f))

for x in ex: jsonschema.validate(x["value"], ref(x["def"]))
d = os.path.dirname(os.path.abspath(__file__)) + "/.."
json.dump(schema, open(d + "/schemas.json", "w"), ensure_ascii=False, indent=1)
json.dump({"examples": ex}, open(d + "/examples.json", "w"), ensure_ascii=False, indent=1)
print(len(defs), "defs,", len(ex), "examples, all valid")
