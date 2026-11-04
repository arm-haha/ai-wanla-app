"""LeafDoc (หมอใบไม้) — deterministic core engine. AI vision only proposes species/symptom tags; every score, cause, plan and date comes from here."""
from datetime import date, timedelta
VERSION = "leafdoc-engine/1.0.0"

def rnd(x):  # half-up rounding (NOT Python banker's round) — TS must use Math.floor(x + 0.5)
    return int(x + 0.5)

# id: (name_th, name_en, base_water_days, light_need, pet_toxic, humidity_lover, emoji)
SPECIES = {
    "monstera":  ("มอนสเตอร่า", "Monstera deliciosa", 7, "bright_indirect", True, True, "🌿"),
    "pothos":    ("พลูด่าง", "Golden pothos", 7, "medium", True, False, "🍃"),
    "snake":     ("ลิ้นมังกร", "Snake plant", 14, "low", True, False, "🗡️"),
    "zz":        ("กวักมรกต", "ZZ plant", 14, "low", True, False, "💎"),
    "rubber":    ("ยางอินเดีย", "Rubber plant", 8, "bright_indirect", True, False, "🌳"),
    "fiddle":    ("ไทรใบสัก", "Fiddle-leaf fig", 7, "bright_indirect", True, False, "🎻"),
    "fern":      ("เฟิร์นบอสตัน", "Boston fern", 3, "medium", False, True, "🌱"),
    "cactus":    ("แคคตัส", "Cactus", 21, "direct", False, False, "🌵"),
    "spider":    ("เศรษฐีเรือนใน", "Spider plant", 6, "medium", False, False, "🌾"),
}
LIGHT_ORDER = ["low", "medium", "bright_indirect", "direct"]
LIGHT_TH = {"low": "แสงน้อย", "medium": "แสงปานกลาง", "bright_indirect": "แสงสว่างรำไร", "direct": "แดดตรง"}
LIGHT_FACTOR = {"low": 1.4, "medium": 1.0, "bright_indirect": 0.85, "direct": 0.7}
POT_FACTOR = {"plastic": 1.0, "ceramic_glazed": 1.0, "terracotta": 0.8, "self_watering": 1.5}
def season_of(d):
    m = d.month
    return "hot" if m in (3, 4, 5) else "rainy" if m in (6, 7, 8, 9, 10) else "cool"
SEASON_FACTOR = {"hot": 0.8, "rainy": 1.2, "cool": 1.1}
SEASON_TH = {"hot": "หน้าร้อน", "rainy": "หน้าฝน", "cool": "หน้าหนาว"}

# id: (label_th, severity)
SYMPTOMS = {
    "yellow_lower": ("ใบล่างเหลือง", 10), "yellow_all": ("เหลืองทั้งต้น", 18), "brown_tips": ("ปลายใบไหม้น้ำตาล", 6),
    "crispy_edges": ("ขอบใบกรอบแห้ง", 10), "black_stem": ("โคนต้นดำนิ่ม", 25), "drooping": ("ใบตก ห้อย", 12),
    "leaf_drop": ("ใบร่วง", 12), "leggy": ("ยืดยาว ใบซีด", 10), "spots_halo": ("จุดน้ำตาลขอบเหลือง", 12),
    "webbing": ("ใยขาวใต้ใบ", 18), "sticky_bugs": ("เหนียว มีแมลงเกาะ", 14), "curling": ("ใบม้วน", 8),
    "mushy_base": ("โคนเน่าเละ มีกลิ่น", 28), "no_growth": ("ไม่แตกใบใหม่", 6), "sun_patches": ("รอยไหม้ขาวซีด", 10),
}
# cause id: (label_th, emoji, {symptom: weight}, explain_th)
CAUSES = {
    "overwater": ("รดน้ำมากไป", "💧", {"yellow_lower": 3, "drooping": 2, "mushy_base": 3, "black_stem": 2, "leaf_drop": 1}, "ดินแฉะนาน รากหายใจไม่ออก ใบล่างเลยเหลืองก่อน"),
    "root_rot": ("รากเน่า", "🦠", {"mushy_base": 4, "black_stem": 4, "drooping": 2, "yellow_all": 1}, "น้ำขังจนเชื้อราเข้าราก ต้องรีบผ่าตัดราก"),
    "underwater": ("ขาดน้ำ", "🏜️", {"drooping": 3, "crispy_edges": 3, "curling": 2, "leaf_drop": 1}, "ดินแห้งนานเกิน ใบเลยกรอบและม้วนเก็บน้ำ"),
    "low_light": ("แสงไม่พอ", "🌑", {"leggy": 4, "no_growth": 2, "yellow_lower": 1, "leaf_drop": 1}, "ต้นยืดหาแสง ใบใหม่เล็กและซีด"),
    "sunburn": ("โดนแดดแรงไป", "🔥", {"sun_patches": 4, "crispy_edges": 1, "curling": 1}, "แดดตรงเผาใบเป็นรอยขาวซีด"),
    "low_humidity": ("อากาศแห้ง/แอร์", "🌬️", {"brown_tips": 4, "curling": 1, "crispy_edges": 1}, "ห้องแอร์ความชื้นต่ำ ปลายใบเลยไหม้"),
    "spider_mites": ("ไรแดง", "🕷️", {"webbing": 5, "curling": 1, "yellow_all": 1}, "แมลงตัวจิ๋วดูดน้ำเลี้ยงใต้ใบ ชอบอากาศแห้ง"),
    "sap_bugs": ("เพลี้ย", "🐛", {"sticky_bugs": 5, "curling": 1, "yellow_lower": 1}, "เพลี้ยดูดน้ำเลี้ยง ทิ้งคราบเหนียว"),
    "leaf_spot": ("โรคใบจุด", "🍂", {"spots_halo": 5}, "เชื้อราที่ใบ ชอบใบเปียกและลมไม่ถ่ายเท"),
    "hungry": ("ขาดปุ๋ย", "🍽️", {"yellow_all": 3, "no_growth": 2, "leggy": 1}, "ดินเดิมนานจนธาตุอาหารหมด"),
}
GRADES = [(80, "thriving", "แข็งแรงดี", "🌿", "#22C55E"), (60, "fussy", "เริ่มงอแง", "🌤️", "#A3E635"),
          (40, "sick", "ป่วยอยู่", "🤒", "#FBBF24"), (0, "critical", "วิกฤต รีบช่วย", "🚑", "#C2410C")]

def water_interval(species, light, pot, on):
    base = SPECIES[species][2]
    f = LIGHT_FACTOR[light] * POT_FACTOR[pot] * SEASON_FACTOR[season_of(on)]
    return max(1, rnd(base * f))

def water_status(plant, on):
    iv = water_interval(plant["species"], plant["light"], plant["pot"], on)
    last = date.fromisoformat(plant["last_watered"])
    since = (on - last).days
    due = last + timedelta(days=iv)
    left = (due - on).days
    st = "overdue" if left < 0 else "today" if left == 0 else "soon" if left <= 1 else "ok"
    th = {"overdue": f"เลยกำหนด {-left} วัน", "today": "รดวันนี้", "soon": "พรุ่งนี้", "ok": f"อีก {left} วัน"}[st]
    nxt = [(due + timedelta(days=iv * k)).isoformat() for k in range(4)] if left >= 0 else [(on + timedelta(days=iv * k)).isoformat() for k in range(4)]
    return {"interval_days": iv, "days_since": since, "due_on": due.isoformat(), "days_left": left, "status": st, "status_th": th,
            "season": season_of(on), "next_dates": nxt, "finger_test_th": "จิ้มนิ้วลงดิน 2 ข้อ ถ้ายังชื้นให้เลื่อนไป 2 วัน"}

def context_bonus(cause, ctx, iv):
    soil, light, since = ctx["soil"], ctx["light"], ctx["days_since_water"]
    b = 0
    if cause in ("overwater", "root_rot", "leaf_spot"):
        b += {"wet": 3 if cause != "leaf_spot" else 1, "moist": 0, "dry": -3}[soil]
        if cause == "overwater" and since * 2 < iv: b += 2
    if cause == "underwater":
        b += {"wet": -3, "moist": 0, "dry": 3}[soil]
        if since * 2 > iv * 3: b += 2
    if cause == "low_light": b += {"low": 3, "medium": 0, "bright_indirect": -2, "direct": -2}[light]
    if cause == "sunburn": b += {"low": -3, "medium": -2, "bright_indirect": 0, "direct": 3}[light]
    if cause in ("low_humidity", "spider_mites") and ctx.get("ac_room"): b += 2
    if cause == "hungry" and ctx.get("months_since_feed", 0) >= 6: b += 2
    return b

def diagnose(plant, symptoms, ctx, on):
    sym = [s for s in SYMPTOMS if s in set(symptoms)]  # canonical order
    iv = water_interval(plant["species"], ctx["light"], plant["pot"], on)
    raw = []
    for cid, (lab, emo, w, why) in CAUSES.items():
        hit = [s for s in sym if s in w]
        if not hit: continue
        sc = sum(w[s] for s in hit) + context_bonus(cid, ctx, iv)
        if sc > 0: raw.append((cid, sc, hit))
    raw.sort(key=lambda r: (-r[1], list(CAUSES).index(r[0])))
    top = raw[:3]; tot = sum(r[1] for r in top)
    causes = [{"cause_id": c, "label_th": CAUSES[c][0], "emoji": CAUSES[c][1], "points": p, "confidence_pct": rnd(100 * p / tot),
               "evidence": h, "explain_th": CAUSES[c][3]} for c, p, h in top]
    if causes:  # make percentages add to exactly 100
        causes[0]["confidence_pct"] += 100 - sum(c["confidence_pct"] for c in causes)
    pen = sum(SYMPTOMS[s][1] for s in sym)
    sp = SPECIES[plant["species"]]
    if LIGHT_ORDER.index(ctx["light"]) < LIGHT_ORDER.index(sp[3]) - 1: pen += 5
    score = max(5, min(100, 100 - pen))
    g = next(g for g in GRADES if score >= g[0])
    return {"engine": VERSION, "plant_id": plant["id"], "species": plant["species"], "on": on.isoformat(), "symptoms": sym,
            "symptoms_th": [SYMPTOMS[s][0] for s in sym], "health_score": score, "grade": g[1], "grade_th": g[2], "emoji": g[3], "color": g[4],
            "causes": causes, "top_cause": causes[0]["cause_id"] if causes else None,
            "disclaimer_th": "ผลนี้เป็นการคาดเดาจากอาการ ไม่ใช่การตรวจในแล็บ ต้นมีค่ามากให้ปรึกษาร้านต้นไม้"}

PLANS = {
    "overwater": ["หยุดรดน้ำ ยกกระถางเช็กว่ารูระบายน้ำไม่ตัน", "ย้ายไปที่แสงรำไร ลมผ่าน ให้ดินแห้งเร็วขึ้น", "ตัดใบเหลืองที่โคนออก (กรรไกรสะอาด)",
                  "จิ้มนิ้วเช็กดิน 2 ข้อ ยังแฉะ = ยังไม่รด", "ถ้าดินยังแฉะ เปลี่ยนเป็นดินโปร่ง (ดิน+เพอร์ไลต์+เปลือกสน)", "รดครั้งแรกเมื่อดินแห้ง 2 ข้อ รดจนไหลออกรู แล้วเทน้ำในจานรองทิ้ง", "ถ่ายรูปมุมเดิมเทียบวันแรก 📸"],
    "root_rot": ["ถอดกระถาง ล้างดินออกดูราก", "ตัดรากดำนิ่มทิ้งให้หมด (เหลือแต่รากขาวแน่น)", "ผึ่งรากให้แห้ง 1 วันในที่ร่ม",
                 "ลงดินใหม่โปร่ง ๆ ในกระถางมีรูระบาย", "ยังไม่รดน้ำ ให้รากสมานแผล", "รดน้ำน้อย ๆ ครั้งแรก", "ถ่ายรูปมุมเดิมเทียบวันแรก 📸"],
    "underwater": ["รดแบบแช่ก้น: วางกระถางในกะละมังน้ำ 20 นาที", "ปลิดใบกรอบที่แห้งตายออก", "ตั้งเตือนรดน้ำตามรอบในแอป",
                   "คลุมหน้าดินด้วยกาบมะพร้าวสับช่วยเก็บความชื้น", "เช็กดิน ถ้าแห้ง 2 ข้อให้รดจนไหลออกรู", "ดูว่าใบเริ่มตั้งขึ้นไหม", "ถ่ายรูปมุมเดิมเทียบวันแรก 📸"],
    "low_light": ["ย้ายใกล้หน้าต่าง (ห่าง 1 เมตร ไม่โดนแดดตรง)", "ใช้ Light Meter ในแอปวัดมุมใหม่", "หมุนกระถาง 1/4 รอบให้โดนแสงทั่ว",
                  "ลดน้ำลงนิดเพราะแสงน้อยดินแห้งช้า", "ถ้าไม่มีหน้าต่าง ลองไฟปลูกต้นไม้ 12 ชม./วัน", "เช็ดฝุ่นบนใบให้รับแสงเต็มที่", "ถ่ายรูปมุมเดิมเทียบวันแรก 📸"],
    "sunburn": ["ถอยออกจากแดดตรง หรือกั้นม่านบาง", "ใบที่ไหม้แล้วไม่กลับมาเขียว ตัดได้ถ้าเสียเกินครึ่ง", "รดน้ำตามรอบ อย่าให้ดินแห้งสนิท",
                "วัดแสงมุมใหม่ด้วย Light Meter", "ดูใบใหม่ว่าไม่มีรอยซีด", "ค่อย ๆ ปรับแสงทีละน้อยถ้าจะย้ายกลับ", "ถ่ายรูปมุมเดิมเทียบวันแรก 📸"],
    "low_humidity": ["ย้ายให้ห่างช่องลมแอร์", "จับกลุ่มต้นไม้ไว้ใกล้กันเพิ่มความชื้น", "วางถาดกรวด+น้ำใต้กระถาง",
                     "เล็มปลายใบไหม้ตามรูปทรงใบ", "พ่นละอองน้ำตอนเช้า (ไม่พ่นตอนเย็น)", "เช็กใต้ใบหาไรแดง", "ถ่ายรูปมุมเดิมเทียบวันแรก 📸"],
    "spider_mites": ["แยกต้นออกห่างต้นอื่นทันที", "ล้างใต้ใบด้วยฝักบัวแรงพอดี", "เช็ดใต้ใบด้วยน้ำสบู่อ่อน ๆ",
                     "ทำซ้ำ: ล้างใต้ใบอีกรอบ", "เพิ่มความชื้นรอบต้น", "ทำซ้ำ: เช็ดน้ำสบู่อีกรอบ", "ถ่ายรูปใต้ใบเทียบวันแรก 📸"],
    "sap_bugs": ["แยกต้นออกห่างต้นอื่นทันที", "ใช้สำลีชุบแอลกอฮอล์เช็ดตัวเพลี้ยออก", "ล้างคราบเหนียวด้วยน้ำสบู่อ่อน ๆ",
                 "เช็กซอกใบและใต้ใบอีกรอบ", "ทำซ้ำ: เช็ดแอลกอฮอล์", "ดูมดเดินขึ้นต้นไหม (มดพาเพลี้ยมา)", "ถ่ายรูปเทียบวันแรก 📸"],
    "leaf_spot": ["ตัดใบที่เป็นจุดทิ้ง (ไม่ทิ้งในกระถาง)", "หยุดพ่นน้ำโดนใบ รดที่โคนแทน", "ย้ายไปที่ลมถ่ายเท",
                  "เช็กว่ามีใบใหม่เป็นจุดไหม", "เว้นระยะห่างจากต้นอื่น", "รดน้ำตอนเช้าเท่านั้น", "ถ่ายรูปเทียบวันแรก 📸"],
    "hungry": ["ให้ปุ๋ยละลายช้าตามฉลาก (ครึ่งอัตราก่อน)", "รดน้ำให้ทั่วหลังให้ปุ๋ย", "ดูว่ารากล้นกระถางไหม",
               "ถ้ารากแน่น เตรียมเปลี่ยนกระถางใหญ่ขึ้น 1 ไซซ์", "อย่าให้ปุ๋ยซ้ำเกินฉลาก", "เช็ดใบให้สะอาด", "ถ่ายรูปเทียบวันแรก 📸"],
}
HEALTHY_PLAN = ["รดน้ำตามรอบในแอป", "หมุนกระถาง 1/4 รอบ", "เช็ดฝุ่นบนใบ", "เช็กใต้ใบหาแมลง", "ดูว่ามีใบใหม่ไหม", "พักผ่อน ไม่ต้องทำอะไร 😌", "ถ่ายรูปบันทึกการเติบโต 📸"]

def rescue_plan(dx, start):
    st = date.fromisoformat(start)
    steps = PLANS[dx["top_cause"]] if dx["top_cause"] else HEALTHY_PLAN
    second = dx["causes"][1]["cause_id"] if len(dx["causes"]) > 1 else None
    days = []
    for i, s in enumerate(steps):
        d = {"day": i + 1, "on": (st + timedelta(days=i)).isoformat(), "task_th": s, "done": False}
        days.append(d)
    if second:  # one extra tip from the runner-up cause on day 3
        days[2]["extra_th"] = "เผื่อไว้ (" + CAUSES[second][0] + "): " + PLANS[second][0]
    return {"plant_id": dx["plant_id"], "cause_id": dx["top_cause"], "title_th": f"แผนชุบชีวิต 7 วัน: {CAUSES[dx['top_cause']][0]}" if dx["top_cause"] else "แผนดูแล 7 วัน",
            "start_on": start, "days": days, "recheck_on": (st + timedelta(days=7)).isoformat()}

def plan_progress(plan, done_days):
    n = sum(1 for d in plan["days"] if d["day"] in set(done_days))
    return {"done": n, "of": len(plan["days"]), "pct": rnd(100 * n / len(plan["days"]))}

def light_reading(lux):
    band = "low" if lux < 500 else "medium" if lux < 2000 else "bright_indirect" if lux < 10000 else "direct"
    if band == "direct": fits = [k for k, v in SPECIES.items() if v[3] == "direct"]
    else: fits = [k for k, v in SPECIES.items() if v[3] != "direct" and abs(LIGHT_ORDER.index(v[3]) - LIGHT_ORDER.index(band)) <= 1]
    return {"lux_est": lux, "band": band, "band_th": LIGHT_TH[band], "fits": fits, "note_th": "ค่าประมาณจากกล้องมือถือ ใช้เทียบมุมในบ้าน ไม่ใช่เครื่องวัดจริง"}

def lux_from_luma(mean_luma, exposure_ev=0.0):
    """mean_luma 0-255 from a 64x64 downscaled camera frame. Rough log mapping, fixed so TS matches."""
    return rnd(10 * (2 ** (mean_luma / 20.0)) * (2 ** exposure_ev))

def pet_check(species):
    t = SPECIES[species][4]
    return {"species": species, "pet_toxic": t, "badge_th": "⚠️ อันตรายต่อแมว/หมา ถ้ากัดกิน" if t else "✅ ค่อนข้างปลอดภัยกับสัตว์เลี้ยง",
            "verified": False, "source_note": "ตรวจกับรายชื่อพืชของ ASPCA ก่อนปล่อยแอป"}

def room_match(ans):
    """ans: light band, ac_room bool, pets bool, forgetful bool → ranked species."""
    out = []
    for k, (th, en, wd, need, toxic, humid, emo) in SPECIES.items():
        s = 50 - 25 * abs(LIGHT_ORDER.index(need) - LIGHT_ORDER.index(ans["light"]))
        if ans["pets"] and toxic: s -= 30
        if ans["forgetful"]: s += 15 if wd >= 14 else -15 if wd <= 3 else 0
        if ans["ac_room"] and humid: s -= 10
        out.append({"species": k, "name_th": th, "emoji": emo, "fit": max(0, min(100, s * 2))})
    out.sort(key=lambda r: (-r["fit"], list(SPECIES).index(r["species"])))
    return out[:3]

def glow_up(before, after, new_leaves):
    d = after["health_score"] - before["health_score"]
    days = (date.fromisoformat(after["on"]) - date.fromisoformat(before["on"])).days
    return {"kind": "glow_up", "size": "1080x1920", "plant_id": before["plant_id"], "before_on": before["on"], "after_on": after["on"], "days": days,
            "before_score": before["health_score"], "after_score": after["health_score"], "delta": d, "new_leaves": new_leaves,
            "headline_th": f"{days} วัน จาก {before['health_score']} → {after['health_score']} {after['emoji']}",
            "sub_th": f"ใบใหม่ {new_leaves} ใบ · รอดแล้ว!" if d > 0 else "ยังสู้ต่อ 💪", "bg": "#14532D", "accent": "#A3E635", "footer": "ทำด้วย LeafDoc · AI วันละแอป"}

def care_streak(days_list, today):
    s = set(days_list); n = 0; d = date.fromisoformat(today)
    while d.isoformat() in s: n += 1; d -= timedelta(days=1)
    return n

def jungle_level(n_plants, waterings_on_time, checkups):
    xp = n_plants * 20 + waterings_on_time * 5 + checkups * 10
    lv = [(0, 1, "มือใหม่หัดปลูก"), (100, 2, "สายเขียวฝึกหัด"), (250, 3, "คุณพ่อ/แม่ต้นไม้"), (500, 4, "เจ้าป่าคอนโด"), (1000, 5, "หมอใบไม้ตัวจริง")]
    cur = [l for l in lv if xp >= l[0]][-1]
    nxt = next((l for l in lv if l[0] > xp), None)
    return {"xp": xp, "level": cur[1], "title_th": cur[2], "next_at": nxt[0] if nxt else None}

def plant_wrapped(log, month):
    m = [e for e in log if e["on"].startswith(month)]
    w = [e for e in m if e["kind"] == "water"]; c = [e for e in m if e["kind"] == "checkup"]
    on_time = sum(1 for e in w if e.get("on_time"))
    causes = [e["top_cause"] for e in c if e.get("top_cause")]
    top = max(sorted(set(causes)), key=causes.count) if causes else None
    best = max(c, key=lambda e: e.get("delta", 0)) if c else None
    return {"month": month, "waterings": len(w), "on_time_pct": rnd(100 * on_time / len(w)) if w else 0, "checkups": len(c),
            "top_cause": top, "top_cause_th": CAUSES[top][0] if top else None,
            "best_glow_plant": best["plant_id"] if best and best.get("delta", 0) > 0 else None, "best_delta": best.get("delta", 0) if best else 0}
