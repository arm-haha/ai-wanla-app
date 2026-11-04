# CleanQuest (ห้องรกหาย) — Prompt สั่งงาน (จัดเต็ม)

ใช้คู่กับ `prd.md` · `schemas.json` · `examples.json` · `reference/cleanquest.py`
สแต็ก: Next.js 14 App Router + TypeScript + Tailwind + shadcn/ui + framer-motion + PWA + Vercel
สี: mist `#F5F7FF` · ink `#1E1B4B` · lilac `#A78BFA` · sparkle `#22D3EE` · lemon `#FDE047` · mess `#F43F5E` · clean `#10B981`
ฟอนต์: Kanit (ตัวเลขสกอร์/หัวข้อ) + IBM Plex Sans Thai (เนื้อหา)
กติกาเหล็ก: คอร์ deterministic ตาม `reference/cleanquest.py` — AI แค่ **เสนอ hotspot id + severity + box** (ผู้ใช้ยืนยัน) และ (ถ้าเปิด) เขียน pep talk สั้นๆ · ห้ามให้ AI ให้คะแนน นาที ราคา หรือตัดสิน keep/sell

ตัวเลขเดโมที่ล็อก (ห้องหอฟ้า 2026-10-21 20:30):
- สแกนก่อน 8 จุด: เสื้อผ้ากอง×2, ขยะพื้น×2, แก้วค้าง, ซองขนม, โต๊ะรก, กล่องพัสดุ, เตียง, สายชาร์จ → **mess 88 → clean 12 "ห้องวิกฤต 🚨"** · ประมาณ 38 นาที · bed 30 = desk 30 > floor 28 → โซนแย่สุด bed (เสมอใช้ลำดับ bed, desk, floor)
- โหมด 🔥: ซองขนม(2น.) → ขยะ(6) → เตียง(2) → แก้ว(4) | เสื้อผ้า(12) | กล่อง(4) → โต๊ะ(5) → สาย(3) · สปรินต์ **14/12/12** · สกอร์คาดการณ์ 20→40→46→56→80→88→96→100
- โหมด 😴 5 นาที: ซองขนม + เตียง → 26 · โหมด 🙂: 4 เควส 14 นาที → 56
- Timer ทำ q1–q3 ที่ 600 วิ → live **46** เหลือ 1,680 วิ ถัดไป q4 (สปรินต์ 1)
- สแกนหลัง: เหลือฝุ่นพื้น×1 → **94 "ห้องโชว์ ✨"** · Glow-up **12 → 94 (+82) "ห้องเกิดใหม่ 🦋"** "ห้องฟ้า 12 → 94 ใน 38 นาที"
- Declutter: หูฟังเก่า → **ขาย ฿770** · เสื้อคอนเสิร์ต → เก็บ (ความทรงจำ) · ไดร์พัง → ทิ้ง · ยีนส์ → บริจาค · กระติกน้ำ → เก็บ
- แบ่งงาน: ฟ้า q5,q6,q1,q3 = 20 นาที · มุก q2,q7,q4,q8 = 18 นาที
- Progress ก่อนเก็บ 150 XP Lv2 → หลังเก็บ **283 XP Lv3** streak 7 · Weekly Reset อาทิตย์ 2026-10-25 (อีก 4 วัน, สัปดาห์นี้ทำแล้ว) · Wrapped ต.ค. 4 รอบ 85 นาที ขยับเฉลี่ย +44 ดีสุด +82 จุดรกประจำห้อง เสื้อผ้ากอง

---

## A) Master prompt (วางครั้งเดียว)
```
คุณเป็น senior full-stack ที่จะสร้างแอป CleanQuest (ห้องรกหาย) ตาม PRD ที่แนบ
เป้าหมาย: mini suite "ถ่ายรูปห้อง → คะแนนความรก + จุดรก → เควสเกมแบ่งสปรินต์ → Before/After" + เครื่องมือ declutter/รูมเมท/streak ที่ทำให้กลับมาเปิดทุกสัปดาห์
UI ภาษาไทย (examples.json → ui_copy_th) mobile-first 390px, PWA, deploy Vercel
สแต็ก: Next.js 14 App Router + TS + Tailwind + shadcn/ui + framer-motion · local-first localStorage "cleanquest:v1" ตาม schema LocalStore · รูปเก็บ IndexedDB
โครง:
- /lib/engine.ts = พอร์ต reference/cleanquest.py แบบ 1:1 (mess_score, quest_plan, timer_tick, glow_up, declutter, chore_split, progress, weekly_reset, wrapped)
- /lib/catalog.ts = HOTSPOTS, SEV_TH, MODES, LABELS จาก examples.json (hotspot_catalog ฯลฯ)
- /app/api/scan/route.ts = vision model (Prompt K) คืน AiScanResponse · ไม่มี API key → โหมดเดโมใช้ ai_scan_response_example + scan_input
- หน้า: /, /scan, /score/[id], /plan/[id], /timer/[id], /glow/[id], /declutter, /split/[id], /wrapped, /reel-demo
- ทุกตัวเลขผ่าน engine เท่านั้น · ห้าม Math.random ในคอร์
ทำ Prompt B–J ต่อทีละอัน ทุกขั้นต้องผ่าน unit test ที่ตรงกับ reference/tests.py (25 เคส)
```

## B) Engine port + tests
```
พอร์ต reference/cleanquest.py เป็น /lib/engine.ts ให้ผลตรงกันทุกค่า
- _norm: hotspot id ต้องอยู่ใน catalog, severity 1–3 (ไม่งั้น throw), ตัดซ้ำเก็บตัวแรก, เรียงตามลำดับ catalog
- clean_score = max(0, 100 − Σ weight×severity) · worst_zone เสมอกันใช้ลำดับ bed → desk → floor
- quest order: key (−points/minutes, −points, catalogIndex) · แพ็กสปรินต์ ≤15 นาที
- score_after ของเควส = max(0, 100 − (mess_points − ผลรวม points ที่ทำแล้ว))
- declutter resale = round(paid × factor / 10) × 10 · wrapped avg_delta ใช้ round แบบ Python (half-even) → เขียน roundHalfEven() (เดโม 44.5 → 44)
เขียน vitest 25 เคสตาม reference/tests.py (ตัวเลขใน expect_locked)
```

## C) Room Snap + ยืนยันจุดรก
```
/scan: กล้องเต็มจอ + เส้นกริด 3×3 + คำแนะนำ "ถ่ายกว้างให้เห็นพื้นกับโต๊ะ" · เลือกรูปจากอัลบั้มได้
ส่งรูป (ย่อ ≤1280px) → /api/scan → แสดงรูปพร้อม pin วงกลมตาม box (สี mess) เด้งทีละอัน 120ms
ใต้รูป: ชิปจุดรก confidence ≥0.5 ติ๊กไว้, 0.3–0.5 จาง · แตะชิปเพื่อเลือกระดับ นิดหน่อย/พอสมควร/เยอะมาก · "+ เพิ่มจุดที่ AI ไม่เห็น" เปิดลิสต์ 13 ชนิด
is_room_photo=false → ui_copy_th.not_room · บันทึก ScanInput + LogEntry "scan"
```

## D) Mess Score (⭐ wow)
```
/score/[id]: ตัวเลขใหญ่ Kanit นับขึ้นจาก 0 → 12 ใน 900ms, วงแหวนสีไล่ mess→lemon→clean ตามคะแนน, ถ้า <40 ตัวเลขสั่นเบาๆ + ป้าย "ห้องวิกฤต 🚨"
แถบ 3 โซน (เตียง/โต๊ะ/พื้น) แสดง zone_points · ลิสต์ hotspot เรียงตาม points พร้อมอีโมจิ
ปุ่ม "แปลงเป็นเควส" → เลือกโหมด 😴 🙂 🔥 (ui_copy_th.mode_pick) → /plan
```

## E) Quest Plan + Timer Mode
```
/plan: การ์ดสปรินต์ (สปรินต์ 1 · 14 นาที) มีเควสเป็นการ์ดย่อย: อีโมจิ, ชื่อ, นาที, +XP, ป้าย "⚡ งานไว" ถ้า quick_win, กราฟเส้นเล็กสกอร์คาดการณ์
/timer: นาฬิกาวงกลมนับถอยหลังรวม, เควสปัจจุบันตัวใหญ่, ปุ่ม "เสร็จ!" → confetti + "+{xp} XP" + สกอร์ live วิ่งขึ้น (timer_tick) · จบสปรินต์ → ui_copy_th.sprint_break พัก 60 วิ
เปิดหน้าจอค้าง (Wake Lock API) · เสียงติ๊ง/สั่นเปิดปิดได้ · จบทุกเควส → ปุ่ม "ถ่ายหลังเก็บ"
```

## F) Before/After Glow-up Card
```
สแกนซ้ำ → engine.mess_score → engine.glow_up
หน้า /glow: slider ลากเทียบรูปก่อน/หลัง + ตัวเลข 12 → 94 นับขึ้น + ฉายา "ห้องเกิดใหม่ 🦋"
ส่งออก GlowUpCard 1080×1920 (html-to-image) 2 เลย์เอาต์ split_before_after/slider · watermark "CleanQuest · AI วันละแอป" · ปุ่มเบลอบางส่วนก่อนแชร์ (ป้องกันข้อมูลส่วนตัว)
บันทึก Session + LogEntry "session" + "quest" (xp ต่อเควส)
```

## G) Declutter Decider
```
/declutter: ฟอร์มสั้นต่อชิ้น: ชื่อ, รูป(ไม่บังคับ), สภาพ (ดี/มีร่องรอย/พัง), ไม่ได้ใช้กี่เดือน (slider), ราคาที่ซื้อ, มีความทรงจำไหม, มีซ้ำไหม
ผลเป็นการ์ดปัดแบบ swipe: เก็บ 💚 ขาย 💰 บริจาค 🎁 ทิ้ง 🗑️ + เหตุผล · ถ้าขาย แสดง listing_th + ปุ่มคัดลอก
สรุปท้าย: "ขายได้รวม ฿770 · บริจาค 1 · ทิ้ง 1" · LogEntry "declutter" ต่อชิ้น
```

## H) แบ่งงานรูมเมท + LINE
```
/split/[id]: ใส่ชื่อรูมเมท (สูงสุด 6) → engine.chore_split → การ์ดต่อคน (เควส + นาทีรวม)
ปุ่ม "ส่งเข้า LINE รูมเมท" → line.me/R/share?text= ข้อความ: "🧹 เควสคืนนี้ ฟ้า 20 นาที: เสื้อผ้า, กล่อง, ซองขนม, เตียง · มุก 18 นาที: ขยะ, โต๊ะ, แก้ว, สาย — ใครเสร็จก่อนเลือกเมนูข้าว 😆"
```

## I) Streak / Weekly Reset / Wrapped
```
หน้าแรก: สกอร์ล่าสุด + streak "สแกนติดกัน 7 วัน 🔥" + XP bar (Lv = xp//100+1) + การ์ด Weekly Reset (weekly_reset, เปลี่ยนวันได้ใน settings)
แจ้งเตือน (Notification API) เช้าวัน reset 10:00 ถ้ายังไม่ทำสัปดาห์นี้
/wrapped: สไลด์ 5 หน้า: จำนวนรอบ → นาทีรวม → ขยับเฉลี่ย/ดีสุด → จุดรกประจำห้อง (อีโมจิใหญ่) → การ์ดแชร์
```

## J) QA + /reel-demo
```
/reel-demo: โหลด fixture ห้องฟ้าทั้งหมด เล่นทีละฉากด้วยปุ่มลูกศร (สแกน → 12 → 🔥 plan → timer เร่ง 20× → 94 glow → declutter ฿770 → split)
ตรวจ: ตัวเลขตรง expect_locked, 390px ไม่ล้น, contrast ตัวอักษรผ่าน AA, ทุกปุ่มมี label ไทย, ไม่มีคีย์ API ฝั่ง client
```

---

## K) Runtime — Vision scan (system prompt สำหรับ /api/scan)
```
คุณคือผู้ตรวจห้อง ดูรูปห้องแล้วตอบเป็น JSON ตาม schema AiScanResponse เท่านั้น
- เลือก hotspot ได้เฉพาะจาก allowed_hotspots: {{ids}}
- severity: 1 นิดหน่อย, 2 พอสมควร, 3 เยอะมาก
- box = [x, y, w, h] สัดส่วน 0–1 ของรูป
- ถ้าไม่ใช่รูปห้อง is_room_photo=false, hotspots=[]
- ห้ามให้คะแนน ห้ามประเมินเวลา ห้ามตัดสินผู้อยู่อาศัย ไม่อ่าน/ไม่ระบุข้อมูลส่วนตัวที่เห็นในรูป (ชื่อบนกล่องพัสดุ ที่อยู่ เอกสาร)
- note_th ≤120 ตัวอักษร บรรยายสิ่งที่เห็นแบบสุภาพ
```

## L) Runtime — Pep talk (ถ้าเปิด)
```
เขียนข้อความเชียร์ภาษาไทย ≤60 ตัวอักษร สำหรับเควส "{{quest.title_th}}" สกอร์ตอนนี้ {{live_score}} สไตล์ {{style}} (coach/bestie/army)
ห้ามเปลี่ยนหรือแต่งตัวเลขใหม่ ใช้ได้แค่ตัวเลขที่ให้ · ห้ามดูถูกผู้ใช้ · ตอบ JSON {"text_th": "..."}
ถ้า error ใช้ pep_talk_examples ใน examples.json
```

## M) Runtime — แคปชัน Reel
```
เขียนแคปชัน Reel ภาษาไทย 3 แบบ (≤150 ตัวอักษร) จาก GlowUpCard: before {{before}} after {{after}} นาที {{minutes}}
มีคำถามชวนคอมเมนต์ "ห้องแกได้กี่คะแนน?" + CTA "คอมเมนต์ 'ห้อง' รับลิงก์ฟรี" + แฮชแท็ก 4 อัน (#AIวันละแอป #จัดห้อง #ห้องรก #beforeafter)
```
