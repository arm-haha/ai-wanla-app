# Work-order prompts — NailPop

ใช้ทีละข้อกับ AI codegen (Cursor / Lovable / v0 ฯลฯ). Stack แนะนำ: Next.js + Tailwind (PWA, mobile-first) + on-device hand landmarks (MediaPipe Hands) + nail segmentation model (เช่น YOLOv8-seg ที่เทรนชุดเล็บ) + image-edit/inpaint API ที่รองรับ mask สำหรับทาลาย. ใช้ `schemas.json` เป็น type กลาง และ `reference/nailpop.py` เป็น logic อ้างอิง (port เป็น TS ให้ผลตรงกับ tests).

**P0 — Scaffold**: สร้าง PWA ภาษาไทย mobile-first ชื่อ NailPop ใช้ design tokens ใน prd.md (ครีม #FFF7F3, ชมพูนู้ด #F9D5DC, ink #2A1E22, accent #E8457A, ทอง #C9A24D, Kanit) bottom nav: ลองเล็บ · ไดอารี่ · เทศกาล · ตั้งค่า. เก็บข้อมูลใน IndexedDB ตาม `Person` / `DiaryEntry`.

**P1 — Hand Snap**: กล้องหลัง + กรอบมือ + เตือนแสง/เบลอ/เอียง ตาม `scan_quality()`; ถ้า `ok=false` แสดง `tips_th` และปุ่มถ่ายใหม่. Output `HandPhoto`.

**P2 — Nail Detect + Measure**: hand landmarks → crop แต่ละปลายนิ้ว → segment เล็บ → วัด width/bed/free edge (mm โดยสเกลจากความกว้างนิ้ว) + taper + corner_round → port `detect_nail()` / `hand_scan()` ให้ตรง tests (มายด์ = เหลี่ยมมน กลาง Q84). Output `NailDetect`, `HandScan`, `Pipeline`.

**P3 — Try-On Grid 9** (wow): port `fit_score()` / `try_on_grid()`; render ทีละช่อง (แสดง skeleton แล้วค่อย ๆ เติมภาพ) → grid 3×3 ป้าย Fit + ราคา; แตะเปิด Before/After slider. Render ด้วย prompt A2 เฉพาะใน mask เล็บ. Output `TryOnGrid`, `TryOnTile`.

**P4 — Skin-Tone Match**: ควิซ 3 ข้อแบบการ์ดปัด + สุ่มสีผิวจากหลังมือ (ค่าเฉลี่ย patch นอก mask เล็บ) → port `undertone()` + `shade_recommend()`; แสดง 5 สีที่ใช่ + สีที่ควรเลี่ยง + ปุ่ม "ลองสีนี้" ส่งเข้า grid. Output `UndertoneResult`, `ShadeRec`.

**P5 — Design Library**: โหลด `DESIGNS` (14 ลาย) จาก JSON ตาม `Design`; filter ตามเทคนิค/โอกาส/งบ; แอดมินเพิ่มลายได้ภายหลัง.

**P6 — Price + Salon Card**: port `price_estimate()` / `salon_card()`; การ์ดแนวตั้ง (รูปลาย + ทรง + ความยาว + hex + ช่วงราคา + โน้ต) บันทึกเป็นรูป และปุ่มส่ง LINE (`line_share_url`). แสดง disclaimer ราคาเสมอ. Output `PriceEstimate`, `SalonCard`.

**P7 — Friend Vote**: เลือก 2–4 ลาย → `vote_link()` (anonymous, 48 ชม., ครอปเฉพาะเล็บ) → หน้าโหวตเว็บไม่ต้องล็อกอิน → `friend_vote()` แสดงผล % แบบเรียลไทม์. Output `VoteLink`, `VoteResult`.

**P8 — Nail Diary + Reminder**: `diary_entry()` + `care_reminder()` + `reminder_status()`; local notification วันเช็ก/ถึงเวลา/ควรถอด; หน้าสรุป `diary_stats()` (ค่าใช้จ่ายรวม/เฉลี่ย/ลายโปรด). Output `DiaryEntry`, `CareReminder`, `ReminderStatus`, `DiaryStats`.

**P9 — Occasion Presets**: `occasion_preset()` 6 เทศกาล; หน้า Home ดันเทศกาลที่ใกล้ที่สุด (สงกรานต์ เม.ย. · ลอยกระทง พ.ย. · ปีใหม่ ธ.ค.). Output `OccasionPreset`.

**P10 — DIY Mode**: `diy_guide()` ทีละสเต็ป มีตัวจับเวลาต่อขั้น; ลายที่ `diy_ok=false` แสดงปุ่ม "ใช้ Salon Card แทน". Output `DiyGuide`.

**P11 — Health Guard + Share + Quota**: `health_guard()` ก่อนกดทำ/จองร้าน; `share_card()` Before/After + Grid 1080×1350 / 1080×1920 มีลายน้ำ; `quota()` ฟรี 3 กริด/วัน paywall สุภาพ. Output `HealthGuard`, `ShareCard`, `Quota`.

**P12 — Tests**: เขียน unit test TS ให้ตรงกับ `reference/tests.py` ทั้ง 35 ข้อ และ validate payload ด้วย `schemas.json`.

## AI prompts
**A1 Nail & hand extract** (vision, JSON mode): "ดูรูปมือที่ผู้ใช้ถ่ายเพื่อลองทาเล็บ. ตอบ JSON: มือซ้าย/ขวา, รายการเล็บที่เห็น (finger, กรอบ normalized 0–1, ความกว้าง/ความยาวโดยประมาณเทียบความกว้างนิ้ว, taper 0–1, corner_round 0–1, free_edge ประมาณ mm), lighting 0–1, blur 0–1, tilt 0–1, และ flags สุขภาพเล็บที่เห็นชัด (lifting, redness, swelling, discoloration). ห้ามเดาตัวตน อายุ หรือวินิจฉัยโรค ถ้าไม่ใช่รูปมือคนจริงให้บอกเหตุผลสั้น ๆ ภาษาไทย."

**A2 Try-on render (inpaint ใน mask เล็บ)**: "Paint a {technique} manicure in the '{design_name_en}' style ({finish}, colors {colors}) ONLY inside the provided nail masks, following each nail's real curvature, cuticle line and highlights. Shape the free edge as {shape}, length {length}. Keep every pixel outside the masks unchanged — do not alter fingers, skin tone, jewelry or background. Photorealistic, natural reflections, no extra fingers."

**A3 Undertone hint** (vision, JSON): "จาก patch ผิวหลังมือ (ไม่รวมเล็บ) ภายใต้แสงที่ระบุ ตอบค่า RGB เฉลี่ยหลังปรับ white balance และระดับความเชื่อมั่น 0–1. ห้ามตัดสินความสวย/เชื้อชาติ."

**A4 Over-edit guard**: เทียบภาพก่อน/หลังนอก mask เล็บ (mean abs diff ≤ 2/255 เป็นค่าเริ่มต้นที่ต้องปรับจริง) และ hand landmark ต้องตรงเดิม; ถ้า fail ให้ render ใหม่หรือ composite เฉพาะ mask.

**A5 Salon note writer** (text): "เขียนโน้ตสั้นถึงช่างทำเล็บภาษาไทย สุภาพ ≤ 3 บรรทัด จาก JSON SalonCard: ลาย, ทรง, ความยาว, เทคนิค, โค้ดสี, งบประมาณ และข้อจำกัดของลูกค้า. ห้ามอ้างว่าเป็นราคาจริงของร้าน ห้ามแนะนำยาหรือการรักษา."
