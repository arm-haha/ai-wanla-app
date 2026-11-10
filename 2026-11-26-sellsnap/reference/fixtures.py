"""Demo fixture: พี่บอส (Boss) is selling a cream desk lamp. Fictional only."""
TODAY = "2026-11-26"

def _shot(sid, glare, blur, crop, dets):
    return {"id": sid, "px_w": 1170, "px_h": 2532, "glare": glare, "blur": blur, "crop": crop, "detections": dets}

def _d(key, value, conf=0.93):
    return {"key": key, "value": value, "confidence": conf}

BOSS = {
    "id": "u01", "name_th": "พี่บอส", "name_en": "Boss", "age": 31, "city_th": "กรุงเทพฯ",
    "goal_th": "ขายโคมไฟตั้งโต๊ะสีครีมสภาพดี อยากได้ชื่อโพสต์ ช่วงราคา และข้อความตอบคนทัก",
}
# quality 90: 0.35*0.12 + 0.40*0.10 + 0.25*0.08 = 0.042+0.04+0.02 = 0.102 → 90
BOSS_SHOT = _shot("s01", 0.12, 0.10, 0.08, [
    _d("category", "lamp", 0.95), _d("item_th", "โคมไฟตั้งโต๊ะ", 0.94),
    _d("color_th", "ครีม", 0.90), _d("condition", "good", 0.88),
    _d("defect_th", "มีรอยขีดเล็กที่ฐาน", 0.84), _d("wear", 0.32, 0.80),
])

NID = {
    "id": "u02", "name_th": "พี่นิด", "name_en": "Nid", "age": 28, "city_th": "ขอนแก่น",
    "goal_th": "ขายกระเป๋าผ้าสภาพพอใช้",
}
NID_SHOT = _shot("s02", 0.18, 0.12, 0.10, [
    _d("category", "bag", 0.92), _d("item_th", "กระเป๋าผ้า", 0.90),
    _d("color_th", "กรม", 0.88), _d("condition", "fair", 0.86),
    _d("defect_th", "สายเริ่มรุ่ย", 0.82),
])

SOM = {
    "id": "u03", "name_th": "น้องสม", "name_en": "Som", "age": 22, "city_th": "เชียงใหม่",
    "goal_th": "ขายหนังสือเรียนสภาพเหมือนใหม่",
}
SOM_SHOT = _shot("s03", 0.10, 0.10, 0.10, [
    _d("category", "book", 0.96), _d("item_th", "หนังสือเตรียมสอบ", 0.93),
    _d("condition", "like_new", 0.91),
])

# wear-only shot (no condition key) for inference
WEAR_SHOT = _shot("s04", 0.15, 0.10, 0.10, [
    _d("category", "chair", 0.90), _d("item_th", "เก้าอี้ไม้", 0.88),
    _d("wear", 0.70, 0.85),
])

BAD_SHOT = _shot("s05", 0.68, 0.52, 0.50, [_d("category", "lamp", 0.70), _d("item_th", "โคมไฟ", 0.68)])
EMPTY_SHOT = _shot("s06", 0.20, 0.15, 0.10, [])
LOWCONF_SHOT = _shot("s07", 0.12, 0.10, 0.08, [
    _d("category", "lamp", 0.41), _d("item_th", "โคมไฟตั้งโต๊ะ", 0.94),
])

# inventory for sold-log tests
INVENTORY = [
    {"id": "l01", "status": "for_sale", "ask_thb": 600, "sold_thb": None, "date": None, "title_th": "โคมไฟตั้งโต๊ะ สีครีม สภาพดี"},
    {"id": "l02", "status": "for_sale", "ask_thb": 300, "sold_thb": None, "date": None, "title_th": "กระเป๋าผ้า สีกรม ใช้งานได้ มีรอย"},
    {"id": "l03", "status": "sold", "ask_thb": 80, "sold_thb": 80, "date": "2026-11-20", "title_th": "หนังสือเตรียมสอบ เหมือนใหม่"},
]

PEOPLE = [BOSS, NID, SOM]
