# SplitBill Pro — ชุดส่งมอบเช้า (AI วันละแอป)

**วันที่:** 2026-09-29 (Asia/Bangkok)  
**วันในคิว:** 2 / 10  
**ช่อง:** AI วันละแอป  
**สถานะ:** Delivery-ready สำหรับรอบเช้าวันที่สอง

มินิสวีทหารบิลร้านอาหาร/คาเฟ่สำหรับเพื่อนคนไทย — ถ่ายสลิป → OCR รายการ → ลากเมนูให้คน → คิดทิป/เซอร์วิสชาร์จ → แชร์ยอดต่อคน  
ฮุคหลัก Reel: **สแกนสลิป → หารบิลตามเมนูจริง ใน 15 วินาที**

---

## ไฟล์ในโฟลเดอร์นี้

| ไฟล์ | ใช้ทำอะไร |
|---|---|
| `prd.md` | สเปกผลิตภัณฑ์เต็ม: ปัญหา เป้าหมาย ผู้ใช้ สตอรี่ หน้าจอ เทค acceptance ความเสี่ยง ช็อต Reel |
| `prompts.md` | Prompt หลายส่วนสำหรับ codegen ทั้งแอป / OCR mock / bill engine / share / UI / Reel / QA |
| `schemas.json` | JSON Schema ละเอียดพร้อม description (bill, people, items, tip, share, history, analytics) |
| `examples.json` | ตัวอย่างบิลไทย + สคริปต์ Reel + feature checklist + UI copy |
| `README.md` | ไฟล์นี้ — วิธีใช้แพ็ก + ฮุคโพสต์ |

แพ็กเต็มแบบ zip: `/workspace/splitbill-pro.zip` (unzip แล้วได้ `splitbill-pro/...`)

---

## ฟีเจอร์บังคับ ≥ 5 (Must-have)

| # | ฟีเจอร์ | ทำไมติดรีเทน / ไวรัล |
|---|---|---|
| 1 | **Receipt Scan / OCR** | Wow แรกใน 3 วินาที — สลิปรก → รายการขึ้นครบ |
| 2 | **Item Assign** | ลากเมนูให้เพื่อน / แชร์จาน = หัวใจของคลิป |
| 3 | **Tip & Service Charge** | ทิป % + เซอร์วิสชาร์จ + VAT แบบสลิปไทย |
| 4 | **Split Modes** | equal / by item / custom — ปรับยอดคนเองได้ |
| 5 | **Share Pack** | การ์ดสรุปสวย + ข้อความ LINE + ลิงก์ mock + QR ออปชัน |

**Nice-to-have (เสริมถ้าเสร็จเร็ว):** Friends presets · Bill History (localStorage) · Settle tracker · Multi-currency display (THB primary)

---

## วิธีใช้กับ AI codegen (เช้านี้)

1. เปิด `prompts.md` ส่วน **A) Master prompt** วางเป็นคำสั่งหลัก
2. แนบบริบท: `prd.md` + `schemas.json` + `examples.json`
3. สั่งให้ `npm run dev` ผ่าน และ **happy path จบก่อน** (สแกน/อัปโหลด → OCR → ใส่คน → ลากเมนู → ทิป → สรุป → แชร์)
4. ใส่ demo receipt fixture ตามส่วน B + ตรวจ `FeatureChecklist` ใน `examples.json`
5. ก่อนถ่าย Reel รันส่วน H (QA) + เช็คลิสต์ `feature_checklist_example`

เป้าเวลา: gen + polish เดโมมือถือใน 1 วัน

---

## ฮุคโพสต์แชท / คาปชันสั้น

> สแกนสลิป → หารบิลตามเมนูจริง ใน 15 วินาที

เวอร์ชันยาวขึ้นเล็กน้อย:

> กินร้านด้วยกันแล้วใครจ่ายอะไร เลิกบวกเลขในแชท วันนี้แจกแอป SplitBill Pro จากช่อง AI วันละแอป ถ่ายสลิป ลากเมนูให้เพื่อน แชร์ยอด LINE ได้เลย ลองฟรีที่ลิงก์ในไบโอ

---

## กฎช่อง (อย่าพลาดตอนถ่าย)

- เปิดคลิปด้วย **สลิป → รายการขึ้น** ภายใน 3 วินาที
- ในคลิปเดียวโชว์อย่างน้อย **3 ฟีเจอร์** (OCR, ลากเมนู, แชร์การ์ด)
- UI มือถือแนวตั้ง สวย ปุ่มใหญ่ — ไม่โชว์เดสก์ทอปรก
- ใช้สลิปเดโม/สลิปตัวเอง — ห้ามโชว์เลขบัตร / ข้อมูลส่วนตัวคนอื่น
- ปิดท้ายด้วย CTA: ลิงก์ในไบโอ / คอมเมนต์คำว่า **「หาร」**

---

## สแต็กแนะนำ (สรุป)

- Next.js 14 App Router + TypeScript + Tailwind + shadcn/ui
- OCR: pluggable — default `mock_demo` (fixture คุณภาพดี) · optional Tesseract/client หรือ API ผ่าน env
- Storage: localStorage (bills / friends / history)
- Deploy: Vercel
- ไม่มี auth · ไม่มีเพย์เมนต์จริงใน MVP (แชร์สรุปอย่างเดียว)

รายละเอียดเต็มอยู่ใน `prd.md` § Tech และ `prompts.md` ส่วน A–H

---

## Acceptance ก่อนประกาศว่า “พร้อมลงคลิป”

- [ ] Must-have ครบ 5 ฟีเจอร์และติ๊กใน `feature_checklist_example`
- [ ] Demo receipt fixture โหลดแล้วได้รายการเมนูครบ
- [ ] ลาก/ติ๊กเมนูให้ ≥3 คน แล้วยอดต่อคนอัปเดตทันที
- [ ] ทิป % + service charge คำนวณถูกต้องตามตัวอย่างใน `examples.json`
- [ ] Share ได้รูปการ์ด + ข้อความคัดลอก LINE บนมือถือจริง
- [ ] Editor ใช้ได้ที่ความกว้าง ~390px ไม่เละ
- [ ] สคริปต์ Reel ใน `examples.json` → `reel_script_th` ถ่ายครบช็อต
