"""Build ../examples.json and ../schemas.json from the reference engine, then validate against the schema."""
import json, pathlib, jsonschema
from datetime import date
import leaf as L, fixtures as X
from schema import ROOT

OUT = pathlib.Path(__file__).resolve().parent.parent
COLORS = {"cream": "#F7F5EE", "forest": "#14532D", "leaf": "#22C55E", "lime": "#A3E635", "sun": "#FBBF24", "clay": "#C2410C", "water": "#0EA5E9", "ink": "#1C1917"}
on = date.fromisoformat(X.TODAY)
P = {p["id"]: p for p in X.PLANTS}
water = {pid: L.water_status(p, on) for pid, p in P.items()}
checkups = {pid: {"plant_id": pid, "on": X.TODAY, "symptoms": c["symptoms"], "ctx": c["ctx"], "source": "demo"} for pid, c in X.CHECKUPS.items()}
dx = {pid: L.diagnose(P[pid], c["symptoms"], c["ctx"], on) for pid, c in X.CHECKUPS.items()}
plan = L.rescue_plan(dx["p1"], X.TODAY); plan2 = L.rescue_plan(dx["p2"], X.TODAY)
prog = L.plan_progress(plan, X.PLAN_DONE_DAYS)
a = X.P1_AFTER
dx_after = L.diagnose(dict(P["p1"], light=a["ctx"]["light"]), a["symptoms"], a["ctx"], date.fromisoformat(a["on"]))
glow = L.glow_up(dx["p1"], dx_after, a["new_leaves"])
light = [dict(L.light_reading(L.lux_from_luma(s["mean_luma"])), spot_th=s["spot_th"], mean_luma=s["mean_luma"]) for s in X.LUMA_SAMPLES]
pets = [L.pet_check(p["species"]) for p in X.PLANTS]
match = L.room_match(X.ROOM_QUIZ)
log = X.LOG + [{"on": X.TODAY, "kind": "checkup", "plant_id": pid, "top_cause": d["top_cause"], "delta": 0, "score": d["health_score"]} for pid, d in dx.items()]
wrapped = L.plant_wrapped(log, "2026-10")
streak = L.care_streak(X.CARE_DAYS, X.TODAY)
checkup_count = sum(1 for e in log if e["kind"] == "checkup")
on_time = sum(1 for e in log if e.get("on_time"))
level = L.jungle_level(len(X.PLANTS), on_time, checkup_count)

expect_locked = {
    "today": X.TODAY, "season": L.season_of(on),
    "health_scores": {k: v["health_score"] for k, v in dx.items()}, "grades": {k: v["grade"] for k, v in dx.items()},
    "p1_causes": [[c["cause_id"], c["points"], c["confidence_pct"]] for c in dx["p1"]["causes"]],
    "p2_top": [dx["p2"]["causes"][0]["cause_id"], dx["p2"]["causes"][0]["confidence_pct"]],
    "water": {k: [v["interval_days"], v["status"], v["due_on"]] for k, v in water.items()},
    "plan_title": plan["title_th"], "plan_progress": prog, "recheck_on": plan["recheck_on"],
    "glow": [glow["before_score"], glow["after_score"], glow["delta"], glow["days"], glow["headline_th"]],
    "light": [[l["lux_est"], l["band"]] for l in light],
    "room_match": [[m["species"], m["fit"]] for m in match],
    "pet_toxic": {p["species"]: p["pet_toxic"] for p in pets},
    "wrapped": {k: wrapped[k] for k in ("waterings", "on_time_pct", "checkups", "top_cause")},
    "care_streak": streak, "jungle": [level["xp"], level["level"], level["title_th"]],
}
species = [{"id": k, "name_th": v[0], "name_en": v[1], "base_water_days": v[2], "light_need": v[3], "pet_toxic": v[4], "humidity_lover": v[5], "emoji": v[6], "verified": False} for k, v in L.SPECIES.items()]
symptoms = [{"id": k, "label_th": v[0], "severity": v[1]} for k, v in L.SYMPTOMS.items()]
causes = [{"id": k, "label_th": v[0], "emoji": v[1], "weights": v[2], "explain_th": v[3], "plan_th": L.PLANS[k]} for k, v in L.CAUSES.items()]
ui = {
    "home_title": "ต้นไม้ของฉัน", "snap_cta": "📸 ส่องใบ ตรวจสุขภาพ", "demo_cta": "ลองป่าคอนโดของบีม (ตัวอย่าง)", "scanning": "หมอใบไม้กำลังตรวจ…",
    "chips_title": "เห็นอาการไหนบ้าง? (แตะเลือก)", "soil_q": "จิ้มนิ้วลงดิน 2 ข้อ รู้สึกยังไง?", "soil": {"wet": "แฉะ", "moist": "ชื้น ๆ", "dry": "แห้ง"},
    "score_title": "คะแนนสุขภาพ", "causes_title": "น่าจะเป็นเพราะ…", "plan_cta": "เริ่มแผนชุบชีวิต 7 วัน", "water_title": "ตารางรดน้ำ",
    "light_title": "วัดแสงมุมนี้", "pet_title": "ปลอดภัยกับน้องแมว/หมาไหม", "match_title": "ห้องฉันควรปลูกอะไร", "glow_title": "Glow-up ต้นไม้",
    "wrapped_title": "เดือนนี้ป่าฉันเป็นยังไง", "remind_push": "{name} หิวน้ำแล้ว 💧", "grades": {g[1]: g[2] for g in L.GRADES},
    "disclaimer": "ผลนี้คาดเดาจากอาการ ไม่ใช่การตรวจในแล็บ · ข้อมูลพืชมีพิษต่อสัตว์ต้องตรวจกับแหล่งทางการก่อนเชื่อ",
}
reel = [
    {"t": "0-3s", "shot": "ซูมใบมอนสเตอร่าเหลือง ห้อย มือจับใบร่วง", "vo_th": "ต้นไม้ซื้อมาตายทุกต้น… ต้นนี้ก็กำลังจะไป", "overlay_th": "ต้นที่ 4 แล้ว 😭"},
    {"t": "3-8s", "shot": "จอคอม: วาง Prompt A → โค้ดวิ่ง → แอปเขียว ๆ ขึ้น (ตัดเร็ว x8)", "vo_th": "เลยให้ AI สร้างหมอต้นไม้ให้ซะเลย", "overlay_th": "สร้างแอปใน 1 ชม."},
    {"t": "8-14s", "shot": "ถ่ายใบ → เส้นสแกนวิ่ง → กรอบรอบใบเหลือง → วงแหวนคะแนน 0→55 🤒 → ชิป 'รดน้ำมากไป 50%'", "vo_th": "ถ่ายใบเดียว รู้เลย รดน้ำเยอะไป!", "overlay_th": "สุขภาพ 55/100 🤒"},
    {"t": "14-19s", "shot": "แผนชุบชีวิต 7 วัน เลื่อนลง + ตารางรดน้ำ 'ทุก 12 วัน ไม่ใช่ทุก 7'", "vo_th": "ให้แผน 7 วัน และบอกว่าควรรดทุกกี่วัน", "overlay_th": "ฉันรดถี่ไปเกือบเท่าตัว 💧"},
    {"t": "19-24s", "shot": "สลับเร็ว: Light Meter มุมทีวี 640 → ข้างหน้าต่าง 2,560 · ป้าย ⚠️ แมว · ห้องฉันควรปลูกอะไร → เศรษฐีเรือนใน 100", "vo_th": "วัดแสงได้ เช็กพิษกับแมวได้ แนะนำต้นที่เหมาะกับห้องได้", "overlay_th": "7 ฟีเจอร์ในแอปเดียว"},
    {"t": "24-30s", "shot": "Glow-up card สไลด์ before/after 55 → 94 ใบใหม่ 2 ใบ", "vo_th": "14 วันผ่านไป รอดแล้ว! คอมเมนต์ 'ต้นไม้' เดี๋ยวส่งแอปให้", "overlay_th": "คอมเมนต์ 'ต้นไม้' รับแอปฟรี 🌿"},
]
examples = {
    "meta": {"app": "LeafDoc (หมอใบไม้)", "date": X.TODAY, "engine": L.VERSION, "fictional_note_th": "บุคคล ต้นไม้ ค่าแสง และประวัติทั้งหมดเป็นตัวอย่างสมมติ", "colors": COLORS},
    "species": species, "symptoms": symptoms, "causes": causes, "healthy_plan_th": L.HEALTHY_PLAN,
    "grades": [{"min": a, "grade": b, "label_th": c, "emoji": d, "color": e} for a, b, c, d, e in L.GRADES],
    "factors": {"light": L.LIGHT_FACTOR, "pot": L.POT_FACTOR, "season": L.SEASON_FACTOR, "season_months": {"hot": [3, 4, 5], "rainy": [6, 7, 8, 9, 10], "cool": [11, 12, 1, 2]}},
    "demo": {"persona": X.PERSONA, "plants": X.PLANTS, "checkup_inputs": list(checkups.values())},
    "water_status": water, "diagnoses": dx, "rescue_plans": [plan, plan2], "plan_done_days": X.PLAN_DONE_DAYS, "plan_progress": prog,
    "recheck": {"input": {"plant_id": "p1", "on": a["on"], "symptoms": a["symptoms"], "ctx": a["ctx"], "source": "demo"}, "diagnosis": dx_after, "new_leaves": a["new_leaves"]},
    "glow_up": glow, "light_readings": light, "pet_checks": pets, "room_quiz": X.ROOM_QUIZ, "room_match": match,
    "log": log, "wrapped": wrapped, "care_days": X.CARE_DAYS, "care_streak": streak, "jungle_level": level,
    "local_store": {"version": 1, "settings": {"reminder_time": "08:00", "has_pets": True, "ac_room": True, "ai_vision": False},
                    "plants": X.PLANTS, "diagnoses": list(dx.values()), "plans": [plan], "log": log, "care_days": X.CARE_DAYS},
    "ai_examples": {
        "vision_request": {"image_b64_jpeg": "<base64 jpeg ตัดทิ้งในตัวอย่าง>", "known_species": None},
        "vision_response": {"species_guess": "monstera", "species_confidence": 0.86, "symptoms": ["yellow_lower", "drooping", "brown_tips"],
                            "leaf_boxes": [{"x": 0.12, "y": 0.58, "w": 0.3, "h": 0.25, "symptom": "yellow_lower"}, {"x": 0.55, "y": 0.2, "w": 0.18, "h": 0.15, "symptom": "brown_tips"}],
                            "note_th": "ใบล่างเหลือง 2 ใบ ปลายใบบนมีรอยไหม้เล็กน้อย"},
        "care_chat_response": {"answer_th": "มอนมอนยังไม่ต้องรดนะ ดินยังแฉะอยู่ รออีกสัก 3–4 วันแล้วจิ้มนิ้วเช็กอีกที", "never_change_score": True},
    },
    "ui_copy_th": ui, "reel_script": reel, "expect_locked": expect_locked,
}
(OUT / "examples.json").write_text(json.dumps(examples, ensure_ascii=False, indent=2))
(OUT / "schemas.json").write_text(json.dumps(ROOT, ensure_ascii=False, indent=2))

D = ROOT["$defs"]; n = 0; errs = 0
def check(defname, inst):
    global n, errs
    v = jsonschema.Draft202012Validator({"$defs": D, "$ref": f"#/$defs/{defname}"})
    e = list(v.iter_errors(inst)); n += 1; errs += len(e)
    for x in e: print("ERR", defname, x.message[:160])
for s in species: check("Species", s)
for s in symptoms: check("Symptom", s)
for c in causes: check("Cause", c)
for p in X.PLANTS: check("Plant", p)
for c in checkups.values(): check("CheckupInput", c)
check("CheckupInput", examples["recheck"]["input"])
for w in water.values(): check("WaterStatus", w)
for d in list(dx.values()) + [dx_after]: check("Diagnosis", d)
for p in (plan, plan2): check("RescuePlan", p)
check("PlanProgress", prog); check("GlowUpCard", glow)
for l in light: check("LightReading", {k: l[k] for k in ("lux_est", "band", "band_th", "fits", "note_th")})
for p in pets: check("PetCheck", p)
check("RoomQuiz", X.ROOM_QUIZ); check("RoomMatch", match)
for e in log: check("LogEntry", e)
check("Wrapped", wrapped); check("JungleLevel", level); check("LocalStore", examples["local_store"])
check("AiVisionResponse", examples["ai_examples"]["vision_response"]); check("AiCareChatResponse", examples["ai_examples"]["care_chat_response"])
print(f"validated {n} objects, {errs} errors · {len(D)} defs")
print(json.dumps(expect_locked, ensure_ascii=False))
