"""Demo fixture: น้องเบนซ์ (Benz) photographs a condo rental contract and finds two red flags before signing. Fictional only, not a real contract."""
TODAY = "2026-11-16"

def _p(pid, kind, glare, blur, tilt, fill, dets):
    return {"id": pid, "px_w": 3024, "px_h": 4032, "kind": kind, "glare": glare, "blur": blur, "tilt": tilt,
            "text_fill": fill, "detections": dets}

def _d(clause, conf, excerpt=""):
    return {"clause": clause, "confidence": conf, "excerpt_th": excerpt}

BENZ = {"id": "u01", "name_th": "น้องเบนซ์", "name_en": "Benz", "age": 29, "city_th": "กรุงเทพฯ",
        "goal_th": "จะเช่าคอนโด อยากรู้จุดอันตรายก่อนเซ็น", "region": "bkk"}
BENZ_TERMS = {"rent_thb": 18000, "deposit_months": 3, "advance_months": 1, "term_months": 12,
              "extras_thb": 2000, "late_fee_per_day_thb": 200}
BENZ_PHOTO = _p("p01", "rental", 0.16, 0.10, 0.08, 0.90, [
    _d("auto_renew", 0.93, "หากไม่บอกเลิกก่อน 30 วัน ให้ถือว่าต่อสัญญาอีก 12 เดือน"),
    _d("excess_deposit", 0.91, "ผู้เช่าวางมัดจำสามเดือน"),
    _d("no_receipt", 0.44, ""),
])
BENZ_NOTE = "ยังไม่เซ็น ขอพาพี่ไปอ่านและถามเรื่องมัดจำ 3 เดือนกับการต่ออัตโนมัติก่อน"
BENZ_CHECKED = ["parties", "address", "rent"]  # incomplete

PEOPLE = [
    BENZ,
    {"id": "u02", "name_th": "พี่โอม", "name_en": "Ohm", "age": 41, "city_th": "ขอนแก่น",
     "goal_th": "จะเซ็นสัญญากู้ ดอก 2% ต่อเดือน", "region": "province"},
    {"id": "u03", "name_th": "พี่นิด", "name_en": "Nid", "age": 35, "city_th": "พัทยา",
     "goal_th": "สัญญาเช่าบ้านมีช่องว่างหลายจุด", "region": "tourist"},
    {"id": "u04", "name_th": "น้องบิว", "name_en": "Beau", "age": 26, "city_th": "เชียงใหม่",
     "goal_th": "สัญญาเช่าดูเรียบ ๆ อยากเช็กให้ครบ", "region": "province"},
    {"id": "u05", "name_th": "ลุงชัย", "name_en": "Chai", "age": 58, "city_th": "กรุงเทพฯ",
     "goal_th": "ลูกเอาสัญญากู้มาให้ช่วยอ่าน", "region": "bkk"},
]

LOAN_TERMS = {"principal_thb": 100000, "interest_pct_month": 2.0, "term_months": 12}
CLEAN_RENT = {"rent_thb": 9000, "deposit_months": 1, "advance_months": 1, "term_months": 6, "extras_thb": 0, "late_fee_per_day_thb": 0}

PHOTOS = [
    BENZ_PHOTO,
    _p("p02", "loan", 0.18, 0.12, 0.10, 0.86, [_d("interest_high", 0.95, "ดอกเบี้ยร้อยละสองต่อเดือน"), _d("seizure", 0.88, "ผู้ให้กู้มีสิทธิหักบัญชีได้ทันที")]),
    _p("p03", "rental", 0.20, 0.15, 0.12, 0.84, [_d("blank_terms", 0.92, "มีช่องว่างค่าปรับ"), _d("entry_no_notice", 0.87, "ผู้ให้เช่าเข้าห้องได้ตลอดเวลา")]),
    _p("p04", "rental", 0.14, 0.08, 0.06, 0.92, [_d("utility_unclear", 0.84, "ค่าน้ำไฟตามที่ผู้ให้เช่ากำหนด")]),
    _p("p05", "loan", 0.16, 0.10, 0.08, 0.88, [_d("hidden_fee", 0.86, "ค่าดำเนินการตามที่ผู้ให้กู้ประกาศ")]),
    _p("p06", "rental", 0.15, 0.10, 0.08, 0.90, [_d("repair_all", 0.90, "ผู้เช่ารับผิดชอบซ่อมแซมทั้งหมด"), _d("early_termination", 0.82, "ห้ามเลิกก่อนครบกำหนด")]),
    _p("p07", "rental", 0.62, 0.48, 0.45, 0.32, []),
    _p("p08", "rental", 0.12, 0.08, 0.05, 0.94, []),
]

DIARY = [
    ("e01", "u01", "2026-10-02", "rental", "สัญญาห้องเก่า (สมมติ)", "yellow"),
    ("e02", "u01", "2026-11-16", "rental", "คอนโด FictoResidence", "red"),
]
