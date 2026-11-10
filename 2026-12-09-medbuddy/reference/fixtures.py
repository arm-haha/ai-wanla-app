"""Demo fixture: พี่นนท์ builds a med schedule for คุณวันดี from three fictional envelopes. Fictional only."""
from medbuddy import parse_label

TODAY = "2026-12-09"

def _photo(pid, glare, blur, crop):
    return {"id": pid, "px_w": 3024, "px_h": 4032, "glare": glare, "blur": blur, "crop": crop}

WANDEE_PHOTOS = [
    _photo("p01", 0.10, 0.10, 0.10),
    _photo("p02", 0.12, 0.08, 0.14),
    _photo("p03", 0.16, 0.12, 0.10),
]
PHOTOS = WANDEE_PHOTOS + [_photo("p04", 0.62, 0.48, 0.55)]

PRIL_RAW = {"name": "FictoPril", "strength_th": "5 mg", "dose_th": "วันละ 1 เม็ด เช้า",
            "slots": ["morning"], "food": "after_food", "qty": 14, "daily_units": 1, "confidence": 0.92}
MET_RAW = {"name": "FictoMet", "strength_th": "500 mg", "dose_th": "เช้า 1 เม็ด เย็น 1 เม็ด",
           "slots": ["morning", "evening"], "food": "after_food", "qty": 20, "daily_units": 2, "confidence": 0.90}
PAIN_RAW = {"name": "FictoPain", "strength_th": "500 mg", "dose_th": "ทานเมื่อปวด ไม่เกิน 3 ครั้ง/วัน",
            "slots": ["as_needed"], "food": "any", "qty": 8, "daily_units": None, "prn_max_per_day": 3, "confidence": 0.88}
LOW_RAW = dict(PRIL_RAW, confidence=0.41)

PRIL = parse_label(PRIL_RAW)
MET = parse_label(MET_RAW)
PAIN = parse_label(PAIN_RAW)
LOW = parse_label(LOW_RAW)
MEDS = [PRIL, MET, PAIN]

WANDEE = {
    "id": "p01", "name_th": "คุณวันดี", "name_en": "Wandee", "age": 68, "city_th": "นนทบุรี",
    "clinic_th": "Ficto Clinic", "doctor_th": "นพ.วันชัย (สมมติ)", "visit_date": "2026-12-16",
}
NON = {
    "id": "u01", "name_th": "พี่นนท์", "name_en": "Non", "age": 36, "city_th": "นนทบุรี",
    "relation_th": "ลูก", "patient": WANDEE,
}
