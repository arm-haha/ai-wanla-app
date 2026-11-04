# ClosetDice — ชุดส่งมอบเช้า (AI วันละแอป)

**วันที่:** 2026-10-05 (Asia/Bangkok)  
**วันในคิว:** 6 / 10  
**ช่อง:** AI วันละแอป  
**สถานะ:** Delivery-ready สำหรับรอบเช้าวันที่หก

มินิสวีทตู้เสื้อผ้า + สุ่มชุดแต่งตัวสำหรับคนไทย — ถ่ายรูปเสื้อผ้า → ตัดพื้นหลัง + ติดแท็กอัตโนมัติ → กด **ทอยลูกเต๋า** → ได้ชุด flat-lay ตามอากาศและโอกาส → ล็อกชิ้นที่ชอบแล้วทอยที่เหลือ → บันทึกปฏิทิน OOTD กันใส่ซ้ำ → แชร์การ์ดลุคสวย  
ฮุคหลัก Reel: **เสื้อผ้าเต็มตู้แต่ไม่มีอะไรใส่? ทอยทีเดียว ได้ชุดเลย 🎲**

---

## ไฟล์ในโฟลเดอร์นี้

| ไฟล์ | ใช้ทำอะไร |
|---|---|
| `prd.md` | สเปกเต็ม: ปัญหา เป้าหมาย persona สตอรี่ ฟีเจอร์ กติกาสุ่มชุด หน้าจอ เทค acceptance ความเสี่ยง ช็อต Reel แผนวันเดียว |
| `prompts.md` | Prompt A–N: master codegen / ตู้เดโม / types / Outfit Engine / vision tagging / UI ลูกเต๋า+flat-lay / Snap / Calendar / Share / nice-to-have / Reel / QA / แก้บั๊ก / รูปเดโม |
| `schemas.json` | JSON Schema (draft 2020-12): ClothingItem, ClothingTagResult, OutfitFilters, LockState, Outfit, DiceRoll, WearLogEntry, ShareCard, SharePayload, Settings, LocalStore, AnalyticsEvent, FeatureChecklist |
| `examples.json` | ตู้เดโม 14 ชิ้นของ "ฟ้า" + ผลทอย rain/office (seed 20261005) + ทอยแบบล็อก + no_valid + wear log + การ์ดแชร์ + UI copy ไทย + สคริปต์ Reel (ตรวจกับ schema แล้ว ผ่าน 0 error) |
| `README.md` | ไฟล์นี้ |

แพ็กเต็มแบบ zip: `/workspace/closetdice.zip` (unzip แล้วได้ `closetdice/...`)

---

## ฟีเจอร์บังคับ ≥ 5 (Must-have)

| # | ฟีเจอร์ | ทำไมติดรีเทน / ไวรัล |
|---|---|---|
| 1 | **Snap → Closet** | Wow แรก — เสื้อยับบนเตียงกลายเป็นสติกเกอร์ตัดพื้นหลัง + แท็ก "เชิ้ต · ครีม · ออฟฟิศ" เด้งเอง |
| 2 | **Outfit Dice** ⭐ | ไฮไลต์หลัก — ลูกเต๋า 3D หมุน → ชิ้นร่วงประกอบเป็น flat-lay + คะแนนเข้ากัน + ชื่อลุคไทย |
| 3 | **Weather & Occasion Lock** | ชิป 🌧ฝน/💼ออฟฟิศ + 🔒 ล็อกชิ้นที่ชอบ ทอยใหม่เฉพาะที่เหลือ — ความเป็นเกมทำให้คนอยากลอง |
| 4 | **OOTD Calendar** | กด「ใส่ชุดนี้วันนี้」→ ปฏิทินเต็มภาพชุด + streak + ไม่สุ่มซ้ำ 7 วัน = เหตุผลเปิดทุกเช้า |
| 5 | **Share Outfit Card** | การ์ด story/feed สวย + แคปชันพร้อม → ลง IG/LINE = โฆษณาแอปให้ฟรี |

**Nice-to-have:** ชิ้นถูกลืม/สถิติตู้ (cost-per-wear) · 7-Day Dice Challenge · Trip Packing Dice · Friend Vote 3 ลุค · Color Harmony hint · Dark mode + เสียงลูกเต๋า/สั่น

---

## วิธีใช้กับ AI codegen (เช้านี้)

1. เปิด `prompts.md` ส่วน **A) Master prompt** วางเป็นคำสั่งหลัก
2. แนบบริบท: `prd.md` + `schemas.json` + `examples.json`
3. สั่งให้ `npm run dev` ผ่าน และ **happy path จบก่อน** (ตู้เดโม → ฝน+ออฟฟิศ → ทอย → ล็อก → ทอย → ใส่ชุดนี้ → แชร์)
4. ส่วน **D** สร้าง `lib/dice.ts` + เทสต์ (หัวใจของแอป) · ส่วน **N** สร้างรูปเดโม 14 ชิ้น
5. ค่อยทำ Snap ของจริง (ส่วน G) · ก่อนถ่ายรันส่วน **L (QA)** + ติ๊ก `feature_checklist_example`

เป้าเวลา: gen + polish เดโมมือถือใน 1 วัน (ตารางใน `prd.md` §20)

---

## ฮุคโพสต์ / คาปชันสั้น

> เสื้อผ้าเต็มตู้แต่ไม่มีอะไรใส่? ทอยทีเดียว ได้ชุดเลย 🎲

เวอร์ชันยาว:

> ทุกเช้ายืนหน้าตู้ 15 นาทีแล้วจบที่เสื้อตัวเดิม? วันนี้แจกแอป ClosetDice จากช่อง AI วันละแอป ถ่ายเสื้อผ้าเข้าตู้ บอกว่าฝนตกไปทำงาน กดทอยลูกเต๋า ได้ชุดเลย ล็อกตัวที่ชอบแล้วทอยใหม่ได้ จำให้ว่าใส่อะไรไปแล้วไม่ให้ซ้ำ คอมเมนต์ "ทอย" รับลิงก์ฟรี

---

## กฎช่อง (อย่าพลาดตอนถ่าย)

- เปิดคลิปด้วย **ตู้เต็ม → นิ้วจิ้มลูกเต๋า** ภายใน 3 วินาที
- โชว์อย่างน้อย **3 ฟีเจอร์** ในคลิปเดียว (Snap → Closet, Outfit Dice + Lock, Share/Calendar)
- ใช้ seed `20261005` + ฝน/ออฟฟิศ เพื่อให้ได้ลุคสวยเดิมทุกเทค ("Minimal ครีม-กรม วันฝนพรำ ☔" คะแนน 86)
- จบด้วยใส่ชุดจริงเดินออกประตู = before/after ที่คนดูเชื่อ
- ห้ามพูดเรื่องรูปร่าง ("ดูผอม/ดูสูง") — คะแนนคือความเข้ากันของสีเท่านั้น
- CTA: คอมเมนต์คำว่า **「ทอย」**

---

## สแต็กแนะนำ (สรุป)

- Next.js 14 App Router + TypeScript + Tailwind + shadcn/ui + framer-motion
- Outfit engine pure `lib/dice.ts` (seeded) · tagging/cutout pluggable — default `mock_demo`
- รูป IndexedDB (webp ≤600px) · metadata localStorage · ไม่มี backend/auth
- Share: html-to-image + navigator.share · อากาศ optional Open-Meteo
- Deploy: Vercel (PWA)

---

## Acceptance ก่อนประกาศว่า “พร้อมลงคลิป”

- [ ] Must-have ครบ 5 และติ๊กใน `feature_checklist_example`
- [ ] 「ลองตู้เดโม」โหลด 14 ชิ้น PNG โปร่งใส < 1s
- [ ] ทอย 20 ครั้ง ฝน+ออฟฟิศ ไม่มีผ้าใบขาว/โลฟเฟอร์ ไม่มีชุดนอกช่วง formality
- [ ] ล็อกเสื้อแล้วทอย 10 ครั้ง เสื้อไม่เปลี่ยน
- [ ] ใส่ชุดนี้ → ปฏิทินขึ้น → ไม่สุ่มซ้ำ 7 วัน → อยู่หลังรีเฟรช
- [ ] Snap จากกล้องมือถือจริงได้ (หรือ fallback ใน 25 วิ) แท็กแก้ได้
- [ ] การ์ดแชร์ story/feed ฟอนต์ไทยครบ แชร์ได้ iOS + Android
- [ ] 360–430px ไม่ล้น · ลูกเต๋าลื่นตอนอัดจอ
- [ ] มี disclaimer「AI ช่วยแนะนำ — สไตล์สุดท้ายเป็นของคุณ」

---

## Wow moment ที่ต้องโชว์ในคลิป

1. **เสื้อเชิ้ตยับบนเตียง → สติกเกอร์ลอยตัดพื้นหลัง + แท็กเด้ง**
2. **ลูกเต๋าลาเวนเดอร์หมุน → เชิ้ตครีม + แจ็กเก็ตกันฝนสีเนย + สแล็กกรม + รัดส้นยางดำ + กระเป๋าผ้าร่วงลงเป็น flat-lay** → ล็อกเสื้อ → ทอยอีก → กลายเป็นพลีทเบจ ("Soft ครีม-เบจ ☁️")

ดู `examples.json` → `dice_roll_example`, `reroll_with_lock_example`, `reel_script_th`
