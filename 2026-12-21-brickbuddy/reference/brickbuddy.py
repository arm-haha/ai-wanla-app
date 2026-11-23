"""BrickBuddy reference logic — deterministic, no network. Turns ONE photo of a messy pile of building bricks into
"what can I build right now?": scan quality, inventory, build matching with substitutions, colour assignment, layer steps,
find-it highlight, sort helper, stability check, daily challenge, creation score, diary, share/Reel, quota and safety guard.
Brand-neutral: works with any compatible stud bricks. Never copies official set instructions. Small parts: not for under-3s."""
import datetime as _dt

PARTS = {  # part id: Thai name, studs on top, size class, kind
    "brick_2x4": ("อิฐ 2×4", 8, "L", "brick"), "brick_2x2": ("อิฐ 2×2", 4, "M", "brick"), "brick_1x4": ("อิฐ 1×4", 4, "M", "brick"),
    "brick_1x2": ("อิฐ 1×2", 2, "S", "brick"), "brick_1x1": ("อิฐ 1×1", 1, "S", "brick"),
    "plate_2x4": ("แผ่น 2×4", 8, "M", "plate"), "plate_2x2": ("แผ่น 2×2", 4, "S", "plate"), "plate_1x2": ("แผ่น 1×2", 2, "S", "plate"),
    "slope_2x2": ("หลังคาเอียง 2×2", 2, "M", "slope"), "tile_1x2": ("แผ่นเรียบ 1×2", 0, "S", "tile"), "round_1x1": ("ปุ่มกลม 1×1", 1, "S", "round"),
    "wheel": ("ล้อ", 0, "M", "special"), "window": ("หน้าต่าง", 0, "M", "special"), "eye_1x1": ("ปุ่มตา 1×1", 1, "S", "special"),
}
COLORS = {"red": "#D0312D", "blue": "#1E5AA8", "yellow": "#F6C21C", "green": "#2E8B3E", "white": "#F4F4F4", "black": "#1B1B1B",
          "gray": "#8A8D91", "orange": "#F07F1D", "brown": "#6B3E26", "pink": "#F29CC0", "tan": "#D9BB7B", "trans_clear": "#DDEEFF"}
COLOR_TH = {"red": "แดง", "blue": "น้ำเงิน", "yellow": "เหลือง", "green": "เขียว", "white": "ขาว", "black": "ดำ", "gray": "เทา",
            "orange": "ส้ม", "brown": "น้ำตาล", "pink": "ชมพู", "tan": "ครีม", "trans_clear": "ใส"}
# part that can stand in for another: need 1 × key  ==  give n × value
SUBS = {"brick_2x4": ("brick_2x2", 2), "brick_2x2": ("brick_1x2", 2), "brick_1x4": ("brick_1x2", 2), "brick_1x2": ("brick_1x1", 2),
        "plate_2x4": ("plate_2x2", 2), "plate_2x2": ("plate_1x2", 2), "tile_1x2": ("plate_1x2", 1), "round_1x1": ("brick_1x1", 1),
        "eye_1x1": ("round_1x1", 1)}
# roles map to the colour picked from the pile (most plentiful colour that has enough pieces)
BUILDS = {
    "race_car":   {"th": "รถแข่งจิ๋ว",       "cat": "vehicle",  "min": 8,  "level": 1, "age": 4, "need": {"plate_2x4": 2, "brick_2x2": 2, "brick_1x2": 2, "slope_2x2": 1, "wheel": 4, "tile_1x2": 1}},
    "duck":       {"th": "เป็ดน้อย",         "cat": "animal",   "min": 5,  "level": 1, "age": 4, "need": {"brick_2x4": 1, "brick_2x2": 2, "brick_1x2": 1, "slope_2x2": 1, "eye_1x1": 2}},
    "house":      {"th": "บ้านหลังคาแดง",    "cat": "home",     "min": 15, "level": 2, "age": 5, "need": {"plate_2x4": 2, "brick_2x4": 4, "brick_1x2": 6, "window": 1, "slope_2x2": 4}},
    "rocket":     {"th": "จรวดสู่ดวงจันทร์", "cat": "vehicle",  "min": 12, "level": 2, "age": 5, "need": {"brick_2x2": 6, "slope_2x2": 2, "brick_1x1": 4, "round_1x1": 3, "plate_2x2": 2}},
    "robot":      {"th": "หุ่นยนต์ยิ้มแป้น", "cat": "character", "min": 10, "level": 2, "age": 5, "need": {"brick_2x4": 2, "brick_2x2": 2, "brick_1x2": 4, "eye_1x1": 2, "plate_1x2": 2, "brick_1x1": 2}},
    "dino":       {"th": "ไดโนเสาร์ทีเร็กซ์", "cat": "animal",  "min": 18, "level": 3, "age": 7, "need": {"brick_2x4": 3, "brick_2x2": 4, "brick_1x4": 2, "brick_1x2": 4, "slope_2x2": 3, "eye_1x1": 2, "plate_1x2": 2}},
    "phone_stand": {"th": "ที่วางมือถือ",    "cat": "useful",   "min": 7,  "level": 1, "age": 6, "need": {"plate_2x4": 2, "brick_2x4": 3, "brick_1x4": 2, "slope_2x2": 2}},
    "pencil_cup": {"th": "กล่องใส่ดินสอ",   "cat": "useful",   "min": 14, "level": 2, "age": 6, "need": {"plate_2x4": 2, "brick_2x4": 6, "brick_2x2": 4, "brick_1x2": 4}},
    "xmas_tree":  {"th": "ต้นคริสต์มาส",     "cat": "seasonal", "min": 10, "level": 2, "age": 5, "need": {"plate_2x4": 1, "brick_2x4": 2, "brick_2x2": 3, "plate_2x2": 3, "round_1x1": 6, "brick_1x1": 1}},
    "snowman":    {"th": "ตุ๊กตาหิมะ",       "cat": "seasonal", "min": 6,  "level": 1, "age": 4, "need": {"brick_2x2": 4, "brick_1x2": 2, "eye_1x1": 2, "round_1x1": 1, "plate_2x2": 1}},
    "ny_2027":    {"th": "ป้ายปีใหม่ 2027",  "cat": "seasonal", "min": 20, "level": 3, "age": 7, "need": {"plate_2x4": 4, "brick_1x2": 14, "brick_1x1": 8, "tile_1x2": 4}},
    "boat":       {"th": "เรือใบ",           "cat": "vehicle",  "min": 9,  "level": 1, "age": 5, "need": {"plate_2x4": 2, "brick_2x4": 2, "slope_2x2": 2, "brick_1x1": 3, "tile_1x2": 2}},
    "flower":     {"th": "กระถางดอกไม้",    "cat": "home",     "min": 6,  "level": 1, "age": 4, "need": {"brick_2x2": 2, "brick_1x1": 2, "round_1x1": 4, "plate_1x2": 2}},
    "castle_tower": {"th": "หอคอยปราสาท",   "cat": "home",     "min": 25, "level": 3, "age": 8, "need": {"brick_2x4": 8, "brick_2x2": 6, "brick_1x2": 6, "brick_1x1": 4, "window": 1}},
}
ROLE_KIND = {"brick": "main", "slope": "accent", "plate": "base", "tile": "detail", "round": "detail", "special": "fixed"}
CHALLENGES = [("animal", "สัตว์ที่มีขา 4 ขา", 20, 10), ("vehicle", "ยานพาหนะที่วิ่งได้จริง", 25, 12), ("tall", "ตึกให้สูงที่สุดไม่ล้ม", 40, 8),
              ("color", "ใช้แค่ 2 สี", 20, 10), ("tiny", "ของจิ๋วไม่เกิน 10 ชิ้น", 10, 5), ("seasonal", "ของขวัญปีใหม่", 30, 15),
              ("face", "หน้าคนในครอบครัว (แบบการ์ตูน)", 25, 10)]
GUARD = {None: ("ok", "เล่นให้สนุก! ตัวต่อชิ้นเล็กไม่เหมาะกับเด็กต่ำกว่า 3 ปี"),
         "toddler_small_parts": ("stop", "เด็กต่ำกว่า 3 ปีห้ามเล่นชิ้นเล็ก (เสี่ยงติดคอ) — เปลี่ยนเป็นตัวต่อชิ้นใหญ่สำหรับเด็กเล็ก"),
         "swallowed_part": ("stop", "ถ้าเด็กกลืนชิ้นส่วน/หายใจลำบาก โทร 1669 หรือไปโรงพยาบาลทันที ห้ามล้วงคอ"),
         "under_13_no_parent": ("stop", "อายุต่ำกว่า 13 ปี ให้ผู้ปกครองเปิดกล้องและยืนยันก่อนใช้"),
         "face_in_photo": ("warn", "เห็นหน้าคนในรูป ระบบจะเบลออัตโนมัติก่อนส่ง AI"),
         "official_set_copy": ("stop", "แอปไม่คัดลอกคู่มือชุดลิขสิทธิ์ของแบรนด์ — สร้างได้เฉพาะไอเดียต้นฉบับจากกองของคุณ"),
         "not_bricks": ("warn", "มีของที่ไม่ใช่ตัวต่อในรูป (เหรียญ/ถ่าน/แม่เหล็ก) เก็บให้พ้นมือเด็กก่อน"),
         "battery_or_magnet": ("stop", "เห็นถ่านกระดุมหรือแม่เหล็กในกอง อันตรายมากถ้ากลืน — เก็บออกก่อนเล่น")}
REEL_SHOTS = [("pile", "เทตัวต่อกองใหญ่ \"กองนี้ต่ออะไรได้?\""), ("scan", "ถ่ายรูป ประกายสแกนนับชิ้น"), ("ideas", "การ์ดไอเดีย 6 แบบเด้งขึ้น"),
              ("steps", "ทำตามทีละขั้น ไฮไลต์ชิ้นในกอง"), ("reveal", "ของเสร็จหมุนโชว์ + คะแนนดาว"), ("cta", "คอมเมนต์ BRICK รับแพ็กฟรี")]
GRID_COLS = "ABCDEF"


def _r(x, n=2):
    return round(x + 0.0, n)


def scan_quality(light, blur, spread, overlap):
    """light/blur/spread/overlap 0..1 → score 0..100. spread = pieces laid out in one layer, overlap = pieces stacked on each other."""
    for v in (light, blur, spread, overlap):
        if not 0 <= v <= 1:
            raise ValueError("inputs must be 0..1")
    score = round(100 * (0.3 * light + 0.25 * (1 - blur) + 0.25 * spread + 0.2 * (1 - overlap)))
    tips = []
    if light < 0.6: tips.append("เปิดไฟหรือย้ายไปใกล้หน้าต่าง")
    if blur > 0.3: tips.append("ถือมือถือนิ่ง ๆ แตะจอให้โฟกัส")
    if spread < 0.6: tips.append("เกลี่ยตัวต่อให้เป็นชั้นเดียวบนพื้นสีพื้น ๆ")
    if overlap > 0.4: tips.append("แยกชิ้นที่ต่อติดกันหรือทับกันออกก่อน")
    return {"score": score, "ok": score >= 70 and not tips, "tips_th": tips}


def pile_scan(photo):
    return {"photo_id": photo["id"], "quality": scan_quality(photo["light"], photo["blur"], photo["spread"], photo["overlap"])}


def grid_cell(x, y):
    """position in photo (0..1) → grid label A1..F4 for the Find-It highlight."""
    if not (0 <= x <= 1 and 0 <= y <= 1):
        raise ValueError("position must be 0..1")
    return GRID_COLS[min(5, int(x * 6))] + str(min(3, int(y * 4)) + 1)


def inventory(pieces):
    """pieces: [{part, color, count}] from the vision model (low-confidence rows dropped) → counts by part / colour."""
    by_part, by_color, studs = {}, {}, 0
    for p in pieces:
        if p["part"] not in PARTS or p["color"] not in COLORS:
            raise ValueError("unknown part/colour: %s %s" % (p["part"], p["color"]))
        if p.get("confidence", 1) < 0.5:
            continue
        by_part[p["part"]] = by_part.get(p["part"], 0) + p["count"]
        by_color[p["color"]] = by_color.get(p["color"], 0) + p["count"]
        studs += PARTS[p["part"]][1] * p["count"]
    total = sum(by_part.values())
    top = sorted(by_color, key=lambda c: (-by_color[c], c))[:3]
    return {"total": total, "studs": studs, "by_part": dict(sorted(by_part.items())), "by_color": dict(sorted(by_color.items())),
            "top_colors": top, "kinds": len(by_part)}


def _take(have, part, n):
    """take n of part from have (mutates); if short, use ONE level of substitution (e.g. 2× brick_2x2 for a brick_2x4)."""
    got = min(have.get(part, 0), n)
    have[part] = have.get(part, 0) - got
    missing, subs = n - got, []
    if missing and part in SUBS:
        alt, k = SUBS[part]
        covered = min(missing, have.get(alt, 0) // k)
        if covered:
            have[alt] -= covered * k
            subs.append({"need": part, "use": alt, "per": k, "count": covered})
        missing -= covered
    return missing, subs


def match_build(build_id, inv):
    b = BUILDS[build_id]
    have = dict(inv["by_part"])
    need_total = sum(b["need"].values())
    missing, subs = {}, []
    short = {}
    for part, n in b["need"].items():  # pass 1: exact parts first so substitutes never steal a part needed as-is
        got = min(have.get(part, 0), n); have[part] = have.get(part, 0) - got
        if n - got:
            short[part] = n - got
    for part, m0 in short.items():     # pass 2: substitutions for what is still short
        m, s = _take(have, part, m0)
        if m:
            missing[part] = m
        subs += s
    have_n = need_total - sum(missing.values())
    pct = round(100 * have_n / need_total)
    return {"build": build_id, "name_th": b["th"], "category": b["cat"], "minutes": b["min"], "level": b["level"], "match_pct": pct,
            "can_build": not missing, "missing": missing, "substitutions": subs,
            "pieces": need_total}


def suggest_builds(inv, age, max_minutes=30, top=6):
    """rank every catalogue build: buildable first, then match %, then quicker; respects age & time."""
    out = []
    for bid, b in BUILDS.items():
        if b["age"] > age or b["min"] > max_minutes:
            continue
        out.append(match_build(bid, inv))
    out.sort(key=lambda m: (not m["can_build"], -m["match_pct"], len(m["substitutions"]), m["minutes"], m["build"]))
    return out[:top]


def assign_colors(build_id, pieces):
    """pick one colour per role from what the pile actually has (most plentiful colour of that part kind)."""
    b = BUILDS[build_id]
    roles = {}
    for part in b["need"]:
        role = ROLE_KIND[PARTS[part][3]]
        if role == "fixed" or role in roles:
            continue
        pool = {}
        for p in pieces:
            if ROLE_KIND[PARTS[p["part"]][3]] == role:
                pool[p["color"]] = pool.get(p["color"], 0) + p["count"]
        if pool:
            roles[role] = sorted(pool, key=lambda c: (-pool[c], c))[0]
    if build_id in ("xmas_tree",) and "main" in roles:
        roles["main"] = "green" if any(p["color"] == "green" for p in pieces) else roles["main"]
    return {"build": build_id, "roles": roles, "hex": {r: COLORS[c] for r, c in roles.items()}}


def build_steps(build_id, colors):
    """layer-by-layer steps: base plates → bricks (bottom up, 2 kinds per step max) → slopes → details/specials."""
    b = BUILDS[build_id]
    order = {"plate": 0, "brick": 1, "slope": 2, "special": 3, "tile": 4, "round": 4}
    parts = sorted(b["need"].items(), key=lambda kv: (order[PARTS[kv[0]][3]], -PARTS[kv[0]][1], kv[0]))
    steps, n = [], 0
    for part, cnt in parts:
        kind = PARTS[part][3]
        role = ROLE_KIND[kind]
        color = colors["roles"].get(role, "gray") if role != "fixed" else None
        per = 4 if kind == "brick" else cnt
        left = cnt
        while left:
            take = min(per, left); left -= take; n += 1
            tip = {"plate": "วางเป็นฐานให้แน่น กดให้ได้ยินเสียงคลิก", "brick": "วางเหลื่อมรอยต่อกับชั้นล่าง จะไม่ล้ม",
                   "slope": "ด้านเอียงหันออกด้านนอก", "special": "ใส่ให้ตรงปุ่ม หมุนดูว่าคล่อง", "tile": "ปิดผิวด้านบนให้เรียบ",
                   "round": "เติมรายละเอียดสุดท้าย"}[kind]
            steps.append({"n": n, "part": part, "name_th": PARTS[part][0], "color": color, "count": take, "tip_th": tip})
    return {"build": build_id, "steps": steps, "step_count": len(steps), "minutes": b["min"]}


def find_piece(pieces, part, color):
    """Find-It: where in the photo is this piece? returns grid cells sorted, or a friendly not-found."""
    cells = sorted({grid_cell(*pos) for p in pieces if p["part"] == part and p["color"] == color for pos in p.get("positions", [])})
    return {"part": part, "color": color, "found": bool(cells), "cells": cells,
            "hint_th": ("ดูช่อง " + ", ".join(cells)) if cells else "ไม่เจอในรูป ลองใช้ชิ้นทดแทนหรือเกลี่ยกองแล้วถ่ายใหม่"}


def sort_plan(inv, bins=4, by="color"):
    """split the pile into N boxes by colour or size, balancing counts (largest groups first)."""
    if by not in ("color", "size"):
        raise ValueError("by must be color or size")
    if bins < 2:
        raise ValueError("need ≥ 2 bins")
    if by == "color":
        groups = dict(inv["by_color"])
    else:
        groups = {}
        for part, n in inv["by_part"].items():
            groups[PARTS[part][2]] = groups.get(PARTS[part][2], 0) + n
    boxes = [{"box": i + 1, "groups": [], "count": 0} for i in range(bins)]
    for g in sorted(groups, key=lambda k: (-groups[k], k)):
        bx = min(boxes, key=lambda x: (x["count"], x["box"]))
        bx["groups"].append(g); bx["count"] += groups[g]
    spread = max(x["count"] for x in boxes) - min(x["count"] for x in boxes)
    return {"by": by, "bins": bins, "boxes": boxes, "balance_gap": spread}


def stability(layers, base_studs, stagger_pct):
    """quick wobble check for towers: taller vs base, and how many seams are staggered (brick bond)."""
    if layers < 1 or base_studs < 1 or not 0 <= stagger_pct <= 100:
        raise ValueError("bad input")
    ratio = layers / max(1, base_studs ** 0.5 * 2)
    score = max(0, min(100, round(100 - max(0, ratio - 1) * 35 - (100 - stagger_pct) * 0.4)))
    level = "solid" if score >= 75 else ("wobbly" if score >= 45 else "will_fall")
    tip = {"solid": "แข็งแรงดี ต่อได้อีก", "wobbly": "เพิ่มฐานให้กว้างขึ้น หรือวางเหลื่อมรอยต่อให้มากขึ้น",
           "will_fall": "ฐานเล็กเกินไปสำหรับความสูงนี้ ขยายฐานเป็น 2 เท่าก่อนต่อขึ้น"}[level]
    return {"layers": layers, "base_studs": base_studs, "stagger_pct": stagger_pct, "score": score, "level": level, "tip_th": tip}


def daily_challenge(date):
    d = _dt.date.fromisoformat(date)
    key, th, cap, mins = CHALLENGES[d.toordinal() % len(CHALLENGES)]
    if d.month == 12 and d.day >= 20 or d.month == 1 and d.day <= 3:
        key, th, cap, mins = CHALLENGES[5]
    return {"date": date, "theme": key, "title_th": th, "max_pieces": cap, "minutes": mins, "badge": "challenge_" + key}


def creation_score(pieces_used, colors_used, symmetry, layers, on_theme, max_pieces=None):
    """kid-friendly score: always ≥ 1 star, never negative wording."""
    if not 0 <= symmetry <= 1:
        raise ValueError("symmetry 0..1")
    pts = min(30, pieces_used) + min(5, colors_used) * 4 + round(symmetry * 20) + min(10, layers) * 2 + (15 if on_theme else 0)
    over = max_pieces is not None and pieces_used > max_pieces
    if over:
        pts -= 10
    pts = max(5, min(100, pts))
    stars = 1 + min(4, pts // 20)
    badges = []
    if colors_used >= 5: badges.append("rainbow")
    if symmetry >= 0.8: badges.append("symmetry_star")
    if layers >= 10: badges.append("sky_high")
    if on_theme and not over: badges.append("challenge_done")
    cheer = ["เริ่มต้นได้ดีมาก!", "เยี่ยมเลย ลองเพิ่มสีอีกนิด", "สวยมาก! ครอบครัวต้องชอบ", "สุดยอดนักสร้าง!", "ระดับมาสเตอร์บิลเดอร์!"][stars - 1]
    return {"points": pts, "stars": stars, "badges": badges, "over_limit": over, "cheer_th": cheer}


def diary_summary(entries, today):
    days = sorted({e["date"] for e in entries})
    streak, d = 0, _dt.date.fromisoformat(today)
    while d.isoformat() in days:
        streak += 1; d -= _dt.timedelta(days=1)
    builds = [e for e in entries if e["kind"] == "build"]
    badges = sorted({b for e in entries for b in e.get("badges", [])})
    best = max((e.get("stars", 0) for e in builds), default=0)
    return {"today": today, "builds": len(builds), "challenges": sum(e["kind"] == "challenge" for e in entries),
            "pieces_used": sum(e.get("pieces", 0) for e in builds), "streak": streak, "best_stars": best, "badges": badges}


def share_card(name_th, stars, layout="before_after"):
    if layout not in ("before_after", "steps_grid", "badge"):
        raise ValueError("layout")
    return {"name_th": name_th, "stars": stars, "layout": layout, "size": "1080x1350", "watermark": "BrickBuddy · AI วันละแอป",
            "badge_th": "ต่อจากกองเดิมที่บ้าน ไม่ต้องซื้อเพิ่ม"}


def reel_plan(build_th, seconds=20):
    if not 15 <= seconds <= 30:
        raise ValueError("Reel must be 15–30 s")
    n = len(REEL_SHOTS); cut = [round(seconds * i / n, 1) for i in range(n + 1)]
    return {"build": build_th, "seconds": seconds, "ratio": "9:16", "bpm": 118,
            "shots": [{"kind": k, "start": cut[i], "end": cut[i + 1], "caption_th": c} for i, (k, c) in enumerate(REEL_SHOTS)],
            "watermark": "BrickBuddy · AI วันละแอป"}


def quota(used_today, plan="free"):
    limit = {"free": 3, "plus": 30}[plan]
    return {"plan": plan, "scans_per_day": limit, "used": used_today, "left": max(0, limit - used_today), "blocked": used_today >= limit}


def age_check(age, parent_ok=False, found=()):
    """found: hazards spotted by the vision model ('battery', 'magnet', 'coin', 'face')."""
    flags = []
    if age < 3: flags.append("toddler_small_parts")
    if age < 13 and not parent_ok: flags.append("under_13_no_parent")
    if "battery" in found or "magnet" in found: flags.append("battery_or_magnet")
    if "coin" in found: flags.append("not_bricks")
    if "face" in found: flags.append("face_in_photo")
    level = "stop" if any(GUARD[f][0] == "stop" for f in flags) else ("warn" if flags else "ok")
    return {"allowed": level != "stop", "level": level, "flags": flags, "messages_th": [GUARD[f][1] for f in flags] or [GUARD[None][1]]}


def safety_guard(flag=None):
    level, msg = GUARD[flag]
    return {"flag": flag, "level": level, "message_th": msg, "block": level == "stop"}
