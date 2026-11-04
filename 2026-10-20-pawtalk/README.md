# PawTalk (แมวหมาพูดได้) — ชุดส่งมอบเช้า (AI วันละแอป)

**วันที่:** 2026-10-20 (Asia/Bangkok) · **ช่อง:** AI วันละแอป · **สถานะ:** พร้อม gen วันนี้
**ฮุค Reel:** แมวกูด่าอะไรกูอยู่ทุกเช้า?? ถ่ายรูปเดียว แอปแปลเป็นคำพูดไทยเลย 🐾

เดโมบ้านแพรว (สมมติ) 07:05: ส้มฉุนจ้องชาม ร้องลั่น หางสะบัด → **หิว 62% · หงุดหงิด 23% · อยากให้สนใจ 15%** · vibe 38 → 👑 "ทาสสส อีก 25 นาทีข้าวต้องมา ช้า 1 วิหักเงินเดือน" → สลับ 🎭 "ไม่ได้กินมา 300 ปีแล้ว…จะเป็นลมแล้วนะแพรว" → หลังกินข้าว vibe **96** → Duet กับชิบะข้าวปั้น → Care board "ถ่ายพยาธิเลย 7 วัน" 😱 → 260 kcal/68 g ต่อวัน → อายุคน 28

## ไฟล์
| ไฟล์ | ใช้ทำอะไร |
|---|---|
| `prd.md` | ปัญหา ไวรัล persona 10 ฟีเจอร์ กติกาคอร์ หน้าจอ เทค ความปลอดภัย acceptance แผนวันเดียว |
| `prompts.md` | Prompt A–J (codegen ทั้งแอปทีละส่วน, QA, หน้าอัด Reel) + runtime K–M (vision cue, เกลาบับเบิล, แคปชัน) |
| `schemas.json` | JSON Schema draft 2020-12, 32 defs (Pet, SnapInput, MoodResult, ThoughtBubble, Duet, CareItem/Status, HealthResult, FoodPlan, HumanAge, Wrapped, PetIdCard, MemeCard, LocalStore, Ai*) |
| `examples.json` | cue 30 ตัว (แมว 16/หมา 14) · อาการ 18 · บับเบิล 63 template · เดโม 2 ตัว · ผลอารมณ์ · persona flip · duet · care board · health · food · อายุ · ID/meme card · Wrapped · UI copy ไทย · สคริปต์ Reel · expect_locked (validate 39 objects 0 error) |
| `reference/` | `pawtalk.py` (คอร์ deterministic) · `fixtures.py` · `schema.py` · `build.py` · `tests.py` (25 tests ผ่าน) |

ใช้งาน: วาง Prompt A + แนบ `prd.md`, `schemas.json`, `examples.json`, `reference/pawtalk.py` → ส่ง Prompt B–J ต่อทีละอัน
ตรวจซ้ำ: `cd reference && python3 build.py && python3 tests.py`

## ฟีเจอร์
**Must-have:** ① Pet Snap → Thought Bubble (⭐ wow) ② Mood Meter + Vibe ③ Persona Flip + Meme Card ④ Care Board + เตือน ⑤ Health Check คัดกรอง
**Nice-to-have:** ⑥ Duet น้องคุยกัน ⑦ Food Calculator ⑧ อายุเทียบคน + Pet ID Card ⑨ Mood Diary + streak/XP ⑩ Pet Wrapped

## สี
`#FFF8F0` cream · `#3B2A20` cocoa · `#F97316` orange · `#FDBA74` peach · `#34D399` mint · `#60A5FA` sky · `#EC4899` berry · `#DC2626` alert

## กับดัก
- **คนเชื่อว่าแปลใจจริง:** ติด "แปลเพื่อความบันเทิงจากภาษากาย" ทุกการ์ด และพูดในคลิปด้วย
- **AI มั่ว cue:** AI เลือกได้แค่ cue ใน enum และผู้ใช้ยืนยันชิปก่อน อารมณ์/% มาจาก engine เสมอ
- **Health Check ถูกมองเป็นหมอ:** คัดกรอง 4 ระดับเท่านั้น ไม่มียา/การรักษา ฉุกเฉินส่งไปโรงพยาบาลสัตว์ (ข้อมูลอาการเป็นแนวทางทั่วไป ควรให้สัตวแพทย์ตรวจทานก่อนปล่อยจริง)
- **ตัวเลขอาหาร/อายุเป็นค่าประมาณ:** ระบุบนการ์ดเสมอ ให้เทียบฉลากอาหารและหมอ
- **มุกหยาบเกิน:** template คุมเอง ถ้าเปิด AI เกลา ต้องกรองคำและ fallback เป็น template
- **น้องไม่ยอมทำท่าตอนอัด:** ใช้ /reel-demo กับ fixture หรืออัดตอนก่อนมื้อข้าวจริง (ช่วงที่แมวจ้องชามอยู่แล้ว)

> บุคคล สัตว์เลี้ยง ประวัติ และตัวเลขในเดโมทั้งหมดเป็นตัวอย่างสมมติ
