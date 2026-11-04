# HairMirror — ลองทรงก่อนตัด (AI วันละแอป · 2026-11-02)

เซลฟี่ 1 รูป → รู้ทรงหน้า → เห็นตัวเองใน 9 ทรงผม → คะแนนเข้ากับหน้า/สภาพผม/เวลา/งบ → ให้เพื่อนโหวต → การ์ดยื่นช่างเป็นมิล → เช็กทำสีต้องฟอกไหม → ไดอารีตัดผม + เตือนรอบ

## ในแพ็ก
- `prd.md` — ปัญหา, must-have / nice-to-have, หน้าจอ, demo fixture, design tokens, guardrails
- `prompts.md` — work-order prompts P0–P10 + vision/image-edit prompts (landmark, try-on, identity check, color)
- `schemas.json` — JSON Schema 2020-12 (16 defs)
- `examples.json` — 56 ตัวอย่าง (ข้อมูลสมมติ) validate ผ่านหมด
- `reference/` — `hairmirror.py` logic deterministic, `fixtures.py` (ภูมิ + catalog 9 ทรง), `tests.py` (22 tests), `build.py`

## รัน
```
cd reference && python3 tests.py && python3 build.py   # ต้องมี jsonschema
```

## หมายเหตุ
- กฎจัดทรงหน้าและน้ำหนักคะแนนเป็นแนวทางที่ตั้งเอง ไม่ใช่มาตรฐานความงาม ปรับได้ใน hairmirror.py
- ราคาร้าน ค่าฟอก ผมยาว 1.25 ซม./เดือน เป็นค่าตัวอย่าง ให้ผู้ใช้แก้เอง
- ภาพลองทรงต้องผ่าน identity check (เปลี่ยนแค่ผม) ก่อนแสดง
