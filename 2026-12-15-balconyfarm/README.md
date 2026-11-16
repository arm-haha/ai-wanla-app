# BalconyFarm — ถ่ายระเบียง เห็นสวนผักก่อนปลูก (AI วันละแอป · 2026-12-15)

ถ่ายระเบียงคอนโด/บ้าน 1 รูป + หันมือถือบอกทิศ → AI ประเมินแดดกี่ชั่วโมง/วัน (แดดเต็ม / ครึ่งแดด / ร่มรำไร) → แนะนำผักสวนครัวที่ปลูกรอดจริง (12 ชนิด กะเพรา โหระพา ต้นหอม ผักชี พริก ฯลฯ ตามแดดและฤดู) → ภาพจำลองระเบียงกลายเป็นสวนผัก 3 สไตล์ → ผังวางกระถาง + เช็กน้ำหนักต่อตารางเมตร → ตารางรดน้ำรายวัน → นับถอยหลังวันเก็บ + เงินที่ประหยัด → ลิสต์ซื้อของพร้อมงบและคืนทุน → ไดอารี่สวน, การ์ดแชร์, โควตา, Safety Guard (ค่าประมาณ ห้ามวางกระถางบน/นอกราว)

**EN:** Snap your balcony and point the phone to set its facing → AI estimates direct-sun hours (full sun / partial / shade) → picks Thai kitchen plants that will actually survive (12 herbs and veg, by light and season) → a mock-up of your balcony turned into a garden in 3 styles → a pot layout with a load-per-m² check → a daily watering plan → harvest countdown and money saved → a shopping list with budget and payback → garden diary, share card, daily quota and safety guard (estimates; never put pots on or outside the railing).

## ในแพ็ก / Pack contents
- `prd.md` — ปัญหา, must-have / nice-to-have (10 ฟีเจอร์), หน้าจอ, demo fixture, design tokens, Reel shot list, guardrails, metrics
- `prompts.md` — work-order prompts P0–P12 + AI prompts A1–A5
- `schemas.json` — JSON Schema 2020-12 (23 defs)
- `examples.json` — 124 ตัวอย่าง (ข้อมูลสมมติ) validate ผ่านหมด
- `reference/` — `balconyfarm.py` logic deterministic (8 ทิศ, 12 พืชสวนครัว, 3 ฤดู), `fixtures.py` (พี่เก่ง + 3 คนสมมติ), `tests.py` (31 tests), `build.py`
- `social/` — `make_cover.py`, ปก 1080×1350 / 1080×1080, `fb_post.md`

## รัน / Run
```
cd reference && python3 tests.py && python3 build.py   # ต้องมี jsonschema
```

## หมายเหตุ / Notes
- ชั่วโมงแดดต่อทิศ (`FACING`), ข้อมูลพืช (`PLANTS`), ราคาดิน/กระถาง และเงินที่ประหยัดเป็น **ค่าตัวอย่างที่ตั้งเอง** ปรับได้
- ค่าน้ำหนักแนะนำ `LOAD_LIMIT_KG_M2 = 150` เป็น **ค่าตัวอย่างแบบระมัดระวัง** ไม่ใช่ค่าทางวิศวกรรมของอาคารคุณ ถามนิติบุคคล/ผู้ออกแบบอาคารเสมอ
- ห้ามแขวน/วางกระถางบนหรือนอกราวระเบียง และทำตามกฎคอนโด
- ทุกตัวอย่างเป็นบุคคลสมมติ ภาพปกสร้างด้วย PIL เป็นภาพประกอบ ไม่ใช้รูปคนจริงหรือแบรนด์จริง
