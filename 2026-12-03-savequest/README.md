# SaveQuest — ออมเงินแบบเกม เห็นกระปุกโต (AI วันละแอป · 2026-12-03)

ตั้งเป้าพร้อมรูปความฝัน → เห็นกระปุกโตตามเปอร์เซ็นต์ที่ออมได้ มีชาเลนจ์รายวัน แผน 52 สัปดาห์หรือสุ่มตัวเลข สตรีคต่อเนื่อง และการ์ดไมล์สโตนสำหรับแชร์

**EN:** Set a savings goal with a wish photo → watch a jar grow with every baht you save, play daily challenges, follow a 52-week or random-number plan, keep a streak and share milestone cards.

## ในแพ็ก / Pack contents
- `prd.md` — ปัญหา, must-have / nice-to-have (10 ฟีเจอร์), หน้าจอ, demo fixture, design tokens, guardrails, shot list Reel
- `prompts.md` — work-order prompts P0–P12 + AI vision/text prompts A1–A5
- `schemas.json` — JSON Schema 2020-12 (19 defs)
- `examples.json` — 106 ตัวอย่าง (ข้อมูลสมมติ) validate ผ่านหมด
- `reference/` — `savequest.py` logic deterministic (กระปุก 7 เป้า, ชาเลนจ์ 8 ข้อ, แผน 52 สัปดาห์/สุ่ม, สตรีค, ปัดเศษ, กระปุกร่วม), `fixtures.py` (น้องมิ้น + 2 คนสมมติ, 5 รูปเป้า), `tests.py` (41 tests), `build.py`
- `social/` — `make_cover.py`, ปก 1080×1350 / 1080×1080, `fb_post.md`

## รัน / Run
```
cd reference && python3 tests.py && python3 build.py   # ต้องมี jsonschema
```

## หมายเหตุ / Notes
- SaveQuest เป็น **เกมช่วยออมเงิน ไม่ใช่บัญชีธนาคาร ไม่ใช่คำแนะนำการลงทุน และไม่รับฝากเงินจริง**
- จำนวนเงิน แผน 52 สัปดาห์ (สัปดาห์ที่ n × ฐาน เช่น ฿100) และชาเลนจ์รายวันเป็น **ค่าตัวอย่างที่ตั้งเอง** ปรับได้ใน `GOALS` / `CHALLENGES`
- รูปเป้าใช้เป็นแรงบันดาลใจเท่านั้น ไม่ใช่ใบจองหรือราคาจริงของทัวร์/สินค้า
- ทุกตัวอย่างเป็นบุคคลสมมติ ภาพปกสร้างด้วย PIL เป็นภาพประกอบ ไม่ใช้รูปคนจริง
