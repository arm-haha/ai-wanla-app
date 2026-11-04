# LabelLens — ฉลากบอกหมด (AI วันละแอป · 2026-10-28)

ถ่ายฉลากขนม/เครื่องดื่ม 1 รูป → น้ำตาลกลายเป็นช้อนชาหล่นลงแก้ว → เกรด A–E + ไฟจราจร → เทียบ 2 ชิ้น → เช็กของที่แพ้ → บันทึกทั้งวัน + streak หวานน้อย

## ในแพ็ก
- `prd.md` — must-have / nice-to-have, หน้าจอ, flow, demo fixture, design tokens, guardrails
- `prompts.md` — work-order prompts P0–P9 + vision system prompt
- `schemas.json` — JSON Schema 2020-12 (13 defs)
- `examples.json` — 54 ตัวอย่าง (ข้อมูลสมมติ ไม่ใช่ฉลากแบรนด์จริง) validate ผ่านหมด
- `reference/` — `labellens.py` logic deterministic, `fixtures.py`, `tests.py` (19 tests), `build.py`

## รัน
```
cd reference && python3 tests.py && python3 build.py   # ต้องมี jsonschema
```

## หมายเหตุ
- ตัวเลขใน demo เป็นตัวอย่าง ตอนถ่าย Reel ให้ใช้ฉลากจริงที่ซื้อมา
- เกณฑ์/โควตาเป็นค่าเริ่มของแอป ปรับได้ ไม่ใช่คำแนะนำทางการแพทย์
