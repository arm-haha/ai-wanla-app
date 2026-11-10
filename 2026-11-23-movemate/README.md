# MoveMate — ย้ายบ้านไม่ป่วน (AI วันละแอป · 2026-11-23)

เช็กลิสต์ทีละห้อง ทำป้ายกล่องพร้อมคิวอาร์และรูปของในกล่อง (เก็บในเครื่อง) ค้นของว่าอยู่ในกล่องไหน ดูไทม์ไลน์วันย้ายเป็นชั่วโมง และลิสต์โอนยูทิลิตี้ (ไฟ น้ำ เน็ต พัสดุ คืนกุญแจ) พร้อมประมาณค่ากล่องเทปและรถกระบะเป็นบาท

**EN:** Room-by-room checklists, box labels with a QR code and an on-device photo of the contents, find-my-item search, a moving-day hour-by-hour timeline, a utility transfer list, and a THB cost estimate for boxes, tape and a van.

## ในแพ็ก / Pack contents
- `prd.md` — ปัญหา, must-have / nice-to-have (10 ฟีเจอร์), หน้าจอ, demo fixture, design tokens, guardrails, shot list Reel
- `prompts.md` — work-order prompts P0–P12 + AI prompts A1–A5
- `schemas.json` — JSON Schema 2020-12 (16 defs)
- `examples.json` — 83 ตัวอย่าง (ข้อมูลสมมติ) validate ผ่านหมด
- `reference/` — `movemate.py` logic deterministic (6 ห้อง, ป้าย MM-Bxx, ค้นของ, ไทม์ไลน์, ยูทิลิตี้, ประมาณราคา), `fixtures.py` (พี่แอม + น้องบี, 10 กล่อง), `tests.py` (41 tests), `build.py`
- `social/` — `make_cover.py`, ปก 1080×1350 / 1080×1080, `fb_post.md`
- `movemate.zip` — ทั้งโฟลเดอร์ในไฟล์เดียว

## รัน / Run
```
cd reference && python3 tests.py && python3 build.py   # ต้องมี jsonschema
```

## หมายเหตุ / Notes
- MoveMate เป็น **เช็กลิสต์ย้ายบ้านเบื้องต้น ไม่ใช่บริษัทขนย้ายและไม่ใช่ใบเสนอราคา**
- ค่ากระบะ กล่อง และเทปใน `VAN_TYPES` / `BOX_COST` เป็นค่าตัวอย่าง ปรับตามพื้นที่ได้
- รูปของในกล่องเก็บในเครื่อง (`on_device`) อย่าวางของมีค่าในกล่องที่ยังไม่มีป้าย
- บุคคลและที่อยู่ในตัวอย่างเป็นสมมติ ภาพปกสร้างด้วย PIL เป็นภาพประกอบ ไม่ใช้รูปคนหรือบ้านจริง
