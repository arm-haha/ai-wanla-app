# ReplyKit — Prompt สั่งงาน (จัดเต็ม)

ใช้กับ AI codegen (Cursor / Claude / GPT) สำหรับสร้างแอปทั้งก้อน  
และใช้สร้าง demo chat fixtures / mock paste→reply packs

**วันที่แพ็ก:** 2026-10-02 (Asia/Bangkok) · Day 5/10 · AI วันละแอป  
**เอกสารคู่กัน:** `prd.md`, `schemas.json`, `examples.json`

---

## A) Master prompt สร้างทั้งแอป (วางครั้งเดียว)

```text
สร้างเว็บแอปมือถือเป็นหลักชื่อ ReplyKit (ภาษาไทย UI ก่อน)

วันที่ส่งมอบคอนเทนต์: 2026-10-02 สำหรับช่อง "AI วันละแอป"
เป้าหมายผู้ใช้: วางข้อความแชท/คอมเมนต์/DM ที่ตอบยาก → AI/mock สร้างชุดตอบหลายโทน → หมุน Tone Dial → เก็บสถานการณ์ใน Situation Library → อัปโหลดสกรีนช็อตแล้ว mock ดึงข้อความ → คัดลอก + แชร์การ์ดตอบสวย

สแต็กบังคับ:
- Next.js 14 App Router + TypeScript + Tailwind CSS + shadcn/ui
- Reply engine pluggable ใน lib/reply.ts: ค่าเริ่มต้น engine "mock_demo" โหลด fixture คุณภาพดี
  (รองรับสลับไป llm_api ผ่าน env ถ้าระบุ แต่ไม่บังคับ)
- Screenshot extract pluggable ใน lib/extract.ts: ค่าเริ่ม mock_demo
- Tone helpers ใน lib/tones.ts (pure)
- Share card + caption ใน lib/share.ts
- Situations helpers ใน lib/situations.ts หรือ /data/situations.json
- เก็บ packs / situations / favorites / settings ใน localStorage (lib/storage.ts)
- Deploy พร้อมบน Vercel (PWA พื้นฐานมี manifest ก็พอ)
- ไม่มี auth และไม่มีเคลมว่ารู้ความสัมพันธ์ / ไม่ส่งข้อความแทนผู้ใช้ / ไม่มีโซเชียลฟีดใน MVP

ต้องมีอย่างน้อย 5 ฟีเจอร์ must-have:
1) Paste → Reply Pack — textarea + ปุ่ม「ใช้ข้อความเดโม」+ progress สวย + กองการ์ดตอบ 3–5 โทนโผล่พร้อมอนิเมชัน
2) Tone Dial — soft / funny / pro / firm / warm; filter หรือ regenerate เมื่อเปลี่ยนโทน
3) Situation Library — คิทไทย: ตอบช้า, ปฏิเสธนุ่มๆ, ทวงงาน, คุยหัวหน้า, ลูกค้าโกรธ, แชทแฟนหรือเพื่อน + สร้าง/rename/favorite
4) Screenshot → Extract — อัปโหลดสกรีนช็อต + ปุ่ม「ใช้รูปเดโม」→ mock ดึง last inbound → Reply Pack
5) Copy & Share Reply Card — one-tap copy + การ์ดแชร์สวย + แคปชันคัดลอก IG/LINE + navigator.share

พิเศษถ้าเสร็จเร็ว (nice-to-have):
- Rewrite my draft
- Voice preview (speechSynthesis th-TH)
- Favorite replies history
- Bilingual TH/EN
- emoji booster
- Dark chat mode

หน้าจอ: Home, Paste Composer, Reply Pack Result, Tone Dial, Situation Library, Screenshot Extract, Share sheet, Rewrite/Voice/Dark (optional)

UX บังคับ:
- มือถือแนวตั้งก่อน (390px เป็นฐาน)
- ปุ่มใหญ่ นิ้วกดง่าย การ์ดตอบใหญ่
- โทนพื้น cream/off-white (#FFFBEB / #FAFAF9) + teal/mint (#0D9488 / #14B8A6) + coral (#FB7185) — อ่านคำตอบไทยชัดบน Reel
- ข้อความ UI ภาษาไทยตาม examples.json → ui_copy_th
- โทนช่วยเหลือ เป็นมิตร มี disclaimer「ตัวช่วยร่างข้อความ」

คุณภาพโค้ด:
- แยก components, hooks, lib/reply.ts, lib/tones.ts, lib/extract.ts, lib/share.ts, lib/storage.ts, lib/situations.ts
- มี TypeScript types ให้สอดคล้อง schemas.json
- README ภาษาไทย: วิธีรัน, วิธีเพิ่มข้อความเดโม, วิธีถ่าย Reel เดโม
- อย่าทำระบบล็อกอิน เคลมรู้ความสัมพันธ์ หรือส่งข้อความเข้า LINE จริงใน MVP
- เริ่มจากให้รัน `npm run dev` ผ่าน และทำ happy path ให้จบก่อน แล้วค่อยเสริม rewrite/voice/dark

อ้างอิงฟิลด์และตัวอย่างจาก schemas.json + examples.json ที่แนบมา
เมื่อจบให้สรุปว่าฟีเจอร์ must 5 ตัวอยู่ไฟล์ไหน และวิธีโหลดข้อความเดโม 1 ย่อหน้า
```

---

## B) Prompt สร้าง Demo chat fixtures / mock paste→replies

```text
สร้างชุดข้อมูลเดโมสำหรับ ReplyKit

1) ข้อความ inbound สมมติสไตล์ LINE จากเพื่อน: ประมาณ
   "เดี๋ยวก่อนนน คุยเรื่องวันเสาร์ไปไหนกัน ทำไมเงียบ 3 วันแล้ว 🥺"
2) ไฟล์ /public/fixtures/demo-chat.json ตาม schema ReplyPack + ChatMessage
3) ต้องมีอย่างน้อย 4–5 ReplyOption ภาษาไทย เช่น:
   - soft: ขอโทษที่เงียบ + ยังอยากไปวันเสาร์ + เสนอช่วงเย็น/โมงใหม่
   - funny: มุขเบาๆ เรื่องจมงาน/แบตสังคมหมด + ยอมรับผิด + นัดใหม่
   - warm: ขอบคุณที่ทักมาเตือน + เล่าสั้นๆ ว่ายุ่ง + นัดคุยดีๆ
   - firm: ขอโทษชัด + ช่วงนี้ตารางแน่น + เสนอ 2 ทางเลือก (เลื่อน/ไปสั้นๆ)
   - pro (ออปชัน): สุภาพกระชับ โทนเพื่อนที่โตแล้ว
4) confidence ≥ 0.8 สำหรับ fixture เดโม
5) generate_ms ประมาณ 700–1500
6) situation_id: reply_late_friend, title_th: "ตอบช้า · เพื่อน"
7) วันที่/เวลาเป็น Asia/Bangkok

สร้างเพิ่ม (ออปชัน) fixture สำรอง: สกรีนช็อตแชทเดโมสำหรับ Screenshot → Extract
และสถานการณ์「ปฏิเสธนุ่มๆ」3–4 คำตอบ

หลีกเลี่ยง: เคลมรู้ความสัมพันธ์, ส่งแทนผู้ใช้, หยาบคาย, ด่าเพื่อน

ตั้งชื่อผู้ใช้ตัวอย่าง: "มิ้นต์"
ส่งท้าย: ตาราง tone | text_th สั้นๆ สำหรับแปะในรีโป
ให้เนื้อหาสุดท้ายตรงกับ paste_reply_example ใน examples.json
```

---

## C) Prompt สร้าง TypeScript types จาก schemas

```text
อ่าน schemas.json ของ ReplyKit แล้วสร้างไฟล์ types/replykit.ts

ต้องมี type/interface อย่างน้อย:
ChatMessage, ToneId, ReplyOption, ReplyPack, Situation,
ExtractResult, ShareCard, SharePayload, LocalStore,
AnalyticsEvent, FeatureChecklist, ReplyEngine, ExtractEngine,
AppStatus, ToneDialState

กติกา:
- ใช้ union string ตรง enum ใน schema
- คอมเมนต์ JSDoc สั้นภาษาอังกฤษอ้าง description
- export ทุก type
- อย่าใส่ any
- ถ้ามี optional ใน schema ให้เป็น ? ใน TS
```

---

## D) Prompt UI polish / โทนแบรนด์

```text
ออกแบบ UI ReplyKit โหมดมือถือ

โทน: พื้น cream (#FFFBEB) / off-white (#FAFAF9), การ์ดขาว (#FFFFFF),
ไฮไลต์ teal (#0D9488) / mint (#14B8A6), coral accent (#FB7185),
ตัวอักษร ink (#134E4A), ข้อความรอง (#64748B)
ฟอนต์: system / Inter / Noto Sans Thai
ความหนาแน่นต่ำ เน้นการ์ดตอบใหญ่ + คำตอบไทยชัด ไม่โปสเตอร์รก ไม่ดาร์คโหมดบังคับ

หน้า Home ต้องมี:
- โลโก้ข้อความ ReplyKit
- หัวข้อ: วางข้อความแชท → ได้ชุดตอบหลายโทน ใน 10 วินาที
- คำอธิบายสั้น 1 บรรทัด
- แถบเดโมเลื่อนได้: ข้อความแชท → กองการ์ดตอบ → Tone Dial
- ปุ่มหลักใหญ่: วางข้อความ
- ปุ่มรอง: ใช้ข้อความเดโม
- แถวไอคอน 5 ฟีเจอร์: วาง→ชุดตอบ | โทน | คลังสถานการณ์ | สกรีนช็อต | แชร์การ์ด
- ฟุตเตอร์เล็ก: สร้างสำหรับช่อง AI วันละแอป + disclaimer สั้น

หน้า Reply Pack:
- กองการ์ดตอบพร้อมป้ายโทน
- ปุ่มคัดลอกใหญ่ต่อใบ
- Tone Dial ชัด

อย่าใส่ราคาคอร์ส soft skill ปุ่มสมัครสมาชิก หรือ「AI รู้ใจคุณ」
ส่งเป็นโครงสร้างคอมโพเนนต์ React + คลาส Tailwind
ใช้ข้อความจาก examples.json → ui_copy_th
```

---

## E) Prompt Share Reply Card + caption

```text
เขียน lib/share.ts + คอมโพเนนต์ ShareReplyCard สำหรับ ReplyKit

ต้องได้:
1) รูปการ์ดสรุปคำตอบแนวตั้งสวย (แนะนำ 1080x1350 หรือ 1080x1920)
   - หัวข้อ ReplyKit + ป้ายโทน
   - ข้อความ inbound ย่อ 1–2 บรรทัด
   - คำตอบที่เลือกตัวใหญ่
   - ฟุตเตอร์เล็ก ReplyKit · AI วันละแอป
   - โทน teal + coral ไม่ใส่「รู้ความสัมพันธ์」/ชื่อคนจริง
2) ข้อความแคปชันภาษาไทยสำหรับ IG/LINE ตามเทมเพลตใน examples.json → share_card_example
3) API:
   - buildSharePayload(pack, selectedReply, options): SharePayload
   - renderShareCardPng(...): Promise<Blob>
   - copyCaption(text): Promise<void>
   - shareNative(payload): Promise<void>
4) ชื่อไฟล์: replykit-{date}-{HHmmss}.png

โทนการ์ด: friendly chat helper อ่านชัดบนมือถือและ Reel
ข้อความ error UI เป็นภาษาไทย
อย่าใส่คำว่า「ส่งแทน」「คืนดีชัวร์」「AI รู้ใจ」บนการ์ด
```

---

## F) Prompt ถ่าย Reel / สคริปต์พูด (shot-list)

```text
เขียนสคริปต์ Reel 30 วินาทีภาษาไทย สำหรับแอป ReplyKit
โทนเพื่อนพูด ไม่ขายของแข็ง ไม่พูดคำว่า disruption/ecosystem
ไม่ขู่เรื่องเสียเพื่อน ไม่เคลมว่ารู้ความสัมพันธ์

โครงเวลา:
0-3s ฮุค วางข้อความ → ชุดตอบขึ้น
3-8s บอกว่าสร้างด้วย AI วันนี้
8-14s โชว์ Paste → Reply Pack (เพื่อนวันเสาร์ เงียบ 3 วัน)
14-22s Tone Dial → คัดลอกคำตอบ
22-28s Situation Library เร็วๆ + Share Reply Card
28-35s CTA ลิงก์ในไบโอ + ให้คอมเมนต์「ตอบ」

ข้อกำหนด:
- ข้อความบนจอทีละช็อตสั้น ไม่เกิน 8 คำ
- มี voice line ต่อช็อต
- ระบุของใช้ถ่าย: มือถือจริง 1 เครื่อง, ข้อความเดโม 1 ชุด, แพ็กมี ≥4 โทน
- โชว์อย่างน้อย 3 ฟีเจอร์ในคลิปเดียว
- ส่งออกเป็น JSON ตามคีย์ reel_script_th ใน examples.json ได้ด้วย
```

---

## G) Prompt QA ก่อนลงคลิป

```text
เช็ก ReplyKit ก่อนถ่าย Reel สำหรับคลิปวันที่ 2026-10-02

ทดสอบเคส:
1) โหลดข้อความเดโม — ได้ชุดตอบไทย 4–5 โทนตาม examples
2) Tone Dial เปลี่ยนโทน — แพ็กกรองหรือ regen ชัด
3) คัดลอกคำตอบ 1 ใบ — toast สำเร็จ
4) Situation Library เปิดคิท「ตอบช้า」+ favorite + สร้างใหม่ได้
5) Screenshot: ใช้รูปเดโม — extract ข้อความ → Reply Pack
6) แชร์รูปการ์ด + คัดลอกแคปชันบนมือถือ
7) (ถ้ามี) วางข้อความจริงสั้น/ยาว — ต้องไม่แครช

เช็กรายการ:
- ไม่มี NaN / undefined บน UI
- ปุ่มใหญ่ใช้นิ้วได้ที่ 390px
- UI ภาษาไทยไม่ตัดคำแปลกๆ
- มี disclaimer ตัวช่วยร่าง มองเห็นได้
- ไม่มีข้อความ「รู้ความสัมพันธ์」/ ส่งแทน
- Library ไม่พังถ้า localStorage ว่าง
- สีหลัก teal+coral ตามแบรนด์

รายงานเป็นตาราง: เคส | ผล | severity (blocker/major/minor) | วิธีแก้สั้นๆ
สรุปท้ายว่าพร้อมถ่าย Reel หรือยัง พร้อมติ๊ก FeatureChecklist
```

---

## H) Prompt Reply / Tone engine

```text
เขียน lib/reply.ts และ lib/tones.ts สำหรับ ReplyKit ให้เข้ากับ schemas.json

lib/reply.ts:
- generatePack(input: { inbound_th, situation_id?, tones?, engine? }): ReplyPack
- pickDemoPack(): ReplyPack  // fixture เพื่อนวันเสาร์
- rankByTone(pack, selectedTones): ReplyOption[]

lib/tones.ts:
- TONE_META: Record<ToneId, { label_th, label_en, emoji, color }>
- filterByTones(replies, tones): ReplyOption[]
- defaultTonesForSituation(situationId): ToneId[]
- dialState(selected: ToneId[]): ToneDialState

ข้อกำหนด:
- ฟังก์ชันบริสุทธิ์ เทสได้
- ผลตัวอย่างต้องสอดคล้อง paste_reply_example / tone_dial_example ใน examples.json
- ไม่พึ่งเซิร์ฟเวอร์ในโหมด mock_demo
- ความยาว text_th แนะนำ 40–160 ตัวอักษรต่อใบ (มือถืออ่านง่าย)
```

---

## I) Prompt เพิ่ม Rewrite / Voice / Favorites / Dark (nice)

```text
ตอนนี้ ReplyKit ทำ happy path ครบ 5 ฟีเจอร์ must แล้ว
ช่วยเพิ่มตามลำดับความคุ้มของคลิป:

1) Rewrite my draft — textarea วางร่างของฉัน → ปรับโทน
2) Voice preview — speechSynthesis th-TH อ่านคำตอบ
3) Favorite replies history — เก็บ ReplyOption ที่กดหัวใจ
4) Bilingual TH/EN — สลับดูคู่กัน
5) emoji booster — เติม/ลดอีโมจิตามโทน
6) Dark chat mode — ธีมมืดสลับได้ เก็บใน settings

กติกา:
- อย่าพัง API ของ reply/tones/extract/share เดิม
- มือถือใช้นิ้วได้
- อัปเดต FeatureChecklist ใน examples
- ไม่ต้องเพิ่ม auth หรือส่งข้อความเข้าแชทจริง
```

---

## J) Prompt ซ่อม JSON / validate ตอนรันจริง

```text
มี object ReplyPack / ReplyOption / Situation / ExtractResult / SharePayload จากแอป ReplyKit
ตรวจกับ schemas.json (draft 2020-12)
ถ้าไม่ผ่าน: บอกฟิลด์ที่ผิด และคืนค่า object ที่ซ่อมแล้ว
ห้ามแต่งเนื้อหาคำตอบที่ผู้ใช้ตั้งใจ นอกจากต้องใส่ default ที่ขาด
ตอบเป็นภาษาไทยสรุป + บล็อก JSON เต็ม
```

---

## K) Few-shot ข้อความ UI สั้นๆ

**ตอน generate:** 「กำลังคิดชุดตอบหลายโทน…」  
**สำเร็จ:** 「ได้ชุดตอบแล้ว — เลือกโทนแล้วก็อปได้เลย」  
**คัดลอกแล้ว:** 「คัดลอกแล้ว ไปวางในแชทได้」  
**เปลี่ยนโทน:** 「โทน{name} — จัดแพ็กให้แล้ว」  
**แชร์:** 「คัดลอกแคปชันแล้ว」  
**ผิดพลาด:** 「สร้างชุดตอบไม่สำเร็จ ลองวางข้อความใหม่」  
**extract:** 「กำลังอ่านข้อความจากรูป…」  
**disclaimer สั้น:** 「ตัวช่วยร่างข้อความ — คุณเลือกส่งเอง」  

(ชุดเต็มอยู่ที่ `examples.json` → `ui_copy_th`)

---

## L) Prompt สร้าง situations starter data

```text
สร้างไฟล์ data/situations.json สำหรับ ReplyKit

ต้องมีอย่างน้อย:
1) reply_late — ตอบช้า
2) soft_no — ปฏิเสธนุ่มๆ
3) chase_work — ทวงงาน
4) talk_boss — คุยหัวหน้า
5) angry_customer — ลูกค้าโกรธ
6) friend_or_partner — แชทแฟนหรือเพื่อน

แต่ละรายการ: id, title_th, title_en, emoji, prompt_hint_th, default_tones[], sample_inbound_th, color_hex (เข้ากับโทน teal/coral)

สร้าง starter ที่ผูกกับ paste_reply_example: reply_late_friend ภายใต้กลุ่มตอบช้า
ส่งออก JSON ถูกต้อง UTF-8
```

---

## M) Prompt ออกแบบ Reply Pack Result + card stack

```text
สร้างหน้า/คอมโพเนนต์ ReplyPackResult สำหรับ ReplyKit

องค์ประกอบ:
1) Header ย่อ inbound + ปุ่มแก้ข้อความ
2) กองการ์ดตอบเลื่อนแนวนอนหรือแนวตั้ง — แต่ละใบมีป้ายโทน สีต่างกันเล็กน้อย
3) ปุ่มคัดลอกใหญ่ / หัวใจ (nice) / แชร์ใบนี้
4) Tone Dial ด้านล่างหรือด้านบน
5) ปุ่ม「บันทึกเป็นสถานการณ์」+ 「สร้างใหม่」
6) ข้อความย่อย disclaimer ตัวช่วยร่าง

พฤติกรรม:
- ตอนโหลด fixture ให้ animate การ์ดโผล่ทีละใบ (wow สำหรับ Reel)
- confidence < 0.55 แสดงแบนเนอร์「อาจไม่เข้าบริบท — แก้ข้อความต้นทางได้」
- ห้ามใช้คำ「ส่งแทนคุณ」บนหน้านี้

ส่งเป็น React + Tailwind สอดคล้อง ui_copy_th
```

---

## N) Prompt Tone Dial + Situation Library + Screenshot Extract

```text
สร้างคอมโพเนนต์ ToneDial, SituationLibrary, ScreenshotExtract สำหรับ ReplyKit

ToneDial:
1) ชิปหรือวงล้อ 5 โทน: soft funny pro firm warm
2) multi-select หรือ single-select ก็ได้ — ระบุใน props (MVP แนะนำ multi filter)
3) ปุ่ม「สร้างใหม่ตามโทนนี้」
4) สี active teal, accent coral

SituationLibrary:
1) กริดการ์ดคิทไทย ≥6
2) favorite / rename / create
3) empty state「ยังไม่มีสถานการณ์ — บันทึกจากชุดตอบแรกเลย」
4) แตะแล้วเติม composer หรือ generate

ScreenshotExtract:
1) พรีวิวรูป + ปุ่มใช้รูปเดโม
2) progress extracting
3) แสดง last_inbound_th แก้ได้
4) CTA สร้าง Reply Pack

ข้อมูลจาก lib/tones.ts, lib/situations.ts, lib/extract.ts
อย่าใส่กราฟ「โอกาสคืนดี」หรือเคลมรู้ความสัมพันธ์
```

---

## O) Prompt Screenshot mock extract fixture

```text
สร้าง fixture สกรีนช็อตสำหรับ ReplyKit Screenshot → Extract

1) คำอธิบายภาพสมมติ: หน้าจอ LINE แชทกับเพื่อน「มิกซ์」มีบับเบิล inbound ล่าสุดเรื่องวันเสาร์
2) ไฟล์ /public/fixtures/demo-screenshot.json ตาม schema ExtractResult
3) last_inbound_th ต้องสอดคล้องข้อความใน paste_reply_example
4) extract_ms 800–1400, confidence ≥ 0.8
5) engine: mock_demo
6) warnings_th เป็น [] หรือคำเตือนเบาๆ ว่าเป็นโหมดเดโม

ให้ตรงกับ screenshot_extract_example ใน examples.json
```
