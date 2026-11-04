# PRD — PawTalk (แมวหมาพูดได้)

**เวอร์ชัน:** 1.0 · 2026-10-20 · ช่อง AI วันละแอป
**ฮุค Reel:** "แมวกูด่าอะไรกูอยู่ทุกเช้า?" ถ่ายรูปเดียว แอปแปลภาษากายเป็นคำพูดไทยตลกๆ + บอกงานทาสที่ลืม 🐾

## 1. ปัญหา
- ทาสแมว/หมาไทยอยากรู้ว่าน้องคิดอะไร และชอบแชร์คลิปน้องอยู่แล้ว (คอนเทนต์สัตว์เลี้ยงเป็นหมวดที่คนดูและแชร์เยอะ)
- ลืมรอบถ่ายพยาธิ/เห็บหมัด/วัคซีน ไม่รู้ว่าให้อาหารเท่าไหร่ และตกใจไม่รู้ว่าอาการไหนต้องรีบไปหมอ

## 2. ทำไมไวรัล
- Before/after ทางอารมณ์ชัด: "หิว 62% vibe 38" → หลังกินข้าว "ชิลล์ vibe 96"
- บับเบิลภาษาไทยตลก + สลับนิสัย 3 แบบในวินาทีเดียว = มีมพร้อมแชร์
- คนดูทุกคนเอาไปลองกับน้องตัวเองได้ทันที → คอมเมนต์ขอลิงก์

## 3. Persona
- **แพรว (สมมติ)** 27 ปี คอนโด เลี้ยงแมวส้ม "ส้มฉุน" + ชิบะ "ข้าวปั้น" ถ่ายน้องลง IG ทุกวัน ลืมนัดถ่ายพยาธิบ่อย

## 4. ฟีเจอร์ (10)
| # | ฟีเจอร์ | ระดับ | หมายเหตุ |
|---|---|---|---|
| 1 | Pet Snap → Thought Bubble ⭐ | Must | AI เสนอ cue → engine ให้อารมณ์ → บับเบิลไทย |
| 2 | Mood Meter + Vibe | Must | % ต่ออารมณ์ (รวม 100) + vibe 0–100 + safety hint |
| 3 | Persona Flip + Meme Card | Must | เจ้านาย/ดราม่าควีน/ขี้อ้อน · การ์ด 1080×1920 |
| 4 | Care Board + เตือน | Must | ถ่ายพยาธิ เห็บหมัด วัคซีน ตัดเล็บ อาบน้ำ + มื้อถัดไป |
| 5 | Health Check คัดกรอง | Must | emergency / soon / watch / ok + ปุ่มหาโรงพยาบาลสัตว์ |
| 6 | Duet — น้องคุยกัน | Nice | แชต 3 ข้อความ แมว↔หมา |
| 7 | Food Calculator | Nice | RER = 70 × kg^0.75 × factor → g/วัน, g/มื้อ |
| 8 | อายุเทียบคน + Pet ID Card | Nice | การ์ด 1080×1350 |
| 9 | Mood Diary + streak + XP/Level | Nice | snap 10, care_done 15, health_check 5 XP |
| 10 | Pet Wrapped รายเดือน | Nice | อารมณ์ประจำเดือน, วันที่หงุดหงิดสุด |

## 5. กติกาคอร์ (deterministic, ดู reference/pawtalk.py)
- อารมณ์ 7 แบบ: happy, chill, hungry, annoyed, scared, playful, needy
- cue แมว 16 / หมา 14 แต่ละ cue มีน้ำหนักต่ออารมณ์ (examples.json → cue_catalog)
- meal bonus: ถ้าอีก ≤60 นาทีถึงมื้อ → hungry +2
- % ใช้ largest remainder ให้รวม 100 · เสมอกันให้ scared > annoyed > hungry > needy > playful > happy > chill (เน้นความปลอดภัย)
- บับเบิล: 7 อารมณ์ × 3 persona × 3 ประโยค = 63 template · index = Σ charCode(`pet|date|mood|persona`) mod 3 (วันเดียวกันได้ประโยคเดิม)
- Care: due = last_done + interval · เลย = overdue · ≤3 วัน = due_soon
- Health: ระดับสูงสุดของอาการที่เลือก · ลูกแมว/ลูกหมา <6 เดือน หรืออาการ watch ≥3 อย่าง → ยกเป็น soon
- Food factor: แมวทำหมัน 1.2 / ไม่ทำ 1.4 / <1 ปี 2.5 / ลดน้ำหนัก 0.8 · หมาทำหมัน 1.6 / ไม่ทำ 1.8 / <1 ปี 2.5 / ลดน้ำหนัก 1.0 (ค่าประมาณทั่วไป)
- อายุคน: ปีแรก 15, ปีที่สอง 24, ต่อไปแมว +4/ปี, หมาเล็ก/กลาง/ใหญ่ +4/+5/+6 (ประมาณการ)

## 6. ตัวเลขเดโมที่ล็อก
ดู `examples.json → expect_locked` และหัว `prompts.md` (ส้มฉุน หิว 62% vibe 38 → 96 · ถ่ายพยาธิเลย 7 วัน · 260 kcal 68 g · Lv3 205 XP streak 7)

## 7. หน้าจอ
Home (การ์ดน้อง + มื้อถัดไป + งานทาสแดง) → Snap → Cue Confirm → Result (บับเบิล + Mood Meter + persona) → Share · Duet · Care · Health · Pet · Wrapped · Reel Demo
แท็บล่าง: 🏠 บ้าน · 📸 แปลใจ · ✅ งานทาส · 🩺 เช็กอาการ · 🐾 น้อง

## 8. เทค
Next.js 14 + TS + Tailwind + shadcn/ui + framer-motion · PWA · localStorage `pawtalk:v1` + IndexedDB รูป · `/api/cues` เรียก vision model ที่มี (key ใน env) · ไม่มี key = โหมดเดโม · html-to-image สำหรับการ์ด

## 9. ความปลอดภัย/ความเป็นส่วนตัว
- บับเบิลเป็นความบันเทิง ติด disclaimer ทุกการ์ด
- Health เป็นการคัดกรองเบื้องต้น ไม่แนะนำยา/การรักษา ฉุกเฉินชี้ไปโรงพยาบาลสัตว์
- รูปอยู่ในเครื่อง ส่งออกเฉพาะตอนเรียก AI (ย่อ ≤1024px ไม่เก็บฝั่งเซิร์ฟเวอร์)
- คำพูดห้ามหยาบ/ล้อเลียนเจ้าของรุนแรง (ใช้ "ทาส" แบบมุกทั่วไปได้)

## 10. Acceptance
- 25 unit tests ตรง reference · % รวม 100 ทุกผล · persona flip ไม่เรียก AI
- Snap → บับเบิล ≤4 วินาที (โหมดเดโม ≤1 วินาที)
- Health emergency แสดงปุ่มหาโรงพยาบาลสัตว์ทุกครั้ง
- การ์ดแชร์ 1080×1920 / 1080×1350 คมชัด ฟอนต์ไทยครบ

## 11. แผนวันเดียว
| เวลา | งาน |
|---|---|
| 09:00 | Prompt A+B engine + tests |
| 10:30 | C onboarding + D Snap/Bubble |
| 12:30 | E Mood Meter/Diary + F Duet |
| 14:00 | G Care + H Health |
| 15:30 | I Wrapped/ID card + J QA |
| 16:30 | อัด Reel ตาม reel_script + deploy |
