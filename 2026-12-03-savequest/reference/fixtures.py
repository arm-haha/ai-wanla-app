"""Demo fixture: น้องมิ้น (Mint) grows a Japan-trip jar to 42%. Fictional only."""
from datetime import date, timedelta
from savequest import complete_challenge

TODAY = "2026-12-03"

def _photo(pid, glare, blur, crop, goal_id="japan_trip"):
    return {"id": pid, "px_w": 3024, "px_h": 4032, "glare": glare, "blur": blur, "crop": crop, "goal_id": goal_id}

MINT_PHOTO = _photo("p01", 0.10, 0.10, 0.10, "japan_trip")
MINT = {
    "id": "u01", "name_th": "น้องมิ้น", "name_en": "Mint", "age": 27, "city_th": "กรุงเทพฯ",
    "goal_id": "japan_trip", "goal_th": "เที่ยวญี่ปุ่น", "goal_thb": 45000, "saved_thb": 18900,
    "start": "2026-03-03", "deadline": "2026-12-03", "week": 18, "base_thb": 100,
    "seed": "u01-2026", "photo": MINT_PHOTO,
}

BEE_PHOTO = _photo("p02", 0.18, 0.12, 0.16, "emergency")
BEE = {
    "id": "u02", "name_th": "พี่บี", "name_en": "Bee", "age": 32, "city_th": "เชียงใหม่",
    "goal_id": "emergency", "goal_th": "กองฉุกเฉิน 3 เดือน", "goal_thb": 30000, "saved_thb": 22500,
    "start": "2026-06-01", "deadline": "2026-12-31", "week": 26, "base_thb": 50,
    "seed": "u02-2026", "photo": BEE_PHOTO,
}

ARM_PHOTO = _photo("p03", 0.20, 0.15, 0.12, "gadget")
ARM = {
    "id": "u03", "name_th": "น้องอาร์ม", "name_en": "Arm", "age": 23, "city_th": "ขอนแก่น",
    "goal_id": "gadget", "goal_th": "Gadgets ที่ตั้งใจซื้อ", "goal_thb": 15000, "saved_thb": 12000,
    "start": "2026-09-01", "deadline": "2026-12-20", "week": 14, "base_thb": 100,
    "seed": "u03-2026", "photo": ARM_PHOTO,
}

PEOPLE = [MINT, BEE, ARM]

# 12-day streak ending today
MINT_DATES = [(date.fromisoformat(TODAY) - timedelta(days=i)).isoformat() for i in range(11, -1, -1)]
# Bee missed yesterday, used a freeze
BEE_DATES = [(date.fromisoformat(TODAY) - timedelta(days=i)).isoformat() for i in range(6, -1, -1) if i != 1]
BEE_FROZEN = [(date.fromisoformat(TODAY) - timedelta(days=1)).isoformat()]

PHOTOS = [
    MINT_PHOTO,
    BEE_PHOTO,
    ARM_PHOTO,
    _photo("p04", 0.62, 0.48, 0.55, "concert"),  # poor quality
    _photo("p05", 0.15, 0.10, 0.10, "tuition"),
]

MINT_CHALLENGE = complete_challenge("skip_cafe", TODAY)
MINT_TEAM = [
    {"name_th": "น้องมิ้น", "amount_thb": 18900},
    {"name_th": "พี่บี", "amount_thb": 3600},
    {"name_th": "น้องอาร์ม", "amount_thb": 1500},
]
