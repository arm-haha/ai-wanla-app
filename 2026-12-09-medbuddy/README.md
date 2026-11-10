# MedBuddy — ถ่ายซองยาพ่อแม่ ได้ตารางกินยาและเตือนลูก (AI วันละแอป · 2026-12-09)

ถ่ายซองยาโรงพยาบาล → อ่านชื่อ ขนาด และมื้อยา จัดตารางเช้า-กลางวัน-เย็น-ก่อนนอน ส่งให้ลูกในครอบครัวเตือน แจ้งเมื่อใกล้หมด และทำบัตรรายการยาไปพบแพทย์ (ต้องยืนยันกับเภสัชกร ห้ามเปลี่ยนขนาดยาเอง)

**EN:** Photograph a parent’s medicine envelopes → read the name, strength and times, build a daily schedule, share it with family, get a refill nudge and a doctor-visit card (confirm with a pharmacist; the app never changes doses).

## ในแพ็ก / Pack contents
- `prd.md` — ปัญหา, must-have / nice-to-have (10 ฟีเจอร์), หน้าจอ, demo fixture, design tokens, guardrails, shot list Reel
- `prompts.md` — work-order prompts P0–P12 + AI vision/text prompts A1–A5
- `schemas.json` — JSON Schema 2020-12 (18 defs)
- `examples.json` — 86 ตัวอย่าง (ข้อมูลสมมติ) validate ผ่านหมด
- `reference/` — `medbuddy.py` logic deterministic (อ่านซอง, ยืนยันเมื่อความมั่นใจต่ำ, ตาราง, เตือนใกล้หมด, คู่มือลืมยาที่ไม่ให้กินเพิ่ม, การ์ดพบแพทย์), `fixtures.py` (พี่นนท์ + คุณวันดี, ยาสมมติ FictoPril / FictoMet / FictoPain), `tests.py` (41 tests), `build.py`
- `social/` — `make_cover.py`, ปก 1080×1350 / 1080×1080, `fb_post.md`

## รัน / Run
```
cd reference && python3 tests.py && python3 build.py   # ต้องมี jsonschema
```

## หมายเหตุ / Notes
- MedBuddy เป็น **ตารางช่วยเตือนเท่านั้น ไม่ใช่เภสัชกร ไม่ใช่แพทย์ และไม่ใช่ใบสั่งยา**
- **ห้ามเปลี่ยนขนาดยาเอง** ทุกครั้งต้องยืนยันกับเภสัชกรหรือแพทย์ก่อนใช้จริง ถ้าความมั่นใจของระบบต่ำกว่า 0.6 ต้องให้ผู้ใช้ยืนยันทุกช่องก่อนบันทึก
- ชื่อยาในตัวอย่างขึ้นต้นด้วย Ficto เป็น **ยาสมมติสำหรับเดโมเท่านั้น ไม่ใช่ยาจริงและไม่ใช่ขนาดที่ใช้ได้จริง**
- คู่มือลืมยาจะไม่แนะนำให้กินเพิ่มเป็นสองเท่า ต้องโทรถามเภสัชกรหรือแพทย์
- บุคคล คลินิก และแพทย์ในตัวอย่างเป็นสมมติ ภาพปกสร้างด้วย PIL เป็นภาพประกอบ ไม่ใช้คนจริงหรือซองยาจริง
