# Work-order prompts — SellSnap

ใช้ทีละข้อกับ AI codegen (Cursor / Lovable / v0 ฯลฯ). Stack แนะนำ: Next.js + Tailwind (PWA, mobile-first) + vision สำหรับอ่านรูปสินค้า + IndexedDB. ใช้ `schemas.json` เป็น type กลาง และ `reference/sellsnap.py` เป็น logic อ้างอิง (port เป็น TS ให้ผลตรงกับ tests).

**P0 — Scaffold**: สร้าง PWA ภาษาไทย mobile-first ชื่อ SellSnap ใช้ design tokens ใน prd.md (ครีม #FFFBEB, เขียว #16A34A, เหลือง #F59E0B, Kanit) bottom nav: ถ่ายของ · โพสต์ · ตอบแชท · สมุดขาย. ทุกหน้าผลลัพธ์แสดง `SafetyGuard`.

**P1 — Item Snap**: กล้องหลัง + กรอบสินค้า + เตือนแสงสะท้อน/เบลอ/ครอป ตาม `scan_quality()`; ถ้า `ok=false` แสดง `tips_th`. Output `ItemPhoto`, `ScanQuality`.

**P2 — Item Read**: เรียก vision A1 → port `parse_item()` ความมั่นใจ < 0.6 ไม่นับหมวด. Output `ItemScan`, `Detection`.

**P3 — Title + Description** (wow): port `listing()` ให้ตรง tests (พี่บอส = "โคมไฟตั้งโต๊ะ สีครีม สภาพดี" มีตำหนิฐาน ราคา ฿600). ตัดชื่อไม่เกิน 60 ตัวอักษร. Output `Listing`.

**P4 — Condition Grade**: port `condition_grade()` ใช้ค่า condition โดยตรง หรืออนุมานจาก wear. พี่บอส = B สภาพดี, wear 0.70 = D. Output `ConditionGrade`.

**P5 — Price Range**: port `price_range()` จากตาราง `PRICES` ให้ตรง tests (โคมไฟสภาพดี = ฿450–750 กลาง ฿600). โชว์ disclaimer ทุกครั้ง. Output `PriceRange`.

**P6 — Photo Tips**: port `photo_tips()` ตามคุณภาพรูป และว่ามีรูปตำหนิ/เทียบขนาด/ครบ 3 มุมหรือยัง. Output `PhotoTips`.

**P7 — Buyer replies**: port `reply_templates()` 5 ชุด ต่อราคาใช้ 95% ของราคากลาง ปัด 10 บาท (พี่บอส = ฿570). Output `ReplyKit`, `ReplyTemplate`.

**P8 — Sold Log**: port `sold_log()` สถานะ for_sale / reserved / sold, รวมยอดขาย. Output `SoldLog`, `LogRow`.

**P9 — Share Card + Quota**: `share_card()` 1080 มีลายน้ำ; `quota()` ฟรี 3 ครั้ง/วัน. Output `ShareCard`, `Quota`.

**P10 — Meetup safety**: `safety_guard(wants_prepay, public_meetup)` โอนล่วงหน้า+นัดที่ลับ = หยุด.

**P11 — Privacy**: ลบรูปสินค้าได้หลังสร้างโพสต์ ห้ามอ่าน QR ชำระเงินหรือบัญชีในรูป.

**P12 — Tests**: เขียน unit test TS ให้ตรงกับ `reference/tests.py` ทั้ง 41 ข้อ และ validate payload ด้วย `schemas.json`.

## AI prompts
**A1 Item extract** (vision, JSON mode): "ดูรูปสินค้ามือสอง. ตอบ JSON เป็น detections: key ใน {category, item_th, color_th, brand_th, defect_th, condition, wear}, value เป็นข้อความไทย หมวดใน {lamp, chair, bag, electronics, clothes, kitchen, book, toy, other}, condition ใน {like_new, good, fair, poor, for_parts} หรือ wear 0–1, confidence 0–1. ห้ามอ่าน QR ชำระเงิน เบอร์โทร หรือบัญชี. ถ้าไม่ใช่รูปสินค้า ให้บอกสั้น ๆ ภาษาไทย."

**A2 Listing writer** (text): "จาก JSON Listing เขียนโพสต์ภาษาไทยสุภาพ ≤ 8 บรรทัด ใช้ชื่อ ตำหนิ และช่วงราคาใน JSON เท่านั้น ห้ามรับประกันสภาพ ห้ามใส่ราคาอื่น."

**A3 Photo coach** (text): "จาก PhotoTips เขียนคำแนะนำสั้น เรียงตาม keys น้ำเสียงช่วยเหลือ ไม่ตำหนิผู้ใช้."

**A4 Bargain helper** (text): "จาก ReplyKit เลือกเทมเพลตตามสถานการณ์ที่ผู้ใช้เลือก ห้ามเปลี่ยนตัวเลขใน JSON."

**A5 Over-confidence + safety**: "ถ้า confidence ของ category หรือ condition < 0.6 ให้ถามย้ำ; ถ้าผู้ใช้จะนัดในที่ลับหรือโอนก่อนส่งของ ให้ใช้ safety_guard()."
