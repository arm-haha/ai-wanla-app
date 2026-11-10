# Work-order prompts — SpecsTry

ใช้ทีละข้อกับ AI codegen (Cursor / Lovable / v0 ฯลฯ). Stack แนะนำ: Next.js + Tailwind (PWA, mobile-first) + vision/image-edit สำหรับอ่านหน้าและวางกรอบ + IndexedDB. ใช้ `schemas.json` เป็น type กลาง และ `reference/specstry.py` เป็น logic อ้างอิง (port เป็น TS ให้ผลตรงกับ tests).

**P0 — Scaffold**: สร้าง PWA ภาษาไทย mobile-first ชื่อ SpecsTry ใช้ design tokens ใน prd.md (ครีม #F6F3EE, หมึก #1A1A1A, ทอง #C9A36A, ฟ้าอมเขียว #2A6F7F, Kanit) bottom nav: ลองแว่น · กรอบ · ไดอารี่ · ร้าน. เก็บข้อมูลใน IndexedDB ตาม `Person` / `DiaryEntry`. ทุกหน้าผลลัพธ์แสดง `SafetyGuard`.

**P1 — Face Snap**: กล้องหน้า + กรอบใบหน้าตรง + เตือนแสงสะท้อน/เบลอ/เอียง/หน้าเล็ก/ไม่เห็นตา ตาม `scan_quality()`; ถ้า `ok=false` แสดง `tips_th` และปุ่มถ่ายใหม่. Output `FacePhoto`, `ScanQuality`.

**P2 — Face Shape Scan**: เรียก vision A1 → measures + PD ประมาณ → port `face_shape()` / `face_scan()` (ความมั่นใจ < 0.6 ไม่จัดทรงหน้า ถามย้ำ). แสดงโครงหน้าและป้ายทรง. Output `FaceScan`, `FaceShape`, `Pipeline`.

**P3 — Frame Try-On Grid** (wow): image-edit วางกรอบจากคลังบนหน้า คงใบหน้าเดิม ใส่ลายน้ำ `WATERMARK`. port `overlay_tryon()` / `tryon_grid()` / `fit_score()` ให้ตรง tests (น้องเกล f01 = 96, อันดับหนึ่ง f02/f07 = 98). Output `TryOn`, `TryOnGrid`, `FitScore`.

**P4 — Size Check จาก PD**: port `size_check()` / `pd_status()` ให้ตรง tests (เกล กรอบ 132 มม. หน้า 136 มม. พอดี, PD 62 typical, ศูนย์เลนส์ห่าง 6 มม.). โชว์ป้ายชัดว่า PD จากรูปใช้ตัดเลนส์ไม่ได้. Output `SizeCheck`, `PdStatus`.

**P5 — Compare Grid**: เลือก 2–4 กรอบ → `compare_grid()`. เลื่อนเทียบซ้าย-ขวา. Output `CompareGrid`.

**P6 — Frame Library**: โหลด `FRAMES` (12) ตาม `FrameInfo`; กรองทรง/วัสดุ/ไลฟ์สไตล์; หน้ารายละเอียดมีไซซ์และความกว้างกรอบ.

**P7 — Lens Notes + Price**: port `lens_advice()` / `price_range()` / `quote_check()`; ช่องใส่ราคาร้าน → ป้าย ถูก/สมเหตุสมผล/แพง/แพงมาก + คำถาม; โปรเกรสซีฟในอายุน้อยต้องมีคำเตือน. Output `LensAdvice`, `PriceRange`, `QuoteCheck`.

**P8 — Optician Card**: port `optician_card()`; การ์ดแนวตั้ง (ทรงหน้า ไซซ์กรอบ PD ประมาณ งบ โน้ต) บันทึกเป็นรูปและปุ่มส่ง LINE. เขียนชัดว่าให้ร้านวัดจริง. Output `OpticianCard`.

**P9 — Diary**: `diary_entry()` + `diary_stats()` สถานะ wishlist/tried/bought. Output `DiaryEntry`, `DiaryStats`.

**P10 — Share Card + Quota**: `share_card()` 1080×1350/1080×1920 มีลายน้ำ; `quota()` ฟรี 3 ครั้ง/วัน. Output `ShareCard`, `Quota`.

**P11 — Safety & Privacy**: `safety_guard()` ทุกผล; ห้ามแสดงค่าสายตา; ลบเซลฟี่หลังประมวลผล; ห้ามใช้รูปคนอื่นโดยไม่ยินยอม; ห้ามโชว์ว่า "เข้ากับหน้า 100%" หรือ "ใช้ PD นี้ตัดเลนส์ได้".

**P12 — Tests**: เขียน unit test TS ให้ตรงกับ `reference/tests.py` ทั้ง 41 ข้อ และ validate payload ด้วย `schemas.json`.

## AI prompts
**A1 Face measure extract** (vision, JSON mode): "ดูเซลฟี่หน้าตรงของผู้ใช้เพื่อลองกรอบแว่น (ห้ามเป็นใบหน้าเด็กเล็ก). ตอบ JSON: undertone (warm/cool/neutral), face_fill 0–1, eyes_visible 0–1, glare 0–1, blur 0–1, tilt 0–1, face_confidence 0–1, pd_mm โดยประมาณจากระยะระหว่างศูนย์กลางตา (ถ้าไม่แน่ใจให้ค่าต่ำและบอกไม่แน่ใจ), measures เป็นมม. โดยประมาณ (length_mm, forehead_mm, cheek_mm, jaw_mm). ถ้าไม่ใช่รูปหน้าตรงให้บอกสั้น ๆ ภาษาไทย. ห้ามระบุตัวบุคคล ห้ามให้ค่าสายตา."

**A2 Frame overlay** (image-edit): "วางกรอบแว่นตามคำอธิบาย/ภาพกรอบลงบนใบหน้าในรูป ให้ขาแว่นและสะพานจมูกวางตามสัดส่วนหน้า คงใบหน้า สีผิว ผม เดิม ห้ามปรับรูปหน้าหรือผิว ผลต้องเป็นภาพจำลองมีลายน้ำ ห้ามทำใหดูเหมือนถ่ายกับแว่นจริงโดยไม่มีลายน้ำ."

**A3 Fit reason writer** (text): "จาก JSON FitScore และ SizeCheck เขียนเหตุผลภาษาไทย ≤ 2 ประโยคว่าทำไมกรอบนี้เข้าหรือไม่เข้า ห้ามเปลี่ยนคะแนนหรือตัวเลขมม. ใน JSON และห้ามรับประกันว่าจะใส่สบายจริง."

**A4 Optician card writer** (text): "จาก JSON OpticianCard เขียนข้อความถึงร้านแว่นภาษาไทยสุภาพ ≤ 8 บรรทัด รวมทรงหน้า ไซซ์กรอบ และงบ ต้องมีประโยคที่บอกว่า PD จากแอปเป็นค่าประมาณ ห้ามใช้ตัดเลนส์ ต้องวัดที่ร้าน ห้ามใส่ค่าสายตา."

**A5 Over-confidence guard**: "ตรวจ output ของ A1 — ถ้า face_confidence < 0.6 ห้ามจัดทรงหน้า ต้องถามย้ำ; ถ้า PD นอกช่วง 54–74 มม. ให้ใช้ข้อความ `pd_status()` และห้ามส่งต่อให้ขั้นตอนตัดเลนส์; ห้ามสร้างหรือเดาค่าสายตา (SPH/CYL/AXIS) เด็ดขาด."
