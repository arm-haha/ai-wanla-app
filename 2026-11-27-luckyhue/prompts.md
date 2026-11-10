# Work-order prompts — LuckyHue

ใช้ทีละข้อกับ AI codegen (Cursor / Lovable / v0 ฯลฯ). Stack แนะนำ: Next.js + Tailwind (PWA, mobile-first) + vision สำหรับอ่านตู้เสื้อผ้า + IndexedDB. ใช้ `schemas.json` เป็น type กลาง และ `reference/luckyhue.py` เป็น logic อ้างอิง (port เป็น TS ให้ผลตรงกับ tests).

**P0 — Scaffold**: สร้าง PWA ภาษาไทย mobile-first ชื่อ LuckyHue ใช้ design tokens ใน prd.md (ฟ้า #38BDF8, พื้น #E0F2FE, Kanit) bottom nav: สีของฉัน · ตู้เสื้อผ้า · วอลเปเปอร์ · ปฏิทิน. ทุกหน้าผลลัพธ์แสดง `SafetyGuard` และ disclaimer เพื่อความสนุก.

**P1 — Birth day**: เลือกวันในสัปดาห์หรือใส่วันเกิด → port `weekday_from_date()` / `lucky_color()`. พี่เมย์ 1998-05-01 และวันนี้ 2026-11-27 = วันศุกร์ สีฟ้า #38BDF8. Output `LuckyColor`.

**P2 — Closet Snap**: กล้องหลัง + กรอบเสื้อผ้า + เตือนแสง/เบลอ/ครอป ตาม `scan_quality()`. Output `ClosetPhoto`, `ScanQuality`.

**P3 — Closet Read**: เรียก vision A1 → port `parse_closet()`. พี่เมย์คุณภาพ 88 เจอ 5 ชิ้น. Output `ClosetScan`, `ClosetItem`.

**P4 — Outfit mixer** (wow): port `outfit_mix()` ให้ตรง tests (เสื้อขาว + กระโปรงฟ้า + กระเป๋าเบจ = แมตช์ คะแนน 67; เสื้อชมพู+กระโปรงฟ้า = clash; อัตโนมัติ 4 ชิ้น คะแนน 62). Output `OutfitMix`.

**P5 — Wallpaper**: port `wallpaper()` ขนาด 1080×1920 / 1080×1080 / 1170×2532 พาเลตต์ + คำอวยพร + ลายน้ำ. Output `Wallpaper`.

**P6 — Weekly calendar**: port `weekly_calendar()` สัปดาห์เริ่มวันจันทร์ (27 พ.ย. 2026 → เริ่ม 23 พ.ย.) ไฮไลต์วันเกิด. Output `WeeklyCalendar`, `CalendarDay`.

**P7 — Color library**: โชว์ 7 วันจาก `WEEKDAYS` / `ColorInfo` มีสวิตช์พุธกลางคืนแสด.

**P8 — Today badge**: ถ้า `today_is_birth_day` โชว์ป้ายวันนี้สีมงคลของคุณ.

**P9 — Share Card + Quota**: `share_card()` 1080 มีลายน้ำ; `quota()` ฟรี 3 ครั้ง/วัน. Output `ShareCard`, `Quota`.

**P10 — Safety**: `safety_guard(treats_as_fortune)` ถ้าผู้ใช้จะใช้สีตัดสินใจเรื่องเงิน/สุขภาพ = เตือน.

**P11 — Privacy**: ลบรูปตู้เสื้อผ้าได้หลังมิกซ์ชุด ห้ามระบุที่อยู่หรือคนในรูป.

**P12 — Tests**: เขียน unit test TS ให้ตรงกับ `reference/tests.py` ทั้ง 41 ข้อ และ validate payload ด้วย `schemas.json`.

## AI prompts
**A1 Closet extract** (vision, JSON mode): "ดูรูปเสื้อผ้าในตู้หรือที่วางเรียง. ตอบ JSON เป็นรายการชิ้น: id, name_th, category ใน {top, bottom, shoes, bag, accessory}, color_key (english สั้น เช่น blue, white, beige, pink, navy), color_th, confidence 0–1. ถ้าไม่ใช่รูปเสื้อผ้า ให้บอกสั้น ๆ ภาษาไทย. ห้ามระบุยี่ห้อที่มีโลโก้ชัดถ้าไม่จำเป็น ห้ามบรรยายคนในรูป."

**A2 Outfit narrator** (text): "จาก OutfitMix เขียนสรุปภาษาไทย ≤ 3 บรรทัด ใช้จำนวนชิ้นและสีใน JSON เท่านั้น ห้ามบอกว่าใส่แล้วจะโชคดี."

**A3 Wallpaper copy** (text): "จาก Wallpaper เขียนคำโปรยสั้น รวมสีและคำอวยพรใน JSON ห้ามเพิ่มคำทำนาย."

**A4 Week blurb** (text): "จาก WeeklyCalendar เขียนบรรทัดเดียวว่าสัปดาห์นี้ไฮไลต์วันใด สีใด ตาม JSON."

**A5 Fortune guard**: "ถ้าผู้ใช้ถามว่าสีนี้จะทำให้รวยหรือได้รัก ให้ใช้ข้อความ safety_guard(treats_as_fortune=True) และย้ำว่าเพื่อความสนุก."
