"""Build ../examples.json and ../schemas.json from the engine, then validate every object."""
import json, pathlib, jsonschema
import posemate as T, fixtures as X
from schema import ROOT
OUT = pathlib.Path(__file__).resolve().parent.parent
COLORS = {"cream": "#FFF7EE", "ink": "#1F1A2E", "coral": "#FF6B5A", "sunset": "#FFB347", "lavender": "#B8A4FF", "mint": "#3DDC97", "ghost": "#7DF9FF", "warn": "#F43F5E"}
scene = T.scene_read(**X.SCENE); cards = T.pose_cards(scene)
stiff, live = T.pose_match("p_window_lean", X.STIFF_KP), T.pose_match("p_window_lean", X.LIVE_KP)
before = T.shot_score(**X.BEFORE); after = T.shot_score(**X.AFTER, pose=live["match"]); glow = T.glow_up(before, after)
coach = {s: T.angle_coach(p) for s, p in {"half": "p_window_lean", "full": "p_wall_lean", "close": "p_cup_sip"}.items()}
caps = T.caption_pack("cafe_window", "Baan Glass Café (ร้านสมมติ)"); grid = T.grid_plan(X.PHOTOS)
pops = [T.outfit_pop(*o) for o in X.OUTFIT_BG]
groups = {n: T.pose_cards(T.scene_read("street_wall" if n != 3 else "stairs", "shade", n)) for n in (2, 3, 4)}
store = {"version": 1, "name": X.NAME, "saved_poses": ["p_window_lean"], "streak_days": 3,
         "sessions": [{"id": "s1", "date": X.TODAY, "scene": scene, "pose_id": "p_window_lean", "before": before["total"], "after": after["total"]}],
         "settings": {"keep_photos": False, "grid_lines": True, "sound": True}}
ai_scene = {"spot": "cafe_window", "light": "window", "clutter": 1, "horizon_tilt_deg": 0.5, "bg_hex": "#EFE3D3", "note_th": "หน้าต่างบานใหญ่ด้านซ้าย แสงนุ่ม มีแก้วเปล่าบนโต๊ะ 1 ใบ"}
ai_caps = {"captions_th": ["แดดบ่ายสามโมงคือฟิลเตอร์ที่ดีที่สุด", "มาคาเฟ่เพื่อกาแฟ (และรูป 200 รูป)", "ช้าลงหน่อย โลกยังรอได้"]}
ui = {"home_title": "โพสท่าไม่เป็น? ให้ AI จัดท่าให้", "scan_cta": "📷 ถ่ายฉากก่อน 1 รูป", "ghost_hint": "ยืนให้ตรงเงา เงาเปลี่ยนเป็นสีเขียว = กดได้",
      "match_live": "ตรงท่า {match}%", "friend_mode": "โหมดเพื่อนถ่าย", "score_cta": "ให้คะแนนรูปนี้", "glow_card": "{before} → {after}",
      "caption_cta": "ขอแคปชันไทย", "grid_cta": "จัดฟีด 9 ช่อง", "outfit_cta": "เสื้อเด้งจากฉากไหม", "privacy": "รูปอยู่ในเครื่องเท่านั้น ส่งแค่รูปฉากไปอ่านแสง ไม่เก็บ",
      "disclaimer": "คะแนนวัดมุมกล้องและองค์ประกอบ ไม่ได้วัดหน้าตาหรือหุ่น ทุกคนถ่ายสวยได้"}
reel = [{"t": "0–3s", "shot": "รูปคาเฟ่ก่อน: ย้อนแสง เอียง ยืนแข็ง ป้ายคะแนน 30", "overlay_th": "ไปคาเฟ่ทีไร ได้รูปแบบนี้ทุกที…"},
        {"t": "3–7s", "shot": "speed-ramp gen แอปด้วย AI", "overlay_th": "เลยให้ AI สร้างแอปจัดท่าให้"},
        {"t": "7–12s", "shot": "ถ่ายฉาก → การ์ด 3 ท่าเด้ง → เลือก 'พิงขอบหน้าต่าง'", "overlay_th": "ถ่ายฉาก 1 รูป ได้ 3 ท่า"},
        {"t": "12–18s", "shot": "เงาสีฟ้าซ้อนบนกล้อง ตัวเลข 65% ไต่ขึ้น 94% เงาเป็นสีเขียว", "overlay_th": "ยืนตามเงา 65 → 94% ✅"},
        {"t": "18–23s", "shot": "จอเพื่อน: ตัวหนังสือใหญ่ 'ถือระดับอก ใช้ 1x ห่าง 1.5 ม.'", "overlay_th": "เพื่อนถ่ายไม่เป็นก็รอด"},
        {"t": "23–27s", "shot": "การ์ด Glow-up 30 → 94 + แวบแคปชันไทย + ฟีด 9 ช่อง", "overlay_th": "30 → 94 แค่ทำตามแอป"},
        {"t": "27–30s", "shot": "รูปสุดท้ายเต็มจอ", "overlay_th": "คอมเมนต์ 'โพส' เดี๋ยวส่งลิงก์ฟรี"}]
expect = {"cards": [c["id"] for c in cards], "match": [stiff["match"], live["match"]], "before": before["total"], "after": after["total"],
          "before_fixes": before["fixes_th"], "pop": [p["score"] for p in pops], "grid": [grid["order"], grid["balance"]]}
EX = {"_note": "ข้อมูลทั้งหมดเป็นตัวอย่างสมมติ (น้ำหวาน, ร้านสมมติ) สร้างโดย reference/build.py", "today": X.TODAY, "colors": COLORS,
      "pose_library": T.POSES, "angle_presets": T.ANGLE, "scene": scene, "pose_cards": cards, "pose_match_stiff": stiff, "pose_match_live": live,
      "shot_before_input": {**X.BEFORE, "subject_xy": list(X.BEFORE["subject_xy"])}, "shot_before": before, "shot_after": after, "glow_up": glow,
      "angle_coach": coach, "caption_pack": caps, "grid_photos": X.PHOTOS, "grid_plan": grid, "outfit_pop": pops, "group_cards": groups,
      "local_store": store, "ai_scene_response_example": ai_scene, "ai_caption_example": ai_caps, "ui_copy_th": ui, "reel_script": reel, "expect_locked": expect}
CHECK = [("Pose", p) for p in T.POSES] + [("Scene", scene), ("PoseCards", cards), ("PoseMatch", stiff), ("PoseMatch", live), ("ShotInput", EX["shot_before_input"]),
         ("ShotScore", before), ("ShotScore", after), ("GlowUp", glow), ("CaptionPack", caps), ("GridPlan", grid), ("LocalStore", store),
         ("AiSceneResponse", ai_scene), ("AiCaptionResponse", ai_caps)] + [("AngleCoach", c) for c in coach.values()] + [("OutfitPop", p) for p in pops] \
        + [("GridPhoto", p) for p in X.PHOTOS] + [("PoseCards", g) for g in groups.values()]
if __name__ == "__main__":
    errs = 0
    for name, o in CHECK:
        v = jsonschema.Draft202012Validator({**ROOT, "$ref": f"#/$defs/{name}"}, format_checker=jsonschema.FormatChecker())
        for e in v.iter_errors(o): errs += 1; print(name, e.message)
    (OUT / "schemas.json").write_text(json.dumps(ROOT, ensure_ascii=False, indent=2))
    (OUT / "examples.json").write_text(json.dumps(EX, ensure_ascii=False, indent=2))
    print(f"validated {len(CHECK)} objects, {errs} errors, {len(ROOT['$defs'])} defs")
    raise SystemExit(1 if errs else 0)
