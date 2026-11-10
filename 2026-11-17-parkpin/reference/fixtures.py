"""Demo fixture: พี่เจ (Jay) pins a spot at FictoMall Bangna B2, green zone, pillar C-14. Fictional only."""
TODAY = "2026-11-17"
NOW = "2026-11-17T16:50:00"
PARKED = "2026-11-17T14:20:00"

def _p(pid, mall, floor, zone, color, pillar, glare, blur, tilt, fill, conf, has_plate=False):
    return {"id": pid, "px_w": 3024, "px_h": 4032, "mall_id": mall, "floor": floor, "zone": zone,
            "color": color, "pillar": pillar, "glare": glare, "blur": blur, "tilt": tilt,
            "sign_fill": fill, "confidence": conf, "has_plate": has_plate}

JAY = {"id": "u01", "name_th": "พี่เจ", "name_en": "Jay", "age": 41, "city_th": "กรุงเทพฯ",
       "goal_th": "จำที่จอด FictoMall บางนา แล้วส่งให้ภรรยา"}
JAY_PHOTO = _p("p01", "fictomall_bangna", "B2", "C", "green", "C-14", 0.18, 0.10, 0.08, 0.88, 0.94)
JAY_HINT = "ใกล้ประตู 3 รถสีเทาจอดหัวออก"
JAY_NOTE = "ชั้น B2 เสา C-14 นะ เดี๋ยวไปหานะ"

PEOPLE = [
    JAY,
    {"id": "u02", "name_th": "พี่ฟ้า", "name_en": "Fah", "age": 33, "city_th": "เชียงใหม่",
     "goal_th": "จอด FictoWorld แล้วลืมชั้น"},
    {"id": "u03", "name_th": "น้องกิ๊ฟ", "name_en": "Gift", "age": 27, "city_th": "กรุงเทพฯ",
     "goal_th": "จอด FictoPlex สิริ ไปดูหนัง"},
    {"id": "u04", "name_th": "ลุงสม", "name_en": "Som", "age": 60, "city_th": "สมุทรปราการ",
     "goal_th": "จอด FictoPark สนามบิน รับลูก"},
    {"id": "u05", "name_th": "พี่นุช", "name_en": "Nuch", "age": 45, "city_th": "กรุงเทพฯ",
     "goal_th": "แชร์ที่จอดให้ลูกไปเอารถ"},
]

PHOTOS = [
    JAY_PHOTO,
    _p("p02", "fictoworld_chiangmai", "3F", "A", "blue", "A-02", 0.16, 0.12, 0.10, 0.86, 0.91),
    _p("p03", "fictoplex_siri", "B1", "D", "yellow", "D-09", 0.20, 0.10, 0.12, 0.84, 0.90),
    _p("p04", "fictopark_airport", "rooftop", "E", "orange", "E-21", 0.25, 0.15, 0.10, 0.80, 0.88),
    _p("p05", "fictomall_bangna", "B1", "B", "red", "B-03", 0.15, 0.10, 0.08, 0.90, 0.93),
    _p("p06", "fictoplex_siri", "G", "A", "white", "A-01", 0.14, 0.08, 0.06, 0.92, 0.95),
    _p("p07", "fictomall_bangna", "B2", "C", "green", "C-14", 0.62, 0.50, 0.45, 0.30, 0.40),
    _p("p08", "fictomall_bangna", "B2", "C", "green", "C-14", 0.18, 0.10, 0.08, 0.88, 0.94, True),
]

HISTORY = [
    ("pin02", "u01", _p("p09", "fictoplex_siri", "B1", "D", "yellow", "D-02", 0.1, 0.1, 0.1, 0.9, 0.9), "2026-11-01T13:00:00", "ใกล้ลิฟต์โรงหนัง"),
    ("pin01", "u01", JAY_PHOTO, PARKED, JAY_HINT),
]
