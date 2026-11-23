# Work-order prompts — SizeSure

> ให้ AI codegen (Cursor / Claude / v0 / Lovable ฯลฯ) ทำทีละ prompt ตามลำดับ ใช้ `schemas.json` เป็นสัญญาข้อมูล และ `reference/sizesure.py` เป็นตรรกะต้นแบบ (port เป็น TypeScript ให้ผลเท่ากับ `tests.py`)

**P0 — Scaffold**: สร้าง PWA (Next.js หรือ Vite + React + Tailwind) มือถือก่อน ภาษาไทยเป็นหลัก สลับ EN ได้ ใช้ design tokens ใน prd.md (ขาวนวล #FAFAF7 น้ำเงิน #1F2A44 เหลืองสายวัด #FFC83D เขียว #22A06B, Kanit) port `sizesure.py` → `src/logic/sizesure.ts` พร้อม unit test เทียบ `tests.py` ทั้ง 35 ข้อ

**P1 — Privacy gate**: ถามอายุ, "วัดตัวเองหรือคนที่อยู่ด้วยและยินยอม", ติ๊กยืนยัน "ใส่เสื้อผ้าพอดีตัว" → `privacy_check()`; อายุ < 18 → ซ่อนกล้อง แสดงฟอร์มกรอกสายวัด (`override` บนค่าเริ่มต้นว่าง) พร้อมภาพสอนวัดรอบอก/เอว/สะโพก. Output `PrivacyCheck`.

**P2 — Capture**: กรอกส่วนสูง → กล้องหน้า/หลัง + โครงร่างไกด์ + นับถอยหลัง 5 วิ (วางมือถือพิงผนังระดับเอว) ถ่ายหน้า แล้วหันข้าง; ประเมิน light/full_body/pose_ok/clothing/ref_visible ฝั่งเครื่อง → `photo_check()`. Output `PhotoCheck`.

**P3 — Body outline**: ใช้ MediaPipe Pose + Selfie Segmentation บนเครื่อง หาระดับอก (ใต้รักแร้), เอว (จุดแคบสุดระหว่างซี่โครงล่างกับสะโพก), สะโพก (จุดกว้างสุดรอบก้น) → วัดความกว้างหน้า/ความหนาข้างเป็นพิกเซล + height_px + a4_px; ส่งภาพย่อแบบ silhouette ให้ A1 ตรวจ nudity/people/clothing. Output `AiBodyMeasure`.

**P4 — Measurements**: `measure_body(ai, height)` → การ์ดตัวเลข + margin ± + ป้ายเตือน (scale_mismatch, loose_clothes); แอนิเมชันสายวัดพันรอบโครงร่างกราฟิก (ห้ามแสดงรูปถ่ายจริงซ้ำ) ลบรูปต้นฉบับทันที; ปุ่ม "แก้ด้วยสายวัด" → `override()`. Output `Measurements`.

**P5 — Chart reader (A2)**: เลือกรูปตารางไซซ์จากแกลเลอรี/แคปจอ → A2 → `AiChartRead` → `normalize_chart()`; แสดงตารางที่แปลงแล้วพร้อมป้าย "นิ้ว → ซม." / "วางราบ ×2"; ถ้าค่ารอบอกผู้ใหญ่ < 60 ซม. และ method ไม่ใช่ flat → ถามยืนยันว่า "ร้านวัดแบบวางราบไหม?". Output `SizeChart`.

**P6 — Size Pick + Fit Meter**: ชิปเลือก kind/fit/stretch → `recommend()` → ไซซ์ตัวใหญ่ + ไซซ์สำรอง + แถบมิเตอร์รายจุด (เขียวพอดี/ส้มคับ/ฟ้าหลวม) + ease ซม. + ความมั่นใจ + advice_th. Output `SizeRecommendation`.

**P7 — Shoe on A4**: ไกด์ "วางกระดาษ A4 ชิดผนัง ส้นเท้าชิดผนัง ถ่ายจากด้านบนตรง ๆ" → หา a4_px (ด้านยาว) + foot_px + width_px → `shoe_size()`. Output `ShoeSize`.

**P8 — Passport & Gift**: `passport()` การ์ดต่อคน (โปรไฟล์หลายคนใน IndexedDB) ลิงก์แชร์แบบ "ไซซ์เท่านั้น" → ฝั่งผู้รับเปิดแล้วใช้ `gift_pick()`. Output `SizePassport`, `GiftPick`.

**P9 — Return-Risk & Log**: ก่อนกด "ไปร้านค้า" แสดง `return_risk(rec, converted, reviews)` (ผู้ใช้เลือกว่ารีวิวบอกอะไร); บันทึก `LogEntry` → `log_summary()` สวิตช์ซ่อนตัวเลข + เตือนวัดใหม่ก่อน 11.11/12.12. Output `ReturnRisk`, `LogSummary`.

**P10 — Share / Reel**: `share_card()` 1080×1350 3 เลย์เอาต์ ไม่มีตัวเลขสัดส่วน ไม่มีรูปตัว ลายน้ำ "SizeSure · AI วันละแอป"; `reel_plan()` → canvas 1080×1920 6 ช็อต 120 BPM ใช้โครงร่างกราฟิก → MediaRecorder.

**P11 — Quota / Guard**: `quota()` ฟรีวัด 3 ครั้ง/วัน; `safety_guard()` ทุก flag; ข้อความเตือน medical_use เมื่อผู้ใช้เลือกหมวด "ชุดพิธี/ชุดแต่งงาน".

**P12 — QA**: รัน `reference/tests.py` (35 tests) และ validate output ทุกตัวกับ `schemas.json`; ทดสอบกับอาสาสมัครหลายรูปร่าง/ส่วนสูงเทียบสายวัด, เสื้อหลวม, ห้องมืด, มือถือเอียง, ตารางนิ้ว/ซม./วางราบ/ค่าช่วง, รองเท้าเท้ากว้าง, อายุ 15 (ต้องไม่เปิดกล้อง), รูปไม่ใส่เสื้อ (ต้อง stop).

## AI prompts

**A1 — Photo checker (vision, JSON only)**
```
คุณคือผู้ตรวจรูปของแอป SizeSure ดูรูปหน้าตรงและด้านข้าง (ภาพ silhouette ย่อ) แล้วตอบ JSON เท่านั้น:
{people: จำนวนคน, nudity: true ถ้าไม่ใส่เสื้อผ้าหรือใส่แค่ชุดชั้นใน, clothing: fitted|normal|loose|bulky, pose_ok: ยืนตรงแขนกางเล็กน้อยไหม,
 a4_visible: เห็นกระดาษ A4 ครบไหม, confidence 0..1}
ห้ามประเมินรูปร่าง ห้ามบอกว่าอ้วน/ผอม ห้ามเดาน้ำหนัก อายุ หรือตัวตน
```
**A2 — Size-chart reader (vision, JSON only)**
```
อ่านรูปตารางไซซ์จากร้านค้า ตอบ JSON ตาม schema AiChartRead เท่านั้น
- unit: cm หรือ inch (ดูหัวตาราง เช่น "นิ้ว", "in", "ซม.")
- method: flat ถ้าเขียน "วัดแบบวางราบ", "อก (วางราบ)", "ครึ่งรอบ", "1/2"; body ถ้าเป็น "สัดส่วนผู้สวมใส่"; garment ถ้าเป็น "รอบอกเสื้อ" เต็มรอบ
- rows: [{label, values: {chest, waist, hip, length, shoulder, sleeve, inseam}}] ค่าเดี่ยวหรือ [ต่ำ, สูง]
ถ้าไม่แน่ใจ method ให้ใส่ "garment" และเพิ่ม shop_th ว่า "ไม่แน่ใจวิธีวัด"; ห้ามเติมไซซ์ที่ไม่มีในรูป
```
**A3 — Advice writer**: "จาก SizeRecommendation เขียนคำแนะนำ 1–2 บรรทัดภาษาไทยเป็นกันเอง โทษ 'เสื้อ' ไม่โทษ 'ตัว' (เช่น 'ไซซ์นี้คับที่สะโพก' ไม่ใช่ 'สะโพกคุณใหญ่') ห้ามเปลี่ยนไซซ์หรือตัวเลข ห้ามพูดถึงน้ำหนัก/ลดน้ำหนัก"
**A4 — Shop chat helper**: "เขียนข้อความแชตถามร้าน (สุภาพ สั้น) พร้อมสัดส่วน <chest/waist/hip ซม.> ถามว่า <ไซซ์ A หรือ B> เหมาะกว่าไหม และเปลี่ยนไซซ์ได้หรือไม่ ไม่แนบรูป"
**A5 — Log nudge**: "จาก LogSummary เขียนข้อความเตือน 1 บรรทัด เช่น ชวนวัดใหม่ก่อน 12.12 ห้ามแสดงตัวเลขถ้า hidden=true ห้ามพูดถึงหุ่นหรือน้ำหนัก"
