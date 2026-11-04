# Work-order prompts — LabelLens

**P0 Setup** — สร้าง Expo (React Native) + TypeScript หรือ Next.js PWA มือถือ ใช้ design tokens ใน prd.md ตัวเลขใหญ่หนา ทุกหน้าภาษาไทย สร้าง `lib/logic.ts` โดยพอร์ตจาก `reference/labellens.py` ทีละฟังก์ชัน พร้อม unit test ให้ค่าตรงกับ `reference/tests.py` (เช่น ชาเขียวหวาน = 10 ช้อน, เกรด C 50)

**P1 Onboarding** — 3 การ์ด: เลือกสิ่งที่แพ้ (chip: นม ไข่ ถั่วลิสง ถั่วเหลือง แป้งสาลี กุ้ง ปลา งา), เป้าหมาย (ลดหวาน/ลดเค็ม/สมดุล/โหมดเด็ก), โควตาต่อวัน (ค่าเริ่ม 24 g / 2000 mg แก้ได้) เก็บเป็น `UserProfile` ใน local storage

**P2 Camera** — กล้องพร้อมกรอบ "ตารางโภชนาการ" และ "ส่วนประกอบ" (ถ่าย 1–2 รูป) + ช่องสแกนบาร์โค้ด (optional) ส่งรูปไป `/api/read-label`

**P3 Vision system prompt** —
```
คุณคือผู้อ่านฉลากอาหารไทย อ่านจากภาพเท่านั้น ห้ามเดา ห้ามคำนวณ
คืน JSON ตาม schema Label เท่านั้น: name_th, form (drink|solid), serving_size (g หรือ ml), servings_per_pack,
per_serving{kcal,sugar_g,fat_g,sodium_mg}, ingredients_th (คัดลอกตามจริง), additives (รหัส E/INS ที่เห็น เขียนเป็น E###),
ocr_confidence 0-1. ถ้าค่าใดอ่านไม่ออก ใส่ null และลด ocr_confidence ถ้าไม่ใช่ฉลากอาหาร คืน {"error":"not_label"}
```
validate ด้วย `schemas.json#/$defs/Label` ถ้าไม่ผ่านหรือ confidence < 0.7 → หน้า "ยืนยันตัวเลข" ให้แก้ก่อน

**P4 Result screen (WOW)** — แอนิเมชันช้อนชาหล่นลงแก้วตามจำนวน `sugar_spoons(pack_totals.sugar_g)` (ทีละช้อน 120ms + เสียงติ๊ง), จากนั้นเกรด A–E เด้งขึ้น, ไฟ 3 ดวง, quota bar (`daily_pct`) วิ่งจาก 0, "เดิน X นาที" (`walk_off`) ปุ่ม: เทียบอีกชิ้น / เพิ่มลงวันนี้ / แชร์

**P5 Allergen & Additive** — ไฮไลต์คำที่ตรง `allergen_hits` ในข้อความส่วนประกอบเป็นแถบแดง + banner "⚠️ มี นม" ; รายการรหัส E จาก `decode_additives` แสดงเป็น chip (info เทา / caution เหลือง / unknown ขีด)

**P6 Battle** — สองคอลัมน์ ช้อนชาเรียงซ้าย-ขวา มงกุฎบนผู้ชนะ (`battle`) แสดง "ต่างกัน N ช้อน · ราคาต่าง ฿X" ถ้า tie แสดง "เสมอ"

**P7 Diary + Streak + Swap** — Diary วันนี้รวม `budget_day`, แถบเกิน 100% เป็นแดง; `week_streak` แสดงไฟ 7 วัน; บนหน้า result ถ้า `swap_suggest` ไม่เป็น null โชว์การ์ด "สลับเป็น ... -N ช้อน" (ใช้ประวัติที่ผู้ใช้เคยสแกนเป็น candidates)

**P8 Reel Cards** — render การ์ด 1080×1920 ตาม `ReelCard` 5 แบบ (sugar_spoons, battle, day_total, swap, streak) ตัวเลขใหญ่กลางจอ disclaimer ล่างเสมอ ปุ่ม save/share

**P9 QA** — โหลด `examples.json` เป็น fixture โหมด demo (ไม่ต้องใช้กล้อง) ทุก screen ต้องแสดงค่าตรงกับตัวอย่าง; ทดสอบรูปที่ไม่ใช่ฉลาก, ค่า null, servings_per_pack = 0 (ต้อง error สวย ๆ)
