# PRD: ReplyKit

**Product name:** ReplyKit  
**Tagline (TH):** วางข้อความแชท → ได้ชุดตอบหลายโทน ใน 10 วินาที  
**Tagline (EN):** Paste an awkward chat → instant multi-tone reply pack  
**Version:** 1.0 (MVP — AI-วันละแอป Day 5/10)  
**Channel date:** 2026-10-02 (Asia/Bangkok)  
**Platform:** Web app (mobile-first) + PWA  
**Language:** Thai UI first, English secondary  
**Status:** Delivery-ready for official morning run  
**Related docs:** `README.md`, `prompts.md`, `schemas.json`, `examples.json`  
**Last updated:** 2026-10-02 (Asia/Bangkok)

---

## 1. สรุปสั้นๆ

แอปมินิสวีทให้คนไทยวางหรืออัปโหลดข้อความแชท / คอมเมนต์ / DM ที่ตอบยาก → AI/mock สร้างชุดตอบพร้อมใช้หลายโทน (นุ่ม / ตลก / มืออาชีพ / หนักแน่น / อบอุ่น) → หมุน Tone Dial กรองหรือ regen → เก็บสถานการณ์บ่อยๆ ใน Situation Library → อัปโหลดสกรีนช็อตแล้ว mock ดึงข้อความ inbound ล่าสุด → คัดลอกหนึ่งแตะ + แชร์การ์ดตอบสวยไป IG หรือ LINE

ออกแบบให้เดโมใน Reel 15–30 วินาทีเห็นวางข้อความ→ชุดตอบหลายโทนชัด และมีฟีเจอร์รองที่ดึงคนกลับมาเปิดซ้ำเมื่อเจอแชทอึดอัด (Tone Dial, Situation Library, Screenshot Extract, Share Reply Card)

MVP ไม่มีบัญชีผู้ใช้ ไม่เคลม「AI รู้ความสัมพันธ์」 ไม่ส่งข้อความแทนผู้ใช้ ไม่มีโซเชียลฟีด ไม่มี sync กับ LINE API จริง

---

## 2. ปัญหาที่แก้

| ปัญหาวันนี้ | ผลกระทบ |
|---|---|
| อ่านแชทแล้วค้างพิมพ์นาน ไม่รู้จะเปิดยังไง | ความสัมพันธ์ฝืด / งานค้าง / เครียด |
| ChatGPT ทั่วไปต้องเขียนพรอมต์ยาวทุกครั้ง | คนเลิกใช้ตอนมือถือมือเดียว |
| เทมเพลตตอบสำเร็จรูปไม่เข้าโทนไทย / ไม่ตรงสถานการณ์ | ดูแข็งหรือดูปลอม |
| แอปแชทช่วยพิมพ์ของต่างประเทศ UI หนัก ภาษาไทยรองรับไม่สนุก | เลิกใช้หลัง 1–2 ครั้ง |
| ไม่มีภาพการ์ดตอบสวยๆ ให้แชร์เพื่อน | ไม่มีไวรัล / ไม่มีแรงเปิดซ้ำ |

**โอกาสช่อง AI วันละแอป:** แจกแอปฟรีที่ผลลัพธ์เห็นทันทีหลังวางข้อความ → save rate สูง → คนเข้าลิงก์ลองตอนเจอแชทจริง → ติดตามเพื่อรอแอปวันถัดไป

---

## 3. เป้าหมายผลิตภัณฑ์

### 3.1 Goals (MVP / วันเดียว + คลิปเช้า)

1. Happy path จบบนมือถือ: วางข้อความ (หรือโหลด fixture) → ได้ Reply Pack → Tone Dial → (ออปชัน) Situation save → Copy/Share ภายใน **≤ 60 วินาที** สำหรับผู้ใช้ทั่วไป
2. มี **≥ 5 ฟีเจอร์ must-have** ที่ใช้ได้จริงและโชว์ในคลิปได้อย่างน้อย 3 ตัว
3. Demo chat fixture คุณภาพดีอย่างน้อย **1 ชุด** (เพื่อนเงียบ 3 วันเรื่องวันเสาร์) พร้อม mock replies 4–5 โทน
4. ข้อความตอบใน fixture สอดคล้องกับตัวอย่างใน `examples.json` (ตัวช่วยร่าง — ไม่ใช่ส่งแทน)
5. คลิป Reel 25–35 วินาทีถ่ายจบด้วย UI จริง ไม่ใช่ mock อย่างเดียว

### 3.2 Non-goals (MVP)

- ไม่มีระบบล็อกอิน / คลาวด์ซิงก์แพ็ก
- ไม่เคลม「AI รู้ความสัมพันธ์」/ 「ตอบแทนคุณได้ 100%」/ ส่งข้อความเข้า LINE จริง
- ไม่โฟกัส translation เต็มรูปแบบหรือ agent แชทยาวใน MVP
- ไม่มี native iOS/Android store build
- ไม่มีโซเชียลฟีด / แข่งเพื่อน / leaderboard
- ไม่บังคับ LLM API จริง — `mock_demo` คุณภาพดีพอสำหรับเดโมและคลิป
- ไม่มี paid coach / แชทที่ปรึกษาความสัมพันธ์

---

## 4. ผู้ใช้และบทบาท

| บทบาท | ความต้องการหลัก |
|---|---|
| **คนทำงานวัย 20–35 (หลัก)** | ตอบแชทงาน/ลูกค้า/หัวหน้าเร็ว ไม่ดูแข็ง |
| **วัยรุ่น / คนมีโซเชียล** | ตอบเพื่อน/แฟน/คอมเมนต์ที่อึดอัดโดยไม่เสียมุข |
| **ผู้ชมช่อง AI วันละแอป** | เห็น wow วางข้อความ→ชุดตอบ ใน 3 วินาที อยากลองลิงก์ในไบโอ |
| **ผู้สร้างคลิป (เรา)** | gen แอปใน 1 วัน มีสคริปต์ช็อตและเช็คลิสต์พร้อมถ่าย |

---

## 5. User stories

1. ในฐานะผู้ใช้ ฉันวางข้อความแชทอึดอัดแล้วได้ชุดตอบภาษาไทยหลายโทนภายในไม่กี่วินาที
2. ในฐานะผู้ใช้ ฉันหมุน Tone Dial แล้วเห็นแพ็กกรองหรือ regen ตามโทนที่เลือก
3. ในฐานะผู้ใช้ ฉันเปิด Situation Library เลือกคิทไทย (ตอบช้า / ปฏิเสธนุ่มๆ ฯลฯ) หรือสร้าง/favorite ได้
4. ในฐานะผู้ใช้ ฉันอัปโหลดสกรีนช็อตแชทหรือกดใช้รูปเดโมแล้วได้ข้อความ inbound ล่าสุด → Reply Pack
5. ในฐานะผู้ใช้ ฉันคัดลอกคำตอบหนึ่งแตะและแชร์การ์ดตอบสวย + แคปชัน IG/LINE ได้
6. ในฐานะผู้ชม Reel ฉันเห็นวางข้อความ→ชุดตอบใน 3 วินาทีแรกแล้วอยากลองแอป
7. ในฐานะระบบ ทุกแพ็ก/สถานการณ์/การตั้งค่าต้องเก็บตาม `ReplyPack`, `Situation`, `LocalStore`

---

## 6. ฮุค Reel (3 วินาทีแรก)

**Before:** หน้าจอแชทเพื่อน「ทำไมเงียบ 3 วันแล้ว 🥺」+ คนค้างพิมพ์  
**After:** กองการ์ดตอบโทน soft / funny / firm สี teal — ข้อความไทยใหญ่  
**ข้อความบนจอ:** `วางข้อความแชท → ได้ชุดตอบหลายโทน ใน 10 วินาที`  
**เสียง:** 「วางแชทแป๊บเดียว ได้ชุดตอบหลายโทน」

**Wow moment กลางคลิป:** วางข้อความ → ชุดตอบโผล่ → หมุน Tone Dial → คัดลอก + แชร์การ์ดตอบ

---

## 7. ทำไมคนติดตาม / เปิดซ้ำ

- ผลวางข้อความ→ชุดตอบทันที (เหมาะ Reel + save)
- ใช้จริงได้ทุกครั้งที่เจอแชทอึดอัด / ทวงงาน / ปฏิเสธนุ่มๆ
- แจกฟรีจากช่อง → เซฟคลิป + เข้าลิงก์
- รีเทนชัน: Tone Dial, Situation Library, Screenshot Extract, Share Reply Card, favorites
- คอมเมนต์「ตอบ」= สัญญาณทำคลิปต่อ / ขอฟีเจอร์เพิ่ม

---

## 8. กฎผลิตภัณฑ์ช่อง

- **ขั้นต่ำ 5 ฟีเจอร์** must-have (ตารางด้านล่าง)
- Gen ได้ใน 1 วันด้วย AI codegen (Next.js + reply engine pluggable)
- เดโมหลักจบในมือถือแนวตั้ง (~390px)
- UI สวย พอเป็นพรีวิว “แอปจริง” ไม่ใช่ฟอร์มดิบ
- ภาษาไทยก่อน — คีย์สคีมาภาษาอังกฤษได้
- โทนช่วยเหลือ เป็นมิตร — ใช้คำว่า「ตัวช่วยร่างข้อความ」ชัดเจน ห้าม「AI รู้ความสัมพันธ์」

---

## 9. ฟีเจอร์

### 9.1 Must-have (≥ 5)

| # | ฟีเจอร์ | รายละเอียด | Acceptance ย่อ |
|---|---|---|---|
| 1 | **Paste → Reply Pack** | วางข้อความ / โหลดเดโม → 3–5 reply options พร้อม tone labels + อนิเมชัน; default engine `mock_demo` | fixture เดโมขึ้น 4–5 โทนใน ≤2s |
| 2 | **Tone Dial** | soft / funny / pro / firm / warm (4–5); filter หรือ regenerate เมื่อเปลี่ยนโทน | เปลี่ยนโทนแล้วแพ็กอัปเดตชัด |
| 3 | **Situation Library** | คิทไทย: ตอบช้า, ปฏิเสธนุ่มๆ, ทวงงาน, คุยหัวหน้า, ลูกค้าโกรธ, แชทแฟนหรือเพื่อน; สร้าง/rename/favorite | มี ≥6 คิท + สร้าง/favorite ได้ |
| 4 | **Screenshot → Extract** | อัปโหลดสกรีนช็อต หรือปุ่ม「ใช้รูปเดโม」→ mock extract last inbound → Reply Pack | รูปเดโมได้ข้อความไทย + แพ็กใน ≤2s |
| 5 | **Copy & Share Reply Card** | one-tap copy + การ์ดแชร์สวย + แคปชัน IG/LINE + navigator.share | ได้รูป+ข้อความบน iPhone Safari |

### 9.2 Nice-to-have

| # | ฟีเจอร์ | รายละเอียด |
|---|---|---|
| 6 | **Rewrite my draft** | วางร่างของฉัน → ปรับโทนโดยไม่เปลี่ยนสาระ |
| 7 | **Voice preview** | อ่านคำตอบด้วย speechSynthesis ภาษาไทย (th-TH) |
| 8 | **Favorite replies history** | ประวัติคำตอบที่กดหัวใจ เปิดใช้ซ้ำได้ |
| 9 | **Bilingual TH/EN** | สลับดูคำตอบไทย/อังกฤษคู่กัน |
| 10 | **Emoji booster** | เติม/ลดอีโมจิตามโทน |
| 11 | **Dark chat mode** | ธีมมืดสไตล์หน้าต่างแชท |

---

## 10. ขอบเขตฟีเจอร์

### 10.1 In scope

- Home, Paste Composer, Reply Pack Result, Tone Dial, Situation Library, Screenshot Extract, Share sheet
- Reply engine pluggable: `mock_demo` (default) · optional `llm_api` ผ่าน env
- Tone filter/regen ใน `lib/tones.ts` (pure functions)
- Share card render บน Canvas / DOM-to-image
- Analytics events ฝั่ง client (optional log)
- PWA ติดตั้งได้แบบพื้นฐาน (manifest + icons)
- Disclaimer UI: 「ReplyKit เป็นตัวช่วยร่างข้อความ คุณเลือกส่งเอง — ไม่ได้รู้ความสัมพันธ์หรือเจตนาของคู่สนทนา」

### 10.2 Out of scope (เฟสถัดไป)

- Auth / cloud sync แพ็ก
- LINE / WhatsApp / Instagram API ส่งข้อความจริง
- Agent แชทยาวหลายเทิร์น / memory ความสัมพันธ์
- โซเชียลฟีด / follow เพื่อน
- Paid relationship coach
- ฝึกโมเดล OCR/vision เองสำหรับสกรีนช็อต

---

## 11. User flow หลัก (Happy path)

```text
เปิดแอป → วางข้อความอึดอัด (หรือกด「ใช้ข้อความเดโม」)
  → Generate / mock parse (progress สวย เป้า ≤ 2s สำหรับ fixture)
  → ดูผล: กองการ์ดตอบ 4–5 โทน พร้อมป้าย soft/funny/pro/firm/warm
  → หมุน Tone Dial กรองหรือ regen
  → คัดลอกคำตอบที่ชอบ / บันทึกสถานการณ์ใน Situation Library
  → (ออปชัน) อัปโหลดสกรีนช็อตหรือใช้รูปเดโม → extract → Reply Pack
  → แชร์ Reply Card / คัดลอกแคปชัน / เปิด share sheet
  → กลับมาเปิดคิทจาก Situation Library ครั้งถัดไป
```

### สถานะเซสชัน generate / แชร์

`idle` → `generating` → `pack_ready` → `tone_filtering` → `copying` → `sharing`  
ทางแยก: `extracting` (จาก screenshot) · `error` (พร้อมข้อความไทยสั้นๆ + ปุ่มลองใหม่ / วางข้อความ)

---

## 12. หน้าจอ (MVP)

| # | หน้าจอ | องค์ประกอบหลัก |
|---|---|---|
| 1 | **Home** | โลโก้, หัวข้อไทย, แถบเดโมวางข้อความ→ชุดตอบ, CTA「วางข้อความ」, แถบ 5 ฟีเจอร์ไอคอน, ปุ่มรอง「ใช้ข้อความเดโม」, ลิงก์ไป Situation Library |
| 2 | **Paste Composer** | textarea ใหญ่, ปุ่มข้อความเดโม, ชิปสถานการณ์เร็ว, ปุ่ม「ได้ชุดตอบ」 |
| 3 | **Reply Pack Result** | กองการ์ดตอบ (tone chips), คัดลอกต่อใบ, Tone Dial, ปุ่มแชร์ |
| 4 | **Tone Dial** | วงล้อหรือชิป 5 โทน; active state ชัด; filter/regen |
| 5 | **Situation Library** | การ์ดคิทไทย, สร้าง/rename/favorite, แตะแล้วโหลดพรอมต์สถานการณ์ |
| 6 | **Screenshot Extract** | อัปโหลด/กล้อง, ปุ่มรูปเดโม, progress, พรีวิวข้อความที่ดึงได้ |
| 7 | **Share sheet** | พรีวิวการ์ดตอบ, คัดลอกแคปชัน, แชร์ระบบ |
| 8 | **Rewrite / Voice / Dark** (nice) | ร่างของฉัน, พรีวิวเสียง, ธีมมืด |

**โทนแบรนด์:** พื้น cream/off-white (#FFFBEB / #FAFAF9), ไฮไลต์ teal/mint (#0D9488 / #14B8A6), coral accent (#FB7185), การ์ดขาวมุมมน, ตัวอักษรคำตอบไทยใหญ่, ปุ่ม primary ใหญ่ — โทน “friendly chat helper” ที่ถ่าย Reel แล้วอ่านง่าย ไม่ดาร์กบังคับ ไม่ดราม่า

---

## 13. ความต้องการเชิงฟังก์ชัน

### FR-1 Paste → Reply Pack
- รับข้อความจาก textarea (หรือโหลด fixture)
- รัน engine ตาม `reply_engine` (ค่าเริ่ม `mock_demo`)
- มีปุ่ม「ใช้ข้อความเดโม」โหลด fixture จาก `/fixtures/demo-chat.json`
- เก็บ `generate_ms`, confidence, replies[] ใน `ReplyPack`
- แสดง 3–5 `ReplyOption` พร้อม `tone` label + animation เข้าทีละใบ
- ถ้า generate ล้มเหลว: ให้ลองใหม่หรือเลือกสถานการณ์จาก Library
- แสดง disclaimer ตัวช่วยร่างใกล้ผลลัพธ์

### FR-2 Tone Dial
- โทนพรีเซ็ต: `soft`, `funny`, `pro`, `firm`, `warm` (อย่างน้อย 4–5)
- เมื่อเลือกโทน: **filter** แพ็กปัจจุบัน หรือ **regenerate** ตามโทน (ตั้งค่าได้; ค่าเริ่ม filter แล้วมีปุ่ม「สร้างใหม่ตามโทนนี้」)
- UI เป็นชิปหรือวงล้อที่นิ้วหมุน/แตะง่ายบน 390px
- เก็บ `selected_tones[]` ใน settings / session

### FR-3 Situation Library
- คิทพรีเซ็ตไทยอย่างน้อย: ตอบช้า, ปฏิเสธนุ่มๆ, ทวงงาน, คุยหัวหน้า, ลูกค้าโกรธ, แชทแฟนหรือเพื่อน
- สร้างสถานการณ์ใหม่ / เปลี่ยนชื่อ / ลบ (ยืนยันก่อนลบ) / favorite
- แต่ละสถานการณ์เก็บ `prompt_hint_th`, `default_tones[]`, `sample_inbound_th`
- แตะสถานการณ์แล้วเติม composer หรือ generate ทันที

### FR-4 Screenshot → Extract
- รับไฟล์ภาพจากไฟล์หรือกล้อง
- รัน engine ตาม `extract_engine` (ค่าเริ่ม `mock_demo`)
- มีปุ่ม「ใช้รูปเดโม」โหลด fixture ภาพแชท + ข้อความ inbound
- ผลลัพธ์ `ExtractResult` มี `last_inbound_th`, confidence, warnings
- หลัง extract สำเร็จ → ส่งต่อไปสร้าง Reply Pack อัตโนมัติ
- ถ้า extract ล้มเหลว: ให้วางข้อความมือได้

### FR-5 Copy & Share Reply Card
- คัดลอกข้อความตอบหนึ่งแตะ (clipboard) + toast ภาษาไทย
- เรนเดอร์การ์ดสรุปคำตอบ/โทนเป็น PNG (Canvas หรือ html-to-image)
- แสดง: ข้อความต้นทางย่อ, คำตอบที่เลือก, ป้ายโทน, โทน teal+coral
- สร้างแคปชันไทยสำหรับ IG/LINE ตามเทมเพลต
- `navigator.share` ถ้ามี + fallback คัดลอก/ดาวน์โหลด
- ห้ามใส่「AI รู้ใจคุณ」/ ชื่อคนจริงโดยไม่จำเป็น

### FR-6 Local retention
- บันทึก packs + situations + favorites + settings ตาม `LocalStore`
- ไม่บังคับ auth; ใช้ได้หลังโหลดครั้งแรกแบบออฟไลน์ (cache หน้า)

### FR-7 Analytics (เบา)
- ยิงอีเวนต์ตาม enum ใน schema (console หรือ provider ภายหลัง)

### FR-8 Safety copy
- ทุกจุดที่โชว์ผล generate ต้องเข้าถึง disclaimer ได้
- หลีกเลี่ยงคำว่า「AI รู้ความสัมพันธ์」「ส่งแทนคุณ」「รับประกันคืนดี」ใน UI หลัก

---

## 14. ความต้องการเชิงไม่ใช่ฟังก์ชัน

| หัวข้อ | เป้า |
|---|---|
| Generate / mock latency (fixture) | p50 ≤ 2s |
| Tone filter | อัปเดต < 100ms |
| Mobile layout | ใช้งานได้ที่ 390×844 โดยไม่เลื่อนแนวนอนพัง |
| ภาษา | th-TH เป็นค่าเริ่มต้น |
| ความเป็นส่วนตัว | ประมวลผลข้อความฝั่ง client เป็นหลัก ไม่อัปโหลดเซิร์ฟเวอร์ถ้าไม่ใช้ LLM/vision API |
| Deploy | Vercel preview URL พร้อมแชร์ในไบโอ |
| การ์ดตอบ | ตัวอักษรอ่านชัดบน Reel; ปุ่มคัดลอกนิ้วใหญ่ |
| Accessibility เบา | ปุ่มใหญ่ คอนทราสต์ข้อความบน Reel ผ่านตาเปล่า |

---

## 15. Tech แนะนำสำหรับ gen วันเดียว

| ชั้น | เลือก |
|---|---|
| Frontend | Next.js 14 (App Router) + TypeScript + Tailwind + shadcn/ui |
| Reply engine | `mock_demo` default · optional LLM API ผ่าน env |
| Extract | `mock_demo` สำหรับ screenshot · optional vision API |
| Tone helpers | `lib/tones.ts` (pure) + `lib/reply.ts` |
| Share | Canvas / `html-to-image` + `lib/share.ts` |
| State | React state + `lib/storage.ts` (localStorage) |
| Fixtures | `/public/fixtures/demo-chat.json` (+ ภาพสกรีนช็อตเดโม) |
| Situations | `/data/situations.json` หรือฝังใน `lib/situations.ts` |
| Deploy | Vercel |

**โครงสร้างรีโปแนะนำ**

```text
/replykit
  README.md
  prd.md
  prompts.md
  schemas.json
  examples.json
  /app
  /components
  /lib
    reply.ts
    tones.ts
    extract.ts
    share.ts
    storage.ts
    situations.ts
  /public/fixtures
  /data
```

ถ้าไม่มี LLM/Vision API key: ใช้ `mock_demo` + ปุ่มข้อความเดโม/รูปเดโมเป็นหลัก แล้วหมายเหตุใน UI ว่า「โหมดเดโม — วางข้อความจริงได้เสมอ」

---

## 16. ข้อมูลและสคีมา

แหล่งความจริง (ดูรายละเอียดใน `schemas.json` / ตัวอย่างใน `examples.json`):

- `ChatMessage` / `ToneId` / `ReplyOption` / `ReplyPack`
- `Situation` / `ExtractResult` / `ShareCard` / `SharePayload`
- `LocalStore` / `AnalyticsEvent`
- `FeatureChecklist` / `UiCopyTh` / `ReelScript`
- `ReplyEngine` / `ExtractEngine` / `AppStatus`

---

## 17. Analytics / สำเร็จของแอปในช่อง

**Primary (ผลิตภัณฑ์):** % เซสชันที่ทำ `pack_generated` อย่างน้อย 1 ครั้ง และ/หรือ `reply_copied` / `share_success`  
**Primary (ช่อง):** save rate ของ Reel + จำนวนคอมเมนต์「ตอบ」

**Secondary:**
- `generate_success` rate / median `generate_ms`
- การใช้ Tone Dial ต่อเซสชัน
- การเปิด Situation Library / favorite
- การใช้ Screenshot Extract vs Paste

**Guardrail:** อัตรา `generate_fail`, คอมเมนต์บ่นว่าแอป「ส่งแทน」「รู้ความสัมพันธ์」, UI ที่ดูดราม่าเกิน

---

## 18. Reel shot list (25–35 วินาที)

| เวลา | ภาพ | ข้อความบนจอ | เสียงพูด |
|---|---|---|---|
| 0–3s | แชทเพื่อนเงียบ → กองการ์ดตอบ | วางแล้วได้ชุดตอบ | วางแชทแป๊บเดียว ได้ชุดตอบหลายโทน |
| 3–8s | มอนทาจ gen / โลโก้ | สร้างด้วย AI วันนี้ | วันนี้ทำแอป ReplyKit สดๆ |
| 8–14s | วางข้อความเดโม → แพ็กโผล่ | Paste → Reply Pack | เพื่อนทักวันเสาร์ เงียบ 3 วัน ได้คำตอบเลย |
| 14–22s | Tone Dial + คัดลอก | Tone Dial · Copy | หมุนโทนนุ่มหรือตลก แล้วก็อปได้ทันที |
| 22–28s | Situation Library เร็วๆ + Share card | คิทสถานการณ์ แชร์ได้ | มีไลบรารีสถานการณ์และแชร์การ์ดสวย |
| 28–35s | ผลสุดท้าย + ลิงก์ | ลิงก์ในไบโอ | ลองฟรีที่ลิงก์ในไบโอ แล้วคอมเมนต์「ตอบ」 |

รายละเอียดช็อตเต็มใน `examples.json` → `reel_script_th`

---

## 19. ความเสี่ยง

| ความเสี่ยง | แผนลดความเสี่ยง |
|---|---|
| คนเข้าใจว่า AI ส่งข้อความแทน / รู้ความสัมพันธ์ | Disclaimer ชัดทุกจุด + คัดก็อปปี้「ตัวช่วยร่าง — คุณเลือกส่งเอง」 |
| LLM จริงตอบโทนไม่ไทย / ยาวเกิน | ใช้ mock_demo เป็นฮุค Reel หลัก + จำกัดความยาวต่อใบ |
| สกรีนช็อตอ่านภาษาไทยผิด / UI แชทหลากแพลตฟอร์ม | mock extract + ให้แก้ข้อความก่อน gen ได้ |
| เดโมใช้แชทจริงที่มีข้อมูลส่วนตัว | ใช้ fixture สมมติ「เพื่อนเรื่องวันเสาร์」ที่สร้างเอง |
| มือถือเครื่องอ่อนเรนเดอร์การ์ดช้า | การ์ดเรียบๆ teal+coral ไม่ใส่เอฟเฟกต์หนัก |
| ผู้ใช้คาดหวังซิงก์ LINE จริง | บอกชัดใน MVP ว่าเป็นเว็บช่วยร่าง เก็บในเครื่อง |

---

## 20. แผนส่งมอบวันเดียว (สำหรับคลิป)

| ช่วง | งาน |
|---|---|
| เช้า | Gen โครง Next.js + Home/Composer/Pack ตาม Master prompt |
| สาย | mock reply + demo fixture เพื่อนวันเสาร์ 4–5 โทน + Tone Dial |
| บ่าย | Situation Library + Screenshot Extract + Share Reply Card |
| เย็น | QA ตามตัวอย่าง + ถ่าย Reel ตาม shot list + อัป Vercel + ใส่ลิงก์ไบโอ |

---

## 21. Open questions

1. Tone Dial ควร filter อย่างเดียวหรือ regen ทุกครั้งที่หมุน? (MVP แนะนำ filter + ปุ่ม regen)
2. รอบถัดไปต่อ LLM/vision จริงคุ้มไหมสำหรับคลิป หรือพอ mock_demo + Paste?
3. เก็บ analytics แค่ console หรือต่อ Plausible/PostHog ตั้งแต่วันที่ 5?

---

## 22. Acceptance criteria (ผ่านก่อนลงคลิป)

- [ ] ปุ่มข้อความเดโมโหลดผล Reply Pack ไทย 4–5 โทนตาม fixture
- [ ] Tone Dial เปลี่ยนโทนแล้วแพ็กกรอง/regen ชัด
- [ ] Situation Library มีคิทไทย ≥6 + สร้าง/rename/favorite ได้
- [ ] Screenshot: ปุ่มใช้รูปเดโม → extract ข้อความ → Reply Pack
- [ ] Copy one-tap + Share ได้รูปการ์ด + แคปชัน + share sheet (หรือ fallback)
- [ ] มี ≥ 5 ฟีเจอร์ must ตามตาราง และติ๊กใน `FeatureChecklist`
- [ ] มือถือ 390px ใช้งานได้ไม่เละ การ์ดใหญ่ อ่านคำตอบบน Reel ได้
- [ ] สคริปต์ Reel ถ่ายครบช็อต + CTA「ตอบ」ชัด
- [ ] มี disclaimer ตัวช่วยร่าง และไม่มีเคลมรู้ความสัมพันธ์ / ส่งแทน ใน UI หลัก

---

## 23. รายละเอียด Tone และการสร้างแพ็ก (สำหรับ engine)

### 23.1 โทนมาตรฐาน
- `soft` — นุ่ม น้อม ขอโทษเบาๆ ไม่ดราม่า
- `funny` — ตลกเบาๆ มีมุข ไม่เสียมารยาท
- `pro` — สุภาพ กระชับ โทนงาน/ลูกค้า
- `firm` — ชัดเจน ตั้งขอบเขต ไม่หยาบ
- `warm` — อบอุ่น เป็นกันเอง โทนเพื่อน/แฟน

### 23.2 ลำดับสร้าง ReplyPack
1. รับ `inbound_th` (+ ออปชัน situation_id, selected_tones)
2. เรียก engine → ได้ `ReplyOption[]` (3–5 ใบ)
3. แปะ `tone`, `text_th`, `short_label_th`, `emoji` (ออปชัน)
4. `generate_ms` และ `confidence` สำหรับ QA
5. ถ้ามี Tone Dial filter: แสดงเฉพาะโทนที่เลือก หรือเรียงโทนที่เลือกขึ้นก่อน

### 23.3 ความไม่แน่นอนของ extract/generate
- `ExtractResult.confidence` / `ReplyPack.confidence` 0–1; ถ้า < 0.55 แนะนำให้แก้ข้อความ inbound
- อนุญาตให้แก้ `inbound_th` ก่อนกดสร้างใหม่
- ห้ามซ่อนว่าเป็นตัวช่วยร่างอัตโนมัติที่อาจไม่เข้าบริบทจริง

### 23.4 ตัวอย่างเดโมหลัก (ต้องตรง examples)
- สถานการณ์: เพื่อนทักเรื่องวันเสาร์ เงียบไป 3 วัน
- Inbound ประมาณ: 「เดี๋ยวก่อนนน คุยเรื่องวันเสาร์ไปไหนกัน ทำไมเงียบ 3 วันแล้ว 🥺」
- จำนวนคำตอบ: 4–5 โทน (soft / funny / honest-as-soft-or-warm / firm / ออปชัน pro หรือ warm)
- ใช้เป็น fixture ฮุค Reel และทดสอบ Tone Dial

---

## 24. สำเนาแบรนด์และไมโครคัดก็อปปี้

| จุด | ทิศทางสำเนา |
|---|---|
| Home | สด สั้น ชวนวางข้อความ ไม่ขายคอร์ส soft skill |
| หลัง generate | 「ได้ชุดตอบแล้ว — เลือกโทนแล้วก็อปได้เลย」 |
| หลัง copy | 「คัดลอกแล้ว ไปวางในแชทได้」 |
| Tone Dial | 「หมุนโทนที่ใช่ — นุ่ม ตลก โปร หนักแน่น อบอุ่น」 |
| Disclaimer | 「ReplyKit เป็นตัวช่วยร่างข้อความ คุณเลือกส่งเอง — ไม่ได้รู้ความสัมพันธ์หรือเจตนาของคู่สนทนา」 |

สีหลักในโค้ด (แนะนำ CSS variables):

```text
--bg: #FFFBEB;
--bg-soft: #FAFAF9;
--card: #FFFFFF;
--primary: #0D9488;
--primary-soft: #CCFBF1;
--primary-mint: #14B8A6;
--accent: #FB7185;
--accent-soft: #FFE4E6;
--ink: #134E4A;
--muted: #64748B;
```

---

## 25. ภาคผนวก — สำเนาแพ็ก

แหล่งหลัก:

```text
/workspace/ai-wanla-app/2026-10-02-replykit/
  README.md
  prd.md
  prompts.md
  schemas.json
  examples.json
```

Zip ในโฟลเดอร์: `/workspace/ai-wanla-app/2026-10-02-replykit/replykit.zip`  
Zip ราก: `/workspace/replykit.zip` (unzip แล้วได้ `replykit/...`)

---

## 26. รายละเอียดหน้าจอและคอมโพเนนต์ (สำหรับ codegen)

### 26.1 Home
- Hero หัวข้อไทย + คำบรรยาย 1 บรรทัด
- Demo strip แนวนอน 3 เฟรม: ข้อความแชท → กองการ์ดตอบ → Tone Dial
- Primary CTA `วางข้อความ` / Secondary `ใช้ข้อความเดโม`
- แถวไอคอน 5 ฟีเจอร์ must
- ลิงก์ข้อความ `เปิดคลังสถานการณ์` ไป Situation Library
- Footer disclaimer หนึ่งบรรทัด

### 26.2 Paste Composer
- Textarea สูงอย่างน้อย ~30vh ตัวอักษรไทยใหญ่
- ปุ่มใช้ข้อความเดโม / วางจากคลิปบอร์ด (ถ้าอนุญาต)
- ชิปสถานการณ์เร็ว 3–6 อัน
- CTA หลัก「ได้ชุดตอบ」
- ตัวนับตัวอักษรเบาๆ (ไม่บังคับตัด)

### 26.3 Reply Pack Result
- Header ย่อ inbound 1–2 บรรทัด
- กองการ์ดตอบเลื่อนได้ — แต่ละใบมีป้ายโทน + ปุ่มคัดลอก + หัวใจ (nice)
- Tone Dial ใต้หรือเหนือกอง
- ปุ่มแชร์การ์ด / บันทึกสถานการณ์
- Disclaimer ใต้แพ็ก

### 26.4 Tone Dial
- ชิป 5 โทนหรือวงล้อ
- Active สี teal; accent coral เมื่อเลือก soft/warm ตามดีไซน์
- ปุ่มรอง「สร้างใหม่ตามโทนนี้」

### 26.5 Situation Library
- กริด/ลิสต์การ์ดคิท: ชื่อไทย · อีโมจิ · favorite star
- FAB สร้างสถานการณ์
- แตะแล้วเติม composer หรือ generate

### 26.6 Screenshot Extract
- พื้นที่พรีวิวสูงอย่างน้อย ~40vh
- ปุ่มเปิดกล้อง / เลือกไฟล์ / ใช้รูปเดโม
- Progress ตอน extracting
- หลังสำเร็จแสดงข้อความที่ดึงได้ แก้ได้ แล้วกดสร้างแพ็ก

### 26.7 Share sheet
- พรีวิวการ์ดตอบ
- คัดลอกแคปชัน
- แชร์ระบบ / ดาวน์โหลดรูป
- ข้อความว่าไม่เก็บแชทบนเซิร์ฟเวอร์ใน MVP

---

## 27. เกณฑ์คุณภาพ Reel (ช่อง)

1. ฮุค 3 วินาทีแรกต้องเห็นการเปลี่ยนข้อความ→ชุดตอบ ไม่ใช่โลโก้ยาว
2. ในคลิปเดียวโชว์ ≥3 ฟีเจอร์ must
3. UI จริงจากบิลด์ที่ deploy ไม่ใช่แค่ Figma
4. พูดหรือติดข้อความ「ตัวช่วยร่างข้อความ」อย่างน้อย 1 ครั้ง
5. CTA ปิดคลิป: ลิงก์ในไบโอ + คอมเมนต์「ตอบ」
6. ห้ามใช้เพลง/ฟุตเทจที่เสี่ยงลิขสิทธิ์หนักโดยไม่จำเป็น — โฟกัสหน้าจอแอป

---

## 28. ค่าเริ่มต้นที่ล็อกสำหรับเดโมเช้านี้

| ค่า | ค่าเริ่ม |
|---|---|
| Reply engine | `mock_demo` |
| Extract engine | `mock_demo` |
| Hero fixture | เพื่อนทักวันเสาร์ เงียบ 3 วัน · 4–5 โทน |
| ความกว้าง UI ฐาน | 390px |
| คำคอมเมนต์ CTA | ตอบ |
| localStorage key | `replykit.v1` |
| ภาษา UI | th-TH |
| สีหลัก | teal `#0D9488` + mint `#14B8A6` + coral `#FB7185` + cream `#FFFBEB` |
| โทนเริ่มแสดง | soft, funny, warm, firm ( + pro ออปชัน) |

ค่าเหล่านี้ต้องตรงกับ `examples.json` เพื่อให้ QA เทียบได้เร็วตอนเย็นก่อนขึ้นคลิป

---

## 29. ตัวอย่างข้อความตอบเดโม (สรุปสำหรับ PRD)

Inbound: `เดี๋ยวก่อนนน คุยเรื่องวันเสาร์ไปไหนกัน ทำไมเงียบ 3 วันแล้ว 🥺`

| โทน | ทิศทางคำตอบ (ย่อ) |
|---|---|
| soft | ขอโทษที่เงียบ + ยังอยากไป + เสนอวันเวลาใหม่ |
| funny | มุขเบาๆ เรื่องแบตหมด/จมงาน + ยอมรับผิด + นัดใหม่ |
| warm | อบอุ่น ขอบคุณที่ทัก + เล่าสั้นๆ ว่ายุ่ง + นัดคุย |
| firm | ขอโทษชัด + ขอบเขตว่าช่วงนี้แน่น + เสนอทางเลือก 1–2 แบบ |
| pro | (ถ้าใช้) สุภาพกระชับแบบเพื่อนที่โตแล้ว |

รายละเอียดข้อความเต็มอยู่ใน `examples.json` → `paste_reply_example`
