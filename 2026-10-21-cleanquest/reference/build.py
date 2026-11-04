"""Build ../examples.json and ../schemas.json from the engine, then validate every object."""
import json, pathlib, jsonschema
from datetime import date
import cleanquest as C, fixtures as X
from schema import ROOT
OUT = pathlib.Path(__file__).resolve().parent.parent
COLORS = {"mist": "#F5F7FF", "ink": "#1E1B4B", "lilac": "#A78BFA", "sparkle": "#22D3EE", "lemon": "#FDE047", "mess": "#F43F5E", "clean": "#10B981"}
on = date.fromisoformat(X.TODAY)
scan_in = {"room_id": "room1", "at": "2026-10-21T20:30:00+07:00", "hotspots": X.BEFORE, "source": "demo"}
before, after = C.mess_score(X.BEFORE), C.mess_score(X.AFTER)
plans = {m: C.quest_plan(X.BEFORE, m) for m in C.MODES}
fire = plans["fire"]
timer = [C.timer_tick(fire, [], 0), C.timer_tick(fire, ["q1", "q2", "q3"], 600), C.timer_tick(fire, [q["id"] for q in fire["quests"]], 2280)]
glow = C.glow_up(before, after, fire["total_minutes"], len(fire["quests"]), X.NAME)
decl = [C.declutter(i) for i in X.ITEMS]
split = C.chore_split(fire["quests"], X.ROOMMATES)
today_session = {"on": X.TODAY, "before": before["clean_score"], "after": after["clean_score"], "minutes": fire["total_minutes"], "hotspots": [h["id"] for h in X.BEFORE]}
sessions = X.SESSIONS + [today_session]
log = X.LOG + [{"on": X.TODAY, "kind": "scan"}, {"on": X.TODAY, "kind": "session"}] + [{"on": X.TODAY, "kind": "quest", "xp": q["xp"]} for q in fire["quests"]] + \
      [{"on": X.TODAY, "kind": "declutter"} for _ in X.ITEMS]
prog_before = C.progress(X.LOG + [{"on": X.TODAY, "kind": "scan"}], on)
prog = C.progress(log, on)
reset = C.weekly_reset(sessions, on)
wr = C.wrapped(sessions, "2026-10")
store = {"version": 1, "name": X.NAME, "roommates": X.ROOMMATES, "sessions": sessions, "items": X.ITEMS, "log": log,
         "settings": {"reset_weekday": 6, "notify": True, "sound": True}}
ai_resp = {"is_room_photo": True, "hotspots": [
    {"id": "clothes_pile", "severity": 2, "confidence": 0.91, "box": [0.05, 0.30, 0.35, 0.40]},
    {"id": "trash_floor", "severity": 2, "confidence": 0.84, "box": [0.55, 0.70, 0.30, 0.25]},
    {"id": "dishes_cups", "severity": 1, "confidence": 0.77, "box": [0.62, 0.35, 0.15, 0.12]},
    {"id": "boxes_parcels", "severity": 1, "confidence": 0.66, "box": [0.40, 0.72, 0.15, 0.20]},
    {"id": "cables_mess", "severity": 1, "confidence": 0.42, "box": [0.70, 0.48, 0.12, 0.08]}],
    "note_th": "เห็นเสื้อผ้ากองบนเก้าอี้ ถุงขยะ 2 ใบข้างโต๊ะ แก้วชานมบนโต๊ะ"}
pep = {"coach": "อีก 1 เควส ห้องขึ้น 56 แล้ว ลุย!", "bestie": "แกกก เก็บขยะเสร็จแล้ว เก่งมากกก", "army": "พลทหาร! เสื้อผ้ากองนั้น 12 นาที เริ่ม!"}
ui = {"home_title": "ห้องรกแค่ไหน ให้ AI ตัดสิน", "scan_cta": "📸 สแกนห้อง", "confirm": "AI เจอจุดรกพวกนี้ ถูกไหม? แตะเพื่อแก้ระดับ",
      "add_hotspot": "+ เพิ่มจุดที่ AI ไม่เห็น", "score_title": "คะแนนห้อง", "mode_pick": "วันนี้ไหวแค่ไหน? 😴 5 นาที · 🙂 15 นาที · 🔥 เคลียร์หมด",
      "start": "เริ่มเควส ⏱️", "quest_done": "เสร็จ! +{xp} XP", "sprint_break": "พัก 1 นาที ดื่มน้ำก่อน 💧", "rescan": "ถ่ายหลังเก็บ เทียบ Before/After",
      "glow_share": "แชร์ Glow-up", "declutter_title": "เก็บ ขาย บริจาค หรือทิ้ง?", "copy_listing": "คัดลอกข้อความขาย", "split_title": "แบ่งงานกับรูมเมท",
      "split_share": "ส่งเข้า LINE รูมเมท", "streak": "สแกนติดกัน {n} วัน 🔥", "reset_title": "Weekly Reset อีก {n} วัน",
      "not_room": "ไม่เห็นห้องในรูป ลองถ่ายกว้างๆ ให้เห็นพื้นกับโต๊ะ", "privacy": "รูปอยู่ในเครื่องคุณ ส่งให้ AI เฉพาะตอนสแกน และไม่เก็บบนเซิร์ฟเวอร์"}
reel = [{"t": "0–3s", "shot": "แพนกล้องห้องรก เสื้อผ้ากอง ถุงขยะ", "overlay_th": "ห้องกูได้คะแนนเท่าไหร่วะ…"},
        {"t": "3–7s", "shot": "speed-ramp gen แอปด้วย AI", "overlay_th": "เลยให้ AI สร้างแอปตัดสินห้องรก"},
        {"t": "7–11s", "shot": "สแกน → pin จุดรกเด้ง → สกอร์ 12 สีแดงสั่น", "overlay_th": "12/100 ห้องวิกฤต 🚨"},
        {"t": "11–15s", "shot": "เลือก 🔥 → เควส 8 อัน 3 สปรินต์ 38 นาที", "overlay_th": "แปลงเป็นเกม 38 นาที"},
        {"t": "15–22s", "shot": "timelapse เก็บห้อง + ติ๊กเควส สกอร์วิ่ง 12→46→80", "overlay_th": "ทุกเควสสกอร์ขึ้นสด"},
        {"t": "22–26s", "shot": "Before/After slider 12 → 94 + การ์ด ห้องเกิดใหม่", "overlay_th": "12 → 94 ใน 38 นาที 🦋"},
        {"t": "26–30s", "shot": "แวบ Declutter หูฟังขายได้ ฿770 + แบ่งงานรูมเมท", "overlay_th": "คอมเมนต์ 'ห้อง' เดี๋ยวส่งลิงก์ให้ฟรี"}]
expect = {"before": [before["clean_score"], before["mess_points"], before["label_th"], before["est_minutes"]],
          "after": [after["clean_score"], after["label_th"]],
          "fire_order": [q["hotspot"] for q in fire["quests"]], "fire_sprints": [s["minutes"] for s in fire["sprints"]],
          "fire_scores": [q["score_after"] for q in fire["quests"]], "lazy": [[q["hotspot"] for q in plans["lazy"]["quests"]], plans["lazy"]["score_after"]],
          "normal": [plans["normal"]["total_minutes"], plans["normal"]["score_after"]], "timer_mid": timer[1]["live_score"],
          "glow": [glow["before"], glow["after"], glow["delta"], glow["title_th"]], "declutter": [d["decision"] for d in decl], "resale_i1": decl[0]["resale_thb"],
          "split": [[s["person"], s["minutes"]] for s in split], "progress": prog, "reset": reset, "wrapped": [wr["sessions"], wr["minutes"], wr["avg_delta"], wr["top_hotspot"]]}
EX = {"_note": "ข้อมูลทั้งหมดเป็นตัวอย่างสมมติ (ห้องหอฟ้า) สร้างโดย reference/build.py", "today": X.TODAY, "colors": COLORS,
      "hotspot_catalog": [{"id": k, "label_th": v[0], "zone": v[1], "weight": v[2], "base_min": v[3], "quest_th": v[4], "emoji": v[5]} for k, v in C.HOTSPOTS.items()],
      "severity_th": C.SEV_TH, "modes": C.MODE_TH, "score_labels": C.LABELS, "scan_input": scan_in, "mess_before": before, "mess_after": after,
      "quest_plans": plans, "timer_states": timer, "glow_up_card": glow, "declutter_items": X.ITEMS, "declutter_results": decl,
      "chore_split": split, "sessions": sessions, "progress_before_session": prog_before, "progress": prog, "weekly_reset": reset, "wrapped_oct": wr,
      "local_store": store, "ai_scan_response_example": ai_resp, "pep_talk_examples": pep, "ui_copy_th": ui, "reel_script": reel, "expect_locked": expect}
CHECK = [("ScanInput", scan_in), ("MessScore", before), ("MessScore", after)] + [("QuestPlan", p) for p in plans.values()] + [("TimerState", t) for t in timer] \
    + [("GlowUpCard", glow)] + [("DeclutterItem", i) for i in X.ITEMS] + [("DeclutterResult", d) for d in decl] + [("ChoreShare", s) for s in split] \
    + [("Session", s) for s in sessions] + [("Progress", prog_before), ("Progress", prog), ("WeeklyReset", reset), ("Wrapped", wr), ("LocalStore", store), ("AiScanResponse", ai_resp)] \
    + [("AiPepTalkResponse", {"text_th": t}) for t in pep.values()]
if __name__ == "__main__":
    errs = 0
    for name, o in CHECK:
        v = jsonschema.Draft202012Validator({**ROOT, "$ref": f"#/$defs/{name}"}, format_checker=jsonschema.FormatChecker())
        for e in v.iter_errors(o):
            errs += 1; print(name, e.message)
    (OUT / "schemas.json").write_text(json.dumps(ROOT, ensure_ascii=False, indent=2))
    (OUT / "examples.json").write_text(json.dumps(EX, ensure_ascii=False, indent=2))
    print(f"validated {len(CHECK)} objects, {errs} errors, {len(ROOT['$defs'])} defs")
    raise SystemExit(1 if errs else 0)
