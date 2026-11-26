"""Fictional demo data only — no real people, places or brands."""
USER = {"id": "u01", "name_th": "คุณแพร", "name_en": "Prae", "age": 32, "city_th": "นนทบุรี"}
OFFICE = {"id": "u02", "name_th": "พี่ต้น", "name_en": "Ton", "age": 38, "city_th": "กรุงเทพฯ"}
KID = {"id": "u03", "name_th": "น้องใบบัว", "name_en": "Baibua", "age": 11, "city_th": "เชียงใหม่"}
SCAN = {"room_type": "living", "width_m": 4.2, "depth_m": 3.6, "tables": 1, "has_balcony": True, "rental": True,
        "zones": ["wall", "sofa", "table", "window", "ceiling"], "light": "warm", "clutter": 0.35, "confidence": 0.9}
SCAN_SMALL = {"room_type": "studio", "width_m": 3.0, "depth_m": 2.5, "tables": 1, "has_balcony": False, "rental": True,
              "zones": ["wall", "bed", "table"], "light": "cool", "clutter": 0.6, "confidence": 0.82}
SCAN_OFFICE = {"room_type": "office", "width_m": 8.0, "depth_m": 6.0, "tables": 3, "has_balcony": False, "rental": False,
               "zones": ["wall", "table", "window", "ceiling"], "light": "cool", "clutter": 0.2, "confidence": 0.88}
ADULTS, KIDS, BUDGET, HOURS = 9, 3, 4000, 5.5
START, END = "2026-12-31T19:00", "2027-01-01T00:30"
THEME = "countdown_gold"
GUESTS = ["แพร", "เอก", "แม่ติ๋ม", "ป้านวล", "บอส", "จูน", "น้าเล็ก", "ฟ้า", "ต่อ"]   # adults who join the gift swap
COUPLES = [("แพร", "เอก"), ("บอส", "จูน")]
