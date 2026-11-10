"""Demo fixture: พี่เมย makes an 8-month milestone card for น้องภู. Fictional only."""
TODAY = "2026-12-04"

def _photo(pid, glare, blur, crop, child_id="c01"):
    return {"id": pid, "px_w": 3024, "px_h": 4032, "glare": glare, "blur": blur, "crop": crop, "child_id": child_id}

PHU_PHOTO = _photo("p01", 0.10, 0.10, 0.10)
PHU = {
    "id": "c01", "name_th": "น้องภู", "name_en": "Phu", "birth": "2026-04-04",
    "weight_kg": 8.4, "height_cm": 70.0, "photo": PHU_PHOTO,
}
MEY = {
    "id": "u01", "name_th": "พี่เมย", "name_en": "Mey", "age": 31, "city_th": "กรุงเทพฯ",
    "relation_th": "แม่", "own_child": True, "parent_confirmed": True, "all_guardians_ok": True,
    "child": PHU,
}
NAN = {
    "id": "u02", "name_th": "พี่แนน", "name_en": "Nan", "age": 28, "city_th": "เชียงใหม่",
    "relation_th": "แม่", "own_child": True, "parent_confirmed": True, "all_guardians_ok": True,
    "child": {
        "id": "c02", "name_th": "น้องไผ่", "name_en": "Phai", "birth": "2025-12-04",
        "weight_kg": 9.8, "height_cm": 76.0, "photo": _photo("p02", 0.16, 0.12, 0.14, "c02"),
    },
}
PEOPLE = [MEY, NAN]
PHOTOS = [
    PHU_PHOTO,
    NAN["child"]["photo"],
    _photo("p03", 0.62, 0.48, 0.55, "c01"),
    _photo("p04", 0.18, 0.10, 0.12, "c01"),
    _photo("p05", 0.12, 0.14, 0.10, "c02"),
]
PHU_FIRSTS = [
    ("smile", 2, "ยิ้มให้แม่ครั้งแรก"),
    ("roll", 5, "พลิกจากหงายเป็นคว่ำ"),
    ("sit", 8, "นั่งเล่นได้นานขึ้น"),
]
# 8 monthly slots for collage (months 1-8) — fictional illustrated photo ids
PHU_COLLAGE = [{"photo_id": f"m{i:02d}", "month": i, "label_th": f"เดือนที่ {i}"} for i in range(1, 9)]
