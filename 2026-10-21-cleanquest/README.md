# CleanQuest (ห้องรกหาย) — ชุดส่งมอบเช้า (AI วันละแอป)

**วันที่:** 2026-10-21 (Asia/Bangkok) · **ช่อง:** AI วันละแอป · **สถานะ:** พร้อม gen วันนี้
**ฮุค Reel:** ห้องกูได้ 12/100 😭 ถ่ายรูปเดียว AI ให้คะแนนความรก แล้วแปลงเป็นเกม จนได้ 94 ใน 38 นาที

เดโมห้องหอฟ้า (สมมติ) คืนวันพุธ 20:30: สแกนเจอ 8 จุดรก → **12/100 ห้องวิกฤต 🚨** → โหมด 🔥 เควส 8 อัน 3 สปรินต์ (14/12/12 นาที) → timer สกอร์ขึ้นสด 12→46→80 → สแกนหลัง **94 ห้องโชว์ ✨** → การ์ด "ห้องเกิดใหม่ 🦋 +82" → หูฟังเก่าขายได้ ฿770 → แบ่งงานกับมุก 20/18 นาที → 283 XP Lv3 streak 7

## ไฟล์
| ไฟล์ | ใช้ทำอะไร |
|---|---|
| `prd.md` | ปัญหา ไวรัล persona 10 ฟีเจอร์ กติกาคอร์ หน้าจอ เทค ความเป็นส่วนตัว acceptance แผนวันเดียว |
| `prompts.md` | Prompt A–J (codegen ทั้งแอปทีละส่วน, QA, หน้าอัด Reel) + runtime K–M (vision scan, pep talk, แคปชัน) |
| `schemas.json` | JSON Schema draft 2020-12, 28 defs (ScanInput, MessScore, QuestPlan, TimerState, GlowUpCard, DeclutterItem/Result, ChoreShare, Session, Progress, WeeklyReset, Wrapped, LocalStore, Ai*) |
| `examples.json` | hotspot 13 ชนิด · ผลสแกนก่อน/หลัง · แผน 3 โหมด · timer 3 สถานะ · glow card · declutter 5 ชิ้น · แบ่งงาน · sessions · progress · Wrapped · ตัวอย่าง AI · UI copy ไทย · สคริปต์ Reel · expect_locked (validate 35 objects 0 error) |
| `reference/` | `cleanquest.py` (คอร์ deterministic) · `fixtures.py` · `schema.py` · `build.py` · `tests.py` (25 tests ผ่าน) |

ใช้งาน: วาง Prompt A + แนบ `prd.md`, `schemas.json`, `examples.json`, `reference/cleanquest.py` → ส่ง Prompt B–J ต่อทีละอัน
ตรวจซ้ำ: `cd reference && python3 build.py && python3 tests.py`

## ฟีเจอร์
**Must-have:** ① Room Snap → Mess Score + Hotspot Pins (⭐ wow) ② Quest Plan สปรินต์ 15 นาที 3 โหมด ③ Timer Mode สกอร์ขึ้นสด ④ Before/After Glow-up Card ⑤ Declutter Decider + ข้อความขาย
**Nice-to-have:** ⑥ แบ่งงานรูมเมท → LINE ⑦ Streak + XP/Level ⑧ Weekly Reset ⑨ Room Wrapped ⑩ Pep Talk 3 สไตล์

## สี
`#F5F7FF` mist · `#1E1B4B` ink · `#A78BFA` lilac · `#22D3EE` sparkle · `#FDE047` lemon · `#F43F5E` mess · `#10B981` clean

## กับดัก
- **AI ให้คะแนนมั่ว/ไม่คงที่:** AI เสนอแค่จุดรก+ระดับ ผู้ใช้ยืนยันชิปก่อน สกอร์มาจากสูตรเสมอ ถ่ายรูปเดิมได้ผลเดิม
- **รูปห้องหลุดข้อมูลส่วนตัว:** ชื่อ/ที่อยู่บนกล่องพัสดุ เอกสาร หน้าต่างเห็นวิว → ปุ่มเบลอก่อนแชร์ + ไม่เก็บรูปบนเซิร์ฟเวอร์
- **ไม่อยากโชว์ห้องจริงในคลิป:** จัดห้องรกจำลองสำหรับอัด หรือใช้ /reel-demo
- **timelapse ไม่ satisfying:** ตั้งกล้องมุมสูงนิ่งๆ มุมเดียวทั้งก่อนและหลัง แสงเดียวกัน
- **ราคาขายเป็นค่าประมาณ:** ระบุบนการ์ด ให้เช็กราคาตลาดก่อนโพสต์
- **มุกทำให้อาย:** โทนแซวเบาๆ ไม่ด่าคนรก ไม่มีคำเหยียด

> บุคคล ห้อง ประวัติ และตัวเลขในเดโมทั้งหมดเป็นตัวอย่างสมมติ
