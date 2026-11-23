"""Fictional demo data only — no real people, no brand names."""
from brickbuddy import *

TODAY = "2026-12-21"
PEOPLE = [
    {"id": "u01", "name_th": "น้องภูมิ", "name_en": "Phum", "age": 7, "city_th": "นนทบุรี", "role_th": "นักสร้างตัวจิ๋ว (แม่เปิดกล้องให้)"},
    {"id": "u02", "name_th": "คุณแม่ฝน", "name_en": "Fon", "age": 36, "city_th": "นนทบุรี", "role_th": "ผู้ปกครอง ถ่ายรูปกอง"},
    {"id": "u03", "name_th": "น้องข้าวปุ้น", "name_en": "Khaopun", "age": 4, "city_th": "ลำปาง", "role_th": "ต่อกับพี่สาว"},
    {"id": "u04", "name_th": "พี่ต้า", "name_en": "Ta", "age": 29, "city_th": "กรุงเทพฯ", "role_th": "สายของแต่งโต๊ะทำงาน"},
]
PHOTOS = [
    {"id": "p01", "light": 0.9, "blur": 0.05, "spread": 0.85, "overlap": 0.1},
    {"id": "p02", "light": 0.55, "blur": 0.2, "spread": 0.5, "overlap": 0.3},
    {"id": "p03", "light": 0.4, "blur": 0.5, "spread": 0.3, "overlap": 0.6},
]
# Phum's pile: what the vision model returned (positions = where clusters of that piece sit in the photo, 0..1)
PILE = [
    {"part": "brick_2x4", "color": "red", "count": 3, "confidence": 0.95, "positions": [[0.12, 0.2], [0.55, 0.7]]},
    {"part": "brick_2x4", "color": "blue", "count": 3, "confidence": 0.93, "positions": [[0.8, 0.15]]},
    {"part": "brick_2x2", "color": "yellow", "count": 6, "confidence": 0.92, "positions": [[0.3, 0.4], [0.62, 0.3]]},
    {"part": "brick_2x2", "color": "white", "count": 5, "confidence": 0.9, "positions": [[0.45, 0.85]]},
    {"part": "brick_1x2", "color": "blue", "count": 8, "confidence": 0.9, "positions": [[0.2, 0.6], [0.9, 0.5]]},
    {"part": "brick_1x2", "color": "red", "count": 4, "confidence": 0.88, "positions": [[0.7, 0.9]]},
    {"part": "brick_1x1", "color": "yellow", "count": 6, "confidence": 0.85, "positions": [[0.35, 0.1]]},
    {"part": "plate_2x4", "color": "green", "count": 3, "confidence": 0.9, "positions": [[0.05, 0.9]]},
    {"part": "plate_2x2", "color": "green", "count": 4, "confidence": 0.86, "positions": [[0.5, 0.5]]},
    {"part": "plate_1x2", "color": "black", "count": 4, "confidence": 0.8, "positions": [[0.95, 0.95]]},
    {"part": "slope_2x2", "color": "red", "count": 4, "confidence": 0.9, "positions": [[0.25, 0.3]]},
    {"part": "wheel", "color": "black", "count": 4, "confidence": 0.97, "positions": [[0.75, 0.6]]},
    {"part": "eye_1x1", "color": "white", "count": 2, "confidence": 0.8, "positions": [[0.6, 0.05]]},
    {"part": "round_1x1", "color": "orange", "count": 3, "confidence": 0.75, "positions": [[0.15, 0.45]]},
    {"part": "tile_1x2", "color": "gray", "count": 2, "confidence": 0.7, "positions": [[0.85, 0.8]]},
    {"part": "window", "color": "trans_clear", "count": 1, "confidence": 0.45, "positions": [[0.4, 0.6]]},  # unsure → ignored,
    {"part": "brick_1x1", "color": "green", "count": 2, "confidence": 0.4, "positions": [[0.98, 0.02]]},  # low confidence → ignored
]
INV = inventory(PILE)
IDEAS = suggest_builds(INV, PEOPLE[0]["age"], 30)
COLORS_DUCK = assign_colors("duck", PILE)
STEPS_DUCK = build_steps("duck", COLORS_DUCK)
DIARY = [
    {"date": "2026-12-19", "kind": "build", "build": "snowman", "pieces": 10, "stars": 3, "badges": []},
    {"date": "2026-12-20", "kind": "challenge", "build": "xmas_tree", "pieces": 16, "stars": 4, "badges": ["challenge_done"]},
    {"date": "2026-12-20", "kind": "build", "build": "xmas_tree", "pieces": 16, "stars": 4, "badges": ["challenge_done", "symmetry_star"]},
    {"date": "2026-12-21", "kind": "build", "build": "duck", "pieces": 7, "stars": 3, "badges": []},
    {"date": "2026-12-21", "kind": "sort"},
]
