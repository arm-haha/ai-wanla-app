# Work-order prompts — SnapLingo

ใช้ทีละข้อกับ AI codegen (Cursor / Lovable / v0 ฯลฯ). Stack แนะนำ: Next.js + Tailwind (PWA, mobile-first) + vision สำหรับอ่านของในรูป + IndexedDB. ใช้ `schemas.json` เป็น type กลาง และ `reference/snaplingo.py` เป็น logic อ้างอิง (port เป็น TS ให้ผลตรงกับ tests).

**P0 — Scaffold**: สร้าง PWA ภาษาไทย mobile-first ชื่อ SnapLingo ใช้ design tokens ใน prd.md (เหลือง #FEF9C3, ฟ้า #0284C7, Kanit) bottom nav: ถ่ายของ · การ์ด · ควิซ · สติกเกอร์. โหมดผู้ปกครองเป็นค่าเริ่มต้น. ทุกหน้าผลลัพธ์แสดง `SafetyGuard`.

**P1 — Object Snap**: กล้องหลัง + กรอบของบนโต๊ะ + เตือนแสง/เบลอ/ครอป ตาม `scan_quality()`. แนะนำไม่ให้อยู่ในเฟรมกับใบหน้าเด็ก. Output `ScenePhoto`, `ScanQuality`.

**P2 — Object labels** (wow): เรียก vision A1 → port `parse_scene()` / `labels()` / `label_card()`. น้องเต้าครัว = kettle, cup, spoon คุณภาพ 89. Output `SceneScan`, `LabelSet`, `LabelCard`.

**P3 — Pronunciation**: แสดง `en_line_th` และ `zh_line_th` มีปุ่มฟัง (TTS ของเครื่อง ใช้ name_en / pinyin ไม่บันทึกเสียงเด็ก).

**P4 — Flashcards**: port `flashcards(keys, lang)` สลับ en/zh. Output `FlashDeck`, `FlashCard`.

**P5 — Mini quiz**: port `mini_quiz()` 3 ตัวเลือก ตำแหน่งคำตอบสลับตามดัชนีคำ. เดโมตอบ [kettle, kettle, spoon] = ถูก 2/3 (67%). Output `MiniQuiz`, `QuizQuestion`, `Choice`.

**P6 — Streak rewards**: port `progress(prev, quiz)`. ถูก ≥ 50% ต่อสตรีค ได้สติกเกอร์ตอนครบ 3/7/14/30. Output `Progress`, `Reward`.

**P7 — Word library**: โชว์ `WORDS` 16 คำ กรองตาม topic kitchen/room/daily.

**P8 — Parent mode**: เก็บโปรไฟล์ผู้ปกครอง/เด็กตาม `Person` ในเครื่อง ไม่บังคับรูปเด็ก.

**P9 — Share Card + Quota**: `share_card()` 1080 มีลายน้ำ; `quota()` ฟรี 3 ครั้ง/วัน. Output `ShareCard`, `Quota`.

**P10 — Safety**: `safety_guard(child_face_in_frame, parent_ok)` ไม่มีผู้ปกครองยินยอม = หยุด.

**P11 — Privacy**: ลบรูปของหลังติดป้ายได้ ห้ามอัปโหลดรูปเด็กไปเทรน ห้ามให้คะแนนจากใบหน้า.

**P12 — Tests**: เขียน unit test TS ให้ตรงกับ `reference/tests.py` ทั้ง 41 ข้อ และ validate payload ด้วย `schemas.json`.

## AI prompts
**A1 Object extract** (vision, JSON mode): "ดูรูปของใช้ในบ้าน (ไม่ต้องมีคน). ตอบ JSON เป็น detections: key เลือกจากคลัง {kettle, cup, spoon, plate, fridge, rice_cooker, chair, table, book, lamp, pillow, clock, shoes, bag, toothbrush, plant}, value true, confidence 0–1. ถ้ามีใบหน้าเด็กให้ตั้ง child_face=true แต่ห้ามอธิบายใบหน้า. ถ้าไม่ใช่รูปของใช้ ให้บอกสั้น ๆ ภาษาไทย."

**A2 Label narrator** (text): "จาก LabelCard เขียนบรรทัดเดียวภาษาไทย รวมชื่อไทย อังกฤษ และจีน ตาม JSON ห้ามเปลี่ยนการออกเสียง."

**A3 Quiz writer**: "ใช้คำถามและตัวเลือกจาก MiniQuiz ตามเดิม ห้ามแต่งตัวเลือกใหม่."

**A4 Streak cheer** (text): "จาก Progress ชื่นชมสั้น ๆ ถ้าผ่าน และบอกจำนวนวันต่อเนื่อง ห้ามบอกว่าเด็กฉลาดจากใบหน้าหรือคะแนน IQ."

**A5 Child-face guard**: "ถ้าภาพมีใบหน้าเด็ก ให้ใช้ safety_guard และแนะนำให้ถ่ายเฉพาะของ."
