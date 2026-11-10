"""Demo fixture: พี่เจ lays out a Friday 1-for-1 poster for Ficto Café. Fictional only."""
TODAY = "2026-12-07"

JAY = {
    "id": "u01", "name_th": "พี่เจ", "name_en": "Jay", "age": 29, "city_th": "กรุงเทพฯ",
    "shop_th": "Ficto Café", "role_th": "เจ้าของร้านกาแฟสมมติ",
}
MORN = {
    "id": "u02", "name_th": "พี่มอ", "name_en": "Morn", "age": 34, "city_th": "เชียงใหม่",
    "shop_th": "Ficto Night Market", "role_th": "ผู้จัดตลาดนัดสมมติ",
}
PEOPLE = [JAY, MORN]

JAY_BRAND = {"name_th": "Ficto Café", "colors": ["#4A2C2A", "#F8F1E3", "#E8772E"], "heading": "Kanit", "body": "Sarabun"}
MORN_BRAND = {"name_th": "Ficto Night Market", "colors": ["#1E3A5F", "#F4EFE6", "#C4A574"], "heading": "Kanit", "body": "Sarabun"}

JAY_BRIEF = {
    "template": "sale", "size_id": "ig_portrait",
    "title": "โปรศุกร์ 1 แถม 1", "subtitle": "เครื่องดื่มทุกแก้ว",
    "details": "วันศุกร์ 9:00–18:00 · ซอยสุขใจ 12",
    "date_th": "ทุกวันศุกร์", "place_th": "ซอยสุขใจ 12",
    "cta_th": "มาร้านได้เลย", "qr_url": "https://line.me/R/ti/p/@ficto-cafe",
}
MORN_BRIEF = {
    "template": "event", "size_id": "fb_post",
    "title": "ตลาดนัดยามเย็น", "subtitle": "ของทำมือ 30 ร้าน",
    "details": "เสาร์-อาทิตย์ 16:00–21:00",
    "date_th": "เสาร์-อาทิตย์ 16:00–21:00", "place_th": "ลาน Ficto Yard",
    "cta_th": "เข้าฟรี", "qr_url": "https://maps.example/ficto-yard",
}
JAY_MENU = [
    {"name_th": "ลาเต้ Ficto", "price_thb": 85},
    {"name_th": "อเมริกาโน่", "price_thb": 70},
    {"name_th": "ชาไทยเย็น", "price_thb": 65},
    {"name_th": "ครัวซองต์เนย", "price_thb": 55},
]
