"""Fictional demo data only."""
from cakedream import *
PEOPLE = [
    {"id": "u01", "name_th": "แม่ปุ๊ก", "name_en": "Mae Puk", "age": 34, "city_th": "นนทบุรี"},
    {"id": "u02", "name_th": "พี่แนน", "name_en": "Nan", "age": 27, "city_th": "กรุงเทพฯ"},
    {"id": "u03", "name_th": "ลุงชัย", "name_en": "Uncle Chai", "age": 58, "city_th": "เชียงใหม่"},
    {"id": "u04", "name_th": "ฟ้า", "name_en": "Fah", "age": 22, "city_th": "ขอนแก่น"},
]
PHOTOS = [
    {"id": "p01", "px_w": 1080, "px_h": 1350, "glare": 0.1, "blur": 0.05, "crop": 0.0},
    {"id": "p02", "px_w": 720, "px_h": 960, "glare": 0.4, "blur": 0.2, "crop": 0.1},
    {"id": "p03", "px_w": 640, "px_h": 640, "glare": 0.6, "blur": 0.5, "crop": 0.4},
]
TODAY = "2026-12-11"
PARTY = "2026-12-19"
DINO = design_spec("dinosaur", "vanilla_chiffon", 2, "HBD น้องภูมิ 5 ขวบ")
GUESTS = serving_calc(8, 10)
DIARY = [
    {"date": "2026-06-02", "theme": "korean_minimal", "paid_baht": 650, "stars": 4},
    {"date": "2026-09-14", "theme": "football", "paid_baht": 1100, "stars": 5},
    {"date": "2026-12-19", "theme": "dinosaur", "paid_baht": 1250, "stars": 5},
]
