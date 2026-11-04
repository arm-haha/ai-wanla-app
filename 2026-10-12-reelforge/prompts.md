# ReelForge — Prompt สั่งงาน (จัดเต็ม)

ใช้คู่กับ `prd.md` · `schemas.json` · `examples.json` · `reference/reel.py`
เป้าหมาย: gen แอปวันเดียวจบ happy path เดโม "เจี๊ยบ" แล้วอัด Reel ได้
สแต็ก: Next.js 14 App Router + TypeScript + Tailwind + shadcn/ui + framer-motion + PWA + Vercel
สี: bg `#0F0A1A` · magenta `#E11D48` · violet `#8B5CF6` · cream `#FDF4FF` · gold `#FBBF24`
คอร์ logic ต้อง deterministic mirror `reference/reel.py` — AI เป็นทางเลือกเสริมเท่านั้น

ตัวเลขเดโมที่ล็อก:
- ไอเดีย: `ขายคุกกี้เนยสด ส่ง LINE ทั้งกรุงเทพ ชิ้นละ 45 บาท เซ็ต 6 ชิ้น 240`
- style `soft_sell_before_after` · 30 วิ · ช็อต 5 · durations `3,6,8,8,5`
- ฮุคชนะ `hook_a` มี `vs` + `30 วิ` · CTA 「คุกกี้」 · ปก 3 แบบ

---

## A) Master prompt สร้างทั้งแอป (วางครั้งเดียว)

```
คุณเป็น senior full-stack ที่จะสร้างแอป ReelForge ตาม PRD ที่แนบ

เป้าหมายผลิตภัณฑ์:
Mini suite เปลี่ยนไอเดีย/voice note/เทมเพลตเป็นชุดถ่าย Reel พร้อมจับเวลา
(Blueprint + Film Mode + Caption Pack ไทย + Overlay/Cover + Hook A/B Lab)
สำหรับแม่ค้า/นักเรียน/ครีเอเตอร์มือใหม่ชาวไทย

สแต็กบังคับ:
- Next.js 14 App Router + TypeScript + Tailwind CSS + shadcn/ui + framer-motion
- PWA (manifest, icons, basic SW) deploy Vercel
- local-first: IndexedDB blueprints + localStorage key "reelforge:v1"
- html-to-image สำหรับปก/การ์ดแชร์ · JSZip สำหรับ export pack (nice-to-have)
- optional AI via /api/ai/* อ่าน process.env.AI_API_KEY — ไม่มี key ก็ใช้คอร์ได้ 100%

สี (อย่าเปลี่ยน):
--bg #0F0A1A; --magenta #E11D48; --violet #8B5CF6; --cream #FDF4FF; --gold #FBBF24;

Must-have 5 ฟีเจอร์ (ทำให้จบก่อน):
1) Idea Drop → Reel Blueprint (wow แรก)
2) Shot List + Film Mode Timer
3) Caption Pack (Thai) รวม CTA keyword
4) Overlay & Cover Forge (3 ปก 1080x1920 PNG)
5) Hook A/B Lab (3 ฮุค + คะแนน + swap)

คอร์ deterministic (พอร์ตจาก reference/reel.py ทีละฟังก์ชัน ให้ผลตรง examples.json):
- parseIdea(raw)
- allocateDurations(weights, target)
- buildBlueprint(idea, style, durationTarget, selectedHookId?)
- rankHooks(hooks)
- buildCaptionPack(blueprint)
- buildOverlays(blueprint)
- filmProgress(shots, elapsedS) / filmRewind / swapHook
- suggestTrendAngles(idea)

เดโม fixture "เจี๊ยบ":
กดปุ่ม "ลองข้อมูลตัวอย่าง" แล้วต้องได้ผลลัพธ์ตรง expect_locked ใน examples.json
ทุกครั้ง (ห้ามสุ่ม)

UI ภาษาไทยเป็นหลัก · ดู examples.json → ui_copy_th
อย่าทำ video editor / อย่ารับประกันยอดขาย / อย่าบังคับล็อกอิน

ลำดับงาน:
1. scaffold + theme + PWA เปล่า
2. lib/* + vitest ให้ test_vectors ผ่าน
3. Home + Blueprint
4. Film Mode
5. Captions + Overlays/Covers
6. Hook Lab
7. nice-to-have ถ้าเหลือเวลา
8. QA ตามส่วน K

ส่งมอบ: โค้ดรันได้ locally · README สั้น · ปุ่มเดโมทำงาน · พร้อมอัดหน้าจอ
```

แนบไฟล์: `prd.md` `schemas.json` `examples.json` `reference/reel.py`

---

## B) ข้อมูลตัวอย่าง "เจี๊ยบ"

```
ใช้ examples.json เป็นแหล่งความจริงเดียวสำหรับเดโม

persona: เจี๊ยบ — แม่ค้าออนไลน์ขายขนมบ้าน / คอนเทนต์มือใหม่ (สมมติ)
raw_idea: "ขายคุกกี้เนยสด ส่ง LINE ทั้งกรุงเทพ ชิ้นละ 45 บาท เซ็ต 6 ชิ้น 240"
style: soft_sell_before_after
duration_target_s: 30

ต้องโชว์บน UI หลังกดเดโม:
- product คุกกี้เนยสด · snacks · ฿45 · เซ็ต 6/240 · LINE · กรุงเทพ
- 5 ช็อต เวลา 3 / 6 / 8 / 8 / 5
- ฮุคชนะ: โพสต์ข้อความอย่างเดียว vs คลิป 30 วิ — อันไหนขายได้มากกว่า?
- caption_short มีคำว่า คุกกี้ และ comment_cta_keyword = "คุกกี้"
- ปก 3 ชื่อ: "ข้อความ vs คลิป 30 วิ" / "คุกกี้เนยสด" / "คอมเมนต์ 「คุกกี้」"
- Film Mode รวม 30 วิ · ที่ elapsed=10 อยู่ช็อต 3

อย่าแต่งตัวเลขใหม่ · ถ้าต้องการเคสเพิ่ม ใช้ extra_ideas ใน examples.json
```

---

## C) TypeScript types + zod

```
สร้าง types/reelforge.ts และ lib/validate.ts
- mirror schemas.json $defs หลัก: ParsedIdea, Shot, Blueprint, HookCandidate,
  HookScores, CaptionPack, OverlaysPack, CoverVariant, FilmProgress, StyleId, CategoryKey
- ใช้ zod ให้ parse/blueprint output ผ่าน safeParse ก่อน set state
- export type จาก zod infer
- ห้ามใช้ any ในคอร์ lib
- เขียน fixture loader อ่านจาก /data/demo.json (คัดลอกจาก examples ส่วนที่ต้องใช้ตอนรัน
  หรือ hardcode DEMO ค่าเดียวกับ expect_locked)

เพิ่ม vitest:
- แต่ละฟังก์ชันคอร์มีเทสต์อย่างน้อยตาม test_vectors ใน examples.json (14 เคส)
```

---

## D) `lib/parseIdea.ts` + `lib/blueprint.ts` (หัวใจคลิป)

```
พอร์ต reference/reel.py ฟังก์ชันต่อไปนี้ให้ผล byte-เทียบได้ในระดับฟิลด์สำคัญ
(ตัวเลข / id / durations / cta ต้องตรง — ข้อความ overlay ต้องตรงภาษาไทยตาม fixture):

1) parseIdea(raw: string): ParsedIdea
   - normalize whitespace
   - category rules ตามลำดับ CATEGORY_RULES
   - price / set / channel / area regex เหมือน Python
   - cta_keyword จากหมวด (+ คุกกี้ถ้า product มีคำว่าคุกกี้)

2) allocateDurations(weights: number[], target: number): number[]
   - sum ต้องเท่า target เสมอ · แต่ละช่อง >= 1
   - ใช้알고리즘เดียวกับ Python (floor + กระจายเศษตาม fractional part)

3) buildBlueprint(idea, style, durationTarget, selectedHookId?)
   - STYLES คงที่ 5 สไตล์
   - สร้าง hooks 3 สูตร → rankHooks → เลือก winner
   - สร้าง shots พร้อม start_s/end_s/duration_s/overlay/vo/prompt
   - assert sum durations === durationTarget

เทสต์บังคับ:
parse demo cookie → product/category/prices/channel/area/cta ตรง
blueprint 30s → durations [3,6,8,8,5] · hook_a · cta คุกกี้ · bgm warm_upbeat

ทำไฟล์นี้ให้เทสต์ผ่านก่อนเริ่ม UI
```

---

## E) `lib/hooks.ts` + `lib/captions.ts` + `lib/overlays.ts` + `lib/film.ts`

```
1) rankHooks(hooks):
   - คะแนน curiosity/clarity/emotion ตาม heuristic ใน reel.py / prd §24
   - ใส่ rank, is_winner
   - เดโม: hook_a total สูงสุด

2) buildCaptionPack(blueprint):
   - short / long ไทย
   - hashtags 8–12 จาก pool หมวด + common
   - comment_cta_keyword จาก blueprint.cta_keyword
   - short ต้อง include CTA keyword

3) buildOverlays(blueprint):
   - per_shot overlay lines
   - covers 3 แบบ size [1080,1920] titles ตาม fixture

4) filmProgress(shots, elapsedS) / filmRewind / swapHook
   - ที่ 0s → ช็อต 1 progress 0
   - ที่ 10s → ช็อต 3
   - ที่ 30s → done
   - swapHook เรียก buildBlueprint ด้วย selectedHookId · duration เดิม

vitest ต้องคลุม test_vectors ทั้งหมดที่เกี่ยวกับฟังก์ชันเหล่านี้
```

---

## F) Idea Drop + Blueprint UI + Film Mode

```
หน้า Home (app/page.tsx):
- textarea + placeholder จาก ui_copy_th.idea_placeholder
- ชิปสไตล์ / ชิปเวลา
- ปุ่มสร้าง Blueprint + ปุ่มเดโม
- เมื่อเดโม: ใส่ raw idea + style + 30 แล้วเรียก buildBlueprint ทันที
- แอนิเมชัน: ช็อตการ์ด stagger ด้วย framer-motion

หน้า Blueprint (component หรือ /blueprint):
- แสดง hook ใหญ่ · รายช็อต · bgm · cta
- ปุ่มเข้า Film Mode

Film Mode (fullscreen client component):
- ไม่ใช่กล้องอัดในแอป — เป็นตัวช่วยจับเวลา + พรอมป์
- countdown 3 วิ (ข้ามได้)
- แสดง prompt_th + overlay_th ของช็อตปัจจุบัน
- requestAnimationFrame หรือ setInterval 100ms อัปเดต filmProgress
- auto-advance เมื่อช็อตจบ (settings.auto_advance_film)
- ปุ่ม rewind → filmRewind(shots, shotIndex)
- ปุ่มข้ามช็อต / ออก
- haptic (ถ้ามี) เมื่อจบช็อตและเมื่อครบ 30 วิ
- UI บอกชัด "เปิดกล้องเครื่องแยก แล้วถ่ายตามพรอมป์นี้"

บันทึก blueprint ลง IndexedDB หลังสร้างสำเร็จ
อัปเดตสตรีคใน localStorage ตามวัน Asia/Bangkok
```

---

## G) Caption Pack + Overlay & Cover Forge

```
แท็บ/หน้า Captions:
- แสดง caption_short_th, caption_long_th, hashtags chips, comment_cta_line_th
- ปุ่มคัดลอกแต่ละช่อง → toast "คัดลอกแล้ว"
- เน้นคำ CTA ด้วยสีทองหรือแมเจนตา

แท็บ Overlays & Covers:
- ลิสต์ overlay รายช็อต พรีวิวเงาบนพื้นมืด
- 3 การ์ดปก (contrast/product/cta) อัตราส่วน 9:16
- ปุ่ม "บันทึกปก PNG" ใช้ html-to-image จาก DOM node ขนาด 1080×1920
  (scale อุปกรณ์ให้คม)
- safe zone hint จาก ui_copy_th.safe_zone_hint

ตรวจกับ overlays_example ใน examples.json ชื่อ title ต้องตรงเดโม
```

---

## H) Hook A/B Lab

```
แสดง hooks_ranked 3 การ์ด:
- ข้อความฮุค
- แถบคะแนน 3 แกน (curiosity/clarity/emotion) + total
- อันดับ 1 มีขอบทอง + ป้าย ui_copy_th.winner_badge

ปุ่ม "ใช้ฮุคนี้":
- เรียก swapHook(blueprint, hookId)
- อัปเดต state blueprint
- toast toast_hook_swapped
- ช็อต 1 overlay/vo เปลี่ยนตามฮุคใหม่ · เวลารวมยัง 30

อย่าให้ผู้ใช้แก้คะแนนเอง — คะแนนมาจาก heuristic เท่านั้น
(ถ้ามี AI เสนอฮุคใหม่ ต้องส่งเข้า rankHooks ก่อน)
```

---

## I) Share Blueprint Card + Export (nice / ทำหลัง must)

```
Share Card 1080×1920:
- title/subtitle/lines จาก share_card_example
- ธีม cinema_neon · html-to-image

Export Pack ZIP (nice):
- blueprint.json (serialize blueprint)
- captions.txt (short + long + hashtags + CTA)
- overlays/ cover_a.png …
- README_th.txt วิธีถ่ายตาม Film Mode
ใช้ JSZip + file-saver
```

---

## J) Nice-to-have pack

```
ทำตามลำดับถ้าเหลือเวลาหลัง must-have + QA เบื้องต้น:

1) Style Templates library — หน้าเลือกสไตล์มีคำอธิบาย + emoji จาก style_library
2) Voice → Idea — ช่องวาง transcript (voice_transcript_example) แล้ว parseIdea
3) Trend Angle Suggest — แสดง suggestTrendAngles · แตะแล้วสลับ style แล้วสร้างใหม่
4) History list — อ่านจาก IndexedDB · แตะเปิด Blueprint เก่า
5) Streak badge บน Home
6) Settings: ai_assist, haptics, auto_advance_film, countdown_beep, ลบข้อมูลทั้งหมด
7) Optional AI routes ตามส่วน M — ปิดได้ด้วย ai_assist=off
```

---

## K) QA ก่อนถ่าย

```
เช็คลิสต์ก่อนอัด Reel ช่อง:

[ ] กดเดโมแล้วได้ 5 ช็อต 3+6+8+8+5 ภายใน ≤ 10 วิ บนมือถือจริงหรือโหมดมือถือ
[ ] ฮุคบน Blueprint มีคำว่า "vs" และ "30 วิ"
[ ] Film Mode วิ่งครบ 30 วิ · ที่ ~10s ขึ้นช็อต 3 · rewind กลับช็อต 3 ได้
[ ] แคปชันสั้นมี 「คุกกี้」 · คัดลอกได้
[ ] ปก 3 แบบ export PNG เปิดดูบนเครื่องได้ อัตราส่วน 9:16
[ ] Hook Lab สลับเป็น B แล้วช็อต 1 เปลี่ยน · สลับกลับ A ได้
[ ] ปิดเครือข่ายแล้วยังสร้าง Blueprint จากเดโมได้ (คอร์ในเครื่อง)
[ ] ไม่มีปุ่มล็อกอินบังคับ · มี disclaimer
[ ] สีตรงธีมมืดนีออน · ตัวอักษรครีมอ่านออกบนพื้นมืด
[ ] vitest หรือ `python3 reference/tests.py` ผ่าน
[ ] อัดหน้าจอตาม reel_script_th ครบว้าว 2 จังหวะใน README
```

---

## L) แก้ปัญหาเร็ว (ใช้เมื่อพัง)

```
อาการ: durations ไม่รวม 30
→ ตรวจ allocateDurations กับเทสต์ allocate_30_soft_sell · อย่าปัดทศนิยมคนละแบบกับ Python

อาการ: hook_b ชนะแทน hook_a
→ ตรวจโบนัส vs / 30 วิ / อันไหน · ข้อความ hook_a ต้องตรง fixture

อาการ: Film Mode กระตุก / ข้ามช็อต
→ ใช้ elapsed จาก performance.now() เริ่มตอน countdown จบ · อย่านับ frame เป็นวินาที

อาการ: ปก PNG เบลอ
→ ใส่ pixelRatio 2–3 ใน html-to-image · ขนาดโหนดจริง 1080×1920

อาการ: มี key AI แล้วผลเดโมเปลี่ยน
→ AI ห้ามทับคอร์เดโมอัตโนมัติ · ใช้เฉพาะเมื่อผู้ใช้กด "ให้ AI ช่วยเสนอ"

อาการ: hydration mismatch
→ Film Mode / เวลาสตรีค เป็น client-only · อย่า render Date แบบสุ่มใน SSR
```

---

## M) Runtime prompts (ที่แอปส่งให้ LLM)

ใช้เฉพาะตอน `ai_assist !== "off"` และมี `AI_API_KEY`
คอร์เกรดคะแนน/โครงช็อตยังอยู่ในเครื่องเสมอ

### M1 — เสนอฮุคเพิ่ม (ไม่แทนที่ heuristic)

```
ระบบ: คุณช่วยเขียนฮุค Reel ภาษาไทยสั้นๆ สำหรับแม่ค้า/ครีเอเตอร์มือใหม่
ผู้ใช้จะส่งสินค้า สไตล์ และฮุคที่มีแล้ว — เสนอทางเลือกใหม่ 1–3 อัน
ห้ามคัดลอกคำเดิมทุกตัว · ห้ามสัญญาว่าขายได้แน่นอน · ความยาว 18–70 ตัวอักษร
ตอบ JSON ตาม AiHooksResponse เท่านั้น

ผู้ใช้:
idea: {{idea_normalized}}
product: {{product}}
category: {{category}}
style: {{style}}
existing_hooks: {{existing_hooks_json}}
```

### M2 — แคปชันทางเลือก

```
ระบบ: เขียนแคปชัน Reel ภาษาไทย โทนเป็นมิตร ไม่แข็งขาย
ต้องมีคำคอมเมนต์ CTA ตรง {{cta_keyword}} ในแคปชันสั้น
ตอบ JSON ตาม AiCaptionResponse เท่านั้น ห้ามมี markdown

ผู้ใช้:
product: {{product}}
hook: {{hook_th}}
cta_keyword: {{cta_keyword}}
tone: {{tone}}
channel: {{channel}}
```

### M3 — มุมคลิปเสริม

```
ระบบ: เสนอมุมรีลที่เข้ากับคนไทย 3–5 อัน ผูก style จากชุด
soft_sell_before_after | teach_3_steps | storytime | unboxing | soft_sell
ตอบ JSON ตาม AiAngleResponse

ผู้ใช้:
idea: {{idea_normalized}}
category: {{category}}
```

หลังได้ response: ฮุคใหม่ต้องผ่าน rankHooks ก่อนแสดง · แคปชันใหม่ต้องผู้ใช้กดยืนยันก่อนทับ

---

## N) Reel overlay / แคปชัน (สำหรับคลิปช่อง AI วันละแอป)

```
ฮุคเปิด (บนจอ):
ไอเดียในหัวแต่ไม่รู้จะเปิดคลิปยังไง?

Overlay ต่อเนื่อง (ดู reel_script_th):
- โยนไอเดียเข้าไป 10 วิ
- ได้ชุดถ่าย · ฮุค · CTA
- Film Mode · ช็อต 1/5
- แคปชันไทย · คอมเมนต์ คุกกี้
- ฮุค A/B + ปก 3 แบบ
- คอมเมนต์ 「รีล」 รับลิงก์

แคปชันโพสต์สั้น:
ไอเดียในหัวแต่ไม่รู้จะเปิดคลิปยังไง? โยนเข้าแอปนี้ 10 วิ… ได้ชุดถ่ายพร้อมจับเวลาเลย 🎬

แคปชันยาว:
มีไอเดียขายของ / เล่าเรื่อง แต่ค้างที่หน้าจอว่างเปล่า? วันนี้แจก ReelForge จากช่อง AI วันละแอป
วางไอเดียหรือ voice note แอปจัด Blueprint ให้: ฮุค 0–3 วิ · ช็อตรายข้อพร้อมเวลา · แคปชันไทย · ข้อความบนจอ · ปกคลิป · ทดลองฮุค 3 สูตร แล้วเข้า Film Mode จับเวลาถ่ายตาม
(ข้อมูลตัวอย่างสมมติ)
คอมเมนต์คำว่า "รีล" รับลิงก์ฟรี

ห้ามในคลิป:
- พูดรับประกันยอดวิว/ยอดขาย
- โชว์แชทลูกค้าจริงโดยไม่เบลอ
- อ้างว่าแอปตัดต่อคลิปให้อัตโนมัติ
```

---

## ภาคผนวก — คำสั่งเทียบผลกับ Python

```bash
cd /workspace/ai-wanla-app/2026-10-12-reelforge/reference
python3 build.py      # เขียน examples.json ใหม่จากคอร์
python3 schema.py     # เขียน+ตรวจ schemas.json
python3 tests.py      # ต้องพิมพ์ fails 0
```

ใน TypeScript ให้สร้างสคริปต์ `pnpm test:core` ที่ assert ค่าเดียวกับ expect_locked
ถ้าผล TS ≠ Python แปลว่าพอร์ตผิด — แก้ lib ก่อนต่อ UI

## ภาคผนวก — โครงโฟลเดอร์แนะนำ

```
app/
  layout.tsx
  page.tsx                 # Home
  blueprint/page.tsx
  film/page.tsx
  api/ai/hooks/route.ts
  api/ai/captions/route.ts
  api/ai/angles/route.ts
components/
  IdeaDrop.tsx
  StyleChips.tsx
  BlueprintView.tsx
  ShotCard.tsx
  FilmMode.tsx
  CaptionPack.tsx
  CoverForge.tsx
  HookLab.tsx
  ShareCard.tsx
  DemoButton.tsx
lib/
  parseIdea.ts
  blueprint.ts
  hooks.ts
  captions.ts
  overlays.ts
  film.ts
  styles.ts
  storage.ts
  demo.ts
types/reelforge.ts
public/manifest.webmanifest
```

## ภาคผนวก — Acceptance ย่อสำหรับโมเดล

ก่อนประกาศเสร็จ: must-have 5 · เดโมตัวเลขล็อก · film 30s · tests เขียว · ไม่มี key ก็ใช้ได้ · UI ไทย · disclaimer · พร้อมอัดตาม README wow moments


---

## ภาคผนวก — Prompt ย่อยสำหรับคอมโพเนนต์ (ใช้ทีละชิ้นถ้าโมเดลล้น context)

### F1) DemoButton + demo.ts

```
สร้าง components/DemoButton.tsx และ lib/demo.ts
- DEMO_RAW, DEMO_STYLE, DEMO_DURATION คงที่ตาม expect_locked
- คลิกแล้ว setIdea(DEMO_RAW) setStyle(DEMO_STYLE) setDuration(30) แล้วเรียก onGenerate()
- ระหว่างสร้างโชว์ skeleton การ์ดช็อต 5 อัน + ข้อความ "กำลังตี Blueprint…"
- analytics: demo_loaded แล้ว blueprint_built
- ต้องเสร็จภายในเป้า 10 วิ (จริงๆ ควร < 100ms เพราะไม่มีเครือข่าย)
```

### F2) ShotCard

```
components/ShotCard.tsx
props: shot: Shot, index animation delay
แสดง: วงเลข n สีแมเจนตา · duration_s · title_th · overlay_th (บรรทัดเดียว)
ขยายได้: vo_th · prompt_th · camera_th
motion: initial opacity0 y12 → inView stagger
```

### F3) FilmMode detailed

```
components/FilmMode.tsx ('use client')
state: phase = 'countdown' | 'running' | 'paused' | 'done'
countdown from 3 using setInterval 1s
เมื่อ running: let start = performance.now() - pausedAccum
ทุก 100ms: elapsed = (now - start)/1000 → filmProgress(shots, elapsed)
UI layers:
- top bar: ช็อต {n}/{N} · เหลือช็อต Xs · รวม Ys
- center: big overlay_th (text-4xl font-bold cream) + prompt_th รอง
- bottom: dual progress bars (shot violet, total magenta)
buttons: rewind (filmRewind), pause/resume, skip (กระโดด end ของช็อตปัจจุบัน), exit
เมื่อ done: แสดง ui_copy_th.film_done + ปุ่มกลับ Blueprint + ปุ่มแชร์การ์ด
accessibility: aria-live สำหรับเปลี่ยนช็อต
อย่าขอ permission กล้องใน v1
```

### F4) CoverForge export

```
components/CoverForge.tsx
มี 3 DOM nodes อ้างอิง covers จาก buildOverlays
แต่ละใบ: พื้น bg · accent bar · title_th ใหญ่ · subtitle_th · badge_th มุม
ปุ่ม export เรียก toPng(node, { width:1080, height:1920, pixelRatio:2 })
ดาวน์โหลดชื่อ reelforge-cover-{id}.png
อย่าใส่โลโก้ธนาคาร/IG จริง · ใส่คำว่า ReelForge มุมเล็กพอ
```

### F5) HookLab bars

```
components/HookLab.tsx
สำหรับแต่ละฮุค วาด 3 progress bar ความกว้างตามคะแนน 0–100
สี: curiosity violet · clarity cream · emotion magenta
total แสดงตัวเลขทอง
เรียงตาม rank จาก blueprint.hooks_ranked (อย่าเรียงใหม่เอง)
```

### G1) storage.ts

```
lib/storage.ts
- localStorage "reelforge:v1" เก็บ Settings + streak + last_blueprint_id
- IndexedDB db "reelforge" store "blueprints" keyPath blueprint_id
- functions: saveBlueprint, listBlueprints, getBlueprint, clearAll
- streak: ถ้า last_date เป็นเมื่อวาน +1 · วันนี้ซ้ำไม่เพิ่ม · ขาดวันรีเซ็ต 1
ใช้วันที่ Asia/Bangkok (กทม. UTC+7) คำนวณจาก toLocaleDateString หรือ temporal polyfill ง่ายๆ
```

---

## ภาคผนวก — ตัวอย่าง vitest (คัดลอกแล้วเติม)

```ts
import { describe, it, expect } from "vitest";
import { parseIdea } from "@/lib/parseIdea";
import { buildBlueprint } from "@/lib/blueprint";
import { buildCaptionPack } from "@/lib/captions";
import { buildOverlays } from "@/lib/overlays";
import { filmProgress, allocateDurations } from "@/lib/film";

const RAW = "ขายคุกกี้เนยสด ส่ง LINE ทั้งกรุงเทพ ชิ้นละ 45 บาท เซ็ต 6 ชิ้น 240";

describe("ReelForge core", () => {
  it("parses demo cookie idea", () => {
    const idea = parseIdea(RAW);
    expect(idea.product).toBe("คุกกี้เนยสด");
    expect(idea.category).toBe("snacks");
    expect(idea.price_unit).toBe(45);
    expect(idea.price_set).toBe(240);
    expect(idea.set_qty).toBe(6);
    expect(idea.channel).toBe("LINE");
    expect(idea.area).toBe("กรุงเทพ");
    expect(idea.cta_keyword).toBe("คุกกี้");
  });

  it("builds 30s soft_sell_before_after blueprint", () => {
    const bp = buildBlueprint(parseIdea(RAW), "soft_sell_before_after", 30);
    expect(bp.shot_count).toBe(5);
    expect(bp.shots.map(s => s.duration_s)).toEqual([3,6,8,8,5]);
    expect(bp.hook.id).toBe("hook_a");
    expect(bp.hook.text_th).toContain("vs");
    expect(bp.cta_keyword).toBe("คุกกี้");
    expect(bp.bgm_mood).toBe("warm_upbeat");
  });

  it("caption contains CTA", () => {
    const caps = buildCaptionPack(buildBlueprint(parseIdea(RAW), "soft_sell_before_after", 30));
    expect(caps.comment_cta_keyword).toBe("คุกกี้");
    expect(caps.caption_short_th).toContain("คุกกี้");
    expect(caps.hashtags.length).toBeGreaterThanOrEqual(8);
  });

  it("three covers", () => {
    const o = buildOverlays(buildBlueprint(parseIdea(RAW), "soft_sell_before_after", 30));
    expect(o.covers).toHaveLength(3);
    expect(o.covers.map(c => c.id)).toEqual(["cover_a","cover_b","cover_c"]);
  });

  it("film progress at 10s is shot 3", () => {
    const bp = buildBlueprint(parseIdea(RAW), "soft_sell_before_after", 30);
    const fp = filmProgress(bp.shots, 10);
    expect(fp.shot.n).toBe(3);
    expect(fp.done).toBe(false);
  });

  it("allocate durations sum", () => {
    expect(allocateDurations([3,6,8,8,5], 30)).toEqual([3,6,8,8,5]);
    expect(allocateDurations([3,6,8,8,5], 15).reduce((a,b)=>a+b,0)).toBe(15);
  });
});
```

---

## ภาคผนวก — copy ไมโครอินเทอร์แอคชัน

| จังหวะ | copy ไทย |
|---|---|
| กำลังสร้าง | กำลังตี Blueprint… |
| สร้างเสร็จ | ชุดถ่ายพร้อมแล้ว 🎬 |
| เริ่ม Film | เตรียมกล้องเครื่อง · เริ่มใน 3 |
| จบช็อต | ช็อตนี้ครบ · พักหายใจ แล้วต่อ |
| จบทั้งหมด | ครบทุกช็อต · เก่งมาก! |
| สลับฮุค | สลับฮุคแล้ว · ช็อต 1 อัปเดต |
| คัดลอก | คัดลอกแล้ว |
| ว่างไอเดีย | วางไอเดียก่อนนะ จะได้สร้างชุดถ่ายให้ |
| ไม่มีเน็ต | โหมดในเครื่อง · ใช้ได้ตามปกติ |
| ไม่มี AI key | ใช้เทมเพลตในเครื่อง (ไม่ต้องมี key) |

---

## ภาคผนวก — สิ่งที่โมเดลมักทำผิด (ดำห้าม)

1. สุ่ม durations ใหม่ทุกครั้งที่ generate — ผิด ต้อง deterministic จาก style weights
2. เรียก LLM ในเส้นทางเดโมหลัก — ผิด เดโมต้องออฟไลน์ได้
3. ทำให้ Film Mode เป็น recorder ที่ขอ getUserMedia บังคับ — ไม่ใช่สCope v1
4. แปล CTA keyword เป็นอังกฤษ — เดโมต้องเป็น 「คุกกี้」
5. ใช้พื้นขาว / สีเขียวมิ้นต์ของ SlipBook — คนละแอป ใช้ cinema neon ตามสเปก
6. ใส่โลโก้ IG/TikTok ทางการ — ใช้ไอคอนทั่วไปหรือตัวอักษร
7. เปลี่ยนชื่อแอปเป็น Reel Studio / ClipForge — คง ReelForge
