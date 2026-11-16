# Work-order prompts — BalconyFarm

ใช้ทีละข้อกับ AI codegen (Cursor / Lovable / v0 ฯลฯ). Stack แนะนำ: Next.js + Tailwind (PWA, mobile-first) + vision model อ่านรูประเบียง + image-edit model สำหรับภาพจำลอง + DeviceOrientation API (เข็มทิศ) + IndexedDB. ใช้ `schemas.json` เป็น type กลาง และ `reference/balconyfarm.py` เป็น logic อ้างอิง (port เป็น TS ให้ผลตรงกับ tests).

**P0 — Scaffold**: PWA ภาษาไทย mobile-first ชื่อ BalconyFarm ใช้ design tokens ใน prd.md (ครีม #F4F9EE, เขียว #3FA34D, ส้มแดด #FFB547, ดินเผา #C8693F, Kanit). bottom nav: ระเบียง · ผัก · รดน้ำ · ไดอารี่. ทุกหน้าผลแสดง `SafetyGuard` + disclaimer.

**P1 — Balcony Capture**: กล้อง + เส้นไกด์ "ให้เห็นพื้นถึงราว". เช็ก `scan_quality()`; เรียก A1 → `AiBalconyExtract`; ถ้า `is_balcony=false` → `safety_guard("not_balcony")`. ให้ผู้ใช้แก้กว้าง/ลึกได้ด้วยสไลเดอร์ (ค่าเริ่มจาก AI).

**P2 — Sun Meter**: อ่านเข็มทิศจาก DeviceOrientation ตอนหันหน้าออกนอกระเบียง → map เป็น 8 ทิศ; stepper ชั้น; port `sun_estimate()` ให้ตรง tests (se, 0.3, 1.0, ชั้น 12 = 3.8 ชม. ครึ่งแดด). มิเตอร์ดวงอาทิตย์ 3 โซน. Output `SunEstimate`.

**P3 — Plant Picker**: การ์ดผัก 12 ชนิด เรียงตาม `plant_picks()` แสดง score + `why_th`; แตะเพื่อเพิ่ม/ลบ (exclude). Output `PlantPicks`.

**P4 — Garden Mockup** (wow): `mockup_spec()` → ส่งรูปเดิม + `image_prompt` เข้า A2 (image edit) สร้าง 4:5; สไลเดอร์ ก่อน/หลัง ลากกลางจอ + แอนิเมชันใบไม้งอก. 3 สไตล์ให้เลือก. นับ `quota()`.

**P5 — Layout + Load**: port `layout()` วาดผังมุมบน (กระถางวงกลมตาม `pot_cm`, แถบทางเดิน 60 ซม.) + ป้ายสีตาม `load_status`; `skipped` แสดงเป็น "ไม่พอที่". ถ้า `over` → `safety_guard("overload")`. Output `Layout`.

**P6 — Water Plan**: port `water_plan()` ตาราง 7 วัน ไอคอนบัวรดน้ำ; แจ้งเตือนในเครื่อง 07:30; กด "รดแล้ว" = `DiaryEntry(action=water)`. Output `WaterPlan`.

**P7 — Harvest Countdown**: `harvest_plan()` วงแหวนนับถอยหลังต่อต้น + ยอดประหยัด ฿/เดือน. Output `HarvestPlan`.

**P8 — Shopping List**: `shopping_list()` ติ๊กซื้อของ + งบรวม + คืนทุน; ปุ่มคัดลอกเป็นข้อความไปร้านต้นไม้. Output `ShoppingList`.

**P9 — Garden Diary**: บันทึก water/harvest(grams)/photo/fertilize → `diary_summary()` สตรีค + กรัม + ฿. Output `DiarySummary`.

**P10 — Share Card**: `share_card()` เรนเดอร์ 1080×1350 ก่อน/หลัง ลายน้ำ "BalconyFarm · AI วันละแอป" + Web Share API.

**P11 — Quota & Guard**: `quota()` ฟรี 3 ภาพจำลอง/วัน; `safety_guard()` (railing / overload / pesticide / not_balcony).

**P12 — QA**: รัน `reference/tests.py` (31 tests) และ validate output ทุกตัวกับ `schemas.json`; ทดสอบเข็มทิศ iOS (ต้องขอ permission) + Android, จอเล็ก, รูปย้อนแสง.

## AI prompts
**A1 — Balcony read (vision → JSON)**
```
คุณคือผู้ช่วยจัดสวนระเบียง ดูรูปแล้วตอบเป็น JSON ตาม AiBalconyExtract เท่านั้น
obstruction = สัดส่วนท้องฟ้าที่ถูกตึก/ต้นไม้บังเมื่อมองออกจากระเบียง (0–1)
overhang_m = ความยื่นของชายคา/ระเบียงชั้นบนเหนือหัว (เมตร), width_m/depth_m = ขนาดพื้นระเบียงโดยประมาณ ใช้ประตูบานเลื่อน (สูง ~2.1 ม.) เป็นสเกล
railing ∈ [glass, metal_bars, concrete_wall]
ถ้าไม่ใช่ระเบียงให้ is_balcony=false; ถ้าไม่แน่ใจ confidence < 0.7 ห้ามเดา
ถ้าเห็นกระถางวางบนราวหรือแขวนนอกราว ให้ระบุใน notes_th
```
**A2 — Garden mock-up (image edit)**: ใช้ `MockupSpec.image_prompt` กับรูปเดิม; คงผนัง ราว พื้น และมุมกล้องเดิม; กระถางทั้งหมดอยู่บนพื้นด้านในราว; ห้ามคน ห้ามโลโก้.
**A3 — Plant care tip**: "ให้เคล็ดลับดูแล <plant_th> 3 ข้อ สำหรับระเบียง <light_th> ฤดู <season> ภาษาง่าย ห้ามแนะนำสารเคมีอันตราย"
**A4 — Recipe from harvest**: "ผักที่เก็บได้วันนี้ <list> เสนอเมนูไทยง่าย ๆ 2 เมนู ใช้เวลาไม่เกิน 15 นาที"
**A5 — Diary nudge**: "จาก DiarySummary เขียนข้อความชวนดูแลสวนต่อ 1 บรรทัด อบอุ่น ไม่กดดัน ห้ามเปลี่ยนตัวเลข"
