# HomeworkHero — ถ่ายการบ้านลูก ได้วิธีสอนทีละขั้น (AI วันละแอป · 2026-11-13)

ถ่ายการบ้าน 1 รูป → AI จัดวิชาและระดับตามหลักสูตรไทย แล้วให้คำใบ้ทีละขั้น **โดยไม่บอกคำตอบ** พร้อมสคริปต์ให้ผู้ปกครองถามลูก ข้อฝึกคล้ายกัน และบันทึกความก้าวหน้า. ถ่ายสมุด → Homework Scan (วิชา + ป.1–ม.6) → Step Hints 3 ระดับ (ระดับ 1–2 ไม่มีคำตอบ ระดับ 3 เป็นวิธีคิดพร้อมช่องว่าง) → Parent Script (อย่าทำข้อให้ลูก) → Similar Practice ข้อละตัวเลข (คำตอบอยู่ในโหมดผู้ปกครองเท่านั้น) → Progress Log → นาฬิกาจับเวลาและกำลังใจ → จุดที่มักผิด → บันทึกถึงครูทาง LINE → โควตา, Safety Guard

**EN:** One photo of the homework → AI tags the Thai-curriculum subject and level, then gives step-by-step hints **without the answer**, a parent script, similar practice and a progress log. Homework Scan (P.1–M.6), 3-level Step Hints (levels 1–2 never include the answer; level 3 is the method with blanks), a Parent Script (don't do the work for them), similar practice with a parent-only answer key, a progress log, a timebox, common-mistake flags, a teacher note on LINE, a quota and a safety guard.

## ในแพ็ก / Pack contents
- `prd.md` — ปัญหา, must-have / nice-to-have (10 ฟีเจอร์), หน้าจอ, demo fixture, design tokens, Reel shot list, guardrails (ไม่บอกคำตอบในหน้าหลัก ไม่ใช่ครู/ไม่ใช่หลักสูตรทางการ)
- `prompts.md` — work-order prompts P0–P12 + AI vision/text prompts A1–A5
- `schemas.json` — JSON Schema 2020-12 (21 defs)
- `examples.json` — 100 ตัวอย่าง (ข้อมูลสมมติ) validate ผ่านหมด
- `reference/` — `homeworkhero.py` logic deterministic (10 แม่แบบ, 4 วิชา, 12 ระดับ), `fixtures.py` (พี่นุ่น + 4 คนสมมติ, 8 รูป), `tests.py` (41 tests รวมทดสอบว่าคำใบ้ 1–2 ไม่หลุดคำตอบ), `build.py`
- `social/` — `make_cover.py`, ปก 1080×1350 / 1080×1080, `fb_post.md`

## รัน / Run
```
cd reference && python3 tests.py && python3 build.py   # ต้องมี jsonschema
```

## หมายเหตุ / Notes
- HomeworkHero **ให้คำใบ้และวิธีคิด ไม่บอกคำตอบของการบ้านในหน้าหลัก** การเปิดคำตอบมีได้เฉพาะโหมดผู้ปกครอง (`parent_reveal`)
- ไม่ใช่ครู ไม่ใช่หลักสูตร สพฐ. อย่างเป็นทางการ และไม่ใช้ทำงานให้ลูก
- แม่แบบ 10 ข้อเป็น **ตัวอย่างที่ตั้งเอง** ไม่ครอบคลุมทุกสาระ; ระดับ ป.1–ม.6 เป็นป้ายจัดกลุ่ม ไม่ใช่ตัวชี้วัดทางการ
- ทุกตัวอย่างเป็นบุคคลสมมติ ภาพปกสร้างด้วย PIL เป็นภาพประกอบ ไม่ใช้ใบหน้าเด็กหรือการบ้านจริงของใคร
