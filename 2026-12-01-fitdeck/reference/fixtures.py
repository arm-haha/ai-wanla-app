"""Demo fixture: พี่กิ๊ฟ (Gift) has a yoga mat and 4 kg dumbbells at home. Fictional only."""
TODAY = "2026-12-01"

def _shot(sid, glare, blur, crop, dets):
    return {"id": sid, "px_w": 1170, "px_h": 2532, "glare": glare, "blur": blur, "crop": crop, "detections": dets}

def _d(key, value=True, conf=0.93):
    return {"key": key, "value": value, "confidence": conf}

GIFT = {
    "id": "u01", "name_th": "พี่กิ๊ฟ", "name_en": "Gift", "age": 29, "city_th": "กรุงเทพฯ",
    "goal_th": "อยากออกกำลัง 20 นาทีที่บ้านด้วยเสื่อโยคะและดัมเบิล 4 กก.",
}
GIFT_SHOT = _shot("s01", 0.12, 0.10, 0.08, [
    _d("yoga_mat", True, 0.95), _d("dumbbell", True, 0.94), _d("weight_kg", 4, 0.88),
])

BEE = {
    "id": "u02", "name_th": "พี่บี", "name_en": "Bee", "age": 41, "city_th": "ขอนแก่น",
    "goal_th": "ไม่มีอุปกรณ์ อยากได้แผนน้ำหนักตัว",
}
BEE_SHOT = _shot("s02", 0.15, 0.12, 0.10, [])  # no gear, bodyweight — quality? n_dets=0, score drops 30

# Recalibrate Bee: we still want a usable photo of an empty corner that's sharp
# so quality ok without detections? parse_gear ok if score>=60, but n_dets=0 subtracts 30.
# Use a shot with bodyweight explicitly? Or a chair only.
# Better: empty room with no detections, but I want score>=60 without -30... 
# Actually I'll give Bee a chair+wall photo.
BEE_SHOT = _shot("s02", 0.12, 0.10, 0.10, [_d("chair", True, 0.90), _d("wall", True, 0.86)])

TON = {
    "id": "u03", "name_th": "น้องต้น", "name_en": "Ton", "age": 24, "city_th": "เชียงใหม่",
    "goal_th": "มีเชือกกระโดดกับยางยืด อยากลองระดับกลาง",
}
TON_SHOT = _shot("s03", 0.10, 0.10, 0.10, [_d("jump_rope", True, 0.92), _d("resistance_band", True, 0.90)])

BAD_SHOT = _shot("s04", 0.68, 0.52, 0.50, [_d("yoga_mat", True, 0.70)])
EMPTY_SHOT = _shot("s05", 0.20, 0.15, 0.10, [])
LOWCONF_SHOT = _shot("s06", 0.12, 0.10, 0.08, [_d("dumbbell", True, 0.41), _d("yoga_mat", True, 0.95)])

PEOPLE = [GIFT, BEE, TON]
