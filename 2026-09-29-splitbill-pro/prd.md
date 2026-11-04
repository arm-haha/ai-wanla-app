# PRD: SplitBill Pro

**Product name:** SplitBill Pro  
**Tagline (TH):** สแกนสลิป → หารบิลตามเมนูจริง ใน 15 วินาที  
**Tagline (EN):** Scan a Thai receipt, assign dishes, split fair — share in one tap  
**Version:** 1.0 (MVP — AI-วันละแอป Day 2/10)  
**Channel date:** 2026-09-29 (Asia/Bangkok)  
**Platform:** Web app (mobile-first) + PWA  
**Language:** Thai UI first, English secondary  
**Status:** Delivery-ready for official morning run  
**Related docs:** `README.md`, `prompts.md`, `schemas.json`, `examples.json`  
**Last updated:** 2026-09-29 (Asia/Bangkok)

---

## 1. สรุปสั้นๆ

แอปมินิสวีทให้กลุ่มเพื่อนคนไทยถ่าย/อัปโหลดสลิปร้านอาหารหรือคาเฟ่ → OCR ดึงรายการเมนู+ราคา → เพิ่มชื่อเพื่อน → ลากหรือติ๊กเมนูให้คน (หรือแชร์จาน) → คิดทิป / เซอร์วิสชาร์จ / VAT ตามสลิปไทย → เลือกโหมดหาร (เท่ากัน / ตามเมนู / ปรับเอง) → แชร์สรุปเป็นรูปการ์ดสวย + ข้อความ LINE + ลิงก์ mock

ออกแบบให้เดโมใน Reel 15–30 วินาทีเห็นสลิป→ยอดต่อคนชัด และมีฟีเจอร์รองที่ดึงคนกลับมาเปิดซ้ำ (friends presets, history, settle tracker)

MVP ไม่มีบัญชีผู้ใช้ ไม่มีเพย์เมนต์จริง / PromptPay gateway ไม่เก็บบิลบนคลาวด์

---

## 2. ปัญหาที่แก้

| ปัญหาวันนี้ | ผลกระทบ |
|---|---|
| หารบิลด้วยเครื่องคิดเลข + พิมพ์ในแชท | ช้า ผิดบ่อย ทะเลาะเรื่องใครกินอะไร |
| แอปหารบิลต่างประเทศไม่รองรับสลิปไทย / เซอร์วิสชาร์จ | ต้องแก้ตัวเลขมือหลายรอบ |
| หารเท่ากันทั้งโต๊ะทั้งที่บางคนไม่กินบางจาน | ไม่แฟร์ เพื่อนเงียบแต่หงุดหงิด |
| สรุปยอดไม่มีรูปสวยส่ง LINE | ต้องแคปจอรก หรือพิมพ์ยาว |
| เครื่องมือ B2B / expense report | ไม่เหมาะเดโม Reel 15–30 วินาที และคนทั่วไปไม่ใช้ |

**โอกาสช่อง AI วันละแอป:** แจกแอปฟรีที่ผลลัพธ์เห็นทันทีหลังสแกนสลิป → save rate สูง → คนเข้าลิงก์ลองตอนกินข้าวจริง → ติดตามเพื่อรอแอปวันถัดไป

---

## 3. เป้าหมายผลิตภัณฑ์

### 3.1 Goals (MVP / วันเดียว + คลิปเช้า)

1. Happy path จบบนมือถือ: อัปโหลด/สแกนสลิป → OCR (หรือโหลด fixture) → ใส่คน ≥3 → ลากเมนู → ใส่ทิป → แชร์ได้ภายใน **≤ 60 วินาที** สำหรับผู้ใช้ทั่วไป
2. มี **≥ 5 ฟีเจอร์ must-have** ที่ใช้ได้จริงและโชว์ในคลิปได้อย่างน้อย 3 ตัว
3. Demo receipt fixture คุณภาพดีอย่างน้อย **1 ใบ** (ร้านไทย มี service charge + VAT) พร้อม OCR mock result
4. คำนวณยอดต่อคนตรงกับตัวอย่างใน `examples.json` (tolerance ±0.01 THB หลังปัด)
5. คลิป Reel 25–35 วินาทีถ่ายจบด้วย UI จริง ไม่ใช่ mock อย่างเดียว

### 3.2 Non-goals (MVP)

- ไม่มีระบบล็อกอิน / คลาวด์ซิงก์บิล
- ไม่เชื่อม PromptPay / โอนเงินจริง / payment gateway
- ไม่ทำ OCR ภาษาจีน/ญี่ปุ่นเป็นหลัก (โฟกัสสลิปไทย + ตัวเลข)
- ไม่มี native iOS/Android store build
- ไม่ทำบัญชีร้าน / ใบกำกับภาษี / รายงานบัญชีบริษัท
- ไม่บังคับ API OCR จริง — mock_demo คุณภาพดีพอสำหรับเดโมและคลิป

---

## 4. ผู้ใช้และบทบาท

| บทบาท | ความต้องการหลัก |
|---|---|
| **เพื่อนกินข้าวกลุ่ม 3–8 คน (หลัก)** | หารบิลแฟร์ตามเมนู ส่ง LINE ได้ทันทีหลังจ่าย |
| **คนจ่ายบิลแทน** | รู้ว่าใครติดเท่าไร ไม่ต้องไล่ทวงด้วยตัวเลขมั่ว |
| **ผู้ชมช่อง AI วันละแอป** | เห็น wow สลิป→ยอด ใน 3 วินาที อยากลองลิงก์ในไบโอ |
| **ผู้สร้างคลิป (เรา)** | gen แอปใน 1 วัน มีสคริปต์ช็อตและเช็คลิสต์พร้อมถ่าย |

---

## 5. User stories

1. ในฐานะผู้ใช้ ฉันถ่ายหรืออัปโหลดสลิปแล้วได้รายการเมนู+ราคาอัตโนมัติภายในไม่กี่วินาที
2. ในฐานะผู้ใช้ ฉันเพิ่มชื่อเพื่อนพร้อมสี/อวตาร์แล้วลากเมนูให้แต่ละคนได้
3. ในฐานะผู้ใช้ ฉันติ๊กหลายคนบนจานเดียวเพื่อแชร์ราคากันได้
4. ในฐานะผู้ใช้ ฉันใส่ทิปเป็น % หรือจำนวนเงิน และเปิด/ปิด service charge + VAT ตามสลิป
5. ในฐานะผู้ใช้ ฉันสลับโหมดหาร equal / by item / custom แล้วยอดต่อคนอัปเดตทันที
6. ในฐานะผู้ใช้ ฉันแชร์สรุปเป็นรูปการ์ด + คัดลอกข้อความ LINE + เปิด share sheet ได้
7. ในฐานะผู้ชม Reel ฉันเห็นสลิป→ยอดต่อคนใน 3 วินาทีแรกแล้วอยากลองแอป
8. ในฐานะระบบ ทุกบิลต้องเก็บ state ตาม `BillState` และ history ตาม `LocalStore`

---

## 6. ฮุค Reel (3 วินาทีแรก)

**Before:** สลิปร้านอาหารยับๆ + แชทเพื่อนถาม「ใครกินอะไร」  
**After:** รายการเมนูขึ้นครบ → การ์ดยอดต่อคน 3 สีสวย  
**ข้อความบนจอ:** `สแกนสลิป → หารบิลตามเมนูจริง ใน 15 วินาที`  
**เสียง:** 「กินด้วยกันแล้วเลิกบวกเลขในแชท」

**Wow moment กลางคลิป:** ลากเมนูให้เพื่อน 3 คนเร็วๆ → ยอดบนการ์ดกระโดดขึ้นตาม → กดแชร์ LINE

---

## 7. ทำไมคนติดตาม / เปิดซ้ำ

- ผลสลิป→ยอดทันที (เหมาะ Reel + save)
- ใช้จริงได้ทุกมื้อกินกับเพื่อน / หลังเลิกงาน / ทริป
- แจกฟรีจากช่อง → เซฟคลิป + เข้าลิงก์
- รีเทนชัน: Friends presets, Bill History, Settle tracker, โหมดหารหลายแบบ
- คอมเมนต์「หาร」= สัญญาณทำคลิปต่อ / ขอฟีเจอร์เพิ่ม

---

## 8. กฎผลิตภัณฑ์ช่อง

- **ขั้นต่ำ 5 ฟีเจอร์** must-have (ตารางด้านล่าง)
- Gen ได้ใน 1 วันด้วย AI codegen (Next.js + OCR pluggable)
- เดโมหลักจบในมือถือแนวตั้ง (~390px)
- UI สวย พอเป็นพรีวิว “แอปจริง” ไม่ใช่ฟอร์มดิบ
- ภาษาไทยก่อน — คีย์สคีมาภาษาอังกฤษได้

---

## 9. ฟีเจอร์

### 9.1 Must-have (≥ 5)

| # | ฟีเจอร์ | รายละเอียด | Acceptance ย่อ |
|---|---|---|---|
| 1 | **Receipt Scan / OCR** | ถ่าย/อัปโหลดสลิป → ได้รายการเมนู+ราคา; default engine `mock_demo` + ช่องเสียบ Tesseract/API | fixture เดโมขึ้นรายการครบใน ≤2s |
| 2 | **Item Assign** | แตะ/ลากเมนูให้คน หรือติ๊กหลายคนแชร์จาน (แบ่งราคาเท่าๆ ในกลุ่มที่ติ๊ก) | ยอดต่อคนอัปเดตทันทีหลังลาก |
| 3 | **Tip & Service Charge** | ทิป % หรือจำนวนเงินคงที่ + service charge ตามสลิป + VAT ถ้ามี | ตัวเลขตรงตัวอย่าง ±0.01 THB |
| 4 | **Split Modes** | `equal` / `by_item` / `custom` (แก้ยอดคนเองได้ใน custom) | สลับโหมดแล้วไม่พัง assignments |
| 5 | **Share Pack** | รูปการ์ดสรุปสวย + ข้อความคัดลอก LINE + deep share sheet + ลิงก์ mock (QR ออปชัน) | ได้รูป+ข้อความบน iPhone Safari |

### 9.2 Nice-to-have

| # | ฟีเจอร์ | รายละเอียด |
|---|---|---|
| 6 | **Friends presets** | รายชื่อเพื่อนถาวรใน localStorage เลือกเร็วตอนเปิดบิลใหม่ |
| 7 | **Bill History** | ประวัติบิลล่าสุดสูงสุด 20 รายการ (localStorage) |
| 8 | **Settle tracker** | ติ๊กใครจ่ายแล้ว/ยัง ต่อบิล |
| 9 | **Multi-currency display** | แสดงหน่วยอื่นได้ แต่คำนวณหลักเป็น THB |

---

## 10. ขอบเขตฟีเจอร์

### 10.1 In scope

- Home, Scan/Upload, Bill Editor (items + people), Split Summary, Share sheet, History (optional)
- OCR pluggable: `mock_demo` (default) · optional `tesseract_client` / `ocr_api` ผ่าน env
- Bill engine ใน `lib/split.ts` (pure functions)
- Share card render บน Canvas / DOM-to-image
- Analytics events ฝั่ง client (optional log)
- PWA ติดตั้งได้แบบพื้นฐาน (manifest + icons)

### 10.2 Out of scope (เฟสถัดไป)

- Auth / cloud sync บิล
- PromptPay QR จริง / โอนเงินในแอป / payment gateway
- OCR ฝึกโมเดลเอง
- สแกนหลายสลิปรวมบิลอัตโนมัติ
- บัญชีร้าน / e-tax / ใบเสร็จรับเงินออกให้ลูกค้า

---

## 11. User flow หลัก (Happy path)

```text
เปิดแอป → ถ่ายหรืออัปโหลดสลิป (หรือกด「ใช้สลิปเดโม」)
  → OCR / mock parse (progress สวย เป้า ≤ 2s สำหรับ fixture)
  → ตรวจ/แก้รายการเมนูสั้นๆ ถ้าต้องการ
  → เพิ่มเพื่อน (≥2 คน) หรือเลือกจาก Friends presets
  → ลาก/ติ๊กเมนูให้คน (แชร์จานได้)
  → ตั้งทิป / เปิด service charge / VAT
  → เลือก Split Mode (default by_item)
  → ดูสรุปยอดต่อคนบนการ์ดสี
  → แชร์รูป / คัดลอกข้อความ LINE / เปิด share sheet
  → บันทึก history ท้องถิ่น (nice)
```

### สถานะบิล

`idle` → `scanning` → `editing` → `splitting` → `sharing`  
ทางแยก: `error` (พร้อมข้อความไทยสั้นๆ + ปุ่มลองใหม่ / ใส่รายการมือ)

---

## 12. หน้าจอ (MVP)

| # | หน้าจอ | องค์ประกอบหลัก |
|---|---|---|
| 1 | **Home** | โลโก้, หัวข้อไทย, แถบเดโมสลิป→การ์ดยอด, CTA「เริ่มหารบิล」, แถบ 5 ฟีเจอร์ไอคอน, ปุ่มรอง「ใช้สลิปเดโม」 |
| 2 | **Scan / Upload** | ช่องกล้อง/ไฟล์, ปุ่มสลิปเดโม, progress OCR, พรีวิวสลิป |
| 3 | **Bill Editor** | รายการเมนู+ราคา, แถบคน (อวตาร์สี), โซนลาก/ติ๊ก assign, แผงทิป/เซอร์วิส/VAT, สลับ Split Mode |
| 4 | **Split Summary** | การ์ดยอดต่อคนใหญ่ สีต่างกัน, รวมทิป/เซอร์วิส, ปุ่มไปแชร์ |
| 5 | **Share sheet** | พรีวิวการ์ดรูป, ปุ่มคัดลอกข้อความ LINE, แชร์ระบบ, ลิงก์ mock, QR ออปชัน |
| 6 | **History** (nice) | รายการบิลล่าสุดจาก localStorage |

**โทนแบรนด์:** พื้นขาวครีมอ่อน (#FFF8F1 / #FAF7F2), ไฮไลต์ teal/mint (#0D9488 / #14B8A6), ตัวเลขเงินตัวหนาชัด, ปุ่ม primary ใหญ่, การ์ดยอดต่อคนมีอวตาร์สีสด — โทน “money clarity” ที่ถ่าย Reel แล้วอ่านง่าย

---

## 13. ความต้องการเชิงฟังก์ชัน

### FR-1 Receipt Scan / OCR
- รับไฟล์ภาพจากไฟล์หรือกล้อง
- รัน engine ตาม `ocr_engine` (ค่าเริ่ม `mock_demo`)
- มีปุ่ม「ใช้สลิปเดโม」โหลด fixture จาก `/fixtures/demo-receipt.json`
- เก็บ `ocr_ms`, confidence, raw text ใน `OcrResult`
- ถ้า OCR ล้มเหลว: ให้แก้/เพิ่มรายการมือได้

### FR-2 Item Assign
- แต่ละ `LineItem` มี `assignments[]` อ้าง `person_id`
- ถ้าหลายคนบนจานเดียว → หารราคาเท่าๆ (ปัดเงินตามกฎใน `lib/split.ts`)
- UI: แตะเมนูแล้วเลือกคน หรือลากเมนูใส่การ์ดคน

### FR-3 Tip & Service Charge
- `TipSettings`: mode `percent` | `fixed` + value
- `ServiceCharge`: enabled + percent (ค่าเริ่ม 10% แบบร้านไทยหลายแห่ง)
- `TaxSettings`: VAT enabled + percent (ค่าเริ่ม 7%)
- ลำดับคำนวณชัดเจนใน bill engine (ดู schemas + examples)

### FR-4 Split Modes
- `equal`: หารรวมเท่ากันทุกคน (ยังโชว์เมนูได้แต่ไม่บังคับ assign)
- `by_item`: ใช้ assignments เป็นหลัก (default)
- `custom`: แก้ยอดสุทธิคนเองได้ แล้วระบบกระจายส่วนต่างหรือล็อกตามที่ระบุ

### FR-5 Share Pack
- เรนเดอร์การ์ดสรุปเป็น PNG (Canvas หรือ html-to-image)
- สร้างข้อความไทยสำหรับ LINE ตามเทมเพลต
- `navigator.share` ถ้ามี + fallback คัดลอก/ดาวน์โหลด
- ลิงก์ mock `https://splitbill.pro/b/{bill_id}` (ไม่ต้องมี backend จริงใน MVP)
- QR ออปชัน encode ลิงก์ mock หรือข้อความสรุป

### FR-6 Local retention (nice path)
- บันทึก friends + history ตาม `LocalStore`
- ไม่บังคับ auth

### FR-7 Analytics (เบา)
- ยิงอีเวนต์ตาม enum ใน schema (console หรือ provider ภายหลัง)

---

## 14. ความต้องการเชิงไม่ใช่ฟังก์ชัน

| หัวข้อ | เป้า |
|---|---|
| OCR / mock latency (fixture) | p50 ≤ 2s |
| Bill recalc | ยอดอัปเดต < 100ms หลังเปลี่ยน assign/ทิป |
| Mobile layout | ใช้งานได้ที่ 390×844 โดยไม่เลื่อนแนวนอนพัง |
| ภาษา | th-TH เป็นค่าเริ่มต้น |
| ความเป็นส่วนตัว | ประมวลผลสลิปฝั่ง client เป็นหลัก ไม่อัปโหลดเซิร์ฟเวอร์ถ้าไม่ใช้ OCR API |
| Deploy | Vercel preview URL พร้อมแชร์ในไบโอ |
| เงิน | แสดงเป็นบาท (THB) ปัดทศนิยม 2 ตำแหน่ง ตามกฎใน engine |

---

## 15. Tech แนะนำสำหรับ gen วันเดียว

| ชั้น | เลือก |
|---|---|
| Frontend | Next.js 14 (App Router) + TypeScript + Tailwind + shadcn/ui |
| OCR | `mock_demo` default · optional Tesseract.js หรือ API ผ่าน env |
| Bill engine | `lib/split.ts` (pure) + `lib/money.ts` |
| Share | Canvas / `html-to-image` + `lib/share.ts` |
| State | React state + `lib/storage.ts` (localStorage) |
| Fixtures | `/public/fixtures/demo-receipt.json` (+ ภาพสลิปเดโม) |
| Deploy | Vercel |

**โครงสร้างรีโปแนะนำ**

```text
/splitbill-pro
  README.md
  prd.md
  prompts.md
  schemas.json
  examples.json
  /app
  /components
  /lib
    split.ts
    money.ts
    ocr.ts
    share.ts
    storage.ts
  /public/fixtures
```

ถ้าไม่มี OCR API key: ใช้ `mock_demo` + ปุ่มสลิปเดโมเป็นหลัก แล้วหมายเหตุใน UI ว่า「โหมดเดโม — ใส่สลิปจริงได้เมื่อเปิด OCR」

---

## 16. ข้อมูลและสคีมา

แหล่งความจริง (ดูรายละเอียดใน `schemas.json` / ตัวอย่างใน `examples.json`):

- `MoneyAmount` / `Person` / `LineItem` / `Assignment`
- `TipSettings` / `ServiceCharge` / `TaxSettings` / `SplitMode`
- `BillState` / `SharePayload`
- `OcrEngine` / `OcrResult`
- `LocalStore` / `HistoryItem`
- `AnalyticsEvent` / `FeatureChecklist`

---

## 17. Analytics / สำเร็จของแอปในช่อง

**Primary (ผลิตภัณฑ์):** % เซสชันที่ทำ `share_success` หรือ `copy_line_text` อย่างน้อย 1 ครั้ง  

**Primary (ช่อง):** save rate ของ Reel + จำนวนคอมเมนต์「หาร」  

**Secondary:**
- `ocr_success` rate / median `ocr_ms`
- จำนวนครั้ง `item_assign` ต่อเซสชัน (เป้า ≥ 3 ในเดโม)
- การใช้ tip / service charge
- สัดส่วน split mode ที่ใช้

**Guardrail:** อัตรา `ocr_fail`, ผู้ใช้บ่นว่ายอดไม่ตรงสลิป

---

## 18. Reel shot list (25–35 วินาที)

| เวลา | ภาพ | ข้อความบนจอ | เสียงพูด |
|---|---|---|---|
| 0–3s | สลิปยับ → รายการขึ้น | สแกนแล้วได้เมนู | กินด้วยกันแล้วเลิกบวกเลขในแชท |
| 3–8s | มอนทาจ gen / โลโก้ | สร้างด้วย AI วันนี้ | วันนี้ทำแอป SplitBill Pro สดๆ |
| 8–14s | อัปโหลดสลิป → OCR progress → รายการ | สแกนสลิป | ถ่ายสลิป รายการขึ้นเอง |
| 14–22s | ลากเมนูให้ 3 คน + ทิป | ลากเมนูให้เพื่อน | ลากเมนูให้เพื่อน คิดทิปให้ด้วย |
| 22–28s | การ์ดยอดต่อคน + Share LINE | แชร์ยอด LINE | กดแชร์ได้ทั้งรูปและข้อความ |
| 28–35s | ผลสุดท้าย + ลิงก์ | ลิงก์ในไบโอ | ลองฟรีที่ลิงก์ในไบโอ แล้วคอมเมนต์「หาร」 |

รายละเอียดช็อตเต็มใน `examples.json` → `reel_script_th`

---

## 19. ความเสี่ยง

| ความเสี่ยง | แผนลดความเสี่ยง |
|---|---|
| OCR สลิปยับ/มุมเอียงอ่านผิด | มีปุ่มสลิปเดโมคุณภาพดีในคลิป + ให้แก้รายการมือได้ + โชว์ progress ชัด |
| ฟอนต์ไทยบนสลิปอ่านยาก (thermal print) | อย่าพึ่ง OCR จริงเป็นฮุคเดียว — ใช้ mock_demo ใน Reel หลัก; Tesseract/API เป็นออปชัน |
| ยอดปัดเศษไม่ตรงสลิปร้าน | กำหนดกฎปัดใน `lib/money.ts` ชัด + โชว์ส่วนต่าง「เศษปัด」บนสรุป |
| คนคาดหวังโอนเงินในแอป / PromptPay | คัดก็อปปี้ชัดว่า「แชร์สรุปอย่างเดียว ไม่ใช่แอปโอนเงิน」— **ห้ามต่อ PromptPay/payment โดยไม่มี compliance** |
| เดโมใช้สลิปคนอื่นมีข้อมูลส่วนตัว | ใช้ fixture สร้างเอง / เบลอข้อมูลอ่อนไหว |
| มือถือเครื่องอ่อนเรนเดอร์การ์ดช้า | เรนเดอร์การ์ดเรียบๆ โทนครีม+teal ไม่ใส่เอฟเฟกต์หนัก |

---

## 20. แผนส่งมอบวันเดียว (สำหรับคลิป)

| ช่วง | งาน |
|---|---|
| เช้า | Gen โครง Next.js + Home/Scan/Editor ตาม Master prompt |
| สาย | OCR mock + demo fixture + Item Assign ลื่นบนมือถือ |
| บ่าย | Tip/Service/VAT + Split Modes + Share Pack |
| เย็น | QA ตามตัวอย่างตัวเลข + ถ่าย Reel ตาม shot list + อัป Vercel + ใส่ลิงก์ไบโอ |

---

## 21. Open questions

1. ลำดับคำนวณ service charge กับ VAT จะยึดแบบ「เซอร์วิสก่อน VAT」เป็นค่าเริ่มเสมอ หรือให้ผู้ใช้สลับได้ใน MVP?
2. รอบถัดไปใส่ PromptPay QR แบบ「โชว์ยอดอย่างเดียวให้สแกนจากแอปธนาคาร」โดยไม่ถือเงิน — คุ้มความเสี่ยง合规ไหม?
3. เก็บ analytics แค่ console หรือต่อ Plausible/PostHog ตั้งแต่วันที่ 2?

---

## 22. Acceptance criteria (ผ่านก่อนลงคลิป)

- [ ] ปุ่มสลิปเดโมโหลดรายการเมนูครบตาม fixture
- [ ] เพิ่มคนได้อย่างน้อย 4 คน พร้อมสี/อวตาร์ต่างกัน
- [ ] ลากหรือติ๊กเมนูให้คน + แชร์จานได้ ยอดอัปเดตทันที
- [ ] ทิป % + service charge + VAT คำนวณตรงตัวอย่างใน `examples.json`
- [ ] สลับ Split Modes ได้ 3 แบบโดยไม่พัง state
- [ ] Share ได้รูปการ์ด + คัดลอกข้อความ LINE + share sheet (หรือ fallback)
- [ ] มี ≥ 5 ฟีเจอร์ must ตามตาราง และติ๊กใน `FeatureChecklist`
- [ ] มือถือ 390px ใช้งาน editor ได้ไม่เละ
- [ ] สคริปต์ Reel ถ่ายครบช็อต + CTA「หาร」ชัด
- [ ] ไม่โชว์เลขบัตร/ข้อมูลส่วนตัวจริงในคลิป และไม่มีเพย์เมนต์จริง

---

## 23. ภาคผนวก — สำเนาแพ็ก

แหล่งหลัก:

```text
/workspace/splitbill-pro/
  README.md
  prd.md
  prompts.md
  schemas.json
  examples.json
```

Zip: `/workspace/splitbill-pro.zip`  
ออปชันวันที่: `/workspace/ai-wanla-app/2026-09-29-splitbill-pro/`
