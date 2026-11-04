# RoomGlow — ห้องเดิม ลุคใหม่ (AI วันละแอป · 2026-11-03)

ถ่ายห้อง 1 รูป → Glow Score → เห็นห้องตัวเองใน 6 ลุค → ลิสต์ของตามงบ (โหมดห้องเช่า ไม่เจาะผนัง) → Before/After → แผนไฟ, คำนวณสี/วอลเปเปอร์, เคลียร์ของ, แผนวันหยุด, ให้เพื่อนโหวต

## ในแพ็ก
- `prd.md` — ปัญหา, must-have / nice-to-have, หน้าจอ, demo fixture, design tokens, guardrails
- `prompts.md` — work-order prompts P0–P10 + AI prompts (room scan, restyle, layout check, palette)
- `schemas.json` — JSON Schema 2020-12 (17 defs)
- `examples.json` — 54 ตัวอย่าง (ข้อมูลสมมติ) validate ผ่านหมด
- `reference/` — `roomglow.py` logic deterministic, `fixtures.py` (ห้องของฝน + catalog 12 ชิ้น), `tests.py` (22 tests), `build.py`

## รัน
```
cd reference && python3 tests.py && python3 build.py   # ต้องมี jsonschema
```

## หมายเหตุ
- ราคาสินค้า ค่า impact และน้ำหนัก Glow Score เป็นค่าตัวอย่างที่ตั้งเอง ไม่ใช่ราคาร้านจริง ปรับใน fixtures.py / roomglow.py
- ค่า lux (นอน 150 / นั่งเล่น 200 / โต๊ะ 500), สี 10 ตร.ม./ลิตร, วอลเปเปอร์ 5.3 ตร.ม./ม้วน เป็นค่าประมาณทั่วไป
- ภาพแต่งใหม่ต้องผ่าน layout check ก่อนแสดง
