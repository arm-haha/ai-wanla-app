# LeafDoc — Prompt สั่งงาน (จัดเต็ม)

ใช้คู่กับ `prd.md` · `schemas.json` · `examples.json` · `reference/leaf.py`
สแต็ก: Next.js 14 App Router + TypeScript + Tailwind + shadcn/ui + framer-motion + PWA + Vercel
สี: cream `#F7F5EE` · forest `#14532D` · leaf `#22C55E` · lime `#A3E635` · sun `#FBBF24` · clay `#C2410C` · water `#0EA5E9` · ink `#1C1917`
คอร์ต้อง deterministic ตาม `reference/leaf.py` — AI แค่เสนอชนิดต้นกับอาการ ห้ามให้คะแนนหรือเปลี่ยนตัวเลข

ตัวเลขเดโมที่ล็อก (ป่าคอนโดของบีม 2026-10-19 หน้าฝน):
- คะแนน p1 **55** sick · p2 **70** fussy · p3 **100** thriving
- p1 สาเหตุ `overwater 11pt 50%` · `low_humidity 6pt 27%` · `root_rot 5pt 23%` · p2 `underwater 61%`
- รดน้ำ p1 ทุก 12 วัน ok ครบ 2026-10-29 · p2 ทุก 8 วัน overdue (ครบ 2026-10-15) · p3 ทุก 13 วัน ok 2026-10-23
- แผน 3/7 = 43% · ตรวจซ้ำ 2026-10-26 · Glow-up 55 → 94 (+39, 14 วัน, ใบใหม่ 2)
- Light 640 / 2560 / 20480 · Room Match spider 100, fern 50, pothos 40 · Wrapped 6 / 50% / 3 / overwater · streak 5 · XP 105 Lv2

---

## A) Master prompt สร้างทั้งแอป (วางครั้งเดียว)
```
คุณเป็น senior full-stack ที่จะสร้างแอป LeafDoc (หมอใบไม้) ตาม PRD ที่แนบ

เป้าหมาย: mini suite "ถ่ายใบเดียว → รู้ว่าต้นไม้ป่วยเพราะอะไร → มีแผนชุบชีวิต + ตารางรดน้ำที่ถูกต้อง" สำหรับคนเมือง/คอนโดไทย
ภาษา UI ไทยเป็นหลัก (ดู examples.json → ui_copy_th)

สแต็กบังคับ:
- Next.js 14 App Router + TypeScript + Tailwind + shadcn/ui + framer-motion
- PWA (manifest, icons, service worker, Notification API สำหรับเตือนรดน้ำ; ถ้าไม่อนุญาต → ป้ายในแอป) · mobile-first 390px · deploy Vercel
- local-first: localStorage key "leafdoc:v1" ตาม schema LocalStore · รูปเก็บ IndexedDB · ไม่มีล็อกอิน
- html-to-image สำหรับ Glow-up card และ Wrapped
- optional AI: /api/ai/vision (รูป → species_guess + symptoms + leaf_boxes ตาม AiVisionResponse) และ /api/ai/chat อ่าน process.env.AI_API_KEY
  ไม่มี key → แอปใช้ได้ครบด้วยการแตะชิปอาการเอง + demo

สี (ห้ามเปลี่ยน): --cream #F7F5EE --forest #14532D --leaf #22C55E --lime #A3E635 --sun #FBBF24 --clay #C2410C --water #0EA5E9 --ink #1C1917

Must-have 5 ฟีเจอร์ (ทำให้จบก่อน):
1) Leaf Snap → Health Score (wow: เส้นสแกน + กรอบอาการ + วงแหวนคะแนนนับขึ้นไล่สี)
2) Symptom Doctor (3 สาเหตุ + % รวม 100 + คำอธิบาย)
3) แผนชุบชีวิต 7 วัน (ติ๊กได้ + progress + นัดตรวจซ้ำ)
4) Smart Water Schedule (ชนิด×แสง×กระถาง×ฤดูไทย + แจ้งเตือน)
5) Glow-up Card before/after 1080×1920

Nice-to-have: Light Meter, Pet-safe Check, Room Match, My Jungle + Level + streak, Plant Wrapped, AI Care Chat

โครงสร้างไฟล์:
/lib/engine/{data.ts,round.ts,season.ts,water.ts,diagnose.ts,plan.ts,light.ts,pets.ts,match.ts,glow.ts,level.ts,wrapped.ts}
/lib/store.ts /lib/photos.ts (IndexedDB) /lib/share.ts /lib/notify.ts
/app/(screens)/{page.tsx,snap,checkup,result,plan/[id],plant/[id],light,match,glow/[id],wrapped,settings}
/app/api/ai/{vision,chat}/route.ts
/fixtures/demo.json (= examples.json ทั้งไฟล์)
/tests/engine.test.ts (vitest)

ขั้นแรก: สร้างโปรเจกต์ + ไฟล์ทั้งหมดเป็น skeleton + README สั้น แล้วหยุดรอ prompt ถัดไป
```

## B) Engine (port จาก Python ให้ตรงทุกตัวเลข)
```
Port reference/leaf.py เป็น TypeScript ใน /lib/engine ให้ผลลัพธ์ "ตรงทุกฟิลด์" กับ examples.json:
- species / symptoms / causes / plans / grades / factors โหลดจาก examples.json (อย่า hardcode ซ้ำ) ลำดับ key ของ causes สำคัญ (ใช้เป็น tie-break)
- rnd(x) = Math.floor(x + 0.5) ใช้ทุกที่ ห้าม Math.round กับค่าลบ ห้าม toFixed
- วันที่เป็น YYYY-MM-DD local ล้วน คำนวณต่างวันด้วย UTC midnight เพื่อกัน DST/timezone เพี้ยน
- seasonOf, waterInterval (max 1), waterStatus (overdue → next_dates เริ่มวันนี้, ไม่งั้นเริ่ม due_on)
- contextBonus ตาม reference ทุกเงื่อนไข (overwater: since*2 < iv → +2 · underwater: since*2 > iv*3 → +2)
- diagnose: symptoms เรียงตามลำดับ canonical ของ SYMPTOMS · เก็บ cause ที่ points > 0 · sort (-points, index) · top 3 · % half-up แล้วบวกเศษให้อันดับ 1 · คะแนน 100 − Σseverity − 5 (แสงต่ำกว่าที่ต้องการ >1 ขั้น) clamp 5..100
- rescuePlan (day 3 ได้ extra_th จากสาเหตุอันดับ 2), planProgress, luxFromLuma = rnd(10 * 2^(luma/20) * 2^ev), lightReading (direct → เฉพาะต้นที่ต้องการ direct), petCheck, roomMatch (50 − 25×ระยะแสง, pets&toxic −30, forgetful ±15, ac&humid −10, ×2 clamp 0..100, top 3), glowUp, careStreak, jungleLevel, plantWrapped (tie → เรียงชื่อ cause แล้วเอาตัวแรก)

เขียน vitest:
- ทุก diagnoses / water_status / rescue_plans / glow_up / light_readings / room_match / wrapped ใน examples.json → deepEqual
- expect_locked ทุกค่า
- property: % รวม 100 · คะแนน 5..100 · ทุก Cause มี plan 7 ข้อ
รัน test จนผ่านทั้งหมด แล้วรายงานผล
```

## C) Home + Snap + Checkup + Result (wow)
```
สร้างหน้า:
1) Home "/" — หัว "ต้นไม้ของฉัน" + การ์ดต้นแบบ grid 2 คอลัมน์ (รูป, ชื่อเล่น, วงแหวนคะแนนเล็ก, ป้ายรดน้ำสี water/clay ตามสถานะ) + FAB ใหญ่ "📸 ส่องใบ ตรวจสุขภาพ" + ปุ่ม "ลองป่าคอนโดของบีม (ตัวอย่าง)" โหลด demo.local_store
2) Snap — <input capture="environment"> + กรอบใบไม้โปร่ง · ย่อรูป ≤1024px · เก็บ IndexedDB
   มี AI key → POST /api/ai/vision → เติม species + ชิปอาการ + leaf_boxes · ไม่มี → ไปเลือกเอง
3) Checkup — ชิปอาการ 15 ตัว (ui toggle, ติ๊กจาก AI มี ✨) · คำถาม: ดิน (แฉะ/ชื้น ๆ/แห้ง) · แสงมุมนี้ (4 ระดับ + ปุ่ม "วัดเลย" ไป Light Meter) · รดล่าสุดกี่วัน (stepper)
4) Result — WOW sequence (framer-motion):
   a) รูปใบเต็มการ์ด เส้นสแกน lime ไล่บน→ล่าง 900ms
   b) กรอบ leaf_boxes pop ทีละอัน stagger 120ms พร้อมป้ายอาการ
   c) วงแหวนคะแนนนับ 0→health_score 1.2s สีตาม grade (#22C55E/#A3E635/#FBBF24/#C2410C) + emoji
   d) การ์ดสาเหตุ 3 ใบ slide-up: emoji + label + แถบ % + explain_th + ชิป evidence
   e) ปุ่ม forest "เริ่มแผนชุบชีวิต 7 วัน" + ลิงก์ "ดูตารางรดน้ำ"
   ใบไม้ SVG ร่วง 3 ใบถ้า critical / ใบอ่อนงอก ถ้า thriving · disclaimer ล่างสุด
บันทึก Diagnosis + LogEntry(kind checkup) ลง store
ทดสอบด้วย demo: p1 ต้องได้ 55 🤒 + overwater 50%
```

## D) แผนชุบชีวิต 7 วัน
```
หน้า /plan/[id]: หัว title_th + แถบ progress (planProgress) + ไทม์ไลน์แนวตั้ง 7 วัน
- วันนี้ไฮไลต์ lime · วันที่ผ่านแล้วยังไม่ติ๊กเป็นสี sun · ติ๊กแล้วมี ✓ เด้ง + เพิ่ม care_days วันนี้
- day 3 แสดง extra_th ในกล่องเล็ก "เผื่อไว้"
- วันที่ 8 การ์ด "ตรวจซ้ำได้แล้ว 📸" → ไป Snap โดยผูก plant_id แล้วสร้าง Glow-up อัตโนมัติ
- แจ้งเตือนตามเวลาใน settings: "วันที่ {n}: {task_th}"
demo: ติ๊ก 1–3 → 43%
```

## E) Smart Water Schedule + แจ้งเตือน
```
หน้า /plant/[id]: การ์ดใหญ่ "รดทุก {interval_days} วัน" + เหตุผลแตกเป็นชิป (ฐานชนิดต้น × แสง × กระถาง × ฤดู) + สถานะ status_th
- ปฏิทินแถบ 4 วันถัดไป · ปุ่ม "รดแล้ว 💧" → last_watered = วันนี้, LogEntry on_time = (days_left ∈ {0, -1, 1})
- finger_test_th ใต้ปุ่มเสมอ · ปุ่ม "ดินยังชื้น เลื่อน 2 วัน"
- แก้ชนิดกระถาง/แสง → คำนวณใหม่ทันที (animate ตัวเลข)
- /lib/notify.ts: ขอสิทธิ์ Notification, ตั้ง reminder ทุกวัน reminder_time สำหรับต้นที่ status today/overdue ข้อความ "{nickname} หิวน้ำแล้ว 💧"
- Home: ป้ายสี clay เมื่อ overdue
demo: p1 "อีก 10 วัน" (ทุก 12 วัน) · p2 "เลยกำหนด 4 วัน"
```

## F) Glow-up Card + Plant Wrapped
```
/glow/[id]: สไลเดอร์ before/after (ลากเส้นกลาง) รูปวันแรก vs วันตรวจซ้ำ + headline_th ใหญ่ + sub_th + คะแนนสองฝั่ง
- export html-to-image 1080×1920 (bg forest, accent lime, footer "ทำด้วย LeafDoc · AI วันละแอป") + ปุ่ม share (Web Share API) / ดาวน์โหลด
- demo: "14 วัน จาก 55 → 94 🌿" · "ใบใหม่ 2 ใบ · รอดแล้ว!"
/wrapped: การ์ดแนวตั้ง 4 ใบเลื่อน (รดกี่ครั้ง · ตรงรอบ % · สาเหตุยอดฮิต · ต้นที่ glow-up มากสุด) + export
- demo ต.ค.: 6 ครั้ง · 50% · 3 การตรวจ · รดน้ำมากไป
```

## G) Nice-to-have pack
```
1) Light Meter /light: เปิดกล้อง getUserMedia → วาด frame ลง canvas 64×64 → mean luma (0.299R+0.587G+0.114B) → luxFromLuma → แถบ 4 ระดับ + ต้นที่เหมาะ + ปุ่ม "บันทึกมุมนี้" · บอกชัดว่าเป็นค่าประมาณ
   ไม่มีกล้อง → slider luma ให้ลอง · demo luma 120/160/220 → 640/2560/20480
2) Pet-safe: ป้ายบนการ์ดต้นทุกต้นเมื่อ settings.has_pets · แตะดูรายละเอียด + source_note
3) Room Match /match: 4 คำถามแบบการ์ดปัด → top 3 + fit bar · demo spider 100
4) My Jungle Level: XP badge บน Home + streak 🔥 (careStreak) · demo XP 105 Lv2 streak 5
5) AI Care Chat (มี key): ปุ่ม "ถามหมอใบไม้" ในหน้าต้น ส่ง context ต้น + diagnosis ล่าสุด · ห้ามตอบตัวเลขคะแนนใหม่
```

## H) API routes (optional AI)
```
/api/ai/vision: รับ AiVisionRequest → เรียกโมเดล vision ด้วย prompt K → validate กับ AiVisionResponse (zod) → ตัด symptoms ที่ไม่อยู่ใน enum → ส่งกลับ
/api/ai/chat: รับ {plant, diagnosis, question} → prompt L → AiCareChatResponse
ไม่มี AI_API_KEY → 501 {error:"ai_disabled"} และ UI แสดง "ต้องตั้งค่า AI ก่อน แตะเลือกอาการเองได้เลย"
จำกัดรูป ≤ 1.5MB, timeout 20s, ไม่เก็บรูปบนเซิร์ฟเวอร์
```

## I) QA
```
ตรวจทั้งแอป:
- vitest ผ่านทั้งหมด + expect_locked
- 390px ไม่มี scroll แนวนอน · ฟอนต์ไทยไม่ตัดสระ · dark text บน cream contrast ≥ 4.5
- ไม่มี AI key: ทุกหน้าใช้ได้ · มี key: vision ผิด schema ต้องไม่พัง
- เปลี่ยนเดือนเป็น เม.ย./ธ.ค. → รอบรดน้ำเปลี่ยนตามฤดู
- ลบ localStorage แล้วเปิดใหม่ → onboarding + ปุ่ม demo
รายงานรายการที่แก้
```

## J) หน้าอัด Reel (/reel)
```
หน้าลับ /reel?step=1..6 สำหรับอัดจอ: โหลด demo, ปิด UI ที่ไม่จำเป็น, ตัวหนังสือใหญ่ 1.2x
step1 Home มอนมอนป้ายแดง · step2 Result p1 wow sequence (กดซ้ำได้) · step3 แผน 7 วัน + "ทุก 12 วัน"
step4 Light Meter 640→2560 · step5 Pet badge + Room Match · step6 Glow-up สไลด์ 55→94
ใส่ปุ่ม replay และ query ?speed=0.5 สำหรับสโลว์
```

---

## Runtime prompts (ใช้ในแอป)

### K) Vision — ตรวจใบ
```
You are a houseplant symptom tagger. Look at the photo and return ONLY JSON matching AiVisionResponse.
- species_guess: one of [monstera, pothos, snake, zz, rubber, fiddle, fern, cactus, spider] or "unknown"
- symptoms: only from [yellow_lower, yellow_all, brown_tips, crispy_edges, black_stem, drooping, leaf_drop, leggy, spots_halo, webbing, sticky_bugs, curling, mushy_base, no_growth, sun_patches]; at most 6; only what is clearly visible
- leaf_boxes: normalized 0..1 boxes around the visible symptoms
- note_th: Thai, ≤120 chars, plain words, no diagnosis, no scores
Do not guess causes or give care advice. If the photo is not a plant, return species_guess "unknown" and symptoms [].
```

### L) Care Chat
```
คุณคือ "หมอใบไม้" ผู้ช่วยดูแลต้นไม้ ตอบภาษาไทยเป็นกันเอง ≤ 3 ประโยค ใช้ข้อมูลต้น (ชนิด แสง กระถาง รดล่าสุด) และผลตรวจล่าสุดที่ให้มาเท่านั้น
ห้ามให้คะแนนสุขภาพใหม่ ห้ามเปลี่ยนรอบรดน้ำที่แอปคำนวณ ถ้าไม่แน่ใจให้แนะนำ finger test หรือปรึกษาร้านต้นไม้
เรื่องพิษต่อสัตว์ ให้บอกว่าควรตรวจกับแหล่งทางการและพาไปหาสัตวแพทย์ถ้าสัตว์กินเข้าไป
ตอบเป็น JSON: {"answer_th": "...", "never_change_score": true}
```

### M) แคปชัน Reel
```
เขียนแคปชัน Reels/TikTok ภาษาไทย 3 แบบ (ขำ · อบอุ่น · สาระ) สำหรับคลิปชุบชีวิตต้นไม้ด้วยแอป LeafDoc
ข้อมูล: ต้น {nickname} ({species_th}) คะแนน {before} → {after} ใน {days} วัน ใบใหม่ {new_leaves} ใบ สาเหตุ {cause_th}
แต่ละแบบ ≤ 2 บรรทัด + CTA "คอมเมนต์ 'ต้นไม้' รับแอปฟรี" + แฮชแท็ก 5 อัน (#ต้นไม้ในคอนโด #AIวันละแอป ...)
```
