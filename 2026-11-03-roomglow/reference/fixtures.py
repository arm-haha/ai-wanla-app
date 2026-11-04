"""Demo fixture: ฝน, condo bedroom 3.2×4.0 m, ceiling 2.6 m, budget ฿3,000, renter. Prices are example values."""
ROOM = {"name": "ฝน", "room_type": "bedroom", "width_m": 3.2, "length_m": 4.0, "height_m": 2.6, "doors": 1, "windows": 1,
        "renter": True, "budget_thb": 3000, "existing_lm": 800}
SCAN = {"light": 0.3, "clutter": 0.7, "harmony": 0.4, "cohesion": 0.3}
CATALOG = [
 {"id": "led_strip", "name_th": "ไฟเส้น LED หลังหัวเตียง 3 ม.", "category": "light", "price_thb": 290, "impact": 9, "renter_safe": True, "styles": ["any"], "minutes": 20, "boost": {"light": 0.25, "cohesion": 0.05}},
 {"id": "floor_lamp", "name_th": "โคมตั้งพื้นผ้าลินิน", "category": "light", "price_thb": 690, "impact": 8, "renter_safe": True, "styles": ["muji", "japandi", "cozy", "korean"], "minutes": 10, "boost": {"light": 0.2, "cohesion": 0.1}},
 {"id": "bedding_set", "name_th": "ชุดผ้าปูสีครีม/เบจ", "category": "textile", "price_thb": 890, "impact": 10, "renter_safe": True, "styles": ["muji", "korean", "japandi", "cozy"], "minutes": 15, "boost": {"harmony": 0.25, "cohesion": 0.15}},
 {"id": "rug_round", "name_th": "พรมกลม 120 ซม.", "category": "textile", "price_thb": 590, "impact": 6, "renter_safe": True, "styles": ["korean", "cozy", "boho"], "minutes": 5, "boost": {"harmony": 0.1, "cohesion": 0.1}},
 {"id": "curtain_linen", "name_th": "ม่านลินินสีขาวนวล (ราวเดิม)", "category": "textile", "price_thb": 650, "impact": 7, "renter_safe": True, "styles": ["muji", "japandi", "korean"], "minutes": 15, "boost": {"harmony": 0.15, "light": 0.05}},
 {"id": "storage_box", "name_th": "กล่องเก็บของผ้า 4 ใบ", "category": "declutter", "price_thb": 390, "impact": 8, "renter_safe": True, "styles": ["any"], "minutes": 60, "boost": {"clutter": 0.35}},
 {"id": "wall_sticker", "name_th": "วอลเปเปอร์ลอกออกได้ (ผนังหัวเตียง)", "category": "wall", "price_thb": 870, "impact": 7, "renter_safe": True, "styles": ["japandi", "cozy", "boho", "industrial"], "minutes": 90, "boost": {"harmony": 0.15, "cohesion": 0.1}},
 {"id": "paint_wall", "name_th": "ทาสีผนังทั้งห้อง", "category": "wall", "price_thb": 1950, "impact": 10, "renter_safe": False, "styles": ["any"], "minutes": 360, "boost": {"harmony": 0.3}},
 {"id": "shelf_drill", "name_th": "ชั้นลอยเจาะผนัง", "category": "furniture", "price_thb": 450, "impact": 5, "renter_safe": False, "styles": ["any"], "minutes": 45, "boost": {"clutter": 0.15}},
 {"id": "plant_fake", "name_th": "ต้นไม้ปลอมกระถางดินเผา", "category": "plant", "price_thb": 250, "impact": 4, "renter_safe": True, "styles": ["any"], "minutes": 2, "boost": {"harmony": 0.05, "cohesion": 0.05}},
 {"id": "poster_set", "name_th": "โปสเตอร์+เทปกาวไม่ทิ้งรอย 3 ใบ", "category": "decor", "price_thb": 190, "impact": 4, "renter_safe": True, "styles": ["korean", "boho", "industrial", "cozy"], "minutes": 10, "boost": {"cohesion": 0.1}},
 {"id": "mirror_lean", "name_th": "กระจกยาวพิงผนัง", "category": "furniture", "price_thb": 790, "impact": 6, "renter_safe": True, "styles": ["korean", "muji", "japandi"], "minutes": 5, "boost": {"light": 0.1, "cohesion": 0.05}},
]
DECLUTTER = [
 {"name": "เสื้อไม่ได้ใส่ 1 ปี 14 ตัว", "action": "donate"}, {"name": "หูฟังเก่า", "action": "sell", "resale_thb": 450},
 {"name": "เก้าอี้พับ", "action": "sell", "resale_thb": 300}, {"name": "กล่องพัสดุเปล่า", "action": "toss"},
 {"name": "โคมหัวเตียงเดิม", "action": "keep"}]
POLL = ["muji", "korean", "japandi"]
VOTES = [{"voter": v, "option": o} for v, o in [("เมย์", "korean"), ("บีม", "korean"), ("แม่", "muji"), ("ต้น", "korean"), ("จูน", "japandi"), ("ปาล์ม", "korean"), ("เมย์", "korean")]]
