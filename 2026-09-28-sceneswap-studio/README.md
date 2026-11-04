# SceneSwap Studio — ชุดส่งมอบเช้า (AI วันละแอป)

**วันที่:** 2026-09-28 (Asia/Bangkok)  
**วันในคิว:** 1 / 10  
**ช่อง:** AI วันละแอป  
**สถานะ:** Delivery-ready สำหรับรอบเช้าวันแรก

มินิสวีทเปลี่ยนพื้นหลังรูปโปร + ใส่ฉากใหม่ เน้น before/after wow ใน 15–30 วินาที  
ฮุคหลัก Reel: **smart cutout + สลับฉากทันที**

---

## ไฟล์ในโฟลเดอร์นี้

| ไฟล์ | ใช้ทำอะไร |
|---|---|
| `prd.md` | สเปกผลิตภัณฑ์เต็ม: ปัญหา เป้าหมาย ผู้ใช้ สตอรี่ หน้าจอ เทค acceptance ความเสี่ยง ช็อต Reel |
| `prompts.md` | Prompt หลายส่วนสำหรับ codegen ทั้งแอป / ฉาก / compose / export / UI / Reel / QA |
| `schemas.json` | JSON Schema ละเอียดพร้อม description (โปรเจกต์ ฉาก export history analytics) |
| `examples.json` | ตัวอย่างข้อมูลจริง + สคริปต์ Reel + feature checklist + UI copy |
| `README.md` | ไฟล์นี้ — วิธีใช้แพ็ก + ฮุคโพสต์ |

แพ็กเต็มแบบ zip: `/workspace/sceneswap-studio.zip` (unzip แล้วได้ `sceneswap-studio/...`)

---

## ฟีเจอร์บังคับ ≥ 5 (Must-have)

| # | ฟีเจอร์ | ทำไมติดรีเทน / ไวรัล |
|---|---|---|
| 1 | **Smart Cutout** | Wow แรกใน 3 วินาที — ถอดพื้นหลังอัตโนมัติ |
| 2 | **Scene Library** | ≥20 ฉาก สลับเร็วๆ บน subject เดิม = คลิปเด็ด |
| 3 | **Custom Scene Upload** | ใส่ฉากตัวเอง → ใช้ซ้ำทุกวัน |
| 4 | **Light & Shadow Match** | ทำให้ผลดูจริง ไม่ลอยจากฉาก |
| 5 | **Export Pack** | PNG โปร่งใส + IG 1:1 + Story 9:16 + LinkedIn + Shopee |

**Nice-to-have (เสริมถ้าเสร็จเร็ว):** Hair/Edge Refine · Batch 3 รูป · Favorites + History (local)

---

## วิธีใช้กับ AI codegen (เช้านี้)

1. เปิด `prompts.md` ส่วน **A) Master prompt** วางเป็นคำสั่งหลัก
2. แนบบริบท: `prd.md` + `schemas.json` + `examples.json`
3. สั่งให้ `npm run dev` ผ่าน และ **happy path จบก่อน** (อัปโหลด → cutout → สลับฉาก → แสง → export)
4. เติม Scene Library assets ตามส่วน B + ตรวจ `FeatureChecklist` ใน `examples.json`
5. ก่อนถ่าย Reel รันส่วน H (QA) + เช็คลิสต์ `feature_checklist_example`

เป้าเวลา: gen + polish เดโมมือถือใน 1 วัน

---

## ฮุคโพสต์แชท / คาปชันสั้น

> ถอดพื้นหลัง + ใส่ฉากใหม่ ใน 10 วินาที — รูปโปรสวยพร้อมลงทุกแอป

เวอร์ชันยาวขึ้นเล็กน้อย:

> ห้องรก → ดาดฟ้ากรุงเทพ ในคลิกเดียว วันนี้แจกแอป SceneSwap Studio จากช่อง AI วันละแอป ลองฟรีที่ลิงก์ในไบโอ แล้วคอมเมนต์ฉากที่อยากได้

---

## กฎช่อง (อย่าพลาดตอนถ่าย)

- เปิดคลิปด้วย **before/after ภายใน 3 วินาที**
- ในคลิปเดียวโชว์อย่างน้อย **3 ฟีเจอร์** (cutout, สลับฉาก, export)
- UI มือถือแนวตั้ง สวย ปุ่มใหญ่ — ไม่โชว์เดสก์ทอปรก
- ห้ามใช้ฉากที่มีใบหน้าคนจริงหรือโลโก้แบรนด์โดยไม่มีสิทธิ์
- ปิดท้ายด้วย CTA: ลิงก์ในไบโอ / คอมเมนต์คำว่า **「ฉาก」**

---

## สแต็กแนะนำ (สรุป)

- Next.js 14 App Router + TypeScript + Tailwind + shadcn/ui
- Cutout: `@imgly/background-removal` (client) เป็นค่าเริ่มต้น
- Compose: Canvas 2D
- Storage: localStorage (history / favorites)
- Deploy: Vercel

รายละเอียดเต็มอยู่ใน `prd.md` § Tech และ `prompts.md` ส่วน A–F

---

## Acceptance ก่อนประกาศว่า “พร้อมลงคลิป”

- [ ] Must-have ครบ 5 ฟีเจอร์และติ๊กใน `feature_checklist_example`
- [ ] ฉากในไลบรารี ≥ 20
- [ ] Export ได้ PNG โปร่งใส + 9:16 + 1:1 บนมือถือจริง
- [ ] Editor ใช้ได้ที่ความกว้าง ~390px ไม่เละ
- [ ] สคริปต์ Reel ใน `examples.json` → `reel_script_th` ถ่ายครบช็อต
