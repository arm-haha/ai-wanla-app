# ข้อมูลสมมติสำหรับ demo — ไม่ใช่ราคาสินค้าจริง
PROFILE = {"name": "มายด์", "monthly_income": 25000, "work_days": 22, "hours_per_day": 8, "jar_goal_thb": 15000, "jar_goal_name_th": "ตั๋วญี่ปุ่น"}
BAG = {"id": "bag", "name_th": "กระเป๋าสะพายข้าง", "price_thb": 3990, "category": "fashion", "source": "screenshot"}
SNEAKER = {"id": "sneaker", "name_th": "รองเท้าวิ่ง", "price_thb": 2890, "category": "sport", "source": "photo"}
LATTE = {"id": "latte", "name_th": "ลาเต้เย็น", "price_thb": 75, "category": "food", "source": "manual"}
PHONE = {"id": "phone", "name_th": "มือถือรุ่นใหม่", "price_thb": 32900, "category": "gadget", "source": "link"}
BAG_ANS = {"need": False, "have_similar": True, "want_30d": False, "cash_ready": True, "sale_pressure": True}
SNEAKER_ANS = {"need": True, "have_similar": False, "want_30d": True, "cash_ready": True, "sale_pressure": False}
PHONE_ANS = {"need": False, "have_similar": True, "want_30d": True, "cash_ready": False, "sale_pressure": False}
SKIPS = [{"name_th": "กระเป๋าสะพายข้าง", "price_thb": 3990}, {"name_th": "หูฟังไร้สาย", "price_thb": 1590},
         {"name_th": "เสื้อแจ็กเก็ต", "price_thb": 1290}]
DECISIONS = [dict(s, outcome="skipped") for s in SKIPS] + [{"name_th": "รองเท้าวิ่ง", "price_thb": 2890, "outcome": "bought"}]
