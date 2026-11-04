"""Demo fixture constants for ReelForge — persona เจี๊ยบ (สมมติ)."""

TODAY = "2026-10-12"
PERSONA = {
    "name": "เจี๊ยบ",
    "role_th": "แม่ค้าออนไลน์ขายขนมบ้าน / คนทำคอนเทนต์มือใหม่",
    "note_th": "เจี๊ยบ เป็นตัวละครสมมติ ชื่อร้านและตัวเลขในแพ็กนี้แต่งขึ้นเพื่อเดโม",
}

DEMO_IDEA_RAW = "ขายคุกกี้เนยสด ส่ง LINE ทั้งกรุงเทพ ชิ้นละ 45 บาท เซ็ต 6 ชิ้น 240"
DEMO_STYLE = "soft_sell_before_after"
DEMO_DURATION = 30

# Expected must-match numbers (asserted in tests + README)
EXPECT = {
    "product": "คุกกี้เนยสด",
    "category": "snacks",
    "price_unit": 45.0,
    "price_set": 240.0,
    "set_qty": 6,
    "channel": "LINE",
    "area": "กรุงเทพ",
    "cta_keyword": "คุกกี้",
    "shot_count": 5,
    "durations": [3, 6, 8, 8, 5],
    "hook_winner_id": "hook_a",
    "hook_winner_contains": ["vs", "30 วิ"],
    "cover_count": 3,
    "hooks_count": 3,
}

# Extra ideas for test vectors / style library demos
EXTRA_IDEAS = [
    {
        "id": "idea_beauty",
        "raw": "รีวิวเซรั่มวิตามินซี ทาเช้าเย็น ขวดละ 390 บาท สั่ง Shopee",
        "style": "unboxing",
        "duration": 30,
    },
    {
        "id": "idea_study",
        "raw": "สรุปชีวะระบบหายใจ ติวสอบเข้า ม.ปลาย 3 ขั้น",
        "style": "teach_3_steps",
        "duration": 30,
    },
    {
        "id": "idea_story",
        "raw": "จากแม่บ้านสู่แม่ค้าคุกกี้ เริ่มขายใน LINE",
        "style": "storytime",
        "duration": 30,
    },
]

# History of past blueprints (streak / retention demo)
HISTORY_META = [
    {"blueprint_id": "bp_soft_sell_before_after_30_snacks", "title_th": "คุกกี้เนยสด · ก่อน/หลัง", "created_at": "2026-10-12T07:58:00+07:00", "duration_s": 30},
    {"blueprint_id": "bp_teach_3_steps_30_study", "title_th": "ติวชีวะ 3 ขั้น", "created_at": "2026-10-11T20:10:00+07:00", "duration_s": 30},
    {"blueprint_id": "bp_unboxing_30_beauty", "title_th": "Unbox เซรั่ม", "created_at": "2026-10-10T18:40:00+07:00", "duration_s": 30},
]

STREAK = {"days": 3, "last_date": "2026-10-12", "label_th": "สตรีค 3 วัน · เก่งมาก 🔥"}

COLORS = {
    "bg": "#0F0A1A",
    "magenta": "#E11D48",
    "violet": "#8B5CF6",
    "cream": "#FDF4FF",
    "gold": "#FBBF24",
}
