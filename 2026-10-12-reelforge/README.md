# ReelForge — ชุดส่งมอบเช้า (AI วันละแอป)

**วันที่:** 2026-10-12 (Asia/Bangkok)
**วันในคิว:** 10 / 10 (รอบสุดท้าย · ชดเชยรอบ 9 ต.ค. ที่พลาด)
**ช่อง:** AI วันละแอป
**สถานะ:** พร้อม gen วันนี้

โยนไอเดียขายคุกกี้เนยสด → 10 วิได้ **Blueprint 5 ช็อต (3+6+8+8+5 = 30 วิ)** · ฮุคชนะ **「โพสต์ข้อความอย่างเดียว vs คลิป 30 วิ」** · แคปชันไทย + คอมเมนต์ **「คุกกี้」** · ปก 3 แบบ · เข้า Film Mode จับเวลาถ่าย
ฮุคหลัก Reel: **ไอเดียในหัวแต่ไม่รู้จะเปิดคลิปยังไง? โยนเข้าแอปนี้ 10 วิ… ได้ชุดถ่ายพร้อมจับเวลาเลย 🎬**

---

## ไฟล์ในโฟลเดอร์นี้

| ไฟล์ | ใช้ทำอะไร |
|---|---|
| `prd.md` | สเปกเต็ม: ปัญหา ทำไมไวรัล เป้าหมาย persona สตอรี่ ฟีเจอร์ กติกา parse/blueprint/hooks/captions/film ความเป็นส่วนตัว หน้าจอ flow UI เทค acceptance ความเสี่ยง ช็อต Reel แผนวันเดียว |
| `prompts.md` | Prompt A–N: master codegen / เดโม / types / parseIdea+blueprint / hooks+captions / idea drop+film / overlays+covers / hook lab / nice-to-have / QA / แก้บั๊ก / **runtime prompts 3 ตัว** / หน้าอัด Reel |
| `schemas.json` | JSON Schema (draft 2020-12) 47 defs: ParsedIdea, Blueprint, Shot, HookCandidate, CaptionPack, OverlaysPack, CoverVariant, FilmProgress, StyleTemplate, ShareCard, LocalStore, AiHooksRequest ฯลฯ |
| `examples.json` | ข้อมูลตัวอย่าง "เจี๊ยบ" (สมมติ): ไอเดียคุกกี้ · blueprint 5 ช็อต · caption pack · 3 ปก · Hook A/B Lab · Film Mode ณ 0/3/10/29/30 วิ · UI copy ไทย · สคริปต์ Reel · test vectors 14 ข้อ (ตรวจกับ schema แล้ว 0 error, คำนวณซ้ำแล้วตรง) |
| `reference/` | Python อ้างอิง: `reel.py` (parse + blueprint + hooks + captions + overlays + film), `fixtures.py`, `build.py`, `schema.py`, `tests.py` |
| `README.md` | ไฟล์นี้ |

แพ็กเต็มแบบ zip: `/workspace/reelforge.zip` (unzip แล้วได้ `reelforge/...`)

---

## ฟีเจอร์บังคับ ≥ 5 (Must-have)

| # | ฟีเจอร์ | ทำไมติดรีเทน / ไวรัล |
|---|---|---|
| 1 | **Idea Drop → Reel Blueprint** ⭐ | Wow แรก: วางไอเดีย 10 วิ → ได้ฮุค · บีต · CTA · เวลา · มู้ด BGM |
| 2 | **Shot List + Film Mode Timer** ⭐ | การ์ดพรอมป์ + นับถอยหลัง + แถบ progress · ถ่ายตามได้ทันที |
| 3 | **Caption Pack (Thai)** | แคปชันสั้น/ยาว + แฮชแท็ก 8–12 + คำคอมเมนต์ CTA |
| 4 | **Overlay & Cover Forge** | ข้อความบนจอรายช็อต + ปก 3 แบบ 1080×1920 ส่งออก PNG |
| 5 | **Hook A/B Lab** | ฮุค 3 สูตร จัดอันดับ curiosity/clarity/emotion · สลับเข้า Blueprint แตะเดียว |

**Nice-to-have:** Style Templates (ก่อน/หลัง, สอน 3 ขั้น, Storytime, Unboxing, Soft sell) · Voice → Idea · Trend Angle Suggest · Export Pack ZIP · Streak/History · Share Blueprint Card

---

## วิธีใช้กับ AI codegen (เช้านี้)

1. เปิด `prompts.md` ส่วน **A) Master prompt** วางเป็นคำสั่งหลัก
2. แนบบริบท: `prd.md` + `schemas.json` + `examples.json` + `reference/reel.py`
3. สั่งให้ happy path ด้วยข้อมูลตัวอย่างจบก่อน (ไอเดียคุกกี้ → 5 ช็อต 30 วิ → ฮุค A → 「คุกกี้」 → 3 ปก → Film Mode)
4. ส่วน **D** ทำ `lib/parseIdea.ts` + `lib/blueprint.ts` + เทสต์ให้ผ่านก่อน UI (หัวใจคลิป) · ส่วน **E** ทำ hooks/captions/overlays
5. ค่อยต่อ Film Mode (ส่วน **F**) แล้วลองถ่ายตามเดโม · ก่อนถ่ายรันส่วน **K (QA)**

เป้าเวลา: ราว 7 ชม. (ตารางใน `prd.md` §21)

---

## ฮุคโพสต์ / แคปชันสั้น

> ไอเดียในหัวแต่ไม่รู้จะเปิดคลิปยังไง? โยนเข้าแอปนี้ 10 วิ… ได้ชุดถ่ายพร้อมจับเวลาเลย 🎬

เวอร์ชันยาว:

> มีไอเดียขายของ / เล่าเรื่อง แต่ค้างที่หน้าจอว่างเปล่า? วันนี้แจก ReelForge จากช่อง AI วันละแอป วางไอเดียหรือ voice note แอปจัด Blueprint ให้: ฮุค 0–3 วิ · ช็อตรายข้อพร้อมเวลา · แคปชันไทย · ข้อความบนจอ · ปกคลิป · ทดลองฮุค 3 สูตร แล้วเข้า Film Mode จับเวลาถ่ายตาม คอมเมนต์ "รีล" รับลิงก์ฟรี

---

## กฎช่อง (อย่าพลาดตอนถ่าย)

- เปิดคลิปด้วย **หน้าโฮมมืดนีออน + ช่องวางไอเดีย** ภายใน 3 วินาที
- โชว์อย่างน้อย **4 ฟีเจอร์** (Blueprint → Film Mode → Caption/CTA → Hook A/B หรือปก) + การ์ดแชร์แวบเดียว
- **ห้าม**โชว์ยอดขายจริง / สลิปโอนจากลูกค้าจริงในคลิป — ใช้เดโม "เจี๊ยบ" เท่านั้น
- **ห้าม**พูดว่า "รับประกันยอดพุ่ง" หรือ "AI เขียนสคริปต์แทนคุณทั้งหมด" — เน้นชุดถ่าย + จับเวลา
- ใส่ "(ข้อมูลตัวอย่างสมมติ)" ใน caption · CTA: คอมเมนต์คำว่า **「รีล」**

---

## สแต็กแนะนำ (สรุป)

- Next.js 14 App Router + TypeScript + Tailwind + shadcn/ui + framer-motion · PWA · Vercel
- คอร์ logic ในเครื่อง: `lib/parseIdea.ts` `lib/blueprint.ts` `lib/hooks.ts` `lib/captions.ts` `lib/overlays.ts` `lib/film.ts` (mirror `reference/reel.py` — ไม่มี key ก็ใช้ได้จริง)
- AI ผ่าน `/api/ai/*` (env `AI_API_KEY`) ใช้แค่ขยายฮุค/แคปชันทางเลือก — คะแนนฮุค + โครงช็อตใช้สูตรในเครื่องเสมอ
- ข้อมูล IndexedDB (`blueprints`) + localStorage `reelforge:v1` · การ์ด/ปก html-to-image
- สี: พื้น `#0F0A1A` · แมเจENTA `#E11D48` · ไวโอเล็ต `#8B5CF6` · ครีม `#FDF4FF` · ทอง `#FBBF24`

---

## Acceptance ก่อนประกาศว่า “พร้อมลงคลิป”

- [ ] Must-have ครบ 5 และติ๊กใน `feature_checklist_example`
- [ ] 「ลองข้อมูลตัวอย่าง」→ 5 ช็อต · 3+6+8+8+5=30 · ฮุค A · CTA 「คุกกี้」 · ปก 3 แบบ ภายใน ≤ 10 วิ ทุกเทค
- [ ] Film Mode รวม 30 วิ · auto-advance · rewind ช็อตได้
- [ ] test_vectors ผ่าน 14/14 · schema 0 error
- [ ] ไม่บังคับล็อกอิน · ไม่มี key ก็สร้าง Blueprint ได้
- [ ] มี disclaimer "ตัวอย่างสมมติ · ไม่รับประกันยอดขาย"

---

## Wow moment ที่ต้องโชว์ในคลิป

1. **วางไอเดีย / กดเดโม → การ์ด Blueprint บินเข้ามา 5 ช็อตพร้อมเวลาวิ่ง 3·6·8·8·5 → ฮุคใหญ่ "ข้อความ vs คลิป 30 วิ"**
2. **เข้า Film Mode → นับถอยหลัง → การ์ดพรอมป์ช็อต 1 → แถบ progress วิ่ง → สลับฮุค B แล้วช็อต 1 เปลี่ยนทันที**

ดู `examples.json` → `blueprint_example`, `caption_pack_example`, `overlays_example`, `hook_lab_example`, `film_mode_examples`, `reel_script_th`
