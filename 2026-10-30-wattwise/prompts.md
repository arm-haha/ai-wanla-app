# Work-order prompts — WattWise (วางทีละอันใน AI codegen: v0 / Lovable / Bolt / Cursor)

**P0 — Scaffold**
สร้างเว็บแอป mobile-first ชื่อ "WattWise — ค่าไฟไปไหนหมด" ด้วย React + Vite + Tailwind ภาษาไทยทั้งหมด ธีมมืด bg #0B1220 การ์ด #111A2E สีหลัก volt #FACC15, cool #38BDF8, save #22C55E, burn #F97316, danger #EF4444 ฟอนต์ IBM Plex Sans Thai ตัวเลข tabular-nums ใหญ่ bottom tab 5 แท็บ: หน้าแรก / ถ่าย / เครื่องใช้ / ประหยัด / แชร์ เก็บข้อมูล localStorage ตาม schemas.json (Home, Appliance, Bill, MeterReading, StandbyItem) ไม่ต้องล็อกอิน

**P1 — Onboarding**
3 สเต็ป: ชื่อบ้าน, ผู้ให้บริการ (MEA/PEA/คอนโด/อื่น ๆ), เรท ฿/หน่วย (ปุ่ม "คำนวณจากบิล" = ยอด÷หน่วย), เป้าค่าไฟ/เดือน, จำนวนคน ปุ่ม "ลองด้วยข้อมูลตัวอย่าง" โหลด fixture ของแนน

**P2 — Logic module**
พอร์ต reference/wattwise.py เป็น TypeScript (lib/wattwise.ts) ฟังก์ชัน kwhMonth, applianceCost, acTempSim, billBreakdown, standbyLeak, goalTrack, roomSplit, swapPayback ปัดทศนิยม 2 ตำแหน่ง ผลลัพธ์ต้องตรงกับ examples.json ทุกตัว เขียน unit test (vitest) ตาม tests.py

**P3 — Bill Snap (vision)**
หน้าถ่าย/อัปโหลดบิล ส่งรูปไป vision model ด้วย VISION PROMPT ด้านล่าง ได้ BillExtract ถ้า needs_confirm หรือ confidence<0.6 ให้ฟอร์มยืนยันหน่วย/ยอด บันทึก Bill แล้วไปหน้า Bill Pie

**P4 — Bill Pie (wow)**
donut chart แอนิเมชันเด้งทีละชิ้นเรียงจากใหญ่ไปเล็ก ตรงกลางแสดง "฿1,848" แล้วเปลี่ยนเป็น "แอร์ 55%" ชิ้นสีเทา "ยังหาไม่เจอ" + ปุ่ม "เพิ่มเครื่องใช้" ถ้า over_estimated ขึ้นเตือน "ประมาณเกินบิล ลองลดชั่วโมง" แตะชิ้นไหนเปิดรายละเอียด ฿/เดือน ฿/ปี ฿/ชม.

**P5 — Appliance Snap + list**
preset 12 เครื่อง (แอร์ 9k/12k/18k BTU, ตู้เย็น, น้ำอุ่น, หม้อหุงข้าว, ไมโครเวฟ, เตารีด, เครื่องซักผ้า, คอม, ทีวี, พัดลม) แก้วัตต์ได้ ถ่ายป้าย/ฉลากเบอร์ 5 → LABEL PROMPT → LabelExtract สไลเดอร์ชั่วโมง/วัน 0–24 ค่าเงินอัปเดตสด tier สี

**P6 — AC Temp Slider (wow #2)**
สไลเดอร์ 18–30°C ใหญ่เต็มจอ พื้นหลังไล่สีส้ม→ฟ้าตามอุณหภูมิ ตัวเลข ฿/เดือน วิ่งแบบ count-up แสดง "ประหยัด ฿X/เดือน · ฿Y/ปี" และบรรทัด assumption_th เสมอ ปุ่มตั้งค่า %/°C (0–20%, default 10%)

**P7 — Standby Leak Hunter**
เช็กลิสต์การ์ด (ทีวี, คอม+จอ, ที่ชาร์จ, เราเตอร์, ไมโครเวฟนาฬิกา, กล่องทีวี, ลำโพง) ใส่วัตต์สแตนด์บายได้ แสดงฟองเงินรั่ว ฿/ปี ไฮไลต์ worst_id

**P8 — Goal & Meter Tracker**
ถ่ายมิเตอร์ (vision อ่านตัวเลข ยืนยันเสมอ) หรือพิมพ์ กราฟเส้นใช้จริงเทียบเส้นงบ แสดง projected_thb, on_track (เขียว/แดง), budget_per_day_kwh กันมิเตอร์ถอยหลัง

**P9 — Fair Split + Swap Payback + Tip Deck**
Split: ใส่ชื่อรูมเมท+หน่วย (หรือเลือกเครื่องใช้ของแต่ละคน) → roomSplit เทียบกับหารเท่า; Swap: วัตต์เก่า/ใหม่/ชม./ราคา → payback_months; Tips: สร้างจาก acSim, standby, habit เรียงตาม save_month_thb ติ๊กทำแล้วสะสม "ประหยัดแล้ว ฿"

**P10 — Share Cards**
5 การ์ด 1080×1920 (bill_pie, ac_save, standby, goal, split) ใช้ html-to-image ดาวน์โหลด/แชร์ ตัวเลขใหญ่ volt บนพื้น night + disclaimer_th เล็กด้านล่าง + โลโก้ "AI วันละแอป"

---
**VISION PROMPT — bill**
คุณอ่านใบแจ้งค่าไฟฟ้าไทย (กฟน./กฟภ./นิติคอนโด) จากรูป ตอบ JSON ตาม BillExtract เท่านั้น: units_kwh (จำนวนหน่วยที่ใช้), total_thb (ยอดรวมที่ต้องชำระ), period_th, meter_prev, meter_now, confidence 0–1, needs_confirm ถ้าตัวเลขไม่ชัดให้ใส่ null และ needs_confirm=true ห้ามเดา ห้ามคำนวณอัตราเอง

**VISION PROMPT — label**
อ่านป้ายสเปก/ฉลากประหยัดไฟเบอร์ 5 ของเครื่องใช้ไฟฟ้า ตอบ JSON ตาม LabelExtract: name_th, watt (กำลังไฟฟ้า W), btu (ถ้าเป็นแอร์), energy_label_stars, kwh_per_year (ถ้าฉลากระบุ), confidence, needs_confirm ถ้าไม่เห็นค่าให้ null ห้ามเดาวัตต์จากรุ่น

**VISION PROMPT — meter**
อ่านเลขหน่วยบนมิเตอร์ไฟฟ้า ตอบ {"meter_kwh": number|null, "confidence": 0–1} ถ้าหน้าปัดเบลอหรือมีตัวเลขเลื่อนครึ่งหลักให้ confidence ต่ำ
