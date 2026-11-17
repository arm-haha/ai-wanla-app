# Work-order prompts — WrapRide

ใช้ทีละข้อกับ AI codegen (Cursor / Lovable / v0 ฯลฯ). Stack แนะนำ: Next.js + Tailwind (PWA, mobile-first) + vision model อ่านรูปรถ + image-edit model (พร้อม mask ตัวรถ) สำหรับภาพจำลอง + Canvas/MediaRecorder ทำ Reel + IndexedDB. ใช้ `schemas.json` เป็น type กลาง และ `reference/wrapride.py` เป็น logic อ้างอิง (port เป็น TS ให้ผลตรงกับ tests).

**P0 — Scaffold**: PWA ภาษาไทย mobile-first ชื่อ WrapRide ใช้ design tokens ใน prd.md (กราไฟต์ #10161C, มิ้นต์ #7FD1AE, ส้ม #FF7A1A, ม่วงนีออน #7A3CFF, Kanit). bottom nav: ลองสี · ล้อ/สติกเกอร์ · ราคา · โรงรถ. ทุกหน้าผลแสดง `SafetyGuard` + disclaimer.

**P1 — Vehicle Capture**: กล้อง + กรอบไกด์ "ถอยให้เห็นรถทั้งคัน มุมเฉียงหน้า 45°". เช็ก `scan_quality()`; เรียก A1 → `AiVehicleExtract`; ถ้า `is_vehicle=false` → `safety_guard("not_vehicle")`; ถ้า `plate_visible` → เบลอป้าย + `safety_guard("plate_visible")`. ให้ผู้ใช้แก้ประเภทรถ/สีเดิมได้.

**P2 — Wrap Try-On** (wow): carousel 12 สี + แถบ 5 ผิว + ปุ่ม ทั้งคัน / ทูโทน / หลังคา / ฝากระโปรง / คาดลาย → `wrap_spec()` → ส่งรูปเดิม + mask + `image_prompt` เข้า A2 สร้าง 4:5; ระหว่างรอ แสดงสวอตช์ทันที. สไลเดอร์ ก่อน/หลัง + แอนิเมชันสีไหล. นับ `quota()`.

**P3 — Finish Lab**: การ์ดสวอตช์จาก `finish_swatch()` (base/highlight/shadow, `shift_hex` สำหรับเปลี่ยนสีตามมุม เอียงมือถือแล้วไล่สีด้วย DeviceOrientation). Output `FinishSwatch`.

**P4 — Rim & Sticker Studio**: ล้อ 4 สไตล์ × 5 สี + สติกเกอร์ ≤ 3 ลาย ลากวางบนรถ; ถ้าวางบนพื้นที่ต้องห้าม → `rim_sticker_spec(areas=...)` คืน `ok=false` → `safety_guard("covers_lights")`. ส่ง `image_prompt` เข้า A2. Output `RimStickerSpec`.

**P5 — Fair Price Check**: port `price_check()` แท็บ wrap / ทำสี / ล้อ / สติกเกอร์; แถบช่วงราคาแนวนอน + หมุดราคาที่ร้านเสนอ สีตาม verdict (เทา no_quote, เหลือง suspicious_low, เขียว fair, ส้ม high, แดง too_high). ป้าย "ค่าประมาณ" ชัดเจน. Output `PriceCheck`.

**P6 — Shop Brief Card**: `shop_brief()` การ์ดสวย ๆ + ปุ่มคัดลอกข้อความ / แชร์รูปการ์ดไป LINE (Web Share API) แนบรูปเดิม + ภาพจำลอง + สวอตช์. Output `ShopBrief`.

**P7 — Legal & Insurance Check**: `legal_check()` เช็กลิสต์ไอคอน (action / warn / info) + `note_th` ตัวเล็กใต้สุด; ห้ามเพิ่มตัวเลขค่าธรรมเนียม/กำหนดวันเอง. Output `LegalCheck`.

**P8 — Before/After Reel Maker**: `reel_plan(spec, 15–30)` → เรนเดอร์ canvas 1080×1920 ตาม shots (before, scan, swipe, compare, cta) + เพลง 120 BPM + ลายน้ำ → MediaRecorder เป็น MP4/WebM. Output `ReelPlan`.

**P9 — Garage Diary**: บันทึก wash/wrap/service/rim/photo/tire + ค่าใช้จ่าย → `diary_summary()` อายุฟิล์ม วันล้างครั้งถัดไป (แจ้งเตือนในเครื่อง) ยอดใช้จ่าย + care tip. Output `DiarySummary`.

**P10 — Share Card**: `share_card()` เรนเดอร์ 1080×1350 ก่อน/หลัง ลายน้ำ "WrapRide · AI วันละแอป" + Web Share API.

**P11 — Quota & Guard**: `quota()` ฟรี 5 ภาพจำลอง/วัน; `safety_guard()` (plate_visible / covers_lights / not_vehicle / someone_elses_car / brand_logo).

**P12 — QA**: รัน `reference/tests.py` (37 tests) และ validate output ทุกตัวกับ `schemas.json`; ทดสอบรูปย้อนแสง รถสีดำสะท้อน มอเตอร์ไซค์ด้านข้าง จอเล็ก และเช็กว่าป้ายทะเบียนเบลอทุกภาพที่แชร์.

## AI prompts
**A1 — Vehicle read (vision → JSON)**
```
คุณคือผู้ช่วยร้านทำฟิล์มรถ ดูรูปแล้วตอบเป็น JSON ตาม AiVehicleExtract เท่านั้น
vehicle ∈ [eco_car, sedan, suv, pickup, big_bike, scooter]; original_family = กลุ่มสีหลักเดิมของตัวรถ
angle ∈ [front_45, side, rear_45, front, rear, unknown]; plate_visible = เห็นป้ายทะเบียนอ่านได้หรือไม่
ถ้าไม่ใช่รถยนต์/มอเตอร์ไซค์ให้ is_vehicle=false; ถ้าไม่แน่ใจ confidence < 0.7 ห้ามเดา
ห้ามอ่านหรือพิมพ์เลขทะเบียนออกมา ห้ามระบุยี่ห้อ/รุ่นรถ
```
**A2 — Wrap / rim mock-up (image edit)**: ใช้ `WrapSpec.image_prompt` หรือ `RimStickerSpec.image_prompt` กับรูปเดิม + mask ตัวรถ; คงรูปทรง มุมกล้อง พื้นหลัง ไฟ กระจก และล้อ (ถ้าไม่ได้เปลี่ยนล้อ); เบลอป้าย; ห้ามคน ห้ามโลโก้.
**A3 — Colour stylist**: "รถ <vehicle_th> สีเดิม <family> ผู้ใช้ชอบสไตล์ <style> เสนอ 3 คอมโบ สี+ผิว+สีล้อ จากรายการ COLORS/FINISHES/RIM_COLORS เท่านั้น พร้อมเหตุผลสั้น ๆ"
**A4 — Shop chat helper**: "จาก ShopBrief เขียนข้อความทักร้าน wrap ทาง LINE สุภาพ 3–4 บรรทัด ถามเกรดฟิล์ม ประกัน ระยะเวลา ห้ามเปลี่ยนตัวเลขราคา"
**A5 — Diary nudge**: "จาก DiarySummary เขียนข้อความเตือนดูแลรถ 1 บรรทัด เป็นกันเอง ห้ามเปลี่ยนตัวเลขหรือวันที่"
