# ContractLens — ถ่ายสัญญาเช่า/กู้ เจอจุดอันตรายก่อนเซ็น (AI วันละแอป · 2026-11-16)

ถ่ายสัญญา 1 รูป → AI ไฮไลต์จุดเสี่ยงเป็นสีไฟจราจร สรุปภาษาคน คิดยอดที่ต้องจ่าย และมีคำถาม+เช็กลิสต์ก่อนเซ็น. ถ่ายเอกสาร → Contract Scan (เช่า หรือ กู้) → Risk Highlights (แดง/เหลือง/เขียว ตามกฎตัวอย่าง 12 ข้อ เช่น ต่ออัตโนมัติ มัดจำสูง ดอกเบี้ยสูง ช่องว่างในสัญญา) → สรุปภาษาคน → เครื่องคิดค่าใช้จ่าย (ย้ายเข้า / ยอดกู้รวมตัวอย่าง) → คำถามที่ควรถาม → เช็กลิสต์ก่อนเซ็น → การ์ดส่งครอบครัวทาง LINE → ไดอารี่, โควตา, Safety Guard (**ไม่ใช่คำปรึกษาทางกฎหมาย**)

**EN:** One photo of a rental or loan contract → AI highlights risky clauses as a traffic light, summarises in plain Thai, estimates fees, and gives questions plus a sign-the-dotted-line checklist. Contract Scan, Risk Highlights (12 example rules), a plain-Thai summary, a fee calculator, questions to ask, a sign checklist, a family card on LINE, a diary, a quota and a safety guard (**not legal advice**).

## ในแพ็ก / Pack contents
- `prd.md` — ปัญหา, must-have / nice-to-have (10 ฟีเจอร์), หน้าจอ, demo fixture, design tokens, Reel shot list, guardrails (ไม่ใช่ทนาย/ไม่ใช่กฎหมาย เกณฑ์เป็นค่าตัวอย่าง)
- `prompts.md` — work-order prompts P0–P12 + AI vision/text prompts A1–A5
- `schemas.json` — JSON Schema 2020-12 (22 defs)
- `examples.json` — 72 ตัวอย่าง (ข้อมูลสมมติ) validate ผ่านหมด
- `reference/` — `contractlens.py` logic deterministic (12 จุดเสี่ยง, สัญญาเช่า/กู้), `fixtures.py` (น้องเบนซ์ + 4 คนสมมติ, 8 รูป), `tests.py` (41 tests), `build.py`
- `social/` — `make_cover.py`, ปก 1080×1350 / 1080×1080, `fb_post.md`

## รัน / Run
```
cd reference && python3 tests.py && python3 build.py   # ต้องมี jsonschema
```

## หมายเหตุ / Notes
- ContractLens **ไม่ใช่คำปรึกษาทางกฎหมาย ไม่ใช่ทนาย และไม่ใช่ข้อความกฎหมาย** ก่อนเซ็นควรปรึกษาทนายหรือหน่วยงานที่เชื่อถือได้
- เกณฑ์เตือน (เช่น มัดจำ > 2 เดือน, ดอกเบี้ย ≥ 1.5%/เดือน) เป็น **ค่าตัวอย่างที่แอปตั้งเอง ไม่ใช่เพดานกฎหมาย**
- เครื่องคิดเงินเป็นการจำลองจากตัวเลขที่กรอก ไม่ใช่ใบแจ้งหนี้ และดอกกู้ตัวอย่างคิดแบบคงที่ ไม่ใช่ตารางลดต้นลดดอกจริง
- ทุกตัวอย่างเป็นบุคคลและสัญญาสมมติ ภาพปกสร้างด้วย PIL เป็นภาพประกอบ ไม่ใช้สัญญาจริงของใคร
