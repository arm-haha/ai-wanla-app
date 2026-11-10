# TinySteps — การ์ดพัฒนาการลูกรายเดือนจากรูป (AI วันละแอป · 2026-12-04)

ถ่ายรูปลูกแต่ละเดือน → ได้การ์ดไมล์สโตนสวย ๆ พร้อมคำบรรยาย บันทึกส่วนสูงน้ำหนักในแถบตัวอย่าง ไทม์ไลน์ครั้งแรก คอลลาจรายเดือน และส่งให้ครอบครัว (ไม่ใช่คำแนะนำทางการแพทย์)

**EN:** Photograph each month → a pretty milestone card with a caption, an example-only growth log, a first-moments timeline, a monthly collage and a family share card (not medical advice).

## ในแพ็ก / Pack contents
- `prd.md` — ปัญหา, must-have / nice-to-have (10 ฟีเจอร์), หน้าจอ, demo fixture, design tokens, guardrails, shot list Reel
- `prompts.md` — work-order prompts P0–P12 + AI vision/text prompts A1–A5
- `schemas.json` — JSON Schema 2020-12 (21 defs)
- `examples.json` — 91 ตัวอย่าง (ข้อมูลสมมติ) validate ผ่านหมด
- `reference/` — `tinysteps.py` logic deterministic (การ์ดรายเดือน, แถบตัวอย่าง, ไทม์ไลน์ครั้งแรก 8 แบบ, คอลลาจ, คำบรรยาย), `fixtures.py` (พี่เมย + น้องภูสมมติ, พี่แนน + น้องไผ่, 5 รูป), `tests.py` (41 tests), `build.py`
- `social/` — `make_cover.py`, ปก 1080×1350 / 1080×1080, `fb_post.md`

## รัน / Run
```
cd reference && python3 tests.py && python3 build.py   # ต้องมี jsonschema
```

## หมายเหตุ / Notes
- TinySteps เป็น **การ์ดความทรงจำ ไม่ใช่คำแนะนำทางการแพทย์ ไม่ใช่แบบประเมินพัฒนาการ และไม่ใช่กราฟการเจริญเติบโตทางการ**
- แถบน้ำหนัก/ส่วนสูง และช่วงเดือนของ "ครั้งแรก" เป็น **ค่าตัวอย่างที่ตั้งเองในแอป** ถ้ากังวลให้ปรึกษาแพทย์ ห้ามอ่านว่าลูกช้าหรือเร็ว
- ใช้ได้เฉพาะรูปของลูกตนเอง (หรือรูปที่ผู้ปกครองยินยอม) ควรคิดก่อนแชร์รูปเด็กในที่สาธารณะ
- อายุต่ำกว่า 13 ปีใช้แอปนี้ไม่ได้ในฐานะผู้ใช้ — ผู้ใช้ต้องเป็นผู้ปกครองอายุ 18 ปีขึ้นไป
- ทุกตัวอย่างเป็นบุคคลสมมติ ภาพปกสร้างด้วย PIL เป็นภาพประกอบ (รอยเท้า ตุ๊กตา การ์ด) ไม่ใช้รูปเด็กจริง
