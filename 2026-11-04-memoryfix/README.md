# MemoryFix — รูปเก่าพ่อแม่ ชัดเหมือนใหม่ (AI วันละแอป · 2026-11-04)

ถ่ายรูปเก่าจากอัลบั้ม → ดัดมุม/ลบแสงสะท้อน → Damage Score → ซ่อมกดเดียว + สไลเดอร์ Before/After → ลงสี → เช็กว่าพิมพ์ขนาดไหนได้ → ไทม์ไลน์ครอบครัว, แท็กคน, Then & Now, อัดเสียงเล่าเรื่อง, ขยับเบาๆ (มีความยินยอม)

## ในแพ็ก
- `prd.md` — ปัญหา, must-have / nice-to-have (11 ฟีเจอร์), หน้าจอ, demo fixture, design tokens, guardrails
- `prompts.md` — work-order prompts P0–P11 + AI prompts A1–A5
- `schemas.json` — JSON Schema 2020-12 (14 defs)
- `examples.json` — 39 ตัวอย่าง (ข้อมูลสมมติ) validate ผ่านหมด
- `reference/` — `memoryfix.py` logic deterministic, `fixtures.py` (อัลบั้มแม่ของต้น 5 รูป), `tests.py` (22 tests), `build.py`

## รัน
```
cd reference && python3 tests.py && python3 build.py   # ต้องมี jsonschema
```

## หมายเหตุ
- น้ำหนัก Damage Score, เกณฑ์ step, โควตาฟรี 3 รูป/วัน, threshold identity เป็นค่าที่ตั้งเอง ปรับได้
- ขนาดพิมพ์ใช้มาตรฐาน 4x6 / 5x7 / 8x10 นิ้ว และ A4, เกณฑ์ ≥200 dpi (300 dpi ดีที่สุด)
- สีจาก colorize เป็นการเดาของ AI ต้องติดป้ายเสมอ
