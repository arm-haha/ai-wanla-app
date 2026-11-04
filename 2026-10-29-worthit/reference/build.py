"""Generate ../schemas.json + ../examples.json and validate every example."""
import json, os, jsonschema
from worthit import *
from fixtures import *
S = "https://json-schema.org/draft/2020-12/schema"
num0 = {"type": "number", "minimum": 0}
tier = {"enum": ["green", "amber", "red"]}
defs = {
 "Profile": {"type": "object", "required": ["name", "monthly_income"], "properties": {"name": {"type": "string"},
   "monthly_income": {"type": "number", "exclusiveMinimum": 0}, "work_days": {"type": "integer", "minimum": 1, "maximum": 31},
   "hours_per_day": {"type": "number", "exclusiveMinimum": 0, "maximum": 24}, "jar_goal_thb": num0, "jar_goal_name_th": {"type": "string"}}},
 "Item": {"type": "object", "required": ["id", "name_th", "price_thb", "source"], "properties": {"id": {"type": "string"},
   "name_th": {"type": "string", "minLength": 1}, "price_thb": {"type": "number", "exclusiveMinimum": 0},
   "category": {"enum": ["fashion", "sport", "food", "gadget", "beauty", "home", "other"]},
   "source": {"enum": ["photo", "screenshot", "link", "manual"]}, "ocr_confidence": {"type": "number", "minimum": 0, "maximum": 1}}},
 "VisionExtract": {"type": "object", "required": ["name_th", "price_thb", "confidence", "needs_confirm"], "properties": {
   "name_th": {"type": "string"}, "price_thb": {"type": ["number", "null"]}, "original_price_thb": {"type": ["number", "null"]},
   "shop_hint": {"type": ["string", "null"]}, "confidence": {"type": "number", "minimum": 0, "maximum": 1}, "needs_confirm": {"type": "boolean"}}},
 "WorkTime": {"type": "object", "required": ["price_thb", "hourly_wage", "hours", "work_days", "pct_of_month", "label_th"], "properties": {
   "price_thb": num0, "hourly_wage": num0, "hours": num0, "work_days": num0, "pct_of_month": num0, "label_th": {"type": "string"}}},
 "CostPerUse": {"type": "object", "required": ["total_uses", "per_use_thb", "tier"], "properties": {"total_uses": num0, "per_use_thb": num0, "tier": tier}},
 "Answers": {"type": "object", "required": [q[0] for q in QUESTIONS], "properties": {q[0]: {"type": "boolean"} for q in QUESTIONS}, "additionalProperties": False},
 "Verdict": {"type": "object", "required": ["score", "verdict", "verdict_th"], "properties": {"score": {"type": "integer", "minimum": 0, "maximum": 100},
   "verdict": {"enum": ["buy", "wait", "skip"]}, "verdict_th": {"type": "string"}}},
 "CoolOff": {"type": "object", "required": ["ends_at", "hours_left", "unlocked"], "properties": {"ends_at": {"type": "string", "format": "date-time"},
   "hours_left": num0, "unlocked": {"type": "boolean"}}},
 "SkipJar": {"type": "object", "required": ["saved_thb", "count", "goal_thb", "goal_pct", "reached"], "properties": {"saved_thb": num0,
   "count": {"type": "integer", "minimum": 0}, "goal_thb": num0, "goal_pct": {"type": "number", "minimum": 0, "maximum": 100}, "reached": {"type": "boolean"}}},
 "MonthReport": {"type": "object", "required": ["bought", "skipped", "spent_thb", "saved_thb", "hours_saved", "biggest_skip"], "properties": {
   "bought": {"type": "integer", "minimum": 0}, "skipped": {"type": "integer", "minimum": 0}, "spent_thb": num0, "saved_thb": num0, "hours_saved": num0,
   "biggest_skip": {"type": ["string", "null"]}}},
 "HabitCost": {"type": "object", "required": ["per_month_thb", "per_year_thb", "hours_per_month", "hours_per_year"], "properties": {k: num0 for k in ("per_month_thb", "per_year_thb", "hours_per_month", "hours_per_year")}},
 "DupeQuery": {"type": "object", "required": ["item_id", "search_terms_th", "note_th"], "properties": {"item_id": {"type": "string"},
   "search_terms_th": {"type": "array", "items": {"type": "string"}, "minItems": 1, "maxItems": 5}, "note_th": {"type": "string"}}},
 "ShareCard": {"type": "object", "required": ["kind", "title_th", "big_stat", "sub_th"], "properties": {
   "kind": {"enum": ["work_hours", "verdict", "skip_jar", "month_report", "cooloff_win"]}, "title_th": {"type": "string"},
   "big_stat": {"type": "string"}, "sub_th": {"type": "string"}, "disclaimer_th": {"type": "string"}}},
}
schema = {"$schema": S, "$id": "worthit.schemas.json", "title": "WorthIt schemas", "$defs": defs}
DIS = "ตัวอย่างสมมติ คำนวณจากรายได้ที่ผู้ใช้กรอกเอง ไม่ใช่คำแนะนำทางการเงิน"
items = [BAG, SNEAKER, LATTE, PHONE]
wt = {i["id"]: work_time(i["price_thb"], PROFILE) for i in items}
ex = {
 "Profile": [PROFILE, {"name": "พี่โอ๊ต", "monthly_income": 18000, "work_days": 26, "hours_per_day": 9}],
 "Item": items,
 "VisionExtract": [{"name_th": "กระเป๋าสะพายข้าง", "price_thb": 3990, "original_price_thb": 5990, "shop_hint": "แอปช้อปปิ้ง", "confidence": 0.93, "needs_confirm": False},
                   {"name_th": "ไม่แน่ใจ", "price_thb": None, "original_price_thb": None, "shop_hint": None, "confidence": 0.31, "needs_confirm": True}],
 "WorkTime": list(wt.values()),
 "CostPerUse": [cost_per_use(2890, 12, 12), cost_per_use(3990, 2, 12), cost_per_use(75, 1, 1)],
 "Answers": [BAG_ANS, SNEAKER_ANS, PHONE_ANS],
 "Verdict": [verdict(BAG_ANS, "red", wt["bag"]["pct_of_month"]), verdict(SNEAKER_ANS, "amber", wt["sneaker"]["pct_of_month"]),
             verdict(PHONE_ANS, "green", wt["phone"]["pct_of_month"])],
 "CoolOff": [cooloff_status("2026-10-29T08:00:00+07:00", 24, "2026-10-29T20:00:00+07:00"),
             cooloff_status("2026-10-29T08:00:00+07:00", 72, "2026-11-01T09:00:00+07:00")],
 "SkipJar": [skip_jar(SKIPS, PROFILE["jar_goal_thb"]), skip_jar([], 15000)],
 "MonthReport": [month_report(DECISIONS, PROFILE), month_report([], PROFILE)],
 "HabitCost": [habit_cost(75, 5, PROFILE), habit_cost(45, 7, PROFILE)],
 "DupeQuery": [{"item_id": "bag", "search_terms_th": ["กระเป๋าสะพายข้าง หนังPU สีครีม", "กระเป๋า crossbody มินิมอล"], "note_th": "แอปให้แค่คำค้น ไม่เดาราคา ผู้ใช้ไปเทียบเอง"}],
 "ShareCard": [
  {"kind": "work_hours", "title_th": "กระเป๋าใบนี้ = ทำงาน", "big_stat": "28 ชม.", "sub_th": "3.5 วันทำงาน · 16% ของเงินเดือน", "disclaimer_th": DIS},
  {"kind": "verdict", "title_th": "คุ้มไหม?", "big_stat": "5/100", "sub_th": "ข้ามไป เก็บเงินเข้าโหล", "disclaimer_th": DIS},
  {"kind": "skip_jar", "title_th": "เดือนนี้ไม่ซื้อไป 3 ชิ้น", "big_stat": "฿6,870", "sub_th": "ตั๋วญี่ปุ่น 45.8%", "disclaimer_th": DIS},
  {"kind": "month_report", "title_th": "เวลาชีวิตที่ได้คืน", "big_stat": "48 ชม.", "sub_th": "ซื้อ 1 · ข้าม 3", "disclaimer_th": DIS},
  {"kind": "cooloff_win", "title_th": "รอครบ 24 ชม. แล้ว", "big_stat": "ไม่อยากได้แล้ว", "sub_th": "+฿3,990 เข้าโหล", "disclaimer_th": DIS}],
}
for k, v in ex.items():
    for o in v: jsonschema.validate(o, {"$schema": S, "$defs": defs, "$ref": f"#/$defs/{k}"})
d = os.path.dirname(os.path.abspath(__file__)) + "/.."
json.dump(schema, open(d + "/schemas.json", "w"), ensure_ascii=False, indent=1)
json.dump(ex, open(d + "/examples.json", "w"), ensure_ascii=False, indent=1)
print(len(defs), "defs,", sum(map(len, ex.values())), "examples valid")
