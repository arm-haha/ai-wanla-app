# PawTalk (แมวหมาพูดได้) — Prompt สั่งงาน (จัดเต็ม)

ใช้คู่กับ `prd.md` · `schemas.json` · `examples.json` · `reference/pawtalk.py`
สแต็ก: Next.js 14 App Router + TypeScript + Tailwind + shadcn/ui + framer-motion + PWA + Vercel
สี: cream `#FFF8F0` · cocoa `#3B2A20` · orange `#F97316` · peach `#FDBA74` · mint `#34D399` · sky `#60A5FA` · berry `#EC4899` · alert `#DC2626`
ฟอนต์: Mitr (หัวข้อ/บับเบิล) + IBM Plex Sans Thai (เนื้อหา)
กติกาเหล็ก: คอร์ deterministic ตาม `reference/pawtalk.py` — AI แค่ **เสนอ cue tag ใน enum** และ (ถ้าเปิด) เกลาคำบับเบิลโดยห้ามเปลี่ยนอารมณ์ ห้ามให้ AI ให้คะแนน/ระดับอาการ/ตัวเลขใดๆ

ตัวเลขเดโมที่ล็อก (บ้านแพรว 2026-10-20 07:05):
- ส้มฉุน (แมว) cue `staring_at_bowl, meow_loud, tail_flick` + ข้าวเช้า 07:30 (อีก 25 นาที → +2 hungry) → **หิว 8pt 62% · หงุดหงิด 3pt 23% · อยากให้สนใจ 2pt 15%** · vibe **38 ระวังนะ**
- บับเบิล boss: "ทาสสส อีก 25 นาทีข้าวต้องมา ช้า 1 วิหักเงินเดือน" · drama: "ไม่ได้กินมา 300 ปีแล้ว…จะเป็นลมแล้วนะแพรว" · sweet: "หนูนั่งรอตรงนี้นะ ไม่ไปไหนเลย"
- หลังกินข้าว 08:10 `slow_blink, loaf, purr` → ชิลล์ 61% vibe **96**
- ข้าวปั้น (ชิบะ) `tail_wag_loose, play_bow, bringing_toy` → อยากเล่น 54% vibe 87 → "หนูเอาของเล่นมาให้แล้ว"
- Duet: ส้มฉุน(boss) → ข้าวปั้น(sweet) → ส้มฉุน "ชามว่างคือการดูหมิ่นข้า"
- Care board: t1 ถ่ายพยาธิส้มฉุน **เลย 7 วัน** → t5 อาบน้ำข้าวปั้นเลย 2 → t6 ยาหนอนหัวใจ อีก 1 → t2 เห็บหมัด อีก 2 → t4 ตัดเล็บ 4 → t3 วัคซีน 13 (2026-11-02)
- Health: ส้มฉุน hairball+vomit_once → watch · ข้าวปั้น scratching_more → watch · ตัวอย่างแดง straining_no_urine → **emergency**
- Food: ส้มฉุน 260 kcal / 68 g/วัน / 34 g/มื้อ · ข้าวปั้น 582 kcal / 166 g / 83 g · อายุคน 28 / 24
- Progress XP 205 Lv3 streak 7 · Wrapped ต.ค. ส้มฉุน 13 snaps หิว 6 ครั้ง happy 23% หงุดหงิดสุดวันพุธ

---

## A) Master prompt (วางครั้งเดียว)
```
คุณเป็น senior full-stack ที่จะสร้างแอป PawTalk (แมวหมาพูดได้) ตาม PRD ที่แนบ
เป้าหมาย: mini suite "ถ่ายรูปน้อง → อ่านภาษากาย → บับเบิลความคิดตลกๆ ภาษาไทย" + เครื่องมือดูแลสัตว์เลี้ยงที่ทำให้กลับมาเปิดทุกวัน
UI ภาษาไทย (examples.json → ui_copy_th) mobile-first 390px, PWA, deploy Vercel
สแต็ก: Next.js 14 App Router + TS + Tailwind + shadcn/ui + framer-motion · local-first localStorage key "pawtalk:v1" ตาม schema LocalStore · รูปเก็บ IndexedDB (ไม่อัปโหลดถ้าไม่ได้ใช้ AI)
โครง:
- /lib/engine.ts = พอร์ต reference/pawtalk.py แบบ 1:1 (read_mood, thought_bubble, bubble_index, duet, care_board, next_meal, health_check, food_plan, human_age, progress, wrapped)
- /lib/catalog.ts = CUES, CUE_TH, BUBBLES, SYMPTOMS จาก examples.json (cue_catalog, bubble_templates, symptom_catalog)
- /app/api/cues/route.ts = เรียก vision model (Prompt K) คืน AiCueResponse; ไม่มี API key → โหมดเดโมใช้ examples.json
- หน้า: /, /snap, /result/[id], /duet, /care, /health, /pet/[id], /wrapped, /reel-demo
- ทุกการคำนวณผ่าน engine เท่านั้น · ห้าม Math.random ในคอร์
ทำ Prompt B–J ต่อทีละอัน ทุกขั้นต้องผ่าน unit test ที่ตรงกับ reference/tests.py (25 เคส)
```

## B) Engine port + tests
```
พอร์ต reference/pawtalk.py เป็น /lib/engine.ts ให้ผลตรงกันทุกค่า
- _alloc_pct: largest remainder, tie-break ตาม PRIORITY ["scared","annoyed","hungry","needy","playful","happy","chill"]
- read_mood: cue ต้องอยู่ในตารางของ species (ไม่งั้น throw), เรียงตามลำดับในตาราง+ตัดซ้ำ, meal bonus +2 hungry ถ้าอีก ≤60 นาทีถึงมื้อ (นับข้ามเที่ยงคืนด้วย mod 1440)
- vibe = round(100 × Σ(points×VIBE_W)/Σpoints) · VIBE_W happy/chill/playful 1, needy/hungry 0.5, annoyed/scared 0 · ≥80 "ฟินมาก" ≥50 "โอเค" อื่นๆ "ระวังนะ"
- bubble_index = ผลรวม charCodeAt ของ `${pet_id}|${date}|${mood}|${persona}` mod 3 (Python ord = JS charCodeAt สำหรับอักษรไทยใน BMP)
- Math.round ของ JS ≠ round ของ Python ที่ .5 → เขียน roundHalfEven() ใช้ให้ตรง
เขียน vitest 25 เคสตาม reference/tests.py (ตัวเลขใน expect_locked ของ examples.json)
```

## C) Pet onboarding + Pet Profile
```
หน้าเพิ่มน้อง (สูงสุด 10 ตัว): ชื่อ, แมว/หมา, สายพันธุ์, เพศ, อายุ (ปี/เดือน), น้ำหนัก, ทำหมันแล้วไหม, ขนาด (หมา), เวลาให้ข้าว (chip 07:30 / 19:00 แก้ได้), บุคลิกเสียง (👑 เจ้านาย / 🎭 ดราม่าควีน / 🥺 ขี้อ้อน)
Pet page: รูปวงกลม + การ์ดอายุคน (human_age) + Food Plan (food_plan, ใส่ kcal/100g จากฉลาก) + mood ล่าสุด + ปุ่ม "บัตรประจำตัว" (PetIdCard 1080×1350)
validate ด้วย schema Pet ก่อนบันทึก
```

## D) Pet Snap → Thought Bubble (⭐ wow)
```
/snap: กล้องเต็มจอ + กรอบอุ้งเท้า, ปุ่มชัตเตอร์ส้ม, เลือกน้องจากแถบด้านบน
หลังถ่าย: ส่งรูป (ย่อ ≤1024px) ไป /api/cues → แสดง "AI เห็นแบบนี้ ถูกไหม?" เป็นชิป cue (confidence ≥0.5 ติ๊กไว้, 0.3–0.5 แสดงแบบจาง) + "+ เพิ่มท่าทางที่เห็น" เปิดลิสต์ cue ภาษาไทยของ species นั้น
กด "แปลใจเลย" → engine.read_mood → engine.thought_bubble
แอนิเมชัน: รูปซูมนิด → บับเบิลเด้งจากหัวน้อง (spring) → ตัวอักษรพิมพ์ทีละคำ 40ms → badge "🍗 หิว 62%" → Mood Meter bar ไหลเข้า
แถบสลับ persona 3 ปุ่ม (เปลี่ยนข้อความทันที ไม่เรียก AI) · ปุ่ม "แชร์มีม" → MemeCard 1080×1920 (html-to-image) watermark "PawTalk · AI วันละแอป"
ถ้า is_pet_photo=false → ui_copy_th.not_pet_photo
ทุกบับเบิลมี disclaimer เล็กๆ "แปลเพื่อความบันเทิง…"
```

## E) Mood Meter + Diary
```
การ์ด Mood Meter: แท่งแนวนอนต่ออารมณ์ (สีตาม mood: hungry orange, annoyed berry, scared sky, needy peach, playful mint, happy #FBBF24, chill #A78BFA) + วง Vibe 0–100
ถ้า top_mood เป็น scared/annoyed → แบนเนอร์ safety_hint "ให้พื้นที่ อย่าเพิ่งอุ้ม/ลูบ"
ปุ่ม "ถ่ายอีกรอบหลังกินข้าว" → เทียบ Before/After (เดโม 38 → 96) เป็น split card
บันทึก LogEntry kind "snap" ทุกครั้ง · หน้า Diary = ปฏิทินอีโมจิรายวัน + streak "แปลใจติดกัน 7 วัน 🔥"
```

## F) Duet — ให้น้องคุยกัน
```
/duet: เลือกน้อง 2 ตัวที่ snap วันนี้แล้ว → engine.duet → แสดงเป็นแชตแบบ LINE (bubble ซ้าย/ขวา + รูปโปรไฟล์) 3 ข้อความ เด้งทีละอัน 700ms
ส่งออกเป็น MemeCard layout "duet_chat" · ถ้ามีน้องตัวเดียว ให้เลือก "เงาในกระจก" = ตัวเดิม persona ต่างกัน
```

## G) Care Board + แจ้งเตือน
```
/care "งานทาสวันนี้": engine.care_board เรียง overdue → due_soon → ok
แต่ละแถว: ไอคอน kind, ชื่อน้อง, label, "เลยกำหนด 7 วัน" (แดง) / "อีก 2 วัน" (ส้ม) / วันที่ (เขียว), ปุ่ม ✓ ทำแล้ว (ตั้ง last_done = วันนี้ + LogEntry care_done +15 XP)
การ์ด "มื้อถัดไป" (next_meal) นับถอยหลัง · Notification API เตือนมื้อ+งานครบกำหนด 09:00; ถ้าไม่อนุญาต → badge ในแอป
เพิ่ม/แก้งาน: kind, label, last_done, interval_days (ค่าเริ่ม: ถ่ายพยาธิ 90, เห็บหมัด 30, วัคซีน 365, ตัดเล็บ 14, อาบน้ำ 14, หนอนหัวใจ 30) — ค่าเริ่มเป็นตัวตั้งต้น ให้ผู้ใช้แก้ตามที่หมอสั่ง
```

## H) Health Check (คัดกรอง ไม่ใช่วินิจฉัย)
```
/health: เลือกน้อง → ชิปอาการจาก symptom_catalog (กรองตาม species) → engine.health_check
ผล: การ์ดใหญ่ตาม level — emergency แดงเต็มจอ + ปุ่ม "หาโรงพยาบาลสัตว์ใกล้ฉัน" (เปิด Google Maps query "โรงพยาบาลสัตว์ 24 ชั่วโมง") · soon ส้ม · watch เขียวพร้อม "สิ่งที่ควรสังเกต"
ห้าม AI แต่งคำแนะนำการรักษา/ยา · disclaimer ทุกครั้ง · บันทึก LogEntry health_check
```

## I) Wrapped + Pet ID Card + Level
```
/wrapped: เลือกเดือน → engine.wrapped → สไลด์ 5 หน้าแบบ story (อารมณ์ประจำเดือน, จำนวน snap, % happy, วันที่หงุดหงิดที่สุด (แปล Wed → วันพุธ), งานดูแลที่ทำ) + ปุ่มแชร์
Level/XP ตาม engine.progress แสดงที่ header (Lv3 · 205 XP)
PetIdCard 1080×1350 ตาม examples.json.pet_id_card
```

## J) QA + หน้าอัด Reel
```
- /reel-demo?fixture=praew โหลด local_store จาก examples.json แล้วเล่นสคริปต์ reel_script อัตโนมัติ (ปุ่ม Next ซ่อนมุมจอ)
- QA: vitest 25 เคสผ่าน, Lighthouse PWA ≥90, ทุกหน้า 390×844 ไม่มี scroll แนวนอน, ฟอนต์ไทยไม่ขาด, ปิดเน็ตแล้วยังใช้ Care/Health/Food ได้
- ตรวจ copy: ไม่มีคำว่า "วินิจฉัย/รักษา" ในผล Health ยกเว้นใน disclaimer
```

---

## Runtime prompts

### K) Vision → cue tags (เรียกจาก /api/cues)
```
SYSTEM: คุณคือผู้ช่วยอ่านภาษากายสัตว์เลี้ยงจากภาพ ตอบเป็น JSON ตาม schema AiCueResponse เท่านั้น
- species_seen: cat | dog | other | none
- cues: เลือกได้เฉพาะจาก allowed_cues ที่ให้มา (ห้ามคิดใหม่) สูงสุด 8 พร้อม confidence 0–1 เฉพาะสิ่งที่มองเห็นจริงในภาพ
- ห้ามสรุปอารมณ์ ห้ามให้คะแนน ห้ามพูดเรื่องโรค
- note_th: บรรยายสิ่งที่เห็นสั้นๆ ≤120 ตัวอักษร
USER: species={species}, allowed_cues={allowed_cues}, image=<attached>
```

### L) เกลาบับเบิล (ตัวเลือก ปิดได้)
```
SYSTEM: เกลาประโยคความคิดของสัตว์เลี้ยงให้ตลกขึ้นแบบภาษาไทยวัยรุ่น ยาว ≤{max_chars} ตัวอักษร
ต้องคงอารมณ์ {bubble.mood} และบุคลิก {bubble.persona_th} ห้ามหยาบคาย ห้ามเนื้อหาทางเพศ/ความรุนแรง ห้ามพูดเรื่องสุขภาพ
ตอบ JSON {"text_th": "...", "kept_mood": "{bubble.mood}"} ถ้า kept_mood ไม่ตรงหรือยาวเกิน → แอปใช้ข้อความ template เดิม
USER: ต้นฉบับ: "{bubble.text_th}" ชื่อน้อง: {pet_name}
```

### M) แคปชันโพสต์
```
เขียนแคปชัน IG/TikTok ภาษาไทย 2 บรรทัด + แฮชแท็ก 5 อัน จากมีมนี้: น้อง {pet_name} อารมณ์ {mood_th} คำพูด "{text_th}" ปิดท้ายด้วย "แปลโดย PawTalk 🐾"
```
