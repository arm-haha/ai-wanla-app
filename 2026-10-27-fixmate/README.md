# FixMate — ของพังซ่อมเอง (AI วันละแอป · 2026-10-27)

ถ่ายของพัง 1 รูป → AI ชี้จุดเสีย → เช็กความปลอดภัย → ซ่อมเองหรือเรียกช่าง (เทียบราคา) → ขั้นตอนทีละสเต็ป → การ์ด Before/After + ยอดประหยัด

## ในแพ็ก
- `prd.md` — ฟีเจอร์ must-have / nice-to-have, หน้าจอ, demo fixture, design tokens, guardrails
- `prompts.md` — work-order prompts P0–P9 + system prompt ของ vision
- `schemas.json` — JSON Schema 2020-12 (14 defs)
- `examples.json` — 38 ตัวอย่าง (ข้อมูลสมมติ) validate ผ่านหมด
- `reference/` — `fixmate.py` logic deterministic, `fixtures.py`, `tests.py` (17 tests), `build.py`

## รัน
```
cd reference && python3 tests.py && python3 build.py   # ต้องมี jsonschema
```

## หมายเหตุ
- ราคาอะไหล่/ค่าช่างใน demo เป็นตัวอย่าง ให้ผู้ใช้กรอกเอง
- แอปเป็นตัวช่วย ไม่แทนช่าง งานไฟฟ้าหลัก แก๊ส น้ำยาแอร์ โครงสร้าง → เรียกช่างเสมอ
