# Work-order prompts — InterviewAce

ใช้ทีละข้อกับ AI codegen (Cursor / Lovable / v0 ฯลฯ). Stack แนะนำ: Next.js + Tailwind (PWA, mobile-first) + speech-to-text สำหรับถอดเสียง + IndexedDB. ใช้ `schemas.json` เป็น type กลาง และ `reference/interviewace.py` เป็น logic อ้างอิง (port เป็น TS ให้ผลตรงกับ tests).

**P0 — Scaffold**: สร้าง PWA ภาษาไทย mobile-first ชื่อ InterviewAce ใช้ design tokens ใน prd.md (กรมท่า #101828, ฟ้า #38BDF8, เขียว #34D399, อำพัน #F5C84C, Kanit) bottom nav: ซ้อม · คะแนน · คลังคำถาม · แบบฝึก. เก็บประวัติใน IndexedDB ตาม `Person`. ทุกหน้าผลลัพธ์แสดง `SafetyGuard`.

**P1 — Role Question Bank**: โหลด `ROLES` ตาม `RoleInfo` ให้เลือกตำแหน่ง แล้วสุ่มหรือไล่ `question_card(role, index)`. Output `RoleInfo`, `QuestionCard`.

**P2 — Answer capture**: อัดเสียงหรือพิมพ์คำตอบ จับเวลาเป็นวินาที ถอดเสียงเป็นข้อความที่มีช่องว่างระหว่างคำ (หรือตัดคำก่อนส่งเข้า logic).

**P3 — Voice Answer Scoring** (wow): port `score_answer(transcript, duration_sec)` ให้ตรง tests (น้องกันต์ = รวม 72, โครง 80, ความชัด 62, ความยาว 72, STAR 75, พร้อมปานกลาง). แอนิเมชันเข็ม 4 แกนแล้วโชว์คะแนนรวมใหญ่. Output `AnswerScore`.

**P4 — Filler-Word Counter**: port `filler_count()` ไฮไลต์คำว่า อ่า เอ่อ คือ ก็ แบบ ในข้อความ. Output `FillerCount`.

**P5 — STAR flags + rewrite**: แสดง `star_flags()` ช่องที่ขาด และฟอร์ม `star_rewrite()` ให้ผู้ใช้เติมสี่ส่วน. Output `StarFlags`, `StarRewrite`.

**P6 — Confidence Report**: `confidence_report()` แสดงทิปตามจุดอ่อน. Output `ConfidenceReport`.

**P7 — Timer + Drills**: โชว์เป้า 75 วินาที / 100 คำ และ `drill(focus)` ตามแกนที่ต่ำสุด. Output `Drill`.

**P8 — History**: เก็บคะแนนรายคำถาม ดูแนวโน้มรวม (ไม่ทำเป็นใบรับรอง).

**P9 — Share Card + Quota**: `share_card()` 1080×1350/1080×1920 มีลายน้ำและ disclaimer; `quota()` ฟรี 3 คำตอบ/วัน. Output `ShareCard`, `Quota`.

**P10 — Safety & Privacy**: `safety_guard()` ทุกผล; ลบไฟล์เสียงหลังถอดข้อความ; ห้ามอ้างว่าได้งานหรือผ่านสัมภาษณ์.

**P11 — Onboarding copy**: หน้าแรกบอกชัดว่าเป็นการซ้อม ไม่ใช่คะแนนจากบริษัทจริง พร้อมตัวอย่างมิเตอร์ 72 (ภาพประกอบ).

**P12 — Tests**: เขียน unit test TS ให้ตรงกับ `reference/tests.py` ทั้ง 41 ข้อ และ validate payload ด้วย `schemas.json`.

## AI prompts
**A1 Speech to spaced Thai** (speech/text): "ถอดเสียงคำตอบสัมภาษณ์เป็นภาษาไทย และใส่ช่องว่างระหว่างคำให้ logic นับคำได้. คงคำเติมอย่าง อ่า เอ่อ แบบ ไว้ ห้ามเก็บสวยจนหาย. ห้ามเติมประวัติที่ผู้ใช้ไม่ได้พูด."

**A2 STAR extract** (text): "จากคำตอบ ดึงประโยคที่ใกล้ สถานการณ์ งานที่ได้รับ สิ่งที่ทำ ผลลัพธ์. ถ้าส่วนไหนไม่มี ให้เว้นว่าง ห้ามแต่งผลลัพธ์หรือตัวเลขที่ไม่มีในคำตอบ."

**A3 STAR rewrite writer** (text): "เขียนคำตอบใหม่สี่ประโยคตาม JSON StarRewrite น้ำเสียงสุภาพ กระชับ ห้ามเปลี่ยนตัวเลขในผลลัพธ์ และห้ามสัญญาว่าจะได้งาน."

**A4 Coach tip writer** (text): "จาก ConfidenceReport เขียนทิป 1–2 ข้อภาษาไทย ไม่ห้วน ไม่ดูถูก และไม่รับประกันผลสัมภาษณ์จริง."

**A5 Over-claim guard**: "ตรวจ A3/A4 — ห้ามใช้คำว่า รับประกัน, ได้งานแน่, ผ่านรอบนี้แน่นอน. ถ้าคะแนนในข้อความไม่ตรง JSON ให้ใช้ headline จาก `score_answer()` แทน."
