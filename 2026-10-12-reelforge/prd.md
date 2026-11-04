# ReelForge — PRD (AI วันละแอป · Day 10/10)

**วันที่:** 2026-10-12 (Asia/Bangkok) · **ช่อง:** AI วันละแอป · **สถานะ:** พร้อม gen วันนี้
**เอกสารคู่กัน:** `prompts.md` · `schemas.json` · `examples.json` · `reference/` (สูตร Python ใช้เทียบผลกับ TypeScript)
**หมายเหตุคิว:** วันที่ 9 ต.ค. ส่ง ReelForge ไม่สำเร็จ — แพ็กนี้เป็นรอบชดเชยวันสุดท้ายของคิว 10 แอป

---

## 1) สรุปหนึ่งบรรทัด

โยนไอเดีย / voice note / เทมเพลตเข้าแอป → ได้ชุดถ่าย Reel พร้อมจับเวลา: ฮุค · ช็อตรายข้อ · แคปชันไทย · ข้อความบนจอ · ปกคลิป · ทดลองฮุค A/B แล้วเข้า Film Mode ถ่ายตาม

**ฮุค Reel:** ไอเดียในหัวแต่ไม่รู้จะเปิดคลิปยังไง? โยนเข้าแอปนี้ 10 วิ… ได้ชุดถ่ายพร้อมจับเวลาเลย 🎬

## 2) ปัญหา

- คนไทยอยากลง Reels (แม่ค้าออนไลน์ / นักเรียน / ฟรีแลนซ์) แต่ค้างที่หน้าจอว่าง — ไม่รู้จะเปิดคลิปประโยคไหน
- มีไอเดียในหัวหรือ voice note ยาวๆ แต่ไม่มีโครง 30 วิ → ถ่ายแล้วเลอะ / ยาวเกิน / ไม่มี CTA
- แอปตัดต่อวิดีโอทั่วไปหนักและไม่ได้ช่วย "คิดโครง" — คนมือใหม่ต้องการ shot list + ตัวจับเวลามากกว่า timeline editor
- แคปชันไทย + แฮชแท็ก + คำคอมเมนต์ CTA มักคิดทีหลังจนลืม หรือคัดลอกของฝรั่งไม่เข้าบริบท

## 3) ทำไมไวรัลบน Reels

- **ภาพที่ทุกคนเจอเอง:** หน้าจอว่าง + ไอเดียในหัว = เจ็บตรงจุดใน 2 วิแรก
- **ก่อน/หลังชัด:** ข้อความอย่างเดียว → Blueprint 5 ช็อตพร้อมเวลา + Film Mode นับถอยหลัง
- **ตัวเลขเดโมจำง่าย:** 3+6+8+8+5 = 30 วิ · CTA 「คุกกี้」 · ฮุค "ข้อความ vs คลิป"
- **เซฟไว้ทำตาม:** หมวด "สอนถ่ายรีล" คนกดเซฟเยอะ และแอปใช้ได้ทันทีโดยไม่ต้องมีฟุตเทจสวย
- **การ์ด Blueprint / ปก** = ผู้ใช้แชร์ต่อเอง เป็นโฆษณาฟรีให้ช่อง

## 4) เป้าหมาย / ไม่ใช่เป้าหมาย

**เป้าหมาย**
- เดโมจบใน 30 วิ: วางไอเดีย → Blueprint → Film Mode → Caption/CTA → Hook A/B หรือปก
- สร้าง Blueprint ได้โดยไม่ต้องมี API key (เทมเพลต + heuristic ในเครื่อง)
- UI สวยแบบสตูดิโอรีล (พื้นมืด + นีออน) ถ่ายหน้าจอแล้วดูแพงบน Reels
- ภาษาไทยเป็นหลักทุกจุดสัมผัส

**ไม่ใช่เป้าหมาย (v1)**
- ไม่ใช่แอปตัดต่อวิดีโอ (ไม่มี timeline / ไม่ผสานคลิปให้)
- ไม่โพสต์ขึ้น IG/TikTok แทนผู้ใช้
- ไม่รับประกันยอดวิว/ยอดขาย
- ไม่มีบัญชีผู้ใช้บังคับ / คลาวด์ซิงก์
- ไม่ gen วิดีโอด้วย AI (แค่โครง + ข้อความ + ตัวจับเวลา)

## 5) ผู้ใช้หลัก

- **แม่ค้าออนไลน์ / แม่บ้านขายของ** อยากมีรีลแต่ไม่รู้จะพูดอะไร (ตัวละครเดโม: "เจี๊ยบ" — สมมติ · ขายคุกกี้เนยสด)
- **นักเรียน / ติวเตอร์** อยากสรุปสั้นๆ เป็นรีลติว
- **คนทำคอนเทนต์มือใหม่** มี voice note เต็มเครื่อง แต่เปิดกล้องทีไรสมองว่าง

## 6) User stories

1. ฉันวางไอเดียสั้นๆ หรือวางข้อความจาก voice note แล้วได้ Blueprint ภายใน 10 วินาที
2. ฉันเลือกสไตล์ (ก่อน/หลัง, สอน 3 ขั้น, Storytime…) และความยาว 15/30/45/60 วิ ได้โครงช็อตที่เวลารวมตรงเป้า
3. ฉันเข้า Film Mode แล้วเห็นข้อความที่ต้องพูด + นับถอยหลัง + แถบ progress · ถ่ายช็อตเดิมซ้ำได้
4. ฉันได้แคปชันสั้น/ยาว ภาษาไทย + แฮชแท็ก + คำคอมเมนต์ CTA พร้อมคัดลอก
5. ฉันได้ข้อความ overlay รายช็อต และปกคลิป 3 แบบ ส่งออก PNG
6. ฉันเทียบฮุค 3 สูตร เห็นคะแนน แล้วสลับฮุคเข้า Blueprint ได้ในแตะเดียว
7. ฉันอยากเก็บประวัติ Blueprint และเห็นสตรีควันที่สร้างคลิป เพื่อกลับมาเปิดซ้ำ

## 7) ฟีเจอร์ (≥ 5 บังคับ)

### Must-have (core demo)

| # | ฟีเจอร์ | รายละเอียด | Wow |
|---|---|---|---|
| 1 | **Idea Drop → Reel Blueprint** ⭐ | textarea วางไอเดีย · ปุ่มเดโม · (ทางเลือก) วาง transcript · เลือก style + duration → `parse_idea` + `build_blueprint` → การ์ด: Hook · Beats/Shots · CTA · duration · BGM mood · แอนิเมชันการ์ดช็อตเรียงเข้ามา | **Wow แรก** |
| 2 | **Shot List + Film Mode Timer** ⭐ | รายการช็อตเลขลำดับ · แตะเข้า Film Mode เต็มจอ · countdown 3 วิ · การ์ดพรอมป์กลางจอ · แถบ progress ช็อต + รวม · auto-advance · rewind ช็อต · haptic เมื่อจบช็อต | ถ่ายตามได้เลย |
| 3 | **Caption Pack (Thai)** | สั้น · ยาว · hashtags 8–12 จาก pool ตามหมวด · comment CTA keyword (เดโม: 「คุกกี้」) · ปุ่มคัดลอกทีละช่อง | พร้อมวางโพสต์ |
| 4 | **Overlay & Cover Forge** | overlay ใหญ่รายช็อต (≤ ~42 ตัวอักษร) · ปก 3 แบบ 1080×1920 (contrast / product / cta) · export PNG ด้วย html-to-image | ปกสวยในคลิป |
| 5 | **Hook A/B Lab** | ฮุค 3 สูตร · คะแนน curiosity / clarity / emotion · อันดับ 1 ติดแบดจ์ · แตะ "ใช้ฮุคนี้" → `swap_hook` อัปเดตช็อต 1 | ทดลองฮุคทันที |

### Nice-to-have (retention — ทำถ้าเหลือเวลา)

- **Style Templates library** — 5 สไตล์ใน `reference/reel.py → STYLES` (มีใน fixture แล้ว)
- **Voice → Idea** — ช่องวาง transcript จาก speech-to-text ของมือถือ (ไม่บังคับ mic API ใน v1)
- **Trend Angle Suggest** — `suggest_trend_angles` 5 มุม ภาษาไทย ผูก style
- **Export Pack ZIP** — blueprint.json + captions.txt + overlays PNG
- **Streak / History** — local history + สตรีควัน
- **Share Blueprint Card** — การ์ด 1080×1920 สรุปฮุค/ช็อต/CTA

## 8) กติกา parse ไอเดีย (`lib/parseIdea.ts` — pure, deterministic)

อินพุต: ข้อความดิบภาษาไทย/อังกฤษปน
เอาต์พุต: `ParsedIdea` — ดู `schemas.json → ParsedIdea`

กติกาหลัก (mirror `reference/reel.py`):
1. ตัดช่องว่างซ้ำ → `normalized`
2. จับหมวดจาก keyword list ตามลำดับ (snacks → beauty → study → …) คนแรกที่ชนะ
3. จับชื่อสินค้าด้วย regex เฉพาะ (คุกกี้…, ขนม…, เซรั่ม…) ไม่งั้นตัด 28 ตัวแรก
4. จับราคา: `ชิ้นละ N บาท` / `ขวดละ` / `กล่องละ` / `ราคา` / `฿N`
5. จับเซ็ต: `เซ็ต Q ชิ้น P` → `set_qty`, `price_set`
6. จับช่องทาง: LINE / IG / TikTok / Shopee / Lazada / Facebook
7. จับพื้นที่: กรุงเทพ/กทม/เชียงใหม่…
8. `cta_keyword` จากหมวด (snacks+คุกกี้ → 「คุกกี้」) ไม่สุ่ม

**ห้าม:** เดาสินค้าที่ไม่มีในข้อความ · เปลี่ยนราคา · ประดิษฐ์ช่องทาง

## 9) กติกา Blueprint / Hooks / Captions / Film

### 9.1 Style templates
แต่ละ style มี beats คงที่ `(beat_id, role, weight, overlay_key)` — ดู `STYLES` ใน `reel.py`
`allocate_durations(weights, target)` แบ่งวินาทีจำนวนเต็มให้ผลรวมเท่า `target` เสมอ (ทุกช็อตอย่างน้อย 1 วิ)

เดโมล็อก: style `soft_sell_before_after` · target 30 → durations **[3, 6, 8, 8, 5]**

### 9.2 Hooks
`_default_hooks(idea, style)` สร้าง 3 สูตรคงที่ตาม style
`rank_hooks` ให้คะแนน curiosity/clarity/emotion จาก keyword heuristic + โบนัสความยาว + โบนัส `vs`/`30 วิ`/`พุ่ง`
เรียง `total` มาก→น้อย แล้ว `id` น้อย→มาก · rank 1 = winner
เดโม: **hook_a** ชนะเสมอด้วยประโยค contrast "โพสต์ข้อความอย่างเดียว vs คลิป 30 วิ…"

### 9.3 Captions
`build_caption_pack` ใช้เทมเพลตไทย + hashtag pool ตามหมวด + COMMON_TAGS
บังคับ: `comment_cta_keyword` = idea.cta_keyword · แคปชันสั้นต้องมีคำ CTA

### 9.4 Overlays & covers
รายช็อตใช้ `shot.overlay_th` · ปก 3 แบบ titles ล็อกในเดโม:
1. `ข้อความ vs คลิป 30 วิ`
2. `คุกกี้เนยสด`
3. `คอมเมนต์ 「คุกกี้」`

### 9.5 Film mode
`film_progress(shots, elapsed_s)` คืนช็อตปัจจุบัน + progress
- ณ 0s → ช็อต 1
- ณ 10s → ช็อต 3 (เพราะ 3+6=9)
- ณ 30s → done
`film_rewind(shots, index)` กลับต้นช็อต
`swap_hook(blueprint, hook_id)` สร้าง blueprint ใหม่ด้วยฮุคที่เลือก (เวลาเท่าเดิม)

## 10) ความเป็นส่วนตัว + ความปลอดภัย (ทำก่อน UI)

- ทำงานในเครื่องเป็นค่าเริ่ม · ไม่บังคับล็อกอิน
- ไม่อัปโหลดไอเดียไปเซิร์ฟเวอร์ถ้า `ai_assist=off`
- ถ้าเปิด AI: ส่งเฉพาะข้อความไอเดีย/ฮุคที่ผู้ใช้ยืนยัน — ไม่ส่งรูป/วิดีโอ
- ไม่เก็บไฟล์วิดีโอที่ถ่าย (Film Mode เป็นตัวช่วยจับเวลา ไม่ใช่กล้องอัดในแอป v1 — ผู้ใช้เปิดกล้องเครื่องแยก หรือใช้ screen + กล้องหน้าตามที่ถนัด; แอปโชว์พรอมป์ overlay)
- ปุ่มลบประวัติ Blueprint ทั้งหมด
- Disclaimer: ไม่รับประกันยอดขาย/ยอดวิว · ข้อมูลตัวอย่างสมมติ

## 11) หน้าจอ

1. **Home** — โลโก้ ReelForge · ช่องไอเดีย · ปุ่มเดโม · ชิปสไตล์ · ชิปเวลา · สตรีคเล็กๆ
2. **Blueprint** — ฮุคใหญ่ · รายช็อต · BGM mood · CTA · ปุ่ม Film Mode / Caption / Overlay / Hook Lab
3. **Film Mode** — เต็มจอพื้นมืด · countdown · พรอมป์ · progress · ปุ่ม rewind / ข้าม / ออก
4. **Captions** — สั้น/ยาว/แฮชแท็ก/CTA · คัดลอก
5. **Overlays & Covers** — พรีวิวรายช็อต · 3 ปก · ส่งออก PNG
6. **Hook A/B Lab** — การ์ด 3 ฮุค + แถบคะแนน · ปุ่มใช้ฮุคนี้
7. **Styles / Angles** — ไลบรารีเทมเพลต + มุมแนะนำ
8. **History** — รายการ Blueprint ล่าสุด
9. **Share Card** — พรีวิวการ์ด + บันทึก
10. **Settings** — ภาษา · AI assist · haptic · ลบข้อมูล

## 12) Core flows

### Flow A — Happy path เดโม (หัวใจคลิป)
1. Home → 「ลองข้อมูลตัวอย่าง · เจี๊ยบ」
2. เติมไอเดียคุกกี้ + style ก่อน/หลัง + 30 วิ อัตโนมัติ
3. แสดง Blueprint ≤ 10 วิ (แอนิเมชันการ์ดช็อต)
4. ผู้ใช้กด Film Mode → countdown → ช็อต 1..5
5. กลับ Blueprint → แท็บแคปชันเห็น 「คุกกี้」
6. แท็บปก → ส่งออกปก A
7. Hook Lab → เห็น A ชนะ · (ทางเลือก) สลับ B

### Flow B — ไอเดียเอง
วางข้อความ → เลือก style/duration → สร้าง → แก้ฮุคใน Lab → Film Mode → คัดลอกแคปชัน

### Flow C — Voice paste
วาง transcript → แอป normalize เป็นไอเดีย → เหมือน Flow B

## 13) UI / แบรนด์

| โทเคน | ค่า |
|---|---|
| พื้น | `#0F0A1A` (dark cinema) |
| แมเจนตา | `#E11D48` (neon accent / CTA) |
| ไวโอเล็ต | `#8B5CF6` (secondary / chips) |
| ครีม | `#FDF4FF` (ตัวอักษรหลัก) |
| ทอง | `#FBBF24` (แบดจ์ชนะ / ดาว) |
| ฟอนต์ | sans หนาสำหรับ overlay · body อ่านง่าย |
| มุมโค้ง | การ์ด 20–24px · ชิปเต็มเม็ด |
| แอนิเมชัน | framer-motion: การ์ดช็อต stagger · progress spring · ฮุคสลับ crossfade |

โทน: สตูดิโอรีลกลางคืน — ถ่ายหน้าจอแล้วมี glow นีออน ไม่ใช้พื้นขาว

## 14) Tech

- **Framework:** Next.js 14 App Router + TypeScript + Tailwind + shadcn/ui + framer-motion
- **PWA:** manifest + service worker พื้นฐาน · ไอคอนนีออน
- **Deploy:** Vercel
- **State:** Zustand หรือ React context + persist
- **Storage:** IndexedDB (`blueprints`) · localStorage key `reelforge:v1`
- **Export:** `html-to-image` สำหรับปก/การ์ด · JSZip สำหรับ export pack
- **AI (optional):** route handlers `/api/ai/hooks` `/api/ai/captions` `/api/ai/angles` อ่าน `AI_API_KEY` — ถ้าไม่มี key ปุ่ม AI ซ่อนหรือโชว์ "ใช้โหมดในเครื่อง"
- **ทดสอบคอร์:** port `reference/reel.py` → `lib/*.ts` ให้ test_vectors ผ่านคู่กัน

## 15) ข้อมูล (สรุป — เต็มใน `schemas.json`, 47 defs)

เอนทิตีหลัก: ParsedIdea · Blueprint · Shot · HookCandidate · CaptionPack · OverlaysPack · CoverVariant · FilmProgress · StyleTemplate · ShareCard · Settings · LocalStore · AiHooksRequest/Response

เดโมล็อกตัวเลข (ต้องตรงทุกไฟล์):
- ไอเดีย: `ขายคุกกี้เนยสด ส่ง LINE ทั้งกรุงเทพ ชิ้นละ 45 บาท เซ็ต 6 ชิ้น 240`
- product `คุกกี้เนยสด` · category `snacks` · price 45 / set 6×240 · channel LINE · area กรุงเทพ · CTA `คุกกี้`
- 5 ช็อต · durations 3,6,8,8,5 · รวม 30
- hook_a rank 1 · covers 3

## 16) Analytics (local / console เท่านั้น)

อีเวนต์: `idea_submitted` · `blueprint_built` · `film_mode_started` · `hook_swapped` · `cover_exported` · `share_card_exported` · `demo_loaded` · `export_zip`
เก็บในเครื่องหรือ `console.info` — ไม่ส่งテレメทรีภายนอกใน v1

## 17) Acceptance criteria

1. Must-have 5 ฟีเจอร์ใช้งานได้ครบบนเดโม fixture
2. 「ลองข้อมูลตัวอย่าง」ได้ผลตาม `expect_locked` ทุกครั้ง (deterministic)
3. Film Mode: รวม 30 วิ · ณ 10s อยู่ช็อต 3 · rewind กลับต้นช็อตได้
4. Caption สั้นมี 「คุกกี้」 · hashtags ≥ 8
5. ปก 3 แบบ export เป็น PNG 1080×1920 ได้
6. Hook Lab แสดง 3 ฮุค · สลับแล้วช็อต 1 เปลี่ยน · เวลารวมยัง 30
7. ไม่มี API key ก็ใช้คอร์ได้
8. `python3 reference/tests.py` → fails 0 · schema validate 0 error
9. UI ไทย · มี disclaimer
10. PWA เปิดจากโฮมสกรีนได้ (อย่างน้อย manifest + icons)

## 18) ความเสี่ยง / กับดัก

| ความเสี่ยง | อาการ | กันยังไง |
|---|---|---|
| LLM เขียนช็อตสุ่ม | ตัวเลขเดโมไม่ตรงทุกเทค | คอร์ deterministic ในเครื่อง · AI เป็นทางเลือกเสริมเท่านั้น |
| Film Mode สับสนว่าเป็นกล้องในแอป | ผู้ใช้รออัดแต่ไม่มีไฟล์ | คัดลอกชัด: "เปิดกล้องเครื่อง / ถ่ายตามพรอมป์" · หรือโหมด picture-in-picture ภายหลัง |
| Overlay ยาวเกินจอ | ตัวอักษรถูกตัดบน IG | จำกัด ~42 ตัว · พรีวิว safe zone |
| ยัดฟีเจอร์ตัดต่อ | งานไม่จบวันเดียว | Out of scope ชัด · โฟกัส Blueprint + Timer |
| โฆษณายอดพุ่ง | โดนรีพอร์ต/เสียความน่าเชื่อถือ | Disclaimer + ห้ามพูดรับประกันในคลิปช่อง |
| Hashtag ซ้ำ/น้อยเกิน | ดูขี้เกียจ | pool ตามหมวด + COMMON · บังคับ 8–12 |

## 19) Reel shot list (สรุป — เต็มใน `examples.json → reel_script_th`)

0–3s โฮมมืดนีออน + ฮุคคำถาม · 3–7s วางไอเดีย/เดโม · 7–12s Blueprint 5 ช็อต · 12–18s Film Mode · 18–22s Caption+CTA · 22–26s Hook Lab/ปก · 26–30s การ์ดแชร์ + คอมเมนต์ 「รีล」

## 20) Out of scope (ภายหลัง)

- ตัดต่อรวมคลิปอัตโนมัติ / AI avatar / text-to-video
- โพสต์ตรงไป IG/TikTok Graph API
- ทีมเวิร์กสเปซ / คลาวด์ซิงก์
- วิเคราะห์ยอดวิวหลังโพสต์
- ภาษาอังกฤษเต็มรูปแบบ (มีสวิตช์โครงสร้างพอ)

## 21) แผนวันเดียว (~7 ชม.)

| ช่วง | เวลา | งาน |
|---|---|---|
| 0 | 0:00–0:30 | scaffold Next.js + Tailwind + สี + PWA เปล่า + ฟอนต์ |
| 1 | 0:30–2:00 | พอร์ต `reel.py` → `lib/*.ts` + เทสต์ vitest ให้ test_vectors ผ่าน |
| 2 | 2:00–3:00 | Home + Idea Drop + ปุ่มเดโม + หน้า Blueprint |
| 3 | 3:00–4:00 | Film Mode Timer (countdown, progress, rewind, auto-advance) |
| 4 | 4:00–5:00 | Caption Pack + Overlay/Cover export PNG |
| 5 | 5:00–5:45 | Hook A/B Lab + swap |
| 6 | 5:45–6:30 | Nice-to-have ที่เหลือเวลา (styles/history/share) + AI routes แบบ optional |
| 7 | 6:30–7:00 | QA ตามส่วน K · อัด Reel ตามสคริปต์ · เช็ก disclaimer |

**คำสั่งตรวจคอร์ก่อน UI:**  
`cd reference && python3 build.py && python3 schema.py && python3 tests.py`


## 22) รายละเอียดหน้าจอ (wire สั้น)

### Home
- Hero: โลโก้ + tagline "โยนไอเดีย → ได้ชุดถ่ายพร้อมจับเวลา"
- Textarea สูง 120–160px พื้น `#1A1228` ขอบ glow แมเจนตาตอนโฟกัส
- แถวชิปสไตล์เลื่อนแนวนอน (5 สไตล์) · แถวชิปเวลา 15/30/45/60 (ดีฟอลต์ 30)
- ปุ่มหลักแมเจนตา "สร้าง Blueprint" · ปุ่มรองโกสต์ "ลองข้อมูลตัวอย่าง · เจี๊ยบ"
- ท้ายจอ: สตรีค · ประวัติล่าสุด 1 การ์ด

### Blueprint
- ฮุคใหญ่ด้านบน (ครีมบนพื้นมืด) · แบดจ์สไตล์ + เวลา + BGM
- ลิสต์ช็อต: เลขวงกลมนีออน · เวลา · title · overlay ย่อ · แตะขยาย VO/พรอมป์
- Sticky CTA ล่าง: Film Mode (หลัก) · แคปชัน · ปก · ฮุค A/B

### Film Mode
- ซ่อนนาวิเกชัน · safe area
- บน: ช็อต n/N · เวลาเหลือช็อต · เวลาเหลือรวม
- กลาง: การ์ดพรอมป์ + overlay ใหญ่
- ล่าง: แถบ progress สองชั้น (ช็อต / รวม) · ปุ่ม rewind · ปause · ข้าม
- countdown 3-2-1 ก่อนเริ่มและก่อนแต่ละช็อต (ตั้งปิดได้ใน Settings)

### Hook A/B Lab
- 3 การ์ดซ้อน/เรียง · แถบคะแนน 3 แกน · อันดับ 1 มีขอบทอง + ป้าย "ชนะ · แนะนำ"
- ปุ่ม "ใช้ฮุคนี้" → toast "สลับฮุคแล้ว · ช็อต 1 อัปเดต"

## 23) ตารางตัวเลขเดโมที่ล็อก (อย่าเปลี่ยน)

| ฟิลด์ | ค่า |
|---|---|
| raw idea | ขายคุกกี้เนยสด ส่ง LINE ทั้งกรุงเทพ ชิ้นละ 45 บาท เซ็ต 6 ชิ้น 240 |
| product | คุกกี้เนยสด |
| category | snacks |
| price_unit / set | 45 / 6 ชิ้น 240 |
| channel / area | LINE / กรุงเทพ |
| style | soft_sell_before_after |
| durations | 3, 6, 8, 8, 5 (sum 30) |
| hook winner | hook_a (contrast · มีคำว่า vs และ 30 วิ) |
| CTA keyword | คุกกี้ |
| covers | 3 (contrast / product / cta) |
| film @10s | ช็อต 3 |

## 24) เกณฑ์คะแนนฮุค (สรุป heuristic)

- base curiosity 38 / clarity 42 / emotion 36
- +12 ต่อคีย์เวิร์ดที่โดนในแกนนั้น
- +10 ถ้าความยาว 18–70 ตัวอักษร · +8 ถ้ามี ? ! — หรือ vs
- โบนัสพิเศษ: มี `vs` หรือ `อันไหน` → +14 curiosity · มี `30 วิ`/`3 ขั้น` → +10 clarity · มี `พุ่ง`/`ขายได้`/`แม่ค้า` → +12 emotion
- clamp 0–100 ต่อแกน · total = ผลรวม · เรียง total แล้ว id

## 25) สัญญา AI ทางเลือก (ไม่บล็อกเดโม)

ถ้ามี `AI_API_KEY`:
- `/api/ai/hooks` → เสนอฮุคเพิ่ม แต่ต้องผ่าน `rank_hooks` ก่อนแสดง
- `/api/ai/captions` → แคปชันทางเลือก · ผู้ใช้กด "ใช้เวอร์ชันนี้" ก่อนทับของเดิม
- `/api/ai/angles` → มุมคลิปเสริม

ถ้าไม่มี key: UI ใช้เฉพาะ deterministic packs จาก `examples.json` / `lib/*` — เดโมยังจบได้ 100%

## 26) คำศัพท์ในแอป (อย่าแปลปน)

ใช้คำไทยเหล่านี้คงที่: Blueprint, Film Mode, ฮุค, ช็อต, แคปชัน, ปก, Overlay, CTA, สตรีค
ไม่ต้องแปล Blueprint/Film Mode เป็นไทยยาว — คุ้นในกลุ่มครีเอเตอร์ไทยแล้ว
