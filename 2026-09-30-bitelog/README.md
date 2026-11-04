# BiteLog — ชุดส่งมอบเช้า (AI วันละแอป)

**วันที่:** 2026-09-30 (Asia/Bangkok)  
**วันในคิว:** 3 / 10  
**ช่อง:** AI วันละแอป  
**สถานะ:** Delivery-ready สำหรับรอบเช้าวันที่สาม

มินิสวีทบันทึกมื้ออาหารไทยสำหรับคนทั่วไป — ถ่ายจาน → AI/mock รู้ชื่อเมนูไทย + ประมาณแคลอรี่/แมโคร → ไลบรารีอาหารไทย → แดชบอร์ดรายวัน → เพิ่มเร็ว/รายการโปรด → แชร์การ์ดความคืบหน้า  
ฮุคหลัก Reel: **ถ่ายอาหาร → รู้แคลอรี่และมื้อไทย ใน 10 วินาที**

---

## ไฟล์ในโฟลเดอร์นี้

| ไฟล์ | ใช้ทำอะไร |
|---|---|
| `prd.md` | สเปกผลิตภัณฑ์เต็ม: ปัญหา เป้าหมาย ผู้ใช้ สตอรี่ หน้าจอ เทค acceptance ความเสี่ยง ช็อต Reel |
| `prompts.md` | Prompt หลายส่วนสำหรับ codegen ทั้งแอป / mock vision / macro engine / share / UI / Reel / QA |
| `schemas.json` | JSON Schema ละเอียดพร้อม description (meal, food, macros, scan, share, store, analytics) |
| `examples.json` | ตัวอย่างมื้อไทย + สคริปต์ Reel + feature checklist + UI copy |
| `README.md` | ไฟล์นี้ — วิธีใช้แพ็ก + ฮุคโพสต์ |

แพ็กเต็มแบบ zip: `/workspace/bitelog.zip` (unzip แล้วได้ `bitelog/...`)

---

## ฟีเจอร์บังคับ ≥ 5 (Must-have)

| # | ฟีเจอร์ | ทำไมติดรีเทน / ไวรัล |
|---|---|---|
| 1 | **Photo Bite Scan** | Wow แรกใน 3 วินาที — รูปจานธรรมดา → การ์ดโภชนาการสีสด + ชื่อเมนูไทย |
| 2 | **Thai Food Library** | ค้นหาพรีเซ็ตเมนูไทยยอดฮิต (ก๋วยเตี๋ยว ข้าวผัด ส้มตำ ชาไทย ฯลฯ) + ขนาดเสิร์ฟ |
| 3 | **Daily Macro Dashboard** | วงแหวน/แถบ kcal · โปรตีน · คาร์บ · ไขมัน vs เป้า + ไทม์ไลน์มื้อวันนี้ |
| 4 | **Quick Add & Favorites** | 1-tap เพิ่มมื้อโปรด/ล่าสุด ปรับปริมาณ (+/-) เร็ว |
| 5 | **Share Progress Card** | การ์ดวัน/สตรีคสวย + คัดลอกแคปชัน IG/LINE |

**Nice-to-have (เสริมถ้าเสร็จเร็ว):** Water tracker · Meal tags (เช้า/กลางวัน/เย็น/ของว่าง) · Weekly chart · Streak & gentle reminders copy · Offline localStorage history

---

## วิธีใช้กับ AI codegen (เช้านี้)

1. เปิด `prompts.md` ส่วน **A) Master prompt** วางเป็นคำสั่งหลัก
2. แนบบริบท: `prd.md` + `schemas.json` + `examples.json`
3. สั่งให้ `npm run dev` ผ่าน และ **happy path จบก่อน** (ถ่าย/อัปโหลดหรือโหลดเดโม → scan result → ยืนยันปริมาณ → บันทึก → แดชบอร์ดอัปเดต → แชร์การ์ด)
4. ใส่ demo meal photo fixtures ตามส่วน B + ตรวจ `FeatureChecklist` ใน `examples.json`
5. ก่อนถ่าย Reel รันส่วน H (QA) + เช็คลิสต์ `feature_checklist_example`

เป้าเวลา: gen + polish เดโมมือถือใน 1 วัน

---

## ฮุคโพสต์แชท / คาปชันสั้น

> ถ่ายอาหาร → รู้แคลอรี่และมื้อไทย ใน 10 วินาที

เวอร์ชันยาวขึ้นเล็กน้อย:

> กินข้าวแล้วไม่รู้จะใส่มื้อไหนกี่แคล วันนี้แจกแอป BiteLog จากช่อง AI วันละแอป ถ่ายจานรู้ชื่อเมนูไทย+แคลอรี่ ประมาณแมโคร ดูแดชบอร์ดรายวัน แล้วแชร์การ์ดความคืบหน้าได้เลย ลองฟรีที่ลิงก์ในไบโอ

---

## กฎช่อง (อย่าพลาดตอนถ่าย)

- เปิดคลิปด้วย **รูปจาน → การ์ดโภชนาการขึ้น** ภายใน 3 วินาที
- ในคลิปเดียวโชว์อย่างน้อย **3 ฟีเจอร์** (Photo Bite Scan, Dashboard, Share Card)
- UI มือถือแนวตั้ง สวย ปุ่มใหญ่ — ไม่โชว์เดสก์ทอปรก
- ใช้รูปอาหารเดโม/จานตัวเอง — ห้ามเคลมความแม่นระดับแพทย์/นักโภชนาการ
- ปิดท้ายด้วย CTA: ลิงก์ในไบโอ / คอมเมนต์คำว่า **「แคล」**

---

## สแต็กแนะนำ (สรุป)

- Next.js 14 App Router + TypeScript + Tailwind + shadcn/ui
- Food vision: pluggable — default `mock_demo` (fixture คุณภาพดี) · optional vision API ผ่าน env
- Storage: localStorage (daily logs / favorites / history)
- Deploy: Vercel (PWA-ready)
- ไม่มี auth · ไม่มีเคลมทางการแพทย์ · ไม่มีโซเชียลฟีดใน MVP

รายละเอียดเต็มอยู่ใน `prd.md` § Tech และ `prompts.md` ส่วน A–H

---

## Acceptance ก่อนประกาศว่า “พร้อมลงคลิป”

- [ ] Must-have ครบ 5 ฟีเจอร์และติ๊กใน `feature_checklist_example`
- [ ] Demo meal fixture โหลดแล้วได้ชื่อเมนูไทย + kcal/macros สมเหตุสมผล
- [ ] ยืนยันปริมาณแล้วบันทึก → แดชบอร์ด (rings/bars) อัปเดตทันที
- [ ] Thai Food Library ค้นหาได้ ≥ 8 เมนูตัวอย่าง + ปรับ portion
- [ ] Quick Add จาก Favorites / Recent ใช้งานได้
- [ ] Share ได้รูปการ์ดวัน/สตรีค + คัดลอกแคปชันบนมือถือจริง
- [ ] Editor ใช้ได้ที่ความกว้าง ~390px ไม่เละ
- [ ] สคริปต์ Reel ใน `examples.json` → `reel_script_th` ถ่ายครบช็อต
- [ ] UI ไม่มีข้อความ guilt-shame และมี disclaimer ประมาณการชัด


---

## Wow moment ที่ต้องโชว์ในคลิป

รูปอาหารธรรมดา/เบลอเล็กน้อย → การ์ดโภชนาการสีครีม-coral + ชื่อเมนูไทยชัด + ตัวเลข kcal ใหญ่  
เดโมหลักแนะนำ: **ข้าวผัดกุ้งไข่ดาว ~720 kcal** (ดู `examples.json` → `meal_scan_example`)

อย่าลืมพูดสั้นๆ ว่าเป็น「ประมาณการ」— mock_demo ใช้ถ่าย Reel ได้ ไม่ต้องรอ Vision API

---

## Happy path เป้า ≤ 60 วินาที

1. เปิดแอป → กด「ใช้รูปเดโม」  
2. เห็นผลสแกนชื่อไทย + kcal/macros  
3. ปรับปริมาณ (+/-) แล้วบันทึก  
4. Daily Macro Dashboard อัปเดต rings/bars  
5. แชร์ Share Progress Card + คัดลอกแคปชัน  

รายละเอียดช็อตถ่ายอยู่ใน `examples.json` → `reel_script_th` และแผนวันเดียวอยู่ใน `prd.md` §20
