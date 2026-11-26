# Work-order prompts — PartyPop

> ให้ AI codegen (Cursor / Claude / v0 / Lovable ฯลฯ) ทำทีละ prompt ตามลำดับ ใช้ `schemas.json` เป็นสัญญาข้อมูล และ `reference/partypop.py` เป็นตรรกะต้นแบบ (port เป็น TypeScript ให้ผลเท่ากับ `tests.py`)

**P0 — Scaffold**: สร้าง PWA (Next.js หรือ Vite + React + Tailwind) มือถือก่อน ภาษาไทยเป็นหลัก สลับ EN ได้ ใช้ design tokens ใน prd.md (ม่วง #14102B ทอง #FFC440 ชมพู #FF6B8B ฟ้า #82DCFF, Kanit + Sarabun) port `partypop.py` → `src/logic/partypop.ts` พร้อม unit test เทียบ `tests.py` ทั้ง 35 ข้อ (fixture คุณแพรจาก `fixtures.py`) เก็บข้อมูลใน IndexedDB บนเครื่อง ราคาทุกบรรทัดแก้ได้และจำค่าที่แก้

**P1 — Party setup**: ชื่อเจ้าภาพ, อายุ (< 13 → `privacy_check(age=…)` ขอ parent mode), วัน-เวลาเริ่ม/จบ, ผู้ใหญ่/เด็ก/เด็กเล็ก < 3 ขวบ, งบรวม (บาท), โหมด ครอบครัว/ออฟฟิศ/เพื่อน, มีแอลกอฮอล์ไหม + มีแขกขับรถกี่คน, แพ้อาหาร → `party_flags(...)` → `privacy_check(flags)` แสดงคำเตือนเป็นการ์ดสีเหลือง/แดง; `alcohol_minor` → ปิดตัวเลือกแอลกอฮอล์ทั้งหมด. Output `User`, `PrivacyCheck`.

**P2 — Room scan (A1)**: กล้อง/อัปโหลด 1 รูป (ย่อเหลือ 1280 px ลบ EXIF/GPS) → A1 → `AiRoomScan` → หน้าจอยืนยันขนาด (สไลเดอร์กว้าง/ลึก ทีละ 0.1 ม. + "ไม่แน่ใจ ใช้ค่าประมาณ") → `room_from_scan` → `capacity(room, adults, kids)` การ์ด comfy/mingle/over + ทิป; over → ปุ่ม "ใช้ระเบียงด้วย" (ถ้า has_balcony). Output `Room`, `Capacity`.

**P3 — Budget**: `budget_split(total, adults, kids)` → โดนัทชาร์ต 5 ส่วน + "เฉลี่ยคนละ … บาท"; potluck → แบนเนอร์ "ให้แขกช่วยถือมาคนละจาน". ผู้ใช้ปรับสัดส่วนได้ แต่ผลรวมต้องเท่างบเสมอ. Output `BudgetSplit`.

**P4 — Theme & Party Preview (A2)** ⭐: การ์ดธีม 6 ใบ (`THEMES` + `DRESS`) → `deco_plan(room, theme, budget.decor, guests)` → `render_prompt(room, plan)` → ส่ง A2 แบบ image-to-image (รูปเดิม + mask ผนัง/เพดาน/โต๊ะ) → ได้ภาพ After → สไลเดอร์ Before/After + หมุดชี้ของแต่ละชิ้น (ชื่อ ×แพ็ก ราคา) + ป้าย "ข้ามไว้ก่อน: …" สำหรับ `skipped`. ตัวอักษรบนภาพ (HAPPY NEW YEAR, ป้ายราคา) วาดทับด้วย canvas ไม่ให้ AI วาด. แอนิเมชัน "ของตกแต่งหล่นลงที่" + คอนเฟตติ. Output `DecoPlan`, `DecoPick`, `RenderPrompt`.

**P5 — Menu**: เลือกสไตล์ `MENU_STYLES` + ชั่วโมงงาน → `menu_plan(style, adults, kids, hours, allergies)` → การ์ดต่อเมนู "ต้องใช้ 1.62 กก. → ซื้อ 2 กก. (4 แพ็ก)" + ราคา; allergy → ป้ายส่วนผสมพิมพ์ได้. Output `MenuPlan`, `MenuItem`.

**P6 — Shopping list**: `shopping_list(plan, menu, budget)` แยกตามร้าน ติ๊กได้ แชร์เป็นข้อความ/รูปให้คนช่วยซื้อ; `fits == false` → ปุ่ม "ทำให้ลงงบ" → `trim_menu()` แสดงทางเลือก (เปลี่ยนเมนู หรือ Potluck n จาน). Output `ShoppingList`, `MenuTrim`.

**P7 — Timeline**: `timeline(start, end, new_year=True, alcohol)` → รายการงานพร้อมเวลา + แจ้งเตือน (Notification API) + ติ๊กเสร็จ; โหมดวันงาน: นาฬิกานับถอยหลังเต็มจอ 23:59 → 00:00 พลุบนจอ (ไม่มีพลุจริง). Output `Timeline`.

**P8 — Games**: `game_plan(players, mode, kids, minutes)` → การ์ดเกม (วิธีเล่น 3 บรรทัดจาก A4, อุปกรณ์, เวลา) + ตัวจับเวลา + การ์ดคำใบ้/บิงโกพิมพ์ได้; ไม่มีเกมดื่มในคลังเลย. Output `GamePlan`.

**P9 — Invite & gift swap**: `invite()` การ์ด 1080×1350 ตามธีม + ข้อความเชิญจาก A3; public = ซ่อนที่อยู่ (ส่งโลเคชันหลังกด "ไปแน่นอน"). `gift_swap(names, seed, cap, exclude)` → หน้าจอส่งมือถือเวียน: แต่ละคนใส่โค้ดลับ 4 ตัว → การ์ดพลิกเห็นชื่อคนที่ต้องซื้อให้ (เห็นทีละคน) + ปุ่ม "สุ่มใหม่" สำหรับเจ้าภาพ (seed ใหม่). Output `Invite`, `GiftSwap`.

**P10 — Split, Share / Reel**: `cost_split(total, adults, kids, host_pays)` + QR พร้อมเพย์ของเจ้าภาพ (ผู้ใช้ใส่เอง แอปไม่ยุ่งกับเงิน); `share_card(kind)` 3 แบบ เบลอหน้า ซ่อนที่อยู่ ลายน้ำ "PartyPop · AI วันละแอป"; `reel_plan()` → canvas 1080×1920 7 ช็อต 120 BPM → MediaRecorder; `countdown(today)` บน Home. Output `CostSplit`, `ShareCard`, `ReelPlan`, `Countdown`.

**P11 — Quota / Guard**: `quota()` ฟรี 3 ภาพ After/วัน; `safety_guard()` ทุก flag; ถ้า A1 เห็นเตาถ่าน/เทียนจริง/พลุในรูป → `indoor_fire` warn; ภาพที่มีคนในรูป → `photo_of_others` เบลอก่อนแชร์.

**P12 — QA**: รัน `reference/tests.py` (35 tests) และ validate output ทุกตัวกับ `schemas.json`; ทดสอบห้องสตูดิโอเล็ก 12 คน (over), งบ 1,500 (potluck), งบ 0 ค่าตกแต่ง (ลิสต์ว่าง), เปลี่ยนธีมทุกแบบ, งานกลางวันไม่คร่อมเที่ยงคืน (ไม่มีนับถอยหลัง), จับสลาก 3 คนที่ห้ามจับกันจนเป็นไปไม่ได้ (แจ้งให้แก้), มีเด็ก + แอลกอฮอล์ (stop), ภาพ After ไม่มีตัวอักษรเพี้ยน/โลโก้.

## AI prompts

**A1 — Room scan (vision, JSON only)**
```
คุณคือผู้ช่วยของแอป PartyPop ดูรูปห้องแล้วตอบ JSON ตาม schema AiRoomScan เท่านั้น:
{room_type: living|studio|office|dining|garden|rooftop, width_m, depth_m (ประมาณจากขนาดประตู ~0.8×2 ม. โซฟา 3 ที่นั่ง ~2 ม.),
 tables: จำนวนโต๊ะที่วางอาหารได้, has_balcony, rental (เดาจากคอนโด/หอ ถ้าไม่แน่ใจ true), zones: [wall, sofa, table, window, ceiling, bed, floor],
 light: warm|cool|dim, clutter 0..1, confidence 0..1}
ห้ามคำนวณพื้นที่ จำนวนแขก ราคา หรือของที่ต้องซื้อเอง ถ้าเห็นเตาถ่าน เทียนจริง หรือพลุ ให้ลด confidence และใส่ "floor" ใน zones
```
**A2 — Party render (image-to-image)**: "แต่งห้องในรูปนี้สำหรับปาร์ตี้ปีใหม่ ธีม <theme> โทนสี <palette> คงตำแหน่งผนัง หน้าต่าง โซฟา โต๊ะ และมุมกล้องเดิมทุกอย่าง เพิ่มเฉพาะ: <items_th> ติดแบบไม่เจาะผนัง แสงอบอุ่นยามค่ำคืน ห้ามมีตัวอักษร ตัวเลข ใบหน้าคน โลโก้หรือแบรนด์ ห้ามมีไฟจริง เทียนจริง หรือพลุในห้อง สัดส่วน 4:5"
**A3 — Invite line**: "จาก Invite เขียนข้อความเชิญ 2 บรรทัด ≤ 60 ตัวอักษร สนุก อบอุ่น ใส่ dress code ห้ามใส่ที่อยู่ ห้ามชวนดื่มแอลกอฮอล์ ห้ามเปลี่ยนวันเวลา"
**A4 — Game host**: "จากเกมใน GamePlan เขียนวิธีเล่น 3 บรรทัด + คำใบ้/โจทย์ 10 ข้อ เหมาะกับ <mode> และอายุผู้เล่น ไม่มีการดื่ม ไม่มีการลงโทษที่ทำให้อายหรือเจ็บตัว ไม่ล้อรูปร่างหน้าตา เนื้อหาไม่เกี่ยวกับการเมือง/ศาสนา"
**A5 — Wish & recap**: "เขียนคำอวยพรปีใหม่สั้น ๆ 1 บรรทัดสำหรับเกมเป่าลูกโป่ง 12 แบบ และสรุปงาน 3 บรรทัดสำหรับการ์ดแชร์หลังงาน ใช้ข้อมูลจริงจาก ShoppingList/GamePlan เท่านั้น ห้ามอ้างแบรนด์ ห้ามแต่งตัวเลข"
