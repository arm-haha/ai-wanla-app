# StickerMe — เซลฟี่เดียว ได้สติกเกอร์ LINE หน้าตัวเองทั้งเซ็ต (AI วันละแอป · 2026-11-25)

ถ่ายเซลฟี่รูปเดียว → AI วาดเป็นชุดสติกเกอร์ 16 อารมณ์ (ยิ้ม หัวเราะ รัก โกรธ ง่วง ฯลฯ) ติดข้อความไทยสั้น ๆ เลือกสไตล์ 8 แบบ แล้วแพ็กตามขนาดที่ใช้ใน LINE Creators พร้อมกันใช้เฉพาะใบหน้าของตนเอง

**EN:** One selfie → an illustrated 16-emotion sticker set (happy, laugh, love, angry, sleepy and more), short Thai text bubbles, 8 style packs, and an export checklist sized for LINE Creators, with an own-face consent guard.

## ในแพ็ก / Pack contents
- `prd.md` — ปัญหา, must-have / nice-to-have (10 ฟีเจอร์), หน้าจอ, demo fixture, design tokens, guardrails, shot list Reel
- `prompts.md` — work-order prompts P0–P12 + AI vision/image/text prompts A1–A5
- `schemas.json` — JSON Schema 2020-12 (19 defs)
- `examples.json` — 89 ตัวอย่าง (ข้อมูลสมมติ) validate ผ่านหมด
- `reference/` — `stickerme.py` logic deterministic (สแกนเซลฟี่, ชุดอารมณ์, ข้อความไทย, สเปกส่ง Creators, กันใช้หน้าคนอื่น), `fixtures.py` (น้องเจน + 2 คนสมมติ, 6 เซลฟี่), `tests.py` (41 tests), `build.py`
- `social/` — `make_cover.py`, ปก 1080×1350 / 1080×1080, `fb_post.md`

## รัน / Run
```
cd reference && python3 tests.py && python3 build.py   # ต้องมี jsonschema
```

## หมายเหตุ / Notes
- StickerMe เป็น **ภาพประกอบจากเซลฟี่ ไม่ใช่รูปถ่ายจริง และไม่ใช่ผลิตภัณฑ์ของ LINE**
- ขนาด 370×320 / 240×240 / 96×74 และจำนวน 8, 16, 24 ใบ เป็น **ค่าตัวอย่างที่อ้างอิงสเปกที่เผยแพร่ทั่วไป** ต้องตรวจกับคู่มือทางการของ LINE Creators Studio ก่อนอัปโหลด
- ใช้ได้เฉพาะใบหน้าของตนเอง ถ้าดูเหมือนผู้เยาว์ต้องได้รับความยินยอมจากผู้ปกครอง ห้ามใช้หน้าคนอื่นหรือเลียนแบบคนดัง
- ตัวอย่างและภาพปกเป็นบุคคลสมมติ/ภาพวาด ไม่ใช้ใบหน้าจริง
