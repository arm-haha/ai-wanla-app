# PRD: BiteLog

**Product name:** BiteLog  
**Tagline (TH):** ถ่ายอาหาร → รู้แคลอรี่และมื้อไทย ใน 10 วินาที  
**Tagline (EN):** Snap a Thai meal, get calories & macros — log in one tap  
**Version:** 1.0 (MVP — AI-วันละแอป Day 3/10)  
**Channel date:** 2026-09-30 (Asia/Bangkok)  
**Platform:** Web app (mobile-first) + PWA  
**Language:** Thai UI first, English secondary  
**Status:** Delivery-ready for official morning run  
**Related docs:** `README.md`, `prompts.md`, `schemas.json`, `examples.json`  
**Last updated:** 2026-09-30 (Asia/Bangkok)

---

## 1. สรุปสั้นๆ

แอปมินิสวีทให้คนไทยทั่วไปถ่ายหรืออัปโหลดรูปมื้ออาหาร → AI/mock รู้ชื่อเมนูไทย + ประมาณแคลอรี่และแมโคร (โปรตีน คาร์บ ไขมัน) → ยืนยันปริมาณเสิร์ฟ → บันทึกลง Daily Log → ดูแดชบอร์ดวงแหวนเทียบเป้าวัน → เพิ่มมื้อโปรดด้วย 1 แตะ → แชร์การ์ดความคืบหน้าวัน/สตรีคสวยๆ ไป IG หรือ LINE

ออกแบบให้เดโมใน Reel 15–30 วินาทีเห็นรูปจาน→การ์ดโภชนาการชัด และมีฟีเจอร์รองที่ดึงคนกลับมาเปิดซ้ำ (favorites, water tracker, weekly chart, streak reminders)

MVP ไม่มีบัญชีผู้ใช้ ไม่เคลมความแม่นระดับแพทย์/นักโภชนาการ ไม่มีโซเชียลฟีด ไม่มี coaching แบบเสียเงิน

---

## 2. ปัญหาที่แก้

| ปัญหาวันนี้ | ผลกระทบ |
|---|---|
| อยากรู้แคลอรี่แต่พิมพ์ชื่อเมนูไทยในแอปต่างประเทศไม่เจอ | ล้มเลิกบันทึกหลัง 2–3 มื้อ |
| แอปแคลใหญ่ UI หนัก รู้สึกถูกตัดสิน (guilt UX) | คนปิดแอป ไม่กลับมาเปิด |
| ถ่ายรูปแล้วได้แต่ชื่ออังกฤษ / ตัวเลขมั่ว | ไม่เชื่อผล ไม่แชร์ต่อ |
| บันทึกช้าหลายขั้นตอนหลังกินเสร็จ | ลืมใส่ ข้อมูลวันว่าง |
| เครื่องมือ B2B nutrition / clinic SaaS | ไม่เหมาะเดโม Reel 15–30 วินาที และคนทั่วไปไม่ใช้ |

**โอกาสช่อง AI วันละแอป:** แจกแอปฟรีที่ผลลัพธ์เห็นทันทีหลังถ่ายจาน → save rate สูง → คนเข้าลิงก์ลองตอนกินข้าวจริง → ติดตามเพื่อรอแอปวันถัดไป

---

## 3. เป้าหมายผลิตภัณฑ์

### 3.1 Goals (MVP / วันเดียว + คลิปเช้า)

1. Happy path จบบนมือถือ: อัปโหลด/ถ่ายรูปมื้อ (หรือโหลด fixture) → scan result → ยืนยัน portion → บันทึก → แดชบอร์ดอัปเดต → แชร์การ์ด ภายใน **≤ 60 วินาที** สำหรับผู้ใช้ทั่วไป
2. มี **≥ 5 ฟีเจอร์ must-have** ที่ใช้ได้จริงและโชว์ในคลิปได้อย่างน้อย 3 ตัว
3. Demo meal fixture คุณภาพดีอย่างน้อย **1 จาน** (เช่น ข้าวผัดกุ้ง + ไข่ดาว) พร้อม mock vision result สมเหตุสมผล
4. ตัวเลขแมโครใน fixture สอดคล้องกับตัวอย่างใน `examples.json` (ประมาณการ — ไม่ต้องแม่นระดับแล็บ)
5. คลิป Reel 25–35 วินาทีถ่ายจบด้วย UI จริง ไม่ใช่ mock อย่างเดียว

### 3.2 Non-goals (MVP)

- ไม่มีระบบล็อกอิน / คลาวด์ซิงก์มื้ออาหาร
- ไม่เคลมวินิจฉัยโรค / แนะนำยา / แผนลดน้ำหนักทางการแพทย์
- ไม่โฟกัสบาร์โค้ดยา / ซูเปอร์มาร์เก็ตเป็นหลัก (โฟกัสมื้อไทยในชีวิตประจำวัน)
- ไม่มี native iOS/Android store build
- ไม่มีโซเชียลฟีด / ติดตามเพื่อน / leaderboard แบบแข่งขันลดน้ำหนัก
- ไม่บังคับ Vision API จริง — `mock_demo` คุณภาพดีพอสำหรับเดโมและคลิป
- ไม่มี paid coaching / แชทนักโภชนาการ

---

## 4. ผู้ใช้และบทบาท

| บทบาท | ความต้องการหลัก |
|---|---|
| **คนไทยกินนอกบ้าน / สั่งเดลิเวอรี (หลัก)** | ถ่ายจานรู้แคลคร่าวๆ บันทึกเร็ว ไม่รู้สึกถูกดุ |
| **คนเริ่มนับแมโครแบบสบายๆ** | เห็นเป้าวัน + มื้อไทม์ไลน์ ไม่ต้องกรอกละเอียดทุกกรัม |
| **ผู้ชมช่อง AI วันละแอป** | เห็น wow รูปจาน→การ์ดโภชนาการ ใน 3 วินาที อยากลองลิงก์ในไบโอ |
| **ผู้สร้างคลิป (เรา)** | gen แอปใน 1 วัน มีสคริปต์ช็อตและเช็คลิสต์พร้อมถ่าย |

---

## 5. User stories

1. ในฐานะผู้ใช้ ฉันถ่ายหรืออัปโหลดรูปมื้อแล้วได้ชื่อเมนูไทย + ประมาณ kcal/macros ภายในไม่กี่วินาที
2. ในฐานะผู้ใช้ ฉันปรับปริมาณเสิร์ฟ (+/- หรือเลือกขนาด) ก่อนกดบันทึกได้
3. ในฐานะผู้ใช้ ฉันค้นหาเมนูไทยจากไลบรารีแล้วเพิ่มมื้อโดยไม่ต้องถ่ายรูปได้
4. ในฐานะผู้ใช้ ฉันเห็นวงแหวน/แถบ kcal โปรตีน คาร์บ ไขมันเทียบเป้าวัน และไทม์ไลน์มื้อวันนี้
5. ในฐานะผู้ใช้ ฉันแตะมื้อโปรดหรือมื้อล่าสุดเพื่อเพิ่มซ้ำเร็ว พร้อมปรับปริมาณ
6. ในฐานะผู้ใช้ ฉันแชร์การ์ดความคืบหน้าวัน/สตรีคเป็นรูป + คัดลอกแคปชัน IG/LINE ได้
7. ในฐานะผู้ชม Reel ฉันเห็นรูปจาน→การ์ดโภชนาการใน 3 วินาทีแรกแล้วอยากลองแอป
8. ในฐานะระบบ ทุกมื้อต้องเก็บตาม `MealEntry` และ DailyLog ตาม `LocalStore`

---

## 6. ฮุค Reel (3 วินาทีแรก)

**Before:** รูปจานข้าวผัดมุมเอียง/เบลอเล็กน้อย + คนสงสัย「กี่แคลวะ」  
**After:** การ์ดโภชนาการสีสด — ชื่อเมนูไทย + kcal ใหญ่ + แมโคร 3 แถบ  
**ข้อความบนจอ:** `ถ่ายอาหาร → รู้แคลอรี่และมื้อไทย ใน 10 วินาที`  
**เสียง:** 「ถ่ายจานเดียว รู้แคลกับแมโครทันที」

**Wow moment กลางคลิป:** รูปอาหารธรรมดา → การ์ดสีสัน + ชื่อไทยชัด → แดชบอร์ดวงแหวนกระโดดขึ้น → กดแชร์การ์ดวัน

---

## 7. ทำไมคนติดตาม / เปิดซ้ำ

- ผลรูปจาน→แคลทันที (เหมาะ Reel + save)
- ใช้จริงได้ทุกมื้อเช้า/กลางวัน/เย็น/ของว่าง
- แจกฟรีจากช่อง → เซฟคลิป + เข้าลิงก์
- รีเทนชัน: Favorites, Daily Dashboard, Streak, Water tracker, Weekly chart
- คอมเมนต์「แคล」= สัญญาณทำคลิปต่อ / ขอฟีเจอร์เพิ่ม

---

## 8. กฎผลิตภัณฑ์ช่อง

- **ขั้นต่ำ 5 ฟีเจอร์** must-have (ตารางด้านล่าง)
- Gen ได้ใน 1 วันด้วย AI codegen (Next.js + vision pluggable)
- เดโมหลักจบในมือถือแนวตั้ง (~390px)
- UI สวย พอเป็นพรีวิว “แอปจริง” ไม่ใช่ฟอร์มดิบ
- ภาษาไทยก่อน — คีย์สคีมาภาษาอังกฤษได้
- โทนอบอุ่น ไม่ guilt-shame — ใช้คำว่า「ประมาณการ」ชัดเจน

---

## 9. ฟีเจอร์

### 9.1 Must-have (≥ 5)

| # | ฟีเจอร์ | รายละเอียด | Acceptance ย่อ |
|---|---|---|---|
| 1 | **Photo Bite Scan** | ถ่าย/อัปโหลดรูปมื้อ → ได้ชื่อเมนูไทย + ประมาณ kcal/macros; default engine `mock_demo` + ช่องเสียบ vision API | fixture เดโมขึ้นผลใน ≤2s |
| 2 | **Thai Food Library** | ค้นหาพรีเซ็ตเมนูไทยยอดฮิต พร้อม portion มาตรฐาน (จาน/ชาม/แก้ว) | ค้นหาเจอ ≥8 เมนูตัวอย่าง + เพิ่มมื้อได้ |
| 3 | **Daily Macro Dashboard** | วงแหวน/แถบ kcal, protein, carb, fat vs daily goal + ไทม์ไลน์มื้อวันนี้ | หลังบันทึกมื้อ rings อัปเดตทันที |
| 4 | **Quick Add & Favorites** | 1-tap จาก favorites/recent + ปุ่ม +/- portion | เพิ่มมื้อโปรดจบใน ≤3 แตะ |
| 5 | **Share Progress Card** | รูปการ์ดวัน/สตรีคสวย + แคปชันคัดลอก IG/LINE + share sheet | ได้รูป+ข้อความบน iPhone Safari |

### 9.2 Nice-to-have

| # | ฟีเจอร์ | รายละเอียด |
|---|---|---|
| 6 | **Water tracker** | แตะเพิ่มน้ำทีละแก้ว (250ml) ในวันเดียวกัน |
| 7 | **Meal tags** | แท็กเช้า / กลางวัน / เย็น / ของว่าง บน MealEntry |
| 8 | **Weekly chart** | กราฟแท่งหรือเส้น kcal 7 วันล่าสุดจาก localStorage |
| 9 | **Streak & gentle reminders** | นับวันติดต่อกันที่มีมื้อ ≥1 + สำเนาเตือนอ่อนโยน (ไม่ดุ) |
| 10 | **Offline localStorage history** | ประวัติมื้อ/วันสูงสุด ~30 วัน ใช้งานออฟไลน์ได้หลังโหลดครั้งแรก |

---

## 10. ขอบเขตฟีเจอร์

### 10.1 In scope

- Home, Scan/Upload, Scan Result Confirm, Library, Dashboard, Favorites/Quick Add, Share sheet
- Food vision pluggable: `mock_demo` (default) · optional `vision_api` ผ่าน env
- Macro engine ใน `lib/macros.ts` (pure functions)
- Share card render บน Canvas / DOM-to-image
- Analytics events ฝั่ง client (optional log)
- PWA ติดตั้งได้แบบพื้นฐาน (manifest + icons)
- Disclaimer UI: 「ตัวเลขเป็นประมาณการ ไม่ใช่คำแนะนำทางการแพทย์」

### 10.2 Out of scope (เฟสถัดไป)

- Auth / cloud sync มื้ออาหาร
- วินิจฉัยโรค / meal plan แพทย์ / ยา
- บาร์โค้ดเภสัช / ฐานข้อมูลอาหารโลกทั้งก้อน
- โซเชียลฟีด / follow เพื่อน / ranking ลดน้ำหนัก
- Paid coaching / แชทนักโภชนาการ
- ฝึกโมเดล vision เอง

---

## 11. User flow หลัก (Happy path)

```text
เปิดแอป → ถ่ายหรืออัปโหลดรูปมื้อ (หรือกด「ใช้รูปเดโม」)
  → Vision / mock parse (progress สวย เป้า ≤ 2s สำหรับ fixture)
  → ดูผล: ชื่อเมนูไทย + kcal + macros + confidence
  → ปรับ portion (+/- หรือเลือกขนาด) แล้วกดยืนยันบันทึก
  → Daily Macro Dashboard อัปเดต rings/bars + ไทม์ไลน์มื้อ
  → (ทางเลือก) บันทึกเป็น Favorite
  → แชร์การ์ดวัน / คัดลอกแคปชัน / เปิด share sheet
  → กลับมาเพิ่มมื้อถัดไปด้วย Quick Add หรือ Library
```

### สถานะเซสชันสแกน

`idle` → `scanning` → `confirming` → `logged` → `sharing`  
ทางแยก: `error` (พร้อมข้อความไทยสั้นๆ + ปุ่มลองใหม่ / ค้นหาจากไลบรารี)

---

## 12. หน้าจอ (MVP)

| # | หน้าจอ | องค์ประกอบหลัก |
|---|---|---|
| 1 | **Home** | โลโก้, หัวข้อไทย, แถบเดโมรูปจาน→การ์ดโภชนาการ, CTA「ถ่ายมื้อนี้」, แถบ 5 ฟีเจอร์ไอคอน, ปุ่มรอง「ใช้รูปเดโม」, ลิงก์ไปแดชบอร์ดวันนี้ |
| 2 | **Scan / Upload** | ช่องกล้อง/ไฟล์, ปุ่มรูปเดโม, progress vision, พรีวิวรูปใหญ่ |
| 3 | **Scan Result Confirm** | การ์ดผลใหญ่ (ชื่อไทย + kcal ตัวหนา + macro chips), ปรับ portion, แท็กมื้อ (nice), ปุ่ม「บันทึกมื้อ」 |
| 4 | **Thai Food Library** | ช่องค้นหา, รายการเมนูไทยจัดกลุ่ม, แตะแล้วไปหน้าปรับ portion |
| 5 | **Daily Macro Dashboard** | วงแหวน kcal + แถบ P/C/F vs เป้า, ไทม์ไลน์มื้อวันนี้, ทางลัด Quick Add |
| 6 | **Favorites / Quick Add** | รายการโปรด + มื้อล่าสุด, ปุ่ม +/- , 1-tap เพิ่ม |
| 7 | **Share sheet** | พรีวิวการ์ดวัน/สตรีค, คัดลอกแคปชัน, แชร์ระบบ |
| 8 | **Weekly / Water** (nice) | กราฟ 7 วัน, ตัวนับแก้วน้ำ |

**โทนแบรนด์:** พื้นครีม/off-white (#FFF7ED / #FFFBEB), ไฮไลต์ coral/salmon (#F97316 / #FB923C), เขียวสดสำหรับ healthy (#22C55E / #16A34A), ตัวเลขแมโครตัวหนาชัด, พรีวิวรูปอาหารใหญ่, ปุ่ม primary ใหญ่ — โทน “warm food vibe” ที่ถ่าย Reel แล้วอ่านง่าย ไม่ดาร์ก ไม่ guilt

---

## 13. ความต้องการเชิงฟังก์ชัน

### FR-1 Photo Bite Scan
- รับไฟล์ภาพจากไฟล์หรือกล้อง
- รัน engine ตาม `vision_engine` (ค่าเริ่ม `mock_demo`)
- มีปุ่ม「ใช้รูปเดโม」โหลด fixture จาก `/fixtures/demo-meal.json` (+ ภาพใน `/public/fixtures/`)
- เก็บ `scan_ms`, confidence, detected dishes ใน `ScanResult`
- ถ้าสแกนล้มเหลว: ให้ค้นจาก Thai Food Library หรือพิมพ์ชื่อมือได้
- แสดง disclaimer ประมาณการใกล้ผลลัพธ์

### FR-2 Thai Food Library
- รายการ `FoodItem` พรีเซ็ต ≥ 8–12 เมนูไทยใน MVP (ขยายทีหลังได้)
- ค้นหาด้วยชื่อไทย / ชื่อเล่น / แท็ก (เช่น ก๋วยเตี๋ยว, ของว่าง, เครื่องดื่ม)
- แต่ละรายการมี typical portions และ macros ต่อหน่วย
- แตะแล้วเข้า flow ปรับ portion → บันทึกเหมือนหลังสแกน

### FR-3 Daily Macro Dashboard
- เป้าวัน `MacroTargets` (kcal, protein_g, carb_g, fat_g) แก้ได้ใน settings เบาๆ
- แสดง consumed vs target เป็นวงแหวน (kcal) + แถบ (P/C/F)
- ไทม์ไลน์ `MealEntry[]` ของวันนี้ เรียงเวลา
- หลังบันทึก/ลบมื้อ ต้อง recalculate < 100ms

### FR-4 Quick Add & Favorites
- `Favorite` อ้าง FoodItem หรือ snapshot มื้อพร้อม portion ล่าสุด
- Recent meals จากประวัติสั้นๆ (เช่น 10 รายการล่าสุด)
- ปุ่ม +/- ปรับ multiplier / grams / scoops ตามชนิด portion
- 1-tap เพิ่มเข้า DailyLog วันนี้

### FR-5 Share Progress Card
- เรนเดอร์การ์ดสรุปวันเป็น PNG (Canvas หรือ html-to-image)
- แสดง: วันที่, kcal วันนี้ vs เป้า, macro chips, จำนวนมื้อ, streak (ถ้ามี), โทนครีม+coral+เขียว
- สร้างแคปชันไทยสำหรับ IG/LINE ตามเทมเพลต
- `navigator.share` ถ้ามี + fallback คัดลอก/ดาวน์โหลด
- ห้ามใส่ตัวเลขน้ำหนักตัว / BMI / คำดูถูกบนการ์ด

### FR-6 Local retention (nice path)
- บันทึก daily logs + favorites + settings ตาม `LocalStore`
- ไม่บังคับ auth; ใช้ได้หลังโหลดครั้งแรกแบบออฟไลน์ (cache หน้า)

### FR-7 Analytics (เบา)
- ยิงอีเวนต์ตาม enum ใน schema (console หรือ provider ภายหลัง)

### FR-8 Safety copy
- ทุกจุดที่โชว์ตัวเลขโภชนาการต้องเข้าถึง disclaimer ได้
- หลีกเลี่ยงคำว่า「ผิด」「ห้ามกิน」「อ้วน」「ดีโทษ」ใน UI หลัก

---

## 14. ความต้องการเชิงไม่ใช่ฟังก์ชัน

| หัวข้อ | เป้า |
|---|---|
| Vision / mock latency (fixture) | p50 ≤ 2s |
| Macro recalc | อัปเดต < 100ms หลังเพิ่ม/ลบมื้อหรือเปลี่ยนเป้า |
| Mobile layout | ใช้งานได้ที่ 390×844 โดยไม่เลื่อนแนวนอนพัง |
| ภาษา | th-TH เป็นค่าเริ่มต้น |
| ความเป็นส่วนตัว | ประมวลผลรูปฝั่ง client เป็นหลัก ไม่อัปโหลดเซิร์ฟเวอร์ถ้าไม่ใช้ vision API |
| Deploy | Vercel preview URL พร้อมแชร์ในไบโอ |
| ตัวเลข | แสดง kcal เป็นจำนวนเต็ม; macros เป็นกรัมทศนิยม 0–1 ตำแหน่งตาม schema |
| Accessibility เบา | ปุ่มใหญ่ คอนทราสต์ตัวเลขบน Reel ผ่านตาเปล่า |

---

## 15. Tech แนะนำสำหรับ gen วันเดียว

| ชั้น | เลือก |
|---|---|
| Frontend | Next.js 14 (App Router) + TypeScript + Tailwind + shadcn/ui |
| Vision | `mock_demo` default · optional vision API ผ่าน env |
| Macro engine | `lib/macros.ts` (pure) + `lib/portion.ts` |
| Share | Canvas / `html-to-image` + `lib/share.ts` |
| State | React state + `lib/storage.ts` (localStorage) |
| Fixtures | `/public/fixtures/demo-meal.json` (+ ภาพมื้อเดโม) |
| Food data | `/data/thai-food-library.json` หรือฝังใน `lib/food-library.ts` |
| Deploy | Vercel |

**โครงสร้างรีโปแนะนำ**

```text
/bitelog
  README.md
  prd.md
  prompts.md
  schemas.json
  examples.json
  /app
  /components
  /lib
    macros.ts
    portion.ts
    vision.ts
    share.ts
    storage.ts
    food-library.ts
  /public/fixtures
  /data
```

ถ้าไม่มี Vision API key: ใช้ `mock_demo` + ปุ่มรูปเดโมเป็นหลัก แล้วหมายเหตุใน UI ว่า「โหมดเดโม — ใส่รูปจริงได้เมื่อเปิด Vision」

---

## 16. ข้อมูลและสคีมา

แหล่งความจริง (ดูรายละเอียดใน `schemas.json` / ตัวอย่างใน `examples.json`):

- `MealEntry` / `FoodItem` / `Portion` / `MacroNutrients`
- `MacroTargets` / `DailyLog` / `ScanResult`
- `Favorite` / `ShareCard` / `SharePayload`
- `LocalStore` / `AnalyticsEvent`
- `FeatureChecklist` / `UiCopyTh` / `ReelScript`
- `VisionEngine` / `MealTag` / `WaterLog` (nice)

---

## 17. Analytics / สำเร็จของแอปในช่อง

**Primary (ผลิตภัณฑ์):** % เซสชันที่ทำ `meal_logged` อย่างน้อย 1 ครั้ง และ/หรือ `share_success`  
**Primary (ช่อง):** save rate ของ Reel + จำนวนคอมเมนต์「แคล」  

**Secondary:**
- `scan_success` rate / median `scan_ms`
- จำนวนครั้งใช้ Library vs Scan ต่อเซสชัน
- การใช้ Favorites / Quick Add
- การเปิด Share card

**Guardrail:** อัตรา `scan_fail`, คอมเมนต์บ่นว่าแอป「เคลมหมอ」, UI ที่ทำให้รู้สึกถูกดุ

---

## 18. Reel shot list (25–35 วินาที)

| เวลา | ภาพ | ข้อความบนจอ | เสียงพูด |
|---|---|---|---|
| 0–3s | รูปจานเบลอ → การ์ดโภชนาการ | ถ่ายแล้วรู้แคล | ถ่ายจานเดียว รู้แคลกับแมโครทันที |
| 3–8s | มอนทาจ gen / โลโก้ | สร้างด้วย AI วันนี้ | วันนี้ทำแอป BiteLog สดๆ |
| 8–14s | อัปโหลดรูป → scan progress → ผลเมนูไทย | Photo Bite Scan | ถ่ายข้าวผัดกุ้ง ขึ้นชื่อไทยให้เลย |
| 14–22s | ยืนยัน portion → แดชบอร์ด rings | บันทึกแล้วดูเป้าวัน | ปรับปริมาณ บันทึก วงแหวนอัปเดต |
| 22–28s | Library / Favorites เร็วๆ + Share card | เพิ่มเร็ว แชร์ได้ | มีไลบรารีไทยและแชร์การ์ดสวย |
| 28–35s | ผลสุดท้าย + ลิงก์ | ลิงก์ในไบโอ | ลองฟรีที่ลิงก์ในไบโอ แล้วคอมเมนต์「แคล」 |

รายละเอียดช็อตเต็มใน `examples.json` → `reel_script_th`

---

## 19. ความเสี่ยง

| ความเสี่ยง | แผนลดความเสี่ยง |
|---|---|
| คนเข้าใจว่าตัวเลขแม่นระดับแล็บ/แพทย์ | Disclaimer ชัดทุกจุด + คัดก็อปปี้「ประมาณการ」— **ห้ามเคลมทางการแพทย์** |
| Vision จริงอ่านเมนูไทยผิด / รูปมืด | ใช้ mock_demo เป็นฮุค Reel หลัก + ให้แก้ชื่อ/เลือกจาก Library ได้ |
| UX แนว guilt-shame ทำให้เลิกใช้ | ตรวจสำเนา UI ห้ามคำดูถูก; ใช้โทนอบอุ่น + streak แบบอ่อนโยน |
| เดโมใช้รูปคนอื่น / แบรนด์ร้านโดยไม่ตั้งใจ | ใช้ fixture สร้างเอง / รูปจานที่ถ่ายเอง |
| มือถือเครื่องอ่อนเรนเดอร์การ์ดช้า | การ์ดเรียบๆ ครีม+coral+เขียว ไม่ใส่เอฟเฟกต์หนัก |
| ผู้ใช้คาดหวัง barcode ทุกอย่างในเซเว่น | โฟกัสมื้อไทย; Library ขยายทีหลัง ไม่สัญญาครบทุก SKU |

---

## 20. แผนส่งมอบวันเดียว (สำหรับคลิป)

| ช่วง | งาน |
|---|---|
| เช้า | Gen โครง Next.js + Home/Scan/Confirm ตาม Master prompt |
| สาย | mock vision + demo fixture ข้าวผัดกุ้ง+ไข่ดาว + Library พื้นฐาน |
| บ่าย | Macro Dashboard + Quick Add/Favorites + Share Progress Card |
| เย็น | QA ตามตัวอย่าง + ถ่าย Reel ตาม shot list + อัป Vercel + ใส่ลิงก์ไบโอ |

---

## 21. Open questions

1. เป้าแมโครวันเริ่มต้นจะใช้ค่า generic (เช่น 2000 kcal / P100 / C250 / F65) หรือให้เลือกแบบเบาๆ (ลด/รักษารูปร่าง/เพิ่ม) โดยไม่ถามน้ำหนัก?
2. รอบถัดไปต่อ Vision API จริงคุ้มไหมสำหรับคลิป หรือพอ mock_demo + Library?
3. เก็บ analytics แค่ console หรือต่อ Plausible/PostHog ตั้งแต่วันที่ 3?

---

## 22. Acceptance criteria (ผ่านก่อนลงคลิป)

- [ ] ปุ่มรูปเดโมโหลดผลสแกนชื่อเมนูไทย + kcal/macros ตาม fixture
- [ ] ปรับ portion แล้วตัวเลขบนการ์ดผลอัปเดตก่อนบันทึก
- [ ] บันทึกมื้อแล้ว Daily Macro Dashboard (rings/bars + ไทม์ไลน์) อัปเดตทันที
- [ ] Thai Food Library ค้นหาและเพิ่มมื้อได้ ≥ 8 รายการตัวอย่าง
- [ ] Favorites / Recent Quick Add ใช้งานได้พร้อม +/- 
- [ ] Share ได้รูปการ์ด + คัดลอกแคปชัน + share sheet (หรือ fallback)
- [ ] มี ≥ 5 ฟีเจอร์ must ตามตาราง และติ๊กใน `FeatureChecklist`
- [ ] มือถือ 390px ใช้งานได้ไม่เละ พรีวิวรูปใหญ่ อ่านตัวเลขบน Reel ได้
- [ ] สคริปต์ Reel ถ่ายครบช็อต + CTA「แคล」ชัด
- [ ] มี disclaimer ประมาณการ และไม่มีเคลมแพทย์ / guilt-shame ใน UI หลัก

---

## 23. รายละเอียดแมโครและการประมาณการ (สำหรับ engine)

### 23.1 หน่วยและกฎแสดงผล
- `kcal`: จำนวนเต็ม (ปัด half-up จากค่าคำนวณ)
- `protein_g`, `carb_g`, `fat_g`: ทศนิยม 1 ตำแหน่งตอนคำนวณภายใน แสดง 0–1 ตำแหน่งตามพื้นที่ UI
- `portion.multiplier` ค่าเริ่ม 1.0 = typical serving ของเมนูนั้น
- เมื่อผู้ใช้กด +/- ให้ขยับทีละ 0.25 (หรือตาม `step` ของ Portion) แล้วคูณ macros ฐาน

### 23.2 ลำดับคำนวณ DailyLog
1. รวบรวม `MealEntry` ของ `date` เดียวกัน (Asia/Bangkok)
2. `consumed = sum(entry.nutrients)` ทุกมื้อ
3. `remaining = target - consumed` (ติดลบได้ — UI แสดงเกินเป้าแบบกลางๆ ไม่แดงดุ)
4. `progress_pct = min(100, round(consumed/target*100))` ต่อแต่ละ macro
5. (nice) เติม `water_ml` จาก WaterLog

### 23.3 ความไม่แน่นอนของสแกน
- `ScanResult.confidence` 0–1; ถ้า < 0.55 แนะนำให้ผู้ใช้เลือกจาก Library
- อนุญาตให้แก้ `detected_name_th` ก่อนบันทึก
- ห้ามซ่อนว่าเป็นประมาณการ

### 23.4 ตัวอย่างเดโมหลัก (ต้องตรง examples)
- มื้อ: ข้าวผัดกุ้ง + ไข่ดาว (จานเดียวรวม)
- ประมาณ: ~720 kcal · P 32g · C 78g · F 28g ที่ multiplier 1.0
- ใช้เป็น fixture ฮุค Reel และทดสอบ recalculation

---

## 24. สำเนาแบรนด์และไมโครคัดก็อปปี้

| จุด | ทิศทางสำเนา |
|---|---|
| Home | อบอุ่น สั้น ชวนถ่าย ไม่ขายคอร์สลดน้ำหนัก |
| หลังสแกน | 「ได้ประมาณการมื้อนี้แล้ว — ปรับปริมาณได้」 |
| เกินเป้า | 「วันนี้เกินเป้าเล็กน้อย — พรุ่งนี้เริ่มใหม่ได้เสมอ」 ไม่ใช้「ล้มเหลว」 |
| สตรีค | 「ต่อเนื่อง X วันแล้ว เก่งมาก」 แบบเพื่อน ไม่แบบโค้ชโหด |
| Disclaimer | 「BiteLog ให้ประมาณการเพื่อบันทึกส่วนตัว ไม่ใช่คำแนะนำทางการแพทย์」 |

สีหลักในโค้ด (แนะนำ CSS variables):

```text
--bg: #FFF7ED;
--card: #FFFFFF;
--accent: #F97316;
--accent-soft: #FFEDD5;
--healthy: #22C55E;
--ink: #1C1917;
--muted: #78716C;
```

---

## 25. ภาคผนวก — สำเนาแพ็ก

แหล่งหลัก:

```text
/workspace/ai-wanla-app/2026-09-30-bitelog/
  README.md
  prd.md
  prompts.md
  schemas.json
  examples.json
```

Zip ในโฟลเดอร์: `/workspace/ai-wanla-app/2026-09-30-bitelog/bitelog.zip`  
Zip ราก: `/workspace/bitelog.zip` (unzip แล้วได้ `bitelog/...`)


---

## 26. รายละเอียดหน้าจอและคอมโพเนนต์ (สำหรับ codegen)

### 26.1 Home
- Hero หัวข้อไทย + คำบรรยาย 1 บรรทัด
- Demo strip แนวนอน 3 เฟรม: รูปจาน → การ์ดผล → แดชบอร์ด rings
- Primary CTA `ถ่ายมื้อนี้` / Secondary `ใช้รูปเดโม`
- แถวไอคอน 5 ฟีเจอร์ must
- ลิงก์ข้อความ `ดูมื้อวันนี้` ไป Dashboard
- Footer disclaimer หนึ่งบรรทัด

### 26.2 Scan / Upload
- พื้นที่พรีวิวสูงอย่างน้อย ~45vh
- ปุ่มเปิดกล้อง / เลือกไฟล์ / ใช้รูปเดโม
- Progress bar หรือ skeleton การ์ดตอน `scanning`
- ถ้า error: ปุ่มลองใหม่ + ไป Library

### 26.3 Scan Result Confirm
- ชื่อเมนูแก้ได้
- Alternatives chips
- kcal ตัวใหญ่ + macro chips
- Portion stepper
- Disclaimer ใต้การ์ดผล
- CTA บันทึกมื้อนี้

### 26.4 Library
- Search input sticky
- ผลลัพธ์เป็นแถว: emoji · ชื่อไทย · kcal ต่อหน่วย · ปุ่มบวก
- กรองหมวดหมู่ chips (เส้นก๋วยเตี๋ยว / ข้าว / ของหวาน / เครื่องดื่ม)

### 26.5 Dashboard
- วันที่ไทย + ปุ่มแชร์มุมขวา
- วงแหวน kcal
- แถบ P/C/F
- ไทม์ไลน์มื้อ + ปุ่มลบต่อรายการ
- ทางลัด Quick Add / Library / ถ่ายมื้อ

### 26.6 Share sheet
- พรีวิวการ์ด
- คัดลอกแคปชัน
- แชร์ระบบ / ดาวน์โหลดรูป
- ข้อความว่าไม่เก็บรูปบนเซิร์ฟเวอร์ใน MVP

---

## 27. เกณฑ์คุณภาพ Reel (ช่อง)

1. ฮุค 3 วินาทีแรกต้องเห็นการเปลี่ยนรูป→การ์ด ไม่ใช่โลโก้ยาว
2. ในคลิปเดียวโชว์ ≥3 ฟีเจอร์ must
3. UI จริงจากบิลด์ที่ deploy ไม่ใช่แค่ Figma
4. พูดหรือติดข้อความ「ประมาณการ」อย่างน้อย 1 ครั้ง
5. CTA ปิดคลิป: ลิงก์ในไบโอ + คอมเมนต์「แคล」
6. ห้ามใช้เพลง/ฟุตเทจที่เสี่ยงลิขสิทธิ์หนักโดยไม่จำเป็น — โฟกัสหน้าจอแอป

---

## 28. ค่าเริ่มต้นที่ล็อกสำหรับเดโมเช้านี้

| ค่า | ค่าเริ่ม |
|---|---|
| Vision engine | `mock_demo` |
| เป้าวัน | 2000 kcal / P100 / C250 / F65 |
| Hero fixture | ข้าวผัดกุ้งไข่ดาว ~720 kcal |
| ความกว้าง UI ฐาน | 390px |
| คำคอมเมนต์ CTA | แคล |
| localStorage key | `bitelog.v1` |
| ภาษา UI | th-TH |

ค่าเหล่านี้ต้องตรงกับ `examples.json` เพื่อให้ QA เทียบตัวเลขได้เร็วตอนเย็นก่อนขึ้นคลิป
