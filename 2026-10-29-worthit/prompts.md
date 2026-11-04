# Work-order prompts — WorthIt (ใช้ทีละข้อกับ AI codegen เช่น Cursor / v0 / Lovable)

**P0 — Scaffold**: สร้าง PWA ด้วย Next.js + Tailwind + Framer Motion ชื่อ "WorthIt — คุ้มไหมก่อนกดซื้อ" mobile-first 390px, ภาษาไทยทั้งแอป, ฟอนต์ IBM Plex Sans Thai + Space Grotesk สำหรับตัวเลข, design tokens ตาม prd.md, เก็บข้อมูลทั้งหมดใน localStorage (ไม่มี backend ยกเว้น 1 API route สำหรับ vision)

**P1 — Onboarding**: 3 สไลด์: รายได้ต่อเดือน, วันทำงาน/เดือน + ชม./วัน (default 22/8), เป้าโหล (ชื่อ+ยอด) → validate ตาม `$defs/Profile` ใน schemas.json ข้อความย้ำ "รายได้อยู่ในเครื่องคุณเท่านั้น"

**P2 — Core math**: port `reference/worthit.py` เป็น `lib/worthit.ts` ให้ผลตรงทุกตัวเลข (hourly_wage, work_time, fmt_hours, cost_per_use, verdict, cooloff_hours, cooloff_status, skip_jar, month_report, habit_cost) + เขียน unit test จากเคสใน `reference/tests.py`

**P3 — Snap & Vision**: ปุ่มกล้องใหญ่/อัปโหลด screenshot/วางลิงก์/พิมพ์เอง → API route ส่งรูปให้ vision model ด้วย system prompt ด้านล่าง → ผลต้องผ่าน `$defs/VisionExtract`; ถ้า confidence < 0.7 หรือ price null → หน้า confirm ให้แก้ราคา

**P4 — Result screen (WOW)**: ราคาแสดงใหญ่ 0.6 วิ แล้ว morph เป็นหน้าปัดนาฬิกาที่หมุนเท่าจำนวนชั่วโมง, นับเลขขึ้นถึง label_th, ใต้ลงมาเป็น chip "x.x วันทำงาน" และ "x% ของเงินเดือน", haptic ตอนจบ

**P5 — Cost-per-Use + Quiz**: 2 slider (ใช้/เดือน, กี่เดือน) → per_use + สีตาม tier; ต่อด้วย 5 การ์ด swipe ซ้าย/ขวา ตาม QUESTIONS → Verdict screen สี buy/wait/skip + ปุ่ม "ซื้อ" "รอ" "ไม่ซื้อ"

**P6 — Cool-off Timers**: ปุ่ม "รอ" สร้าง timer ตาม cooloff_hours, หน้า Wishlist แสดง countdown, Web Notification ตอนครบ "ยังอยากได้ ___ อยู่ไหม?" ตอบ ใช่ → กลับไป Verdict / ไม่ → เข้าโหล + การ์ด cooloff_win

**P7 — Skip Jar**: animation เหรียญหล่นลงโหลแก้ว (ยอดบาทบนเหรียญ), progress เข้าเป้า, confetti เมื่อ reached

**P8 — Habit Math + Report**: หน้า Habit (ราคา × ครั้ง/สัปดาห์ → ต่อเดือน/ปี/ชั่วโมง) และ Monthly Report ตาม `$defs/MonthReport`

**P9 — Dupe Hunt + Share Card**: AI คืนเฉพาะ `$defs/DupeQuery` (คำค้น ไม่มีราคา) ปุ่มคัดลอกคำค้น; Share Card 9:16 ทุก kind ใน `$defs/ShareCard` export PNG ผ่าน html-to-image, มี disclaimer มุมล่าง

**P10 — Polish & QA**: empty states, dark mode, ทดสอบด้วย fixtures (มายด์) ให้ได้ตัวเลขตรง prd.md, Lighthouse PWA ผ่าน

## Vision system prompt
```
คุณอ่านภาพหน้าสินค้า/ป้ายราคา/สกรีนช็อตแอปช้อปปิ้ง ตอบเป็น JSON เท่านั้นตามสคีมา VisionExtract:
{"name_th": string, "price_thb": number|null, "original_price_thb": number|null, "shop_hint": string|null, "confidence": 0-1, "needs_confirm": boolean}
กฎ: ใช้ราคาที่ต้องจ่ายจริง (ราคาหลังลด) เป็น price_thb; ราคาขีดฆ่าเป็น original_price_thb
ถ้าอ่านราคาไม่ชัด ให้ price_thb = null และ needs_confirm = true ห้ามเดา
ถ้าเป็นสกุลเงินอื่น ให้ price_thb = null, needs_confirm = true และระบุสกุลใน shop_hint
ชื่อสินค้าสั้น ≤ 30 ตัวอักษร ภาษาไทย ไม่ใส่ชื่อแบรนด์ถ้าไม่เห็นชัด
```

## Dupe prompt
```
จากชื่อสินค้า "{name_th}" หมวด {category} ให้คำค้นภาษาไทย 2–5 คำสำหรับหาของลักษณะคล้ายกันที่อาจถูกกว่า
ตอบ JSON {"item_id","search_terms_th":[...],"note_th"} ห้ามใส่ราคา ห้ามอ้างชื่อร้านหรือบอกว่าถูกกว่าเท่าไร
```
