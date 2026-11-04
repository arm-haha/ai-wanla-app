# ExamDeck — ชุดส่งมอบเช้า (AI วันละแอป)

**วันที่:** 2026-10-01 (Asia/Bangkok)  
**วันในคิว:** 4 / 10  
**ช่อง:** AI วันละแอป  
**สถานะ:** Delivery-ready สำหรับรอบเช้าวันที่สี่

มินิสวีทเด็คทวนข้อสอบสำหรับนักเรียนไทย — ถ่ายโน้ต/สไลด์/ข้อสอบ → AI/mock แตกเป็นการ์ด Q&A → สไวป์ทวน → ไลบรารีเด็คตามวิชา → แดชบอร์ดความชำนาญ → แชร์การ์ดสตรีคสวย  
ฮุคหลัก Reel: **ถ่ายโน้ต/ข้อสอบ → ได้เด็คทวนทันที ใน 10 วินาที**

---

## ไฟล์ในโฟลเดอร์นี้

| ไฟล์ | ใช้ทำอะไร |
|---|---|
| `prd.md` | สเปกผลิตภัณฑ์เต็ม: ปัญหา เป้าหมาย ผู้ใช้ สตอรี่ หน้าจอ เทค acceptance ความเสี่ยง ช็อต Reel |
| `prompts.md` | Prompt หลายส่วนสำหรับ codegen ทั้งแอป / mock photo→cards / quiz / share / UI / Reel / QA |
| `schemas.json` | JSON Schema ละเอียดพร้อม description (flashcard, deck, session, mastery, extract, share, store, analytics) |
| `examples.json` | ตัวอย่างชีวะ「ระบบหายใจ」+ สคริปต์ Reel + feature checklist + UI copy |
| `README.md` | ไฟล์นี้ — วิธีใช้แพ็ก + ฮุคโพสต์ |

แพ็กเต็มแบบ zip: `/workspace/examdeck.zip` (unzip แล้วได้ `examdeck/...`)

---

## ฟีเจอร์บังคับ ≥ 5 (Must-have)

| # | ฟีเจอร์ | ทำไมติดรีเทน / ไวรัล |
|---|---|---|
| 1 | **Photo → Cards** | Wow แรกใน 3 วินาที — รูปโน้ต/ข้อสอบ → กองการ์ด Q&A โผล่พร้อมอนิเมชัน |
| 2 | **Swipe Quiz** | ทวนแบบสไวป์/แตะ รู้แล้ว / ยังไม่ชัวร์ + สตรีคฟีดแบ็ก — เปิดซ้ำทุกวันก่อนสอบ |
| 3 | **Deck Library** | โฟลเดอร์วิชา (คณิต อังกฤษ ชีวะ ประวัติ ฯลฯ) + สร้าง/เปลี่ยนชื่อเด็ค |
| 4 | **Mastery Dashboard** | % ชำนาญ, จำนวน due วันนี้, วงแหวน/แถบสตรีคเรียน |
| 5 | **Share Study Card** | การ์ดแชร์สตรีค/ความคืบหน้าเด็คสวย + คัดลอกแคปชัน IG/LINE + navigator.share |

**Nice-to-have (เสริมถ้าเสร็จเร็ว):** Paste Text → Cards · Multi-choice mode · Exam countdown timer · Voice read question · Dark study mode · Offline history

---

## วิธีใช้กับ AI codegen (เช้านี้)

1. เปิด `prompts.md` ส่วน **A) Master prompt** วางเป็นคำสั่งหลัก
2. แนบบริบท: `prd.md` + `schemas.json` + `examples.json`
3. สั่งให้ `npm run dev` ผ่าน และ **happy path จบก่อน** (ถ่าย/อัปโหลดหรือโหลดเดโม → extract cards → ยืนยันเด็ค → Swipe Quiz → แดชบอร์ดอัปเดต → แชร์การ์ด)
4. ใส่ demo note photo fixtures ตามส่วน B + ตรวจ `FeatureChecklist` ใน `examples.json`
5. ก่อนถ่าย Reel รันส่วน H (QA) + เช็คลิสต์ `feature_checklist_example`

เป้าเวลา: gen + polish เดโมมือถือใน 1 วัน

---

## ฮุคโพสต์แชท / คาปชันสั้น

> ถ่ายโน้ต/ข้อสอบ → ได้เด็คทวนทันที ใน 10 วินาที

เวอร์ชันยาวขึ้นเล็กน้อย:

> ถ่ายโน้ตแล้วไม่เคยทวน? วันนี้แจกแอป ExamDeck จากช่อง AI วันละแอป ถ่ายโน้ต/ข้อสอบได้เด็คแฟลชการ์ดทันที สไวป์ทวน ดูความชำนาญ แล้วแชร์การ์ดสตรีคได้เลย ลองฟรีที่ลิงก์ในไบโอ

---

## กฎช่อง (อย่าพลาดตอนถ่าย)

- เปิดคลิปด้วย **รูปโน้ต → กองการ์ด Q&A ขึ้น** ภายใน 3 วินาที
- ในคลิปเดียวโชว์อย่างน้อย **3 ฟีเจอร์** (Photo → Cards, Swipe Quiz, Share Study Card)
- UI มือถือแนวตั้ง สวย ปุ่มใหญ่ — ไม่โชว์เดสก์ทอปรก
- ใช้รูปโน้ตเดโม/โน้ตตัวเอง — ห้ามเคลม「สอบผ่านชัวร์」หรือเป็นเฉลยข้อสอบสด
- ปิดท้ายด้วย CTA: ลิงก์ในไบโอ / คอมเมนต์คำว่า **「เด็ค」**

---

## สแต็กแนะนำ (สรุป)

- Next.js 14 App Router + TypeScript + Tailwind + shadcn/ui
- Photo→Cards: pluggable — default `mock_demo` (fixture คุณภาพดี) · optional vision API ผ่าน env
- Storage: localStorage (decks / cards / sessions / mastery)
- Deploy: Vercel (PWA-ready)
- ไม่มี auth · ไม่มีเคลมสอบผ่าน · ไม่มีโซเชียลฟีดใน MVP

รายละเอียดเต็มอยู่ใน `prd.md` § Tech และ `prompts.md` ส่วน A–N

---

## Acceptance ก่อนประกาศว่า “พร้อมลงคลิป”

- [ ] Must-have ครบ 5 ฟีเจอร์และติ๊กใน `feature_checklist_example`
- [ ] Demo note fixture โหลดแล้วได้การ์ด Q&A ภาษาไทย 6–8 ใบ (ระบบหายใจ)
- [ ] ยืนยันเด็คแล้วเข้า Swipe Quiz ได้ — รู้แล้ว / ยังไม่ชัวร์ อัปเดต mastery
- [ ] Deck Library มีโฟลเดอร์วิชาตัวอย่าง + สร้าง/เปลี่ยนชื่อเด็คได้
- [ ] Mastery Dashboard แสดง % ชำนาญ, due วันนี้, สตรีค
- [ ] Share ได้รูปการ์ดสตรีค/ความคืบหน้า + คัดลอกแคปชันบนมือถือจริง
- [ ] Editor ใช้ได้ที่ความกว้าง ~390px ไม่เละ
- [ ] สคริปต์ Reel ใน `examples.json` → `reel_script_th` ถ่ายครบช็อต
- [ ] UI ไม่มีเคลม「สอบผ่านชัวร์」/เฉลยข้อสอบสด และมี disclaimer เครื่องมือทวน

---

## Wow moment ที่ต้องโชว์ในคลิป

รูปโน้ตชีวะมือเขียน/สไลด์「ระบบหายใจ」→ กองการ์ด Q&A สี indigo-violet + ตัวอักษรไทยใหญ่ พลิกได้  
เดโมหลักแนะนำ: **ม.ปลาย ชีวะ ระบบหายใจ → 7 การ์ด** (ดู `examples.json` → `photo_extract_example`)

อย่าลืมพูดสั้นๆ ว่าเป็น「เครื่องมือทวน / ฝึกจำ」— mock_demo ใช้ถ่าย Reel ได้ ไม่ต้องรอ Vision API

---

## Happy path เป้า ≤ 60 วินาที

1. เปิดแอป → กด「ใช้รูปเดโม」  
2. เห็นกองการ์ด Q&A จากโน้ตระบบหายใจ  
3. บันทึกเป็นเด็ค「ชีวะ · ระบบหายใจ」  
4. เข้า Swipe Quiz สไวป์รู้แล้ว / ยังไม่ชัวร์ 2–3 ใบ  
5. Mastery Dashboard อัปเดต → แชร์ Share Study Card + คัดลอกแคปชัน  

รายละเอียดช็อตถ่ายอยู่ใน `examples.json` → `reel_script_th` และแผนวันเดียวอยู่ใน `prd.md` §20
