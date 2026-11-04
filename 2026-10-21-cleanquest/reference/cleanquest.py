"""CleanQuest (ห้องรกหาย) — deterministic core. AI only proposes hotspot tags + severity from a photo; every score/plan/number comes from here."""
from datetime import date, timedelta
import math

# id: (label_th, zone, weight, base_min, quest_th, emoji)
HOTSPOTS = {
    "clothes_pile":   ("เสื้อผ้ากองบนเก้าอี้/เตียง", "bed",   12, 6, "พับ/แขวนเสื้อผ้าที่กองอยู่", "👕"),
    "trash_floor":    ("ขยะ/ถุงบนพื้น",            "floor", 10, 3, "เก็บขยะใส่ถุงเดียว มัดปากถุง", "🗑️"),
    "dishes_cups":    ("แก้ว/จานค้าง",              "desk",  10, 4, "รวมแก้ว/จานไปล้าง", "🥤"),
    "snack_wrappers": ("ซองขนม/กล่องเดลิเวอรี",      "desk",   8, 2, "ทิ้งซองขนมและกล่องข้าว", "🍟"),
    "desk_clutter":   ("โต๊ะรก ของวางเกลื่อน",       "desk",   8, 5, "เคลียร์โต๊ะ เหลือแค่ของใช้วันนี้", "🗂️"),
    "boxes_parcels":  ("กล่องพัสดุยังไม่แกะ/ไม่ทิ้ง",  "floor",  8, 4, "แกะของ พับกล่องรวมไว้ทิ้ง", "📦"),
    "laundry_full":   ("ตะกร้าผ้าล้น",               "floor",  7, 3, "แยกผ้า ยัดถุงพร้อมส่งซัก", "🧺"),
    "bed_unmade":     ("เตียงไม่ได้เก็บ",             "bed",    6, 2, "ปูเตียง ตบหมอน พับผ้าห่ม", "🛏️"),
    "floor_dust":     ("พื้นมีฝุ่น/เส้นผม",           "floor",  6, 5, "กวาด/ถูพื้นรอบห้อง", "🧹"),
    "shoes_scattered":("รองเท้ากระจาย",              "floor",  5, 2, "จับคู่รองเท้า เข้าชั้น", "👟"),
    "books_papers":   ("หนังสือ/กระดาษกอง",           "desk",   5, 4, "จัดหนังสือ ทิ้งกระดาษไม่ใช้", "📚"),
    "cosmetics":      ("เครื่องสำอาง/ของใช้กระจาย",    "desk",   5, 3, "รวมของใช้เข้าตะกร้า/ลิ้นชัก", "💄"),
    "cables_mess":    ("สายชาร์จพันกัน",              "desk",   4, 3, "ม้วนสาย รัดเก็บ", "🔌"),
}
PRIORITY = list(HOTSPOTS)          # tie-break order = catalog order
SEV_TH = {1: "นิดหน่อย", 2: "พอสมควร", 3: "เยอะมาก"}
MODES = {"lazy": 5, "normal": 15, "fire": None}   # minute budget per run (None = everything)
MODE_TH = {"lazy": "ขี้เกียจมาก 5 นาที", "normal": "ปกติ 15 นาที", "fire": "ไฟลุก เคลียร์หมด"}
SPRINT_MIN = 15
XP = {"scan": 10, "quest": 0, "session": 20, "declutter": 5}   # quest XP = its points
LEVEL_XP = 100
LABELS = [(90, "ห้องโชว์ ✨"), (70, "อยู่ได้สบาย"), (40, "เริ่มรก"), (0, "ห้องวิกฤต 🚨")]

def _label(score): return next(t for th, t in LABELS if score >= th)

def _norm(hotspots):
    seen, out = set(), []
    for h in hotspots:
        hid, sev = h["id"], h["severity"]
        if hid not in HOTSPOTS: raise ValueError(f"unknown hotspot {hid}")
        if sev not in SEV_TH: raise ValueError("severity must be 1..3")
        if hid in seen: continue
        seen.add(hid); out.append({"id": hid, "severity": sev})
    return sorted(out, key=lambda h: PRIORITY.index(h["id"]))

def points(h): return HOTSPOTS[h["id"]][2] * h["severity"]
def minutes(h): return HOTSPOTS[h["id"]][3] * h["severity"]

def mess_score(hotspots):
    """clean_score = max(0, 100 − Σ weight×severity). Higher = cleaner."""
    hs = _norm(hotspots)
    total = sum(points(h) for h in hs)
    score = max(0, 100 - total)
    zones = {}
    for h in hs: zones[HOTSPOTS[h["id"]][1]] = zones.get(HOTSPOTS[h["id"]][1], 0) + points(h)
    worst = max(zones, key=lambda z: (zones[z], -["bed", "desk", "floor"].index(z))) if zones else None
    pins = [{"id": h["id"], "severity": h["severity"], "label_th": HOTSPOTS[h["id"]][0], "severity_th": SEV_TH[h["severity"]],
             "points": points(h), "emoji": HOTSPOTS[h["id"]][5]} for h in sorted(hs, key=lambda h: (-points(h), PRIORITY.index(h["id"])))]
    return {"clean_score": score, "mess_points": total, "label_th": _label(score), "worst_zone": worst,
            "zone_points": zones, "hotspots": pins, "est_minutes": sum(minutes(h) for h in hs)}

def quest_plan(hotspots, mode="normal"):
    """Order by impact-per-minute (points/minutes desc, then points desc, then catalog). Pack into 15-min sprints.
    mode lazy/normal: keep only quests that fit the budget greedily in that order."""
    if mode not in MODES: raise ValueError("bad mode")
    hs = _norm(hotspots)
    order = sorted(hs, key=lambda h: (-points(h) / minutes(h), -points(h), PRIORITY.index(h["id"])))
    budget = MODES[mode]
    if budget is not None:
        kept, used = [], 0
        for h in order:
            if used + minutes(h) <= budget: kept.append(h); used += minutes(h)
        order = kept
    base = mess_score(hs)["mess_points"]
    quests, sprints, cur, cur_min, removed = [], [], [], 0, 0
    for i, h in enumerate(order, 1):
        m = minutes(h)
        if cur and cur_min + m > SPRINT_MIN: sprints.append(cur); cur, cur_min = [], 0
        cur.append(f"q{i}"); cur_min += m
        removed += points(h)
        quests.append({"id": f"q{i}", "hotspot": h["id"], "title_th": HOTSPOTS[h["id"]][4], "emoji": HOTSPOTS[h["id"]][5],
                       "minutes": m, "xp": points(h), "quick_win": m <= 3, "score_after": max(0, 100 - (base - removed))})
    if cur: sprints.append(cur)
    total = sum(q["minutes"] for q in quests)
    return {"mode": mode, "mode_th": MODE_TH[mode], "quests": quests,
            "sprints": [{"n": i + 1, "quest_ids": s, "minutes": sum(q["minutes"] for q in quests if q["id"] in s)} for i, s in enumerate(sprints)],
            "total_minutes": total, "score_before": max(0, 100 - base), "score_after": quests[-1]["score_after"] if quests else max(0, 100 - base)}

def timer_tick(plan, done_ids, elapsed_sec):
    """Live Timer Mode state: current sprint, remaining seconds, live score."""
    done = [q for q in plan["quests"] if q["id"] in set(done_ids)]
    gained = sum(q["xp"] for q in done)
    live = min(100, plan["score_before"] + gained)
    nxt = next((q for q in plan["quests"] if q["id"] not in set(done_ids)), None)
    sprint = next((s["n"] for s in plan["sprints"] if nxt and nxt["id"] in s["quest_ids"]), None)
    total = plan["total_minutes"] * 60
    return {"live_score": live, "xp_gained": gained, "done": len(done), "left": len(plan["quests"]) - len(done),
            "next_quest": nxt["id"] if nxt else None, "sprint": sprint, "remaining_sec": max(0, total - elapsed_sec),
            "finished": nxt is None}

def glow_up(before, after, minutes_spent, quests_done, name):
    b, a = before["clean_score"], after["clean_score"]
    d = a - b
    title = "ห้องเกิดใหม่ 🦋" if d >= 60 else "ล้างบาง 💪" if d >= 30 else "ดีขึ้นแล้ว 👍" if d > 0 else "ลองอีกรอบนะ"
    return {"name": name, "before": b, "after": a, "delta": d, "minutes": minutes_spent, "quests_done": quests_done,
            "title_th": title, "headline_th": f"ห้อง{name} {b} → {a} ใน {minutes_spent} นาที",
            "size_px": [1080, 1920], "layout": "split_before_after", "watermark": "CleanQuest · AI วันละแอป"}

COND_F = {"good": 0.6, "worn": 0.35, "broken": 0}
COND_TH = {"good": "สภาพดี", "worn": "มีร่องรอยใช้งาน", "broken": "เสีย/ชำรุด"}
def declutter(item):
    """keep / sell / donate / trash. Rules in order:
    broken → trash · sentimental → keep · used ≤6 months & not duplicate → keep ·
    resale ≥ 100 → sell · good/worn → donate."""
    c = item["condition"]
    resale = int(round(item.get("paid_thb", 0) * COND_F[c] / 10.0) * 10) if c != "broken" else 0
    if c == "broken": d, why = "trash", "ชำรุดแล้ว ทิ้งหรือแยกขยะอิเล็กทรอนิกส์"
    elif item.get("sentimental"): d, why = "keep", "มีความทรงจำ เก็บไว้ในกล่องความทรงจำ 1 กล่อง"
    elif item["last_used_months"] <= 6 and not item.get("duplicate"): d, why = "keep", "ยังใช้อยู่ เก็บให้มีที่ประจำ"
    elif resale >= 100: d, why = "sell", f"ไม่ได้ใช้ {item['last_used_months']} เดือน ขายได้ราว ฿{resale}"
    else: d, why = "donate", "ไม่ได้ใช้แล้ว ราคาขายต่ำ บริจาคดีกว่า"
    out = {"item_id": item["id"], "name_th": item["name_th"], "decision": d, "reason_th": why, "resale_thb": resale if d == "sell" else 0}
    if d == "sell":
        out["listing_th"] = f"ขาย {item['name_th']} {COND_TH[c]} ใช้น้อย ฿{resale} นัดรับได้/ส่งได้ ทักแชทเลย"
    return out

def chore_split(quests, people):
    """Balanced split: biggest quest first, give to person with lowest load (minutes), tie → order in list."""
    load = {p: 0 for p in people}; assign = {p: [] for p in people}
    for q in sorted(quests, key=lambda q: (-q["minutes"], q["id"])):
        p = min(people, key=lambda x: (load[x], people.index(x)))
        load[p] += q["minutes"]; assign[p].append(q["id"])
    return [{"person": p, "quest_ids": assign[p], "minutes": load[p]} for p in people]

def progress(log, today):
    xp = sum(e.get("xp", XP[e["kind"]]) if e["kind"] == "quest" else XP[e["kind"]] for e in log)
    days = {e["on"] for e in log}; streak, d = 0, today
    while d.isoformat() in days: streak += 1; d -= timedelta(days=1)
    return {"xp": xp, "level": xp // LEVEL_XP + 1, "streak_days": streak}

def weekly_reset(sessions, today, weekday=6):
    """Next weekly reset day (default Sunday=6) and whether this week is already done."""
    days_ahead = (weekday - today.weekday()) % 7
    nxt = today + timedelta(days=days_ahead)
    week_start = today - timedelta(days=today.weekday())
    done = any(week_start.isoformat() <= s["on"] <= today.isoformat() for s in sessions)
    return {"next_reset": nxt.isoformat(), "days_left": days_ahead, "done_this_week": done}

def wrapped(sessions, month):
    ss = [s for s in sessions if s["on"].startswith(month)]
    if not ss: return {"month": month, "sessions": 0, "minutes": 0, "avg_delta": 0, "best_delta": 0, "top_hotspot": None, "hotspot_counts": {}}
    counts = {}
    for s in ss:
        for h in s["hotspots"]: counts[h] = counts.get(h, 0) + 1
    top = max(counts, key=lambda k: (counts[k], -PRIORITY.index(k)))
    deltas = [s["after"] - s["before"] for s in ss]
    return {"month": month, "sessions": len(ss), "minutes": sum(s["minutes"] for s in ss),
            "avg_delta": int(round(sum(deltas) / len(ss))), "best_delta": max(deltas), "top_hotspot": top, "hotspot_counts": counts}
