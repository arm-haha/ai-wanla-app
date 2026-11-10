"""Demo fixture: พี่นุ่น (Noon) helps her P.4 child with a percent-discount word problem — hints only. Fictional only."""
TODAY = "2026-11-13"

def _p(pid, glare, blur, tilt, fill, tid, conf, fields):
    return {"id": pid, "px_w": 3024, "px_h": 4032, "glare": glare, "blur": blur, "tilt": tilt,
            "text_fill": fill, "template": tid, "confidence": conf, "fields": fields}

NOON = {"id": "u01", "name_th": "พี่นุ่น", "name_en": "Noon", "age": 36, "city_th": "กรุงเทพฯ",
        "goal_th": "ช่วยลูกป.4 เรียนโจทย์ปัญหาร้อยละ โดยไม่บอกคำตอบ", "child_grade": "p4"}
NOON_FIELDS = {"price": 800, "percent": 25}
NOON_PHOTO = _p("p01", 0.15, 0.10, 0.08, 0.90, "percent_discount", 0.94, NOON_FIELDS)

PEOPLE = [
    NOON,
    {"id": "u02", "name_th": "พี่กบ", "name_en": "Kob", "age": 41, "city_th": "ขอนแก่น",
     "goal_th": "ลูกป.3 สับสนพื้นที่กับความยาวรอบรูป", "child_grade": "p3"},
    {"id": "u03", "name_th": "พี่เจี๊ยบ", "name_en": "Jeab", "age": 39, "city_th": "เชียงใหม่",
     "goal_th": "ลูกป.5 ติดเศษส่วนของจำนวน", "child_grade": "p5"},
    {"id": "u04", "name_th": "พี่โจ้", "name_en": "Joe", "age": 38, "city_th": "พัทยา",
     "goal_th": "ลูกม.1 เลือกกาลกริยาภาษาอังกฤษไม่ถูก", "child_grade": "m1"},
    {"id": "u05", "name_th": "พี่ฝน", "name_en": "Fon", "age": 44, "city_th": "กรุงเทพฯ",
     "goal_th": "ลูกม.2 ย้ายข้างสมการแล้วลืมเปลี่ยนเครื่องหมาย", "child_grade": "m2"},
]

PHOTOS = [
    NOON_PHOTO,
    _p("p02", 0.18, 0.12, 0.10, 0.86, "area_rect", 0.91, {"length": 10, "width": 4, "unit": "เมตร"}),
    _p("p03", 0.16, 0.10, 0.08, 0.88, "fraction_of", 0.92, {"whole": 24, "num": 1, "den": 3}),
    _p("p04", 0.20, 0.12, 0.10, 0.84, "eng_tense", 0.90, {"sentence": "They ____ football yesterday.", "time_word": "yesterday", "answer": "played", "choices": ["play", "played", "playing"]}),
    _p("p05", 0.15, 0.10, 0.08, 0.87, "linear_eq", 0.93, {"a": 2, "b": 3, "c": 11}),
    _p("p06", 0.16, 0.11, 0.09, 0.85, "water_cycle", 0.89, {"clue": "น้ำในทะเลกลายเป็นไอเมื่อโดนความร้อน", "answer": "การระเหย"}),
    _p("p07", 0.60, 0.48, 0.45, 0.35, "percent_discount", 0.40, {"price": 800, "percent": 25}),
    _p("p08", 0.14, 0.08, 0.06, 0.92, "decimal_add", 0.95, {"a": 1.25, "b": 2.5}),
]

NOON_NOTE = "ลูกคิดเงินที่ลดได้แล้ว แต่ยังไม่แน่ใจว่าต้องลบออกจากราคาเดิมไหม ใช้คำใบ้ระดับ 2 ยังไม่เปิดคำตอบ"
PROGRESS = [
    ("e01", "c01", "2026-11-06", "decimal_add", 1, 12, True),
    ("e02", "c01", "2026-11-10", "percent_discount", 2, 18, True),
    ("e03", "c01", "2026-11-13", "percent_discount", 2, 7, False),
]
