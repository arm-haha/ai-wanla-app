RATE = 4.20  # ตัวอย่าง — ผู้ใช้ตั้งเองจากบิลจริง (ยอดรวม ÷ หน่วย)
BILL = {"month": "2026-10", "units_kwh": 440, "total_thb": 1848.0}
APPS = [
 {"id": "ac", "name_th": "แอร์ห้องนอน", "watt": 1000, "hours_per_day": 8, "category": "cooling"},
 {"id": "fridge", "name_th": "ตู้เย็น", "kwh_per_day": 1.2, "category": "kitchen"},
 {"id": "heater", "name_th": "เครื่องทำน้ำอุ่น", "watt": 3500, "hours_per_day": 0.25, "category": "bath"},
 {"id": "pc", "name_th": "คอมเล่นเกม", "watt": 200, "hours_per_day": 5, "category": "work"},
 {"id": "tv", "name_th": "ทีวี", "watt": 100, "hours_per_day": 4, "category": "entertain"},
 {"id": "rice", "name_th": "หม้อหุงข้าว", "watt": 600, "hours_per_day": 0.5, "category": "kitchen"},
]
STANDBY = [{"id": "tv_sb", "name_th": "ทีวีสแตนด์บาย", "standby_watt": 5}, {"id": "pc_sb", "name_th": "คอม+จอ ปิดไม่สุด", "standby_watt": 6},
           {"id": "charger", "name_th": "ที่ชาร์จเสียบทิ้ง", "standby_watt": 1}, {"id": "router", "name_th": "เราเตอร์", "standby_watt": 8}]
READINGS = [{"date": "2026-10-01", "meter_kwh": 10230.0}, {"date": "2026-10-08", "meter_kwh": 10318.2}, {"date": "2026-10-15", "meter_kwh": 10412.7}]
ROOMS = [{"name": "แนน", "kwh": 260}, {"name": "ฟ้า", "kwh": 180}]
