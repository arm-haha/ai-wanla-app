# InkTry — ลองรอยสักบนตัวก่อนสักจริง (AI วันละแอป · 2026-11-11)

ถ่ายผิว 1 รูป → AI วางลายบนตัวคุณ ปรับตำแหน่ง ขนาด สี/ขาวดำ ดูพรีวิวว่าจางแค่ไหนใน 1–5–10 ปี แล้วส่งบรีฟให้ช่างทาง LINE. ถ่ายผิว → Skin Scan หาตำแหน่ง + โทนผิว → Try-On วางลาย (12 แบบ / 15 จุด) → เช็กขนาดเป็นซม. → เทียบสีกับขาวดำ → Aging Preview 1/5/10 ปี → Pain & Aftercare ตามจุด → ช่วงราคา ฿ + เช็กราคาที่ร้านเสนอ → Artist Brief Card ส่งช่างทาง LINE → ไดอารี่รอยสัก, การ์ดแชร์, โควตา, Safety Guard (18+, ไม่ใช่คำแพทย์, ภาพจำลอง)

**EN:** One skin photo → AI places a tattoo on your body. Adjust placement, size, color or black-and-white, preview 1/5/10-year aging, then send an artist brief on LINE. Skin Scan, Try-On library, centimetre size check, color vs BW, aging preview, pain and aftercare by spot, THB price range and quote check, an Artist Brief Card, a tattoo diary, a share card, a daily quota and a safety guard (18+, not medical advice, preview only).

## ในแพ็ก / Pack contents
- `prd.md` — ปัญหา, must-have / nice-to-have (10 ฟีเจอร์), หน้าจอ, demo fixture, design tokens, Reel shot list, guardrails (ภาพจำลอง ไม่ใช่ช่าง/แพทย์ ราคาเป็นช่วงประมาณ ต้องอายุ 18+)
- `prompts.md` — work-order prompts P0–P12 + AI vision/text prompts A1–A5
- `schemas.json` — JSON Schema 2020-12 (25 defs)
- `examples.json` — 98 ตัวอย่าง (ข้อมูลสมมติ) validate ผ่านหมด
- `reference/` — `inktry.py` logic deterministic (15 จุด, 10 สไตล์, 12 ลาย), `fixtures.py` (พี่มิ้นต์ + 4 คนสมมติ, 8 รูปผิว), `tests.py` (41 tests), `build.py`
- `social/` — `make_cover.py`, ปก 1080×1350 / 1080×1080, `fb_post.md`

## รัน / Run
```
cd reference && python3 tests.py && python3 build.py   # ต้องมี jsonschema
```

## หมายเหตุ / Notes
- InkTry เป็น **ภาพจำลอง ไม่ใช่รอยสักจริง** และ **ไม่ใช่คำแนะนำทางการแพทย์** — ปรึกษาช่างสักที่มีใบอนุญาต และแพทย์หากมีโรคผิวหนังหรือประวัติคีลอยด์
- ผู้ใช้ต้อง**อายุ 18 ปีขึ้นไป** ประวัติคีลอยด์ / ตั้งครรภ์ / แผลติดเชื้อ = ยังไม่ควรนัดสัก
- การจำลองความเก่า (จาง % / เบลอ มม.) และระดับความเจ็บ 0–10 เป็น **ค่าตัวอย่างที่ตั้งเอง** ไม่รับประกันผลบนผิวจริง
- ช่วงราคา (฿400/ซม. × สไตล์ × สี × พื้นที่, ขั้นต่ำ ฿1,500) เป็น **ค่าประมาณการ ไม่ใช่ราคาร้านจริง** ปรับได้ใน `BASE_PER_CM` / `STYLES` / `REGION_MULT`
- ทุกตัวอย่างเป็นบุคคลสมมติ ภาพปกสร้างด้วย PIL เป็นภาพประกอบ ไม่ใช้ผิวหรือรอยสักของคนจริง
