# Work-order prompts — StainSOS

ใช้ทีละข้อกับ AI codegen (Cursor / Lovable / v0 ฯลฯ). Stack แนะนำ: Next.js + Tailwind (PWA, mobile-first) + vision model สำหรับอ่านคราบและป้ายผ้า + IndexedDB. ใช้ `schemas.json` เป็น type กลาง และ `reference/stainsos.py` เป็น logic อ้างอิง (port เป็น TS ให้ผลตรงกับ tests).

**P0 — Scaffold**: สร้าง PWA ภาษาไทย mobile-first ชื่อ StainSOS ใช้ design tokens ใน prd.md (ขาว #F7F7F2, ฟ้า #0EA5E9, ส้ม #D97706, เขียว #16A34A, แดง #DC2626, Kanit). bottom nav: เลอะแล้ว! · ชุดในบ้าน · ป้ายผ้า · ไดอารี่. ทุกหน้าผลแสดง `SafetyGuard`.

**P1 — Stain Snap**: กล้องหลัง + กรอบคราบ + เตือนแสง/เบลอ/ครอป ตาม `scan_quality()`; ถ้า `ok=false` แสดง `tips_th`. Output `StainPhoto`, `PhotoScan`.

**P2 — Stain Scan** (wow): เรียก vision A1 แล้ว port `parse_stain()`; ถ้า `needs_confirm` แสดงชิปให้เลือกชนิดคราบ/ผ้าใหม่ และห้ามไปหน้าแผน. Output `ParsedStain`.

**P3 — Risk Meter**: port `risk_meter()` ให้ตรง tests (ชาไทย 2 ชม. ผ้าฝ้ายขาว 4 ซม. = 50 medium, จาง 70%). เกจครึ่งวงกลมหมุนเข้าเลข. Output `RiskMeter`.

**P4 — Home Kit**: ติ๊กของในบ้านจาก `ITEMS` (ยกเว้นคลอรีน/แอมโมเนีย/ไฮโดรเจนเปอร์ออกไซด์ ซ่อนไว้ในหมวด "น้ำยาที่มีอยู่" เพื่อใช้กับ Mix Check เท่านั้น). เก็บใน IndexedDB.

**P5 — Rescue Steps + Timer**: port `rescue_plan()`; การ์ดทีละขั้น ปุ่มเริ่มจับเวลาเมื่อ minutes > 0 ขั้นที่ missing แสดงของทดแทนหรือปุ่ม "เพิ่มในลิสต์ซื้อ". ถ้า `dry_clean` แสดงแผน 3 ขั้นและปุ่มหาร้านซักแห้ง. Output `RescuePlan`.

**P6 — Mix Danger Check**: `safety_check()` ทุกครั้งที่ผู้ใช้เลือกน้ำยา ถ้า danger จอแดงเต็มและปิดปุ่มเริ่ม. Output `SafetyCheck`.

**P7 — Care-Label Decoder**: vision A2 อ่านสัญลักษณ์ → `care_label()`; แล้ว `plan_fits_label()` แจ้งถ้าแผนขัดป้าย. Output `CareLabel`, `LabelFit`.

**P8 — Before/After Card**: ถ่ายหลังซัก (รูปจริงเท่านั้น) วางคู่รูปก่อน + `share_card()` 1080×1350/1080×1920 ลายน้ำ. Output `ShareCard`.

**P9 — Kit Check + Diary**: `kit_check()` แสดง "พร้อม X/8 คราบ"; บันทึก `DiaryEntry` หลังจบแผน (หาย/จาง/ไม่หาย + ราคาเสื้อ) และ `diary_summary()`. Output `KitCheck`, `DiarySummary`.

**P10 — Quota**: `quota()` ฟรี 3 สแกน/วัน มี paywall แบบนุ่ม.

**P11 — Safety & Privacy copy**: onboarding บอกว่าเป็นค่าประมาณ ทดสอบมุมด้านในก่อน ห้ามผสมน้ำยา ใส่ถุงมือ เปิดหน้าต่าง; รูปลบหลังประมวลผล.

**P12 — Tests**: เขียน unit test TS ให้ตรงกับ `reference/tests.py` ทั้ง 40 ข้อ และ validate payload ด้วย `schemas.json`.

## AI prompts
**A1 Stain extract** (vision, JSON mode): "ดูรูปคราบบนผ้า ตอบ JSON ตาม AiStainExtract: stain (coffee|thai_tea|curry|oil|lipstick|ink|blood|mud), fabric (cotton|denim|polyester|rayon|wool|silk), color (white|colored), age_hours (ถ้าไม่รู้ให้ 1), size_cm, confidence 0–1, notes_th. ถ้าไม่แน่ใจให้ confidence ต่ำ อย่าเดา ห้ามระบุตัวบุคคลหรือแบรนด์จากรูป."

**A2 Care-label read** (vision): "อ่านสัญลักษณ์ป้ายวิธีดูแลผ้าในรูป ตอบเป็นรายการโค้ดจาก: wash_30, wash_40, wash_60, hand_wash, no_wash, no_bleach, non_chlorine_bleach, tumble_low, no_tumble, iron_low, iron_med, dry_clean, no_dry_clean. ถ้าอ่านไม่ชัดให้ข้ามสัญลักษณ์นั้น."

**A3 Step coach** (text): "จาก RescuePlan เขียนคำพูดสั้น ๆ เป็นกันเองภาษาไทยสำหรับแต่ละขั้น ห้ามเพิ่มน้ำยาหรือขั้นตอนที่ไม่มีใน JSON ห้ามแนะนำน้ำร้อนกับคราบเลือด และห้ามพูดถึงน้ำยาฟอกคลอรีน."

**A4 Card composer** (layout): "จัดการ์ดก่อน/หลังจากรูปจริงสองรูปของผู้ใช้ ใส่ hook_th และลายน้ำ ห้ามแต่งรูปหลังให้ดูสะอาดกว่าจริง."

**A5 Safety guard**: "ตรวจข้อความจาก A1–A3 ถ้ามีคำแนะนำผสมน้ำยาสองชนิด น้ำยาฟอกคลอรีน น้ำร้อนกับคราบโปรตีน หรือรับประกันว่าคราบจะหาย ให้แทนด้วยข้อความจาก `safety_guard()` และถ้า confidence < 0.6 ห้ามสร้างแผน."
