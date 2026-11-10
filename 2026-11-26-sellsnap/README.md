# SellSnap — ถ่ายของมือสอง ได้โพสต์ขายพร้อมราคา (AI วันละแอป · 2026-11-26)

ถ่ายของมือสองรูปเดียว → AI ตั้งชื่อโพสต์ เขียนคำบรรยาย ประเมินสภาพ A–E แนะนำช่วงราคาเป็นบาท ให้คำแนะนำถ่ายรูป และมีข้อความตอบคนทัก (ต่อราคา นัดรับ ขายแล้ว กันมิจฉาชีพ) พร้อมบันทึกของที่ขายแล้ว

**EN:** One photo of a second-hand item → a listing title and description, condition grade A–E, a THB price range, photo tips, buyer-reply templates (bargain, meetup, sold, scam-guard) and a sold log.

## ในแพ็ก / Pack contents
- `prd.md` — ปัญหา, must-have / nice-to-have (10 ฟีเจอร์), หน้าจอ, demo fixture, design tokens, guardrails, shot list Reel
- `prompts.md` — work-order prompts P0–P12 + AI vision/text prompts A1–A5
- `schemas.json` — JSON Schema 2020-12 (16 defs)
- `examples.json` — 89 ตัวอย่าง (ข้อมูลสมมติ) validate ผ่านหมด
- `reference/` — `sellsnap.py` logic deterministic (อ่านสินค้า, เกรดสภาพ, ช่วงราคาตัวอย่าง, โพสต์, ทิปถ่ายรูป, เทมเพลตตอบ, สมุดขาย), `fixtures.py` (พี่บอส + 2 คนสมมติ, 7 รูป), `tests.py` (41 tests), `build.py`
- `social/` — `make_cover.py`, ปก 1080×1350 / 1080×1080, `fb_post.md`

## รัน / Run
```
cd reference && python3 tests.py && python3 build.py   # ต้องมี jsonschema
```

## หมายเหตุ / Notes
- SellSnap เป็น **ตัวช่วยเขียนโพสต์ ไม่ใช่ตลาดกลางและไม่ใช่ราคาตลาดจริง**
- ช่วงราคา (เช่น โคมไฟสภาพดี ฿450–750) เป็น **ค่าตัวอย่างที่ตั้งเอง** ใน `PRICES`
- นัดรับในที่สาธารณะ อย่าโอนเงินให้คนแปลกหน้า ตรวจของก่อนส่งมอบ
- ตัวอย่างและภาพปกเป็นบุคคล/สินค้าสมมติ ภาพวาด ไม่ใช้รูปของจริงหรือคนจริง
