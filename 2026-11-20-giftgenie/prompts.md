# Work-order prompts — GiftGenie

ใช้ทีละข้อกับ AI codegen (Cursor / Lovable / v0 ฯลฯ). Stack แนะนำ: Next.js + Tailwind (PWA, mobile-first) + IndexedDB. ใช้ `schemas.json` เป็น type กลาง และ `reference/giftgenie.py` เป็น logic อ้างอิง (port เป็น TS ให้ผลตรงกับ tests).

**P0 — Scaffold**: สร้าง PWA ภาษาไทย mobile-first ชื่อ GiftGenie ใช้ design tokens ใน prd.md (พื้น #3B1D2A, ครีม #F8EFE6, ชมพู #E85A71, ทอง #E0B25E, Kanit) bottom nav: ควิซ · ไอเดีย · การ์ด · ปฏิทิน. เก็บข้อมูลใน IndexedDB ตาม `Person` / `OccasionEvent`. ทุกหน้าผลลัพธ์แสดง `SafetyGuard`.

**P1 — Persona Quiz**: ฟอร์ม 5 ข้อ + ช่องงบบาท ตาม `persona_quiz()` ตรวจค่า enum และงบ ≥ 0; แสดงป้ายถ้าผู้รับเป็นเด็ก. Output `Quiz`.

**P2 — Budget Picks** (wow): port `budget_picks()` / `gift_score()` ให้ตรง tests (พี่บิ๋ม งบ 1,500 = เสื้อ FictoSoft 890 คะแนน 100 เป็นอันดับหนึ่ง ตามด้วยชุดชงชา 750 / 100 และบัตรคาเฟ่ 650 / 90). การ์ดสินค้าโชว์ช่วงราคาและเหตุผล. Output `BudgetPicks`, `GiftPick`.

**P3 — Already-has Swap**: ปุ่ม "มีอยู่แล้ว" เรียก `already_has_swap(quiz, exclude_ids)` แล้วแทนที่การ์ด. Output `SwapPicks`.

**P4 — Card Message Writer**: เลือกโทน 4 แบบ → `card_messages(occasion, tone, name, n)`; คัดลอกข้อความได้. Output `CardMessage`.

**P5 — Occasion Calendar**: `occasion_event()` + `reminder_status()` (ok/soon/due/past ตามวัน 21/7) และ `calendar_stats()`; แจ้งเตือนในเครื่อง. Output `OccasionEvent`, `ReminderStatus`, `CalendarStats`.

**P6 — Wrap Ideas**: port `wrap_ideas(budget)` ตามช่วง low/mid/high/luxe. Output `WrapIdeas`.

**P7 — Gift Library**: หน้าคลัง `GIFTS` (16 ชิ้น) ตาม `GiftInfo` กรองด้วยโอกาส/งบ/โทน ใช้ออฟไลน์ได้.

**P8 — Share Card + Quota**: `share_card()` 1080×1350/1080×1920 มีลายน้ำ; `quota()` ฟรี 3 ครั้ง/วัน. Output `ShareCard`, `Quota`.

**P9 — Safety & Age gate**: `safety_guard(is_minor, adult_item)`; ซ่อนของ `adult_only` จากผลของเด็ก และไม่โชว์ราคาเป็นคูปองจริง.

**P10 — Experience toggle**: ปุ่มกรองเฉพาะของที่เป็นประสบการณ์ (เช่น บัตรคาเฟ่) จากคลังชุดเดิม ไม่ต้องคลังใหม่.

**P11 — Last-minute copy**: ข้อความช่วยว่าของในคลังตัวอย่างหาซื้อในห้างทั่วไปได้ ไม่ต้องพรีออเดอร์ (ไม่รับประกันสต็อกจริง).

**P12 — Tests**: เขียน unit test TS ให้ตรงกับ `reference/tests.py` ทั้ง 41 ข้อ และ validate payload ด้วย `schemas.json`.

## AI prompts
**A1 Quiz clarifier** (text): "ถ้าคำตอบข้อใดคลุมเครือ ให้ถามย้ำเป็นภาษาไทยสั้น ๆ ทีละข้อ (ความสัมพันธ์ ช่วงอายุ โทน ความชอบ โอกาส งบ) ห้ามเดาของขวัญก่อนควิซครบ."

**A2 Why-it-fits writer** (text): "จาก Quiz และ GiftPick เขียนเหตุผลภาษาไทย ≤ 2 ประโยคว่าทำไมของนี้เข้ากับคนรับ ใช้คะแนนและแท็กใน JSON ห้ามเปลี่ยนราคา และห้ามพูดว่ามีของพร้อมส่ง."

**A3 Card message writer** (text): "จากโอกาส โทน และชื่อผู้รับ เขียนข้อความการ์ดภาษาไทยตามโทน ห้ามด่า ห้ามล้อเลียนช่วงไว้ทุกข์ ถ้าโทน formal ให้สุภาพ หากมีแม่แบบใน CARD_BANK ให้ใช้เป็นแนว."

**A4 Wrap stylist** (text): "จาก WrapIdeas จัดขั้นตอนห่อของ 3 ข้อ ภาษาสั้น ๆ ของใช้หาง่ายในบ้าน ห้ามบังคับซื้ออุปกรณ์แพง."

**A5 Age safety guard**: "ตรวจผล BudgetPicks — ถ้า is_minor=true ต้องไม่มีรายการ adult_only; ถ้ามีให้ตัดออกแล้วใช้ safety_guard(stop). ห้ามแนะนำแอลกอฮอล์ ของมีคม หรือยา."
