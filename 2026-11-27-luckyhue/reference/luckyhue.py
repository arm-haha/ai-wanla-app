"""LuckyHue deterministic logic (no AI calls).
Weekday colours follow a common Thai folk mapping. Sources differ (especially Wednesday).
This is for fun — not fortune-telling, not astrology, not a promise of luck.
"""
from datetime import date, timedelta
FREE_SCANS_PER_DAY = 3
MIN_CONF = 0.6
WATERMARK = "Made with LuckyHue · for fun only, not fortune-telling"
SAFETY_DISCLAIMER_TH = "LuckyHue เป็นสีมงคลตามวันที่นิยมหาสนุก ไม่ใช่หมอดู ไม่ใช่โหราศาสตร์ และไม่รับประกันโชคชะตา แหล่งที่มาของสีประจำวันอาจต่างกัน โดยเฉพาะวันพุธ"

# Daytime folk mapping commonly cited in Thai popular culture. Wednesday-night orange is optional.
WEEKDAYS = {
    "sunday":    {"id": "d01", "name_th": "วันอาทิตย์", "color_th": "แดง",    "color_en": "red",    "hex": "#DC2626", "accent": "#FEE2E2"},
    "monday":    {"id": "d02", "name_th": "วันจันทร์",  "color_th": "เหลือง",  "color_en": "yellow", "hex": "#EAB308", "accent": "#FEF9C3"},
    "tuesday":   {"id": "d03", "name_th": "วันอังคาร",  "color_th": "ชมพู",   "color_en": "pink",   "hex": "#EC4899", "accent": "#FCE7F3"},
    "wednesday": {"id": "d04", "name_th": "วันพุธ",    "color_th": "เขียว",   "color_en": "green",  "hex": "#16A34A", "accent": "#DCFCE7",
                  "night_color_th": "แสด", "night_hex": "#F97316"},
    "thursday":  {"id": "d05", "name_th": "วันพฤหัสบดี","color_th": "ส้ม",    "color_en": "orange", "hex": "#F97316", "accent": "#FFEDD5"},
    "friday":    {"id": "d06", "name_th": "วันศุกร์",   "color_th": "ฟ้า",    "color_en": "blue",   "hex": "#38BDF8", "accent": "#E0F2FE"},
    "saturday":  {"id": "d07", "name_th": "วันเสาร์",   "color_th": "ม่วง",   "color_en": "purple", "hex": "#7C3AED", "accent": "#EDE9FE"},
}
DOW_PY = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

COLOR_ALIASES = {
    "red": ["red", "crimson", "maroon"],
    "yellow": ["yellow", "gold", "mustard"],
    "pink": ["pink", "rose", "magenta"],
    "green": ["green", "olive", "mint"],
    "orange": ["orange", "coral", "peach"],
    "blue": ["blue", "sky", "navy", "light_blue", "teal"],
    "purple": ["purple", "violet", "lavender"],
}
NEUTRALS = {"white", "black", "beige", "gray", "grey", "cream", "brown", "navy"}  # navy also aliases blue
# navy can count as both lucky-blue and a deep neutral; treat as lucky for friday, else neutral.

CATEGORY_ORDER = ["top", "bottom", "shoes", "bag", "accessory"]

BLESSINGS = {
    "sunday": "ขอให้วันนี้มีพลังและเริ่มต้นสดใส",
    "monday": "ขอให้วันนี้ราบรื่นและใจเบา",
    "tuesday": "ขอให้วันนี้มีความกล้าและอ่อนโยน",
    "wednesday": "ขอให้วันนี้เติบโตและใจเย็น",
    "thursday": "ขอให้วันนี้ฉลาดเลือกและเฮง ๆ",
    "friday": "ขอให้วันนี้สบายและสิ่งดี ๆ เข้ามา",
    "saturday": "ขอให้วันนี้มั่นคงและพักผ่อนได้",
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
        tips.append("แสงสะท้อนในตู้เยอะ เปิดประตูตู้แล้วถ่ายในที่ร่ม")
    if blur > 0.4:
        tips.append("ภาพเบลอ วางมือนิ่งหรือถ่ายทีละชิ้น")
    if crop > 0.45:
        tips.append("เสื้อผ้าถูกครอป ถ่ายให้เห็นทั้งตัวเสื้อหรือกางเกง")
    if n_dets == 0:
        tips.append("ยังไม่เจอเสื้อผ้าในรูป แขวนหรือวางของบนพื้นเรียบแล้วถ่ายใหม่")
    return {"score": score, "ok": score >= 60 and n_dets >= 1, "tips_th": tips}


def weekday_from_date(iso):
    d = date.fromisoformat(iso)
    return DOW_PY[d.weekday()]


def lucky_color(weekday, today_iso=None, use_wednesday_night=False):
    if weekday not in WEEKDAYS:
        raise ValueError("unknown weekday " + str(weekday))
    info = WEEKDAYS[weekday]
    night = bool(use_wednesday_night and weekday == "wednesday")
    color_th = info["night_color_th"] if night else info["color_th"]
    hexv = info["night_hex"] if night else info["hex"]
    today_match = None
    if today_iso:
        today_match = weekday_from_date(today_iso) == weekday
    return {
        "weekday": weekday, "name_th": info["name_th"], "color_th": color_th,
        "color_en": "orange" if night else info["color_en"], "hex": hexv, "accent": info["accent"],
        "is_birth_day": True, "today_is_birth_day": today_match,
        "night_mode": night,
        "headline_th": f"สีมงคล{info['name_th']}คือสี{color_th}",
        "blessing_th": BLESSINGS[weekday],
        "disclaimer_th": SAFETY_DISCLAIMER_TH,
    }


def _val(dets, key, default=None):
    for d in dets:
        if d.get("key") == key and d.get("confidence", 0) >= MIN_CONF:
            return d["value"]
    return default


def parse_closet(shot):
    q = scan_quality(shot["glare"], shot["blur"], shot["crop"], len(shot.get("items") or shot.get("detections") or []))
    items = []
    raw = shot.get("items")
    if raw is None:
        # detections may include item objects under key "item"
        raw = [d["value"] for d in shot.get("detections", []) if d.get("key") == "item" and d.get("confidence", 0) >= MIN_CONF]
    for it in raw or []:
        if it.get("category") not in CATEGORY_ORDER:
            raise ValueError("unknown category " + str(it.get("category")))
        items.append({"id": it["id"], "name_th": it["name_th"], "category": it["category"],
                      "color_key": it["color_key"], "color_th": it.get("color_th") or it["color_key"]})
    return {"shot_id": shot["id"], "quality": q, "ok": q["ok"] and len(items) >= 1,
            "items": items, "count": len(items),
            "message_th": f"เจอเสื้อผ้า {len(items)} ชิ้น" if items else "ยังไม่เจอเสื้อผ้าในรูป"}


def _is_lucky(color_key, lucky_en):
    aliases = set(COLOR_ALIASES.get(lucky_en, [lucky_en]))
    return color_key in aliases


def _is_neutral(color_key, lucky_en):
    if color_key == "navy" and lucky_en == "blue":
        return False  # counts as lucky blue
    return color_key in NEUTRALS


def outfit_mix(closet, lucky, pick=None):
    if not closet.get("ok"):
        raise ValueError("closet not ok")
    lucky_en = lucky["color_en"]
    items = closet["items"]
    if pick is not None:
        chosen = []
        by_id = {i["id"]: i for i in items}
        for pid in pick:
            if pid not in by_id:
                raise ValueError("unknown item " + pid)
            chosen.append(by_id[pid])
    else:
        # auto: prefer one item per category, lucky first then neutral
        chosen = []
        for cat in CATEGORY_ORDER:
            group = [i for i in items if i["category"] == cat]
            lucky_items = [i for i in group if _is_lucky(i["color_key"], lucky_en)]
            neutrals = [i for i in group if _is_neutral(i["color_key"], lucky_en)]
            if lucky_items:
                chosen.append(lucky_items[0])
            elif neutrals:
                chosen.append(neutrals[0])
    lucky_n = sum(1 for i in chosen if _is_lucky(i["color_key"], lucky_en))
    neu_n = sum(1 for i in chosen if _is_neutral(i["color_key"], lucky_en))
    other_n = len(chosen) - lucky_n - neu_n
    if not chosen or lucky_n == 0:
        verdict, msg = "no_match", f"ยังไม่มีชิ้นสี{lucky['color_th']} ลองจับคู่กับของกลาง ๆ หรือเพิ่มชิ้นสีนี้"
    elif other_n > 0:
        verdict, msg = "clash", f"มีชิ้นที่หลุดจากสี{lucky['color_th']} ลองเปลี่ยนเป็นสีกลางหรือสีมงคล"
    else:
        verdict, msg = "match", f"แมตช์สี{lucky['color_th']}{lucky['name_th']} ได้ {lucky_n} ชิ้น คู่กับของกลาง {neu_n} ชิ้น"
    score = 0 if not chosen else round(100 * (lucky_n + 0.5 * neu_n) / len(chosen))
    return {"items": chosen, "count": len(chosen), "lucky_n": lucky_n, "neutral_n": neu_n, "other_n": other_n,
            "score": score, "verdict": verdict,
            "headline_th": msg, "color_th": lucky["color_th"], "hex": lucky["hex"],
            "disclaimer_th": SAFETY_DISCLAIMER_TH}


def wallpaper(lucky, size="1080x1920"):
    if size not in ("1080x1920", "1080x1080", "1170x2532"):
        raise ValueError("unknown size " + size)
    palette = [lucky["hex"], lucky["accent"], "#111827"]
    return {"size": size, "weekday": lucky["weekday"], "color_th": lucky["color_th"], "hex": lucky["hex"],
            "palette": palette, "blessing_th": lucky["blessing_th"],
            "title_th": f"วอลเปเปอร์สี{lucky['color_th']}{lucky['name_th']}",
            "watermark": WATERMARK, "disclaimer_th": SAFETY_DISCLAIMER_TH}


def weekly_calendar(start_iso, birth_weekday):
    start = date.fromisoformat(start_iso)
    # start from Monday of that week
    monday = start - timedelta(days=start.weekday())
    days = []
    for i, key in enumerate(DOW_PY):
        d = monday + timedelta(days=i)
        info = WEEKDAYS[key]
        days.append({"iso": d.isoformat(), "weekday": key, "name_th": info["name_th"],
                     "color_th": info["color_th"], "hex": info["hex"],
                     "is_birth_day": key == birth_weekday})
    birth = next(d for d in days if d["is_birth_day"])
    return {"start_iso": monday.isoformat(), "birth_weekday": birth_weekday,
            "days": days, "count": 7,
            "headline_th": f"สัปดาห์นี้ไฮไลต์{birth['name_th']} สี{birth['color_th']}",
            "disclaimer_th": SAFETY_DISCLAIMER_TH}


def share_card(name_th, lucky, mix):
    return {"title_th": f"LuckyHue — {name_th}",
            "headline_th": lucky["headline_th"],
            "hook_th": "สีมงคลประจำวัน + วอลเปเปอร์สายมู",
            "color_th": lucky["color_th"], "hex": lucky["hex"],
            "outfit_score": mix["score"] if mix else None,
            "layout": "hue_card", "sizes": ["1080x1350", "1080x1920", "1080x1080"],
            "watermark": WATERMARK, "cta_th": "คอมเมนต์ HUE รับแพ็กฟรี"}


def quota(used_today, want, pro=False):
    if pro:
        return {"allowed": want, "left_after": None, "paywall": False}
    left = max(0, FREE_SCANS_PER_DAY - used_today)
    allowed = min(want, left)
    return {"allowed": allowed, "left_after": left - allowed, "paywall": allowed < want}


def safety_guard(treats_as_fortune=False):
    if treats_as_fortune:
        return {"level": "warn", "message_th": "อย่าใช้สีมงคลตัดสินใจเรื่องเงิน สุขภาพ หรือความสัมพันธ์ " + SAFETY_DISCLAIMER_TH}
    return {"level": "ok", "message_th": SAFETY_DISCLAIMER_TH}
