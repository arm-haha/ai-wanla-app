# Work-order prompts — ContractLens

ใช้ทีละข้อกับ AI codegen (Cursor / Lovable / v0 ฯลฯ). Stack แนะนำ: Next.js + Tailwind (PWA, mobile-first) + vision/OCR + IndexedDB. ใช้ `schemas.json` เป็น type กลาง และ `reference/contractlens.py` เป็น logic อ้างอิง (port เป็น TS ให้ผลตรงกับ tests). **ห้ามอ้างว่าเป็นคำกฎหมาย.**

**P0 — Scaffold**: สร้าง PWA ภาษาไทย mobile-first ชื่อ ContractLens ใช้ design tokens ใน prd.md (กระดาษ #F3EFE6, หมึก #1A1A1A, แดง #DC2626, เหลือง #E7B00C, Kanit) bottom nav: สแกน · จุดเสี่ยง · คำนวณ · เช็กลิสต์. ทุกหน้าผลลัพธ์แสดง `SafetyGuard`.

**P1 — Doc Snap**: กล้องหลัง + กรอบเอกสาร + เตือนแสงสะท้อน/เบลอ/เอียง ตาม `scan_quality()`. Output `ContractPhoto`, `ScanQuality`.

**P2 — Contract Scan**: เรียก vision A1 → ชนิดสัญญา + Detection[] → port `contract_scan()` (ความมั่นใจ < 0.6 ไป uncertain ถามย้ำ). Output `ContractScan`, `Pipeline`.

**P3 — Risk Highlights** (wow): port `risk_highlights()` ให้ตรง tests (น้องเบนซ์ = แดง คะแนน 86, จุดแดง 2 ข้อ: ต่ออัตโนมัติ + มัดจำสูง). แอนิเมชันขีดแดงบนข้อความแล้วโชว์เกจ. Output `RiskHighlights`, `RiskItem`.

**P4 — Plain-Thai Summary**: port `plain_summary()`. ห้ามเพิ่มข้อกฎหมายที่ไม่มีใน JSON. Output `PlainSummary`.

**P5 — Fee Calculator**: port `fee_calc()` ให้ตรง tests (ย้ายเข้า ฿92,000; กู้ตัวอย่างต้น 100,000 ดอก 2%/เดือน 12 เดือน รวม 124,000). ป้ายชัดว่าเป็นแบบจำลอง. Output `RentalFees` / `LoanFees`.

**P6 — Clause Library**: โหลด `CLAUSES` (12) ตาม `ClauseInfo` ใช้ออฟไลน์.

**P7 — Questions + Checklist**: port `questions_to_ask()` / `sign_checklist()` ให้ตรง tests (เบนซ์ทำแล้ว 3/10 ยังไม่พร้อม). Output `Questions`, `SignChecklist`.

**P8 — Family Card**: port `family_card()` ส่ง LINE ต้องมีข้อความไม่ใช่คำกฎหมาย. Output `FamilyCard`.

**P9 — Diary**: `diary_entry()` / `diary_stats()`. Output `DiaryEntry`, `DiaryStats`.

**P10 — Share + Quota**: `share_card()` มีลายน้ำ; `quota()` ฟรี 3 ครั้ง/วัน. Output `ShareCard`, `Quota`.

**P11 — Safety & Privacy**: `safety_guard()` ทุกผล; ห้ามใส่มาตรากฎหมายที่โมเดลแต่ง; ลบรูปเอกสารหลังประมวลผล; ห้ามเก็บเลขบัตร/บัญชี/ลายเซ็น.

**P12 — Tests**: เขียน unit test TS ให้ตรงกับ `reference/tests.py` ทั้ง 41 ข้อ และ validate ด้วย `schemas.json`.

## AI prompts
**A1 Contract extract** (vision, JSON mode): "ดูรูปหน้าสัญญาที่ผู้ใช้ถ่าย. ตอบ JSON: kind (rental หรือ loan), glare blur tilt text_fill 0–1, รายการข้อที่เข้ากับ {auto_renew, excess_deposit, heavy_penalty, entry_no_notice, hidden_fee, utility_unclear, repair_all, interest_high, early_termination, no_receipt, seizure, blank_terms} พร้อม excerpt สั้นและ confidence 0–1, ตัวเลขที่เห็น (ค่าเช่า มัดจำเป็นเดือน ดอกเบี้ยต่อเดือน ระยะเดือน) ถ้ามี. ห้ามระบุชื่อจริง เลขบัตร เลขบัญชี. ห้ามตัดสินว่าถูกหรือผิดกฎหมาย. ถ้าไม่ใช่สัญญา ให้บอกสั้น ๆ ภาษาไทย."

**A2 Plain-Thai writer** (text): "จาก JSON PlainSummary และ RiskHighlights เขียนสรุปภาษาไทยง่าย ≤ 5 ประโยค ห้ามเปลี่ยนตัวเลข ห้ามเพิ่มมาตรากฎหมาย ห้ามบอกว่า 'เซ็นได้/เซ็นไม่ได้ตามกฎหมาย' ถ้ามีจุดแดงต้องชวนชะลอแล้วถาม/ปรึกษาผู้รู้."

**A3 Question writer** (text): "จาก JSON Questions เรียบเรียงคำถามสุภาพเป็นข้อ ๆ ห้ามเพิ่มคำถามที่ชี้ว่าอีกฝ่ายผิดกฎหมาย."

**A4 Family card writer** (text): "จาก JSON FamilyCard เขียนข้อความสั้นถึงครอบครัว ต้องมีประโยคว่าไม่ใช่คำปรึกษาทางกฎหมาย."

**A5 Over-confidence guard**: "ตรวจ output ของ A1–A2 — ถ้า confidence < 0.6 อย่านับเป็นจุดเสี่ยง ต้องถามย้ำ; ห้ามใส่ชื่อมาตราหรือคำว่าผิดกฎหมาย/ถูกกฎหมาย; ถ้าโมเดลอยากให้คำปรึกษา ให้ใช้ข้อความจาก `safety_guard()` แทน."
