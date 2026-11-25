"""Generate ../schemas.json + ../examples.json and validate every example."""
import json, os, jsonschema
from dreamboard import *
from fixtures import *

S = "https://json-schema.org/draft/2020-12/schema"
s = {"type": "string"}; b = {"type": "boolean"}; ns = {"type": ["string", "null"]}
u = {"type": "number", "minimum": 0, "maximum": 1}; num = {"type": "number"}; nn = {"type": "number", "minimum": 0}
i0 = {"type": "integer", "minimum": 0}; i1 = {"type": "integer", "minimum": 1}
pct = {"type": "integer", "minimum": 0, "maximum": 100}
date = {"type": "string", "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}$"}
month = {"type": "string", "pattern": "^[0-9]{4}-[0-9]{2}$"}
hexc = {"type": "string", "pattern": "^#[0-9A-F]{6}$"}
arr = lambda x, **k: dict({"type": "array", "items": x}, **k)
R = lambda n: {"$ref": "#/$defs/" + n}
cat = {"enum": CAT_KEYS}; unit = {"enum": list(UNITS)}; theme = {"enum": list(THEMES)}; device = {"enum": list(DEVICES)}
flags = {"enum": [k for k in GUARD if k]}
lvl = {"enum": ["ok", "warn", "stop"]}


def obj(props, req=None, extra=False):
    return {"type": "object", "required": req if req is not None else list(props), "properties": props, "additionalProperties": extra}


defs = {
    "User": obj({"id": s, "name_th": s, "name_en": s, "age": {"type": "integer", "minimum": 8, "maximum": 120}, "city_th": s, "monthly_income": nn}),
    "Category": obj({"key": cat, "name_th": s, "name_en": s, "color": hexc}),
    "Unit": obj({"key": unit, "name_th": s, "step": {"type": "number", "exclusiveMinimum": 0}, "max_per_month": {"type": ["number", "null"]}}),
    "BoardTheme": obj({"key": theme, "name_th": s, "palette": arr(hexc, minItems=6, maxItems=6)}),
    "Device": obj({"key": device, "w": i1, "h": i1, "clock_zone": u, "bottom_zone": u}),
    "GoalText": obj({"text_th": {"type": "string", "minLength": 1, "maxLength": 200}, "today": date}),
    "AiGoalParse": obj({"title_th": s, "category": cat, "unit": {"enum": list(UNITS) + [""]}, "start_value": num, "target_value": num,
                        "deadline": {"type": ["string", "null"], "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}$"}, "flags": arr(flags),
                        "needs_clarification_th": ns, "confidence": u}),
    "Goal": obj({"id": s, "title_th": s, "category": cat, "category_th": s, "unit": {"enum": list(UNITS) + [""]}, "start_value": num,
                 "target_value": num, "start": date, "deadline": date}),
    "SmartCheck": obj({"score": {"enum": [0, 20, 40, 60, 80, 100]}, "specific": b, "measurable": b, "achievable": b, "relevant": b, "timed": b,
                       "per_month": {"type": ["number", "null"]}, "flag": {"enum": [None, "extreme_diet"]}, "tips_th": arr(s)}),
    "Milestone": obj({"month": month, "label_th": s, "target": num, "delta": num, "pct": pct}),
    "Roadmap": obj({"goal_id": s, "months": {"type": "integer", "minimum": 1, "maximum": 13}, "unit": unit, "milestones": arr(R("Milestone"), minItems=1)}),
    "WeeklyHabit": obj({"goal_id": s, "weeks": i1, "per_week": {"type": "number", "exclusiveMinimum": 0}, "unit": unit, "text_th": s}),
    "Tile": obj({"goal_id": s, "x": i0, "y": i0, "w": i1, "h": i1, "color": hexc, "category": cat}),
    "BoardLayout": obj({"device": device, "theme": theme, "w": i1, "h": i1, "safe_top": i0, "safe_bottom": i1, "tiles": arr(R("Tile"), minItems=1, maxItems=6)}),
    "WordOfYear": obj({"category": cat, "word_th": s, "word_en": s, "line_th": s}),
    "Countdown": obj({"date": date, "days_to_new_year": i1, "days_passed": i0, "year_pct": pct}),
    "LogEntry": obj({"date": date, "amount": {"type": "number", "exclusiveMinimum": 0}}),
    "Streak": obj({"weeks": i0, "this_week_done": b, "badge_th": {"enum": list(BADGES.values()) + [None]}, "next_badge_at": {"type": ["integer", "null"]}}),
    "Progress": obj({"goal_id": s, "done": nn, "expected": num, "pct": pct, "status": {"enum": ["done", "ahead", "on_track", "behind"]},
                     "glow": {"type": "integer", "minimum": 0, "maximum": 5}, "message_th": s}),
    "BoardGlow": obj({"overall_pct": pct, "level": {"type": "integer", "minimum": 0, "maximum": 5}, "lit_tiles": i0,
                      "tiles": arr(obj({"goal_id": s, "glow": {"type": "integer", "minimum": 0, "maximum": 5}}))}),
    "Review": obj({"period": {"enum": ["mid_year", "year"]}, "title_th": s, "goals": i1, "goals_done": i0, "overall_pct": pct, "best_goal_id": s,
                   "best_title_th": s, "note_th": s}),
    "BuddyCard": obj({"owner_th": s, "buddy_th": s, "pact_th": s, "items": arr(obj({"title_th": s, "amount_hidden": b})), "private": b}),
    "ShareCard": obj({"kind": {"enum": ["board", "progress", "review"]}, "size": {"const": "1080x1350"}, "amounts_hidden_default": {"const": True},
                      "faces_blurred": {"const": True}, "glow_level": {"type": ["integer", "null"]}, "word_th": ns, "watermark": s}),
    "ReelShot": obj({"kind": {"enum": [k for k, _, _ in REEL_SHOTS]}, "start": nn, "end": num, "caption_th": s}),
    "ReelPlan": obj({"seconds": {"type": "integer", "minimum": 15, "maximum": 30}, "ratio": {"const": "9:16"}, "bpm": i1, "shots": arr(R("ReelShot"), minItems=3), "watermark": s}),
    "Quota": obj({"plan": {"enum": ["free", "plus"]}, "boards_per_day": i1, "used": i0, "left": i0, "blocked": b}),
    "PrivacyCheck": obj({"allowed": b, "level": lvl, "flags": arr(flags), "messages_th": arr(s, minItems=1), "share_allowed": b}),
    "SafetyGuard": obj({"flag": {"type": ["string", "null"]}, "level": lvl, "message_th": s, "block": b}),
}
schema = {"$schema": S, "$id": "https://github.com/arm-haha/ai-wanla-app/2026-12-24-dreamboard/schemas.json", "title": "DreamBoard", "$defs": defs}
ref = lambda n: {"$schema": S, "$defs": defs, "$ref": "#/$defs/" + n}

ex = []
add = lambda dd, v, note="": ex.append({"def": dd, "note": note, "value": v})
for x in (USER, BUDDY, TEEN): add("User", x, x["name_en"])
for c in CATEGORIES: add("Category", {"key": c[0], "name_th": c[1], "name_en": c[2], "color": c[3]}, c[0])
for k, v in UNITS.items(): add("Unit", dict(key=k, **v), k)
for k, (n, pal) in THEMES.items(): add("BoardTheme", {"key": k, "name_th": n, "palette": pal}, k)
for k, (w, h, t, bt) in DEVICES.items(): add("Device", {"key": k, "w": w, "h": h, "clock_zone": t, "bottom_zone": bt}, k)
TEXTS = [("ปีหน้าอยากเก็บเงินไปญี่ปุ่นสัก 6 หมื่น", {"title_th": "เก็บเงินเที่ยวญี่ปุ่น 60,000 บาท", "category": "money", "unit": "THB", "start_value": 0, "target_value": 60000, "deadline": "2027-12-31", "flags": [], "needs_clarification_th": None, "confidence": 0.92}),
         ("อยากผอม จาก 68 เหลือ 62 ก่อนสงกรานต์... ไม่สิ ก่อนกลางปี", {"title_th": "ลดน้ำหนักจาก 68 เหลือ 62 กก.", "category": "health", "unit": "kg_loss", "start_value": 0, "target_value": 6, "deadline": "2027-06-30", "flags": [], "needs_clarification_th": None, "confidence": 0.88}),
         ("อ่านหนังสือเดือนละ 2 เล่ม", {"title_th": "อ่านหนังสือให้ได้ 24 เล่ม", "category": "learn", "unit": "book", "start_value": 0, "target_value": 24, "deadline": "2027-12-31", "flags": [], "needs_clarification_th": None, "confidence": 0.9}),
         ("ลด 10 โลใน 1 เดือนก่อนงานแต่ง", {"title_th": "ลด 10 กก. ใน 1 เดือนก่อนงานแต่ง", "category": "health", "unit": "kg_loss", "start_value": 0, "target_value": 10, "deadline": "2027-01-31", "flags": ["extreme_diet"], "needs_clarification_th": None, "confidence": 0.86}),
         ("อยากรวย", {"title_th": "อยากรวย", "category": "money", "unit": "", "start_value": 0, "target_value": 0, "deadline": None, "flags": [], "needs_clarification_th": "อยากเก็บเงินเท่าไร ภายในเมื่อไร?", "confidence": 0.4}),
         ("ขอให้ถูกหวยรางวัลที่ 1", {"title_th": "ถูกหวยรางวัลที่ 1", "category": "money", "unit": "", "start_value": 0, "target_value": 0, "deadline": None, "flags": ["gambling"], "needs_clarification_th": "ลองเปลี่ยนเป็นเป้าเก็บเงินเดือนละเท่าไรดี?", "confidence": 0.8}),
         ("ให้แฟนเก่ากลับมา", {"title_th": "ให้แฟนเก่ากลับมา", "category": "mind", "unit": "", "start_value": 0, "target_value": 0, "deadline": None, "flags": ["other_person"], "needs_clarification_th": "ลองเขียนเป็นสิ่งที่เราทำเพื่อใจตัวเอง เช่น ออกกำลังกายสัปดาห์ละ 3 ครั้ง", "confidence": 0.7}),
         ("หัดว่ายน้ำให้เป็น เรียนสัก 12 ครั้ง", {"title_th": "เรียนว่ายน้ำ 12 ครั้ง", "category": "hobby", "unit": "lesson", "start_value": 0, "target_value": 12, "deadline": "2027-06-30", "flags": [], "needs_clarification_th": None, "confidence": 0.85})]
for t, a in TEXTS:
    add("GoalText", {"text_th": t, "today": "2026-12-24"}, t[:20]); add("AiGoalParse", a, t[:20])
EXTRA = [{"id": "g6", "title_th": "เรียนว่ายน้ำ 12 ครั้ง", "category": "hobby", "category_th": "งานอดิเรก", "unit": "lesson", "start_value": 0, "target_value": 12, "start": Y0, "deadline": "2027-06-30"},
         {"id": "g7", "title_th": "ฝึกภาษาอังกฤษ 100 ชั่วโมง", "category": "learn", "category_th": "เรียนรู้", "unit": "hours", "start_value": 0, "target_value": 100, "start": Y0, "deadline": Y1},
         {"id": "g8", "title_th": "โทรหาแม่ 52 ครั้ง", "category": "family", "category_th": "ครอบครัว", "unit": "times", "start_value": 0, "target_value": 52, "start": Y0, "deadline": Y1}]
ALL = GOALS + EXTRA + [G_CRASH, G_VAGUE, G_HUGE]
for g in ALL:
    add("Goal", g, g["id"]); add("SmartCheck", smart_check(g, USER["monthly_income"]), g["id"])
add("Goal", safe_replan(G_CRASH), "b1 re-planned"); add("SmartCheck", smart_check(safe_replan(G_CRASH)), "b1 re-planned")
for g in GOALS + EXTRA:
    rm = roadmap(g); add("Roadmap", rm, g["id"]); add("WeeklyHabit", weekly_habit(g), g["id"])
for m in roadmap(G_MONEY)["milestones"]: add("Milestone", m, "g1 " + m["month"])
for th, dev, n in (("sunrise", "iphone", 5), ("pastel", "android", 1), ("midnight", "desktop", 5), ("thai_gold", "iphone", 3), ("nature", "android", 6), ("minimal", "desktop", 2)):
    L = layout((GOALS + EXTRA)[:n], th, dev); add("BoardLayout", L, "%s/%s/%d" % (th, dev, n))
for t in layout(GOALS)["tiles"]: add("Tile", t, t["goal_id"])
for gs in (GOALS, [G_MONEY, G_BOOK], [G_TRIP, EXTRA[2]], [EXTRA[0]]): add("WordOfYear", word_of_year(gs), ",".join(g["id"] for g in gs))
for dt in ("2026-12-24", "2027-01-01", "2027-06-30", "2027-12-31"): add("Countdown", countdown(dt), dt)
for l in LOGS["g1"] + LOGS["g2"][:3]: add("LogEntry", l, l["date"])
for ck, dt in ((CHECKINS, "2027-02-07"), (CHECKINS, "2027-02-10"), (CHECKINS, "2027-02-16"), (CHECKINS[:4], "2027-01-24"), ([], "2027-01-24")): add("Streak", streak(ck, dt), dt)
for p in [progress(g, LOGS[g["id"]], MID) for g in GOALS]: add("Progress", p, p["goal_id"] + " mid-year")
add("Progress", progress(G_MONEY, LOGS["g1"], "2027-03-15"), "g1 2027-03-15")
add("Progress", progress(G_TRIP, [{"date": "2027-03-01", "amount": 5}], "2027-03-02"), "g5 done")
PM = [progress(g, LOGS[g["id"]], MID) for g in GOALS]
add("BoardGlow", board_glow(PM), "mid-year"); add("BoardGlow", board_glow([progress(g, [], "2027-01-05") for g in GOALS]), "week 1")
add("Review", review(GOALS, PM, "mid_year"), "mid_year"); add("Review", review(GOALS, [progress(g, LOGS[g["id"]] + [{"date": "2027-12-20", "amount": delta(g)}], Y1) for g in GOALS]), "year all done")
add("BuddyCard", buddy_card("คุณมิ้นท์", "คุณโบ๊ท", GOALS), "private"); add("BuddyCard", buddy_card("คุณมิ้นท์", "คุณโบ๊ท", GOALS[2:], False), "public")
for k, gl, w in (("board", 0, "แข็งแรง"), ("progress", 2, None), ("review", 3, "แข็งแรง")): add("ShareCard", share_card(k, gl, w), k)
for sec in (15, 20, 24, 30): add("ReelPlan", reel_plan(sec), str(sec))
for sh in reel_plan(24)["shots"]: add("ReelShot", sh, sh["kind"])
for a in ((0,), (2,), (3,), (5, "plus")): add("Quota", quota(*a), str(a))
for a in (((), 28), (("gambling",), 28), ((), 12), ((), 12, True), (("self_harm",), 30), (("extreme_diet", "medical"), 35), (("photo_of_others",), 28)):
    add("PrivacyCheck", privacy_check(*a), str(a))
for f in GUARD: add("SafetyGuard", safety_guard(f), str(f))

for x in ex: jsonschema.validate(x["value"], ref(x["def"]))
dd = os.path.dirname(os.path.abspath(__file__)) + "/.."
json.dump(schema, open(dd + "/schemas.json", "w"), ensure_ascii=False, indent=1)
json.dump({"examples": ex}, open(dd + "/examples.json", "w"), ensure_ascii=False, indent=1)
print(len(defs), "defs,", len(ex), "examples, all valid")
