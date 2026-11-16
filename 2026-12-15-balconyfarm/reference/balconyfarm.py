"""BalconyFarm deterministic logic (no AI calls). Balcony kitchen-garden planner — sun hours, loads, prices and savings are estimates only."""
import math, datetime as _dt

# Base direct-sun hours/day for an open balcony in central Thailand (~14°N), by facing (illustrative figures).
FACING = {"n": 2.0, "ne": 3.0, "e": 4.5, "se": 5.5, "s": 6.0, "sw": 5.5, "w": 4.5, "nw": 3.0}
FACING_TH = {"n": "ทิศเหนือ", "ne": "ทิศตะวันออกเฉียงเหนือ", "e": "ทิศตะวันออก", "se": "ทิศตะวันออกเฉียงใต้", "s": "ทิศใต้",
             "sw": "ทิศตะวันตกเฉียงใต้", "w": "ทิศตะวันตก", "nw": "ทิศตะวันตกเฉียงเหนือ"}
LIGHT_TH = {"full": "แดดเต็ม", "partial": "ครึ่งแดด", "shade": "ร่มรำไร"}
# plant: th, min/max sun h, good months, pot diameter cm, wet weight kg per pot, water every N days (baseline),
# days to first harvest, THB saved per month (vs buying), seedling/seed cost THB, pot cost THB, soil litres
PLANTS = {
    "kaprao":       {"th": "กะเพรา",       "sun": (4, 8), "months": list(range(1, 13)), "pot_cm": 25, "kg": 6,  "water": 1, "harvest": 45,  "save": 60, "seed": 25, "pot": 45,  "soil": 8},
    "horapha":      {"th": "โหระพา",       "sun": (3, 8), "months": list(range(1, 13)), "pot_cm": 25, "kg": 6,  "water": 1, "harvest": 40,  "save": 50, "seed": 25, "pot": 45,  "soil": 8},
    "chili":        {"th": "พริกขี้หนู",     "sun": (5, 8), "months": list(range(1, 13)), "pot_cm": 30, "kg": 10, "water": 2, "harvest": 75,  "save": 40, "seed": 30, "pot": 60,  "soil": 15},
    "spring_onion": {"th": "ต้นหอม",       "sun": (3, 6), "months": list(range(1, 13)), "pot_cm": 20, "kg": 4,  "water": 1, "harvest": 30,  "save": 40, "seed": 20, "pot": 35,  "soil": 5},
    "coriander":    {"th": "ผักชี",         "sun": (3, 6), "months": [11, 12, 1, 2],     "pot_cm": 20, "kg": 4,  "water": 1, "harvest": 40,  "save": 50, "seed": 20, "pot": 35,  "soil": 5},
    "lemongrass":   {"th": "ตะไคร้",        "sun": (5, 8), "months": list(range(1, 13)), "pot_cm": 30, "kg": 10, "water": 2, "harvest": 90,  "save": 30, "seed": 20, "pot": 60,  "soil": 15},
    "kaffir_lime":  {"th": "มะกรูด",        "sun": (5, 8), "months": list(range(1, 13)), "pot_cm": 40, "kg": 25, "water": 2, "harvest": 180, "save": 30, "seed": 120, "pot": 120, "soil": 30},
    "mint":         {"th": "สะระแหน่",      "sun": (2, 5), "months": list(range(1, 13)), "pot_cm": 20, "kg": 4,  "water": 1, "harvest": 30,  "save": 40, "seed": 20, "pot": 35,  "soil": 5},
    "morning_glory": {"th": "ผักบุ้ง",       "sun": (5, 8), "months": list(range(1, 13)), "pot_cm": 35, "kg": 12, "water": 1, "harvest": 21,  "save": 60, "seed": 15, "pot": 70,  "soil": 10},
    "lettuce":      {"th": "ผักสลัด",        "sun": (3, 5), "months": [11, 12, 1, 2],     "pot_cm": 25, "kg": 5,  "water": 1, "harvest": 35,  "save": 80, "seed": 30, "pot": 45,  "soil": 6},
    "cherry_tomato": {"th": "มะเขือเทศเชอร์รี", "sun": (6, 8), "months": [10, 11, 12, 1, 2], "pot_cm": 35, "kg": 15, "water": 1, "harvest": 70, "save": 70, "seed": 30, "pot": 70, "soil": 20},
    "pandan":       {"th": "ใบเตย",         "sun": (1, 4), "months": list(range(1, 13)), "pot_cm": 25, "kg": 7,  "water": 2, "harvest": 60,  "save": 20, "seed": 30, "pot": 45,  "soil": 8},
}
SEASON_WATER = {"hot": 0.7, "rainy": 1.5, "cool": 1.2}
SOIL_BAHT_PER_L = 3
LOAD_LIMIT_KG_M2 = 150      # conservative example figure; check the building's spec / juristic office
WALKWAY_M = 0.6
DISCLAIMER = "ชั่วโมงแดด น้ำหนัก ราคา และเงินที่ประหยัดเป็นค่าประมาณ ตรวจกฎคอนโดและอย่าวางกระถางบนหรือนอกราวระเบียง"


def _rng(x, lo, hi, name):
    if isinstance(x, bool) or not isinstance(x, (int, float)) or x < lo or x > hi:
        raise ValueError(f"{name} out of range")


def _plant(p):
    if p not in PLANTS: raise ValueError(f"unknown plant {p}")
    return PLANTS[p]


def season(month):
    _rng(month, 1, 12, "month")
    return "hot" if month in (3, 4, 5) else ("rainy" if 6 <= month <= 10 else "cool")


def scan_quality(glare, blur, crop):
    for v, n in ((glare, "glare"), (blur, "blur"), (crop, "crop")):
        _rng(v, 0, 1, n)
    score = round(100 - glare * 35 - blur * 40 - crop * 25)
    tips = []
    if glare > 0.3: tips.append("ย้อนแสงเกินไป หันหลังให้ดวงอาทิตย์แล้วถ่ายใหม่")
    if blur > 0.3: tips.append("ภาพเบลอ ถือนิ่ง ๆ แล้วถ่ายใหม่")
    if crop > 0.3: tips.append("ถ่ายให้เห็นระเบียงทั้งความกว้าง ตั้งแต่พื้นถึงราว")
    return {"score": max(0, score), "ok": score >= 70, "tips_th": tips}


def balcony_scan(photo):
    return {"photo_id": photo["id"], "quality": scan_quality(photo["glare"], photo["blur"], photo["crop"])}


def sun_estimate(facing, obstruction, overhang_m, floor):
    if facing not in FACING: raise ValueError("facing")
    _rng(obstruction, 0, 1, "obstruction"); _rng(overhang_m, 0, 3, "overhang_m"); _rng(floor, 1, 80, "floor")
    eff_obs = obstruction * (0.6 if floor >= 10 else 1.0)
    hours = round(FACING[facing] * (1 - eff_obs) * (1 - min(0.6, overhang_m * 0.15)), 1)
    light = "full" if hours >= 5 else ("partial" if hours >= 3 else "shade")
    hot = facing in ("w", "sw")
    note = "แดดบ่ายร้อนจัด ใช้กระถางสีอ่อนและรดน้ำเช้า-เย็น" if hot else ("แดดเช้าอ่อนโยน เหมาะกับผักใบ" if facing in ("e", "se", "ne") else "แสงสม่ำเสมอ")
    return {"facing": facing, "facing_th": FACING_TH[facing], "sun_hours": hours, "light": light, "light_th": LIGHT_TH[light],
            "hot_afternoon": hot, "note_th": note, "headline_th": f"{FACING_TH[facing]} แดดตรงประมาณ {hours} ชม./วัน → {LIGHT_TH[light]}"}


def plant_fit(plant, sun_hours, month):
    p = _plant(plant); lo, hi = p["sun"]
    if lo <= sun_hours <= hi: light = 1.0
    elif lo - 1 <= sun_hours < lo or hi < sun_hours <= hi + 1: light = 0.5
    else: light = 0.0
    seas = month in p["months"]
    score = round((light * 0.7 + (0.3 if seas else 0)) * 100)
    why = []
    if light == 1.0: why.append("แดดพอดี")
    elif light == 0.5: why.append("แดดเกือบพอ" if sun_hours < lo else "แดดเยอะไปนิด")
    else: why.append("แดดไม่เหมาะ")
    why.append("ตรงฤดู" if seas else "นอกฤดู โตช้า")
    return {"plant": plant, "plant_th": p["th"], "score": score, "light_fit": light, "in_season": seas, "why_th": " · ".join(why)}


def plant_picks(sun, month, top=5, exclude=()):
    _rng(top, 1, 12, "top")
    fits = [plant_fit(k, sun["sun_hours"], month) for k in PLANTS if k not in exclude]
    fits.sort(key=lambda f: (-f["score"], -PLANTS[f["plant"]]["save"], PLANTS[f["plant"]]["harvest"], f["plant"]))
    picks = [f for f in fits if f["score"] >= 50][:top]
    if not picks: raise ValueError("no suitable plants for this light")
    return {"sun_hours": sun["sun_hours"], "light": sun["light"], "month": month, "picks": picks,
            "headline_th": "แนะนำ " + " ".join(f["plant_th"] for f in picks[:3])}


def layout(width_m, depth_m, plants):
    """Pots in rows along the railing side, leaving a WALKWAY_M walkway. plants = list of keys (one pot each)."""
    _rng(width_m, 0.6, 20, "width_m"); _rng(depth_m, 0.6, 10, "depth_m")
    if not plants: raise ValueError("no plants")
    usable_d = round(depth_m - WALKWAY_M, 2)
    if usable_d < 0.2: raise ValueError("balcony too shallow — use wall/hanging planters")
    W = int(width_m * 100); D = int(usable_d * 100)
    order = sorted(plants, key=lambda k: (-_plant(k)["pot_cm"], k))
    placed, skipped, x, y, row_h = [], [], 0, 0, 0
    for k in order:
        c = PLANTS[k]["pot_cm"]
        if x + c > W: x, y, row_h = 0, y + row_h, 0
        if y + c > D: skipped.append(k); continue
        placed.append({"plant": k, "x_cm": x, "y_cm": y, "pot_cm": c}); x += c; row_h = max(row_h, c)
    kg = sum(PLANTS[p["plant"]]["kg"] for p in placed)
    load = round(kg / (width_m * usable_d), 1)
    status = "ok" if load <= LOAD_LIMIT_KG_M2 * 0.6 else ("warn" if load <= LOAD_LIMIT_KG_M2 else "over")
    msg = {"ok": "น้ำหนักรวมสบาย ๆ", "warn": "ค่อนข้างหนัก กระจายกระถางชิดผนัง ไม่วางกองรวม", "over": "หนักเกินค่าแนะนำ ลดกระถางใหญ่หรือถามนิติบุคคล"}[status]
    return {"width_m": width_m, "depth_m": depth_m, "usable_depth_m": usable_d, "walkway_m": WALKWAY_M, "pots": placed, "skipped": skipped,
            "total_wet_kg": kg, "load_kg_m2": load, "load_limit_kg_m2": LOAD_LIMIT_KG_M2, "load_status": status, "load_th": msg}


def water_plan(plants, month, facing, today, sun_hours=5.0, days=7):
    _rng(days, 1, 14, "days"); _rng(sun_hours, 0, 12, "sun_hours")
    if not plants: raise ValueError("no plants")
    if facing not in FACING: raise ValueError("facing")
    sf = SEASON_WATER[season(month)] * (0.8 if facing in ("w", "sw") else 1.0) * (1.0 if sun_hours >= 5 else (1.3 if sun_hours >= 3 else 1.6))
    every = {k: max(1, round(_plant(k)["water"] * sf)) for k in dict.fromkeys(plants)}
    t = _dt.date.fromisoformat(today); out = []
    for d in range(days):
        out.append({"date": (t + _dt.timedelta(days=d)).isoformat(), "water": [k for k in every if d % every[k] == 0]})
    return {"season": season(month), "every_days": every, "days": out, "tip_th": "รดน้ำเช้าก่อน 9 โมง เช็กดินด้วยนิ้ว ถ้ายังชื้นข้ามได้"}


def harvest_plan(plants, planted):
    if not plants: raise ValueError("no plants")
    t = _dt.date.fromisoformat(planted); items = []
    for k in dict.fromkeys(plants):
        p = _plant(k)
        items.append({"plant": k, "plant_th": p["th"], "first_harvest": (t + _dt.timedelta(days=p["harvest"])).isoformat(), "days": p["harvest"]})
    items.sort(key=lambda i: (i["days"], i["plant"]))
    save = sum(_plant(k)["save"] for k in plants)
    return {"planted": planted, "items": items, "first_up": items[0]["plant_th"], "saves_baht_month": save,
            "headline_th": f"เก็บ{items[0]['plant_th']}ได้ก่อนใน {items[0]['days']} วัน ประหยัดค่าผักราว ฿{save}/เดือน"}


def shopping_list(plants):
    if not plants: raise ValueError("no plants")
    rows = {}
    for k in plants:
        p = _plant(k)
        r = rows.setdefault(k, {"plant": k, "plant_th": p["th"], "pots": 0, "pot_cm": p["pot_cm"], "soil_l": 0, "cost_baht": 0})
        r["pots"] += 1; r["soil_l"] += p["soil"]; r["cost_baht"] += p["seed"] + p["pot"] + p["soil"] * SOIL_BAHT_PER_L
    items = list(rows.values()); total = sum(r["cost_baht"] for r in items)
    save = sum(_plant(k)["save"] for k in plants)
    return {"items": items, "soil_total_l": sum(r["soil_l"] for r in items), "total_baht": total, "payback_months": round(total / save, 1),
            "disclaimer_th": "ราคาเป็นค่าตัวอย่าง ร้านจริงอาจต่างกัน"}


def mockup_spec(sun, picks, style="tropical_cafe"):
    styles = {"tropical_cafe": "cozy tropical cafe style, wooden shelf, warm string lights", "minimal_white": "minimal white pots, clean lines",
              "thai_retro": "terracotta and enamel pots, rattan stool, Thai retro"}
    if style not in styles: raise ValueError("style")
    names = ", ".join(f["plant"].replace("_", " ") for f in picks["picks"])
    return {"style": style, "plants": [f["plant"] for f in picks["picks"]], "image_prompt":
            f"same condo balcony from the photo, {sun['light']} sun, potted kitchen herbs: {names}; {styles[style]}; all pots inside the railing on the floor, "
            "photorealistic 4:5, keep walls and railing unchanged, no people, no logos", "disclaimer_th": "ภาพจำลอง ต้นไม้จริงต้องใช้เวลาโต"}


def diary_summary(entries, today):
    if not entries: raise ValueError("empty diary")
    days = sorted({e["date"] for e in entries}, reverse=True)
    t = _dt.date.fromisoformat(today); streak = 0
    for i, d in enumerate(days):
        if _dt.date.fromisoformat(d) == t - _dt.timedelta(days=i): streak += 1
        else: break
    g = sum(e.get("grams", 0) for e in entries if e["action"] == "harvest")
    return {"entries": len(entries), "streak_days": streak, "harvest_g": g, "saved_baht": round(g * 0.12),
            "headline_th": f"ดูแลต่อเนื่อง {streak} วัน เก็บผักได้ {g} กรัม ประหยัด ~฿{round(g * 0.12)}"}


def share_card(sun, picks, hook_th):
    return {"title_th": f"ระเบียง{sun['light_th']} ปลูกได้ {len(picks['picks'])} อย่าง", "hook_th": hook_th, "layout": "balcony_before_after",
            "sizes": ["1080x1350", "1080x1920"], "watermark": "BalconyFarm · AI วันละแอป", "cta_th": "คอมเมนต์ FARM รับแพ็กฟรี", "disclaimer_th": "ภาพจำลอง ค่าประมาณ"}


def quota(used_today, free_per_day=3, pro=False):
    _rng(used_today, 0, 10000, "used_today")
    if pro: return {"allowed": 1, "left_after": None, "paywall": False}
    left = free_per_day - used_today
    return {"allowed": 1 if left > 0 else 0, "left_after": max(left - 1, 0), "paywall": left <= 0}


def safety_guard(flag=None):
    msgs = {None: ("ok", "วางกระถางบนพื้นด้านในราวเท่านั้น ใช้จานรองกันน้ำหยดใส่ห้องล่าง"),
            "railing": ("stop", "ห้ามแขวนหรือวางกระถางบนราว/นอกราว เสี่ยงตกใส่คนข้างล่าง"),
            "overload": ("warn", "น้ำหนักเกินค่าแนะนำ ลดกระถางใหญ่และสอบถามนิติบุคคลก่อน"),
            "pesticide": ("warn", "ผักกินเอง เลี่ยงสารเคมี ใช้น้ำส้มควันไม้/สบู่อ่อนเจือจาง และล้างก่อนกิน"),
            "not_balcony": ("stop", "ไม่พบระเบียงในรูป ถ่ายใหม่ให้เห็นพื้นและราว")}
    if flag not in msgs: raise ValueError("flag")
    lv, m = msgs[flag]
    return {"level": lv, "message_th": m}
