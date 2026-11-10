# Work-order prompts — FitDeck

ใช้ทีละข้อกับ AI codegen (Cursor / Lovable / v0 ฯลฯ). Stack แนะนำ: Next.js + Tailwind (PWA, mobile-first) + vision สำหรับอ่านอุปกรณ์ + IndexedDB. ใช้ `schemas.json` เป็น type กลาง และ `reference/fitdeck.py` เป็น logic อ้างอิง (port เป็น TS ให้ผลตรงกับ tests).

**P0 — Scaffold**: สร้าง PWA ภาษาไทย mobile-first ชื่อ FitDeck ใช้ design tokens ใน prd.md (กรม #0F172A, เขียว #22C55E, ส้ม #F97316, Kanit) bottom nav: ถ่ายของ · แผน · จับเวลา · บันทึก. ทุกหน้าผลลัพธ์แสดง `SafetyGuard`.

**P1 — Gear Snap**: กล้องหลัง + กรอบมุมอุปกรณ์ + เตือนแสง/เบลอ/ครอป ตาม `scan_quality()`. Output `GearPhoto`, `ScanQuality`.

**P2 — Equipment detect** (wow): เรียก vision A1 → port `parse_gear()`. พี่กิ๊ฟ = เสื่อ + ดัมเบิล 4 กก. คุณภาพ 90. ความมั่นใจ < 0.6 ไม่นับ. Output `GearScan`.

**P3 — 20-min plan**: port `make_plan(gear, level)` ให้ตรง tests (พี่กิ๊ฟ beginner = 7 ท่า 1,200 วินาที ตามลำดับ march_warm → goblet_squat → knee_push → glute_bridge → dumbbell_row → dead_bug → stretch_close). Output `Plan`, `Move`.

**P4 — Timer cards**: port `timer_cards()` นาฬิกานับถอยหลังตาม `start_sec`/`end_sec`. Output `TimerDeck`, `TimerCard`.

**P5 — Progress log**: port `log_session()`. ทำไม่ครบหรือ feeling=stop นับเป็น stopped. Output `SessionLog`, `LogRow`.

**P6 — Safety notes**: โชว์ `safety_th` ทุกท่า และ `safety_guard(pain, dizzy, cleared)`.

**P7 — Level switch**: สลับ beginner/intermediate จากสล็อตในโค้ดอ้างอิง.

**P8 — Manual gear**: ผู้ใช้ติ๊กอุปกรณ์เองได้ถ้า OCR ผิด แล้วรันแผนชุดเดิม.

**P9 — Share Card + Quota**: `share_card()` 1080 มีลายน้ำ; `quota()` ฟรี 3 ครั้ง/วัน. Output `ShareCard`, `Quota`.

**P10 — Privacy**: ลบรูปห้องหลังจัดแผนได้ ห้ามระบุที่อยู่หรือคนในรูป.

**P11 — Empty room**: ถ้าไม่เจอของและคุณภาพต่ำ ให้ถ่ายใหม่หรือยืนยันแผนน้ำหนักตัว.

**P12 — Tests**: เขียน unit test TS ให้ตรงกับ `reference/tests.py` ทั้ง 41 ข้อ และ validate payload ด้วย `schemas.json`.

## AI prompts
**A1 Gear extract** (vision, JSON mode): "ดูรูปอุปกรณ์ออกกำลังกายในบ้าน. ตอบ JSON เป็น detections: key ใน {yoga_mat, dumbbell, resistance_band, jump_rope, chair, wall, weight_kg}, value เป็น true หรือตัวเลขกิโลกรัม, confidence 0–1. ห้ามเดายี่ห้อ ห้ามอธิบายคนในรูป. ถ้าไม่ใช่รูปอุปกรณ์ ให้บอกสั้น ๆ ภาษาไทย."

**A2 Plan narrator** (text): "จาก Plan เขียนสรุปภาษาไทย ≤ 4 บรรทัด รวมจำนวนนาที จำนวนท่า และ 2 ท่าหลัก ห้ามรับประกันผลลดน้ำหนักหรือกล้ามเนื้อ."

**A3 Timer cue** (text): "ใช้ cue_th และ safety_th จาก TimerCard ตามเดิม น้ำเสียงกระชับ."

**A4 After-session note** (text): "จาก LogRow เขียนกำลังใจสั้น ถ้า stopped ให้ย้ำว่าพักได้และอย่าฝืนเจ็บ."

**A5 Pain guard**: "ถ้าผู้ใช้บอกว่าเจ็บหรือเวียนหัว ให้ใช้ safety_guard(pain/dizzy=True) และหยุดจับเวลา."
