"""Demo fixture: มายด์ (Mind) picks nails for a friend's wedding. Fictional only."""
NOW = "2026-11-09T08:00:00+07:00"

def _hand(pid, hand, nails, lighting, blur, tilt):
    return {"id": pid, "hand": hand, "px_w": 3024, "px_h": 4032, "lighting": lighting, "blur": blur, "tilt": tilt, "nails": nails}

def _n(f, w, bed, free, taper, corner):
    return {"finger": f, "width_mm": w, "bed_len_mm": bed, "free_edge_mm": free, "taper": taper, "corner_round": corner}

# มายด์ 26, office worker Bangkok, friend's wedding Saturday. Medium squoval natural nails, warm undertone.
MIND = {"id": "u01", "name_th": "มายด์", "name_en": "Mind", "age": 26, "city_th": "กรุงเทพฯ",
        "goal_th": "ไปงานแต่งเพื่อนวันเสาร์ แต่จันทร์ต้องเข้าออฟฟิศ", "occasion": "wedding", "budget_thb": 900, "region": "bkk",
        "quiz": {"vein": "green", "jewelry": "gold", "sun": "tan"}, "skin_rgb": [224, 182, 140]}
MIND_PHOTO = _hand("h01", "left", [
    _n("thumb", 14.0, 13.0, 2.5, 0.10, 0.45), _n("index", 11.0, 12.0, 2.2, 0.15, 0.40),
    _n("middle", 11.5, 12.5, 2.4, 0.12, 0.42), _n("ring", 11.0, 12.0, 2.0, 0.20, 0.55),
    _n("pinky", 8.5, 9.0, 1.8, 0.15, 0.65)], lighting=0.80, blur=0.15, tilt=0.10)

PEOPLE = [
    MIND,
    {"id": "u02", "name_th": "น้องเฟิร์น", "name_en": "Fern", "age": 22, "city_th": "เชียงใหม่", "goal_th": "เล็บสั้นไปฝึกงาน",
     "occasion": "office", "budget_thb": 500, "region": "province", "quiz": {"vein": "blue", "jewelry": "silver", "sun": "burn"}, "skin_rgb": [240, 205, 200]},
    {"id": "u03", "name_th": "พี่ปอ", "name_en": "Por", "age": 30, "city_th": "พัทยา", "goal_th": "เล็บสดใสเล่นสงกรานต์",
     "occasion": "songkran", "budget_thb": 1200, "region": "tourist", "quiz": {"vein": "mixed", "jewelry": "both", "sun": "both"}, "skin_rgb": [205, 165, 140]},
    {"id": "u04", "name_th": "คุณจอย", "name_en": "Joy", "age": 35, "city_th": "อุดรธานี", "goal_th": "ต่อเล็บไปงานลอยกระทง",
     "occasion": "loy_krathong", "budget_thb": 2000, "region": "province", "quiz": {"vein": "green", "jewelry": "gold", "sun": "tan"}, "skin_rgb": [150, 110, 75]},
    {"id": "u05", "name_th": "น้องแพร", "name_en": "Prae", "age": 17, "city_th": "ขอนแก่น", "goal_th": "ทำเองที่บ้าน งบน้อย",
     "occasion": "date", "budget_thb": 300, "region": "province", "quiz": {"vein": "blue", "jewelry": "silver", "sun": "both"}, "skin_rgb": [230, 190, 175]},
]

PHOTOS = [
    MIND_PHOTO,
    _hand("h02", "right", [_n(f, 10.5, 11.0, 0.8, 0.05, 0.8) for f in ["thumb", "index", "middle", "ring", "pinky"]], 0.9, 0.1, 0.05),
    _hand("h03", "left", [_n(f, 10.0, 11.5, 4.5, 0.55, 0.7) for f in ["thumb", "index", "middle", "ring", "pinky"]], 0.40, 0.30, 0.30),
    _hand("h04", "right", [_n(f, 11.0, 12.0, 6.0, 0.50, 0.2) for f in ["thumb", "index", "middle", "ring"]], 0.70, 0.50, 0.45),
    _hand("h05", "left", [_n(f, 9.5, 10.0, 1.0, 0.0, 0.1) for f in ["thumb", "index", "middle", "ring", "pinky"]], 0.60, 0.20, 0.15),
]

# Friend vote on Mind's top picks (10 fictional friends)
MIND_VOTES = ["d01", "d01", "d02", "d01", "d05", "d01", "d01", "d02", "d01", "d11"]

DIARY = [
    ("e01", "2026-09-20", "d10", "regular", 250, 4, "ร้านใกล้ออฟฟิศ"),
    ("e02", "2026-10-11", "d04", "gel", 550, 5, "ร้านใกล้ออฟฟิศ"),
    ("e03", "2026-11-09", "d01", "gel", 690, 5, "ร้านในห้าง"),
]
