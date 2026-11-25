# Work-order prompts — DreamBoard

> ให้ AI codegen (Cursor / Claude / v0 / Lovable ฯลฯ) ทำทีละ prompt ตามลำดับ ใช้ `schemas.json` เป็นสัญญาข้อมูล และ `reference/dreamboard.py` เป็นตรรกะต้นแบบ (port เป็น TypeScript ให้ผลเท่ากับ `tests.py`)

**P0 — Scaffold**: สร้าง PWA (Next.js หรือ Vite + React + Tailwind) มือถือก่อน ภาษาไทยเป็นหลัก สลับ EN ได้ ใช้ design tokens ใน prd.md (ม่วง #2A1850 ส้ม #FF9A62 ทอง #FFC440 ชมพู #FF6B8B, Kanit + Sarabun + Mali) port `dreamboard.py` → `src/logic/dreamboard.ts` พร้อม unit test เทียบ `tests.py` ทั้ง 37 ข้อ (fixture คุณมิ้นท์จาก `fixtures.py`) เก็บข้อมูลใน IndexedDB บนเครื่อง

**P1 — Profile**: ชื่อเล่น, อายุ (< 13 → `privacy_check(age=…)` ขอ parent mode), รายได้ต่อเดือน (ไม่บังคับ ใช้เช็กเป้าออม), ตัวเลือก "ซ่อนตัวเลขเงิน/น้ำหนักในการ์ดแชร์" เปิดไว้เป็นค่าเริ่มต้น. Output `User`.

**P2 — Write goals (A1)**: ช่องพิมพ์/ปุ่มไมค์ (Web Speech API th-TH) ทีละเป้า สูงสุด 6 → ส่ง `GoalText` ให้ A1 → `AiGoalParse` → แสดงการ์ดเป้าให้แก้ตัวเลข/หน่วย/วันจบได้ → สร้าง `Goal` (start = 1 ม.ค. ปีหน้าถ้าวันนี้อยู่ใน ธ.ค.) → `privacy_check(flags)`; stop → ข้อความไทยจาก `GUARD` ไม่บันทึกเป้า. Output `Goal`, `AiGoalParse`.

**P3 — SMART & safe re-plan**: `smart_check(goal, income)` → แถบ 5 ช่อง S-M-A-R-T + คะแนน + tips; `flag == "extreme_diet"` → ปุ่ม "ปรับให้ปลอดภัย" → `safe_replan()` แสดงวันจบใหม่; achievable=false → ปุ่ม "ลดตัวเลข/ยืดเวลา" แบบสไลเดอร์ที่คำนวณใหม่ทันที. Output `SmartCheck`.

**P4 — Roadmap & weekly step**: `roadmap(goal)` → กราฟขั้นบันได 12 เดือน (เดือนนี้ไฮไลต์) + `weekly_habit(goal)` เป็นการ์ด "สัปดาห์นี้แค่…" บนหน้า Home. Output `Roadmap`, `Milestone`, `WeeklyHabit`.

**P5 — Board builder**: เลือกธีม (`THEMES`) + อุปกรณ์ (เดาจาก user agent: iphone/android/desktop) → `layout(goals, theme, device)` → canvas ขนาดจริง: พื้นหลังไล่สีตามธีม, การ์ดตาม `tiles[]` (x,y,w,h) มุมโค้ง 22 px, ไอคอนหมวด, ชื่อเป้าภาษาไทย (ตัดคำด้วย Intl.Segmenter th), ring %, แถบ progress, `word_of_year()` ใต้นาฬิกา; ห้ามวาดอะไรใน safe zone. แอนิเมชัน "การ์ดบินเข้าที่" + พลุ (wow). Output `BoardLayout`, `Tile`, `WordOfYear`.

**P6 — Tile art (A2) & export**: ต่อการ์ด ขอ A2 วาดพื้นหลังนามธรรมตามหมวด (ไม่มีตัวอักษร ไม่มีหน้าคน ไม่มีโลโก้) หรือใช้ gradient สำรองถ้าออฟไลน์; ส่งออก PNG ความละเอียดอุปกรณ์ + หน้าวิธีตั้งเป็นล็อกสกรีน (iOS Shortcuts / Android set wallpaper intent). อัปโหลดรูปตัวเองได้ 1 รูปต่อการ์ด → `privacy_check(["photo_of_others"])` ถ้าตรวจพบคนอื่น.

**P7 — Weekly check-in**: แจ้งเตือนวันอาทิตย์ 19:00 (Notification API) → ใส่ตัวเลขที่ทำได้ต่อเป้า → `LogEntry` → `streak(checkins, today)` + เหรียญใหม่ (confetti). Output `LogEntry`, `Streak`.

**P8 — Progress & glow**: `progress(goal, logs, today)` ต่อเป้า → สถานะ + ข้อความ (A4 เขียนต่อได้ 1 บรรทัด) → `board_glow(progs)` → render วอลล์ใหม่ที่การ์ดเรืองแสงตาม `glow` (0 = โปร่ง, 5 = เรืองเต็ม) + ปุ่ม "อัปเดตวอลล์เดือนนี้". Output `Progress`, `BoardGlow`.

**P9 — Review & buddy**: 30 มิ.ย. และ 31 ธ.ค. → `review(goals, progs, period)` + A5 เขียนสรุป → การ์ด 1080×1350; `buddy_card(owner, buddy, goals, private)` แชร์ลิงก์ให้เพื่อนเช็กอินด้วยกัน (ข้อมูลเพื่อนอยู่เครื่องเพื่อน แลกแค่สถานะ % ถ้ายินยอม). Output `Review`, `BuddyCard`.

**P10 — Share / Reel**: `share_card(kind)` 3 แบบ ซ่อนตัวเลขเงิน/น้ำหนักเป็นค่าเริ่มต้น เบลอหน้าคนอื่น ลายน้ำ "DreamBoard · AI วันละแอป"; `reel_plan()` → canvas 1080×1920 7 ช็อต 100 BPM → MediaRecorder; `countdown(today)` บนหน้า Home ช่วง ธ.ค. Output `ShareCard`, `ReelPlan`, `Countdown`.

**P11 — Quota / Guard**: `quota()` ฟรี 3 บอร์ด/วัน; `safety_guard()` ทุก flag; ถ้า A1 ตรวจพบ `self_harm` ให้หยุด flow แสดงสายด่วน 1323 ทันทีและไม่บันทึกข้อความ; ไม่มีปุ่มหรือข้อความแนะนำการลงทุนใด ๆ.

**P12 — QA**: รัน `reference/tests.py` (37 tests) และ validate output ทุกตัวกับ `schemas.json`; ทดสอบเป้าคลุมเครือ ("อยากรวย"), ลด 10 กก. ใน 1 เดือน (ต้องปรับแผน), ออมเกินรายได้, หวย (warn), ข้อความเศร้า/ทำร้ายตัวเอง (stop + 1323), 1–6 การ์ดบน iPhone/Android/เดสก์ท็อป (ไม่ทับนาฬิกา), ชื่อเป้าภาษาไทยยาว ๆ (ตัดบรรทัดถูก), เช็กอินขาด 1 อาทิตย์ (สตรีครีเซ็ตแบบไม่ด่า).

## AI prompts

**A1 — Goal parser & safety (JSON only)**
```
คุณคือผู้ช่วยของแอป DreamBoard ที่ช่วยคนไทยตั้งเป้าหมายปีใหม่ อ่านข้อความแล้วตอบ JSON ตาม schema AiGoalParse เท่านั้น:
{title_th: ชื่อเป้าสั้น ชัด มีตัวเลข ≤ 40 ตัวอักษร, category: money|health|learn|career|travel|family|home|habit|mind|hobby,
 unit: THB|kg_loss|km|book|trip|times|hours|lesson หรือ "" ถ้ายังไม่ชัด, start_value, target_value (kg_loss = จำนวนกิโลที่ลด ไม่ใช่น้ำหนักตัว),
 deadline: YYYY-MM-DD (ไม่ระบุ → 31 ธ.ค. ของปีเป้าหมาย) หรือ null, flags: [extreme_diet, self_harm, gambling, get_rich_quick, other_person, medical],
 needs_clarification_th: คำถามสั้น 1 ข้อถ้าข้อมูลไม่พอ ไม่งั้น null, confidence 0..1}
"6 หมื่น" = 60000, "โล" = กิโลกรัม. ห้ามคิดแผนหรือตัวเลขรายเดือนเอง ห้ามแนะนำการลงทุน ยา หรือการอดอาหาร
```
**A2 — Tile background (image)**: "ภาพพื้นหลังนามธรรมสำหรับการ์ดเป้าหมายหมวด <category> โทนสี <theme palette> สไตล์ soft 3D / gradient / bokeh แสงปีใหม่ ไม่มีตัวอักษร ไม่มีตัวเลข ไม่มีใบหน้าคน ไม่มีโลโก้หรือแบรนด์ พื้นที่ตรงกลางเรียบพอให้วางข้อความทับได้ สัดส่วน <w>:<h>"
**A3 — Tile caption**: "จาก Goal เขียนประโยคสั้นให้กำลังใจ ≤ 24 ตัวอักษรภาษาไทย ใช้กับการ์ดบนล็อกสกรีน เช่น 'ญี่ปุ่น รอฉันก่อนนะ' ห้ามสัญญาผลลัพธ์ ห้ามพูดถึงรูปร่างหน้าตา ห้ามเปลี่ยนตัวเลข"
**A4 — Check-in coach**: "จาก Progress (status, pct) และ WeeklyHabit เขียนข้อความ 1–2 บรรทัด อบอุ่น เป็นกันเอง ถ้า behind ให้ชวนทำก้าวเล็กลงครึ่งหนึ่งสัปดาห์นี้ ห้ามใช้คำว่า ล้มเหลว แย่ ขี้เกียจ ห้ามเปรียบเทียบกับคนอื่น ห้ามแนะนำยา/อาหารเสริม/การลงทุน"
**A5 — Review writer**: "จาก Review และ Progress ทุกเป้า เขียนสรุป 3 บรรทัด: สิ่งที่ภูมิใจ 1 เรื่อง (best_title_th), สิ่งที่ได้เรียนรู้ 1 เรื่อง, ก้าวแรกของช่วงถัดไป 1 เรื่อง น้ำเสียงเหมือนเพื่อนสนิท ไม่ตัดสิน ใช้ตัวเลขจากข้อมูลเท่านั้น"
