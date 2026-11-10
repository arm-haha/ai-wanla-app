"""Demo fixture: พี่แอม (Am) is moving a 1-bedroom condo on Saturday. Fictional only."""
TODAY = "2026-11-23"
MOVE_DATE = "2026-11-28"  # Saturday
VAN_HOUR = 12

AM = {
    "id": "u01", "name_th": "พี่แอม", "name_en": "Am", "age": 33, "city_th": "กรุงเทพฯ",
    "goal_th": "ย้ายคอนโด 1 ห้องนอนไปเช่าใหม่วันเสาร์ โดยไม่ทำของหาย",
    "move_date": MOVE_DATE, "region": "bkk", "van_type": "pickup", "van_hour": VAN_HOUR,
}

def _box(n, room, contents, fragile=False, photo=None):
    from movemate import make_box, _code
    return make_box(_code(n), room, contents, fragile, photo)

# built lazily in tests via make_box to avoid import cycle at module load? fixtures can import after path set.
# We'll construct in a function.

AM_BOX_SPECS = [
    (1, "kitchen", ["จานชามชุดขาว", "แก้วน้ำ 8 ใบ", "ชามซุป"], True, "ph01"),
    (2, "kitchen", ["เครื่องปรุง", "ข้าวสาร", "กาแฟ"], False, "ph02"),
    (3, "bedroom", ["เสื้อผ้าฤดูหนาว", "เสื้อยืด", "กางเกง"], False, "ph03"),
    (4, "bedroom", ["ที่ชาร์จมือถือ", "สาย USB", "ปลั๊กพ่วง", "หูฟัง"], False, "ph04"),
    (5, "living", ["หนังสือ 12 เล่ม", "กรอบรูป"], False, "ph05"),
    (6, "bathroom", ["ผ้าเช็ดตัว", "ของใช้ในห้องน้ำ"], False, None),
    (7, "balcony", ["ต้นไม้เล็ก 2 ใบ", "ราวพับ"], True, "ph07"),
    (8, "living", ["สาย HDMI", "รีโมทสำรอง", "อุปกรณ์ทีวี"], False, "ph08"),
    (9, "misc", ["เอกสารสัญญาเช่า", "แฟ้มประกัน"], False, None),
    (10, "kitchen", ["หม้อกระทะ", "เขียง"], False, "ph10"),
]
AM_PACKED = {
    "kitchen": ["kitchen_1", "kitchen_2", "kitchen_3", "kitchen_4"],
    "bedroom": ["bedroom_1", "bedroom_5"],
    "bathroom": [],
}
AM_UTILS = {
    "electricity": "การไฟฟ้า FictoMEA นัด 28 พ.ย. 16:00",
    "water": "ประปา FictoMWA แจ้งแล้วยกเลิก 29 พ.ย.",
    "internet": None, "parcel": None, "keys": None, "address": "แจ้งที่ทำงานแล้ว", "waste": None,
}

BEE = {
    "id": "u02", "name_th": "น้องบี", "name_en": "Bee", "age": 27, "city_th": "เชียงใหม่",
    "goal_th": "ย้ายบ้านเช่าในเชียงใหม่ด้วยรถเล็ก",
    "move_date": "2026-12-05", "region": "province", "van_type": "pickup", "van_hour": 9,
}
