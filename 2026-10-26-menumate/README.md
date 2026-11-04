# MenuMate — อ่านเมนูไม่ออก (AI วันละแอป · 2026-10-26)

ถ่ายเมนูภาษาญี่ปุ่น/เกาหลี/จีน 1 รูป → เมนูไทย + ราคาบาท + ป้ายแพ้อาหาร → จัดออเดอร์ตามงบ → การ์ดยื่นสั่งพนักงาน → เช็กบิล + หารเงิน

## ในแพ็ก
- `prd.md` — PRD สั้น ฟีเจอร์ must-have / nice-to-have, หน้าจอ, demo fixture, design tokens
- `prompts.md` — work-order prompts P0–P9 สำหรับ AI codegen + system prompt ของ vision
- `schemas.json` — JSON Schema 2020-12 (14 defs)
- `examples.json` — 39 ตัวอย่าง (ข้อมูลสมมติ, rate ตัวอย่าง 0.23 ฿/¥) ผ่าน validate ทั้งหมด
- `reference/` — `menumate.py` logic แบบ deterministic, `fixtures.py`, `tests.py` (17 tests), `build.py` (สร้าง+validate schemas/examples)

## รัน
```
cd reference && python3 tests.py && python3 build.py   # ต้องมี jsonschema
```

## หมายเหตุ
- ร้าน/ราคาใน demo เป็นข้อมูลสมมติ ไม่ใช่ร้านจริง; อัตราแลกเปลี่ยนต้องให้ผู้ใช้ตั้งเอง
- ป้ายแพ้อาหารเป็นตัวช่วย ไม่ใช่การรับรอง ต้องยืนยันกับร้านเสมอ
