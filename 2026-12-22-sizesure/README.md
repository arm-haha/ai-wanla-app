# SizeSure — ถ่าย 2 รูป รู้ไซซ์ก่อนกดสั่ง (AI วันละแอป · 2026-12-22)

ใส่เสื้อยืดพอดีตัว + เลกกิ้ง → พิมพ์ส่วนสูง → ถ่ายรูปหน้าตรง 1 รูป + ด้านข้าง 1 รูป (แปะกระดาษ A4 ที่ผนังช่วยเช็กสเกล) → AI หาเส้นขอบตัว คำนวณ **รอบอก เอว สะโพก ไหล่ แขน ขาใน** ด้วยโมเดลวงรี (กว้าง × หนา) ±2 ซม. → แคปหน้าจอ **ตารางไซซ์ของร้าน** → แอปอ่านตาราง แปลงนิ้วเป็นเซนติเมตร และ **คูณ 2 ให้อัตโนมัติถ้าร้านวัดแบบวางราบ** (กับดักที่คนสั่งผิดบ่อยที่สุด) → **แนะนำไซซ์ + มิเตอร์พอดี/คับ/หลวมรายจุด** ตามทรงที่ชอบ (สลิม/ปกติ/โอเวอร์ไซซ์) และความยืดของผ้า → **ไซซ์รองเท้าจากเท้าบนกระดาษ A4** (EU/US/UK + หน้าเท้ากว้างไหม) → **Size Passport** การ์ดไซซ์ประจำตัวของทุกคนในบ้าน → **Gift Size** ซื้อของขวัญปีใหม่ให้คนอื่นถูกไซซ์ → **Return-Risk** ก่อนกดสั่ง → บันทึกการวัด (ซ่อนตัวเลขได้) → การ์ดแชร์ / Reel พร้อม Privacy & Safety Guard (ต้องใส่เสื้อผ้า, อายุต่ำกว่า 18 ใช้สายวัดแทนรูป, วัดได้เฉพาะตัวเอง, ไม่มีคะแนนหุ่น)

**EN:** Put on a fitted T-shirt and leggings → type your height → take one front and one side photo (an A4 sheet on the wall double-checks scale) → AI finds your outline and estimates **chest, waist, hip, shoulder, sleeve and inseam** with an ellipse model (width × depth), about ±2 cm → screenshot the **shop's size chart** → the app reads it, converts inches to cm and **doubles flat-lay measurements automatically** (the #1 reason people order the wrong size) → **size pick + a per-area fit meter (good / tight / loose)** for your preferred fit (slim / regular / oversize) and fabric stretch → **shoe size from your foot on A4 paper** (EU/US/UK + wide-foot check) → a **Size Passport** card for everyone in the family → **Gift Size** for buying New Year presents for others → a **return-risk** check before you pay → a measurement log (numbers can be hidden) → share card / Reel, with a Privacy & Safety Guard (clothes on, under-18s use a tape measure instead of photos, measure yourself or a consenting person only, no body scoring).

## ในแพ็ก / Pack contents
- `prd.md` — ปัญหา, must-have / nice-to-have (10 ฟีเจอร์), หน้าจอ, demo fixture, design tokens, Reel shot list, build plan, risks / traps, guardrails, metrics
- `prompts.md` — work-order prompts P0–P12 + AI prompts A1–A5
- `schemas.json` — JSON Schema 2020-12 (21 defs)
- `examples.json` — 114 ตัวอย่าง (ข้อมูลสมมติ) validate ผ่านหมด
- `reference/` — `sizesure.py` logic deterministic (โมเดลวงรี Ramanujan, ตัวแปลงตารางไซซ์ inch/flat-lay, ตัวเลือกไซซ์ 3 ทรง × 3 ความยืด, ตารางรองเท้า 22–30 ซม., passport, gift, return-risk, log), `fixtures.py` (พี่แพรว 160 ซม. + 3 คนสมมติ, ร้านสมมติ 3 ร้าน), `tests.py` (35 tests), `build.py`
- `social/` — `make_cover.py`, ปก 1080×1350 / 1080×1080, `fb_post.md`, `caption_fb.txt`

## รัน / Run
```
cd reference && python3 tests.py && python3 build.py   # ต้องมี jsonschema
```

## หมายเหตุ / Notes
- ตัวเลขทั้งหมดเป็น **ค่าประมาณ** (±2 ซม. เมื่อใส่ชุดพอดีตัว, ±5 ซม. เมื่อเสื้อหลวม) ใช้ประกอบตารางของร้านเสมอ และแก้ด้วยสายวัดได้ (±1 ซม.)
- ตารางรองเท้าเป็นค่ากลางโดยประมาณ แต่ละแบรนด์ต่างกันได้ครึ่งไซซ์
- ต้องใส่เสื้อผ้าพอดีตัว ห้ามถ่ายแบบไม่ใส่เสื้อผ้า; รูปถูกประมวลผลแล้ว **ลบทันที** เก็บแค่ตัวเลข; อายุต่ำกว่า 18 ปีไม่ใช้รูป ให้ผู้ปกครองวัดด้วยสายวัด
- แอปไม่ให้คะแนนรูปร่าง ไม่คำนวณ BMI/น้ำหนัก ไม่แนะนำลดน้ำหนัก การ์ดแชร์ไม่แสดงตัวเลขสัดส่วน
- ทุกตัวอย่างเป็นบุคคลและร้านสมมติ ภาพปกสร้างด้วย PIL ล้วน (หุ่นเป็นภาพกราฟิก ไม่ใช่รูปคนจริง) ไม่ใช้แบรนด์จริง
