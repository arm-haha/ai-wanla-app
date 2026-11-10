# FitDeck — ถ่ายอุปกรณ์ที่มี ได้ตารางออกกำลังกายที่บ้าน (AI วันละแอป · 2026-12-01)

ถ่ายมุมอุปกรณ์ในบ้าน → AI จับเสื่อโยคะ ดัมเบิล ยางยืด เชือกกระโดด หรือเก้าอี้ แล้วจัดแผน 20 นาทีพร้อมการ์ดจับเวลา บันทึกความก้าวหน้า และคำเตือนความปลอดภัย

**EN:** Photograph the equipment you already have → AI spots a mat, dumbbells, a band, a jump rope or a chair, then builds a 20-minute plan with timer cards, a progress log and safety notes.

## ในแพ็ก / Pack contents
- `prd.md` — ปัญหา, must-have / nice-to-have (10 ฟีเจอร์), หน้าจอ, demo fixture, design tokens, guardrails, shot list Reel
- `prompts.md` — work-order prompts P0–P12 + AI vision/text prompts A1–A5
- `schemas.json` — JSON Schema 2020-12 (14 defs)
- `examples.json` — 107 ตัวอย่าง (ข้อมูลสมมติ) validate ผ่านหมด
- `reference/` — `fitdeck.py` logic deterministic (อ่านอุปกรณ์, แผน 20 นาที, การ์ดจับเวลา, บันทึกเซสชัน, กันเจ็บ), `fixtures.py` (พี่กิ๊ฟ + 2 คนสมมติ, 6 รูป), `tests.py` (41 tests), `build.py`
- `social/` — `make_cover.py`, ปก 1080×1350 / 1080×1080, `fb_post.md`

## รัน / Run
```
cd reference && python3 tests.py && python3 build.py   # ต้องมี jsonschema
```

## หมายเหตุ / Notes
- FitDeck เป็น **ตารางตัวอย่าง ไม่ใช่เทรนเนอร์และไม่ใช่คำแนะนำทางการแพทย์**
- ถ้าเจ็บหรือเวียนหัวให้หยุดทันที และปรึกษาแพทย์ก่อนเริ่มถ้ามีโรคประจำตัว
- ระยะเวลาท่าเป็นค่าที่ตั้งเองในคลังท่า รวมแผนเดโม 20 นาที (1,200 วินาที)
- ตัวอย่างและภาพปกเป็นบุคคล/อุปกรณ์สมมติ ภาพวาด ไม่ใช้คนจริงหรือยี่ห้อจริง
