# SlipBook — Prompt สั่งงาน (จัดเต็ม)

ใช้กับ AI codegen (Cursor / Claude / GPT) สร้างแอปทั้งก้อน + prompt ที่ใช้ "ข้างในแอป" ตอนเรียก LLM จริง

**วันที่แพ็ก:** 2026-10-08 (Asia/Bangkok) · Day 9/10 · AI วันละแอป
**เอกสารคู่กัน:** `prd.md`, `schemas.json`, `examples.json`, `reference/slip.py`

| ส่วน | ใช้ทำอะไร |
|---|---|
| A | Master prompt สร้างทั้งแอป |
| B | ข้อมูลตัวอย่าง "ต้นกล้า" (18 สลิป + ประวัติ ส.ค.–ก.ย.) |
| C | TypeScript types + zod |
| D | `lib/parse.ts` อ่านสลิปไทย (หัวใจคลิป) |
| E | `lib/categorize.ts` + `lib/money.ts` + `lib/recurring.ts` |
| F | Slip Drop + OCR worker + Importing animation + Review Sheet |
| G | Month Dashboard + Ledger |
| H | Budget Jars + ใช้ได้อีกวันละ + Recurring |
| I | Money Wrapped + Share Card |
| J | Nice-to-have pack |
| K | QA ก่อนถ่าย |
| L | แก้ปัญหาเร็ว |
| M | Runtime prompts (ที่แอปส่งให้ LLM) |
| N | Reel overlay / แคปชัน |

---

## A) Master prompt สร้างทั้งแอป (วางครั้งเดียว)

```text
สร้างเว็บแอปมือถือเป็นหลักชื่อ SlipBook (UI ภาษาไทยก่อน) — เปลี่ยนสลิปโอนเงินในแกลเลอรี่ให้เป็นบัญชีรายจ่าย

วันที่ส่งมอบคอนเทนต์: 2026-10-08 สำหรับช่อง "AI วันละแอป"
เป้าหมายผู้ใช้: เลือกสลิปหลายใบครั้งเดียว → ภายใน ~3 วิ ได้รายการบัญชีครบ (ยอด วันเวลา ผู้รับ หมวด) ข้ามสลิปซ้ำ
→ แดชบอร์ดว่าเงินไหลไปไหน → งบรายหมวด + "ใช้ได้อีกวันละ ฿x" → อะไรตัดเงินทุกเดือน → Wrapped สรุปเดือนไว้แชร์

สแต็กบังคับ:
- Next.js 14 App Router + TypeScript + Tailwind CSS + shadcn/ui + framer-motion · PWA · Deploy Vercel · ไม่มี auth ไม่มี DB
- lib/parse.ts pure deterministic (vitest) ตาม prd.md §8 — ต้องให้ผลตรง examples.json → parsed_slips ทุกช่อง
  (ต้นฉบับอ้างอิงคือ reference/slip.py → parse_slip)
- lib/categorize.ts (กฎ examples.json → category_rules ตามลำดับ + merchant memory + ชื่อคน) · lib/money.ts (dashboard,
  heat, budget, safe_per_day) · lib/recurring.ts · lib/wrapped.ts — pure ทั้งหมด ตาม prd.md §9
- lib/ocr.ts: tesseract.js v5 ภาษา "tha+eng" ใน Web Worker, คิวพร้อมกัน 2 งาน, ย่อรูปด้านยาว 1600px + grayscale ก่อน OCR,
  preload ตอนเปิดแอป · โหมดเดโมข้าม OCR ใช้ ocr_text จาก fixture
- /api/ai/parse และ /api/ai/wrapped (server, env AI_API_KEY) ใช้เฉพาะเมื่อผู้ใช้เปิดใน Settings — ไม่มี key แอปใช้ได้ครบ
- lib/storage.ts: IndexedDB (idb) stores txns, imports + localStorage "slipbook:v1" ตาม LocalStore · ห้ามเก็บรูปสลิป
- lib/share.ts: html-to-image → PNG 1080x1920 / 1080x1080 + navigator.share({files}) + fallback ดาวน์โหลด

ต้องมีอย่างน้อย 5 ฟีเจอร์ must-have:
1) Slip Drop → Auto Book — ปุ่มใหญ่เลือกหลายรูป + ลากวาง → หน้า Importing: การ์ดสลิป (ใบเสร็จขาวขอบหยัก ไม่ใช่หน้าตา
   สลิปธนาคารจริง) บินเข้ากองทีละใบ + "กำลังอ่าน 12/18" + ตัวนับยอดวิ่ง → Import Result "เพิ่ม 17 · ข้ามสลิปซ้ำ 1 · รอเช็ก 2"
   แถว duplicate สีเทา, needs_review สีเหลือง · กันซ้ำด้วย dedupe_key ทั้งในชุดและกับของเดิม · ปิดเลขบัญชี
2) Smart Category + Merchant Memory — ชิป "{ชื่อ} คือใคร?" ตัวเลือก ครอบครัว/เพื่อน/อื่นๆ + สวิตช์ "จำไว้ ครั้งหน้าจัดให้เลย"
   แก้หมวดได้ทุกรายการ (bottom sheet) · memory ชนะกฎเสมอ
3) Month Dashboard — ยอดรวมตัวใหญ่นับขึ้น + โดนัทหมวดหมู่ (แตะดูรายการ) + ปฏิทินความร้อน 5 ระดับ (เริ่มวันจันทร์)
   + ท็อป 5 ผู้รับ + การ์ดเงินเข้าแยก · เลือกเดือนได้
4) Budget Jars — โหลแก้ว SVG เติมน้ำตาม % (ok เขียว / warn เหลือง ≥80% / over แดง + navigator.vibrate(30))
   + ตัวเลขใหญ่ "ใช้ได้อีกวันละ ฿563" + หน้าตั้งงบ (ค่าเริ่มจาก examples.json → budgets)
5) Money Wrapped + Share Card — สไลด์สตอรี่ 6 หน้า (แตะซ้าย/ขวา, progress bar บนสุด) → การ์ด wrapped_story / donut_square
   สวิตช์ "ซ่อนตัวเลขเงิน" · ห้ามมีชื่อคน เลขอ้างอิง เลขบัญชีบนการ์ด

Nice-to-have ทำถ้าเหลือเวลา (ตามลำดับ): หน้า "ตัดเงินทุกเดือน" (lib/recurring.ts), ค้นหา/กรอง Ledger, เพิ่มเงินสดด้วยมือ,
ส่งออก CSV, เตือน 21:00, ล็อก PIN + ลบข้อมูลทั้งหมด

ปุ่ม「ลองข้อมูลตัวอย่าง (ต้นกล้า)」: ใส่ ledger รายการที่ slip_id = null (ประวัติ ส.ค.–ก.ย. 34 รายการ) + merchant_memory_before
+ budgets + settings_example ลง storage → แล้วเล่น Importing ด้วย slips_raw 18 ใบ (ใช้ ocr_text แทน OCR, หน่วง 120ms/ใบ)
→ ผลต้องได้ 17 / 1 / 2 · เงินออก ฿6,584.50 · เงินเข้า ฿150 ทุกครั้ง · วันนี้ของเดโม = 2026-10-08 (ตรึงไว้ในโหมดเดโม)

หน้าจอ (prd.md §11): Home/Drop, Importing, Import Result, Review Sheet, Dashboard, Ledger, Budget, Recurring, Wrapped,
Share, Settings · bottom nav: สลิป | ภาพรวม | งบ | สรุป + ไอคอนตั้งค่ามุมขวาบน

แบรนด์: พื้น #F4FBF7 · การ์ด #FFFFFF · ตัวอักษร #0B1F17 · รอง #5B6B63 · หลัก #059669 · หลักเข้ม #047857 · เหลืองสลิป #FDE68A
· เตือน #F59E0B · เกิน #F43F5E · สีหมวดจาก examples.json → categories · ฟอนต์ Kanit 600 (หัวข้อ) + IBM Plex Sans Thai
(ตัวเลข tabular-nums) · มุมโค้ง 20px · เงานุ่ม · ปุ่มหลักสูง 56px

ความเป็นส่วนตัว: ป้ายบน Home "อ่านสลิปในเครื่อง · ไม่เก็บรูป · ปิดเลขบัญชีให้อัตโนมัติ" · disclaimer ใต้แดชบอร์ด
"SlipBook ช่วยจดรายจ่ายจากสลิป ไม่ได้ตรวจสอบว่าสลิปจริงหรือปลอม และไม่เชื่อมบัญชีธนาคาร"

ข้อความ UI ใช้ examples.json → ui_copy_th · ทุก object ต้องผ่าน zod ที่แปลงจาก schemas.json

ส่งมอบ: โค้ดครบ, README วิธีรัน, vitest ผ่าน test_vectors ทั้ง 13, npm run build ผ่าน, Lighthouse PWA ผ่าน
ทำ happy path ด้วยข้อมูลเดโมให้จบก่อน แล้วค่อยต่อ OCR จริง/AI
```

---

## B) ข้อมูลตัวอย่าง "ต้นกล้า"

```text
โหลด examples.json แล้วสร้าง lib/demo.ts:
- DEMO_TODAY = "2026-10-08"
- seedHistory(): ใส่ ledger.filter(t => t.slip_id === null) (34 รายการ ส.ค.–ก.ย.) ลง IndexedDB txns
- seedSettings(): settings_example, budgets, merchant_memory_before
- demoSlips(): slips_raw (18 ใบ) → ใช้ ocr_text ตรงๆ แทน OCR
- หลัง import เสร็จ ผลต้องเท่ากับ import_batch_example และ ledger ทั้ง 51 รายการ (34 + 17) ตรงกับ examples.json → ledger
  ยกเว้น s07 ที่ category_source จะเป็น "person_default" จนกว่าผู้ใช้แตะยืนยัน (หลังยืนยัน = "user" ตาม ledger)
- ปุ่ม "รีเซ็ตเดโม" ล้างแล้วเริ่มใหม่ได้ทุกเทค
ชื่อทั้งหมดเป็นตัวละครสมมติ เลขบัญชี/เลขอ้างอิงแต่งขึ้น
```

## C) TypeScript types + zod

```text
แปลง schemas.json ($defs ทั้ง 41 ตัว) เป็น lib/types.ts (TypeScript) + lib/schemas.ts (zod) ชื่อตรงกัน
- Money = number ≥ 0 ทศนิยม 2 ตำแหน่ง (เก็บเป็น number แต่คำนวณผลรวมด้วย satang integer แล้วหาร 100 เพื่อกันทศนิยมเพี้ยน)
- MaskedAccount ต้อง reject เลขบัญชีเต็ม (เช่น "1234567890")
- เขียนเทสต์: ทุก section ใน examples.json parse ผ่าน zod
```

## D) `lib/parse.ts` (หัวใจคลิป)

```text
เขียน lib/parse.ts ให้ผลตรงกับ reference/slip.py → parse_slip ทุกกรณี (พอร์ตทีละบรรทัดได้เลย)

export function parseSlip(ocrText: string, ownerNames: string[]): ParsedFields
ลำดับ:
1) amount: ลอง regex 3 ตัวตามลำดับ (prd.md §8 ข้อ 1) ตัดคอมมา → number
2) date: ไทยย่อ (ม.ค.–ธ.ค.) → อังกฤษ (Jan–Dec) → d/m/y · ปี 2 หลัก ≥50 → +2500 (พ.ศ.) ไม่งั้น +2000 · >2400 → −543
   คืน "YYYY-MM-DD"
3) time: ตัวแรก HH:MM(:SS)? → "HH:MM"
4) ref: หลัง label (รหัสอ้างอิง|เลขที่รายการ|หมายเลขอ้างอิง|Ref No.|Transaction ID) [A-Za-z0-9]{8,30}
5) direction: "in" ถ้ามี รับเงิน|เงินเข้า|ได้รับเงิน|Received หรือบรรทัด ไปยัง/ถึง/ผู้รับ/To มีชื่อใน ownerNames
6) counterparty: บรรทัดหลัง ไปยัง/ถึง/ผู้รับ/To (out) หรือ จาก/ผู้โอน/From (in) · ตัดเลขบัญชีที่ขึ้นต้นด้วย x/X/* ออกไปเป็น
   counterparty_account_masked
7) bank จากคำใบ้ (BANK_HINTS) · confidence ถ่วงน้ำหนัก amount .35 date .2 time .1 ref .2 counterparty .15 (ปัด 2 ตำแหน่ง)
8) missing = ฟิลด์ที่เป็น null

export function dedupeKey(p): "ref:"+ref หรือ `fp:${date}|${time}|${amount.toFixed(2)}|${normKey(counterparty)}`
export function normKey(s) = trim + lowercase + ช่องว่างหลายตัว → ตัวเดียว

เทสต์ vitest: วนทุก slips_raw → parseSlip(ocr_text, ["ต้นกล้า"]) ต้องเท่ากับ parsed_slips (ฟิลด์ amount date time ref
counterparty counterparty_account_masked direction bank parse_confidence missing_fields dedupe_key)
+ เทสต์เพิ่ม: "฿ 12,345.00", "Amount: THB 99.50", "15/09/26 07:01" (ค.ศ. 2026), ข้อความที่ไม่ใช่สลิป → amount null
ห้ามเดาค่า: ไม่เจอ = null
```

## E) `lib/categorize.ts` + `lib/money.ts` + `lib/recurring.ts`

```text
1) categorize(counterparty, direction, memory) → {category, source, confidence}
   in → income/direction/1 · memory[normKey] → memory/1 · กฎ category_rules ตามลำดับ (contains, lowercase) → rule/0.9
   · ขึ้นต้น นาย|นาง|น.ส.|นางสาว|ด.ช.|ด.ญ.|คุณ|MR|MRS|MS → friends/person_default/0.5 · ไม่งั้น other/fallback/0.3
   status needs_review ถ้า parse_confidence < 0.85 (missing_fields) หรือ confidence หมวด < 0.6 (who_is_this) · duplicate ไม่มี reason
2) dashboard(txns, "YYYY-MM") ตาม Dashboard schema · percent ปัด 1 ตำแหน่ง · เรียงยอดมาก→น้อย แล้วตาม key
   heat(amount, maxOfMonth) 0–4 ตาม prd.md §9
3) budgetStatus(dashboard, budgets, today) · round = Math.floor(x + 0.5) · state over/warn(≥80)/ok
   safe_per_day = round(left_total / (days_in_month − day + 1)) ถ้า left > 0 ไม่งั้น 0
4) recurring(txns): หมวด ∈ {subscription,bills,health,fun,other}, out, ผู้รับเดิม, เดือนละ 1 ครั้งพอดี, ≥ 2 เดือน,
   ทุกยอดต่างจากยอดแรก ≤ 5% → yearly = amount × 12 · เรียงยอดมาก→น้อย
5) wrapped(txns, "YYYY-MM") → 6 สไลด์ตาม wrapped_sep (favorite = ผู้รับที่ถี่สุด, เทียบ "≈ ข้าวมันไก่ floor(ยอด/60) จาน")
เทสต์: dashboard_oct, dashboard_sep, budget_status_oct, subscriptions, wrapped_sep ต้องเท่ากับ examples.json ทุกตัวเลข
(ต.ค. ฿6,584.50 / 16 · ฿563/วัน · ฿10,776/ปี · ก.ย. ฿10,533 / 31)
```

## F) Slip Drop + OCR worker + Importing + Review Sheet

```text
Home: หัว "สลิปเต็มแกลเลอรี่?" รอง "โยนเข้ามาเลย เดี๋ยวทำบัญชีให้" · กองการ์ดสลิป 3 ใบลอยเอียงเบาๆ (framer-motion, loop)
ปุ่มหลัก 56px "เลือกสลิปจากแกลเลอรี่" (<input type=file multiple accept="image/*">) + โซนลากวางบนเดสก์ท็อป
+ ปุ่มรอง "ลองข้อมูลตัวอย่าง (ต้นกล้า)" + ป้ายความเป็นส่วนตัว

ครั้งแรก: ถาม "ชื่อคุณบนสลิปคือ?" (เก็บ settings.owner_names) ก่อน import

lib/ocr.ts:
- createWorker('tha+eng') ครั้งเดียว preload ตอนแอปเปิด (แถบ "กำลังเตรียมตัวอ่านสลิป…" ถ้ายังไม่พร้อม)
- ก่อน OCR: วาดลง OffscreenCanvas ย่อด้านยาว 1600px, grayscale, เพิ่ม contrast 1.2
- คิวพร้อมกัน 2 · onProgress(done,total) · ปล่อย objectURL ทันที ไม่เก็บรูป
- ถ้า settings.ai_parse = "fallback" และ confidence < 0.85 → ส่ง ocr_text (ปิดเลขบัญชีแล้ว) ไป /api/ai/parse (Prompt M1)

Importing: การ์ดสลิปบินจากล่างเข้ากองกลางจอทีละใบ (stagger 120ms), ตัวนับ "กำลังอ่าน {done}/{total} สลิป…",
ยอดรวมนับขึ้น (useSpring) · จบ → กองแตกออกเป็นแถวรายการ (layoutId) → Import Result

Import Result: แถบสรุป "เพิ่ม 17 · ข้ามสลิปซ้ำ 1 · รอเช็ก 2" · รายการกลุ่มตามวัน: ไอคอนหมวด, ผู้รับ, เวลา, ยอด (เงินเข้าสีเขียว +)
ชิปเทา "สลิปซ้ำ — ข้ามให้แล้ว" · ชิปเหลือง "อ่านไม่ครบ ช่วยเช็กหน่อย" / "{ชื่อ} คือใคร?"
Review Sheet (shadcn Sheet): แก้ยอด วัน เวลา ผู้รับ หมวด (grid ไอคอน 11 หมวด) + โน้ต + สวิตช์ "จำไว้ ครั้งหน้าจัดให้เลย"
→ บันทึก memory[normKey(ชื่อ)] และอัปเดตทุกรายการเดิมของชื่อนั้นที่ source ≠ user
analytics: import_started / import_completed / category_corrected
```

## G) Month Dashboard + Ledger

```text
Dashboard (แท็บ "ภาพรวม"):
- หัว "{เดือน} เงินไหลไปไหน?" + ตัวเลือกเดือน ‹ ต.ค. 2026 ›
- ยอดใช้รวมตัวใหญ่ 48px นับขึ้น + "{n} รายการ" + การ์ดเล็ก "เงินเข้า +฿150"
- โดนัท (SVG) สีตามหมวด ตรงกลางแสดงหมวดอันดับ 1 + % · legend เรียงยอด · แตะชิ้น → Ledger กรองหมวดนั้น
  animation: ชิ้นกวาดเข้าทีละชิ้น 600ms
- ปฏิทินความร้อน: grid 7 คอลัมน์ เริ่มจันทร์ · สีเขียว 5 ระดับ (#ECFDF5 → #047857) ตาม heat · แตะวัน → รายการวันนั้น
- ท็อป 5 ผู้รับ (ชื่อ, ครั้ง, ยอด) · disclaimer ตัวเล็กด้านล่าง
Ledger: รายการทั้งเดือนกลุ่มตามวัน (sticky header วันที่ไทย "พ. 8 ต.ค.") + ช่องค้นหา + ชิปกรองหมวด + ปัดซ้ายลบ (ยืนยัน)
ตัวเลขเงินทุกที่: Intl.NumberFormat('th-TH', {style:'currency', currency:'THB'}) + tabular-nums
```

## H) Budget Jars + ใช้ได้อีกวันละ + Recurring

```text
Budget (แท็บ "งบ"):
- การ์ดบนสุด: "ใช้ได้อีกวันละ" + ตัวเลขใหญ่ ฿563 + "เหลือ ฿13,515.50 · อีก 24 วัน" · ถ้า left ≤ 0 → การ์ดแดง "เกินงบรวมแล้ว ฿x"
- grid โหลแก้ว 2 คอลัมน์ (SVG: ฝา + ตัวโหล + น้ำ path คลื่นขยับเบาๆ) ระดับน้ำ = min(percent,100)%
  สี ok #059669 / warn #F59E0B / over #F43F5E · ใต้โหล "ใช้ ฿x / ฿งบ" · over สั่น 30ms ครั้งเดียวต่อวัน
- ปุ่ม "ตั้งงบ" → sheet slider ต่อหมวด + ปุ่ม "ใช้ค่าแนะนำ" (examples.json → budgets) · บันทึก analytics budget_set
Recurring (เข้าจากการ์ดใน Budget): "ตัดเงินทุกเดือน" รายการ: ผู้รับ, ฿/เดือน, ตัดราววันที่ {day_of_month}, ฿/ปี
ตัวเลขรวมใหญ่ "ปีละ ฿10,776" + ข้อความ "ยังใช้ครบทุกอันไหม?"
```

## I) Money Wrapped + Share Card

```text
Wrapped (แท็บ "สรุป"): เลือกเดือนที่จบแล้ว (ค่าเริ่มเดือนก่อน) → สไลด์ 6 หน้าเต็มจอ แตะซ้าย/ขวา progress bar บนสุด
พื้นไล่สีต่อหน้า (มิ้นต์ → เหลือง → ส้ม → ชมพู → ฟ้า → ม่วง) ตัวเลขนับขึ้น · ข้อความจาก wrapped_sep.slides
(ถ้าเปิด AI: ขอ headline ขำๆ จาก Prompt M3 แต่ตัวเลขใช้จาก lib/wrapped.ts เท่านั้น)
หน้า 6 จบด้วยปุ่ม "แชร์การ์ด"
Share: พรีวิว 2 แบบ (wrapped_story 1080x1920, donut_square 1080x1080) · สวิตช์ "ซ่อนตัวเลขเงิน" (แทนด้วย %/•••)
footer "ทำบัญชีจากสลิปใน 10 วิ · SlipBook" · ห้ามมีชื่อคน/เลขอ้างอิง/เลขบัญชี (เทสต์ด้วย snapshot)
html-to-image pixelRatio 2 → navigator.share({files:[png]}) → fallback ดาวน์โหลด · analytics share_card_exported
```

## J) Nice-to-have pack

```text
ทำทีละข้อ commit แยก:
1) ค้นหา Ledger: พิมพ์ชื่อ/หมวด/ยอด → ผลรวม "Café Amazon · 11 ครั้ง · ฿715" (ช่วง 1 ก.ย.–8 ต.ค. ในเดโม)
2) เพิ่มเงินสดด้วยมือ: FAB "+" → ยอด (numpad ใหญ่) → หมวด → บันทึก source "manual"
3) ส่งออก CSV: date,time,counterparty,amount,direction,category,note (UTF-8 BOM ให้ Excel อ่านไทยได้)
4) เตือน 21:00 "วันนี้มีสลิปใหม่ไหม โยนเข้ามาเลย" (Notification API ขณะแอปติดตั้งเป็น PWA)
5) ล็อก PIN 4 หลัก + ปุ่มลบข้อมูลทั้งหมด (ยืนยัน 2 ชั้น)
6) ปุ่ม "หารบิลกับเพื่อน" บนรายการ → เปิดลิงก์ SplitBill Pro พร้อมยอด (query string)
7) self-transfer: ถ้า "จาก" และ "ไปยัง" เป็นชื่อเจ้าของทั้งคู่ → แท็ก transfer_self ไม่นับในแดชบอร์ด
```

## K) QA ก่อนถ่าย

```text
ตรวจทั้งหมดแล้วรายงานเป็นตาราง ผ่าน/ไม่ผ่าน:
1) vitest ผ่าน test_vectors 13 ข้อ + parsed_slips ครบ 18
2) เดโม 5 รอบติด: 17/1/2, ฿6,584.50, +฿150, ฿563/วัน, ฿10,776/ปี, Wrapped ก.ย. ฿10,533 — เหมือนกันทุกรอบ ≤ 3 วิ
3) แตะ "แพรวา ส. คือใคร?" → เพื่อน + จำไว้ → import ชุดใหม่ที่มีชื่อนี้ → จัดหมวดเอง source memory
4) import ชุดเดิมซ้ำทั้งชุด → เพิ่ม 0 ข้ามซ้ำ 18
5) IndexedDB ไม่มี Blob รูป · ค้นทั้ง storage ไม่เจอเลขบัญชีเต็ม · การ์ดแชร์ไม่มีชื่อคน
6) สลิปจริงของทีม 3 ธนาคาร: ยอด + วันที่ถูก (ถ้าผิดบันทึก ocr_text ไว้ทำ fixture เพิ่ม)
7) iPhone Safari + Android Chrome: เลือกหลายรูปได้, share sheet ทำงาน, ฟอนต์ไทยไม่เพี้ยน, ตัวเลขไม่ล้นจอ 360px
8) ไม่มี AI_API_KEY → ไม่มี error ใน console · ปิดเน็ตหลังโหลด OCR แล้วยังอ่านสลิปได้
9) disclaimer "ไม่ตรวจสลิปปลอม" อยู่ใต้แดชบอร์ดและใน Settings
```

## L) แก้ปัญหาเร็ว (ใช้เมื่อพัง)

```text
- OCR ไทยได้ตัวอักษรแตก: ใช้ traineddata "tha" แบบ best, ขยายรูปเป็นด้านยาว 2000px, threshold ขาวดำ, ตั้ง PSM 6
- เลข 8 กลายเป็น 3 / , กลายเป็น . : regex ยอมรับช่องว่างในตัวเลข แล้ว confidence ต่ำ → ถาม · เปิดโหมด AI fallback
- วันที่ผิดปี (2569 กลายเป็น 3112): ตรวจ _year ตาม prd.md §8 ข้อ 2 · เทสต์ "69", "2569", "26", "2026"
- โดนัทเปอร์เซ็นต์รวมไม่ถึง 100: ปกติจากการปัด แสดงตามจริง อย่าบังคับปัด
- ผลรวมทศนิยมเพี้ยน (6584.499999): รวมเป็นสตางค์ (Math.round(x*100)) แล้วหาร 100
- html-to-image ฟอนต์หาย: preload ฟอนต์ + await document.fonts.ready ก่อน toPng
- iOS เลือกได้ทีละรูป: ตรวจว่ามี attribute multiple และไม่ได้ใส่ capture
```

## M) Runtime prompts (ที่แอปส่งให้ LLM)

### M1 — แยกสลิปจากข้อความ OCR (ใช้เฉพาะ confidence < 0.85)

```text
SYSTEM: คุณคือตัวแยกข้อมูลสลิปโอนเงินภาษาไทย ตอบเป็น JSON ตาม schema AiParseResponse เท่านั้น
กติกา:
- ใช้เฉพาะข้อมูลที่เห็นในข้อความ ห้ามเดาหรือเติมตัวเลข ถ้าไม่แน่ใจให้เป็น null และลด confidence
- amount เป็นตัวเลข THB ทศนิยม 2 ตำแหน่ง (ตัดคอมมา) · date "YYYY-MM-DD" ค.ศ. (แปลง พ.ศ. −543) · time "HH:MM"
- direction = "in" ถ้าผู้รับเป็นชื่อใน owner_names หรือมีคำว่า รับเงิน/เงินเข้า ไม่งั้น "out"
- counterparty ห้ามใส่เลขบัญชี · ถ้าข้อความไม่ใช่สลิปโอน/จ่ายเงิน is_slip = false
- notes_th บอกสั้นๆ ว่าฟิลด์ไหนไม่ชัด
USER: {"ocr_text": "<ข้อความ OCR ที่ปิดเลขบัญชีแล้ว>", "owner_names": ["ต้นกล้า"], "image_attached": false}
```
หลังได้ผล: validate zod → ถ้าไม่ผ่านหรือ amount ไม่ตรงกับตัวเลขใดในข้อความ OCR → ทิ้งผล AI ใช้ผล regex + ถามผู้ใช้

### M2 — เดาหมวดชื่อร้านที่ไม่รู้จัก (ทางเลือก)

```text
SYSTEM: จัดหมวดรายจ่ายจากชื่อผู้รับเงินภาษาไทย/อังกฤษ เลือก 1 ใน: food, cafe, transport, shopping, bills, subscription,
family, friends, health, fun, other · ตอบ JSON {category, confidence 0–1, reason_th ≤ 15 คำ}
ถ้าเป็นชื่อบุคคลให้ตอบ friends confidence ≤ 0.5 (แอปจะถามผู้ใช้เอง) · ไม่แน่ใจตอบ other
USER: {"counterparty": "ร้านป้าศรี ข้าวแกง"}
```
ผลจาก AI ใช้เป็นแค่ข้อเสนอ (source "ai") — memory และกฎในเครื่องชนะเสมอ

### M3 — Wrapped headline ขำๆ (ตัวเลขห้ามแตะ)

```text
SYSTEM: เขียนข้อความสรุปเดือนแบบเพื่อนแซวกันขำๆ ภาษาไทย สุภาพ ไม่ตำหนิ ไม่ให้คำแนะนำการลงทุน
ใช้ตัวเลขจาก input เท่านั้น ห้ามคำนวณหรือสร้างตัวเลขใหม่ · ตอบ JSON AiWrappedLines {headline_th ≤ 12 คำ, lines_th 3–5 บรรทัด ≤ 14 คำ, tip_th 1 บรรทัด}
ห้ามใส่ชื่อบุคคล (ชื่อร้านใส่ได้)
USER: <wrapped_sep ที่ลบ counterparty ที่เป็นชื่อคนออกแล้ว>
```
หลังได้ผล: ตรวจว่าทุกตัวเลขในข้อความมีอยู่ใน input — ถ้ามีตัวเลขแปลกปลอม ใช้ข้อความ template แทน

## N) Reel overlay / แคปชัน

```text
ข้อความบนจอ (ตาม examples.json → reel_script_th):
0–3s  "สลิปเต็มเครื่อง แต่ไม่รู้เงินหายไปไหน 😵"
3–7s  "ให้ AI เขียนแอปให้ 1 วัน"
7–13s "18 สลิป → บัญชีใน 3 วิ · ข้ามสลิปซ้ำ 1"
13–17s "ต.ค. ใช้ไป ฿6,585 · 🏠 ครอบครัว 45.6%"
17–21s "สอนครั้งเดียว ครั้งหน้าจัดให้เอง"
21–25s "ใช้ได้อีกวันละ ฿563"
25–28s "ตัดทุกเดือน ปีละ ฿10,776 😳"
28–30s "คอมเมนต์「สลิป」รับลิงก์ฟรี"

แคปชัน: สลิปโอนเงินเต็มแกลเลอรี่แต่ไม่เคยจดบัญชี? วันนี้แจก SlipBook จากช่อง AI วันละแอป เลือกสลิปทีเดียวทั้งกอง
แอปอ่านยอด แยกหมวด ข้ามสลิปซ้ำ บอกว่าเงินไหลไปไหน เหลือใช้ได้วันละเท่าไหร่ อะไรตัดเงินทุกเดือน แล้วสรุปเป็นการ์ดไว้แชร์
อ่านในเครื่อง ไม่เก็บรูป คอมเมนต์ "สลิป" รับลิงก์ฟรี
(ข้อมูลในคลิปเป็นตัวอย่างสมมติ · แอปไม่ได้ตรวจสลิปปลอม)

กฎอัดหน้าจอ: ใช้โหมดเดโมเท่านั้น · ซ่อน status bar/แจ้งเตือน · ความละเอียด 1080x1920 60fps · เร่งความเร็ว Importing ไม่ได้
(มันเร็วอยู่แล้ว) แต่ตัด Review Sheet ให้เหลือ 3 วิ
```
