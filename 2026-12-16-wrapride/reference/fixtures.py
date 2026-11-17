"""Fictional demo data only."""
from wrapride import *
PEOPLE = [
    {"id": "u01", "name_th": "พี่ต้น", "name_en": "Ton", "age": 31, "city_th": "กรุงเทพฯ (ลาดพร้าว)", "vehicle": "eco_car"},
    {"id": "u02", "name_th": "น้องมายด์", "name_en": "Mind", "age": 22, "city_th": "เชียงใหม่", "vehicle": "scooter"},
    {"id": "u03", "name_th": "ช่างบอย", "name_en": "Boy", "age": 38, "city_th": "ชลบุรี", "vehicle": "pickup"},
    {"id": "u04", "name_th": "เจ๊นก", "name_en": "Jae Nok", "age": 47, "city_th": "นครราชสีมา", "vehicle": "suv"},
]
PHOTOS = [
    {"id": "p01", "px_w": 1080, "px_h": 1350, "glare": 0.1, "blur": 0.05, "crop": 0.0},
    {"id": "p02", "px_w": 720, "px_h": 960, "glare": 0.4, "blur": 0.2, "crop": 0.1},
    {"id": "p03", "px_w": 640, "px_h": 640, "glare": 0.6, "blur": 0.5, "crop": 0.4},
]
TODAY = "2026-12-16"
SPEC = wrap_spec("eco_car", "mint_green", "matte", "two_tone", "deep_black", original_family="white")
RIMS = rim_sticker_spec("eco_car", "five_spoke", "black", ["side_stripe"])
PRICE = price_check("eco_car", "wrap", "matte", "two_tone", quote_baht=24000)
RIM_PRICE = price_check("eco_car", "rims")
BRIEF = shop_brief(PEOPLE[0], SPEC, RIMS, PRICE, "อยากได้ก่อนปีใหม่")
LEGAL = legal_check(SPEC)
REEL = reel_plan(SPEC, 20)
DIARY = [
    {"date": "2026-12-01", "kind": "photo"},
    {"date": "2026-12-10", "kind": "wrap", "cost_baht": 24000},
    {"date": "2026-12-10", "kind": "rim", "cost_baht": 14500},
    {"date": "2026-12-14", "kind": "wash", "cost_baht": 150},
]
