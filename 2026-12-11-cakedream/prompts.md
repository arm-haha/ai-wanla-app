# Work-order prompts — CakeDream

ใช้ทีละข้อกับ AI codegen (Cursor / Lovable / v0 ฯลฯ). Stack แนะนำ: Next.js + Tailwind (PWA, mobile-first) + text/vision model สำหรับแยกไอเดีย + image model สำหรับภาพเค้กจำลอง + IndexedDB. ใช้ `schemas.json` เป็น type กลาง และ `reference/cakedream.py` เป็น logic อ้างอิง (port เป็น TS ให้ผลตรงกับ tests).

**P0 — Scaffold**: PWA ภาษาไทย mobile-first ชื่อ CakeDream ใช้ design tokens ใน prd.md (ครีม #FFF8F0, ชมพู #F9A8D4, เขียว #7CC36B, เหลือง #F4D35E, Kanit). bottom nav: ออกแบบ · สั่งร้าน · อบเอง · ไดอารี่. ทุกหน้าผลแสดง `SafetyGuard`.

**P1 — Idea Input**: ช่องพิมพ์ + ปุ่มไมค์ (speech-to-text ภาษาไทย) + แนบรูปตัวอย่าง (เช็ก `scan_quality()` ถ้า `ok=false` แสดง `tips_th`). เรียก A1 → `AiIdeaExtract`; ถ้า confidence < 0.7 ให้ชิปยืนยันธีม/รส.

**P2 — Mockup Studio** (wow): port `design_spec()` แล้วส่ง `image_prompt` เข้า A2 สร้าง 3 ภาพ 4:5 ปัดเลือกได้ คอนเฟตตีตอนภาพขึ้น. Output `DesignSpec`.

**P3 — Serving Calculator**: stepper ผู้ใหญ่/เด็ก + สายหวาน + เหลือกลับบ้าน. port `serving_calc()` ให้ตรง tests (8+10 = 14 ชิ้น = 2 ปอนด์ 8 นิ้ว). Output `Servings`.

**P4 — Message Fit**: พรีวิวตัวอักษรบนหน้าเค้กเป็นวงกลมตามขนาด port `glyphs()` + `message_fit()` (สระบน-ล่าง/วรรณยุกต์ไม่นับ). Output `MessageFit`.

**P5 — Flavor & Allergy**: การ์ดรส 7 แบบ + ติ๊กแพ้ ไข่/นม/กลูเตน/ถั่ว. port `allergy_guard()`; level `stop` ล็อกปุ่มถัดไปจนเปลี่ยนรส. Output `AllergyCheck`.

**P6 — Price & Fair Check**: เลือกพื้นที่ → `price_estimate()` แสดงแถบ low–mid–high + ฿/ชิ้น; ใส่ราคาร้าน → `fair_price()` ป้ายสี. Output `PriceEstimate`, `FairPrice`.

**P7 — Countdown**: date picker วันงาน → `order_deadline()`; สร้างการแจ้งเตือนในเครื่อง 1 วันก่อน `order_by`. Output `OrderDeadline`.

**P8 — Order Card**: `order_card()` เรนเดอร์การ์ด 1080×1350 (ภาพจำลอง + รายละเอียด) + ปุ่มแชร์ LINE (Web Share API) + คัดลอกข้อความ. Output `OrderCard`.

**P9 — DIY Mode**: `diy_recipe()` ตารางวัตถุดิบตามปอนด์ ติ๊กซื้อ เวลาอบพร้อมจับเวลา. Output `DiyRecipe`.

**P10 — Diary & Share**: บันทึก `DiaryEntry` หลังงาน (รูปเค้กจริง + ดาว + ราคา) → `diary_summary()`; `share_card()` แบบ ไอเดีย → ภาพ. ลายน้ำ "CakeDream · AI วันละแอป".

**P11 — Quota & Guard**: `quota()` ฟรี 3 ภาพ/วัน; `safety_guard("real_brand")` ถ้า A1 เจอชื่อแบรนด์/ตัวละครลิขสิทธิ์.

**P12 — QA**: รัน `reference/tests.py` (35 tests) และ validate output ทุกตัวกับ `schemas.json`; ทดสอบ iPhone SE + Android จอเล็ก, โหมดออฟไลน์ของ Diary.

## AI prompts
**A1 — Idea extract (text/vision → JSON)**
```
คุณคือผู้ช่วยออกแบบเค้ก อ่านข้อความ/รูปของผู้ใช้แล้วตอบเป็น JSON ตาม AiIdeaExtract เท่านั้น
theme ∈ [dinosaur, unicorn, korean_minimal, floral, football, princess, cartoon_bear, gold_luxury]
flavor ∈ [vanilla_chiffon, chocolate, thai_tea, pandan_coconut, strawberry, almond_crunch, eggless_choc]
message = ข้อความที่ผู้ใช้อยากให้เขียนบนเค้ก (คงตัวสะกดเดิม), colors = HEX ไม่เกิน 3 สี
ถ้าเจอชื่อแบรนด์หรือตัวละครลิขสิทธิ์ ให้เลือกธีมทั่วไปที่ใกล้ที่สุดและเขียน notes_th เตือน
ถ้าไม่แน่ใจ confidence < 0.7 ห้ามเดา
```
**A2 — Cake mock-up image**: ใช้ `DesignSpec.image_prompt` + "professional bakery product photo, front 3/4 view, clean pastel background, realistic buttercream texture, message text exactly: '<message>'". ห้ามคนจริง ห้ามโลโก้.
**A3 — Order note polish**: "เขียนข้อความสั่งเค้กถึงร้านจาก lines_th ให้สุภาพ กระชับ ไม่เกิน 6 บรรทัด ห้ามเปลี่ยนตัวเลข ราคา วันที่ หรือข้อความบนเค้ก"
**A4 — Theme ideas**: "เสนอ 3 ไอเดียธีมเค้กสำหรับ <อายุ/โอกาส/สิ่งที่ชอบ> เลือกจาก theme list เท่านั้น พร้อมเหตุผล 1 บรรทัด"
**A5 — Message ideas**: "เสนอข้อความบนเค้ก 5 แบบ ภาษาไทย/อังกฤษ ไม่เกิน <limit_per_line> ตัวอักษร (ไม่นับสระบน-ล่างและวรรณยุกต์)"
