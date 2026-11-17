"""WrapRide reference logic — deterministic, no network. All prices are ESTIMATES (example ranges set by the pack), not quotes.
Legal text is general guidance only; always confirm current rules with the Department of Land Transport (กรมการขนส่งทางบก) and your insurer."""
import datetime as _dt

VEHICLES = {  # wrap_m2 = approx. wrappable surface; wrap/paint/rim = (low, high) THB example ranges for gloss full wrap / full respray / rim set
    "eco_car":   {"th": "อีโคคาร์",        "kind": "car",  "wrap_m2": 14, "wrap": (15000, 30000), "paint": (18000, 45000), "rim_in": 15, "rims": 4},
    "sedan":     {"th": "รถเก๋ง",          "kind": "car",  "wrap_m2": 17, "wrap": (20000, 40000), "paint": (25000, 60000), "rim_in": 17, "rims": 4},
    "suv":       {"th": "SUV / PPV",       "kind": "car",  "wrap_m2": 21, "wrap": (25000, 50000), "paint": (30000, 75000), "rim_in": 18, "rims": 4},
    "pickup":    {"th": "กระบะ",           "kind": "car",  "wrap_m2": 20, "wrap": (22000, 45000), "paint": (28000, 70000), "rim_in": 17, "rims": 4},
    "big_bike":  {"th": "บิ๊กไบค์",         "kind": "bike", "wrap_m2": 3,  "wrap": (5000, 12000),  "paint": (8000, 20000),  "rim_in": 17, "rims": 2},
    "scooter":   {"th": "สกู๊ตเตอร์ / ออโต้", "kind": "bike", "wrap_m2": 2,  "wrap": (2500, 6000),   "paint": (3500, 9000),   "rim_in": 14, "rims": 2},
}
FINISHES = {  # price multiplier vs gloss, highlight mix (white), shadow mix (black)
    "gloss":       {"th": "เงา",        "x": 1.0,  "hi": 0.45, "sh": 0.35},
    "satin":       {"th": "กึ่งเงา",     "x": 1.1,  "hi": 0.25, "sh": 0.28},
    "matte":       {"th": "ด้าน",       "x": 1.15, "hi": 0.12, "sh": 0.20},
    "chrome":      {"th": "โครเมียม",   "x": 2.2,  "hi": 0.70, "sh": 0.55},
    "color_shift": {"th": "เปลี่ยนสีตามมุม", "x": 1.5,  "hi": 0.40, "sh": 0.35},
}
COLORS = {
    "mint_green":     {"th": "เขียวมิ้นต์",     "hex": "#7FD1AE", "family": "green"},
    "army_green":     {"th": "เขียวทหาร",      "hex": "#4B5320", "family": "green"},
    "midnight_blue":  {"th": "น้ำเงินเที่ยงคืน", "hex": "#1E2A4A", "family": "blue"},
    "sky_blue":       {"th": "ฟ้าพาสเทล",      "hex": "#7EC8F2", "family": "blue"},
    "cement_grey":    {"th": "เทาซีเมนต์",     "hex": "#8A8D8F", "family": "grey"},
    "deep_black":     {"th": "ดำ",            "hex": "#1B1B1B", "family": "black"},
    "pearl_white":    {"th": "ขาวมุก",         "hex": "#F2F0EA", "family": "white"},
    "candy_red":      {"th": "แดงแคนดี้",      "hex": "#C8102E", "family": "red"},
    "sunset_orange":  {"th": "ส้มซันเซ็ต",     "hex": "#FF7A1A", "family": "orange"},
    "lavender":       {"th": "ม่วงลาเวนเดอร์",  "hex": "#B9A6E8", "family": "purple"},
    "hot_pink":       {"th": "ชมพูช็อก",       "hex": "#FF4FA3", "family": "pink"},
    "champagne_gold": {"th": "ทองแชมเปญ",     "hex": "#D4B483", "family": "gold"},
}
COVERAGE = {  # share of full-wrap price/area
    "full": {"th": "ทั้งคัน", "x": 1.0}, "two_tone": {"th": "ทูโทน (ทั้งคัน + หลังคา/กระจกมองข้างสีคู่)", "x": 1.1},
    "roof": {"th": "หลังคา", "x": 0.15}, "hood": {"th": "ฝากระโปรงหน้า", "x": 0.12}, "stripes": {"th": "คาดลาย", "x": 0.10},
}
RIM_STYLES = {"multi_spoke": "ก้านถี่", "five_spoke": "5 ก้าน", "mesh": "ลายตาข่าย", "deep_dish": "ขอบลึก"}
RIM_COLORS = {"black": {"th": "ดำ", "hex": "#151515"}, "gunmetal": {"th": "เทากันเมทัล", "hex": "#3B3F45"}, "silver": {"th": "เงิน", "hex": "#C9CDD2"},
              "bronze": {"th": "บรอนซ์", "hex": "#8C6A3F"}, "gold": {"th": "ทอง", "hex": "#C9A227"}}
RIM_PRICE_PER_IN = {"car": (150, 450), "bike": (60, 200)}  # THB per wheel per inch (example range)
STICKERS = {"side_stripe": "เส้นข้างตัวรถ", "hood_stripes": "แถบคู่ฝากระโปรง", "pinstripe": "เส้นพินสไตรป์", "kanok": "ลายกนกไทย",
            "checker": "ลายธงตาหมากรุก", "race_number": "เบอร์แข่ง (ตัวเลขของคุณเอง)"}
STICKER_BAHT = {"car": 1500, "bike": 600}
FORBIDDEN_AREAS = ("headlight", "taillight", "plate", "windscreen")
DISCLAIMER = "ภาพเป็นภาพจำลอง สีจริงต่างตามแสงและเกรดฟิล์ม ราคาเป็นช่วงประมาณ ไม่ใช่ใบเสนอราคา"
LEGAL_NOTE = "ข้อมูลทั่วไป ไม่ใช่คำแนะนำทางกฎหมาย ตรวจขั้นตอนล่าสุดกับสำนักงานขนส่งและบริษัทประกันก่อนทำ"


def _rng(x, lo, hi, name):
    if isinstance(x, bool) or not isinstance(x, (int, float)) or x < lo or x > hi:
        raise ValueError(f"{name} out of range")


def _get(d, k, name):
    if k not in d: raise ValueError(f"unknown {name} {k}")
    return d[k]


def _mix(hexc, other, t):
    a = [int(hexc[i:i + 2], 16) for i in (1, 3, 5)]; b = [int(other[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * t):02X}" for x, y in zip(a, b))


def scan_quality(glare, blur, crop):
    for v, n in ((glare, "glare"), (blur, "blur"), (crop, "crop")):
        _rng(v, 0, 1, n)
    score = round(100 - glare * 35 - blur * 40 - crop * 25)
    tips = []
    if glare > 0.3: tips.append("แสงสะท้อนบนตัวรถเยอะ ถ่ายในร่มหรือช่วงเช้า/เย็น")
    if blur > 0.3: tips.append("ภาพเบลอ ถือนิ่ง ๆ แล้วถ่ายใหม่")
    if crop > 0.3: tips.append("ถอยออกให้เห็นรถทั้งคัน มุมเฉียงหน้า 45° ดีที่สุด")
    return {"score": max(0, score), "ok": score >= 70, "tips_th": tips}


def vehicle_scan(photo):
    return {"photo_id": photo["id"], "quality": scan_quality(photo["glare"], photo["blur"], photo["crop"])}


def finish_swatch(color, finish):
    """Deterministic preview swatch: base / highlight / shadow (+ shift colour for color_shift)."""
    c = _get(COLORS, color, "color"); f = _get(FINISHES, finish, "finish")
    out = {"color": color, "finish": finish, "base_hex": c["hex"], "highlight_hex": _mix(c["hex"], "#FFFFFF", f["hi"]),
           "shadow_hex": _mix(c["hex"], "#000000", f["sh"]), "label_th": f"{c['th']} {f['th']}"}
    if finish == "chrome": out["highlight_hex"] = _mix(c["hex"], "#FFFFFF", 0.7)
    if finish == "color_shift": out["shift_hex"] = _mix(c["hex"], "#7A3CFF", 0.55)
    return out


def wrap_spec(vehicle, color, finish, coverage="full", accent_color=None, original_family="white"):
    """Hook: photo → recoloured wrap. Returns the image-edit prompt + swatch."""
    v = _get(VEHICLES, vehicle, "vehicle"); _get(COVERAGE, coverage, "coverage"); sw = finish_swatch(color, finish)
    if coverage == "two_tone" and accent_color is None: accent_color = "deep_black"
    if accent_color is not None: _get(COLORS, accent_color, "accent_color")
    area = {"full": "entire body panels", "two_tone": "body panels, with roof and mirror caps in the accent colour", "roof": "roof only",
            "hood": "hood/bonnet only", "stripes": "two racing stripes over hood and roof"}[coverage]
    acc = f", accent {accent_color.replace('_', ' ')} gloss" if accent_color else ""
    prompt = (f"same {v['kind']} from the photo, same angle and background; {area} wrapped in {color.replace('_', ' ')} {finish.replace('_', ' ')} vinyl{acc}; "
              "keep headlights, taillights, windows and licence plate area unchanged and uncovered; plate blurred; photorealistic 4:5; no people, no logos, no brand badges added")
    main_change = coverage in ("full", "two_tone") and COLORS[color]["family"] != original_family
    title = f"{v['th']} {COLORS[color]['th']} {FINISHES[finish]['th']}" + (f" + {COLORS[accent_color]['th']}" if accent_color else "")
    return {"vehicle": vehicle, "color": color, "finish": finish, "coverage": coverage, "accent_color": accent_color, "swatch": sw,
            "main_color_change": main_change, "image_prompt": prompt, "title_th": title, "disclaimer_th": DISCLAIMER}


def rim_sticker_spec(vehicle, rim_style=None, rim_color=None, stickers=(), areas=()):
    v = _get(VEHICLES, vehicle, "vehicle")
    if rim_style is not None: _get(RIM_STYLES, rim_style, "rim_style")
    if rim_color is not None: _get(RIM_COLORS, rim_color, "rim_color")
    for s in stickers: _get(STICKERS, s, "sticker")
    if len(stickers) > 3: raise ValueError("max 3 stickers")
    blocked = [a for a in areas if a in FORBIDDEN_AREAS]
    parts = []
    if rim_style: parts.append(f"{v['rim_in']}-inch {rim_style.replace('_', ' ')} rims in {rim_color or 'black'}")
    if stickers: parts.append("decals: " + ", ".join(s.replace("_", " ") for s in stickers))
    return {"vehicle": vehicle, "rim_style": rim_style, "rim_color": rim_color, "rim_inch": v["rim_in"], "stickers": list(stickers),
            "blocked_areas": blocked, "ok": not blocked, "image_prompt": "same vehicle and angle; " + ("; ".join(parts) or "no change") +
            "; nothing over lights, windows or licence plate; no brand logos",
            "note_th": "ห้ามติดทับไฟหน้า/ไฟท้าย/ป้ายทะเบียน/กระจกหน้า" if blocked else "ตำแหน่งติดตั้งปลอดภัย"}


def price_check(vehicle, job, finish="gloss", coverage="full", quote_baht=None, stickers=0):
    """job ∈ wrap | paint | rims | stickers. Returns an ESTIMATE range + verdict on an optional shop quote."""
    v = _get(VEHICLES, vehicle, "vehicle")
    if job == "wrap":
        f = _get(FINISHES, finish, "finish")["x"]; c = _get(COVERAGE, coverage, "coverage")["x"]
        lo, hi = v["wrap"][0] * f * c, v["wrap"][1] * f * c
    elif job == "paint":
        c = _get(COVERAGE, coverage, "coverage")["x"]; lo, hi = v["paint"][0] * c, v["paint"][1] * c
    elif job == "rims":
        a, b = RIM_PRICE_PER_IN[v["kind"]]; lo, hi = a * v["rim_in"] * v["rims"], b * v["rim_in"] * v["rims"]
    elif job == "stickers":
        _rng(stickers, 1, 3, "stickers"); lo, hi = STICKER_BAHT[v["kind"]] * stickers * 0.6, STICKER_BAHT[v["kind"]] * stickers * 1.6
    else:
        raise ValueError("job")
    lo, hi = int(round(lo, -2)), int(round(hi, -2))
    out = {"vehicle": vehicle, "job": job, "low_baht": lo, "high_baht": hi, "quote_baht": quote_baht, "verdict": "no_quote",
           "verdict_th": f"ช่วงราคาประมาณ ฿{lo:,}–฿{hi:,}", "disclaimer_th": "ช่วงราคาตัวอย่างโดยประมาณ ราคาจริงขึ้นกับร้าน เกรดฟิล์ม และสภาพสีเดิม"}
    if quote_baht is not None:
        _rng(quote_baht, 1, 5_000_000, "quote_baht")
        if quote_baht < lo * 0.8: verdict, th = "suspicious_low", "ถูกผิดปกติ ถามเกรดฟิล์ม การรับประกัน และการลอกออกให้ชัด"
        elif quote_baht <= hi: verdict, th = "fair", "อยู่ในช่วงราคาประมาณ สมเหตุสมผล"
        elif quote_baht <= hi * 1.15: verdict, th = "high", "สูงกว่าช่วงนิดหน่อย ลองขอใบเสนอราคาเทียบ"
        else: verdict, th = "too_high", "แพงกว่าช่วงปกติมาก ขอใบเสนอราคาเทียบ 2–3 ร้าน"
        out.update(verdict=verdict, verdict_th=f"฿{quote_baht:,} → {th}")
    return out


def shop_brief(person, spec, rims=None, price=None, notes_th=""):
    v = VEHICLES[spec["vehicle"]]
    lines = [f"รถ: {v['th']}", f"งาน: wrap {COVERAGE[spec['coverage']]['th']}", f"สี: {COLORS[spec['color']]['th']} ({spec['swatch']['base_hex']}) ผิว{FINISHES[spec['finish']]['th']}"]
    if spec["accent_color"]: lines.append(f"สีคู่: {COLORS[spec['accent_color']]['th']} ({COLORS[spec['accent_color']]['hex']})")
    if rims and rims["rim_style"]: lines.append(f"ล้อ: {rims['rim_inch']}\" {RIM_STYLES[rims['rim_style']]} สี{RIM_COLORS[rims['rim_color'] or 'black']['th']}")
    if rims and rims["stickers"]: lines.append("สติกเกอร์: " + ", ".join(STICKERS[s] for s in rims["stickers"]))
    if price: lines.append(f"งบที่ตั้งไว้: ฿{price['low_baht']:,}–฿{price['high_baht']:,}")
    lines += ["ขอ: เกรด/ยี่ห้อฟิล์ม, ระยะรับประกัน, ระยะเวลาทำ, ค่าลอกออก", "ไม่ติดทับไฟ ป้ายทะเบียน และกระจก"]
    if notes_th: lines.append(f"หมายเหตุ: {notes_th}")
    return {"to_th": "ร้านทำ wrap", "from_name_th": person["name_th"], "lines_th": lines, "text_th": "\n".join(lines),
            "attach": ["before_photo", "mockup_4x5", "swatch"], "cta_th": "คัดลอกส่ง LINE ร้านได้เลย"}


def legal_check(spec):
    """General reminders only — no specific fees/deadlines asserted."""
    items = []
    if spec["main_color_change"]:
        items.append({"code": "dlt_color", "level": "action", "text_th": "เปลี่ยนสีหลักของรถ โดยทั่วไปต้องแจ้งเปลี่ยนสีในเล่มทะเบียนกับกรมการขนส่งทางบก ตรวจเอกสาร ค่าธรรมเนียม และกำหนดเวลาล่าสุดกับสำนักงานขนส่งก่อนทำ"})
        items.append({"code": "insurance", "level": "action", "text_th": "แจ้งบริษัทประกันเรื่องเปลี่ยนสี/ติดฟิล์ม เพื่อไม่ให้มีปัญหาตอนเคลม"})
    else:
        items.append({"code": "dlt_color", "level": "info", "text_th": "ตกแต่งบางส่วน สีหลักไม่เปลี่ยน มักไม่ต้องแก้เล่ม แต่ถ้าไม่แน่ใจสอบถามสำนักงานขนส่ง"})
    if spec["finish"] == "chrome" and spec["coverage"] in ("full", "two_tone"):
        items.append({"code": "reflective", "level": "warn", "text_th": "ผิวโครเมียม/สะท้อนแสงมากอาจแยงตาผู้อื่นและอาจติดข้อจำกัด ตรวจกับขนส่งก่อนทำทั้งคัน"})
    items.append({"code": "lights_plate", "level": "info", "text_th": "ห้ามติดฟิล์มทับไฟหน้า ไฟท้าย ไฟเลี้ยว และป้ายทะเบียน"})
    lv = "action" if any(i["level"] == "action" for i in items) else ("warn" if any(i["level"] == "warn" for i in items) else "info")
    return {"level": lv, "items": items, "note_th": LEGAL_NOTE}


def reel_plan(spec, seconds=20):
    _rng(seconds, 15, 30, "seconds")
    s = seconds
    shots = [(0, 3, "before", "ภาพรถเดิม + ข้อความ 'เบื่อสีรถเดิม?'"), (3, round(s * 0.35), "scan", "สแกนรถ เส้นเลเซอร์วิ่งผ่าน"),
             (round(s * 0.35), round(s * 0.7), "swipe", f"ปัดเปลี่ยนสี → {spec['title_th']}"), (round(s * 0.7), s - 3, "compare", "สไลเดอร์ ก่อน/หลัง + ราคาประมาณ"),
             (s - 3, s, "cta", "คอมเมนต์ WRAP รับแพ็กฟรี")]
    return {"seconds": s, "ratio": "9:16", "music_bpm": 120, "shots": [{"from_s": a, "to_s": b, "kind": k, "text_th": t} for a, b, k, t in shots],
            "watermark": "WrapRide · AI วันละแอป"}


def diary_summary(entries, today, wash_every_days=14):
    if not entries: raise ValueError("empty diary")
    t = _dt.date.fromisoformat(today)
    for e in entries:
        if e["kind"] not in ("wash", "wrap", "service", "rim", "photo", "tire"): raise ValueError("kind")
    wraps = sorted(e["date"] for e in entries if e["kind"] == "wrap")
    washes = sorted(e["date"] for e in entries if e["kind"] == "wash")
    age = (t - _dt.date.fromisoformat(wraps[-1])).days if wraps else None
    last_wash = washes[-1] if washes else (wraps[-1] if wraps else min(e["date"] for e in entries))
    next_wash = (_dt.date.fromisoformat(last_wash) + _dt.timedelta(days=wash_every_days)).isoformat()
    spend = sum(e.get("cost_baht", 0) for e in entries)
    tip = "สัปดาห์แรกหลังติดฟิล์ม เลี่ยงฉีดน้ำแรงดันสูงใกล้ขอบฟิล์ม" if age is not None and age < 7 else "ล้างมือด้วยแชมพูค่า pH กลาง เลี่ยงขัดแรงบนผิวด้าน"
    return {"entries": len(entries), "wrap_age_days": age, "next_wash": next_wash, "spend_baht": spend, "care_tip_th": tip,
            "headline_th": f"ฟิล์มอายุ {age if age is not None else '-'} วัน · ล้างครั้งต่อไป {next_wash} · ใช้ไป ฿{spend:,}"}


def share_card(spec, hook_th):
    return {"title_th": spec["title_th"], "hook_th": hook_th, "layout": "car_before_after", "sizes": ["1080x1350", "1080x1920"],
            "watermark": "WrapRide · AI วันละแอป", "cta_th": "คอมเมนต์ WRAP รับแพ็กฟรี", "disclaimer_th": "ภาพจำลอง ราคาโดยประมาณ"}


def quota(used_today, free_per_day=5, pro=False):
    _rng(used_today, 0, 10000, "used_today")
    if pro: return {"allowed": 1, "left_after": None, "paywall": False}
    left = free_per_day - used_today
    return {"allowed": 1 if left > 0 else 0, "left_after": max(left - 1, 0), "paywall": left <= 0}


def safety_guard(flag=None):
    msgs = {None: ("ok", "ภาพจำลองเพื่อดูไอเดีย ตัดสินใจกับร้านจริงอีกครั้ง"),
            "plate_visible": ("warn", "เห็นป้ายทะเบียน ระบบเบลอให้อัตโนมัติก่อนแชร์"),
            "covers_lights": ("stop", "ห้ามติดฟิล์ม/สติกเกอร์ทับไฟหรือป้ายทะเบียน"),
            "not_vehicle": ("stop", "ไม่พบรถในรูป ถ่ายใหม่ให้เห็นรถทั้งคัน"),
            "someone_elses_car": ("warn", "ใช้รูปรถของคุณเอง หรือได้รับอนุญาตจากเจ้าของ"),
            "brand_logo": ("stop", "ไม่สร้างโลโก้/ลายลิขสิทธิ์ของแบรนด์อื่น ใช้ลายของคุณเอง")}
    if flag not in msgs: raise ValueError("flag")
    lv, m = msgs[flag]
    return {"level": lv, "message_th": m}
