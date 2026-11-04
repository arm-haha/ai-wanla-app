# ToneMe (สีไหนใช่เรา) — Prompt สั่งงาน (จัดเต็ม)

ใช้คู่กับ `prd.md` · `schemas.json` · `examples.json` · `reference/toneme.py`
สแต็ก: Next.js 14 App Router + TypeScript + Tailwind + shadcn/ui + framer-motion + PWA + Vercel
สี UI: linen `#FBF7F2` · ink `#2B2238` · rose `#E8879B` · peach `#F6B48F` · sage `#8FB8A0` · sky `#8DB6E8` · gold `#D4A64A` · no `#E5484D`
ฟอนต์: Kanit (หัวข้อ/ตัวเลข) + IBM Plex Sans Thai
กติกาเหล็ก: คอร์ deterministic ตาม `reference/toneme.py` — AI แค่ **หากรอบแก้ม/หน้าผาก/ผม/ม่านตา + เช็กแสง** และ (ถ้าเปิด) เขียนแคปชันสั้น · ห้าม AI ตัดสินซีซั่นหรือให้คะแนน

ตัวเลขเดโมที่ล็อก (มายด์ สมมติ): skin `#D9A27E` hair `#2B1D14` eyes `#3A2618` เส้นเลือดเขียว ใส่ทอง → **True Autumn 🍂** warmth 21 lightness 48 contrast 59 conf 78 · drape `#E8823F` 96 vs `#FF69B4` 0 · ชุด 50 → 96 · shop `#2A8C82` 91 · closet 50% · แก๊ง ครีมอูฐ 85

---
## Prompt A — โครงโปรเจกต์ + engine
สร้าง Next.js 14 PWA ชื่อ ToneMe ตาม prd.md พอร์ต `reference/toneme.py` เป็น `lib/toneme.ts` ทีละฟังก์ชัน (hex→Lab D65, ΔE76, analyze, color_score, drape_battle, palette_card, outfit_check, makeup, shop_scan, closet_audit, hair_guide, friend_compare) ใช้ค่าคงที่ PALETTES/MAKEUP/HAIR ตาม examples.json สร้าง types จาก schemas.json ($defs) เขียน vitest ให้ทุกค่าใน `expect_locked` ผ่าน ตั้ง theme สี/ฟอนต์ข้างบน

## Prompt B — กล้อง + light check + sampling
หน้า `/scan` เปิดกล้องหน้า มีกรอบวงรีวางหน้า ข้อความ "หันหน้าเข้าหน้าต่าง ไม่แต่งหน้า ปิดฟิลเตอร์" ถ่ายแล้วย่อ ≤1024px ส่ง `/api/scan` (AiScanRequest) ได้ AiScanResponse → ถ้า `light_ok=false` แสดง bad_light ตาม light_issue และปุ่มถ่ายใหม่ ถ้าผ่าน ใช้ canvas เฉลี่ยสีในแต่ละ region (ตัด 10% สว่าง/มืดสุดทิ้ง) → skin = เฉลี่ยแก้มซ้าย/ขวา/หน้าผาก ไม่ส่งรูปไปเก็บที่ไหน ลบ blob ทันทีหลังได้ hex มีโหมด "เลือกสีเอง" (color picker 3 ช่อง) สำหรับคนไม่อยากถ่าย

## Prompt C — Quiz + Reveal (wow)
`/quiz` 2 คำถามแบบการ์ดใหญ่: เส้นเลือดข้อมือ (เขียว/น้ำเงิน/ปนกัน/ไม่แน่ใจ) พร้อมรูปตัวอย่าง และทอง/เงิน → เรียก analyze → `/reveal` แอนิเมชัน: จุดสี 3 จุดลอยออกจากหน้า → แถบ warmth/lightness/contrast วิ่ง → การ์ดพลิกเผยซีซั่น + พาเลตต์ 12 สีกระจายเป็นวง (framer-motion stagger) + confidence ถ้า confidence < 65 แสดง "ก้ำกึ่ง ลองสแกนอีกครั้งในแสงอื่น"

## Prompt D — Drape Battle
`/drape` แสดงเซลฟี่ (เก็บแค่ใน memory ระหว่าง session) ครอบด้วยวงผ้าสีรอบคอ/ไหล่ เลือกสี A/B จากพาเลตต์ จากสีเลี่ยง หรือ color picker หรือถ่ายผ้าจริง ปัดซ้าย/ขวาสลับ A↔B แบบ split slider แสดงคะแนนและ line_th ผู้ชนะมีมงกุฎ เสียง "ติ๊ง" ปุ่มบันทึกคลิปสั้น 3 วิ (MediaRecorder ของ canvas) สำหรับลง Reel

## Prompt E — Palette Card
`/palette` การ์ด 1080×1920 (html-to-image): ชื่อ + ซีซั่น, 12 สีใช่ (วงกลม + ชื่อไทย + hex), 4 สีเลี่ยงขีดฆ่า, โลหะที่ใช่ watermark "ToneMe · AI วันละแอป" ปุ่ม "เซฟเป็นวอลเปเปอร์" และ "แชร์" (Web Share API)

## Prompt F — Outfit Check
`/outfit` ถ่ายรูปชุด แล้วแตะบนชิ้นผ้าเพื่อดูดสี (eyedropper บน canvas, เฉลี่ย 9×9 px) กำหนด slot ให้แต่ละจุด (top/bottom/outer/scarf/bag/shoes/glasses) → outfit_check แสดงคะแนนรวมใหญ่ + แถวรายชิ้น + chip สีแนะนำ แตะ chip = จำลองเปลี่ยนสีชิ้นนั้นแล้วคะแนนใหม่วิ่งขึ้น (เช่น 50→96)

## Prompt G — Makeup + Hair
`/makeup` แสดงกลุ่มสีลิป บลัช อายแชโดว์ เป็น swatch ใหญ่ ทาบบนเซลฟี่แบบโปร่ง (multiply ที่ region ปาก/แก้มโดยประมาณจาก AiScanResponse) พร้อม note_th ไม่ระบุยี่ห้อ · `/hair` 2 สีผมแนะนำ ทาบพรีวิวบน region ผม

## Prompt H — Shop Scan + Closet Audit
`/shop` กล้องหลังมีเป้ากลางจอ ดูดสีจุดกลาง → shop_scan แสดง ใช่/พอได้/ไม่ใช่ เต็มจอสีเขียว/เหลือง/แดง และสีใกล้สุด รองรับเลือกรูปจากแกลเลอรี (สกรีนช็อตแอปช้อป) · `/closet` เพิ่มไอเทม (ชื่อ + ดูดสี) → closet_audit กราฟโดนัท ใช่/พอได้/ไม่ใช่ + match_pct + "ซื้อต่อ 3 สี"

## Prompt I — Friend Group Color + Settings
`/friends` สร้างลิงก์เชิญ (เพื่อนสแกนเองแล้วส่งแค่ชื่อ + season กลับมาผ่าน query string ไม่มีรูป) หรือกรอกซีซั่นเอง → friend_compare การ์ดแก๊ง + สีกลาง · `/settings` ลบข้อมูลทั้งหมด, show_avoid, ข้อความ privacy + disclaimer

## Prompt J — QA + /reel-demo
สร้าง `/reel-demo` โหลด local_store ของมายด์ เล่นลำดับ reel_script อัตโนมัติ (ปุ่มถัดไปซ่อนมุมจอ) ตรวจ: ตัวเลขตรง expect_locked, ไม่มีรูปถูกเขียนลง storage, ข้อความ disclaimer อยู่ใน /reveal, ไม่มีคำเปรียบเทียบสีผิว, Lighthouse PWA ผ่าน, จอ 360px ไม่ล้น

---
## Runtime K — AI Scan (vision)
System: คุณช่วยหาตำแหน่งบนใบหน้าเพื่อดึงสีเท่านั้น ห้ามประเมินความสวย ห้ามบอกซีซั่น ห้ามพูดถึงสีผิวในเชิงดี/ไม่ดี
User: [รูป] ตอบ JSON ตาม AiScanResponse เท่านั้น: face_found, light_ok (false ถ้ามืด แสงเหลืองจัด มีฟิลเตอร์ ย้อนแสง หรือแต่งหน้าหนา), light_issue, regions เป็นกรอบ [x,y,w,h] 0–1 ของ cheek_l, cheek_r, forehead, hair, iris, note_th ≤100 ตัวอักษร

## Runtime L — AI Stylist Caption
Input: AiStylistRequest · Output: AiStylistResponse `caption_th` ≤90 ตัวอักษร โทนเพื่อนสาย แฟชั่น ใช้ชื่อสีไทยจากข้อมูลเท่านั้น ห้ามแต่งตัวเลขใหม่ ห้ามพูดถึงรูปร่าง/น้ำหนัก/สีผิว

## Runtime M — แคปชัน Reel
เขียนแคปชัน IG/TikTok ไทย 3 แบบ (สั้น/เล่าเรื่อง/ชวนคอมเมนต์) จาก expect_locked ปิดท้าย "คอมเมนต์ 'สี' เดี๋ยวส่งลิงก์ฟรี" + 5 แฮชแท็ก (#personalcolor #AIวันละแอป #ซีซั่นสี #แต่งตัว #สีที่ใช่)
