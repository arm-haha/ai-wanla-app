# ReplyKit — ชุดส่งมอบเช้า (AI วันละแอป)

**วันที่:** 2026-10-02 (Asia/Bangkok)  
**วันในคิว:** 5 / 10  
**ช่อง:** AI วันละแอป  
**สถานะ:** Delivery-ready สำหรับรอบเช้าวันที่ห้า

มินิสวีทช่วยร่างข้อความตอบแชท/คอมเมนต์/DM สำหรับคนไทย — วางข้อความอึดอัด → ได้ชุดตอบหลายโทน (นุ่ม / ตลก / มืออาชีพ / หนักแน่น / อบอุ่น) → เลือกโทนด้วย Tone Dial → เก็บสถานการณ์ใน Situation Library → อัปโหลดสกรีนช็อตแชทแล้ว mock ดึงข้อความ → คัดลอก + แชร์การ์ดตอบสวย  
ฮุคหลัก Reel: **วางข้อความแชท → ได้ชุดตอบหลายโทน ใน 10 วินาที**

---

## ไฟล์ในโฟลเดอร์นี้

| ไฟล์ | ใช้ทำอะไร |
|---|---|
| `prd.md` | สเปกผลิตภัณฑ์เต็ม: ปัญหา เป้าหมาย ผู้ใช้ สตอรี่ หน้าจอ เทค acceptance ความเสี่ยง ช็อต Reel |
| `prompts.md` | Prompt หลายส่วนสำหรับ codegen ทั้งแอป / mock paste→replies / tone / share / UI / Reel / QA |
| `schemas.json` | JSON Schema ละเอียดพร้อม description (message, tone, replyOption, replyPack, situation, extract, share, store, analytics) |
| `examples.json` | ตัวอย่างข้อความเพื่อนเงียบ 3 วันเรื่องวันเสาร์ + สคริปต์ Reel + feature checklist + UI copy |
| `README.md` | ไฟล์นี้ — วิธีใช้แพ็ก + ฮุคโพสต์ |

แพ็กเต็มแบบ zip: `/workspace/replykit.zip` (unzip แล้วได้ `replykit/...`)

---

## ฟีเจอร์บังคับ ≥ 5 (Must-have)

| # | ฟีเจอร์ | ทำไมติดรีเทน / ไวรัล |
|---|---|---|
| 1 | **Paste → Reply Pack** | Wow แรกใน 3 วินาที — วางข้อความอึดอัด → ชุดตอบ 3–5 โทนโผล่พร้อมอนิเมชัน |
| 2 | **Tone Dial** | หมุน soft / funny / pro / firm / warm — กรองหรือ gen แพ็กใหม่เมื่อเปลี่ยนโทน |
| 3 | **Situation Library** | คิทไทย: ตอบช้า, ปฏิเสธนุ่มๆ, ทวงงาน, คุยหัวหน้า, ลูกค้าโกรธ, แชทแฟนหรือเพื่อน + สร้าง/เปลี่ยนชื่อ/favorite |
| 4 | **Screenshot → Extract** | อัปโหลดสกรีนช็อตแชท หรือปุ่ม「ใช้รูปเดโม」→ mock ดึงข้อความ inbound ล่าสุด → Reply Pack |
| 5 | **Copy & Share Reply Card** | คัดลอกหนึ่งแตะ + การ์ดแชร์สวย + แคปชัน IG/LINE + navigator.share |

**Nice-to-have (เสริมถ้าเสร็จเร็ว):** Rewrite my draft · Voice preview (speechSynthesis th-TH) · Favorite replies history · Bilingual TH/EN · emoji booster · Dark chat mode

---

## วิธีใช้กับ AI codegen (เช้านี้)

1. เปิด `prompts.md` ส่วน **A) Master prompt** วางเป็นคำสั่งหลัก
2. แนบบริบท: `prd.md` + `schemas.json` + `examples.json`
3. สั่งให้ `npm run dev` ผ่าน และ **happy path จบก่อน** (วางข้อความหรือโหลดเดโม → ได้ Reply Pack → หมุน Tone Dial → เปิด Situation Library → Screenshot extract → คัดลอก/แชร์การ์ด)
4. ใส่ demo chat fixtures ตามส่วน B + ตรวจ `FeatureChecklist` ใน `examples.json`
5. ก่อนถ่าย Reel รันส่วน G (QA) + เช็คลิสต์ `feature_checklist_example`

เป้าเวลา: gen + polish เดโมมือถือใน 1 วัน

---

## ฮุคโพสต์แชท / คาปชันสั้น

> วางข้อความแชท → ได้ชุดตอบหลายโทน ใน 10 วินาที

เวอร์ชันยาวขึ้นเล็กน้อย:

> เพื่อนทักเรื่องวันเสาร์แล้วเงียบ 3 วัน ไม่รู้จะตอบยังไง? วันนี้แจกแอป ReplyKit จากช่อง AI วันละแอป วางข้อความได้ชุดตอบหลายโทน หมุนโทนได้ เก็บสถานการณ์บ่อยๆ แล้วแชร์การ์ดตอบสวย ลองฟรีที่ลิงก์ในไบโอ

---

## กฎช่อง (อย่าพลาดตอนถ่าย)

- เปิดคลิปด้วย **วางข้อความ → ชุดตอบหลายโทนขึ้น** ภายใน 3 วินาที
- ในคลิปเดียวโชว์อย่างน้อย **3 ฟีเจอร์** (Paste → Reply Pack, Tone Dial, Copy & Share Reply Card)
- UI มือถือแนวตั้ง สวย ปุ่มใหญ่ — ไม่โชว์เดสก์ทอปรก
- ใช้ข้อความเดโม/ข้อความตัวเอง — ห้ามเคลม「AI รู้ความสัมพันธ์」หรือ「ตอบแทนคุณได้ 100%」
- ปิดท้ายด้วย CTA: ลิงก์ในไบโอ / คอมเมนต์คำว่า **「ตอบ」**

---

## สแต็กแนะนำ (สรุป)

- Next.js 14 App Router + TypeScript + Tailwind + shadcn/ui
- Paste/Screenshot→Replies: pluggable — default `mock_demo` (fixture คุณภาพดี) · optional LLM API ผ่าน env
- Storage: localStorage (packs / situations / favorites / settings)
- Deploy: Vercel (PWA-ready)
- ไม่มี auth · ไม่เคลมว่ารู้ความสัมพันธ์ · ไม่มีโซเชียลฟีดใน MVP

รายละเอียดเต็มอยู่ใน `prd.md` § Tech และ `prompts.md` ส่วน A–N

---

## Acceptance ก่อนประกาศว่า “พร้อมลงคลิป”

- [ ] Must-have ครบ 5 ฟีเจอร์และติ๊กใน `feature_checklist_example`
- [ ] Demo fixture โหลดแล้วได้ชุดตอบภาษาไทย 4–5 โทน (เพื่อนเงียบ 3 วันเรื่องวันเสาร์)
- [ ] Tone Dial เปลี่ยนโทนแล้วกรอง/regen แพ็กได้
- [ ] Situation Library มีคิทไทยตัวอย่าง ≥6 + สร้าง/เปลี่ยนชื่อ/favorite ได้
- [ ] Screenshot → Extract: ปุ่มใช้รูปเดโม → mock ดึงข้อความ → Reply Pack
- [ ] Copy & Share ได้รูปการ์ดตอบ + คัดลอกแคปชันบนมือถือจริง
- [ ] Editor ใช้ได้ที่ความกว้าง ~390px ไม่เละ
- [ ] สคริปต์ Reel ใน `examples.json` → `reel_script_th` ถ่ายครบช็อต
- [ ] UI มี disclaimer「ตัวช่วยร่างข้อความ」และไม่มีเคลมว่ารู้ความสัมพันธ์

---

## Wow moment ที่ต้องโชว์ในคลิป

ข้อความเพื่อน LINE สไตล์「เดี๋ยวก่อนนน คุยเรื่องวันเสาร์ไปไหนกัน ทำไมเงียบ 3 วันแล้ว 🥺」→ กองการ์ดตอบโทน soft / funny / honest / firm สี teal-mint + coral  
เดโมหลักแนะนำ: **เพื่อนทักเรื่องวันเสาร์ เงียบ 3 วัน → 4–5 ชุดตอบ** (ดู `examples.json` → `paste_reply_example`)

อย่าลืมพูดสั้นๆ ว่าเป็น「ตัวช่วยร่างข้อความ — คุณเลือกส่งเอง」— mock_demo ใช้ถ่าย Reel ได้ ไม่ต้องรอ LLM API

---

## Happy path เป้า ≤ 60 วินาที

1. เปิดแอป → กด「ใช้ข้อความเดโม」หรือวางข้อความเพื่อน  
2. เห็นชุดตอบหลายโทน (soft / funny / honest / firm / warm)  
3. หมุน Tone Dial เลือก soft หรือ funny แล้วดูแพ็กเปลี่ยน  
4. เปิด Situation Library บันทึกเป็น「ตอบช้า · เพื่อน」หรือ favorite  
5. (ออปชันในคลิป) กดใช้รูปเดโม Screenshot → Extract  
6. คัดลอกคำตอบ + แชร์ Reply Card + คัดลอกแคปชัน  

รายละเอียดช็อตถ่ายอยู่ใน `examples.json` → `reel_script_th` และแผนวันเดียวอยู่ใน `prd.md` §20
