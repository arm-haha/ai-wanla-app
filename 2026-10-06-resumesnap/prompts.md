# ResumeSnap — Prompt สั่งงาน (จัดเต็ม)

ใช้กับ AI codegen (Cursor / Claude / GPT) สร้างแอปทั้งก้อน + prompt ที่ใช้ "ข้างในแอป" ตอนเรียก LLM จริง

**วันที่แพ็ก:** 2026-10-06 (Asia/Bangkok) · Day 7/10 · AI วันละแอป
**เอกสารคู่กัน:** `prd.md`, `schemas.json`, `examples.json`

| ส่วน | ใช้ทำอะไร |
|---|---|
| A | Master prompt สร้างทั้งแอป |
| B | ข้อมูลตัวอย่าง "มายด์" + ประกาศงาน Kinjai |
| C | TypeScript types |
| D | `lib/score.ts` + tailor (หัวใจคลิป 63 → 87) |
| E | Bullet Glow-up + grounding guard |
| F | 6 เทมเพลต + auto-fit หน้าเดียว + Editor |
| G | Export PDF / PNG / TXT + การ์ดแชร์ |
| H | Brain dump ของจริง: LLM + OCR รูปเรซูเม่เก่า + เสียง |
| I | Nice-to-have pack |
| J | Reel script / overlay |
| K | QA ก่อนถ่าย |
| L | แก้ปัญหาเร็ว |
| M | Runtime prompts (system prompt ที่แอปส่งให้ LLM) |

---

## A) Master prompt สร้างทั้งแอป (วางครั้งเดียว)

```text
สร้างเว็บแอปมือถือเป็นหลักชื่อ ResumeSnap (UI ภาษาไทยก่อน)

วันที่ส่งมอบคอนเทนต์: 2026-10-06 สำหรับช่อง "AI วันละแอป"
เป้าหมายผู้ใช้: เทโน้ตมั่วๆ (พิมพ์/พูด/ถ่ายรูปเรซูเม่เก่า) → ได้เรซูเม่ A4 หน้าเดียวสวยพร้อมส่ง →
วางประกาศงาน → เห็นคะแนนเข้ากัน + คีย์เวิร์ดที่ขาด → กดปรับให้ตรงงาน (ไม่แต่งเรื่อง) → ส่งออก PDF + การ์ดแชร์ก่อน/หลัง

สแต็กบังคับ:
- Next.js 14 App Router + TypeScript + Tailwind CSS + shadcn/ui + framer-motion
- lib/score.ts pure deterministic (vitest) ตามกติกาใน prd.md §8
- lib/extract.ts, lib/tailor.ts, lib/glowup.ts มี 2 engine: "mock_demo" (ค่าเริ่ม คืนค่าจาก examples.json) และ "llm_api"
  (เรียก route /api/ai ฝั่ง server, อ่าน env AI_API_KEY, structured JSON ตาม schemas.json)
- lib/grounding.ts: ทุก bullet ที่ AI สร้างต้องมี source_quote ที่อยู่ใน RawInput; ตัวเลขที่ไม่มีใน RawInput → [X] + needs_confirm
- lib/fit.ts: auto-fit 1 หน้า A4 (ลด spacing → ลดฟอนต์ทีละ 0.25pt ขั้นต่ำ 9.5pt → ถ้ายังล้นให้แนะนำตัด bullet)
- lib/storage.ts: localStorage key "resumesnap:v1" ตาม LocalStore + IndexedDB สำหรับรูป
- lib/export.ts: หน้า /print/[id] + window.print() (@page A4 margin 0) + PNG (html-to-image) + TXT แบบ ATS
- lib/share.ts: การ์ด 1080x1920 ก่อน/หลัง เบลอข้อมูลส่วนตัวค่าเริ่ม + navigator.share files + fallback ดาวน์โหลด
- Deploy Vercel + PWA manifest · ไม่มี auth ไม่มี database

ต้องมีอย่างน้อย 5 ฟีเจอร์ must-have:
1) Brain Dump → Resume — textarea ใหญ่ + ไมค์ (Web Speech th-TH) + แนบรูปเรซูเม่เก่า → animation "ข้อความแตกเป็นหัวข้อ
   ประกอบเป็นกระดาษ A4" + ชิปถามข้อมูลที่ขาด (missing_fields)
2) Template Flip — carousel 6 เทมเพลต (clean_blue, minimal_mono, creative_side, modern_photo, ats_plain, fresh_grad)
   ปัดซ้าย-ขวา ข้อมูลชุดเดียว + เลือกสีหลัก 6 สี + ป้าย "ATS ปลอดภัย"
3) Job Match Tailor — วางประกาศ → keyword (mock/LLM) → gauge คะแนน 0–100 + breakdown 4 แท่ง + chip เจอ/ขาด
   → การ์ดคำแนะนำ (grounded กดใช้ได้ / ungrounded แสดงเป็นคำถามเท่านั้น) → "ปรับเรซูเม่ให้ตรงงานนี้" สร้างสำเนา
   (parent_id) → คะแนนวิ่งขึ้น + คีย์เวิร์ดถูกปาดไฮไลต์เหลือง
4) Bullet Glow-up — ปุ่ม ✨ ทุก bullet → sheet 3 สไตล์ (impact / concise / formal อังกฤษ) → ห้ามแต่งตัวเลข ใช้ [X]
5) Export & Share — PDF A4/Letter, PNG, TXT · ชื่อไฟล์ ชื่อ_นามสกุล_ตำแหน่ง.pdf · บล็อกถ้ามี needs_confirm ค้าง ·
   การ์ดแชร์ 3 แบบ (story_before_after / square_preview / qr_card)

ปุ่ม「ลองข้อมูลตัวอย่าง (มายด์)」โหลด examples.json → extract_result_example + job_post_example ได้ทันที
และ mock engine ต้องให้ผลเหมือนเดิมทุกครั้ง (63 ก่อน → 87 หลัง)

พิเศษถ้าเสร็จเร็ว (nice-to-have): Cover Letter 3 โทน, Interview Drill, Application Tracker, Photo Check (เชิงเทคนิคเท่านั้น),
TH/EN toggle, Version Compare, Dark mode

หน้าจอ: Home, Brain Dump, Generating, Resume Editor, Job Match, Tailored Compare, Export/Share, Settings
(+ Cover Letter / Drill / Tracker ถ้าทำ) · bottom nav: เรซูเม่ | จับคู่งาน | สมัครแล้ว | ตั้งค่า

UX บังคับ:
- มือถือ 390px ฐาน, ปุ่ม ≥48px, พรีวิว A4 ย่อพอดีจอด้วย CSS transform
- สี: พื้น #F5F8FF, กระดาษ #FFFFFF, ฟ้า #2563EB, หมึก #0F172A, ไฮไลต์ #FDE047, เขียว #22C55E, ส้ม #F97316, ขอบ #E2E8F0
- ฟอนต์ UI IBM Plex Sans Thai · ในเรซูเม่ Sarabun/IBM Plex Sans Thai + Inter (EN)
- ข้อความ UI ตาม examples.json → ui_copy_th
- ใต้ gauge: 「คะแนนประมาณจากคีย์เวิร์ดและโครงสร้าง ไม่ใช่คะแนนจากระบบ HR จริง」
- footer Editor: 「AI ช่วยเรียบเรียง — ตรวจทุกข้อให้เป็นความจริงก่อนส่ง」

กฎความปลอดภัย (ห้ามละเมิด):
- ห้ามสร้างประสบการณ์ ทักษะ เครื่องมือ ตัวเลข หรือวุฒิที่ไม่มีในข้อมูลผู้ใช้
- ห้ามอนุมานอายุ เพศ ศาสนา สถานภาพ หน้าตา · show_photo / show_age ค่าเริ่ม false
- ไม่ส่งข้อมูลออกนอกเครื่อง ยกเว้นผู้ใช้เปิด llm_api

คุณภาพโค้ด:
- components/, components/templates/*.tsx, hooks/, lib/*.ts, types/resumesnap.ts สอดคล้อง schemas.json
- unit tests: score.ts (ตัวอย่าง 63/87), grounding.ts (ตัวเลขแปลกปลอม → [X]), fit.ts (ไม่ต่ำกว่า 9.5pt)
- README ไทย: วิธีรัน, ใส่ AI_API_KEY, วิธีถ่าย Reel
- เริ่มจาก npm run dev ผ่าน + happy path (ตัวอย่าง → ปัดเทมเพลต → วางประกาศ → 63 → ปรับ → 87 → ✨ → PDF → แชร์)
  ด้วย mock ก่อน แล้วค่อยต่อ LLM/OCR/เสียงจริง

อ้างอิงฟิลด์จาก schemas.json + ตัวอย่างจาก examples.json ที่แนบมา
เมื่อจบสรุปว่า must 5 ตัวอยู่ไฟล์ไหน + วิธีโหลดข้อมูลตัวอย่าง 1 ย่อหน้า
```

---

## B) ข้อมูลตัวอย่าง "มายด์" + ประกาศงาน

```text
สร้างไฟล์ /public/demo/maid.json จาก examples.json ให้มี:
- brain_dump_input (RawInput) — ข้อความโน้ตมั่วๆ ของมายด์ (ใช้ตามตัวอย่างทุกตัวอักษร)
- extract_result_example (ExtractResult) — เรซูเม่ฐาน r_base
- job_post_example (JobPost) — Kinjai Foods (บริษัทสมมติ) Junior Content Marketing, 12 keyword
- match_before_example / tailored_resume_example / match_after_example
- bullet_glowup_examples, cover_letter_example, interview_drill_example

กติกา:
- ทุกชื่อ/บริษัทเป็นของสมมติ อีเมล @example.com เบอร์ปิดบางส่วน 08x-xxx-1234
- เวลา Asia/Bangkok (+07:00)
- mock engine (lib/extract.ts, lib/tailor.ts, lib/glowup.ts) อ่านไฟล์นี้แล้วหน่วง 2400ms / 1200ms / 700ms ตามลำดับ
  เพื่อให้ animation ในคลิปเหมือนเดิมทุกเทค
- ถ้าผู้ใช้พิมพ์ข้อความอื่นที่ไม่ใช่ตัวอย่างและไม่มี key → แสดง「โหมดตัวอย่าง: ใส่ AI key เพื่อใช้ข้อมูลของคุณ」
  และยังให้ลองข้อมูลตัวอย่างได้
- เพิ่มประกาศงานตัวอย่างที่ 2 (job_demo_2: Social Media Executive) สำหรับ Tracker
```

---

## C) TypeScript types

```text
อ่าน schemas.json ของ ResumeSnap แล้วสร้าง types/resumesnap.ts

ต้องมี: Lang, TemplateId, AccentColor, InputSource, SectionKey, DateYM, RawInput, Link, Contact, Bullet,
ExperienceItem, ProjectItem, EducationItem, SkillGroup, LanguageSkill, Certification, ResumeDoc, ExtractResult,
JobKeyword, JobPost, TailorSuggestion, MatchResult, GlowupOption, BulletGlowup, CoverLetter, InterviewQuestion,
InterviewDrill, ExportJob, ShareCard, ApplicationEntry, PhotoCheck, Settings, LocalStore, AnalyticsEvent,
FeatureChecklist, AiEngine ("mock_demo" | "llm_api")

กติกา: union string ตรง enum, JSDoc สั้นอังกฤษ, export ทุก type, ห้าม any, optional ใช้ ?
เพิ่ม zod schemas คู่กันใน lib/zod.ts สำหรับ validate ผลจาก LLM ก่อนเก็บ (ถ้า parse ไม่ผ่าน → retry 1 ครั้ง → fallback แจ้งผู้ใช้)
```

---

## D) `lib/score.ts` + tailor (หัวใจคลิป)

```text
เขียน lib/score.ts (pure, ไม่มี side effect) export:
  scoreResume(resume: ResumeDoc, job: JobPost, opts?: { onePage?: boolean }): MatchResult

กติกา (ตาม prd.md §8 ห้ามเปลี่ยน):
- corpus = headline + summary + role ทุกงาน + ชื่อโปรเจกต์ + ทุก bullet + skills items + languages (name, test)
  + activities + education (degree, major) → lowercase
- keyword เจอ = term หรือ alias ใดๆ เป็น substring ของ corpus (case-insensitive)
- keywords = floor(60 * Σweight เจอ / Σweight ทั้งหมด)
- structure = (email && phone ? 5 : 0) + (summary ? 4 : 0) + (ทุก experience มี start และ end ? 3 : 0)
              + (section_order.slice(0,3) มี "skills" ? 3 : 0)
- impact = floor(15 * #bullet(has_metric && !needs_confirm) / #bullet ทั้งหมดใน experience+projects)
- length = (fits_one_page ? 8 : 0) + (ทุก bullet ≤ 110 ตัวอักษร ? 2 : 0)
- score_label: 0–49 ยังห่าง, 50–69 พอใช้, 70–84 ดี, 85–100 เข้าทางมาก
- matched_keywords / missing_keywords เรียงตามลำดับใน job.keywords

Unit test บังคับ (vitest):
- extract_result_example.resume + job_post_example → {31,12,10,10} = 63, matched 5 ตัว
- tailored_resume_example + job_post_example → {52,15,10,10} = 87, missing = Meta Business Suite, Brand voice, Teamwork

แล้วเขียน lib/tailor.ts:
  suggest(resume, job, raw: RawInput): TailorSuggestion[]   // mock = คืน match_before_example.suggestions
  applyAll(resume, suggestions): ResumeDoc                 // ใช้เฉพาะ grounded === true, สร้างสำเนาใหม่ id ใหม่ parent_id = เดิม
- ungrounded ทุกตัวแสดงเป็นการ์ดคำถาม 2 ปุ่ม「เคยทำ เพิ่มเลย」/「ไม่เคย」 — กด "เคยทำ" ค่อยเพิ่มด้วย origin "user"

UI Job Match:
- gauge วงกลม 160px นับเลขด้วย framer-motion spring, สีส้ม (<70) → เขียว (≥70)
- breakdown 4 แท่งแนวนอน + tooltip อธิบายแต่ละแท่งเป็นภาษาคน
- ตอน applyAll: เลื่อนพรีวิวไปที่จุดที่เปลี่ยน แล้วปาดไฮไลต์เหลือง #FDE047 ที่คำใหม่ (clip-path 0.4s ทีละคำ ห่าง 120ms)
  แล้วค่อยนับ gauge 63 → 87 + เสียง ding เบาๆ (ปิดได้)
```

---

## E) Bullet Glow-up + grounding guard

```text
เขียน lib/grounding.ts:
- normalize(s): lowercase, ยุบช่องว่าง, ตัด zero-width, แปลงเลขไทย ๐-๙ เป็นอารบิก
- isGrounded(bullet, raw): source_quote มีและเป็น substring ของ normalize(raw.text)
- numbersIn(s): ดึงตัวเลขรวมรูปแบบ 1.2K, 310K, 3.42, 25%, 1,200
- guardNumbers(text, raw): ตัวเลขใดใน text ที่ไม่มีใน numbersIn(raw.text) → แทนด้วย "[X]" และคืน { text, placeholders, needs_confirm }
  ข้อยกเว้น: "N เท่า" หรือ % ที่คำนวณได้จากการหาร 2 ตัวเลขใน raw (คลาดเคลื่อน ≤5%) ยอมให้ผ่าน เช่น 4.8K/1.2K = "4 เท่า"
  ระยะเวลา ("ใน 8 เดือน") ต้องมีใน raw ตรงตัวเท่านั้น ห้ามคำนวณจากวันที่เอง
- ใช้ guard กับผลทุกตัวจาก extract / tailor / glowup ก่อนบันทึก

เขียน lib/glowup.ts:
  glowup(bullet: Bullet, ctx: { resume, job?, raw }): Promise<BulletGlowup>
- mock: คืน bullet_glowup_examples ตาม bullet_id ถ้าไม่มีให้ใช้ template
  impact = "<กริยาแสดงผลงาน> <สิ่งที่ทำ> [ผลลัพธ์ [X]]"
- llm: ใช้ runtime prompt M3

UI GlowupSheet (bottom sheet):
- ประโยคเดิมขีดฆ่าจางๆ ด้านบน → 3 การ์ดสไตล์ (ป้าย 💥 ปัง / ✂️ กระชับ / 🇬🇧 English)
- [X] แสดงเป็นช่องกรอกสีเหลืองในบรรทัด แตะแล้วพิมพ์ตัวเลขได้ทันที
- เลือกแล้ว bullet origin = "ai_glowup", ถ้ายังมี [X] → needs_confirm = true และมี badge เหลืองบนพรีวิว
- ปุ่ม "ใช้ประโยคเดิม" เสมอ
```

---

## F) 6 เทมเพลต + auto-fit + Editor

```text
สร้าง components/templates/ ทั้งหมด 6 ไฟล์ รับ props { resume: ResumeDoc, accent: string } render ขนาด A4 จริง (794x1123 px @96dpi)

1) clean_blue — คอลัมน์เดียว, ชื่อใหญ่ 28pt, เส้นใต้หัวข้อสี accent, ATS ปลอดภัย
2) minimal_mono — ขาวดำ, serif หัวข้อ, ระยะห่างเยอะ, ATS ปลอดภัย
3) creative_side — แถบซ้าย 32% สี accent ใส่ contact/skills/languages, ขวาใส่ประสบการณ์
4) modern_photo — วงกลมรูป 96px มุมขวาบน (แสดงเมื่อ show_photo), การ์ด section มุมโค้ง
5) ats_plain — ไม่มีไอคอน/ตาราง/คอลัมน์, หัวข้อภาษาอังกฤษมาตรฐานได้ (Experience, Education, Skills)
6) fresh_grad — education + projects ขึ้นก่อน experience

ทุกเทมเพลต:
- ใช้ section_order ของ resume (fresh_grad override ได้), ไม่ render section ว่าง
- วันที่แสดงเป็น "มิ.ย. 2567 – ส.ค. 2567" ตอน lang=th (พ.ศ.) และ "Jun 2024 – Aug 2024" ตอน en; present → "ปัจจุบัน"/"Present"
- bullet ที่ needs_confirm มีจุดเหลืองเล็กๆ บนจอเท่านั้น (ไม่ออกตอนพิมพ์)

lib/fit.ts: วัด scrollHeight ของกระดาษ ถ้า > 1123px → ลด line-height/gap ทีละขั้น (3 ขั้น) → ลดฟอนต์ 0.25pt
จนถึง 9.5pt → ยังล้น set fits_one_page=false + toast "ยาวเกิน 1 หน้า ลองตัด bullet ที่สั้นที่สุดไหม?"

TemplateCarousel: scroll-snap แนวนอน, พรีวิวย่อ 0.42x, จุดบอกตำแหน่ง, haptic เบาๆ ทุกครั้งที่ snap, แถบสี 6 จุดด้านล่าง
(#2563EB, #0F172A, #0D9488, #DB2777, #EA580C, #7C3AED)

Editor: แตะ section บนพรีวิว → sheet แก้ไขฟอร์ม · ลากเรียง section ได้ · ชิป missing_fields ลอยด้านบน
```

---

## G) Export + Share

```text
lib/export.ts:
- exportPdf(resumeId): ถ้ามี bullet needs_confirm → คืน ExportJob { blocked_by_unconfirmed: n } และเปิด sheet
  "เหลือ {n} จุดที่ต้องยืนยันก่อนส่งออก" พร้อมลิสต์ให้แตะไปแก้
- ไม่ติด → เปิด /print/[id] (เทมเพลตเดียวกัน scale 1, @page { size: A4; margin: 0 }, ซ่อน UI) → window.print()
  ตั้ง document.title = file_name เพื่อให้ชื่อไฟล์ PDF ถูก
- file_name = `${ชื่อ}_${นามสกุล}_${ตำแหน่งย่อ}.pdf` แปลงเป็นอังกฤษถ้ามี nickname EN ไม่งั้นใช้ไทยได้ ห้ามมี / \
- exportPng: html-to-image pixelRatio 2
- exportAtsTxt: ข้อความล้วนเรียงหัวข้อมาตรฐาน สำหรับวางในช่องเว็บสมัครงาน

lib/share.ts การ์ด 1080x1920 (story_before_after):
- ครึ่งบน "ก่อน": ภาพโน้ตมั่ว (render จาก RawInput 6 บรรทัดแรก เบลอเลขโทร/อีเมล) เอียง -4°
- ครึ่งล่าง "หลัง": พรีวิวเรซูเม่ tailored เอียง 3° + gauge 63 → 87
- หัว headline_th, มุมล่าง "ทำด้วย ResumeSnap · AI วันละแอป"
- blur_personal_info=true → เบลอ phone, email, นามสกุล, line_id ทุกที่
- square_preview 1080x1080 · qr_card = การ์ดนามบัตรมี QR ไปลิงก์พอร์ตของผู้ใช้ (ใช้ลิงก์ที่ผู้ใช้กรอก ไม่สร้าง hosting เอง)
- navigator.share({ files }) + fallback ดาวน์โหลด + ปุ่มคัดลอกแคปชัน:
  "เมื่อก่อนเรซูเม่หนูแบบนี้ 😭 ตอนนี้แบบนี้ ✨ ทำฟรีใน 1 นาที #AIวันละแอป #ResumeSnap"
```

---

## H) Brain dump ของจริง (LLM + OCR + เสียง)

```text
1) /app/api/ai/route.ts (server):
   - รับ { task: "extract" | "keywords" | "tailor" | "glowup" | "cover_letter" | "drill", payload }
   - ใช้ AI_API_KEY จาก env, ไม่ log เนื้อหาผู้ใช้, timeout 25s
   - system prompt จากส่วน M ตาม task, ขอ JSON ตาม schema, parse ด้วย zod, ไม่ผ่าน → retry 1 ครั้งพร้อม error
   - ผลทุกตัววิ่งผ่าน lib/grounding.ts ก่อนคืน
   - rate limit ง่ายๆ ต่อ IP 20 ครั้ง/ชม. (in-memory) กันโดนยิงตอนคลิปดัง

2) เสียง: hooks/useSpeech.ts ใช้ webkitSpeechRecognition lang "th-TH", continuous, interim results แสดงสด,
   จำกัด 120 วิ, ไม่รองรับ → ซ่อนปุ่ม → RawInput.source = "voice", voice_seconds

3) รูปเรซูเม่เก่า: รับรูป → ย่อ ≤1600px → ถ้ามี key ส่งเป็น vision ใน task "extract" (source photo_old_cv)
   ไม่มี key → Tesseract.js (tha+eng, lazy load, แสดง progress) → ข้อความ OCR ให้ผู้ใช้แก้ก่อนกด "จัดให้หน่อย"

4) วาง LINE chat / LinkedIn: ตัด timestamp และชื่อผู้ส่งแบบ LINE export ออกก่อนส่ง (regex บรรทัด "HH:MM\tชื่อ\t")

5) Generating screen: แบ่งข้อความ RawInput เป็นชิ้นตามบรรทัด ให้ลอยขึ้นและหมุนเล็กน้อย → พอผลมา ให้ชิ้นบินเข้าไปยัง
   section ที่ตรงกัน (map ด้วย source_quote) → กระดาษ A4 fade in ทีละ section 150ms
```

---

## I) Nice-to-have pack

```text
ทำทีละตัว เรียงตามลำดับ หยุดได้ทุกเมื่อ:

1) Cover Letter — ปุ่มในหน้า Match "เขียนอีเมลสมัครงาน" เลือกโทน formal / friendly_pro / short_email + ภาษา
   ใช้ข้อมูลจาก resume tailored เท่านั้น (runtime M4) ปุ่มคัดลอก subject / body แยกกัน — แอปไม่ส่งอีเมลเอง
2) Application Tracker — แท็บ "สมัครแล้ว" การ์ดคอลัมน์สถานะ (saved, applied, interview, offer, rejected, ghosted)
   เปลี่ยน applied → ตั้ง follow_up_on = +7 วัน แสดง badge "ถึงวันตามงาน" บน Home
3) Interview Drill — 4–8 คำถามจากประกาศ+เรซูเม่ (runtime M5) การ์ดทีละใบ แสดง why_asked_th + star_hint_th
   ผู้ใช้พิมพ์/พูดคำตอบ → feedback_th 2–3 ข้อ (โครง STAR ครบไหม มีตัวเลขไหม) ไม่ให้คะแนนตัวบุคคล
4) TH/EN toggle — แปลทั้งเรซูเม่เป็นอีกเวอร์ชัน (lang en) เก็บ parent_id, ชื่อเฉพาะไม่แปล
5) Version Compare — เลือก 2 เวอร์ชัน แสดง diff ระดับ bullet (เพิ่มเขียว / เปลี่ยนเหลือง / ลบแดง)
6) Photo Check — ตรวจด้วย canvas: ความสว่างเฉลี่ย, ความชัด (Laplacian variance), สัดส่วน, ความรกพื้นหลัง (edge density ขอบภาพ)
   คืน PhotoCheck · ห้ามมีข้อความเรื่องหน้าตา/รูปร่าง/อายุ เด็ดขาด
7) Dark mode
อัปเดต feature_checklist ทุกครั้งที่ทำเสร็จ
```

---

## J) Reel script / overlay

```text
จาก examples.json → reel_script_th สร้าง:
1) overlay text 7 ช็อต ภาษาไทย สั้นไม่เกิน 22 ตัวอักษรต่อบรรทัด ฟอนต์หนา ขอบดำ
2) คำพูดพากย์ 28 วิ (ประมาณ 70–80 คำ) โทนเพื่อนเล่าให้ฟัง
3) แคปชันโพสต์ 3 แบบ (สั้น/กลาง/ยาว) + แฮชแท็ก 6 ตัว
4) คอมเมนต์ปักหมุด: "พิมพ์ เรซูเม่ ใต้คลิปนี้ เดี๋ยวส่งลิงก์ให้ ✨ ข้อมูลอยู่ในเครื่องคุณ ไม่เก็บไปไหน"
5) ไอเดียตอนต่อ 3 ตอน (จาก alt_reel_ideas_th)
ห้ามสัญญาว่า "ได้งานแน่นอน" หรือ "ผ่าน ATS 100%" ใช้คำว่า "ตรงงานขึ้น" / "HR อ่านง่ายขึ้น"
```

---

## K) QA ก่อนถ่าย

```text
ตรวจ ResumeSnap ตาม checklist แล้วรายงานผ่าน/ไม่ผ่าน พร้อมแก้ทันที:
1) ลองข้อมูลตัวอย่าง → Editor ≤ 3 วิ หน้าเดียว (iPhone 13 mini 375px และ Pixel 7 412px)
2) ปัด 6 เทมเพลต ทุกแบบหน้าเดียว ไม่มีตัวหนังสือล้นกรอบ
3) วางประกาศ Kinjai → 63 · ปรับ → 87 · Meta Business Suite ไม่ถูกใส่เอง
4) glow-up b_02 ได้ 3 สไตล์ · glow-up activities ได้ [X] และบล็อก PDF
5) PDF จาก iOS Safari + Android Chrome: สระบน/ล่างไม่ลอย ไม่ตัดคำกลางพยางค์ ชื่อไฟล์ถูก
6) การ์ดแชร์เบลอเบอร์/อีเมล/นามสกุล
7) รีเฟรชแล้วข้อมูลอยู่ · ปุ่มลบทั้งหมดใช้ได้
8) ไม่มี key → ไม่มี error แดง ขึ้นโหมดตัวอย่าง
9) animation ลื่น 60fps ตอนอัดจอ (ปิด devtools) · เสียง ding ปิดได้
10) ทุกหน้ามี disclaimer ตามที่กำหนด
```

---

## L) แก้ปัญหาเร็ว (ใช้เมื่อพัง)

```text
แอป ResumeSnap มีปัญหา: <วางอาการ + error + หน้าจอ>
ข้อจำกัด: ห้ามเปลี่ยน schemas.json, ห้ามเปลี่ยนกติกา lib/score.ts (test 63/87 ต้องผ่าน), ห้ามเอา grounding guard ออก
ขอ: สาเหตุ 1–2 บรรทัด → patch เล็กที่สุด → วิธีทดสอบซ้ำ 3 ขั้น
ปัญหาที่เจอบ่อย:
- ฟอนต์ไทยใน PDF เพี้ยน → ใช้ @font-face ไฟล์ local + font-display: block + รอ document.fonts.ready ก่อน print
- html-to-image ไม่มีฟอนต์ → ใส่ fontEmbedCSS / preload ฟอนต์
- Web Speech ไม่ทำงานบน iOS PWA → ซ่อนปุ่มเมื่อเปิดแบบ standalone
- auto-fit วนไม่จบ → จำกัด 12 รอบ
```

---

## M) Runtime prompts (ที่แอปส่งให้ LLM)

### M1 — extract (Brain Dump → ResumeDoc)
```text
SYSTEM:
คุณคือผู้ช่วยจัดเรซูเม่สำหรับคนไทย หน้าที่คือ "จัดระเบียบ" ข้อมูลที่ผู้ใช้ให้มา ไม่ใช่แต่งเพิ่ม
ตอบเป็น JSON ตาม schema ExtractResult เท่านั้น (ไม่ต้องมีคำอธิบาย)

กฎ:
1. ทุก bullet ต้องมี source_quote = ข้อความต้นฉบับจาก INPUT ที่เป็นที่มา (คัดลอกตรงตัว)
2. ห้ามเพิ่มตัวเลข เครื่องมือ ทักษะ บริษัท ตำแหน่ง หรือวุฒิ ที่ไม่มีใน INPUT
3. ถ้าข้อมูลสำคัญขาด (email, phone, วันที่ทำงาน) ให้ใส่ใน missing_fields พร้อมคำถาม ask_th สั้นเป็นกันเอง
4. ห้ามอนุมานอายุ เพศ ศาสนา สถานภาพ · show_photo=false, show_age=false
5. แปลงวันที่เป็น YYYY-MM (ค.ศ.) ถ้าผู้ใช้เขียน พ.ศ. ให้ลบ 543 · "ถึงตอนนี้" = "present"
6. bullet ขึ้นต้นด้วยคำกริยา สั้น ≤ 110 ตัวอักษร has_metric=true ถ้ามีตัวเลขจาก INPUT
7. summary 1–2 ประโยค ใช้เฉพาะข้อเท็จจริงจาก INPUT
8. lang = {{lang}} · template_id = "clean_blue" · accent_color = "#2563EB"
9. ถ้า INPUT ไม่ใช่ข้อมูลเรซูเม่ ให้คืน confidence < 0.3 และ warnings อธิบาย

USER:
INPUT ({{source}}):
"""{{raw_text}}"""
TODAY: {{today}} (Asia/Bangkok)
```

### M2 — keywords + tailor
```text
SYSTEM:
อ่านประกาศงาน แล้วทำ 2 อย่าง ตอบ JSON { "keywords": JobKeyword[], "suggestions": TailorSuggestion[] }

keywords: 8–20 คำ ใช้คำ "ตามที่ประกาศเขียน" (ภาษาเดียวกับประกาศ) weight 3 = ต้องมี, 2 = สำคัญ, 1 = พิจารณาพิเศษ
aliases ใส่ได้เฉพาะการสะกดต่าง/คำย่อ ห้ามใส่คำแปล

suggestions: เทียบกับ RESUME และ RAW (ข้อมูลดิบของผู้ใช้)
- grounded=true เฉพาะเมื่อสิ่งที่เสนอเป็นการ "เรียกเรื่องที่ทำจริงด้วยคำของประกาศ" และหาที่มาได้ใน RAW หรือ RESUME
- ถ้าประกาศต้องการสิ่งที่ไม่พบเลย → kind "add_missing_info_ask", grounded=false, after = คำถามถามผู้ใช้
- ห้ามเพิ่มตัวเลขใหม่ ถ้าจำเป็นใช้ [X]
- reason_th อธิบายแบบเพื่อนบอก 1 ประโยค
- สูงสุด 8 ข้อ เรียงตามผลต่อคะแนน

USER:
JOB: """{{job_text}}"""
RESUME: {{resume_json}}
RAW: """{{raw_text}}"""
```

### M3 — glowup
```text
SYSTEM:
เขียน bullet ใหม่ 3 สไตล์ ตอบ JSON BulletGlowup
- impact: กริยาแรง + สิ่งที่ทำ + ผลลัพธ์ (ถ้ามีตัวเลขใน SOURCE)
- concise: ≤ 60 ตัวอักษร
- formal: ภาษาอังกฤษแบบเรซูเม่ (past tense ถ้าจบแล้ว, present ถ้า end = present)
ห้ามเพิ่มตัวเลขหรือข้อเท็จจริงที่ไม่มีใน SOURCE ถ้าผลลัพธ์จะดีขึ้นด้วยตัวเลข ให้ใส่ [X] และ needs_user_number=true
ถ้ามีประกาศงาน ให้ใช้คำของประกาศเมื่อมีความหมายตรงกับสิ่งที่ทำจริง

USER:
BULLET: "{{text}}" · ROLE: {{role}} @ {{org}} · END: {{end}}
SOURCE: """{{source_quote_or_raw}}"""
JOB_KEYWORDS: {{keywords}}
```

### M4 — cover letter
```text
SYSTEM:
เขียนอีเมลสมัครงานจากเรซูเม่ที่ให้เท่านั้น ตอบ JSON CoverLetter
tone: {{tone}} · lang: {{lang}} · ความยาว short_email ≤ 120 คำ, อื่นๆ ≤ 250 คำ
โครง: ทักทาย → ตำแหน่งที่สมัคร → 1–2 ผลงานที่ตรงประกาศที่สุด (มีตัวเลขถ้ามี) → ทำไมอยากร่วมงาน (จากข้อมูลบริษัทในประกาศเท่านั้น) → ปิด
ห้ามแต่งข้อมูลบริษัทหรือผลงาน ห้ามใช้คำเว่อร์ ("มุ่งมั่นอย่างยิ่งยวด")
USER: RESUME {{resume_json}} · JOB {{job_text}}
```

### M5 — interview drill
```text
SYSTEM:
สร้างคำถามสัมภาษณ์ 4–8 ข้อ ตอบ JSON InterviewDrill
ผสม: 2 ข้อจากผลงานในเรซูเม่ · 2 ข้อจากงานหลักในประกาศ · 1 ข้อพฤติกรรม (ทีม/ปัญหา) · 1 ข้อภาษาอังกฤษถ้าประกาศขอ
ทุกข้อมี why_asked_th (HR อยากรู้อะไร) และ star_hint_th (ใช้ item ไหนในเรซูเม่เล่า) + linked_item_id ถ้ามี
ห้ามถามเรื่องส่วนตัวที่เลือกปฏิบัติ (อายุ แต่งงาน ศาสนา ตั้งครรภ์)
USER: RESUME {{resume_json}} · JOB {{job_text}}
```
