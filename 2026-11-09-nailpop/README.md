# NailPop — ลองสีเล็บก่อนทำ (AI วันละแอป · 2026-11-09)

ถ่ายมือ 1 รูป → AI ทาเล็บให้ 9 แบบบนเล็บจริงของคุณในไม่กี่วินาที. ถ่ายมือ → ตรวจเล็บ 5 นิ้ว + วัดทรง (เหลี่ยม/เหลี่ยมมน/กลม/วงรี/อัลมอนด์/บัลเลต์/สติเลตโต้) และความยาว → Try-On Grid 9 ลาย จัดอันดับด้วย Fit Score → เช็กโทนผิว อุ่น/เย็น/กลาง แนะนำสีที่ใช่และสีที่ควรเลี่ยง → Salon Card (ลาย + ทรง + ความยาว + ช่วงราคาประมาณ ฿ + โน้ตถึงช่าง ส่ง LINE ได้ทันที) → โหวตกับเพื่อน, Nail Diary + เตือนถอดเจล/เติมโคน, พรีเซ็ตเทศกาล (สงกรานต์ งานแต่ง ออฟฟิศ ลอยกระทง), โหมด DIY ทีละขั้น, Health Guard, การ์ดแชร์ Before/After

**EN:** One hand photo → AI paints 9 nail designs on your real nails in seconds. Nail detection with shape and length, a ranked 9-design Try-On Grid, skin undertone match with best and avoid shades, a Salon Card (design, shape, length, estimated THB price range and a note for your nail tech, shareable to LINE), friend vote, nail diary with gel removal/refill reminders, occasion presets, DIY step guide, nail health guard and a before/after share card.

## ในแพ็ก / Pack contents
- `prd.md` — ปัญหา, must-have / nice-to-have (10 ฟีเจอร์), หน้าจอ, demo fixture, design tokens, guardrails (ภาพเป็นภาพจำลอง ราคาเป็นช่วงประมาณ ไม่วินิจฉัยโรคเล็บ)
- `prompts.md` — work-order prompts P0–P12 + AI vision/render prompts A1–A5
- `schemas.json` — JSON Schema 2020-12 (26 defs)
- `examples.json` — 76 ตัวอย่าง (ข้อมูลสมมติ) validate ผ่านหมด
- `reference/` — `nailpop.py` logic deterministic, `fixtures.py` (มายด์ + 4 คนสมมติ, 14 ลายเล็บ), `tests.py` (35 tests), `build.py`
- `social/` — `make_cover.py`, ปก 1080×1350 / 1080×1080, `fb_post.md`
- `nailpop.zip` — ทั้งโฟลเดอร์ในไฟล์เดียว

## รัน / Run
```
cd reference && python3 tests.py && python3 build.py   # ต้องมี jsonschema
```

## หมายเหตุ / Notes
- ภาพ Try-On เป็น **ภาพจำลองจาก AI** สีจริงขึ้นกับยี่ห้อสี แสง และฝีมือช่าง — ทุกการ์ดมีลายน้ำบอกชัด
- ช่วงราคา (เจล ฿350–600 + ลาย ฿100–900, ตัวคูณพื้นที่) เป็น **ค่าประมาณการที่ตั้งเอง ไม่ใช่ราคาร้านจริง** ปรับได้ใน `BASE_PRICE` / `ART_PRICE` / `REGION_MULT`
- น้ำหนัก Fit Score (โทนผิว 35 · โอกาส 25 · ความยาว 15 · ทรง 10 · งบ 15), กติกาทรงเล็บ, ระยะเตือน (เจล เช็ก 14 / ถึงเวลา 21 / ควรถอดภายใน 28 วัน), โควตาฟรี 3 กริด/วัน เป็นค่าที่ตั้งเอง
- Health Guard เป็นแค่การเตือนให้พัก/ปรึกษาผู้เชี่ยวชาญ **ไม่ใช่การวินิจฉัย**
- ทุกตัวอย่างเป็นบุคคลสมมติ ภาพปกสร้างด้วย PIL เป็นภาพประกอบ ไม่ใช้มือ/ใบหน้าคนจริง
