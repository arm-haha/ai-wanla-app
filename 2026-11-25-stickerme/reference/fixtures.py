"""Demo fixture: น้องเจน (Jane) wants a chibi LINE sticker set from one selfie. Fictional only — no real faces."""
TODAY = "2026-11-25"

def _selfie(sid, glare, blur, crop, face_conf, face_frac, extras=None):
    d = {"id": sid, "px_w": 1170, "px_h": 2532, "glare": glare, "blur": blur, "crop": crop,
         "face_conf": face_conf, "face_frac": face_frac, "detections": [
             {"key": "face", "value": True, "confidence": face_conf},
             {"key": "face_frac", "value": face_frac, "confidence": face_conf},
         ]}
    if extras:
        d["detections"].extend(extras)
    return d

JANE = {
    "id": "u01", "name_th": "น้องเจน", "name_en": "Jane", "age": 24, "city_th": "กรุงเทพฯ",
    "goal_th": "เซลฟี่เดียวอยากได้สติกเกอร์ LINE หน้าตัวเองทั้งเซ็ต สไตล์จิ๋วหัวโต มีข้อความไทย",
    "style": "chibi",
}
# score = 91: 0.30*0.08 + 0.35*0.08 + 0.20*0.05 + 0.15*0.20 = 0.092
JANE_SELFIE = _selfie("s01", 0.08, 0.08, 0.05, 0.95, 0.80)

BECK = {
    "id": "u02", "name_th": "พี่เบค", "name_en": "Beck", "age": 31, "city_th": "เชียงใหม่",
    "goal_th": "อยากได้ชุด 8 ใบสไตล์ป๊อป สำหรับแชทงาน",
    "style": "pop",
}
BECK_SELFIE = _selfie("s02", 0.12, 0.10, 0.10, 0.90, 0.62)

MIN = {
    "id": "u03", "name_th": "น้องมิน", "name_en": "Min", "age": 16, "city_th": "ขอนแก่น",
    "goal_th": "อยากทำสติกเกอร์แต่ต้องให้ผู้ปกครองยินยอมก่อน",
    "style": "comic",
}
MIN_SELFIE = _selfie("s03", 0.10, 0.10, 0.10, 0.88, 0.70)

BAD_SHOT = _selfie("s04", 0.68, 0.52, 0.50, 0.72, 0.18)
EMPTY_SHOT = {"id": "s05", "px_w": 1170, "px_h": 2532, "glare": 0.20, "blur": 0.15, "crop": 0.10,
              "face_conf": 0.20, "face_frac": 0.05, "detections": []}
LOWCONF_SHOT = _selfie("s06", 0.10, 0.10, 0.10, 0.41, 0.60)

JANE_CONSENT = {"own_face": True, "other_person": False, "apparent_minor": False,
                "guardian_consent": False, "celebrity_likeness": False}
MIN_CONSENT_NO = {"own_face": True, "other_person": False, "apparent_minor": True,
                  "guardian_consent": False, "celebrity_likeness": False}
MIN_CONSENT_YES = {"own_face": True, "other_person": False, "apparent_minor": True,
                   "guardian_consent": True, "celebrity_likeness": False}
OTHER_CONSENT = {"own_face": False, "other_person": True, "apparent_minor": False,
                 "guardian_consent": False, "celebrity_likeness": False}

PEOPLE = [JANE, BECK, MIN]
