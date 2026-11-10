# Work-order prompts — MedBuddy

ใช้ทีละข้อกับ AI codegen (Cursor / Lovable / v0 ฯลฯ). Stack แนะนำ: Next.js + Tailwind (PWA, mobile-first) + vision สำหรับอ่านข้อความบนซองยา + IndexedDB + การแจ้งเตือนในเครื่อง. ใช้ `schemas.json` เป็น type กลาง และ `reference/medbuddy.py` เป็น logic อ้างอิง (port เป็น TS ให้ผลตรงกับ tests).

**P0 — Scaffold**: สร้าง PWA ภาษาไทย mobile-first ชื่อ MedBuddy ใช้ design tokens ใน prd.md (ขาว #F6F8FB, ฟ้า #2563EB, เขียว #16A34A, อำพัน #F59E0B, แดง #DC2626, Kanit) bottom nav: ตาราง · ถ่ายซอง · ใกล้หมด · นัดแพทย์. เก็บข้อมูลใน IndexedDB ตาม `Person` / `ParsedLabel`. ทุกหน้าผลลัพธ์แสดง `SafetyGuard` สีแดงชัดว่าห้ามเปลี่ยนขนาดยาเอง.

**P1 — Label Snap**: กล้องหลัง + กรอบซองยา + เตือนแสง/เบลอ/ครอป ตาม `scan_quality()`; ถ้า `ok=false` แสดง `tips_th`. Output `LabelPhoto`, `ScanQuality`.

**P2 — Label Scan**: เรียก vision A1 แล้ว port `parse_label()`; ถ้า `needs_confirm` ให้ผู้ใช้แก้/ยืนยันทุกช่อง ห้ามบันทึกขนาดยาที่ยังไม่ชัด. Output `ParsedLabel`.

**P3 — Schedule** (wow): port `schedule()` ให้ตรง tests (เช้า 2, เย็น 1, เมื่อปวด 1). แสดงการ์ดมื้อใหญ่ ติ๊กได้ทีละรายการ. ห้ามจัดตารางถ้ารายการยัง `needs_confirm`. Output `Schedule`.

**P4 — Caregiver Share**: `caregiver_share()` ส่งลิงก์หรือการ์ดให้ลูกในครอบครัว ติ๊กมื้อที่กินแล้ว (ไม่นับมื้อเมื่อมีอาการในรายการค้าง). Output `CaregiverShare`.

**P5 — Refill Reminder**: port `refill()` (FictoPril 14 วัน soon, FictoMet 10 วัน soon, FictoPain ask). ยาใช้เมื่อมีอาการห้ามคำนวณวันหมดเอง. Output `Refill`.

**P6 — Doctor-Visit Card**: `visit_card()` รวมรายการที่ผู้ใช้บันทึก มีข้อความว่าไม่ใช่ใบสั่งยา และเตือนให้นำซองจริงไปด้วย. Output `VisitCard`.

**P7 — Missed Dose + Interaction Flag**: `missed_dose_guide()` ขึ้นต้นด้วยอย่ากินเพิ่มเป็นสองเท่า และ `interaction_flag()` เมื่อมีหลายชนิดให้ถามเภสัชกร. Output `MissedGuide`, `InteractionFlag`.

**P8 — Library (demo only)**: แสดง `LIBRARY` โดยติดป้ายว่าเป็นชื่อสมมติ ไม่ใช่ยาจริง. Output `LibraryItem`.

**P9 — Share Card + Quota**: `share_card()` 1080×1350/1080×1920 มีลายน้ำและ disclaimer; `quota()` ฟรี 3 ซอง/วัน. Output `ShareCard`, `Quota`.

**P10 — Safety & Privacy**: `safety_guard()` ทุกผล; ลบรูปซองหลังอ่าน; ห้ามเก็บชื่อยาไปเทรน; ห้ามมีปุ่ม "ปรับขนาด" หรือคำแนะนำให้เพิ่ม/ลดยา.

**P11 — Onboarding copy**: หน้าแรกบอกชัดว่าต้องยืนยันกับเภสัชกร ห้ามเปลี่ยนขนาดยาเอง และตัวอย่างในแอปเป็นยาสมมติ.

**P12 — Tests**: เขียน unit test TS ให้ตรงกับ `reference/tests.py` ทั้ง 41 ข้อ และ validate payload ด้วย `schemas.json`.

## AI prompts
**A1 Envelope extract** (vision, JSON mode): "ดูรูปซองยาที่ผู้ใช้ถ่าย. ตอบ JSON: name, strength_th, dose_th, slots (morning|noon|evening|bedtime|as_needed), food (before_food|after_food|with_food|any), qty, confidence 0–1. ถ้าอ่านไม่ชัดให้ confidence ต่ำและอย่าเดาขนาดยาหรือจำนวนครั้งต่อวัน. ห้ามแนะนำขนาดใหม่ ห้ามเทียบเป็นยาชื่อการค้าจริง และห้ามระบุตัวบุคคลจากรูป."

**A2 Confirm prompt** (text): "จาก ParsedLabel ที่ needs_confirm=true เขียนคำถามภาษาไทยให้ผู้ใช้ยืนยันทีละช่อง น้ำเสียงสุภาพ ห้ามเสนอขนาดยาใหม่."

**A3 Schedule copy** (text): "จาก JSON Schedule เขียนสรุปมื้อยาสั้น ๆ ภาษาไทย ห้ามเปลี่ยนชื่อยา ขนาด หรือจำนวนมื้อใน JSON และต้องปิดท้ายว่าให้ยืนยันกับเภสัชกร."

**A4 Visit card composer** (image/layout): "จัดเป็นการ์ดพบแพทย์ตาม VisitCard: ชื่อคนไข้ คลินิก วันนัด รายการยา disclaimer ว่าไม่ใช่ใบสั่งยา. โทนขาว-ฟ้า. ห้ามใส่โลโก้โรงพยาบาลจริง."

**A5 Safety guard**: "ตรวจ A1–A3 — ถ้ามีคำแนะนำให้เพิ่ม ลด หยุด หรือกินสองเท่า ให้แทนที่ด้วยข้อความจาก `missed_dose_guide()` / `safety_guard()` ทันที และถ้า confidence < 0.6 ห้ามจัดตาราง."
