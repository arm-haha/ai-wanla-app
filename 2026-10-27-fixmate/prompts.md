# FixMate — Work-order prompts (วางทีละข้อใน AI codegen)

**P0 Setup** — สร้าง React + Vite + Tailwind PWA ชื่อ FixMate ภาษาไทย mobile-first. ใช้ design tokens จาก prd.md, font Prompt. โครง routes: /, /diagnose, /safety, /verdict, /parts, /steps, /done, /care, /profile. state ด้วย zustand + localStorage. โหลด `schemas.json` + `examples.json` เป็น mock data โหมด Demo.

**P1 Core logic** — port `reference/fixmate.py` เป็น `src/lib/fixmate.ts` (safety_gate, diy_cost, verdict, drip_waste, step_progress, care_schedule, savings_tally, pro_message) ให้ผลตรงกับ examples.json ทุกตัว + เขียน vitest ตาม `reference/tests.py`.

**P2 Snap & Diagnose** — หน้า Home ปุ่มกล้องใหญ่ (getUserMedia/อัปโหลด). ส่งรูปไป `/api/diagnose` คืน JSON ตาม `$defs/Diagnosis` เท่านั้น. แสดงรูปพร้อม pin (xy 0–1) แอนิเมชันเด้ง, การ์ดสาเหตุเป็นแถบ %, chip ความยาก 1–5, เวลา.

**P3 Safety Gate** — เรียก safetyGate(diag). STOP: จอแดงเต็ม ไอคอนสั่น อ่าน reasons ทีละบรรทัด ปุ่ม "ส่งข้อความหาช่าง" (P6) ไม่มีปุ่มซ่อมเอง. CAUTION: แถบเหลือง + checklist ยืนยันก่อนไปต่อ; low_confidence → ปุ่มถ่ายเพิ่ม.

**P4 Parts & Tools** — list อะไหล่ (name_th, search_kw ปุ่มคัดลอก, ช่องราคาแก้ได้ default จาก AI แต่ติดป้าย "ราคาประมาณ กรอกเองได้"). Toggle เครื่องมือที่มี (sync profile.owned_tools). รวมยอดสด.

**P5 Verdict split-screen** — ซ้าย "เรียกช่าง ฿X" (ช่องกรอกใบเสนอ), ขวา "ซ่อมเอง ฿Y · Z นาที". นับเลขวิ่ง + confetti เมื่อ verdict=diy แสดง "ประหยัด ฿…". need_photo → กลับไปถ่าย.

**P6 Pro message** — สร้างข้อความจาก proMessage() ปุ่ม แชร์ LINE (line.me/R/share?text=) / คัดลอก / SMS. ห้ามส่งอัตโนมัติ.

**P7 Fix Steps** — การ์ด swipe ทีละขั้น รูปพร้อม arrow_xy, warn_th สีเหลือง, timer ต่อขั้น, ปุ่ม "เสร็จ" อัปเดต stepProgress, ปุ่ม "ติดตรงนี้" เปิดแชตแนบรูป (P9).

**P8 Done + Reel Card + Tally** — ถ่ายรูป after, สร้าง ReelCard 9:16 (before/after slider, stat, โลโก้) export PNG ด้วย html-to-image. บันทึก fix ลง history → savingsTally + badge. Care Calendar หน้า /care จาก careSchedule() เรียงเกินกำหนดก่อน + Notification API.

**P9 Stuck chat** — `/api/ask` ส่ง context (diagnosis, step id, รูปใหม่) คืนคำแนะนำสั้น ≤ 3 บรรทัด; ถ้าเจอ hazard ใหม่ให้คืน hazard_tags แล้ววิ่ง Safety Gate ใหม่.

## System prompt — /api/diagnose (vision)
คุณคือช่างซ่อมบ้านมืออาชีพ ดูรูปแล้วตอบ JSON ตาม schema Diagnosis เท่านั้น ภาษาไทยง่าย. ใส่ hazard_tags ทุกอย่างที่เห็นหรือสงสัย (gas_smell, burn_mark, sparking, water_near_power, ceiling_sag, structural_crack, main_panel, refrigerant, hot_surface_smell, ladder_over_2m, power_tool, sharp_edge, heavy_lift, shutoff_unknown). ถ้าไม่แน่ใจให้ confidence ต่ำ ห้ามเดา. causes รวม p ≈ 1. ไม่ต้องตัดสินว่าซ่อมเองได้ไหม — ระบบตัดสินเอง. พร้อม parts (ชื่อไทย + search_kw), tools, steps (≤ 7 ขั้น, ขั้นแรกต้องเป็นการตัดน้ำ/ไฟเสมอเมื่อเกี่ยวข้อง).
