# CakeDream — บอกธีม เห็นเค้กในฝัน สั่งร้านได้เลย (AI วันละแอป · 2026-12-11)

เล่าไอเดียเค้กเป็นคำพูด → AI แยกธีม รส ข้อความ สี → ภาพเค้กจำลอง 3 แบบ → คำนวณกี่ปอนด์จากจำนวนแขก → เช็กข้อความบนเค้กว่าพอที่ไหม → ช่วงราคา ฿ + เช็กราคาร้าน → Allergy Guard → นับถอยหลังวันสั่ง → Order Card ส่ง LINE ร้าน → โหมดอบเอง, ไดอารี่ปาร์ตี้, การ์ดแชร์, โควตา, Safety Guard (ภาพจำลอง ราคาประมาณ)

**EN:** Describe your dream cake → AI pulls out theme, flavour, message and colours → 3 mock-up images → servings calculator (pounds and inches from your guest list) → message-fits-the-cake check → THB price range and quote check → allergy guard → order-by countdown → bakery order card for LINE → DIY recipe mode, party diary, share card, daily quota and safety guard (mock-ups and prices are estimates).

## ในแพ็ก / Pack contents
- `prd.md` — ปัญหา, must-have / nice-to-have (10 ฟีเจอร์), หน้าจอ, demo fixture, design tokens, Reel shot list, guardrails, metrics
- `prompts.md` — work-order prompts P0–P12 + AI prompts A1–A5
- `schemas.json` — JSON Schema 2020-12 (22 defs)
- `examples.json` — 134 ตัวอย่าง (ข้อมูลสมมติ) validate ผ่านหมด
- `reference/` — `cakedream.py` logic deterministic (8 ธีม, 7 รส, 9 ขนาด ½–8 ปอนด์), `fixtures.py` (แม่ปุ๊ก + 3 คนสมมติ), `tests.py` (35 tests), `build.py`
- `social/` — `make_cover.py`, ปก 1080×1350 / 1080×1080, `fb_post.md`

## รัน / Run
```
cd reference && python3 tests.py && python3 build.py   # ต้องมี jsonschema
```

## หมายเหตุ / Notes
- ภาพเค้กเป็น **ภาพจำลอง** ร้านจริงอาจทำได้ต่างจากภาพ
- ราคา (฿420/ปอนด์ × ตัวคูณความซับซ้อน × พื้นที่ + ท็อปเปอร์ ฿80) และจำนวนชิ้นต่อปอนด์เป็น **ค่าตัวอย่างที่ตั้งเอง** ปรับได้ใน `SIZES` / `CX_MULT` / `REGION_MULT`
- Allergy Guard เป็นตัวช่วยเตือน **ไม่ใช่การรับประกัน** ต้องแจ้งร้านเรื่องแพ้อาหารและการปนเปื้อนทุกครั้ง
- ห้ามใช้โลโก้/ตัวละครลิขสิทธิ์บนเค้กสั่งขาย
- ทุกตัวอย่างเป็นบุคคลสมมติ ภาพปกสร้างด้วย PIL เป็นภาพประกอบ ไม่ใช้รูปคนจริงหรือแบรนด์จริง
