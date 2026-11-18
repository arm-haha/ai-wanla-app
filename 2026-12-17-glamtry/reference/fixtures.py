"""Fictional demo data only."""
from glamtry import *
PEOPLE = [
    {"id": "u01", "name_th": "น้องเฟิร์น", "name_en": "Fern", "age": 24, "city_th": "กรุงเทพฯ (อารีย์)", "skill": 1},
    {"id": "u02", "name_th": "พี่แพร", "name_en": "Prae", "age": 29, "city_th": "ขอนแก่น", "skill": 2},
    {"id": "u03", "name_th": "น้ำหวาน", "name_en": "Namwan", "age": 17, "city_th": "เชียงใหม่", "skill": 1},
    {"id": "u04", "name_th": "เจ๊หน่อย", "name_en": "Jae Noi", "age": 45, "city_th": "หาดใหญ่", "skill": 3},
]
PHOTOS = [
    {"id": "p01", "light": 0.9, "blur": 0.05, "tilt": 0.1, "filter_on": False},
    {"id": "p02", "light": 0.5, "blur": 0.2, "tilt": 0.2, "filter_on": True},
    {"id": "p03", "light": 0.3, "blur": 0.6, "tilt": 0.5, "filter_on": False},
]
TODAY = "2026-12-17"
SHADE = shade_match((214, 170, 140), 94)
LOOKS6 = six_looks(SHADE["depth"], SHADE["undertone"])
SPEC = look_spec("korean_glass", SHADE["depth"], SHADE["undertone"])
TUT = tutorial("korean_glass", SHADE["undertone"], PEOPLE[0]["skill"])
KIT = budget_kit("korean_glass", "budget", owned=("concealer",))
PLAN = occasion_plan("wedding_guest", "2026-12-27", TODAY)
PATCH = patch_test(["cushion", "lip_tint", "eyeshadow"])
CONSENT = consent_check(24, True)
REEL = reel_plan(SPEC, 20)
DIARY = [
    {"date": "2026-12-17", "kind": "try", "look": "korean_glass"},
    {"date": "2026-12-17", "kind": "try", "look": "y2k"},
    {"date": "2026-12-18", "kind": "buy", "item": "cushion", "cost_baht": 259},
    {"date": "2026-12-18", "kind": "buy", "item": "lip_tint", "cost_baht": 129},
    {"date": "2026-12-19", "kind": "open", "item": "mascara"},
    {"date": "2026-12-27", "kind": "wear", "look": "korean_glass"},
]
