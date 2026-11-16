"""Fictional demo data only."""
from riperight import *
PEOPLE = [
    {"id": "u01", "name_th": "พี่ต้อม", "name_en": "Tom", "age": 31, "city_th": "กรุงเทพฯ"},
    {"id": "u02", "name_th": "ป้าแดง", "name_en": "Auntie Daeng", "age": 57, "city_th": "ราชบุรี"},
    {"id": "u03", "name_th": "มายด์", "name_en": "Mind", "age": 24, "city_th": "เชียงใหม่"},
    {"id": "u04", "name_th": "ลุงสมพงษ์", "name_en": "Uncle Sompong", "age": 63, "city_th": "จันทบุรี"},
]
PHOTOS = [
    {"id": "p01", "fruit": "avocado", "px_w": 1080, "px_h": 1350, "glare": 0.1, "blur": 0.05, "crop": 0.0},
    {"id": "p02", "fruit": "mango", "px_w": 720, "px_h": 960, "glare": 0.4, "blur": 0.2, "crop": 0.1},
    {"id": "p03", "fruit": "banana", "px_w": 640, "px_h": 640, "glare": 0.6, "blur": 0.5, "crop": 0.4},
]
TODAY = "2026-12-14"
MONTH = 12
AVO = ripeness("avocado", 0.40, 0.05, "firm")           # demo: wait ~2 days
MANGO = ripeness("mango", 0.85, 0.10, "yielding", "strong")
BANANA = ripeness("banana", 0.95, 0.70)
MELON_KNOCK = knock_test("watermelon", 120, 180)
MELON = ripeness("watermelon", 0.60, 0.05, knock=MELON_KNOCK["cue"])
MELON_NOKNOCK = ripeness("watermelon", 0.60, 0.05)
BASKET = [basket_item("อะโวคาโด", AVO), basket_item("มะม่วง", MANGO), basket_item("แตงโม", MELON)]
DIARY = [
    {"date": "2026-11-02", "fruit": "mango", "predicted": "perfect", "result": "just_right", "paid_baht": 120},
    {"date": "2026-11-20", "fruit": "avocado", "predicted": "almost", "result": "too_raw", "paid_baht": 95},
    {"date": "2026-12-06", "fruit": "watermelon", "predicted": "perfect", "result": "just_right", "paid_baht": 80},
    {"date": "2026-12-14", "fruit": "avocado", "predicted": "almost", "result": "just_right", "paid_baht": 110},
]
