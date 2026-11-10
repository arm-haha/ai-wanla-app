"""Demo fixture: น้องปอ (Por) has a nearly full phone and a battery that dies before the day ends. Fictional only."""
TODAY = "2026-11-24"

def _shot(sid, glare, blur, crop, dets):
    return {"id": sid, "px_w": 1170, "px_h": 2532, "glare": glare, "blur": blur, "crop": crop, "detections": dets}

def _d(key, value, conf=0.93):
    return {"key": key, "value": value, "confidence": conf}

POR = {
    "id": "u01", "name_th": "น้องปอ", "name_en": "Por", "age": 26, "city_th": "กรุงเทพฯ",
    "goal_th": "มือถือเต็ม 127/128 GB แบตไม่ถึงวัน อยากรู้ว่าต้องลบอะไรหรือควรเปลี่ยนเครื่อง",
    "device_th": "FictoPhone 128 GB",
}
POR_STORAGE = _shot("s01", 0.12, 0.10, 0.08, [
    _d("used_gb", 127, 0.96), _d("total_gb", 128, 0.97),
    _d("photos_gb", 84, 0.92), _d("apps_gb", 28, 0.90),
    _d("system_gb", 10, 0.88), _d("other_gb", 5, 0.84),
])
POR_BATTERY = _shot("s02", 0.15, 0.12, 0.10, [
    _d("health_pct", 86, 0.94), _d("screen_on_h", 6.5, 0.88),
    _d("last_charge_h", 9.0, 0.85), _d("brightness_pct", 80, 0.91),
    _d("background_refresh", True, 0.87), _d("low_power", False, 0.90),
])

MUK_STORAGE = _shot("s03", 0.18, 0.10, 0.12, [
    _d("used_gb", 42, 0.95), _d("total_gb", 128, 0.96),
    _d("photos_gb", 20, 0.90), _d("apps_gb", 14, 0.88),
])
MUK_BATTERY = _shot("s04", 0.10, 0.10, 0.10, [
    _d("health_pct", 76, 0.93), _d("screen_on_h", 4.0, 0.86),
    _d("brightness_pct", 50, 0.90), _d("background_refresh", False, 0.88),
    _d("low_power", True, 0.90),
])

OLD_STORAGE = _shot("s05", 0.20, 0.15, 0.10, [
    _d("used_gb", 30, 0.92), _d("total_gb", 64, 0.95),
])
OLD_BATTERY = _shot("s06", 0.16, 0.12, 0.10, [
    _d("health_pct", 68, 0.91), _d("screen_on_h", 3.2, 0.80),
    _d("brightness_pct", 60, 0.86), _d("background_refresh", False, 0.84),
    _d("low_power", True, 0.88),
])

BAD_SHOT = _shot("s07", 0.68, 0.52, 0.50, [_d("used_gb", 100, 0.70), _d("total_gb", 128, 0.72)])
EMPTY_SHOT = _shot("s08", 0.20, 0.15, 0.10, [])
LOWCONF_SHOT = _shot("s09", 0.15, 0.10, 0.10, [_d("used_gb", 127, 0.41), _d("total_gb", 128, 0.96)])

PEOPLE = [
    POR,
    {"id": "u02", "name_th": "น้องมุก", "name_en": "Muk", "age": 24, "city_th": "ขอนแก่น",
     "goal_th": "แบตเริ่มอ่อน แต่พื้นที่ยังเหลือเยอะ", "device_th": "FictoPhone 128 GB"},
    {"id": "u03", "name_th": "ลุงสม", "name_en": "Som", "age": 58, "city_th": "เชียงใหม่",
     "goal_th": "เครื่องเก่าแบตทรุด อยากรู้ว่าซ่อมหรือเปลี่ยน", "device_th": "FictoPhone 64 GB"},
]
