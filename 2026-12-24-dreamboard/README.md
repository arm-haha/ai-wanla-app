# DreamBoard — เป้าปีใหม่ กลายเป็นวอลล์ที่พาไปถึงจริง (AI วันละแอป · 2026-12-24)

พิมพ์เป้าหมายปีใหม่แบบบ่น ๆ ภาษาไทย ("ปีหน้าอยากเก็บเงินไปญี่ปุ่นสัก 6 หมื่น", "อยากผอมจาก 68 เหลือ 62") → AI แปลงเป็น **เป้าที่ชัด วัดผลได้** → โค้ดตรวจ **SMART 5 ข้อ** (มีตัวเลข · มีหน่วย · ทำได้จริงตามเวลา/รายได้ · มีหมวด · มีวันจบ) และ **กันเป้าอันตราย** (ลดน้ำหนัก > 1 กก./สัปดาห์ → ปรับแผนให้ปลอดภัยอัตโนมัติ, ออมเกินครึ่งของรายได้ → เตือน) → **แผน 12 เดือนแบบค่อย ๆ เร่ง** (เดือนแรกเบา ๆ ไม่ท้อตั้งแต่ ม.ค.) → **ก้าวเล็ก ๆ ประจำสัปดาห์** ("เก็บสัปดาห์ละ 1,150 บาท วันละ ~165 บาท", "อ่านวันละ ~17 หน้า") → ⭐ **บอร์ดเป้าหมายเป็นวอลเปเปอร์ล็อกสกรีน** 6 ธีม (แสงแรกปีใหม่ · คืนเคานต์ดาวน์ · ทองมงคล · พาสเทล · ป่าเขียว · มินิมอล) จัดการ์ดเป้าไม่ให้ทับนาฬิกา/ปุ่มกล้อง ทั้ง iPhone, Android และเดสก์ท็อป + **คำประจำปี** → **เช็กอินรายสัปดาห์** + สตรีค (สัปดาห์ที่แล้วยังนับ) + เหรียญ 4/12/26/52 สัปดาห์ → **บอร์ดยิ่งทำยิ่งสว่าง** (การ์ดเรืองแสง 0–5 ระดับตาม % ที่ทำได้ สถานะ นำแผน / ตรงแผน / ช้ากว่าแผน แบบไม่ด่า) → **ทบทวนครึ่งปี / สรุปปี** → **การ์ดสัญญากับเพื่อน** (ซ่อนตัวเลขเงิน/น้ำหนักอัตโนมัติ) → นับถอยหลังปีใหม่ + การ์ดแชร์ / Reel พร้อม Safety Guard (ไม่ให้คำแนะนำการลงทุน, เป้าหวย/พนัน/ขึ้นกับคนอื่น → ชวนเปลี่ยนเป็นสิ่งที่เราคุมได้, สัญญาณทำร้ายตัวเอง → สายด่วน 1323, อายุ < 13 ให้ผู้ปกครองช่วย)

**EN:** Type your New Year goals the way you'd say them ("save about 60k for Japan next year", "get from 68 to 62 kg") → AI turns them into **clear, measurable goals** → code runs a **5-point SMART check** (a number · a unit · achievable for the time and income · a category · an end date) and **blocks unsafe goals** (weight loss over 1 kg/week is re-planned at a safe pace automatically, saving more than half your income gets a warning) → a **12-month roadmap that ramps up gently** (an easy January so you don't quit early) → **one tiny weekly step** ("save 1,150 THB a week, about 165 a day", "read ~17 pages a day") → ⭐ a **vision-board lock-screen wallpaper** in 6 themes (New Year sunrise · countdown night · Thai gold · pastel · forest · minimal) with goal tiles kept clear of the clock and camera buttons on iPhone, Android and desktop, plus a **word of the year** → **weekly check-ins** with streaks (last week still counts) and 4/12/26/52-week badges → **the board lights up as you progress** (each tile glows 0–5 by % done; ahead / on track / a little behind, never shaming) → **mid-year and year-end review** → a **buddy pact card** (money and weight numbers hidden automatically) → a New Year countdown and share card / Reel, with a Safety Guard (no investment advice; lottery, gambling or other-person goals are nudged toward things you control; self-harm signals show the 1323 hotline; under-13s set goals with a parent).

## ในแพ็ก / Pack contents
- `prd.md` — ปัญหา, must-have / nice-to-have (10 ฟีเจอร์), หน้าจอ, demo fixture, design tokens, Reel shot list, build plan, risks / traps, guardrails, metrics
- `prompts.md` — work-order prompts P0–P12 + AI prompts A1–A5
- `schemas.json` — JSON Schema 2020-12 (28 defs)
- `examples.json` — 178 ตัวอย่าง (ข้อมูลสมมติ) validate ผ่านหมด
- `reference/` — `dreamboard.py` logic deterministic (SMART check, เพดานความปลอดภัยลดน้ำหนัก/ออมเงิน, safe re-plan, แผน 12 เดือนแบบ ramp, ก้าวรายสัปดาห์, จัดการ์ดบนล็อกสกรีนตาม safe zone, คำประจำปี, นับถอยหลัง, สตรีครายสัปดาห์ + เหรียญ, ความคืบหน้าเทียบแผน, ระดับเรืองแสงของบอร์ด, ทบทวนครึ่งปี/สรุปปี, การ์ดเพื่อน, quota, guard), `fixtures.py` (คุณมิ้นท์ 28 ปี กับเป้าปี 2570 ห้าข้อ + เป้าแย่ 3 แบบ), `tests.py` (37 tests), `build.py`
- `social/` — `make_cover.py`, ปก 1080×1350 / 1080×1080, `fb_post.md`, `caption_fb.txt`

## รัน / Run
```
cd reference && python3 tests.py && python3 build.py   # ต้องมี jsonschema
```

## หมายเหตุ / Notes
- AI ทำแค่ "แปลงข้อความเป็นร่างเป้า + วาดพื้นหลังการ์ด + เขียนข้อความให้กำลังใจ" ส่วนตัวเลข แผน ขีดจำกัดความปลอดภัย การจัดวาง และสถานะ เป็นโค้ด deterministic ทดสอบได้ ผลเหมือนเดิมทุกครั้ง
- ข้อมูลเป้าและบันทึกเก็บบนเครื่อง การ์ดแชร์ซ่อนตัวเลขเงิน/น้ำหนักเป็นค่าเริ่มต้น รูปบนบอร์ดต้องเป็นรูปของเราหรือได้รับอนุญาต (เบลอหน้าคนอื่นในการ์ดแชร์)
- ไม่ใช่คำแนะนำทางการเงิน การลงทุน หรือการแพทย์; เป้าลดน้ำหนักถูกจำกัดที่ ≤ 1 กก./สัปดาห์ (แนะนำ 0.5) ผู้มีโรคประจำตัวควรปรึกษาแพทย์
- ข้อความทุกแบบเป็นเชิงบวก ไม่ประจาน ไม่จัดอันดับ ไม่มีคำว่า "ล้มเหลว"
- ทุกตัวอย่างเป็นบุคคลสมมติ ภาพปกสร้างด้วยโค้ดล้วน ไม่ใช้รูปคนจริงหรือแบรนด์จริง
