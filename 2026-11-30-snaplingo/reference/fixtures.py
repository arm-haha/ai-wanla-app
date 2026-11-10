"""Demo fixture: พี่แอน (Ann) helps น้องเต้า (Tao), 7, learn words from kitchen objects. Fictional only — no child photos."""
TODAY = "2026-11-30"

def _shot(sid, glare, blur, crop, dets):
    return {"id": sid, "px_w": 1170, "px_h": 2532, "glare": glare, "blur": blur, "crop": crop, "detections": dets}

def _d(key, conf=0.93):
    return {"key": key, "value": True, "confidence": conf}

ANN = {
    "id": "u01", "name_th": "พี่แอน", "name_en": "Ann", "age": 34, "city_th": "กรุงเทพฯ", "role": "parent",
    "goal_th": "อยากให้ลูกเรียนรู้คำศัพท์จากของในครัว โดยไม่ต้องถ่ายหน้าลูก",
}
TAO = {
    "id": "u02", "name_th": "น้องเต้า", "name_en": "Tao", "age": 7, "city_th": "กรุงเทพฯ", "role": "child",
    "goal_th": "เล่นทายคำจากกาต้มน้ำ แก้ว และช้อน",
    "parent_id": "u01",
}
# quality 89: 0.35*0.12 + 0.40*0.10 + 0.25*0.12 = 0.112
KITCHEN = _shot("s01", 0.12, 0.10, 0.12, [_d("kettle", 0.96), _d("cup", 0.94), _d("spoon", 0.91)])
# Tao answers: kettle ok, cup wrong (picks plate?), spoon ok → 2/3
# We'll set answers in tests after seeing choice keys.

ROOM = _shot("s02", 0.10, 0.10, 0.10, [_d("chair", 0.92), _d("book", 0.90)])
BAD_SHOT = _shot("s03", 0.68, 0.52, 0.50, [_d("cup", 0.70)])
EMPTY_SHOT = _shot("s04", 0.20, 0.15, 0.10, [])
LOWCONF_SHOT = _shot("s05", 0.12, 0.10, 0.12, [_d("kettle", 0.41), _d("cup", 0.94)])

PEOPLE = [ANN, TAO]
