# SingScore — ร้องคาราโอเกะให้คะแนน + โค้ชเสียง (AI วันละแอป · 2026-12-02)

ฮัมหรือร้องแบบฝึกสเกลต้นฉบับ → ได้คะแนนเสียงและจังหวะ หาคีย์ วอร์มอัพ การ์ดแข่งดูเอท และบันทึกการฝึก (แพ็กนี้ไม่มีเนื้อเพลงลิขสิทธิ์)

**EN:** Hum or sing an original scale exercise → get pitch and timing scores, a key finder, warm-ups, a duet battle card and a practice log (no copyrighted lyrics bundled).

## ในแพ็ก / Pack contents
- `prd.md` — ปัญหา, must-have / nice-to-have (10 ฟีเจอร์), หน้าจอ, demo fixture, design tokens, guardrails, shot list Reel
- `prompts.md` — work-order prompts P0–P12 + AI audio/text prompts A1–A5
- `schemas.json` — JSON Schema 2020-12 (13 defs)
- `examples.json` — 91 ตัวอย่าง (ข้อมูลสมมติ) validate ผ่านหมด
- `reference/` — `singscore.py` logic deterministic (คะแนนเสียง/จังหวะ, หาคีย์, วอร์มอัพ, การ์ดดูเอท, บันทึกฝึก — ไม่มีเนื้อเพลง), `fixtures.py` (พี่ต้อม + น้องนีน่าสมมติ, แบบฝึก ScaleRun in C), `tests.py` (41 tests), `build.py`
- `social/` — `make_cover.py`, ปก 1080×1350 / 1080×1080, `fb_post.md`

## รัน / Run
```
cd reference && python3 tests.py && python3 build.py   # ต้องมี jsonschema
```

## หมายเหตุ / Notes
- SingScore เป็น **คะแนนฝึกซ้อม ไม่ใช่ครูสอนร้องและไม่ใช่แพทย์**
- **แพ็กนี้ไม่มีเนื้อเพลงหรือแทร็กคาราโอเกะที่มีลิขสิทธิ์** ผู้ใช้ต้องฮัมหรือใช้แทร็กของตนเอง
- คะแนนคำนวณจากส่วนเบี่ยงเบน cents และมิลลิวินาทีด้วยสูตรที่ตั้งเอง (เช่น เบี่ยง 36 cents = เสียง 82)
- ถ้าเจ็บคอหรือฝืนเสียงให้หยุดทันที
- ตัวอย่างและภาพปกเป็นบุคคลสมมติ/ภาพวาด ไม่ใช้คนจริงหรือเพลงจริง
