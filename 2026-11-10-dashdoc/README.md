# DashDoc — ไฟโชว์หน้าปัด ขับต่อได้ไหม (AI วันละแอป · 2026-11-10)

ถ่ายรูปหน้าปัด 1 รูป → AI อ่านไฟเตือนทุกดวง บอกความเร่งด่วนแบบสัญญาณไฟจราจรและตอบ "ขับต่อได้ไหม" ภาษาคน ถ่ายหน้าปัด → Light Scan + Urgency Meter (แดง จอดเดี๋ยวนี้ / เหลือง ขับต่อได้ ~X กม. ไปอู่ / เขียว-ฟ้า ข้อมูลเฉย ๆ) → Do-This-Now ขั้นตอนทำทันที → Fair Price Check ช่วงราคาซ่อม ฿ + คำถามที่ควรถามช่าง → Mechanic Card ส่งอู่ทาง LINE → Car Diary เตือนเช็กระยะตามกม./วัน (น้ำมันเครื่อง ยาง แบต พ.ร.บ. ภาษี) → Emergency Kit เบอร์ฉุกเฉิน + วิธีเปลี่ยนยาง จั๊มสตาร์ท เครื่องร้อน, การ์ดแชร์ผลสแกน, Safety Guard

**EN:** One dashboard photo → AI reads every warning light, rates urgency as a traffic light and answers "can I keep driving?" in plain Thai. Light Scan + Urgency Meter, Do-This-Now steps, Fair Price Check (THB ranges + questions for the mechanic), a Mechanic Card for LINE, a Car Diary with km/date reminders, an Emergency Kit with roadside guides, a share card and a safety guard.

## ในแพ็ก / Pack contents
- `prd.md` — ปัญหา, must-have / nice-to-have (10 ฟีเจอร์), หน้าจอ, demo fixture, design tokens, guardrails (คำแนะนำเบื้องต้น ไม่ใช่ช่าง ราคาเป็นช่วงประมาณ ไฟแดง = จอด)
- `prompts.md` — work-order prompts P0–P12 + AI vision/text prompts A1–A5
- `schemas.json` — JSON Schema 2020-12 (24 defs)
- `examples.json` — 98 ตัวอย่าง (ข้อมูลสมมติ) validate ผ่านหมด
- `reference/` — `dashdoc.py` logic deterministic (17 ไฟเตือน, 16 รายการซ่อม), `fixtures.py` (พี่โอ๊ต + 4 คนสมมติ, 8 รูปหน้าปัด), `tests.py` (41 tests), `build.py`
- `social/` — `make_cover.py`, ปก 1080×1350 / 1080×1080, `fb_post.md`
- `dashdoc.zip` — ทั้งโฟลเดอร์ในไฟล์เดียว

## รัน / Run
```
cd reference && python3 tests.py && python3 build.py   # ต้องมี jsonschema
```

## หมายเหตุ / Notes
- DashDoc เป็น **คำแนะนำเบื้องต้น ไม่ใช่ช่างและไม่ใช่การวินิจฉัยจริง** — ไฟสีแดงหรืออาการรุนแรง (ควัน กลิ่นไหม้ เบรกนิ่ม เครื่องร้อน) = จอดในที่ปลอดภัยทันที
- ระยะขับต่อ (กม./วัน/ความเร็วสูงสุด) ต่อไฟแต่ละดวง และกติกา escalate (เช็กเครื่องกะพริบ, สีแดงจริงบนไฟเหลือง, อาการรุนแรง) เป็น **ค่าตัวอย่างที่ตั้งเอง** ต้องให้ช่างจริงรีวิวก่อนปล่อยใช้
- ช่วงราคาซ่อม (฿ ตามรายการ × ตัวคูณพื้นที่ × ตัวคูณประเภทรถ) เป็น **ค่าประมาณการ ไม่ใช่ราคาอู่จริง** ปรับได้ใน `FIXES` / `REGION_MULT` / `CAR_CLASSES`
- ระยะเช็ก (น้ำมันเครื่อง 10,000 กม./6 เดือน ฯลฯ) ต้องตามคู่มือรถแต่ละรุ่น; เบอร์ฉุกเฉินสาธารณะ (191/1193/1669) ให้ตรวจกับแหล่งทางการก่อนใช้ ส่วนเบอร์ประกัน/รถยก/อู่เป็น placeholder ให้ผู้ใช้กรอก
- ทุกตัวอย่างเป็นบุคคลและรถสมมติ ภาพปกสร้างด้วย PIL เป็นภาพประกอบ ไม่ใช้รูปคนหรือรถจริง
