# Work-order prompts — DoodlePop

ใช้ทีละข้อกับ AI codegen (Cursor / Lovable / v0 ฯลฯ). Stack แนะนำ: Next.js + Tailwind (PWA, mobile-first) + API route เรียก vision model / segmentation; แอนิเมชันใช้ 2D mesh deformation บน canvas/WebGL (เช่น PixiJS mesh หรือ skeletal rig แบบ Spine-like) + ffmpeg.wasm สำหรับ MP4/GIF. ใช้ `schemas.json` เป็น type กลาง และ `reference/doodlepop.py` เป็น logic อ้างอิง (port เป็น TS ให้ผลตรงกับ tests).

**P0 — Scaffold**: สร้าง PWA ภาษาไทย mobile-first ชื่อ DoodlePop ตาม design tokens ใน prd.md (กระดาษ #FFF8E7, สีเทียนแดง/เหลือง/ฟ้า/เขียว/ชมพู, ฟอนต์ Mali + Noto Sans Thai, ปุ่ม ≥56px). Bottom nav: แกลเลอรี · สแกน · นิทาน · ของเล่น. เก็บข้อมูลใน IndexedDB ตาม `Kid`, `Drawing` (ไฟล์ภาพเก็บ local). หน้าแรกให้เลือกลูก (อวาตาร์ ไม่ใช้รูปหน้า).

**P1 — Doodle Snap**: กล้อง + overlay กรอบกระดาษ. ส่งภาพไป AI ตาม A1 ได้ `ScanExtract`. ถ้า `has_child_face=true` ทิ้งภาพทันทีไม่บันทึก แสดง `retake_reason_th`. port `scan_score()` + `retake_reason()` แสดงเกจ 0–100 + ป้าย (ถ่ายใหม่ดีกว่า/ใช้ได้/ชัดมาก). Output `ScanReport`.

**P2 — Cleanup**: port `cleanup_steps()` รันตามลำดับ (perspective → deshadow → remove_paper → sharpen_lines → fill_gaps → cutout) ใช้ A2 สำหรับ segmentation/cutout. แสดงอนิเมชันกระดาษ "ลอก" ออกเหลือตัวละคร (ช็อตสำคัญใน Reel). ยางลบ/แปรงเติมให้แม่แก้ขอบได้.

**P3 — Auto Rig**: ใช้ `parts` จาก A1 + A3 (ตำแหน่งข้อต่อ) → port `rig()` วาดหมุดข้อต่อบนตัวละคร ลากแก้ได้. ถ้า `needs_manual_pins` ให้วิซาร์ด 3 ขั้น "แตะหัว → แตะตัว → แตะขา". Output `Rig`.

**P4 — Bring to Life** (wow): การ์ดใหญ่ 6 ท่าจาก `rig().presets` พร้อมไอคอน (โบกมือ กระโดด เต้น เดิน หมุนตัว นอนหลับ; fallback ส่ายตัว/กระดึ๊บ). แตะแล้วเล่นทันทีบนพื้นหลังกระดาษ + เงาใต้เท้า + เสียงเอฟเฟกต์. port `clip()` (ความยาว wave 2 วิ jump 1.5 dance 4 walk 2 spin 2 sleep 3). ปุ่ม "Before/After" ให้กระดาษเดิมค่อยๆ กลายเป็นตัวขยับ. Output `AnimationClip`.

**P5 — Share as Reel/GIF/MP4**: port `export_spec()` — reel_mp4 1080×1920@30, square_mp4 1080×1080@30, gif 480×480@12 (≤6 วิ ไม่มีเพลง). เลือกเพลงจากคลังลิขสิทธิ์ฟรี 6 เพลง, ลายน้ำ "Made with DoodlePop" มุมล่าง, เทมเพลต Reel: 2 วิกระดาษ → 1 วิลอกกระดาษ → ท่าวน. ต้องผ่าน `parent_gate("export_video")`. สร้าง `share_card()` (ไม่มีหน้าเด็ก).

**P6 — Story Maker**: ลูกแตะเลือกตัวละคร 1–3 ตัวจากแกลเลอรี → port `story_plan(age, n)` (≤4 ขวบ 4 หน้า, 5–6 ขวบ 5 หน้า, 7+ 6 หน้า) → เรียก A4 ได้ `Story`. โหมดอ่าน: หน้าละ 1 จอ ตัวละครขยับตาม `pose`, ไฮไลต์คำตามเสียง TTS ไทย หรือเสียงแม่อัดเอง. ปุ่ม "สร้างใหม่" นับโควตา.

**P7 — Family Gallery + Year Recap**: port `gallery()`, `age_at()`, `detail_score()`, `year_recap()`. ไทม์ไลน์แนวตั้งตามลูก ป้ายอายุตอนวาด. Year Recap เป็นสไลด์โชว์ 15 วิ (รูปแรก vs ล่าสุด + "รายละเอียดเพิ่มขึ้น 26%") ส่งออกเป็น Reel ได้.

**P8 — Sticker Pack**: เลือกรูป × ท่า → port `sticker_pack()` + `fit_box()` (370×320, เลขคู่) ใส่ขอบขาว 8px + คำพูดไทย (`PRESET_TH`) → zip PNG พร้อม main/tab image ตามแนวทาง LINE Creators Market.

**P9 — Coloring Page**: A5 แปลงเป็นลายเส้น, เส้นหนาตาม `coloring_line_px(age)`, ระบายในแอปด้วยนิ้ว (bucket fill) หรือพิมพ์ A4. Output `ColoringPage`.

**P10 — Daily Draw Prompt + Grandparent Share**: port `daily_prompt()` (ไม่ซ้ำ 30 วัน) แสดงบนหน้าแรกพร้อมปุ่ม "วาดเสร็จแล้ว สแกนเลย". `share_link()` ลิงก์ดูอย่างเดียว 7 วัน, ลบ EXIF/location, `noindex`, ต้องผ่านด่านผู้ปกครอง.

**P11 — Print Gift + Parent controls + Quota**: port `print_check()` แสดงการ์ด แก้ว/เสื้อ/โปสเตอร์ A4/สติกเกอร์ 7 ซม. เขียว/แดงตาม dpi. `parent_gate()` ด้วยโจทย์บวกเลข 2 หลักหรือ PIN 4 หลัก. `quota()` ฟรี 3 แอนิเมชัน + 1 นิทาน/วัน, paywall แบบสุภาพในโหมดผู้ปกครองเท่านั้น (ไม่โชว์ในโหมดเด็ก).

**P12 — Tests**: เขียน unit test TS ให้ตรงกับ `reference/tests.py` ทั้ง 27 ข้อ และ validate payload ทุกตัวด้วย `schemas.json`.

## AI prompts
**A1 Doodle scan** (vision, JSON mode, ตอบตาม `ScanExtract`):
"คุณคือผู้ช่วยสแกนรูปวาดเด็ก ดูภาพกระดาษรูปวาดที่ถ่ายด้วยมือถือ. หา 4 มุมกระดาษ (normalized 0–1 ตามเข็มนาฬิกาจากซ้ายบน), ให้คะแนน 0–1 สี่ด้าน (shadow เงา, blur เบลอ, tilt เอียง, crop_cut รูปวาดโดนตัดขอบ), บอกประเภทตัวละคร (animal/person/robot/vehicle/house/monster/plant/other), ตั้งชื่อน่ารักภาษาไทย, นับส่วน head/body/arms/legs/tail/wings, นับจำนวนสีเทียน, บอกว่ามีตัวหนังสือในรูปไหม. ถ้าในภาพมีหน้าเด็กจริง ให้ has_child_face=true และห้ามบรรยายเด็ก. ถ้าไม่เจอรูปวาด drawing_found=false พร้อมเหตุผลสั้นๆ ภาษาไทย."

**A2 Cleanup/cutout** (segmentation/image model): "Extract the hand-drawn crayon character from this paper photo. Remove paper texture, shadows and background to transparent PNG. Keep the child's original lines, colors, wobbles and proportions exactly — do NOT redraw, beautify, add details or change the style. Close small gaps in outlines only."

**A3 Joint finder** (vision, JSON): "จากภาพตัวละครพื้นใส ให้ตำแหน่งข้อต่อ normalized: head, neck, hip, และ shoulder/elbow/hand, hip/knee/foot ของแต่ละแขนขา, tail_base/tail_tip, wing_base ถ้ามี. ถ้าไม่แน่ใจให้ confidence < 0.5 เพื่อให้ผู้ใช้แก้หมุดเอง."

**A4 Bedtime story** (text, JSON ตาม `Story.pages`):
"แต่งนิทานก่อนนอนภาษาไทยสำหรับเด็กอายุ {age} ปี จำนวน {pages} หน้า หน้าละไม่เกิน {words_per_page} คำ ตัวละครคือ {characters: ชื่อ + ลักษณะจากรูปวาด}. ภาษาง่าย ประโยคสั้น มีคำซ้ำให้เด็กพูดตาม, เรื่องอบอุ่นเรื่องมิตรภาพ/ความกล้าหาญเล็กๆ, ห้ามน่ากลัว ห้ามความรุนแรง ห้ามแบรนด์สินค้า, หน้าสุดท้ายจบด้วยการเข้านอนอย่างสงบ. แต่ละหน้าระบุ drawing_ids ที่ปรากฏ และ pose จาก {presets}."

**A5 Line-art**: "Convert this crayon drawing into clean black outline line-art for a coloring page, {line_px}px strokes at A4 300 dpi, closed regions for bucket fill, white fill, keep the child's shapes."
