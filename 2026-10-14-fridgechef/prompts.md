# FridgeChef — Prompt สั่งงาน (จัดเต็ม)

ใช้คู่กับ `prd.md` · `schemas.json` · `examples.json` · `reference/fridge.py`
สแต็ก: Next.js 14 App Router + TypeScript + Tailwind + shadcn/ui + framer-motion + PWA + Vercel
สี: bg `#F7FAFC` · ink `#0F172A` · ice `#38BDF8` · tomato `#EF4444` · basil `#22C55E` · yolk `#FBBF24`
คอร์ต้อง deterministic ตาม `reference/fridge.py` — AI เป็นตัวเสริมเท่านั้น

ตัวเลขเดโมที่ล็อก (ตู้เย็นปุ๊ก 2026-10-14):
- 13 detections → confirmed 12, "มะนาว ใช่ไหม?" 0.41
- Top3 `kaprao_moo_kai_dao 138` · `khao_pad_sausage 137` · `khao_tom_moo 134`
- ช่วยของ ฿60 · Cook Mode 6 ขั้น 450 วิ · ลิสต์ ~฿80 · dice → `khai_jiao_moo_sap` · Wrapped 9/12/฿225/3

---

## A) Master prompt สร้างทั้งแอป (วางครั้งเดียว)
```
คุณเป็น senior full-stack ที่จะสร้างแอป FridgeChef (ตู้เย็นเชฟ) ตาม PRD ที่แนบ

เป้าหมาย: mini suite "ถ่ายตู้เย็น → รู้ว่าทำเมนูไหนได้" สำหรับคนไทยทั่วไป
ภาษา UI ไทยเป็นหลัก (ดู examples.json → ui_copy_th)

สแต็กบังคับ:
- Next.js 14 App Router + TypeScript + Tailwind + shadcn/ui + framer-motion
- PWA (manifest, icons, SW) deploy Vercel · mobile-first 390px
- local-first: localStorage key "fridgechef:v1" ตาม schema LocalStore · ไม่มีล็อกอิน
- html-to-image สำหรับการ์ดแชร์ · Screen Wake Lock ใน Cook Mode
- optional AI: /api/ai/vision, /api/ai/recipes อ่าน process.env.AI_API_KEY
  ไม่มี key → แอปใช้ได้ 100% ผ่านโหมดพิมพ์ + เดโม

สี (ห้ามเปลี่ยน): --bg #F7FAFC --ink #0F172A --ice #38BDF8 --tomato #EF4444 --basil #22C55E --yolk #FBBF24

Must-have 5 ฟีเจอร์ (ทำให้จบก่อน):
1) Fridge Snap → Ingredient Chips (wow: กรอบสแกนวิ่ง + chips เด้งลงถาด)
2) Menu Match 3 เมนู (+ฟิลเตอร์ ไม่เผ็ด/ไม่กินหมู/มังสวิรัติ/เวลา)
3) Cook Mode (ขั้นละจอ + จับเวลา + Wake Lock)
4) Use-First Radar (วงแหวนสี today/soon/ok/check)
5) ลิสต์ซื้อของแยกร้าน + ส่ง LINE

Nice-to-have: Dice สุ่มเมนู, Waste Wrapped, Staples settings, Share cards, โหมดพิมพ์แทนถ่าย

คอร์ deterministic — พอร์ต reference/fridge.py เป็น lib/fridge.ts ทีละฟังก์ชัน:
expiryStatus, buildInventory, usableKeys, rescueBonus, matchRecipe, menuMatch,
cookMode, cookProgress, useFirstRadar, shoppingList, menuDice, cookLogEntry, wasteWrapped
ข้อมูล CATALOG / RECIPES / STAPLES คัดจาก examples.json (catalog, recipes, staples)

เดโม: ปุ่ม "ลองข้อมูลตัวอย่าง (ตู้เย็นปุ๊ก)" ใช้ examples.json → demo_input
และ today = "2026-10-14" ตายตัว ผลต้องตรง expect_locked ทุกครั้ง

ห้าม: บอกว่าอาหาร "ปลอดภัย", เก็บรูปบนเซิร์ฟเวอร์, บังคับล็อกอิน, สุ่มแบบไม่มี seed
ส่งมอบ: โค้ดครบ, README รันได้, vitest ครอบ test_vectors ทั้งหมดใน examples.json
ทำตามลำดับ Prompt B → J ที่จะส่งต่อไป เริ่มจากโครงโปรเจกต์ + types ก่อน
```

## B) Types + คอร์ logic + tests
```
สร้าง types/fridge.ts จาก schemas.json ($defs: Detection, InventoryItem, Recipe, MenuMatch,
MenuFilters, CookMode, CookProgress, Radar, ShoppingList, DiceResult, CookLogEntry, Wrapped,
ShareCard, Settings, LocalStore) แล้วเขียน lib/fridge.ts พอร์ตจาก reference/fridge.py
- วันที่คำนวณเป็นวันล้วน (ไม่ใช้ timezone shift) → แปลง "YYYY-MM-DD" เป็น UTC midnight แล้วลบกัน
- round แบบ Python round() ใช้ banker's rounding — ในชุดเดโมไม่มีค่า .5 แต่เขียน helper pyRound ให้ตรง
- menuDice ใช้ LCG 32-bit: x = (Math.imul(1664525, x) + 1013904223) >>> 0
เขียน __tests__/fridge.test.ts ให้ครอบ examples.json → test_vectors (16 ข้อ) + expect_locked ทุก key
```

## C) Scan + Chips + เดโม
```
ทำหน้า /scan:
- input capture="environment" + อัปโหลดรูป · ย่อรูปฝั่ง client ≤1MB
- ถ้ามี AI key → POST /api/ai/vision ; ไม่มี → ใช้ demo_input.detections เมื่อเป็นรูปเดโม
  หรือเปิดโหมดพิมพ์ ("ไข่ หมูสับ กะเพรา" → map คำไทยกับ catalog.name_th)
- แอนิเมชัน: เส้นสแกนสี ice วิ่งบนลงล่าง 1.2 วิ → วาด bbox โค้งมนทีละกล่อง (stagger 80ms)
  → chip บินจากกล่องลงถาดล่าง (framer-motion layoutId)
- Chips Review: จัดกลุ่มตาม category, วงแหวน expiry รอบ emoji, แตะเพื่อแก้ qty/added_on,
  confidence < 0.60 = สีจาง + ข้อความ "{name} ใช่ไหม?" ปุ่ม ✓ ยืนยัน / ✕ ลบ
- บันทึก inventory ลง LocalStore แล้วไป /menu
```

## D) Menu Match + Recipe Detail + Radar
```
/menu: เรียก menuMatch(inventory, filters) แสดง 3 การ์ดใหญ่
- การ์ด: emoji 56px, ชื่อเมนู, match_pct เป็นวงแหวน basil, เวลา, badge_th,
  pill tomato "ช่วยของใกล้เสีย ฿{rescue_value_thb}" เมื่อ > 0
- แถบฟิลเตอร์ chip: ไม่เผ็ด · ไม่กินหมู · มังสวิรัติ · ≤10 นาที · ≤15 นาที
- ปุ่ม "ดูทั้งหมด" = menuMatch(inv, {max_missing:3}, top_n=0)
/recipe/[id]: ของที่ใช้ (ติ๊ก basil) ของที่ขาด (tomato + "ใส่ลิสต์") staples เป็นสีเทา → "เริ่มทำเลย 👩‍🍳"
/radar: 4 คอลัมน์ ใช้วันนี้ / ใช้เร็ว / สบาย / เช็กก่อนกิน + headline_th + มูลค่าเสี่ยง ฿
ตรวจกับเดโม: top3 + scores ต้องตรง expect_locked
```

## E) Cook Mode + Shopping List
```
/cook/[id]: ขั้นละจอ (swipe/แตะครึ่งขวา = ถัดไป, ครึ่งซ้าย = ย้อน) ตัวอักษร 28px
- ขั้นที่ timer_s > 0: วงแหวนนับถอยหลังใหญ่ ปุ่มเริ่ม/หยุด, จบแล้วสั่น + เสียง "ติ๊ง" + timer_done
- ใช้ cookProgress(recipeId, stepIndex, elapsed) เป็นแหล่งความจริงเดียว
- Wake Lock ตอนอยู่หน้า cook · จบแล้ว cookLogEntry → push history, ลบ/ลด qty ของที่ใช้,
  แสดงการ์ด rescue (share_cards[0])
/list: shoppingList(selectedMatches) แยกร้าน ติ๊กได้ ปุ่ม "ส่งเข้า LINE"
  = https://line.me/R/share?text=<encodeURIComponent(line_text)> และปุ่มคัดลอก
เดโม: เลือก kai_pad_kaprao + pad_kalam_pli + yum_sai_krok (หลังยืนยันมะนาว) → total 80
```

## F) Nice-to-have: Dice + Wrapped + Share Cards + Settings
```
- /dice: pool = menuMatch(inv,{max_missing:0},0) · menuDice(pool, seed) seed เดโม 20261014
  (ใช้งานจริง seed = YYYYMMDD ของวันนั้น) แสดง 6 frames ทีละ 120ms แล้วเด้งการ์ด pick
- /wrapped: wasteWrapped(history, "YYYY-MM") การ์ดเข้ม ink + yolk ตัวเลขใหญ่ 5 บรรทัด
- ShareCard renderer 1080x1920 / 1080x1080 ตาม examples.json → share_cards ส่งออก PNG
  (html-to-image) + Web Share API
- /settings: staples, diet, household, stove, ai_vision on/off, ปุ่มล้างข้อมูล
```

## G) AI vision route (optional)
```
สร้าง app/api/ai/vision/route.ts รับ AiVisionRequest คืน AiVisionResponse (schemas.json)
- ใช้ vision model ที่มีใน env ; system prompt = Prompt K ด้านล่าง
- validate output ด้วย zod จาก schema: key ต้องอยู่ใน allowed_keys มิฉะนั้นย้ายไป unknown_items_th
- added_on = วันนี้ (ผู้ใช้แก้ได้) · timeout 15 วิ → fallback โหมดพิมพ์
- ไม่ log รูป ไม่เก็บรูป
```

## H) QA checklist
```
ไล่ตรวจทีละข้อแล้วรายงานผ่าน/ไม่ผ่าน:
1. เดโม → ทุก key ใน expect_locked ตรง
2. ยืนยันมะนาว → "ดูทั้งหมด" มี yum_sai_krok + yum_woon_sen
3. ฟิลเตอร์ไม่เผ็ด → top3 = khao_pad_sausage, khao_tom_moo, tom_jued_tofu_moo
4. ฟิลเตอร์ ≤8 นาที → khai_jiao_moo_sap, khai_pad_makheua_thet, pad_kalam_pli
5. ของหมดอายุ (days_left<0) ไม่ถูกใช้ในเมนู · ตู้เย็นว่าง → empty state
6. Cook Mode timer, Wake Lock, เสียง · ลิสต์ LINE ข้อความตรง
7. Dice seed เดิมผลเดิม · Wrapped 9/12/225/3
8. ไม่มี AI key ใช้ได้ครบ · 390px ไม่ล้น · ฟอนต์ไทยไม่ตัดสระ · PWA install ได้
```

## I) แก้บั๊ก (ใช้ซ้ำ)
```
ผลลัพธ์ไม่ตรง examples.json ที่ {path}: ได้ {actual} แต่คาด {expected}
เทียบ lib/fridge.ts กับ reference/fridge.py ฟังก์ชัน {fn} บรรทัดต่อบรรทัด
(จุดที่พลาดบ่อย: การเรียงลำดับ tie-break, pyRound, การนับวัน, LCG unsigned)
แก้ให้ตรงโดยไม่เปลี่ยน fixture แล้วรัน test ทั้งหมด
```

## J) หน้าอัด Reel
```
เพิ่ม ?reel=1: ซ่อนแถบเบราว์เซอร์ (fullscreen), ขยายแอนิเมชันสแกน 1.5x,
ปุ่ม "ข้ามไปขั้นถัดไป" สำหรับ Cook Mode (เร่ง timer 10x ตอนถ่าย), ตัวอักษรใหญ่ขึ้น 10%
ลำดับ: Home → Scan (demo photo) → Chips → Radar → Menu → Cook (เร่ง) → List → Dice → Wrapped card
```

---

## Runtime prompts (ใช้ใน /api/ai/*)

### K) Vision — นับของในตู้เย็น
```
คุณคือผู้ช่วยดูภาพตู้เย็นภาษาไทย ระบุวัตถุดิบที่มองเห็นชัดเท่านั้น
ตอบ JSON ตาม AiVisionResponse เท่านั้น ห้ามมีข้อความอื่น
- key ต้องอยู่ใน allowed_keys ที่ให้มา ; ของที่ไม่อยู่ในรายการ → ใส่ชื่อไทยใน unknown_items_th
- qty ประมาณจากภาพ (ฟอง/ลูก/ชิ้น/กรัม) ถ้าไม่แน่ใจใส่ 1
- confidence 0–1 ตามความชัด ห้ามเดา ; ของที่เห็นไม่ชัดให้ confidence < 0.6
- bbox = [x1,y1,x2,y2] normalized 0–1
- ห้ามประเมินว่าของเสีย/ไม่เสีย
```

### L) Recipes — สูตรเพิ่ม (เมื่อคลังเรามีน้อยกว่า 3 เมนู)
```
คุณคือเชฟอาหารไทยบ้าน ๆ สร้างสูตรไม่เกิน 3 สูตรจาก have + staples เท่านั้น
ตอบ JSON ตาม AiRecipeResponse (Recipe: id snake_case, name_th, emoji, time_min ≤ time_max,
tags, required ≥1 จาก have, optional, steps [[ข้อความ, timer_s]])
- เนื้อสัตว์ต้องมีขั้นทำให้สุก มี timer ชัด
- เคารพ diet (not_spicy, no_pork, vegetarian)
- ใส่ disclaimer_th: "สูตรจาก AI ตรวจความสุกของเนื้อสัตว์ก่อนกิน"
```

### M) แคปชัน Reel (ใช้เองตอนโพสต์)
```
เขียนแคปชัน Reel ภาษาไทย 3 แบบ (สั้น ตลก ประหยัด) สำหรับแอป FridgeChef
ข้อมูล: ตู้เย็นหอพัก 12 อย่าง → 3 เมนู, ช่วยของใกล้เสีย ฿60, ทั้งเดือนประหยัด ฿225
ต้องมี CTA "คอมเมนต์ 'ตู้เย็น' รับลิงก์ฟรี" + แฮชแท็ก 5 อัน ไม่เกิน 220 ตัวอักษร
```
