# SnapLingo — ถ่ายของรอบบ้าน ได้คำศัพท์อังกฤษ/จีนให้ลูก (AI วันละแอป · 2026-11-30)

ถ่ายของในบ้าน → ได้ป้ายคำศัพท์ไทย–อังกฤษ–จีน พร้อมวิธีอ่าน แฟลชการ์ด แบบทดสอบสั้น และรางวัลต่อเนื่องรายวัน (ถ่ายเฉพาะตัวของ ไม่ต้องมีใบหน้าเด็ก)

**EN:** Photograph household objects → Thai/English/Chinese labels with pronunciation, flashcards, a mini quiz and streak rewards (object photos only, no child face required).

## ในแพ็ก / Pack contents
- `prd.md` — ปัญหา, must-have / nice-to-have (10 ฟีเจอร์), หน้าจอ, demo fixture, design tokens, guardrails, shot list Reel
- `prompts.md` — work-order prompts P0–P12 + AI vision/text prompts A1–A5
- `schemas.json` — JSON Schema 2020-12 (17 defs)
- `examples.json` — 87 ตัวอย่าง (ข้อมูลสมมติ) validate ผ่านหมด
- `reference/` — `snaplingo.py` logic deterministic (อ่านของ, ป้ายคำศัพท์, แฟลชการ์ด, แบบทดสอบ, สตรีค/สติกเกอร์), `fixtures.py` (พี่แอน + น้องเต้าสมมติ, 5 รูปของ), `tests.py` (41 tests), `build.py`
- `social/` — `make_cover.py`, ปก 1080×1350 / 1080×1080, `fb_post.md`

## รัน / Run
```
cd reference && python3 tests.py && python3 build.py   # ต้องมี jsonschema
```

## หมายเหตุ / Notes
- SnapLingo เป็น **คลังคำศัพท์ตัวอย่างสำหรับเล่นกับของในบ้าน ไม่ใช่หลักสูตรโรงเรียน**
- การออกเสียงเป็นค่าตัวอย่าง แอปนี้ไม่ตรวจเสียงพูดจริง
- ถ่ายเฉพาะตัวของ ไม่ต้องมีใบหน้าเด็กในรูป ถ้ามีใบหน้าเด็กต้องได้รับความยินยอมจากผู้ปกครอง
- ตัวอย่างและภาพปกเป็นบุคคล/ของสมมติ ภาพวาด ไม่ใช้เด็กจริงหรือบ้านจริง
