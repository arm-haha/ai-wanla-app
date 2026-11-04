# ScamScan (มิจฉาสแกน) — ชุดส่งมอบเช้า (AI วันละแอป)

**วันที่:** 2026-10-16 (Asia/Bangkok) · **ช่อง:** AI วันละแอป · **สถานะ:** พร้อม gen วันนี้
**ฮุค Reel:** แม่ส่ง SMS "บัญชีถูกระงับ" มาถาม… วางปุ๊บ มิเตอร์แดง 90/100 พร้อมชี้ว่าหลอกตรงไหน 🚨

เดโมกล่องข้อความป้าแดง (สมมติ): 4 ข้อความ → **90 / 85 / 55 / 0** → Link X-Ray "เว็บจริงคือ kasikornbank.com" → Family Card ส่ง LINE → Call Shield 80 → Quiz 4/5 → Wrapped ต.ค. เช็ก 8 เจอเสี่ยง 6

## ไฟล์
| ไฟล์ | ใช้ทำอะไร |
|---|---|
| `prd.md` | สเปก: ปัญหา ไวรัล persona ฟีเจอร์ กติกาคอร์ ตัวเลขล็อก หน้าจอ UI เทค ความปลอดภัย acceptance ความเสี่ยง แผนวันเดียว |
| `prompts.md` | Prompt A–J (codegen ทั้งแอปทีละส่วน, QA, หน้าอัด Reel) + runtime K–M (OCR, อธิบายผู้สูงอายุ, แคปชัน) |
| `schemas.json` | JSON Schema draft 2020-12, 29 defs (ScanInput, Rule, Brand, ScanResult, LinkXray, ActionPlan, FamilyCard, Quiz*, CallShield, Wrapped, LocalStore, Ai*) |
| `examples.json` | 13 rules · 8 แบรนด์ allowlist · demo inbox · ผลสแกนทุกข้อความ · X-Ray 4 ลิงก์ · Family Card · Quiz deck 10 ใบ · Call Shield · History/Wrapped · UI copy ไทย · สคริปต์ Reel · expect_locked (validate กับ schema แล้ว 68 objects 0 error) |
| `reference/` | `scam.py` (คอร์ deterministic) · `fixtures.py` · `schema.py` · `build.py` (สร้าง+ตรวจ JSON) · `tests.py` (18 tests ผ่าน) |

ใช้งาน: วาง Prompt A + แนบ `prd.md`, `schemas.json`, `examples.json`, `reference/scam.py` → ส่ง Prompt B–J ต่อทีละอัน
ตรวจซ้ำ: `cd reference && python3 build.py && python3 tests.py`

## ฟีเจอร์
**Must-have:** ① Paste → Scam Meter (⭐ wow) ② Red-Flag Highlighter ③ Link X-Ray ④ Action Card ⑤ Family Alert Card → LINE
**Nice-to-have:** ⑥ Quiz จริงหรือหลอก ⑦ Call Shield ⑧ History + Wrapped ⑨ Grandparent Mode ⑩ AI อธิบายเพิ่ม

## สี
`#0B1220` night · `#111A2E` panel · `#F8FAFC` paper · `#DC2626` siren · `#F97316` amber · `#FACC15` caution · `#16A34A` safe · `#38BDF8` shield

> คะแนนเป็นสัญญาณเตือน ไม่ใช่คำตัดสิน · แอปไม่เปิดลิงก์ในข้อความ · allowlist โดเมนและเบอร์ AOC 1441 ต้องตรวจกับเว็บทางการก่อนปล่อย · บุคคล ผู้ส่ง โดเมน และข้อความเดโมทั้งหมดเป็นตัวอย่างสมมติ
