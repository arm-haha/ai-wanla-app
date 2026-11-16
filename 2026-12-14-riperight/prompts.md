# Work-order prompts — RipeRight

ใช้ทีละข้อกับ AI codegen (Cursor / Lovable / v0 ฯลฯ). Stack แนะนำ: Next.js + Tailwind (PWA, mobile-first) + vision model สำหรับอ่านผลไม้ + Web Audio API (FFT บนเครื่อง) สำหรับ Knock Test + IndexedDB. ใช้ `schemas.json` เป็น type กลาง และ `reference/riperight.py` เป็น logic อ้างอิง (port เป็น TS ให้ผลตรงกับ tests).

**P0 — Scaffold**: PWA ภาษาไทย mobile-first ชื่อ RipeRight ใช้ design tokens ใน prd.md (ครีม #FFF7E6, เขียว #6BBF59, เหลือง #FFC93C, ส้ม #FF8A3D, Kanit). bottom nav: สแกน · ตะกร้า · ตลาด · ไดอารี่. ทุกหน้าผลแสดง `SafetyGuard` + disclaimer.

**P1 — Camera Scan**: กล้องเต็มจอ กรอบวงกลมเล็งผลไม้ + ปุ่มเลือกจากคลังภาพ. เช็ก `scan_quality()` ถ้า `ok=false` แสดง `tips_th`. เรียก A1 → `AiCueExtract`; ถ้า `mold_seen` → `safety_guard("mold")` ทันที; confidence < 0.7 ให้ชิปยืนยันชนิดผลไม้.

**P2 — Ripeness Meter** (wow): มิเตอร์ครึ่งวงกลม 4 โซนสี เข็มกวาดแบบ spring 0.8 วิ. ชิปตัวเลือก ความนิ่ม (hard/firm/yielding/soft/mushy) และกลิ่น (none/faint/strong) แตะแล้วเข็มขยับใหม่. port `ripeness()` ให้ตรง tests (อะโวคาโด 0.40/0.05/firm = 32 ยังดิบ 3 วัน). Output `RipenessResult`.

**P3 — Knock Test**: แสดงเฉพาะแตงโม/ทุเรียน. Web Audio จับเสียง 3 ครั้ง → FFT หา Hz เด่น + เวลาเสียงลดลง 20 dB (decay_ms) ทำบนเครื่อง ไม่อัดเก็บ. port `knock_test()` แล้วส่ง `cue` เข้า `ripeness(..., knock=cue)`. Output `KnockResult`.

**P4 — Price Check**: ช่องราคารวม + น้ำหนัก (กก.) + เดือนจากเครื่อง → `price_check()` แถบ low–high + ป้ายสี + ป้าย "ในฤดู/นอกฤดู". Output `PriceCheck`.

**P5 — Ripen Control**: 3 ปุ่ม เร่ง / ปกติ / ชะลอ → `storage_plan()` แสดง steps + ไอคอนที่เก็บ (เคาน์เตอร์/ถุงกระดาษ/ตู้เย็น). Output `StoragePlan`.

**P6 — Basket & Eat Plan**: ปุ่ม "เพิ่มลงตะกร้า" จากผลสแกน (`basket_item()`) → `eat_plan()` ตารางการ์ดรายวัน (กิน / รอ / เลยช่วงอร่อย) + แจ้งเตือนในเครื่องตอนเช้าวันที่ลูกไหนพร้อม. Output `EatPlan`.

**P7 — Pick Checklist**: เลือกผลไม้ → 4 คำถามจาก `CHECKLISTS` แบบสวิตช์ใหญ่ ๆ ใช้มือเดียวที่ตลาด → `pick_check()`. Output `PickCheck`.

**P8 — Season Calendar**: กริด 12 เดือน ไฮไลต์เดือนนี้ `season_calendar()`; กดผลไม้ดูช่วงราคาอ้างอิง. Output `SeasonCalendar`.

**P9 — Fruit Diary**: หลังผ่าแล้วถาม "พอดี / ดิบไป / สุกไป" + ราคาที่จ่าย → `DiaryEntry` → `diary_summary()` แสดง % ทายถูก. Output `DiarySummary`.

**P10 — Share Card**: `share_card()` เรนเดอร์ 1080×1350 (รูปผลไม้ + มิเตอร์ + คะแนน) ลายน้ำ "RipeRight · AI วันละแอป" + Web Share API.

**P11 — Quota & Guard**: `quota()` ฟรี 5 สแกน/วัน; `safety_guard()` ตาม flag (mold / durian_alcohol / not_fruit).

**P12 — QA**: รัน `reference/tests.py` (35 tests) และ validate output ทุกตัวกับ `schemas.json`; ทดสอบแสงตลาดกลางคืน, iPhone SE + Android จอเล็ก, ไมค์ในที่มีเสียงรบกวน.

## AI prompts
**A1 — Fruit cue extract (vision → JSON)**
```
คุณคือผู้ช่วยดูผลไม้ ดูรูปแล้วตอบเป็น JSON ตาม AiCueExtract เท่านั้น
fruit ∈ [durian, mango, avocado, banana, watermelon, papaya, pineapple, mangosteen]
color = สัดส่วนผิวที่เปลี่ยนเป็นสีสุกของผลไม้ชนิดนั้น (0 = เขียวดิบทั้งลูก, 1 = สีสุกเต็มที่)
spots = สัดส่วนจุดกระ/รอยช้ำสีน้ำตาลดำ (0–1)
mold_seen = true ถ้าเห็นรา จุดฟูขาว/เขียว หรือเนื้อแตกเยิ้ม
ถ้าไม่ใช่ผลไม้ในรายการ หรือไม่แน่ใจ ให้ confidence < 0.7 และเขียน notes_th ห้ามเดา
```
**A2 — Explain result**: "อธิบายผล RipenessResult นี้เป็นภาษาไทยเป็นกันเอง 2 บรรทัด ห้ามเปลี่ยนตัวเลข คะแนน วัน หรือระดับ และห้ามบอกว่ากินได้ปลอดภัยแน่นอน"
**A3 — Use-it-up ideas**: "ผลไม้ <fruit_th> ระดับ <stage_th> เสนอเมนูง่าย 3 อย่าง (เช่น สมูทตี้ ขนม ยำ) ใช้ของในครัวไทยทั่วไป ไม่เกิน 15 นาที"
**A4 — Market chat helper**: "เขียนประโยคสุภาพ 1 บรรทัดสำหรับขอแม่ค้าเลือกลูก/ต่อราคา จาก PriceCheck นี้ ห้ามกล่าวหาว่าแม่ค้าโกง"
**A5 — Diary insight**: "จาก DiarySummary และรายการ DiaryEntry สรุปเป็นเคล็ดลับส่วนตัว 1 ข้อ เช่น 'อะโวคาโดของคุณมักต้องรอเพิ่ม 1 วัน' ห้ามเกินข้อมูลที่มี"
