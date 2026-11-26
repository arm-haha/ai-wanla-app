# PartyPop — ถ่ายห้อง 1 รูป เห็นปาร์ตี้ปีใหม่ ครบในงบ (AI วันละแอป · 2026-12-25)

ถ่ายห้องนั่งเล่น/คอนโด/ห้องประชุม 1 รูป + ใส่ **จำนวนแขก (ผู้ใหญ่/เด็ก)** + **งบเป็นบาท** → AI อ่านห้อง (กว้าง × ลึก, โต๊ะ, ระเบียง, ห้องเช่าไหม) → โค้ดคำนวณ **ความจุ** (นั่งได้กี่คน ยืนได้กี่คน เว้นทางออก ≥ 80 ซม.) → **แบ่งงบอัตโนมัติ** (ตกแต่ง 25% · อาหาร 50% · เครื่องดื่ม 12% · เกม/ของขวัญ 8% · สำรอง 5%) → ⭐ **เห็นห้องตัวเองแต่งปาร์ตี้แล้ว** ใน 6 ธีม (เคานต์ดาวน์ทอง · คริสต์มาสอบอุ่น · พาสเทลป๊อป · งานวัดย้อนยุค · นีออนดิสโก้ · มินิมอลขาวทอง) พร้อมลิสต์ของตกแต่งที่ **ไม่เกินงบ** และ **ไม่ต้องเจาะผนัง** (ธงราวกี่แพ็กตามความยาวผนัง ลูกโป่งกี่แพ็กตามพื้นที่) → **เมนู + คำนวณปริมาณ** (สุกี้หม้อไฟฟ้า / ข้าว+กับข้าวถาด / ของทานเล่น — เด็กคิด 60%, เครื่องดื่มตามชั่วโมง, น้ำแข็งต่อคน) → **ลิสต์ช้อปปิ้งเป็นบาท** แยกตามร้าน ติ๊กได้ → **ไทม์ไลน์งาน** (ส่งการ์ด T-7 วัน → แต่งห้องคืนก่อน → ของสด T-4 ชม. → 23:59 นับถอยหลัง → จับสลาก → กลับบ้านปลอดภัย) → **เกมงานครอบครัว/ออฟฟิศ** ตามจำนวนคนและเวลา (ไม่มีเกมดื่ม) → **การ์ดเชิญ** ตามธีม (เวอร์ชันแชร์ซ่อนที่อยู่ + RSVP) → **จับสลากของขวัญ** ในแอป (ไม่จับได้ตัวเอง กันคู่รักจับกันเอง มีโค้ดลับเปิดดูทีละคน) → **หารค่าใช้จ่าย** (เด็กฟรี เจ้าภาพออกค่าตกแต่งได้) + การ์ด Before/After / Reel พร้อม Safety Guard (ผู้เยาว์ = ไม่มีแอลกอฮอล์, ดื่มไม่ขับ, ห้ามพลุ/เทียนจริง/เตาถ่านในห้อง, เกินความจุ, เสียงดังหลังเที่ยงคืน, เด็กเล็กกับลูกโป่ง, แพ้อาหาร)

**EN:** Snap one photo of your living room, condo or meeting room, enter **guests (adults/kids)** and a **THB budget** → AI reads the room (width × depth, tables, balcony, rental or not) → code works out **capacity** (seated, standing, with an 80 cm exit path) → **auto-splits the budget** (decor 25% · food 50% · drinks 12% · games/gifts 8% · reserve 5%) → ⭐ **see your own room decorated for the party** in 6 themes (countdown gold · cozy Christmas · pastel pop · Thai temple fair · neon disco · minimal white & gold) with a decor list that **fits the budget** and needs **no nails** (garland packs by wall length, balloon packs by floor area) → **menu + portion calculator** (electric-pot suki / rice + trays / party snacks; kids count as 60%, drinks by the hour, ice per guest) → a **THB shopping list** grouped by shop with check boxes → a **party timeline** (invites at T-7 days → decorate the night before → fresh food T-4 h → 23:59 countdown → gift swap → get home safe) → **family / office games** that fit the head count and time (no drinking games) → a themed **invitation card** (the shareable version hides the address, with RSVP) → an in-app **gift-swap draw** (no one draws themselves, couples can be kept apart, secret codes to peek one by one) → **cost splitting** (kids free, host can cover decor) + Before/After card and Reel, with a Safety Guard (minors = no alcohol, don't drink and drive, no fireworks, real candles or charcoal grills indoors, over-capacity, late-night noise, small kids and balloons, food allergies).

## ในแพ็ก / Pack contents
- `prd.md` — ปัญหา, must-have / nice-to-have (10 ฟีเจอร์), หน้าจอ, demo fixture, design tokens, Reel shot list, build plan, risks / traps, guardrails, metrics
- `prompts.md` — work-order prompts P0–P12 + AI prompts A1–A5
- `schemas.json` — JSON Schema 2020-12 (25 defs)
- `examples.json` — 118 ตัวอย่าง (ข้อมูลสมมติ) validate ผ่านหมด
- `reference/` — `partypop.py` logic deterministic (คำนวณพื้นที่/ความจุ, แบ่งงบ, เลือกของตกแต่งตามงบ+ธีม+ขนาดห้อง, prompt ภาพที่คงโครงห้องเดิม, เมนูและปริมาณตามแพ็กที่ซื้อได้จริง, ลิสต์ช้อปปิ้ง, ปรับเมนูเมื่อเกินงบ/Potluck, ไทม์ไลน์นับถอยหลัง, เลือกเกม, จับสลาก, การ์ดเชิญ, หารเงิน, quota, guard), `fixtures.py` (คุณแพร 32 ปี ห้องนั่งเล่นคอนโด 4.2 × 3.6 ม. แขก 9 ผู้ใหญ่ + 3 เด็ก งบ 4,000 บาท), `tests.py` (35 tests), `build.py`
- `social/` — `make_cover.py`, ปก 1080×1350 / 1080×1080, `fb_post.md`, `caption_fb.txt`

## รัน / Run
```
cd reference && python3 tests.py && python3 build.py   # ต้องมี jsonschema
```

## หมายเหตุ / Notes
- AI ทำแค่ "อ่านรูปห้องเป็นร่างข้อมูล + วาดภาพห้องหลังแต่ง + เขียนข้อความสนุก ๆ" ส่วนตัวเลข ความจุ งบ จำนวนแพ็ก ปริมาณอาหาร ราคา ไทม์ไลน์ และผลจับสลาก เป็นโค้ด deterministic ทดสอบได้ ผลเหมือนเดิมทุกครั้ง
- ราคาสินค้าใน `DECOR` / `FOOD` เป็นราคาตัวอย่างที่ตั้งเอง ไม่ใช่ราคาร้านจริง ไม่อ้างอิงแบรนด์ใด ปรับได้ใน `partypop.py`
- รูปห้องและข้อมูลแขกเก็บบนเครื่อง การ์ดเชิญเวอร์ชันแชร์ไม่โชว์ที่อยู่ รูปที่มีคนอื่นเบลอหน้าก่อนแชร์
- ไม่มีเกมดื่ม งานที่มีเด็กไม่ใส่แอลกอฮอล์ ใช้เทียน LED/หม้อไฟฟ้าแทนไฟจริง และเตือนเรื่องกลับบ้านปลอดภัย
- ทุกตัวอย่างเป็นบุคคลสมมติ ภาพปกสร้างด้วยโค้ดล้วน ไม่ใช้รูปคนจริงหรือแบรนด์จริง
