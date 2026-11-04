# VoiceMood — Prompt สั่งงาน (จัดเต็ม)

ใช้กับ AI codegen (Cursor / Claude / GPT) สร้างแอปทั้งก้อน + prompt ที่ใช้ "ข้างในแอป" ตอนเรียก LLM จริง

**วันที่แพ็ก:** 2026-10-07 (Asia/Bangkok) · Day 8/10 · AI วันละแอป
**เอกสารคู่กัน:** `prd.md`, `schemas.json`, `examples.json`

| ส่วน | ใช้ทำอะไร |
|---|---|
| A | Master prompt สร้างทั้งแอป |
| B | ข้อมูลตัวอย่าง "น้ำหวาน" (15 entries, 24 ก.ย.–7 ต.ค.) |
| C | TypeScript types + zod |
| D | `lib/mood.ts` lexicon engine (หัวใจคลิป 25 → 75) |
| E | `lib/safety.ts` + Support Sheet (ทำก่อน UI) |
| F | Record + waveform + STT + ลูกแก้ว Aura + Result |
| G | Comfort Card + Breathe + Re-check |
| H | Mood Garden + Mood Triggers |
| I | Share Aura Card |
| J | Nice-to-have pack |
| K | QA ก่อนถ่าย |
| L | แก้ปัญหาเร็ว |
| M | Runtime prompts (ที่แอปส่งให้ LLM) |
| N | Reel overlay / แคปชัน |

---

## A) Master prompt สร้างทั้งแอป (วางครั้งเดียว)

```text
สร้างเว็บแอปมือถือเป็นหลักชื่อ VoiceMood (UI ภาษาไทยก่อน) — สมุดบันทึกอารมณ์ด้วยเสียง

วันที่ส่งมอบคอนเทนต์: 2026-10-07 สำหรับช่อง "AI วันละแอป"
เป้าหมายผู้ใช้: กดค้างพูดระบายเรื่องวันนี้ ~30 วิ → คำลอยเข้าลูกแก้ว → ลูกแก้วกลายเป็น "สีใจ" + คะแนน 0–100
+ อากาศใจ (☀️⛅☁️🌧️⛈️) → การ์ดปลอบใจ + หายใจ 60 วิ → เช็กใจอีกรอบเห็นก่อน/หลัง → สวนอารมณ์รายเดือน
→ แพทเทิร์นว่าอะไรชาร์จ/ดูดพลัง → แชร์การ์ด aura (ไม่ใส่ข้อความที่พูด)

สแต็กบังคับ:
- Next.js 14 App Router + TypeScript + Tailwind CSS + shadcn/ui + framer-motion · PWA · Deploy Vercel · ไม่มี auth ไม่มี DB
- lib/mood.ts pure deterministic (vitest) ตามกติกา prd.md §8 และ lexicon ใน examples.json → lexicon_th
- lib/safety.ts ตรวจ safety_terms_th ก่อนวิเคราะห์ทุกครั้ง (prd.md §9)
- lib/comfort.ts มี 2 engine: "template_v1" (ค่าเริ่ม) และ "llm_api" (route /api/ai ฝั่ง server, env AI_API_KEY)
- lib/stt.ts: Web Speech API (webkitSpeechRecognition, lang th-TH, interimResults, continuous) → fallback MediaRecorder
  + /api/ai/transcribe (ถ้ามี key) → fallback โหมดพิมพ์
- lib/triggers.ts, lib/garden.ts, lib/wrapped.ts pure functions
- lib/storage.ts: IndexedDB (idb) stores entries / breaths / capsules + localStorage "voicemood:v1" ตาม LocalStore
- lib/share.ts: การ์ด 1080x1920 ด้วย html-to-image + navigator.share files + fallback ดาวน์โหลด

ต้องมีอย่างน้อย 5 ฟีเจอร์ must-have:
1) Voice Vent → Mood Aura — ปุ่มไมค์ใหญ่ 96px กดค้าง (pointer events, รองรับแตะสลับเปิด/ปิดด้วย) + วงคลื่นจาก AnalyserNode
   รอบลูกแก้ว + คำ interim ลอยขึ้น → ปล่อย → คำถูกดูดเข้าลูกแก้ว (framer-motion layout) → ลูกแก้วไล่สีเป็น aura
   + score นับขึ้น + อากาศใจ + label + chip ธีม + summary · ปุ่ม "ดูว่าคำไหนทำให้เป็นสีนี้" (ไฮไลต์คำใน transcript, แตะลบคำได้)
2) Comfort Card + Breathe + Re-check — การ์ด validate / reframe / tiny action → Breathe 4-4-6 × 4 รอบ ลูกแก้วพอง/ยุบ
   + navigator.vibrate → ปุ่ม "เช็กใจอีกรอบ" อัด 10 วิ → แผงก่อน/หลัง (Recheck)
3) Mood Garden — ปฏิทินเดือน เริ่มวันจันทร์ ลูกแก้วสีต่อวัน + สตรีค + แตะดูรายการวันนั้น
4) Mood Triggers — การ์ด lifts/drains + กราฟแท่งบวกลบ · ถ้าข้อมูลไม่พอแสดง "เล่าอีก {n} วัน"
5) Share Aura Card — variant aura_story (ค่าเริ่ม) + garden_square · show_transcript ค่าเริ่ม false

ปุ่ม「ลองข้อมูลตัวอย่าง (น้ำหวาน)」โหลด examples.json → history_entries 14 entries แรกเข้า IndexedDB
แล้วเปิด Result ของ entry vm_014 (25 🌧️) ให้ทันที · Re-check ในโหมดเดโมใช้ข้อความ recheck_example (75 ⛅)
ผลต้องเหมือนเดิมทุกครั้ง

Nice-to-have: Mood Wrapped, ขอบคุณ 3 อย่าง, Time Capsule, เตือน 21:30, PIN lock, Duo Compare, ส่งออก .txt / ลบทั้งหมด

หน้าจอ: Home/Record, Listening, Result, Comfort, Breathe, Re-check, Garden, Patterns, Share, Support Sheet, Settings
bottom nav: เล่า | สวนอารมณ์ | แพทเทิร์น | ตั้งค่า

UX บังคับ:
- มือถือ 390px ฐาน · ปุ่ม ≥ 48px · ธีมกลางคืน: พื้น #14112B การ์ด #221E3F ขอบ #3B3566 ตัวอักษร #F5F3FF รอง #A5A1C8
- aura: bright #FACC15 / calm #34D399 / tense #FB7185 / low #818CF8 / neutral #C4B5FD (secondary ตาม mood_rules.quadrant_palette)
- ฟอนต์ IBM Plex Sans Thai · ตัวเลข Inter tabular
- ห้ามแฟลชเร็ว · respect prefers-reduced-motion · เสียง chime ปิดได้
- ข้อความ UI ตาม examples.json → ui_copy_th
- ใต้คะแนน: 「คะแนนจากคำที่คุณเล่าเอง ไม่ใช่การวัดทางการแพทย์」
- ป้าย Home: 「เก็บในเครื่องคุณเท่านั้น · ไม่เก็บไฟล์เสียง」

กฎความปลอดภัย (ห้ามละเมิด):
- safety ก่อนทุกอย่าง: เจอคำเสี่ยง → ไม่คำนวณคะแนน ไม่โชว์อากาศ ไม่ให้แชร์ → Support Sheet (1323, 1669)
- ห้ามใช้คำวินิจฉัย (ซึมเศร้า, โรควิตก) ห้ามบอกว่ารักษา/แทนผู้เชี่ยวชาญ
- ไม่ส่งข้อความออกนอกเครื่อง ยกเว้นผู้ใช้เปิด llm_api เอง · ไม่เก็บเสียงถ้า keep_audio = false

คุณภาพโค้ด:
- components/, components/aura/Orb.tsx, hooks/useRecorder.ts, hooks/useSpeech.ts, lib/*.ts, types/voicemood.ts ตรง schemas.json
- unit tests: mood.test.ts (15 entries + negation + ไม่เจอคำ), safety.test.ts, triggers.test.ts, garden.test.ts
- README ไทย: วิธีรัน, ใส่ AI_API_KEY, browser ที่รองรับไมค์ภาษาไทย, วิธีถ่าย Reel
- เริ่มจาก npm run dev ผ่าน + happy path ด้วยเดโมก่อน แล้วค่อยต่อไมค์จริง / LLM

เมื่อจบสรุปว่า must 5 ตัวอยู่ไฟล์ไหน + วิธีโหลดข้อมูลตัวอย่าง 1 ย่อหน้า
```

---

## B) ข้อมูลตัวอย่าง "น้ำหวาน"

```text
สร้าง /public/demo/namwan.json จาก examples.json ให้มี:
- demo_persona, lexicon_th, mood_rules
- history_entries (15 รายการ vm_001–vm_015) — ใช้ transcript ตามตัวอย่างทุกตัวอักษร
- voice_input_example, analysis_example, comfort_card_example, breath_session_example, recheck_example
- garden_example, trigger_insights_example, mood_wrapped_example, share_card_example

lib/demo.ts:
- loadDemo(): ลบข้อมูลเดิม (ถามยืนยันถ้ามีข้อมูลจริง) → ใส่ vm_001–vm_014 → เปิด Result ของ vm_014
- Re-check ในโหมดเดโม: เล่นข้อความ vm_015 แบบพิมพ์ทีละคำ 9 วิ (ดูเหมือนพูดจริงในคลิป) แล้วบันทึก vm_015
- "Listening" เดโม: แสดง interim_chunks ทีละก้อนห่าง 1.1 วิ + waveform สุ่มด้วย seed 20261007 (เหมือนเดิมทุกเทค)
- วิเคราะห์หน่วง 1800ms เพื่อให้ animation ดูดคำเข้าลูกแก้วครบ
- ทุกชื่อเป็นตัวละครสมมติ · เวลา +07:00
- ป้าย "โหมดตัวอย่าง" มุมบน กดออกได้
```

---

## C) TypeScript types + zod

```text
อ่าน schemas.json ของ VoiceMood แล้วสร้าง types/voicemood.ts

ต้องมี: Lang, Quadrant, WeatherKey, ThemeKey, HexColor, DateLocal, DateTime, AiEngine, SttEngine, LexiconTerm,
VoiceInput, MatchedTerm, Weather, Aura, ThemeChip, SafetyFlag, MoodAnalysis, TinyAction, ComfortCard, BreathSession,
Recheck, HistoryEntry, MoodEntry, GardenDay, MoodGarden, TriggerInsight, TriggerReport, MoodWrapped, Gratitude,
TimeCapsule, Reminder, ShareCard, SupportResource, SafetyCheck, Settings, LocalStore, AnalyticsEvent, FeatureItem,
FeatureChecklist

กติกา: union string ตรง enum, JSDoc สั้นอังกฤษ, export ทุก type, ห้าม any
เพิ่ม lib/zod.ts สำหรับ validate ผลจาก LLM (ComfortCard, LlmMoodHint, WeeklyNarrative) — parse ไม่ผ่าน → retry 1 → fallback template_v1
```

---

## D) `lib/mood.ts` (หัวใจคลิป)

```text
เขียน lib/mood.ts (pure ไม่มี side effect) export:
  analyzeText(text: string, lexicon: LexiconTerm[], opts?: { entryId?: string; engine?: AiEngine }): Omit<MoodAnalysis,"summary_th"|"safety">
  quadrantOf(v: number, energy: number): Quadrant
  weatherOf(score: number): Weather
  dayAggregate(entries: HistoryEntry[]): GardenDay

กติกา (prd.md §8 ห้ามเปลี่ยน):
- normalize: ตัด zero-width, ยุบช่องว่าง (ไม่ lowercase ไทย ไม่ตัดวรรณยุกต์)
- เรียง lexicon ตามความยาว term มากไปน้อย; สำหรับแต่ละ term หา occurrence แรกที่ไม่ทับช่วงที่ถูกใช้แล้ว → mark ช่วงนั้น
  นับ term ละครั้งเดียว · matched_terms เรียงตาม index
- negation: text.slice(i-3, i) === "ไม่" และ term ไม่ขึ้นต้นด้วย "ไม่" → valence = -valence, energy = 0, negated = true
- valence_sum = Σ, energy_sum = Σ · v = clamp(valence_sum,-8,8) · e = clamp(energy_sum,-8,8)
- energy = round((e+8)/16*10) · score = round((v+8)/16*100) · round = Math.floor(x+0.5)
- quadrant: v==0 neutral · v>0 (energy>=6 ? bright : calm) · v<0 (energy>=6 ? tense : low)
- weather: >=80 sunny ☀️ แดดจ้า · >=60 clear ⛅ ฟ้าโปร่ง · >=41 cloudy ☁️ เมฆครึ้ม · >=21 drizzle 🌧️ ฝนพรำ · else storm ⛈️ พายุเข้า
- themes = theme ของ matched (ยกเว้น "feeling") ตามลำดับแรกที่เจอ ไม่ซ้ำ
- aura.primary/secondary จาก mood_rules.quadrant_palette · glow_intensity = round2(min(1, 0.35 + |v|/8*0.65))
  · motion = energy>=6 ? "swirl_fast" : "pulse_slow"

Unit tests บังคับ (vitest) — อ่านค่าคาดหวังจาก examples.json:
- ทุก history_entries[i]: score, energy, quadrant, themes ตรงกัน (15 รายการ)
- vm_014 → valence_sum -4, energy_sum -1, score 25, energy 4, "low", 🌧️, 7 matched_terms
- vm_015 → score 75, energy 5, "calm", ⛅
- "วันนี้ไม่สบายใจเลย" → negated สบายใจ, valence -2, score 38, quadrant low
- "วันนี้กินข้าวแล้ว" → ไม่เจอคำ → score 50, neutral, ☁️
- dayAggregate(วันที่ 2026-10-07) → score 50, quadrant calm (entry ล่าสุด)
```

---

## E) `lib/safety.ts` + Support Sheet (ทำก่อน UI)

```text
เขียน lib/safety.ts:
  checkSafety(text: string, terms = SAFETY_TERMS): SafetyCheck
- SAFETY_TERMS = examples.json → safety_terms_th (substring, ไม่สน negation — "ไม่อยากอยู่แล้ว" คือคำเสี่ยงเอง)
- เจอ ≥ 1 → risk_level "urgent", action "show_support_sheet", resources = 1323 + 1669 (ตาม safety_check_examples[1])
- ไม่เจอ → "none", "continue"
- pipeline บังคับใน lib/pipeline.ts: checkSafety → (urgent ? หยุด : analyzeText → comfort)
- โหมด LLM: เรียก M4 เพิ่มได้ ถ้า LLM บอก elevated → action "soft_check_in" (แสดงการ์ดถามความรู้สึก + ปุ่ม 1323 เล็กๆ)
  LLM ลดระดับที่ lexicon เจอแล้วไม่ได้

components/SupportSheet.tsx:
- bottom sheet เต็มจอ พื้น #221E3F ไม่มีลูกแก้ว ไม่มีคะแนน ไม่มีปุ่มแชร์
- หัวข้อ「คุณไม่ได้อยู่คนเดียวนะ」+ message_th + ปุ่มโทร tel:1323 ใหญ่ + tel:1669 + 「ส่งข้อความหาคนที่ไว้ใจ」(เปิด share sheet ข้อความว่าง ผู้ใช้เลือกเอง)
- บันทึก entry แบบ flag ไว้ (ไม่มี analysis score) และไม่ขึ้นใน Garden เป็นสี (เป็นจุดเทาอ่อน)
- analytics เก็บแค่ event safety_sheet_shown ไม่เก็บข้อความ

tests: safety_check_examples ทั้ง 2 ตัว + pipeline urgent ต้องไม่เรียก analyzeText
```

---

## F) Record + waveform + STT + ลูกแก้ว Aura + Result

```text
hooks/useSpeech.ts:
- ตรวจ ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)
- lang "th-TH", interimResults true, continuous true · onresult รวม final + interim → state { finalText, interim, chunks[] }
- จำกัด 90 วิ · หยุดเมื่อปล่อยนิ้ว · error "not-allowed" → สลับ typed mode + ข้อความ ui_copy_th.mic_denied
- ไม่รองรับ → ถ้ามี key ใช้ MediaRecorder (webm/opus หรือ mp4 บน iOS) แล้ว POST /api/ai/transcribe · ไม่มี key → typed mode

hooks/useRecorder.ts: getUserMedia → AudioContext → AnalyserNode (fftSize 256) → ค่า RMS 32 แท่งต่อเฟรม (ไม่เก็บไฟล์ถ้า keep_audio false)

components/aura/Orb.tsx:
- props { primary, secondary, glow, motion, levels?: number[], state: "idle"|"listening"|"absorbing"|"result"|"breathe" }
- วาดด้วย div 3 ชั้น: radial-gradient(primary→transparent) + radial-gradient(secondary) offset + conic noise จาง, blur 40px
- idle: ม่วงเทา #6D5FA8 หายใจช้า 4 วิ · listening: วงคลื่น 32 แท่งรอบลูกแก้วตาม levels
- absorbing: คำ (span) แต่ละคำบินเข้า center (framer-motion, stagger 60ms, scale→0) แล้วลูกแก้ว tween สีจากเทา → primary 1.2 วิ
- result: หมุน 20 วิ/รอบ (swirl_fast 8 วิ/รอบ) · prefers-reduced-motion → ไม่หมุน

app/result/[id]/page.tsx:
- ลูกแก้ว 260px + score นับ 0 → score (spring) + weather emoji ใหญ่ + label_th + chip ธีม + summary_th (template ถ้าไม่มี LLM:
  "วันนี้มีเรื่อง{themes} เป็นหลัก ใจคุณ{label_th}")
- ปุ่ม 「ดูว่าคำไหนทำให้เป็นสีนี้」→ transcript ไฮไลต์ matched_terms (เขียว = บวก, ชมพู = ลบ) แตะคำ → "ไม่นับคำนี้" → คำนวณใหม่
- CTA หลัก: 「อ่านการ์ดของคุณ」→ Comfort
```

---

## G) Comfort Card + Breathe + Re-check

```text
lib/comfort.ts:
  buildComfort(analysis: MoodAnalysis, transcript: string, engine: AiEngine): Promise<ComfortCard>
- template_v1: เลือก validate/reframe จากตารางต่อ quadrant × theme แรก (อย่างน้อย 5 quadrant × 4 ประโยค)
  reframe ต้องอ้างอิงสิ่งที่มีใน transcript: ถ้ามี term บวกใด → "คุณยังเห็นช่วงเล็กๆ ที่ใจเบาลงตอน{term บวก}..."
  ถ้าไม่มี term บวก → "แค่คุณหยุดมาเล่าให้ฟัง ก็คือการดูแลตัวเองแล้ว"
- tiny_action ตาม quadrant: low/tense → breathe · neutral → walk 5 นาที · calm → gratitude · bright → message_friend
- เดโม vm_014 ต้องได้ comfort_card_example ตรงตัว
- llm_api: runtime prompt M2 → zod → fail → template

app/breathe:
- pattern 4-4-6 × 4 รอบ (56 วิ) · ลูกแก้ว scale 0.7 → 1.15 (เข้า 4 วิ) ค้าง 4 วิ → 0.7 (ออก 6 วิ)
- สีลูกแก้ว tween จาก orb_from (สีปัจจุบัน) → #34D399 ทีละรอบ 25%
- ข้อความ ui_copy_th.breathe_in/hold/out · navigator.vibrate(30) ตอนเปลี่ยนเฟส · ปุ่มข้าม
- จบ → บันทึก BreathSession → ปุ่ม 「เช็กใจอีกรอบ」

app/recheck:
- อัด ≤ 15 วิ (โหมดเดโมใช้ vm_015) → pipeline → บันทึก entry ใหม่ recheck_of = entry เดิม
- แผงก่อน/หลัง: ลูกแก้วเล็ก 2 ลูก ซ้าย (25 🌧️ #818CF8) → ลูกศร → ขวา (75 ⛅ #34D399) + caption_th
  "(จากคำที่คุณเล่าเอง)" ตัวเล็กด้านล่างเสมอ
- ถ้าคะแนนหลังต่ำกว่าเดิม: ไม่โชว์ลูกศรแดง แค่ "ขอบคุณที่บอกตรงๆ นะ วันนี้หนักจริง" + ปุ่มโทรหาเพื่อน/พักผ่อน
```

---

## H) Mood Garden + Mood Triggers

```text
lib/garden.ts:
  buildGarden(month: "YYYY-MM", entries: HistoryEntry[], today: DateLocal): MoodGarden
- days ครบเดือน · วันไม่มีบันทึก = null ทุกช่อง · score = round(avg) · quadrant/color = entry ล่าสุด
- streak_days = นับย้อนจาก today ต่อเนื่องที่มีบันทึก (ข้ามเดือนได้) · test: เดโม → 14
- ต้องได้ garden_example ตรงตัว

app/garden:
- grid 7 คอลัมน์ เริ่มจันทร์ หัวคอลัมน์ จ อ พ พฤ ศ ส อา · ลูกแก้ว 36px (glow ตามคะแนน) · วันนี้มีวงแหวน
- เปิดหน้า → ลูกแก้วเด้งเข้าทีละวัน stagger 70ms + เสียง pop เบา (ปิดได้)
- ด้านบน: "สตรีค 14 วัน 🔥" + legend 5 สี · แตะวัน → sheet รายการ entries วันนั้น

lib/triggers.ts:
  buildTriggers(entries: HistoryEntry[], minWith = 3): TriggerReport
- ตาม prd.md §8 ข้อ 10 · avg ปัด 1 ตำแหน่ง · delta = avg_with − avg_without ก่อนปัด แล้วปัด 1 ตำแหน่ง
- text_th: lifts "วันที่มีเรื่อง{label} {emoji} ใจคุณดีกว่าปกติ +{round(|delta|)} คะแนน" / drains "... ต่ำกว่าปกติ −{n} คะแนน"
- test: เดโม 15 entries → ตรง trigger_insights_example ทั้งลำดับและค่า (work −21.0, exercise +16.7, sleep −12.2, pet +9.0, body +3.8, family −1.7)

app/patterns:
- การ์ด 2 ใบบนสุด: 「ชาร์จใจ ⚡」(lifts สูงสุด) / 「ดูดพลัง 🪫」(drains สูงสุด)
- กราฟแท่งแนวนอนจากศูนย์กลาง (เขียว #34D399 ขวา / ชมพู #FB7185 ซ้าย) animate width
- entries < 6 → แสดง ui_copy_th.triggers_need_more
- ใต้กราฟ: "แพทเทิร์นจากคำที่คุณเล่า ไม่ใช่เหตุและผลทางการแพทย์"
```

---

## I) Share Aura Card

```text
components/share/AuraStory.tsx (1080x1920 render ที่ scale 0.3 สำหรับพรีวิว):
- พื้น #14112B + ดาวจุดเล็ก · ลูกแก้ว 640px สีของ entry · headline_th ใหญ่ ("ใจฉันวันนี้ 🌧️ ฝนพรำ")
- sub_th = label + theme ที่มีค่าบวก (ถ้ามี) เช่น "แต่มีแมวช่วย 🐱"
- after_badge_th ถ้ามี Recheck ("หายใจ 1 นาที → ⛅ 75")
- watermark "VoiceMood · AI วันละแอป" มุมล่าง
- show_transcript false = ห้ามมีข้อความที่พูดแม้แต่คำเดียว · show_score / show_themes สลับได้
components/share/GardenSquare.tsx (1080x1080): สวนอารมณ์เดือนนี้ + สตรีค
lib/share.ts: html-to-image toPng (pixelRatio 1) → File → navigator.canShare({files}) ? share : download
ชื่อไฟล์ voicemood_YYYY-MM-DD.png · เดโมต้องได้ share_card_example
```

---

## J) Nice-to-have pack

```text
ทำทีละตัวตามลำดับ หยุดได้ทุกเมื่อ:
1) Mood Wrapped (lib/wrapped.ts): period 7 วันล่าสุด → slides_th 6 หน้าแบบ stories (แตะซ้าย/ขวา, progress bar บน)
   เดโมต้องได้ mood_wrapped_example (avg 53.2, top bright, best 1 ต.ค. 75, hardest 2 ต.ค. 19)
2) Gratitude: หลัง Comfort ถ้า tiny_action = gratitude หรือผู้ใช้กด → 3 ช่อง ≤ 80 ตัวอักษร
3) Time Capsule: บันทึกข้อความ/เสียงถึงตัวเอง เลือกเปิด 1/3/6 เดือน ล็อกจนถึง open_at
4) Reminder 21:30: Notification API + service worker (PWA) · iOS ต้อง Add to Home Screen ก่อน แจ้งผู้ใช้
5) PIN lock 4 หลัก (hash ด้วย SubtleCrypto SHA-256 + salt ในเครื่อง) · ลืม PIN = ลบข้อมูลทั้งหมดเท่านั้น
6) Duo Compare: โหมด 2 คนพูดต่อกัน → ลูกแก้ว 2 ลูกชนกัน → การ์ด duo_compare (ไม่บันทึกของคนที่ 2)
7) Export .txt + ปุ่ม 「ลบข้อมูลทั้งหมด」(ยืนยัน 2 ชั้น)
```

---

## K) QA ก่อนถ่าย

```text
รัน checklist นี้แล้วรายงานผ่าน/ไม่ผ่านทีละข้อ:
- npm test ผ่านทั้งหมด (mood, safety, triggers, garden, wrapped)
- เดโม: Home → ลองข้อมูลตัวอย่าง → Result 25 🌧️ ใน ≤ 3 วิ → Comfort ตรงตัว → Breathe 56 วิ → Re-check 75 ⛅
  → Garden 7 ลูกใน ต.ค. สตรีค 14 → Patterns work −21 / exercise +17 → Share PNG ไม่มีข้อความที่พูด
- ไมค์จริงบน Chrome Android ภาษาไทย: พูด "วันนี้เหนื่อยมากแต่ดีใจที่ได้เจอเพื่อน" → matched เหนื่อย, ดีใจ, เจอเพื่อน
- ปฏิเสธสิทธิ์ไมค์ → typed mode ทันที ไม่ค้าง
- ข้อความ "ไม่อยากอยู่แล้ว" → Support Sheet ไม่มีคะแนน ไม่มีแชร์ · tel:1323 กดได้
- ไม่มี AI_API_KEY → ไม่มี error ใน console
- รีเฟรช → ข้อมูลยังอยู่ · keep_audio false → ไม่มี blob ใน IndexedDB
- Lighthouse PWA installable · 390px ไม่ล้น · prefers-reduced-motion ไม่หมุน
- ภาพหน้าจอ Result / Breathe / Garden ดูสวยในโหมด screen record 1080x1920
```

---

## L) แก้ปัญหาเร็ว (ใช้เมื่อพัง)

```text
- Web Speech ไทยไม่ขึ้นบน iOS → ใช้ typed mode หรือถ่ายด้วย Android/Chrome เดสก์ท็อป; ตรวจว่า HTTPS
- interim ซ้ำซ้อน → เก็บเฉพาะ results[i].isFinal ต่อท้าย finalText, interim แสดงแยก
- AnalyserNode เงียบ → ต้อง resume AudioContext หลัง user gesture
- ลูกแก้วกระตุกบนมือถือ → ลด blur เป็น 24px, ใช้ transform/opacity เท่านั้น, will-change: transform
- html-to-image ฟอนต์ไทยเพี้ยน → preload ฟอนต์ด้วย FontFace แล้วรอ document.fonts.ready ก่อน toPng
- คะแนนไม่ตรงเทสต์ → เช็กลำดับ match (ยาว→สั้น), negation slice(i-3,i), Math.floor(x+0.5)
- navigator.share files ไม่รองรับ → ดาวน์โหลดแทน + toast "บันทึกรูปแล้ว"
```

---

## M) Runtime prompts (ที่แอปส่งให้ LLM)

### M1 — mood hint (เสริม lexicon)

```text
SYSTEM:
คุณช่วยอ่านบันทึกอารมณ์ภาษาไทยที่ผู้ใช้พูดเอง ตอบ JSON เท่านั้น:
{ "summary_th": string (≤ 120 ตัวอักษร, บุรุษที่ 2 "คุณ", ใช้เฉพาะสิ่งที่ผู้ใช้พูด),
  "extra_terms": [{ "term": string (คัดลอกตรงจากข้อความ), "valence": -3..3, "energy": -3..3, "theme": ThemeKey }] (≤ 5),
  "themes_hint": ThemeKey[] }
กฎ:
1. ห้ามวินิจฉัย ห้ามใช้คำทางจิตเวช
2. extra_terms ต้องเป็นวลีที่อยู่ในข้อความจริง และไม่ซ้ำกับ LEXICON ที่ให้
3. ถ้าข้อความไม่เกี่ยวกับความรู้สึกเลย ให้ extra_terms = [] และ summary_th = ""
แอปจะคำนวณคะแนนเองด้วยสูตรเดิมจาก LEXICON + extra_terms

USER:
LEXICON_TERMS: {{lexicon_terms_csv}}
TEXT: """{{transcript}}"""
```

### M2 — comfort card

```text
SYSTEM:
คุณเขียนการ์ดปลอบใจสั้นๆ แบบเพื่อนที่อบอุ่น ไม่สั่งสอน ภาษาไทยเป็นกันเอง ตอบ JSON ตาม ComfortCard:
validate_th (≤ 140 ตัวอักษร: ยอมรับความรู้สึกโดยไม่ตัดสิน),
reframe_th (≤ 160 ตัวอักษร: มุมมองใหม่ที่อ้างอิงสิ่งที่ผู้ใช้พูดจริงอย่างน้อย 1 อย่าง ห้ามแต่งเหตุการณ์),
tiny_action (type ตาม ALLOWED_ACTION, ทำได้ใน ≤ {{minutes}} นาที), alt_actions ≤ 2
กฎ: ห้ามใช้ "ต้อง", "ควรจะ", "อย่าคิดมาก", "สู้ๆ" · ห้ามวินิจฉัย · ห้ามแนะนำยา · ไม่ใช้อีโมจิเกิน 1 ตัว
disclaimer_th = "VoiceMood เป็นสมุดบันทึกอารมณ์ ไม่ใช่การวินิจฉัยทางการแพทย์"

USER:
QUADRANT: {{quadrant}} · SCORE: {{score}} · THEMES: {{themes}}
POSITIVE_TERMS: {{positive_terms}} · ALLOWED_ACTION: {{allowed_action}}
TEXT: """{{transcript}}"""
```

### M3 — weekly narrative (Mood Wrapped)

```text
SYSTEM:
สรุปสัปดาห์อารมณ์เป็น 6 สไลด์สั้น (≤ 40 ตัวอักษรต่อสไลด์) โทนให้กำลังใจ จาก STATS ที่ให้เท่านั้น
ห้ามเพิ่มตัวเลขที่ไม่มีใน STATS · ตอบ JSON { "slides_th": string[6] }

USER:
STATS: {{wrapped_stats_json}}
```

### M4 — safety double-check

```text
SYSTEM:
อ่านข้อความแล้วประเมินว่ามีสัญญาณว่าผู้พูดอาจทำร้ายตัวเองหรือไม่ ตอบ JSON เท่านั้น:
{ "risk_level": "none" | "elevated" | "urgent", "reason_en": string (≤ 15 words) }
urgent = พูดถึงการตาย/ทำร้ายตัวเอง/ไม่อยากมีชีวิตอยู่ ตรงหรืออ้อม · elevated = สิ้นหวังรุนแรง รู้สึกเป็นภาระ ไม่มีใคร
ถ้าไม่แน่ใจ ให้เลือกระดับที่สูงกว่า

USER:
TEXT: """{{transcript}}"""
```

---

## N) Reel overlay / แคปชัน

```text
ทำหน้า /reel (ซ่อนจาก nav) สำหรับอัดหน้าจอ 1080x1920:
- ปุ่มเล่นลำดับเดโมอัตโนมัติตาม reel_script_th.shots (Listening → Absorb → Result → Comfort → Breathe เร่ง 4x → Re-check
  → Garden → Patterns → Share) พร้อม overlay ข้อความแต่ละช็อต (ฟอนต์ IBM Plex Sans Thai Bold 64px ขอบดำ 4px)
- ซ่อน status bar ปลอม · safe area บน/ล่าง 220px สำหรับ UI ของ Reels
- แคปชัน: reel_script_th.caption_th
```
