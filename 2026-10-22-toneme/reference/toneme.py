"""ToneMe (สีไหนใช่เรา) — deterministic core. AI only locates face regions + checks light; every number comes from here."""
import math
def hex_rgb(h):
    h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
def _lin(c):
    c /= 255; return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
def lab(h):
    r, g, b = (_lin(c) for c in hex_rgb(h))
    x = (0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047
    y = 0.2126 * r + 0.7152 * g + 0.0722 * b
    z = (0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883
    f = lambda t: t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116
    fx, fy, fz = f(x), f(y), f(z)
    return (116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz))
def de(a, b):
    p, q = lab(a), lab(b); return math.dist(p, q)
def hue(h):
    _, a, b = lab(h); return math.degrees(math.atan2(b, a)) % 360

VEIN = {"green": 10, "blue": -10, "mixed": 0, "unsure": 0}
METAL = {"gold": 8, "silver": -8, "both": 0, "unsure": 0}
SEASON_TH = {"spring": "สปริง 🌷", "summer": "ซัมเมอร์ 🌊", "autumn": "ออทัมน์ 🍂", "winter": "วินเทอร์ ❄️"}
SUBS = {"spring": ["light", "true", "bright"], "summer": ["light", "true", "soft"], "autumn": ["soft", "true", "deep"], "winter": ["bright", "true", "deep"]}
SUB_TH = {"light": "Light", "true": "True", "bright": "Bright", "soft": "Soft", "deep": "Deep"}
# name_th, hex  — 12 best colors per season + 4 avoid
PALETTES = {
 "spring": {"best": [("พีชคอรัล", "#FF7F66"), ("แอปริคอต", "#FBB273"), ("เหลืองดอกทานตะวัน", "#FFD23F"), ("เขียวแอปเปิล", "#8DC63F"),
                     ("เทอร์คอยซ์อุ่น", "#2EC4B6"), ("ฟ้าน้ำทะเลใส", "#4FB3E8"), ("แซลมอน", "#FA8072"), ("ครีมงาช้าง", "#FFF4DC"),
                     ("คาราเมลอ่อน", "#C68E5A"), ("ชมพูแตงโม", "#FF6F7D"), ("ม่วงไลแล็กอุ่น", "#B79CED"), ("กรมท่าสว่าง", "#3A5BA0")],
            "avoid": [("ดำสนิท", "#000000"), ("เทาเย็น", "#8E9AAF"), ("เบอร์กันดี", "#6D1A36"), ("ชมพูบานเย็นเย็น", "#C2185B")]},
 "summer": {"best": [("ชมพูกุหลาบฝุ่น", "#D8A1AE"), ("ลาเวนเดอร์", "#B9A7D8"), ("ฟ้าพาสเทล", "#9CC3E4"), ("เขียวเซจเย็น", "#9DB5A0"),
                     ("เทาฟ้า", "#A3B1C2"), ("มินต์หม่น", "#A8D5C9"), ("กรมท่าเทา", "#4A5D7E"), ("ราสเบอร์รีหม่น", "#B5546E"),
                     ("โกโก้เย็น", "#7D6B6B"), ("ขาวนวลเย็น", "#F2F2F7"), ("พลัมอ่อน", "#8E5E8C"), ("ฟ้าเดนิม", "#6E8DB8")],
            "avoid": [("ส้มสด", "#FF6A00"), ("เหลืองมัสตาร์ด", "#D4A017"), ("ดำสนิท", "#000000"), ("น้ำตาลส้ม", "#A0522D")]},
 "autumn": {"best": [("เทอร์ราคอตตา", "#C8553D"), ("มัสตาร์ด", "#D4A017"), ("เขียวขี้ม้า", "#6B7F3A"), ("น้ำตาลอิฐ", "#8B4513"),
                     ("ส้มฟักทอง", "#E07B39"), ("เทียล", "#2A7F7A"), ("ครีมอูฐ", "#C19A6B"), ("เบอร์กันดีอุ่น", "#7B2D26"),
                     ("เขียวมะกอก", "#808000"), ("แซลมอนอิฐ", "#D9775F"), ("ทองเก่า", "#B8860B"), ("ช็อกโกแลต", "#5C3A21")],
            "avoid": [("ชมพูบาร์บี้", "#FF69B4"), ("ฟ้าน้ำแข็ง", "#CDE8F6"), ("ขาวจั๊วะ", "#FFFFFF"), ("เทาเย็น", "#8E9AAF")]},
 "winter": {"best": [("ขาวจั๊วะ", "#FFFFFF"), ("ดำสนิท", "#000000"), ("แดงทับทิม", "#C8102E"), ("บานเย็น", "#C2185B"),
                     ("น้ำเงินรอยัล", "#1F3FBF"), ("มรกต", "#00875A"), ("ม่วงองุ่น", "#5B2A86"), ("ฟ้าน้ำแข็ง", "#CDE8F6"),
                     ("ชมพูช็อกกิ้ง", "#FF1F8E"), ("เทาถ่าน", "#36393F"), ("กรมท่าเข้ม", "#14213D"), ("เงินเย็น", "#C0C6CF")],
            "avoid": [("ส้มฟักทอง", "#E07B39"), ("ครีมอูฐ", "#C19A6B"), ("เขียวขี้ม้า", "#6B7F3A"), ("พีชคอรัล", "#FF7F66")]}}
MAKEUP = {  # family_th, hex
 "spring": {"lip": [("คอรัลพีช", "#F26B5B"), ("ชมพูแตงโม", "#FF6F7D")], "blush": [("พีช", "#F9A27F")], "shadow": [("ทองแชมเปญ", "#E3C08D"), ("น้ำตาลคาราเมล", "#B07A4F")]},
 "summer": {"lip": [("โรสนู้ด", "#C98B95"), ("เบอร์รีหม่น", "#A64D6B")], "blush": [("ชมพูกุหลาบ", "#E3A1B0")], "shadow": [("ทอปเทา", "#A49A9A"), ("ลาเวนเดอร์", "#B9A7D8")]},
 "autumn": {"lip": [("อิฐ", "#B4523C"), ("น้ำตาลส้ม", "#A0522D")], "blush": [("เทอร์ราคอตตา", "#D27D5C")], "shadow": [("บรอนซ์", "#A87437"), ("เขียวมะกอก", "#6B7F3A")]},
 "winter": {"lip": [("แดงบลูเบส", "#B1062C"), ("ฟูเชีย", "#C2185B")], "blush": [("ชมพูเย็น", "#E06C9F")], "shadow": [("เงิน", "#C0C6CF"), ("กรมท่า", "#14213D")]}}
HAIR = {"spring": [("น้ำตาลคาราเมล", "#A0683A"), ("น้ำผึ้ง", "#C68E3F")], "summer": [("น้ำตาลเทาแอช", "#7A6A5E"), ("โรสบราวน์", "#8C5E5E")],
        "autumn": [("น้ำตาลช็อกโกแลต", "#5C3A21"), ("แดงทองแดง", "#8B3A1E")], "winter": [("ดำธรรมชาติ", "#1B1B1B"), ("น้ำตาลเข้มเย็น", "#3B2F2F")]}
METAL_TIP = {"spring": "gold", "autumn": "gold", "summer": "silver", "winter": "silver"}

def analyze(skin, hair, eyes, vein="unsure", metal="unsure", light_ok=True):
    """skin/hair/eyes = sampled hex. Returns the season profile."""
    if not light_ok: raise ValueError("bad_light")
    if vein not in VEIN or metal not in METAL: raise ValueError("bad_quiz")
    ls, lh, le = lab(skin)[0], lab(hair)[0], lab(eyes)[0]
    warmth = round((hue(skin) - 58) * 2 + VEIN[vein] + METAL[metal])
    lightness = round(ls * 0.6 + lh * 0.25 + le * 0.15)
    contrast = round(abs(ls - lh))
    warm, light, clear = warmth >= 0, lightness >= 50, contrast >= 45
    season = ("spring" if light else "autumn") if warm else ("summer" if light else "winter")
    t, v, c = min(abs(warmth) / 20, 1), min(abs(lightness - 50) / 15, 1), min(abs(contrast - 45) / 15, 1)
    dom = max([("t", t), ("v", v), ("c", c)], key=lambda x: x[1])[0]
    sub = "true" if dom == "t" else ("light" if light else "deep") if dom == "v" else ("bright" if clear else "soft")
    if sub not in SUBS[season]: sub = "true"
    conf = round(50 + 40 * (t + v + c) / 3)
    return {"season": season, "sub": sub, "label": f"{SUB_TH[sub]} {season.capitalize()}", "label_th": SEASON_TH[season],
            "warmth": warmth, "lightness": lightness, "contrast": contrast,
            "undertone": "warm" if warm else "cool", "depth": "light" if light else "deep", "chroma": "clear" if clear else "soft",
            "confidence": min(conf, 95), "metal": METAL_TIP[season]}

def nearest(season, hx):
    best = min(PALETTES[season]["best"], key=lambda p: de(hx, p[1]))
    return best, de(hx, best[1])
def color_score(season, hx):
    (name, ph), d = nearest(season, hx)
    avoid_d = min(de(hx, a[1]) for a in PALETTES[season]["avoid"])
    s = 100 - d * 1.5
    if avoid_d < 15: s -= (15 - avoid_d) * 3
    return max(0, min(100, round(s))), name, ph
def verdict(s):
    return ("ใช่เลย 💖", "yes") if s >= 75 else ("พอได้ 🙂", "maybe") if s >= 50 else ("ไม่ใช่ทาง 🙅", "no")

def drape_battle(profile, a, b):
    sa, na, _ = color_score(profile["season"], a); sb, nb, _ = color_score(profile["season"], b)
    win = "a" if sa >= sb else "b"
    return {"a": {"hex": a, "score": sa, "near_th": na}, "b": {"hex": b, "score": sb, "near_th": nb}, "winner": win,
            "gap": abs(sa - sb), "line_th": f"สี{'A' if win == 'a' else 'B'} ชนะ +{abs(sa - sb)} หน้าดูสว่างขึ้น"}

def palette_card(profile, name):
    p = PALETTES[profile["season"]]
    return {"name": name, "label": profile["label"], "label_th": profile["label_th"],
            "best": [{"name_th": n, "hex": h} for n, h in p["best"]], "avoid": [{"name_th": n, "hex": h} for n, h in p["avoid"]],
            "metal": profile["metal"], "size_px": [1080, 1920], "watermark": "ToneMe · AI วันละแอป"}

def outfit_check(profile, items):
    """items: [{slot, hex}] — top item weighted x2 (near the face)."""
    rows, tot, w = [], 0, 0
    for it in items:
        s, n, ph = color_score(profile["season"], it["hex"]); v = verdict(s)
        k = 2 if it["slot"] in ("top", "scarf", "glasses") else 1
        tot += s * k; w += k
        rows.append({"slot": it["slot"], "hex": it["hex"], "score": s, "verdict_th": v[0], "verdict": v[1], "swap_hex": ph, "swap_th": n})
    overall = round(tot / w) if w else 0
    worst = min(rows, key=lambda r: r["score"]) if rows else None
    tip = f"เปลี่ยน{SLOT_TH[worst['slot']]}เป็นสี{worst['swap_th']} จะขึ้นเป็นลุคเดียวกันทั้งตัว" if worst and worst["score"] < 75 else "ทั้งชุดอยู่ในพาเลตต์แล้ว ปังมาก"
    return {"overall": overall, "verdict_th": verdict(overall)[0], "items": rows, "tip_th": tip}
SLOT_TH = {"top": "เสื้อ", "bottom": "กางเกง/กระโปรง", "outer": "เสื้อคลุม", "scarf": "ผ้าพันคอ", "bag": "กระเป๋า", "shoes": "รองเท้า", "glasses": "แว่น"}

def makeup(profile):
    m = MAKEUP[profile["season"]]
    return {k: [{"family_th": n, "hex": h} for n, h in v] for k, v in m.items()} | {"note_th": "เป็นโทนสี ไม่ใช่ยี่ห้อ ลองเทียบ swatch ที่ข้อมือในแสงกลางวัน"}

def shop_scan(profile, hx):
    s, n, ph = color_score(profile["season"], hx); v = verdict(s)
    return {"hex": hx, "score": s, "verdict": v[1], "verdict_th": v[0], "near_th": n, "near_hex": ph}

def closet_audit(profile, items):
    res = [shop_scan(profile, i["hex"]) | {"id": i["id"], "name_th": i["name_th"]} for i in items]
    yes = sum(r["verdict"] == "yes" for r in res)
    covered = {r["near_th"] for r in res if r["verdict"] == "yes"}
    missing = [n for n, _ in PALETTES[profile["season"]]["best"] if n not in covered][:3]
    return {"total": len(res), "yes": yes, "maybe": sum(r["verdict"] == "maybe" for r in res), "no": sum(r["verdict"] == "no" for r in res),
            "match_pct": round(100 * yes / len(res)) if res else 0, "items": res, "buy_next_th": missing}

def hair_guide(profile):
    return [{"name_th": n, "hex": h} for n, h in HAIR[profile["season"]]]

def friend_compare(friends):
    """friends: [{name, season}] → group card with best shared color."""
    seasons = [f["season"] for f in friends]
    scores = {}
    for s in PALETTES:
        for n, h in PALETTES[s]["best"]:
            if n in scores: continue
            scores[n] = (sum(color_score(x, h)[0] for x in seasons), h)
    name, (tot, hx) = max(scores.items(), key=lambda kv: (kv[1][0], kv[0]))
    return {"members": friends, "count": {s: seasons.count(s) for s in PALETTES if s in seasons},
            "group_color_th": name, "group_color_hex": hx, "avg_score": round(tot / len(seasons)),
            "line_th": f"ใส่สี{name}ไปด้วยกัน ทุกคนรอด เฉลี่ย {round(tot / len(seasons))}/100"}
