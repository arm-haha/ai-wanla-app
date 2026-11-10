# Work-order prompts — TinySteps

ใช้ทีละข้อกับ AI codegen (Cursor / Lovable / v0 ฯลฯ). Stack แนะนำ: Next.js + Tailwind (PWA, mobile-first) + vision สำหรับจัดครอปภาพ (ไม่วินิจฉัย) + IndexedDB. ใช้ `schemas.json` เป็น type กลาง และ `reference/tinysteps.py` เป็น logic อ้างอิง (port เป็น TS ให้ผลตรงกับ tests).

**P0 — Scaffold**: สร้าง PWA ภาษาไทย mobile-first ชื่อ TinySteps ใช้ design tokens ใน prd.md (ครีม #F7EFE6, ชมพู #F2B8C6, มิ้นต์ #8FCBB3, Kanit) bottom nav: การ์ด · ไทม์ไลน์ · เติบโต · อัลบั้ม. เก็บข้อมูลใน IndexedDB ตาม `Person` / `Child`. ทุกหน้าผลลัพธ์แสดง `SafetyGuard`. ผู้ใช้ต้องยืนยันอายุ ≥ 18 และว่าเป็นผู้ปกครองก่อนใช้.

**P1 — Photo Snap**: กล้อง + กรอบนุ่ม + เตือนแสง/เบลอ/ครอป ตาม `scan_quality()`; ถ้า `ok=false` แสดง `tips_th`. Output `MilestonePhoto`, `ScanQuality`.

**P2 — Consent Guard**: port `consent_guard()` (ต้องเป็นรูปลูกตนเอง, ผู้ปกครองยืนยัน, อายุผู้ใช้ ≥ 18, ผู้ปกครองเกี่ยวข้องยินยอมก่อนแชร์). Output `ConsentGuard`.

**P3 — Milestone Card** (wow): คำนวณ `age_months(birth, photo_date)` แล้ว `milestone_card()` ให้ตรง tests (น้องภู 8 เดือน นั่งทรงตัวได้). แอนิเมชันตัวเลขเดือน + การ์ดใหญ่. Output `MilestoneCard`.

**P4 — Caption Writer**: `captions(kind, name_th, n)` ให้เลือก 1 คำบรรยาย แก้ข้อความได้ก่อนบันทึก. Output `Caption`.

**P5 — First-Moments Timeline**: เลือกจาก `FIRSTS` 8 แบบ → `log_first()` / `timeline()`; ถ้าอยู่นอกช่วงตัวอย่าง แสดง tip ให้ปรึกษาแพทย์ โดยไม่ใช้คำว่าช้า/เร็ว. Output `FirstInfo`, `LoggedFirst`, `Timeline`.

**P6 — Growth Log**: port `example_band()` / `growth_entry()`; แสดงแถบตัวอย่างและป้าย "อยู่ใน/ต่ำกว่า/สูงกว่าแถบตัวอย่างในแอป" + disclaimer. ห้ามใส่เปอร์เซ็นไทล์แพทย์. Output `ExampleBand`, `GrowthEntry`.

**P7 — Month Library + Collage**: `month_ideas(month)` และ `collage()` กริด 2×2 หรือ 3×3. Output `MonthIdeas`, `Collage`.

**P8 — Print Sheet**: `print_sheet()` เลย์เอาต์ portrait_a4 / book_20 / collage_a4 มีเส้นตัด 3 มม. Output `PrintSheet`.

**P9 — Share Card + Quota**: `share_card()` 1080×1350/1080×1920 มีลายน้ำและ disclaimer; `quota()` ฟรี 3 การ์ด/วัน. Output `ShareCard`, `Quota`.

**P10 — Safety & Privacy**: `safety_guard()` ทุกผล; ลบรูปต้นฉบับหลังทำบัตร; ห้ามเก็บใบหน้าไปเทรน; มีคำเตือนก่อนแชร์รูปเด็กในที่สาธารณะ.

**P11 — Onboarding copy**: หน้าแรกบอกชัดว่าไม่ใช่แอปแพทย์ และใช้ภาพประกอบในตัวอย่าง ไม่ใช้รูปเด็กจริง.

**P12 — Tests**: เขียน unit test TS ให้ตรงกับ `reference/tests.py` ทั้ง 41 ข้อ และ validate payload ด้วย `schemas.json`.

## AI prompts
**A1 Photo crop assist** (vision, JSON mode): "ดูรูปที่ผู้ปกครองถ่ายเพื่อทำบัตรเดือน. ตอบ JSON: glare 0–1, blur 0–1, crop 0–1, subject_centered true/false. ห้ามประเมินอายุ ห้ามวินิจฉัยพัฒนาการ ห้ามระบุโรค และห้ามเทียบกับเด็กคนอื่น. ถ้าไม่ใช่รูปที่เหมาะสมกับการ์ดความทรงจำ ให้บอกสั้น ๆ ภาษาไทย."

**A2 Caption writer** (text): "จากชนิดครั้งแรกและชื่อเล่นใน JSON เขียนคำบรรยายภาษาไทย ≤ 2 ประโยค น้ำเสียงอบอุ่น ไม่เปรียบเทียบกับเด็กคนอื่น ห้ามใช้คำว่าช้า เร็ว ผิดปกติ เก่งกว่า หรือพัฒนาการล่าช้า. ถ้ามีข้อความใน CAPTION_BANK ให้ใช้เป็นแนว."

**A3 Card composer** (image/layout): "จัดเป็นการ์ดตาม MilestoneCard: ชื่อ, เดือนที่, ชื่อครั้งแรก, คำบรรยาย, disclaimer ด้านล่าง. โทนครีม-ชมพู. ห้ามใส่โลโก้คลินิกหรือกราฟแพทย์."

**A4 Timeline copy** (text): "สรุปไทม์ไลน์ครั้งแรกเป็นภาษาไทยสั้น ๆ ตามลำดับเดือน ห้ามตีความว่าช้าหรือเร็ว."

**A5 Medical-overclaim guard**: "ตรวจ A2/A4 — ถ้ามีคำว่า วินิจฉัย, เปอร์เซ็นไทล์แพทย์, ช้า, เร็ว, ผิดปกติ, โรค ให้แทนที่ด้วยข้อความจาก `safety_guard()` และแถบตัวอย่างเท่านั้น."
