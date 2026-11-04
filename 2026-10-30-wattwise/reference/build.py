"""Generate ../schemas.json + ../examples.json and validate every example."""
import json, os, jsonschema
from wattwise import *
from fixtures import *
S = "https://json-schema.org/draft/2020-12/schema"
n0 = {"type": "number", "minimum": 0}; s = {"type": "string"}; tier = {"enum": ["green", "amber", "red"]}
def obj(req, props, **kw): return {"type": "object", "required": req, "properties": props, **kw}
defs = {
 "Home": obj(["name", "rate_thb_per_kwh"], {"name": s, "rate_thb_per_kwh": {"type": "number", "exclusiveMinimum": 0},
   "provider": {"enum": ["MEA", "PEA", "condo", "other"]}, "goal_thb": n0, "household_size": {"type": "integer", "minimum": 1}}),
 "Appliance": obj(["id", "name_th"], {"id": s, "name_th": {"type": "string", "minLength": 1}, "watt": n0,
   "hours_per_day": {"type": "number", "minimum": 0, "maximum": 24}, "kwh_per_day": n0,
   "category": {"enum": ["cooling", "kitchen", "bath", "work", "entertain", "laundry", "other"]}, "room": s},
   anyOf=[{"required": ["watt", "hours_per_day"]}, {"required": ["kwh_per_day"]}]),
 "LabelExtract": obj(["name_th", "watt", "confidence", "needs_confirm"], {"name_th": s, "watt": {"type": ["number", "null"]},
   "btu": {"type": ["number", "null"]}, "energy_label_stars": {"type": ["integer", "null"], "minimum": 1, "maximum": 5},
   "kwh_per_year": {"type": ["number", "null"]}, "confidence": {"type": "number", "minimum": 0, "maximum": 1}, "needs_confirm": {"type": "boolean"}}),
 "ApplianceCost": obj(["appliance_id", "kwh_month", "cost_month_thb", "cost_year_thb", "tier"], {"appliance_id": s, "kwh_month": n0,
   "cost_month_thb": n0, "cost_year_thb": n0, "cost_per_hour_thb": {"type": ["number", "null"]}, "tier": tier}),
 "Bill": obj(["month", "units_kwh", "total_thb"], {"month": {"type": "string", "pattern": "^\\d{4}-\\d{2}$"},
   "units_kwh": {"type": "number", "exclusiveMinimum": 0}, "total_thb": {"type": "number", "exclusiveMinimum": 0}}),
 "BillExtract": obj(["units_kwh", "total_thb", "confidence", "needs_confirm"], {"units_kwh": {"type": ["number", "null"]},
   "total_thb": {"type": ["number", "null"]}, "period_th": {"type": ["string", "null"]}, "meter_prev": {"type": ["number", "null"]},
   "meter_now": {"type": ["number", "null"]}, "confidence": {"type": "number", "minimum": 0, "maximum": 1}, "needs_confirm": {"type": "boolean"}}),
 "Breakdown": obj(["bill_units", "bill_thb", "effective_rate", "estimated_kwh", "unexplained_kwh", "unexplained_pct", "over_estimated", "slices"],
   {"bill_units": n0, "bill_thb": n0, "effective_rate": n0, "estimated_kwh": n0, "unexplained_kwh": n0, "unexplained_pct": n0,
    "over_estimated": {"type": "boolean"}, "top_appliance_id": {"type": ["string", "null"]},
    "slices": {"type": "array", "items": obj(["appliance_id", "kwh", "pct", "thb"], {"appliance_id": s, "kwh": n0, "pct": n0, "thb": n0})}}),
 "AcSim": obj(["from_c", "to_c", "pct_per_deg", "base_cost_thb", "new_cost_thb", "save_month_thb", "save_year_thb", "assumption_th"],
   {"from_c": {"type": "integer", "minimum": 16, "maximum": 30}, "to_c": {"type": "integer", "minimum": 16, "maximum": 30},
    "pct_per_deg": {"type": "number", "minimum": 0, "maximum": 0.3}, "base_cost_thb": n0, "new_cost_thb": n0,
    "save_month_thb": {"type": "number"}, "save_year_thb": {"type": "number"}, "assumption_th": s}),
 "StandbyItem": obj(["id", "name_th", "standby_watt"], {"id": s, "name_th": s, "standby_watt": n0}),
 "StandbyLeak": obj(["total_standby_watt", "kwh_month", "cost_month_thb", "cost_year_thb"], {"total_standby_watt": n0, "kwh_month": n0,
   "cost_month_thb": n0, "cost_year_thb": n0, "worst_id": {"type": ["string", "null"]}}),
 "MeterReading": obj(["date", "meter_kwh"], {"date": {"type": "string", "format": "date"}, "meter_kwh": n0, "photo": {"type": "boolean"}}),
 "GoalTrack": obj(["used_kwh", "days", "per_day_kwh", "projected_kwh", "projected_thb", "goal_thb", "budget_per_day_kwh", "on_track", "gap_thb"],
   {"used_kwh": n0, "days": {"type": "integer", "minimum": 1}, "per_day_kwh": n0, "projected_kwh": n0, "projected_thb": n0, "goal_thb": n0,
    "budget_per_day_kwh": n0, "on_track": {"type": "boolean"}, "gap_thb": {"type": "number"}}),
 "RoomShare": obj(["name", "kwh", "pct", "thb"], {"name": s, "kwh": n0, "pct": n0, "thb": n0}),
 "SwapPayback": obj(["save_month_thb", "payback_months"], {"save_month_thb": {"type": "number"}, "payback_months": {"type": ["number", "null"]}}),
 "Tip": obj(["id", "title_th", "save_month_thb", "effort"], {"id": s, "title_th": s, "save_month_thb": n0, "effort": {"enum": ["easy", "medium", "hard"]},
   "source": {"enum": ["ac_sim", "standby", "swap", "habit"]}}),
 "ShareCard": obj(["kind", "title_th", "big_stat", "sub_th"], {"kind": {"enum": ["bill_pie", "ac_save", "standby", "goal", "split"]},
   "title_th": s, "big_stat": s, "sub_th": s, "disclaimer_th": s}),
}
schema = {"$schema": S, "$id": "wattwise.schemas.json", "title": "WattWise schemas", "$defs": defs}
DIS = "ค่าประมาณจากวัตต์×ชั่วโมง×เรทที่ผู้ใช้ตั้งเอง ไม่ใช่บิลทางการ"
bd = bill_breakdown(BILL, APPS, RATE); ac = ac_temp_sim(1008, 25, 27); sb = standby_leak(STANDBY, RATE)
gt = goal_track(READINGS, 1500, RATE, "2026-10-15"); split = room_split(1848, ROOMS)
ex = {
 "Home": [{"name": "คอนโดแนน", "rate_thb_per_kwh": RATE, "provider": "MEA", "goal_thb": 1500, "household_size": 2}],
 "Appliance": APPS,
 "LabelExtract": [{"name_th": "แอร์ 12,000 BTU", "watt": 1000, "btu": 12000, "energy_label_stars": 5, "kwh_per_year": None, "confidence": 0.88, "needs_confirm": False},
                  {"name_th": "ตู้เย็น 2 ประตู", "watt": None, "btu": None, "energy_label_stars": 5, "kwh_per_year": 438, "confidence": 0.81, "needs_confirm": False},
                  {"name_th": "ไม่แน่ใจ", "watt": None, "btu": None, "energy_label_stars": None, "kwh_per_year": None, "confidence": 0.22, "needs_confirm": True}],
 "ApplianceCost": [appliance_cost(a, RATE) for a in APPS],
 "Bill": [BILL, {"month": "2026-09", "units_kwh": 512, "total_thb": 2150.4}],
 "BillExtract": [{"units_kwh": 440, "total_thb": 1848.0, "period_th": "ต.ค. 2569", "meter_prev": 9790, "meter_now": 10230, "confidence": 0.9, "needs_confirm": False},
                 {"units_kwh": None, "total_thb": 1848.0, "period_th": None, "meter_prev": None, "meter_now": None, "confidence": 0.45, "needs_confirm": True}],
 "Breakdown": [bd],
 "AcSim": [ac, ac_temp_sim(1008, 24, 26)],
 "StandbyItem": STANDBY, "StandbyLeak": [sb, standby_leak([], RATE)],
 "MeterReading": READINGS,
 "GoalTrack": [gt, goal_track(READINGS, 1800, RATE, "2026-10-15")],
 "RoomShare": split,
 "SwapPayback": [swap_payback(1000, 700, 8, 15900, RATE), swap_payback(60, 60, 5, 200, RATE)],
 "Tip": [{"id": "t1", "title_th": "แอร์ 25 → 27°C + พัดลมช่วย", "save_month_thb": ac["save_month_thb"], "effort": "easy", "source": "ac_sim"},
         {"id": "t2", "title_th": "ถอดปลั๊ก/ปิดสวิตช์ปลั๊กพ่วงก่อนนอน", "save_month_thb": sb["cost_month_thb"], "effort": "easy", "source": "standby"},
         {"id": "t3", "title_th": "อาบน้ำอุ่นสั้นลง 15 → 10 นาที", "save_month_thb": r2(110.25 / 3), "effort": "medium", "source": "habit"}],
 "ShareCard": [
  {"kind": "bill_pie", "title_th": "ค่าไฟ ฿1,848 ไปไหน?", "big_stat": "แอร์ 55%", "sub_th": "฿1,008 จากแอร์ตัวเดียว", "disclaimer_th": DIS},
  {"kind": "ac_save", "title_th": "แอร์ 25 → 27°C", "big_stat": "−฿192/เดือน", "sub_th": "≈ ฿2,298/ปี", "disclaimer_th": DIS},
  {"kind": "standby", "title_th": "ไฟรั่วตอนปิดเครื่อง", "big_stat": "฿726/ปี", "sub_th": "เราเตอร์กินสุด 8W", "disclaimer_th": DIS},
  {"kind": "goal", "title_th": "เป้า ฿1,500", "big_stat": "เกิน ฿199", "sub_th": "ต้องลดเหลือ 11.5 หน่วย/วัน", "disclaimer_th": DIS},
  {"kind": "split", "title_th": "หารค่าไฟตามจริง", "big_stat": "แนน ฿1,092 · ฟ้า ฿756", "sub_th": "แทนหารครึ่ง ฿924", "disclaimer_th": DIS}],
}
here = os.path.dirname(os.path.abspath(__file__)); n = 0
for k, items in ex.items():
    for it in items:
        jsonschema.validate(it, {"$schema": S, "$defs": defs, "$ref": f"#/$defs/{k}"}); n += 1
json.dump(schema, open(os.path.join(here, "..", "schemas.json"), "w"), ensure_ascii=False, indent=1)
json.dump(ex, open(os.path.join(here, "..", "examples.json"), "w"), ensure_ascii=False, indent=1)
print(f"{len(defs)} defs, {n} examples valid")
