# GiftGenie — คิดของขวัญไม่ออก ตอบ 5 ข้อได้ไอเดียตามงบ (AI วันละแอป · 2026-11-20)

ตอบ 5 ข้อ (ความสัมพันธ์ ช่วงอายุ โทน ของที่ชอบ โอกาส) + งบเป็นบาท → ได้ไอเดียของขวัญเรียงตามคะแนนความเหมาะ พร้อมข้อความการ์ด 4 โทน ปฏิทินเตือนวันสำคัญ และไอเดียห่อของตามงบ มีระบบกันของไม่เหมาะกับเด็ก (เช่น แอลกอฮอล์)

**EN:** Answer five questions (relationship, age band, vibe, hobbies, occasion) plus a THB budget → ranked gift ideas with a fit score, card messages in four tones, an occasion calendar and wrapping ideas. Adult-only items are blocked for minors.

## ในแพ็ก / Pack contents
- `prd.md` — ปัญหา, must-have / nice-to-have (10 ฟีเจอร์), หน้าจอ, demo fixture, design tokens, guardrails, shot list Reel
- `prompts.md` — work-order prompts P0–P12 + AI text prompts A1–A5
- `schemas.json` — JSON Schema 2020-12 (14 defs)
- `examples.json` — 94 ตัวอย่าง (ข้อมูลสมมติ) validate ผ่านหมด
- `reference/` — `giftgenie.py` logic deterministic (คลังของ 16 ชิ้น, ควิซ 5 ข้อ, การ์ด 4 โทน, ปฏิทิน), `fixtures.py` (พี่บิ๋ม + 3 คนสมมติ), `tests.py` (41 tests), `build.py`
- `social/` — `make_cover.py`, ปก 1080×1350 / 1080×1080, `fb_post.md`
- `giftgenie.zip` — ทั้งโฟลเดอร์ในไฟล์เดียว

## รัน / Run
```
cd reference && python3 tests.py && python3 build.py   # ต้องมี jsonschema
```

## หมายเหตุ / Notes
- GiftGenie เป็น **ไอเดียของขวัญเบื้องต้น ไม่ใช่ร้านค้าและไม่ใช่คูปองจริง**
- ราคาเป็นช่วงประมาณการที่ตั้งเองใน `GIFTS` ไม่ใช่ราคาร้านจริง ชื่อสินค้า (FictoSoft, FictoBean ฯลฯ) เป็นสมมติ
- ของที่มีแอลกอฮอล์หรือทำเครื่องหมาย `adult_only` จะไม่ถูกเสนอให้ผู้รับที่เป็นเด็ก (ช่วงอายุ 0–12 และ 13–17)
- ข้อความการ์ดเป็นแม่แบบตัวอย่าง ปรับโทนได้ใน `CARD_BANK`
- บุคคลในตัวอย่างเป็นสมมติทั้งหมด ภาพปกสร้างด้วย PIL เป็นภาพประกอบ ไม่ใช้รูปคนจริง
