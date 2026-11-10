# LuckyHue — สีมงคลประจำวัน + วอลเปเปอร์สายมู (AI วันละแอป · 2026-11-27)

ใส่วันเกิด → ได้สีมงคลตามวันในสัปดาห์ ถ่ายรูปตู้เสื้อผ้าแล้วจับคู่ชุดกับสีนั้น ทำวอลเปเปอร์ และดูปฏิทินสีทั้งสัปดาห์ (เพื่อความสนุก ไม่ใช่หมอดู)

**EN:** Enter your birth day of week → get the folk lucky colour, mix an outfit from a closet photo, make a wallpaper and see a weekly colour calendar (for fun, not fortune-telling).

## ในแพ็ก / Pack contents
- `prd.md` — ปัญหา, must-have / nice-to-have (10 ฟีเจอร์), หน้าจอ, demo fixture, design tokens, guardrails, shot list Reel
- `prompts.md` — work-order prompts P0–P12 + AI vision/text prompts A1–A5
- `schemas.json` — JSON Schema 2020-12 (14 defs)
- `examples.json` — 86 ตัวอย่าง (ข้อมูลสมมติ) validate ผ่านหมด
- `reference/` — `luckyhue.py` logic deterministic (สีตามวัน, มิกซ์ชุดจากตู้, วอลเปเปอร์, ปฏิทินสัปดาห์, คำเตือนเพื่อความสนุก), `fixtures.py` (พี่เมย์เกิดวันศุกร์ + 2 คนสมมติ), `tests.py` (41 tests), `build.py`
- `social/` — `make_cover.py`, ปก 1080×1350 / 1080×1080, `fb_post.md`

## รัน / Run
```
cd reference && python3 tests.py && python3 build.py   # ต้องมี jsonschema
```

## หมายเหตุ / Notes
- LuckyHue เป็น **สีมงคลตามวันที่นิยมหาสนุก ไม่ใช่หมอดู ไม่ใช่โหราศาสตร์ และไม่รับประกันโชคชะตา**
- แมปสี (อา แดง / จ เหลือง / อ ชมพู / พ เขียว / พฤ ส้ม / ศ ฟ้า / ส ม่วง) เป็น **ชุดที่พบได้บ่อยในวัฒนธรรมประชานิยม** แหล่งที่มาอาจต่างกัน โดยเฉพาะวันพุธ (กลางวันเขียว / กลางคืนแสด)
- ตัวอย่างและภาพปกเป็นบุคคลสมมติ/ภาพวาด ไม่ใช้คนจริงหรือตู้เสื้อผ้าจริง
