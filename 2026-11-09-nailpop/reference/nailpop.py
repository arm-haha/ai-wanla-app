"""NailPop deterministic logic (no AI calls). Prices, weights, timings are app-chosen example values — not salon quotes or medical advice."""
import datetime as _dt
import urllib.parse as _up

SHAPES = {
    "square": "เหลี่ยม", "squoval": "เหลี่ยมมน", "round": "กลม", "oval": "วงรี",
    "almond": "อัลมอนด์", "coffin": "บัลเลต์ (คอฟฟิน)", "stiletto": "สติเลตโต้",
}
LENGTHS = {"short": "สั้น", "medium": "กลาง", "long": "ยาว"}
LENGTH_ORDER = ["short", "medium", "long"]
UNDERTONES = {"warm": "โทนอุ่น", "cool": "โทนเย็น", "neutral": "โทนกลาง"}
TECHNIQUES = {"regular": "สีทาธรรมดา", "gel": "สีเจล", "extension": "ต่อเล็บ (PolyGel/อะคริลิก)"}
FINISHES = ["glossy", "matte", "chrome", "cat_eye", "glitter", "pearl"]
OCCASIONS = {
    "office": "ไปทำงาน", "wedding": "งานแต่ง", "songkran": "สงกรานต์",
    "loy_krathong": "ลอยกระทง", "date": "เดต/วาเลนไทน์", "new_year": "ปีใหม่",
}
FINGERS = ["thumb", "index", "middle", "ring", "pinky"]

# Price model (THB, Bangkok baseline) — estimates only
BASE_PRICE = {"regular": (150, 300), "gel": (350, 600), "extension": (800, 1500)}
ART_PRICE = {0: (0, 0), 1: (100, 250), 2: (250, 500), 3: (500, 900)}
LONG_SURCHARGE = (100, 200)
REMOVAL_PRICE = (100, 150)
REGION_MULT = {"bkk": 1.0, "province": 0.85, "tourist": 1.15}

# Fit score weights (sum 100)
W_TONE, W_OCC, W_LEN, W_SHAPE, W_BUDGET = 35, 25, 15, 10, 15

# Aftercare timing (days)
CARE_DAYS = {
    "regular": {"check": 5, "due": 7, "remove_by": 10},
    "gel": {"check": 14, "due": 21, "remove_by": 28},
    "extension": {"check": 14, "due": 21, "remove_by": 35},
}
FREE_GRIDS_PER_DAY = 3
WATERMARK = "Made with NailPop · AI preview, real result depends on your nail tech"
PRICE_DISCLAIMER_TH = "ราคาเป็นช่วงประมาณการ ไม่ใช่ราคาจริงของร้าน ขึ้นกับร้านและพื้นที่"

DESIGNS = [
    {"id": "d01", "name_th": "นู้ดมิลค์กี้มุก", "name_en": "Milky Nude Pearl", "technique": "gel", "finish": "pearl", "art": 1,
     "colors": ["#F3DCCB", "#FFF6EE"], "tones": ["warm", "neutral"], "occasions": ["wedding", "office"], "len_min": "short", "shapes": ["squoval", "oval", "almond"]},
    {"id": "d02", "name_th": "เฟรนช์ทิปคลาสสิก", "name_en": "Classic French Tip", "technique": "gel", "finish": "glossy", "art": 1,
     "colors": ["#F7E1D7", "#FFFFFF"], "tones": ["warm", "cool", "neutral"], "occasions": ["wedding", "office"], "len_min": "medium", "shapes": ["squoval", "almond", "square"]},
    {"id": "d03", "name_th": "แดงเชอร์รี่เงา", "name_en": "Cherry Red Gloss", "technique": "gel", "finish": "glossy", "art": 0,
     "colors": ["#B3122E"], "tones": ["cool", "neutral"], "occasions": ["date", "new_year"], "len_min": "short", "shapes": ["round", "oval", "almond"]},
    {"id": "d04", "name_th": "อิฐส้มเทอร์ราคอตตา", "name_en": "Terracotta Brick", "technique": "gel", "finish": "matte", "art": 0,
     "colors": ["#C0603F"], "tones": ["warm"], "occasions": ["office", "loy_krathong"], "len_min": "short", "shapes": ["squoval", "round"]},
    {"id": "d05", "name_th": "ทองโครมเจ้าสาว", "name_en": "Bridal Gold Chrome", "technique": "gel", "finish": "chrome", "art": 2,
     "colors": ["#E9D3A6", "#C9A24D"], "tones": ["warm"], "occasions": ["wedding", "loy_krathong", "new_year"], "len_min": "medium", "shapes": ["almond", "oval"]},
    {"id": "d06", "name_th": "ลาเวนเดอร์ละมุน", "name_en": "Soft Lavender", "technique": "gel", "finish": "glossy", "art": 0,
     "colors": ["#C9B6E4"], "tones": ["cool"], "occasions": ["office", "date"], "len_min": "short", "shapes": ["round", "squoval", "oval"]},
    {"id": "d07", "name_th": "แคทอายสีกุหลาบ", "name_en": "Rose Cat-Eye", "technique": "gel", "finish": "cat_eye", "art": 2,
     "colors": ["#D99AA5", "#8E4A5C"], "tones": ["cool", "neutral"], "occasions": ["date", "wedding"], "len_min": "medium", "shapes": ["almond", "coffin"]},
    {"id": "d08", "name_th": "ดอกไม้สงกรานต์", "name_en": "Songkran Flowers", "technique": "gel", "finish": "glossy", "art": 2,
     "colors": ["#7FD3E6", "#FFFFFF", "#F6A6C1"], "tones": ["cool", "neutral", "warm"], "occasions": ["songkran"], "len_min": "short", "shapes": ["round", "squoval", "oval"]},
    {"id": "d09", "name_th": "กระทงทองกลิตเตอร์", "name_en": "Krathong Gold Glitter", "technique": "gel", "finish": "glitter", "art": 2,
     "colors": ["#1F2A55", "#D8B35A"], "tones": ["warm", "neutral"], "occasions": ["loy_krathong", "new_year"], "len_min": "medium", "shapes": ["almond", "oval", "coffin"]},
    {"id": "d10", "name_th": "เบจออฟฟิศมินิมอล", "name_en": "Office Minimal Beige", "technique": "regular", "finish": "glossy", "art": 0,
     "colors": ["#D9BFA6"], "tones": ["warm", "neutral"], "occasions": ["office"], "len_min": "short", "shapes": ["square", "squoval", "round"]},
    {"id": "d11", "name_th": "ออมเบรชมพูนม", "name_en": "Milk Pink Ombré", "technique": "gel", "finish": "glossy", "art": 1,
     "colors": ["#F9D5DC", "#FFFFFF"], "tones": ["cool", "neutral"], "occasions": ["wedding", "office", "date"], "len_min": "short", "shapes": ["oval", "almond", "squoval"]},
    {"id": "d12", "name_th": "มะกอกด้านเท่ ๆ", "name_en": "Matte Olive", "technique": "gel", "finish": "matte", "art": 0,
     "colors": ["#6B7B4B"], "tones": ["warm"], "occasions": ["office"], "len_min": "short", "shapes": ["square", "squoval"]},
    {"id": "d13", "name_th": "ซิลเวอร์โครมมิเรอร์", "name_en": "Silver Mirror Chrome", "technique": "extension", "finish": "chrome", "art": 3,
     "colors": ["#C8CDD3", "#8C939B"], "tones": ["cool"], "occasions": ["new_year", "date"], "len_min": "long", "shapes": ["coffin", "stiletto", "almond"]},
    {"id": "d14", "name_th": "พีชคอรัลซัมเมอร์", "name_en": "Peach Coral Summer", "technique": "regular", "finish": "glossy", "art": 1,
     "colors": ["#F59A7E", "#FFE1D2"], "tones": ["warm"], "occasions": ["songkran", "date"], "len_min": "short", "shapes": ["round", "oval", "squoval"]},
]
DESIGN_BY_ID = {d["id"]: d for d in DESIGNS}

SHADES = {
    "warm": {"best": [("นู้ดพีช", "#E8B79A"), ("ส้มอิฐ", "#C0603F"), ("ทองแชมเปญ", "#E9D3A6"), ("แดงอิฐ", "#9E2B25"), ("เขียวมะกอก", "#6B7B4B")],
             "avoid": [("ฟ้าน้ำแข็ง", "#BFE3F2"), ("เงินเย็น", "#C8CDD3")]},
    "cool": {"best": [("ชมพูนม", "#F9D5DC"), ("ลาเวนเดอร์", "#C9B6E4"), ("แดงเชอร์รี่", "#B3122E"), ("เงินโครม", "#C8CDD3"), ("กรมท่า", "#1F2A55")],
             "avoid": [("ส้มอิฐ", "#C0603F"), ("เหลืองมัสตาร์ด", "#D4A017")]},
    "neutral": {"best": [("นู้ดมิลค์กี้", "#F3DCCB"), ("โรสดัสตี้", "#D99AA5"), ("แดงคลาสสิก", "#B3122E"), ("กรมท่า", "#1F2A55"), ("เบจ", "#D9BFA6")],
                "avoid": [("นีออนเขียว", "#39FF14")]},
}

OCCASION_PRESETS = {
    "office": {"tip_th": "สั้น-กลาง สีนู้ด/เบจ ดูสุภาพ ไม่ติดคีย์บอร์ด", "palette": ["#D9BFA6", "#F3DCCB", "#C9B6E4"], "max_length": "medium"},
    "wedding": {"tip_th": "นู้ดมุก เฟรนช์ หรือทองอ่อน ถ่ายรูปคู่ช่อดอกไม้สวย", "palette": ["#F3DCCB", "#FFFFFF", "#E9D3A6"], "max_length": "long"},
    "songkran": {"tip_th": "สีสดใส ฟ้า/ชมพู/ลายดอกไม้ เลือกเจลทนน้ำ", "palette": ["#7FD3E6", "#F6A6C1", "#FFFFFF"], "max_length": "medium"},
    "loy_krathong": {"tip_th": "กรมท่า + ทองกลิตเตอร์ เข้าชุดไทย ใต้แสงเทียน", "palette": ["#1F2A55", "#D8B35A", "#E9D3A6"], "max_length": "long"},
    "date": {"tip_th": "แดงเชอร์รี่ แคทอายกุหลาบ ดูมีเสน่ห์", "palette": ["#B3122E", "#D99AA5"], "max_length": "long"},
    "new_year": {"tip_th": "โครม กลิตเตอร์ เงา ๆ รับแสงปาร์ตี้", "palette": ["#C8CDD3", "#D8B35A", "#B3122E"], "max_length": "long"},
}


# ---------- 1) Hand Snap + nail detection ----------
def classify_shape(taper, corner_round, bed_len_mm, free_edge_mm, width_mm):
    """taper 0..1 (0 straight sides, 1 pointed), corner_round 0..1 (0 sharp, 1 fully round)."""
    if width_mm <= 0:
        raise ValueError("width_mm must be > 0")
    if taper >= 0.75:
        return "stiletto"
    if taper >= 0.45:
        return "almond" if corner_round >= 0.5 else "coffin"
    if corner_round < 0.25:
        return "square"
    if corner_round < 0.6:
        return "squoval"
    return "oval" if (bed_len_mm + free_edge_mm) / width_mm >= 1.4 else "round"


def classify_length(free_edge_mm):
    if free_edge_mm < 1.5:
        return "short"
    if free_edge_mm < 4.0:
        return "medium"
    return "long"


def detect_nail(m):
    shape = classify_shape(m["taper"], m["corner_round"], m["bed_len_mm"], m["free_edge_mm"], m["width_mm"])
    length = classify_length(m["free_edge_mm"])
    return {"finger": m["finger"], "shape": shape, "shape_th": SHAPES[shape], "length": length,
            "length_th": LENGTHS[length], "width_mm": m["width_mm"],
            "total_len_mm": round(m["bed_len_mm"] + m["free_edge_mm"], 1)}


def _majority(vals, order):
    best = max(order, key=lambda v: (vals.count(v), -order.index(v)))
    return best


def scan_quality(lighting, blur, tilt, nails_visible):
    """lighting 0..1 (1 good), blur/tilt 0..1 (0 good). Returns 0-100 + ok + tips."""
    q = 100 * (0.45 * lighting + 0.35 * (1 - blur) + 0.20 * (1 - tilt))
    q = q * min(1.0, nails_visible / 5)
    q = round(max(0, min(100, q)))
    tips = []
    if lighting < 0.5: tips.append("ไปถ่ายใกล้หน้าต่าง แสงกลางวัน")
    if blur > 0.4: tips.append("วางมือนิ่ง ๆ บนโต๊ะ แล้วแตะโฟกัสที่เล็บ")
    if tilt > 0.4: tips.append("ถ่ายจากด้านบนตรง ๆ กางนิ้วเล็กน้อย")
    if nails_visible < 5: tips.append("ให้เห็นเล็บครบ 5 นิ้ว")
    return {"score": q, "ok": q >= 60 and nails_visible >= 4, "tips_th": tips}


def hand_scan(photo):
    nails = [detect_nail(m) for m in photo["nails"]]
    if not nails:
        raise ValueError("no nails detected")
    shape = _majority([n["shape"] for n in nails], list(SHAPES))
    length = _majority([n["length"] for n in nails], LENGTH_ORDER)
    qual = scan_quality(photo["lighting"], photo["blur"], photo["tilt"], len(nails))
    return {"photo_id": photo["id"], "hand": photo["hand"], "nail_count": len(nails), "nails": nails,
            "shape": shape, "shape_th": SHAPES[shape], "length": length, "length_th": LENGTHS[length],
            "quality": qual}


# ---------- 3) Skin-tone match ----------
def undertone(quiz, skin_rgb):
    """quiz: vein green|blue|mixed, jewelry gold|silver|both, sun tan|burn|both. skin_rgb from back-of-hand sample."""
    pts = {"warm": 0, "cool": 0}
    m = {"vein": {"green": "warm", "blue": "cool"}, "jewelry": {"gold": "warm", "silver": "cool"},
         "sun": {"tan": "warm", "burn": "cool"}}
    for k, table in m.items():
        t = table.get(quiz.get(k))
        if t: pts[t] += 1
    r, g, b = skin_rgb
    hint = "warm" if (g - b) >= 45 else ("cool" if (r - g) >= 45 and (g - b) < 35 else "neutral")
    if hint != "neutral":
        pts[hint] += 1
    diff = pts["warm"] - pts["cool"]
    tone = "warm" if diff >= 2 else ("cool" if diff <= -2 else "neutral")
    lum = 0.299 * r + 0.587 * g + 0.114 * b
    depth = "light" if lum >= 200 else ("medium" if lum >= 160 else ("tan" if lum >= 120 else "deep"))
    conf = round(min(1.0, 0.5 + 0.125 * abs(diff)), 3)
    return {"undertone": tone, "undertone_th": UNDERTONES[tone], "depth": depth, "points": pts,
            "rgb_hint": hint, "confidence": conf}


def shade_recommend(tone, depth="medium"):
    if tone not in SHADES:
        raise KeyError(tone)
    t = SHADES[tone]
    best = [{"name_th": n, "hex": h} for n, h in t["best"]]
    if depth in ("tan", "deep"):
        best.sort(key=lambda x: _lum(x["hex"]))  # deeper skin: richer shades first
    return {"undertone": tone, "depth": depth, "best": best,
            "avoid": [{"name_th": n, "hex": h} for n, h in t["avoid"]],
            "note_th": "แนะนำตามโทนผิวแบบคร่าว ๆ เลือกที่ชอบได้เสมอ"}


def _lum(hx):
    r, g, b = int(hx[1:3], 16), int(hx[3:5], 16), int(hx[5:7], 16)
    return 0.299 * r + 0.587 * g + 0.114 * b


# ---------- Price ----------
def _r10(x):
    return int(round(x / 10.0) * 10)


def price_estimate(technique, art, length, region="bkk", removal=False):
    if technique not in BASE_PRICE: raise KeyError(technique)
    if art not in ART_PRICE: raise KeyError(art)
    lo, hi = BASE_PRICE[technique]
    alo, ahi = ART_PRICE[art]
    lo, hi = lo + alo, hi + ahi
    if length == "long" and technique != "extension":
        lo, hi = lo + LONG_SURCHARGE[0], hi + LONG_SURCHARGE[1]
    if removal:
        lo, hi = lo + REMOVAL_PRICE[0], hi + REMOVAL_PRICE[1]
    k = REGION_MULT[region]
    return {"technique": technique, "art_level": art, "length": length, "region": region, "removal": removal,
            "min_thb": _r10(lo * k), "max_thb": _r10(hi * k), "disclaimer_th": PRICE_DISCLAIMER_TH}


# ---------- 2) Try-On Grid 9 ----------
def fit_score(design, scan, tone, occasion=None, budget_thb=None, region="bkk"):
    d = design
    if tone in d["tones"]:
        s_tone = W_TONE
    elif tone == "neutral":
        s_tone = round(W_TONE * 0.7)
    else:
        s_tone = round(W_TONE * 0.3)
    s_occ = W_OCC if occasion in d["occasions"] else (round(W_OCC * 0.6) if occasion is None else round(W_OCC * 0.2))
    s_len = W_LEN if LENGTH_ORDER.index(scan["length"]) >= LENGTH_ORDER.index(d["len_min"]) or d["technique"] == "extension" else round(W_LEN * 0.3)
    s_shape = W_SHAPE if scan["shape"] in d["shapes"] else round(W_SHAPE * 0.4)
    p = price_estimate(d["technique"], d["art"], scan["length"], region)
    if budget_thb is None or p["max_thb"] <= budget_thb:
        s_b = W_BUDGET
    elif p["min_thb"] <= budget_thb:
        s_b = round(W_BUDGET * 0.5)
    else:
        s_b = 0
    return s_tone + s_occ + s_len + s_shape + s_b, p


def _why(d, scan, tone, occasion):
    bits = []
    if tone in d["tones"]: bits.append(f"เข้ากับผิว{UNDERTONES[tone]}")
    if occasion in d["occasions"]: bits.append(f"เหมาะกับ{OCCASIONS[occasion]}")
    if scan["shape"] in d["shapes"]: bits.append(f"สวยกับทรง{SHAPES[scan['shape']]}")
    return " · ".join(bits) or "ลองแนวใหม่ดูก็ได้"


def try_on_grid(scan, tone, occasion=None, budget_thb=None, region="bkk", n=9, designs=None):
    if n < 1 or n > 9: raise ValueError("n must be 1-9")
    pool = designs or DESIGNS
    rows = []
    for d in pool:
        sc, p = fit_score(d, scan, tone, occasion, budget_thb, region)
        rows.append((sc, d, p))
    rows.sort(key=lambda r: (-r[0], r[1]["id"]))
    tiles = []
    for i, (sc, d, p) in enumerate(rows[:n]):
        tiles.append({"rank": i + 1, "slot": f"r{i // 3 + 1}c{i % 3 + 1}", "design_id": d["id"], "name_th": d["name_th"],
                      "colors": list(d["colors"]), "finish": d["finish"], "technique": d["technique"],
                      "fit_score": sc, "price_min_thb": p["min_thb"], "price_max_thb": p["max_thb"],
                      "why_th": _why(d, scan, tone, occasion), "render": "overlay_on_real_nails"})
    return {"photo_id": scan["photo_id"], "undertone": tone, "occasion": occasion, "budget_thb": budget_thb,
            "count": len(tiles), "tiles": tiles, "watermark": WATERMARK}


# ---------- 4) Salon Card ----------
def salon_card(name_th, design_id, scan, region="bkk", removal=False, extra_note_th=""):
    d = DESIGN_BY_ID[design_id]
    p = price_estimate(d["technique"], d["art"], scan["length"], region, removal)
    note = f"ขอทรง{scan['shape_th']} ยาว{scan['length_th']} · {TECHNIQUES[d['technique']]} · ลาย {d['name_th']} ({', '.join(d['colors'])})"
    if extra_note_th: note += f" · {extra_note_th}"
    text = (f"สวัสดีค่ะ ชื่อ{name_th}นะคะ อยากทำเล็บแบบนี้ค่ะ 💅\n{note}\nงบประมาณ ~฿{p['min_thb']:,}–{p['max_thb']:,}\n"
            f"(ภาพจาก NailPop เป็นภาพจำลอง)")
    return {"title_th": "Salon Card", "name_th": name_th, "design_id": d["id"], "design_name_th": d["name_th"],
            "shape": scan["shape"], "shape_th": scan["shape_th"], "length": scan["length"], "length_th": scan["length_th"],
            "technique": d["technique"], "technique_th": TECHNIQUES[d["technique"]], "colors": list(d["colors"]),
            "price_min_thb": p["min_thb"], "price_max_thb": p["max_thb"], "note_th": note, "share_text_th": text,
            "line_share_url": "https://line.me/R/share?text=" + _up.quote(text), "disclaimer_th": PRICE_DISCLAIMER_TH}


# ---------- 5) Friend Vote ----------
def friend_vote(grid, votes):
    """votes: list of design_ids (one per friend). Ties broken by grid rank."""
    ids = [t["design_id"] for t in grid["tiles"]]
    counts = {i: 0 for i in ids}
    invalid = 0
    for v in votes:
        if v in counts: counts[v] += 1
        else: invalid += 1
    total = sum(counts.values())
    if total == 0:
        return {"total": 0, "invalid": invalid, "winner": None, "winner_pct": 0, "results": []}
    winner = max(ids, key=lambda i: (counts[i], -ids.index(i)))
    res = [{"design_id": i, "votes": counts[i], "pct": round(100 * counts[i] / total)} for i in ids if counts[i] > 0]
    res.sort(key=lambda r: (-r["votes"], ids.index(r["design_id"])))
    return {"total": total, "invalid": invalid, "winner": winner, "winner_pct": round(100 * counts[winner] / total), "results": res}


def vote_link(grid_id, top_ids):
    if not 2 <= len(top_ids) <= 4: raise ValueError("pick 2-4 designs to vote")
    return {"grid_id": grid_id, "options": list(top_ids), "url": f"https://nailpop.app/v/{grid_id}?o=" + ",".join(top_ids),
            "expires_hours": 48, "anonymous": True}


# ---------- 6) Nail Diary + reminder ----------
def _d(s):
    return _dt.date.fromisoformat(s)


def care_reminder(done_date, technique):
    if technique not in CARE_DAYS: raise KeyError(technique)
    c = CARE_DAYS[technique]
    d0 = _d(done_date)
    f = lambda k: (d0 + _dt.timedelta(days=c[k])).isoformat()
    msg = {"regular": "สีเริ่มลอก ล้างด้วยน้ำยาแล้วทาใหม่ได้",
           "gel": "เล็บยาวขึ้นจนเห็นโคน ควรถอดเจล/ทำใหม่ที่ร้าน อย่าแกะเอง",
           "extension": "ควรเติมโคน (refill) หรือถอดอย่างถูกวิธีที่ร้าน"}[technique]
    return {"technique": technique, "done_date": done_date, "check_date": f("check"), "due_date": f("due"),
            "remove_by": f("remove_by"), "message_th": msg}


def reminder_status(rem, today):
    t = _d(today)
    if t >= _d(rem["remove_by"]): st = "overdue"
    elif t >= _d(rem["due_date"]): st = "due"
    elif t >= _d(rem["check_date"]): st = "check"
    else: st = "ok"
    return {"status": st, "days_since": (t - _d(rem["done_date"])).days, "days_to_due": (_d(rem["due_date"]) - t).days}


def diary_entry(entry_id, date, design_id, technique, price_thb, rating, salon_th="", photo_on_device=True):
    if not 1 <= rating <= 5: raise ValueError("rating 1-5")
    return {"id": entry_id, "date": date, "design_id": design_id, "technique": technique, "price_thb": price_thb,
            "rating": rating, "salon_th": salon_th, "on_device": photo_on_device,
            "reminder": care_reminder(date, technique)}


def diary_stats(entries):
    if not entries:
        return {"count": 0, "total_thb": 0, "avg_thb": 0, "avg_rating": 0, "favorite_design": None}
    tot = sum(e["price_thb"] for e in entries)
    ids = [e["design_id"] for e in entries]
    fav = max(sorted(set(ids)), key=ids.count)
    return {"count": len(entries), "total_thb": tot, "avg_thb": round(tot / len(entries)),
            "avg_rating": round(sum(e["rating"] for e in entries) / len(entries), 2), "favorite_design": fav}


# ---------- 7) Occasion presets ----------
def occasion_preset(key):
    if key not in OCCASION_PRESETS: raise KeyError(key)
    p = OCCASION_PRESETS[key]
    ids = [d["id"] for d in DESIGNS if key in d["occasions"]]
    return {"key": key, "label_th": OCCASIONS[key], "tip_th": p["tip_th"], "palette": list(p["palette"]),
            "max_length": p["max_length"], "design_ids": ids}


# ---------- 8) DIY mode ----------
DIY_STEPS = {
    "prep": ("ล้างมือ ตะไบทรง ดันหนัง (ไม่ตัดหนังลึก)", 8),
    "base": ("ทาเบสโค้ทบาง ๆ", 3),
    "color": ("ทาสี 2 ชั้นบาง ๆ รอแห้งทีละชั้น", 10),
    "gel_cure": ("อบเครื่อง UV/LED ชั้นละ 30–60 วิ", 6),
    "art": ("ลงลาย/ทิป ด้วยพู่กันเล็กหรือสติกเกอร์", 15),
    "top": ("ทาท็อปโค้ท ปิดปลายเล็บ", 3),
    "cleanup": ("เก็บขอบด้วยสำลีพันไม้ชุบน้ำยา", 3),
}


def diy_guide(design_id):
    d = DESIGN_BY_ID[design_id]
    if d["technique"] == "extension" or d["art"] >= 3:
        return {"design_id": design_id, "diy_ok": False, "steps": [], "total_min": 0,
                "tools_th": [], "note_th": "ลายนี้ต้องใช้ช่างและอุปกรณ์เฉพาะ แนะนำทำที่ร้าน"}
    keys = ["prep", "base", "color"]
    if d["technique"] == "gel": keys.append("gel_cure")
    if d["art"] >= 1: keys.append("art")
    keys += ["top", "cleanup"]
    mult = 1.5 if d["art"] == 2 else 1.0
    steps = []
    for i, k in enumerate(keys):
        t, m = DIY_STEPS[k]
        steps.append({"n": i + 1, "key": k, "text_th": t, "minutes": int(round(m * mult)) if k == "art" else m})
    tools = ["ตะไบ", "เบส/ท็อปโค้ท", "สีตามลาย"] + (["เครื่องอบ UV/LED"] if d["technique"] == "gel" else []) + (["พู่กันเพ้นท์"] if d["art"] >= 1 else [])
    return {"design_id": design_id, "diy_ok": True, "steps": steps, "total_min": sum(s["minutes"] for s in steps),
            "tools_th": tools, "note_th": "มือใหม่ใช้เวลานานกว่านี้ได้ ไม่ต้องรีบ"}


# ---------- Safety ----------
def health_guard(flags):
    """flags: lifting, redness, swelling, pain, discoloration, fungus_suspect (bool). Not a diagnosis."""
    stop = [k for k in ("redness", "swelling", "pain", "fungus_suspect") if flags.get(k)]
    warn = [k for k in ("lifting", "discoloration") if flags.get(k)]
    if stop:
        return {"level": "stop", "flags": stop + warn, "message_th": "พักทำเล็บก่อน และปรึกษาแพทย์/เภสัชกร แอปนี้ไม่ใช่การวินิจฉัย"}
    if warn:
        return {"level": "warn", "flags": warn, "message_th": "แจ้งช่างก่อนทำ ให้ถอดของเดิมอย่างถูกวิธี อย่าแกะเอง"}
    return {"level": "ok", "flags": [], "message_th": "พร้อมทำเล็บ"}


def pipeline_steps(photo):
    steps = ["hand_detect", "nail_segment", "shape_measure"]
    if photo["tilt"] >= 0.25: steps.insert(1, "deskew")
    if photo["lighting"] < 0.5: steps.insert(1, "relight")
    steps += ["undertone_sample", "tryon_render_x9", "fit_rank"]
    return steps


def share_card(name_th, design_id, fit, vote_pct=None):
    d = DESIGN_BY_ID[design_id]
    head = f"{name_th} เลือก {d['name_th']} · Fit {fit}"
    if vote_pct is not None: head += f" · เพื่อนโหวต {vote_pct}%"
    return {"title_th": "NailPop", "headline_th": head, "hook_th": "ถ่ายมือ 1 รูป → ลองเล็บ 9 แบบบนเล็บจริงในไม่กี่วินาที",
            "design_id": design_id, "fit_score": fit, "layout": "before_after_grid", "sizes": ["1080x1350", "1080x1920"],
            "watermark": WATERMARK, "cta_th": "ลองสีเล็บก่อนทำ ลิงก์ในไบโอ"}


def quota(used_today, wanted, pro=False):
    if pro:
        return {"allowed": wanted, "left_after": None, "paywall": False}
    left = max(0, FREE_GRIDS_PER_DAY - used_today)
    allowed = min(left, wanted)
    return {"allowed": allowed, "left_after": left - allowed, "paywall": wanted > allowed}
