# BiteLog — Prompt สั่งงาน (จัดเต็ม)

ใช้กับ AI codegen (Cursor / Claude / GPT) สำหรับสร้างแอปทั้งก้อน  
และใช้สร้าง demo meal fixtures / mock vision results

**วันที่แพ็ก:** 2026-09-30 (Asia/Bangkok) · Day 3/10 · AI วันละแอป  
**เอกสารคู่กัน:** `prd.md`, `schemas.json`, `examples.json`

---

## A) Master prompt สร้างทั้งแอป (วางครั้งเดียว)

```text
สร้างเว็บแอปมือถือเป็นหลักชื่อ BiteLog (ภาษาไทย UI ก่อน)

วันที่ส่งมอบคอนเทนต์: 2026-09-30 สำหรับช่อง "AI วันละแอป"
เป้าหมายผู้ใช้: ถ่าย/อัปโหลดรูปมื้ออาหาร → AI/mock รู้ชื่อเมนูไทย + ประมาณ kcal/macros → ยืนยันปริมาณ → บันทึกลง Daily Log → ดูแดชบอร์ดแมโครรายวัน → เพิ่มมื้อโปรดเร็ว → แชร์การ์ดความคืบหน้าวัน/สตรีค

สแต็กบังคับ:
- Next.js 14 App Router + TypeScript + Tailwind CSS + shadcn/ui
- Food vision pluggable ใน lib/vision.ts: ค่าเริ่มต้น engine "mock_demo" โหลด fixture คุณภาพดี
  (รองรับสลับไป vision_api ผ่าน env ถ้าระบุ แต่ไม่บังคับ)
- Macro engine pure functions ใน lib/macros.ts + lib/portion.ts
- Share card + caption ใน lib/share.ts
- Thai food library ใน lib/food-library.ts หรือ /data/thai-food-library.json
- เก็บ daily logs / favorites / settings ใน localStorage (lib/storage.ts)
- Deploy พร้อมบน Vercel (PWA พื้นฐานมี manifest ก็พอ)
- ไม่มี auth และไม่มีเคลมทางการแพทย์ / ไม่มีโซเชียลฟีดใน MVP

ต้องมีอย่างน้อย 5 ฟีเจอร์ must-have:
1) Photo Bite Scan — อัปโหลด/ถ่ายรูปมื้อ + ปุ่ม「ใช้รูปเดโม」+ progress สวย + การ์ดผลเมนูไทย+kcal+macros
2) Thai Food Library — ค้นหาพรีเซ็ตเมนูไทยยอดฮิต + typical portions
3) Daily Macro Dashboard — วงแหวน/แถบ kcal·protein·carb·fat vs เป้า + ไทม์ไลน์มื้อวันนี้
4) Quick Add & Favorites — 1-tap จาก favorites/recent + ปุ่ม +/- portion
5) Share Progress Card — รูปการ์ดวัน/สตรีค + แคปชันคัดลอก IG/LINE + navigator.share

พิเศษถ้าเสร็จเร็ว (nice-to-have):
- Water tracker (แตะเพิ่มน้ำทีละ 250ml)
- Meal tags (เช้า/กลางวัน/เย็น/ของว่าง)
- Weekly chart (kcal 7 วัน)
- Streak & gentle reminders copy
- Offline localStorage history (~30 วัน)

หน้าจอ: Home, Scan/Upload, Scan Result Confirm, Library, Dashboard, Favorites/Quick Add, Share sheet, Weekly/Water (optional)

UX บังคับ:
- มือถือแนวตั้งก่อน (390px เป็นฐาน)
- ปุ่มใหญ่ นิ้วกดง่าย
- โทนพื้นครีม/off-white (#FFF7ED) + coral/salmon (#F97316) + เขียวสด (#22C55E) — อ่านตัวเลขแมโครชัดบน Reel
- พรีวิวรูปอาหารใหญ่ การ์ดผลสีสัน ตัวเลข kcal ตัวหนา
- ข้อความ UI ภาษาไทยตาม examples.json → ui_copy_th
- โทนอบอุ่น ไม่ guilt-shame มี disclaimer「ประมาณการ」

คุณภาพโค้ด:
- แยก components, hooks, lib/macros.ts, lib/portion.ts, lib/vision.ts, lib/share.ts, lib/storage.ts, lib/food-library.ts
- มี TypeScript types ให้สอดคล้อง schemas.json
- README ภาษาไทย: วิธีรัน, วิธีเพิ่มรูปเดโม, วิธีถ่าย Reel เดโม
- อย่าทำระบบล็อกอิน เคลมแพทย์ หรือโซเชียลฟีดใน MVP
- เริ่มจากให้รัน `npm run dev` ผ่าน และทำ happy path ให้จบก่อน แล้วค่อยเสริม water/weekly/streak

อ้างอิงฟิลด์และตัวอย่างจาก schemas.json + examples.json ที่แนบมา
เมื่อจบให้สรุปว่าฟีเจอร์ must 5 ตัวอยู่ไฟล์ไหน และวิธีโหลดรูปเดโม 1 ย่อหน้า
```

---

## B) Prompt สร้าง Demo meal photo fixtures / mock vision results

```text
สร้างชุดข้อมูลเดโมสำหรับ BiteLog

1) คำอธิบายหรือไฟล์ภาพมื้อสมมติ: จาน「ข้าวผัดกุ้ง + ไข่ดาว」มุมเหนือจาน แสงธรรมชาติ
2) ไฟล์ /public/fixtures/demo-meal.json ตาม schema ScanResult + FoodItem ที่ตรวจจับได้
3) ต้องมีอย่างน้อย:
   - detected_name_th: "ข้าวผัดกุ้งไข่ดาว" (หรือแยกเป็น 2 components ก็ได้ แต่มื้อรวมหนึ่ง MealEntry)
   - nutrients สมเหตุสมผลประมาณ: kcal 720, protein_g 32, carb_g 78, fat_g 28 ที่ portion multiplier 1.0
   - confidence ≥ 0.8 สำหรับ fixture เดโม
   - scan_ms ประมาณ 900–1500
   - alternatives 2–3 รายการ (เช่น ข้าวผัดกุ้งอย่างเดียว, ข้าวผัดไข่)
   - วันที่/เวลาเป็น Asia/Bangkok

สร้างเพิ่ม (ออปชัน) fixture ที่ 2: ส้มตำไทย + ไก่ย่าง หรือชาไทยเย็น สำหรับโชว์ Library/Quick Add

หลีกเลี่ยง: เคลมความแม่น 100%, ชื่อยา, คำดูถูกน้ำหนัก, โลโก้ร้านจริงที่อาจมีปัญหาลิขสิทธิ์ในคลิป

ตั้งชื่อผู้ใช้ตัวอย่างใน daily log: "มิ้นต์"
ส่งท้าย: ตารางเมนู | kcal | P/C/F | portion สำหรับแปะในรีโป
ให้ตัวเลขสุดท้ายตรงกับ meal_scan_example / daily_log_example ใน examples.json
```

---

## C) System prompt สำหรับ Food Vision Assistant (ออปชัน, ภาษาไทย)

```text
คุณช่วยผู้ใช้ประมาณมื้ออาหารใน BiteLog
พูดภาษาไทยสั้นๆ อบอุ่น ไม่เทคนิคเกิน ไม่ดุ ไม่ทำให้อับอาย

หน้าที่:
1) อ่านคำอธิบายรูปหรือผล mock แล้วแนะนำชื่อเมนูไทย + ประมาณ kcal/macros เป็น JSON ตาม schema ScanResult / MacroNutrients
2) ถ้ามั่นใจไม่ถึง ให้ใส่ confidence ต่ำและชวนเลือกจาก Thai Food Library
3) เสนอ alternatives 2–3 รายการเมื่อรูปคลุมเครือ
4) ใช้หน่วยจาน/ชาม/แก้วที่คนไทยคุ้น ไม่บังคับกรัมเสมอไป (กรัมเป็นออปชัน)
5) ห้ามวินิจฉัยโรค ห้ามสั่งงดอาหารแบบแพทย์ ห้ามพูด「คุณอ้วน/ผอมผิดปกติ」

ถ้าภาพมืด เบลอ หรือมีหลายจาน:
- บอกให้ถ่ายใหม่ให้เห็นจานชัด แสงพอ
- หรือให้เลือกเมนูจากไลบรารีทีละรายการ

ทุกคำตอบต้องย้ำว่าเป็น「ประมาณการเพื่อบันทึกส่วนตัว」
ห้ามสัญญาความแม่นระดับแล็บหรือนักโภชนาการ
```

---

## D) Prompt Macro / daily goal engine

```text
เขียน lib/portion.ts และ lib/macros.ts สำหรับ BiteLog ให้เข้ากับ schemas.json

lib/portion.ts:
- type Portion = { unit: "plate"|"bowl"|"cup"|"glass"|"piece"|"gram"|"ml"|"scoop"; amount: number; step?: number; label_th: string }
- applyMultiplier(base: MacroNutrients, multiplier: number): MacroNutrients
- clampMultiplier(m: number): number  // เช่น 0.25–3.0
- formatPortionTh(portion, multiplier): string  // เช่น "1 จาน", "1.5 ชาม"

lib/macros.ts:
อินพุต: MacroTargets, MealEntry[], (ออปชัน) WaterLog
เอาต์พุต: DailyLog summary { consumed, remaining, progress_pct, meals_count, ... }

ฟังก์ชันหลัก:
- sumNutrients(entries: MealEntry[]): MacroNutrients
- remaining(targets, consumed): MacroNutrients  // ติดลบได้
- progressPct(consumed, target): number  // 0–100+ แต่ UI แหวนแคป 100
- buildDailyLog(date, targets, entries, extras?): DailyLog
- scaleFoodItem(food: FoodItem, multiplier: number): MacroNutrients

ข้อกำหนด:
- ฟังก์ชันบริสุทธิ์ เทสได้
- ผลตัวอย่างต้องสอดคล้อง daily_log_example / meal_scan_example ใน examples.json
- kcal แสดงจำนวนเต็ม; macros กรัมทศนิยม 1 ตำแหน่งตอนคำนวณ
- คอมเมนต์สั้นภาษาอังกฤษในโค้ด
- ไม่พึ่งเซิร์ฟเวอร์
- ไม่มีสูตร BMR/TDEE บังคับใน MVP (เป้าวันตั้งเองหรือใช้ default)
```

---

## E) Prompt Share card + caption

```text
เขียน lib/share.ts + คอมโพเนนต์ ShareCard สำหรับ BiteLog

ต้องได้:
1) รูปการ์ดสรุปวันแนวตั้งสวย (แนะนำ 1080x1350 หรือ 1080x1920)
   - หัวข้อ BiteLog + วันที่ไทย
   - ตัวเลข kcal วันนี้ใหญ่ vs เป้า
   - chips โปรตีน/คาร์บ/ไขมัน
   - จำนวนมื้อ (+ streak ถ้ามี)
   - ฟุตเตอร์เล็ก BiteLog · AI วันละแอป
   - โทนครีม + coral + เขียว ไม่ใส่ BMI/น้ำหนักตัว/คำดูถูก
2) ข้อความแคปชันภาษาไทยสำหรับ IG/LINE ตามเทมเพลตใน examples.json → share_card_example
3) API:
   - buildSharePayload(dailyLog, options): SharePayload
   - renderShareCardPng(...): Promise<Blob>
   - copyCaption(text): Promise<void>
   - shareNative(payload): Promise<void>  // navigator.share fallback download/copy
4) ชื่อไฟล์: bitelog-{date}-{HHmmss}.png

โทนการ์ด: warm food vibe อ่านชัดบนมือถือและ Reel
ข้อความ error UI เป็นภาษาไทย
อย่าใส่คำว่า「เผาผลาญ」「ลงโทษ」「โกงไดเอท」บนการ์ด
```

---

## F) Prompt UI polish / โทนแบรนด์

```text
ออกแบบ UI BiteLog โหมดมือถือ

โทน: พื้นครีม/off-white (#FFF7ED / #FFFBEB), การ์ดขาว, ไฮไลต์ coral/salmon (#F97316 / #FB923C),
เขียวสด healthy (#22C55E), ตัวเลขแมโครตัวหนาสีหินเข้ม (#1C1917), ข้อความรองสีหิน (#78716C)
ฟอนต์: system / Inter / Noto Sans Thai
ความหนาแน่นต่ำ เน้นพรีวิวรูปอาหารใหญ่ + ตัวเลข kcal ชัด ไม่โปสเตอร์รก ไม่ดาร์คโหมดบังคับ

หน้า Home ต้องมี:
- โลโก้ข้อความ BiteLog
- หัวข้อ: ถ่ายอาหาร → รู้แคลอรี่และมื้อไทย ใน 10 วินาที
- คำอธิบายสั้น 1 บรรทัด
- แถบเดโมเลื่อนได้: รูปจาน → การ์ดโภชนาการ → แดชบอร์ด rings
- ปุ่มหลักใหญ่: ถ่ายมื้อนี้
- ปุ่มรอง: ใช้รูปเดโม
- แถวไอคอน 5 ฟีเจอร์: สแกนรูป | ไลบรารีไทย | แดชบอร์ด | เพิ่มเร็ว | แชร์การ์ด
- ฟุตเตอร์เล็ก: สร้างสำหรับช่อง AI วันละแอป + disclaimer สั้น

หน้า Dashboard:
- วงแหวน kcal ใหญ่กลาง
- แถบ P/C/F ใต้แหวน
- ไทม์ไลน์มื้อวันนี้แบบการ์ดเล็กมีรูป/อีโมจิ
- FAB หรือปุ่ม「+ มื้อ」

อย่าใส่ราคาคอร์ส ปุ่มสมัครสมาชิก ปุ่ม「ปรึกษาหมอ」หรือเกจความอ้วน
ส่งเป็นโครงสร้างคอมโพเนนต์ React + คลาส Tailwind
ใช้ข้อความจาก examples.json → ui_copy_th
```

---

## G) Prompt ถ่าย Reel / สคริปต์พูด (shot-list)

```text
เขียนสคริปต์ Reel 30 วินาทีภาษาไทย สำหรับแอป BiteLog
โทนเพื่อนพูด ไม่ขายของแข็ง ไม่พูดคำว่า disruption/ecosystem
ไม่ขู่เรื่องน้ำหนัก ไม่เคลมหมอ

โครงเวลา:
0-3s ฮุค รูปจาน → การ์ดโภชนาการขึ้น
3-8s บอกว่าสร้างด้วย AI วันนี้
8-14s โชว์ Photo Bite Scan (ข้าวผัดกุ้งไข่ดาว)
14-22s ยืนยัน portion → Dashboard rings อัปเดต
22-28s Library/Favorites เร็วๆ + Share Progress Card
28-35s CTA ลิงก์ในไบโอ + ให้คอมเมนต์「แคล」

ข้อกำหนด:
- ข้อความบนจอทีละช็อตสั้น ไม่เกิน 8 คำ
- มี voice line ต่อช็อต
- ระบุของใช้ถ่าย: มือถือจริง 1 เครื่อง, รูปมื้อเดโม 1 จาน, แดชบอร์ดมี ≥2 มื้อ
- โชว์อย่างน้อย 3 ฟีเจอร์ในคลิปเดียว
- ส่งออกเป็น JSON ตามคีย์ reel_script_th ใน examples.json ได้ด้วย
```

---

## H) Prompt QA ก่อนลงคลิป

```text
เช็ก BiteLog ก่อนถ่าย Reel สำหรับคลิปวันที่ 2026-09-30

ทดสอบเคส:
1) โหลดรูปเดโม — ได้ชื่อเมนูไทย + kcal/macros ตาม examples
2) ปรับ portion +/- แล้วตัวเลขอัปเดตก่อนบันทึก
3) บันทึกมื้อ → Dashboard rings/bars + ไทม์ไลน์อัปเดต
4) ค้นหา Library อย่างน้อย "ข้าวผัด", "ส้มตำ", "ชาไทย" แล้วเพิ่มมื้อได้
5) Quick Add จาก Favorites/Recent
6) แชร์รูปการ์ด + คัดลอกแคปชันบนมือถือ
7) (ถ้ามี) อัปโหลดรูปอาหารจริงภาพชัด / ภาพมืด — ต้องไม่แครช อย่างน้อยให้เลือกจาก Library ได้

เช็กรายการ:
- ไม่มี NaN / undefined บน UI
- ปุ่มใหญ่ใช้นิ้วได้ที่ 390px
- UI ภาษาไทยไม่ตัดคำแปลกๆ
- มี disclaimer ประมาณการ มองเห็นได้
- ไม่มีข้อความ guilt-shame / เคลมแพทย์
- Favorites/History ไม่พังถ้า localStorage ว่าง
- สีหลักครีม+coral+เขียว ตามแบรนด์

รายงานเป็นตาราง: เคส | ผล | severity (blocker/major/minor) | วิธีแก้สั้นๆ
สรุปท้ายว่าพร้อมถ่าย Reel หรือยัง พร้อมติ๊ก FeatureChecklist
```

---

## I) Prompt เพิ่ม Water / Weekly / Streak (nice)

```text
ตอนนี้ BiteLog ทำ happy path ครบ 5 ฟีเจอร์ must แล้ว
ช่วยเพิ่มตามลำดับความคุ้มของคลิป:

1) Meal tags — เช้า/กลางวัน/เย็น/ของว่าง บนฟอร์มยืนยันมื้อ
2) Water tracker — ปุ่ม +250ml บน Dashboard สูงสุดประมาณ 3000ml/วัน
3) Streak — นับวันติดต่อกันที่มี ≥1 มื้อ + สำเนาอ่อนโยน
4) Weekly chart — แท่ง kcal 7 วันจาก LocalStore
5) Offline history — เก็บ DailyLog ย้อนหลังสูงสุด ~30 วัน

กติกา:
- อย่าพัง API ของ macros/share/vision เดิม
- มือถือใช้นิ้วได้
- อัปเดต FeatureChecklist ใน examples
- ไม่ต้องเพิ่ม auth หรือเคลมแพทย์
- อย่าใช้สีแดงดุเมื่อเกินเป้าน้ำ/แคล — ใช้ coral อ่อนหรือข้อความกลางๆ
```

---

## J) Prompt ซ่อม JSON / validate ตอนรันจริง

```text
มี object ScanResult / MealEntry / DailyLog / SharePayload จากแอป BiteLog
ตรวจกับ schemas.json (draft 2020-12)
ถ้าไม่ผ่าน: บอกฟิลด์ที่ผิด และคืนค่า object ที่ซ่อมแล้ว
ห้ามแต่งตัวเลขโภชนาการที่ผู้ใช้ตั้งใจ นอกจากต้องใส่ default ที่ขาด
ตอบเป็นภาษาไทยสรุป + บล็อก JSON เต็ม
```

---

## K) Few-shot ข้อความ UI สั้นๆ

**ตอนสแกน:** 「กำลังดูมื้อนี้…」  
**สำเร็จ:** 「ได้ประมาณการแล้ว — ปรับปริมาณได้」  
**บันทึกแล้ว:** 「บันทึกมื้อแล้ว แดชบอร์ดอัปเดตแล้ว」  
**จากไลบรารี:** 「เพิ่มจากไลบรารีแล้ว」  
**แชร์:** 「คัดลอกแคปชันแล้ว」  
**ผิดพลาด:** 「อ่านรูปไม่สำเร็จ ลองถ่ายใหม่หรือค้นจากไลบรารี」  
**เกินเป้า (อ่อนโยน):** 「วันนี้เกินเป้าเล็กน้อย — ไม่เป็นไร พรุ่งนี้เริ่มใหม่ได้」  

(ชุดเต็มอยู่ที่ `examples.json` → `ui_copy_th`)


---

## L) Prompt สร้าง Thai Food Library data file

```text
สร้างไฟล์ data/thai-food-library.json สำหรับ BiteLog ตาม schema FoodItem[]

ต้องมีอย่างน้อย 10 เมนูไทยที่คนทั่วไปกินบ่อย:
1) ก๋วยเตี๋ยวเรือหมู
2) ข้าวผัดกุ้ง
3) ข้าวผัดกุ้งไข่ดาว (คอมโบเดโม)
4) ส้มตำไทย
5) ไก่ย่าง
6) ผัดไทยกุ้ง
7) ต้มยำกุ้งน้ำข้น
8) ข้าวมันไก่
9) ชาไทยเย็น
10) ข้าวเหนียวมะม่วง
11) ไข่เจียวหมูสับ (ออปชัน)
12) กาแฟเย็น (ออปชัน)

แต่ละรายการต้องมี:
- id, name_th, name_en, category (noodle|rice|salad|grill|soup|dessert|drink|other)
- tags[] ภาษาไทย เช่น ["กลางวัน","จานเดียว"]
- typical_portion { unit, amount, label_th, step }
- nutrients ต่อ typical portion (kcal, protein_g, carb_g, fat_g) สมเหตุสมผลแบบประมาณการร้านทั่วไป ไม่ใช่แล็บ
- emoji สำหรับ UI
- search_aliases[] เช่น ["ก๋วยเตี๋ยว","เรือ"] 

ข้อกำหนด:
- ตัวเลขเป็นประมาณการร้านอาหารทั่วไปในไทย ไม่คัดลอกฐานข้อมูลปิด
- เรียงหมวดหมู่ให้อ่านง่าย
- ใช้ใน Library search (match ชื่อ + aliases + tags)
- ส่งออก JSON ถูกต้อง UTF-8
```

---

## M) Prompt ออกแบบ Scan Result Confirm + portion stepper

```text
สร้างหน้า/คอมโพเนนต์ ScanResultConfirm สำหรับ BiteLog

องค์ประกอบ:
1) พรีวิวรูปมื้อมุมบนมน ใหญ่ พอโชว์บน Reel
2) ชื่อเมนูไทยตัวใหญ่ แก้ได้ (input)
3) แถว alternatives เลื่อนแนวนอนถ้ามี
4) การ์ดตัวเลข: kcal ใหญ่กลาง + chips P/C/F
5) Portion stepper: ปุ่ม − / + และป้าย label_th (เช่น 1 จาน → 1.25 จาน)
6) (nice) Meal tag chips: เช้า กลางวัน เย็น ของว่าง
7) ปุ่มหลัก「บันทึกมื้อนี้」+ ปุ่มรอง「เลือกจากไลบรารีแทน」
8) ข้อความย่อย disclaimer ประมาณการ

พฤติกรรม:
- ทุกครั้งที่เปลี่ยน multiplier ให้ scale nutrients จาก base แล้ว animate ตัวเลขสั้นๆ
- confidence < 0.55 แสดงแบนเนอร์เหลืองอ่อน「ไม่แน่ใจ — ช่วยเลือกเมนูให้ตรงขึ้นได้」
- ห้ามใช้สีแดงดุหรือไอคอนเตือนแรงเกี่ยวกับแคลอรี่

ส่งเป็น React + Tailwind สอดคล้อง ui_copy_th
```

---

## N) Prompt Daily Macro Dashboard rings

```text
สร้างคอมโพเนนต์ MacroDashboard สำหรับ BiteLog

ต้องมี:
1) Header วันที่ไทย (เช่น พุธ 30 ก.ย. 2026) + ปุ่มแชร์
2) วงแหวน kcal ใหญ่ (SVG หรือ CSS conic) แสดง consumed/target
3) ใต้แหวน: ข้อความ「เหลืออีก X kcal」หรือ「เกิน X kcal」โทนกลาง ไม่ดุ
4) สามแถบ progress: โปรตีน / คาร์บ / ไขมัน พร้อมตัวเลข g
5) ไทม์ไลน์มื้อ: รายการ MealEntry วันนี้ เรียงเวลา มีอีโมจิ/รูปเล็ก ชื่อ แคล ปุ่มลบ
6) แถวทางลัด: Quick Add · Library · ถ่ายมื้อ
7) (nice) แถบน้ำ Water: ไอคอนแก้ว + ปุ่ม +250ml

ข้อมูลจาก buildDailyLog() ใน lib/macros.ts
ว่างเปล่า: empty state น่ารัก「ยังไม่มีมื้อวันนี้ — ถ่ายจานแรกเลย」
อย่าใส่กราฟ BMI หรือสเกลน้ำหนัก
