# PhoneRescue — มือถือเต็ม/แบตหมดไว ถ่ายหน้าตั้งค่ารู้เลยว่าต้องทำอะไร (AI วันละแอป · 2026-11-24)

ถ่ายหรือแคปหน้าตั้งค่าพื้นที่ว่างและสุขภาพแบต → AI อ่านตัวเลข จัดแผนเก็บข้อมูลเรียงตาม GB ที่จะได้คืน (รูปซ้ำ แคปจอ สำรองแชท แอปไม่ได้ใช้ แคช) พร้อมคู่มือลบรูปซ้ำ เคล็ดลับประหยัดแบต และเทียบราคาเปลี่ยนแบตกับเครื่องใหม่เป็นบาท

**EN:** Photograph your storage and battery settings screens → AI reads the numbers, builds a cleanup plan ranked by GB you’ll get back (duplicate photos, screenshots, chat backups, unused apps, cache), plus a duplicate-photo guide, battery tips and a THB repair-or-replace price check.

## ในแพ็ก / Pack contents
- `prd.md` — ปัญหา, must-have / nice-to-have (10 ฟีเจอร์), หน้าจอ, demo fixture, design tokens, guardrails, shot list Reel
- `prompts.md` — work-order prompts P0–P12 + AI vision/text prompts A1–A5
- `schemas.json` — JSON Schema 2020-12 (16 defs)
- `examples.json` — 84 ตัวอย่าง (ข้อมูลสมมติ) validate ผ่านหมด
- `reference/` — `phonerescue.py` logic deterministic (อ่านพื้นที่/แบต, แผนเก็บข้อมูล, คู่มือรูปซ้ำ, เคล็ดลับแบต, เทียบซ่อม/เปลี่ยน), `fixtures.py` (น้องปอ + 2 คนสมมติ, 9 แคปจอ), `tests.py` (41 tests), `build.py`
- `social/` — `make_cover.py`, ปก 1080×1350 / 1080×1080, `fb_post.md`
- `phonerescue.zip` — ทั้งโฟลเดอร์ในไฟล์เดียว

## รัน / Run
```
cd reference && python3 tests.py && python3 build.py   # ต้องมี jsonschema
```

## หมายเหตุ / Notes
- PhoneRescue เป็น **คำแนะนำเบื้องต้น ไม่ใช่ร้านซ่อมและไม่ใช่ใบเสนอราคา**
- ตัวเลข GB ที่จะได้คืน และช่วงราคาเปลี่ยนแบต (฿1,900–3,500) / เครื่องใหม่ (฿12,900–19,900) เป็น **ค่าตัวอย่างที่ตั้งเอง** ใน `CLEANUP` / `BATTERY_REPAIR` / `NEW_PHONE`
- สำรองรูปและแชทก่อนลบ และอย่ารีเซ็ตเครื่องถ้ายังไม่ได้สำรอง
- รุ่นเครื่องในตัวอย่าง (FictoPhone) เป็นสมมติ ภาพปกสร้างด้วย PIL เป็นภาพประกอบ ไม่ใช้รูปคนหรือหน้าจอจริง
