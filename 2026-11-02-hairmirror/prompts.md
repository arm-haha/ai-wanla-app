# Work-order prompts — HairMirror (วางทีละอันใน v0 / Lovable / Bolt / Cursor)

**P0 — Scaffold**
สร้างเว็บแอป mobile-first ชื่อ "HairMirror — ลองทรงก่อนตัด" React + Vite + Tailwind ภาษาไทยทั้งหมด ธีม salon cream #FAF7F2, ink #1A1A1A, silver #C9CED6, accent #FF5C8A, mint #2EC4B6, warn #F59E0B, danger #E11D48 ฟอนต์ Prompt + IBM Plex Sans Thai มุม 20px bottom tab 5 แท็บ: ส่องกระจก / ลองทรง / โหวต / การ์ดช่าง / ไดอารี เก็บข้อมูล localStorage ตาม schemas.json (Profile, Style, CutLog, Vote) ไม่ต้องล็อกอิน ปุ่ม "ลองด้วยข้อมูลตัวอย่าง" โหลด fixture ของภูมิ

**P1 — Onboarding**
3 สเต็ป: สภาพผม (ตรง/หยัก/หยิก/ฟู + บาง/กลาง/หนา + ยาวกี่ซม.), จัดทรงได้กี่นาที/วัน (สไลเดอร์ 0–20), งบดูแล/เดือน (฿0–1,000), สไตล์ (masc/femme/any) บันทึก Profile

**P2 — Logic module**
พอร์ต reference/hairmirror.py เป็น TypeScript (lib/hair.ts): faceShape, monthlyUpkeep, styleMatch, rankStyles, growOut, pollTally, colorCheck, barberCard, cutReminder, yearCost ปัดทศนิยม 2 ตำแหน่ง ผลต้องตรง examples.json เขียน vitest ตาม tests.py ใส่ catalog 9 ทรงจาก fixtures.py เป็น data/styles.json (+ แยก masc/femme ได้ภายหลัง)

**P3 — Selfie Cam + Face Shape Scan**
กล้องหน้าพร้อมกรอบวงรีนำทาง เช็กแสงสว่าง/หน้าตรง ถ่ายแล้วส่ง vision ด้วย LANDMARK PROMPT → FaceLandmarkExtract ถ้า face_found=false หรือ confidence<0.6 ขึ้น retake_reason_th ให้ถ่ายใหม่ จากนั้น faceShape() แล้วแอนิเมชันวาดเส้นกรอบหน้า 4 เส้น (ยาว/หน้าผาก/โหนก/กราม) ก่อนเฉลย "คุณคือ หน้ากลม"

**P4 — AI Try-On Grid (WOW)**
rankStyles() เอา 9 ทรงทั้งหมด สร้าง TryOnRequest ต่อทรงด้วย TRY-ON PROMPT (image edit model, keep_identity, seed คงที่) ยิงพร้อมกันไม่เกิน 3 ช่อง แสดง grid 3×3 ช่อง skeleton กระพริบ แล้ว flip เปิดทีละช่อง ป้ายคะแนนมุมขวา (ปัง=mint, ลองได้=warn, เสี่ยง=danger) ถ้า identity_ok=false ให้ status=retry สร้างใหม่ 1 ครั้งแล้วค่อยซ่อนช่อง

**P5 — Style Detail: Before/After + Score**
แตะช่อง → สไลเดอร์ลากก่อน/หลังเต็มจอ ด้านล่าง: คะแนน 0–100 วงแหวนแยก 4 ส่วน (หน้า/ผม/เวลา/งบ), reasons_th เป็นชิป, ค่าดูแล ฿/เดือน ฿/ปี (yearCost), ปุ่ม "ใส่ในโหวต" "ทำการ์ดช่าง" "ไว้ยาวอีกนานไหม" (growOut จาก current_length_cm ถึง target ของทรง)

**P6 — Friend Vote**
เลือก 2–4 ทรง → สร้างลิงก์ /v/:pollId (ใช้ Supabase/Firebase ตาราง votes หรือ mock ด้วย localStorage ในโหมดเดโม) เพื่อนเปิดเห็นการ์ดทรง ใส่ชื่อเล่น กดโหวต 1 ครั้ง (โหวตซ้ำ = แทนที่) หน้าผลแสดงแท่ง % แบบ live + มงกุฎผู้ชนะ หรือ "เสมอ! ให้ช่างตัดสิน" ใช้ pollTally() ทิ้งเสียงที่ option ไม่อยู่ในโพล

**P7 — Barber Card**
จากทรงที่ชนะ สร้าง BarberCard: ภาพหัวด้านข้าง/หลังวาดโซนสีพร้อมความยาวเป็นมิล (top/fringe/sides/back/neckline แก้ได้), กล่อง "พูดกับช่างแบบนี้" ตัวใหญ่, ข้อห้าม, ภาพลองทรง + ภาพก่อน โหมดเต็มจอความสว่างสูงสำหรับยื่นช่าง ปุ่มบันทึกเป็นรูป

**P8 — Color Try-On + Bleach Check**
พาเลต 7 สี (ทองแดง, น้ำผึ้ง, ช็อกโกแลต, ash brown, ash, ชานม, ดำน้ำเงิน) + ระดับ 1–10 + undertone (warm/cool/neutral; ปุ่ม "ช่วยดู" ใช้ vision ประเมินจากเส้นเลือดข้อมือ = แค่คำแนะนำ) image edit เปลี่ยนสีผมอย่างเดียว ด้านล่างแสดง colorCheck(): ต้องฟอกไหม กี่รอบ ราคาประมาณ (ตั้งราคาร้านเองได้) และ warning_th

**P9 — Diary + Reminder**
บันทึก CutLog (วันที่ ทรง ร้าน ราคา รูปหลังตัด คะแนน 1–5 โน้ต) timeline รูปเรียงตามเวลา cutReminder() ตั้ง notification (Web Push หรือ .ics) "ถึงรอบเก็บทรงแล้ว" สรุปใช้เงินกับผมปีนี้ ฿

**P10 — Share Cards**
5 การ์ด 1080×1920 (try_on_grid, before_after, poll, barber_card, face_shape) html-to-image ตัวเลขใหญ่สีชมพู #FF5C8A บน cream + disclaimer_th เล็ก + โลโก้ "AI วันละแอป" ปุ่มแชร์ IG Story / LINE

---
**LANDMARK PROMPT (vision)**
คุณวิเคราะห์เซลฟี่หน้าตรง ตอบ JSON ตาม FaceLandmarkExtract เท่านั้น: face_found, face_length (ไรผมถึงปลายคาง), forehead_w (ความกว้างหน้าผากจุดกว้างสุด), cheek_w (โหนกแก้มกว้างสุด), jaw_w (มุมกรามซ้าย-ขวา) ทั้งหมดหน่วยเดียวกันเป็นสัดส่วนพิกเซลของรูป, hairline_visible, current_hair {type, length_cm โดยประมาณ, natural_level 1–10}, confidence 0–1, retake_reason_th ถ้าหน้าเอียง/มีของบัง/มืดให้ค่าที่วัดไม่ได้เป็น null และ confidence ต่ำ ห้ามเดา ห้ามประเมินความสวย อายุ เชื้อชาติ หรือเพศ

**TRY-ON PROMPT (image edit)**
แก้ไขเฉพาะทรงผมของคนในรูปให้เป็น "{style_name_en}" ({barber_phrase_th}) ความยาวโซน: {zones} สีผมเดิม เส้นผม{hair_type} สมจริงเหมือนรูปถ่ายจากร้านตัดผม แสงตามรูปต้นฉบับ ห้ามเปลี่ยนใบหน้า ตา จมูก ปาก สีผิว รูปร่าง เสื้อผ้า และพื้นหลัง ห้ามแต่งหน้า ห้ามทำให้ผิวขาวหรือหน้าเรียวขึ้น มุมกล้องเดิม

**IDENTITY CHECK (vision, ต่อภาพ)**
เทียบภาพ A (ต้นฉบับ) กับภาพ B (ลองทรง) ตอบ {"identity_ok": bool, "changed_non_hair": [..]} identity_ok=false ถ้าสิ่งอื่นนอกจากผมเปลี่ยน (รูปหน้า สีผิว ตา ฟัน เสื้อ พื้นหลัง)

**COLOR PROMPT (image edit)**
เปลี่ยนเฉพาะสีผมเป็น {color_family} ระดับ {target_level}/10 ให้รากผมเนียน คงทรงและทุกอย่างนอกจากสีผม
