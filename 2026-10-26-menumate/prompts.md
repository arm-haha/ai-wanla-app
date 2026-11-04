# Work-order prompts — MenuMate (อ่านเมนูไม่ออก)

ใช้ทีละ prompt กับ AI codegen (Cursor / v0 / Lovable / Bolt). ทุก prompt อ้างอิง `schemas.json`, `examples.json`, และ logic ใน `reference/menumate.py` (คำนวณด้วยโค้ด ไม่ให้ LLM คิดเลข)

---
## P0 — Scaffold + design system
สร้าง mobile-first web app (Next.js + Tailwind + PWA) ชื่อ "MenuMate — อ่านเมนูไม่ออก" UI ภาษาไทย
- สี: washi #FBF8F1 พื้น, sumi #1C1B22 ตัวหนังสือ, torii #E2483D ปุ่มหลัก, matcha #6BAF6B safe, warn #F59E0B, avoid #DC2626, yuzu #F5C542 ป้ายราคาบาท, sky #5BA4E6 ลิงก์
- ฟอนต์ Noto Sans Thai + Noto Sans JP/KR/SC, การ์ดมุมมน 20px เงานุ่ม
- เก็บข้อมูลใน localStorage/IndexedDB (ไม่ต้อง login) ตาม type ใน schemas.json
- โหลด examples.json เป็น "Demo mode" ปุ่มเดียวเห็นทุกฟีเจอร์ (สำหรับถ่าย Reel)
- Routes: /onboarding /home /scan/:id /item/:id /order /point /bill /split /wrapped /phrases /settings

## P1 — Onboarding + UserPrefs + ExchangeRate
3 สเต็ป สวยๆ: (1) ไปประเทศไหน → ตั้ง currency, (2) แพ้อะไร (ชิปเลือกได้หลายอัน) + diet (no_pork/no_beef/halal/vegetarian), (3) เผ็ดได้แค่ไหน (สไลเดอร์ 0–3 พริก)
- Rate: ให้ผู้ใช้กรอกเอง (เริ่มจากค่าล่าสุดที่เคยกรอก) แสดง "อัปเดตล่าสุด" เสมอ; ถ้าต่อ API ได้ให้ source="api"
- Validate ตาม UserPrefs / ExchangeRate

## P2 — Menu Snap → Thai Menu (WOW)
- ปุ่มกล้องใหญ่ + เลือกจากอัลบั้ม, บีบอัดรูป ≤1600px
- ส่งรูปเข้า vision LLM ด้วย system prompt ด้านล่าง ต้องได้ JSON ตาม `MenuScan` เท่านั้น (validate; ถ้าไม่ผ่าน retry 1 ครั้ง แล้วแสดง error สุภาพ)
- Animation: รูปเมนูจริงเบลอเป็นพื้นหลัง → การ์ดไทยเด้งขึ้นทีละใบ (stagger 80ms) พร้อมราคาบาท `to_thb()` และป้าย "เด็ด" ถ้า must_try ≥ 85
- ถ้ามี bbox ให้แตะการ์ดแล้วไฮไลต์ตำแหน่งบนรูปต้นฉบับ

System prompt (vision):
```
You read restaurant menu photos for Thai travelers. Return ONLY JSON matching the MenuScan schema.
For every visible dish line: original_name copied EXACTLY as printed (never re-translate), romanized,
thai_name (natural Thai), thai_desc (≤ 60 Thai chars, what it is + main ingredients), price as a number
in local currency, category, spice_level 0-3, ingredients (lowercase english tags: pork, beef, chicken,
seafood, fish, shrimp, crab, egg, milk, soy, wheat, peanut, sesame, alcohol, lard...), allergens,
must_try 0-100 (how iconic/popular this dish type is), emoji, confidence 0-1 for how sure you are of
the reading. If a line is unreadable, skip it and count it in unreadable_regions. Never invent prices.
If unsure about ingredients, lower confidence instead of guessing.
```

## P3 — Safe-to-Eat Flags
- ใช้ `flag_item(item, prefs)` (port จาก reference) ทุกการ์ดมีป้าย 🟢 กินได้ / 🟡 ระวัง / 🔴 เลี่ยง + เหตุผลภาษาไทย
- ฟิลเตอร์ด้านบน: "เฉพาะที่กินได้", "เด็ด", "ไม่เผ็ด", เรียงตามราคา
- Disclaimer ใต้ทุกป้ายแดง/เหลือง: "AI อาจพลาด ยืนยันกับร้านด้วย Allergy Card"

## P4 — Budget Order Builder
- อินพุต: งบ (สกุลท้องถิ่น พร้อมแสดงบาท), จำนวนคน
- ใช้ `build_order()` → แสดงตะกร้า, total, เหลือเท่าไร, คนละเท่าไร (local + บาท), ถ้า mains_covered=false แจ้ง "งบไม่พอ main ครบทุกคน"
- ผู้ใช้ +/− หรือสลับเมนูเองได้ ตัวเลขอัปเดตสด แถบงบเป็น progress bar สี matcha→warn→avoid

## P5 — Point-to-Order Card
- `point_card(items, order, lang, note)` เต็มจอ พื้นขาว ตัวใหญ่ หมุนจอแนวนอนได้ ชื่อเมนูใช้ original_name เท่านั้น
- ใส่โน้ตแพ้อาหารภาษาท้องถิ่นอัตโนมัติจาก prefs, ปุ่ม 🔊 อ่านออกเสียง (Web Speech TTS ตาม lang)
- ปุ่ม "ร้านเข้าใจแล้ว ✓" → บันทึกมื้อเข้า diary

## P6 — Bill Check + Split
- ถ่ายใบเสร็จ → vision LLM คืน `ReceiptLine[]` (copy ชื่อตามใบเสร็จ, ราคาเป็นตัวเลข)
- `bill_check(order_items, lines, tax_rate, service_rate)` → การ์ดผลลัพธ์: ✅ ตรง / ⚠️ เกิน ¥xxx พร้อมรายชื่อรายการเกิน/ไม่ได้รับ/ราคาไม่ตรง
- ประโยคช่วยถามพนักงาน (เช่น "これは注文していません") ในภาษาท้องถิ่น
- `split_even()` หารต่อคนเป็นบาท + ปุ่มคัดลอกข้อความส่ง LINE

## P7 — Allergy Card + Phrase Pocket
- Allergy Card: สร้างจาก prefs (LLM แปล 1 ครั้ง แล้ว cache) โชว์ภาษาท้องถิ่น + ไทยตัวเล็กด้านล่าง ตาม `AllergyCard`
- Phrase Pocket: 10 ประโยคตาม `Phrase` (ขอน้ำ/ไม่เผ็ด/เช็กบิล/รับบัตรไหม/ไม่ใส่...) ปุ่มเล่นเสียง

## P8 — Diary + Trip Wrapped + Reel cards
- ทุกมื้อเก็บ {city,total_local,items_tried,avoided}; `trip_wrapped()` → การ์ด 9:16 แชร์ได้ (html-to-image)
- ReelCard 4 แบบ (menu_flip / order_win / bill_catch / wrapped) export PNG 1080×1920 ใส่ลายน้ำ "MenuMate · AI วันละแอป"

## P9 — QA
- Port tests จาก reference/tests.py (17 เคส) แล้วต้องผ่านทั้งหมด
- Validate ทุก example ใน examples.json กับ schemas.json
- ทดสอบ: รูปมืด/เอียง, เมนูไม่มีราคา, rate=0 (ต้อง error), งบน้อยกว่าเมนูถูกสุด, ภาษาเกาหลี/จีน
