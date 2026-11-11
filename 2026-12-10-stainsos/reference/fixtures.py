"""Demo fixture: น้องแพร rescues a white cotton uniform shirt with a Thai-tea stain. Fictional only."""
from stainsos import parse_stain

def _photo(pid, glare, blur, crop):
    return {"id": pid, "px_w": 3024, "px_h": 4032, "glare": glare, "blur": blur, "crop": crop}

PRAE = {"id": "u01", "name_th": "น้องแพร", "name_en": "Prae", "age": 24, "city_th": "เชียงใหม่"}
PEOPLE = [PRAE,
          {"id": "u02", "name_th": "พี่โอ๊ต", "name_en": "Oat", "age": 31, "city_th": "กรุงเทพฯ"},
          {"id": "u03", "name_th": "คุณแม่จอย", "name_en": "Joy", "age": 42, "city_th": "ขอนแก่น"},
          {"id": "u04", "name_th": "ต้นกล้า", "name_en": "Tonkla", "age": 19, "city_th": "ภูเก็ต"}]
PHOTOS = [_photo("p01", 0.10, 0.08, 0.10), _photo("p02", 0.20, 0.15, 0.12),
          _photo("p03", 0.15, 0.30, 0.20), _photo("p04", 0.62, 0.48, 0.55), _photo("p05", 0.05, 0.05, 0.05)]

TEA_RAW = {"stain": "thai_tea", "fabric": "cotton", "color": "white", "age_hours": 2, "size_cm": 4, "confidence": 0.91}
CURRY_RAW = {"stain": "curry", "fabric": "polyester", "color": "colored", "age_hours": 3, "size_cm": 4, "confidence": 0.84}
INK_SILK_RAW = {"stain": "ink", "fabric": "silk", "color": "colored", "age_hours": 30, "size_cm": 2, "confidence": 0.88}
BLOOD_RAW = {"stain": "blood", "fabric": "cotton", "color": "white", "age_hours": 0.5, "size_cm": 3, "confidence": 0.80}
MUD_RAW = {"stain": "mud", "fabric": "denim", "color": "colored", "age_hours": 4, "size_cm": 12, "confidence": 0.93}
LOW_RAW = {"stain": "coffee", "fabric": "cotton", "color": "white", "age_hours": 1, "size_cm": 3, "confidence": 0.41}

TEA = parse_stain(TEA_RAW)
CURRY = parse_stain(CURRY_RAW)
INK_SILK = parse_stain(INK_SILK_RAW)
BLOOD = parse_stain(BLOOD_RAW)
MUD = parse_stain(MUD_RAW)
LOW = parse_stain(LOW_RAW)

PRAE_KIT = ["dish_soap", "baking_soda", "white_vinegar", "oxygen_bleach"]
SHIRT_LABEL = ["wash_40", "non_chlorine_bleach", "tumble_low", "iron_med"]
SILK_LABEL = ["hand_wash", "no_bleach", "no_tumble", "iron_low", "dry_clean"]

DIARY = [
    {"date": "2026-12-10", "item_th": "เสื้อนักศึกษาขาว", "stain": "thai_tea", "result": "removed", "value_baht": 290},
    {"date": "2026-12-03", "item_th": "กางเกงยีนส์", "stain": "mud", "result": "removed", "value_baht": 890},
    {"date": "2026-11-28", "item_th": "เสื้อยืดลายแมว", "stain": "curry", "result": "faded", "value_baht": 250},
    {"date": "2026-11-20", "item_th": "ผ้าปูที่นอน", "stain": "blood", "result": "removed", "value_baht": 590},
    {"date": "2026-11-12", "item_th": "เสื้อเชิ้ตทำงาน", "stain": "ink", "result": "stuck", "value_baht": 450},
]
