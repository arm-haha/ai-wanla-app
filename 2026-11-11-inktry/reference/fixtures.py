"""Demo fixture: พี่มิ้นต์ (Mint) tries a fine-line olive sprig on her inner forearm before booking. Fictional only."""
TODAY = "2026-11-11"

def _p(pid, glare, blur, tilt, skin, undertone, dets):
    return {"id": pid, "px_w": 3024, "px_h": 4032, "glare": glare, "blur": blur, "tilt": tilt,
            "skin_visible": skin, "undertone": undertone, "detections": dets}

def _d(placement, conf, side="left"):
    return {"placement": placement, "confidence": conf, "side": side}

MINT = {"id": "u01", "name_th": "พี่มิ้นต์", "name_en": "Mint", "age": 28, "city_th": "กรุงเทพฯ",
        "goal_th": "อยากลองช่อใบโอลิฟ์เส้นบางที่แขนด้านในก่อนจองช่าง", "region": "bkk"}
MINT_PHOTO = _p("p01", 0.18, 0.10, 0.08, 0.92, "warm",
                [_d("inner_forearm", 0.94, "left"), _d("wrist", 0.42, "left")])

PEOPLE = [
    MINT,
    {"id": "u02", "name_th": "น้องเพชร", "name_en": "Petch", "age": 22, "city_th": "เชียงใหม่",
     "goal_th": "อยากสักข้อมือแต่ไม่แน่ใจว่าเล็กไปไหม", "region": "province"},
    {"id": "u03", "name_th": "พี่เอก", "name_en": "Ekk", "age": 41, "city_th": "พัทยา",
     "goal_th": "อยากได้มังกรสีที่ต้นแขน ให้อู่สักที่ท่องเที่ยวประเมินราคา", "region": "tourist"},
    {"id": "u04", "name_th": "พี่ฟ้า", "name_en": "Fah", "age": 33, "city_th": "ขอนแก่น",
     "goal_th": "เคยมีคีลอยด์ อยากรู้ว่าแอปจะเตือนไหม", "region": "province"},
    {"id": "u05", "name_th": "น้องต้า", "name_en": "Ta", "age": 19, "city_th": "กรุงเทพฯ",
     "goal_th": "อยากสักหลังมือ แต่กลัวจางเร็ว", "region": "bkk"},
]

PHOTOS = [
    MINT_PHOTO,
    _p("p02", 0.20, 0.12, 0.10, 0.88, "cool", [_d("wrist", 0.91, "right")]),
    _p("p03", 0.25, 0.15, 0.12, 0.90, "neutral", [_d("upper_arm", 0.95, "left")]),
    _p("p04", 0.62, 0.22, 0.48, 0.70, "warm", [_d("ribs", 0.86, "right")]),
    _p("p05", 0.16, 0.10, 0.08, 0.93, "cool", [_d("hand", 0.92, "left")]),
    _p("p06", 0.18, 0.10, 0.10, 0.90, "neutral", [_d("calf", 0.89, "right")]),
    _p("p07", 0.20, 0.55, 0.15, 0.30, "warm", []),
    _p("p08", 0.15, 0.10, 0.08, 0.91, "warm", [_d("behind_ear", 0.87, "left")]),
]

MINT_DESIGN = "d01"
MINT_PLACEMENT = "inner_forearm"
MINT_SIZE = 8
MINT_MODE = "bw"
MINT_QUOTE = 3500
MINT_NOTE = "ชอบแนวเส้นบาง อยากให้ช่อไม่เกินข้อพับศอก และขอแบบขาวดำก่อน"
MINT_FLAGS = ["none"]

DIARY = [
    ("e01", "u01", "2026-06-02", "d03", "behind_ear", 2, "done", "FictoInk สุขุมวิท", 2200),
    ("e02", "u01", "2026-11-20", "d01", "inner_forearm", 8, "booked", "FictoInk สุขุมวิท", 0),
    ("e03", "u01", "2025-12-18", "d06", "wrist", 3, "wishlist", "", 0),
]
