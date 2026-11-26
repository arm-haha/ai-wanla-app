"""PartyPop — deterministic reference logic (port to TypeScript; tests.py is the contract).
The AI only reads the room photo into a draft scan (A1), paints the decorated "after" image (A2) and writes short
fun text (A3–A5). Everything that decides numbers — capacity, the decor list that fits the budget, the budget split,
menu portions, the THB shopping list, the timeline, the game plan, the gift-swap draw and cost sharing — is plain code."""
import math, random, hashlib
from datetime import date as _date, datetime as _dt, timedelta

THEMES = {"countdown_gold": ("เคานต์ดาวน์ทองระยิบ", "Countdown gold", ["#14102B", "#FFC440", "#F5E6B8", "#FF6B8B", "#FFFFFF", "#2A1850"]),
          "cozy_xmas": ("คริสต์มาสอบอุ่น", "Cozy Christmas", ["#B3202A", "#1F6B45", "#F7E8D0", "#E9B949", "#FFFFFF", "#5A2E1A"]),
          "pastel_pop": ("พาสเทลป๊อป", "Pastel pop", ["#FFD6E0", "#C1E1FF", "#D7F9D0", "#FFF1B8", "#E5D4FF", "#FFFFFF"]),
          "thai_fair": ("งานวัดย้อนยุค", "Thai temple fair", ["#E63946", "#F4A261", "#2A9D8F", "#FFD166", "#FFFFFF", "#264653"]),
          "neon_disco": ("นีออนดิสโก้", "Neon disco", ["#0B0B1E", "#FF2E97", "#00E5FF", "#B967FF", "#FFE600", "#FFFFFF"]),
          "minimal_white": ("มินิมอลขาวทอง", "Minimal white & gold", ["#FFFFFF", "#F2EDE4", "#D4AF37", "#C9C2B8", "#8A8178", "#1E1E1E"])}
THEME_KEYS = list(THEMES)
DRESS = {"countdown_gold": "ทอง/ดำ/วิบวับ", "cozy_xmas": "แดง/เขียว", "pastel_pop": "สีพาสเทล", "thai_fair": "ผ้าถุง/เสื้อลายดอก",
         "neon_disco": "สีสะท้อนแสง", "minimal_white": "ขาว/ครีม"}
# decor catalog — generic items, sample THB prices (not real shop prices); qty rule decides how many packs a room needs
# key: (name_th, zone, price, pack_desc, priority 1=first, themes ("*" = all), rule)
DECOR = {"garland": ("ธงราวตัวอักษร HAPPY NEW YEAR", "wall", 59, "ยาว 2 ม./แพ็ก", 1, "*", "wall_m/2"),
         "balloons": ("ลูกโป่งสีธีม", "ceiling", 89, "20 ลูก/แพ็ก", 2, "*", "area*1.5/20"),
         "lights": ("ไฟ LED เส้น (ใช้ถ่าน/USB)", "wall", 129, "5 ม./เส้น", 3, "*", "(wall_m+depth_m)/5"),
         "backdrop": ("ม่านฟอยล์มุมถ่ายรูป", "photo", 79, "1×2 ม./ชิ้น", 4, "*", "1"),
         "number_balloons": ("ลูกโป่งฟอยล์ตัวเลขปีใหม่", "photo", 159, "4 ตัว/ชุด", 5, "countdown_gold,neon_disco,minimal_white,pastel_pop", "1"),
         "tablecloth": ("ผ้าปูโต๊ะลายธีม", "table", 99, "1 ผืน", 6, "*", "tables"),
         "hats": ("หมวกปาร์ตี้ + ที่คาดผม", "guest", 69, "10 ชิ้น/แพ็ก", 7, "*", "guests/10"),
         "props": ("พร็อพถ่ายรูปบนไม้", "photo", 99, "12 ชิ้น/ชุด", 8, "*", "1"),
         "led_candles": ("เทียน LED กลางโต๊ะ", "table", 89, "6 ชิ้น/แพ็ก", 9, "cozy_xmas,minimal_white,countdown_gold", "tables"),
         "mini_tree": ("ต้นคริสต์มาสตั้งโต๊ะ 60 ซม.", "floor", 249, "1 ต้น", 5, "cozy_xmas", "1"),
         "paper_lanterns": ("โคมกระดาษงานวัด", "ceiling", 119, "6 ใบ/แพ็ก", 3, "thai_fair", "wall_m/2"),
         "disco_ball": ("ลูกบอลดิสโก้ + ไฟหมุน USB", "ceiling", 199, "1 ชุด", 3, "neon_disco", "1")}
DECO_SHARE = {"decor": 0.25, "food": 0.50, "drinks": 0.12, "games_gifts": 0.08, "reserve": 0.05}
MIN_FOOD_PER_HEAD = 120      # THB per guest-equivalent; below this suggest potluck
KID_FACTOR = 0.6             # a child eats ~60% of an adult portion
SEAT_M2, STAND_M2, USABLE = 1.2, 0.6, 0.7   # m² per seated / standing guest; share of floor not covered by furniture
# menu styles — per adult portion for the whole party; price per unit and pack size (sample THB)
FOOD = {"meat": ("หมู/ไก่สไลซ์", "kg", 280, 0.5, "ตลาด/ซูเปอร์"), "seafood": ("ลูกชิ้น/ซีฟู้ดรวม", "kg", 220, 0.5, "ตลาด/ซูเปอร์"),
        "veg": ("ผักรวม", "kg", 80, 0.5, "ตลาด/ซูเปอร์"), "noodle": ("วุ้นเส้น/บะหมี่", "kg", 60, 0.5, "ตลาด/ซูเปอร์"),
        "rice": ("ข้าวสาร", "kg", 45, 1.0, "ตลาด/ซูเปอร์"), "sauce": ("น้ำจิ้ม", "L", 90, 0.5, "ตลาด/ซูเปอร์"),
        "snack": ("ขนมขบเคี้ยว", "kg", 220, 0.1, "ซูเปอร์"), "fruit": ("ผลไม้ตัด", "kg", 70, 1.0, "ตลาด/ซูเปอร์"),
        "dessert": ("ขนมหวาน/เค้กชิ้น", "ชิ้น", 25, 1, "ร้านเบเกอรี่"), "drink": ("น้ำอัดลม/น้ำผลไม้", "L", 20, 1.5, "ซูเปอร์"),
        "water": ("น้ำดื่ม", "L", 7, 6.0, "ซูเปอร์"), "ice": ("น้ำแข็ง", "kg", 7, 3.0, "ร้านน้ำแข็ง/ซูเปอร์"),
        "chicken_dish": ("กับข้าวถาด (ไก่/หมู)", "ถาด", 180, 1, "ร้านกับข้าว")}
MENU_STYLES = {"suki": ("สุกี้/ชาบูหม้อไฟฟ้า", {"meat": 0.15, "seafood": 0.10, "veg": 0.15, "noodle": 0.08, "sauce": 0.05, "fruit": 0.12, "dessert": 1}),
               "buffet": ("ข้าว + กับข้าวถาด", {"rice": 0.12, "chicken_dish": 0.2, "veg": 0.08, "fruit": 0.12, "dessert": 1}),
               "snack": ("ของทานเล่นปาร์ตี้", {"snack": 0.12, "fruit": 0.2, "dessert": 2, "chicken_dish": 0.12})}
DRINK_L_PER_H = 0.25         # soft drink + water per adult per hour (water = 60%)
ICE_KG_PER_GUEST = 0.6
GAMES = [  # key, name_th, name_en, min, max, minutes, kid_ok, family_ok, office_ok, props_th
    ("bingo", "บิงโกปีใหม่ (คำทายตามธีม)", "New Year bingo", 4, 40, 20, True, True, True, "การ์ดบิงโกพิมพ์จากแอป + ปากกา"),
    ("charades", "ใบ้คำท่าทาง ละคร/เพลงดัง", "Charades", 4, 30, 15, True, True, True, "การ์ดคำจากแอป"),
    ("pass_parcel", "ส่งกล่องของขวัญตามเพลง", "Pass the parcel", 5, 25, 10, True, True, False, "กล่องห่อหลายชั้น + เพลง"),
    ("musical_chairs", "เก้าอี้ดนตรี", "Musical chairs", 6, 16, 10, True, True, False, "เก้าอี้/เบาะ จำนวนคน − 1"),
    ("year_quiz", "ควิซย้อนปีนี้ (ข่าว/เพลง/มีม)", "Year-in-review quiz", 4, 50, 15, False, True, True, "มือถือทุกคน"),
    ("who_said", "ทายสิใครพูด (คำคมปีนี้ของแต่ละคน)", "Who said it?", 5, 30, 15, False, False, True, "กระดาษโน้ต"),
    ("balloon_pop", "เป่าลูกโป่งชิงคำอวยพร", "Balloon wishes", 4, 20, 10, True, True, True, "ลูกโป่ง + กระดาษคำอวยพร"),
    ("draw_guess", "วาดภาพทายคำ", "Draw & guess", 4, 20, 15, True, True, True, "กระดาษ A4 + ปากกาเมจิก"),
    ("photo_hunt", "ล่าภาพตามโจทย์ในงาน", "Photo hunt", 6, 40, 20, True, True, True, "มือถือ + โจทย์จากแอป"),
    ("lucky_draw", "จับรางวัลประจำงาน", "Lucky draw", 3, 100, 10, True, True, True, "สลากจากแอป")]
GAME = {g[0]: g for g in GAMES}
MONTHS_TH = ["ม.ค.", "ก.พ.", "มี.ค.", "เม.ย.", "พ.ค.", "มิ.ย.", "ก.ค.", "ส.ค.", "ก.ย.", "ต.ค.", "พ.ย.", "ธ.ค."]
GUARD = {None: ("ok", "ข้อมูลและรูปห้องเก็บบนเครื่อง การ์ดเชิญแชร์ได้โดยไม่โชว์ที่อยู่ ตัวเลขราคาเป็นค่าประมาณ"),
         "alcohol_minor": ("stop", "งานนี้มีผู้เยาว์ ไม่ใส่เครื่องดื่มแอลกอฮอล์ในเมนูของเด็ก และไม่มีเกมดื่ม"),
         "drink_drive": ("warn", "ดื่มแล้วไม่ขับ — แอปเพิ่มหัวข้อ 'กลับบ้านปลอดภัย' (เรียกรถ/ค้างคืน/คนขับที่ไม่ดื่ม) ในไทม์ไลน์"),
         "indoor_fire": ("warn", "ห้ามจุดพลุ/ประทัด/เทียนจริงหรือเตาถ่านในห้อง ใช้เทียน LED และหม้อไฟฟ้า เช็กกฎคอนโด/หมู่บ้าน"),
         "over_capacity": ("warn", "แขกเกินพื้นที่ เว้นทางเดินถึงประตู ≥ 80 ซม. ลองย้ายโต๊ะ ใช้ระเบียง หรือแบ่งรอบ"),
         "noise_late": ("warn", "หลังเที่ยงคืนลดเสียงเพลง แจ้งเพื่อนบ้านล่วงหน้า และเคารพกฎอาคาร"),
         "small_kids_balloons": ("warn", "มีเด็กเล็กต่ำกว่า 3 ขวบ เก็บลูกโป่งแตก/ชิ้นเล็กให้พ้นมือ ป้องกันสำลัก"),
         "food_allergy": ("warn", "มีแขกแพ้อาหาร แยกจาน/ป้ายส่วนผสม (ถั่ว กุ้ง นม) ให้ชัด"),
         "photo_of_others": ("warn", "รูปที่มีคนอื่น เบลอหน้าก่อนแชร์ เว้นแต่เขาอนุญาต"),
         "minor": ("warn", "อายุต่ำกว่า 13 ปี ให้ผู้ปกครองช่วยวางแผนงานและเปิด parent mode ก่อนแชร์การ์ดเชิญ")}
REEL_SHOTS = [("hook", "ห้องเดิม ๆ จะจัดปาร์ตี้ปีใหม่ยังไงดี?", 0.12), ("build", "สร้างแอปด้วย AI จากแพ็กนี้", 0.12),
              ("scan", "ถ่ายห้อง + ใส่จำนวนแขก + งบ", 0.14), ("wow", "ปุ๊บ! ห้องกลายเป็นปาร์ตี้", 0.18),
              ("list", "ลิสต์ของ + เมนู ครบในงบ", 0.16), ("swap", "จับสลากของขวัญในแอป", 0.14), ("cta", "คอมเมนต์ PARTY รับแพ็กฟรี", 0.14)]
WATERMARK = "PartyPop · AI วันละแอป"


def d(s):
    return s if isinstance(s, _date) else _date.fromisoformat(s)


def ceil_div(x, step):
    return int(math.ceil(round(x / step, 6)))


def money(x):
    return int(round(x))


# ---------- room ----------
def room_from_scan(scan):
    """AiRoomScan → Room. Code recomputes area, never trusts an AI-written area."""
    w, dep = scan["width_m"], scan["depth_m"]
    if not (1.5 <= w <= 20 and 1.5 <= dep <= 20):
        raise ValueError("room size out of range")
    return {"room_type": scan["room_type"], "width_m": w, "depth_m": dep, "area_m2": round(w * dep, 2),
            "wall_m": w, "tables": max(1, scan["tables"]), "has_balcony": scan["has_balcony"], "rental": scan["rental"]}


def capacity(room, adults, kids=0):
    usable = room["area_m2"] * USABLE
    seated, standing = int(usable // SEAT_M2), int(usable // STAND_M2)
    n = adults + kids
    if n <= seated:
        status, tip = "comfy", "นั่งได้ครบทุกคน สบาย ๆ"
    elif n <= standing:
        status, tip = "mingle", "นั่งได้ %d คน ที่เหลือยืน/นั่งเบาะพื้น จัดโต๊ะอาหารชิดผนังเป็นบุฟเฟต์" % seated
    else:
        status, tip = "over", "เกินพื้นที่ %d คน ลองใช้ระเบียง แบ่งรอบ หรือย้ายโซนอาหาร" % (n - standing)
    return {"guests": n, "seated_max": seated, "standing_max": standing, "status": status, "exit_path_cm": 80, "tip_th": tip,
            "flag": "over_capacity" if status == "over" else None}


# ---------- budget ----------
def guest_eq(adults, kids):
    return round(adults + kids * KID_FACTOR, 2)


def budget_split(total, adults, kids=0):
    if total <= 0 or adults < 1:
        raise ValueError("budget/adults")
    parts = {k: money(total * v) for k, v in DECO_SHARE.items()}
    parts["reserve"] += total - sum(parts.values())          # rounding leftovers go to reserve
    ge = guest_eq(adults, kids)
    per_head = money(total / (adults + kids))
    food_per = round(parts["food"] / ge, 1)
    potluck = food_per < MIN_FOOD_PER_HEAD
    tip = ("งบอาหารต่อคนน้อย ลองให้แขกถือมาคนละ 1 จาน (Potluck) แอปแบ่งให้ว่าใครเอาอะไร" if potluck else "งบพอดี ไม่ต้องให้แขกช่วยถือของมา")
    return {"total": total, "decor": parts["decor"], "food": parts["food"], "drinks": parts["drinks"], "games_gifts": parts["games_gifts"],
            "reserve": parts["reserve"], "per_head": per_head, "food_per_guest": food_per, "potluck": potluck, "tip_th": tip}


# ---------- decor ----------
def _qty(rule, room, guests):
    env = {"wall_m": room["wall_m"], "depth_m": room["depth_m"], "area": room["area_m2"], "tables": room["tables"], "guests": guests}
    return max(1, int(math.ceil(round(eval(rule, {}, env), 6))))


def deco_plan(room, theme, decor_budget, guests):
    if theme not in THEMES:
        raise ValueError("theme")
    cands = [(v[4], k) for k, v in DECOR.items() if v[5] == "*" or theme in v[5].split(",")]
    picks, skipped, spent = [], [], 0
    for _, k in sorted(cands):
        name, zone, price, pack, pr, _t, rule = DECOR[k]
        q = _qty(rule, room, guests); cost = q * price
        if spent + cost <= decor_budget:
            picks.append({"key": k, "name_th": name, "zone": zone, "packs": q, "pack_th": pack, "unit_price": price, "cost": cost,
                          "no_nails": True}); spent += cost
        else:
            skipped.append(k)
    zones = sorted({p["zone"] for p in picks})
    return {"theme": theme, "theme_th": THEMES[theme][0], "budget": decor_budget, "spent": spent, "left": decor_budget - spent,
            "items": picks, "skipped": skipped, "zones": zones, "palette": THEMES[theme][2]}


def render_prompt(room, plan):
    """What the app sends to the image model (A2): keep the room geometry, add only listed items."""
    items = ", ".join("%s ×%d" % (p["name_th"], p["packs"]) for p in plan["items"])
    return {"keep_layout": True, "theme": plan["theme"], "palette": plan["palette"], "items_th": items,
            "forbid": ["text", "faces", "logos", "brands", "real fire", "fireworks indoors"], "size": "1080x1350"}


# ---------- menu ----------
def menu_plan(style, adults, kids=0, hours=5, allergies=()):
    if style not in MENU_STYLES:
        raise ValueError("style")
    if not 1 <= hours <= 12:
        raise ValueError("hours")
    ge = guest_eq(adults, kids); n = adults + kids
    need = dict((k, v * ge) for k, v in MENU_STYLES[style][1].items())
    drink_l = DRINK_L_PER_H * hours * ge
    need["drink"] = drink_l * 0.4; need["water"] = drink_l * 0.6; need["ice"] = ICE_KG_PER_GUEST * n
    items = []
    for k, amt in need.items():
        name, unit, price, pack, sec = FOOD[k]
        packs = ceil_div(amt, pack); qty = round(packs * pack, 2)
        cost = money(qty * price) if unit not in ("ชิ้น", "ถาด") else packs * price
        items.append({"key": k, "name_th": name, "need": round(amt, 2), "unit": unit, "buy_qty": qty, "packs": packs,
                      "cost": cost, "section_th": sec})
    total = sum(i["cost"] for i in items)
    return {"style": style, "style_th": MENU_STYLES[style][0], "adults": adults, "kids": kids, "hours": hours, "guest_eq": ge,
            "items": items, "total": total, "allergy_labels": sorted(set(allergies)),
            "flag": "food_allergy" if allergies else None}


# ---------- shopping ----------
def shopping_list(plan, menu, budget):
    rows = [{"name_th": p["name_th"], "qty_th": "%d × %s" % (p["packs"], p["pack_th"]), "section_th": "ร้านของตกแต่ง/เครื่องเขียน",
             "cost": p["cost"], "checked": False} for p in plan["items"]]
    for i in menu["items"]:
        q = ("%g %s" % (i["buy_qty"], i["unit"])) if i["unit"] not in ("ชิ้น", "ถาด") else "%d %s" % (i["packs"], i["unit"])
        rows.append({"name_th": i["name_th"], "qty_th": q, "section_th": i["section_th"], "cost": i["cost"], "checked": False})
    rows.sort(key=lambda r: (r["section_th"], -r["cost"]))
    total = sum(r["cost"] for r in rows)
    by = {}
    for r in rows:
        by[r["section_th"]] = by.get(r["section_th"], 0) + r["cost"]
    food_budget = budget["food"] + budget["drinks"]
    return {"rows": rows, "sections": [{"section_th": k, "cost": v} for k, v in sorted(by.items())], "total": total,
            "budget": budget["total"], "over_by": max(0, total - (budget["decor"] + food_budget)),
            "fits": plan["spent"] <= budget["decor"] and menu["total"] <= food_budget}


def trim_menu(style, adults, kids, hours, food_budget):
    """Cheapest fix when food is over budget: switch to a cheaper style first, then suggest potluck share."""
    for st in [style] + [s for s in ("buffet", "snack", "suki") if s != style]:
        m = menu_plan(st, adults, kids, hours)
        if m["total"] <= food_budget:
            return {"style": st, "total": m["total"], "potluck_dishes": 0, "changed": st != style}
    m = menu_plan(style, adults, kids, hours)
    gap = m["total"] - food_budget
    return {"style": style, "total": m["total"], "potluck_dishes": int(math.ceil(gap / 150.0)), "changed": False}


# ---------- timeline ----------
TASKS = [(-7 * 24 * 60, "invite", "ส่งการ์ดเชิญ + ขอ RSVP"), (-3 * 24 * 60, "rsvp", "ปิด RSVP · สั่งของตกแต่งออนไลน์"),
         (-48 * 60, "shop", "ซื้อของแห้ง/เครื่องดื่ม · ชาร์จไฟ LED"), (-24 * 60, "decorate", "ติดธงราว ลูกโป่ง มุมถ่ายรูป (เทปกาว ไม่เจาะผนัง)"),
         (-4 * 60, "fresh", "ซื้อของสด + น้ำแข็ง"), (-2 * 60, "table", "จัดโต๊ะบุฟเฟต์ หม้อไฟฟ้า ป้ายแพ้อาหาร"),
         (-60, "test", "เทสต์ไฟ เพลย์ลิสต์ มือถือฉายเกม"), (0, "welcome", "ต้อนรับ ถ่ายรูปมุม backdrop"),
         (90, "games", "เกมรอบ 1"), (None, "countdown", "นับถอยหลัง 10…1 สวัสดีปีใหม่!"),
         ("cd+10", "gift_swap", "เปิดสลากจับของขวัญ"), ("end", "home", "กลับบ้านปลอดภัย · เก็บกวาด")]


def timeline(start, end, new_year=True, alcohol=False):
    s, e = _dt.fromisoformat(start), _dt.fromisoformat(end)
    if e <= s:
        raise ValueError("end before start")
    mid = _dt(s.year + 1, 1, 1) if (s.month == 12 and s.day == 31) else None
    out = []
    for off, k, t in TASKS:
        if k in ("countdown", "gift_swap") and not (new_year and mid and s < mid <= e):
            if k == "countdown":
                continue
            at = s + timedelta(minutes=150)
        elif k == "countdown":
            at = mid - timedelta(minutes=1)
        elif k == "gift_swap":
            at = mid + timedelta(minutes=10)
        elif off == "end":
            at = e
        else:
            at = s + timedelta(minutes=off)
        txt = t + (" — เรียกรถ/ค้างคืน ไม่ดื่มแล้วขับ" if (k == "home" and alcohol) else "")
        out.append({"key": k, "at": at.isoformat(timespec="minutes"), "text_th": txt, "done": False})
    out.sort(key=lambda x: x["at"])
    return {"start": s.isoformat(timespec="minutes"), "end": e.isoformat(timespec="minutes"), "tasks": out,
            "flag": "noise_late" if e.hour < 6 and e.date() > s.date() else None}


# ---------- games ----------
def game_plan(players, mode="family", kids=0, minutes=60):
    if mode not in ("family", "office", "friends"):
        raise ValueError("mode")
    col = {"family": 7, "office": 8, "friends": 7}[mode]
    ok = [g for g in GAMES if g[3] <= players <= g[4] and (g[col] or mode == "friends") and (g[6] or kids == 0)]
    ok.sort(key=lambda g: (-(g[6] and kids > 0), g[5], g[0]))
    picks, used = [], 0
    for g in ok:
        if used + g[5] <= minutes:
            picks.append({"key": g[0], "name_th": g[1], "minutes": g[5], "props_th": g[9], "kid_ok": g[6]}); used += g[5]
    return {"players": players, "mode": mode, "kids": kids, "minutes": used, "games": picks, "drinking_games": False}


# ---------- gift swap (จับสลาก) ----------
def gift_swap(names, seed, budget_cap=300, exclude=()):
    if len(names) < 3 or len(set(names)) != len(names):
        raise ValueError("need ≥ 3 unique names")
    ex = {frozenset(p) for p in exclude}
    rnd = random.Random(seed)
    for _ in range(5000):
        r = names[:]; rnd.shuffle(r)
        if all(a != b and frozenset((a, b)) not in ex for a, b in zip(names, r)):
            pairs = [{"giver": a, "receiver": b, "code": hashlib.sha1(("%s|%s|%s" % (seed, a, b)).encode()).hexdigest()[:4].upper()}
                     for a, b in zip(names, r)]
            return {"people": len(names), "seed": seed, "budget_cap": budget_cap, "pairs": pairs, "secret": True,
                    "rule_th": "ของขวัญไม่เกิน %d บาท ห้ามบอกใครจนถึงเวลาเปิด" % budget_cap}
    raise ValueError("no valid draw")


# ---------- invite ----------
def invite(host_th, start, theme, place_th, address_th, rsvp_days=3, public=True):
    s = _dt.fromisoformat(start)
    rsvp = (s.date() - timedelta(days=rsvp_days))
    return {"host_th": host_th, "title_th": "ปาร์ตี้ส่งท้ายปีบ้าน%s" % host_th, "date_th": "%d %s %d" % (s.day, MONTHS_TH[s.month - 1], s.year + 543),
            "time_th": s.strftime("%H:%M") + " น.", "theme": theme, "dress_th": DRESS[theme], "place_th": place_th,
            "address_th": None if public else address_th, "address_hidden": public, "rsvp_by": rsvp.isoformat(),
            "palette": THEMES[theme][2][:3], "watermark": WATERMARK}


# ---------- cost split ----------
def cost_split(total, adults, kids=0, host_pays_decor=0):
    if adults < 1:
        raise ValueError("adults")
    share = total - host_pays_decor
    each = int(math.ceil(share / adults / 10.0)) * 10
    return {"total": total, "host_pays": host_pays_decor, "payers": adults, "kids_free": kids, "each": each,
            "collected": each * adults, "extra": each * adults - share}


# ---------- misc ----------
def countdown(today):
    t = d(today); ny = _date(t.year + 1, 1, 1)
    return {"date": t.isoformat(), "days_to_new_year": (ny - t).days, "be_year": t.year + 544, "weekday_th": "วัน" + ["จันทร์", "อังคาร", "พุธ", "พฤหัสบดี", "ศุกร์", "เสาร์", "อาทิตย์"][ny.weekday()]}


def share_card(kind, theme="countdown_gold"):
    if kind not in ("before_after", "invite", "shopping"):
        raise ValueError("kind")
    return {"kind": kind, "size": "1080x1350", "theme": theme, "faces_blurred": True, "address_hidden": True, "watermark": WATERMARK}


def reel_plan(seconds=24):
    if not 15 <= seconds <= 30:
        raise ValueError("15–30 s")
    t, shots = 0.0, []
    for k, cap, frac in REEL_SHOTS:
        e = round(t + seconds * frac, 1) if k != "cta" else float(seconds)
        shots.append({"kind": k, "start": round(t, 1), "end": e, "caption_th": cap}); t = e
    return {"seconds": seconds, "ratio": "9:16", "bpm": 120, "shots": shots, "watermark": WATERMARK}


def quota(used, plan="free"):
    per = {"free": 3, "plus": 30}[plan]
    return {"plan": plan, "renders_per_day": per, "used": used, "left": max(0, per - used), "blocked": used >= per}


def safety_guard(flag=None):
    lv, msg = GUARD[flag]
    return {"flag": flag, "level": lv, "message_th": msg, "block": lv == "stop"}


def party_flags(kids=0, kids_under3=0, alcohol=False, driving_guests=0, fire_items=(), end_after_midnight=False, over=False, allergies=()):
    f = []
    if alcohol and kids: f.append("alcohol_minor")
    if alcohol and driving_guests: f.append("drink_drive")
    if fire_items: f.append("indoor_fire")
    if over: f.append("over_capacity")
    if end_after_midnight: f.append("noise_late")
    if kids_under3: f.append("small_kids_balloons")
    if allergies: f.append("food_allergy")
    return f


def privacy_check(flags=(), age=25, parent_mode=False):
    fl = list(flags) + (["minor"] if age < 13 else [])
    levels = [GUARD[f][0] for f in fl] or ["ok"]
    lv = "stop" if "stop" in levels else ("warn" if "warn" in levels else "ok")
    msgs = [GUARD[f][1] for f in fl] or [GUARD[None][1]]
    share = lv != "stop" and (age >= 13 or parent_mode)
    return {"allowed": lv != "stop", "level": lv, "flags": fl, "messages_th": msgs, "share_allowed": share}
