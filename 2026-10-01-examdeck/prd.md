# PRD: ExamDeck

**Product name:** ExamDeck  
**Tagline (TH):** ถ่ายโน้ต/ข้อสอบ → ได้เด็คทวนทันที ใน 10 วินาที  
**Tagline (EN):** Snap notes or exam papers → instant review flashcards  
**Version:** 1.0 (MVP — AI-วันละแอป Day 4/10)  
**Channel date:** 2026-10-01 (Asia/Bangkok)  
**Platform:** Web app (mobile-first) + PWA  
**Language:** Thai UI first, English secondary  
**Status:** Delivery-ready for official morning run  
**Related docs:** `README.md`, `prompts.md`, `schemas.json`, `examples.json`  
**Last updated:** 2026-10-01 (Asia/Bangkok)

---

## 1. สรุปสั้นๆ

แอปมินิสวีทให้นักเรียนไทยถ่ายหรืออัปโหลดรูปโน้ต / สไลด์ / ใบข้อสอบเก่า → AI/mock แตกเป็นแฟลชการ์ด Q&A ภาษาไทย → บันทึกเป็นเด็คตามวิชา → ทวนแบบสไวป์ (รู้แล้ว / ยังไม่ชัวร์) → ดูแดชบอร์ด % ชำนาญ + due วันนี้ + สตรีค → แชร์การ์ดความคืบหน้าสวยๆ ไป IG หรือ LINE

ออกแบบให้เดโมใน Reel 15–30 วินาทีเห็นรูปโน้ต→กองการ์ดชัด และมีฟีเจอร์รองที่ดึงคนกลับมาเปิดซ้ำก่อนสอบ (Swipe Quiz, Deck Library, Mastery Dashboard, streak share)

MVP ไม่มีบัญชีผู้ใช้ ไม่เคลม「สอบผ่านชัวร์」 ไม่เป็นเฉลยข้อสอบสด ไม่มีโซเชียลฟีด ไม่มี Anki sync

---

## 2. ปัญหาที่แก้

| ปัญหาวันนี้ | ผลกระทบ |
|---|---|
| ถ่ายโน้ต/สไลด์เก็บในแกลเลอรีแล้วไม่เคยทวน | ความรู้หายก่อนสอบ รูปกองเป็นขยะ |
| Anki / Quizlet UI หนัก ตั้งค่าเยอะ ภาษาไทยรองรับไม่สนุก | นักเรียนเลิกใช้หลัง 1–2 วัน |
| พิมพ์การ์ดเองช้ามากหลังเลิกเรียน | ไม่สร้างเด็คตั้งแต่แรก |
| แอปติว B2B / LMS โรงเรียน | ไม่เหมาะเดโม Reel 15–30 วินาที และคนทั่วไปไม่ติดตั้ง |
| ไม่มีภาพความคืบหน้าสวยๆ ให้แชร์เพื่อน | ไม่มีแรงใจเปิดซ้ำ / ไม่ไวรัล |

**โอกาสช่อง AI วันละแอป:** แจกแอปฟรีที่ผลลัพธ์เห็นทันทีหลังถ่ายโน้ต → save rate สูง → คนเข้าลิงก์ลองตอนอ่านหนังสือจริง → ติดตามเพื่อรอแอปวันถัดไป

---

## 3. เป้าหมายผลิตภัณฑ์

### 3.1 Goals (MVP / วันเดียว + คลิปเช้า)

1. Happy path จบบนมือถือ: อัปโหลด/ถ่ายโน้ต (หรือโหลด fixture) → extract cards → ยืนยันเด็ค → Swipe Quiz → แดชบอร์ดอัปเดต → แชร์การ์ด ภายใน **≤ 60 วินาที** สำหรับผู้ใช้ทั่วไป
2. มี **≥ 5 ฟีเจอร์ must-have** ที่ใช้ได้จริงและโชว์ในคลิปได้อย่างน้อย 3 ตัว
3. Demo note fixture คุณภาพดีอย่างน้อย **1 ชุด** (ชีวะ「ระบบหายใจ」) พร้อม mock extract 6–8 การ์ด
4. ข้อความ Q&A ใน fixture สอดคล้องกับตัวอย่างใน `examples.json` (เครื่องมือทวน — ไม่ใช่เฉลยข้อสอบสด)
5. คลิป Reel 25–35 วินาทีถ่ายจบด้วย UI จริง ไม่ใช่ mock อย่างเดียว

### 3.2 Non-goals (MVP)

- ไม่มีระบบล็อกอิน / คลาวด์ซิงก์เด็ค
- ไม่เคลม「สอบผ่านชัวร์」/ คะแนนเพิ่มขึ้น / เฉลยข้อสอบสดระหว่างสอบ
- ไม่โฟกัส Anki import/export หรือ spaced-repetition อัลกอริทึมหนักใน MVP (ใช้ mastery ง่ายๆ พอ)
- ไม่มี native iOS/Android store build
- ไม่มีโซเชียลฟีด / แข่งเพื่อน / leaderboard คะแนนสอบ
- ไม่บังคับ Vision API จริง — `mock_demo` คุณภาพดีพอสำหรับเดโมและคลิป
- ไม่มี paid tutor / แชทติวเตอร์

---

## 4. ผู้ใช้และบทบาท

| บทบาท | ความต้องการหลัก |
|---|---|
| **นักเรียนม.ปลาย / มหาวิทยาลัย (หลัก)** | ถ่ายโน้ตได้การ์ดทวนเร็ว ไม่ต้องพิมพ์เอง |
| **คนเตรียมสอบเข้า / กพ / ใบขับขี่ ฯลฯ** | มีเด็คแยกวิชา + เห็น due วันนี้ชัด |
| **ผู้ชมช่อง AI วันละแอป** | เห็น wow รูปโน้ต→กองการ์ด ใน 3 วินาที อยากลองลิงก์ในไบโอ |
| **ผู้สร้างคลิป (เรา)** | gen แอปใน 1 วัน มีสคริปต์ช็อตและเช็คลิสต์พร้อมถ่าย |

---

## 5. User stories

1. ในฐานะผู้ใช้ ฉันถ่ายหรืออัปโหลดรูปโน้ตแล้วได้การ์ด Q&A ภาษาไทยหลายใบภายในไม่กี่วินาที
2. ในฐานะผู้ใช้ ฉันแก้คำถาม/คำตอบก่อนบันทึกเป็นเด็คได้
3. ในฐานะผู้ใช้ ฉันทวนด้วยสไวป์/แตะ「รู้แล้ว」หรือ「ยังไม่ชัวร์」และเห็นสตรีค
4. ในฐานะผู้ใช้ ฉันจัดเด็คเป็นโฟลเดอร์วิชา (คณิต อังกฤษ ชีวะ ประวัติ) สร้าง/เปลี่ยนชื่อได้
5. ในฐานะผู้ใช้ ฉันเห็น % ชำนาญ, จำนวน due วันนี้, และวงแหวนสตรีคบนแดชบอร์ด
6. ในฐานะผู้ใช้ ฉันแชร์การ์ดสตรีค/ความคืบหน้าเด็คเป็นรูป + คัดลอกแคปชัน IG/LINE ได้
7. ในฐานะผู้ชม Reel ฉันเห็นรูปโน้ต→กองการ์ดใน 3 วินาทีแรกแล้วอยากลองแอป
8. ในฐานะระบบ ทุกการ์ด/เด็ค/เซสชันต้องเก็บตาม `Flashcard`, `Deck`, `StudySession` ใน `LocalStore`

---

## 6. ฮุค Reel (3 วินาทีแรก)

**Before:** รูปโน้ตชีวะมือเขียน/สไลด์เบลอเล็กน้อย + คนสงสัย「ทวนยังไงดี」  
**After:** กองการ์ด Q&A สี indigo — คำถามไทยใหญ่ + พลิกเห็นคำตอบ  
**ข้อความบนจอ:** `ถ่ายโน้ต/ข้อสอบ → ได้เด็คทวนทันที ใน 10 วินาที`  
**เสียง:** 「ถ่ายโน้ตใบเดียว ได้เด็คทวนทันที」

**Wow moment กลางคลิป:** รูปโน้ตธรรมดา → กองการ์ดโผล่ → สไวป์ทวน → แดชบอร์ด % ชำนาญกระโดด → กดแชร์การ์ดสตรีค

---

## 7. ทำไมคนติดตาม / เปิดซ้ำ

- ผลรูปโน้ต→การ์ดทันที (เหมาะ Reel + save)
- ใช้จริงได้ทุกคืนก่อนสอบ / ระหว่างพักเที่ยง
- แจกฟรีจากช่อง → เซฟคลิป + เข้าลิงก์
- รีเทนชัน: Swipe Quiz, Deck Library, Mastery Dashboard, Share Study Card, streak
- คอมเมนต์「เด็ค」= สัญญาณทำคลิปต่อ / ขอฟีเจอร์เพิ่ม

---

## 8. กฎผลิตภัณฑ์ช่อง

- **ขั้นต่ำ 5 ฟีเจอร์** must-have (ตารางด้านล่าง)
- Gen ได้ใน 1 วันด้วย AI codegen (Next.js + extract pluggable)
- เดโมหลักจบในมือถือแนวตั้ง (~390px)
- UI สวย พอเป็นพรีวิว “แอปจริง” ไม่ใช่ฟอร์มดิบ
- ภาษาไทยก่อน — คีย์สคีมาภาษาอังกฤษได้
- โทนเรียนสนุก ไม่เครียด — ใช้คำว่า「เครื่องมือทวน / ฝึกจำ」ชัดเจน ห้าม「สอบผ่านชัวร์」

---

## 9. ฟีเจอร์

### 9.1 Must-have (≥ 5)

| # | ฟีเจอร์ | รายละเอียด | Acceptance ย่อ |
|---|---|---|---|
| 1 | **Photo → Cards** | ถ่าย/อัปโหลดโน้ต → ได้ Q&A flashcards; default engine `mock_demo` + ช่องเสียบ vision API; ปุ่ม「ใช้รูปเดโม」 | fixture เดโมขึ้น 6–8 การ์ดใน ≤2s |
| 2 | **Swipe Quiz** | โหมดทวน: พลิกการ์ด, สไวป์/แตะ รู้แล้ว / ยังไม่ชัวร์ + สตรีคฟีดแบ็ก | ทวน ≥3 การ์ดแล้ว mastery อัปเดต |
| 3 | **Deck Library** | โฟลเดอร์วิชา + สร้าง/เปลี่ยนชื่อเด็ค + นับจำนวนการ์ด | มี ≥4 วิชาตัวอย่าง + สร้างเด็คใหม่ได้ |
| 4 | **Mastery Dashboard** | % mastered, due-today, study streak rings/bars | หลังควิซ rings/% อัปเดตทันที |
| 5 | **Share Study Card** | รูปการ์ดสตรีค/ความคืบหน้า + แคปชันคัดลอก IG/LINE + share sheet | ได้รูป+ข้อความบน iPhone Safari |

### 9.2 Nice-to-have

| # | ฟีเจอร์ | รายละเอียด |
|---|---|---|
| 6 | **Paste Text → Cards** | วางข้อความโน้ต → แตก Q&A โดยไม่ต้องถ่ายรูป |
| 7 | **Multi-choice mode** | โหมดตัวเลือก 4 ข้อจากการ์ดเดิม (สร้างตัวลวงง่ายๆ) |
| 8 | **Exam countdown timer** | นับถอยหลังวันสอบต่อเด็ค |
| 9 | **Voice read question** | อ่านคำถามด้วย speechSynthesis ภาษาไทย |
| 10 | **Dark study mode** | ธีมมืดสำหรับทวนกลางคืน |
| 11 | **Offline history** | ประวัติเซสชันทวนใน localStorage หลังโหลดครั้งแรก |

---

## 10. ขอบเขตฟีเจอร์

### 10.1 In scope

- Home, Photo Upload, Extract Confirm, Swipe Quiz, Deck Library, Mastery Dashboard, Share sheet
- Extract engine pluggable: `mock_demo` (default) · optional `vision_api` ผ่าน env
- Mastery engine ใน `lib/mastery.ts` (pure functions — ง่าย: known / unsure counts)
- Share card render บน Canvas / DOM-to-image
- Analytics events ฝั่ง client (optional log)
- PWA ติดตั้งได้แบบพื้นฐาน (manifest + icons)
- Disclaimer UI: 「ExamDeck เป็นเครื่องมือทวนและฝึกจำ ไม่ใช่เฉลยข้อสอบสดหรือรับประกันผลสอบ」

### 10.2 Out of scope (เฟสถัดไป)

- Auth / cloud sync เด็ค
- Anki .apkg import/export / FSRS เต็มรูปแบบ
- เฉลยข้อสอบสด / แชร์คำตอบระหว่างสอบ
- โซเชียลฟีด / follow เพื่อน / ranking คะแนนสอบ
- Paid tutor / แชทติวเตอร์
- ฝึกโมเดล OCR/vision เอง

---

## 11. User flow หลัก (Happy path)

```text
เปิดแอป → ถ่ายหรืออัปโหลดรูปโน้ต (หรือกด「ใช้รูปเดโม」)
  → Extract / mock parse (progress สวย เป้า ≤ 2s สำหรับ fixture)
  → ดูผล: กองการ์ด Q&A 6–8 ใบ พลิกพรีวิวได้ แก้ข้อความได้
  → ตั้งชื่อเด็ค + เลือกวิชา แล้วกดบันทึก
  → เข้า Swipe Quiz: พลิก → รู้แล้ว / ยังไม่ชัวร์
  → Mastery Dashboard อัปเดต % / due / streak
  → แชร์การ์ดสตรีค / คัดลอกแคปชัน / เปิด share sheet
  → กลับมาทวนเด็คอื่นจาก Deck Library
```

### สถานะเซสชัน extract / ทวน

`idle` → `extracting` → `confirming` → `saved` → `quizzing` → `sharing`  
ทางแยก: `error` (พร้อมข้อความไทยสั้นๆ + ปุ่มลองใหม่ / วางข้อความ)

---

## 12. หน้าจอ (MVP)

| # | หน้าจอ | องค์ประกอบหลัก |
|---|---|---|
| 1 | **Home** | โลโก้, หัวข้อไทย, แถบเดโมรูปโน้ต→กองการ์ด, CTA「ถ่ายโน้ต」, แถบ 5 ฟีเจอร์ไอคอน, ปุ่มรอง「ใช้รูปเดโม」, ลิงก์ไปแดชบอร์ด |
| 2 | **Photo / Upload** | ช่องกล้อง/ไฟล์, ปุ่มรูปเดโม, progress extract, พรีวิวรูปใหญ่ |
| 3 | **Extract Confirm** | กองการ์ดพรีวิว (พลิกได้), แก้ Q/A, ตั้งชื่อเด็ค+วิชา, ปุ่ม「บันทึกเด็ค」 |
| 4 | **Swipe Quiz** | การ์ดใหญ่พลิก, ปุ่ม/สไวป์ รู้แล้ว · ยังไม่ชัวร์, แถบความคืบหน้าเซสชัน, สตรีค |
| 5 | **Deck Library** | โฟลเดอร์วิชา, รายการเด็ค, สร้าง/เปลี่ยนชื่อ, นับการ์ด |
| 6 | **Mastery Dashboard** | % mastered, due วันนี้, วงแหวน/แถบสตรีค, ทางลัดทวน |
| 7 | **Share sheet** | พรีวิวการ์ดสตรีค/ความคืบหน้า, คัดลอกแคปชัน, แชร์ระบบ |
| 8 | **Paste / Multi / Dark** (nice) | วางข้อความ, โหมดตัวเลือก, ธีมมืด |

**โทนแบรนด์:** พื้นขาว/off-white (#FAFAF9), ไฮไลต์ indigo/violet (#4F46E5 / #6366F1), amber accent (#F59E0B), การ์ดขาวมุมมน, ตัวอักษรคำถามไทยใหญ่, ปุ่ม primary ใหญ่ — โทน “study focus vibe” ที่ถ่าย Reel แล้วอ่านง่าย ไม่ดาร์กบังคับ ไม่เครียด

---

## 13. ความต้องการเชิงฟังก์ชัน

### FR-1 Photo → Cards
- รับไฟล์ภาพจากไฟล์หรือกล้อง
- รัน engine ตาม `extract_engine` (ค่าเริ่ม `mock_demo`)
- มีปุ่ม「ใช้รูปเดโม」โหลด fixture จาก `/fixtures/demo-note.json` (+ ภาพใน `/public/fixtures/`)
- เก็บ `extract_ms`, confidence, cards[] ใน `PhotoExtractResult`
- ถ้า extract ล้มเหลว: ให้วางข้อความ (nice) หรือสร้างการ์ดว่างมือได้
- แสดง disclaimer เครื่องมือทวนใกล้ผลลัพธ์

### FR-2 Swipe Quiz
- โหลดการ์ดจากเด็คที่เลือก (หรือ due วันนี้)
- พลิกการ์ดด้วยแตะกลาง / ปุ่ม「ดูคำตอบ」
- สไวป์ขวาหรือปุ่ม「รู้แล้ว」→ `known`; สไวป์ซ้ายหรือ「ยังไม่ชัวร์」→ `unsure`
- อัปเดต `QuizAnswer` + สรุปเซสชัน `StudySession`
- แสดงสตรีคฟีดแบ็กสั้นๆ หลังตอบถูกต่อเนื่อง (เช่น「ต่อเนื่อง 3 ใบ!」)

### FR-3 Deck Library
- วิชาพรีเซ็ต: คณิต, อังกฤษ, ชีวะ, ประวัติ, ฟิสิกส์, อื่นๆ
- สร้างเด็คใหม่ / เปลี่ยนชื่อ / ลบ (ยืนยันก่อนลบ)
- แสดงจำนวนการ์ด + % mastered ต่อเด็ค
- แตะเด็คแล้วเลือก「ทวน」หรือ「ดูการ์ด」

### FR-4 Mastery Dashboard
- คำนวณ `MasteryStats`: total_cards, mastered_count, mastery_pct, due_today, streak_days
- วงแหวน mastery + แถบ due / streak
- ทางลัด「ทวน due วันนี้」
- หลังจบเซสชันต้อง recalculate < 100ms

### FR-5 Share Study Card
- เรนเดอร์การ์ดสรุปสตรีค/เด็คเป็น PNG (Canvas หรือ html-to-image)
- แสดง: ชื่อเด็ค, % ชำนาญ, จำนวนการ์ดทวนวันนี้, streak, โทน indigo+amber
- สร้างแคปชันไทยสำหรับ IG/LINE ตามเทมเพลต
- `navigator.share` ถ้ามี + fallback คัดลอก/ดาวน์โหลด
- ห้ามใส่「สอบผ่านชัวร์」/ คะแนนปลอม / ชื่อโรงเรียนจริงโดยไม่จำเป็น

### FR-6 Local retention
- บันทึก decks + cards + sessions + settings ตาม `LocalStore`
- ไม่บังคับ auth; ใช้ได้หลังโหลดครั้งแรกแบบออฟไลน์ (cache หน้า)

### FR-7 Analytics (เบา)
- ยิงอีเวนต์ตาม enum ใน schema (console หรือ provider ภายหลัง)

### FR-8 Safety copy
- ทุกจุดที่โชว์ผล extract ต้องเข้าถึง disclaimer ได้
- หลีกเลี่ยงคำว่า「สอบผ่านชัวร์」「เฉลยข้อสอบ」「โกงสอบ」ใน UI หลัก

---

## 14. ความต้องการเชิงไม่ใช่ฟังก์ชัน

| หัวข้อ | เป้า |
|---|---|
| Extract / mock latency (fixture) | p50 ≤ 2s |
| Mastery recalc | อัปเดต < 100ms หลังจบการ์ดหรือเซสชัน |
| Mobile layout | ใช้งานได้ที่ 390×844 โดยไม่เลื่อนแนวนอนพัง |
| ภาษา | th-TH เป็นค่าเริ่มต้น |
| ความเป็นส่วนตัว | ประมวลผลรูปฝั่ง client เป็นหลัก ไม่อัปโหลดเซิร์ฟเวอร์ถ้าไม่ใช้ vision API |
| Deploy | Vercel preview URL พร้อมแชร์ในไบโอ |
| การ์ด | ตัวอักษรคำถามอ่านชัดบน Reel; ปุ่มสไวป์นิ้วใหญ่ |
| Accessibility เบา | ปุ่มใหญ่ คอนทราสต์ข้อความบน Reel ผ่านตาเปล่า |

---

## 15. Tech แนะนำสำหรับ gen วันเดียว

| ชั้น | เลือก |
|---|---|
| Frontend | Next.js 14 (App Router) + TypeScript + Tailwind + shadcn/ui |
| Extract | `mock_demo` default · optional vision API ผ่าน env |
| Mastery engine | `lib/mastery.ts` (pure) + `lib/quiz.ts` |
| Share | Canvas / `html-to-image` + `lib/share.ts` |
| State | React state + `lib/storage.ts` (localStorage) |
| Fixtures | `/public/fixtures/demo-note.json` (+ ภาพโน้ตเดโม) |
| Subjects | `/data/subjects.json` หรือฝังใน `lib/subjects.ts` |
| Deploy | Vercel |

**โครงสร้างรีโปแนะนำ**

```text
/examdeck
  README.md
  prd.md
  prompts.md
  schemas.json
  examples.json
  /app
  /components
  /lib
    extract.ts
    mastery.ts
    quiz.ts
    share.ts
    storage.ts
    subjects.ts
  /public/fixtures
  /data
```

ถ้าไม่มี Vision API key: ใช้ `mock_demo` + ปุ่มรูปเดโมเป็นหลัก แล้วหมายเหตุใน UI ว่า「โหมดเดโม — ใส่รูปจริงได้เมื่อเปิด Vision」

---

## 16. ข้อมูลและสคีมา

แหล่งความจริง (ดูรายละเอียดใน `schemas.json` / ตัวอย่างใน `examples.json`):

- `Flashcard` / `Deck` / `SubjectFolder`
- `StudySession` / `QuizAnswer` / `MasteryStats`
- `PhotoExtractResult` / `ShareCard` / `SharePayload`
- `LocalStore` / `AnalyticsEvent`
- `FeatureChecklist` / `UiCopyTh` / `ReelScript`
- `ExtractEngine` / `CardStatus` / `AnswerVerdict`

---

## 17. Analytics / สำเร็จของแอปในช่อง

**Primary (ผลิตภัณฑ์):** % เซสชันที่ทำ `deck_saved` อย่างน้อย 1 ครั้ง และ/หรือ `quiz_session_completed` / `share_success`  
**Primary (ช่อง):** save rate ของ Reel + จำนวนคอมเมนต์「เด็ค」

**Secondary:**
- `extract_success` rate / median `extract_ms`
- จำนวนการ์ดต่อเด็คเฉลี่ย
- การใช้ Swipe Quiz vs แค่ดูการ์ด
- การเปิด Share card

**Guardrail:** อัตรา `extract_fail`, คอมเมนต์บ่นว่าแอป「โกงสอบ」หรือ「รับประกันผ่าน」, UI ที่ทำให้เครียดเกิน

---

## 18. Reel shot list (25–35 วินาที)

| เวลา | ภาพ | ข้อความบนจอ | เสียงพูด |
|---|---|---|---|
| 0–3s | รูปโน้ตเบลอ → กองการ์ด | ถ่ายแล้วได้เด็ค | ถ่ายโน้ตใบเดียว ได้เด็คทวนทันที |
| 3–8s | มอนทาจ gen / โลโก้ | สร้างด้วย AI วันนี้ | วันนี้ทำแอป ExamDeck สดๆ |
| 8–14s | อัปโหลดรูป → extract → การ์ดโผล่ | Photo → Cards | ถ่ายโน้ตชีวะ ระบบหายใจ ได้การ์ดเลย |
| 14–22s | สไวป์ทวน + แดชบอร์ด % | Swipe Quiz · Mastery | สไวป์รู้แล้ว ดูความชำนาญอัปเดต |
| 22–28s | Deck Library เร็วๆ + Share card | เด็คตามวิชา แชร์ได้ | มีไลบรารีวิชาและแชร์การ์ดสวย |
| 28–35s | ผลสุดท้าย + ลิงก์ | ลิงก์ในไบโอ | ลองฟรีที่ลิงก์ในไบโอ แล้วคอมเมนต์「เด็ค」 |

รายละเอียดช็อตเต็มใน `examples.json` → `reel_script_th`

---

## 19. ความเสี่ยง

| ความเสี่ยง | แผนลดความเสี่ยง |
|---|---|
| คนเข้าใจว่าเป็นเฉลยข้อสอบสด / โกงสอบ | Disclaimer ชัดทุกจุด + คัดก็อปปี้「เครื่องมือทวน」— **ห้ามเคลมสอบผ่าน** |
| Vision จริงอ่านลายมือไทยผิด / รูปมืด | ใช้ mock_demo เป็นฮุค Reel หลัก + ให้แก้ Q/A ก่อนบันทึกได้ |
| Anki users คาด FSRS เต็ม | วางตำแหน่งเป็น「ทวนเร็วสวย」ไม่ใช่ทดแทน Anki; mastery ง่ายพอสำหรับ MVP |
| เดโมใช้รูปข้อสอบจริงที่มีลิขสิทธิ์ข้อสอบวัดผล | ใช้ fixture โน้ตสมมติ「ระบบหายใจ」ที่สร้างเอง |
| มือถือเครื่องอ่อนเรนเดอร์การ์ดช้า | การ์ดเรียบๆ indigo+amber ไม่ใส่เอฟเฟกต์หนัก |
| ผู้ใช้คาดหวังซิงก์ข้ามเครื่อง | บอกชัดใน MVP ว่าเก็บในเครื่อง (localStorage) |

---

## 20. แผนส่งมอบวันเดียว (สำหรับคลิป)

| ช่วง | งาน |
|---|---|
| เช้า | Gen โครง Next.js + Home/Upload/Confirm ตาม Master prompt |
| สาย | mock extract + demo fixture ระบบหายใจ 7 การ์ด + Deck Library พื้นฐาน |
| บ่าย | Swipe Quiz + Mastery Dashboard + Share Study Card |
| เย็น | QA ตามตัวอย่าง + ถ่าย Reel ตาม shot list + อัป Vercel + ใส่ลิงก์ไบโอ |

---

## 21. Open questions

1. Mastery ง่ายแบบ known≥2 ครั้งติด = mastered พอไหม หรือจะใส่ due interval แบบคร่าวๆ (1/3/7 วัน) ใน MVP?
2. รอบถัดไปต่อ Vision/OCR จริงคุ้มไหมสำหรับคลิป หรือพอ mock_demo + Paste Text?
3. เก็บ analytics แค่ console หรือต่อ Plausible/PostHog ตั้งแต่วันที่ 4?

---

## 22. Acceptance criteria (ผ่านก่อนลงคลิป)

- [ ] ปุ่มรูปเดโมโหลดผล extract การ์ด Q&A ไทย 6–8 ใบตาม fixture
- [ ] แก้ Q/A + ตั้งชื่อเด็ค/วิชา แล้วบันทึกได้
- [ ] Swipe Quiz: พลิก + รู้แล้ว/ยังไม่ชัวร์ อัปเดตเซสชัน
- [ ] Mastery Dashboard (% / due / streak) อัปเดตหลังควิซ
- [ ] Deck Library มีโฟลเดอร์วิชาตัวอย่าง + สร้าง/เปลี่ยนชื่อเด็คได้
- [ ] Share ได้รูปการ์ด + คัดลอกแคปชัน + share sheet (หรือ fallback)
- [ ] มี ≥ 5 ฟีเจอร์ must ตามตาราง และติ๊กใน `FeatureChecklist`
- [ ] มือถือ 390px ใช้งานได้ไม่เละ การ์ดใหญ่ อ่านคำถามบน Reel ได้
- [ ] สคริปต์ Reel ถ่ายครบช็อต + CTA「เด็ค」ชัด
- [ ] มี disclaimer เครื่องมือทวน และไม่มีเคลมสอบผ่าน / เฉลยข้อสอบสดใน UI หลัก

---

## 23. รายละเอียด Mastery และการทวน (สำหรับ engine)

### 23.1 สถานะการ์ด
- `new` — ยังไม่เคยทวน
- `learning` — เคยตอบ unsure หรือ known ยังไม่ถึงเกณฑ์
- `mastered` — known ติดกัน ≥ 2 ครั้งในเซสชันล่าสุด (ค่าเริ่ม MVP; ปรับได้ใน settings เบาๆ)
- `due` — ถึงเวลาทวนซ้ำ (nice: interval 1/3/7 วัน; MVP อาจนับ unsure ทั้งหมดเป็น due)

### 23.2 ลำดับคำนวณ MasteryStats
1. รวบรวม `Flashcard` ของผู้ใช้ (ทั้งแอปหรือต่อเด็ค)
2. `mastered_count` = จำนวนที่ status == mastered
3. `mastery_pct = round(mastered_count / max(1,total_cards) * 100)`
4. `due_today` = จำนวน new + learning ที่ควรทวนวันนี้
5. `streak_days` = วันติดต่อกันที่มี StudySession ≥1 (Asia/Bangkok)

### 23.3 ความไม่แน่นอนของ extract
- `PhotoExtractResult.confidence` 0–1; ถ้า < 0.55 แนะนำให้แก้การ์ดทีละใบหรือวางข้อความ
- อนุญาตให้แก้ `question_th` / `answer_th` ก่อนบันทึก
- ห้ามซ่อนว่าเป็นเครื่องมือทวนอัตโนมัติที่อาจผิด

### 23.4 ตัวอย่างเดโมหลัก (ต้องตรง examples)
- วิชา: ชีวะ · หัวข้อ: ระบบหายใจ (ม.ปลาย)
- จำนวนการ์ด: 7 ใบ Q&A ภาษาไทย
- ใช้เป็น fixture ฮุค Reel และทดสอบ mastery recalc

---

## 24. สำเนาแบรนด์และไมโครคัดก็อปปี้

| จุด | ทิศทางสำเนา |
|---|---|
| Home | สด สั้น ชวนถ่ายโน้ต ไม่ขายคอร์สติว |
| หลัง extract | 「ได้เด็คทวนแล้ว — แก้คำถามก่อนบันทึกได้」 |
| หลัง unsure | 「โอเค เก็บไว้ทวนอีกครั้ง」 ไม่ใช้「โง่」「อ่อน」 |
| สตรีค | 「ทวนต่อเนื่อง X วันแล้ว สุดยอด」 แบบเพื่อน |
| Disclaimer | 「ExamDeck เป็นเครื่องมือทวนและฝึกจำ ไม่ใช่เฉลยข้อสอบสดหรือรับประกันผลสอบ」 |

สีหลักในโค้ด (แนะนำ CSS variables):

```text
--bg: #FAFAF9;
--card: #FFFFFF;
--primary: #4F46E5;
--primary-soft: #EEF2FF;
--accent: #F59E0B;
--accent-soft: #FEF3C7;
--ink: #1E1B4B;
--muted: #64748B;
```

---

## 25. ภาคผนวก — สำเนาแพ็ก

แหล่งหลัก:

```text
/workspace/ai-wanla-app/2026-10-01-examdeck/
  README.md
  prd.md
  prompts.md
  schemas.json
  examples.json
```

Zip ในโฟลเดอร์: `/workspace/ai-wanla-app/2026-10-01-examdeck/examdeck.zip`  
Zip ราก: `/workspace/examdeck.zip` (unzip แล้วได้ `examdeck/...`)

---

## 26. รายละเอียดหน้าจอและคอมโพเนนต์ (สำหรับ codegen)

### 26.1 Home
- Hero หัวข้อไทย + คำบรรยาย 1 บรรทัด
- Demo strip แนวนอน 3 เฟรม: รูปโน้ต → กองการ์ด → Swipe Quiz
- Primary CTA `ถ่ายโน้ต` / Secondary `ใช้รูปเดโม`
- แถวไอคอน 5 ฟีเจอร์ must
- ลิงก์ข้อความ `ดูความชำนาญ` ไป Dashboard
- Footer disclaimer หนึ่งบรรทัด

### 26.2 Photo / Upload
- พื้นที่พรีวิวสูงอย่างน้อย ~45vh
- ปุ่มเปิดกล้อง / เลือกไฟล์ / ใช้รูปเดโม
- Progress bar หรือ skeleton กองการ์ดตอน `extracting`
- ถ้า error: ปุ่มลองใหม่ + วางข้อความ (nice)

### 26.3 Extract Confirm
- กองการ์ดพรีวิวเลื่อนได้ พลิกหน้า/หลัง
- แก้ question_th / answer_th ได้
- ช่องชื่อเด็ค + เลือกวิชา chips
- Disclaimer ใต้กองการ์ด
- CTA บันทึกเด็คนี้

### 26.4 Swipe Quiz
- การ์ดใหญ่กลางจอ (~70% ความสูง usable)
- แตะเพื่อพลิก
- ปุ่มล่าง: ยังไม่ชัวร์ (ซ้าย) · รู้แล้ว (ขวา) — หรือสไวป์
- แถบ progress เซสชัน + สตรีคเล็กๆ มุมบน

### 26.5 Deck Library
- แท็บ/ชิปวิชา
- การ์ดเด็ค: ชื่อ · จำนวนการ์ด · % mastered · ปุ่มทวน
- FAB สร้างเด็ค / ถ่ายโน้ต

### 26.6 Mastery Dashboard
- วงแหวน % ชำนาญ
- ชิป due วันนี้ + สตรีควัน
- รายการเด็คล่าสุดที่ทวน
- ปุ่มแชร์มุมขวา

### 26.7 Share sheet
- พรีวิวการ์ด
- คัดลอกแคปชัน
- แชร์ระบบ / ดาวน์โหลดรูป
- ข้อความว่าไม่เก็บรูปบนเซิร์ฟเวอร์ใน MVP

---

## 27. เกณฑ์คุณภาพ Reel (ช่อง)

1. ฮุค 3 วินาทีแรกต้องเห็นการเปลี่ยนรูป→กองการ์ด ไม่ใช่โลโก้ยาว
2. ในคลิปเดียวโชว์ ≥3 ฟีเจอร์ must
3. UI จริงจากบิลด์ที่ deploy ไม่ใช่แค่ Figma
4. พูดหรือติดข้อความ「เครื่องมือทวน」อย่างน้อย 1 ครั้ง
5. CTA ปิดคลิป: ลิงก์ในไบโอ + คอมเมนต์「เด็ค」
6. ห้ามใช้เพลง/ฟุตเทจที่เสี่ยงลิขสิทธิ์หนักโดยไม่จำเป็น — โฟกัสหน้าจอแอป

---

## 28. ค่าเริ่มต้นที่ล็อกสำหรับเดโมเช้านี้

| ค่า | ค่าเริ่ม |
|---|---|
| Extract engine | `mock_demo` |
| Hero fixture | ชีวะ ระบบหายใจ · 7 การ์ด |
| ความกว้าง UI ฐาน | 390px |
| คำคอมเมนต์ CTA | เด็ค |
| localStorage key | `examdeck.v1` |
| ภาษา UI | th-TH |
| สีหลัก | indigo `#4F46E5` + amber `#F59E0B` + bg `#FAFAF9` |
| Mastered rule (MVP) | known ติดกัน ≥ 2 ครั้ง |

ค่าเหล่านี้ต้องตรงกับ `examples.json` เพื่อให้ QA เทียบได้เร็วตอนเย็นก่อนขึ้นคลิป
