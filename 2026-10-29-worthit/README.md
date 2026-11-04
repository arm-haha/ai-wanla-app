# WorthIt — คุ้มไหมก่อนกดซื้อ (AI วันละแอป · 2026-10-29)

ถ่าย/แคปของที่อยากได้ → ราคากลายเป็น "ชั่วโมงที่ต้องทำงานแลก" → ราคาต่อครั้งใช้ → Quiz 5 ข้อ → ซื้อ/รอ/ข้าม → Cool-off Timer → เงินที่ไม่ซื้อหล่นลงโหลเข้าเป้าหมาย

## ในแพ็ก
- `prd.md` — must-have / nice-to-have, หน้าจอ, flow, demo fixture, design tokens, guardrails
- `prompts.md` — work-order prompts P0–P10 + vision prompt + dupe prompt
- `schemas.json` — JSON Schema 2020-12 (13 defs)
- `examples.json` — 35 ตัวอย่าง (ข้อมูลสมมติ) validate ผ่านหมด
- `reference/` — `worthit.py` logic deterministic, `fixtures.py`, `tests.py` (21 tests), `build.py`

## รัน
```
cd reference && python3 tests.py && python3 build.py   # ต้องมี jsonschema
```

## หมายเหตุ
- ราคาใน demo เป็นตัวอย่าง ตอนถ่าย Reel ให้ใช้ของจริงที่อยากได้จริง
- ไม่ใช่คำแนะนำทางการเงิน รายได้ผู้ใช้อยู่ในเครื่องเท่านั้น
