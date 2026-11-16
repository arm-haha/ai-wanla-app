"""RipeRight deterministic logic (no AI calls). Fruit ripeness meter + market helper — every result is an estimate, not a food-safety guarantee."""
import math, datetime as _dt

# Per-fruit model. w = weights for cues (color, firm, aroma, spots, knock) summing to 1.
# ripen_days = days on the counter from hard-green (index 0) to "perfect" (index 0.65).
# price = example in-season THB/kg range (illustrative figures, not live market data).
FRUITS = {
    "durian":     {"th": "ทุเรียนหมอนทอง",   "w": (0.15, 0.30, 0.30, 0.05, 0.20), "ripen_days": 4, "fridge_ok": True,  "price": (120, 180), "season": [4, 5, 6, 7], "knock": True},
    "mango":      {"th": "มะม่วงน้ำดอกไม้",   "w": (0.45, 0.30, 0.15, 0.10, 0.00), "ripen_days": 5, "fridge_ok": True,  "price": (40, 80),   "season": [2, 3, 4, 5], "knock": False},
    "avocado":    {"th": "อะโวคาโด",         "w": (0.25, 0.60, 0.00, 0.15, 0.00), "ripen_days": 5, "fridge_ok": True,  "price": (80, 150),  "season": [7, 8, 9, 10, 11], "knock": False},
    "banana":     {"th": "กล้วยหอม",         "w": (0.55, 0.15, 0.10, 0.20, 0.00), "ripen_days": 3, "fridge_ok": False, "price": (25, 45),   "season": list(range(1, 13)), "knock": False},
    "watermelon": {"th": "แตงโม",            "w": (0.35, 0.00, 0.00, 0.05, 0.60), "ripen_days": 0, "fridge_ok": True,  "price": (15, 30),   "season": [11, 12, 1, 2, 3, 4], "knock": True},
    "papaya":     {"th": "มะละกอฮอลแลนด์",    "w": (0.55, 0.25, 0.10, 0.10, 0.00), "ripen_days": 4, "fridge_ok": True,  "price": (15, 30),   "season": list(range(1, 13)), "knock": False},
    "pineapple":  {"th": "สับปะรดภูแล",       "w": (0.45, 0.10, 0.35, 0.10, 0.00), "ripen_days": 2, "fridge_ok": True,  "price": (15, 35),   "season": [4, 5, 6, 12, 1], "knock": False},
    "mangosteen": {"th": "มังคุด",            "w": (0.45, 0.40, 0.00, 0.15, 0.00), "ripen_days": 3, "fridge_ok": True,  "price": (40, 90),   "season": [5, 6, 7, 8], "knock": False},
}
FIRMNESS = {"hard": 0.0, "firm": 0.35, "yielding": 0.7, "soft": 0.9, "mushy": 1.0}
AROMA = {"none": 0.0, "faint": 0.5, "strong": 1.0}
STAGES = [(0.35, "unripe", "ยังดิบ"), (0.60, "almost", "ใกล้สุก"), (0.85, "perfect", "สุกพอดี"), (9, "overripe", "สุกเกิน")]
PERFECT = 0.65
OFF_SEASON_MULT = 1.4
CHECKLISTS = {
    "durian": ["ก้านยังเขียวสด ไม่เหี่ยว", "บีบหนาม 2 อันเข้าหากันได้ (หนามอ่อน)", "เคาะแล้วเสียงโปร่ง ๆ", "ร่องพูชัด"],
    "mango": ["ผิวเหลืองทั่วลูก", "กดเบา ๆ แล้วนิ่มนิดหน่อย", "ขั้วมีกลิ่นหอม", "ไม่มีจุดช้ำดำ"],
    "avocado": ["เปลือกเริ่มเข้มขึ้น", "กดแล้วยุบเล็กน้อย", "แงะขั้วแล้วข้างในเขียว", "ไม่มีรอยบุบ"],
    "banana": ["เหลืองทั้งลูก", "มีจุดน้ำตาลเล็ก ๆ (กระ)", "ไม่มีรอยดำช้ำใหญ่", "ขั้วไม่เน่า"],
    "watermelon": ["มีจุดเหลืองตรงที่วางกับดิน", "ลายเขียวเข้มชัด", "เคาะแล้วเสียงทุ้มก้อง", "หนักกว่าที่คิดเมื่อยก"],
    "papaya": ["ผิวเหลืองเกินครึ่งลูก", "กดแล้วนิ่มนิดหน่อย", "ไม่มีจุดดำยุบ", "ไม่มียางไหล"],
    "pineapple": ["ตาผลใหญ่ เรียบ", "ผิวเหลืองจากก้นขึ้นมา", "ก้นมีกลิ่นหอมหวาน", "ดึงใบกลางออกได้ง่าย"],
    "mangosteen": ["เปลือกม่วงเข้ม", "กดเปลือกแล้วยุบได้เล็กน้อย", "กลีบเลี้ยงยังเขียว", "ไม่มียางเหลืองที่เปลือก"],
}
DISCLAIMER = "ผลเป็นค่าประมาณจากรูปและคำตอบของคุณ ไม่ใช่การรับรองความปลอดภัยของอาหาร ถ้ามีรา กลิ่นบูด หรือเนื้อเละผิดปกติ ห้ามกิน"


def _rng(x, lo, hi, name):
    if isinstance(x, bool) or not isinstance(x, (int, float)) or x < lo or x > hi:
        raise ValueError(f"{name} out of range")


def _fruit(f):
    if f not in FRUITS: raise ValueError(f"unknown fruit {f}")
    return FRUITS[f]


def _date(s):
    return _dt.date.fromisoformat(s)


def scan_quality(glare, blur, crop):
    for v, n in ((glare, "glare"), (blur, "blur"), (crop, "crop")):
        _rng(v, 0, 1, n)
    score = round(100 - glare * 35 - blur * 40 - crop * 25)
    tips = []
    if glare > 0.3: tips.append("แสงสะท้อนเยอะ ย้ายไปถ่ายใต้แสงธรรมชาติ ไม่ใช้แฟลช")
    if blur > 0.3: tips.append("ภาพเบลอ ถือนิ่ง ๆ แตะโฟกัสที่ผลไม้")
    if crop > 0.3: tips.append("ผลไม้โดนครอป ถ่ายให้เห็นทั้งลูก")
    return {"score": max(0, score), "ok": score >= 70, "tips_th": tips}


def fruit_scan(photo):
    return {"photo_id": photo["id"], "fruit": photo["fruit"], "quality": scan_quality(photo["glare"], photo["blur"], photo["crop"])}


def ripeness(fruit, color, spots, firmness=None, aroma=None, knock=None):
    """color/spots 0..1 from the vision step; firmness/aroma optional user taps; knock = knock_test()['cue']. Missing cue → weight re-normalised."""
    f = _fruit(fruit)
    _rng(color, 0, 1, "color"); _rng(spots, 0, 1, "spots")
    if firmness is not None and firmness not in FIRMNESS: raise ValueError("firmness")
    if aroma is not None and aroma not in AROMA: raise ValueError("aroma")
    wc, wf, wa, ws, wk = f["w"]
    if knock is not None:
        if not f["knock"]: raise ValueError("knock cue only for watermelon / durian")
        _rng(knock, 0, 1, "knock")
    parts = [(wc, color), (ws, spots)]
    if firmness is not None: parts.append((wf, FIRMNESS[firmness]))
    if aroma is not None: parts.append((wa, AROMA[aroma]))
    if knock is not None: parts.append((wk, knock))
    tw = sum(w for w, _ in parts)
    if tw == 0: raise ValueError("not enough cues")
    idx = sum(w * v for w, v in parts) / tw
    if spots >= 0.6: idx = max(idx, 0.86)          # heavy spotting always means overripe
    idx = round(idx, 3)
    stage, stage_th = next((s, t) for lim, s, t in STAGES if idx < lim)
    rd = f["ripen_days"]
    ripens = rd > 0
    if not ripens and stage in ("unripe", "almost"): days_to_perfect, eat_within = 0, 0
    else:
        days_to_perfect = 0 if idx >= 0.60 else math.ceil((PERFECT - idx) / PERFECT * rd)
        eat_within = 0 if stage == "overripe" else (2 if stage == "perfect" else days_to_perfect + 2)
    used = [n for n, v in (("color", 1), ("spots", 1), ("firmness", firmness), ("aroma", aroma), ("knock", knock)) if v is not None]
    conf = round(min(0.95, 0.55 + 0.1 * len(used)), 2)
    if not ripens and stage in ("unripe", "almost"): head = f"{f['th']} ยังไม่สุกพอ และไม่สุกต่อหลังตัดจากต้น เลือกลูกอื่นดีกว่า"
    elif stage == "unripe": head = f"{f['th']} ยังดิบ รออีกประมาณ {days_to_perfect} วัน"
    elif stage == "almost": head = f"{f['th']} ใกล้สุก กินได้ในอีก {days_to_perfect} วัน"
    elif stage == "perfect": head = f"{f['th']} สุกพอดี กินภายใน {eat_within} วัน"
    else: head = f"{f['th']} สุกเกินแล้ว เหมาะทำสมูทตี้/ขนม ตรวจกลิ่นและราก่อนกิน"
    return {"fruit": fruit, "fruit_th": f["th"], "index": idx, "score": min(100, round(idx * 100)), "stage": stage, "stage_th": stage_th,
            "ripens_after_pick": ripens, "days_to_perfect": days_to_perfect, "eat_within_days": eat_within, "cues_used": used, "confidence": conf,
            "headline_th": head, "disclaimer_th": DISCLAIMER}


def knock_test(fruit, hz, decay_ms):
    """Mic knock test. Deep ringing thump = ripe; high pitch = unripe; very low + dead = overripe/hollow."""
    f = _fruit(fruit)
    if not f["knock"]: raise ValueError("knock test only for watermelon / durian")
    _rng(hz, 30, 600, "hz"); _rng(decay_ms, 10, 2000, "decay_ms")
    if hz > 220: v, th, cue = "unripe", "เสียงแหลม แน่น ยังไม่สุก", 0.2
    elif hz >= 90 and decay_ms >= 120: v, th, cue = "ripe", "เสียงทุ้มก้อง สุกกำลังดี", 0.75
    elif hz >= 90: v, th, cue = "almost", "เสียงทุ้มแต่สั้น ใกล้สุก", 0.5
    elif decay_ms < 80: v, th, cue = "overripe", "เสียงตื้อ ๆ ทึบ อาจสุกเกิน/เนื้อแป้ง", 0.95
    else: v, th, cue = "ripe", "เสียงทุ้มต่ำ สุกดี", 0.8
    return {"fruit": fruit, "hz": hz, "decay_ms": decay_ms, "verdict": v, "verdict_th": th, "cue": cue,
            "tip_th": "เคาะ 3 ครั้งใกล้ไมค์ในที่เงียบ ใช้ข้อนิ้วกลาง"}


def in_season(fruit, month):
    _rng(month, 1, 12, "month")
    return month in _fruit(fruit)["season"]


def price_check(fruit, total_baht, kg, month):
    f = _fruit(fruit)
    _rng(total_baht, 0.01, 100000, "total_baht"); _rng(kg, 0.05, 100, "kg")
    seas = in_season(fruit, month)
    lo, hi = f["price"]
    m = 1.0 if seas else OFF_SEASON_MULT
    lo, hi = round(lo * m), round(hi * m)
    per = round(total_baht / kg, 1)
    mid = (lo + hi) / 2
    if per < lo * 0.6: v, th = "suspicious_low", "ถูกผิดปกติ เช็กสภาพ/น้ำหนักให้ดี"
    elif per < lo: v, th = "cheap", "ถูก คุ้มเลย"
    elif per <= hi: v, th = "fair", "ราคาสมเหตุสมผล"
    elif per <= hi * 1.3: v, th = "pricey", "แพงไปหน่อย ลองต่อราคา"
    else: v, th = "very_pricey", "แพงมาก ลองร้านอื่น"
    return {"fruit": fruit, "per_kg": per, "ref_low": lo, "ref_high": hi, "in_season": seas, "verdict": v, "verdict_th": th,
            "diff_from_mid_pct": round((per - mid) / mid * 100), "disclaimer_th": "ช่วงราคาอ้างอิงเป็นค่าตัวอย่าง ไม่ใช่ราคาตลาดจริงวันนี้"}


def storage_plan(fruit, stage, goal):
    f = _fruit(fruit)
    if stage not in ("unripe", "almost", "perfect", "overripe"): raise ValueError("stage")
    if goal not in ("speed_up", "keep", "slow_down"): raise ValueError("goal")
    steps, where, factor = [], "counter", 1.0
    if goal == "speed_up":
        if stage in ("perfect", "overripe"): steps.append("สุกแล้ว ไม่ต้องเร่ง")
        elif f["ripen_days"] == 0: steps.append("ผลไม้ชนิดนี้ไม่สุกต่อหลังเก็บ เลือกลูกที่สุกแล้วตั้งแต่ซื้อ")
        else:
            where, factor = "paper_bag", 0.7
            steps += ["ใส่ถุงกระดาษพร้อมกล้วยสุก 1 ลูก", "วางที่อุณหภูมิห้อง ไม่โดนแดด"]
    elif goal == "slow_down":
        if f["fridge_ok"] and stage in ("perfect", "overripe"):
            where, factor = "fridge", 2.0
            steps += ["แช่ช่องผักในตู้เย็น", "ห่อ/ใส่กล่องกันกลิ่นติดของอื่น"]
        elif not f["fridge_ok"]:
            where, factor = "counter", 1.3
            steps += ["ห้ามแช่ตู้เย็นตอนยังไม่สุก เปลือกจะดำ", "แยกหวี ห่อขั้วด้วยฟิล์ม"]
        else:
            where, factor = "counter", 1.2
            steps += ["ยังไม่สุก อย่าเพิ่งแช่เย็น จะไม่สุกต่อ", "วางในที่เย็น ลมผ่าน แยกจากกล้วย"]
    else:
        steps.append("วางที่อุณหภูมิห้อง ไม่โดนแดด")
    return {"fruit": fruit, "goal": goal, "where": where, "speed_factor": factor, "steps_th": steps}


def eat_plan(items, today, days=5):
    """items: [{"label","fruit","days_to_perfect","eat_within_days"}] → day-by-day what to eat first."""
    if not items: raise ValueError("empty basket")
    _rng(days, 1, 14, "days")
    t = _date(today); out = []
    for d in range(days):
        eat, wait, late = [], [], []
        for it in items:
            ready = it["days_to_perfect"]; last = max(it["eat_within_days"], ready + 1)
            if ready <= d < last: eat.append(it["label"])
            elif d < ready: wait.append(it["label"])
            else: late.append(it["label"])
        out.append({"date": (t + _dt.timedelta(days=d)).isoformat(), "eat": eat, "waiting": wait, "past_best": late})
    soon = sorted(items, key=lambda x: (x["eat_within_days"], x["label"]))[0]["label"]
    return {"start": today, "days": out, "eat_first": soon, "headline_th": f"กิน{soon}ก่อน แล้วค่อยไล่ตามตาราง"}


def pick_check(fruit, answers):
    qs = CHECKLISTS[fruit] if fruit in CHECKLISTS else _fruit(fruit)
    if not isinstance(answers, list) or len(answers) != len(qs) or not all(isinstance(a, bool) for a in answers):
        raise ValueError("answers must be 4 booleans")
    yes = sum(answers)
    v, th = ("pick", "เลือกลูกนี้ได้เลย") if yes >= 3 else (("maybe", "พอได้ ลองเทียบอีกลูก") if yes == 2 else ("skip", "ข้ามลูกนี้ไป"))
    return {"fruit": fruit, "questions_th": qs, "answers": answers, "yes": yes, "verdict": v, "verdict_th": th}


def season_calendar(month):
    _rng(month, 1, 12, "month")
    fs = [f for f in FRUITS if month in FRUITS[f]["season"]]
    return {"month": month, "fruits": fs, "fruits_th": [FRUITS[f]["th"] for f in fs], "tip_th": f"เดือนนี้มีผลไม้ตามฤดู {len(fs)} ชนิด ราคามักถูกและหวานกว่า"}


def basket_item(label, scan):
    return {"label": label, "fruit": scan["fruit"], "days_to_perfect": scan["days_to_perfect"], "eat_within_days": scan["eat_within_days"]}


def diary_summary(entries):
    if not entries: raise ValueError("empty diary")
    hit = sum(1 for e in entries if e["result"] == "just_right")
    cnt = {}
    for e in entries: cnt[e["fruit"]] = cnt.get(e["fruit"], 0) + 1
    top = sorted(cnt.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]
    acc = round(hit / len(entries) * 100)
    spent = sum(e["paid_baht"] for e in entries)
    return {"count": len(entries), "accuracy_pct": acc, "spent_baht": spent, "top_fruit": top,
            "headline_th": f"ทายถูก {hit}/{len(entries)} ครั้ง ({acc}%) ซื้อผลไม้ไป ฿{spent:,}"}


def share_card(scan, hook_th):
    return {"title_th": f"{scan['fruit_th']} {scan['stage_th']} {scan['score']}/100", "hook_th": hook_th, "layout": "fruit_meter",
            "sizes": ["1080x1350", "1080x1920"], "watermark": "RipeRight · AI วันละแอป", "cta_th": "คอมเมนต์ RIPE รับแพ็กฟรี", "disclaimer_th": "ค่าประมาณ ไม่ใช่การรับรองความปลอดภัยอาหาร"}


def quota(used_today, free_per_day=5, pro=False):
    _rng(used_today, 0, 10000, "used_today")
    if pro: return {"allowed": 1, "left_after": None, "paywall": False}
    left = free_per_day - used_today
    return {"allowed": 1 if left > 0 else 0, "left_after": max(left - 1, 0), "paywall": left <= 0}


def safety_guard(flag=None):
    msgs = {None: ("ok", "ผลเป็นค่าประมาณ ใช้ตาและจมูกตัวเองยืนยันด้วย"),
            "mold": ("stop", "เห็นรา/จุดฟู ทิ้งทั้งลูก ห้ามตัดส่วนที่ขึ้นราแล้วกินต่อ"),
            "durian_alcohol": ("warn", "ทุเรียนกับแอลกอฮอล์ไม่ควรกินพร้อมกัน และคนเป็นเบาหวาน/โรคไตควรกินแต่น้อย"),
            "not_fruit": ("stop", "ไม่พบผลไม้ในรูป ลองถ่ายใหม่ให้เห็นทั้งลูก")}
    if flag not in msgs: raise ValueError("flag")
    lv, m = msgs[flag]
    return {"level": lv, "message_th": m}
