# Work-order prompts — StickerMe

ใช้ทีละข้อกับ AI codegen (Cursor / Lovable / v0 ฯลฯ). Stack แนะนำ: Next.js + Tailwind (PWA, mobile-first) + vision/image-edit สำหรับอ่านเซลฟี่และวาดสติกเกอร์ + IndexedDB. ใช้ `schemas.json` เป็น type กลาง และ `reference/stickerme.py` เป็น logic อ้างอิง (port เป็น TS ให้ผลตรงกับ tests).

**P0 — Scaffold**: สร้าง PWA ภาษาไทย mobile-first ชื่อ StickerMe ใช้ design tokens ใน prd.md (ครีม #FFF7ED, ชมพู #FB7185, เหลือง #FBBF24, Kanit) bottom nav: สร้างชุด · สไตล์ · พรีวิว · ส่งออก. ทุกหน้าผลลัพธ์แสดง `SafetyGuard`. มีเกตยินยอมใบหน้าตนเองก่อนเริ่มสร้าง.

**P1 — Selfie Snap**: กล้องหน้า + กรอบใบหน้า + เตือนแสงสะท้อน/เบลอ/ครอป/หน้าเล็ก ตาม `scan_quality()`; ถ้า `ok=false` แสดง `tips_th` และปุ่มถ่ายใหม่. Output `Selfie`, `ScanQuality`, `FaceScan`.

**P2 — Consent Guard**: ก่อนสร้างชุดให้ยืนยัน `own_face`. port `consent_guard()`. ถ้าเป็นหน้าคนอื่น / คนดัง / ผู้เยาว์ไม่มีผู้ปกครองยินยอม = หยุด. Output `ConsentGuard`.

**P3 — Emotion Set** (wow): เรียก image-edit A2 ตามสไตล์ที่เลือก วาด 16 อารมณ์จาก `DEFAULT_SET_16`. port `make_pack()` ให้ตรง tests (น้องเจน = จิ๋วหัวโต 16 ใบ มีข้อความ 8 ใบ). ใส่ลายน้ำทุกใบ. Output `StickerPack`, `Sticker`.

**P4 — Thai Text Bubbles**: โหลด `BUBBLES` 8 วลี คู่กับ 8 ใบแรกตาม `DEFAULT_BUBBLE_MAP`. ช่องพิมพ์ข้อความเองใช้ `bubble_check()` จำกัดความยาว. Output `BubbleCheck`.

**P5 — Style Packs**: โหลด `STYLES` 8 สไตล์ ตาม `StyleInfo`. เปลี่ยนสไตล์แล้วสร้างชุดใหม่ด้วยอารมณ์เดิม. Output `StyleInfo`.

**P6 — Export Spec**: port `export_spec()` ให้ตรง tests (ชุดเจนพร้อมส่ง, ขนาด 370×320 / 240×240 / 96×74, PNG พื้นโปร่งใส). แสดงเช็กลิสต์และเตือนให้ตรวจคู่มือทางการ. Output `ExportSpec`, `SpecCheck`.

**P7 — Chat Preview**: port `chat_preview()` แสดง 4 ใบในแชทจำลอง. Output `ChatPreview`.

**P8 — Pack size**: สลับ 8 / 16 / 24 ใบ จากคลัง `EMOTIONS` 24 อารมณ์. จำนวนอื่นใช้ไม่ได้.

**P9 — Share Card + Quota**: `share_card()` 1080×1350/1080×1920 มีลายน้ำ; `quota()` ฟรี 3 ครั้ง/วัน. Output `ShareCard`, `Quota`.

**P10 — Privacy**: ลบเซลฟี่หลังสร้างชุดได้ ห้ามอัปโหลดรูปคนอื่น ห้ามเก็บใบหน้าไว้เทรน.

**P11 — Safety copy**: ทุกหน้าผลมีข้อความว่าภาพประกอบ ไม่ใช่ผลิตภัณฑ์ของ LINE และต้องตรวจสเปกกับคู่มือทางการก่อนอัปโหลด.

**P12 — Tests**: เขียน unit test TS ให้ตรงกับ `reference/tests.py` ทั้ง 41 ข้อ และ validate payload ด้วย `schemas.json`.

## AI prompts
**A1 Face extract** (vision, JSON mode): "ดูเซลฟี่ที่ผู้ใช้ถ่ายเพื่อทำสติกเกอร์ (ห้ามประมวลผลใบหน้าเด็กถ้าไม่มีธงผู้ปกครองยินยอม). ตอบ JSON: face_conf 0–1, face_frac 0–1 (สัดส่วนใบหน้าในเฟรม), glare 0–1, blur 0–1, crop 0–1, apparent_minor บูลีน, other_person_suspected บูลีน, celebrity_likeness บูลีน. ถ้าไม่ใช่รูปใบหน้า ให้บอกสั้น ๆ ภาษาไทย. ห้ามระบุตัวบุคคล."

**A2 Sticker render** (image-edit): "จากเซลฟี่ วาดสติกเกอร์ภาพประกอบอารมณ์ตาม emotion และสไตล์ที่ระบุ ขนาดภาพ 370×320 พื้นโปร่งใส คงลักษณะใบหน้าโดยรวมแต่ทำให้เป็นการ์ตูน ไม่ใช่ภาพถ่าย ใส่ลายน้ำว่าเป็นภาพประกอบ ห้ามทำให้เหมือนโลโก้หรือสติกเกอร์ทางการของ LINE ห้ามวาดใบหน้าคนอื่นหรือคนดัง."

**A3 Bubble layout** (image-edit): "ติดข้อความไทยตาม JSON บนสติกเกอร์ ตัวอักษรใหญ่ อ่านง่าย อยู่ในกรอบ ห้ามเปลี่ยนใบหน้าและห้ามเพิ่มคำที่ไม่มีใน JSON."

**A4 Pack caption** (text): "จาก StickerPack เขียนคำโปรยภาษาไทย ≤ 3 บรรทัด รวมสไตล์ จำนวนใบ และจำนวนข้อความ ห้ามรับประกันว่าจะผ่านการอนุมัติของ LINE."

**A5 Over-confidence + consent guard**: "ถ้า face_conf < 0.6 ให้ถ่ายใหม่ ห้ามสร้างชุด; ถ้าเป็นหน้าคนอื่น คนดัง หรือผู้เยาว์ไม่มีผู้ปกครองยินยอม ให้ใช้ข้อความจาก consent_guard() และหยุด."
