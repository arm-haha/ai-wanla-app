"""LabelLens (ฉลากบอกหมด) deterministic core logic. All thresholds are app defaults the user can change."""
G_PER_TSP = 4.0            # 1 ช้อนชา น้ำตาล ~4 g
DAILY = {"sugar_g": 24, "sodium_mg": 2000, "fat_g": 65, "kcal": 2000}   # Thai-style defaults (ช้อนชา 6/วัน), user-editable
WALK_KCAL_PER_MIN = 4.0    # เดินเร็วโดยประมาณ ใช้เป็นภาพประกอบ ไม่ใช่คำแนะนำทางการแพทย์
GREEN, AMBER, RED = "green", "amber", "red"
# traffic-light per 100 g/ml (solid, drink)
TL = {"sugar_g": ((5, 22.5), (2.5, 11.25)), "fat_g": ((3, 17.5), (1.5, 8.75)), "sodium_mg": ((120, 600), (120, 600))}
ALLERGENS = {"milk": ["นม", "นมผง", "เวย์", "milk", "whey", "casein"], "egg": ["ไข่", "egg"], "peanut": ["ถั่วลิสง", "peanut"],
             "soy": ["ถั่วเหลือง", "soy", "ซอยเลซิติน"], "wheat": ["แป้งสาลี", "wheat", "กลูเตน", "gluten"],
             "shrimp": ["กุ้ง", "shrimp"], "fish": ["ปลา", "fish"], "sesame": ["งา", "sesame"]}
ADDITIVES = {"E621": ("ผงชูรส (MSG)", "info"), "E951": ("แอสปาร์แตม สารให้ความหวาน", "caution"), "E955": ("ซูคราโลส สารให้ความหวาน", "info"),
             "E211": ("โซเดียมเบนโซเอต วัตถุกันเสีย", "info"), "E102": ("ทาร์ทราซีน สีเหลือง", "caution"), "E330": ("กรดซิตริก", "info"),
             "E471": ("อิมัลซิไฟเออร์", "info"), "E250": ("โซเดียมไนไตรต์ (เนื้อแปรรูป)", "caution")}

def pack_totals(label):
    """label: per-serving values + servings_per_pack. returns whole-pack totals."""
    n = label["servings_per_pack"]
    if n <= 0: raise ValueError("servings_per_pack must be > 0")
    keys = ("kcal", "sugar_g", "fat_g", "sodium_mg")
    return {k: round(label["per_serving"][k] * n, 1) for k in keys}

def sugar_spoons(sugar_g):
    return round(sugar_g / G_PER_TSP, 1)

def per100(label, key):
    return label["per_serving"][key] * 100 / label["serving_size"]

def traffic_light(label):
    idx = 1 if label["form"] == "drink" else 0
    out = {}
    for k, th in TL.items():
        lo, hi = th[idx]; v = per100(label, k)
        out[k] = GREEN if v <= lo else (RED if v > hi else AMBER)
    return out

def grade(label):
    """A–E: start 100, penalties by traffic light, extra if one pack > 50% daily sugar/sodium."""
    tl = traffic_light(label); t = pack_totals(label); s = 100
    for c in tl.values(): s -= {GREEN: 0, AMBER: 15, RED: 30}[c]
    if t["sugar_g"] > DAILY["sugar_g"] * 0.5: s -= 15
    if t["sugar_g"] > DAILY["sugar_g"]: s -= 20
    if t["sodium_mg"] > DAILY["sodium_mg"] * 0.5: s -= 15
    s = max(0, s)
    letter = "A" if s >= 85 else "B" if s >= 70 else "C" if s >= 50 else "D" if s >= 30 else "E"
    return {"score": s, "grade": letter, "lights": tl}

def daily_pct(totals):
    return {k: round(totals[k] * 100 / DAILY[k]) for k in DAILY}

def walk_off(kcal):
    return int(round(kcal / WALK_KCAL_PER_MIN))

def allergen_hits(ingredients_th, user_allergies):
    text = ingredients_th.lower(); hits = []
    for a in user_allergies:
        for w in ALLERGENS.get(a, []):
            if w.lower() in text: hits.append({"allergen": a, "matched": w}); break
    return {"safe": not hits, "hits": hits}

def decode_additives(codes):
    out = []
    for c in codes:
        c = c.upper().replace(" ", "").replace("INS", "E")
        if not c.startswith("E"): c = "E" + c
        name, lvl = ADDITIVES.get(c, ("ไม่รู้จักในฐานข้อมูล", "unknown"))
        out.append({"code": c, "name_th": name, "level": lvl})
    return out

def battle(a, b):
    ga, gb = grade(a), grade(b); ta, tb = pack_totals(a), pack_totals(b)
    if ga["score"] == gb["score"]: win = "tie"
    else: win = a["id"] if ga["score"] > gb["score"] else b["id"]
    return {"a": a["id"], "b": b["id"], "score_a": ga["score"], "score_b": gb["score"], "winner": win,
            "sugar_diff_tsp": round(abs(sugar_spoons(ta["sugar_g"]) - sugar_spoons(tb["sugar_g"])), 1),
            "price_diff_thb": round(abs(a.get("price_thb", 0) - b.get("price_thb", 0)), 2)}

def budget_day(entries):
    """entries: list of {label, packs}. sums totals and flags over-budget keys."""
    tot = {k: 0.0 for k in DAILY}
    for e in entries:
        t = pack_totals(e["label"])
        for k in DAILY: tot[k] += t[k] * e.get("packs", 1)
    tot = {k: round(v, 1) for k, v in tot.items()}
    pct = daily_pct(tot)
    return {"totals": tot, "pct": pct, "over": sorted(k for k, p in pct.items() if p > 100),
            "sugar_tsp": sugar_spoons(tot["sugar_g"]), "items": len(entries)}

def swap_suggest(label, candidates):
    """best same-category candidate with higher score; None if nothing better."""
    base = grade(label)["score"]
    pool = [c for c in candidates if c["category"] == label["category"] and c["id"] != label["id"] and grade(c)["score"] > base]
    if not pool: return None
    best = max(pool, key=lambda c: (grade(c)["score"], -c.get("price_thb", 0)))
    return {"from": label["id"], "to": best["id"], "score_gain": grade(best)["score"] - base,
            "sugar_saved_tsp": round(sugar_spoons(pack_totals(label)["sugar_g"]) - sugar_spoons(pack_totals(best)["sugar_g"]), 1)}

def week_streak(days):
    """days: list of {date, sugar_tsp}; streak = consecutive most-recent days under 6 tsp."""
    s = 0
    for d in sorted(days, key=lambda x: x["date"], reverse=True):
        if d["sugar_tsp"] <= DAILY["sugar_g"] / G_PER_TSP: s += 1
        else: break
    return {"streak": s, "badge": "หวานน้อย 7 วัน" if s >= 7 else ("หวานน้อย 3 วัน" if s >= 3 else None)}
