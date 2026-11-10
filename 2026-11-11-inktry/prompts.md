# Work-order prompts — InkTry

ใช้ทีละข้อกับ AI codegen (Cursor / Lovable / v0 ฯลฯ). Stack แนะนำ: Next.js + Tailwind (PWA, mobile-first) + vision/image-edit model สำหรับอ่านผิวและวางลาย + IndexedDB. ใช้ `schemas.json` เป็น type กลาง และ `reference/inktry.py` เป็น logic อ้างอิง (port เป็น TS ให้ผลตรงกับ tests).

**P0 — Scaffold**: สร้าง PWA ภาษาไทย mobile-first ชื่อ InkTry ใช้ design tokens ใน prd.md (ครีม #F4EFE6, หมึก #111111, ทอง #C9A36A, Kanit) bottom nav: ลองลาย · คลังลาย · ไดอารี่ · ดูแล. เก็บข้อมูลใน IndexedDB ตาม `Person` / `DiaryEntry`. ทุกหน้าผลลัพธ์แสดง `SafetyGuard`. มีเกตอายุ 18+ ก่อนเริ่มสแกน.

**P1 — Skin Snap**: กล้องหลัง + กรอบผิว + เตือนแสงสะท้อน/เบลอ/เอียง/ผิวน้อย ตาม `scan_quality()`; ถ้า `ok=false` แสดง `tips_th` และปุ่มถ่ายใหม่. Output `SkinPhoto`, `ScanQuality`.

**P2 — Skin Scan**: เรียก vision A1 → `Detection[]` → port `identify_placement()` / `skin_scan()` (ความมั่นใจ < 0.6 ไปอยู่ `uncertain` และถามย้ำ "นี่คือ ... ใช่ไหม?"). Output `SkinScan`, `IdentifiedPlacement`, `Pipeline`.

**P3 — Placement Try-On** (wow): เลือกลายจากคลังหรืออัปโหลด → image-edit วางลายบนผิวในรูป คงผิวและสัดส่วนเดิม ใส่ลายน้ำ `WATERMARK`. port `overlay_tryon()` / `size_check()`. เลื่อนขนาดเป็นซม. ถ้าเล็กไป/ใหญ่ไปแสดงป้ายและช่วงที่แนะนำ. Output `TryOn`, `SizeCheck`.

**P4 — Color vs BW**: port `color_variants()` / `contrast_score()` ให้ตรง tests (พี่มิ้นต์ขาวดำ 80 / สี 76 แนะนำขาวดำ). สลับก่อน-หลังสองโหมด. Output `ColorVariants`.

**P5 — Aging Preview**: port `aging_preview()` ให้ตรง tests (เส้นบาง แขนด้านใน 8 ซม. ขาวดำ: 1 ปีจาง 12% / 5 ปี 60% เบลอ 0.98 มม. / 10 ปี 90%). สไลเดอร์ 1/5/10 ปี แสดง % และคำอธิบาย. ห้ามอ้างว่าเป็นผลจริง. Output `AgingPreview`.

**P6 — Design + Placement Library**: โหลด `DESIGNS` (12) และ `PLACEMENTS` (15) ตาม `DesignInfo` / `PlacementInfo`; กรองสไตล์/จุด; หน้ารายละเอียดมีช่วงขนาด ระดับเจ็บ วันพักฟื้น.

**P7 — Pain, Aftercare, Price**: port `pain_guide()` / `aftercare_guide()` / `price_range()` / `quote_check()`; ช่องใส่ราคาที่ร้านเสนอ → ป้าย ถูก/สมเหตุสมผล/แพง/แพงมาก + คำถามถามช่าง + disclaimer ราคา. Output `PainGuide`, `AftercareGuide`, `PriceRange`, `QuoteCheck`.

**P8 — Artist Brief Card**: port `artist_card()`; การ์ดแนวตั้ง (ลาย จุด ขนาด โหมด สี พรีวิว 5 ปี งบ คำถาม) บันทึกเป็นรูปและปุ่มส่ง LINE (`line_share_url`). ถ้า `can_book=false` ซ่อนปุ่มนัด โชว์เหตุผล. Output `ArtistCard`.

**P9 — Diary**: `diary_entry()` + `diary_stats()` สถานะ wishlist/booked/done/touch_up; เตือนคิวและรอบเติม (ค่าที่ตั้งเอง). Output `DiaryEntry`, `DiaryStats`.

**P10 — Share Card + Quota**: `share_card()` 1080×1350/1080×1920 มีลายน้ำ; `quota()` ฟรี 3 ครั้ง/วัน paywall สุภาพ. Output `ShareCard`, `Quota`.

**P11 — Safety & Privacy**: เกต 18+; `safety_from_flags()` / `safety_guard()` ทุกผล; คีลอยด์/ตั้งครรภ์/แผลติดเชื้อ = ระดับแดง; ลบรูปผิวหลังประมวลผล; ห้ามใช้รูปคนอื่นโดยไม่ยินยอม; ห้ามโชว์ผลว่า "เหมือนสักจริง 100%".

**P12 — Tests**: เขียน unit test TS ให้ตรงกับ `reference/tests.py` ทั้ง 41 ข้อ และ validate payload ด้วย `schemas.json`.

## AI prompts
**A1 Skin and placement extract** (vision, JSON mode): "ดูรูปผิวที่ผู้ใช้ถ่ายเพื่อลองรอยสัก (ไม่ใช่ใบหน้าเด็ก). ตอบ JSON: undertone (warm/cool/neutral), skin_visible 0–1, glare 0–1, blur 0–1, tilt 0–1, รายการตำแหน่งที่เห็น (placement เลือกจาก {inner_forearm, outer_forearm, wrist, upper_arm, shoulder, ankle, calf, thigh, back, nape, ribs, collarbone, hand, finger, behind_ear}, side left/right, confidence 0–1). ถ้าไม่ใช่รูปผิวคน ให้บอกสั้น ๆ ภาษาไทย. ห้ามระบุตัวบุคคล ห้ามเดาตำแหน่งที่ไม่ชัด ให้ confidence ต่ำแทน."

**A2 Tattoo overlay** (image-edit): "วางลายสักตามคำอธิบาย/ภาพอ้างอิงลงบนตำแหน่งที่ระบุในรูปผิว คงสีผิว ขน และสัดส่วนเดิม ห้ามเปลี่ยนใบหน้าหรือร่างกาย ห้ามทำให้ดูเหมือนรอยสักจริงโดยไม่มีลายน้ำ ผลต้องเป็นภาพจำลองที่ดูธรรมชาติตามแสงของรูปเดิม โหมดสีตาม color_mode (color หรือ bw). ห้ามใช้ลายที่มีลิขสิทธิ์ของศิลปินอื่น."

**A3 Aging preview render** (image-edit): "จากภาพลองลายเดิม จำลองความเก่าตาม JSON AgingPreview (fade_pct, spread_mm, years) ทำให้เส้นนุ่มและสีจางลงตามตัวเลข ห้ามลบลายจนหาย และห้ามอ้างในภาพว่าเป็นผลจริง ต้องมีลายน้ำภาพจำลอง."

**A4 Artist brief writer** (text): "จาก JSON ArtistCard เขียนข้อความบรีฟช่างภาษาไทยสุภาพ ≤ 8 บรรทัด รวมลาย ตำแหน่ง ขนาดซม. โหมดสี งบประมาณ และ 1 ประโยคจาก note_th ห้ามเปลี่ยนตัวเลขใน JSON และห้ามรับประกันผลสักจริง."

**A5 Over-confidence guard**: "ตรวจ output ของ A1 — ถ้าความมั่นใจของตำแหน่ง < 0.6 ให้ถามย้ำ ห้ามวางลายลงจุดที่ไม่แน่ใจ; ถ้าผู้ใช้อายุ < 18 หรือมีธงคีลอยด์/ตั้งครรภ์/แผลติดเชื้อ ให้ใช้ข้อความจาก `safety_from_flags()` ห้ามเชิญให้นัดสัก."
