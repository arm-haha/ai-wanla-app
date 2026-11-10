"""Demo fixture: พี่บิ๋ม (Bim) answers 5 questions and gets birthday-gift ideas within ฿1,500 for her boyfriend. Fictional only."""
TODAY = "2026-11-20"

BIM = {
    "id": "u01", "name_th": "พี่บิ๋ม", "name_en": "Bim", "age": 31, "city_th": "กรุงเทพฯ",
    "goal_th": "ซื้อของขวัญวันเกิดแฟน งบ 1,500 ชอบคาเฟ่และเสื้อโอเวอร์ไซส์",
}
BIM_QUIZ = dict(relationship="partner", age_band="25-34", vibe="cozy", hobbies=["cafe", "fashion"],
                occasion="birthday", budget_thb=1500, receiver_name_th="ต้น")

NAN = {
    "id": "u02", "name_th": "พี่แนน", "name_en": "Nan", "age": 41, "city_th": "เชียงใหม่",
    "goal_th": "ของขึ้นบ้านใหม่ให้เพื่อน งบ 2,000",
}
NAN_QUIZ = dict(relationship="friend", age_band="35-49", vibe="practical", hobbies=["home", "plants", "cooking"],
                occasion="housewarming", budget_thb=2000, receiver_name_th="เจ")

GAI = {
    "id": "u03", "name_th": "น้องไกด์", "name_en": "Guide", "age": 28, "city_th": "ขอนแก่น",
    "goal_th": "ของวันเกิดหลาน 8 ขวบ งบ 600",
}
GAI_QUIZ = dict(relationship="kid", age_band="0-12", vibe="playful", hobbies=["games"],
                occasion="birthday", budget_thb=600, receiver_name_th="น้องภูมิ")

OT = {
    "id": "u04", "name_th": "พี่โอ้", "name_en": "Oh", "age": 36, "city_th": "ภูเก็ต",
    "goal_th": "ของขอบคุณหัวหน้า งบ 800",
}
OT_QUIZ = dict(relationship="colleague", age_band="50+", vibe="practical", hobbies=["cafe", "books"],
                occasion="thank_you", budget_thb=800, receiver_name_th="คุณสุรีย์")

PEOPLE = [BIM, NAN, GAI, OT]
QUIZZES = {"bim": BIM_QUIZ, "nan": NAN_QUIZ, "gai": GAI_QUIZ, "ot": OT_QUIZ}

EVENTS = [
    ("e01", "ต้น", "birthday", "2026-12-08", 1500),       # 18 days → soon
    ("e02", "แม่", "birthday", "2026-11-25", 1000),        # 5 days → due
    ("e03", "เจ", "housewarming", "2026-12-20", 2000),     # 30 days → ok
    ("e04", "คุณสุรีย์", "thank_you", "2026-11-18", 800),  # past
]
