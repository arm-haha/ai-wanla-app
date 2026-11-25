"""Fictional demo data only — no real people."""
USER = {"id": "u01", "name_th": "คุณมิ้นท์", "name_en": "Mint", "age": 28, "city_th": "กรุงเทพฯ", "monthly_income": 25000}
BUDDY = {"id": "u02", "name_th": "คุณโบ๊ท", "name_en": "Boat", "age": 29, "city_th": "นนทบุรี", "monthly_income": 30000}
TEEN = {"id": "u03", "name_th": "น้องพิม", "name_en": "Pim", "age": 12, "city_th": "ขอนแก่น", "monthly_income": 0}
Y0, Y1 = "2027-01-01", "2027-12-31"
G_MONEY = {"id": "g1", "title_th": "เก็บเงินเที่ยวญี่ปุ่น 60,000 บาท", "category": "money", "category_th": "เงิน", "unit": "THB",
           "start_value": 0, "target_value": 60000, "start": Y0, "deadline": Y1}
G_WEIGHT = {"id": "g2", "title_th": "ลดน้ำหนักจาก 68 เหลือ 62 กก.", "category": "health", "category_th": "สุขภาพ", "unit": "kg_loss",
            "start_value": 0, "target_value": 6, "start": Y0, "deadline": "2027-06-30"}
G_BOOK = {"id": "g3", "title_th": "อ่านหนังสือให้ได้ 24 เล่ม", "category": "learn", "category_th": "เรียนรู้", "unit": "book",
          "start_value": 0, "target_value": 24, "start": Y0, "deadline": Y1}
G_RUN = {"id": "g4", "title_th": "วิ่งสะสม 300 กม.", "category": "health", "category_th": "สุขภาพ", "unit": "km",
         "start_value": 0, "target_value": 300, "start": Y0, "deadline": Y1}
G_TRIP = {"id": "g5", "title_th": "พาแม่เที่ยวต่างจังหวัด 4 ทริป", "category": "family", "category_th": "ครอบครัว", "unit": "trip",
          "start_value": 0, "target_value": 4, "start": Y0, "deadline": Y1}
GOALS = [G_MONEY, G_WEIGHT, G_BOOK, G_RUN, G_TRIP]
G_CRASH = {"id": "b1", "title_th": "ลด 10 กก. ใน 1 เดือนก่อนงานแต่ง", "category": "health", "category_th": "สุขภาพ", "unit": "kg_loss",
           "start_value": 0, "target_value": 10, "start": Y0, "deadline": "2027-01-31"}
G_VAGUE = {"id": "b2", "title_th": "อยากรวย", "category": "money", "category_th": "เงิน", "unit": "", "start_value": 0, "target_value": 0,
           "start": Y0, "deadline": Y0}
G_HUGE = {"id": "b3", "title_th": "เก็บเงิน 300,000 บาทในปีเดียว", "category": "money", "category_th": "เงิน", "unit": "THB",
          "start_value": 0, "target_value": 300000, "start": Y0, "deadline": Y1}
# what Mint logged by 30 Jun 2027
LOGS = {"g1": [{"date": "2027-%02d-28" % m, "amount": a} for m, a in zip(range(1, 7), (3500, 3000, 4000, 3500, 4000, 4500))],
        "g2": [{"date": "2027-%02d-15" % m, "amount": a} for m, a in zip(range(1, 7), (1.0, 1.0, 0.5, 1.5, 1.0, 0.5))],
        "g3": [{"date": "2027-%02d-20" % m, "amount": 1} for m in range(1, 7)],
        "g4": [{"date": "2027-%02d-10" % m, "amount": a} for m, a in zip(range(1, 7), (20, 25, 15, 30, 35, 40))],
        "g5": [{"date": "2027-04-13", "amount": 1}]}
MID = "2027-06-30"
CHECKINS = ["2027-01-03", "2027-01-10", "2027-01-17", "2027-01-24", "2027-01-31", "2027-02-07"]
