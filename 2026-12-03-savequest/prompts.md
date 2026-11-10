# Work-order prompts — SaveQuest

ใช้ทีละข้อกับ AI codegen (Cursor / Lovable / v0 ฯลฯ). Stack แนะนำ: Next.js + Tailwind (PWA, mobile-first) + vision model สำหรับอ่านรูปเป้า (ไม่บังคับถ้าผู้ใช้เลือกจากคลัง) + IndexedDB. ใช้ `schemas.json` เป็น type กลาง และ `reference/savequest.py` เป็น logic อ้างอิง (port เป็น TS ให้ผลตรงกับ tests).

**P0 — Scaffold**: สร้าง PWA ภาษาไทย mobile-first ชื่อ SaveQuest ใช้ design tokens ใน prd.md (กรมท่าอุ่น #1A1423, ทอง #F5C84C, ส้ม #E8772E, ครีม #F8F1E3, Kanit) bottom nav: กระปุก · ชาเลนจ์ · แผน · ร่วมกัน. เก็บข้อมูลใน IndexedDB ตาม `Person`. ทุกหน้าผลลัพธ์แสดง `SafetyGuard`.

**P1 — Goal Snap**: กล้องหรือเลือกรูปความฝัน + เตือนแสงสะท้อน/เบลอ/ครอป ตาม `scan_quality()`; ถ้า `ok=false` แสดง `tips_th` และปุ่มถ่ายใหม่. Output `GoalPhoto`, `ScanQuality`.

**P2 — Goal Library**: โหลด `GOALS` ตาม `GoalInfo`; ให้เลือกเป้าหรือกรอกเอง (ชื่อ + จำนวนเงิน + วันเริ่ม/วันเป้า). Output `GoalInfo`.

**P3 — Goal Jar Studio** (wow): port `jar_fill()` / `milestones()` ให้ตรง tests (น้องมิ้น = 42% growing อีก ฿3,600 ถึง 50%). แอนิเมชันน้ำ/เหรียญในกระปุกวิ่งขึ้นจนถึง %. Output `JarFill`, `Milestones`.

**P4 — Daily Challenge**: แสดง `daily_challenge(today, user_id)` และให้เลือกจากคลัง 8 ข้อ → `complete_challenge()` แล้วบวก `save_thb` เข้ากระปุก. Output `Challenge`, `CompletedChallenge`.

**P5 — 52-Week Plan**: port `week52_plan()` / `week52_fit_base()`; แสดงปฏิทิน 52 ช่อง ติ๊กสัปดาห์ที่ออมแล้ว. Output `Week52Plan`.

**P6 — Random-Number Plan**: port `random_plan(week, base, seed)` ให้ผลคงที่ต่อ seed เดียวกัน (มิ้นสัปดาห์ 18 = ตัวคูณ 38 ฿3,800). Output `RandomPlan`.

**P7 — Streaks**: port `streak(dates, today, frozen_dates)`; ปุ่มใช้โทเคนแช่แข็งได้ 1 วัน ป้ายไฟลุกเมื่อ ≥ 7 วัน. Output `Streak`.

**P8 — Round-Up + Team Jar**: `round_up(amount, step)` และ `team_jar(goal, contributions)` แสดงสัดส่วนแต่ละคน. Output `RoundUp`, `TeamJar`.

**P9 — Share Card + Quota**: `share_card()` 1080×1350/1080×1920 มีลายน้ำ; `quota()` ฟรี 3 รูปเป้า/วัน paywall สุภาพ. Output `ShareCard`, `Quota`.

**P10 — Safety & Privacy**: `safety_guard()` ทุกผล; ยอดเงินเก็บในเครื่อง; ห้ามอ้างว่าเป็นบัญชีเงินฝากหรือผลตอบแทนการลงทุน.

**P11 — Onboarding copy**: หน้าแรกบอกสั้น ๆ ว่าเป็นเกมช่วยออม ไม่ใช่ธนาคาร พร้อมตัวอย่างกระปุก 42% (ภาพวาด).

**P12 — Tests**: เขียน unit test TS ให้ตรงกับ `reference/tests.py` ทั้ง 41 ข้อ และ validate payload ด้วย `schemas.json`.

## AI prompts
**A1 Goal photo extract** (vision, JSON mode): "ดูรูปที่ผู้ใช้ตั้งเป็นเป้าออมเงิน. ตอบ JSON: subject (เช่น เที่ยว, รถ, บ้าน, แกเจ็ต, อื่น ๆ), confidence 0–1, glare 0–1, blur 0–1, crop 0–1. ห้ามเดาราคาจริง ห้ามอ่านข้อความส่วนตัวในใบเสร็จ และห้ามระบุตัวบุคคล. ถ้าไม่ใช่รูปเป้า ให้บอกสั้น ๆ ภาษาไทย."

**A2 Jar copy writer** (text): "จาก JSON JarFill และ Milestones เขียนประโยคกำลังใจภาษาไทย ≤ 2 ประโยค น้ำเสียงอบอุ่น ไม่กดดัน ห้ามเปลี่ยนตัวเลข % หรือบาทใน JSON และห้ามสัญญาว่าจะถึงเป้าแน่นอน."

**A3 Challenge writer** (text): "จากชาเลนจ์ที่สำเร็จ เขียนข้อความยินดีสั้น ๆ ≤ 1 ประโยค รวมจำนวนบาทที่เก็บได้ ห้ามเพิ่มจำนวนเอง."

**A4 Milestone card composer** (image/layout): "จัดเป็นการ์ดแชร์ตาม ShareCard: ชื่อเป้า, เปอร์เซ็นต์, สตรีค, กระปุกโต, disclaimer ด้านล่าง. ใช้โทนทอง-ส้ม. ห้ามใส่โลโก้ธนาคารจริง."

**A5 Over-promise guard**: "ตรวจ A2/A3 — ห้ามใช้คำว่า รับประกัน, กำไร, ดอกเบี้ย, ผลตอบแทน. ถ้าข้อความขัดกับตัวเลขใน JSON ให้ใช้ headline จาก `jar_fill()` แทน."
