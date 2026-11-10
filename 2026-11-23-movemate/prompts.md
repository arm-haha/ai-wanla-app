# Work-order prompts — MoveMate

ใช้ทีละข้อกับ AI codegen (Cursor / Lovable / v0 ฯลฯ). Stack แนะนำ: Next.js + Tailwind (PWA, mobile-first) + IndexedDB สำหรับรูปในกล่อง. ใช้ `schemas.json` เป็น type กลาง และ `reference/movemate.py` เป็น logic อ้างอิง (port เป็น TS ให้ผลตรงกับ tests).

**P0 — Scaffold**: สร้าง PWA ภาษาไทย mobile-first ชื่อ MoveMate ใช้ design tokens ใน prd.md (กรมท่า #1A2330, ส้ม #F97316, เหลืองเทป #F5C451, Kanit) bottom nav: ห้อง · กล่อง · ค้นของ · วันย้าย. เก็บข้อมูลใน IndexedDB ตาม `Person` / `Box`. ทุกหน้าผลลัพธ์แสดง `SafetyGuard`.

**P1 — Room checklists**: port `room_checklist()` / `apply_checks()` ให้ตรง tests (ครัวพี่แอม 4/5 = 80%). Output `RoomChecklist`, `CheckItem`.

**P2 — Box labels + QR + photo** (wow): สร้างกล่องด้วย `make_box()` ถ่ายรูปของในกล่องเก็บในเครื่อง แสดงป้าย `MM-Bxx` และ `qr_payload`. ของเปราะบางมีแถบสี. Output `Box`, `BoxLabel`.

**P3 — Find-my-item** (wow): ช่องค้นหา → `find_item(query, boxes)` ให้ตรง tests ("ที่ชาร์จ" = MM-B04 ห้องนอน). Output `FindResult`, `FindHit`.

**P4 — Inventory stats**: `inventory_stats()` โชว์จำนวนกล่อง รายการ ของเปราะบาง และกล่องที่มีรูป. Output `InventoryStats`.

**P5 — Moving-day timeline**: port `moving_timeline(date, van_hour, rooms)` ให้ตรง tests (เสาร์ 28 พ.ย. รถ 12:00 เริ่ม 07:00). ติ๊กขั้นได้. Output `Timeline`, `TimelineStep`.

**P6 — Utility list**: `utility_list(profile)` 7 รายการ สถานะ done/pending. Output `UtilityList`, `UtilityItem`.

**P7 — Cost estimate**: port `cost_estimate(n_boxes, van_type, region)` ให้ตรง tests (10 กล่อง pickup กทม. = รถ 2,800 กล่อง 150 เทป 80 รวม 3,030). Output `CostEstimate`.

**P8 — Building notice**: ข้อความสั้นแจ้งนิติบุคคลจากวันย้ายและช่วงเวลารถ ให้แก้ก่อนคัดลอก ห้ามส่งออกอัตโนมัติ.

**P9 — Share Card + Quota**: `share_card()` 1080 มีลายน้ำ; `quota()` ฟรี 3 ป้าย/วัน. Output `ShareCard`, `Quota`.

**P10 — Safety & Privacy**: `safety_guard()` ของมีค่าไม่มีป้าย = stop; รูปเก็บในเครื่องเป็นค่าเริ่มต้น.

**P11 — Print labels**: ส่งออกป้าย 70×50 มม. / 90×60 มม. หลายใบต่อ A4 จาก `BoxLabel`.

**P12 — Tests**: เขียน unit test TS ให้ตรงกับ `reference/tests.py` ทั้ง 41 ข้อ และ validate payload ด้วย `schemas.json`.

## AI prompts
**A1 Box contents extract** (vision, JSON mode): "ดูรูปของในกล่องที่ยูสเซอร์ถ่าย. ตอบ JSON เป็นรายการชื่อของภาษาไทยสั้น ๆ และ fragile true/false ถ้ามีของแตกง่าย. ห้ามเดาสินค้าราคาหรือยี่ห้อที่ไม่ชัด. ห้ามเก็บใบหน้าหรือเอกสารที่อ่านได้เป็นข้อความเต็ม (ให้ระบุแค่ 'เอกสาร' ถ้าเห็นกระดาษ)."

**A2 Timeline narrator** (text): "จาก Timeline เขียนสรุปวันย้ายภาษาไทย ≤ 5 บรรทัด ตามเวลาใน JSON ห้ามเปลี่ยนเวลา และอย่าพูดว่าเป็นตารางของบริษัทขนย้ายจริง."

**A3 Find-item helper** (text): "จาก FindResult บอกภาษาคนว่าของอยู่กล่องไหน ห้องไหน ถ้า count=0 ให้แนะนำลองคำสั้นลงหรือดูรูปกล่อง."

**A4 Utility reminder** (text): "จาก UtilityList เขียนรายการที่ยัง pending เป็นเช็กลิสต์ภาษาสุภาพ อย่าใส่เบอร์หน่วยงานจริงถ้าผู้ใช้ยังไม่กรอก."

**A5 Privacy guard**: "ถ้าภาพในกล่องมีบัตรประชาชนหรือหน้าคน ให้เตือนผู้ใช้ให้เบลอหรือไม่เก็บภาพนั้น และคง on_device=true."
