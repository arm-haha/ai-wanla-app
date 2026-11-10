# PosterPop — พิมพ์รายละเอียดงาน ได้โปสเตอร์สวยทันที (AI วันละแอป · 2026-12-07)

พิมพ์ชื่อโปร งาน หรือเมนู → จัดเลย์เอาต์ภาษาไทยอัตโนมัติ เลือกเทมเพลตโปร/อีเวนต์/เมนู ใส่คิวอาร์ เลือกขนาด FB/IG/พิมพ์ A4–A3 และบันทึกชุดสีร้าน พร้อมเช็กคอนทราสต์ให้อ่านชัด

**EN:** Type a sale, event or menu brief → auto Thai typographic layout, templates, a QR code, FB/IG/print size presets and a brand kit with a contrast check.

## ในแพ็ก / Pack contents
- `prd.md` — ปัญหา, must-have / nice-to-have (10 ฟีเจอร์), หน้าจอ, demo fixture, design tokens, guardrails, shot list Reel
- `prompts.md` — work-order prompts P0–P12 + AI vision/text prompts A1–A5
- `schemas.json` — JSON Schema 2020-12 (14 defs)
- `examples.json` — 80 ตัวอย่าง (ข้อมูลสมมติ) validate ผ่านหมด
- `reference/` — `posterpop.py` logic deterministic (3 เทมเพลต, 6 ขนาด, คอนทราสต์ WCAG AA, ชุดสี, คิวอาร์, กริดเมนู), `fixtures.py` (พี่เจ + Ficto Café, พี่มอ + ตลาดนัดสมมติ), `tests.py` (41 tests), `build.py`
- `social/` — `make_cover.py`, ปก 1080×1350 / 1080×1080, `fb_post.md`

## รัน / Run
```
cd reference && python3 tests.py && python3 build.py   # ต้องมี jsonschema
```

## หมายเหตุ / Notes
- PosterPop เป็น **เครื่องมือจัดเลย์เอาต์ ไม่ใช่โรงพิมพ์ และไม่มีโลโก้แบรนด์สำเร็จ**
- ผู้ใช้ต้องมีสิทธิ์ในข้อความ รูป และเครื่องหมายการค้าที่ใส่ และควรตรวจคำกับราคาอีกครั้งก่อนโพสต์หรือพิมพ์
- สูตรขนาดตัวอักษรตามความยาวหัวข้อ และเกณฑ์คอนทราสต์ AA (ตัวใหญ่ 3:1 / ตัวเนื้อ 4.5:1) เป็นค่าตัวอย่าง ปรับได้ใน `title_size()` / `contrast_check()`
- ร้านและงานในตัวอย่าง (Ficto Café, Ficto Night Market) เป็นสมมติ ภาพปกสร้างด้วย PIL เป็นภาพประกอบ ไม่ใช้โลโก้จริง
