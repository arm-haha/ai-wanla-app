# PRD: SceneSwap Studio

**Product name:** SceneSwap Studio  
**Tagline (TH):** เปลี่ยนพื้นหลังรูปโปร ในคลิกเดียว — สวยพร้อมลงทุกแอป  
**Tagline (EN):** Smart cutout + instant scene swap for everyday creators  
**Version:** 1.0 (MVP — AI-วันละแอป Day 1/10)  
**Channel date:** 2026-09-28 (Asia/Bangkok)  
**Platform:** Web app (mobile-first) + PWA  
**Language:** Thai UI first, English secondary  
**Status:** Delivery-ready for official morning run  
**Related docs:** `README.md`, `prompts.md`, `schemas.json`, `examples.json`  
**Last updated:** 2026-09-28 (Asia/Bangkok)

---

## 1. สรุปสั้นๆ

แอปมินิสวีทให้คนทั่วไปอัปโหลดเซลฟี/รูปสินค้า → ถอดพื้นหลังอัตโนมัติ → เลือกฉากจากไลบรารีหรืออัปโหลดเอง → ปรับแสงเงาให้เข้าฉาก → ส่งออกหลายขนาดพร้อมลง IG / LinkedIn / Shopee / Story

ออกแบบให้เดโมใน Reel 15–30 วินาทีเห็น before/after ชัด และมีฟีเจอร์รองที่ดึงคนกลับมาเปิดซ้ำ (ไลบรารีฉาก, custom scene, export pack, history)

MVP ไม่มีบัญชีผู้ใช้ ไม่มีเครดิตจ่ายเงิน ไม่ตัดวิดีโอ

---

## 2. ปัญหาที่แก้

| ปัญหาวันนี้ | ผลกระทบ |
|---|---|
| รูปโปรพื้นหลังห้องรก / ออฟฟิศไม่เรียบร้อย | ไม่กล้าส่งงาน ลงหางาน หรือโพสต์ขายของ |
| แอปตัดพื้นหลังใหญ่ซับซ้อน / มีลายน้ำ / บังคับสมัคร | คนไทยทั่วไปเลิกใช้กลางคัน |
| ใส่ฉากแล้วคนลอย ไม่มีเงา/แสงไม่เข้า | ดูปลอม ใช้จริงไม่ได้ |
| ส่งออกขนาดเดียว ต้องครอปเองหลายรอบ | เสียเวลา ครีเอเตอร์เลิกแชร์ |
| เครื่องมือ B2B / editor มืออาชีพ | ไม่เหมาะเดโม Reel 15–30 วินาที |

**โอกาสช่อง AI วันละแอป:** แจกแอปฟรีที่ผลลัพธ์เห็นทันที → save rate สูง → คนเข้าลิงก์ลอง → ติดตามเพื่อรอแอปวันถัดไป

---

## 3. เป้าหมายผลิตภัณฑ์

### 3.1 Goals (MVP / วันเดียว + คลิปเช้า)

1. Happy path จบบนมือถือ: อัปโหลด → cutout → สลับฉาก ≥3 ใบ → ปรับแสง → export ได้ภายใน **≤ 60 วินาที** สำหรับผู้ใช้ทั่วไป
2. มี **≥ 5 ฟีเจอร์ must-have** ที่ใช้ได้จริงและโชว์ในคลิปได้อย่างน้อย 3 ตัว
3. ฉากในไลบรารี **≥ 20** ใบ แบ่งหมวดชัด
4. Cutout สำเร็จกับรูปคนชัด **≥ 8/10** เคสทดสอบมาตรฐาน
5. คลิป Reel 25–35 วินาทีถ่ายจบด้วย UI จริง ไม่ใช่ mock อย่างเดียว

### 3.2 Non-goals (MVP)

- ไม่มีระบบล็อกอิน / เครดิต / เพย์วอลล์
- ไม่ตัดพื้นหลังวิดีโอ
- ไม่มีชุมชนแชร์ฉากออนไลน์
- ไม่มี native iOS/Android store build
- ไม่ฝึกโมเดลตัดพื้นหลังเอง — ใช้ไลบรารี client หรือ API สำเร็จรูป
- ไม่ทำ batch ขนาดใหญ่ (nice มีแค่ 3 รูป)

---

## 4. ผู้ใช้และบทบาท

| บทบาท | ความต้องการหลัก |
|---|---|
| **ครีเอเตอร์ / คนทั่วไป (หลัก)** | รูปโปรสวยเร็ว ลงสตอรี่/หางาน/ขายของได้ทันที |
| **แม่ค้า Shopee / IG** | พื้นหลังโปร่งใส + ฉากสตูดิโอสำหรับรูปสินค้า |
| **ผู้ชมช่อง AI วันละแอป** | เห็น wow ใน 3 วินาที อยากลองลิงก์ในไบโอ |
| **ผู้สร้างคลิป (เรา)** | gen แอปใน 1 วัน มีสคริปต์ช็อตและเช็คลิสต์พร้อมถ่าย |

---

## 5. User stories

1. ในฐานะผู้ใช้ ฉันอัปโหลดเซลฟีแล้วได้ subject โปร่งใสอัตโนมัติภายในไม่กี่วินาที
2. ในฐานะผู้ใช้ ฉันปัดเลือกฉากในไลบรารีแล้วเห็นผลบน canvas ทันทีโดยไม่ต้องตัดรูปใหม่
3. ในฐานะผู้ใช้ ฉันอัปโหลดรูปฉากของตัวเองแล้วลาก/ซูม/หมุน subject ให้เข้าเฟรม
4. ในฐานะผู้ใช้ ฉันปรับสไลเดอร์แสงและเงาแล้วรู้สึกว่าคนกลมกับฉากขึ้น
5. ในฐานะผู้ใช้ ฉันส่งออกได้ทั้ง PNG โปร่งใส และ JPG ขนาด Story 9:16 / IG 1:1 ในครั้งเดียว
6. ในฐานะผู้ชม Reel ฉันเห็น before/after ใน 3 วินาทีแรกแล้วอยากลองแอป
7. ในฐานะระบบ ทุกโปรเจกต์ต้องเก็บ state ตาม `ProjectState` และ history ตาม `LocalStore`

---

## 6. ฮุค Reel (3 วินาทีแรก)

**Before:** เซลฟีพื้นหลังห้องรก  
**After:** ยืนบนดาดฟ้าเมือง / สตูดิโอขาว / คาเฟ่แสงอุ่น (สลับเร็ว 2 ครั้ง)  
**ข้อความบนจอ:** `ถอดพื้นหลัง + ใส่ฉากใหม่ ใน 10 วินาที`  
**เสียง:** 「รูปโปรพื้นหลังรก แก้ได้ในคลิกเดียว」

**Wow moment กลางคลิป:** สลับฉาก 4–5 ใบเร็วๆ บน subject เดิม เห็น diff ชัด

---

## 7. ทำไมคนติดตาม / เปิดซ้ำ

- ผลก่อน–หลังทันที (เหมาะ Reel + save)
- ใช้จริงได้: รูปโปรส่งงาน, LinkedIn, Shopee, นามบัตร, สตอรี่
- แจกฟรีจากช่อง → เซฟคลิป + เข้าลิงก์
- รีเทนชัน: Scene Library ชุดใหม่, Custom Scene, Favorites, History, Export หลายขนาด
- คอมเมนต์ขอฉาก = สัญญาณทำคลิปต่อ / อัปเดตไลบรารี

---

## 8. กฎผลิตภัณฑ์ช่อง

- **ขั้นต่ำ 5 ฟีเจอร์** must-have (ตารางด้านล่าง)
- Gen ได้ใน 1 วันด้วย AI codegen (Next.js + cutout client/API)
- เดโมหลักจบในมือถือแนวตั้ง (~390px)
- UI สวย พอเป็นพรีวิว “แอปจริง” ไม่ใช่ฟอร์มดิบ
- ภาษาไทยก่อน — คีย์สคีมาภาษาอังกฤษได้

---

## 9. ฟีเจอร์

### 9.1 Must-have (≥ 5)

| # | ฟีเจอร์ | รายละเอียด | Acceptance ย่อ |
|---|---|---|---|
| 1 | **Smart Cutout** | ถอดพื้นหลังคน/สินค้าอัตโนมัติ แสดง progress สวย เป้า ≤ 3s บนรูปเดโม | สำเร็จ ≥8/10 เคสทดสอบ |
| 2 | **Scene Library** | ≥20 ฉาก หมวด Studio / City / Nature / Cafe / Gradient (+ Abstract) | สลับฉากไม่ต้อง cutout ใหม่ |
| 3 | **Custom Scene Upload** | อัปโหลดฉากเอง + จัดตำแหน่ง subject (ลาก ซูม หมุน) | รองรับ JPG/PNG |
| 4 | **Light & Shadow Match** | สไลเดอร์ brightness / contrast / shadowStrength / shadowOffsetY | เห็นผลบน canvas ทันที |
| 5 | **Export Pack** | PNG โปร่งใส, JPG, พรีเซ็ต IG 1:1, Story 9:16, LinkedIn, Shopee | ดาวน์โหลดได้บน iPhone Safari |

### 9.2 Nice-to-have

| # | ฟีเจอร์ | รายละเอียด |
|---|---|---|
| 6 | **Hair/Edge Refine** | แปรง erase/restore ขอบละเอียด |
| 7 | **Batch (3 รูป)** | ใช้ฉากเดียวกันกับหลาย subject |
| 8 | **Favorites + History** | ฉากโปรด + ผลลัพธ์ล่าสุด 10 รายการ (localStorage) |

---

## 10. ขอบเขตฟีเจอร์

### 10.1 In scope

- Home, Editor, Scenes sheet/page, Export sheet, History
- Client-side cutout เป็นค่าเริ่มต้น + ช่องเสียบ API (remove.bg / Replicate) ถ้าระบุ key
- Compose บน Canvas 2D
- Scene manifest JSON ตาม schema
- Analytics events ฝั่ง client (optional log)
- PWA ติดตั้งได้แบบพื้นฐาน (manifest + icons)

### 10.2 Out of scope (เฟสถัดไป)

- Auth / cloud sync โปรเจกต์
- วิดีโอ / webcam realtime cutout ยาว
- ตลาดฉากจากคอมมูนิตี้
- AI gen ฉากจากข้อความในแอป (ทำนอกแบนด์ตอนสร้าง asset ได้)
- การชำระเงินและเครดิต

---

## 11. User flow หลัก (Happy path)

```text
เปิดแอป → อัปโหลดหรือถ่ายรูป
  → Auto cutout (skeleton/progress เป้า ≤ 3s)
  → เลือกฉากจากไลบรารี หรืออัปโหลดฉากเอง
  → ปรับตำแหน่ง / สเกล / หมุน
  → ปรับแสงเงา
  → (ออปชัน) refine ขอบ
  → เลือกพรีเซ็ตส่งออก → ดาวน์โหลดหรือแชร์
  → บันทึก history ท้องถิ่น
```

### สถานะโปรเจกต์

`idle` → `cutting` → `ready` → `exporting`  
ทางแยก: `error` (พร้อมข้อความไทยสั้นๆ + ปุ่มลองใหม่)

---

## 12. หน้าจอ (MVP)

| # | หน้าจอ | องค์ประกอบหลัก |
|---|---|---|
| 1 | **Home** | โลโก้, หัวข้อไทย, แถบก่อน/หลังเลื่อนได้ 3 ตัวอย่าง, CTA「เริ่มเลย」, แถบ 5 ฟีเจอร์ไอคอน |
| 2 | **Editor** | canvas subject+scene, แถบฉากแนวนอน, ปุ่มอัปโหลดฉาก, สไลเดอร์แสง, ปุ่มส่งออก, เทียบก่อน/หลัง |
| 3 | **Scenes** | กริดหมวด + ช่องค้นหา/แท็ก + ปุ่มหัวใจ favorites |
| 4 | **Export** | การ์ดพรีเซ็ตขนาด, ปุ่มดาวน์โหลด / แชร์, พรีวิวสัดส่วน |
| 5 | **History** | กริดผลลัพธ์ล่าสุด 10 รายการ จาก localStorage |

**โทนแบรนด์:** พื้นดำ–เทาเข้ม, ไฮไลต์ม่วงนีออนอ่อน, ปุ่ม primary ใหญ่, ฟอนต์ system/Inter, เน้นพื้นที่ว่างและภาพเดโม

---

## 13. ความต้องการเชิงฟังก์ชัน

### FR-1 Smart Cutout
- รับไฟล์ภาพจากไฟล์หรือกล้อง
- รัน engine ตาม `cutout_engine` (ค่าเริ่ม `imgly_client`)
- เก็บ `cutout_ms`, ขนาด, object URL ใน `ProjectState.subject`

### FR-2 Scene Library
- โหลด `SceneManifest` จาก `/scenes/manifest.json`
- กรองตามหมวด / แท็ก
- สลับ `scene_id` โดยไม่ทำลาย cutout

### FR-3 Custom Scene
- อัปโหลดภาพเป็นฉาก `mode=custom`
- จำกัดขนาดไฟล์สมเหตุสมผล (เช่น ≤ 12MB) พร้อมข้อความไทยเมื่อเกิน

### FR-4 Transform + Light
- แพน/พินช์ซูม/หมุนบนสัมผัส
- สไลเดอร์แสงเงาแมปเข้า `LightSettings`

### FR-5 Export Pack
- พรีเซ็ตตาม `ExportPresetId`
- ชื่อไฟล์ `sceneswap-{preset}-{timestamp}.{ext}`
- รองรับ `navigator.share` ถ้ามี

### FR-6 Local retention
- บันทึก favorites + history ตาม `LocalStore`
- ไม่บังคับ auth

### FR-7 Analytics (เบา)
- ยิงอีเวนต์ตาม enum ใน schema (console หรือ provider ภายหลัง)

---

## 14. ความต้องการเชิงไม่ใช่ฟังก์ชัน

| หัวข้อ | เป้า |
|---|---|
| Cutout latency (รูปเดโม) | p50 ≤ 3s บนเดสก์ท็อปใหม่; มือถือกลาง ≤ 8s ยอมรับได้ |
| Editor frame | โต้ตอบสไลเดอร์ลื่น ≥ 30fps บนเครื่องกลาง |
| Mobile layout | ใช้งานได้ที่ 390×844 โดยไม่เลื่อนแนวนอนพัง |
| ภาษา | th-TH เป็นค่าเริ่มต้น |
| ความเป็นส่วนตัว | ประมวลผลรูปฝั่ง client เป็นหลัก ไม่อัปโหลดเซิร์ฟเวอร์ถ้าไม่ใช้ API ภายนอก |
| Deploy | Vercel preview URL พร้อมแชร์ในไบโอ |

---

## 15. Tech แนะนำสำหรับ gen วันเดียว

| ชั้น | เลือก |
|---|---|
| Frontend | Next.js 14 (App Router) + TypeScript + Tailwind + shadcn/ui |
| Cutout | `@imgly/background-removal` (default) · optional remove.bg / Replicate |
| Compose | Canvas 2D (`lib/compose.ts`) หรือ Fabric.js ถ้าจำเป็น |
| Export | `lib/export.ts` + พรีเซ็ตคงที่ |
| State | React state + `lib/storage.ts` (localStorage) |
| Assets | `/public/scenes/**` + `manifest.json` |
| Deploy | Vercel |

**โครงสร้างรีโปแนะนำ**

```text
/sceneswap-studio
  README.md
  prd.md
  prompts.md
  schemas.json
  examples.json
  /app
  /components
  /lib
    compose.ts
    export.ts
    storage.ts
    cutout.ts
  /public/scenes
```

ถ้าไม่มี API key: ใช้ client-side removal เป็นหลัก แล้วหมายเหตุใน UI ว่า「ประมวลผลบนเครื่องคุณ」

---

## 16. ข้อมูลและสคีมา

แหล่งความจริง (ดูรายละเอียดใน `schemas.json` / ตัวอย่างใน `examples.json`):

- `SceneAsset` / `SceneManifest`
- `ProjectState` (+ `Transform`, `LightSettings`)
- `ExportJob` / `ExportPresetConfig`
- `HistoryItem` / `LocalStore`
- `AnalyticsEvent`
- `FeatureChecklist`

---

## 17. Analytics / สำเร็จของแอปในช่อง

**Primary (ผลิตภัณฑ์):** % เซสชันที่ทำ `export_success` อย่างน้อย 1 ครั้ง  

**Primary (ช่อง):** save rate ของ Reel + จำนวนคอมเมนต์ขอฉาก  

**Secondary:**
- `cutout_success` rate / median `cutout_ms`
- จำนวนครั้ง `scene_select` ต่อเซสชัน (เป้า ≥ 3 ในเดโม)
- การใช้ custom scene vs library
- พรีเซ็ต export lag ยอดนิยม

**Guardrail:** อัตรา `cutout_fail`, ครีเอเตอร์ร้องขอบผมพังในคอมเมนต์

---

## 18. Reel shot list (25–35 วินาที)

| เวลา | ภาพ | ข้อความบนจอ | เสียงพูด |
|---|---|---|---|
| 0–3s | before/after สลับเร็ว 2 ครั้ง | ก่อน → หลัง | รูปโปรพื้นหลังรก แก้ได้ในคลิกเดียว |
| 3–8s | มอนทาจ gen/「สร้างด้วย AI วันนี้」 | สร้างด้วย AI วันนี้ | วันนี้ทำแอป SceneSwap Studio สดๆ |
| 8–14s | อัปโหลด → cutout progress → subject โปร่งใส | ถอดพื้นหลัง | อัปโหลดแล้วตัดพื้นหลังอัตโนมัติ |
| 14–22s | สลับฉาก 3–5 ใบ | สลับฉาก 1-2-3 | สลับฉากสตูดิโอ ดาดฟ้า คาเฟ่ ได้เลย |
| 22–28s | สไลเดอร์แสง + เปิด Export pack | แสง+เงา+ส่งออก | ปรับแสงเงา แล้วส่งออกทั้ง Reel และรูปโปร |
| 28–35s | ผลสุดท้าย + ลิงก์ | ลิงก์ในไบโอ | ลองฟรีที่ลิงก์ในไบโอ แล้วคอมเมนต์ว่าอยากได้ฉากไหน |

รายละเอียดช็อตเต็มใน `examples.json` → `reel_script_th`

---

## 19. ความเสี่ยง

| ความเสี่ยง | แผนลดความเสี่ยง |
|---|---|
| ขอบผมขาด / ใส่วัตถุบาง | มี refine (nice) + หลีกเล่ยเดโมผมฟูมากในคลิปแรก + ถ่ายรูปเดโมพื้นเรียบแสงหน้า |
| API ช้า/แพง | client fallback เป็นค่าเริ่ม + จำกัดความละเอียดตอนเดโม |
| ฉากมีลิขสิทธิ์ | ใช้ฉาก gen เอง / Unsplash ตามไลเซนส์ / ไฟล์ในโปรเจกต์เท่านั้น |
| คนเทียบแอปใหญ่ (remove.bg ฯลฯ) | โฟกัสความเร็ว + ชุด export สำหรับครีเอเตอร์ไทย + UI สวยสั้น |
| มือถือเครื่องอ่อนตัดช้า | โชว์ progress ชัด + รูปเดโมความละเอียดกลาง |
| ผู้ใช้เข้าใจว่าเป็นแอปตัดวิดีโอ | คัดก็อปปี้ชัดว่า「รูป」ใน Home และแคปชัน |

---

## 20. แผนส่งมอบวันเดียว (สำหรับคลิป)

| ช่วง | งาน |
|---|---|
| เช้า | Gen โครง Next.js + Home/Editor ตาม Master prompt |
| สาย | Cutout + Scene Library อย่างน้อย 20 ฉาก + สลับฉากลื่น |
| บ่าย | Light/Shadow + Export Pack + History เบาๆ |
| เย็น | QA 5 รูป + ถ่าย Reel ตาม shot list + อัป Vercel + ใส่ลิงก์ไบโอ |

---

## 21. Open questions

1. จะโชว์ watermark เล็กๆ 「SceneSwap」บน export ฟรีไหม หรือสะอาดทั้งก้อนเพราะเป็นแอปแจก?
2. รอบถัดไปใส่ AI prompt-to-scene ในแอปเลย หรือแยกเป็นคลิปวันอื่น?
3. เก็บ analytics แค่ console หรือต่อ Plausible/PostHog ตั้งแต่วันที่ 1?

---

## 22. Acceptance criteria (ผ่านก่อนลงคลิป)

- [ ] Cutout ใช้ได้กับรูปคนชัด ≥ 8/10 เคสทดสอบมาตรฐาน (ชายผมสั้น, หญิงผมยาว, คนใส่แว่น, สินค้ากล่อง, แสงย้อน)
- [ ] มีฉากในไลบรารี ≥ 20 และ manifest ผ่าน schema
- [ ] สลับฉากโดยไม่ต้องตัด subject ใหม่
- [ ] Custom scene อัปโหลดแล้วจัดตำแหน่งได้
- [ ] สไลเดอร์ Light & Shadow เห็นผลชัดในเดโม
- [ ] Export ได้อย่างน้อย PNG โปร่งใส + 9:16 + 1:1
- [ ] มี ≥ 5 ฟีเจอร์ must ตามตาราง และติ๊กใน `FeatureChecklist`
- [ ] มือถือ 390px ใช้งาน editor ได้ไม่เละ
- [ ] สคริปต์ Reel ถ่ายครบช็อต + CTA ชัด
- [ ] ไม่มีฉากใบหน้าคนจริง/โลโก้แบรนด์ไม่มีสิทธิ์ในคลิป

---

## 23. ภาคผนวก — สำเนาแพ็ก

แหล่งหลัก:

```text
/workspace/sceneswap-studio/
  README.md
  prd.md
  prompts.md
  schemas.json
  examples.json
```

Zip: `/workspace/sceneswap-studio.zip`  
ออปชันวันที่: `/workspace/ai-wanla-app/2026-09-28-sceneswap-studio/`
