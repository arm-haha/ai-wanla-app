# HandFont — เขียนลายมือแผ่นเดียว ได้ฟอนต์ของตัวเอง (AI วันละแอป · 2026-12-18)

ดาวน์โหลดแบบฟอร์ม A4 → เขียน ก–ฮ สระ วรรณยุกต์ (และ A–Z ถ้าต้องการ) ด้วยปากกา → ถ่ายรูป 1 รูป → Consent Guard ยืนยันว่าเป็นลายมือตัวเอง ไม่ใช่ลายเซ็น → AI หามุมกระดาษ ตัดทีละช่อง ตรวจช่องว่าง/จาง/ล้นกรอบ/เลอะ ให้ถ่ายซ่อมเฉพาะช่อง → vectorize เป็น **ฟอนต์ลายมือของเราเอง (TTF/OTF/WOFF2)** พิมพ์อะไรก็เป็นลายมือเรา → **Thai Mark Engine** วางสระบน-ล่างและวรรณยุกต์ถูกตำแหน่ง (หลบหาง ป ฝ ฟ ฬ, ฎ ฏ, ตัดเชิง ญ ฐ) → Style Tuner (หนา-บาง เอียง ความดิบ ระยะห่าง) + ตัวสำรอง 3 แบบไม่ให้ดูก๊อปวาง → การ์ด 7 แบบ (วันเกิด ขอบคุณ บอกรัก งานแต่ง ส.ค.ส. วันครู โน้ตขอบคุณลูกค้า) → สติกเกอร์ข้อความพื้นใสลง IG Story/LINE → แบบฝึกคัดลายมือ + ให้คะแนนความสม่ำเสมอ → ไดอารี่ ฟอนต์ v1/v2 สตรีคการฝึก → การ์ดแชร์ / Reel, โควตา และ Safety Guard (ห้ามลายมือคนอื่น ห้ามลายเซ็น ห้ามปลอมเอกสาร)

**EN:** Print an A4 template → write the Thai alphabet, vowels and tone marks (plus A–Z if you like) with a pen → snap one photo → a Consent Guard (your own handwriting only, no signatures) → AI finds the sheet corners, cuts every cell and flags empty / faint / overflowing / messy cells so you re-shoot only those → vectorised into **your own handwriting font (TTF/OTF/WOFF2)** — type anything in your handwriting → a **Thai Mark Engine** that stacks upper/lower vowels and tone marks correctly (ascender shift for ป ฝ ฟ ฬ, descender handling for ฎ ฏ ญ ฐ) → a Style Tuner (weight, slant, roughness, tracking) with 3 natural alternates per letter → 7 card templates (birthday, thank-you, love note, wedding, New Year, Teacher's Day, shop thank-you note) → transparent text stickers for IG Story / LINE → handwriting-practice sheets with a consistency score → a font diary (v1/v2, practice streak) → share card / Reel maker, daily quota and a safety guard (no one else's handwriting, no signatures, no forged documents).

## ในแพ็ก / Pack contents
- `prd.md` — ปัญหา, must-have / nice-to-have (10 ฟีเจอร์), หน้าจอ, demo fixture, design tokens, Reel shot list, build plan, risks, guardrails, metrics
- `prompts.md` — work-order prompts P0–P12 + AI prompts A1–A5
- `schemas.json` — JSON Schema 2020-12 (26 defs)
- `examples.json` — 142 ตัวอย่าง (ข้อมูลสมมติ) validate ผ่านหมด
- `reference/` — `handfont.py` logic deterministic (4 แบบฟอร์ม, 44 พยัญชนะ + สระ/วรรณยุกต์ + เลขไทย + A–Z, กฎวางสระ-วรรณยุกต์ไทย, 7 การ์ด × 6 กระดาษ × 6 หมึก), `fixtures.py` (ครูมิ้นท์ + 3 คนสมมติ), `tests.py` (37 tests), `build.py`
- `social/` — `make_cover.py`, ปก 1080×1350 / 1080×1080, `fb_post.md`, `caption_fb.txt`

## รัน / Run
```
cd reference && python3 tests.py && python3 build.py   # ต้องมี jsonschema
```

## หมายเหตุ / Notes
- ใช้ได้เฉพาะ **ลายมือของคุณเอง** ไม่รองรับลายมือคนอื่น/คนดัง และ **ไม่ทำฟอนต์จากลายเซ็น** ฟอนต์นี้ไม่ใช่ลายเซ็นอิเล็กทรอนิกส์ ห้ามใช้ปลอมเอกสาร ใบลา หรือใบรับรอง
- ขนาดไฟล์ฟอนต์ (`font_build`) และความกว้างตัวอักษร (`adv_width`) เป็น **ค่าประมาณ** สำหรับพรีวิว; การตัดคำไทยในแอปจริงใช้ `Intl.Segmenter`
- คะแนนคัดลายมือ (`practice_score`) วัดความสม่ำเสมอเท่านั้น ไม่ใช่การวิเคราะห์นิสัยจากลายมือ
- อายุต่ำกว่า 13 ปีต้องมีผู้ปกครองยืนยัน; ข้อมูลส่วนตัวบนแผ่นถูกเบลอก่อนประมวลผล
- ทุกตัวอย่างเป็นบุคคลสมมติ ภาพปกสร้างด้วย PIL (ตัวอย่างลายมือใช้ฟอนต์ Sriracha แบบ OFL เป็นภาพประกอบ) ไม่ใช้รูปคนจริงหรือแบรนด์จริง
