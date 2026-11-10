"""Demo fixture: น้องมายด์ (Mind) turns one selfie into a 90s yearbook look. Fictional only."""
TODAY = "2026-11-18"

def _photo(pid, glare, blur, crop, dets):
    return {"id": pid, "px_w": 3024, "px_h": 4032, "glare": glare, "blur": blur, "crop": crop, "detections": dets}

def _d(label, conf, own=True, celeb=False, age=22):
    return {"label": label, "confidence": conf, "own_face": own, "celebrity_likely": celeb, "age_apparent": age}

MIND_TRAITS = {
    "warm_tone": 0.25, "high_volume_hair": 0.20, "neon_pref": 0.15, "soft_glam": 0.35,
    "cool_tone": 0.80, "straight_hair": 0.85, "film_pref": 0.90, "casual": 0.88,
    "flash": 0.40, "glossy": 0.30, "thin_brows": 0.45, "metallic": 0.20,
}
MIND_PHOTO = _photo("p01", 0.15, 0.10, 0.12, [_d("mind", 0.96, True, False, 22)])
MIND = {
    "id": "u01", "name_th": "น้องมายด์", "name_en": "Mind", "nickname_th": "มายด์", "age": 22,
    "city_th": "กรุงเทพฯ", "goal_th": "อยากได้รูปรุ่นยุค 90s สำหรับรีลงานรับปริญญา",
    "own_photo": True, "consent_confirmed": True, "guardian_ok": False, "all_consented": True,
    "celebrity_likely": False, "consented": True, "traits": MIND_TRAITS, "photo": MIND_PHOTO,
    "role": "most_likely_friend",
}

FERN_TRAITS = {
    "warm_tone": 0.70, "high_volume_hair": 0.80, "neon_pref": 0.75, "soft_glam": 0.65,
    "cool_tone": 0.30, "straight_hair": 0.25, "film_pref": 0.40, "casual": 0.35,
    "flash": 0.55, "glossy": 0.50, "thin_brows": 0.30, "metallic": 0.45,
}
FERN_PHOTO = _photo("p02", 0.20, 0.15, 0.18, [_d("fern", 0.93, True, False, 23)])
FERN = {
    "id": "u02", "name_th": "พี่เฟิร์น", "name_en": "Fern", "nickname_th": "เฟิร์น", "age": 23,
    "city_th": "เชียงใหม่", "goal_th": "อยากลองลุค 80s นีออนสำหรับปาร์ตี้ธีมย้อนยุค",
    "own_photo": True, "consent_confirmed": True, "guardian_ok": False, "all_consented": True,
    "celebrity_likely": False, "consented": True, "traits": FERN_TRAITS, "photo": FERN_PHOTO,
    "role": "mc",
}

TANG_TRAITS = {
    "warm_tone": 0.35, "high_volume_hair": 0.30, "neon_pref": 0.40, "soft_glam": 0.25,
    "cool_tone": 0.55, "straight_hair": 0.50, "film_pref": 0.45, "casual": 0.60,
    "flash": 0.85, "glossy": 0.80, "thin_brows": 0.78, "metallic": 0.82,
}
TANG_PHOTO = _photo("p03", 0.25, 0.12, 0.20, [_d("tang", 0.91, True, False, 21)])
TANG = {
    "id": "u03", "name_th": "น้องตัง", "name_en": "Tang", "nickname_th": "ตัง", "age": 21,
    "city_th": "ขอนแก่น", "goal_th": "อยากได้ลุค Y2K แฟลชตรงไปโพสต์สตอรี่",
    "own_photo": True, "consent_confirmed": True, "guardian_ok": False, "all_consented": True,
    "celebrity_likely": False, "consented": True, "traits": TANG_TRAITS, "photo": TANG_PHOTO,
    "role": "most_likely_travel",
}

GRACE = {
    "id": "u04", "name_th": "พี่เกรซ", "name_en": "Grace", "nickname_th": "เกรซ", "age": 24,
    "city_th": "ภูเก็ต", "goal_th": "อยากได้หน้ารุ่นรวมเพื่อนสำหรับของที่ระลึก",
    "own_photo": True, "consent_confirmed": True, "guardian_ok": False, "all_consented": True,
    "celebrity_likely": False, "consented": True,
    "traits": {
        "warm_tone": 0.40, "high_volume_hair": 0.35, "neon_pref": 0.30, "soft_glam": 0.55,
        "cool_tone": 0.70, "straight_hair": 0.60, "film_pref": 0.75, "casual": 0.65,
        "flash": 0.35, "glossy": 0.40, "thin_brows": 0.50, "metallic": 0.25,
    },
    "photo": _photo("p04", 0.18, 0.10, 0.15, [_d("grace", 0.94, True, False, 24)]),
    "role": "yearbook_club",
}

PRAE = {
    "id": "u05", "name_th": "น้องแพร", "name_en": "Prae", "nickname_th": "แพร", "age": 16,
    "city_th": "นนทบุรี", "goal_th": "อยากลองสไตล์ 90s แต่ต้องให้แม่กดยินยอมก่อน",
    "own_photo": True, "consent_confirmed": True, "guardian_ok": True, "all_consented": True,
    "celebrity_likely": False, "consented": True,
    "traits": {
        "warm_tone": 0.30, "high_volume_hair": 0.40, "neon_pref": 0.25, "soft_glam": 0.45,
        "cool_tone": 0.75, "straight_hair": 0.70, "film_pref": 0.80, "casual": 0.72,
        "flash": 0.50, "glossy": 0.45, "thin_brows": 0.40, "metallic": 0.30,
    },
    "photo": _photo("p05", 0.22, 0.18, 0.16, [_d("prae", 0.90, True, False, 16)]),
    "role": "quiet_star",
}

PEOPLE = [MIND, FERN, TANG, GRACE, PRAE]

PHOTOS = [
    MIND_PHOTO,
    FERN_PHOTO,
    TANG_PHOTO,
    GRACE["photo"],
    PRAE["photo"],
    _photo("p06", 0.62, 0.48, 0.55, [_d("mind-bad", 0.88, True, False, 22)]),  # poor quality
    _photo("p07", 0.15, 0.10, 0.10, []),  # no face
    _photo("p08", 0.20, 0.15, 0.12, [_d("mind", 0.95, True, False, 22), _d("friend", 0.87, False, False, 22)]),  # two faces
    _photo("p09", 0.15, 0.10, 0.10, [_d("star", 0.97, False, True, 30)]),  # celebrity likely
    _photo("p10", 0.15, 0.12, 0.10, [_d("blur-face", 0.41, True, False, 22)]),  # low confidence
]

MIND_PROFILE = {k: MIND[k] for k in ("own_photo", "consent_confirmed", "guardian_ok", "all_consented", "celebrity_likely", "age")}
