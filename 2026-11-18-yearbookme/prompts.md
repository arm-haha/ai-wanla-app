# Work-order prompts — YearbookMe

ใช้ทีละข้อกับ AI codegen (Cursor / Lovable / v0 ฯลฯ). Stack แนะนำ: Next.js + Tailwind (PWA, mobile-first) + vision/image model สำหรับจัดสไตล์พอร์ตเทรต + IndexedDB. ใช้ `schemas.json` เป็น type กลาง และ `reference/yearbookme.py` เป็น logic อ้างอิง (port เป็น TS ให้ผลตรงกับ tests).

**P0 — Scaffold**: สร้าง PWA ภาษาไทย mobile-first ชื่อ YearbookMe ใช้ design tokens ใน prd.md (ครีม #F4EFE6, กรมท่า #1E3A5F, ทองจาง #C4A574, นีออน #FF2E97, Kanit) bottom nav: สตูดิโอ · หน้ารุ่น · คำคม · คลังยุค. เก็บข้อมูลใน IndexedDB ตาม `Person`. ทุกหน้าผลลัพธ์แสดง `SafetyGuard` และประตู `ConsentGuard` ก่อนแปลงรูป.

**P1 — Selfie Snap**: กล้องหน้า + กรอบหัวถึงไหล่ + เตือนแสงสะท้อน/เบลอ/ครอป ตาม `scan_quality()`; ถ้า `ok=false` แสดง `tips_th` และปุ่มถ่ายใหม่. Output `SelfiePhoto`, `ScanQuality`.

**P2 — Consent Guard**: เรียก vision A1 → `Detection[]` → port `identify_faces()` / `consent_guard()` (ไม่ใช่รูปตนเอง, บุคคลสาธารณะ, มีคนอื่นโดยไม่ยินยอม, อายุ < 13, วัยรุ่นไม่มีผู้ปกครอง = บล็อก). Output `ConsentGuard`, `PhotoScan`, `Pipeline`.

**P3 — Era Studio** (wow): port `era_score()` / `style_render()` / `era_studio()` ให้ตรง tests (น้องมายด์ = 90s 88 เข้าสุด, 80s 39, Y2K 47). เลื่อนเทียบ 3 ลุคในจอเดียว แอนิเมชันเข็มคะแนน → ป้ายยุคใหญ่ "Class of '97". Output `EraStudio`, `StyleRender`.

**P4 — Caption Quotes + Autograph**: เลือกโทน 4 แบบ → `caption_quotes(era, tone, name, n)` และ `autograph(from, to, era, tone)`; คัดลอก/บันทึกรูปการ์ดเซ็น. Output `CaptionQuote`, `Autograph`.

**P5 — Era Library + Prop Kit**: โหลด `ERAS` ตาม `EraInfo`; หน้ารายละเอียดมีโทนสี ทรงผม เสื้อผ้า; `prop_kit()` ให้เลือกพร็อป 1–2 ชิ้น. Output `EraInfo`, `PropKit`.

**P6 — Group Yearbook Page**: เพิ่มเพื่อนที่ `consented=true` เท่านั้น → `member_slot()` / `yearbook_page()`; กริด 2×2 หรือ 3×2; ไม่มีสมาชิกที่ยังไม่ยินยอม. Output `MemberSlot`, `YearbookPage`.

**P7 — Role Stickers**: แปะบทบาทจาก `ROLES` บนสล็อต (ประธานรุ่น ชมรมปีบุ๊ก เพื่อนที่ขาดไม่ได้ ฯลฯ) แก้ได้ก่อนส่งออก.

**P8 — Print Sheet**: port `print_sheet()` เลย์เอาต์ portrait_a4 / four_up / sticker มีแบบเส้นตัด 3 มม. ส่งออก PDF/รูป. Output `PrintSheet`.

**P9 — Share Card + Quota**: `share_card()` 1080×1350/1080×1920 มีลายน้ำ; `quota()` ฟรี 3 ครั้ง/วัน paywall สุภาพ. Output `ShareCard`, `Quota`.

**P10 — Safety & Privacy**: `safety_guard()` ทุกผล; ลบรูปต้นฉบับหลังแปลง; ห้ามเก็บใบหน้าไปเทรน; ไม่โชว์ว่าเป็นสมุดรุ่นจริง.

**P11 — Onboarding copy**: หน้าแรกบอกสั้น ๆ ว่าใช้รูปของตนเองเท่านั้น และมีตัวอย่างลุค 3 ยุค (ภาพวาด ไม่ใช้รูปคนจริง).

**P12 — Tests**: เขียน unit test TS ให้ตรงกับ `reference/tests.py` ทั้ง 41 ข้อ และ validate payload ด้วย `schemas.json`.

## AI prompts
**A1 Face + consent extract** (vision, JSON mode): "ดูเซลฟี่ที่ผู้ใช้ถ่าย. ตอบ JSON: จำนวนใบหน้า, รายการ detections (label, confidence 0–1, own_face ถ้าผู้ใช้บอกว่าเป็นรูปตนเอง, celebrity_likely true ถ้ามีสัญญาณว่าเป็นบุคคลสาธารณะ, age_apparent เป็นตัวเลขประมาณหรือ null ถ้าไม่ชัด), glare 0–1, blur 0–1, crop 0–1 (ยิ่งสูงยิ่งถูกตัดหัว/ไหล่). ห้ามเดาอาชีพหรือชื่อจริง. ถ้าไม่ใช่รูปคน ให้บอกสั้น ๆ ภาษาไทย. ห้ามระบุตัวตนหรือเทียบกับฐานข้อมูลคนดังเป็นรายชื่อ."

**A2 Era stylist** (image): "แปลงพอร์ตเทรตให้อยู่ในสไตล์ยุค {80s|90s|y2k} ตาม JSON StyleRender (palette, grain, flash, frame, hair_th, clothes_th, props_th). คงโครงหน้าเดิม ห้ามทำให้เด็กกว่า/แก่กว่า และห้ามเปลี่ยนเป็นคนอื่น. ไม่ใส่โลโก้โรงเรียนจริง. ถ้าเป็นยุค 90s ให้กรอบขาวปีบุ๊กและลายจุดบาง ๆ."

**A3 Quote writer** (text): "จากยุค โทน และชื่อใน JSON เขียนคำคมภาษาไทย ≤ 2 ประโยค น้ำเสียงตามโทน (sweet/funny/proud/nostalgic) ไม่ด่า ไม่พาดพิงคนจริง ไม่ใส่ชื่อโรงเรียนจริง. ถ้ามีข้อความใน QUOTE_BANK ที่ตรงโทน ให้ใช้เป็นแนว ไม่ต้องก๊อปเป๊ะถ้าไม่จำเป็น."

**A4 Yearbook page composer** (image/layout): "จัดพอร์ตเทรตตาม YearbookPage: กริด cols×rows ใส่ชื่อ ชื่อเล่น บทบาท year_label และ disclaimer ด้านล่าง. ใช้ palette ของยุค. ห้ามเติมคนที่ไม่อยู่ใน members."

**A5 Over-confidence guard**: "ตรวจ A1 — ถ้า confidence ของใบหน้า < 0.6 ให้ถามย้ำและไม่นับเป็นผล; ถ้า celebrity_likely หรือมีใบหน้าที่ own_face=false โดย all_consented=false ให้บล็อกตาม `consent_guard()` ห้ามแปลงรูป."
