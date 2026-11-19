# Work-order prompts — HandFont

> ให้ AI codegen (Cursor / Claude / v0 / Lovable ฯลฯ) ทำทีละ prompt ตามลำดับ ใช้ `schemas.json` เป็นสัญญาข้อมูล และ `reference/handfont.py` เป็นตรรกะต้นแบบ (port เป็น TypeScript ให้ผลเท่ากับ `tests.py`)

**P0 — Scaffold**: สร้าง PWA (Next.js หรือ Vite + React + Tailwind) มือถือก่อน ภาษาไทยเป็นหลัก สลับ EN ได้ ใช้ design tokens ใน prd.md (กระดาษครีม #FAF7EE หมึก #1C2E78 ทอง #FFC440, Kanit) port `handfont.py` → `src/logic/handfont.ts` พร้อม unit test เทียบ `tests.py` ทั้ง 37 ข้อ

**P1 — Consent**: หน้าแรกถาม "ลายมือนี้เป็นของคุณเองใช่ไหม" + อายุ + วัตถุประสงค์ (ส่วนตัว / ร้านค้า / ขายฟอนต์) → `consent_check()`; stop = ปิดปุ่มถัดไปพร้อมข้อความ; อายุ < 13 ให้ผู้ปกครองกดยืนยัน. Output `ConsentCheck`.

**P2 — Template Sheet**: `template_sheet(template)` → สร้าง PDF A4 ด้วย pdf-lib: ช่อง 80 ช่อง/หน้า มีตัวอย่างอักษรจาง ๆ มุมซ้ายบน, เส้น baseline/x-height/ascender, มาร์กเกอร์ 4 มุม (ArUco/QR) สำหรับ warp; สระและวรรณยุกต์มีวงกลมจุดประแสดงตำแหน่งพยัญชนะ. Output `TemplateSheet`.

**P3 — Capture & Scan QA**: กล้องหลัง + กรอบ 4 มุมเรียลไทม์ → ประเมิน light/blur/skew/ink_contrast ฝั่งเครื่อง → `scan_quality()`; ok=false แสดงทิปและให้ถ่ายใหม่. Output `SheetScan`.

**P4 — Cell Extract (A1)**: perspective warp → ตัดช่องตามกริด → ส่งภาพรวมย่อให้ A1 ตรวจลายเซ็น/ข้อมูลส่วนตัว/สไตล์ → คำนวณ ink/touches_border/extra_blobs ต่อช่อง → `glyph_check()` + `coverage()`; ช่องที่พังเป็นสีแดงแตะเพื่อถ่ายซ่อมเฉพาะช่อง. Output `AiGlyphExtract`, `GlyphCheck[]`, `Coverage`.

**P5 — Vectorize & Build**: threshold → potrace (WASM) → simplify path → opentype.js สร้าง glyph ตาม Unicode, advance width จาก bbox + tracking, สร้าง alternates (`calt`/`salt`) ด้วยการบิดเส้นเล็กน้อยตาม roughness → export TTF/OTF/WOFF2 ชื่อ `font_name()`. Output `FontBuild`.

**P6 — Thai Mark Engine**: ใช้ `clusters()` + `mark_placement()` สร้าง GPOS mark-to-base และ mark-to-mark anchors (+ dx/dy สำหรับ ป ฝ ฟ ฬ, ฎ ฏ) และ glyph ญ/ฐ แบบตัดเชิงผ่าน `ccmp`; ทดสอบคำ ที่ ปี่ ฟื้ ฎุ ญู ฐุ ป๋ สั้ กึ๋ ต้องไม่ซ้อนทับ. Output `MarkPlacement`.

**P7 — Style Tuner + Type Test**: สไลเดอร์ weight/slant/roughness/tracking → `style_params()`; ช่องพิมพ์ทดลองเรนเดอร์ด้วย FontFace API แบบ realtime, `pick_alternates()` สลับรูปตัวซ้ำ; `text_preview()` แสดงจำนวนบรรทัด (ตัดคำไทยด้วย Intl.Segmenter). Output `StyleParams`, `TextPreview`.

**P8 — Card & Sticker**: เทมเพลตการ์ด 7 แบบ (`card_layout()`) กระดาษ/หมึกตาม PAPERS/INKS, export PDF (A5/A6/A7) และ PNG; `sticker_export()` → PNG พื้นใส + ขอบขาวแบบสติกเกอร์ + ปุ่มแชร์ไป IG Story/LINE. Output `CardLayout`, `StickerExport`.

**P9 — Practice**: `practice_sheet()` สร้าง PDF แบบฝึก trace (ตัวจาง 25%) / copy / free; ถ่ายผลฝึก → วัด height/baseline/spacing/slant variance → `practice_score()` เกรด A–D + ทิป. Output `PracticeSheet`, `PracticeScore`.

**P10 — Diary & Versions**: เก็บ IndexedDB build/card/sticker/practice → `diary_summary()` สตรีค คะแนนดีขึ้น เวอร์ชันฟอนต์ล่าสุด + ปุ่ม "สร้าง v2 จากลายมือที่ฝึกแล้ว". Output `DiarySummary`.

**P11 — Share / Reel / Quota / Guard**: `share_card()` 1080×1350 3 เลย์เอาต์ ลายน้ำ "HandFont · AI วันละแอป"; `reel_plan()` → canvas 1080×1920 6 ช็อต 112 BPM → MediaRecorder MP4/WebM; `quota()` ฟรี 2 build/วัน; `safety_guard()` ทุก flag. ลบรูปต้นฉบับหลังประมวลผล ≤ 1 ชม.

**P12 — QA**: รัน `reference/tests.py` (37 tests) และ validate output ทุกตัวกับ `schemas.json`; ทดสอบรูปมืด/เอียง 15°/ดินสอจาง/กระดาษมีเส้น/เงามือ, คำไทยยาก 10 คำ, ติดตั้งฟอนต์บน iOS/Android/Windows/macOS/Canva, กรณีลายเซ็น (ต้อง stop), อายุ 11 ไม่มีผู้ปกครอง (ต้อง stop).

## AI prompts

**A1 — Sheet inspector (vision, JSON only)**
```
คุณคือผู้ตรวจแบบฟอร์มลายมือของแอป HandFont ดูรูปกระดาษแบบฟอร์ม แล้วตอบ JSON ตาม schema AiGlyphExtract เท่านั้น
- corners_found: เห็นมาร์กเกอร์ครบ 4 มุมไหม
- cells: ต่อช่อง {char, ink (0..1 สัดส่วนหมึกในช่อง), touches_border, extra_blobs}
- signature_like: true ถ้ามีลายเซ็นหรือการเซ็นชื่อแบบหวัดต่อเนื่องอยู่บนแผ่น
- personal_data: true ถ้ามีเลขบัตร เบอร์โทร ที่อยู่ หรือข้อมูลบัญชี
- handwriting_style: round | loopless | cursive | print | mixed
ห้ามวิเคราะห์นิสัย/บุคลิกจากลายมือ ห้ามเดาตัวตนเจ้าของลายมือ ถ้าไม่แน่ใจ confidence < 0.7
```
**A2 — Glyph cleanup (image edit, optional)**: รับภาพช่องเดียว ลบรอยเลอะ/เส้นกรอบ/ตัวอย่างจาง โดย "คงเส้นลายมือเดิม 100%" ห้ามวาดตัวอักษรใหม่ ห้ามทำให้สวยขึ้นจนไม่ใช่ลายมือเจ้าของ คืนภาพขาวดำ.
**A3 — Card writer**: "ช่วยเขียนข้อความ <card_kind_th> สั้น ๆ ไม่เกิน <max_chars> ตัวอักษร โทน <อบอุ่น/ขำ/ทางการ> ถึง <ผู้รับ> ภาษาไทยเป็นธรรมชาติ ห้ามอ้างว่าเป็นข้อความจากคนอื่นที่ไม่ใช่ผู้ใช้"
**A4 — Practice coach**: "จาก PracticeScore เขียนกำลังใจ 1–2 บรรทัดสำหรับเด็ก/ผู้ใหญ่ บอกจุดที่ควรฝึก (focus) แบบเป็นกันเอง ห้ามเปลี่ยนตัวเลขหรือเกรด ห้ามวิเคราะห์นิสัยจากลายมือ"
**A5 — Diary nudge**: "จาก DiarySummary เขียนข้อความเตือน 1 บรรทัด เช่น ชวนฝึกต่อสตรีค หรือชวนสร้างฟอนต์ v2 ห้ามเปลี่ยนตัวเลขหรือวันที่"
