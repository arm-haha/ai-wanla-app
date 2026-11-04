# ExamDeck — Prompt สั่งงาน (จัดเต็ม)

ใช้กับ AI codegen (Cursor / Claude / GPT) สำหรับสร้างแอปทั้งก้อน  
และใช้สร้าง demo note fixtures / mock photo→cards results

**วันที่แพ็ก:** 2026-10-01 (Asia/Bangkok) · Day 4/10 · AI วันละแอป  
**เอกสารคู่กัน:** `prd.md`, `schemas.json`, `examples.json`

---

## A) Master prompt สร้างทั้งแอป (วางครั้งเดียว)

```text
สร้างเว็บแอปมือถือเป็นหลักชื่อ ExamDeck (ภาษาไทย UI ก่อน)

วันที่ส่งมอบคอนเทนต์: 2026-10-01 สำหรับช่อง "AI วันละแอป"
เป้าหมายผู้ใช้: ถ่าย/อัปโหลดรูปโน้ตหรือข้อสอบ → AI/mock แตกเป็นแฟลชการ์ด Q&A → บันทึกเป็นเด็คตามวิชา → ทวนแบบสไวป์ (รู้แล้ว/ยังไม่ชัวร์) → ดูแดชบอร์ดความชำนาญ → แชร์การ์ดสตรีค/ความคืบหน้า

สแต็กบังคับ:
- Next.js 14 App Router + TypeScript + Tailwind CSS + shadcn/ui
- Photo→Cards pluggable ใน lib/extract.ts: ค่าเริ่มต้น engine "mock_demo" โหลด fixture คุณภาพดี
  (รองรับสลับไป vision_api ผ่าน env ถ้าระบุ แต่ไม่บังคับ)
- Mastery + quiz pure functions ใน lib/mastery.ts + lib/quiz.ts
- Share card + caption ใน lib/share.ts
- Subjects/deck helpers ใน lib/subjects.ts หรือ /data/subjects.json
- เก็บ decks / cards / sessions / settings ใน localStorage (lib/storage.ts)
- Deploy พร้อมบน Vercel (PWA พื้นฐานมี manifest ก็พอ)
- ไม่มี auth และไม่มีเคลมสอบผ่าน / ไม่มีเฉลยข้อสอบสด / ไม่มีโซเชียลฟีดใน MVP

ต้องมีอย่างน้อย 5 ฟีเจอร์ must-have:
1) Photo → Cards — อัปโหลด/ถ่ายโน้ต + ปุ่ม「ใช้รูปเดโม」+ progress สวย + กองการ์ด Q&A โผล่พร้อมอนิเมชัน
2) Swipe Quiz — พลิกการ์ด, สไวป์/แตะ รู้แล้ว / ยังไม่ชัวร์ + สตรีคฟีดแบ็ก
3) Deck Library — โฟลเดอร์วิชา (คณิต อังกฤษ ชีวะ ประวัติ ฯลฯ) + สร้าง/เปลี่ยนชื่อเด็ค
4) Mastery Dashboard — % mastered, due-today, study streak rings/bars
5) Share Study Card — รูปการ์ดสตรีค/ความคืบหน้า + แคปชันคัดลอก IG/LINE + navigator.share

พิเศษถ้าเสร็จเร็ว (nice-to-have):
- Paste Text → Cards
- Multi-choice mode
- Exam countdown timer
- Voice read question (speechSynthesis th-TH)
- Dark study mode
- Offline localStorage history

หน้าจอ: Home, Photo/Upload, Extract Confirm, Swipe Quiz, Deck Library, Mastery Dashboard, Share sheet, Paste/Multi/Dark (optional)

UX บังคับ:
- มือถือแนวตั้งก่อน (390px เป็นฐาน)
- ปุ่มใหญ่ นิ้วกดง่าย การ์ดพลิกใหญ่
- โทนพื้น off-white (#FAFAF9) + indigo/violet (#4F46E5 / #6366F1) + amber (#F59E0B) — อ่านคำถามไทยชัดบน Reel
- ข้อความ UI ภาษาไทยตาม examples.json → ui_copy_th
- โทนเรียนสนุก ไม่เครียด มี disclaimer「เครื่องมือทวน」

คุณภาพโค้ด:
- แยก components, hooks, lib/extract.ts, lib/mastery.ts, lib/quiz.ts, lib/share.ts, lib/storage.ts, lib/subjects.ts
- มี TypeScript types ให้สอดคล้อง schemas.json
- README ภาษาไทย: วิธีรัน, วิธีเพิ่มรูปเดโม, วิธีถ่าย Reel เดโม
- อย่าทำระบบล็อกอิน เคลมสอบผ่าน หรือโซเชียลฟีดใน MVP
- เริ่มจากให้รัน `npm run dev` ผ่าน และทำ happy path ให้จบก่อน แล้วค่อยเสริม paste/multi/dark

อ้างอิงฟิลด์และตัวอย่างจาก schemas.json + examples.json ที่แนบมา
เมื่อจบให้สรุปว่าฟีเจอร์ must 5 ตัวอยู่ไฟล์ไหน และวิธีโหลดรูปเดโม 1 ย่อหน้า
```

---

## B) Prompt สร้าง Demo note fixtures / mock photo→cards

```text
สร้างชุดข้อมูลเดโมสำหรับ ExamDeck

1) คำอธิบายหรือไฟล์ภาพโน้ตสมมติ: หน้าโน้ตม.ปลายวิชาชีวะหัวข้อ「ระบบหายใจ」ลายมือ/พิมพ์ผสม แสงธรรมชาติ
2) ไฟล์ /public/fixtures/demo-note.json ตาม schema PhotoExtractResult + Flashcard[]
3) ต้องมีอย่างน้อย 7 การ์ด Q&A ภาษาไทย เช่น:
   - Q: อวัยวะหลักในระบบหายใจมีอะไรบ้าง → A: จมูก คอหอย กล่องเสียง หลอดลม หลอดลมฝอย ถุงลม ปอด
   - Q: แก๊สที่ร่างกายต้องการตอนหายใจเข้าคืออะไร → A: ออกซิเจน (O₂)
   - Q: การแลกเปลี่ยนแก๊สเกิดที่ใด → A: ถุงลมปอด (alveoli)
   - Q: กล้ามเนื้อสำคัญที่ช่วยหายใจคืออะไร → A: กะบังลม (diaphragm)
   - Q: หายใจเข้า ปริมาตรช่องอกเป็นอย่างไร → A: เพิ่มขึ้น ความดันลด อากาศไหลเข้า
   - Q: โรคที่เกี่ยวข้องกับระบบหายใจ举例如ไร → A: หอบหืด ปอดบวม (ตัวอย่างทวน ไม่ใช่วินิจฉัย)
   - Q: หลอดเลือดที่รับเลือดจากปอดไปหัวใจคืออะไร → A: หลอดเลือดดำปอด (pulmonary veins) — เลือดมี O₂ สูง
4) confidence ≥ 0.8 สำหรับ fixture เดโม
5) extract_ms ประมาณ 900–1500
6) subject: biology, deck_title_th: "ชีวะ · ระบบหายใจ"
7) วันที่/เวลาเป็น Asia/Bangkok

สร้างเพิ่ม (ออปชัน) fixture สำรอง: คณิต「สมการเชิงเส้น」3–5 การ์ด สำหรับโชว์ Deck Library

หลีกเลี่ยง: เคลมสอบผ่าน, เฉลยข้อสอบวัดผลจริง, โลโก้สำนักพิมพ์ข้อสอบ

ตั้งชื่อผู้ใช้ตัวอย่าง: "พลอย"
ส่งท้าย: ตาราง Q | A สั้นๆ สำหรับแปะในรีโป
ให้เนื้อหาสุดท้ายตรงกับ photo_extract_example ใน examples.json
```

---

## C) Prompt สร้าง TypeScript types จาก schemas

```text
อ่าน schemas.json ของ ExamDeck แล้วสร้างไฟล์ types/examdeck.ts

ต้องมี type/interface อย่างน้อย:
Flashcard, Deck, SubjectFolder, StudySession, QuizAnswer,
MasteryStats, PhotoExtractResult, ShareCard, SharePayload,
LocalStore, AnalyticsEvent, FeatureChecklist, ExtractEngine,
CardStatus, AnswerVerdict

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
ออกแบบ UI ExamDeck โหมดมือถือ

โทน: พื้น off-white (#FAFAF9), การ์ดขาว (#FFFFFF), ไฮไลต์ indigo (#4F46E5) / violet (#6366F1),
amber accent (#F59E0B), ตัวอักษร ink (#1E1B4B), ข้อความรอง (#64748B)
ฟอนต์: system / Inter / Noto Sans Thai
ความหนาแน่นต่ำ เน้นการ์ดพลิกใหญ่ + คำถามไทยชัด ไม่โปสเตอร์รก ไม่ดาร์คโหมดบังคับ

หน้า Home ต้องมี:
- โลโก้ข้อความ ExamDeck
- หัวข้อ: ถ่ายโน้ต/ข้อสอบ → ได้เด็คทวนทันที ใน 10 วินาที
- คำอธิบายสั้น 1 บรรทัด
- แถบเดโมเลื่อนได้: รูปโน้ต → กองการ์ด → Swipe Quiz
- ปุ่มหลักใหญ่: ถ่ายโน้ต
- ปุ่มรอง: ใช้รูปเดโม
- แถวไอคอน 5 ฟีเจอร์: รูป→การ์ด | สไวป์ทวน | ไลบรารีเด็ค | ความชำนาญ | แชร์การ์ด
- ฟุตเตอร์เล็ก: สร้างสำหรับช่อง AI วันละแอป + disclaimer สั้น

หน้า Swipe Quiz:
- การ์ดใหญ่กลาง พลิกได้
- ปุ่ม ยังไม่ชัวร์ / รู้แล้ว ใหญ่
- แถบ progress + สตรีค

อย่าใส่ราคาคอร์สติว ปุ่มสมัครสมาชิก หรือ「รับประกันสอบผ่าน」
ส่งเป็นโครงสร้างคอมโพเนนต์ React + คลาส Tailwind
ใช้ข้อความจาก examples.json → ui_copy_th
```

---

## E) Prompt Share Study Card + caption

```text
เขียน lib/share.ts + คอมโพเนนต์ ShareStudyCard สำหรับ ExamDeck

ต้องได้:
1) รูปการ์ดสรุปสตรีค/เด็คแนวตั้งสวย (แนะนำ 1080x1350 หรือ 1080x1920)
   - หัวข้อ ExamDeck + ชื่อเด็คไทย
   - % ชำนาญใหญ่ + จำนวนการ์ดทวนวันนี้
   - สตรีควัน
   - ฟุตเตอร์เล็ก ExamDeck · AI วันละแอป
   - โทน indigo + amber ไม่ใส่「สอบผ่านชัวร์」/คะแนนปลอม
2) ข้อความแคปชันภาษาไทยสำหรับ IG/LINE ตามเทมเพลตใน examples.json → share_card_example
3) API:
   - buildSharePayload(stats, deck, options): SharePayload
   - renderShareCardPng(...): Promise<Blob>
   - copyCaption(text): Promise<void>
   - shareNative(payload): Promise<void>
4) ชื่อไฟล์: examdeck-{date}-{HHmmss}.png

โทนการ์ด: study focus อ่านชัดบนมือถือและ Reel
ข้อความ error UI เป็นภาษาไทย
อย่าใส่คำว่า「โกงสอบ」「เฉลย」「รับประกันผ่าน」บนการ์ด
```

---

## F) Prompt ถ่าย Reel / สคริปต์พูด (shot-list)

```text
เขียนสคริปต์ Reel 30 วินาทีภาษาไทย สำหรับแอป ExamDeck
โทนเพื่อนพูด ไม่ขายของแข็ง ไม่พูดคำว่า disruption/ecosystem
ไม่ขู่เรื่องสอบตก ไม่เคลมสอบผ่าน

โครงเวลา:
0-3s ฮุค รูปโน้ต → กองการ์ดขึ้น
3-8s บอกว่าสร้างด้วย AI วันนี้
8-14s โชว์ Photo → Cards (ชีวะ ระบบหายใจ)
14-22s Swipe Quiz → Mastery Dashboard อัปเดต
22-28s Deck Library เร็วๆ + Share Study Card
28-35s CTA ลิงก์ในไบโอ + ให้คอมเมนต์「เด็ค」

ข้อกำหนด:
- ข้อความบนจอทีละช็อตสั้น ไม่เกิน 8 คำ
- มี voice line ต่อช็อต
- ระบุของใช้ถ่าย: มือถือจริง 1 เครื่อง, รูปโน้ตเดโม 1 หน้า, เด็คมี ≥5 การ์ด
- โชว์อย่างน้อย 3 ฟีเจอร์ในคลิปเดียว
- ส่งออกเป็น JSON ตามคีย์ reel_script_th ใน examples.json ได้ด้วย
```

---

## G) Prompt QA ก่อนลงคลิป

```text
เช็ก ExamDeck ก่อนถ่าย Reel สำหรับคลิปวันที่ 2026-10-01

ทดสอบเคส:
1) โหลดรูปเดโม — ได้การ์ด Q&A ไทย 6–8 ใบตาม examples
2) แก้คำถาม 1 ใบ + ตั้งชื่อเด็ค/วิชา แล้วบันทึก
3) Swipe Quiz ทวน ≥3 ใบ — รู้แล้ว/ยังไม่ชัวร์ อัปเดต
4) Mastery Dashboard % / due / streak อัปเดต
5) Deck Library สร้างเด็คใหม่ + เปลี่ยนชื่อได้
6) แชร์รูปการ์ด + คัดลอกแคปชันบนมือถือ
7) (ถ้ามี) อัปโหลดรูปโน้ตจริงภาพชัด / ภาพมืด — ต้องไม่แครช อย่างน้อยให้แก้การ์ดมือได้

เช็กรายการ:
- ไม่มี NaN / undefined บน UI
- ปุ่มใหญ่ใช้นิ้วได้ที่ 390px
- UI ภาษาไทยไม่ตัดคำแปลกๆ
- มี disclaimer เครื่องมือทวน มองเห็นได้
- ไม่มีข้อความ「สอบผ่านชัวร์」/ เฉลยข้อสอบสด
- Library/History ไม่พังถ้า localStorage ว่าง
- สีหลัก indigo+amber ตามแบรนด์

รายงานเป็นตาราง: เคส | ผล | severity (blocker/major/minor) | วิธีแก้สั้นๆ
สรุปท้ายว่าพร้อมถ่าย Reel หรือยัง พร้อมติ๊ก FeatureChecklist
```

---

## H) Prompt Mastery / quiz engine

```text
เขียน lib/quiz.ts และ lib/mastery.ts สำหรับ ExamDeck ให้เข้ากับ schemas.json

lib/quiz.ts:
- gradeAnswer(verdict: "known"|"unsure"): QuizAnswer
- nextCard(queue, currentId): Flashcard | null
- buildSession(deckId, answers): StudySession
- streakInSession(answers): number  // known ติดกันปัจจุบัน

lib/mastery.ts:
อินพุต: Flashcard[], StudySession[], (ออปชัน) date Asia/Bangkok
เอาต์พุต: MasteryStats { total_cards, mastered_count, mastery_pct, due_today, streak_days, ... }

ฟังก์ชันหลัก:
- updateCardStatus(card, verdict): Flashcard
- isMastered(card): boolean  // known ติด ≥2 เป็นค่าเริ่ม
- dueCards(cards, date): Flashcard[]
- buildMasteryStats(cards, sessions, date): MasteryStats

ข้อกำหนด:
- ฟังก์ชันบริสุทธิ์ เทสได้
- ผลตัวอย่างต้องสอดคล้อง mastery_dashboard_example / study_session_example ใน examples.json
- ไม่พึ่งเซิร์ฟเวอร์
- ไม่บังคับ FSRS เต็มใน MVP
```

---

## I) Prompt เพิ่ม Paste / Multi / Dark / Voice (nice)

```text
ตอนนี้ ExamDeck ทำ happy path ครบ 5 ฟีเจอร์ must แล้ว
ช่วยเพิ่มตามลำดับความคุ้มของคลิป:

1) Paste Text → Cards — textarea วางโน้ต → mock แตก Q&A
2) Multi-choice mode — สร้างตัวลวง 3 ข้อจากการ์ดอื่นในเด็ค
3) Exam countdown timer — ตั้งวันสอบต่อเด็ค แสดงวันเหลือ
4) Voice read question — speechSynthesis ภาษาไทยอ่านคำถาม
5) Dark study mode — ธีมมืดสลับได้ เก็บใน settings
6) Offline history — เก็บ StudySession ย้อนหลัง

กติกา:
- อย่าพัง API ของ extract/quiz/mastery/share เดิม
- มือถือใช้นิ้วได้
- อัปเดต FeatureChecklist ใน examples
- ไม่ต้องเพิ่ม auth หรือเคลมสอบผ่าน
```

---

## J) Prompt ซ่อม JSON / validate ตอนรันจริง

```text
มี object PhotoExtractResult / Flashcard / Deck / StudySession / MasteryStats / SharePayload จากแอป ExamDeck
ตรวจกับ schemas.json (draft 2020-12)
ถ้าไม่ผ่าน: บอกฟิลด์ที่ผิด และคืนค่า object ที่ซ่อมแล้ว
ห้ามแต่งเนื้อหา Q&A ที่ผู้ใช้ตั้งใจ นอกจากต้องใส่ default ที่ขาด
ตอบเป็นภาษาไทยสรุป + บล็อก JSON เต็ม
```

---

## K) Few-shot ข้อความ UI สั้นๆ

**ตอน extract:** 「กำลังแตกโน้ตเป็นการ์ด…」  
**สำเร็จ:** 「ได้เด็คทวนแล้ว — แก้คำถามก่อนบันทึกได้」  
**บันทึกแล้ว:** 「บันทึกเด็คแล้ว พร้อมทวนเลย」  
**รู้แล้ว:** 「เก่ง! ไปใบถัดไป」  
**ยังไม่ชัวร์:** 「โอเค เก็บไว้ทวนอีกครั้ง」  
**แชร์:** 「คัดลอกแคปชันแล้ว」  
**ผิดพลาด:** 「อ่านรูปไม่สำเร็จ ลองถ่ายใหม่หรือแก้การ์ดมือ」  
**สตรีค:** 「ทวนต่อเนื่อง {days} วันแล้ว สุดยอด」  

(ชุดเต็มอยู่ที่ `examples.json` → `ui_copy_th`)

---

## L) Prompt สร้าง subjects + starter decks data

```text
สร้างไฟล์ data/subjects.json สำหรับ ExamDeck

ต้องมีอย่างน้อย:
1) math — คณิต
2) english — อังกฤษ
3) biology — ชีวะ
4) history — ประวัติ
5) physics — ฟิสิกส์
6) other — อื่นๆ

แต่ละรายการ: id, name_th, name_en, emoji, color_hex (เข้ากับโทน indigo/amber)

สร้าง starter deck ตัวอย่าง 1 อัน: biology / "ชีวะ · ระบบหายใจ" ผูกกับ photo_extract_example
ส่งออก JSON ถูกต้อง UTF-8
```

---

## M) Prompt ออกแบบ Extract Confirm + card stack

```text
สร้างหน้า/คอมโพเนนต์ ExtractConfirm สำหรับ ExamDeck

องค์ประกอบ:
1) พรีวิวรูปโน้ตมุมบนมน
2) กองการ์ดเลื่อนแนวนอน — แต่ละใบพลิกหน้า/หลังได้
3) แก้ question_th / answer_th แบบ inline
4) ปุ่มลบการ์ด / เพิ่มการ์ดว่าง
5) ช่องชื่อเด็ค + ชิปเลือกวิชา
6) ปุ่มหลัก「บันทึกเด็คนี้」+ ปุ่มรอง「ถ่ายใหม่」
7) ข้อความย่อย disclaimer เครื่องมือทวน

พฤติกรรม:
- ตอนโหลด fixture ให้ animate กองการ์ดโผล่ทีละใบ (wow สำหรับ Reel)
- confidence < 0.55 แสดงแบนเนอร์「ไม่แน่ใจ — ช่วยแก้คำถามให้ตรงขึ้นได้」
- ห้ามใช้คำ「เฉลยข้อสอบ」บนหน้านี้

ส่งเป็น React + Tailwind สอดคล้อง ui_copy_th
```

---

## N) Prompt Swipe Quiz + Mastery rings

```text
สร้างคอมโพเนนต์ SwipeQuiz และ MasteryDashboard สำหรับ ExamDeck

SwipeQuiz:
1) การ์ดใหญ่ พลิกด้วยแตะ
2) สไวป์ขวา = รู้แล้ว, สไวป์ซ้าย = ยังไม่ชัวร์ (พร้อมปุ่มสำรอง)
3) แถบ progress + สตรีคในเซสชัน
4) จบเซสชันโชว์สรุป known/unsure แล้วไป Dashboard

MasteryDashboard:
1) Header วันที่ไทย + ปุ่มแชร์
2) วงแหวน % ชำนาญ
3) ชิป due วันนี้ + สตรีควัน
4) รายการเด็คพร้อม % ย่อย
5) ทางลัด「ทวน due วันนี้」

ข้อมูลจาก buildMasteryStats() ใน lib/mastery.ts
ว่างเปล่า: empty state「ยังไม่มีเด็ค — ถ่ายโน้ตแรกเลย」
อย่าใส่กราฟคะแนนสอบปลอมหรือ「โอกาสสอบผ่าน」
```
