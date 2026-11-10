# Work-order prompts — PosterPop

ใช้ทีละข้อกับ AI codegen (Cursor / Lovable / v0 ฯลฯ). Stack แนะนำ: Next.js + Tailwind (PWA, mobile-first) + canvas/SVG สำหรับเรนเดอร์โปสเตอร์ + ไลบรารี QR + IndexedDB. ใช้ `schemas.json` เป็น type กลาง และ `reference/posterpop.py` เป็น logic อ้างอิง (port เป็น TS ให้ผลตรงกับ tests).

**P0 — Scaffold**: สร้าง PWA ภาษาไทย mobile-first ชื่อ PosterPop ใช้ design tokens ใน prd.md (ครีม #F8F1E3, น้ำตาล #4A2C2A, ส้ม #E8772E, Kanit + Sarabun) bottom nav: สร้าง · เทมเพลต · ชุดสี · ไฟล์ของฉัน. เก็บชุดสีใน IndexedDB ตาม `BrandKit`. ทุกหน้าส่งออกแสดง `SafetyGuard`.

**P1 — Brief form**: ช่องหัวข้อ ซับไตเติล รายละเอียด วัน สถานที่ CTA และลิงก์คิวอาร์. Output เป็นบรีฟก่อนเข้าเลย์เอาต์.

**P2 — Template Pack**: โหลด `TEMPLATES` ตาม `TemplateInfo`; พรีวิว 3 ใบ (โปร / อีเวนต์ / เมนู). Output `TemplateInfo`.

**P3 — Auto Layout Studio** (wow): port `auto_layout()` / `title_size()` ให้ตรง tests (พี่เจ หัวข้อ 72px, 1080×1350, คอนทราสต์ 11.09 ผ่าน). แอนิเมชันข้อความกระโดดเข้าโซน. Output `PosterLayout`.

**P4 — Size Presets**: เลือกจาก `SIZES` 6 ขนาด แล้วเรนเดอร์ใหม่ด้วย `size_info()`. Output `SizeInfo`.

**P5 — Brand Kit + Contrast**: `brand_kit()` + `contrast_check()` แสดงอัตราส่วนและป้ายผ่าน/ไม่ผ่าน AA (ตัวใหญ่ 3:1 ตัวเนื้อ 4.5:1) ถ้าไม่ผ่านแนะนำให้ปรับสี. Output `BrandKit`, `ContrastCheck`.

**P6 — QR Block**: `qr_block(url, position)` วาง footer_right/left/center ขนาด 220px. Output `QrBlock`.

**P7 — Menu Price Grid**: `menu_grid(items)` คอลัมน์เดียวถ้า ≤ 6 รายการ สองคอลัมน์เมื่อมากกว่า. Output `MenuGrid`.

**P8 — Export**: ส่งออก PNG/PDF ตามขนาดที่เลือก มี bleed 3 มม. สำหรับงานพิมพ์ และลายน้ำในรุ่นฟรี.

**P9 — Share Card + Quota**: `share_card()` 1080×1350/1080×1920; `quota()` ฟรี 3 โปสเตอร์/วัน paywall สุภาพ. Output `ShareCard`, `Quota`.

**P10 — Safety & Rights**: `safety_guard(rights_ok)` ก่อนส่งออก ต้องยืนยันสิทธิ์ในข้อความและรูป ห้ามใส่โลโก้แบรนด์จริงเป็นพรีเซ็ต.

**P11 — Onboarding copy**: หน้าแรกโชว์โปสเตอร์ตัวอย่าง Ficto Café (สมมติ) และบอกว่าผู้ใช้ต้องตรวจคำและสิทธิ์เอง.

**P12 — Tests**: เขียน unit test TS ให้ตรงกับ `reference/tests.py` ทั้ง 41 ข้อ และ validate payload ด้วย `schemas.json`.

## AI prompts
**A1 Brief tidy** (text): "จัดข้อความบรีฟโปสเตอร์ให้สุภาพ กระชับ ไม่เปลี่ยนราคา วัน เวลา หรือชื่อร้านในอินพุต. ตอบ JSON: title, subtitle, details, date_th, place_th, cta_th. ห้ามใส่ชื่อแบรนด์จริงที่ผู้ใช้ไม่ได้พิมพ์มา."

**A2 Layout copy fit** (text): "จาก PosterLayout แนะนำว่าควรตัดหัวข้อหรือไม่ ถ้ายาวเกิน 32 ตัวอักษร เสนอเวอร์ชันสั้นกว่า ≤ 20 ตัว โดยคงความหมาย และห้ามเปลี่ยนตัวเลขโปร."

**A3 Poster composer** (image/layout): "เรนเดอร์โปสเตอร์ตาม PosterLayout: ใช้โซน y/h, สีใน colors, ฟอนต์หัว-เนื้อ, คิวอาร์ถ้ามี. ภาษาไทยต้องไม่ชนขอบ. ใส่ disclaimer เล็ก ๆ มุมล่าง. ห้ามใส่โลโก้แบรนด์ที่ไม่มีในบรีฟ."

**A4 Alt text writer** (text): "เขียนคำอธิบายภาพภาษาไทยสั้น ๆ สำหรับโปสเตอร์ เพื่อช่วยการเข้าถึง ไม่ต้องใส่แฮชแท็ก."

**A5 Rights + contrast guard**: "ตรวจ A3 — ถ้าคอนทราสต์ใน JSON ok=false ห้ามส่งออกโดยไม่เตือน และถ้ามีโลโก้ที่ผู้ใช้ไม่ได้ยืนยันสิทธิ์ ให้บล็อกตาม `safety_guard()`."
