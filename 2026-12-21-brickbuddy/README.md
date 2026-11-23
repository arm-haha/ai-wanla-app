# BrickBuddy — ถ่ายกองตัวต่อ รู้เลยต่ออะไรได้ (AI วันละแอป · 2026-12-21)

เทตัวต่อทั้งลังลงพื้น → ถ่ายรูป 1 รูป → AI นับชิ้นแยกตามรูปทรงและสี (**Pile Scan → Inventory**) → การ์ด **"ต่อได้ทันที"** 6 ไอเดียจากกองที่มีจริง (รถแข่ง เป็ด จรวด หุ่นยนต์ ต้นคริสต์มาส ป้ายปีใหม่ 2027 …) พร้อม % ความครบ และ **ชิ้นทดแทนอัตโนมัติ** (ไม่มี 1×4 ใช้ 1×2 สองชิ้นแทน) → **คู่มือทีละขั้นด้วยสีของเราเอง** วางฐาน → ก่ออิฐ → หลังคา → รายละเอียด → **Find-It** ไฮไลต์ว่าชิ้นที่ต้องใช้อยู่ช่องไหนในรูปกอง (A1–F4) → ช่วยแยกเก็บลงกล่องตามสี/ขนาด → เช็กตึกจะล้มไหม → ชาเลนจ์ประจำวัน (ช่วงปีใหม่เป็นธีม "ของขวัญปีใหม่") → ให้ดาวผลงานแบบใจดีกับเด็ก → ไดอารี่ สตรีค แบดจ์ → การ์ดแชร์ / Reel พร้อม Age & Safety Guard (ชิ้นเล็กไม่เหมาะเด็กต่ำกว่า 3 ปี, เจอถ่านกระดุม/แม่เหล็กในกอง = หยุด)

**EN:** Dump the whole box of bricks on the floor → snap one photo → AI counts every piece by shape and colour (**Pile Scan → Inventory**) → **"Build it now"** cards with 6 ideas from the pieces you actually own (race car, duck, rocket, robot, Christmas tree, a "2027" New Year sign…) with a match % and **automatic substitutions** (no 1×4? use two 1×2) → **step-by-step instructions in your own colours** (base → walls → roof → details) → **Find-It** highlights where each needed piece sits in the pile photo (grid A1–F4) → a sort helper for storage boxes by colour or size → a "will it fall?" stability check → a daily build challenge (New Year gift theme over the holidays) → a kind, kid-friendly star score → a build diary with streaks and badges → share card / Reel maker, with an Age & Safety Guard (small parts are not for under-3s; button batteries or magnets in the pile = stop).

## ในแพ็ก / Pack contents
- `prd.md` — ปัญหา, must-have / nice-to-have (10 ฟีเจอร์), หน้าจอ, demo fixture, design tokens, Reel shot list, build plan, risks / traps, guardrails, metrics
- `prompts.md` — work-order prompts P0–P12 + AI prompts A1–A5
- `schemas.json` — JSON Schema 2020-12 (26 defs)
- `examples.json` — 147 ตัวอย่าง (ข้อมูลสมมติ) validate ผ่านหมด
- `reference/` — `brickbuddy.py` logic deterministic (14 ชนิดชิ้น × 12 สี, 14 ไอเดียต่อ, กฎชิ้นทดแทน, คู่มือทีละชั้น, Find-It กริด, แยกกล่อง, เช็กความมั่นคง, ชาเลนจ์, ให้ดาว), `fixtures.py` (น้องภูมิ 7 ขวบ + 3 คนสมมติ), `tests.py` (36 tests), `build.py`
- `social/` — `make_cover.py`, ปก 1080×1350 / 1080×1080, `fb_post.md`, `caption_fb.txt`

## รัน / Run
```
cd reference && python3 tests.py && python3 build.py   # ต้องมี jsonschema
```

## หมายเหตุ / Notes
- ใช้ได้กับตัวต่อปุ่ม (stud bricks) ทุกยี่ห้อที่ต่อเข้ากันได้ แอปนี้ **ไม่เกี่ยวข้องกับแบรนด์ใด** และ **ไม่คัดลอกคู่มือชุดลิขสิทธิ์** — ไอเดียทั้งหมดเป็นแบบต้นฉบับที่สร้างจากกองของผู้ใช้
- จำนวนชิ้นจากรูปเป็น **ค่าประมาณ** (ชิ้นที่ AI ไม่มั่นใจ < 0.5 จะไม่ถูกนับ และให้ผู้ใช้แตะแก้ได้)
- ตัวต่อชิ้นเล็กเสี่ยงติดคอ **ไม่เหมาะกับเด็กต่ำกว่า 3 ปี**; เด็กต่ำกว่า 13 ปีให้ผู้ปกครองเปิดกล้อง; ใบหน้าคนในรูปถูกเบลอก่อนส่ง AI
- คะแนนดาวเป็นเกมให้กำลังใจ ได้อย่างน้อย 1 ดาวเสมอ ไม่มีคำติ
- ทุกตัวอย่างเป็นบุคคลสมมติ ภาพปกสร้างด้วย PIL ล้วน ไม่ใช้รูปคนจริงหรือแบรนด์จริง
