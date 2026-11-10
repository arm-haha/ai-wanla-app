"""Demo fixture: น้องเกล (Gale) tries thin metal round frames on an oval face before buying. Fictional only."""
TODAY = "2026-11-12"

def _p(pid, glare, blur, tilt, fill, eyes, undertone, conf, pd, measures):
    return {"id": pid, "px_w": 3024, "px_h": 4032, "glare": glare, "blur": blur, "tilt": tilt,
            "face_fill": fill, "eyes_visible": eyes, "undertone": undertone,
            "face_confidence": conf, "pd_mm": pd, "measures": measures}

def _m(length, forehead, cheek, jaw):
    return {"length_mm": length, "forehead_mm": forehead, "cheek_mm": cheek, "jaw_mm": jaw}

GALE = {"id": "u01", "name_th": "น้องเกล", "name_en": "Gale", "age": 26, "city_th": "กรุงเทพฯ",
        "goal_th": "อยากลองแว่นกลมบางโลหะก่อนซื้อ ทำงานออฟฟิศ", "region": "bkk", "lifestyle": "office"}
GALE_PHOTO = _p("p01", 0.16, 0.10, 0.08, 0.82, 0.94, "cool", 0.93, 62, _m(185, 132, 136, 125))

PEOPLE = [
    GALE,
    {"id": "u02", "name_th": "พี่บอม", "name_en": "Bom", "age": 34, "city_th": "ขอนแก่น",
     "goal_th": "หน้ากลม อยากได้กรอบเหลี่ยมไปทำงาน", "region": "province", "lifestyle": "office"},
    {"id": "u03", "name_th": "พี่แนน", "name_en": "Nan", "age": 41, "city_th": "พัทยา",
     "goal_th": "หน้าเหลี่ยม อยากได้ทรงกลมไปเที่ยว", "region": "tourist", "lifestyle": "outdoor"},
    {"id": "u04", "name_th": "น้องมายด์", "name_en": "Mind", "age": 23, "city_th": "เชียงใหม่",
     "goal_th": "หน้าหัวใจ อยากได้แคทอาย", "region": "province", "lifestyle": "fashion"},
    {"id": "u05", "name_th": "ลุงสมศักดิ์", "name_en": "Somsak", "age": 58, "city_th": "กรุงเทพฯ",
     "goal_th": "หน้ายาว สนใจเลนส์โปรเกรสซีฟ ต้องให้ร้านวัด", "region": "bkk", "lifestyle": "casual"},
]

PHOTOS = [
    GALE_PHOTO,
    _p("p02", 0.18, 0.12, 0.10, 0.80, 0.90, "warm", 0.91, 64, _m(160, 134, 136, 132)),  # round Bom
    _p("p03", 0.20, 0.10, 0.12, 0.78, 0.88, "warm", 0.90, 66, _m(168, 138, 140, 138)),  # square Nan
    _p("p04", 0.15, 0.10, 0.08, 0.85, 0.92, "cool", 0.94, 60, _m(180, 140, 138, 120)),  # heart Mind
    _p("p05", 0.16, 0.11, 0.09, 0.80, 0.90, "neutral", 0.89, 63, _m(200, 130, 130, 128)),  # oblong
    _p("p06", 0.17, 0.10, 0.08, 0.81, 0.91, "cool", 0.92, 61, _m(180, 124, 140, 124)),  # diamond
    _p("p07", 0.62, 0.45, 0.40, 0.40, 0.50, "neutral", 0.55, 62, _m(185, 132, 136, 125)),  # bad quality + low conf
    _p("p08", 0.14, 0.08, 0.06, 0.86, 0.95, "cool", 0.96, 50, _m(185, 132, 136, 125)),  # odd PD
]

GALE_FRAME = "f01"
GALE_LIFE = "office"
GALE_QUOTE = 3200
GALE_NOTE = "ชอบกรอบกลมบาง สีทอง ทำงานหน้าจอทั้งวัน ขอให้ร้านวัด PD และค่าสายตาใหม่ก่อนตัดเลนส์"
GALE_GRID = ["f01", "f02", "f03", "f07", "f12", "f10"]

DIARY = [
    ("e01", "u01", "2026-03-12", "f05", "ร้านแว่น FictoOptic สยาม", 0, "tried"),
    ("e02", "u01", "2025-08-01", "f07", "ร้านแว่น FictoOptic สยาม", 5200, "bought"),
    ("e03", "u01", "2026-11-12", "f01", "", 0, "wishlist"),
]
