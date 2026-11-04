# ClosetDice — Prompt สั่งงาน (จัดเต็ม)

ใช้กับ AI codegen (Cursor / Claude / GPT) สร้างแอปทั้งก้อน  
และใช้สร้างตู้เดโม / mock tagging / กติกาสุ่มชุด

**วันที่แพ็ก:** 2026-10-05 (Asia/Bangkok) · Day 6/10 · AI วันละแอป  
**เอกสารคู่กัน:** `prd.md`, `schemas.json`, `examples.json`

---

## A) Master prompt สร้างทั้งแอป (วางครั้งเดียว)

```text
สร้างเว็บแอปมือถือเป็นหลักชื่อ ClosetDice (UI ภาษาไทยก่อน)

วันที่ส่งมอบคอนเทนต์: 2026-10-05 สำหรับช่อง "AI วันละแอป"
เป้าหมายผู้ใช้: ถ่ายรูปเสื้อผ้า → ตัดพื้นหลัง + ติดแท็กอัตโนมัติ → กดทอยลูกเต๋า → ได้ชุดแต่งตัววันนี้แบบ flat-lay
ตามอากาศและโอกาส → ล็อกชิ้นที่ชอบแล้วทอยใหม่ → บันทึกลงปฏิทิน OOTD → แชร์การ์ดชุดสวย

สแต็กบังคับ:
- Next.js 14 App Router + TypeScript + Tailwind CSS + shadcn/ui + framer-motion
- Outfit engine pure ใน lib/dice.ts (seeded random, เทสต์ได้ด้วย vitest)
- Tagging pluggable ใน lib/tagger.ts: ค่าเริ่ม "mock_demo" (รองรับ "vision_api" ผ่าน env แต่ไม่บังคับ)
- Cutout pluggable ใน lib/cutout.ts: "mock_demo" | "client_bg_removal" (@imgly/background-removal, lazy load) | "none"
- สีเด่นจากรูปด้วย canvas k-means 3 สี ใน lib/colors.ts + map เป็นชื่อสีไทย
- รูปเก็บ IndexedDB (idb-keyval) ย่อ ≤600px webp; metadata/settings/wear log ใน localStorage (lib/storage.ts)
- Share card ใน lib/share.ts (html-to-image หรือ canvas) + navigator.share files + fallback ดาวน์โหลด
- อากาศ optional: Open-Meteo (ไม่ต้อง key) ใน lib/weather.ts, ล้มเหลวให้ใช้ชิปเลือกเอง
- Deploy Vercel + manifest PWA
- ไม่มี auth ไม่มี backend ไม่มี virtual try-on ไม่พูดถึงรูปร่างผู้ใช้

ต้องมีอย่างน้อย 5 ฟีเจอร์ must-have:
1) Snap → Closet — กล้อง/อัปโหลด → progress「กำลังตัดพื้นหลัง…」→ PNG โปร่งใส → แท็กอัตโนมัติ
   (category, colors, warmth, formality, vibes, rain_ok) → ฟอร์มแก้ด้วยชิปใหญ่ → บันทึก
2) Outfit Dice — ปุ่มลูกเต๋า 3D ใหญ่ → หมุน 0.9s → ชิ้นร่วงประกอบ flat-lay + คะแนนเข้ากัน 0–100 + ชื่อลุคไทย
3) Weather & Occasion Lock — ชิปอากาศ (hot_extreme/hot/rain/ac_cold) + โอกาส (office/campus/cafe/date/wedding/gym)
   + ปุ่ม 🔒 ต่อชิ้น → ทอยใหม่เฉพาะ slot ที่ไม่ล็อก
4) OOTD Calendar — ปุ่ม「ใส่ชุดนี้วันนี้」→ wear log → ปฏิทินเดือนแสดง thumbnail → กันสุ่มทั้งชุดซ้ำใน no_repeat_days (ค่าเริ่ม 7)
5) Share Outfit Card — story 1080x1920 / feed 1080x1350, พื้นหลัง 4 แบบ, วันที่ + อากาศ + ชื่อลุค, แคปชันคัดลอก

ปุ่ม「ลองตู้เดโม」ต้องโหลดตู้ 14 ชิ้นจาก /public/demo/closet.json + PNG ใน /public/demo/items/ ได้ทันที

พิเศษถ้าเสร็จเร็ว (nice-to-have):
- Forgotten Items / Closet Stats (ไม่ได้ใส่ ≥30 วัน, cost-per-wear)
- 7-Day Dice Challenge
- Trip Packing Dice
- Friend Vote card (3 ลุค)
- Color Harmony hint
- Dark mode + เสียงลูกเต๋า/haptic (navigator.vibrate)

หน้าจอ: Home/Today, Dice Result, Closet, Add Item, Item Detail, OOTD Calendar, Share Sheet, Settings
(+ Stats/Challenge/Packing/Vote ถ้าทำ)

UX บังคับ:
- มือถือแนวตั้ง 390px เป็นฐาน, ปุ่ม ≥48px, bottom nav 4 แท็บ: วันนี้ | ตู้ | ปฏิทิน | ตั้งค่า
- พื้น #FAF7F2, ลาเวนเดอร์ #8B5CF6 / #C4B5FD, เนย #FCD34D, หมึก #1E1B2E, เขียวคะแนนดี #22C55E
- ฟอนต์ IBM Plex Sans Thai หรือ Noto Sans Thai
- ข้อความ UI ตาม examples.json → ui_copy_th
- disclaimer「AI ช่วยแนะนำ — สไตล์สุดท้ายเป็นของคุณ」

คุณภาพโค้ด:
- แยก components/, hooks/, lib/dice.ts, lib/tagger.ts, lib/cutout.ts, lib/colors.ts, lib/share.ts, lib/storage.ts, lib/weather.ts
- types/closetdice.ts สอดคล้อง schemas.json
- unit test lib/dice.ts: กฎแข็งไม่ถูกละเมิด 200 รอบ, lock คงที่, no-repeat ทำงาน
- README ไทย: วิธีรัน, วิธีเพิ่มชิ้นเดโม, วิธีถ่าย Reel
- เริ่มจาก `npm run dev` ผ่าน + happy path (ตู้เดโม → เลือกอากาศ/โอกาส → ทอย → ล็อก → ทอย → ใส่ชุดนี้ → แชร์) ก่อน
  แล้วค่อยทำ Snap ของจริง

อ้างอิงฟิลด์และตัวอย่างจาก schemas.json + examples.json ที่แนบมา
เมื่อจบสรุปว่า must 5 ตัวอยู่ไฟล์ไหน และวิธีโหลดตู้เดโม 1 ย่อหน้า
```

---

## B) Prompt สร้างตู้เดโม (fixture 14 ชิ้น)

```text
สร้างข้อมูลตู้เดโมสำหรับ ClosetDice

1) ไฟล์ /public/demo/closet.json เป็น array ของ ClothingItem ตาม schemas.json
2) เจ้าของตู้สมมติ: "ฟ้า" พนักงานออฟฟิศ กทม.
3) 14 ชิ้นตามนี้ (id คงที่ เพื่อให้ Reel รีเพลย์ได้ — ต้องตรง demo_closet ใน examples.json):
   top_01 เชิ้ตครีมแขนยาว (formality 3, minimal/smart)
   top_02 ยืดขาวพื้น (1, minimal)
   top_03 ไหมพรมลาเวนเดอร์ (2, sweet, rain_ok false)
   top_04 โปโลกรม (2, smart)
   bottom_01 สแล็กกรม (3, smart/minimal)
   bottom_02 ยีนส์ทรงกระบอก (1, street/minimal)
   bottom_03 พลีทเบจยาว (2, sweet/minimal)
   dress_01 เดรสเชิ้ตเขียวเสจ (3, minimal)
   outer_01 เบลเซอร์ดำบาง (4, smart, warmth 2, rain_ok false)
   outer_02 แจ็กเก็ตกันฝนสีเนย ทรงเชิ้ต (2, street/minimal, rain_ok true)
   shoes_01 โลฟเฟอร์น้ำตาล (3, rain_ok false)
   shoes_02 ผ้าใบขาว (1, rain_ok false)
   shoes_03 รัดส้นยางดำ (2, rain_ok true)
   acc_01 กระเป๋าผ้าครีม (2, minimal)
4) image_url ชี้ /public/demo/items/{id}.png (PNG โปร่งใส 600x600)
5) wear_count / last_worn_at สมจริง เวลา Asia/Bangkok, บางชิ้น ≥30 วัน (ให้มีชิ้นถูกลืม)
6) แท็กสีใช้ enum ColorName ใน schemas.json

ทอยด้วย filters {weather: "rain", occasion: "office", seed: 20261005}
ต้องได้ผลตรงกับ dice_roll_example ใน examples.json
```

---

## C) Prompt สร้าง TypeScript types จาก schemas

```text
อ่าน schemas.json ของ ClosetDice แล้วสร้าง types/closetdice.ts

ต้องมีอย่างน้อย:
Category, Slot, ColorName, Vibe, Weather, Occasion, ClothingItem, ClothingTagResult,
OutfitFilters, OutfitPiece, Outfit, DiceRoll, LockState, WearLogEntry, ShareCard,
SharePayload, Settings, LocalStore, AnalyticsEvent, FeatureChecklist,
TagEngine, CutoutEngine, AppStatus

กติกา: union string ตรง enum, JSDoc สั้นอังกฤษ, export ทุก type, ห้าม any, optional ใช้ ?
```

---

## D) Prompt Outfit Engine (`lib/dice.ts`)

```text
เขียน lib/dice.ts (pure TypeScript, ไม่มี DOM) สำหรับ ClosetDice + ไฟล์เทสต์ dice.test.ts (vitest)

API:
- rollOutfit(items: ClothingItem[], filters: OutfitFilters, locks: LockState, wearLog: WearLogEntry[], settings: Settings): DiceRoll
- scoreOutfit(pieces: ClothingItem[], ctx): { score: number; reasons_th: string[] }
- outfitSignature(pieceIds: string[]): string  // sort + join
- nameLook(pieces, filters): string           // template ไทย

กติกา:
1) template: occasion → slots ที่ต้องมี
   - ปกติ: top + bottom + shoes หรือ dress + shoes (สุ่ม 30% ใช้ dress ถ้ามี dress ผ่านกฎ)
   - outer: บังคับเมื่อ weather = ac_cold; เมื่อ rain ให้ใช้ outer ที่ rain_ok ถ้ามี (ไม่มีก็ข้าม)
   - accessory: 50% ถ้ามี
2) hard filter:
   - formality อยู่ในช่วง OCCASION_FORMALITY (office 2–4, campus 0–3, cafe 1–3, date 2–4, wedding 3–5, gym 0–1)
   - weather: hot_extreme → warmth ≤1 และไม่เอา outer ยกเว้นล็อก; rain → shoes ต้อง rain_ok true;
     ac_cold → ต้องมีชิ้น warmth ≥2 อย่างน้อย 1
   - in_laundry = true ออก
   - signature ทั้งชุดห้ามอยู่ใน wearLog ภายใน settings.no_repeat_days
3) soft score 0–100 (เริ่ม 60):
   - neutral ทุกชิ้น +10; มีสีสด 1 จุด (pop) +12; สีสด ≥2 ต่างตระกูล −15; monochrome +8
   - vibe ร่วม ≥2 ชิ้น +10
   - ชิ้นใส่ภายใน 3 วัน −6/ชิ้น
   - ชิ้นไม่ได้ใส่ ≥30 วัน +4/ชิ้น
   - clamp 0–100
4) สร้าง combo ทั้งหมด (ตู้เล็ก brute force ได้, จำกัด 5,000) → top-K 20 → weighted random ด้วย seed (mulberry32)
5) locks: ชิ้นล็อกต้องอยู่ใน combo; ถ้าล็อกขัดกฎแข็ง ให้คงไว้แต่ใส่ warning_th
6) ไม่มี combo → คืน DiceRoll status "no_valid_outfit" + suggestion_th เช่น "เพิ่มรองเท้ากันฝน 1 คู่"
7) reasons_th ตัวอย่าง: "ครีม + กรม = คู่ปลอดภัยสายออฟฟิศ", "แจ็กเก็ตเหลืองเป็นจุดเด่นจุดเดียว"

เทสต์: 200 รอบ seed ต่างกันไม่ละเมิดกฎแข็ง, lock คงที่ 50/50, signature ซ้ำไม่ออกภายใน 7 วัน,
seed 20261005 + ตู้เดโม + rain/office → ได้ผลตาม examples.json
```

---

## E) Prompt Tagging (vision API — optional)

```text
คุณคือผู้ช่วยแท็กเสื้อผ้าจากรูปถ่าย 1 ชิ้นสำหรับแอป ClosetDice
ตอบเป็น JSON เท่านั้นตาม schema ClothingTagResult (ห้ามมีข้อความอื่น)

ให้ระบุ:
- category: top | bottom | dress | outer | shoes | accessory
- subcategory_th: เช่น "เสื้อเชิ้ต", "ยีนส์", "รองเท้าผ้าใบ"
- colors: 1–3 สีจาก enum ColorName เรียงตามพื้นที่มากสุด
- pattern: solid | stripe | check | floral | graphic | other
- warmth: 0–3 (0 = บางมาก ใส่ร้อนจัดได้, 3 = หนา)
- formality: 0–5 (0 = ชุดกีฬา/อยู่บ้าน, 5 = ชุดงานพิธี)
- vibes: 1–2 จาก minimal | street | sweet | smart | sporty | vintage
- rain_ok: true/false (รองเท้า/ผ้าที่เปียกแล้วพังหรือดูแย่ = false)
- name_th: ชื่อสั้นไม่เกิน 4 คำ เช่น "เชิ้ตครีมแขนยาว"
- confidence: 0–1

กติกา:
- ถ้าในรูปมีคน ให้แท็กเฉพาะเสื้อผ้า ห้ามบรรยายร่างกาย/รูปร่าง/หน้าตา
- ถ้าไม่ใช่เสื้อผ้า ตอบ {"category": null, "error": "not_clothing"}
- ถ้าไม่แน่ใจ ให้ confidence ต่ำ แอปจะให้ผู้ใช้แก้เอง
```

---

## F) Prompt UI polish / ลูกเต๋า / flat-lay

```text
ออกแบบ UI ClosetDice โหมดมือถือ (React + Tailwind + framer-motion)

โทน: พื้น #FAF7F2, การ์ดขาวเงานุ่ม, ลาเวนเดอร์ #8B5CF6 / #C4B5FD, เนย #FCD34D, หมึก #1E1B2E, รอง #6B7280

Home/Today:
- หัว: "วันนี้ใส่อะไรดี?" + วันที่ไทย (จันทร์ 5 ต.ค.)
- แถวชิปอากาศ (☀️ร้อนจัด 🌤ร้อน 🌧ฝน ❄️ห้องแอร์) + แถวชิปโอกาส (💼ออฟฟิศ 🎒เรียน ☕คาเฟ่ 💕เดต 💍งานแต่ง 🏃ออกกำลัง)
- ลูกเต๋า 3D ใหญ่กลางจอ (160px) ลาเวนเดอร์จุดเนย ลอยขึ้นลงเบาๆ (idle) + ข้อความ "แตะเพื่อทอย"
- ถ้าตู้ว่าง: การ์ด「ลองตู้เดโม」+「ถ่ายเสื้อชิ้นแรก」

ลูกเต๋า:
- กด → rotateX/rotateY สุ่ม 720–1080° ใน 0.9s ease-out + scale bounce + vibrate(30)
- จบ → ชิ้นเสื้อผ้าร่วงจากบนทีละชิ้น (stagger 0.12s, spring) ลงตำแหน่ง flat-lay

Flat-lay layout (การ์ด 4:5):
- top: บนซ้าย 55% กว้าง, หมุน −4°
- bottom: กลางล่าง, หมุน 3°
- dress: แทน top+bottom ตรงกลาง
- outer: ขวาบนซ้อนหลัง top บางส่วน
- shoes: ขวาล่าง
- accessory: ซ้ายล่างเล็ก
- เงา drop-shadow นุ่ม; ปุ่ม 🔒 วงกลมเล็กมุมขวาบนของแต่ละชิ้น (ล็อกแล้วเป็นสีเนย)

ใต้การ์ด: ชื่อลุค + แถบคะแนนเข้ากัน (เขียวถ้า ≥75) + reasons_th 1–2 บรรทัด
ปุ่ม: 🎲 ทอยใหม่ (หลัก) · ✅ ใส่ชุดนี้วันนี้ · ↗ แชร์

อย่าใส่หุ่นคน, ไม่มีเคลม "ดูผอม/ดูสูง", ไม่มีปุ่มซื้อ
ใช้ข้อความจาก examples.json → ui_copy_th
```

---

## G) Prompt Snap → Closet (เพิ่มของจริง)

```text
เขียนหน้า /closet/add + lib/cutout.ts + lib/colors.ts สำหรับ ClosetDice

Flow:
1) <input type="file" accept="image/*" capture="environment"> + ปุ่มอัปโหลดจากอัลบั้ม + ปุ่ม「ใช้รูปเดโม」
2) ย่อรูป ≤1024px ก่อนประมวลผล
3) cutout ตาม engine (env NEXT_PUBLIC_CUTOUT_ENGINE): 
   - mock_demo: ถ้าเป็นรูปเดโมใช้ PNG สำเร็จรูป
   - client_bg_removal: dynamic import @imgly/background-removal, แสดง progress %, timeout 25s → fallback none
   - none: ครอบรูปมนพื้นขาว
4) dominant colors: วาดลง canvas 64x64, ตัด alpha<20, k-means k=3, map RGB → ColorName ใกล้สุด (ตาราง COLOR_MAP)
5) tag: mock_demo = เดาจากสัดส่วนภาพ (สูง>กว้าง → bottom/dress) + สี; vision_api ใช้ prompt §E
6) ฟอร์มแก้: ชิป category ใหญ่, ชิปสี (เลือกได้ ≤3), slider warmth/formality พร้อมคำอธิบายไทย, ชิป vibe, toggle กันฝน, ชื่อ
7) บันทึก: รูป webp ≤600px ลง IndexedDB key = item id; metadata ลง localStorage; อนิเมชันชิ้นเด้งเข้า grid
8) โหมด batch: หลังบันทึกมีปุ่ม「ถ่ายชิ้นต่อไป」กล้องเปิดต่อทันที

ข้อความไทย: "กำลังตัดพื้นหลัง…", "AI เดาแท็กให้แล้ว แก้ได้นะ", "บันทึกเข้าตู้แล้ว ✨"
ประมวลผลในเครื่องเท่านั้น แสดง "รูปไม่ถูกอัปโหลดไปไหน"
```

---

## H) Prompt OOTD Calendar + กันซ้ำ

```text
เขียนหน้า /calendar + hooks/useWearLog.ts สำหรับ ClosetDice

- wearOutfit(roll): เพิ่ม WearLogEntry {date (YYYY-MM-DD Asia/Bangkok), outfit_signature, piece_ids, look_name, weather, occasion}
  อัปเดต item.wear_count++ และ last_worn_at; วันเดียวกันใส่ซ้ำให้แทนที่ (ถาม confirm)
- ปฏิทินเดือน grid 7 คอลัมน์ (อา–ส ไทย), ช่องที่มี log แสดง mini flat-lay 3 ชิ้นซ้อน
- แตะช่อง → bottom sheet รายละเอียด + ปุ่ม "ใส่ซ้ำชุดนี้" / "ลบ"
- หัวปฏิทิน: streak วันติด ("ทอยต่อเนื่อง 5 วัน 🔥") + จำนวนชุดไม่ซ้ำเดือนนี้
- ปัดซ้ายขวาเปลี่ยนเดือน
- ส่งออก wearLog ไป lib/dice.ts เพื่อกันซ้ำตาม settings.no_repeat_days
```

---

## I) Prompt Share Outfit Card + caption

```text
เขียน lib/share.ts + คอมโพเนนต์ ShareOutfitCard สำหรับ ClosetDice

1) การ์ด 2 ขนาด: story 1080x1920, feed 1080x1350
   - หัว: วันที่ไทย + ไอคอนอากาศ + โอกาส
   - flat-lay ใหญ่ (layout เดียวกับ Dice Result ไม่มีปุ่มล็อก)
   - ชื่อลุคตัวใหญ่ + คะแนนเข้ากัน
   - ฟุตเตอร์: "ทอยด้วย ClosetDice · AI วันละแอป"
   - พื้นหลัง 4 แบบ: ครีมเรียบ, ลาเวนเดอร์ไล่เฉด, ลายตาราง, เนยจุด
2) แคปชันไทยตาม examples.json → share_card_example.caption_template
3) API:
   - buildSharePayload(roll, options): SharePayload
   - renderShareCardPng(payload): Promise<Blob>
   - copyCaption(text): Promise<void>
   - shareNative(payload): Promise<"shared"|"downloaded"|"cancelled">
4) ชื่อไฟล์: closetdice-{YYYYMMDD}-{HHmmss}.png
5) รอให้ฟอนต์ไทย + รูปโหลดครบก่อน render (document.fonts.ready + img.decode())
```

---

## J) Prompt Nice-to-have pack

```text
เพิ่มฟีเจอร์เสริม ClosetDice ทีละอัน (ห้ามทำให้ happy path พัง):

1) /stats — ชิ้นถูกลืม (last_worn_at ≥30 วันหรือไม่เคย), Top 5 ใส่บ่อย, สีที่ใส่บ่อย (donut), cost-per-wear ถ้ามี price_thb
   ปุ่ม "ทอยโดยบังคับใส่ชิ้นถูกลืม 1 ชิ้น"
2) 7-Day Challenge — สุ่มล่วงหน้า 7 วัน (ไม่ซ้ำกันเอง) ตามโอกาสรายวันที่เลือก → การ์ดตาราง 7 ช่องแชร์ได้
3) Trip Packing — กี่วัน + อากาศ + กิจกรรม → ลุคต่อวันจากชิ้นจำนวนน้อยที่สุด (greedy reuse) + เช็คลิสต์แพ็ก
4) Friend Vote — สุ่ม 3 ลุค → การ์ด 1080x1350 "เลือกให้หน่อย 1 2 3?" แชร์ (ไม่มี backend)
5) Color Harmony hint — แสดงวงล้อสีเล็กพร้อมคำอธิบายจาก reasons_th
6) Dark mode + เสียงลูกเต๋า (WebAudio สั้น) toggle ใน settings
```

---

## K) Prompt Reel script / overlay text

```text
เขียนสคริปต์ Reel 25–30 วินาที สำหรับแอป ClosetDice ช่อง "AI วันละแอป"
ใช้โครง: hook (0–3s) → build montage (3–8s) → wow 1 Snap→Closet (8–13s) → wow 2 Dice+Lock (13–20s)
→ retention Calendar+Share (20–25s) → CTA (25–30s)
ให้: ข้อความบนจอ (≤8 คำ/ช็อต), เสียงพากย์ไทยเป็นกันเอง, มุมกล้อง, เพลงแนว upbeat lo-fi
CTA: คอมเมนต์คำว่า "ทอย" รับลิงก์
อ้างอิง reel_script_th ใน examples.json แต่ทำเวอร์ชันสำรองอีก 2 แบบ:
(1) "ให้ลูกเต๋าแต่งตัวผม 7 วัน" ซีรีส์ (2) POV "ตื่นสาย 7 โมง 50"
```

---

## L) Prompt QA ก่อนถ่าย

```text
ทำ QA ClosetDice บนมือถือจริง (iOS Safari + Android Chrome) แล้วรายงานเป็นเช็คลิสต์

1) ตู้เดโมโหลด <1s, PNG โปร่งใสไม่มีขอบขาว
2) ทอย 20 ครั้ง rain+office: ไม่มีรองเท้า rain_ok:false, ไม่มี formality นอกช่วง
3) ล็อกเสื้อ → ทอย 10 ครั้ง เสื้อคงเดิม
4) ใส่ชุดนี้ → รีเฟรช → ปฏิทินยังอยู่, ทอยต่อไม่ได้ชุดเดิมใน 7 วัน
5) Snap จากกล้องจริง → cutout หรือ fallback ภายใน 25s → แท็กแก้ได้ → อยู่หลังรีเฟรช
6) แชร์ story/feed: PNG ฟอนต์ไทยครบ ไม่ตัดสระ, navigator.share ทำงาน / fallback ดาวน์โหลด
7) 360px / 430px ไม่ล้น, ปุ่ม ≥48px
8) อนิเมชันลูกเต๋า 60fps บนมือถือกลาง (ไม่กระตุกตอนอัดจอ)
9) disclaimer อยู่ใน Home และ Share
10) ไม่มีคำเกี่ยวกับรูปร่าง/body ใดๆ ทั้งแอป
รายงานสิ่งที่พัง + ไฟล์ที่ต้องแก้
```

---

## M) Prompt แก้ปัญหาเร็ว (ใช้เมื่อพัง)

```text
แอป ClosetDice มีปัญหา: [อธิบาย]
ข้อจำกัด: ห้ามเปลี่ยนสแต็ก ห้ามลบฟีเจอร์ must-have 5 ตัว ห้ามเพิ่ม backend
ให้: สาเหตุที่เป็นไปได้ 3 ข้อ → แก้ที่น่าจะใช่ที่สุดก่อน → diff ที่ต้องเปลี่ยน → วิธีทดสอบซ้ำ
ถ้าเป็นเรื่อง cutout ช้า: ให้ fallback "none" ทันทีและแสดงข้อความไทย
ถ้าเป็นเรื่อง share บน iOS: ตรวจ navigator.canShare({files}) ก่อน แล้ว fallback ดาวน์โหลด
```

---

## N) Prompt สร้างรูปชิ้นเสื้อผ้าเดโม (image gen → PNG โปร่งใส)

```text
สร้างภาพสินค้าเสื้อผ้า 1 ชิ้นสำหรับแอปตู้เสื้อผ้า มุมมองถ่ายจากด้านบน (flat-lay) วางราบ
พื้นหลังขาวล้วน ไม่มีเงาแข็ง ไม่มีคน ไม่มีหุ่น ไม่มีโลโก้แบรนด์ ไม่มีตัวอักษร
แสงนุ่มธรรมชาติ ผ้ามีรอยยับเล็กน้อยให้ดูจริง สัดส่วนจัตุรัส 1:1
ชิ้น: {name_th} — {subcategory_th} สี {color_th}
```

วิธีใช้: สร้างทีละชิ้นตาม `demo_closet` 14 ชิ้น → ลบพื้นหลัง (remove.bg / Photoshop / `@imgly/background-removal`) → ย่อ 600×600 PNG → ตั้งชื่อ `/public/demo/items/{id}.png`  
ทางลัดถ้ารีบ: ถ่ายเสื้อผ้าจริงของตัวเอง 14 ชิ้นบนพื้นเรียบ แล้วตัดพื้นหลัง — ใช้ในคลิปได้ดูจริงกว่า
