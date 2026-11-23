# Work-order prompts — BrickBuddy

> ให้ AI codegen (Cursor / Claude / v0 / Lovable ฯลฯ) ทำทีละ prompt ตามลำดับ ใช้ `schemas.json` เป็นสัญญาข้อมูล และ `reference/brickbuddy.py` เป็นตรรกะต้นแบบ (port เป็น TypeScript ให้ผลเท่ากับ `tests.py`)

**P0 — Scaffold**: สร้าง PWA (Next.js หรือ Vite + React + Tailwind) มือถือก่อน ภาษาไทยเป็นหลัก สลับ EN ได้ ใช้ design tokens ใน prd.md (ครีม #FFF8EC แดง #D0312D เหลือง #F6C21C น้ำเงิน #1E5AA8, Kanit) port `brickbuddy.py` → `src/logic/brickbuddy.ts` พร้อม unit test เทียบ `tests.py` ทั้ง 36 ข้อ

**P1 — Age gate**: ถาม "ใครเล่น" (ชื่อเล่น + อายุ) + ปุ่มผู้ปกครองยืนยัน → `age_check()`; stop = ปิดกล้องพร้อมข้อความ; < 3 ปีแนะนำตัวต่อชิ้นใหญ่. Output `AgeCheck`.

**P2 — Camera & Scan QA**: กล้องหลัง ไกด์ "เกลี่ยเป็นชั้นเดียวบนพื้นเรียบสีพื้น" ประเมิน light/blur/spread/overlap ฝั่งเครื่อง → `scan_quality()`; ok=false แสดงทิปและให้ถ่ายใหม่. Output `PileScan`.

**P3 — Pile detection (A1)**: ย่อรูปส่ง A1 → `AiPileScan` (ชิ้น สี จำนวน ตำแหน่ง 0..1 + hazards) → ถ้ามี battery/magnet → `age_check(found=...)` stop; ตัดชิ้น confidence < 0.5 → `inventory()`; หน้า Inventory แสดงชิปสีพร้อมปุ่ม +/− แก้จำนวน. Output `Inventory`.

**P4 — Build ideas**: `suggest_builds(inv, age, minutes)` → การ์ด 6 ใบ (ป้าย "ต่อได้เลย" สีเขียว / "ขาด 1 ชิ้น" สีส้ม, % ครบ, เวลา, ระดับ 1–3 ดาว, ชิปชิ้นทดแทน "ใช้ 1×2 ×2 แทน 1×4"); ฟิลเตอร์หมวด vehicle/animal/home/useful/seasonal/character. Output `BuildMatch[]`.

**P5 — Colours & Steps**: `assign_colors()` เลือกสีบทบาท main/accent/base/detail จากกอง → `build_steps()`; เรนเดอร์ภาพ isometric ต่อขั้นจากกริดปุ่ม (SVG/three.js เบา ๆ) ห้ามใช้ image generation; ปุ่ม "ขั้นถัดไป" ขนาดใหญ่สำหรับมือเด็ก + เสียงคลิก. Output `ColorAssignment`, `BuildSteps`.

**P6 — Find-It**: บนทุกขั้น แตะ "หาชิ้นนี้" → `find_piece()` → วาดวงแหวนเรืองแสง #7CF7FF ที่ตำแหน่งจริงบนรูปกอง + ป้ายช่อง A1–F4; ไม่เจอ → เสนอชิ้นทดแทน. Output `FindIt`.

**P7 — Daily challenge**: `daily_challenge(today)` การ์ดธีม + จำกัดชิ้น + ตัวจับเวลานับถอยหลัง; ส่งผลงานเข้า P8. Output `DailyChallenge`.

**P8 — Creation score (A2)**: ถ่ายผลงาน → A2 ประเมิน pieces_used/colors_used/symmetry/layers/on_theme → `creation_score()` → ดาวเด้ง + แบดจ์ + คำชม (A3). Output `CreationScore`.

**P9 — Sort & Stability**: `sort_plan(inv, bins, by)` แสดงกล่องเป็นสี + ป้ายพิมพ์ติดกล่อง; `stability(layers, base, stagger)` สไลเดอร์ความสูง/ฐาน มิเตอร์ แข็งแรง/โยก/ล้มแน่. Output `SortPlan`, `Stability`.

**P10 — Diary**: เก็บ IndexedDB build/challenge/sort → `diary_summary()` แกลเลอรี สตรีค แบดจ์; เตือนวันละครั้ง (A5). Output `DiarySummary`.

**P11 — Share / Reel / Quota / Guard**: `share_card()` 1080×1350 3 เลย์เอาต์ ลายน้ำ "BrickBuddy · AI วันละแอป" (เบลอหน้าคนอัตโนมัติ); `reel_plan()` → canvas 1080×1920 6 ช็อต 118 BPM → MediaRecorder; `quota()` ฟรี 3 สแกน/วัน; `safety_guard()` ทุก flag; ลบรูปกองหลังวิเคราะห์ ≤ 1 ชม.

**P12 — QA**: รัน `reference/tests.py` (36 tests) และ validate output ทุกตัวกับ `schemas.json`; ทดสอบกองบนพรมลาย/แสงไฟเหลือง/ชิ้นทับกัน/ชิ้นใส/ยี่ห้อปนกัน, กองที่มีเหรียญและแม่เหล็ก (ต้อง stop), อายุ 2 (ต้อง stop), ไอเดียที่ต้องใช้ชิ้นทดแทน, มือเด็กกดปุ่มใหญ่ได้.

## AI prompts

**A1 — Pile detector (vision, JSON only)**
```
คุณคือตัวนับชิ้นตัวต่อของแอป BrickBuddy ดูรูปกองตัวต่อบนพื้น แล้วตอบ JSON ตาม schema AiPileScan เท่านั้น
- pieces: [{part, color, count, confidence 0..1, positions: [[x,y] 0..1 ของกลุ่มชิ้นนั้นในรูป]}]
  part ต้องเป็นหนึ่งใน: brick_2x4 brick_2x2 brick_1x4 brick_1x2 brick_1x1 plate_2x4 plate_2x2 plate_1x2 slope_2x2 tile_1x2 round_1x1 wheel window eye_1x1
  color ต้องเป็นหนึ่งใน: red blue yellow green white black gray orange brown pink tan trans_clear
- นับปุ่ม (studs) เพื่อแยก 2×4 กับ 2×2 ให้ถูก แผ่น (plate) สูงราว 1/3 ของอิฐ
- hazards: battery (ถ่านกระดุม) magnet coin face sharp ถ้าเห็น
- connected_clumps: จำนวนกลุ่มชิ้นที่ต่อติดกันอยู่ (นับไม่ได้แม่น)
ห้ามเดาชื่อแบรนด์ ถ้าไม่แน่ใจชิ้นไหนให้ confidence < 0.5
```
**A2 — Creation judge (vision, JSON only)**: "ดูรูปผลงานตัวต่อ ตอบ {pieces_used, colors_used, symmetry 0..1, layers, on_theme (ตรงธีม <theme_th> ไหม)} เท่านั้น ห้ามให้คะแนนเอง ห้ามติ ห้ามระบุตัวตนคนในรูป"
**A3 — Cheer writer**: "จาก CreationScore เขียนคำชม 1 บรรทัดสำหรับเด็ก <age> ขวบ ภาษาไทยง่าย ๆ อบอุ่น ชมสิ่งที่ทำได้ดี (badges) และชวนลองอีกนิด ห้ามเปลี่ยนจำนวนดาว ห้ามเปรียบเทียบกับเด็กคนอื่น"
**A4 — Story mode**: "แต่งนิทาน 4 บรรทัดให้ผลงาน <name_th> ที่เด็กเพิ่งต่อเสร็จ ใช้สี <roles> เป็นรายละเอียด จบด้วยคำถามชวนต่อชิ้นต่อไป ไม่มีความรุนแรง"
**A5 — Diary nudge**: "จาก DiarySummary + DailyChallenge วันนี้ เขียนข้อความเตือน 1 บรรทัดชวนเล่นต่อสตรีค ห้ามเปลี่ยนตัวเลขหรือวันที่"
