"""Demo fixture: พี่โอ๊ต (Oat) sees a yellow check-engine + low tire light on the way to work. Fictional only."""
TODAY = "2026-11-10"

def _p(pid, glare, blur, tilt, dets):
    return {"id": pid, "px_w": 3024, "px_h": 4032, "glare": glare, "blur": blur, "tilt": tilt, "detections": dets}

def _d(sym, color, conf, flashing=False):
    return {"symbol": sym, "color_seen": color, "confidence": conf, "flashing": flashing}

OAT_CAR = {"id": "c01", "model_th": "เก๋งเล็ก FictoCity 1.2", "year": 2019, "fuel": "petrol", "car_class": "eco", "odometer_km": 87450}
OAT = {"id": "u01", "name_th": "พี่โอ๊ต", "name_en": "Oat", "age": 34, "city_th": "กรุงเทพฯ", "goal_th": "ขับไปทำงานสาย บางนา แล้วไฟส้มขึ้น",
       "region": "bkk", "car": OAT_CAR}
OAT_PHOTO = _p("p01", 0.20, 0.10, 0.10, [_d("check_engine", "yellow", 0.93), _d("tpms", "yellow", 0.88), _d("service_due", "green", 0.41)])

PEOPLE = [
    OAT,
    {"id": "u02", "name_th": "น้องมุก", "name_en": "Muk", "age": 24, "city_th": "ขอนแก่น", "goal_th": "ไฟน้ำมันเครื่องขึ้นบนถนนมิตรภาพ", "region": "province",
     "car": {"id": "c02", "model_th": "เก๋งเล็ก FictoCity 1.5", "year": 2016, "fuel": "petrol", "car_class": "eco", "odometer_km": 142300}},
    {"id": "u03", "name_th": "ลุงสมชัย", "name_en": "Somchai", "age": 58, "city_th": "เชียงใหม่", "goal_th": "กระบะบรรทุกของ เข็มความร้อนพุ่งขึ้นเขา", "region": "province",
     "car": {"id": "c03", "model_th": "กระบะ FictoTruck 2.5 ดีเซล", "year": 2014, "fuel": "diesel", "car_class": "suv_pickup", "odometer_km": 231800}},
    {"id": "u04", "name_th": "พี่แนน", "name_en": "Nan", "age": 41, "city_th": "พัทยา", "goal_th": "ไฟแบตขึ้นตอนขับรับลูก", "region": "tourist",
     "car": {"id": "c04", "model_th": "ซีดาน FictoSedan 1.8", "year": 2017, "fuel": "petrol", "car_class": "sedan", "odometer_km": 118900}},
    {"id": "u05", "name_th": "น้องบีม", "name_en": "Beam", "age": 27, "city_th": "กรุงเทพฯ", "goal_th": "ไฟเตือนเยอะ ไม่รู้ว่าอันไหนต้องกลัว", "region": "bkk",
     "car": {"id": "c05", "model_th": "SUV FictoSUV 1.6 ไฮบริด", "year": 2021, "fuel": "hybrid", "car_class": "suv_pickup", "odometer_km": 45200}},
]

PHOTOS = [
    OAT_PHOTO,
    _p("p02", 0.15, 0.10, 0.05, [_d("oil_pressure", "red", 0.96)]),
    _p("p03", 0.30, 0.20, 0.20, [_d("coolant_temp", "red", 0.94), _d("dpf", "yellow", 0.81)]),
    _p("p04", 0.65, 0.20, 0.50, [_d("battery_charge", "red", 0.90), _d("abs", "yellow", 0.72)]),
    _p("p05", 0.10, 0.10, 0.10, [_d("washer", "green", 0.85), _d("high_beam", "blue", 0.92), _d("seat_belt", "red", 0.77)]),
    _p("p06", 0.20, 0.15, 0.10, [_d("check_engine", "yellow", 0.90, True)]),
    _p("p07", 0.20, 0.10, 0.10, [_d("abs", "red", 0.88)]),
    _p("p08", 0.20, 0.55, 0.10, []),
]

SERVICE_LOG = [
    ("e01", "c01", "2026-04-18", 76900, "engine_oil", 1450, "ศูนย์ใกล้บ้าน"),
    ("e02", "c01", "2025-12-05", 69200, "tire_replace", 9800, "ร้านยางบางนา"),
    ("e03", "c01", "2025-09-02", 64000, "battery", 2600, "ร้านแบตซอยบ้าน"),
    ("e04", "c01", "2025-12-20", 70000, "act", 645, "ออนไลน์"),
    ("e05", "c01", "2025-12-05", 69200, "tax", 1100, "ออนไลน์"),
]
OAT_SYMPTOMS = ["none"]
OAT_QUOTES = [("f01", 0), ("f03", 4200), ("f04", 150)]
