# CardReady — รูปติดบัตรผ่านชัวร์ (AI วันละแอป · 2026-11-06)

เซลฟี่มั่ว ๆ → รูปติดบัตรพื้นขาวคมชัดใน 3 วินาที. ถ่ายเซลฟี่ → ตรวจหน้า + ครอปตามสัดส่วนบัตรอัตโนมัติ + ตัดพื้นหลัง → เลือกพื้น ขาว/ฟ้ากรมการ/แดง/สีเอง → เลือกขนาด 1 นิ้ว 2 นิ้ว พาสปอร์ต วีซ่า ใบสมัครงาน → ปรับแสงนุ่มแบบธรรมชาติ (ไม่แต่งหน้าพลาสติก ไม่ดัดหน้า) → จัดหน้า A4 หลายใบพร้อมเส้นตัดและเช็ก dpi → เช็กลิสต์ตามประเภทเอกสาร, ประวัติในเครื่อง, การ์ด Before/After, โหมดครอบครัว, ส่งออก JPG/PNG + PDF

**EN:** Messy selfie → clean white-background ID/pass photo in 3 seconds. Face detect, auto crop, background removal, BG presets, Thai size presets, soft light with no beauty filter, A4 print sheet with cut guides and dpi check, per-document checklists, on-device history, before/after share card, family batch and export pack.

## ในแพ็ก / Pack contents
- `prd.md` — ปัญหา, must-have / nice-to-have (10 ฟีเจอร์), หน้าจอ, demo fixture, design tokens, guardrails (ไม่อ้างการรับรองจากราชการ ไม่แต่งหน้า)
- `prompts.md` — work-order prompts P0–P12 + AI vision prompts A1–A5
- `schemas.json` — JSON Schema 2020-12 (17 defs)
- `examples.json` — 62 ตัวอย่าง (ข้อมูลสมมติ) validate ผ่านหมด
- `reference/` — `cardready.py` logic deterministic, `fixtures.py` (น้องมิ้นท์ + 4 คนสมมติ), `tests.py` (31 tests), `build.py`
- `social/` — `make_cover.py`, ปก 1080×1350 / 1080×1080, `fb_post.md`
- `cardready.zip` — ทั้งโฟลเดอร์ในไฟล์เดียว

## รัน / Run
```
cd reference && python3 tests.py && python3 build.py   # ต้องมี jsonschema
```

## หมายเหตุ / Notes
- ขนาดรูปคำนวณที่ 300 dpi (1 นิ้ว = 25×35 mm = 295×413 px) เป็นขนาดที่ใช้บ่อยในไทย — **ตรวจข้อกำหนดล่าสุดของหน่วยงานปลายทางก่อนใช้จริง** แอปนี้ไม่ได้รับรองจากหน่วยงานราชการ
- Pass Score, น้ำหนักความรก, ค่า soft light สูงสุด, โควตาฟรี 5 ไฟล์/วัน เป็นค่าที่ตั้งเอง ปรับได้
- Soft Light ทำแค่แสงสม่ำเสมอ + ลดสีเหลือง + ลดตำหนิเล็กน้อย ห้ามเปลี่ยนรูปหน้า/ผิวพลาสติก (เพราะรูปติดบัตรต้องเหมือนตัวจริง)
- ทุกตัวอย่างเป็นบุคคลสมมติ ภาพปกสร้างด้วย PIL เป็นภาพประกอบ ไม่ใช้ใบหน้าจริง
