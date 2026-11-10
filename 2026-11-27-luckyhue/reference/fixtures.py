"""Demo fixture: พี่เมย์ (May) was born on Friday and wants today's lucky colour + an outfit. Fictional only."""
TODAY = "2026-11-27"  # Friday
MAY_BIRTH = "1998-05-01"  # Friday

def _shot(sid, glare, blur, crop, items):
    return {"id": sid, "px_w": 1170, "px_h": 2532, "glare": glare, "blur": blur, "crop": crop, "items": items}

def _item(iid, name_th, category, color_key, color_th):
    return {"id": iid, "name_th": name_th, "category": category, "color_key": color_key, "color_th": color_th}

MAY = {
    "id": "u01", "name_th": "พี่เมย์", "name_en": "May", "age": 28, "city_th": "กรุงเทพฯ",
    "birth_iso": MAY_BIRTH, "birth_weekday": "friday",
    "goal_th": "เกิดวันศุกร์ อยากรู้สีมงคล แล้วจับคู่ชุดจากรูปตู้เสื้อผ้า",
}
# quality 88: 0.35*0.14 + 0.40*0.12 + 0.25*0.08 = 0.117
MAY_CLOSET = _shot("s01", 0.14, 0.12, 0.08, [
    _item("i01", "เสื้อเชิ้ตขาว", "top", "white", "ขาว"),
    _item("i02", "กระโปรงฟ้า", "bottom", "blue", "ฟ้า"),
    _item("i03", "กระเป๋าเบจ", "bag", "beige", "เบจ"),
    _item("i04", "รองเท้าดำ", "shoes", "black", "ดำ"),
    _item("i05", "เสื้อชมพู", "top", "pink", "ชมพู"),
])
MAY_PICK = ["i01", "i02", "i03"]  # white + blue + beige → score 67

BOW = {
    "id": "u02", "name_th": "น้องโบว์", "name_en": "Bow", "age": 25, "city_th": "เชียงใหม่",
    "birth_iso": "1999-08-15",  # Sunday? will confirm in tests via weekday_from_date
    "birth_weekday": None,
    "goal_th": "เกิดวันอาทิตย์ อยากได้วอลเปเปอร์สีแดง",
}
# fill weekday at import
from datetime import date as _date
BOW["birth_weekday"] = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"][_date.fromisoformat(BOW["birth_iso"]).weekday()]

KEN = {
    "id": "u03", "name_th": "พี่เคน", "name_en": "Ken", "age": 33, "city_th": "ขอนแก่น",
    "birth_iso": "1993-06-16", "birth_weekday": None,
    "goal_th": "เกิดวันพุธ อยากเทียบสีเขียวกับแสดกลางคืน",
}
KEN["birth_weekday"] = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"][_date.fromisoformat(KEN["birth_iso"]).weekday()]

BAD_SHOT = _shot("s02", 0.68, 0.52, 0.50, [_item("i09", "เสื้อ", "top", "white", "ขาว")])
EMPTY_SHOT = _shot("s03", 0.20, 0.15, 0.10, [])
CLASH_PICK = ["i05", "i02"]  # pink top + blue skirt on Friday

PEOPLE = [MAY, BOW, KEN]
