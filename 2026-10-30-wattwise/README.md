# WattWise — ค่าไฟไปไหนหมด (AI วันละแอป · 2026-10-30)

ถ่ายบิลค่าไฟ → พายบอกว่าเครื่องไหนกินไฟเท่าไหร่ → เลื่อนแอร์ 25→27°C เห็นเงินคืนสด → หาไฟรั่วสแตนด์บาย → ตั้งเป้าและถ่ายมิเตอร์ติดตาม → หารค่าไฟรูมเมทตามจริง

## ในแพ็ก
- `prd.md` — must-have / nice-to-have, หน้าจอ, flow, demo fixture, design tokens, guardrails
- `prompts.md` — work-order prompts P0–P10 + vision prompts (บิล / ป้ายเครื่องใช้ / มิเตอร์)
- `schemas.json` — JSON Schema 2020-12 (16 defs)
- `examples.json` — 46 ตัวอย่าง (ข้อมูลสมมติ) validate ผ่านหมด
- `reference/` — `wattwise.py` logic deterministic, `fixtures.py`, `tests.py` (20 tests), `build.py`

## รัน
```
cd reference && python3 tests.py && python3 build.py   # ต้องมี jsonschema
```

## หมายเหตุ
- เรท 4.20 ฿/หน่วยใน demo เป็นตัวอย่าง ตอนใช้จริงให้คำนวณจากบิลตัวเอง (ยอดรวม ÷ หน่วย)
- "ปรับแอร์ 1°C ประหยัด ~10%" เป็นสมมติฐานที่ตั้งค่าได้ ไม่ใช่ค่าที่วัดจริง
- ทุกตัวเลขเป็นค่าประมาณ ไม่ใช่บิลทางการ
