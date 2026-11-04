# Work-order prompts — MemoryFix

ใช้ทีละข้อกับ AI codegen (Cursor / Lovable / v0 ฯลฯ). Stack แนะนำ: Next.js + Tailwind (PWA, mobile-first) + API route เรียก vision model / image-restore model. ใช้ `schemas.json` เป็น type กลาง และ `reference/memoryfix.py` เป็น logic อ้างอิง (port เป็น TS ให้ผลตรงกับ tests).

**P0 — Scaffold**: สร้าง PWA ภาษาไทย mobile-first ชื่อ MemoryFix ใช้ design tokens ใน prd.md (ครีม #F6F0E6, ซีเปีย #8B5E3C, ทอง #D9A441, ปุ่ม #C2410C, Noto Serif/Sans Thai) bottom nav: อัลบั้ม · สแกน · ไทม์ไลน์ · คน. เก็บข้อมูลใน IndexedDB ตาม `Photo`.

**P1 — Scan & Fix Angle**: หน้ากล้อง + overlay กรอบ 4 มุม. เรียก AI ตาม prompt A1 ได้ `ScanExtract`. ถ้า `photo_found=false` แสดง `retake_reason_th`. ถ้า `glare=true` ขอช็อตที่สองเอียงต่าง ~15° แล้วรวมภาพ. ใช้ `corners` ทำ perspective warp (canvas/OpenCV.js).

**P2 — Damage Score**: port `damage_score()` (น้ำหนัก scratches .25 fading .20 tears .25 blur .15 stains .15) แสดงเกจ 0–100 + ป้ายระดับไทย + 5 แถบย่อย. Output `DamageReport`.

**P3 — Restore pipeline**: port `restore_plan()` + `upscale_factor()`. รัน step ตามลำดับ STEPS เรียก image model (prompt A2) แสดง progress ทีละ step พร้อมไอคอน. หลังเสร็จทำ identity check (A4); ถ้า fail ใช้ผลที่ข้าม face_enhance. Output `RestoreJob`.

**P4 — Before/After slider** (wow): สไลเดอร์ลากแนวตั้ง, ปุ่ม "เล่นอัตโนมัติ" กวาดซ้าย→ขวา 2 วิ (ไว้ถ่าย Reel), ซูมนิ้ว 2 นิ้วเทียบจุดเดียวกัน.

**P5 — Colorize**: toggle สี/ขาวดำ, ป้าย "สีเดาโดย AI" ติดมุมเสมอ, ปรับความอิ่มสีได้.

**P6 — Print & Gift Export**: port `print_options()` แสดง 4 การ์ดขนาด เขียว/แดงตาม ok + dpi. ปุ่ม Save HD, Share card ตาม `share_card()` (1080×1920 + 1080×1350) มีลายน้ำ "AI restored · MemoryFix".

**P7 — Family Timeline**: port `timeline()` แสดงตามยุค พ.ศ., แก้ปีเองได้, รูปไม่ทราบปีไว้ท้าย.

**P8 — People & Then/Now**: แท็กคนบนหน้า (กดหน้า → เลือกชื่อ), `people_index()`; Then&Now ถ่ายรูปปัจจุบัน → วางคู่ + `then_now_caption()` เป็นการ์ดแชร์.

**P9 — Voice Story**: อัดเสียง ≤180 วิ ผูกกับรูป ถอดความด้วย speech-to-text ไทย (A5) เล่นได้ในหน้ารูป. Output `VoiceStory`.

**P10 — Gentle Motion + Quota**: `motion_allowed()` บังคับฟอร์มยินยอมก่อน, ห้าม minor. `quota()` ฟรี 3/วัน แสดง paywall แบบสุภาพ.

**P11 — Tests**: เขียน unit test TS ให้ตรงกับ `reference/tests.py` ทั้ง 22 ข้อ และ validate payload ด้วย `schemas.json`.

## AI prompts
**A1 Scan extract** (vision, JSON mode, ตอบตาม `ScanExtract`):
"คุณคือผู้เชี่ยวชาญรูปถ่ายเก่า ดูภาพที่ผู้ใช้ถ่ายรูปกระดาษเก่าด้วยมือถือ. หา 4 มุมของตัวรูป (normalized 0–1 ตามเข็มนาฬิกาจากซ้ายบน), บอกว่ามีแสงสะท้อนไหม ขาวดำไหม จำนวนหน้าคน, ให้คะแนนความเสียหาย 0–1 ห้าด้าน (scratches, fading, tears, blur, stains), เดาปี ค.ศ. พร้อม confidence และเบาะแสยุค (ภาษาไทย). ถ้าไม่เห็นรูป ให้ photo_found=false และเหตุผลให้ถ่ายใหม่เป็นภาษาไทยสั้นๆ. ห้ามเดาตัวตนบุคคล."

**A2 Restore** (image model): "Restore this scanned vintage photograph. Remove scratches, dust, tears and stains; reduce grain; keep original composition, clothing, background and every face's identity exactly. Do not add or remove people, do not beautify, do not change age. Steps: {steps}."

**A3 Colorize**: "Colorize this black-and-white photo from around {year_est} in {country}. Natural, period-plausible muted tones, realistic skin, no neon. Keep all details unchanged."

**A4 Identity check**: เปรียบเทียบ face embedding ของแต่ละหน้า before/after (cosine ≥ 0.6 เป็นค่าเริ่มต้นที่ต้องปรับจริง) → pass/fail.

**A5 Story transcript**: "ถอดเสียงภาษาไทยตามที่พูดจริง ใส่วรรคตอน ไม่แต่งเติม ไม่สรุป."
