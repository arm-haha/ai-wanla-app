# Work-order prompts — ColorMe

> ให้ AI codegen (Cursor / Claude / v0 / Lovable ฯลฯ) ทำทีละ prompt ตามลำดับ ใช้ `schemas.json` เป็นสัญญาข้อมูล และ `reference/colorme.py` เป็นตรรกะต้นแบบ (port เป็น TypeScript ให้ผลเท่ากับ `tests.py`)

**P0 — Scaffold**: สร้าง PWA (Next.js หรือ Vite + React + Tailwind) มือถือก่อน ภาษาไทยเป็นหลัก สลับ EN ได้ ใช้ design tokens ใน prd.md (ครีม #FFF8EC กรมท่า #1F2A44 เหลืองดินสอ #FFC83D ส้ม #F78C28, Kanit + Sarabun) port `colorme.py` → `src/logic/colorme.ts` พร้อม unit test เทียบ `tests.py` ทั้ง 36 ข้อ (fixture รูปแมว `cat_photo()` port ด้วย LCG เดียวกัน)

**P1 — Profiles & level**: โปรไฟล์ลูกหลายคน (ชื่อเล่น, อายุ, อวาตาร์สัตว์ ไม่ใช้รูปหน้า) → `level_for_age()`; อายุ < 3 → `safety_guard("under_3")`; ตั้งค่าผู้ปกครอง (PIN 4 หลัก) เปิด parent mode. Output `Child`, `Level`.

**P2 — Pick photo & QA**: เลือกจากคลังรูป/กล้อง → ครอปสี่เหลี่ยม/แนวตั้ง → วัด light/sharp/subject/busy บนเครื่อง → `photo_check()` + tips. Output `PhotoInput`, `PhotoCheck`.

**P3 — Clean & guard (A1)**: ส่งภาพย่อ (≤ 512 px) ให้ A1 → `AiPhotoClean` → `privacy_check(own_photo, parent_mode, found)`; stop → ข้อความไทยจาก `GUARD`; background "simplify/remove" → ลบพื้นหลังบนเครื่อง (MediaPipe Selfie/Interactive Segmenter หรือ ONNX u2net) แทนด้วยฟ้า/พื้นเรียบ. Output `AiPhotoClean`, `PrivacyCheck`.

**P4 — Make page**: ย่อเป็น working grid (ด้านยาว 64–120 px ตามระดับ) → `make_page(pic, age, mode)` → แปลง grid เป็นเส้นเวกเตอร์เรียบ (marching squares ต่อช่อง + Chaikin smoothing) ความหนา `line_px` สเกลไป 300 dpi; แอนิเมชัน "เส้นวาดเอง" + สีจางหาย (wow). Output `ColoringPage`, `Palette`.

**P5 — Colour-by-number view**: แสดงเลขที่ `labels[].x/y` (สเกลจาก grid), `fits=false` → เลขเล็กนอกช่อง + ลูกศร; legend เป็นวงกลมสีเทียน + ชื่อไทย; ระบายบนจอได้ (แตะช่อง = เติมสี, โหมดพู่กันสำหรับ calm) + undo. Output `LegendItem`, `RegionLabel`.

**P6 — Booklet PDF**: เลือก 1–12 หน้า → `booklet(pages, name, ink_saver)` → pdf-lib A4 300 dpi: ปก "สมุดระบายสีของ<ชื่อ>" + หน้า + หน้าเฉลย (ภาพสีย่อ) ถ้ามีโหมดเลข; แสดงประมาณหมึกและจำนวนแผ่น. Output `Booklet`.

**P7 — Dot-to-dot**: โครงร่าง subject (contour ของ mask ที่ simplify ด้วย Douglas–Peucker → 8–20 จุด, normalize 0..100) → `dot_to_dot(points, age)` → หน้า A4 จุด + เลข. Output `DotPage`, `Dot`.

**P8 — Scan & Magic Reveal**: กล้องถ่ายหน้าที่ระบายแล้ว → หา 4 มุมกระดาษ + perspective warp (OpenCV.js) → ตัดขอบตามกรอบรูป → ย่อเป็น grid เดียวกับ page → แต่ละเซลล์: ขาว/เทาอ่อน = None, ไม่งั้น `nearest()` → `progress_check(page, scan)` → ดาว + คำชม + สไลด์ก่อน/หลัง (รูปต้นฉบับ ↔ ผลงาน). Output `Progress`.

**P9 — Quest & gallery**: `quest(today, history)` บนหน้า Home + ป้ายสติกเกอร์ใหม่; บันทึก `GalleryEntry` ทุกครั้งที่สแกน → `gallery_summary(entries, month)` → ปุ่ม "ทำสมุดผลงานเดือนนี้" เมื่อ `art_book_ready`. Output `Quest`, `GalleryEntry`, `GallerySummary`.

**P10 — Share / Reel**: `share_card()` 1080×1350 3 เลย์เอาต์ ซ่อนหน้าเด็กทุกกรณี (blur/สติกเกอร์ทับใบหน้าที่ตรวจพบ) ลายน้ำ "ColorMe · AI วันละแอป"; `reel_plan()` → canvas 1080×1920 6 ช็อต 110 BPM → MediaRecorder. Output `ShareCard`, `ReelPlan`.

**P11 — Quota / Guard**: `quota()` ฟรี 5 หน้า/วัน; `safety_guard()` ทุก flag; ตัวจับเวลา 30 นาทีบนจอ → `safety_guard("screen_time")` ชวนไประบายบนกระดาษ; ปุ่มพิมพ์ขายถูกซ่อนถ้า copyright_character.

**P12 — QA**: รัน `reference/tests.py` (36 tests) และ validate output ทุกตัวกับ `schemas.json`; ทดสอบรูปสัตว์เลี้ยงขนฟู, ของเล่นหลายชิ้น, วิวทะเล, รูปมืด, รูปเบลอ, รูปลายทาง (ต้องลดรายละเอียด), บัตรประชาชน (ต้อง stop), ตัวการ์ตูนลิขสิทธิ์ (warn), สแกนกระดาษเอียง/แสงเหลือง.

## AI prompts

**A1 — Photo cleaner & safety (vision, JSON only)**
```
คุณคือผู้ช่วยของแอป ColorMe ที่แปลงรูปเป็นหน้าระบายสีสำหรับเด็ก ดูรูปแล้วตอบ JSON ตาม schema AiPhotoClean เท่านั้น:
{subject_th: สิ่งหลักในรูปสั้น ๆ, background: keep|simplify|remove (remove ถ้าพื้นหลังรกและไม่สำคัญ),
 people: จำนวนคน, child_faces: จำนวนหน้าเด็กที่เห็นชัด, nudity, id_document (บัตร/สลิป/เอกสารที่มีข้อมูลส่วนตัว), violent,
 copyright_character (ตัวการ์ตูน/มาสคอต/โลโก้ที่มีเจ้าของ), suggested_title_th: ชื่อหน้าน่ารัก ≤ 20 ตัวอักษร, confidence 0..1}
ห้ามเดาตัวตน อายุ หรือชื่อจริงของใคร ห้ามบรรยายรูปร่างหน้าตาคน
```
**A2 — Page title & story starter**: "จาก subject_th และธีมภารกิจวันนี้ เขียนชื่อหน้าระบายสี ≤ 20 ตัวอักษร + ประโยคชวนระบาย 1 บรรทัดสำหรับเด็ก <อายุ> ขวบ เช่น 'วันนี้น้องส้มจี๊ดอยากได้ผ้าพันคอสีอะไรดีนะ?' ห้ามใช้ชื่อตัวการ์ตูนลิขสิทธิ์"
**A3 — Praise writer**: "จาก Progress เขียนคำชม 1–2 บรรทัดภาษาไทยสำหรับเด็ก ชมความพยายามและสีที่เลือก (favorite) ห้ามพูดว่าผิด/ไม่สวย/แพ้ ห้ามเปรียบเทียบกับเด็กคนอื่น ห้ามเปลี่ยนจำนวนดาว ถ้ายังไม่เสร็จให้ชวนระบายต่อแบบสนุก"
**A4 — Parent tip**: "จาก Progress (coverage, in_lines, match) เขียนทิปสั้น ๆ ให้ผู้ปกครอง 1 บรรทัด เช่น ฝึกจับดินสอ/ระบายในเส้น/จำเลขกับสี ใช้น้ำเสียงอบอุ่น ไม่ตัดสินเด็ก"
**A5 — Quest nudge**: "จาก Quest เขียนข้อความชวนระบายประจำวัน 1 บรรทัด ใส่ theme_th และ streak (ถ้า > 0) ถ้า new_sticker ไม่ใช่ null ให้ฉลองสติกเกอร์ ห้ามกดดันหรือทำให้รู้สึกผิดถ้าขาดวัน"
