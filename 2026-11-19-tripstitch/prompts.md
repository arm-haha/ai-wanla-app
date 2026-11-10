# Work-order prompts — TripStitch

ใช้ทีละข้อกับ AI codegen (Cursor / Lovable / v0 ฯลฯ). Stack แนะนำ: Next.js + Tailwind (PWA, mobile-first) + vision/OCR สำหรับอ่านแคปจอ + IndexedDB (โหมดออฟไลน์ของการ์ดทริป). ใช้ `schemas.json` เป็น type กลาง และ `reference/tripstitch.py` เป็น logic อ้างอิง (port เป็น TS ให้ผลตรงกับ tests).

**P0 — Scaffold**: สร้าง PWA ภาษาไทย mobile-first ชื่อ TripStitch ใช้ design tokens ใน prd.md (ฟ้า #0F2840, เขียว #14B8A6, เหลืองหมุด #F5C451, ครีม #F7F1E5, Kanit) bottom nav: แคปจอ · แผนวัน · งบ · แพ็กของ. เก็บข้อมูลใน IndexedDB ตาม `Person` / `Place`. ทุกหน้าผลลัพธ์แสดง `SafetyGuard`.

**P1 — Screenshot import**: เลือกหลายรูปจากอัลบั้ม + เตือนแสงสะท้อน/เบลอ/ครอป ตาม `scan_quality()`; ถ้า `ok=false` แสดง `tips_th`. Output `Screenshot`, `ScanQuality`.

**P2 — Place Extract** (wow ต้นทาง): เรียก vision A1 → `Detection[]` → port `extract_places()` (ความมั่นใจ < 0.6 ไปอยู่ `uncertain` และถามย้ำ). Output `Extract`, `Place`, `Pipeline`.

**P3 — Stitch + dedupe**: port `stitch_places()` รวมหลายแคปจอ ตัดรายการซ้ำโดยเก็บความมั่นใจสูงสุด. Output `Stitch`.

**P4 — Day-by-Day Route** (wow): port `plan_days()` ให้ตรง tests (พี่เก้า = 4 วัน นิมมาน → เมืองเก่า → ดอยสุเทพ → แม่ริม, วันที่ 1 FictoBean เช้า + FictoSoi บ่าย). แสดงไทม์ไลน์เช้า/บ่าย/เย็นและนาทีเดินทาง. Output `TripPlan`, `DayPlan`, `Stop`.

**P5 — Closed-day + Rain Plan B**: `closed_warnings()` และ `rain_plan()`; ไฮไลต์ร้านที่ปิดในวันนั้นให้ย้ายวันได้. Output `ClosedWarning`, `RainPlan`.

**P6 — Budget Split**: port `budget_split()` ให้ตรง tests (พี่เก้า งบ 8,000 = ที่พัก 2,700 อาหาร 2,400 เดินทาง 600 ค่าเข้า 100 ของจิปาถะ 1,000 เผื่อ 1,000 รวม 7,800 ป้าย fit). ปรับจำนวนคน/คืน/งบได้. Output `BudgetSplit`, `BudgetLine`.

**P7 — Packing List**: port `packing_list(nights, climates, types)` ตามอากาศและประเภทสถานที่ (เข้าวัด = ชุดสุภาพ, ฝน = ร่ม). Output `PackingList`, `PackItem`.

**P8 — Offline Share Card**: `share_card()` 1080×1350/1080×1920 มีลายน้ำ บันทึกลงเครื่อง เปิดได้โดยไม่ต้องเน็ต. Output `ShareCard`.

**P9 — Quota**: `quota()` ฟรี 3 แคป/วัน paywall สุภาพ. Output `Quota`.

**P10 — Safety & Privacy**: `safety_guard()` ทุกผล; ไม่เก็บที่อยู่บ้าน/เบอร์จากแคปจอ; ลบรูปต้นทางได้หลังดึงชื่อ.

**P11 — Manual add/edit**: ผู้ใช้เพิ่มสถานที่เองหรือแก้ย่าน/ช่วงเวลาได้ ถ้า OCR ผิด โดยยังรัน `plan_days()` ชุดเดิม.

**P12 — Tests**: เขียน unit test TS ให้ตรงกับ `reference/tests.py` ทั้ง 41 ข้อ และ validate payload ด้วย `schemas.json`.

## AI prompts
**A1 Screenshot place extract** (vision, JSON mode): "ดูแคปจอที่ผู้ใช้เซฟไว้ (ไอจี แผนที่ ตึกต็อก หรือเว็บ). ตอบ JSON: รายการสถานที่ (id ชั่วคราว, name_th, name_en ถ้ามี, area เป็นย่านภาษาอังกฤษตัวเล็ก เช่น nimman/old_city, type ใน {cafe, food, temple, market, viewpoint, photo, activity, stay}, source ใน {ig, maps, tiktok, web, note}, confidence 0–1, open_hour/close_hour ถ้าเห็นในแคป ไม่เช่นนั้น null, ticket_thb ถ้ามีราคาค่าเข้า ไม่เช่นนั้น 0). ห้ามเดาชื่อร้านที่ไม่ชัด ให้ confidence ต่ำ. ห้ามดึงที่อยู่บ้าน เบอร์โทร หรือชื่อบุคคล. ถ้าไม่ใช่แคปจอสถานที่ ให้บอกสั้น ๆ ภาษาไทย."

**A2 Day-plan copywriter** (text): "จาก JSON TripPlan เขียนสรุปแต่ละวันภาษาไทย ≤ 2 ประโยค น้ำเสียงกระชับ ไม่เปลี่ยนลำดับสถานที่หรือนาทีเดินทางใน JSON และอย่าพูดว่าเป็นตารางเวลาจริงของร้าน."

**A3 Budget narrator** (text): "จาก BudgetSplit เขียนสรุปงบภาษาไทยสั้น ๆ ตาม verdict (under/fit/tight/over) ใช้ตัวเลขใน JSON เท่านั้น ห้ามเสนอร้านจองจริงหรือส่วนลด."

**A4 Packing helper** (text): "จาก PackingList จัดกลุ่มข้อความตาม group (clothes/weather/activity/essentials) เป็นลิสต์ติ๊กได้ ภาษาสุภาพ ไม่แนะนำของผิดกฎหมายหรือยารักษาโรคเฉพาะราย."

**A5 Over-confidence guard**: "ตรวจ A1 — ถ้า confidence < 0.6 ให้อยู่ใน uncertain และถามย้ำ ห้ามใส่ในแผน; ถ้าพบที่อยู่บ้านหรือเบอร์โทร ให้ตัดทิ้งและเตือนผู้ใช้."
