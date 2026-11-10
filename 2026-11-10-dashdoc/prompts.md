# Work-order prompts — DashDoc

ใช้ทีละข้อกับ AI codegen (Cursor / Lovable / v0 ฯลฯ). Stack แนะนำ: Next.js + Tailwind (PWA, mobile-first) + vision model (OpenAI/Gemini) สำหรับอ่านหน้าปัดและจำแนกสัญลักษณ์ + IndexedDB. ใช้ `schemas.json` เป็น type กลาง และ `reference/dashdoc.py` เป็น logic อ้างอิง (port เป็น TS ให้ผลตรงกับ tests).

**P0 — Scaffold**: สร้าง PWA ภาษาไทย mobile-first ชื่อ DashDoc ใช้ design tokens ใน prd.md (กรมท่า #12161F, อำพัน #FFC107, ส้ม #FF9F1C, แดง #DC2626, เขียว #16A34A, Kanit) bottom nav: สแกน · ไดอารี่ · ไฟเตือน · ฉุกเฉิน. เก็บข้อมูลใน IndexedDB ตาม `Person` / `Car` / `ServiceEntry`. ทุกหน้าผลลัพธ์แสดง `SafetyGuard`.

**P1 — Dash Snap**: กล้องหลัง + กรอบหน้าปัด + เตือนแสงสะท้อน/เบลอ/เอียง ตาม `scan_quality()`; ถ้า `ok=false` แสดง `tips_th` และปุ่มถ่ายใหม่. Output `DashPhoto`, `ScanQuality`.

**P2 — Light Scan**: เรียก vision A1 → `Detection[]` → port `identify_lights()` / `light_scan()` (ความมั่นใจ < 0.6 ไปอยู่ `uncertain` และถามย้ำ "ไฟดวงนี้คือ ... ใช่ไหม?"; เช็กเครื่องกะพริบหรือสีแดงจริงบนไฟเหลือง = ยกเป็นแดง). Output `LightScan`, `IdentifiedLight`, `Pipeline`.

**P3 — Urgency Meter + Verdict** (wow): port `urgency_score()` / `drive_verdict()` ให้ตรง tests (พี่โอ๊ต = 48 เหลือง ~50 กม./80 กม./ชม./1 วัน). แอนิเมชันเข็มเกจสแกนไฟทีละดวง → เข็มวิ่งเข้าโซน → ตัวอักษรใหญ่ "ขับต่อได้ ~50 กม." ไฟแดงแสดงปุ่มโทรประกัน/รถยก ไม่มีปุ่มขับต่อ. Output `Verdict`.

**P4 — Symptom Chips + Do-This-Now**: เลือกอาการ 9 แบบ → `drive_verdict(lights, symptoms)`; แสดง `do_now_steps()` เป็นเช็กลิสต์ติ๊กทีละข้อ (ไฟแดงขึ้นก่อน). Output `DoNowSteps`.

**P5 — Light Library**: โหลด `LIGHTS` (17 ดวง) ตาม `LightInfo`; ค้นหา/กรองด้วยสี; หน้ารายละเอียดมีความหมาย ระยะขับต่อ รายการซ่อมที่น่าจะเป็น.

**P6 — Fair Price Check**: port `price_range()` / `likely_fixes()` / `quote_check()`; กรอกพื้นที่/ประเภทรถ; ช่องใส่ราคาที่อู่เสนอ → ป้าย ถูก/สมเหตุสมผล/แพง/แพงมาก + คำถามถามช่าง + disclaimer ราคา. Output `FixPrice`, `QuoteCheck`.

**P7 — Mechanic Card**: port `mechanic_card()`; การ์ดแนวตั้ง (รุ่นรถ เลขไมล์ ไฟ อาการ งบ) บันทึกเป็นรูปและปุ่มส่ง LINE (`line_share_url`). Output `MechanicCard`.

**P8 — Car Diary + Reminders**: `service_entry()` + `next_due()` + `reminder_status()` (ok/soon/due/overdue ตามกม. 500/1,500 และวัน 14/30); local notification; `diary_stats()`. Output `ServiceEntry`, `NextDue`, `ReminderStatus`, `DiaryStats`.

**P9 — Emergency Kit**: `emergency_kit()` ให้ผู้ใช้กรอกเบอร์ประกัน/รถยก/อู่ (placeholder) + เบอร์สาธารณะที่มีป้าย "ตรวจกับแหล่งทางการ"; `guide()` ยางแบน/จั๊มสตาร์ท/เครื่องร้อน. Output `EmergencyKit`, `Guide`.

**P10 — Share Card + Quota**: `share_card()` 1080×1350/1080×1920 มีลายน้ำ; `quota()` ฟรี 3 สแกน/วัน paywall สุภาพ. Output `ShareCard`, `Quota`.

**P11 — Safety & Privacy**: `safety_guard()` ทุกผล; ลบรูปหน้าปัดหลังสแกน; ห้ามเก็บเลขทะเบียน/ตำแหน่งเกินจำเป็น; ไม่โชว์ผลว่า "ปลอดภัย 100%".

**P12 — Tests**: เขียน unit test TS ให้ตรงกับ `reference/tests.py` ทั้ง 41 ข้อ และ validate payload ด้วย `schemas.json`.

## AI prompts
**A1 Dashboard light extract** (vision, JSON mode): "ดูรูปหน้าปัดรถที่ผู้ใช้ถ่าย. ตอบ JSON: รายการไฟเตือนที่เห็น (symbol เลือกจากรายการ {check_engine, oil_pressure, coolant_temp, battery_charge, brake_system, parking_brake, abs, airbag, tpms, low_fuel, power_steering, dpf, esc, washer, service_due, high_beam, seat_belt}, color_seen red/yellow/green/blue, flashing true/false, confidence 0–1), glare 0–1, blur 0–1, tilt 0–1. ห้ามเดาสัญลักษณ์ที่ไม่ชัด ให้ confidence ต่ำแทน. ถ้าไม่ใช่รูปหน้าปัดรถ ให้บอกสั้น ๆ ภาษาไทย. ห้ามอ่านเลขทะเบียนหรือระบุตัวบุคคล."

**A2 Plain-Thai verdict writer** (text): "จาก JSON Verdict เขียนคำตอบ 'ขับต่อได้ไหม' ภาษาไทยง่าย ๆ ≤ 2 ประโยค น้ำเสียงใจเย็นแต่ชัดเจน ห้ามเปลี่ยนระดับ/ตัวเลข กม./วัน ใน JSON; ถ้า level=red ต้องบอกให้จอดในที่ปลอดภัยก่อนเสมอ; ห้ามบอกว่า 'ปลอดภัยแน่นอน'."

**A3 Mechanic question writer** (text): "จาก QuoteCheck และไฟเตือน เขียนคำถาม 3 ข้อที่ผู้ใช้ควรถามช่าง ภาษาสุภาพ ไม่กล่าวหาว่าช่างโกง ขอดูผลอ่านรหัสและอะไหล่เก่า รับประกันกี่เดือน."

**A4 Mechanic note writer** (text): "เขียนโน้ตสั้นถึงช่างภาษาไทย สุภาพ ≤ 4 บรรทัด จาก JSON MechanicCard: รุ่นรถ ปี เลขไมล์ ไฟเตือน อาการ งบ. ห้ามอ้างว่าราคาเป็นราคาจริงของอู่ ห้ามวินิจฉัยเกินข้อมูล."

**A5 Over-confidence guard**: "ตรวจ output ของ A1/A2 — ถ้าความมั่นใจของไฟที่เป็นแดง < 0.6 ให้ถามย้ำผู้ใช้ ห้ามตอบว่าไม่มีปัญหา; ถ้า A2 ขัดกับ level ใน JSON ให้ใช้ข้อความ template จาก `drive_verdict()` แทน."
