# RipeRight — ถ่ายผลไม้ รู้เลยสุกพอดีไหม (AI วันละแอป · 2026-12-14)

ถ่ายรูปผลไม้ → AI อ่านสีผิวและจุดกระ → มิเตอร์ความสุก 0–100 บอกว่า ยังดิบ / ใกล้สุก / สุกพอดี / สุกเกิน + กินได้วันไหน → เคาะแตงโม/ทุเรียนให้ไมค์ฟังเสียง → เช็กราคาต่อกิโลว่าแพงไหม (รู้ว่าในหรือนอกฤดู) → วิธีเร่งสุก/ชะลอสุก → ตารางกินผลไม้ในตะกร้าทีละวัน → เช็กลิสต์เลือกลูกที่ตลาด → ปฏิทินผลไม้ตามฤดู → ไดอารี่ "ทายถูกไหม", การ์ดแชร์, โควตา, Safety Guard (ค่าประมาณ ไม่ใช่การรับรองความปลอดภัยอาหาร)

**EN:** Snap a fruit → AI reads skin colour and spots → a 0–100 ripeness meter (unripe / almost / perfect / overripe) and the day it's best to eat → knock test for watermelon and durian using the mic → THB-per-kg price check with in/off-season awareness → speed-up or slow-down storage tips → a day-by-day eating plan for your fruit basket → a 4-question market pick checklist → a Thai fruit season calendar, a "did we guess right?" diary, share card, daily quota and safety guard (estimates only, not a food-safety guarantee).

## ในแพ็ก / Pack contents
- `prd.md` — ปัญหา, must-have / nice-to-have (10 ฟีเจอร์), หน้าจอ, demo fixture, design tokens, Reel shot list, guardrails, metrics
- `prompts.md` — work-order prompts P0–P12 + AI prompts A1–A5
- `schemas.json` — JSON Schema 2020-12 (22 defs)
- `examples.json` — 135 ตัวอย่าง (ข้อมูลสมมติ) validate ผ่านหมด
- `reference/` — `riperight.py` logic deterministic (8 ผลไม้ไทย, 5 สัญญาณ สี/กระ/ความนิ่ม/กลิ่น/เสียงเคาะ), `fixtures.py` (พี่ต้อม + 3 คนสมมติ), `tests.py` (35 tests), `build.py`
- `social/` — `make_cover.py`, ปก 1080×1350 / 1080×1080, `fb_post.md`

## รัน / Run
```
cd reference && python3 tests.py && python3 build.py   # ต้องมี jsonschema
```

## หมายเหตุ / Notes
- คะแนนความสุกเป็น **ค่าประมาณ** จากสีในรูปและคำตอบของผู้ใช้ น้ำหนักสัญญาณต่อผลไม้อยู่ใน `FRUITS[...]["w"]` ปรับได้
- ช่วงราคาต่อกิโลและเดือนในฤดูเป็น **ค่าตัวอย่างที่ตั้งเอง** (ไม่ใช่ราคาตลาดจริง) ปรับใน `FRUITS[...]["price"]`, `season`, `OFF_SEASON_MULT`
- เห็นรา จุดฟู กลิ่นบูด หรือเนื้อเละผิดปกติ → **ห้ามกิน** แอปจะขึ้น Safety Guard ระดับ stop
- ทุกตัวอย่างเป็นบุคคลสมมติ ภาพปกสร้างด้วย PIL เป็นภาพประกอบ ไม่ใช้รูปคนจริงหรือแบรนด์จริง
