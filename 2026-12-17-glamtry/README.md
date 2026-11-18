# GlamTry — เซลฟี่เดียว ลองแต่งหน้าก่อนซื้อ (AI วันละแอป · 2026-12-17)

เซลฟี่หน้าสด 1 รูป → Consent Guard เช็กว่าเป็นหน้าตัวเอง อายุ 13+ ไม่ใช่รูปดารา → AI สแกนเฉดผิวและอันเดอร์โทนโดยประมาณ (เช่น 2W ผิวขาวเหลือง อุ่น) → ได้ภาพจำลอง **6 ลุคเต็มหน้า** (เนเชอรัลหน้าสด / เกาหลีผิวฉ่ำ / เจ้าสาวไทย / ปาร์ตี้จัดเต็ม / สาวออฟฟิศ / Y2K) ปัดสไลเดอร์ดู ก่อน/หลัง ปรับความเข้ม 3 ระดับ → Shade Match แนะนำเฉดรองพื้นและสีลิปที่เข้ากับอันเดอร์โทน → การ์ดสอนแต่งทีละขั้นของลุคที่เลือก (มือใหม่ได้เวอร์ชันง่าย) → Budget Kit ชุดของ 3 ระดับราคา (ประหยัด/กลาง/ไฮเอนด์ ราคาประมาณ ไม่อ้างแบรนด์) ติ๊กของที่มีแล้วไม่ต้องซื้อซ้ำ → Occasion Planner วางแผนแต่งหน้าตามงาน + ไทม์ไลน์ patch test → Makeup Diary ลุคที่ชอบ ค่าใช้จ่าย และวันควรเปลี่ยนมาสคาร่า → การ์ดแชร์ / Reel ก่อน-หลัง, โควตา และ Safety Guard (ไม่ทำผิวขาว ไม่ดัดหน้า ไม่แต่งให้เหมือนดารา)

**EN:** One bare-face selfie → a Consent Guard (own photo only, 13+, no celebrity faces) → AI estimates your skin depth and undertone (e.g. 2W, light-warm) → **6 full makeup looks** rendered on your own face (Natural / Korean glass skin / Thai bride / Party glam / Office / Y2K) with a before/after slider and 3 intensity levels → Shade Match for foundation and lip colours that suit your undertone (labelled estimate) → step-by-step tutorial cards for the chosen look (simplified for beginners) → a Budget Kit in 3 price tiers (budget / mid / premium, estimated THB ranges, generic product types, no brand claims) that skips what you already own → an Occasion Planner with a patch-test timeline → a Makeup Diary (favourite looks, spend, when to replace mascara) → share card / before-after Reel maker, daily quota and a safety guard (no skin whitening, no face reshaping, no celebrity look-alikes).

## ในแพ็ก / Pack contents
- `prd.md` — ปัญหา, must-have / nice-to-have (10 ฟีเจอร์), หน้าจอ, demo fixture, design tokens, Reel shot list, build plan, risks, guardrails, metrics
- `prompts.md` — work-order prompts P0–P12 + AI prompts A1–A5
- `schemas.json` — JSON Schema 2020-12 (22 defs)
- `examples.json` — 139 ตัวอย่าง (ข้อมูลสมมติ) validate ผ่านหมด
- `reference/` — `glamtry.py` logic deterministic (6 ลุค, 5 ระดับสีผิว × 4 อันเดอร์โทน, 18 ประเภทเครื่องสำอาง × 3 ระดับราคา, 8 งาน), `fixtures.py` (น้องเฟิร์น + 3 คนสมมติ), `tests.py` (37 tests), `build.py`
- `social/` — `make_cover.py`, ปก 1080×1350 / 1080×1080, `fb_post.md`

## รัน / Run
```
cd reference && python3 tests.py && python3 build.py   # ต้องมี jsonschema
```

## หมายเหตุ / Notes
- ภาพลองแต่งหน้าเป็น **ภาพจำลอง** สีจริงต่างตามผิว แสง และผลิตภัณฑ์; เฉดผิว/โค้ดเฉด (`shade_match`) เป็น **ค่าประมาณจากรูป** ไม่ใช่การวัดจริง ควรทาเทสต์ที่กรอบหน้าใต้แสงธรรมชาติก่อนซื้อ
- ช่วงราคา (`ITEMS`) เป็น **ค่าตัวอย่างโดยประมาณที่ตั้งเอง** ของสินค้า "ประเภท" เดียวกัน ไม่ได้อ้างอิงหรือรับรองแบรนด์ใด
- เรื่อง patch test / แพ้ (`patch_test`) และอายุหลังเปิดใช้ (`pao`) เป็น **ข้อมูลทั่วไป ไม่ใช่คำแนะนำทางการแพทย์** ถ้าแพ้ให้หยุดใช้และปรึกษาแพทย์/เภสัชกร
- Consent Guard: ใช้ได้เฉพาะเซลฟี่ของตัวเอง, อายุต่ำกว่า 13 ปีถูกบล็อก, ไม่รองรับรูปดารา/การแต่งให้เหมือนใคร, ไม่ปรับผิวให้ขาวหรือดัดรูปหน้า
- ทุกตัวอย่างเป็นบุคคลสมมติ ภาพปกสร้างด้วย PIL เป็นภาพวาดประกอบ ไม่ใช้รูปคนจริง ดารา หรือแบรนด์จริง
