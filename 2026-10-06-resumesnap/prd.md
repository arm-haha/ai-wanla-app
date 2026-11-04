# ResumeSnap — PRD (AI วันละแอป · Day 7/10)

**วันที่:** 2026-10-06 (Asia/Bangkok) · **ช่อง:** AI วันละแอป · **สถานะ:** พร้อม gen วันนี้
**เอกสารคู่กัน:** `prompts.md`, `schemas.json`, `examples.json`, `README.md`

---

## 1) สรุปหนึ่งบรรทัด
เทโน้ตมั่วๆ (พิมพ์ / พูด / ถ่ายรูปเรซูเม่เก่า) → ได้เรซูเม่ A4 สวยพร้อมส่งใน 1 นาที → วางประกาศงาน → เห็นคะแนนเข้ากันพุ่ง 63 → 87 → ส่งออก PDF + จดหมายสมัครงาน

**ฮุค Reel:** "เรซูเม่หนูแบบนี้ HR ไม่ตอบ… วางโน้ตมั่วๆ 3 วิ ได้เรซูเม่ระดับ HR ทักกลับ 📄"

## 2) ปัญหา
- เด็กจบใหม่ / คนเปลี่ยนงาน / พนักงานหน้าร้านที่อยากขยับ ไม่รู้จะเริ่มเขียนเรซูเม่ยังไง เปิด Word แล้วค้าง
- เรซูเม่เดิมหน้าตาเชย (ฟอนต์ Angsana, ตาราง, 3 หน้า) และใช้ฉบับเดียวส่งทุกงาน
- ไม่รู้ว่าประกาศงานใช้คำไหน → เขียนเรื่องที่ทำจริงด้วยคำอื่น → HR/ระบบค้นหาไม่เจอ
- เขียนแบบ "ช่วยทำ…" ไม่มีตัวเลข อ่านแล้วไม่เห็นผลงาน

## 3) ทำไมไวรัลบน Reels
- **ทุกคนเคยหรือกำลังหางาน** — กลุ่มคนดูกว้างมาก ทั้งนักศึกษาปีสุดท้าย คนเพิ่งจบ คนอยากลาออก
- **Before/after ชัดในเฟรมเดียว:** โน้ตยาวเหยียดใน LINE → A4 ฟ้าสวย, เลขคะแนน 63 → 87 วิ่ง = ภาพที่คนหยุดดู
- **กดเซฟสูง:** "เดี๋ยวใช้ตอนสมัครงาน" คือเหตุผลเซฟคลาสสิก + แท็กเพื่อนที่กำลังหางาน
- **ตรงเทศกาล:** ต.ค.–มี.ค. ช่วงนักศึกษาหาที่ฝึกงานและเตรียมจบ
- CTA "คอมเมนต์ เรซูเม่" ทำง่าย ไม่เขิน

## 4) เป้าหมาย / ไม่ใช่เป้าหมาย
**เป้าหมาย**
- ผู้ใช้ใหม่ได้เรซูเม่ 1 หน้าที่ดูดีภายใน ≤ 90 วินาทีจากเปิดแอป
- ทำเดโมทั้งคลิปจบใน 28 วินาที ด้วยข้อมูลตัวอย่าง "มายด์" แบบเล่นซ้ำได้เหมือนเดิมทุกเทค
- **AI ห้ามแต่งเรื่อง:** ทุก bullet ต้องย้อนไปเจอในข้อมูลที่ผู้ใช้ให้ (`source_quote`) ตัวเลขที่ไม่มีจะเป็น `[X]` ให้ผู้ใช้กรอก
- ข้อมูลอยู่ในเครื่อง ไม่มีบัญชี ไม่มี backend (ยกเว้นเรียก LLM ถ้าเปิด)

**ไม่ใช่เป้าหมาย**
- ไม่สมัครงานแทนผู้ใช้ / ไม่ส่งอีเมลเอง / ไม่ดึงประกาศจากเว็บหางานอัตโนมัติ
- ไม่อ้างว่าเป็น "คะแนน ATS จริง" — เป็นคะแนนประมาณแบบ deterministic
- ไม่ประเมินหน้าตา อายุ เพศ จากรูป
- ไม่ทำระบบชำระเงิน / เทมเพลตพรีเมียม

## 5) ผู้ใช้หลัก
| Persona | สถานการณ์ | สิ่งที่อยากได้ |
|---|---|---|
| **มายด์** (เดโม) 22 ปี จบนิเทศฯ | ฝึกงาน + ฟรีแลนซ์ TikTok ร้านกาแฟ จะสมัคร Junior Content Marketing | เรซูเม่สวย + ตรงงาน + ไม่ต้องเขียนเอง |
| **ต้น** 29 ปี พนักงานร้านมือถือ | อยากย้ายไปงานเซลส์บริษัท มีแต่ประสบการณ์หน้าร้าน | แปลงงานหน้าร้านเป็นภาษาที่ HR ฟังแล้วได้ |
| **พี่นก** 41 ปี กลับเข้าทำงาน | เรซูเม่ล่าสุดปี 2016 เป็นไฟล์ Word | ถ่ายรูปเรซูเม่เก่าแล้วได้ฉบับใหม่ทันที |

## 6) User stories
1. ในฐานะเด็กจบใหม่ ฉันอยากพิมพ์เล่าเรื่องตัวเองแบบไม่ต้องเรียบร้อย แล้วได้เรซูเม่จัดหัวข้อครบ
2. ฉันอยากถ่ายรูปเรซูเม่เก่า (กระดาษ/จอ) แล้วได้ข้อมูลเข้าแอปโดยไม่ต้องพิมพ์ใหม่
3. ฉันอยากปัดดูหลายแบบแล้วเลือกแบบที่ชอบ โดยข้อมูลไม่หาย
4. ฉันอยากวางประกาศงาน แล้วรู้ว่าขาดคำไหน และกดให้แอปปรับให้ตรง โดยไม่ใส่เรื่องที่ฉันไม่ได้ทำ
5. ฉันอยากแตะประโยคธรรมดาแล้วได้ 3 เวอร์ชันที่ฟังดูมืออาชีพ
6. ฉันอยากได้ PDF A4 หน้าเดียวชื่อไฟล์ถูกต้อง และการ์ดก่อน/หลังที่ปิดเบอร์โทรให้แล้วไว้อวดเพื่อน
7. (retention) ฉันอยากเก็บหลายเวอร์ชันตามงาน และดูว่างานไหนสมัครแล้ว ต้องตามเมื่อไร
8. (retention) ฉันอยากได้อีเมลสมัครงาน และซ้อมคำถามสัมภาษณ์จากเรซูเม่ของฉันเอง

## 7) ฟีเจอร์ (≥5 บังคับ)
### Must-have (core demo)
| # | ฟีเจอร์ | รายละเอียด | Wow |
|---|---|---|---|
| 1 | **Brain Dump → Resume** ⭐ | พิมพ์ / พูด (Web Speech API, ≤ 120 วิ) / ถ่ายรูปเรซูเม่เก่า (OCR ผ่าน LLM vision หรือ Tesseract.js) → `ExtractResult` → หน้า A4 ประกอบตัวทีละ section + ชิปถามข้อมูลที่ขาด | **ใช่ — ช็อตหลัก** ข้อความลอยแตกเป็นหัวข้อ ประกอบเป็นกระดาษ |
| 2 | **Template Flip** | 6 เทมเพลต (`template_catalog`) ปัดซ้าย-ขวา ข้อมูลชุดเดียว + สีหลัก 6 สี + ป้าย "ATS ปลอดภัย" + auto-fit 1 หน้า (ลดระยะห่าง/ฟอนต์ทีละขั้น) | ปัดเร็วๆ 4 แบบในคลิป |
| 3 | **Job Match Tailor** ⭐ | วางประกาศงาน → ดึง keyword (LLM หรือ mock) → คะแนน 0–100 จาก `lib/score.ts` (§8) → การ์ดคำแนะนำ grounded = กดใช้ได้, ungrounded = เป็นคำถาม → สร้างสำเนา tailored (`parent_id`) → คะแนนวิ่งขึ้น | **ใช่ — ช็อตที่สอง** คีย์เวิร์ดไฮไลต์เหลือง + 63 → 87 |
| 4 | **Bullet Glow-up** | แตะ ✨ ที่ bullet ใดก็ได้ → 3 สไตล์ (impact / concise / formal-EN) → ไม่มีตัวเลขในข้อมูลจริง = ใส่ `[X]` + `needs_confirm` | ประโยคธรรมดากลายเป็นประโยคมีตัวเลข |
| 5 | **Export & Share** | PDF A4/Letter (print CSS หรือ @react-pdf), PNG, TXT แบบ ATS · ชื่อไฟล์ `ชื่อ_นามสกุล_ตำแหน่ง.pdf` · การ์ดแชร์ story ก่อน/หลัง เบลอข้อมูลส่วนตัวโดยค่าเริ่ม · บล็อกส่งออกถ้ายังมี `[X]` | ไฟล์ PDF จริงโผล่บนจอ |

### Nice-to-have (retention — ทำถ้าเหลือเวลา)
- **Cover Letter / อีเมลสมัครงาน** 3 โทน (`cover_letter_example`) — คัดลอกไปวางในอีเมลเอง
- **Interview Drill** 4–8 คำถามจากประกาศ + บอกว่าใช้ข้อไหนในเรซูเม่เล่าแบบ STAR + พิมพ์คำตอบแล้วรับฟีดแบ็ก
- **Application Tracker** saved / applied / interview / offer / rejected / ghosted + วันตามงาน (+7 วัน)
- **Photo Check** เช็กเชิงเทคนิค (แสง ครอป พื้นหลัง ความชัด สัดส่วน) — ห้ามพูดถึงหน้าตา
- **TH/EN toggle** แปลทั้งเรซูเม่ เก็บเป็นอีกเวอร์ชัน
- **Version Compare** เทียบฐานหลักกับฉบับ tailored แบบไฮไลต์ diff
- Dark mode

> เหตุผลกลับมาเปิด: สมัครงานใหม่ทุกครั้ง → วางประกาศใหม่ → ได้เวอร์ชันใหม่ + ตามสถานะใน Tracker

## 8) กติกาคะแนน (`lib/score.ts` — pure, deterministic)
คะแนนรวม = keywords (≤60) + structure (≤15) + impact (≤15) + length (≤10)
- **keywords** = `floor(60 × Σweight ที่เจอ / Σweight ทั้งหมด)` ค้นแบบ case-insensitive substring ใน headline, summary, role, bullets, skills, languages(+test), activities, education
- **aliases** ใส่ได้เฉพาะการสะกดต่าง/คำย่อ ห้ามใส่คำแปลไทย — จุดขายคือ "ใช้คำเดียวกับประกาศ"
- **structure:** email+phone (+5) · summary ไม่ว่าง (+4) · ทุก experience มี start/end (+3) · skills อยู่ใน 3 section แรก (+3)
- **impact** = `floor(15 × bullet ที่ has_metric และไม่ needs_confirm / bullet ทั้งหมดใน experience+projects)`
- **length:** หน้าเดียว (+8) · ทุก bullet ≤ 110 ตัวอักษร (+2)
- ป้าย: 0–49 ยังห่าง · 50–69 พอใช้ · 70–84 ดี · 85–100 เข้าทางมาก
- **ตรวจแล้ว:** ข้อมูลเดโมได้ 31+12+10+10 = **63** ก่อน และ 52+15+10+10 = **87** หลัง (ตรงกับ `match_before_example` / `match_after_example`)
- UI ต้องแสดง「คะแนนประมาณจากคีย์เวิร์ดและโครงสร้าง ไม่ใช่คะแนนจากระบบ HR จริง」

## 9) Extract / Tailor / Glow-up engine
- `lib/extract.ts` interface เดียว 2 engine: `mock_demo` (คืน `extract_result_example` หลังหน่วง 2.4 วิ ทำให้คลิปเหมือนเดิมทุกเทค) และ `llm_api` (เรียกผ่าน route `/api/ai` ที่ซ่อน key, structured output ตาม `ExtractResult`)
- **Grounding guard (บังคับ):** ทุก bullet ที่ AI สร้างต้องมี `source_quote` ที่เป็น substring (หลัง normalize ช่องว่าง) ของ RawInput ถ้าไม่เจอ → `needs_confirm: true` + ชิปเหลือง「ยืนยันว่าเป็นเรื่องจริง」
- ตัวเลขใน bullet ที่ไม่มีใน RawInput → แทนด้วย `[X]` อัตโนมัติ (regex ตัวเลขเทียบกับชุดตัวเลขใน RawInput)
- Tailor ห้ามเพิ่ม skill/เครื่องมือที่ไม่เจอในข้อมูล → ต้องเป็น `add_missing_info_ask` (`grounded:false`) เท่านั้น
- ไม่อนุมานอายุ เพศ ศาสนา สถานภาพ จากชื่อหรือรูป · `show_photo`/`show_age` ค่าเริ่ม false

## 10) หน้าจอ
1. **Home** — หัวข้อ "เรซูเม่สวยใน 1 นาที" + 3 ปุ่มใหญ่ (โน้ต / ถ่ายรูป / พูด) + ลองข้อมูลตัวอย่าง + รายการเรซูเม่ที่มี
2. **Brain Dump** — textarea ใหญ่ + ปุ่มไมค์ + แนบรูป + ปุ่ม "จัดให้หน่อย ✨"
3. **Generating** — ข้อความลอยแตกเป็นหัวข้อ + 4 ข้อความสถานะ (`ui_copy_th.generating`)
4. **Resume Editor** — พรีวิว A4 ย่อพอดีจอ + carousel เทมเพลต + แตะ section เพื่อแก้ + ชิปข้อมูลที่ขาด + ปุ่ม ✨ ต่อ bullet
5. **Job Match** — วางประกาศ → วงคะแนน + breakdown 4 แท่ง + คีย์เวิร์ดเจอ/ขาด + การ์ดคำแนะนำ
6. **Tailored Compare** — ก่อน/หลังแบบเลื่อน + คะแนนวิ่ง
7. **Export / Share** — PDF / PNG / TXT + การ์ดแชร์ 3 แบบ
8. **Extras** — Cover Letter, Interview Drill, Tracker (แท็บ "สมัครแล้ว"), Settings
Bottom nav: เรซูเม่ | จับคู่งาน | สมัครแล้ว | ตั้งค่า

## 11) Core flows
**A. Happy path (ถ่าย Reel):** Home → ลองข้อมูลตัวอย่าง → Generating 2.4 วิ → Editor (clean_blue) → ปัด 3 แบบ → กลับ clean_blue → จับคู่งาน → วางประกาศ Kinjai → 63 → "ปรับให้ตรงงานนี้" → 87 → ✨ ที่ b_02 → เลือก impact → Export PDF → แชร์การ์ด
**B. ถ่ายรูปเรซูเม่เก่า:** กล้อง → ครอป → OCR → RawInput(source: photo_old_cv) → flow เดียวกับ A
**C. ยังมี [X]:** Export → แผ่นล่าง "เหลือ 1 จุดที่ต้องยืนยัน" → แตะ → กรอกเลขหรือลบประโยค → Export ได้
**D. Ungrounded suggestion:** การ์ด "เคยใช้ Meta Business Suite ไหม?" → ใช่ (เพิ่มใน skills, origin user) / ไม่เคย (ซ่อน)

## 12) UI / แบรนด์
- พื้น `#F5F8FF` · กระดาษ `#FFFFFF` · ฟ้าหลัก `#2563EB` · หมึกกรม `#0F172A` · ไฮไลต์ `#FDE047` · คะแนนดี `#22C55E` · คะแนนกลาง `#F97316` · ขอบ `#E2E8F0`
- ฟอนต์: UI = IBM Plex Sans Thai · เรซูเม่ = Sarabun / IBM Plex Sans Thai / Inter (EN)
- ภาพจำ: **คีย์เวิร์ดถูกปากกาเน้นข้อความสีเหลืองปาด** ตอน tailor (animation clip-path ซ้าย→ขวา 0.4 วิ)
- วงคะแนน gauge นับเลขขึ้นแบบ spring + สีเปลี่ยน ส้ม→เขียว
- ปุ่ม ≥ 48px · มือถือ 390px ฐาน · พรีวิว A4 สเกลด้วย CSS transform

## 13) Tech
- Next.js 14 App Router + TypeScript + Tailwind + shadcn/ui + framer-motion
- `lib/extract.ts`, `lib/score.ts`, `lib/tailor.ts`, `lib/glowup.ts`, `lib/grounding.ts`, `lib/fit.ts` (auto-fit หน้าเดียว), `lib/export.ts`, `lib/share.ts`, `lib/storage.ts`
- LLM optional ผ่าน `/api/ai` (env `AI_API_KEY`) — ไม่มี key = `mock_demo`
- OCR: LLM vision ถ้ามี key, ไม่มีก็ Tesseract.js (`tha+eng`, lazy load)
- เสียง: Web Speech API `th-TH` (fallback: ซ่อนปุ่มถ้า browser ไม่รองรับ)
- PDF: หน้า `/print/[id]` + `window.print()` กับ `@page { size: A4; margin: 0 }` (เร็วสุด ฟอนต์ไทยถูก) หรือ @react-pdf ถ้าต้องการไฟล์ตรง
- Share card: html-to-image 1080×1920 + `navigator.share` files + fallback ดาวน์โหลด
- เก็บ localStorage (`resumesnap:v1`) + IndexedDB สำหรับรูป · Deploy Vercel + PWA

## 14) ข้อมูล (สรุป — เต็มใน `schemas.json`)
RawInput · Contact · Bullet · ExperienceItem · ProjectItem · EducationItem · SkillGroup · LanguageSkill · Certification · ResumeDoc · ExtractResult · JobKeyword · JobPost · TailorSuggestion · MatchResult · BulletGlowup · CoverLetter · InterviewDrill · ExportJob · ShareCard · ApplicationEntry · PhotoCheck · Settings · LocalStore · AnalyticsEvent · FeatureChecklist
`examples.json` ผ่าน schema 0 error (ตรวจตาม `_meta.schema_map`)

## 15) Analytics (local / console)
`demo_loaded, dump_submitted, resume_generated, template_flipped, lang_toggled, job_pasted, match_scored, suggestion_applied, bullet_glowup, placeholder_filled, export_pdf, share_card, cover_letter_generated, drill_started, application_status_changed`

## 16) Acceptance criteria
- [ ] Must-have 5 ข้อทำงานครบ และติ๊ก `feature_checklist_example`
- [ ] ข้อมูลตัวอย่าง → Editor ≤ 3 วิ ได้หน้า A4 เดียว
- [ ] ปัด 6 เทมเพลตไม่กระตุก ข้อมูลไม่หาย ทุกแบบพอดี 1 หน้า
- [ ] วางประกาศ Kinjai ได้ **63** → กดปรับ → **87** ตรงตามตัวอย่าง (unit test `lib/score.ts`)
- [ ] ข้อเสนอ ungrounded ไม่ถูกใส่เองเด็ดขาด
- [ ] bullet ที่มี `[X]` บล็อกการส่งออก PDF จนกว่าจะแก้
- [ ] PDF ฟอนต์ไทยไม่แตก สระไม่ลอย ทั้ง iOS Safari + Android Chrome
- [ ] การ์ดแชร์เบลอเบอร์โทร/อีเมล/นามสกุลโดยค่าเริ่ม
- [ ] รีเฟรชแล้วข้อมูลยังอยู่ · ปุ่ม "ลบข้อมูลทั้งหมด" ใช้ได้
- [ ] มี disclaimer「AI ช่วยเรียบเรียง — ตรวจทุกข้อให้เป็นความจริงก่อนส่ง」

## 17) ความเสี่ยง / กับดัก
| ความเสี่ยง | ป้องกัน |
|---|---|
| **AI แต่งประสบการณ์/ตัวเลข** → ผู้ใช้โดนจับได้ตอนสัมภาษณ์ และช่องเสียเครดิต | grounding guard + `[X]` + ungrounded = คำถาม + บล็อก export |
| คะแนนถูกเข้าใจว่าเป็น ATS จริง | ใช้คำว่า "คะแนนประมาณ" + disclaimer ใต้ gauge ห้ามพูดในคลิปว่า "ผ่าน ATS แน่นอน" |
| ข้อมูลส่วนตัวหลุด (เบอร์ อีเมล ที่อยู่) ในคลิป/การ์ด | ใช้ตัวละครสมมติ + เบอร์ปิดบางส่วน + เบลอค่าเริ่มบนการ์ด |
| PDF ไทยเพี้ยน (สระลอย ตัดคำผิด) | ใช้ print CSS + ฟอนต์ฝัง + `word-break: keep-all` ทดสอบจริงก่อนถ่าย |
| Auto-fit ทำฟอนต์เล็กจนอ่านไม่ออก | ขั้นต่ำ 9.5pt — ถ้ายังล้น แนะนำตัด bullet แทน |
| รูป/อายุ/เพศในเรซูเม่ไทย → อคติ | เป็นตัวเลือกของผู้ใช้ ค่าเริ่มปิด ไม่มี AI ประเมินหน้าตา |
| OCR รูปเรซูเม่เก่าพลาด | แสดงข้อความ OCR ให้แก้ก่อนกด "จัดให้หน่อย" |
| คลิปยาวเกินเพราะโชว์ทุกอย่าง | คลิปหลักโชว์ 4 ฟีเจอร์ ที่เหลือเก็บไปตอนต่อ |

## 18) Reel shot list (สรุป — เต็มใน `examples.json → reel_script_th`)
0–3 วิ โน้ตมั่ว + เรซูเม่ยับ "HR ไม่ตอบเลย" → 3–7 วาง → ประกอบเป็น A4 → 7–11 ปัดเทมเพลต → 11–17 วางประกาศ 63 → 87 ไฮไลต์เหลือง → 17–21 ✨ glow-up → 21–25 PDF + อีเมลสมัคร → 25–28 CTA "คอมเมนต์ เรซูเม่"
**Build montage (ตอนต่อ/ต้นคลิปยาว):** วาง Master prompt → โค้ดวิ่ง → แอปขึ้นบนมือถือ (เร่ง 8x, 4 วิ)

## 19) Out of scope (ภายหลัง)
ดึงประกาศจาก URL อัตโนมัติ · LinkedIn import แบบ OAuth · เทมเพลตตามแบรนด์บริษัท · AI mock interview ด้วยเสียง · ระบบแชร์ลิงก์เรซูเม่ออนไลน์ (QR) ที่ต้องมี backend

## 20) แผนวันเดียว
| เวลา | งาน | Prompt |
|---|---|---|
| 0:00–0:45 | Scaffold + types + ข้อมูลตัวอย่าง + storage | A, B, C |
| 0:45–2:00 | เทมเพลต 6 แบบ + auto-fit + Editor | F |
| 2:00–3:00 | `lib/score.ts` + tests + Job Match UI + tailor (mock) | D |
| 3:00–3:45 | Glow-up + grounding guard + `[X]` | E |
| 3:45–4:45 | Export PDF + share card | G |
| 4:45–5:30 | Brain dump จริง (LLM) + OCR + เสียง | H |
| 5:30–6:30 | Nice-to-have 1–2 ตัว (Cover Letter, Tracker) | I |
| 6:30–7:30 | QA + polish animation + ถ่าย Reel | J, K, L |
