"""Fictional demo data only — no real people."""
from handfont import *

TODAY = "2026-12-18"
PEOPLE = [
    {"id": "u01", "name_th": "ครูมิ้นท์", "name_en": "Mint", "age": 27, "city_th": "นนทบุรี", "use_th": "ทำใบงาน/การ์ดให้นักเรียน"},
    {"id": "u02", "name_th": "พี่บอส", "name_en": "Boss", "age": 33, "city_th": "เชียงใหม่", "use_th": "โน้ตขอบคุณลูกค้าร้านออนไลน์"},
    {"id": "u03", "name_th": "น้องใบเตย", "name_en": "Baitoey", "age": 11, "city_th": "ขอนแก่น", "use_th": "ฝึกคัดลายมือ (ผู้ปกครองดูแล)"},
    {"id": "u04", "name_th": "คุณยายสมใจ", "name_en": "Somjai", "age": 68, "city_th": "สุพรรณบุรี", "use_th": "ส.ค.ส. ลายมือยายให้หลาน"},
]
PHOTOS = [
    {"id": "s01", "light": 0.85, "blur": 0.05, "skew_deg": 2, "ink_contrast": 0.9},
    {"id": "s02", "light": 0.5, "blur": 0.2, "skew_deg": 10, "ink_contrast": 0.7},
    {"id": "s03", "light": 0.3, "blur": 0.5, "skew_deg": 15, "ink_contrast": 0.4},
]
QUICK = template_chars("thai_quick")
# Mint's sheet: everything fine except 3 cells
_bad = {"ฃ": {"ink": 0.0, "touches_border": False, "extra_blobs": 0},
        "ฬ": {"ink": 0.12, "touches_border": True, "extra_blobs": 0},
        "ๆ": {"ink": 0.02, "touches_border": False, "extra_blobs": 0}}
CELLS = [dict(char=c, **_bad.get(c, {"ink": 0.11, "touches_border": False, "extra_blobs": 0})) for c in QUICK]
CHECKS = [glyph_check(c) for c in CELLS]
COV = coverage("thai_quick", CHECKS)
STYLE = style_params("regular", 4, "natural", 10)
BUILD = font_build(PEOPLE[0], "thai_quick", COV, STYLE, "ttf")
MSG = "สุขสันต์วันครูนะคะ ขอบคุณที่ตั้งใจสอนทุกวัน"
DIARY = [
    {"date": "2026-12-18", "kind": "build", "version": 1},
    {"date": "2026-12-18", "kind": "card"},
    {"date": "2026-12-19", "kind": "sticker"},
    {"date": "2026-12-20", "kind": "practice", "score": 72},
    {"date": "2026-12-21", "kind": "practice", "score": 78},
    {"date": "2026-12-22", "kind": "practice", "score": 83},
    {"date": "2026-12-22", "kind": "build", "version": 2},
]
SAMPLES = [{"height_var": 0.2, "baseline_var": 0.15, "spacing_var": 0.3, "slant_var": 0.1},
           {"height_var": 0.16, "baseline_var": 0.12, "spacing_var": 0.24, "slant_var": 0.1}]
