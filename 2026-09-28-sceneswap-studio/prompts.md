# SceneSwap Studio — Prompt สั่งงาน (จัดเต็ม)

ใช้กับ AI codegen (Cursor / Claude / GPT) สำหรับสร้างแอปทั้งก้อน  
และใช้กับเครื่องมือภาพเมื่อสร้าง Scene Library assets

**วันที่แพ็ก:** 2026-09-28 (Asia/Bangkok) · Day 1/10 · AI วันละแอป  
**เอกสารคู่กัน:** `prd.md`, `schemas.json`, `examples.json`

---

## A) Master prompt สร้างทั้งแอป (วางครั้งเดียว)

```text
สร้างเว็บแอปมือถือเป็นหลักชื่อ SceneSwap Studio (ภาษาไทย UI ก่อน)

วันที่ส่งมอบคอนเทนต์: 2026-09-28 สำหรับช่อง "AI วันละแอป"
เป้าหมายผู้ใช้: อัปโหลดรูปคน/สินค้า → ถอดพื้นหลังอัตโนมัติ → ใส่ฉากใหม่จากไลบรารีหรืออัปโหลดเอง → ปรับแสงเงาให้เข้าฉาก → ส่งออกหลายขนาดพร้อมลงโซเชียล

สแต็กบังคับ:
- Next.js 14 App Router + TypeScript + Tailwind CSS + shadcn/ui
- Canvas compose ในเบราว์เซอร์ (lib/compose.ts)
- Background removal: @imgly/background-removal บน client เป็นค่าเริ่มต้น
  (รองรับสลับไป remove.bg / Replicate ผ่าน env ถ้าระบุ key แต่ไม่บังคับ)
- เก็บ favorites + history ใน localStorage (lib/storage.ts)
- Deploy พร้อมบน Vercel (PWA พื้นฐานมี manifest ก็พอ)

ต้องมีอย่างน้อย 5 ฟีเจอร์ must-have:
1) Smart Cutout — progress/skeleton สวย แสดงเวลาที่ใช้ได้
2) Scene Library — ≥20 ฉากใต้ /public/scenes แบ่งหมวด studio, city, nature, cafe, gradient, abstract พร้อม manifest.json ตาม schema SceneManifest
3) Custom Scene Upload — อัปโหลดฉากเอง + ลาก/พินช์ซูม/หมุน subject
4) Light & Shadow Match — สไลเดอร์ brightness, contrast, shadowStrength, shadowOffsetY
5) Export Pack — PNG transparent, JPG, presets: transparent_png, ig_square (1080x1080), story_9_16 (1080x1920), linkedin (800x800), shopee (1000x1000)

พิเศษถ้าเสร็จเร็ว (nice-to-have):
- Hair/Edge Refine แปรง erase/restore
- Batch สูงสุด 3 รูปด้วยฉากเดียวกัน
- Favorites + History 10 รายการ

หน้าจอ: Home, Editor, Scenes (sheet หรือหน้า), Export (sheet), History

UX บังคับ:
- มือถือแนวตั้งก่อน (390px เป็นฐาน)
- ปุ่มใหญ่ นิ้วกดง่าย โทนดำ–เทาเข้ม ไฮไลต์ม่วงนีออนอ่อน
- โหลด cutout มี skeleton/progress ภาษาไทย
- เทียบก่อน/หลังด้วยสไลเดอร์บนผลลัพธ์ได้
- ข้อความ UI ภาษาไทยตาม examples.json → ui_copy_th

คุณภาพโค้ด:
- แยก components, hooks, lib/compose.ts, lib/export.ts, lib/storage.ts, lib/cutout.ts
- มี TypeScript types ให้สอดคล้อง schemas.json
- README ภาษาไทย: วิธีรัน, วิธีเพิ่มฉาก, วิธีถ่าย Reel เดโม, ลิขสิทธิ์ฉาก
- อย่าทำระบบล็อกอินหรือจ่ายเงินใน MVP
- เริ่มจากให้รัน `npm run dev` ผ่าน และทำ happy path ให้จบก่อน แล้วค่อยเสริม refine/batch

อ้างอิงฟิลด์และตัวอย่างจาก schemas.json + examples.json ที่แนบมา
เมื่อจบให้สรุปว่าฟีเจอร์ must 5 ตัวอยู่ไฟล์ไหน และวิธีเพิ่มฉากใหม่ 1 ย่อหน้า
```

---

## B) Prompt สร้าง Scene Library assets

```text
สร้างชุดฉากสำหรับ SceneSwap Studio จำนวน 24 ไฟล์ (อย่างน้อย 20)

หมวดละ 4 ขึ้นไป ให้ครบ: studio, city, nature, cafe, gradient, abstract
สไตล์: ภาพถ่ายสมจริงหรือ 3D soft แสงสวย
ขนาดเป้าหมาย: แนวตั้ง 1080x1920 เป็นหลัก (ถ้ามีแนวนอน 1920x1080 เป็นโบนัส)
หลีกเลี่ยง: ใบหน้าคนจริง, โลโก้แบรนด์, ข้อความลายน้ำ, ข้อความอ่านได้รกๆ

ตั้งชื่อไฟล์: {category}-{nn}.jpg เช่น studio-01.jpg
สร้าง thumbnail ใต้ /scenes/thumbs/{id}.jpg
สร้างไฟล์ /public/scenes/manifest.json ตาม schema SceneManifest
ฟิลด์ title_th ต้องเป็นภาษาไทยธรรมชาติ เช่น "ดาดฟ้ากรุงเทพยามเย็น"
license ใช้ "generated" หรือ "unsplash" หรือ "owned" ให้ตรงความจริง

ส่งท้าย: ตารางรายการ id | title_th | category สำหรับแปะในรีโป
```

---

## C) System prompt สำหรับ Edge Refine Assistant (ออปชัน)

```text
คุณช่วยผู้ใช้ตัดขอบรูปใน SceneSwap Studio
พูดภาษาไทยสั้นๆ อบอุ่น ไม่เทคนิคเกิน

แนะนำทีละขั้น:
1) ซูมเข้าที่ขอบผมหรือขอบไหล่
2) ใช้แปรงลบ (erase) เก็บพิกเซลพื้นหลังที่เหลือ
3) ใช้แปรงเติม (restore) ถ้าเผลอลบผมหรือนิ้วไป
4) ลดขนาดแปรงเมื่อทำงานใกล้เส้นผม

ห้ามสัญญาผล 100%
ถ้าขอบพังมาก แนะนำให้ถ่ายใหม่: พื้นหลังเรียบ แสงด้านหน้า ไม่ย้อนแสงจัด
ถ้าผู้ใช้ทำสินค้า ให้เตือนไม่ให้เงาสะท้อนพื้นกระจกหายจนดูแบน
```

---

## D) Prompt ออกแบบหน้า Home + โทนแบรนด์

```text
ออกแบบ UI SceneSwap Studio โหมดมือถือ

โทน: พื้นดำ–เทาเข้ม (#0B0B10 โทน), ไฮไลต์ม่วงนีออนอ่อน, ปุ่ม primary ใหญ่มุมโค้ง
ฟอนต์: system / Inter
ความหนาแน่นต่ำ เน้นภาพเดโม ไม่โปสเตอร์รก

หน้า Home ต้องมี:
- โลโก้ข้อความ SceneSwap Studio
- หัวข้อ: เปลี่ยนฉากรูปโปร ในคลิกเดียว
- คำอธิบายสั้น 1 บรรทัด
- แถบก่อน/หลังเลื่อนได้ 3 ตัวอย่าง (ห้องรก→สตูดิโอ, ห้องรก→ดาดฟ้า, สินค้า→พื้นขาว)
- ปุ่มหลักใหญ่: เริ่มเลย
- แถวไอคอน 5 ฟีเจอร์: ตัดพื้นหลัง | ไลบรารีฉาก | ฉากของฉัน | แสงและเงา | ส่งออกชุด
- ฟุตเตอร์เล็ก: สร้างสำหรับช่อง AI วันละแอป

อย่าใส่ราคาหรือปุ่มสมัครสมาชิก
ส่งเป็นโครงสร้างคอมโพเนนต์ React + คลาส Tailwind
```

---

## E) Prompt compose engine

```text
เขียน lib/compose.ts สำหรับ SceneSwap Studio ให้เข้ากับ schema Transform + LightSettings

อินพุต:
- subjectImage: HTMLImageElement (พื้นหลังโปร่งแล้ว)
- sceneImage: HTMLImageElement | null
- canvasWidth: number
- canvasHeight: number
- transform: { x, y, scale, rotation }  // x,y offset จากกึ่งกลาง
- light: { brightness, contrast, shadowStrength, shadowOffsetY }

เอาต์พุต: HTMLCanvasElement

ขั้นตอนวาด:
1) เคลียร์ canvas
2) ถ้ามี scene: วาดแบบ cover เต็มเฟรม
3) วาด soft shadow ใต้ subject ตาม shadowStrength (ellipse + blur จำลองได้)
4) วาด subject ตาม translate → rotate → scale จากศูนย์กลาง + offset
5) ปรับ brightness/contrast เฉพาะ subject (ใช้ filter หรือ offscreen) ไม่ทำลายฉากเกินจำเป็น

ข้อกำหนดเพิ่ม:
- ฟังก์ชันบริสุทธิ์แยกคำนวณเมทริกซ์ transform ถ้าทำได้
- export ฟังก์ชัน drawPreview(...) และ drawForExport(...)
- คอมเมนต์สั้นภาษาอังกฤษในโค้ด พอให้ codegen ต่อได้
- ไม่พึ่งเซิร์ฟเวอร์
```

---

## F) Prompt Export Pack

```text
เขียน lib/export.ts ให้ตรง ExportPresetConfig / ExportJob ใน schemas.json

presets คงที่:
- transparent_png: เฉพาะ subject ไม่มีฉาก ขนาดต้นฉบับ (หรือ max 2048 ด้านยาว) format png
- ig_square: 1080x1080 jpg include_scene true
- story_9_16: 1080x1920 jpg include_scene true
- linkedin: 800x800 jpg include_scene true
- shopee: 1000x1000 jpg include_scene true

API ที่ต้องการ:
- listPresets(): ExportPresetConfig[]
- buildExportJob(presetId): ExportJob
- renderToBlob(projectState, presetId): Promise<Blob>
- downloadBlob(blob, filename)
- shareBlob(blob, filename) ใช้ navigator.share ถ้ารองรับ ไม่รองรับก็ fallback download

ตั้งชื่อไฟล์: sceneswap-{preset}-{YYYYMMDD-HHmmss}.png|jpg
คุณภาพ jpg เริ่ม 0.92
ข้อความ UI error เป็นภาษาไทย
```

---

## G) Prompt ถ่าย Reel / สคริปต์พูด

```text
เขียนสคริปต์ Reel 30 วินาทีภาษาไทย สำหรับแอป SceneSwap Studio
โทนเพื่อนพูด ไม่ขายของแข็ง ไม่พูดคำว่า disruption/ecosystem

โครงเวลา:
0-3s ฮุค before/after
3-8s บอกว่าสร้างด้วย AI วันนี้
8-14s โชว์ตัดพื้นหลัง
14-22s สลับฉาก 3 ใบ
22-28s แสงเงา + export หลายขนาด
28-35s CTA ลิงก์ในไบโอ + ให้คอมเมนต์「ฉาก」

ข้อกำหนด:
- ข้อความบนจอทีละช็อตสั้น ไม่เกิน 6 คำ
- มี voice line ต่อช็อต
- ระบุของใช้ถ่าย: มือถือจริง 1 เครื่อง, รูปเดโม 1 ใบ, ฉากไลบรารี 3 ใบ
- ส่งออกเป็น JSON ตามคีย์ reel_script_th ใน examples.json ได้ด้วย
```

---

## H) Prompt QA ก่อนลงคลิป

```text
เช็ก SceneSwap Studio ก่อนถ่าย Reel สำหรับคลิปวันที่ 2026-09-28

ทดสอบ 5 รูป:
1) ชายผมสั้น พื้นหลังบ้าน
2) หญิงผมยาว
3) คนใส่แว่น
4) สินค้ากล่องบนโต๊ะ
5) รูปแสงย้อน

เช็กรายการ:
- cutout ไม่กินมือ/ไหล่/หู
- สลับฉากไม่กระตุก ไม่ต้อง cutout ใหม่
- สไลเดอร์แสงและเงาเห็นผลชัดในวิดีโอ
- custom scene อัปโหลดได้
- export 9:16 และ 1:1 ดาวน์โหลดได้บน iPhone Safari
- หน้า History/Favorites ไม่พังถ้า localStorage ว่าง
- ไม่มีฉากลิขสิทธิ์น่าสงสัยหรือใบหน้าคนจริง
- UI ภาษาไทยไม่ตัดคำแปลกๆ

รายงานเป็นตาราง: เคส | ผล | severity (blocker/major/minor) | วิธีแก้สั้นๆ
สรุปท้ายว่าพร้อมถ่าย Reel หรือยัง พร้อมติ๊ก FeatureChecklist
```

---

## I) Prompt เพิ่มฟีเจอร์ Nice หลัง happy path

```text
ตอนนี้ SceneSwap Studio ทำ happy path ครบ 5 ฟีเจอร์ must แล้ว
ช่วยเพิ่มตามลำดับความคุ้มของคลิป:

1) Favorites + History (localStorage, สูงสุด 10 history, 50 favorites)
2) Edge Refine แปรงง่ายๆ บน mask
3) Batch 3 รูป — คิวประมวลผล cutout แล้วใส่ฉากเดียวกัน

กติกา:
- อย่าพัง API ของ compose/export เดิม
- มือถือใช้นิ้วได้
- อัปเดต FeatureChecklist ใน examples
- ไม่ต้องเพิ่ม auth
```

---

## J) Prompt ซ่อม JSON / validate ตอนรันจริง

```text
มี object ProjectState / SceneManifest จากแอป SceneSwap Studio
ตรวจกับ schemas.json (draft 2020-12)
ถ้าไม่ผ่าน: บอกฟิลด์ที่ผิด และคืนค่า object ที่ซ่อมแล้ว
ห้ามแต่งค่าที่ผู้ใช้ตั้งใจ (เช่น scene_id) นอกจากต้องใส่ default ที่ขาด
ตอบเป็นภาษาไทยสรุป + บล็อก JSON เต็ม
```

---

## K) Few-shot ข้อความ UI สั้นๆ

**ตอน cutout:** 「กำลังถอดพื้นหลัง…」  
**สำเร็จ:** 「ตัดพื้นหลังแล้ว — เลือกฉากได้เลย」  
**สลับฉาก:** 「เปลี่ยนฉากแล้ว」  
**ส่งออก:** 「บันทึกรูปแล้ว」  
**ผิดพลาด:** 「ตัดพื้นหลังไม่สำเร็จ ลองรูปที่แสงชัดกว่านี้」  

(ชุดเต็มอยู่ที่ `examples.json` → `ui_copy_th`)
