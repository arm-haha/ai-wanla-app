# Work-order prompts — ParkPin

ใช้ทีละข้อกับ AI codegen (Cursor / Lovable / v0 ฯลฯ). Stack แนะนำ: Next.js + Tailwind (PWA, mobile-first) + vision สำหรับอ่านป้ายชั้น/เสา + IndexedDB. ใช้ `schemas.json` เป็น type กลาง และ `reference/parkpin.py` เป็น logic อ้างอิง (port เป็น TS ให้ผลตรงกับ tests). **ห้ามเก็บเลขทะเบียน.**

**P0 — Scaffold**: สร้าง PWA ภาษาไทย mobile-first ชื่อ ParkPin ใช้ design tokens ใน prd.md (ลานเข้ม #1C2430, เหลือง #F5C518, เขียว #16A34A, Kanit) bottom nav: ปักหมุด · นาฬิกา · ทางกลับ · ประวัติ. ทุกหน้าแสดง `SafetyGuard`.

**P1 — Sign Snap**: กล้องหลัง + กรอบป้ายชั้น/เสา + เตือนแสงสะท้อน/เบลอ/ทะเบียนในเฟรม ตาม `scan_quality()`. ถ้ามีป้ายทะเบียนให้เบลอทันที. Output `PinPhoto`, `ScanQuality`.

**P2 — Pin Scan**: เรียก vision A1 → ชั้น โซน สี เสา → port `pin_scan()` (ความมั่นใจ < 0.6 ถามย้ำให้เลือกเอง). Output `PinScan`, `Pipeline`.

**P3 — Save Pin + Timer** (wow): port `save_pin()` / `fee_estimate()` ให้ตรง tests (พี่เจ 14:20–16:50 = 150 นาที คิด ฿60 อีก 45 นาทีขยับเป็น ฿80). นาฬิกาเดินบนหน้าหลัก. ห้ามรับเลขทะเบียนในฟอร์ม. Output `SavedPin`, `FeeEstimate`.

**P4 — Close reminder**: port `close_reminder()` ให้ตรง tests (22:00 ตอน 16:50 เหลือ 310 นาที = ok; 21:40 = soon). Output `CloseReminder`.

**P5 — Walk-back Guide**: port `walkback_guide()` ขั้นตอนชั้น → สี → เสา. Output `WalkbackGuide`.

**P6 — Mall library**: โหลด `MALLS` (4 ลานจำลอง) ตาม `MallInfo` ปรับค่าชั่วโมง/เพดานได้โดยผู้ใช้ (ค่าตั้งต้นเป็นตัวอย่าง).

**P7 — Family Share**: port `family_share()` ส่ง LINE มี disclaimer ค่าจอดเป็นตัวอย่าง. Output `FamilyShare`.

**P8 — Lost-car mode**: port `lost_car()` จากหมุดล่าสุด. Output `LostCar`.

**P9 — History**: `history_stats()` + รายการหมุด. Output `HistoryStats`, `SavedPin`.

**P10 — Share + Quota**: `share_card()` มีลายน้ำ; `quota()` ฟรี 3 หมุด/วัน. Output `ShareCard`, `Quota`.

**P11 — Safety & Privacy**: `safety_guard(has_plate)`; เบลอทะเบียน; ห้ามช่องกรอกทะเบียน; ลบรูปหลังประมวลผล; ห้ามอ้างว่าเป็นราคาห้างจริงหรือนำทางสด.

**P12 — Tests**: เขียน unit test TS ให้ตรงกับ `reference/tests.py` ทั้ง 41 ข้อ และ validate ด้วย `schemas.json`.

## AI prompts
**A1 Sign extract** (vision, JSON mode): "ดูรูปป้ายชั้น โซน หรือเสาในลานจอดที่ผู้ใช้ถ่าย. ตอบ JSON: floor ใน {B3,B2,B1,G,1F,2F,3F,4F,5F,6F,rooftop}, zone (ตัวอักษร/ชื่อสั้น), color ใน {green,yellow,red,blue,orange,purple,white}, pillar (เช่น C-14), glare blur tilt sign_fill 0–1, confidence 0–1, has_plate true/false. ถ้ามีแผ่นป้ายทะเบียนให้ has_plate=true และห้ามคืนเลขทะเบียน. ถ้าอ่านป้ายไม่ชัดให้ confidence ต่ำ. ห้ามระบุรถหรือบุคคล."

**A2 Plate blur** (image-edit): "เบลอเฉพาะแผ่นป้ายทะเบียนในรูป เหลือป้ายชั้น เสา และสีโซนให้ชัด ห้ามเก็บหรืออ่านเลขทะเบียน."

**A3 Walkback writer** (text): "จาก JSON WalkbackGuide เขียนทางเดินกลับภาษาไทยสั้น เป็นขั้น ๆ ห้ามเปลี่ยนชั้น/เสา ห้ามชวนเดินในเลนรถ."

**A4 Family message** (text): "จาก JSON FamilyShare เขียนข้อความสั้นถึงครอบครัว รวมชั้น โซน เสา และค่าจอดอย่างคร่าว ต้องมีประโยคว่าค่าจอดเป็นตารางตัวอย่าง."

**A5 Over-confidence / plate guard**: "ตรวจ output ของ A1 — ถ้า confidence < 0.6 ห้ามบันทึกหมุดอัตโนมัติ ต้องให้ผู้ใช้เลือกชั้น/เสาเอง; ถ้า has_plate=true ต้องเบลอก่อนบันทึก และห้ามมีฟิลด์เลขทะเบียนใน JSON."
