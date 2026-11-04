"""Demo fixture: ห้องหอ 'ฟ้า' (สมมติ) 24 ตร.ม. — Wed 2026-10-21 20:30, roommate 'มุก'."""
TODAY = "2026-10-21"
NAME = "ฟ้า"
ROOMMATES = ["ฟ้า", "มุก"]
BEFORE = [
    {"id": "clothes_pile", "severity": 2}, {"id": "trash_floor", "severity": 2}, {"id": "dishes_cups", "severity": 1},
    {"id": "snack_wrappers", "severity": 1}, {"id": "desk_clutter", "severity": 1}, {"id": "boxes_parcels", "severity": 1},
    {"id": "bed_unmade", "severity": 1}, {"id": "cables_mess", "severity": 1},
]
AFTER = [{"id": "floor_dust", "severity": 1}]   # rescan after 38 min: only dust left (exposed after moving stuff)
ITEMS = [
    {"id": "i1", "name_th": "หูฟังบลูทูธตัวเก่า", "condition": "good", "last_used_months": 14, "paid_thb": 1290, "duplicate": True},
    {"id": "i2", "name_th": "เสื้อยืดคอนเสิร์ต 2019", "condition": "worn", "last_used_months": 30, "paid_thb": 450, "sentimental": True},
    {"id": "i3", "name_th": "ไดร์เป่าผมพัง", "condition": "broken", "last_used_months": 8, "paid_thb": 690},
    {"id": "i4", "name_th": "กางเกงยีนส์ไซซ์เดิม", "condition": "worn", "last_used_months": 20, "paid_thb": 250},
    {"id": "i5", "name_th": "กระติกน้ำ", "condition": "good", "last_used_months": 1, "paid_thb": 390},
]
LOG = [{"on": f"2026-10-{d:02d}", "kind": "scan"} for d in (15, 16, 17, 18, 19, 20)] + \
      [{"on": "2026-10-18", "kind": "session"}, {"on": "2026-10-18", "kind": "quest", "xp": 40}, {"on": "2026-10-11", "kind": "session"}]
SESSIONS = [
    {"on": "2026-10-04", "before": 48, "after": 82, "minutes": 20, "hotspots": ["clothes_pile", "dishes_cups", "bed_unmade"]},
    {"on": "2026-10-11", "before": 55, "after": 88, "minutes": 15, "hotspots": ["clothes_pile", "trash_floor"]},
    {"on": "2026-10-18", "before": 61, "after": 90, "minutes": 12, "hotspots": ["dishes_cups", "snack_wrappers", "clothes_pile"]},
]
