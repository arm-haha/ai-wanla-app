"""GlamTry reference logic — deterministic, no network. Looks are SIMULATIONS; shade matches and prices are ESTIMATES
(example ranges set by the pack, generic product types only — no real brands). Patch-test / allergy text is general info, not medical advice."""
import datetime as _dt

LOOKS = {  # lip / blush / eye base colours, finish, minutes, skill 1–3, items used
    "natural":      {"th": "เนเชอรัลหน้าสด",     "en": "Natural no-makeup", "lip": "#C97B6E", "blush": "#E8A598", "eye": "#B89580", "liner": None,      "finish": "satin", "min": 10, "skill": 1,
                     "items": ["skin_tint", "concealer", "brow", "lip_tint", "mascara"]},
    "korean_glass": {"th": "เกาหลีผิวฉ่ำ",       "en": "Korean glass skin", "lip": "#E06A7A", "blush": "#F4A7B0", "eye": "#E9B7A6", "liner": "#5A3A2E", "finish": "dewy",  "min": 15, "skill": 1,
                     "items": ["primer", "cushion", "concealer", "blush", "eyeshadow", "lip_tint", "highlighter"]},
    "thai_bride":   {"th": "เจ้าสาวไทย",         "en": "Thai bride",        "lip": "#B5485A", "blush": "#E39A8C", "eye": "#A8745A", "liner": "#1E1414", "finish": "satin", "min": 45, "skill": 3,
                     "items": ["primer", "foundation", "concealer", "powder", "brow", "eyeshadow", "eyeliner", "false_lashes", "mascara", "blush", "highlighter", "lipstick", "setting_spray"]},
    "party_glam":   {"th": "ปาร์ตี้จัดเต็ม",       "en": "Party glam",        "lip": "#8E1F2F", "blush": "#D9826E", "eye": "#5B3A4E", "liner": "#111111", "finish": "matte", "min": 35, "skill": 3,
                     "items": ["primer", "foundation", "concealer", "powder", "eyeshadow", "eyeliner", "false_lashes", "blush", "highlighter", "lipstick", "setting_spray"]},
    "office":       {"th": "สาวออฟฟิศเรียบหรู",   "en": "Office polished",   "lip": "#B8645A", "blush": "#DFA08E", "eye": "#9C7B66", "liner": "#3A2A22", "finish": "satin", "min": 15, "skill": 2,
                     "items": ["primer", "foundation", "concealer", "powder", "brow", "eyeshadow", "mascara", "blush", "lipstick"]},
    "y2k":          {"th": "Y2K สายปั๊ว",         "en": "Y2K pop",           "lip": "#E58FB0", "blush": "#F7A1C4", "eye": "#9FC3F0", "liner": "#2B2B6E", "finish": "glossy","min": 20, "skill": 2,
                     "items": ["skin_tint", "concealer", "eyeshadow", "eyeliner", "mascara", "blush", "lip_gloss", "glitter"]},
}
UNDERTONES = {"cool": {"th": "อันเดอร์โทนเย็น", "tint": "#C2185B", "t": 0.15}, "neutral": {"th": "อันเดอร์โทนกลาง", "tint": None, "t": 0.0},
              "warm": {"th": "อันเดอร์โทนอุ่น", "tint": "#E07A3F", "t": 0.15}, "olive": {"th": "อันเดอร์โทนมะกอก", "tint": "#B5651D", "t": 0.12}}
DEPTHS = {"fair": {"th": "ผิวขาวมาก", "n": 1}, "light": {"th": "ผิวขาว-ขาวเหลือง", "n": 2}, "medium": {"th": "ผิวสองสี", "n": 3},
          "tan": {"th": "ผิวแทน", "n": 4}, "deep": {"th": "ผิวเข้ม", "n": 5}}
INTENSITY = {"soft": 0.35, "medium": 0.55, "full": 0.8}
ITEMS = {  # generic product types only; (low, high) THB example ranges per tier
    "primer":        {"th": "ไพรเมอร์",             "budget": (99, 199),  "mid": (290, 590),  "premium": (990, 1900), "pao": 12},
    "skin_tint":     {"th": "สกินทินท์",            "budget": (129, 259), "mid": (350, 690),  "premium": (1100, 2100), "pao": 12},
    "cushion":       {"th": "คุชชั่น",              "budget": (159, 299), "mid": (450, 890),  "premium": (1500, 2600), "pao": 12},
    "foundation":    {"th": "รองพื้น",              "budget": (149, 299), "mid": (450, 990),  "premium": (1500, 2800), "pao": 12},
    "concealer":     {"th": "คอนซีลเลอร์",          "budget": (89, 199),  "mid": (290, 590),  "premium": (900, 1500), "pao": 12},
    "powder":        {"th": "แป้งฝุ่น/แป้งพัฟ",      "budget": (89, 199),  "mid": (290, 590),  "premium": (1000, 1900), "pao": 24},
    "brow":          {"th": "ดินสอเขียนคิ้ว",        "budget": (59, 129),  "mid": (190, 390),  "premium": (700, 1200), "pao": 24},
    "eyeshadow":     {"th": "พาเลตต์อายแชโดว์",      "budget": (99, 249),  "mid": (390, 890),  "premium": (1500, 3200), "pao": 24},
    "eyeliner":      {"th": "อายไลเนอร์",           "budget": (79, 159),  "mid": (250, 450),  "premium": (800, 1300), "pao": 6},
    "mascara":       {"th": "มาสคาร่า",             "budget": (79, 179),  "mid": (290, 490),  "premium": (900, 1400), "pao": 3},
    "false_lashes":  {"th": "ขนตาปลอม",            "budget": (39, 99),   "mid": (150, 290),  "premium": (450, 900),  "pao": 0},
    "blush":         {"th": "บลัชออน",              "budget": (79, 179),  "mid": (290, 590),  "premium": (1000, 1900), "pao": 24},
    "highlighter":   {"th": "ไฮไลต์",               "budget": (89, 199),  "mid": (290, 590),  "premium": (1000, 1900), "pao": 24},
    "lip_tint":      {"th": "ลิปทินท์",             "budget": (59, 159),  "mid": (250, 450),  "premium": (800, 1300), "pao": 12},
    "lipstick":      {"th": "ลิปสติก",              "budget": (79, 199),  "mid": (290, 590),  "premium": (1100, 1700), "pao": 12},
    "lip_gloss":     {"th": "ลิปกลอส",              "budget": (59, 149),  "mid": (250, 450),  "premium": (850, 1300), "pao": 12},
    "glitter":       {"th": "กลิตเตอร์ทาตา",        "budget": (49, 129),  "mid": (190, 350),  "premium": (600, 1100), "pao": 24},
    "setting_spray": {"th": "สเปรย์ล็อกเมคอัพ",      "budget": (99, 199),  "mid": (290, 590),  "premium": (1000, 1700), "pao": 12},
}
TIERS = {"budget": "สายประหยัด (ร้านสะดวกซื้อ/ดรักสโตร์)", "mid": "กลาง ๆ (เคาน์เตอร์ห้าง)", "premium": "จัดเต็ม (ไฮเอนด์)"}
EVENTS = {  # recommended look, hours worn typical
    "office_day":   {"th": "ไปทำงาน",            "look": "office",       "hours": 9},
    "interview":    {"th": "สัมภาษณ์งาน",          "look": "office",       "hours": 3},
    "date":         {"th": "เดตแรก",             "look": "korean_glass", "hours": 4},
    "wedding_guest":{"th": "ไปงานแต่งเพื่อน",      "look": "korean_glass", "hours": 6},
    "own_wedding":  {"th": "งานแต่งตัวเอง",        "look": "thai_bride",   "hours": 12},
    "party":        {"th": "ปาร์ตี้/เคานต์ดาวน์",    "look": "party_glam",   "hours": 6},
    "concert":      {"th": "คอนเสิร์ต/เฟส",        "look": "y2k",          "hours": 7},
    "graduation":   {"th": "รับปริญญา",           "look": "natural",      "hours": 8},
}
GUARD = {None: ("ok", "ภาพลองแต่งหน้าเป็นภาพจำลอง สีจริงต่างตามผิว แสง และผลิตภัณฑ์"),
         "not_own_photo": ("stop", "ใช้ได้เฉพาะเซลฟี่ของคุณเองเท่านั้น ห้ามใช้รูปคนอื่น"),
         "celebrity": ("stop", "ไม่รองรับรูปดารา/คนดัง หรือการแต่งให้เหมือนใคร ใช้หน้าตัวเองเท่านั้น"),
         "under_13": ("stop", "แอปนี้สำหรับอายุ 13 ปีขึ้นไป"),
         "multiple_faces": ("warn", "เจอหลายใบหน้า ครอปให้เหลือหน้าคุณคนเดียว"),
         "no_face": ("stop", "ไม่พบใบหน้าในรูป ถ่ายหน้าตรงใหม่อีกครั้ง"),
         "filter_on": ("warn", "ดูเหมือนเปิดฟิลเตอร์อยู่ ปิดฟิลเตอร์ก่อนเพื่อให้สีแม่นขึ้น"),
         "whitening_request": ("stop", "GlamTry ไม่ปรับผิวให้ขาวขึ้นหรือดัดรูปหน้า ทุกสีผิวสวยในแบบของตัวเอง")}
DISCLAIMER = "ภาพจำลอง ไม่ใช่ผลจริง สีจริงต่างตามผิว แสง และผลิตภัณฑ์ · เฉดผิวและราคาเป็นค่าประมาณ"
PATCH_NOTE = "ข้อมูลทั่วไป ไม่ใช่คำแนะนำทางการแพทย์ ถ้ามีอาการแพ้ (คัน บวม แดงมาก) ให้หยุดใช้และปรึกษาแพทย์/เภสัชกร"
CTA = "คอมเมนต์ GLAM รับแพ็กฟรี"
WM = "GlamTry · AI วันละแอป"


def _rng(x, lo, hi, name):
    if isinstance(x, bool) or not isinstance(x, (int, float)) or x < lo or x > hi:
        raise ValueError(f"{name} out of range")


def _get(d, k, name):
    if k not in d: raise ValueError(f"unknown {name} {k}")
    return d[k]


def _mix(hexc, other, t):
    a = [int(hexc[i:i + 2], 16) for i in (1, 3, 5)]; b = [int(other[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * t):02X}" for x, y in zip(a, b))


def scan_quality(light, blur, tilt, filter_on=False):
    """light = 0 (dark) … 1 (even daylight); blur/tilt = 0 good … 1 bad."""
    for v, n in ((light, "light"), (blur, "blur"), (tilt, "tilt")):
        _rng(v, 0, 1, n)
    score = round(100 - (1 - light) * 40 - blur * 35 - tilt * 25 - (15 if filter_on else 0))
    tips = []
    if light < 0.6: tips.append("แสงน้อย/ไม่เท่ากัน หันหน้าเข้าหน้าต่าง แสงธรรมชาติดีที่สุด")
    if blur > 0.3: tips.append("ภาพเบลอ ถือมือถือนิ่ง ๆ แล้วถ่ายใหม่")
    if tilt > 0.3: tips.append("หน้าเอียง มองกล้องตรง ๆ ระดับสายตา")
    if filter_on: tips.append("ปิดฟิลเตอร์/บิวตี้โหมดก่อนถ่าย")
    score = max(0, score)
    return {"score": score, "ok": score >= 70, "tips_th": tips}


def selfie_scan(photo):
    return {"photo_id": photo["id"], "quality": scan_quality(photo["light"], photo["blur"], photo["tilt"], photo.get("filter_on", False))}


def consent_check(age, own_photo, faces=1, celebrity_match=False, whitening_request=False):
    """Consent Guard: own photo only, 13+, one face, no celebrity likeness, no whitening."""
    _rng(age, 0, 120, "age"); _rng(faces, 0, 20, "faces")
    flags = []
    if age < 13: flags.append("under_13")
    if not own_photo: flags.append("not_own_photo")
    if celebrity_match: flags.append("celebrity")
    if faces == 0: flags.append("no_face")
    elif faces > 1: flags.append("multiple_faces")
    if whitening_request: flags.append("whitening_request")
    levels = [GUARD[f][0] for f in flags]
    lv = "stop" if "stop" in levels else ("warn" if levels else "ok")
    return {"allowed": lv != "stop", "level": lv, "flags": flags, "messages_th": [GUARD[f][1] for f in flags] or [GUARD[None][1]]}


def shade_match(rgb, quality_score=90):
    """Cheek-patch average RGB → depth + undertone estimate. Never suggests a lighter shade than measured."""
    if len(rgb) != 3: raise ValueError("rgb")
    for v in rgb: _rng(v, 0, 255, "rgb")
    _rng(quality_score, 0, 100, "quality_score")
    r, g, b = rgb
    L = 0.299 * r + 0.587 * g + 0.114 * b
    depth = "fair" if L >= 200 else "light" if L >= 175 else "medium" if L >= 145 else "tan" if L >= 115 else "deep"
    rb, rg = r - b, r - g
    if rg < 18 and rb > 35: tone = "olive"
    elif rb >= 70: tone = "warm"
    elif rb <= 45: tone = "cool"
    else: tone = "neutral"
    code = f"{DEPTHS[depth]['n']}{tone[0].upper()}"
    conf = round(min(0.9, quality_score / 100 * 0.9), 2)
    lips = [_lip_for(LOOKS[k]["lip"], tone) for k in ("natural", "korean_glass", "office")]
    return {"skin_hex": "#" + "".join(f"{v:02X}" for v in rgb), "depth": depth, "undertone": tone, "shade_code": code,
            "label_th": f"{DEPTHS[depth]['th']} · {UNDERTONES[tone]['th']} (โค้ดเฉด {code})", "lip_suggestions_hex": lips,
            "confidence": conf, "is_estimate": True,
            "tip_th": "ทาเทสต์ที่กรอบหน้า/ขากรรไกร ดูใต้แสงธรรมชาติก่อนซื้อ" if conf >= 0.6 else "แสงยังไม่ดี ผลอาจคลาด ถ่ายใหม่ใกล้หน้าต่าง",
            "disclaimer_th": "เฉดผิวเป็นค่าประมาณจากรูป ไม่ใช่การวัดจริง"}


def _lip_for(base, tone):
    u = UNDERTONES[tone]
    return base if not u["tint"] else _mix(base, u["tint"], u["t"])


def look_palette(look, undertone="neutral", intensity="medium"):
    lk = _get(LOOKS, look, "look"); _get(UNDERTONES, undertone, "undertone"); op = _get(INTENSITY, intensity, "intensity")
    return {"look": look, "undertone": undertone, "intensity": intensity, "lip_hex": _lip_for(lk["lip"], undertone),
            "blush_hex": _lip_for(lk["blush"], undertone), "eye_hex": lk["eye"], "liner_hex": lk["liner"], "opacity": op, "finish": lk["finish"]}


def look_spec(look, depth, undertone, intensity="medium"):
    lk = _get(LOOKS, look, "look"); _get(DEPTHS, depth, "depth")
    pal = look_palette(look, undertone, intensity)
    prompt = (f"Apply a realistic '{lk['en']}' makeup look to this exact person's own selfie: lips {pal['lip_hex']}, blush {pal['blush_hex']}, "
              f"eyeshadow {pal['eye_hex']}, {lk['finish']} finish, opacity {pal['opacity']}. Keep identity, face shape, skin tone, skin depth and texture unchanged; "
              "no skin whitening, no face slimming, no reshaping; no celebrity likeness; keep hair, background and lighting; output 4:5.")
    return {"look": look, "depth": depth, "undertone": undertone, "intensity": intensity, "palette": pal, "minutes": lk["min"], "skill": lk["skill"],
            "image_prompt": prompt, "title_th": f"{lk['th']} · {lk['min']} นาที", "disclaimer_th": DISCLAIMER}


def six_looks(depth, undertone, intensity="medium"):
    """The hook: one selfie → all 6 looks."""
    return [look_spec(k, depth, undertone, intensity) for k in LOOKS]


_STEP = {  # area, tip
    "primer": ("base", "บาง ๆ เฉพาะ T-zone ช่วยให้รองพื้นติดทน"), "skin_tint": ("base", "ใช้นิ้วเกลี่ยบาง ๆ ให้เห็นผิวจริง"),
    "cushion": ("base", "ตบเบา ๆ ทีละชั้น เน้นกลางหน้า"), "foundation": ("base", "ใช้เฉดตรงโค้ดของคุณ เกลี่ยลงคอให้กลืน"),
    "concealer": ("base", "แต้มเฉพาะใต้ตา/รอยสิว แล้วตบให้เนียน"), "powder": ("base", "ปัดเฉพาะ T-zone กันมัน"),
    "brow": ("brow", "วาดตามทรงคิ้วจริง เริ่มจากหางคิ้ว"), "eyeshadow": ("eye", "สีอ่อนทั่วเปลือกตา สีเข้มที่ร่องตา"),
    "eyeliner": ("eye", "ลากชิดโคนขนตา หางตายกขึ้นเล็กน้อย"), "mascara": ("eye", "ปัดจากโคนแล้วส่ายแปรงขึ้น"),
    "false_lashes": ("eye", "ตัดให้พอดีตา ติดห่างหัวตาเล็กน้อย"), "blush": ("cheek", "ยิ้มแล้วปัดที่โหนกแก้ม เกลี่ยขึ้นขมับ"),
    "highlighter": ("cheek", "แตะสันจมูก โหนกแก้ม และคันศร"), "lip_tint": ("lip", "ทาด้านในริมฝีปากแล้วเม้มให้ไล่สี"),
    "lipstick": ("lip", "เขียนขอบปากก่อนแล้วเติมสี"), "lip_gloss": ("lip", "ทากลางปากให้ดูอวบอิ่ม"),
    "glitter": ("eye", "แตะกลางเปลือกตา/หัวตา ระวังเข้าตา"), "setting_spray": ("finish", "ฉีดห่าง 20 ซม. เป็นรูปตัว X"),
}


def tutorial(look, undertone="neutral", skill=None):
    lk = _get(LOOKS, look, "look")
    pal = look_palette(look, undertone)
    hexes = {"lip": pal["lip_hex"], "cheek": pal["blush_hex"], "eye": pal["eye_hex"]}
    items = lk["items"] if skill is None or skill >= lk["skill"] else [i for i in lk["items"] if i not in ("false_lashes", "glitter", "eyeliner")]
    per = max(1, round(lk["min"] / len(items)))
    steps = [{"n": n, "item": it, "area": _STEP[it][0], "item_th": ITEMS[it]["th"], "tip_th": _STEP[it][1], "color_hex": hexes.get(_STEP[it][0]), "minutes": per}
             for n, it in enumerate(items, 1)]
    return {"look": look, "steps": steps, "total_minutes": per * len(steps), "simplified": len(items) < len(lk["items"]),
            "note_th": "เริ่มจากผิวสะอาดและทาครีมกันแดดก่อนเสมอ"}


def budget_kit(look, tier="budget", owned=()):
    lk = _get(LOOKS, look, "look"); _get(TIERS, tier, "tier")
    for o in owned: _get(ITEMS, o, "item")
    need = [i for i in lk["items"] if i not in owned]
    items = [{"item": i, "item_th": ITEMS[i]["th"], "tier": tier, "low_baht": ITEMS[i][tier][0], "high_baht": ITEMS[i][tier][1]} for i in need]
    lo = sum(x["low_baht"] for x in items); hi = sum(x["high_baht"] for x in items)
    prem_hi = sum(ITEMS[i]["premium"][1] for i in need)
    return {"look": look, "tier": tier, "tier_th": TIERS[tier], "items": items, "skipped_owned": [i for i in lk["items"] if i in owned],
            "low_baht": lo, "high_baht": hi, "save_vs_premium_baht": prem_hi - hi,
            "dupe_tip_th": "เลือกของเนื้อสัมผัส/โทนสีใกล้กันแทนได้ ดูรหัสสี HEX เทียบที่ร้าน",
            "disclaimer_th": "ราคาเป็นช่วงประมาณของสินค้าประเภทเดียวกัน ไม่ได้อ้างอิงแบรนด์ใด"}


def occasion_plan(event, event_date, today, outdoor=False, hot_humid=True):
    ev = _get(EVENTS, event, "event")
    d = (_dt.date.fromisoformat(event_date) - _dt.date.fromisoformat(today)).days
    if d < 0: raise ValueError("event in the past")
    look = ev["look"]; extras = []
    if outdoor or hot_humid: extras.append("setting_spray")
    if ev["hours"] >= 6: extras += ["blotting_paper", "touch_up_lip"]
    timeline = []
    if d >= 7: timeline.append({"days_before": 7, "task_th": "ลองลุคใน GlamTry แล้วลองแต่งจริง 1 รอบ"})
    if d >= 2: timeline.append({"days_before": 2, "task_th": "ทำ patch test ของใหม่ทุกชิ้น ดูผลอย่างน้อย 24–48 ชม."})
    timeline.append({"days_before": 0, "task_th": f"เริ่มแต่งก่อนออกจากบ้าน {LOOKS[look]['min'] + 10} นาที"})
    return {"event": event, "event_th": ev["th"], "event_date": event_date, "days_left": d, "look": look, "hours_worn": ev["hours"],
            "touch_up_kit": extras, "timeline": timeline,
            "warning_th": None if d >= 2 else "เหลือเวลาน้อย ใช้ของที่เคยใช้แล้วไม่แพ้ อย่าลองของใหม่วันงาน"}


def patch_test(new_items, sensitive=False, known_allergies=()):
    for i in new_items: _get(ITEMS, i, "item")
    eye = [i for i in new_items if i in ("eyeliner", "mascara", "glitter", "false_lashes", "eyeshadow")]
    level = "warn" if (sensitive or known_allergies or eye) else "info"
    steps = ["แต้มผลิตภัณฑ์เล็กน้อยที่หลังหูหรือท้องแขน", "ทิ้งไว้และสังเกตอย่างน้อย 24–48 ชม.", "ถ้าคัน แดง บวม ห้ามใช้ต่อ"]
    if eye: steps.append("ของรอบดวงตา: ห้ามใช้ร่วมกับคนอื่น และไม่ใช้กลิตเตอร์ที่ไม่ใช่สำหรับตา")
    if known_allergies: steps.append("อ่านส่วนผสมบนฉลากเทียบกับสิ่งที่เคยแพ้: " + ", ".join(known_allergies))
    return {"level": level, "items": list(new_items), "steps_th": steps, "note_th": PATCH_NOTE}


def reel_plan(spec, seconds=20):
    _rng(seconds, 15, 30, "seconds")
    cut = [0, round(seconds * .15), round(seconds * .35), round(seconds * .7), round(seconds * .85), seconds]
    lk = LOOKS[spec["look"]]
    txt = ["หน้าสด ๆ ไม่รู้จะแต่งลุคไหน? อย่าเพิ่งซื้อ", "เซลฟี่ 1 รูป → AI สแกนเฉดผิว", "ปัด 6 ลุค: เนเชอรัล · เกาหลี · เจ้าสาว · ปาร์ตี้ · ออฟฟิศ · Y2K",
           f"เลื่อนดู ก่อน/หลัง · {lk['th']} + ชุดของงบประมาณ", CTA]
    kinds = ["before", "scan", "swipe", "compare", "cta"]
    return {"seconds": seconds, "ratio": "9:16", "music_bpm": 118,
            "shots": [{"from_s": cut[k], "to_s": cut[k + 1], "kind": kinds[k], "text_th": txt[k]} for k in range(5)], "watermark": WM}


def diary_summary(entries, today):
    if not entries: raise ValueError("empty diary")
    t = _dt.date.fromisoformat(today)
    for e in entries:
        if e["kind"] not in ("try", "wear", "buy", "open", "photo"): raise ValueError("kind")
    worn = [e["look"] for e in entries if e["kind"] in ("try", "wear") and e.get("look")]
    top = max(sorted(set(worn)), key=worn.count) if worn else None
    spend = sum(e.get("cost_baht", 0) for e in entries)
    reps = []
    for e in entries:
        if e["kind"] == "open" and ITEMS[e["item"]]["pao"]:
            od = _dt.date.fromisoformat(e["date"]); m = ITEMS[e["item"]]["pao"]
            y, mo = divmod(od.month - 1 + m, 12)
            rd = od.replace(year=od.year + y, month=mo + 1, day=min(od.day, 28))
            reps.append({"item": e["item"], "replace_by": rd.isoformat(), "days_left": (rd - t).days})
    reps.sort(key=lambda r: r["replace_by"])
    nxt = reps[0] if reps else None
    return {"entries": len(entries), "looks_saved": len(set(worn)), "top_look": top, "spend_baht": spend, "replace_soon": reps,
            "headline_th": f"ลองไป {len(set(worn))} ลุค · ชอบสุด {LOOKS[top]['th'] if top else '-'} · ใช้ไป ฿{spend:,}"
                           + (f" · {ITEMS[nxt['item']]['th']} ควรเปลี่ยนภายใน {nxt['replace_by']}" if nxt else ""),
            "note_th": "อายุหลังเปิดใช้เป็นค่าประมาณทั่วไป ดูสัญลักษณ์บนฉลากของแต่ละชิ้น"}


def share_card(spec, hook_th):
    return {"title_th": spec["title_th"], "hook_th": hook_th, "layout": "selfie_before_after", "sizes": ["1080x1350", "1080x1920"],
            "watermark": WM, "cta_th": CTA, "disclaimer_th": "ภาพจำลอง · เฉดและราคาโดยประมาณ"}


def quota(used_today, free_per_day=3, pro=False):
    _rng(used_today, 0, 10000, "used_today")
    if pro: return {"allowed": 1, "left_after": None, "paywall": False}
    left = free_per_day - used_today
    return {"allowed": 1 if left > 0 else 0, "left_after": max(left - 1, 0), "paywall": left <= 0}


def safety_guard(flag=None):
    if flag not in GUARD: raise ValueError("flag")
    lv, m = GUARD[flag]
    return {"level": lv, "message_th": m}
