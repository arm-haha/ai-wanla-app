"""Demo fixture: น้องมิ้นท์ (Mint) applies for a Bangkok office job. Fictional only."""
NOW = "2026-11-06T08:00:00+07:00"

# Messy dorm selfie under yellow light — before CardReady
MINT_SELFIE = {
    "id": "s01",
    "name_th": "น้องมิ้นท์",
    "name_en": "Mint",
    "age": 24,
    "city_th": "กรุงเทพฯ",
    "purpose_th": "สมัครงานบริษัทในกทม.",
    "doc_type": "job_th",
    "px_w": 3024,
    "px_h": 4032,
    "face": {"cx": 0.52, "cy": 0.42, "h": 0.28, "eyes_open": True, "neutral": True, "front": True},
    "mess": {
        "yellow_cast": 0.65,
        "shadow": 0.55,
        "clutter_bg": 0.80,
        "blur": 0.25,
        "tilt": 0.20,
        "crop_tight": 0.10,
    },
    "target_size": "1_inch",
    "target_bg": "white",
    "soft_light": True,
    "print_copies": 8,
}

# Extra fictional selfies for vault / batch / edge cases
SELFIES = [
    MINT_SELFIE,
    {
        "id": "s02", "name_th": "คุณก้อง", "name_en": "Kong", "age": 31, "city_th": "เชียงใหม่",
        "purpose_th": "ต่อพาสปอร์ต", "doc_type": "passport",
        "px_w": 2400, "px_h": 3200,
        "face": {"cx": 0.50, "cy": 0.40, "h": 0.32, "eyes_open": True, "neutral": True, "front": True},
        "mess": {"yellow_cast": 0.2, "shadow": 0.3, "clutter_bg": 0.4, "blur": 0.1, "tilt": 0.05, "crop_tight": 0.0},
        "target_size": "passport", "target_bg": "white", "soft_light": True, "print_copies": 4,
    },
    {
        "id": "s03", "name_th": "น้องฝ้าย", "name_en": "Fai", "age": 17, "city_th": "ขอนแก่น",
        "purpose_th": "ทำบัตรนักเรียน", "doc_type": "student",
        "px_w": 2000, "px_h": 2000,
        "face": {"cx": 0.48, "cy": 0.45, "h": 0.35, "eyes_open": True, "neutral": False, "front": True},
        "mess": {"yellow_cast": 0.1, "shadow": 0.2, "clutter_bg": 0.5, "blur": 0.4, "tilt": 0.3, "crop_tight": 0.2},
        "target_size": "1_inch", "target_bg": "gov_blue", "soft_light": True, "print_copies": 6,
    },
    {
        "id": "s04", "name_th": "พี่แนน", "name_en": "Nan", "age": 28, "city_th": "ภูเก็ต",
        "purpose_th": "ยื่นวีซ่าท่องเที่ยว", "doc_type": "visa",
        "px_w": 2800, "px_h": 3600,
        "face": {"cx": 0.51, "cy": 0.38, "h": 0.30, "eyes_open": True, "neutral": True, "front": True},
        "mess": {"yellow_cast": 0.0, "shadow": 0.15, "clutter_bg": 0.25, "blur": 0.05, "tilt": 0.0, "crop_tight": 0.0},
        "target_size": "visa", "target_bg": "white", "soft_light": False, "print_copies": 2,
    },
    {
        "id": "s05", "name_th": "ลุงชัย", "name_en": "Chai", "age": 55, "city_th": "นนทบุรี",
        "purpose_th": "ต่อบัตรประชาชน", "doc_type": "national_id",
        "px_w": 1600, "px_h": 2200,
        "face": {"cx": 0.50, "cy": 0.44, "h": 0.33, "eyes_open": True, "neutral": True, "front": True},
        "mess": {"yellow_cast": 0.4, "shadow": 0.6, "clutter_bg": 0.7, "blur": 0.35, "tilt": 0.25, "crop_tight": 0.15},
        "target_size": "1_inch", "target_bg": "white", "soft_light": True, "print_copies": 8,
    },
]

# Checklist signals for Mint after CardReady processing (all pass for job_th)
MINT_SIGNALS = {
    "face_front": True,
    "eyes_open": True,
    "neutral": True,
    "even_light": True,
    "bg_plain": True,
    "formal_wear": True,
}

FAMILY_BATCH = [
    {"id": "m01", "name_th": "น้องมิ้นท์", "relation_th": "ตัวเอง"},
    {"id": "m02", "name_th": "แม่มิ้นท์", "relation_th": "แม่"},
    {"id": "m03", "name_th": "พ่อมิ้นท์", "relation_th": "พ่อ"},
]
