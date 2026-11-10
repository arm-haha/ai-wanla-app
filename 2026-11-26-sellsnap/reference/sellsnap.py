"""SellSnap deterministic logic (no AI calls).
Price ranges are app-chosen examples — not live market data and not a marketplace.
"""
FREE_SCANS_PER_DAY = 3
MIN_CONF = 0.6
WATERMARK = "Made with SellSnap · guidance only, not a live price or a marketplace"
SAFETY_DISCLAIMER_TH = "SellSnap เป็นตัวช่วยเขียนโพสต์ขายของมือสอง ไม่ใช่ตลาดกลางและไม่ใช่ราคาตลาดจริง นัดรับในที่สาธารณะ อย่าโอนเงินให้คนแปลกหน้า และตรวจของก่อนส่งมอบ"
PRICE_DISCLAIMER_TH = "ช่วงราคาเป็นค่าตัวอย่างที่ตั้งเอง ไม่ใช่ราคาตลาดจริง ณ วันนี้"

CONDITIONS = {
    "like_new": {"grade": "A", "name_th": "เหมือนใหม่", "priority": 1},
    "good":     {"grade": "B", "name_th": "สภาพดี", "priority": 2},
    "fair":     {"grade": "C", "name_th": "ใช้งานได้ มีรอย", "priority": 3},
    "poor":     {"grade": "D", "name_th": "สภาพพอใช้", "priority": 4},
    "for_parts":{"grade": "E", "name_th": "ขายซาก/อะไหล่", "priority": 5},
}

# Example mid-market ranges in THB, by category and condition. Not live data.
PRICES = {
    ("lamp", "like_new"): (700, 1200, 900),
    ("lamp", "good"): (450, 750, 600),
    ("lamp", "fair"): (250, 450, 350),
    ("lamp", "poor"): (120, 250, 180),
    ("lamp", "for_parts"): (50, 120, 80),
    ("chair", "like_new"): (900, 1800, 1300),
    ("chair", "good"): (500, 900, 700),
    ("chair", "fair"): (250, 500, 350),
    ("chair", "poor"): (100, 250, 160),
    ("chair", "for_parts"): (50, 100, 70),
    ("bag", "like_new"): (800, 2000, 1200),
    ("bag", "good"): (400, 900, 600),
    ("bag", "fair"): (200, 400, 300),
    ("bag", "poor"): (80, 200, 120),
    ("bag", "for_parts"): (40, 80, 50),
    ("electronics", "like_new"): (1500, 4000, 2500),
    ("electronics", "good"): (800, 2000, 1300),
    ("electronics", "fair"): (400, 800, 600),
    ("electronics", "poor"): (150, 400, 250),
    ("electronics", "for_parts"): (50, 150, 90),
    ("clothes", "like_new"): (250, 700, 400),
    ("clothes", "good"): (120, 350, 220),
    ("clothes", "fair"): (60, 150, 100),
    ("clothes", "poor"): (30, 80, 50),
    ("clothes", "for_parts"): (10, 30, 20),
    ("kitchen", "like_new"): (300, 800, 500),
    ("kitchen", "good"): (150, 400, 250),
    ("kitchen", "fair"): (80, 180, 120),
    ("kitchen", "poor"): (30, 80, 50),
    ("kitchen", "for_parts"): (10, 30, 20),
    ("book", "like_new"): (80, 250, 150),
    ("book", "good"): (40, 120, 80),
    ("book", "fair"): (20, 60, 40),
    ("book", "poor"): (10, 25, 15),
    ("book", "for_parts"): (5, 10, 8),
    ("toy", "like_new"): (200, 600, 350),
    ("toy", "good"): (100, 300, 180),
    ("toy", "fair"): (50, 120, 80),
    ("toy", "poor"): (20, 60, 35),
    ("toy", "for_parts"): (10, 25, 15),
    ("other", "like_new"): (300, 900, 500),
    ("other", "good"): (150, 500, 300),
    ("other", "fair"): (80, 250, 150),
    ("other", "poor"): (30, 100, 60),
    ("other", "for_parts"): (10, 40, 20),
}

CATEGORIES = {
    "lamp": {"id": "c01", "name_th": "โคมไฟ/ส่องสว่าง"},
    "chair": {"id": "c02", "name_th": "เก้าอี้/เฟอร์นิเจอร์"},
    "bag": {"id": "c03", "name_th": "กระเป๋า"},
    "electronics": {"id": "c04", "name_th": "อิเล็กทรอนิกส์"},
    "clothes": {"id": "c05", "name_th": "เสื้อผ้า"},
    "kitchen": {"id": "c06", "name_th": "ของใช้ในครัว"},
    "book": {"id": "c07", "name_th": "หนังสือ"},
    "toy": {"id": "c08", "name_th": "ของเล่น"},
    "other": {"id": "c09", "name_th": "อื่น ๆ"},
}

REPLY_TEMPLATES = {
    "bargain": {
        "id": "r01", "name_th": "ต่อราคา",
        "text_th": "ขอบคุณที่ทักนะคะ ลดให้ได้ที่ ฿{ask} ถ้ามารับเองวันนี้",
    },
    "meetup": {
        "id": "r02", "name_th": "นัดรับ",
        "text_th": "นัดรับที่ที่สาธารณะได้ค่ะ ดูของก่อนได้ โอนหรือจ่ายสดตอนรับ",
    },
    "reserved": {
        "id": "r03", "name_th": "ขอคนนี้ไว้",
        "text_th": "ขอคนนี้ไว้ก่อนนะคะ รอบโอน/มารับภายในเวลาที่นัด ถ้าไม่มาจะเปิดขายต่อ",
    },
    "sold": {
        "id": "r04", "name_th": "ขายแล้ว",
        "text_th": "ขายแล้วค่ะ ขอบคุณที่สนใจ ไว้รอบหน้านะคะ",
    },
    "scam_guard": {
        "id": "r05", "name_th": "กันมิจฉาชีพ",
        "text_th": "ไม่ส่งของก่อนโอน และไม่คลิกลิงก์แปลก นัดรับในที่สาธารณะมีคนพลุกพล่านค่ะ",
    },
}

PHOTO_TIP_BANK = {
    "glare": "แสงสะท้อนบนของเยอะ ย้ายออกจากไฟตรง ๆ หรือถ่ายข้างหน้าต่าง",
    "blur": "ภาพเบลอ วางของนิ่งแล้วถ่ายใหม่ในที่สว่าง",
    "crop": "ของถูกครอป ถ่ายให้เห็นทั้งชิ้นและพื้นเรียบด้านหลัง",
    "no_item": "ยังไม่เจอสินค้าในรูป วางของบนพื้นเรียบแล้วถ่ายใหม่",
    "need_defect": "เพิ่มรูปโชว์ตำหนิใกล้ ๆ จะได้ไม่ต้องถกกันตอนนัดรับ",
    "need_scale": "วางของข้างสิ่งที่บอกขนาด เช่น ขวดน้ำ หรือไม้บรรทัด",
    "need_all": "ถ่ายอย่างน้อย 3 มุม: ด้านหน้า ด้านข้าง และจุดที่ใช้แล้ว",
}


def scan_quality(glare, blur, crop, n_dets):
    for v in (glare, blur, crop):
        if not 0 <= v <= 1:
            raise ValueError("glare/blur/crop must be 0..1")
    score = round(100 * (1 - (0.35 * glare + 0.40 * blur + 0.25 * crop)))
    if n_dets == 0:
        score = max(0, score - 30)
    tips = []
    if glare > 0.5:
        tips.append(PHOTO_TIP_BANK["glare"])
    if blur > 0.4:
        tips.append(PHOTO_TIP_BANK["blur"])
    if crop > 0.45:
        tips.append(PHOTO_TIP_BANK["crop"])
    if n_dets == 0:
        tips.append(PHOTO_TIP_BANK["no_item"])
    return {"score": score, "ok": score >= 60 and n_dets >= 1, "tips_th": tips}


def _val(dets, key, default=None):
    for d in dets:
        if d.get("key") == key and d.get("confidence", 0) >= MIN_CONF:
            return d["value"]
    return default


def parse_item(shot):
    q = scan_quality(shot["glare"], shot["blur"], shot["crop"], len(shot["detections"]))
    category = _val(shot["detections"], "category")
    color_th = _val(shot["detections"], "color_th")
    item_th = _val(shot["detections"], "item_th")
    brand_th = _val(shot["detections"], "brand_th")
    defect_th = _val(shot["detections"], "defect_th")
    if category not in CATEGORIES:
        return {"shot_id": shot["id"], "quality": q, "ok": False, "category": category,
                "item_th": item_th, "color_th": color_th, "brand_th": brand_th, "defect_th": defect_th,
                "message_th": "อ่านหมวดสินค้าไม่ชัด ลองถ่ายใหม่หรือเลือกหมวดเอง"}
    return {"shot_id": shot["id"], "quality": q, "ok": q["ok"], "category": category,
            "item_th": item_th, "color_th": color_th, "brand_th": brand_th, "defect_th": defect_th,
            "category_name_th": CATEGORIES[category]["name_th"],
            "message_th": f"เจอ{item_th or CATEGORIES[category]['name_th']}" + (f"สี{color_th}" if color_th else "")}


def condition_grade(shot, item=None):
    key = _val(shot["detections"], "condition")
    if key not in CONDITIONS:
        # infer from wear 0-1 if present
        wear = _val(shot["detections"], "wear")
        if wear is None:
            return {"ok": False, "condition": None, "grade": None, "name_th": None,
                    "message_th": "ยังให้เกรดสภาพไม่ได้ ลองถ่ายจุดที่ใช้แล้วหรือเลือกสภาพเอง"}
        if wear <= 0.15:
            key = "like_new"
        elif wear <= 0.40:
            key = "good"
        elif wear <= 0.65:
            key = "fair"
        elif wear <= 0.85:
            key = "poor"
        else:
            key = "for_parts"
    c = CONDITIONS[key]
    return {"ok": True, "condition": key, "grade": c["grade"], "name_th": c["name_th"],
            "message_th": f"สภาพ {c['grade']} {c['name_th']}"}


def price_range(item, cond):
    if not item.get("ok"):
        raise ValueError("item not ok")
    if not cond.get("ok"):
        raise ValueError("condition not ok")
    key = (item["category"], cond["condition"])
    if key not in PRICES:
        raise ValueError("unknown price key")
    lo, hi, mid = PRICES[key]
    return {"min_thb": lo, "max_thb": hi, "mid_thb": mid,
            "category": item["category"], "condition": cond["condition"], "grade": cond["grade"],
            "headline_th": f"ราคาแนะนำ ฿{lo:,}–{hi:,} · กลาง ฿{mid:,}".replace(",", ""),
            "disclaimer_th": PRICE_DISCLAIMER_TH}


def listing(item, cond, price, extra_note=None):
    if not item.get("ok") or not cond.get("ok"):
        raise ValueError("need item and condition")
    name = item.get("item_th") or item["category_name_th"]
    color = f"สี{item['color_th']}" if item.get("color_th") else ""
    title = f"{name}{(' ' + color) if color else ''} {cond['name_th']}".strip()
    if len(title) > 60:
        title = title[:57] + "…"
    bits = [f"{name}{(' ' + color) if color else ''} {cond['name_th']}"]
    if item.get("brand_th"):
        bits.append(f"ยี่ห้อ {item['brand_th']}")
    if item.get("defect_th"):
        bits.append(f"ตำหนิ: {item['defect_th']}")
    bits.append(f"ราคาเสนอ ฿{price['mid_thb']} (ช่วงประมาณ ฿{price['min_thb']}–{price['max_thb']})")
    if extra_note:
        bits.append(extra_note)
    bits.append("นัดรับได้ ของจริงตามรูป")
    desc = " ".join(bits)
    return {"title_th": title, "description_th": desc, "item_th": name,
            "condition": cond["condition"], "grade": cond["grade"],
            "min_thb": price["min_thb"], "max_thb": price["max_thb"], "ask_thb": price["mid_thb"],
            "headline_th": title}


def photo_tips(shot, has_defect_shot=False, has_scale_shot=False, n_angles=1):
    q = scan_quality(shot["glare"], shot["blur"], shot["crop"], len(shot["detections"]))
    tips = list(q["tips_th"])
    keys = []
    if q["tips_th"]:
        keys += ["quality"] * 0  # quality tips already included
        if shot["glare"] > 0.5:
            keys.append("glare")
        if shot["blur"] > 0.4:
            keys.append("blur")
        if shot["crop"] > 0.45 or len(shot["detections"]) == 0:
            keys.append("crop" if shot["crop"] > 0.45 else "no_item")
    if not has_defect_shot:
        keys.append("need_defect"); tips.append(PHOTO_TIP_BANK["need_defect"])
    if not has_scale_shot:
        keys.append("need_scale"); tips.append(PHOTO_TIP_BANK["need_scale"])
    if n_angles < 3:
        keys.append("need_all"); tips.append(PHOTO_TIP_BANK["need_all"])
    return {"keys": keys, "tips_th": tips, "count": len(tips),
            "headline_th": f"{len(tips)} ข้อเพื่อให้รูปขายดีขึ้น" if tips else "รูปครบ มุมครบ ตำหนิครบ"}


def reply_templates(price, kinds=None):
    ask = int(round(price["mid_thb"] * 0.95 / 10) * 10)  # slight bargain, nearest 10
    use = kinds or list(REPLY_TEMPLATES)
    out = []
    for k in use:
        if k not in REPLY_TEMPLATES:
            raise ValueError("unknown template " + k)
        t = REPLY_TEMPLATES[k]
        out.append({"id": t["id"], "key": k, "name_th": t["name_th"],
                    "text_th": t["text_th"].format(ask=ask)})
    return {"ask_thb": ask, "templates": out, "count": len(out)}


def sold_log(listings, action, listing_id, sold_thb=None, date=None):
    """listings is a list of dicts with id, status (for_sale|reserved|sold), ask_thb, sold_thb, date."""
    found = None
    for row in listings:
        if row["id"] == listing_id:
            found = row
            break
    if found is None:
        raise ValueError("unknown listing " + listing_id)
    if action == "reserve":
        if found["status"] == "sold":
            raise ValueError("already sold")
        found = dict(found, status="reserved")
    elif action == "sell":
        if sold_thb is None or sold_thb < 0:
            raise ValueError("sold_thb required")
        found = dict(found, status="sold", sold_thb=sold_thb, date=date)
    elif action == "relist":
        found = dict(found, status="for_sale", sold_thb=None)
    else:
        raise ValueError("unknown action " + action)
    rows = [found if r["id"] == listing_id else r for r in listings]
    sold = [r for r in rows if r["status"] == "sold"]
    total = sum(r.get("sold_thb") or 0 for r in sold)
    return {"rows": rows, "sold_count": len(sold), "open_count": sum(1 for r in rows if r["status"] == "for_sale"),
            "reserved_count": sum(1 for r in rows if r["status"] == "reserved"),
            "total_sold_thb": total,
            "headline_th": f"ขายแล้ว {len(sold)} ชิ้น รวม ฿{total}"}


def share_card(name_th, listing, price):
    return {"title_th": f"SellSnap — {name_th}",
            "headline_th": listing["title_th"],
            "hook_th": "ถ่ายของมือสอง ได้โพสต์ขายพร้อมราคา",
            "min_thb": price["min_thb"], "max_thb": price["max_thb"], "ask_thb": listing["ask_thb"],
            "grade": listing["grade"],
            "layout": "listing_card", "sizes": ["1080x1350", "1080x1920", "1080x1080"],
            "watermark": WATERMARK, "cta_th": "คอมเมนต์ SELL รับแพ็กฟรี"}


def quota(used_today, want, pro=False):
    if pro:
        return {"allowed": want, "left_after": None, "paywall": False}
    left = max(0, FREE_SCANS_PER_DAY - used_today)
    allowed = min(want, left)
    return {"allowed": allowed, "left_after": left - allowed, "paywall": allowed < want}


def safety_guard(wants_prepay=False, public_meetup=True):
    if wants_prepay and not public_meetup:
        return {"level": "stop", "message_th": "อย่าโอนเงินหรือส่งของล่วงหน้าให้นัดในที่ลับ " + SAFETY_DISCLAIMER_TH}
    if wants_prepay:
        return {"level": "warn", "message_th": "ระวังคนขอให้โอนก่อนส่งของ " + SAFETY_DISCLAIMER_TH}
    if not public_meetup:
        return {"level": "warn", "message_th": "นัดรับในที่สาธารณะจะปลอดภัยกว่า " + SAFETY_DISCLAIMER_TH}
    return {"level": "ok", "message_th": SAFETY_DISCLAIMER_TH}
