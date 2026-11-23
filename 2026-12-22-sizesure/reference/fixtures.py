"""Fictional demo data only — no real people, no real shops."""
from sizesure import *

TODAY = "2026-12-22"
PEOPLE = [
    {"id": "u01", "name_th": "พี่แพรว", "name_en": "Praew", "age": 28, "height_cm": 160, "city_th": "กรุงเทพฯ", "updated": "2026-12-22"},
    {"id": "u02", "name_th": "พี่โอ๊ต", "name_en": "Oat", "age": 34, "height_cm": 176, "city_th": "ขอนแก่น", "updated": "2026-12-20"},
    {"id": "u03", "name_th": "คุณแม่นวล", "name_en": "Nuan", "age": 61, "height_cm": 154, "city_th": "ราชบุรี", "updated": "2026-12-22"},
    {"id": "u04", "name_th": "น้องมายด์", "name_en": "Mind", "age": 15, "height_cm": 158, "city_th": "เชียงราย", "updated": "2026-12-22"},
]
PHOTOS = [
    {"id": "f01", "light": 0.9, "full_body": 1, "pose_ok": 1, "clothing": "fitted", "ref_visible": 1},
    {"id": "f02", "light": 0.7, "full_body": 1, "pose_ok": 0, "clothing": "normal", "ref_visible": 0},
    {"id": "f03", "light": 0.4, "full_body": 0, "pose_ok": 0, "clothing": "bulky", "ref_visible": 0},
]
# what the vision model measured on Praew's front + side photos (pixels; 10 px ≈ 1 cm at 160 cm)
AI_PRAEW = {"front": {"height_px": 1600, "shoulder_px": 370, "chest_px": 300, "waist_px": 250, "hip_px": 340, "inseam_px": 720, "arm_px": 540},
            "side": {"height_px": 1600, "chest_px": 220, "waist_px": 180, "hip_px": 240},
            "a4_px": 298, "clothing": "fitted", "people": 1, "nudity": False, "pose_ok": True, "confidence": 0.9}
AI_OAT = {"front": {"height_px": 1408, "shoulder_px": 368, "chest_px": 280, "waist_px": 248, "hip_px": 272, "inseam_px": 640, "arm_px": 488},
          "side": {"height_px": 1408, "chest_px": 208, "waist_px": 200, "hip_px": 200},
          "a4_px": 260, "clothing": "loose", "people": 1, "nudity": False, "pose_ok": True, "confidence": 0.74}
M_PRAEW = measure_body(AI_PRAEW, 160)
M_OAT = measure_body(AI_OAT, 176)
# shop chart screenshots, as read by the vision model
CHART_SHIRT = {"shop_th": "ร้านเสื้อครอป (สมมติ)", "unit": "inch", "method": "flat",
               "rows": [{"label": "S", "values": {"chest": 17, "length": 22}}, {"label": "M", "values": {"chest": 18, "length": 23}},
                        {"label": "L", "values": {"chest": 19, "length": 24}}, {"label": "XL", "values": {"chest": 20, "length": 25}}]}
CHART_DRESS = {"shop_th": "ร้านเดรสลินิน (สมมติ)", "unit": "cm", "method": "body",
               "rows": [{"label": "S", "values": {"chest": [82, 86], "waist": [64, 68], "hip": [88, 92]}},
                        {"label": "M", "values": {"chest": [87, 91], "waist": [69, 73], "hip": [93, 97]}},
                        {"label": "L", "values": {"chest": [92, 96], "waist": [74, 78], "hip": [98, 102]}}]}
CHART_JEANS = {"shop_th": "ร้านยีนส์ (สมมติ)", "unit": "inch", "method": "body",
               "rows": [{"label": str(w), "values": {"waist": w, "hip": w + 9}} for w in range(24, 33)]}
N_SHIRT, N_DRESS, N_JEANS = normalize_chart(CHART_SHIRT), normalize_chart(CHART_DRESS), normalize_chart(CHART_JEANS)
REC_SHIRT = recommend(M_PRAEW, N_SHIRT, "top")
REC_DRESS = recommend(M_PRAEW, N_DRESS, "dress")
REC_JEANS = recommend(M_PRAEW, N_JEANS, "bottom", "slim", "some")
SHOE = shoe_size(940, 1188, 360)
PP_PRAEW = passport(PEOPLE[0], M_PRAEW, SHOE)
LOG = [
    {"date": "2026-09-15", "cm": {"chest": 85.5, "waist": 69.0, "hip": 94.0}},
    {"date": "2026-12-22", "cm": dict((k, M_PRAEW["cm"][k]) for k in CIRC)},
]
