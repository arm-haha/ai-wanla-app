# FridgeChef (ตู้เย็นเชฟ) — ชุดส่งมอบเช้า (AI วันละแอป)

**วันที่:** 2026-10-14 (Asia/Bangkok) · **ช่อง:** AI วันละแอป · **สถานะ:** พร้อม gen วันนี้
**ฮุค Reel:** เปิดตู้เย็นถ่ายรูปเดียว… AI บอกเลยว่าคืนนี้ทำเมนูไหนได้ ไม่ต้องออกไปซื้อเพิ่ม 🍳

เดโมตู้เย็นปุ๊ก (สมมติ): 12 อย่าง → ใช้วันนี้ 4 อย่าง → **กะเพราหมูสับไข่ดาว** ช่วยของ ฿60 → Cook Mode 6 ขั้น → ลิสต์ซื้อของ ~฿80 → Wrapped ต.ค. ประหยัด ฿225

## ไฟล์
| ไฟล์ | ใช้ทำอะไร |
|---|---|
| `prd.md` | สเปก: ปัญหา ไวรัล persona ฟีเจอร์ กติกาคอร์ ตัวเลขล็อก หน้าจอ UI เทค ความปลอดภัย acceptance ความเสี่ยง แผนวันเดียว |
| `prompts.md` | Prompt A–J (codegen ทั้งแอป ทีละส่วน, QA, แก้บั๊ก, หน้าอัด Reel) + runtime K–M (vision, สูตร AI, แคปชัน) |
| `schemas.json` | JSON Schema draft 2020-12, 33 defs (Detection, InventoryItem, Recipe, MenuMatch, CookMode, Radar, ShoppingList, DiceResult, Wrapped, ShareCard, LocalStore, Ai*) |
| `examples.json` | catalog 17 วัตถุดิบ · 12 สูตรไทย · demo input · ผลลัพธ์ทุกฟีเจอร์ · UI copy ไทย · สคริปต์ Reel · 16 test vectors (validate กับ schema แล้ว 0 error) |
| `reference/` | `fridge.py` (คอร์ deterministic) · `fixtures.py` · `schema.py` · `build.py` (สร้าง+ตรวจ JSON) · `tests.py` (17 tests ผ่าน) |

ใช้งาน: วาง Prompt A + แนบ `prd.md`, `schemas.json`, `examples.json`, `reference/fridge.py` → ส่ง Prompt B–J ต่อทีละอัน
ตรวจซ้ำ: `cd reference && python3 build.py && python3 tests.py`

## ฟีเจอร์
**Must-have:** ① Fridge Snap → Chips (⭐ wow) ② Menu Match 3 เมนู ③ Cook Mode จับเวลา ④ Use-First Radar ⑤ ลิสต์ซื้อของ → LINE
**Nice-to-have:** ⑥ 🎲 สุ่มเมนู ⑦ Waste Wrapped ⑧ Staples ⑨ Share cards ⑩ โหมดพิมพ์แทนถ่าย

## สี
`#F7FAFC` พื้น · `#0F172A` ink · `#38BDF8` ice · `#EF4444` tomato · `#22C55E` basil · `#FBBF24` yolk

> วันหมดอายุในแอปเป็นค่าประมาณ — แอปต้องเตือนให้ดม/ดูก่อนกินเสมอ · persona และตัวเลขเดโมเป็นข้อมูลสมมติ
