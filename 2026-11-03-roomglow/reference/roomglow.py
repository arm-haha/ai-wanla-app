"""RoomGlow — ห้องเดิม ลุคใหม่: deterministic logic (no AI). AI does room scan + restyle images; this decides numbers."""
import math
R = lambda x: round(x + 0.0, 2)
LUX = {"bedroom": 150, "living": 200, "studio": 200, "desk": 500, "kitchen": 300}
STYLES_TH = {"muji": "มูจิ มินิมอล", "korean": "เกาหลีคลีน", "japandi": "เจแปนดิ", "cozy": "อบอุ่นไฟเหลือง",
             "boho": "โบฮีเมียน", "industrial": "ลอฟต์อินดัส"}

def floor_area(w, l):
    if w <= 0 or l <= 0: raise ValueError("room size must be > 0")
    return R(w * l)

def wall_area(w, l, h, doors=1, windows=1, door_m2=1.8, window_m2=1.5):
    """paintable wall area after openings."""
    return R(max(0.0, 2 * (w + l) * h - doors * door_m2 - windows * window_m2))

def paint_estimate(area_m2, coats=2, coverage_m2_per_l=10, can_l=3.0, can_price_thb=650):
    liters = R(area_m2 * coats / coverage_m2_per_l)
    cans = math.ceil(liters / can_l) if liters > 0 else 0
    return {"liters": liters, "cans": cans, "cost_thb": cans * can_price_thb}

def wallpaper_rolls(accent_wall_m2, roll_m2=5.3, waste=0.1, roll_price_thb=290):
    rolls = math.ceil(accent_wall_m2 * (1 + waste) / roll_m2)
    return {"rolls": rolls, "cost_thb": rolls * roll_price_thb}

def lumens_needed(area_m2, room_type):
    lux = LUX[room_type]
    return {"room_type": room_type, "target_lux": lux, "lumens": int(round(area_m2 * lux))}

def light_plan(area_m2, room_type, existing_lm, style):
    need = lumens_needed(area_m2, room_type)["lumens"]
    gap = max(0, need - existing_lm)
    kelvin = 2700 if style in ("cozy", "boho", "japandi") else (3000 if style == "industrial" else 4000)
    return {"lumens_needed": need, "existing_lm": existing_lm, "gap_lm": gap,
            "bulbs_800lm": math.ceil(gap / 800) if gap else 0, "kelvin": kelvin,
            "tip_th": "เพิ่มโคมตั้งพื้น/ไฟเส้นหลังหัวเตียง" if gap else "แสงพอแล้ว เปลี่ยนสีไฟให้เข้าธีมพอ"}

def glow_score(scan):
    """0-100: light 30, clutter 25, color harmony 25, cohesion 20. inputs 0..1 from scan (clutter: 1=messy)."""
    for k in ("light", "clutter", "harmony", "cohesion"):
        if not 0 <= scan[k] <= 1: raise ValueError(k + " must be 0..1")
    s = scan["light"] * 30 + (1 - scan["clutter"]) * 25 + scan["harmony"] * 25 + scan["cohesion"] * 20
    return int(round(s))

def score_after(scan, picked, lit_ok):
    """apply item boosts (capped at 1) to get the after score."""
    a = dict(scan)
    for it in picked:
        for k, v in it.get("boost", {}).items():
            a[k] = min(1.0, a[k] + v) if k != "clutter" else max(0.0, a[k] - v)
    if lit_ok: a["light"] = max(a["light"], 0.85)
    return glow_score(a)

def shopping_plan(items, budget_thb, style, renter_safe=True):
    """0/1 knapsack maximizing impact within budget. Only items matching style ('any' ok) and renter rule."""
    pool = [i for i in items if (style in i["styles"] or "any" in i["styles"]) and (i["renter_safe"] or not renter_safe)]
    B = int(budget_thb)
    best = [(0, ())] * (B + 1)  # (impact, idx tuple)
    for idx, it in enumerate(pool):
        p = int(it["price_thb"])
        for b in range(B, p - 1, -1):
            cand = best[b - p][0] + it["impact"]
            if cand > best[b][0]: best[b] = (cand, best[b - p][1] + (idx,))
    impact, chosen = best[B]
    picked = [pool[i] for i in chosen]
    picked.sort(key=lambda i: (-i["impact"] / i["price_thb"], i["id"]))
    spent = sum(i["price_thb"] for i in picked)
    skipped = [i["id"] for i in items if i not in pool]
    return {"style": style, "budget_thb": budget_thb, "spent_thb": spent, "left_thb": budget_thb - spent,
            "impact": impact, "items": [i["id"] for i in picked], "excluded_not_renter_safe": [i["id"] for i in items if renter_safe and not i["renter_safe"]],
            "budget_used_pct": R(spent / budget_thb * 100) if budget_thb else 0.0}

def declutter(items):
    """items: name, action keep/sell/donate/toss, resale_thb. Returns counts + cash back."""
    out = {"keep": 0, "sell": 0, "donate": 0, "toss": 0}
    cash = 0
    for i in items:
        out[i["action"]] += 1
        if i["action"] == "sell": cash += i.get("resale_thb", 0)
    return {"counts": out, "resale_thb": cash, "removed": out["sell"] + out["donate"] + out["toss"]}

def weekend_plan(picked_items, catalog):
    """order steps: declutter → paint/wallpaper → big pieces → textiles → lights → decor."""
    order = {"declutter": 0, "wall": 1, "furniture": 2, "textile": 3, "light": 4, "decor": 5, "plant": 5}
    by = {c["id"]: c for c in catalog}
    steps = sorted((by[i] for i in picked_items), key=lambda c: (order[c["category"]], c["id"]))
    t = 0; out = []
    for s in steps:
        t += s["minutes"]; out.append({"item": s["id"], "name_th": s["name_th"], "minutes": s["minutes"], "cum_minutes": t})
    return {"steps": out, "total_minutes": t, "total_hours": R(t / 60)}

def poll_tally(options, votes):
    seen = {}
    for v in votes: seen[v["voter"]] = v["option"]
    rows = [{"option": o, "votes": sum(1 for x in seen.values() if x == o)} for o in options]
    tot = sum(r["votes"] for r in rows)
    for r in rows: r["pct"] = R(r["votes"] / tot * 100) if tot else 0.0
    rows.sort(key=lambda r: -r["votes"])
    tie = tot > 0 and len(rows) > 1 and rows[0]["votes"] == rows[1]["votes"]
    return {"total_votes": tot, "rows": rows, "winner": None if (tot == 0 or tie) else rows[0]["option"], "tie": tie}
