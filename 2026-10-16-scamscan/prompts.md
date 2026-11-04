# ScamScan — Prompt สั่งงาน (จัดเต็ม)

ใช้คู่กับ `prd.md` · `schemas.json` · `examples.json` · `reference/scam.py`
สแต็ก: Next.js 14 App Router + TypeScript + Tailwind + shadcn/ui + framer-motion + PWA + Vercel
สี: night `#0B1220` · panel `#111A2E` · paper `#F8FAFC` · siren `#DC2626` · amber `#F97316` · caution `#FACC15` · safe `#16A34A` · shield `#38BDF8`
คอร์ต้อง deterministic ตาม `reference/scam.py` — AI เป็นตัวเสริมเท่านั้น และห้ามเปลี่ยนคะแนน

ตัวเลขเดโมที่ล็อก (กล่องข้อความป้าแดง 2026-10-16):
- m1 **90** scam (80 + combo 10) · m2 **85** scam · m3 **55** risky · m4 **0** low
- m1 flags `urgency, credential, link, brand_mismatch, bad_tld` · เว็บจริง `kasikornbank.com`
- X-Ray 4 ลิงก์ → `fake_lookalike, official, suspicious, suspicious`
- Quiz seed 20261016 → `q08,q06,q01,q02,q04` ถูก 4/5 · Call Shield 80 · Wrapped 8/6/2 credential kbank streak 5

---

## A) Master prompt สร้างทั้งแอป (วางครั้งเดียว)
```
คุณเป็น senior full-stack ที่จะสร้างแอป ScamScan (มิจฉาสแกน) ตาม PRD ที่แนบ

เป้าหมาย: mini suite "วางข้อความ → รู้ทันทีว่าหลอกไหม หลอกตรงไหน ต้องทำอะไร" สำหรับคนไทยทุกวัย โดยเฉพาะพ่อแม่ผู้สูงอายุ
ภาษา UI ไทยเป็นหลัก (ดู examples.json → ui_copy_th)

สแต็กบังคับ:
- Next.js 14 App Router + TypeScript + Tailwind + shadcn/ui + framer-motion
- PWA (manifest + icons + service worker + share_target รับ text จากแอปอื่น) · mobile-first 390px · deploy Vercel
- local-first: localStorage key "scamscan:v1" ตาม schema LocalStore · ไม่มีล็อกอิน
- html-to-image สำหรับ Family Card · Web Speech API (th-TH) สำหรับอ่านออกเสียง
- optional AI: /api/ai/ocr (รูปแคป → ข้อความ) และ /api/ai/explain อ่าน process.env.AI_API_KEY
  ไม่มี key → แอปใช้ได้ 100% (วางข้อความ + demo) ปุ่มแคปหน้าจอแสดง "ต้องตั้งค่า AI ก่อน"

กฎความปลอดภัย (ห้ามละเมิด):
- ห้าม fetch / เปิด / prefetch ลิงก์ที่อยู่ในข้อความ ลิงก์ใน UI แสดงเป็นข้อความธรรมดา ไม่ใช่ <a>
- ห้ามฝังเบอร์โทรธนาคาร ใช้ข้อความ "ดูเบอร์หลังบัตร/ในแอปทางการ"
- ทุกหน้าผลแสดง disclaimer จาก ui_copy_th.disclaimer
- ระดับ low ห้ามใช้คำว่า "ปลอดภัย 100%"

สี (ห้ามเปลี่ยน): --night #0B1220 --panel #111A2E --paper #F8FAFC --siren #DC2626 --amber #F97316 --caution #FACC15 --safe #16A34A --shield #38BDF8

Must-have 5 ฟีเจอร์ (ทำให้จบก่อน):
1) Paste → Scam Meter (wow: มิเตอร์ครึ่งวงกลมวิ่ง 0→คะแนน ไล่สี + ไซเรนกระพริบเมื่อ ≥75)
2) Red-Flag Highlighter (ไฮไลต์ทีละคำ stagger 120ms แตะเพื่ออ่านคำอธิบาย)
3) Link X-Ray (แตก URL เป็นบล็อกสี + "เว็บจริงคือ …")
4) Action Card (ขั้นตอน + คัดลอกคำตอบปลอดภัย + AOC 1441)
5) Family Alert Card → LINE

Nice-to-have: Quiz จริงหรือหลอก, Call Shield, History + Wrapped, Grandparent Mode, AI explain

โครงสร้างไฟล์:
/lib/engine/{rules.ts,brands.ts,scan.ts,xray.ts,actions.ts,family.ts,quiz.ts,call.ts,wrapped.ts}
/lib/store.ts /lib/share.ts /lib/speech.ts
/app/(screens)/{page.tsx,result,xray,family,quiz,call,history,settings}
/app/api/ai/{ocr,explain}/route.ts
/fixtures/{demo.json (= examples.json ทั้งไฟล์)}
/tests/engine.test.ts (vitest)

ขั้นแรก: สร้างโปรเจกต์ + ไฟล์ทั้งหมดเป็น skeleton + README สั้น แล้วหยุดรอ prompt ถัดไป
```

## B) Engine (port จาก Python ให้ตรงทุกตัวเลข)
```
Port reference/scam.py เป็น TypeScript ใน /lib/engine ให้ผลลัพธ์ "ตรงทุกฟิลด์" กับ examples.json:
- RULES (id, weight, label_th, explain_th, patterns) โหลดจาก examples.json.rules (อย่า hardcode ซ้ำ)
- regex ใช้ flag "gi" และ Unicode; ระวัง \b ไม่ทำงานกับอักษรไทย (ใช้ตามที่ reference ใช้เท่านั้น)
- extractLinks: regex URL_RE เหมือน reference, rstrip ".,)!"
- registeredDomain: 2 ส่วนท้าย ยกเว้น *.{co,or,go,in,ac,net,mi}.th ใช้ 3 ส่วน
- linkXray: flags shortener/bad_tld/no_https/punycode/ip_link/brand_mismatch + verdict ตามลำดับใน reference
- scan: นับ rule ครั้งเดียว (เก็บ hits), raw_score = ผลรวม weight, combo +10 ถ้ามีลิงก์และ (credential หรือ money), cap 100
- highlights: sort (start asc, ยาว desc) แล้วตัดที่ทับกัน
- levelOf, actionPlan, familyCard, quizRound (ต้องใช้ PRNG ที่ให้ผลเหมือน Python random.Random(seed).shuffle → ทำ Mersenne Twister + shuffle แบบ Python หรือ ship ลำดับ round จาก examples.quiz.round เป็น fallback เมื่อ seed ตรง), quizGrade, quizStreak, callShield, historyEntry, shieldWrapped

เขียน vitest:
- ทุก scan_results ใน examples.json → deepEqual กับ scan(text, sender, channel)
- expect_locked ทุกค่า
- ทุก QuizCard: (score>=25) == (truth=="scam")
- highlight: text.slice(start,end) === h.text และไม่ทับกัน
รัน test จนผ่านทั้งหมด แล้วรายงานผล
```

## C) Home + Scan + Result + มิเตอร์ (wow)
```
สร้าง Home และ Result:
- Home: หัวข้อ "ข้อความนี้ หลอกรึเปล่า?" textarea ใหญ่ (auto-grow) ปุ่ม 📋 วาง (navigator.clipboard.readText), 🖼️ แคปหน้าจอ, ปุ่ม demo "ลองกล่องข้อความป้าแดง" แสดง 4 ข้อความเป็น bubble ให้แตะเลือก
- รองรับ share_target: /share?text=... → เติม textarea แล้วสแกนอัตโนมัติ
- Scanning 1.2 วิ: เส้นแสง shield วิ่งบน bubble ข้อความ
- Result:
  1) Meter: SVG ครึ่งวงกลม gradient safe→caution→amber→siren เข็มหมุนด้วย spring (0→score 900ms) ตัวเลขนับขึ้น 72px emoji + label_th ตาม level
     score ≥75: พื้นหลังกระพริบ siren 2 ครั้ง (opacity 0→0.25) + navigator.vibrate([80,40,80]) ถ้ามี
  2) Bubble ข้อความต้นฉบับ ไฮไลต์ตาม highlights (สีตาม rule) ทีละอัน stagger 120ms
  3) รายการ flag: label_th + น้ำหนัก +explain_th (accordion)
  4) disclaimer ด้านล่างเสมอ
- เก็บผลลง history (historyEntry) อัตโนมัติ
```

## D) Link X-Ray
```
สร้าง component <LinkXray> และหน้าเต็ม /xray:
- แสดง URL แตกเป็นบล็อก: [scheme] [subdomain] [โดเมนหลัก] [.tld] [/path] สีบล็อก: ปกติ panel, flag ที่เกี่ยวข้องเป็น siren/amber
- verdict pill: official(safe) / fake_lookalike(siren) / hidden(amber) / suspicious(amber) / unknown(caution)
- ถ้า real_site: แสดง 2 แถวเทียบ "ในข้อความ: kbank-verify-th.top ❌" vs "เว็บจริง: kasikornbank.com ✅" แอนิเมชันตัวอักษรที่ต่างกันกระพริบ
- ช่องวางลิงก์เดี่ยวเพื่อเช็กอย่างเดียวได้
- ห้ามทำเป็นลิงก์กดได้ ใช้ <span> + ปุ่มคัดลอก
- ทดสอบกับ examples.link_xrays ทั้ง 4 อัน
```

## E) Action Card
```
ใต้ผลสแกน แสดง Action Card ตาม actions.steps (icon ใหญ่ + text_th)
- ปุ่ม "คัดลอกคำตอบปลอดภัย" (safe_reply_th) และ chip "ไม่ตอบเลย ดีที่สุด" ถ้ามี best_reply_th
- ปุ่ม "บล็อกผู้ส่ง (จำไว้ในแอป)" → เพิ่มใน blocked_senders; ครั้งหน้าผู้ส่งนี้ขึ้นป้าย "เคยบล็อก"
- ปุ่ม "เผลอกด/โอนไปแล้ว" → sheet: 1) โทรธนาคารเบอร์หลังบัตรให้อายัด 2) แจ้ง AOC 1441 (tel:1441) 3) เปลี่ยนรหัส 4) ถ้าลงแอปแปลก ปิดเน็ต/ถอนแอป
- ข้อความทั้งหมดอ่านออกเสียงได้ (ปุ่ม 🔊) เมื่อเปิด read_aloud
```

## F) Family Alert Card → LINE
```
สร้าง /family:
- เลือกผู้รับจาก settings.family (default "แม่") แล้ว render FamilyCard จาก familyCard(result, from, to)
- การ์ด 1080×1350 พื้น night, แถบ accent ตาม level, ตัวเลขคะแนนใหญ่, ข้อความตัวอย่าง (ตัด 60 ตัว), 3 flag, ขั้นแรกที่ต้องทำ, footer "เช็กด้วย ScamScan · AI วันละแอป"
- export ด้วย html-to-image (pixelRatio 2) → navigator.share({files}) ถ้ารองรับ, ไม่งั้นดาวน์โหลด
- ปุ่ม "ส่ง LINE": https://line.me/R/share?text= + encodeURIComponent(line_text_th)
- โหมดกลับด้าน: แม่กด "ถามลูก" → ข้อความ "มิ้นท์ ข้อความนี้จริงไหม? ScamScan ให้ 90/100"
```

## G) Quiz + Call Shield + History/Wrapped + Grandparent
```
1) /quiz: การ์ดปัด (framer-motion drag) ซ้าย=หลอก ขวา=จริง 5 ใบจาก quizRound(deck, seed=YYYYMMDD ของวันนี้)
   เฉลยหลังปัดแต่ละใบ: ถูก/ผิด + scan() ของการ์ดนั้น (โชว์ flag) · จบรอบ quizGrade + badge + streak (quizStreak)
   บันทึกวันลง quiz_days
2) /call: checklist CALL_SIGNS ปุ่มใหญ่ ติ๊กแล้วคะแนนสด (callShield) ≥50 แสดง say_th ตัวใหญ่ + rule_th + ปุ่มคัดลอก
3) /history: รายการ HistoryEntry (preview, คะแนน, สี) ลบรายตัว/ลบทั้งหมด
   การ์ด Wrapped เดือนนี้: "เช็ก {checked} ข้อความ · เจอเสี่ยง {flagged} · มุกที่เจอบ่อย {top_rule_th} · แบรนด์โดนปลอมบ่อยสุด {most_faked_brand_th} · ฝึก Quiz ติดกัน {quiz_streak_days} วัน" export 1080×1920
4) Grandparent Mode (settings.big_text): root font 1.3×, ปุ่ม ≥64px, ซ่อนรายละเอียดรอง, ปุ่ม 🔊 ทุกการ์ด
5) Settings: allowlist แบรนด์ (ดู/เพิ่ม custom_brands), ครอบครัว, ปิด/เปิด AI explain, ลบข้อมูลทั้งหมด
```

## H) AI (optional) — OCR + Explain
```
- /api/ai/ocr: รับรูป (≤4MB) → เรียก vision model ด้วย Prompt K → ตอบตาม AiOcrResponse → เติม textarea แล้วให้ผู้ใช้ตรวจ/แก้ก่อนสแกน
- /api/ai/explain: ส่ง AiExplainRequest (ตัดเลขบัญชี ≥8 หลัก และเบอร์โทรเป็น *** ก่อน) → Prompt L → AiExplainResponse
- validate ผลด้วย schema (zod หรือ ajv) ถ้าไม่ผ่าน ไม่แสดง และไม่กระทบคะแนน
- ไม่มี AI_API_KEY → endpoint ตอบ 501, UI ซ่อนปุ่มอธิบายเพิ่ม
```

## I) QA + แก้บั๊ก
```
ตรวจทั้งแอปตาม Acceptance ใน prd.md:
- vitest ผ่านทั้งหมด · demo 4 ข้อความ 90/85/55/0
- DevTools Network: ไม่มี request ไปโดเมนในข้อความ
- Lighthouse PWA ผ่าน, a11y ≥90, contrast AA, ทุกปุ่มมี aria-label ภาษาไทย
- ทดสอบข้อความยาว 2000 ตัว, ข้อความว่าง, emoji, ลิงก์หลายอัน, ไม่มีลิงก์
รายงานบั๊กที่เจอ + แก้ + รัน test ซ้ำ
```

## J) หน้าอัด Reel (/reel)
```
สร้างหน้า /reel สำหรับอัดจอ 9:16 (390×844):
- autoplay ตาม examples.reel_script: m1 วางเอง (typing effect 40ms/ตัว) → มิเตอร์ 90 + ไซเรน → highlight → X-Ray เทียบเว็บจริง → Family Card → Call Shield ติ๊ก 4 ข้อ = 80 → Quiz ปัด 2 ใบ → Wrapped
- overlay_th ตัวใหญ่ด้านบนตามช่วงเวลา, ปุ่ม ▶︎ เริ่มใหม่, ซ่อน status bar
- ทุกฉากรวม ≤30 วินาที
```

---

## Runtime prompts (ใช้ใน API)

### K) OCR แคปหน้าจอ
```
คุณอ่านภาพแคปหน้าจอ SMS/LINE/Messenger ภาษาไทย
ส่งคืน JSON เท่านั้น ตาม schema AiOcrResponse: {"text","sender_guess","channel_guess","confidence"}
- text = ข้อความในบับเบิลล่าสุดที่เป็นของ "ผู้ส่ง" (ไม่ใช่ของเจ้าของเครื่อง) คงตัวสะกด ลิงก์ ตัวเลข ตามภาพทุกตัว ห้ามแก้ ห้ามสรุป
- ห้ามเดาลิงก์ที่มองไม่ชัด ใส่ [อ่านไม่ออก]
- channel_guess จาก UI ในภาพ: sms | line | messenger | email | other
```

### L) อธิบายให้ผู้สูงอายุ
```
คุณช่วยอธิบายผลตรวจข้อความน่าสงสัยให้ผู้สูงอายุไทยเข้าใจ
อินพุต: AiExplainRequest {text, flags, level, audience}
ส่งคืน JSON ตาม AiExplainResponse เท่านั้น:
- summary_th ≤200 ตัว ประโยคง่าย สุภาพ ไม่ขู่
- why_th ไม่เกิน 3 ข้อ อ้างอิงเฉพาะ flags ที่ได้รับ ห้ามคิด flag ใหม่
- never_change_score: true — ห้ามบอกคะแนนใหม่ ห้ามบอกว่า "ปลอดภัยแน่นอน"
- ห้ามใส่เบอร์โทร ลิงก์ หรือชื่อบุคคล
```

### M) แคปชัน Reel (ใช้ตอนโพสต์)
```
เขียนแคปชัน Reel ภาษาไทยสำหรับแอป ScamScan 3 แบบ (สั้น/กลาง/ชวนคอมเมนต์) แต่ละแบบ ≤220 ตัว
ต้องมี: ฮุคเรื่องพ่อแม่ได้ SMS หลอก, ตัวเลข 90/100, CTA "คอมเมนต์ 'กันโกง' รับแอปฟรี", แฮชแท็ก 5 อัน
ห้าม: ใช้ชื่อ/โลโก้ธนาคารจริงในแง่ลบ, อ้างว่ากันได้ 100%
```
