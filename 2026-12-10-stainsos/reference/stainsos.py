"""StainSOS deterministic logic (no AI calls). Stain-rescue helper — estimates only, test on a hidden spot first."""

STAINS = {
    "coffee":   {"th": "กาแฟ",          "cls": "tannin",  "base": 35},
    "thai_tea": {"th": "ชาไทย / ชานม",   "cls": "tannin",  "base": 45},
    "curry":    {"th": "แกง / ขมิ้น",     "cls": "oil_pigment", "base": 60},
    "oil":      {"th": "น้ำมัน / ซอส",    "cls": "oil",     "base": 40},
    "lipstick": {"th": "ลิปสติก",        "cls": "oil_pigment", "base": 50},
    "ink":      {"th": "หมึกปากกา",      "cls": "ink",     "base": 65},
    "blood":    {"th": "เลือด",           "cls": "protein", "base": 45},
    "mud":      {"th": "โคลน / ดิน",      "cls": "dirt",    "base": 30},
}
FABRICS = {
    "cotton":    {"th": "ผ้าฝ้าย",     "add": 0,  "delicate": False},
    "denim":     {"th": "ยีนส์",       "add": 0,  "delicate": False},
    "polyester": {"th": "โพลีเอสเตอร์", "add": 5,  "delicate": False},
    "rayon":     {"th": "เรยอน",       "add": 15, "delicate": True},
    "wool":      {"th": "ขนสัตว์",     "add": 20, "delicate": True},
    "silk":      {"th": "ผ้าไหม",      "add": 25, "delicate": True},
}
ITEMS = {
    "water": "น้ำเปล่า", "dish_soap": "น้ำยาล้างจาน", "baking_soda": "เบกกิ้งโซดา",
    "white_vinegar": "น้ำส้มสายชูกลั่น", "oxygen_bleach": "ผงฟอกออกซิเจน (สีตกไม่ได้ใช้)",
    "alcohol": "แอลกอฮอล์ล้างแผล 70%", "hand_sanitizer": "เจลล้างมือแอลกอฮอล์",
    "cornstarch": "แป้งข้าวโพด / แป้งฝุ่น", "brush": "แปรงสีฟันเก่า",
    "gentle_detergent": "น้ำยาซักผ้าไหม/ผ้าถนอม", "chlorine_bleach": "น้ำยาฟอกขาวคลอรีน",
    "ammonia": "แอมโมเนีย", "hydrogen_peroxide": "ไฮโดรเจนเปอร์ออกไซด์",
}
SUBSTITUTE = {"oxygen_bleach": "white_vinegar", "alcohol": "hand_sanitizer", "baking_soda": "cornstarch"}
FORBIDDEN = [
    ("chlorine_bleach", "white_vinegar", "เกิดก๊าซคลอรีน อันตรายต่อปอด"),
    ("chlorine_bleach", "ammonia", "เกิดก๊าซคลอรามีน อันตรายต่อปอด"),
    ("chlorine_bleach", "alcohol", "เกิดสารระเหยอันตราย (คลอโรฟอร์ม)"),
    ("hydrogen_peroxide", "white_vinegar", "เกิดกรดเปอร์อะซิติก กัดผิวและตา"),
]
CARE = {
    "wash_30": ("ซักน้ำไม่เกิน 30°C", 30), "wash_40": ("ซักน้ำไม่เกิน 40°C", 40),
    "wash_60": ("ซักน้ำไม่เกิน 60°C", 60), "hand_wash": ("ซักมือเท่านั้น", 30),
    "no_wash": ("ห้ามซักน้ำ", 0), "no_bleach": ("ห้ามใช้สารฟอกทุกชนิด", None),
    "non_chlorine_bleach": ("ใช้ได้เฉพาะสารฟอกไม่มีคลอรีน", None),
    "tumble_low": ("อบผ้าไฟอ่อน", None), "no_tumble": ("ห้ามอบผ้า", None),
    "iron_low": ("รีดไฟอ่อน (≤110°C)", None), "iron_med": ("รีดไฟกลาง (≤150°C)", None),
    "dry_clean": ("ซักแห้งได้", None), "no_dry_clean": ("ห้ามซักแห้ง", None),
}
MIN_CONF = 0.6
FREE_SCANS_PER_DAY = 3
WATERMARK = "Made with StainSOS · test on a hidden spot first"
DISCLAIMER_TH = ("StainSOS ให้ขั้นตอนทั่วไปและค่าประมาณเท่านั้น ไม่รับประกันว่าคราบจะหาย ทดสอบมุมด้านในก่อนทุกครั้ง "
                 "อ่านป้ายผ้าก่อนใช้ อย่าผสมน้ำยาต่างชนิดกัน ใส่ถุงมือและเปิดหน้าต่าง ผ้าแพงหรือผ้าบอบบางควรส่งร้านซักแห้ง")


def scan_quality(glare, blur, crop):
    for v in (glare, blur, crop):
        if not 0 <= v <= 1:
            raise ValueError("glare/blur/crop must be 0..1")
    score = int(round(100 * (1 - (0.30 * glare + 0.40 * blur + 0.30 * crop))))
    tips = []
    if glare > 0.5:
        tips.append("แสงสะท้อนบนผ้า ถ่ายใกล้หน้าต่างแต่ไม่โดนแดดตรง")
    if blur > 0.4:
        tips.append("ภาพเบลอ ถือนิ่งแล้วถ่ายให้เห็นขอบคราบชัด")
    if crop > 0.45:
        tips.append("คราบถูกตัด ถอยออกให้เห็นคราบทั้งหมดและเนื้อผ้ารอบ ๆ")
    return {"score": score, "ok": score >= 60, "tips_th": tips}


def photo_scan(photo):
    return {"photo_id": photo["id"], "quality": scan_quality(photo["glare"], photo["blur"], photo["crop"])}


def parse_stain(raw):
    if raw["stain"] not in STAINS:
        raise ValueError("unknown stain")
    if raw["fabric"] not in FABRICS:
        raise ValueError("unknown fabric")
    if raw["color"] not in ("white", "colored"):
        raise ValueError("color must be white|colored")
    if raw["age_hours"] < 0 or raw["size_cm"] <= 0:
        raise ValueError("age_hours >= 0 and size_cm > 0")
    if not 0 <= raw["confidence"] <= 1:
        raise ValueError("confidence 0..1")
    need = raw["confidence"] < MIN_CONF
    st, fb = STAINS[raw["stain"]], FABRICS[raw["fabric"]]
    msg = (f"ยังไม่แน่ใจ ช่วยยืนยันว่าเป็นคราบ{st['th']}บน{fb['th']}ก่อน ห้ามเริ่มขั้นตอนจนกว่าจะยืนยัน" if need
           else f"เจอคราบ{st['th']}บน{fb['th']}{'สีขาว' if raw['color'] == 'white' else 'สี'} ประมาณ {raw['size_cm']} ซม.")
    return {"stain": raw["stain"], "stain_th": st["th"], "cls": st["cls"], "fabric": raw["fabric"],
            "fabric_th": fb["th"], "color": raw["color"], "age_hours": raw["age_hours"], "size_cm": raw["size_cm"],
            "confidence": raw["confidence"], "needs_confirm": need, "message_th": msg}


def _age_add(h):
    if h < 1: return 0
    if h < 6: return 5
    if h < 24: return 12
    if h < 72: return 20
    return 30


def risk_meter(p):
    score = STAINS[p["stain"]]["base"] + _age_add(p["age_hours"]) + FABRICS[p["fabric"]]["add"]
    score += 5 if p["color"] == "colored" else 0
    score += 10 if p["size_cm"] > 10 else (5 if p["size_cm"] > 5 else 0)
    score = max(0, min(100, score))
    level = "easy" if score < 40 else "medium" if score < 60 else "hard" if score < 80 else "pro"
    level_th = {"easy": "ง่าย เอาอยู่", "medium": "พอไหว ทำตามขั้น", "hard": "ยาก ต้องใจเย็น", "pro": "ส่งมือโปร"}[level]
    dry = level == "pro" or (FABRICS[p["fabric"]]["delicate"] and score >= 60)
    fade = max(10, min(95, round(100 - score * 0.6)))
    return {"score": score, "level": level, "level_th": level_th, "dry_clean": dry,
            "expected_fade_pct": fade, "act_within_th": "ยิ่งเร็วยิ่งดี ภายใน 1 ชม. หายง่ายสุด",
            "disclaimer_th": "คะแนนและ % เป็นค่าประมาณจากกฎในแอป ไม่ใช่ผลรับประกัน"}


def _base_steps(p):
    c = p["cls"]
    delicate = FABRICS[p["fabric"]]["delicate"]
    blot = ("ซับคราบออกด้วยกระดาษ ห้ามขยี้", None, 1)
    soak = ("แช่ผงฟอกออกซิเจนน้ำอุ่น", "oxygen_bleach", 30) if not delicate else ("แช่น้ำเย็นกับน้ำยาซักผ้าถนอม", "gentle_detergent", 15)
    if c == "tannin":
        steps = [blot, ("ล้างน้ำเย็นจากด้านหลังผ้า", "water", 2), ("ถูเบา ๆ ด้วยน้ำยาล้างจาน", "dish_soap", 3), soak]
    elif c == "oil":
        steps = [blot, ("โรยเบกกิ้งโซดาให้ดูดน้ำมัน", "baking_soda", 15), ("ถูน้ำยาล้างจาน", "dish_soap", 5), ("ล้างน้ำอุ่น", "water", 2)]
    elif c == "oil_pigment":
        steps = [blot, ("โรยเบกกิ้งโซดาให้ดูดน้ำมัน", "baking_soda", 15), ("ถูน้ำยาล้างจาน", "dish_soap", 5), soak]
        if p["stain"] == "curry":
            steps.append(("ตากแดดหลังซัก แสงแดดช่วยให้สีขมิ้นจาง", None, 60))
    elif c == "protein":
        steps = [blot, ("ล้างน้ำเย็นเท่านั้น ห้ามน้ำร้อน", "water", 3), ("ถูน้ำยาล้างจาน", "dish_soap", 5), soak]
    elif c == "ink":
        steps = [blot, ("แตะแอลกอฮอล์ด้วยสำลี เปลี่ยนด้านกระดาษซับบ่อย ๆ", "alcohol", 5), ("ถูน้ำยาล้างจาน", "dish_soap", 3)]
    else:  # dirt
        steps = [("ปล่อยให้โคลนแห้งก่อน", None, 30), ("ปัดออกด้วยแปรง", "brush", 2), ("ถูน้ำยาล้างจาน", "dish_soap", 5)]
    steps.append(("ซักตามป้ายผ้า แล้วเช็กก่อนอบ (ความร้อนทำให้คราบติดถาวร)", None, 0))
    return steps


def rescue_plan(p, kit):
    if p["needs_confirm"]:
        raise ValueError("confirm stain type first")
    risk = risk_meter(p)
    kit = set(kit) | {"water"}
    if risk["dry_clean"]:
        raw = [("ซับคราบออกด้วยกระดาษ ห้ามขยี้", None, 1), ("แตะน้ำเย็นเบา ๆ จากด้านหลัง", "water", 2),
               ("ห่อผ้าแยก ส่งร้านซักแห้งภายใน 24 ชม. บอกชนิดคราบ", None, 0)]
    else:
        raw = _base_steps(p)
    steps, shop, used = [], [], []
    for i, (action, item, mins) in enumerate(raw, 1):
        missing, sub = False, None
        if item and item not in kit:
            missing = True
            if SUBSTITUTE.get(item) in kit:
                sub = SUBSTITUTE[item]
            else:
                shop.append(item)
        use = sub or (None if missing else item)
        if use:
            used.append(use)
        steps.append({"order": i, "action_th": action, "item": item, "minutes": mins, "missing": missing, "substitute": sub})
    warn = []
    if p["color"] == "colored" and any(s["item"] == "oxygen_bleach" or s["substitute"] for s in steps):
        warn.append("ผ้าสี: ทดสอบน้ำยากับตะเข็บด้านในก่อน 5 นาที")
    if p["cls"] == "protein":
        warn.append("คราบเลือด/โปรตีน ห้ามใช้น้ำร้อน จะทำให้คราบติดแน่น")
    warn.append("อย่าอบหรือรีดจนกว่าคราบจะหายหมด")
    return {"stain": p["stain"], "fabric": p["fabric"], "risk_level": risk["level"], "dry_clean": risk["dry_clean"],
            "steps": steps, "step_count": len(steps), "total_minutes": sum(s["minutes"] for s in steps),
            "items_used": sorted(set(used)), "shopping_list": sorted(set(shop)), "warnings_th": warn,
            "disclaimer_th": DISCLAIMER_TH}


def safety_check(items):
    s = set(items)
    pairs = [{"a": a, "b": b, "why_th": why} for a, b, why in FORBIDDEN if a in s and b in s]
    if pairs:
        return {"level": "danger", "pairs": pairs,
                "message_th": "ห้ามใช้ร่วมกันเด็ดขาด: " + " · ".join(f"{ITEMS[x['a']]} + {ITEMS[x['b']]} ({x['why_th']})" for x in pairs)}
    return {"level": "ok", "pairs": [], "message_th": "ไม่พบคู่น้ำยาอันตราย ใช้ทีละชนิดและล้างน้ำออกก่อนเปลี่ยนน้ำยา"}


def care_label(codes):
    if not codes:
        raise ValueError("no codes")
    lines, temps, flags = [], [], set()
    for c in codes:
        if c not in CARE:
            raise ValueError("unknown care code " + c)
        th, t = CARE[c]
        lines.append(th)
        if t is not None:
            temps.append(t)
        flags.add(c)
    bleach = "none" if "no_bleach" in flags else "oxygen_only" if "non_chlorine_bleach" in flags else "any"
    return {"codes": list(codes), "lines_th": lines, "max_wash_c": min(temps) if temps else None,
            "bleach": bleach, "dryer_ok": "no_tumble" not in flags,
            "dry_clean_only": "no_wash" in flags and "dry_clean" in flags}


def plan_fits_label(plan, label):
    issues = []
    if label["bleach"] == "none" and any((s["substitute"] or s["item"]) == "oxygen_bleach" and not s["missing"] for s in plan["steps"]):
        issues.append("ป้ายผ้าห้ามสารฟอก ข้ามขั้นแช่ผงฟอก")
    if label["dry_clean_only"]:
        issues.append("ป้ายผ้าให้ซักแห้งเท่านั้น ส่งร้านซักแห้ง")
    return {"ok": not issues, "issues_th": issues}


def kit_check(kit):
    kit = set(kit) | {"water"}
    ready = [k for k in STAINS if not rescue_plan(parse_stain(
        {"stain": k, "fabric": "cotton", "color": "white", "age_hours": 0.5, "size_cm": 3, "confidence": 0.9}), kit)["shopping_list"]]
    return {"kit": sorted(kit), "ready_for": ready, "ready_count": len(ready), "total": len(STAINS),
            "headline_th": f"ชุดในบ้านพร้อมรับมือ {len(ready)}/{len(STAINS)} คราบ"}


def diary_summary(entries):
    if not entries:
        raise ValueError("no entries")
    removed = [e for e in entries if e["result"] == "removed"]
    faded = [e for e in entries if e["result"] == "faded"]
    rate = round(100 * len(removed) / len(entries))
    saved = sum(e["value_baht"] for e in removed)
    return {"count": len(entries), "removed": len(removed), "faded": len(faded), "success_rate_pct": rate,
            "saved_baht": saved, "headline_th": f"กู้เสื้อรอดแล้ว {len(removed)} ตัว ประหยัดประมาณ ฿{saved:,}",
            "disclaimer_th": "มูลค่าเป็นราคาที่ผู้ใช้กรอกเอง"}


def share_card(item_th, stain_th, fade_pct):
    return {"title_th": "StainSOS ก่อน/หลัง", "headline_th": f"{item_th} รอดแล้ว!",
            "hook_th": f"คราบ{stain_th} จางไปประมาณ {fade_pct}% ใน 1 รอบ", "layout": "before_after",
            "sizes": ["1080x1350", "1080x1920"], "watermark": WATERMARK, "cta_th": "คอมเมนต์ STAIN รับแอปฟรี",
            "disclaimer_th": "ผลจริงขึ้นกับชนิดผ้าและอายุคราบ"}


def quota(used_today, want, pro=False):
    if want < 0 or used_today < 0:
        raise ValueError("negative")
    if pro:
        return {"allowed": want, "left_after": None, "paywall": False}
    left = max(0, FREE_SCANS_PER_DAY - used_today)
    allowed = min(left, want)
    return {"allowed": allowed, "left_after": left - allowed, "paywall": allowed < want}


def pipeline_steps(photo, parsed):
    s = ["stain_photo"]
    if photo["glare"] > 0.5:
        s.append("deglare")
    s += ["parse_stain"]
    if parsed["needs_confirm"]:
        s.append("ask_user_confirm")
        return s
    s += ["risk_meter", "rescue_plan", "safety_check"]
    return s


def safety_guard(level="ok"):
    if level == "danger":
        return {"level": "stop", "message_th": "หยุดก่อน มีน้ำยาที่ห้ามผสมกัน " + DISCLAIMER_TH}
    return {"level": "ok", "message_th": DISCLAIMER_TH}
