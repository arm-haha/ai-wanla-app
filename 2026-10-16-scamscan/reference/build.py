"""Build ../examples.json and ../schemas.json from the reference engine, then validate against the schema."""
import json, pathlib, jsonschema
import scam as S, fixtures as X
from schema import ROOT

OUT = pathlib.Path(__file__).resolve().parent.parent
COLORS = {"night": "#0B1220", "panel": "#111A2E", "paper": "#F8FAFC", "siren": "#DC2626", "amber": "#F97316", "caution": "#FACC15", "safe": "#16A34A", "shield": "#38BDF8"}

scans = {m["id"]: S.scan(m["text"], m["sender"], m["channel"]) for m in X.INBOX}
xrays = [S.link_xray(u) for u in X.LINK_CHECKS]
card = S.family_card(scans["m1"], X.PERSONA["helper_th"], "แม่")
card2 = S.family_card(scans["m3"], X.PERSONA["helper_th"], "แม่")
round_ids = S.quiz_round(X.QUIZ_DECK, X.QUIZ_SEED)
grade = S.quiz_grade(X.QUIZ_DECK, round_ids, X.QUIZ_ANSWERS)
quiz_engine = {c["id"]: S.scan(c["text"], c["sender"], c["channel"])["score"] for c in X.QUIZ_DECK}
call = S.call_shield(X.CALL_TICKED)
history = X.HISTORY + [S.history_entry(scans[i], X.TODAY) for i in ("m1", "m2", "m3", "m4")]
wrapped = S.shield_wrapped(history, "2026-10", X.QUIZ_DAYS)

expect_locked = {
    "today": X.TODAY,
    "inbox_scores": {k: v["score"] for k, v in scans.items()}, "inbox_levels": {k: v["level"] for k, v in scans.items()},
    "m1_flags": [f["rule_id"] for f in scans["m1"]["flags"]], "m1_real_site": scans["m1"]["links"][0]["real_site"],
    "m1_raw_plus_combo": [scans["m1"]["raw_score"], scans["m1"]["combo_bonus"]],
    "xray_verdicts": [x["verdict"] for x in xrays],
    "quiz_round": round_ids, "quiz_right": grade["right"], "quiz_badge": grade["badge_th"],
    "call_shield_score": call["score"], "call_shield_level": call["level"],
    "wrapped": {k: wrapped[k] for k in ("checked", "flagged", "low", "top_rule_id", "most_faked_brand", "quiz_streak_days")},
}
rules = [{"id": r[0], "weight": r[1], "label_th": r[2], "explain_th": r[3], "patterns": r[4]} for r in S.RULES]
brands = [{"id": k, "name_th": v["name_th"], "text": v["text"], "host": v["host"], "official": v["official"], "verified": False} for k, v in S.BRANDS.items()]
ui = {
    "home_title": "ข้อความนี้ หลอกรึเปล่า?", "paste_cta": "📋 วางข้อความ / แชร์มาจาก SMS-LINE", "shot_cta": "🖼️ ส่งรูปแคปหน้าจอ", "demo_cta": "ลองกล่องข้อความป้าแดง (ตัวอย่าง)",
    "scanning": "กำลังส่องหาสัญญาณมิจฉา…", "meter_title": "ระดับความเสี่ยง", "flags_title": "เจอ {n} จุดอันตราย", "xray_title": "Link X-Ray",
    "xray_real_site": "เว็บจริงคือ {site}", "actions_title": "ทำแบบนี้เลย", "copy_reply": "คัดลอกคำตอบปลอดภัย", "family_cta": "ส่งเตือนแม่/พ่อทาง LINE",
    "quiz_title": "จริงหรือหลอก? วันละ 5 ข้อ", "quiz_scam": "หลอก 🚨", "quiz_real": "จริง ✅", "call_title": "กำลังคุยสายอยู่? ติ๊กสิ่งที่ได้ยิน",
    "wrapped_title": "เดือนนี้ฉันรอดมิจฉา", "big_text": "ตัวหนังสือใหญ่", "read_aloud": "อ่านออกเสียง",
    "disclaimer": "ผลนี้เป็นสัญญาณเตือน ไม่ใช่คำตัดสิน · ไม่แน่ใจให้โทรถามเบอร์ทางการที่หาเอง",
    "levels": {lv: lab for _, lv, lab, _, _ in S.LEVELS},
}
reel = [
    {"t": "0-3s", "shot": "มือถือแม่เด้ง SMS 'บัญชีถูกระงับ' ซูมลิงก์", "vo_th": "แม่ส่ง SMS นี้มาถามว่าต้องกดไหม…", "overlay_th": "แม่เกือบกดแล้ว 😱"},
    {"t": "3-8s", "shot": "จอคอม: วาง Prompt A → โค้ดวิ่ง → แอปขึ้น (ตัดเร็ว x8)", "vo_th": "งั้นให้ AI สร้างแอปจับมิจฉาให้แม่เลย", "overlay_th": "สร้างแอปใน 1 ชั่วโมง"},
    {"t": "8-14s", "shot": "วางข้อความ → มิเตอร์วิ่ง 0→90 แดง ไซเรนกระพริบ คำอันตรายถูกไฮไลต์ทีละคำ", "vo_th": "90 เต็ม 100 ไฮไลต์ให้เลยว่าตรงไหนหลอก", "overlay_th": "🚨 90/100"},
    {"t": "14-19s", "shot": "Link X-Ray แตกโดเมน kbank-verify-th.top เทียบ kasikornbank.com", "vo_th": "ลิงก์นี้ไม่ใช่ธนาคารจริง", "overlay_th": "ปลอม ❌ จริง ✅"},
    {"t": "19-24s", "shot": "สลับ 3 ฟีเจอร์: Family Card ส่ง LINE · Call Shield ติ๊ก 4 ข้อ = 80 · Quiz ปัดซ้ายขวา", "vo_th": "ส่งเตือนแม่ได้ คุยสายอยู่ก็เช็กได้ มีเกมฝึกด้วย", "overlay_th": "5 ฟีเจอร์ในแอปเดียว"},
    {"t": "24-30s", "shot": "แม่ยิ้มถือมือถือ ตัวหนังสือใหญ่ + การ์ด Wrapped", "vo_th": "คอมเมนต์ 'กันโกง' เดี๋ยวส่งลิงก์ให้ ไปลงเครื่องพ่อแม่กัน", "overlay_th": "คอมเมนต์ 'กันโกง' รับแอปฟรี"},
]
examples = {
    "meta": {"app": "ScamScan (มิจฉาสแกน)", "date": X.TODAY, "engine": S.VERSION, "fictional_note_th": "บุคคล ผู้ส่ง โดเมน ข้อความ ทั้งหมดเป็นตัวอย่างสมมติ",
             "colors": COLORS},
    "rules": rules, "brands": brands, "levels": [{"min": a, "level": b, "label_th": c, "color": d, "emoji": e} for a, b, c, d, e in S.LEVELS],
    "call_signs": [{"id": a, "weight": b, "label_th": c} for a, b, c in S.CALL_SIGNS],
    "demo": {"persona": X.PERSONA, "inbox": X.INBOX, "scan_inputs": [{"text": m["text"], "sender": m["sender"], "channel": m["channel"], "source": "demo"} for m in X.INBOX]},
    "scan_results": scans, "link_xrays": xrays, "family_cards": [card, card2],
    "quiz": {"deck": X.QUIZ_DECK, "seed": X.QUIZ_SEED, "round": round_ids, "answers": X.QUIZ_ANSWERS, "grade": grade, "engine_scores": quiz_engine},
    "call_shield": call, "history": history, "wrapped": wrapped,
    "local_store": {"version": 1, "settings": {"big_text": True, "read_aloud": True, "family": [{"name_th": "มิ้นท์", "relation_th": "ลูกสาว"}],
                    "share_history_with_family": False, "ai_explain": False}, "history": history, "quiz_days": X.QUIZ_DAYS, "custom_brands": [], "blocked_senders": ["KBank-TH"]},
    "ai_examples": {
        "explain_request": {"text": X.INBOX[0]["text"], "flags": [f["rule_id"] for f in scans["m1"]["flags"]], "level": scans["m1"]["level"], "audience": "elder"},
        "explain_response": {"summary_th": "ข้อความนี้ทำทีเป็นธนาคาร แต่ลิงก์ไม่ใช่เว็บธนาคารจริง และขอ OTP ซึ่งธนาคารไม่ขอแบบนี้", "why_th": ["ขู่ว่าบัญชีถูกระงับให้รีบ", "ลิงก์ .top ไม่ใช่ kasikornbank.com", "ขอ OTP"], "never_change_score": True},
        "ocr_response": {"text": X.INBOX[1]["text"], "sender_guess": "ThaiPost", "channel_guess": "sms", "confidence": 0.93}},
    "ui_copy_th": ui, "reel_script": reel, "expect_locked": expect_locked,
}
checks = [("ScanResult", v) for v in scans.values()] + [("LinkXray", x) for x in xrays] + [("FamilyCard", c) for c in (card, card2)] \
    + [("QuizCard", c) for c in X.QUIZ_DECK] + [("QuizGrade", grade), ("CallShield", call), ("Wrapped", wrapped), ("LocalStore", examples["local_store"])] \
    + [("HistoryEntry", h) for h in history] + [("Rule", r) for r in rules] + [("Brand", b) for b in brands] \
    + [("CallSign", c) for c in examples["call_signs"]] + [("ScanInput", s) for s in examples["demo"]["scan_inputs"]] \
    + [("AiExplainRequest", examples["ai_examples"]["explain_request"]), ("AiExplainResponse", examples["ai_examples"]["explain_response"]), ("AiOcrResponse", examples["ai_examples"]["ocr_response"])]
jsonschema.Draft202012Validator.check_schema(ROOT)
errs = 0
for name, inst in checks:
    v = jsonschema.Draft202012Validator({**ROOT, "$ref": f"#/$defs/{name}"})
    for e in v.iter_errors(inst):
        errs += 1; print("ERR", name, list(e.path), e.message)
(OUT / "schemas.json").write_text(json.dumps(ROOT, ensure_ascii=False, indent=2))
(OUT / "examples.json").write_text(json.dumps(examples, ensure_ascii=False, indent=2))
print(f"validated {len(checks)} objects against {len(ROOT['$defs'])} defs, errors={errs}")
print(json.dumps(expect_locked, ensure_ascii=False))
