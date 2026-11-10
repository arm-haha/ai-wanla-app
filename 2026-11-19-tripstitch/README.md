# TripStitch — แคปจอที่เที่ยวเก็บไว้ กลายเป็นทริปพร้อมเที่ยว (AI วันละแอป · 2026-11-19)

แคปจอร้าน คาเฟ่ จุดถ่ายรูปที่เซฟไว้ในมือถือ → AI ดึงชื่อสถานที่และย่าน จัดเส้นทางรายวันตามช่วงเช้า-บ่าย-เย็น คิดงบประมาณแยกที่พัก อาหาร เดินทาง ค่าเข้า และของจิปาถะ พร้อมลิสต์ของที่ต้องแพ็ก และการ์ดทริปใช้ออฟไลน์ได้

**EN:** Saved screenshots of cafes, shops and photo spots → AI extracts the places, builds a day-by-day route (morning / afternoon / evening), splits a THB budget across stay, food, transport, tickets and extras, makes a packing list and an offline share card.

## ในแพ็ก / Pack contents
- `prd.md` — ปัญหา, must-have / nice-to-have (10 ฟีเจอร์), หน้าจอ, demo fixture, design tokens, guardrails, shot list Reel
- `prompts.md` — work-order prompts P0–P12 + AI vision/text prompts A1–A5
- `schemas.json` — JSON Schema 2020-12 (20 defs)
- `examples.json` — 150 ตัวอย่าง (ข้อมูลสมมติ) validate ผ่านหมด
- `reference/` — `tripstitch.py` logic deterministic (ดึงสถานที่, จัดวัน, งบ, แพ็กของ, เตือนร้านปิด), `fixtures.py` (พี่เก้า + 2 คนสมมติ, 10 แคปจอ), `tests.py` (41 tests), `build.py`
- `social/` — `make_cover.py`, ปก 1080×1350 / 1080×1080, `fb_post.md`
- `tripstitch.zip` — ทั้งโฟลเดอร์ในไฟล์เดียว

## รัน / Run
```
cd reference && python3 tests.py && python3 build.py   # ต้องมี jsonschema
```

## หมายเหตุ / Notes
- TripStitch เป็น **แผนเที่ยวเบื้องต้น ไม่ใช่ข้อมูลเวลาเปิด-ปิด ราคาจอง หรือเส้นทางเรียลไทม์**
- ชั่วโมงเปิด-ปิด วันหยุด ระยะเดินทาง (นาที) และตัวเลขงบเป็น **ค่าตัวอย่างที่ตั้งเอง** ใน `AREA_MIN` / `VISIT_COST` / `STAY_PER_NIGHT` ต้องตรวจกับแหล่งจริงก่อนเดินทาง
- ชื่อร้านในตัวอย่าง (FictoBean, FictoHill, FictoSoi ฯลฯ) เป็นสมมติทั้งหมด ไม่ใช่ร้านจริง
- ห้ามแชร์ตำแหน่งบ้านของผู้อื่นจากแคปจอแผนที่ ภาพปกสร้างด้วย PIL เป็นภาพประกอบ ไม่ใช้รูปคนจริง
