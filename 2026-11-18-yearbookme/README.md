# YearbookMe — เซลฟี่เดียว กลายเป็นรูปรุ่นยุค 80s/90s/Y2K (AI วันละแอป · 2026-11-18)

ถ่ายเซลฟี่ 1 รูป → AI แปลงเป็นรูปรุ่น 3 ยุค (80s นีออน / 90s ฟิล์มปีบุ๊ก / Y2K แฟลชเมทัลลิก) ให้คะแนนความเข้าลุค 0–100 เลือกยุคที่เข้าสุด ใส่คำคมและลายเซ็นเพื่อน จัดหน้ารุ่นรวมกลุ่ม (ต้องยินยอมทุกคน) พิมพ์ A4 หรือแชร์การ์ดได้ ระบบ Consent Guard รับเฉพาะรูปของตนเอง ไม่ใช้รูปคนอื่นหรือบุคคลสาธารณะ

**EN:** One selfie → AI restyles it as a yearbook portrait in three eras (80s neon, 90s film yearbook, Y2K flash chrome), scores how well each look fits, writes captions and friend autographs, builds a group yearbook page (everyone must consent), and exports an A4 sheet or share card. Consent Guard: your own photo only — no other people's or celebrity photos.

## ในแพ็ก / Pack contents
- `prd.md` — ปัญหา, must-have / nice-to-have (10 ฟีเจอร์), หน้าจอ, demo fixture, design tokens, guardrails, shot list Reel
- `prompts.md` — work-order prompts P0–P12 + AI vision/text prompts A1–A5
- `schemas.json` — JSON Schema 2020-12 (20 defs)
- `examples.json` — 92 ตัวอย่าง (ข้อมูลสมมติ) validate ผ่านหมด
- `reference/` — `yearbookme.py` logic deterministic (3 ยุค, คำคม 4 โทน, Consent Guard), `fixtures.py` (น้องมายด์ + 4 คนสมมติ, 10 รูป), `tests.py` (41 tests), `build.py`
- `social/` — `make_cover.py`, ปก 1080×1350 / 1080×1080, `fb_post.md`
- `yearbookme.zip` — ทั้งโฟลเดอร์ในไฟล์เดียว

## รัน / Run
```
cd reference && python3 tests.py && python3 build.py   # ต้องมี jsonschema
```

## หมายเหตุ / Notes
- YearbookMe เป็น **สไตล์จำลองเพื่อความบันเทิง ไม่ใช่สมุดรุ่นทางการและไม่ใช่การยืนยันตัวตน**
- ใช้ได้เฉพาะรูปของตนเอง หรือรูปกลุ่มที่ทุกคนในภาพยินยอมแล้ว — ห้ามอัปโหลดรูปคนอื่นหรือบุคคลสาธารณะมาแปลง
- อายุต่ำกว่า 13 ปีใช้ไม่ได้ อายุ 13–17 ปีต้องมีผู้ปกครองยินยอม
- คะแนนความเข้าลุค สูตรสี เมล็ดฟิล์ม และคำคมเป็น **ค่าตัวอย่างที่ตั้งเอง** ปรับได้ใน `ERAS` / `QUOTE_BANK`
- ชื่อโรงเรียนในตัวอย่าง (Ficto University) และบุคคลทั้งหมดเป็นสมมติ ภาพปกสร้างด้วย PIL เป็นภาพประกอบ ไม่ใช้รูปคนจริง
