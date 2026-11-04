# LeafDoc (หมอใบไม้) — ชุดส่งมอบเช้า (AI วันละแอป)

**วันที่:** 2026-10-19 (Asia/Bangkok) · **ช่อง:** AI วันละแอป · **สถานะ:** พร้อม gen วันนี้
**ฮุค Reel:** ต้นไม้ซื้อมาตายทุกต้น… ถ่ายใบเดียว แอปบอกเลยว่าป่วยเพราะอะไร + แผนชุบชีวิต 7 วัน 🌿

เดโมป่าคอนโดของบีม (สมมติ): 3 ต้น → **55 🤒 / 70 🌤️ / 100 🌿** → มอนมอน "รดน้ำมากไป 50%" → ควรรดทุก 12 วัน (บีมรดทุก 7) → พลูพลูเลยกำหนด 4 วัน → Light 640 → 2,560 lux → Room Match เศรษฐีเรือนใน 100 → Glow-up 14 วัน **55 → 94** ใบใหม่ 2 ใบ

## ไฟล์
| ไฟล์ | ใช้ทำอะไร |
|---|---|
| `prd.md` | สเปก: ปัญหา ไวรัล persona 10 ฟีเจอร์ กติกาคอร์ ตัวเลขล็อก หน้าจอ UI เทค ความปลอดภัย acceptance แผนวันเดียว |
| `prompts.md` | Prompt A–J (codegen ทั้งแอปทีละส่วน, QA, หน้าอัด Reel) + runtime K–M (vision, care chat, แคปชัน) |
| `schemas.json` | JSON Schema draft 2020-12, 35 defs (Species, Symptom, Cause, Plant, CheckupInput, Diagnosis, WaterStatus, RescuePlan, LightReading, RoomMatch, GlowUpCard, Wrapped, LocalStore, Ai*) |
| `examples.json` | 9 ชนิดต้น · 15 อาการ · 10 สาเหตุ+แผน 7 วัน · demo 3 ต้น · ผลตรวจ · ตารางรดน้ำ · แผน · Glow-up · Light · Pet · Room Match · Log/Wrapped · UI copy ไทย · สคริปต์ Reel · expect_locked (validate กับ schema แล้ว 74 objects 0 error) |
| `reference/` | `leaf.py` (คอร์ deterministic) · `fixtures.py` · `schema.py` · `build.py` (สร้าง+ตรวจ JSON) · `tests.py` (20 tests ผ่าน) |

ใช้งาน: วาง Prompt A + แนบ `prd.md`, `schemas.json`, `examples.json`, `reference/leaf.py` → ส่ง Prompt B–J ต่อทีละอัน
ตรวจซ้ำ: `cd reference && python3 build.py && python3 tests.py`

## ฟีเจอร์
**Must-have:** ① Leaf Snap → Health Score (⭐ wow) ② Symptom Doctor ③ แผนชุบชีวิต 7 วัน ④ Smart Water Schedule ⑤ Glow-up Card
**Nice-to-have:** ⑥ Light Meter ⑦ Pet-safe Check ⑧ Room Match ⑨ My Jungle + Level + streak ⑩ Plant Wrapped + AI Care Chat

## สี
`#F7F5EE` cream · `#14532D` forest · `#22C55E` leaf · `#A3E635` lime · `#FBBF24` sun · `#C2410C` clay · `#0EA5E9` water · `#1C1917` ink

## กับดัก
- **วินิจฉัยผิดแล้วต้นตาย = ดราม่า:** ใช้คำว่า "น่าจะ" + % + disclaimer ทุกหน้า ให้ผู้ใช้ยืนยันชิปอาการก่อนคำนวณ
- **AI vision มั่ว:** AI แค่เสนอ tag ใน enum เท่านั้น คะแนนมาจาก engine เสมอ
- **ข้อมูลพิษต่อสัตว์:** `verified:false` ทุกต้นจนกว่าจะตรวจกับ ASPCA เอง
- **Light Meter ไม่ใช่เครื่องวัดจริง:** กล้องปรับ exposure อัตโนมัติ ใช้เทียบมุมในบ้านเท่านั้น
- **รอบรดน้ำเป็นค่าเริ่มต้นประมาณการ** (ฐานต่อชนิดต้นเป็นค่าทั่วไป ไม่ได้อ้างงานวิจัย) ย้ำ finger test เสมอ
- **Glow-up ต้องรอจริง 14 วัน:** อัดฉากใบเหลืองวันนี้ไว้เลย หรือใช้ demo fixture แล้วบอกในคลิปว่าเป็นตัวอย่าง

> บุคคล ต้นไม้ ค่าแสง และประวัติในเดโมทั้งหมดเป็นตัวอย่างสมมติ
