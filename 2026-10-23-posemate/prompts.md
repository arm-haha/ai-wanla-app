# PoseMate (โพสท่าไม่เป็น) — Prompt สั่งงาน (จัดเต็ม)

ใช้คู่กับ `prd.md` · `schemas.json` · `examples.json` · `reference/posemate.py`
สแต็ก: Next.js 14 App Router + TypeScript + Tailwind + shadcn/ui + framer-motion + MediaPipe Tasks Vision + PWA + Vercel
สี UI: cream `#FFF7EE` · ink `#1F1A2E` · coral `#FF6B5A` · sunset `#FFB347` · lavender `#B8A4FF` · mint `#3DDC97` · ghost `#7DF9FF` · warn `#F43F5E`
ฟอนต์: Kanit (หัวข้อ/ตัวเลข) + IBM Plex Sans Thai
กติกาเหล็ก: คะแนนและการเลือกท่าคำนวณตาม `reference/posemate.py` เท่านั้น — AI แค่ **อ่านฉาก (spot/light/clutter/tilt/bg_hex)** และ (ถ้าเปิด) เขียนแคปชัน · ห้าม AI ให้คะแนนหน้าตาหรือหุ่น

ตัวเลขเดโมที่ล็อก (น้ำหวาน สมมติ): ฉาก cafe_window + แสงหน้าต่าง → การ์ด `p_cup_sip`, `p_window_lean`, `p_chin_rest` · ท่าพิงหน้าต่าง ยืนแข็ง 65% → ตรงท่า 94% · รูปก่อน 30 (ลองใหม่ 😅) → หลัง 94 (ปังมาก 🔥) · เสื้อครีม 16 จม vs สีอิฐ 64 เด้ง · grid balance 90

---
## Prompt A — โครงโปรเจกต์ + engine
สร้าง Next.js 14 PWA ชื่อ PoseMate ตาม prd.md พอร์ต `reference/posemate.py` เป็น `lib/posemate.ts` ทีละฟังก์ชัน (scene_read, pose_cards, pose_match, angle_coach, shot_score, glow_up, caption_pack, grid_plan, outfit_pop) ใช้ POSES/ANGLE/LIGHT/W ตาม examples.json สร้าง types จาก schemas.json ($defs) เขียน vitest ให้ทุกค่าใน `expect_locked` ผ่าน ตั้ง theme สี/ฟอนต์ข้างบน

## Prompt B — Spot Scan
หน้า `/spot` เปิดกล้องหลัง กรอบเต็มจอ ข้อความ "ถ่ายฉากเปล่าก่อน 1 รูป" ย่อ ≤768px ส่ง `/api/scene` (AiSceneRequest) → AiSceneResponse → `scene_read` แสดงชิป: จุด, แสง (สีเขียว ≥90 / เหลือง / แดง <50), ของเกะกะ, tip_th มีตัวเลือกจำนวนคน 1–4 และโหมดเลือกจุดเองถ้าไม่อยากถ่าย

## Prompt C — Pose Cards
`/poses` การ์ด 3 ใบ (framer-motion stagger) แต่ละใบมีภาพโครงท่าวาดจาก `kp` เป็นเส้นสี ghost ชื่อท่า cue_th ระดับความยาก (●○○) ป้าย shot ปัดเลือก กดหัวใจเก็บเข้า Library ท่ากลุ่ม (kp = null) ใช้ภาพไอคอน + cue แทนเงา

## Prompt D — Ghost Overlay (wow)
`/shoot` กล้องหลัง (หรือหน้าในโหมดถ่ายเอง) + MediaPipe Pose Landmarker รันบนเครื่อง map 33 จุดเป็น 9 จุดตามลำดับ KP แล้วเรียก `pose_match` ทุก 150ms วาดเงาท่าเป้าหมายเป็นเส้นเรืองแสง `#7DF9FF` ซ้อน ตัวเลข "ตรงท่า xx%" ใหญ่ด้านบน + ข้อความบอกจุดที่ห่างสุด (worst_th) เมื่อ ≥85 เงาเปลี่ยน `#3DDC97` สั่น + เสียงติ๊ง และเปิดปุ่มถ่าย (หรือถ่ายอัตโนมัติ 3 วิ) แสดงเส้นตาราง 1/3 และ level bar จาก DeviceOrientation

## Prompt E — Angle Coach + Friend Mode
แผงล่างของ `/shoot` แสดง `angle_coach` (ความสูง, องศา, เลนส์, ระยะ, tip) ปุ่ม "โหมดเพื่อนถ่าย" สลับเป็นจอเต็ม พื้น ink ตัวหนังสือ ≥40px ทีละ cue (friend_cues_th) ปัดไปข้อถัดไป และไฮไลต์ lens ที่ต้องกด

## Prompt F — Shot Score + Glow-up Card
`/score` รับรูปที่ถ่าย (หรือเลือกรูปเก่าจากแกลเลอรี) วัด tilt (DeviceOrientation/เส้นขอบฟ้าจาก AI), ตำแหน่งคนและ headroom จาก landmarks, แสงจาก scene, clutter, pose → `shot_score` แสดงวงคะแนนวิ่ง + แถบ 6 ด้าน + fixes_th 3 ข้อ ถ้ามีรูปก่อน/หลัง ทำ `glow_up` เป็นการ์ด 1080×1920 split แนวตั้ง ตัวเลข before → after ใหญ่ watermark "PoseMate · AI วันละแอป" ปุ่มเซฟ/แชร์ (Web Share)

## Prompt G — Caption Pack
`/caption` แสดง 3 แคปชันจาก `caption_pack` + ปุ่ม "ให้ AI เขียนใหม่" (`/api/caption`, AiCaptionRequest/Response, mood 4 แบบ) แต่ละอันมีปุ่มคัดลอก แฮชแท็กเป็นชิปเลือกได้

## Prompt H — Outfit Pop + Group + Grid
`/outfit` แตะเสื้อในรูปเพื่อดูดสี + ดูดสีฉากหลัง → `outfit_pop` แสดงเด้ง/จม พร้อมคำแนะนำย้ายมุม · โหมดกลุ่มใช้ `pose_cards` ตามจำนวนคน · `/grid` เลือก 9 รูป ติดป้าย kind (AI หรือผู้ใช้แตะ) อ่าน hue เฉลี่ย → `grid_plan` แสดงตาราง 3×3 ก่อน/หลังจัด + balance

## Prompt I — Library + Me + Storage
`/library` ท่าทั้งหมดกรองตามจุด/จำนวนคน · `/me` streak + session ล่าสุด (before/after) เก็บ LocalStore ใน IndexedDB ตาม schema ห้ามเก็บรูปคน ปุ่มลบข้อมูลทั้งหมด

## Prompt J — QA + /reel-demo
หน้า `/reel-demo` โหลด fixture จาก examples.json เล่นลำดับ reel_script อัตโนมัติ (รูปก่อน 30 → การ์ด 3 ท่า → เงา 65→94 → friend mode → glow-up 30→94 → แคปชัน → grid) สำหรับอัดจอ ตรวจ: vitest ผ่าน, Lighthouse PWA ≥90, ไม่มีรูปคนใน network, ข้อความไทยไม่ล้นจอ 360px

---
## Runtime K — Scene reader (vision, `/api/scene`)
System: "คุณอ่านรูปฉากถ่ายภาพ ตอบ JSON ตาม AiSceneResponse เท่านั้น spot ต้องเป็นหนึ่งใน cafe_window, street_wall, stairs, beach, nature, mirror (เลือกที่ใกล้ที่สุด) light: side/window/front/shade/top/back เทียบกับตำแหน่งที่คนจะยืนหันหน้าเข้ากล้อง clutter = จำนวนของเกะกะเด่นๆ ในฉากหลัง (0–10) horizon_tilt_deg = องศาเอียงของเส้นแนวนอนหลัก bg_hex = สีเด่นของฉากหลัง note_th ≤100 ตัวอักษร ห้ามพูดถึงคนในภาพ"

## Runtime L — Caption writer (`/api/caption`)
System: "เขียนแคปชันไทยสั้น 3 อัน (≤60 ตัวอักษร) สำหรับรูปที่ {spot} ท่า {pose_name_th} อารมณ์ {mood} ไม่ใช้คำหยาบ ไม่พูดถึงรูปร่างหน้าตา ตอบ JSON {captions_th:[...]}"

## Runtime M — Reel caption
"เขียนแคปชัน Reel ไทย 2 บรรทัด + CTA 'คอมเมนต์ โพส รับลิงก์ฟรี' สำหรับคลิปที่แอป PoseMate เปลี่ยนรูปคาเฟ่จาก 30 เป็น 94 คะแนน"
