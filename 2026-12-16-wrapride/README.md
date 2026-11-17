# WrapRide — ถ่ายรถ ลองสีใหม่ก่อนจ่ายจริง (AI วันละแอป · 2026-12-16)

ถ่ายรถยนต์/มอเตอร์ไซค์ 1 รูป → AI อ่านรุ่นตัวถัง สีเดิม และมุมกล้อง → ลองสี wrap ใหม่ได้ทันที (12 สี × 5 ผิว: เงา / กึ่งเงา / ด้าน / โครเมียม / เปลี่ยนสีตามมุม + ทูโทนหลังคา) → ปัดดู ก่อน/หลัง → แต่งล้อและสติกเกอร์ → เช็กราคาประมาณ wrap/ทำสี/ล้อ และดูว่าใบเสนอราคาร้านแพงไปไหม → การ์ดสเปกส่งร้านทาง LINE → เช็กลิสต์เรื่องแจ้งเปลี่ยนสีกับขนส่ง/ประกัน → ทำคลิป Reel ก่อน/หลัง → ไดอารี่รถ, การ์ดแชร์, โควตา, Safety Guard (ไม่ติดทับไฟ/ป้ายทะเบียน, เบลอป้ายอัตโนมัติ)

**EN:** Snap your car or motorbike → AI reads the body type, original colour and angle → try a new wrap instantly (12 colours × 5 finishes: gloss / satin / matte / chrome / colour-shift, plus a two-tone roof) → swipe before/after → Rim & Sticker Studio → a fair-price check for wrap, paint and rims (estimates) that flags a shop quote as fair or too high → a shop brief card to send on LINE → a registration/insurance reminder checklist for colour changes → a before/after Reel maker → garage diary, share card, daily quota and safety guard (nothing over lights or plates; plates auto-blurred).

## ในแพ็ก / Pack contents
- `prd.md` — ปัญหา, must-have / nice-to-have (10 ฟีเจอร์), หน้าจอ, demo fixture, design tokens, Reel shot list, build plan, risks, guardrails, metrics
- `prompts.md` — work-order prompts P0–P12 + AI prompts A1–A5
- `schemas.json` — JSON Schema 2020-12 (19 defs)
- `examples.json` — 145 ตัวอย่าง (ข้อมูลสมมติ) validate ผ่านหมด
- `reference/` — `wrapride.py` logic deterministic (6 ประเภทรถ, 12 สี, 5 ผิว, 5 แบบการหุ้ม, ช่วงราคาประมาณ), `fixtures.py` (พี่ต้น + 3 คนสมมติ), `tests.py` (37 tests), `build.py`
- `social/` — `make_cover.py`, ปก 1080×1350 / 1080×1080, `fb_post.md`

## รัน / Run
```
cd reference && python3 tests.py && python3 build.py   # ต้องมี jsonschema
```

## หมายเหตุ / Notes
- ช่วงราคา (`VEHICLES`, `FINISHES`, `COVERAGE`, `RIM_PRICE_PER_IN`, `STICKER_BAHT`) เป็น **ค่าตัวอย่างโดยประมาณที่ตั้งเอง** ไม่ใช่ใบเสนอราคา ปรับตามตลาดในพื้นที่ได้
- เรื่องแจ้งเปลี่ยนสีรถ (`legal_check`) เป็น **ข้อมูลทั่วไป ไม่ใช่คำแนะนำทางกฎหมาย** แอปไม่ระบุค่าธรรมเนียม/กำหนดเวลาเป็นตัวเลข ให้ตรวจขั้นตอนล่าสุดกับกรมการขนส่งทางบกและบริษัทประกันเสมอ
- ภาพลองสีเป็นภาพจำลอง สีจริงต่างตามแสงและเกรดฟิล์ม; ห้ามติดฟิล์มทับไฟหน้า ไฟท้าย ไฟเลี้ยว ป้ายทะเบียน และกระจกหน้า
- ทุกตัวอย่างเป็นบุคคลสมมติ ภาพปกสร้างด้วย PIL เป็นภาพประกอบ ไม่ใช้รูปคนจริง ป้ายทะเบียนจริง หรือแบรนด์จริง
