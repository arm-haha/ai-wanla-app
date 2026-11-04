# Work-order prompts — RoomGlow (วางทีละอันใน v0 / Lovable / Bolt / Cursor)

**P0 — Scaffold**
สร้างเว็บแอป mobile-first ชื่อ "RoomGlow — ห้องเดิม ลุคใหม่" React + Vite + Tailwind ภาษาไทยทั้งหมด ธีม linen #F7F4EE, ink #2B2A28, oak #C9A27E, sage #8FA98F, glow #FFB547, night #1E2230, danger #E5484D ฟอนต์ Prompt + IBM Plex Sans Thai มุม 24px bottom tab 5 แท็บ: ถ่ายห้อง / 6 ลุค / งบ & ลิสต์ / แผนวันหยุด / โหวต เก็บข้อมูล localStorage ตาม schemas.json (Room, CatalogItem, ShoppingPlan, Vote) ไม่ต้องล็อกอิน ปุ่ม "ลองด้วยห้องตัวอย่าง" โหลด fixture ห้องของฝน

**P1 — Room setup**
ฟอร์ม 3 สเต็ป: ประเภทห้อง (นอน/นั่งเล่น/สตูดิโอ/โต๊ะทำงาน/ครัว), ขนาด กว้าง×ยาว×สูง (มีปุ่ม "ให้ AI เดาจากรูป" ใช้ est_size_m), ห้องเช่าไหม (default ใช่), งบ (สไลเดอร์ ฿500–20,000 snap ที่ 1,000/3,000/10,000) บันทึก Room

**P2 — Logic module**
พอร์ต reference/roomglow.py เป็น TypeScript (lib/room.ts): floorArea, wallArea, paintEstimate, wallpaperRolls, lumensNeeded, lightPlan, glowScore, scoreAfter, shoppingPlan (0/1 knapsack ทีละบาท), declutter, weekendPlan, pollTally ปัดทศนิยม 2 ตำแหน่ง ผลต้องตรง examples.json เขียน vitest ตาม tests.py ใส่ catalog จาก fixtures.py เป็น data/catalog.json

**P3 — Room Snap + Glow Score**
กล้องหลังแนวนอน มีไกด์ "ยืนมุมห้อง เห็นผนัง 2 ด้าน" ถ่ายแล้วส่ง vision ด้วย ROOM SCAN PROMPT → RoomScanExtract ถ้า room_found=false หรือ confidence<0.6 แสดง retake_reason_th ให้ถ่ายใหม่ คำนวณ glowScore แสดงเกจวงกลมวิ่งจาก 0 → 32 พร้อมชิป 4 ตัว (แสง/ความรก/สี/ธีม) และกรอบ bbox ไฮไลต์ "จุดรก" สีแดงจาง

**P4 — Style Grid 6 ลุค (WOW)**
สร้าง RestyleRequest ต่อสไตล์ด้วย RESTYLE PROMPT (image edit, keep_layout, seed คงที่, ส่ง item_ids จาก shoppingPlan ของสไตล์นั้นเพื่อให้ภาพมีของที่ซื้อได้จริง) ยิงพร้อมกันไม่เกิน 3 ช่อง grid 2×3 skeleton แล้วเอฟเฟกต์ "เปิดไฟ" ทีละช่อง ใต้ภาพมีชื่อสไตล์ + Glow หลัง + ราคา ถ้า LAYOUT CHECK ไม่ผ่าน status=retry สร้างใหม่ 1 ครั้ง ไม่ผ่านอีก status=blocked ซ่อนช่อง

**P5 — Budget Slider → Shopping List**
หน้าลิสต์ของสไตล์ที่เลือก เลื่อนงบแล้วคำนวณ shoppingPlan สด ๆ (debounce 150ms) การ์ดของแต่ละชิ้น: ชื่อ, ราคาประมาณ, impact bar, ปุ่ม "หาใน Shopee" / "หาใน Lazada" (ลิงก์ค้นหาด้วย shop_query_th หรือ name_th) แถบงบด้านบน "ใช้ ฿3,000 / ฿3,000 (100%)" toggle โหมดห้องเช่า แสดงชิปเทา "ตัดออก: ทาสีผนัง, ชั้นเจาะผนัง" ติ๊กของที่มีอยู่แล้วเพื่อเอาออกจากลิสต์

**P6 — Before/After + Share Card**
สไลเดอร์ลากกลางภาพเทียบเดิม/ใหม่ ตัวเลข Glow 32 → 78 นับขึ้น สร้าง ShareCard 9:16 (html-to-image) 5 แบบ: style_grid, before_after, budget_receipt (ใบเสร็จแนวสลิป), poll, glow_score ใส่ disclaimer เสมอ

**P7 — Light Planner**
modal: พื้นที่ห้อง × lux ตามประเภท → lumens ที่ต้องการ เทียบ existing_lm แสดงเกจ "ขาด 1,120lm = หลอด 800lm 2 ดวง" + สีไฟ (2700K อบอุ่น/3000K/4000K) ตามสไตล์ พรีวิวโทนสีไฟทับภาพ (CSS overlay)

**P8 — Paint & Wallpaper Calculator**
กรอกจำนวนประตู/หน้าต่าง → wallArea, paintEstimate (ตั้งค่าได้: รอบทา, coverage, ขนาดถัง, ราคา), wallpaperRolls สำหรับผนังเดียว ถ้าห้องเช่าให้แนะนำวอลเปเปอร์ลอกออกได้ก่อน

**P9 — Declutter Sorter + Weekend Plan**
Declutter: การ์ดปัดซ้าย/ขวา/ขึ้น/ลง = ทิ้ง/เก็บ/ขาย/บริจาค ใส่ราคาขายได้ สรุปเงินคืน + ปุ่ม "เอาเงินนี้ไปเพิ่มงบ" Weekend Plan: weekendPlan() เป็น checklist พร้อมเวลาสะสม ติ๊กแล้วมีคอนเฟตตี เก็บสถานะ

**P10 — Friend Vote + Palette**
สร้างลิงก์โหวต (encode ตัวเลือกใน URL hash ไม่ต้องมี backend) ผู้โหวตกรอกชื่อแล้วเลือก 1 ลุค ชื่อซ้ำนับครั้งล่าสุด pollTally แสดงบาร์ % การ์ด Palette ต่อสไตล์ 4–5 สี แตะเพื่อคัดลอก hex

---

## AI prompts (ใช้ใน P3/P4)

**ROOM SCAN PROMPT (vision → JSON ตาม RoomScanExtract)**
คุณคือผู้ช่วยแต่งบ้าน ดูภาพห้องนี้แล้วตอบเป็น JSON เท่านั้นตาม schema RoomScanExtract: room_found, room_type (bedroom/living/studio/desk/kitchen หรือ null), scores 0–1 ได้แก่ light (ความสว่าง/แสงธรรมชาติ), clutter (1 = รกมาก), harmony (สีเข้ากันแค่ไหน), cohesion (ของทั้งหมดเป็นธีมเดียวกันแค่ไหน), items_seen (label_th, kind, bbox 0–1), wall_color_hex, est_size_m (ประมาณจากเตียง 5 ฟุต ≈ 1.5×2.0 ม. หรือประตู ≈ 0.8×2.0 ม., ไม่แน่ใจใส่ null), confidence, retake_reason_th ห้ามเดาถ้าไม่เห็น ห้ามบรรยายเอกสาร/ใบหน้า/ข้อมูลส่วนตัวในภาพ

**RESTYLE PROMPT (image edit)**
แต่งห้องในภาพนี้ใหม่เป็นสไตล์ {style_th} ห้ามย้ายหรือเปลี่ยนรูปทรงของผนัง หน้าต่าง ประตู เพดาน และเตียง/เฟอร์นิเจอร์ชิ้นใหญ่ เปลี่ยนได้เฉพาะ ผ้าปู ม่าน พรม ไฟ ของแต่ง ต้นไม้ และเก็บของรกออก ใส่ของเหล่านี้ให้เห็นชัด: {item_names_th} โทนสี {palette_hex} สีไฟ {kelvin}K มุมกล้องและเลนส์เดิม ภาพสมจริงแบบถ่ายด้วยมือถือ ไม่ใช่ภาพ 3D render ห้ามมีตัวหนังสือหรือโลโก้

**LAYOUT CHECK PROMPT (vision เทียบ 2 ภาพ)**
เทียบภาพ A (เดิม) กับ B (แต่งใหม่) ตอบ JSON {"layout_ok": bool, "moved_th": [..]} layout_ok=false ถ้าหน้าต่าง ประตู ผนัง หรือเตียงย้ายตำแหน่ง/เปลี่ยนขนาดชัดเจน หรือห้องดูใหญ่ขึ้นผิดจริง

**PALETTE PROMPT**
จากภาพ B ดึงสีหลัก 4–5 สีเป็น JSON ตาม Palette (role: base/secondary/accent/wood/metal) ตั้งชื่อสีภาษาไทยสั้น ๆ
