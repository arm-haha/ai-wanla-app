"""HairMirror — ลองทรงก่อนตัด: deterministic logic (no AI). AI does landmarks + image edits; this decides numbers."""
import math
R = lambda x: round(x + 0.0, 2)
SHAPES = ["oval", "round", "square", "heart", "oblong", "diamond"]
SHAPE_TH = {"oval": "หน้ารูปไข่", "round": "หน้ากลม", "square": "หน้าเหลี่ยม", "heart": "หน้ารูปหัวใจ", "oblong": "หน้ายาว", "diamond": "หน้าเพชร"}

def face_shape(m):
    """m: face_length, forehead_w, cheek_w, jaw_w (any unit, same scale). Returns FaceShape."""
    L, F, C, J = m["face_length"], m["forehead_w"], m["cheek_w"], m["jaw_w"]
    if min(L, F, C, J) <= 0: raise ValueError("measurements must be > 0")
    ratio = L / C
    if ratio >= 1.5: s = "oblong"
    elif F > C and F >= J * 1.15: s = "heart"
    elif C >= F * 1.1 and C >= J * 1.1: s = "diamond"
    elif ratio < 1.25: s = "round" if J < C * 0.9 else "square"
    else: s = "oval"
    return {"shape": s, "shape_th": SHAPE_TH[s], "length_to_width": R(ratio),
            "jaw_to_cheek": R(J / C), "forehead_to_cheek": R(F / C)}

def monthly_upkeep(style):
    """salon cost spread per month (52/12 weeks per month)."""
    w = style["maintenance_weeks"]
    return R(style["salon_cost_thb"] * (52 / 12) / w)

def style_match(style, profile, shape):
    """0-100 score: face 50, hair type 20, daily time 15, budget 15."""
    face = 50 if shape in style["suits"] else (20 if style.get("neutral_ok") else 0)
    hair = 20 if profile["hair_type"] in style["hair_types"] else 0
    time_ok = style["daily_minutes"] <= profile["max_daily_minutes"]
    up = monthly_upkeep(style)
    budget_ok = up <= profile["budget_month_thb"]
    score = face + hair + (15 if time_ok else 0) + (15 if budget_ok else 0)
    reasons = []
    reasons.append("เข้ากับ" + SHAPE_TH[shape] if face == 50 else ("พอใช้ได้กับ" + SHAPE_TH[shape] if face else "ไม่ค่อยเข้ากับ" + SHAPE_TH[shape]))
    if not hair: reasons.append("ผมคุณอาจทรงไม่อยู่")
    if not time_ok: reasons.append(f"ต้องจัดทรง {style['daily_minutes']} นาที/วัน")
    if not budget_ok: reasons.append(f"ค่าดูแล ~฿{up:,.0f}/เดือน เกินงบ")
    return {"style_id": style["id"], "score": score, "face_fit": face == 50, "upkeep_month_thb": up,
            "verdict": "ปัง" if score >= 85 else ("ลองได้" if score >= 60 else "เสี่ยง"), "reasons_th": reasons}

def rank_styles(styles, profile, shape, top=3):
    res = [style_match(s, profile, shape) for s in styles]
    res.sort(key=lambda r: (-r["score"], r["upkeep_month_thb"], r["style_id"]))
    return res[:top]

def grow_out(current_cm, target_cm, cm_per_month=1.25):
    if cm_per_month <= 0: raise ValueError("growth must be > 0")
    if target_cm <= current_cm: return {"months": 0, "weeks": 0, "trim_needed": target_cm < current_cm, "assumption_th": f"ผมยาว ~{cm_per_month} ซม./เดือน (ค่าเฉลี่ย ตั้งค่าได้)"}
    months = (target_cm - current_cm) / cm_per_month
    return {"months": R(months), "weeks": math.ceil(months * 52 / 12), "trim_needed": False,
            "assumption_th": f"ผมยาว ~{cm_per_month} ซม./เดือน (ค่าเฉลี่ย ตั้งค่าได้)"}

def poll_tally(options, votes):
    """options: list of style ids; votes: list of {voter, option}. one vote per voter (last wins)."""
    last = {}
    for v in votes:
        if v["option"] not in options: continue
        last[v["voter"]] = v["option"]
    total = len(last); counts = {o: 0 for o in options}
    for o in last.values(): counts[o] += 1
    rows = [{"option": o, "votes": c, "pct": R(100 * c / total) if total else 0.0} for o, c in counts.items()]
    rows.sort(key=lambda r: (-r["votes"], options.index(r["option"])))
    top = rows[0]["votes"] if rows else 0
    leaders = [r["option"] for r in rows if r["votes"] == top and top > 0]
    return {"total_votes": total, "rows": rows, "winner": leaders[0] if len(leaders) == 1 else None, "tie": len(leaders) > 1}

LEVEL_TH = {1: "ดำ", 2: "ดำอมน้ำตาล", 3: "น้ำตาลเข้มมาก", 4: "น้ำตาลเข้ม", 5: "น้ำตาลกลาง", 6: "น้ำตาลอ่อน", 7: "บลอนด์เข้ม", 8: "บลอนด์กลาง", 9: "บลอนด์อ่อน", 10: "บลอนด์สว่างมาก"}
def color_check(natural_level, target_level, undertone, color_family, base_cost_thb=1500, bleach_cost_per_step=800):
    if not (1 <= natural_level <= 10 and 1 <= target_level <= 10): raise ValueError("level 1-10")
    lift = max(0, target_level - natural_level)
    bleach = lift >= 3
    steps = 0 if not bleach else math.ceil((lift - 2) / 2)
    good = {"warm": ["copper", "honey", "chocolate", "ash_brown"], "cool": ["ash", "milk_tea", "black_blue", "ash_brown"],
            "neutral": ["copper", "honey", "chocolate", "ash", "milk_tea", "black_blue", "ash_brown"]}[undertone]
    cost = base_cost_thb + steps * bleach_cost_per_step
    return {"lift_levels": lift, "needs_bleach": bleach, "bleach_sessions": steps, "tone_fit": color_family in good,
            "est_cost_thb": cost, "target_th": LEVEL_TH[target_level],
            "warning_th": "ต้องฟอก ผมเสียง่าย ทำทรีตเมนต์ด้วย" if bleach else "ไม่ต้องฟอก ทำได้ในครั้งเดียว"}

def barber_card(style, zones):
    """zones: list of {zone, length_mm|length_cm, note_th}. normalises to mm and checks sanity."""
    out = []
    for z in zones:
        mm = z.get("length_mm", z.get("length_cm", 0) * 10)
        if mm < 0: raise ValueError("negative length")
        out.append({"zone": z["zone"], "length_mm": mm, "note_th": z.get("note_th", "")})
    order = {"top": 0, "fringe": 1, "sides": 2, "back": 3, "neckline": 4}
    out.sort(key=lambda z: order.get(z["zone"], 9))
    tops = [z["length_mm"] for z in out if z["zone"] in ("top", "fringe")]
    sides = [z["length_mm"] for z in out if z["zone"] in ("sides", "back")]
    contrast = R(min(tops) / max(sides)) if tops and sides and max(sides) > 0 else None
    return {"style_id": style["id"], "name_th": style["name_th"], "zones": out, "top_to_side_ratio": contrast,
            "say_to_barber_th": style["barber_phrase_th"], "dont_th": style.get("dont_th", [])}

def cut_reminder(last_cut_date, maintenance_weeks):
    from datetime import date, timedelta
    d = date.fromisoformat(last_cut_date) + timedelta(weeks=maintenance_weeks)
    return {"next_cut_date": d.isoformat(), "maintenance_weeks": maintenance_weeks}

def year_cost(style, extras_month_thb=0):
    m = monthly_upkeep(style) + extras_month_thb
    return {"month_thb": R(m), "year_thb": R(m * 12)}
