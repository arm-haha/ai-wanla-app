# Work-order prompts — GlamTry

ใช้ทีละข้อกับ AI codegen (Cursor / Lovable / v0 ฯลฯ). Stack แนะนำ: Next.js + Tailwind (PWA, mobile-first) + vision model อ่านใบหน้า + face-mesh (MediaPipe) ทำ mask ปาก/แก้ม/เปลือกตา + image-edit model สำหรับภาพลองแต่งหน้า + Canvas/MediaRecorder ทำ Reel + IndexedDB. ใช้ `schemas.json` เป็น type กลาง และ `reference/glamtry.py` เป็น logic อ้างอิง (port เป็น TS ให้ผลตรงกับ tests).

**P0 — Scaffold**: PWA ภาษาไทย mobile-first ชื่อ GlamTry ใช้ design tokens ใน prd.md (ลินิน #FBF7F2, พลัม #2B2238, โรส #E8879B, พีช #F6B48F, Kanit). bottom nav: ลองลุค · เฉดผิว · ชุดของ · ไดอารี่. ทุกหน้าผลแสดง `SafetyGuard` + disclaimer "ภาพจำลอง · ค่าประมาณ".

**P1 — Consent Guard + Selfie Capture**: หน้ายืนยัน "นี่คือหน้าของฉันเอง" + ปีเกิด → `consent_check()`; ถ้า `allowed=false` หยุดพร้อม `messages_th`. กล้องหน้า + กรอบวงรีไกด์ "หันเข้าหน้าต่าง ปิดฟิลเตอร์ มองตรง". เช็ก `scan_quality()`; เรียก A1 → `AiFaceExtract`; `faces=0` → `safety_guard("no_face")`, `faces>1` → warn, `celebrity_like=true` → `safety_guard("celebrity")`, `filter_detected` → warn.

**P2 — Shade Match**: เฉลี่ย RGB จาก cheek patch (face-mesh) → `shade_match(rgb, quality.score)`; การ์ดโค้ดเฉดใหญ่ ๆ (เช่น 2W) + แถบ 5 ระดับสีผิว + 3 วงสีลิป + ความมั่นใจ + ป้าย "ค่าประมาณ". ห้ามมีปุ่ม/ข้อความทำให้ผิวขาวขึ้น. Output `ShadeMatch`.

**P3 — Look Try-On** (wow): `six_looks(depth, undertone, intensity)` → ส่งรูปเดิม + mask + `image_prompt` ทีละลุคเข้า A2 สร้าง 4:5 (ระหว่างรอ แสดงพรีวิวสวอตช์ offline ทาสีลงบน mask ด้วย canvas blend). กริด 2×3 → แตะลุค → สไลเดอร์ ก่อน/หลัง + แถบความเข้ม ซอฟต์/กลาง/จัดเต็ม. นับ `quota()`. Output `LookSpec[]`.

**P4 — Step-by-Step Tutorial**: `tutorial(look, undertone, person.skill)` การ์ดปัดทีละขั้น (เลขขั้น, ไอคอนบริเวณ, วงสี HEX, เคล็ดลับ, นาที) + ป้าย "เวอร์ชันมือใหม่" ถ้า `simplified`. Output `Tutorial`.

**P5 — Budget Kit & Dupe Finder**: `budget_kit(look, tier, owned)` แท็บ ประหยัด/กลาง/ไฮเอนด์, เช็กบ็อกซ์ "มีแล้ว", แถบรวมราคา ฿low–high + "ประหยัดกว่าไฮเอนด์ ~฿X". ใช้ชื่อประเภทสินค้าเท่านั้น ห้ามชื่อแบรนด์/ลิงก์ร้าน. Output `BudgetKit`.

**P6 — Occasion Planner**: เลือกงาน + วันที่ + กลางแจ้ง/ร้อนชื้น → `occasion_plan()` ไทม์ไลน์แนวตั้ง + ชุดเติมหน้า + แจ้งเตือนในเครื่อง (patch test 2 วันก่อน). Output `OccasionPlan`.

**P7 — Patch-Test Helper**: ของใหม่จาก Budget Kit → `patch_test(items, sensitive, allergies)` เช็กลิสต์ + `note_th` ตัวเล็กใต้สุด; ห้ามแต่งข้อความทางการแพทย์เพิ่มเอง. Output `PatchTest`.

**P8 — Before/After Reel Maker**: `reel_plan(spec, 15–30)` → เรนเดอร์ canvas 1080×1920 ตาม shots (before, scan, swipe 6 ลุค, compare + ชุดของ, cta) + เพลง 118 BPM + ลายน้ำ → MediaRecorder เป็น MP4/WebM. Output `ReelPlan`.

**P9 — Makeup Diary**: บันทึก try/wear/buy/open/photo → `diary_summary()` ลุคโปรด ค่าใช้จ่าย รายการควรเปลี่ยน (แจ้งเตือนในเครื่อง). Output `DiarySummary`.

**P10 — Share Card**: `share_card()` เรนเดอร์ 1080×1350 ก่อน/หลัง หรือกริด 6 ลุค ลายน้ำ "GlamTry · AI วันละแอป" + ป้าย "ภาพจำลอง" + Web Share API.

**P11 — Quota & Guard**: `quota()` ฟรี 3 เซลฟี่/วัน; `safety_guard()` (not_own_photo / celebrity / under_13 / multiple_faces / no_face / filter_on / whitening_request). ลบรูปต้นฉบับหลังประมวลผล ≤ 1 ชม.

**P12 — QA**: รัน `reference/tests.py` (37 tests) และ validate output ทุกตัวกับ `schemas.json`; ทดสอบครบ 5 ระดับสีผิว (ต้องไม่สว่างขึ้นหลัง edit), แสงไฟเหลือง, เปิดฟิลเตอร์, ใส่แว่น, ตาชั้นเดียว, หลายหน้า, อายุ 12 (ต้องบล็อก).

## AI prompts
**A1 — Face read (vision → JSON)**
```
คุณคือผู้ช่วยช่างแต่งหน้า ดูเซลฟี่แล้วตอบเป็น JSON ตาม AiFaceExtract เท่านั้น
faces = จำนวนใบหน้าในรูป; cheek_rgb = ค่าเฉลี่ยสีผิวบริเวณแก้มที่ไม่มีเงา [r,g,b]
eye_shape ∈ [monolid, hooded, double, round, almond, unknown]; filter_detected = มีฟิลเตอร์/บิวตี้โหมดชัดเจนหรือไม่
celebrity_like = true ถ้ารูปดูเป็นภาพดารา/โปสเตอร์/ภาพจากสื่อ (ห้ามระบุชื่อบุคคล)
ถ้าไม่ใช่ใบหน้าคนจริงให้ is_face=false; ถ้าไม่แน่ใจ confidence < 0.7 ห้ามเดา
ห้ามประเมินอายุ เชื้อชาติ หรือความสวย
```
**A2 — Makeup mock-up (image edit)**: ใช้ `LookSpec.image_prompt` กับรูปเดิม + mask ปาก/แก้ม/เปลือกตา/คิ้ว; คงตัวตน รูปหน้า สีผิว เนื้อผิว ผม พื้นหลัง และแสง; ห้ามทำผิวขาว ห้ามเรียวหน้า ห้ามเปลี่ยนเป็นคนอื่น; ใส่ลายน้ำ "ภาพจำลอง".
**A3 — Look stylist**: "ผู้ใช้โค้ดเฉด <shade_code> อันเดอร์โทน <undertone> จะไป <event_th> เสนอ 2 ลุคจาก LOOKS เท่านั้น พร้อมเหตุผลสั้น ๆ คนละ 1 บรรทัด ห้ามพูดถึงการทำผิวขาว"
**A4 — Shopping helper**: "จาก BudgetKit เขียนลิสต์ช้อปสั้น ๆ เป็นกันเอง ใช้ชื่อประเภทสินค้าและรหัสสี HEX เท่านั้น ห้ามชื่อแบรนด์ ห้ามเปลี่ยนตัวเลขราคา ปิดท้ายด้วย 'ของใหม่ทำ patch test ก่อนนะ'"
**A5 — Diary nudge**: "จาก DiarySummary เขียนข้อความเตือน 1 บรรทัด เป็นกันเอง ห้ามเปลี่ยนตัวเลขหรือวันที่"
