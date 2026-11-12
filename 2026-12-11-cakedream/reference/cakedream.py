"""CakeDream deterministic logic (no AI calls). Cake design + party planner — mock-ups and prices are estimates only."""
import math, unicodedata

THEMES = {
    "dinosaur":      {"th": "ไดโนเสาร์",          "palette": ["#7CC36B", "#F4D35E", "#5B8C3A"], "cx": 3, "toppers": ["ไดโนฟองดองต์", "ภูเขาไฟช็อกโกแลต", "ใบไม้น้ำตาล"]},
    "unicorn":       {"th": "ยูนิคอร์น",          "palette": ["#F9C6D9", "#B8A9F0", "#FFFFFF"], "cx": 3, "toppers": ["เขาทอง", "หูฟองดองต์", "ดอกครีมพาสเทล"]},
    "korean_minimal": {"th": "มินิมอลเกาหลี",     "palette": ["#F3E9DC", "#C9A36A", "#FFFFFF"], "cx": 1, "toppers": ["ขอบครีมวินเทจ", "ตัวอักษรไอซิ่ง"]},
    "floral":        {"th": "ดอกไม้ครีม",         "palette": ["#F7B2BD", "#FFE5EC", "#6BA368"], "cx": 2, "toppers": ["กุหลาบครีมบีบ", "ใบไม้ครีม"]},
    "football":      {"th": "ฟุตบอล",            "palette": ["#2E8B57", "#FFFFFF", "#1A1A1A"], "cx": 2, "toppers": ["ลูกบอลฟองดองต์", "ประตูช็อกโกแลต"]},
    "princess":      {"th": "เจ้าหญิง / ปราสาท",   "palette": ["#F8C8DC", "#E6C36A", "#FFFFFF"], "cx": 4, "toppers": ["ปราสาทน้ำตาล", "มงกุฎทอง", "ไข่มุกน้ำตาล"]},
    "cartoon_bear":  {"th": "หมีการ์ตูน",         "palette": ["#C68B59", "#FCE5CD", "#FFFFFF"], "cx": 2, "toppers": ["หน้าหมีฟองดองต์", "หูช็อกโกแลต"]},
    "gold_luxury":   {"th": "ทองหรู (ผู้ใหญ่)",     "palette": ["#1A1A1A", "#D4AF37", "#FFFFFF"], "cx": 3, "toppers": ["แผ่นทองกินได้", "ดริปช็อกโกแลต"]},
}
FLAVORS = {
    "vanilla_chiffon": {"th": "ชิฟฟอนวานิลลา",     "add": 0,   "allergens": ["egg", "dairy", "gluten"]},
    "chocolate":       {"th": "ช็อกโกแลตฟัดจ์",    "add": 60,  "allergens": ["egg", "dairy", "gluten"]},
    "thai_tea":        {"th": "ชาไทย",            "add": 40,  "allergens": ["egg", "dairy", "gluten"]},
    "pandan_coconut":  {"th": "ใบเตยมะพร้าวอ่อน",   "add": 40,  "allergens": ["egg", "gluten"]},
    "strawberry":      {"th": "สตรอว์เบอร์รีครีมสด", "add": 80,  "allergens": ["egg", "dairy", "gluten"]},
    "almond_crunch":   {"th": "อัลมอนด์ครันช์",     "add": 70,  "allergens": ["egg", "dairy", "gluten", "nuts"]},
    "eggless_choc":    {"th": "ช็อกโกแลตไม่ใส่ไข่",   "add": 90,  "allergens": ["dairy", "gluten"]},
}
ALLERGENS = {"egg": "ไข่", "dairy": "นม", "gluten": "แป้งสาลี (กลูเตน)", "nuts": "ถั่ว / อัลมอนด์"}
# pounds → (shape, diameter inches, servings party slice)
SIZES = {0.5: ("round", 4, 3), 1: ("round", 6, 7), 1.5: ("round", 7, 10), 2: ("round", 8, 14),
         3: ("round", 9, 20), 4: ("round", 10, 26), 5: ("tier2", 10, 34), 6: ("tier2", 11, 40), 8: ("tier3", 12, 54)}
BASE_PER_LB = 420          # THB, plain cream cake per pound (example figure)
CX_MULT = {1: 1.0, 2: 1.15, 3: 1.35, 4: 1.6}
REGION_MULT = {"bkk": 1.15, "metro": 1.05, "province": 0.9}
TOPPER_EACH = 80
LEAD_DAYS = {1: 1, 2: 2, 3: 3, 4: 5}
DISCLAIMER = "ภาพจำลองและราคาเป็นค่าประมาณ ร้านจริงอาจทำได้ต่างจากภาพ แจ้งเรื่องแพ้อาหารกับร้านทุกครั้ง"


def _rng(x, lo, hi, name):
    if not isinstance(x, (int, float)) or x < lo or x > hi:
        raise ValueError(f"{name} out of range")


def scan_quality(glare, blur, crop):
    for v, n in ((glare, "glare"), (blur, "blur"), (crop, "crop")):
        _rng(v, 0, 1, n)
    score = round(100 - glare * 35 - blur * 40 - crop * 25)
    tips = []
    if glare > 0.3: tips.append("แสงสะท้อนเยอะ ถ่ายรูปตัวอย่างใหม่ไม่ใช้แฟลช")
    if blur > 0.3: tips.append("ภาพเบลอ ถือนิ่ง ๆ แล้วถ่ายใหม่")
    if crop > 0.3: tips.append("เค้กโดนครอป ถ่ายให้เห็นทั้งก้อน")
    return {"score": max(0, score), "ok": score >= 70, "tips_th": tips}


def ref_scan(photo):
    return {"photo_id": photo["id"], "quality": scan_quality(photo["glare"], photo["blur"], photo["crop"])}


def size_for_servings(n):
    if not isinstance(n, int) or n < 1: raise ValueError("servings must be ≥1")
    for lb in sorted(SIZES):
        if SIZES[lb][2] >= n: return lb
    raise ValueError("too many servings for one cake (max 54) — split into 2 cakes")


def serving_calc(adults, kids, appetite="normal", leftovers=False):
    for v, nm in ((adults, "adults"), (kids, "kids")):
        if not isinstance(v, int) or v < 0: raise ValueError(nm)
    if adults + kids == 0: raise ValueError("no guests")
    if appetite not in ("light", "normal", "dessert_lovers"): raise ValueError("appetite")
    m = {"light": 0.8, "normal": 1.0, "dessert_lovers": 1.3}[appetite]
    need = math.ceil((adults + kids * 0.6) * m * (1.2 if leftovers else 1.0))
    lb = size_for_servings(need)
    shape, dia, serv = SIZES[lb]
    return {"guests": adults + kids, "adults": adults, "kids": kids, "servings_needed": need, "pounds": lb,
            "shape": shape, "diameter_in": dia, "servings_capacity": serv,
            "headline_th": f"แขก {adults + kids} คน → เค้ก {_lb(lb)} ปอนด์ ({dia} นิ้ว) ได้ {serv} ชิ้น"}


def _lb(lb):
    return str(int(lb)) if float(lb).is_integer() else str(lb)


def glyphs(text):
    """Visible character count (Thai vowels/tone marks stacked above/below don't take width)."""
    return sum(1 for ch in text if not unicodedata.combining(ch) and ch not in "\u0e31\u0e34\u0e35\u0e36\u0e37\u0e38\u0e39\u0e3a\u0e47\u0e48\u0e49\u0e4a\u0e4b\u0e4c\u0e4d\u0e4e" and not ch.isspace()) + text.count(" ") // 2


def message_fit(text, pounds):
    if pounds not in SIZES: raise ValueError("unknown size")
    if not isinstance(text, str) or not text.strip(): raise ValueError("empty message")
    dia = SIZES[pounds][1]
    limit = int(dia * 2.5)
    n = glyphs(text)
    lines = 1 if n <= limit else 2
    fits = n <= limit * 2
    tip = "" if n <= limit else ("แบ่ง 2 บรรทัดได้" if fits else f"ยาวเกิน ตัดให้เหลือไม่เกิน {limit * 2} ตัว")
    return {"text": text, "glyphs": n, "limit_per_line": limit, "lines": lines, "fits": fits, "tip_th": tip}


def design_spec(theme, flavor, pounds, message, extra_toppers=0):
    if theme not in THEMES: raise ValueError("theme")
    if flavor not in FLAVORS: raise ValueError("flavor")
    if pounds not in SIZES: raise ValueError("size")
    if not isinstance(extra_toppers, int) or not 0 <= extra_toppers <= 5: raise ValueError("toppers 0-5")
    t = THEMES[theme]; shape, dia, serv = SIZES[pounds]
    cx = min(4, t["cx"] + (1 if shape != "round" else 0) + (1 if extra_toppers >= 3 else 0))
    mf = message_fit(message, pounds)
    tier = {"round": "", "tier2": "2-tier ", "tier3": "3-tier "}[shape]
    prompt = (f"studio photo of a {tier}{dia}-inch {theme.replace('_', ' ')} themed birthday cake, palette {', '.join(t['palette'])}, "
              f"{len(t['toppers']) + extra_toppers} toppers, piped message on top, soft daylight, 4:5, no logos, no real people")
    return {"theme": theme, "theme_th": t["th"], "flavor": flavor, "flavor_th": FLAVORS[flavor]["th"], "pounds": pounds,
            "shape": shape, "diameter_in": dia, "palette": t["palette"], "toppers_th": t["toppers"],
            "extra_toppers": extra_toppers, "complexity": cx, "message": mf, "image_prompt": prompt, "disclaimer_th": DISCLAIMER}


def price_estimate(spec, region="bkk"):
    if region not in REGION_MULT: raise ValueError("region")
    lb = spec["pounds"]
    base = (BASE_PER_LB + FLAVORS[spec["flavor"]]["add"]) * lb * CX_MULT[spec["complexity"]] + spec["extra_toppers"] * TOPPER_EACH
    mid = round(base * REGION_MULT[region] / 10) * 10
    return {"region": region, "low": round(mid * 0.85 / 10) * 10, "mid": mid, "high": round(mid * 1.25 / 10) * 10,
            "per_serving": round(mid / SIZES[lb][2]), "disclaimer_th": "ช่วงราคาประมาณการจากค่าตัวอย่าง ไม่ใช่ราคาร้านจริง"}


def fair_price(estimate, quote):
    if not isinstance(quote, (int, float)) or quote <= 0: raise ValueError("quote")
    lo, mid, hi = estimate["low"], estimate["mid"], estimate["high"]
    if quote < lo * 0.8: v, th = "suspicious_low", "ถูกผิดปกติ ถามขนาด/วัตถุดิบให้ชัด"
    elif quote < lo: v, th = "cheap", "ถูกกว่าช่วงปกติ"
    elif quote <= hi: v, th = "fair", "สมเหตุสมผล"
    elif quote <= hi * 1.3: v, th = "pricey", "แพงกว่าช่วงปกติ ลองถามส่วนลดหรือลดท็อปเปอร์"
    else: v, th = "very_pricey", "แพงมาก ลองเทียบร้านอื่น"
    return {"quote": quote, "verdict": v, "verdict_th": th, "diff_from_mid_pct": round((quote - mid) / mid * 100)}


def allergy_guard(flavor, guest_allergies):
    if flavor not in FLAVORS: raise ValueError("flavor")
    for a in guest_allergies:
        if a not in ALLERGENS: raise ValueError("allergen")
    hits = [a for a in guest_allergies if a in FLAVORS[flavor]["allergens"]]
    alts = [k for k, f in FLAVORS.items() if not any(a in f["allergens"] for a in guest_allergies)]
    level = "ok" if not hits else ("stop" if "nuts" in hits else "warn")
    msg = ("ไม่พบสารก่อแพ้ที่แจ้งไว้ในรสนี้ แต่ต้องยืนยันกับร้านอีกครั้ง" if not hits else
           "รสนี้มี " + ", ".join(ALLERGENS[h] for h in hits) + " — เปลี่ยนรสหรือทำเค้กแยกให้คนที่แพ้")
    return {"level": level, "hits": hits, "alternatives": alts, "message_th": msg}


RECIPE_1LB = {"cake_flour": (90, "แป้งเค้ก", 0.06), "sugar": (110, "น้ำตาลทราย", 0.03), "egg": (4, "ไข่ไก่ (ฟอง)", 5.0),
              "oil": (45, "น้ำมันพืช", 0.06), "milk": (60, "นม", 0.05), "whipping_cream": (200, "วิปปิ้งครีม", 0.2),
              "baking_powder": (4, "ผงฟู", 0.3)}


def diy_recipe(pounds, flavor):
    if pounds not in SIZES: raise ValueError("size")
    if flavor != "vanilla_chiffon": raise ValueError("DIY demo covers vanilla_chiffon only")
    rows = []; total = 0
    for k, (q, th, price) in RECIPE_1LB.items():
        qty = math.ceil(q * pounds) if k != "egg" else math.ceil(q * pounds)
        cost = round(qty * price); total += cost
        rows.append({"item": k, "item_th": th, "qty": qty, "unit": "ฟอง" if k == "egg" else "กรัม", "cost_baht": cost})
    bake_min = 35 + int(8 * (pounds - 1)) if pounds >= 1 else 25
    return {"pounds": pounds, "flavor": flavor, "ingredients": rows, "total_cost_baht": total, "bake_minutes": bake_min,
            "oven_c": 170, "steps_th": ["ตีไข่ขาวกับน้ำตาลจนตั้งยอดอ่อน", "ผสมไข่แดง นม น้ำมัน แป้ง ผงฟู", "ตะล่อมรวม เทพิมพ์",
                                         f"อบ 170°C {bake_min} นาที", "พักเย็นคว่ำพิมพ์ แล้วแต่งวิปครีม"]}


def order_deadline(party_date, complexity, today):
    """dates as ISO strings yyyy-mm-dd"""
    from datetime import date, timedelta
    p = date.fromisoformat(party_date); t = date.fromisoformat(today)
    if complexity not in LEAD_DAYS: raise ValueError("complexity")
    d = p - timedelta(days=LEAD_DAYS[complexity])
    left = (d - t).days
    status = "ok" if left >= 2 else ("last_call" if left >= 0 else "too_late")
    return {"party_date": party_date, "order_by": d.isoformat(), "days_left": left, "status": status,
            "message_th": {"ok": f"สั่งร้านภายใน {d.isoformat()} (เหลือ {left} วัน)", "last_call": "ต้องสั่งวันนี้–พรุ่งนี้!",
                           "too_late": "ไม่ทันเวลาทำลายนี้ ลดความซับซ้อนหรือซื้อเค้กหน้าร้าน + ท็อปเปอร์"}[status]}


def order_card(person, spec, servings, est, allergy, deadline):
    lines = [f"สั่งเค้ก: ธีม{spec['theme_th']} รส{spec['flavor_th']}", f"ขนาด {_lb(spec['pounds'])} ปอนด์ ({spec['diameter_in']} นิ้ว) สำหรับ {servings['guests']} คน",
             f"ข้อความบนเค้ก: \"{spec['message']['text']}\"", "สีหลัก: " + " ".join(spec["palette"]),
             "ท็อปเปอร์: " + ", ".join(spec["toppers_th"]), f"งบประมาณ ฿{est['low']:,}–{est['high']:,}",
             f"รับวันที่ {deadline['party_date']}"]
    if allergy["hits"]:
        lines.append("⚠️ มีแขกแพ้: " + ", ".join(ALLERGENS[h] for h in allergy["hits"]))
    return {"to": "ร้านเค้ก (LINE)", "from_th": person["name_th"], "lines_th": lines, "attach": ["mockup_4x5.png"],
            "share_text": "\n".join(lines), "disclaimer_th": DISCLAIMER}


def diary_summary(entries):
    if not entries: raise ValueError("empty diary")
    n = len(entries); spent = sum(e["paid_baht"] for e in entries)
    stars = round(sum(e["stars"] for e in entries) / n, 1)
    return {"count": n, "spent_baht": spent, "avg_stars": stars, "top_theme": max(entries, key=lambda e: e["stars"])["theme"],
            "headline_th": f"{n} ปาร์ตี้ เฉลี่ย {stars} ดาว"}


def share_card(spec, hook_th):
    return {"title_th": f"เค้กธีม{spec['theme_th']}", "hook_th": hook_th, "layout": "idea_to_mockup",
            "sizes": ["1080x1350", "1080x1920"], "watermark": "CakeDream · AI วันละแอป", "cta_th": "ลองออกแบบเค้กของคุณ", "disclaimer_th": DISCLAIMER}


def quota(used_today, free_per_day=3, pro=False):
    if pro: return {"allowed": 1, "left_after": None, "paywall": False}
    if used_today >= free_per_day: return {"allowed": 0, "left_after": 0, "paywall": True}
    return {"allowed": 1, "left_after": free_per_day - used_today - 1, "paywall": False}


def safety_guard(flag=None):
    if flag == "real_brand": return {"level": "stop", "message_th": "ห้ามใช้โลโก้/ตัวละครลิขสิทธิ์บนเค้กสั่งขาย ใช้ธีมทั่วไปแทน"}
    if flag == "nuts": return {"level": "stop", "message_th": "มีแขกแพ้ถั่ว ห้ามสั่งรสที่มีถั่ว และแจ้งร้านเรื่องปนเปื้อน"}
    return {"level": "ok", "message_th": DISCLAIMER}
