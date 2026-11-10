# SpecsTry — ลองแว่นก่อนซื้อ (AI วันละแอป · 2026-11-12)

เซลฟี่ 1 รูป → AI หาทรงหน้า ลองกรอบแว่นบนหน้าคุณ เช็กขนาดจากค่า PD โดยประมาณ เทียบกรอบหลายอัน แล้วได้การ์ดยื่นร้านแว่น. เซลฟี่ → Face Shape Scan (6 ทรงหน้า) → Try-On Grid จัดอันดับด้วย Fit Score → Size Check จากความกว้างหน้า + ค่า PD ประมาณ (มม.) → เทียบ 2–4 กรอบ → Optician Card (ทรงหน้า ไซซ์กรอบ PD งบ ส่ง LINE) → คำแนะนำชนิดเลนส์ (ไม่ใช่ใบสั่ง) → ช่วงราคา ฿ + เช็กราคาร้าน → ไดอารี่, การ์ดแชร์, โควตา, Safety Guard (ไม่ใช่การตรวจตา ไม่ใช่ใบสั่งแว่น)

**EN:** One selfie → AI finds your face shape, tries frames on your face, checks size from an estimated PD, compares frames and builds an optician card. Face Shape Scan (6 shapes), a ranked Try-On Grid, a millimetre size check, a 2–4 frame compare, an Optician Card for LINE, lens-type notes (not a prescription), a THB price and quote check, a diary, a share card, a daily quota and a safety guard (not an eye exam, not a prescription).

## ในแพ็ก / Pack contents
- `prd.md` — ปัญหา, must-have / nice-to-have (10 ฟีเจอร์), หน้าจอ, demo fixture, design tokens, Reel shot list, guardrails (ภาพจำลอง ไม่ใช่การตรวจตา/ใบสั่ง ราคาเป็นช่วงประมาณ PD จากรูปใช้ตัดเลนส์ไม่ได้)
- `prompts.md` — work-order prompts P0–P12 + AI vision/text prompts A1–A5
- `schemas.json` — JSON Schema 2020-12 (23 defs)
- `examples.json` — 98 ตัวอย่าง (ข้อมูลสมมติ) validate ผ่านหมด
- `reference/` — `specstry.py` logic deterministic (12 กรอบ, 6 ทรงหน้า, 5 ชนิดเลนส์), `fixtures.py` (น้องเกล + 4 คนสมมติ, 8 รูป), `tests.py` (41 tests), `build.py`
- `social/` — `make_cover.py`, ปก 1080×1350 / 1080×1080, `fb_post.md`

## รัน / Run
```
cd reference && python3 tests.py && python3 build.py   # ต้องมี jsonschema
```

## หมายเหตุ / Notes
- SpecsTry เป็น **ภาพจำลองสำหรับลองกรอบ** เท่านั้น **ไม่ใช่การตรวจสายตา ไม่ใช่ใบสั่งแว่น และไม่ใช่คำแพทย์/นักทัศนมาตร**
- ค่า PD จากเซลฟี่เป็น **ค่าประมาณ ห้ามใช้ตัดเลนส์** ต้องวัดที่ร้านหรือคลินิก
- Fit Score (ทรงหน้า 40 · ขนาด 30 · สีกรอบ 15 · ไลฟ์สไตล์ 15) และสูตรความกว้างกรอบ (2×เลนส์ + สะพานจมูก + ปลายขา 8 มม. ต่อข้าง) เป็น **ค่าตัวอย่างที่ตั้งเอง**
- ช่วงราคา (ราคาฐานกรอบ + ค่าเลนส์ × พื้นที่) เป็น **ค่าประมาณการ ไม่ใช่ราคาร้านจริง** ปรับได้ใน `FRAMES` / `LENS_TYPES` / `REGION_MULT`
- ทุกตัวอย่างเป็นบุคคลสมมติ ภาพปกสร้างด้วย PIL เป็นภาพประกอบ ไม่ใช้ใบหน้าคนจริง
