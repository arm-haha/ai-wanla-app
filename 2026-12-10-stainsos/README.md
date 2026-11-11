# StainSOS — เสื้อเลอะ ถ่ายปุ๊บ รู้วิธีขจัดคราบ (AI วันละแอป · 2026-12-10)

ถ่ายคราบบนเสื้อ 1 รูป → AI บอกว่าเป็นคราบอะไร บนผ้าชนิดไหน ให้คะแนนความยาก แล้วสอนขจัดทีละขั้นพร้อมตัวจับเวลา ใช้ของที่มีในบ้าน บอกของทดแทนถ้าไม่มี เตือนคู่น้ำยาที่ห้ามผสม อ่านป้ายผ้าให้ และเก็บไดอารี่ว่ากู้เสื้อรอดไปกี่ตัว. Stain Scan → Risk Meter → Rescue Steps + Timer → Home Kit + ของทดแทน → Mix Danger Check → Care-Label Decoder → Before/After Card → Stain Diary, Kit Check, โควตา, Safety Guard

**EN:** One photo of a stain → AI names the stain and fabric, scores how hard it is, and walks you through removal step by step with timers, using what's already at home (with substitutes). It warns about dangerous product mixes, decodes the care label, makes a before/after share card and keeps a diary of rescued clothes.

## ในแพ็ก / Pack contents
- `prd.md` — ปัญหา, must-have / nice-to-have (10 ฟีเจอร์), หน้าจอ, demo fixture, design tokens, Reel shot list, guardrails
- `prompts.md` — work-order prompts P0–P12 + AI vision/text prompts A1–A5
- `schemas.json` — JSON Schema 2020-12 (21 defs)
- `examples.json` — 125 ตัวอย่าง (ข้อมูลสมมติ) validate ผ่านหมด
- `reference/` — `stainsos.py` logic deterministic (8 คราบ, 6 ชนิดผ้า, 13 สัญลักษณ์ป้ายผ้า, 4 คู่น้ำยาห้ามผสม), `fixtures.py` (น้องแพร + 3 คนสมมติ, 5 รูป), `tests.py` (40 tests), `build.py`
- `social/` — `make_cover.py`, ปก 1080×1350 / 1080×1080, `fb_post.md`

## รัน / Run
```
cd reference && python3 tests.py && python3 build.py   # ต้องมี jsonschema
```

## หมายเหตุ / Notes
- StainSOS ให้ **ขั้นตอนทั่วไปและค่าประมาณ** ไม่รับประกันว่าคราบจะหาย — ทดสอบมุมด้านในก่อนทุกครั้ง และอ่านป้ายผ้าก่อนใช้น้ำยา
- แอป **ไม่เคยแนะนำน้ำยาฟอกคลอรีน** และเตือนทันทีถ้าผู้ใช้จะใช้คู่ที่ห้ามผสม (คลอรีน+น้ำส้มสายชู, คลอรีน+แอมโมเนีย, คลอรีน+แอลกอฮอล์, ไฮโดรเจนเปอร์ออกไซด์+น้ำส้มสายชู)
- คะแนนความยาก 0–100 และ "% ที่น่าจะจาง" เป็น **ค่าจากกฎที่ตั้งเอง** ปรับได้ใน `STAINS` / `FABRICS` / `risk_meter()`
- ผ้าไหม ขนสัตว์ เรยอน หรือคราบระดับ "ส่งมือโปร" แอปจะแนะนำให้ส่งร้านซักแห้ง
- ทุกตัวอย่างเป็นบุคคลสมมติ ภาพปกสร้างด้วย PIL เป็นภาพประกอบ ไม่ใช้รูปคนจริงหรือแบรนด์จริง
