# Work-order prompts — CardReady

ใช้ทีละข้อกับ AI codegen (Cursor / Lovable / v0 ฯลฯ). Stack แนะนำ: Next.js + Tailwind (PWA, mobile-first) + on-device face detection (MediaPipe/face-api) + segmentation model สำหรับตัดพื้นหลัง. ใช้ `schemas.json` เป็น type กลาง และ `reference/cardready.py` เป็น logic อ้างอิง (port เป็น TS ให้ผลตรงกับ tests).

**P0 — Scaffold**: สร้าง PWA ภาษาไทย mobile-first ชื่อ CardReady ใช้ design tokens ใน prd.md (ขาว #FFFFFF, ฟ้าอ่อน #E8F3FF, ink #1A1A1A, mint #2DD4BF, Kanit) bottom nav: ถ่าย · ประวัติ · ครอบครัว · ตั้งค่า. เก็บข้อมูลใน IndexedDB ตาม `Selfie` / `HistoryEntry`.

**P1 — Selfie Snap + Face Detect**: หน้ากล้องหน้า + guide oval + เตือนแสง/เอียง. ตรวจหน้า → `FaceBox` (normalized). ถ้าไม่พบหน้าหรือหลายหน้า แจ้งถ่ายใหม่ภาษาไทย.

**P2 — Auto ID Crop**: port `id_crop_box()` ให้ตรง tests; ครอปตามสัดส่วนของ size ที่เลือก head_ratio ~0.70; แสดง guide หัว/ตา/คาง.

**P3 — BG Remove** (wow): segmentation → alpha matte, ขอบผมนุ่ม (feather 1–2 px), แสดง progress ทีละ step ตาม `pipeline_steps()`. Output `Pipeline`.

**P4 — BG Studio**: พรีเซ็ต ขาว/ฟ้ากรมการ/แดง + color picker hex; ใช้ `resolve_bg_safe()`; ตรวจ hex ผิดรูปแบบแล้วแจ้งเตือน. Output `BgChoice`.

**P5 — Size Presets**: port `size_spec()` / `list_size_presets()` แสดง mm + px @300dpi; สลับขนาดแล้วครอปใหม่ทันที. Output `SizeSpec`.

**P6 — Soft Light & Natural Skin**: port `soft_light_plan()` (strength ≤ 0.35, blemish ≤ 0.25); สไลเดอร์ 2 ตัว; **ห้าม** reshape/ผิวพลาสติก; มีปุ่ม "ดูภาพต้นฉบับ" ค้างดูเทียบได้. Output `SoftLightPlan`.

**P7 — Pass Score**: port `pass_score()`; แสดงเกจ 0–100 + ป้าย ผ่าน/เกือบผ่าน/ยังไม่ผ่าน; ตัวอย่าง Mint ต้องได้ 92. Output `PassReport`.

**P8 — Print Sheet A4**: port `print_sheet_layout()` + `dpi_check()`; พรีวิว A4 พร้อมเส้นตัดและจำนวนใบ; ถ้า dpi ต่ำกว่า 300 แสดงเตือนแดง. Output `PrintSheet`.

**P9 — Doc Checklist**: port `doc_checklist()` ตามประเภทเอกสาร; มิเตอร์ + รายการ ✓/✗ + disclaimer "ไม่ใช่การรับรองจากราชการ". Output `DocChecklist`.

**P10 — Vault + Share Card**: `history_entry()` เก็บในเครื่อง; `share_card()` สร้างการ์ด Before/After 1080×1350 + 1080×1920 มีลายน้ำ. Output `HistoryEntry`, `ShareCard`.

**P11 — Batch + Export + Quota**: `batch_profiles()` ≤ 8 คน (สมมติ), `export_pack()` JPG/PNG/PDF, `quota()` ฟรี 5 ไฟล์/วัน paywall สุภาพ.

**P12 — Tests**: เขียน unit test TS ให้ตรงกับ `reference/tests.py` ทั้ง 31 ข้อ และ validate payload ด้วย `schemas.json`.

## AI prompts
**A1 Face & quality extract** (vision, JSON mode): "ดูเซลฟี่ที่ผู้ใช้ถ่ายเพื่อทำรูปติดบัตร. ตอบ JSON: จำนวนหน้า, กรอบหน้า normalized 0–1 (cx, cy, h), ลืมตา/สีหน้าเป็นกลาง/หันตรงหรือไม่, ให้คะแนนความรก 0–1 หกด้าน (yellow_cast, shadow, clutter_bg, blur, tilt, crop_tight). ห้ามเดาตัวตนหรืออายุ ถ้าไม่เห็นหน้าคนจริงให้บอกเหตุผลสั้นๆ ภาษาไทย."

**A2 Background removal / matte**: "Segment the person from the background and output a clean alpha matte with soft hair edges. Keep face, hair and clothing pixels unchanged. Do not alter facial features."

**A3 Soft light**: "Even out lighting and neutralise the yellow colour cast on this portrait. Mildly calm small blemishes only. Do NOT reshape the face, enlarge eyes, slim the jaw, smooth skin into plastic, or add makeup. The person must look exactly like themselves. Strength ≤ {strength}."

**A4 Identity & over-edit guard**: เปรียบเทียบ face embedding ก่อน/หลัง (cosine ≥ 0.85 เป็นค่าเริ่มต้นที่ต้องปรับจริง) ถ้า fail ให้ลดความแรง soft light หรือใช้ภาพต้นฉบับที่ครอปอย่างเดียว.

**A5 Checklist signals** (vision, JSON): "จากรูปหลังประมวลผล ตอบ true/false ต่อข้อ: face_front, eyes_open, neutral, even_light, bg_plain, no_hat, no_glasses_tint, head_ratio, ears_visible, formal_wear. ตอบตามที่เห็นจริง ไม่เดา."
