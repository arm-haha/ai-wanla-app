# Work-order prompts — SingScore

ใช้ทีละข้อกับ AI codegen (Cursor / Lovable / v0 ฯลฯ). Stack แนะนำ: Next.js + Tailwind (PWA, mobile-first) + pitch/timing detector บนเครื่อง + IndexedDB. ใช้ `schemas.json` เป็น type กลาง และ `reference/singscore.py` เป็น logic อ้างอิง (port เป็น TS ให้ผลตรงกับ tests). **ห้ามใส่เนื้อเพลงหรือไฟล์คาราโอเกะที่มีลิขสิทธิ์ในโปรเจกต์.**

**P0 — Scaffold**: สร้าง PWA ภาษาไทย mobile-first ชื่อ SingScore ใช้ design tokens ใน prd.md (กรม #111827, ชมพู #F472B6, เหลือง #FBBF24, Kanit) bottom nav: แบบฝึก · วอร์ม · คะแนน · บันทึก. ทุกหน้าผลลัพธ์แสดง `SafetyGuard` และข้อความว่าไม่มีเนื้อเพลงลิขสิทธิ์ในแพ็ก.

**P1 — Exercise picker**: โหลด `EXERCISES` 6 แบบฝึกต้นฉบับเท่านั้น (ScaleRun C/G/F, BreathPulse, HumFifth, VowelHold). Output `ExerciseInfo`.

**P2 — Record take**: รับเสียงฮัม/ร้องแบบฝึก แล้วสกัด mean_cents_off, mean_ms_off, notes, confidence (ในแอปจริง). อ้างอิงรูปทรง `Take`. ความมั่นใจ < 0.6 ไม่ให้คะแนน.

**P3 — Pitch / timing score** (wow): port `score_take()` ให้ตรง tests (พี่ต้อม 36 cents / 52 ms = เสียง 82 จังหวะ 74 รวม 79 good). Output `Score`.

**P4 — Key finder**: port `key_finder(notes, exercise)` แบบฝึก C = C major. Output `KeyFind`.

**P5 — Warm-ups**: port `warmups()` 4 ท่า 100 วินาที ลิปทริลล์เป็นท่าแรก. Output `WarmupSet`, `WarmupItem`.

**P6 — Duet battle**: port `duet_battle()` พี่ต้อม 79 vs น้องนีน่า 72 = นำ 7 แต้ม. Output `DuetBattle`.

**P7 — Practice log**: port `practice_log()`. Output `PracticeLog`, `LogRow`.

**P8 — Own-track disclaimer**: ถ้าผู้ใช้จะอัปโหลดแทร็ก ให้ยืนยันว่าตนมีสิทธิ์ใช้ และไม่เก็บไฟล์เพลงไว้ในเซิร์ฟเวอร์ถ้าไม่จำเป็น.

**P9 — Share Card + Quota**: `share_card()` 1080 มีลายน้ำ; `quota()` ฟรี 3 ครั้ง/วัน. Output `ShareCard`, `Quota`.

**P10 — Safety**: `safety_guard(sore_throat, strain)` เจ็บคอ = หยุด.

**P11 — Privacy**: ลบไฟล์เสียงหลังให้คะแนนได้ ห้ามส่งเสียงไปเทรนโมเดลภายนอกโดยไม่ขออนุญาต.

**P12 — Tests**: เขียน unit test TS ให้ตรงกับ `reference/tests.py` ทั้ง 41 ข้อ และ validate payload ด้วย `schemas.json`.

## AI prompts
**A1 Take extract** (audio, JSON mode): "จากคลิปที่ผู้ใช้ฮัมแบบฝึกต้นฉบับ (ไม่ใช่เพลงเชิงพาณิชย์) ตอบ JSON: mean_cents_off >=0, mean_ms_off >=0, notes เป็นชื่อโน้ตเช่น C D E, confidence 0–1. ห้ามถอดเป็นเนื้อเพลง ห้ามระบุชื่อเพลงที่มีลิขสิทธิ์."

**A2 Score narrator** (text): "จาก Score เขียนสรุปภาษาไทย ≤ 3 บรรทัด ใช้ตัวเลขใน JSON เท่านั้น ห้ามชมว่าคุณภาพระดับมืออาชีพ."

**A3 Warmup coach** (text): "ใช้ how_th จาก WarmupItem ตามเดิม น้ำเสียงเบา ย้ำว่าเจ็บคอแล้วหยุด."

**A4 Duet caption** (text): "จาก DuetBattle เขียนบรรทัดเดียวตาม headline_th ห้ามบอกว่าเป็นการประกวดจริง."

**A5 Lyrics / strain guard**: "ถ้าผู้ใช้วางเนื้อเพลงลิขสิทธิ์ให้ปฏิเสธและชวนใช้แบบฝึกต้นฉบับ; ถ้าบอกว่าเจ็บคอ ให้ใช้ safety_guard(sore_throat=True)."
