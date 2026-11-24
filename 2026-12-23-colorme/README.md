# ColorMe — รูปไหนก็ได้ กลายเป็นหน้าระบายสี (AI วันละแอป · 2026-12-23)

เลือกรูปในมือถือ (น้องหมาน้องแมว ของเล่น ที่เที่ยว อาหาร) → AI ช่วยเคลียร์พื้นหลังและบอกว่าในรูปมีอะไร → โค้ดแปลงเป็น **หน้าระบายสีเส้นคมชัด** ตามวัยของลูก (ตัวจิ๋ว 3–5 ขวบเส้นหนา ช่องใหญ่ ≤ 12 ช่อง · ประถมต้น · ประถมปลาย · ผู้ใหญ่ระบายคลายเครียด) โดย **ลดรายละเอียดอัตโนมัติ** จนจำนวนช่องเหมาะกับวัย → โหมด **ระบายตามเลข** (เลขอยู่กลางช่องเสมอ + ตารางสีชื่อไทยตรงกับสีเทียน 13 สีที่มีทุกร้านเครื่องเขียน) → **พิมพ์ A4 เป็นสมุดระบายสีมีชื่อลูกบนปก** (1–12 หน้า, โหมดประหยัดหมึก, หน้าเฉลย) → ลูกระบายเสร็จ **สแกนกลับ → Magic Reveal** ภาพก่อน/หลังคู่กัน + ดาว 1–3 ดวงแบบชมล้วน (ไม่มีสอบตก) → **หน้าลากเส้นต่อจุด** จากโครงร่างรูปเดียวกัน → **ภารกิจระบายประจำวัน** + สติกเกอร์สะสมวันต่อเนื่อง → **แกลเลอรีครอบครัว** ครบ 8 หน้าได้สมุดผลงานประจำเดือน → การ์ดแชร์ / Reel พร้อม Privacy & Safety Guard (ใช้รูปของเราเอง ประมวลผลบนเครื่อง ซ่อนหน้าเด็กในการ์ดแชร์ ไม่แปลงบัตร/เอกสาร เตือนตัวการ์ตูนลิขสิทธิ์ เตือนพักสายตา)

**EN:** Pick any photo on your phone (a pet, a toy, a trip, a favourite dish) → AI tidies the background and names the subject → code turns it into a **clean coloring page** matched to your child's age (thick lines and ≤ 12 big areas for 3–5s, up to detailed pages for adults), **auto-simplifying** until the number of areas suits the age → **colour-by-number** mode (numbers always sit deep inside each area, with a legend in the 13 crayon colours every stationery shop sells) → **print an A4 coloring book with the child's name on the cover** (1–12 pages, ink-saver mode, answer key) → when it's done, **scan it back for a Magic Reveal**: before/after side by side plus 1–3 stars that only praise (no fail) → a **dot-to-dot page** from the same outline → a **daily coloring quest** with streak stickers → a **family gallery** that becomes a monthly art book at 8 pages → share card / Reel, with a Privacy & Safety Guard (your own photos, processed on the device, children's faces hidden on share cards, no ID cards or documents, a copyright-character warning and a screen-break reminder).

## ในแพ็ก / Pack contents
- `prd.md` — ปัญหา, must-have / nice-to-have (10 ฟีเจอร์), หน้าจอ, demo fixture, design tokens, Reel shot list, build plan, risks / traps, guardrails, metrics
- `prompts.md` — work-order prompts P0–P12 + AI prompts A1–A5
- `schemas.json` — JSON Schema 2020-12 (23 defs)
- `examples.json` — 129 ตัวอย่าง (ข้อมูลสมมติ) validate ผ่านหมด
- `reference/` — `colorme.py` logic deterministic (ตัวเลือกพาเลตสีเทียน + ลบจุดฝุ่น, แบ่งช่อง 4-connected, รวมช่องเล็ก, ลดรายละเอียดตามวัย, เส้นขอบ, วางเลขกลางช่องด้วย distance transform, ต่อจุด, สมุด A4 + ประมาณหมึก, ตรวจผลงานแบบชมล้วน, ภารกิจ/สติกเกอร์, แกลเลอรี, guard), `fixtures.py` (รูปน้องแมวส้มจี๊ดสร้างด้วยโค้ด 24×30 + เด็กสมมติ 3 คน), `tests.py` (36 tests), `build.py`
- `social/` — `make_cover.py`, ปก 1080×1350 / 1080×1080, `fb_post.md`, `caption_fb.txt`

## รัน / Run
```
cd reference && python3 tests.py && python3 build.py   # ต้องมี jsonschema
```

## หมายเหตุ / Notes
- AI (vision/image model) ทำแค่ "ทำความสะอาดรูป + บอกว่ามีอะไร + ตรวจความปลอดภัย" ส่วนการแบ่งช่อง นับสี วางเลข ให้ดาว เป็นโค้ด deterministic ทดสอบได้ ผลเหมือนเดิมทุกครั้ง
- ใช้รูปที่ถ่ายเองหรือได้รับอนุญาต ประมวลผลบนเครื่องเป็นหลัก รูปต้นฉบับไม่ถูกอัปโหลด การ์ดแชร์ซ่อนหน้าเด็กเสมอ
- ไม่แปลงบัตรประชาชน สลิป เอกสาร รูปโป๊ หรือรูปรุนแรง; ตัวการ์ตูน/โลโก้ลิขสิทธิ์ระบายเล่นในบ้านได้ แต่ห้ามพิมพ์ขาย
- ให้ดาวแบบชมล้วน ขั้นต่ำ 1 ดาว ไม่มีการจัดอันดับเด็ก ไม่มีคำว่า "ผิด"; เด็กต่ำกว่า 3 ขวบให้ผู้ใหญ่เล่นด้วย (สีเทียนชิ้นเล็ก)
- ทุกตัวอย่างเป็นบุคคลสมมติ ภาพปกและรูปตัวอย่างสร้างด้วยโค้ดล้วน (แมวเป็นภาพกราฟิก ไม่ใช่รูปจริง) ไม่ใช้แบรนด์จริง
