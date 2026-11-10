# ParkPin — จำที่จอดรถในห้าง/ลานจอด (AI วันละแอป · 2026-11-17)

ถ่ายป้ายชั้นและเสา 1 รูป → ปักหมุดชั้น โซน สี เสา ตั้งเวลา คิดค่าจอดอย่างคร่าว และมีทางเดินกลับไปหารถ ส่งให้ครอบครัวได้. ถ่ายป้าย → Pin Floor/Zone (ชั้น โซน สี เสา) → Timer & Fee Estimator (ตารางตัวอย่าง บาท + แจ้งก่อนค่าจอดขยับและก่อนปิดลาน) → Walk-back Guide ทีละขั้น → แชร์ครอบครัวทาง LINE → ประวัติที่จอด → โหมดรถหาย (ย้อนหมุดล่าสุด) → การ์ดแชร์, โควตา, Safety Guard (ห้ามเก็บป้ายทะเบียน อัตราเป็นตัวอย่าง ไม่ใช่ราคาห้างจริง)

**EN:** One photo of the floor sign and pillar → pin the floor, zone, colour and post, start a timer, estimate the parking fee and get walk-back steps you can share with family. Floor/zone pin, a timer and example THB fee estimator with reminders before the next jump and closing time, a walk-back guide, family share on LINE, pin history, a lost-car mode, a share card, a quota and a safety guard (never store licence plates; rates are examples, not official mall prices).

## ในแพ็ก / Pack contents
- `prd.md` — ปัญหา, must-have / nice-to-have (10 ฟีเจอร์), หน้าจอ, demo fixture, design tokens, Reel shot list, guardrails (ห้ามเก็บป้ายทะเบียน อัตรา/เวลาปิดเป็นค่าตัวอย่าง)
- `prompts.md` — work-order prompts P0–P12 + AI vision/text prompts A1–A5
- `schemas.json` — JSON Schema 2020-12 (17 defs)
- `examples.json` — 58 ตัวอย่าง (ข้อมูลสมมติ) validate ผ่านหมด
- `reference/` — `parkpin.py` logic deterministic (4 ลานจำลอง, ตารางค่าจอดตัวอย่าง), `fixtures.py` (พี่เจ + 4 คนสมมติ, 8 รูป), `tests.py` (41 tests), `build.py`
- `social/` — `make_cover.py`, ปก 1080×1350 / 1080×1080, `fb_post.md`

## รัน / Run
```
cd reference && python3 tests.py && python3 build.py   # ต้องมี jsonschema
```

## หมายเหตุ / Notes
- ค่าจอดและเวลาปิดลานเป็น **ตารางตัวอย่างที่ตั้งเอง ไม่ใช่อัตราหรือเวลาของห้างจริง** ตรวจป้ายที่ลานก่อนออก
- **ห้ามถ่ายหรือเก็บแผ่นป้ายทะเบียน** ถ้าในรูปมีป้าย ให้เบลอก่อนบันทึก
- สูตรค่าจอดตัวอย่าง: นาทีแรกตาม `grace_min` ฟรี แล้วคิดเป็นชั่วโมงที่เริ่มต้น × ค่าชั่วโมง จนถึงเพดานต่อวัน
- ทุกตัวอย่างเป็นบุคคลและลานสมมติ ภาพปกสร้างด้วย PIL เป็นภาพประกอบ ไม่ใช้ลานจริงหรือป้ายทะเบียนจริง
