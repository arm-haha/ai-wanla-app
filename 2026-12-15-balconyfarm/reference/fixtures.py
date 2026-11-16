"""Fictional demo data only."""
from balconyfarm import *
PEOPLE = [
    {"id": "u01", "name_th": "พี่เก่ง", "name_en": "Keng", "age": 29, "city_th": "กรุงเทพฯ (บางนา)"},
    {"id": "u02", "name_th": "น้องปลา", "name_en": "Pla", "age": 25, "city_th": "นนทบุรี"},
    {"id": "u03", "name_th": "คุณยายบุญ", "name_en": "Grandma Boon", "age": 68, "city_th": "ขอนแก่น"},
    {"id": "u04", "name_th": "เจ๊หมวย", "name_en": "Jae Muay", "age": 45, "city_th": "หาดใหญ่"},
]
PHOTOS = [
    {"id": "p01", "px_w": 1080, "px_h": 1350, "glare": 0.1, "blur": 0.05, "crop": 0.0},
    {"id": "p02", "px_w": 720, "px_h": 960, "glare": 0.4, "blur": 0.2, "crop": 0.1},
    {"id": "p03", "px_w": 640, "px_h": 640, "glare": 0.6, "blur": 0.5, "crop": 0.4},
]
TODAY = "2026-12-15"
MONTH = 12
SUN = sun_estimate("se", 0.3, 1.0, 12)
PICKS = plant_picks(SUN, MONTH)
GARDEN = [f["plant"] for f in PICKS["picks"]]
LAYOUT = layout(2.4, 1.2, GARDEN)
DIARY = [
    {"date": "2026-12-11", "plant": "horapha", "action": "water"},
    {"date": "2026-12-13", "plant": "horapha", "action": "water"},
    {"date": "2026-12-14", "plant": "spring_onion", "action": "harvest", "grams": 80},
    {"date": "2026-12-15", "plant": "mint", "action": "harvest", "grams": 45},
    {"date": "2026-12-15", "plant": "lettuce", "action": "photo"},
]
