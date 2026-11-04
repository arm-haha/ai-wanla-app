"""Build ../examples.json and ../schemas.json from the engine, then validate every object."""
import json, pathlib, jsonschema
from datetime import date
import pawtalk as P, fixtures as X
from schema import ROOT
OUT = pathlib.Path(__file__).resolve().parent.parent
COLORS = {"cream": "#FFF8F0", "cocoa": "#3B2A20", "orange": "#F97316", "peach": "#FDBA74", "mint": "#34D399", "sky": "#60A5FA", "berry": "#EC4899", "alert": "#DC2626"}
on = date.fromisoformat(X.TODAY); pets = {p["id"]: p for p in X.PETS}
snap_in = {pid: dict(pet_id=pid, at=s["at"], cues=s["cues"], source="demo") for pid, s in X.SNAPS.items()}
mood = {pid: P.read_mood(pets[pid]["species"], s["cues"], s["at"], pets[pid]["meal_times"]) for pid, s in X.SNAPS.items()}
cat_after = P.read_mood("cat", X.CAT_AFTER["cues"], X.CAT_AFTER["at"], pets["cat1"]["meal_times"])
bubbles = {pid: P.thought_bubble(pets[pid], mood[pid], pets[pid]["persona"], X.OWNER, X.TODAY) for pid in pets}
persona_flip = {per: P.thought_bubble(pets["cat1"], mood["cat1"], per, X.OWNER, X.TODAY) for per in P.PERSONAS}
duet = P.duet(pets["cat1"], mood["cat1"], pets["dog1"], mood["dog1"], "boss", "sweet", X.OWNER, X.TODAY)
board = P.care_board(X.CARE, on)
health = {pid: P.health_check(pets[pid], s) for pid, s in X.HEALTH.items()}
health_red = P.health_check(pets["cat1"], X.HEALTH_RED["cat1"])
food = {pid: P.food_plan(pets[pid], f["kcal_per_100g"], f["meals"]) for pid, f in X.FOOD.items()}
age = {pid: P.human_age(p) for pid, p in pets.items()}
log = X.LOG + [{"on": X.TODAY, "kind": "snap", "pet_id": pid, "mood": mood[pid]["top_mood"]} for pid in pets]
prog = P.progress(log, on); wr = P.wrapped(log, "cat1", "2026-10")
next_meal = P.next_meal("07:05", pets["cat1"]["meal_times"])
idcard = {"pet_id": "cat1", "title_th": "บัตรประจำตัวเจ้านาย: ส้มฉุน 👑",
          "lines_th": ["แมวส้มไทย · ชาย · 3 ปี (≈ 28 ปีคน)", "บุคลิก: เจ้านาย", "อารมณ์ประจำเดือน: 🍗 หิว (6/13 ครั้ง)", "วันที่หงุดหงิดที่สุด: วันพุธ"],
          "human_age": age["cat1"]["human_years"], "persona_th": "เจ้านาย", "top_mood_emoji": "🍗", "size_px": [1080, 1350], "watermark": "PawTalk · AI วันละแอป"}
meme = {"pet_id": "cat1", "bubble": bubbles["cat1"], "size_px": [1080, 1920], "layout": "bubble_top", "watermark": "PawTalk · AI วันละแอป"}
store = {"version": 1, "owner_name": X.OWNER, "pets": X.PETS, "care": X.CARE, "log": log, "settings": {"notify": True, "lang": "th"}}
ai_cue_resp = {"species_seen": "cat", "cues": [{"cue": "staring_at_bowl", "confidence": 0.86}, {"cue": "tail_flick", "confidence": 0.58}, {"cue": "ears_forward", "confidence": 0.31}],
               "is_pet_photo": True, "note_th": "เห็นแมวนั่งหน้าชามว่าง หางกำลังขยับ"}
ui_copy = {"home_title": "วันนี้น้องคิดอะไรอยู่?", "snap_cta": "📸 ถ่ายน้อง แปลใจเลย", "cue_confirm": "AI เห็นแบบนี้ ถูกไหม? แตะเพื่อแก้",
           "cue_add": "+ เพิ่มท่าทางที่เห็น", "persona_pick": "เลือกเสียงน้อง: 👑 เจ้านาย · 🎭 ดราม่าควีน · 🥺 ขี้อ้อน",
           "share_cta": "แชร์มีม", "duet_cta": "ให้น้องคุยกัน 💬", "care_title": "งานทาสวันนี้", "overdue": "เลยกำหนด {n} วัน",
           "due_soon": "อีก {n} วัน", "health_title": "เช็กอาการเบื้องต้น", "health_disclaimer": "ไม่ใช่การวินิจฉัย ฉุกเฉินให้ไปโรงพยาบาลสัตว์ทันที",
           "food_title": "ควรกินวันละเท่าไหร่", "age_title": "ถ้าเป็นคนจะอายุ", "wrapped_title": "{pet} ประจำเดือน", "streak": "แปลใจติดกัน {n} วัน 🔥",
           "empty_pet": "เพิ่มน้องตัวแรกก่อนนะ", "not_pet_photo": "ไม่เจอน้องในรูป ลองถ่ายใหม่ให้เห็นทั้งตัว"}
reel = [{"t": "0–3s", "shot": "ส้มฉุนจ้องชามว่าง ร้องลั่น", "overlay_th": "แมวกูด่าอะไรกูอยู่ทุกเช้า??"},
        {"t": "3–8s", "shot": "speed-ramp แคปจอ gen แอปด้วย AI", "overlay_th": "เลยให้ AI สร้างแอปแปลภาษาแมวให้"},
        {"t": "8–13s", "shot": "ถ่ายรูป → ชิปท่าทาง → Mood Meter หิว 62%", "overlay_th": "หิว 62% · หงุดหงิด 23%"},
        {"t": "13–17s", "shot": "บับเบิลเด้ง", "overlay_th": bubbles["cat1"]["text_th"]},
        {"t": "17–21s", "shot": "สลับ persona 3 แบบ", "overlay_th": "เปลี่ยนนิสัยได้ด้วย 😂"},
        {"t": "21–25s", "shot": "Duet แมวคุยกับหมา + Care board แดง", "overlay_th": "แถมเตือนถ่ายพยาธิเลย 7 วัน 😱"},
        {"t": "25–30s", "shot": "Meme card + บัตรประจำตัว", "overlay_th": "คอมเมนต์ 'แมว' เดี๋ยวส่งลิงก์ให้ฟรี"}]
expect = {"cat1_moods": [[m["mood"], m["points"], m["pct"]] for m in mood["cat1"]["moods"]], "cat1_vibe": mood["cat1"]["vibe_score"],
          "cat_after_vibe": cat_after["vibe_score"], "dog1_top": [mood["dog1"]["top_mood"], mood["dog1"]["moods"][0]["pct"]], "dog1_vibe": mood["dog1"]["vibe_score"],
          "cat1_bubble": bubbles["cat1"]["text_th"], "care_order": [r["task_id"] for r in board],
          "health": {k: v["level"] for k, v in health.items()}, "health_red": health_red["level"],
          "food": {k: [v["kcal_per_day"], v["grams_per_day"], v["grams_per_meal"]] for k, v in food.items()},
          "human_age": {k: v["human_years"] for k, v in age.items()}, "progress": prog, "wrapped_top": [wr["top_mood"], wr["mood_counts"][wr["top_mood"]], wr["snaps"]]}
EX = {"_note": "ข้อมูลทั้งหมดเป็นตัวอย่างสมมติ (บ้านแพรว) สร้างโดย reference/build.py", "today": X.TODAY, "colors": COLORS,
      "cue_catalog": {sp: [{"id": c, "label_th": P.CUE_TH[c], "weights": w} for c, w in t.items()] for sp, t in P.CUES.items()},
      "symptom_catalog": [{"id": k, "level": v[0], "species": v[1], "label_th": v[2]} for k, v in P.SYMPTOMS.items()],
      "bubble_templates": P.BUBBLES, "pets": X.PETS, "snap_inputs": snap_in, "mood_results": mood, "cat_after_breakfast": cat_after,
      "thought_bubbles": bubbles, "persona_flip_cat1": persona_flip, "duet": duet, "care_items": X.CARE, "care_board": board, "next_meal_cat1": next_meal,
      "health": health, "health_red_example": health_red, "food": food, "human_age": age, "pet_id_card": idcard, "meme_card": meme,
      "progress": prog, "wrapped_cat1": wr, "local_store": store, "ai_cue_response_example": ai_cue_resp, "ui_copy_th": ui_copy, "reel_script": reel, "expect_locked": expect}
CHECK = [("Pet", p) for p in X.PETS] + [("SnapInput", v) for v in snap_in.values()] + [("MoodResult", v) for v in [*mood.values(), cat_after]] \
    + [("ThoughtBubble", v) for v in [*bubbles.values(), *persona_flip.values()]] + [("Duet", duet)] + [("CareItem", c) for c in X.CARE] \
    + [("CareStatus", r) for r in board] + [("NextMeal", next_meal)] + [("HealthResult", v) for v in [*health.values(), health_red]] \
    + [("FoodPlan", v) for v in food.values()] + [("HumanAge", v) for v in age.values()] + [("Progress", prog), ("Wrapped", wr), ("PetIdCard", idcard),
       ("MemeCard", meme), ("LocalStore", store), ("AiCueResponse", ai_cue_resp)]
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
