"""MoveMate deterministic logic (no AI calls). Costs and times are app-chosen examples — not a mover quote."""
import datetime as _dt
import urllib.parse as _up

ROOMS = {
    "bedroom": {"name_th": "ห้องนอน", "items_th": ["เสื้อผ้า", "ชุดเครื่องนอน", "โคมไฟข้างเตียง", "ของในลิ้นชัก", "ที่ชาร์จและสายไฟ"]},
    "kitchen": {"name_th": "ห้องครัว", "items_th": ["จานชาม", "หม้อกระทะ", "เครื่องปรุง", "เครื่องใช้ไฟฟ้าเล็ก", "ของในตู้เย็น"]},
    "bathroom": {"name_th": "ห้องน้ำ", "items_th": ["ของใช้ในห้องน้ำ", "ผ้าเช็ดตัว", "ยาสามัญ", "อุปกรณ์ซักผ้า"]},
    "living": {"name_th": "ห้องนั่งเล่น", "items_th": ["หนังสือ", "ของตกแต่ง", "อุปกรณ์ทีวี", "สายไฟและปลั๊ก", "โซฟา/โต๊ะ"]},
    "balcony": {"name_th": "ระเบียง", "items_th": ["ต้นไม้", "ราวตากผ้า", "ของเก็บนอกบ้าน"]},
    "misc": {"name_th": "อื่น ๆ", "items_th": ["เอกสารสำคัญ", "ของมีค่า", "กุญแจสำรอง", "กล่องเครื่องมือ"]},
}
VAN_TYPES = {"pickup": 2800, "small_truck": 4200, "mid_truck": 6500}
REGION_VAN = {"bkk": 1.0, "province": 0.85, "tourist": 1.15}
BOX_COST = 15
TAPE_COST = 80
FREE_LABELS_PER_DAY = 3
WATERMARK = "Made with MoveMate · plan only, not a mover quote"
SAFETY_DISCLAIMER_TH = "MoveMate เป็นเช็กลิสต์ย้ายบ้านเบื้องต้น ไม่ใช่บริษัทขนย้าย ราคาเป็นค่าประมาณ ถ่ายรูปในกล่องเก็บในเครื่อง และอย่าวางของมีค่าในกล่องที่ไม่มีป้าย"
PRICE_DISCLAIMER_TH = "ราคาเป็นช่วงประมาณการที่ตั้งเอง ไม่ใช่ใบเสนอราคาจากรถรับจ้างจริง"
UTILITIES = [
    {"key": "electricity", "label_th": "ไฟฟ้า (ชื่อมิเตอร์/การไฟฟ้า)", "hint_th": "แจ้งยกเลิกหรือโอนมิเตอร์ที่อยู่เดิม และเปิดที่อยู่ใหม่"},
    {"key": "water", "label_th": "ประปา", "hint_th": "แจ้งยกเลิก/โอน และบันทึกเลขมิเตอร์วันย้าย"},
    {"key": "internet", "label_th": "เน็ตบ้าน", "hint_th": "นัดช่างย้ายหรือยกเลิกก่อนวันย้ายอย่างน้อย 3–7 วัน"},
    {"key": "parcel", "label_th": "พัสดุและไปรษณีย์", "hint_th": "แจ้งเปลี่ยนที่อยู่และพักของที่คอนโด/รปภ. ชั่วคราว"},
    {"key": "keys", "label_th": "คืนกุญแจที่อยู่เดิม", "hint_th": "นัดคืนกุญแจและถ่ายรูปสภาพห้องก่อนคืน"},
    {"key": "address", "label_th": "อัปเดตที่อยู่", "hint_th": "ธนาคาร กรมธรรม์ ที่ทำงาน และบริการสมัครสมาชิก"},
    {"key": "waste", "label_th": "ขยะและของบริจาค", "hint_th": "แยกของบริจาคก่อนวันย้าย จะได้ไม่ขนของที่ไม่ใช้"},
]

def _code(n):
    return f"B{n:02d}"

def room_checklist(room):
    if room not in ROOMS:
        raise ValueError("unknown room")
    items = [{"key": f"{room}_{i+1}", "text_th": t, "packed": False} for i, t in enumerate(ROOMS[room]["items_th"])]
    return {"room": room, "name_th": ROOMS[room]["name_th"], "items": items, "count": len(items), "packed": 0, "progress": 0}

def apply_checks(checklist, packed_keys):
    items = []
    for it in checklist["items"]:
        items.append({**it, "packed": it["key"] in packed_keys})
    packed = sum(1 for it in items if it["packed"])
    prog = 0 if not items else int(round(100 * packed / len(items)))
    return {"room": checklist["room"], "name_th": checklist["name_th"], "items": items,
            "count": len(items), "packed": packed, "progress": prog}

def make_box(code, room, contents_th, fragile=False, photo_id=None):
    if room not in ROOMS:
        raise ValueError("unknown room")
    if not code or not str(code).startswith("B"):
        raise ValueError("bad box code")
    if not contents_th:
        raise ValueError("empty box")
    qr = f"movemate://box/{code}"
    return {"code": code, "short_th": f"MM-{code}", "room": room, "room_th": ROOMS[room]["name_th"],
            "contents_th": list(contents_th), "item_count": len(contents_th), "fragile": bool(fragile),
            "photo_id": photo_id, "on_device": True, "qr_payload": qr,
            "label_th": f"MM-{code} · {ROOMS[room]['name_th']}" + (" · เปราะบาง" if fragile else "")}

def box_label(box):
    return {"code": box["code"], "short_th": box["short_th"], "label_th": box["label_th"],
            "qr_payload": box["qr_payload"], "room_th": box["room_th"], "fragile": box["fragile"],
            "photo_id": box["photo_id"], "on_device": True, "sizes": ["70x50mm", "90x60mm"]}

def find_item(query, boxes):
    if not query or not query.strip():
        raise ValueError("empty query")
    q = query.strip()
    hits = []
    for b in boxes:
        matched = [c for c in b["contents_th"] if q in c]
        if q.lower() in b["code"].lower() or q in b["short_th"] or matched:
            hits.append({"code": b["code"], "short_th": b["short_th"], "room": b["room"], "room_th": b["room_th"],
                         "matched_th": matched or [q], "fragile": b["fragile"], "photo_id": b["photo_id"]})
    hits.sort(key=lambda h: h["code"])
    return {"query": q, "hits": hits, "count": len(hits)}

def inventory_stats(boxes):
    if not boxes:
        return {"box_count": 0, "item_count": 0, "fragile_count": 0, "rooms": [], "with_photo": 0}
    rooms = sorted({b["room"] for b in boxes})
    return {"box_count": len(boxes), "item_count": sum(b["item_count"] for b in boxes),
            "fragile_count": sum(1 for b in boxes if b["fragile"]), "rooms": rooms,
            "with_photo": sum(1 for b in boxes if b["photo_id"])}

def moving_timeline(move_date, van_hour, rooms):
    if not rooms:
        raise ValueError("no rooms")
    # van_hour is 0-23 int
    if not 5 <= van_hour <= 18:
        raise ValueError("van hour out of range")
    d = _dt.date.fromisoformat(move_date)
    def ts(h, m=0):
        return f"{h:02d}:{m:02d}"
    start_h = max(6, van_hour - 5)
    steps = [
        {"key": "tape", "time": ts(start_h), "text_th": "ปิดกล่องสุดท้าย ติดเทปและป้ายให้ครบ", "owner_th": "คุณ"},
        {"key": "kitchen", "time": ts(start_h + 1), "text_th": "เคลียร์ครัวและของเปราะบางขึ้นรถท้าย ๆ (ขนลงก่อน)", "owner_th": "คุณ"},
        {"key": "rooms", "time": ts(start_h + 2, 30), "text_th": "กล่องห้องนอนและห้องน้ำออกมาที่ทางเดิน", "owner_th": "คุณ"},
        {"key": "van", "time": ts(van_hour), "text_th": "รถกระบะถึงที่อยู่เดิม ตรวจนับกล่องตามป้าย", "owner_th": "คนขับ/คุณ"},
        {"key": "load", "time": ts(van_hour, 30), "text_th": "ขนขึ้นรถ ของหนักลงก่อน ของเปราะบางวางบนสุด", "owner_th": "ทุกคน"},
        {"key": "unload", "time": ts(van_hour + 2), "text_th": "ถึงที่อยู่ใหม่ ขนลงตามห้องที่เขียนบนป้าย", "owner_th": "ทุกคน"},
        {"key": "utils", "time": ts(van_hour + 3, 30), "text_th": "เปิดไฟ-น้ำ เช็กเน็ต และถ่ายรูปมิเตอร์", "owner_th": "คุณ"},
        {"key": "keys", "time": ts(min(20, van_hour + 5)), "text_th": "คืนกุญแจที่อยู่เดิม และถ่ายรูปห้องว่าง", "owner_th": "คุณ"},
    ]
    # if kitchen not in rooms, still keep kitchen step as generic last-boxes? keep all as a default run-of-show
    return {"move_date": move_date, "dow": d.strftime("%A").lower(), "van_hour": van_hour,
            "rooms": list(rooms), "steps": [{"n": i + 1, **s} for i, s in enumerate(steps)], "step_count": len(steps)}

def utility_list(profile):
    rows = []
    missing = []
    for u in UTILITIES:
        val = profile.get(u["key"])
        status = "done" if val else "pending"
        if not val:
            missing.append(u["key"])
        rows.append({"key": u["key"], "label_th": u["label_th"], "hint_th": u["hint_th"],
                     "value_th": val, "status": status})
    return {"items": rows, "count": len(rows), "pending": len(missing), "missing": missing}

def cost_estimate(n_boxes, van_type, region="bkk"):
    if n_boxes < 0:
        raise ValueError("n_boxes < 0")
    if van_type not in VAN_TYPES:
        raise ValueError("unknown van")
    if region not in REGION_VAN:
        raise ValueError("unknown region")
    van = int(round(VAN_TYPES[van_type] * REGION_VAN[region] / 50.0) * 50)
    boxes = n_boxes * BOX_COST
    tape = TAPE_COST if n_boxes else 0
    total = van + boxes + tape
    return {"n_boxes": n_boxes, "van_type": van_type, "region": region,
            "van_thb": van, "boxes_thb": boxes, "tape_thb": tape, "total_thb": total,
            "disclaimer_th": PRICE_DISCLAIMER_TH}

def share_card(name_th, move_date, stats, cost):
    return {"title_th": f"MoveMate — {name_th}",
            "headline_th": f"ย้าย {move_date} · {stats['box_count']} กล่อง",
            "hook_th": "ย้ายบ้านไม่ป่วน", "box_count": stats["box_count"], "item_count": stats["item_count"],
            "total_thb": cost["total_thb"], "layout": "move_card",
            "sizes": ["1080x1350", "1080x1920", "1080x1080"], "watermark": WATERMARK,
            "cta_th": f"{stats['box_count']} กล่อง · ~฿{cost['total_thb']:,} · คอมเมนต์ MOVE รับแพ็กฟรี"}

def quota(used_today, want, pro=False):
    if pro:
        return {"allowed": want, "left_after": None, "paywall": False}
    left = max(0, FREE_LABELS_PER_DAY - used_today)
    allowed = min(want, left)
    return {"allowed": allowed, "left_after": left - allowed, "paywall": allowed < want}

def safety_guard(has_valuables_unlabeled=False, photos_on_device=True):
    if has_valuables_unlabeled:
        return {"level": "stop", "message_th": "ของมีค่ายังไม่มีป้าย อย่าใส่รวมกับกล่องทั่วไป " + SAFETY_DISCLAIMER_TH}
    if not photos_on_device:
        return {"level": "warn", "message_th": "รูปในกล่องควรเก็บในเครื่อง " + SAFETY_DISCLAIMER_TH}
    return {"level": "ok", "message_th": SAFETY_DISCLAIMER_TH}
