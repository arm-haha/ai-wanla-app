# SplitBill Pro — Prompt สั่งงาน (จัดเต็ม)

ใช้กับ AI codegen (Cursor / Claude / GPT) สำหรับสร้างแอปทั้งก้อน  
และใช้สร้าง demo receipt fixtures / OCR mock

**วันที่แพ็ก:** 2026-09-29 (Asia/Bangkok) · Day 2/10 · AI วันละแอป  
**เอกสารคู่กัน:** `prd.md`, `schemas.json`, `examples.json`

---

## A) Master prompt สร้างทั้งแอป (วางครั้งเดียว)

```text
สร้างเว็บแอปมือถือเป็นหลักชื่อ SplitBill Pro (ภาษาไทย UI ก่อน)

วันที่ส่งมอบคอนเทนต์: 2026-09-29 สำหรับช่อง "AI วันละแอป"
เป้าหมายผู้ใช้: ถ่าย/อัปโหลดสลิปร้านอาหาร → OCR รายการเมนู+ราคา → เพิ่มเพื่อน → ลาก/ติ๊กเมนูให้คน (แชร์จานได้) → คิดทิป/เซอร์วิสชาร์จ/VAT → เลือกโหมดหาร → แชร์สรุปเป็นรูปการ์ด + ข้อความ LINE + ลิงก์ mock

สแต็กบังคับ:
- Next.js 14 App Router + TypeScript + Tailwind CSS + shadcn/ui
- OCR pluggable ใน lib/ocr.ts: ค่าเริ่มต้น engine "mock_demo" โหลด fixture คุณภาพดี
  (รองรับสลับไป tesseract_client / ocr_api ผ่าน env ถ้าระบุ แต่ไม่บังคับ)
- Bill engine pure functions ใน lib/split.ts + lib/money.ts
- Share card + LINE text ใน lib/share.ts
- เก็บ bills / friends / history ใน localStorage (lib/storage.ts)
- Deploy พร้อมบน Vercel (PWA พื้นฐานมี manifest ก็พอ)
- ไม่มี auth และไม่มีเพย์เมนต์จริง / PromptPay gateway ใน MVP

ต้องมีอย่างน้อย 5 ฟีเจอร์ must-have:
1) Receipt Scan / OCR — อัปโหลด/ถ่ายสลิป + ปุ่ม「ใช้สลิปเดโม」+ progress สวย
2) Item Assign — แตะ/ลากเมนูให้คน หรือติ๊กหลายคนแชร์จาน
3) Tip & Service Charge — ทิป % หรือจำนวนเงิน + service charge + VAT แบบสลิปไทย
4) Split Modes — equal / by_item / custom
5) Share Pack — รูปการ์ดสรุป + ข้อความคัดลอก LINE + navigator.share + ลิงก์ mock (QR ออปชัน)

พิเศษถ้าเสร็จเร็ว (nice-to-have):
- Friends presets (รายชื่อเพื่อนถาวร local)
- Bill History สูงสุด 20 รายการ
- Settle tracker (ใครจ่ายแล้ว/ยัง)
- Multi-currency display (THB เป็นหลัก)

หน้าจอ: Home, Scan/Upload, Bill Editor, Split Summary, Share sheet, History (optional)

UX บังคับ:
- มือถือแนวตั้งก่อน (390px เป็นฐาน)
- ปุ่มใหญ่ นิ้วกดง่าย
- โทนพื้นขาวครีมอ่อน + ไฮไลต์ teal/mint (#0D9488) — อ่านตัวเลขเงินชัดบน Reel
- การ์ดยอดต่อคนมีอวตาร์สีต่างกัน
- ข้อความ UI ภาษาไทยตาม examples.json → ui_copy_th

คุณภาพโค้ด:
- แยก components, hooks, lib/split.ts, lib/money.ts, lib/ocr.ts, lib/share.ts, lib/storage.ts
- มี TypeScript types ให้สอดคล้อง schemas.json
- README ภาษาไทย: วิธีรัน, วิธีเพิ่มสลิปเดโม, วิธีถ่าย Reel เดโม
- อย่าทำระบบล็อกอินหรือจ่ายเงินใน MVP
- เริ่มจากให้รัน `npm run dev` ผ่าน และทำ happy path ให้จบก่อน แล้วค่อยเสริม friends/history/settle

อ้างอิงฟิลด์และตัวอย่างจาก schemas.json + examples.json ที่แนบมา
เมื่อจบให้สรุปว่าฟีเจอร์ must 5 ตัวอยู่ไฟล์ไหน และวิธีโหลดสลิปเดโม 1 ย่อหน้า
```

---

## B) Prompt สร้าง Demo receipt fixtures / OCR mock data

```text
สร้างชุดข้อมูลเดโมสำหรับ SplitBill Pro

1) ไฟล์ภาพสลิปสมมติหรือคำอธิบาย fixture ร้านอาหารไทยชื่อ "ครัวบ้านนา" 
2) ไฟล์ /public/fixtures/demo-receipt.json ตาม schema OcrResult + LineItem
3) ต้องมีอย่างน้อย:
   - รายการเมนู 6–10 รายการ ชื่อไทยธรรมชาติ ราคาสมจริง (บาท)
   - มีจานแชร์อย่างน้อย 2 รายการ (เช่น ส้มตำ, ต้มยำ)
   - subtotal, service_charge 10%, vat 7%, tip แนะนำ 10%
   - วันที่/เวลาในสลิปเป็น Asia/Bangkok

หลีกเลี่ยง: เลขบัตรเครดิต, เบอร์โทรจริง, ชื่อคนจริงที่ไม่ใช่ตัวอย่าง, QR PromptPay จริง

ตั้งชื่อคนตัวอย่างในบิลเต็ม (examples) 4 คน: มุก, เติ้ล, นนท์, ฝน
ส่งท้าย: ตารางรายการเมนู | ราคา | ใครจ่าย/แชร์ สำหรับแปะในรีโป
ให้ตัวเลขสุดท้ายตรงกับ bill_state_example / split_result_example ใน examples.json
```

---

## C) System prompt สำหรับ OCR Assistant (ออปชัน, ภาษาไทย)

```text
คุณช่วยผู้ใช้ตรวจรายการจากสลิปใน SplitBill Pro
พูดภาษาไทยสั้นๆ อบอุ่น ไม่เทคนิคเกิน

หน้าที่:
1) อ่านข้อความดิบจาก OCR แล้วแนะนำรายการเมนู+ราคาเป็น JSON ตาม schema LineItem
2) ถ้ามั่นใจไม่ถึง ให้ใส่ confidence ต่ำและบอกผู้ใช้ให้แก้
3) จับ service charge / VAT / ส่วนลด ถ้ามีในสลิป
4) ห้ามแต่งรายการที่ไม่มีในสลิป

ถ้าสลิปยับหรือฟอนต์ไทยอ่านไม่ออก:
- บอกให้ถ่ายใหม่ให้ตรง แสงพอ ไม่สะท้อน
- หรือให้พิมพ์รายการมือทีละบรรทัด

ห้ามสัญญาความแม่น 100%
ห้ามแนะนำให้เชื่อมต่อแอปโอนเงินหรือเก็บเลขบัญชีในแอปนี้
```

---

## D) Prompt ออกแบบหน้า Home + โทนแบรนด์

```text
ออกแบบ UI SplitBill Pro โหมดมือถือ

โทน: พื้นขาวครีมอ่อน (#FFF8F1), การ์ดขาว, ไฮไลต์ teal/mint (#0D9488 / #14B8A6),
ตัวเลขเงินตัวหนาสีเทาเข้ม, อวตาร์คนสีสด (coral, sky, violet, amber)
ฟอนต์: system / Inter / Noto Sans Thai
ความหนาแน่นต่ำ เน้นการ์ดยอดและปุ่มใหญ่ ไม่โปสเตอร์รก

หน้า Home ต้องมี:
- โลโก้ข้อความ SplitBill Pro
- หัวข้อ: หารบิลตามเมนูจริง ใน 15 วินาที
- คำอธิบายสั้น 1 บรรทัด
- แถบเดโมเลื่อนได้: สลิป → รายการ → การ์ดยอด 3 คน
- ปุ่มหลักใหญ่: เริ่มหารบิล
- ปุ่มรอง: ใช้สลิปเดโม
- แถวไอคอน 5 ฟีเจอร์: สแกนสลิป | ลากเมนู | ทิป/เซอร์วิส | โหมดหาร | แชร์สรุป
- ฟุตเตอร์เล็ก: สร้างสำหรับช่อง AI วันละแอป

อย่าใส่ราคาหรือปุ่มสมัครสมาชิก หรือปุ่ม「โอนเงิน」
ส่งเป็นโครงสร้างคอมโพเนนต์ React + คลาส Tailwind
```

---

## E) Prompt Bill engine / split calculation lib

```text
เขียน lib/money.ts และ lib/split.ts สำหรับ SplitBill Pro ให้เข้ากับ schemas.json

lib/money.ts:
- type MoneyAmount = { currency: "THB"; amount_satang: number } หรือ amount ในหน่วยบาททศนิยม 2 ตำแหน่ง — เลือกหนึ่งแล้วใช้ตลอด
- แนะนำ: เก็บเป็น integer satang (สตางค์) กันปัญหา floating point แล้ว format เป็นบาทตอนแสดง
- roundHalfUp(baht): number
- formatTHB(amount): string เช่น "฿320.00"
- splitEvenly(totalSatang, n): number[]  // กระจายเศษสตางค์ให้คนแรกๆ

lib/split.ts:
อินพุต: BillState (people, items, assignments, tip, service_charge, tax, split_mode)
เอาต์พุต: SplitResult { per_person: [...], totals: {...} }

ลำดับคำนวณค่าเริ่ม (เอกสารในโค้ดด้วย):
1) food_subtotal = ผลรวม line items
2) service = food_subtotal * service_percent (ถ้าเปิด)
3) vat = (food_subtotal + service) * vat_percent (ถ้าเปิด)  // แบบรวมฐานเซอร์วิส
4) tip = ตาม TipSettings (percent ของ food_subtotal หรือ fixed)
5) grand_total = food_subtotal + service + vat + tip
6) กระจายตาม split_mode:
   - equal: หาร grand_total เท่ากัน
   - by_item: แต่ละคนรับส่วนของเมนูที่ assign (+ หารจานแชร์) แล้วกระจาย service/vat/tip ตามสัดวงเงินอาหารของคนนั้น
   - custom: ใช้ custom_amount ถ้ามี ไม่งั้น fallback by_item

ข้อกำหนด:
- ฟังก์ชันบริสุทธิ์ เทสได้
- ผลต้องตรง split_result_example ใน examples.json
- คอมเมนต์สั้นภาษาอังกฤษในโค้ด
- ไม่พึ่งเซิร์ฟเวอร์
```

---

## F) Prompt Share card / export image

```text
เขียน lib/share.ts + คอมโพเนนต์ ShareCard สำหรับ SplitBill Pro

ต้องได้:
1) รูปการ์ดสรุปแนวตั้งสวย (แนะนำ 1080x1350 หรือ 1080x1920)
   - หัวข้อร้าน + วันที่
   - รายการยอดต่อคนพร้อมอวตาร์สี
   - แถวสรุป: อาหาร / เซอร์วิส / VAT / ทิป / รวม
   - ฟุตเตอร์เล็ก SplitBill Pro · AI วันละแอป
2) ข้อความภาษาไทยสำหรับ LINE ตามเทมเพลตใน examples.json → share_text_line_th
3) API:
   - buildSharePayload(billState, splitResult): SharePayload
   - renderShareCardPng(...): Promise<Blob>
   - copyLineText(text): Promise<void>
   - shareNative(payload): Promise<void>  // navigator.share fallback download/copy
4) ลิงก์ mock: https://splitbill.pro/b/{bill_id}
5) QR ออปชัน (nice): encode ลิงก์ mock

โทนการ์ด: ครีม + teal ตามแบรนด์ อ่านชัดบนมือถือ
ชื่อไฟล์: splitbill-{bill_id_short}-{YYYYMMDD-HHmmss}.png
ข้อความ error UI เป็นภาษาไทย
```

---

## G) Prompt ถ่าย Reel / สคริปต์พูด

```text
เขียนสคริปต์ Reel 30 วินาทีภาษาไทย สำหรับแอป SplitBill Pro
โทนเพื่อนพูด ไม่ขายของแข็ง ไม่พูดคำว่า disruption/ecosystem

โครงเวลา:
0-3s ฮุค สลิป → รายการขึ้น
3-8s บอกว่าสร้างด้วย AI วันนี้
8-14s โชว์สแกน/OCR
14-22s ลากเมนูให้ 3 คน + ทิป
22-28s การ์ดยอด + แชร์ LINE
28-35s CTA ลิงก์ในไบโอ + ให้คอมเมนต์「หาร」

ข้อกำหนด:
- ข้อความบนจอทีละช็อตสั้น ไม่เกิน 8 คำ
- มี voice line ต่อช็อต
- ระบุของใช้ถ่าย: มือถือจริง 1 เครื่อง, สลิปเดโม 1 ใบ, เพื่อนในแอป 3–4 คน
- ส่งออกเป็น JSON ตามคีย์ reel_script_th ใน examples.json ได้ด้วย
```

---

## H) Prompt QA ก่อนลงคลิป

```text
เช็ก SplitBill Pro ก่อนถ่าย Reel สำหรับคลิปวันที่ 2026-09-29

ทดสอบเคส:
1) โหลดสลิปเดโม — รายการครบ ราคาถูก
2) เพิ่มคน 4 คน ลากเมนู + แชร์จานส้มตำ
3) เปิด service 10% + VAT 7% + ทิป 10% — ตัวเลขตรง examples
4) สลับโหมด equal / by_item / custom
5) แชร์รูปการ์ด + คัดลอกข้อความ LINE บนมือถือ
6) (ถ้ามี) อัปโหลดสลิปจริงภาพชัด / ภาพยับ — ต้องไม่แครช อย่างน้อยให้แก้มือได้

เช็กรายการ:
- ยอดต่อคนอัปเดตทันทีหลังลากเมนู
- ไม่มี NaN / undefined บน UI
- ปุ่มใหญ่ใช้นิ้วได้ที่ 390px
- UI ภาษาไทยไม่ตัดคำแปลกๆ
- ไม่มีปุ่มโอนเงิน / PromptPay จริง
- History/Friends ไม่พังถ้า localStorage ว่าง

รายงานเป็นตาราง: เคส | ผล | severity (blocker/major/minor) | วิธีแก้สั้นๆ
สรุปท้ายว่าพร้อมถ่าย Reel หรือยัง พร้อมติ๊ก FeatureChecklist
```

---

## I) Prompt เพิ่ม Friends presets + Settle tracker (nice)

```text
ตอนนี้ SplitBill Pro ทำ happy path ครบ 5 ฟีเจอร์ must แล้ว
ช่วยเพิ่มตามลำดับความคุ้มของคลิป:

1) Friends presets — บันทึกชื่อ+สีอวตาร์ใน localStorage เลือกตอนเปิดบิลใหม่
2) Bill History — สูงสุด 20 บิล เปิดดูสรุปเก่าได้
3) Settle tracker — ติ๊ก person.paid บนหน้า Summary แล้วเซฟในบิล

กติกา:
- อย่าพัง API ของ split/share เดิม
- มือถือใช้นิ้วได้
- อัปเดต FeatureChecklist ใน examples
- ไม่ต้องเพิ่ม auth หรือเพย์เมนต์
```

---

## J) Prompt ซ่อม JSON / validate ตอนรันจริง

```text
มี object BillState / OcrResult / SharePayload จากแอป SplitBill Pro
ตรวจกับ schemas.json (draft 2020-12)
ถ้าไม่ผ่าน: บอกฟิลด์ที่ผิด และคืนค่า object ที่ซ่อมแล้ว
ห้ามแต่งยอดเงินที่ผู้ใช้ตั้งใจ นอกจากต้องใส่ default ที่ขาด
ตอบเป็นภาษาไทยสรุป + บล็อก JSON เต็ม
```

---

## K) Few-shot ข้อความ UI สั้นๆ

**ตอนสแกน:** 「กำลังอ่านสลิป…」  
**สำเร็จ:** 「ได้รายการแล้ว — เพิ่มเพื่อนได้เลย」  
**ลากเมนู:** 「จัดเมนูให้แล้ว」  
**คิดทิป:** 「อัปเดตทิปและเซอร์วิสแล้ว」  
**แชร์:** 「คัดลอกข้อความ LINE แล้ว」  
**ผิดพลาด:** 「อ่านสลิปไม่สำเร็จ ลองถ่ายใหม่หรือพิมพ์รายการเอง」  

(ชุดเต็มอยู่ที่ `examples.json` → `ui_copy_th`)
