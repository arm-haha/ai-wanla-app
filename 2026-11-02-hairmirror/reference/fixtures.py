PROFILE = {"name": "ภูมิ", "age": 22, "hair_type": "straight", "thickness": "thick", "current_length_cm": 6,
           "max_daily_minutes": 5, "budget_month_thb": 300, "gender_style": "masc"}
MEAS = {"face_length": 19.0, "forehead_w": 14.6, "cheek_w": 15.6, "jaw_w": 13.4}
STYLES = [
 {"id": "two_block", "name_th": "ทูบล็อกเท็กซ์เจอร์", "length": "short", "suits": ["round", "oval", "square"], "hair_types": ["straight", "wavy"],
  "daily_minutes": 5, "salon_cost_thb": 250, "maintenance_weeks": 4, "neutral_ok": True,
  "barber_phrase_th": "ไถข้างกับหลัง 6 มิล ไม่ไล่เฟด ด้านบนเหลือ 7 ซม. ซอยเท็กซ์เจอร์ให้ฟู", "dont_th": ["อย่าตัดด้านบนสั้นกว่า 6 ซม."]},
 {"id": "low_fade_crop", "name_th": "ครอปโลว์เฟด", "length": "short", "suits": ["oval", "square", "oblong"], "hair_types": ["straight", "wavy", "curly"],
  "daily_minutes": 3, "salon_cost_thb": 300, "maintenance_weeks": 3, "neutral_ok": True,
  "barber_phrase_th": "โลว์เฟด 0.5 ถึง 3 มิล ด้านบน 4 ซม. หน้าม้าตัดตรงเท็กซ์เจอร์", "dont_th": []},
 {"id": "comma", "name_th": "คอมม่าแฮร์", "length": "medium", "suits": ["round", "oval", "heart", "diamond"], "hair_types": ["straight"],
  "daily_minutes": 10, "salon_cost_thb": 350, "maintenance_weeks": 6, "neutral_ok": True,
  "barber_phrase_th": "ด้านข้าง 3 ซม. ด้านบน 12 ซม. ปล่อยหน้าม้ายาวไว้ม้วนเป็นคอมม่า", "dont_th": ["อย่าซอยหน้าม้าบาง"]},
 {"id": "buzz", "name_th": "บัซคัท", "length": "short", "suits": ["oval", "square", "diamond"], "hair_types": ["straight", "wavy", "curly"],
  "daily_minutes": 0, "salon_cost_thb": 150, "maintenance_weeks": 2, "neutral_ok": False,
  "barber_phrase_th": "ปัตตาเลี่ยน 6 มิล ทั้งหัว เก็บไรผมตรง", "dont_th": []},
 {"id": "middle_part", "name_th": "แสกกลางม่าน", "length": "medium", "suits": ["round", "square", "heart"], "hair_types": ["straight", "wavy"],
  "daily_minutes": 8, "salon_cost_thb": 300, "maintenance_weeks": 6, "neutral_ok": True,
  "barber_phrase_th": "ด้านข้างคลุมหู 1 ซม. ด้านบน 14 ซม. แสกกลางเลเยอร์หน้า", "dont_th": []},
 {"id": "wolf_cut", "name_th": "วูล์ฟคัท", "length": "medium", "suits": ["oval", "heart", "oblong"], "hair_types": ["wavy", "curly"],
  "daily_minutes": 7, "salon_cost_thb": 600, "maintenance_weeks": 8, "neutral_ok": True,
  "barber_phrase_th": "เลเยอร์สั้นด้านบน ปล่อยท้ายทอยยาว ซอยปลายฟุ้ง", "dont_th": []},
 {"id": "side_part", "name_th": "แสกข้างคลาสสิก", "length": "short", "suits": ["round", "oval", "oblong", "diamond"], "hair_types": ["straight", "wavy"],
  "daily_minutes": 6, "salon_cost_thb": 250, "maintenance_weeks": 4, "neutral_ok": True,
  "barber_phrase_th": "ข้าง 9 มิล ไล่ขึ้น ด้านบน 8 ซม. แสกซ้าย 7:3", "dont_th": []},
 {"id": "mullet", "name_th": "มัลเล็ตโมเดิร์น", "length": "medium", "suits": ["oval", "square"], "hair_types": ["wavy", "curly"],
  "daily_minutes": 5, "salon_cost_thb": 450, "maintenance_weeks": 5, "neutral_ok": False,
  "barber_phrase_th": "ข้างสั้น 6 มิล ด้านบน 6 ซม. ท้ายทอยยาว 10 ซม.", "dont_th": []},
 {"id": "french_crop", "name_th": "เฟรนช์ครอป", "length": "short", "suits": ["round", "oval", "oblong"], "hair_types": ["straight", "wavy"],
  "daily_minutes": 2, "salon_cost_thb": 250, "maintenance_weeks": 4, "neutral_ok": True,
  "barber_phrase_th": "ข้าง 3 มิล เฟดสูง ด้านบน 5 ซม. หน้าม้าสั้นตรง", "dont_th": []},
]
ZONES = [{"zone": "sides", "length_mm": 6, "note_th": "ไถ ไม่ไล่เฟด"}, {"zone": "back", "length_mm": 6},
         {"zone": "top", "length_cm": 7, "note_th": "ซอยเท็กซ์เจอร์"}, {"zone": "fringe", "length_cm": 6, "note_th": "ปัดลงเฉียง"},
         {"zone": "neckline", "length_mm": 0, "note_th": "เก็บโค้งธรรมชาติ"}]
VOTES = [{"voter": "ต้น", "option": "two_block"}, {"voter": "ฟ้า", "option": "comma"}, {"voter": "มิว", "option": "two_block"},
         {"voter": "เจ", "option": "french_crop"}, {"voter": "ปลา", "option": "two_block"}, {"voter": "ฟ้า", "option": "two_block"},
         {"voter": "บอส", "option": "comma"}, {"voter": "แนน", "option": "two_block"}, {"voter": "เกม", "option": "mohawk"}]
POLL = ["two_block", "comma", "french_crop"]
