# Work-order prompts — PhoneRescue

ใช้ทีละข้อกับ AI codegen (Cursor / Lovable / v0 ฯลฯ). Stack แนะนำ: Next.js + Tailwind (PWA, mobile-first) + vision/OCR สำหรับอ่านแคปจอตั้งค่า + IndexedDB. ใช้ `schemas.json` เป็น type กลาง และ `reference/phonerescue.py` เป็น logic อ้างอิง (port เป็น TS ให้ผลตรงกับ tests).

**P0 — Scaffold**: สร้าง PWA ภาษาไทย mobile-first ชื่อ PhoneRescue ใช้ design tokens ใน prd.md (กรม #0F172A, เขียว #22C55E, ส้ม #F97316, ฟ้า #38BDF8, Kanit) bottom nav: สแกน · แผนเก็บข้อมูล · แบต · เทียบราคา. ทุกหน้าผลลัพธ์แสดง `SafetyGuard`.

**P1 — Screenshot import**: รับแคปหน้าตั้งค่า + เตือนแสง/เบลอ/ครอป ตาม `scan_quality()`. Output `Screenshot`, `ScanQuality`.

**P2 — Screen Read** (wow): เรียก vision A1 → port `parse_storage()` / `parse_battery()` ให้ตรง tests (น้องปอ = 127/128 GB เหลือ 1 GB, แบต 86%). ความมั่นใจ < 0.6 ไม่นับ. Output `StorageScan`, `BatteryScan`, `Pipeline`.

**P3 — Cleanup Plan** (wow): port `cleanup_plan()` ให้ตรง tests (ได้ 16.8 GB เหลือว่าง ~17.8 GB เรียงรูปซ้ำ → แคปจอ → สำรองแชท → แอป → แคช). แสดงเกจก่อน/หลัง. Output `CleanupPlan`, `CleanupAction`.

**P4 — Duplicate-photo guide**: `duplicate_guide()` 5 ขั้นตอน ย้ำสำรองก่อนลบ. Output `DuplicateGuide`, `GuideStep`.

**P5 — Battery tips**: port `battery_tips()` ตามสุขภาพแบต ความสว่าง รีเฟรชพื้นหลัง โหมดประหยัด เวลาหน้าจอเปิด. Output `BatteryTips`.

**P6 — Repair-or-replace**: port `repair_or_replace()` ให้ตรง tests (น้องปอ = cleanup, น้องมุก 76% = repair_battery, ลุงสม 68% = replace_or_repair). แสดงช่วงราคา ฿. Output `RepairCheck`.

**P7 — Share Card + Quota**: `share_card()` 1080 มีลายน้ำ; `quota()` ฟรี 3 ครั้ง/วัน. Output `ShareCard`, `Quota`.

**P8 — Safety**: `safety_guard(wants_reset, backed_up)` รีเซ็ตโดยไม่สำรอง = stop.

**P9 — Manual override**: ผู้ใช้แก้ตัวเลข used/total/health เองได้ถ้า OCR ผิด แล้วรันแผนชุดเดิม.

**P10 — Weekly reminder**: ตั้งเตือนในเครื่องให้เช็กพื้นที่และสำรองรูป (ไม่บังคับ).

**P11 — Privacy**: ลบแคปจอหลังอ่านตัวเลขได้ ห้ามอ่านรหัสหรือบัญชีในจอ.

**P12 — Tests**: เขียน unit test TS ให้ตรงกับ `reference/tests.py` ทั้ง 41 ข้อ และ validate payload ด้วย `schemas.json`.

## AI prompts
**A1 Settings screen extract** (vision, JSON mode): "ดูแคปจอหน้าตั้งค่าพื้นที่ว่างหรือสุขภาพแบต. ตอบ JSON เป็น detections: key ใน {used_gb, total_gb, photos_gb, apps_gb, system_gb, other_gb, health_pct, screen_on_h, last_charge_h, brightness_pct, background_refresh, low_power}, value เป็นตัวเลขหรือบูลีน, confidence 0–1. ถ้าตัวเลขไม่ชัดให้ confidence ต่ำ. ห้ามอ่านอีเมล รหัส หรือชื่อบัญชี. ถ้าไม่ใช่หน้าตั้งค่า ให้บอกสั้น ๆ ภาษาไทย."

**A2 Cleanup narrator** (text): "จาก CleanupPlan เขียนสรุปภาษาไทย ≤ 4 บรรทัด ใช้ตัวเลขใน JSON เท่านั้น ห้ามรับประกันว่าจะได้พื้นที่ตรงกรัม และย้ำให้สำรองก่อนลบ."

**A3 Battery coach** (text): "จาก BatteryTips เขียนคำแนะนำน้ำเสียงใจเย็น เรียงตาม keys ห้ามบอกว่าสุขภาพแบตเป็นค่าทางการจากผู้ผลิตถ้าผู้ใช้แค่แคปจอ."

**A4 Price comparer** (text): "จาก RepairCheck เขียนสรุปสั้นตาม verdict ใช้ช่วงราคาใน JSON ห้ามอ้างร้านหรือโปรโมชันจริง."

**A5 Over-confidence + reset guard**: "ถ้า confidence ของ used_gb หรือ health_pct < 0.6 ให้ถามย้ำ ห้ามทำแผน; ถ้าผู้ใช้จะรีเซ็ตโดยยังไม่สำรอง ให้ใช้ safety_guard(stop)."
