"""Fictional demo: บีม's condo jungle (3 plants). Everything here is example data."""
TODAY = "2026-10-19"
PERSONA = {"name_th": "บีม", "age": 27, "home_th": "คอนโด 1 ห้องนอน ห้องแอร์ หน้าต่างทิศเหนือ", "pets": True, "pet_th": "แมวชื่อถั่วแระ"}
PLANTS = [
    {"id": "p1", "nickname_th": "มอนมอน", "species": "monstera", "light": "low", "pot": "ceramic_glazed", "last_watered": "2026-10-17", "added_on": "2026-08-02", "spot_th": "มุมทีวี"},
    {"id": "p2", "nickname_th": "พลูพลู", "species": "pothos", "light": "medium", "pot": "plastic", "last_watered": "2026-10-07", "added_on": "2026-07-15", "spot_th": "ชั้นหนังสือ"},
    {"id": "p3", "nickname_th": "ลิ้นลิ้น", "species": "snake", "light": "medium", "pot": "terracotta", "last_watered": "2026-10-10", "added_on": "2026-06-20", "spot_th": "ข้างประตูระเบียง"},
]
CHECKUPS = {
    "p1": {"symptoms": ["drooping", "yellow_lower", "leaf_drop", "brown_tips"], "ctx": {"soil": "wet", "light": "low", "days_since_water": 2, "ac_room": True, "months_since_feed": 3}},
    "p2": {"symptoms": ["curling", "crispy_edges", "drooping"], "ctx": {"soil": "dry", "light": "medium", "days_since_water": 12, "ac_room": True, "months_since_feed": 2}},
    "p3": {"symptoms": [], "ctx": {"soil": "dry", "light": "medium", "days_since_water": 9, "ac_room": False, "months_since_feed": 4}},
}
# day-14 re-check of มอนมอน after the plan (moved to bright indirect)
P1_AFTER = {"on": "2026-11-02", "symptoms": ["brown_tips"], "ctx": {"soil": "moist", "light": "bright_indirect", "days_since_water": 5, "ac_room": True, "months_since_feed": 3}, "new_leaves": 2}
PLAN_DONE_DAYS = [1, 2, 3]
LUMA_SAMPLES = [{"spot_th": "มุมทีวี", "mean_luma": 120}, {"spot_th": "ข้างหน้าต่าง 1 ม.", "mean_luma": 160}, {"spot_th": "ระเบียงเที่ยง", "mean_luma": 220}]
ROOM_QUIZ = {"light": "medium", "ac_room": True, "pets": True, "forgetful": True}
CARE_DAYS = ["2026-10-15", "2026-10-16", "2026-10-17", "2026-10-18", "2026-10-19"]
LOG = [
    {"on": "2026-10-03", "kind": "water", "plant_id": "p1", "on_time": False},
    {"on": "2026-10-07", "kind": "water", "plant_id": "p2", "on_time": True},
    {"on": "2026-10-10", "kind": "water", "plant_id": "p3", "on_time": True},
    {"on": "2026-10-10", "kind": "water", "plant_id": "p1", "on_time": False},
    {"on": "2026-10-17", "kind": "water", "plant_id": "p1", "on_time": False},
    {"on": "2026-10-19", "kind": "water", "plant_id": "p2", "on_time": True},
]
