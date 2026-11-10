# InterviewAce — ซ้อมสัมภาษณ์งานกับ AI (AI วันละแอป · 2026-12-08)

เลือกตำแหน่งแล้วได้คลังคำถาม ตอบด้วยเสียงหรือข้อความ แล้วได้คะแนนโครงคำตอบ ความชัด ความยาว และ STAR พร้อมนับคำเติม เขียนใหม่เป็นโครง STAR และรายงานความพร้อม (เป็นเครื่องมือซ้อม ไม่ได้การันตีว่าจะได้งาน)

**EN:** Pick a role, practise answers, and get scores for structure, clarity, length and STAR, plus a filler-word count, a STAR rewrite and a confidence report (practice only — not a job offer).

## ในแพ็ก / Pack contents
- `prd.md` — ปัญหา, must-have / nice-to-have (10 ฟีเจอร์), หน้าจอ, demo fixture, design tokens, guardrails, shot list Reel
- `prompts.md` — work-order prompts P0–P12 + AI vision/text prompts A1–A5
- `schemas.json` — JSON Schema 2020-12 (12 defs)
- `examples.json` — 82 ตัวอย่าง (ข้อมูลสมมติ) validate ผ่านหมด
- `reference/` — `interviewace.py` logic deterministic (6 ตำแหน่ง, คำถาม 24 ข้อ, คะแนนสูตรคงที่, นับคำเติม, เขียน STAR, แบบฝึก), `fixtures.py` (น้องกันต์ + น้องปินสมมติ), `tests.py` (41 tests), `build.py`
- `social/` — `make_cover.py`, ปก 1080×1350 / 1080×1080, `fb_post.md`

## รัน / Run
```
cd reference && python3 tests.py && python3 build.py   # ต้องมี jsonschema
```

## หมายเหตุ / Notes
- InterviewAce เป็น **เครื่องมือซ้อมสัมภาษณ์เท่านั้น ไม่ใช่การรับรองว่าจะได้งาน และไม่ใช่คะแนนจากผู้สัมภาษณ์จริง**
- คะแนนรวม โครง ความชัด ความยาว และ STAR เป็น **สูตรตัวอย่างที่ตั้งเอง** ปรับได้ใน `score_answer()`
- คำเติมที่นับคือ อ่า / เอ่อ / คือ / ก็ / แบบ เมื่อตัดคำด้วยช่องว่างในข้อความถอดเสียง
- บริษัทในตัวอย่าง (Ficto Media, Ficto Labs) เป็นสมมติ ภาพปกสร้างด้วย PIL เป็นภาพประกอบ ไม่ใช้คนจริง
