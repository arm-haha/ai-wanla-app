"""Demo fixture: พี่เก้า (Kao) turns 6 saved screenshots into a 4-day Chiang Mai trip. Fictional only."""
TODAY = "2026-11-19"

def _shot(sid, glare, blur, crop, dets):
    return {"id": sid, "px_w": 1170, "px_h": 2532, "glare": glare, "blur": blur, "crop": crop, "detections": dets}

def _d(pid, name_th, name_en, area, typ, conf, source="ig", open_h=9, close_h=18, closed=None, ticket=0, note=""):
    return {"id": pid, "name_th": name_th, "name_en": name_en, "area": area, "type": typ, "confidence": conf,
            "source": source, "open_hour": open_h, "close_hour": close_h, "closed_dow": closed or [],
            "ticket_thb": ticket, "note_th": note}

P_BEAN = _d("pl01", "คาเฟ่ FictoBean", "FictoBean Cafe", "nimman", "cafe", 0.94, "ig", 8, 18, note="กาแฟและเค้กในนิมมาน")
P_SOI = _d("pl02", "ร้านข้าวซอย FictoSoi", "FictoSoi Khao Soi", "nimman", "food", 0.91, "tiktok", 10, 21)
P_THAPAE = _d("pl03", "ประตูท่าแพ", "Tha Phae Gate", "old_city", "photo", 0.96, "ig", 0, 24, note="จุดถ่ายรูปยามเช้า")
P_WALK = _d("pl04", "วอล์กกิ้งสตรีท ไนท์บาซาร์", "Walking Street Night Bazaar", "old_city", "market", 0.89, "maps", 17, 23)
P_SUTHEP = _d("pl05", "วัดพระธาตุดอยสุเทพ", "Doi Suthep Temple", "doi_suthep", "temple", 0.97, "maps", 6, 19, ticket=50, note="ชุดสุภาพ")
P_HILL = _d("pl06", "คาเฟ่ FictoHill", "FictoHill Cafe", "mae_rim", "cafe", 0.92, "ig", 9, 17, closed=[1], note="ปิดวันอังคาร")  # Tue=1

KAO_SHOTS = [
    _shot("s01", 0.12, 0.08, 0.10, [P_BEAN]),
    _shot("s02", 0.18, 0.12, 0.15, [P_SOI]),
    _shot("s03", 0.10, 0.10, 0.08, [P_THAPAE]),
    _shot("s04", 0.22, 0.18, 0.20, [P_WALK]),
    _shot("s05", 0.15, 0.10, 0.12, [P_SUTHEP, _d("pl99", "จุดชมวิวไม่ชัด", "Unclear lookout", "doi_suthep", "viewpoint", 0.41, "ig")]),
    _shot("s06", 0.16, 0.11, 0.14, [P_HILL]),
]

KAO = {
    "id": "u01", "name_th": "พี่เก้า", "name_en": "Kao", "age": 29, "city_th": "กรุงเทพฯ",
    "goal_th": "เก็บแคปจอคาเฟ่กับจุดถ่ายรูปในเชียงใหม่ อยากได้ทริป 4 วัน งบ 8,000 สองคน",
    "dest_th": "เชียงใหม่", "start_date": "2026-12-03", "nights": 3, "pax": 2, "budget_thb": 8000,
    "climates": ["cool_morning", "rain_possible"],
}

NINA_PLACES = [
    _d("pl11", "คาเฟ่ FictoSilk", "FictoSilk Cafe", "thonglor", "cafe", 0.90, "ig", 9, 20),
    _d("pl12", "ร้าน FictoBowl", "FictoBowl", "thonglor", "food", 0.88, "maps", 11, 22),
    _d("pl13", "แกลเลอรี FictoFrame", "FictoFrame Gallery", "silom", "activity", 0.86, "web", 10, 18, ticket=150),
]
NINA_SHOTS = [_shot("s11", 0.10, 0.10, 0.10, [NINA_PLACES[0]]),
              _shot("s12", 0.15, 0.12, 0.10, [NINA_PLACES[1], NINA_PLACES[2]])]
NINA = {
    "id": "u02", "name_th": "น้องนิน", "name_en": "Nina", "age": 26, "city_th": "กรุงเทพฯ",
    "goal_th": "สเตย์เคชันในกรุงเทพ 2 วัน จากแคปจอคาเฟ่",
    "dest_th": "กรุงเทพฯ", "start_date": "2026-11-24", "nights": 1, "pax": 1, "budget_thb": 2500,
    "climates": ["hot"],
}

PHU_PLACES = [
    _d("pl21", "ถนนคนเดินเชียงคาน", "Chiang Khan Walking Street", "chiang_khan_walk", "market", 0.93, "ig", 16, 22),
    _d("pl22", "ริมโขง FictoView", "FictoView Mekong", "mekong", "viewpoint", 0.91, "maps", 5, 19),
    _d("pl23", "คาเฟ่ FictoRaft", "FictoRaft Cafe", "mekong", "cafe", 0.87, "tiktok", 8, 17),
    _d("pl24", "จุดชมวิวเนิน FictoHillCK", "FictoHill CK", "hill", "viewpoint", 0.84, "ig", 6, 18),
]
PHU_SHOTS = [_shot("s21", 0.14, 0.10, 0.12, PHU_PLACES)]
PHU = {
    "id": "u03", "name_th": "พี่ภู", "name_en": "Phu", "age": 34, "city_th": "อุดรธานี",
    "goal_th": "ทริปเชียงคาน 3 วันกับครอบครัว",
    "dest_th": "เชียงคาน", "start_date": "2026-12-15", "nights": 2, "pax": 4, "budget_thb": 9000,
    "climates": ["cold", "rain_possible"],
}

MUK_SHOTS = [_shot("s31", 0.66, 0.50, 0.52, [P_BEAN])]  # bad quality, still has a place
EMPTY_SHOT = _shot("s32", 0.20, 0.15, 0.10, [])
CLOSED_TUE_TRIP_START = "2026-12-07"  # Monday, so day 2 is Tuesday — FictoHill closed

PEOPLE = [KAO, NINA, PHU]
KAO_PLACES = [P_BEAN, P_SOI, P_THAPAE, P_WALK, P_SUTHEP, P_HILL]
