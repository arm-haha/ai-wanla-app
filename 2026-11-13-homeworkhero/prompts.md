# Work-order prompts — HomeworkHero

ใช้ทีละข้อกับ AI codegen (Cursor / Lovable / v0 ฯลฯ). Stack แนะนำ: Next.js + Tailwind (PWA, mobile-first) + vision/OCR สำหรับอ่านใบงาน + IndexedDB. ใช้ `schemas.json` เป็น type กลาง และ `reference/homeworkhero.py` เป็น logic อ้างอิง (port เป็น TS ให้ผลตรงกับ tests). **ห้ามมีหน้าผลลัพธ์ที่โชว์คำตอบของการบ้านที่สแกนมาเป็นค่าเริ่มต้น.**

**P0 — Scaffold**: สร้าง PWA ภาษาไทย mobile-first ชื่อ HomeworkHero ใช้ design tokens ใน prd.md (ชอล์ก #E7F0E8, หมึก #1B2430, เหลือง #E7B00C, ฟ้า #2B6CB0, Kanit) bottom nav: สแกน · คำใบ้ · ข้อฝึก · ความก้าวหน้า. เก็บข้อมูลใน IndexedDB ตาม `Person` / `ProgressEntry`. ทุกหน้าแสดง `SafetyGuard`.

**P1 — Page Snap**: กล้องหลัง + กรอบใบงาน + เตือนแสงสะท้อน/เบลอ/เอียง/โจทย์ไม่เต็มกรอบ ตาม `scan_quality()`; ถ้า `ok=false` แสดง `tips_th`. Output `HomeworkPhoto`, `ScanQuality`.

**P2 — Homework Scan**: เรียก vision A1 → แม่แบบ + ช่องข้อมูล + วิชา/ระดับ → port `homework_scan()` (ความมั่นใจ < 0.6 ถามย้ำ ห้ามเดินเครื่องคำใบ้). Output `HomeworkScan`, `Pipeline`.

**P3 — Step Hints** (wow): port `step_hints()` ให้ตรง tests (โจทย์ 800 บาท ลด 25%: คำใบ้ 1–2 **ไม่มี** 200 หรือ 600, คำใบ้ 3 มีช่องว่าง). เปิดทีละระดับด้วยปุ่ม "ยังคิดไม่ออก". ห้ามมีปุ่ม "ดูคำตอบ" บนหน้านี้. Output `StepHints`.

**P4 — Parent Script + mistakes**: port `parent_script()` / `common_mistakes()`. แสดงประโยคถามและจุดที่มักผิด. Output `ParentScript`, `CommonMistakes`.

**P5 — Similar Practice**: port `similar_practice()` ข้อละตัวเลข คนละของกับงานที่สแกน; วิธีคิดมีช่องว่าง; `answer_key` ซ่อนหลังเกตผู้ปกครอง (PIN สั้นหรือยืนยัน "ฉันเป็นผู้ปกครอง"). Output `SimilarPractice`.

**P6 — Curriculum catalog**: โหลด 10 แม่แบบและ 12 ระดับตาม `TemplateInfo` / `LevelInfo`. ป้ายชัดว่าเป็นตัวอย่าง ไม่ใช่ตัวชี้วัด สพฐ.

**P7 — Timebox**: port `timebox()` ให้ตรง tests (20 นาที ใช้ 7 นาที คำใบ้ 1 ระดับ → "เก่งมากที่พยายามเอง"). Output `Timebox`.

**P8 — Progress Log**: `progress_entry()` + `progress_stats()`. ไม่บันทึกคำตอบของงานที่สแกน. Output `ProgressEntry`, `ProgressStats`.

**P9 — Teacher Note**: port `teacher_note()` ส่ง LINE โดย **ห้ามใส่คำตอบ** ในข้อความ. Output `TeacherNote`.

**P10 — Share + Quota**: `share_card()` มีลายน้ำ; `quota()` ฟรี 3 ครั้ง/วัน. Output `ShareCard`, `Quota`.

**P11 — Safety & Privacy**: `parent_reveal()` ซ่อนหลังเกต; `safety_guard(True)` เมื่อเปิด; ลบรูปใบงานหลังประมวลผล; ห้ามเก็บชื่อจริงของเด็ก/โรงเรียนถ้าไม่จำเป็น; ห้ามโหมด "ทำข้อนี้ให้ฉัน".

**P12 — Tests**: เขียน unit test TS ให้ตรงกับ `reference/tests.py` ทั้ง 41 ข้อ โดยเฉพาะ `test_hints_do_not_leak_noon_answer` และ `test_all_templates_hints_safe` และ validate ด้วย `schemas.json`.

## AI prompts
**A1 Worksheet extract** (vision, JSON mode): "ดูรูปใบงาน/สมุดที่ผู้ปกครองถ่าย (ห้ามมีใบหน้าเด็กเป็นจุดโฟกัส). ตอบ JSON: subject ใน {math, thai, sci, eng}, level ใน {p1..p6, m1..m6}, template ถ้าเข้ากับแม่แบบที่ให้, fields ตามแม่แบบ, confidence 0–1, glare blur tilt text_fill 0–1. ห้ามใส่คำตอบของโจทย์ใน JSON. ถ้าอ่านไม่ออกให้ confidence ต่ำและอย่าเดา. ห้ามระบุชื่อเด็กหรือโรงเรียน."

**A2 Hint writer** (text): "จาก JSON StepHints เขียนคำใบ้ภาษาไทยสุภาพสั้น ห้ามเพิ่มตัวเลขคำตอบ ห้ามคำนวณช่องว่างให้ ถ้าโจทย์มีตัวเลข ให้คงตัวเลขจากโจทย์เท่านั้น. น้ำเสียงเป็นโค้ช ไม่ใช่ครูดุ."

**A3 Parent script writer** (text): "จาก JSON ParentScript เขียนบทพูดสั้น ๆ ให้ผู้ปกครอง ห้ามใส่คำตอบ เน้นคำถามที่ให้ลูคอธิบายวิธีคิด."

**A4 Practice writer** (text): "จาก JSON SimilarPractice สร้างโจทย์ภาษาไทยที่ใช้ตัวเลขใน fields เท่านั้น อย่าใส่คำตอบในโจทย์. คำตอบอยู่ใน answer_key ซึ่งห้ามพิมพ์ในโจทย์."

**A5 Over-confidence / no-answer guard**: "ตรวจ output ของ A1–A4 — ถ้ามีตัวเลขหรือคำที่ตรงกับคำตอบสุดท้ายของโจทย์ที่สแกน ให้ลบออกแล้วใช้ข้อความจาก `step_hints()` แทน; ห้ามมีโหมดแก้โจทย์สำเร็จรูป; ถ้า confidence < 0.6 ต้องถามย้ำผู้ปกครอง."
