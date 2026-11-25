"""DreamBoard — deterministic reference logic (port to TypeScript; tests.py is the contract).
The AI only parses free-text Thai goals into a draft Goal (A1), paints tile backgrounds (A2) and writes short
kind lines (A3–A5). Everything that decides numbers — SMART check, safe-rate limits, the 12-month roadmap,
the weekly habit, the lock-screen layout, streaks, progress, glow level and the year review — is plain code."""
import math
from datetime import date as _date, timedelta

CATEGORIES = [("money", "เงิน", "Money", "#F2B705"), ("health", "สุขภาพ", "Health", "#2EC4B6"), ("learn", "เรียนรู้", "Learning", "#5B8DEF"),
              ("career", "งาน", "Career", "#8E6CEF"), ("travel", "เที่ยว", "Travel", "#FF8C42"), ("family", "ครอบครัว", "Family", "#FF6B8B"),
              ("home", "บ้าน", "Home", "#8AC926"), ("habit", "นิสัยดี", "Habits", "#00A6A6"), ("mind", "ใจ", "Mind", "#B388EB"),
              ("hobby", "งานอดิเรก", "Hobby", "#F15BB5")]
CAT = {c[0]: c for c in CATEGORIES}
CAT_KEYS = [c[0] for c in CATEGORIES]
# unit → Thai name, rounding step, max sensible amount per month (None = depends on income) and weekly safety limits
UNITS = {"THB": {"name_th": "บาท", "step": 100, "max_per_month": None},
         "kg_loss": {"name_th": "กก. (ลดลง)", "step": 0.5, "max_per_month": 4.0},
         "km": {"name_th": "กม.", "step": 5, "max_per_month": 250},
         "book": {"name_th": "เล่ม", "step": 1, "max_per_month": 8},
         "trip": {"name_th": "ทริป", "step": 1, "max_per_month": 4},
         "times": {"name_th": "ครั้ง", "step": 1, "max_per_month": 31},
         "hours": {"name_th": "ชั่วโมง", "step": 1, "max_per_month": 120},
         "lesson": {"name_th": "บทเรียน", "step": 1, "max_per_month": 40}}
WEEK_STEP = {"THB": 50, "kg_loss": 0.1, "km": 1}   # rounding for the weekly habit
SAFE_KG_PER_WEEK = 0.5     # recommended
MAX_KG_PER_WEEK = 1.0      # above this the goal is blocked and re-planned
SAVE_MAX_SHARE = 0.5       # saving more than half the monthly income is flagged as not achievable
THEMES = {"pastel": ("พาสเทลฟ้าใส", ["#FFD6E0", "#C1E1FF", "#D7F9D0", "#FFF1B8", "#E5D4FF", "#FFE0C2"]),
          "sunrise": ("แสงแรกปีใหม่", ["#FF9A62", "#FFC46B", "#FF6F91", "#FFD79A", "#F9A8D4", "#FDBA74"]),
          "midnight": ("คืนเคานต์ดาวน์", ["#1F2A6B", "#3B2A7A", "#0F4C75", "#4C1D95", "#1E3A8A", "#312E81"]),
          "thai_gold": ("ทองมงคล", ["#B8860B", "#D4AF37", "#8B0000", "#F5DEB3", "#C5A35A", "#7A1F1F"]),
          "nature": ("ป่าเขียวสดชื่น", ["#2D6A4F", "#52B788", "#95D5B2", "#B7E4C7", "#40916C", "#74C69D"]),
          "minimal": ("มินิมอลขาวดำ", ["#F5F5F5", "#E0E0E0", "#FAFAFA", "#EEEEEE", "#D6D6D6", "#FFFFFF"])}
DEVICES = {"iphone": (1179, 2556, 0.32, 0.10), "android": (1080, 2400, 0.30, 0.08), "desktop": (1920, 1080, 0.0, 0.06)}
WORDS = {"money": ("มั่นคง", "Steady"), "health": ("แข็งแรง", "Strong"), "learn": ("เติบโต", "Grow"), "career": ("ก้าวหน้า", "Rise"),
         "travel": ("เปิดโลก", "Explore"), "family": ("อบอุ่น", "Warm"), "home": ("ลงตัว", "Settle"), "habit": ("สม่ำเสมอ", "Steady steps"),
         "mind": ("ใจดีกับตัวเอง", "Be kind"), "hobby": ("สนุก", "Play")}
MONTHS_TH = ["ม.ค.", "ก.พ.", "มี.ค.", "เม.ย.", "พ.ค.", "มิ.ย.", "ก.ค.", "ส.ค.", "ก.ย.", "ต.ค.", "พ.ย.", "ธ.ค."]
BADGES = {4: "เริ่มต้นแล้ว", 12: "ครบไตรมาส", 26: "ครึ่งปีไม่ทิ้งกัน", 52: "ทั้งปีไม่ยอมแพ้"}   # weekly check-in streak badges
GUARD = {None: ("ok", "ตั้งเป้าที่เราทำเองได้ ข้อมูลเก็บบนเครื่อง การ์ดแชร์ซ่อนตัวเลขเงิน/น้ำหนักได้"),
         "extreme_diet": ("stop", "ลดเร็วเกินไปไม่ปลอดภัย แอปปรับเป้าให้ไม่เกิน 0.5–1 กก./สัปดาห์ ถ้ามีโรคประจำตัวปรึกษาแพทย์ก่อน"),
         "self_harm": ("stop", "ถ้ากำลังรู้สึกไม่ไหว คุยกับสายด่วนสุขภาพจิต 1323 ได้ตลอด 24 ชม. คุณไม่ได้อยู่คนเดียว"),
         "gambling": ("warn", "หวย/พนันควบคุมไม่ได้ ลองเปลี่ยนเป็นเป้าเก็บเงินที่เราคุมเองได้แทน"),
         "get_rich_quick": ("warn", "ระวังโครงการรวยเร็ว/ลงทุนผลตอบแทนสูงผิดปกติ แอปไม่ให้คำแนะนำการลงทุน"),
         "other_person": ("warn", "เป้าที่ขึ้นกับคนอื่นคุมไม่ได้ ลองเขียนเป็นสิ่งที่เราทำเอง เช่น 'โทรหาแม่ทุกอาทิตย์'"),
         "medical": ("warn", "เรื่องยา/การรักษา ปรึกษาแพทย์ก่อนเปลี่ยนแปลง แอปไม่ใช่คำแนะนำทางการแพทย์"),
         "minor": ("warn", "อายุต่ำกว่า 13 ปี ให้ผู้ปกครองช่วยตั้งเป้าและเปิด parent mode ก่อนแชร์"),
         "photo_of_others": ("warn", "รูปบนบอร์ดต้องเป็นรูปของเราหรือได้รับอนุญาต การ์ดแชร์เบลอหน้าคนอื่นให้อัตโนมัติ")}
REEL_SHOTS = [("hook", "ปีใหม่ทีไร ตั้งเป้าแล้วลืมทุกปี?", 0.13), ("build", "สร้างแอปด้วย AI จากแพ็กนี้", 0.12),
              ("type_goals", "พิมพ์เป้าแบบบ่น ๆ AI แปลงเป็นเป้าชัด", 0.18), ("board_reveal", "กดปุ๊บ ได้บอร์ดเป้าหมายสวย ๆ", 0.17),
              ("lockscreen", "ตั้งเป็นล็อกสกรีน เห็นทุกครั้งที่ปลดล็อก", 0.15), ("glow_up", "ทำได้มากขึ้น บอร์ดยิ่งสว่าง", 0.13),
              ("cta", "คอมเมนต์ DREAM รับแพ็กฟรี", 0.12)]


def d(s):
    return s if isinstance(s, _date) else _date.fromisoformat(s)


def round_step(x, step):
    return round(round(x / step) * step, 2)


def ceil_step(x, step):
    return round(math.ceil(round(x / step, 6)) * step, 2)


def months_between(start, deadline):
    a, b = d(start), d(deadline)
    if b <= a:
        raise ValueError("deadline must be after start")
    return (b.year - a.year) * 12 + b.month - a.month + 1


def delta(g):
    return round(g["target_value"] - g["start_value"], 2)


def smart_check(g, monthly_income=None):
    """Score a goal on S-M-A-R-T (20 points each) with Thai tips; flags unsafe weight-loss rates."""
    tips, flag = [], None
    specific = len(g.get("title_th", "").strip()) >= 6 and g.get("target_value", 0) > g.get("start_value", 0)
    measurable = g.get("unit") in UNITS
    relevant = g.get("category") in CAT
    try:
        n = months_between(g["start"], g["deadline"])
        timed = n <= 13
    except (KeyError, ValueError):
        n, timed = None, False
    per_month = round(delta(g) / n, 2) if (n and specific) else None
    achievable = False
    if per_month is not None and measurable:
        u = UNITS[g["unit"]]
        if g["unit"] == "kg_loss":
            weeks = (d(g["deadline"]) - d(g["start"])).days / 7
            per_week = delta(g) / weeks
            achievable = per_week <= MAX_KG_PER_WEEK
            if not achievable:
                flag = "extreme_diet"
        elif g["unit"] == "THB":
            achievable = monthly_income is None or per_month <= monthly_income * SAVE_MAX_SHARE
        else:
            achievable = per_month <= u["max_per_month"]
    if not specific: tips.append("ใส่ตัวเลขให้ชัด เช่น 'เก็บเงิน 60,000 บาท' แทน 'อยากรวย'")
    if not measurable: tips.append("เลือกหน่วยวัดผล (บาท กม. เล่ม ครั้ง ชั่วโมง…)")
    if specific and measurable and not achievable: tips.append("เป้านี้หนักเกินไปสำหรับเวลาที่มี ลองลดตัวเลขหรือยืดเวลา")
    if not relevant: tips.append("เลือกหมวดของเป้า เพื่อให้บอร์ดจัดสีและไอคอนให้")
    if not timed: tips.append("ใส่วันสิ้นสุดภายใน 1 ปี เช่น 31 ธ.ค.")
    score = 20 * sum((specific, measurable, achievable, relevant, timed))
    return {"score": score, "specific": specific, "measurable": measurable, "achievable": achievable, "relevant": relevant,
            "timed": timed, "per_month": per_month, "flag": flag, "tips_th": tips}


def safe_replan(g):
    """For an extreme weight-loss goal keep the target but push the deadline to the safe rate (0.5 kg/week)."""
    if g["unit"] != "kg_loss":
        raise ValueError("only weight-loss goals are re-planned")
    weeks = math.ceil(delta(g) / SAFE_KG_PER_WEEK)
    out = dict(g); out["deadline"] = (d(g["start"]) + timedelta(weeks=weeks)).isoformat()
    return out


def roadmap(g):
    """Monthly milestones with a gentle ramp (start small, speed up later). Last milestone hits the target exactly."""
    a = d(g["start"]); n = months_between(g["start"], g["deadline"]); step = UNITS[g["unit"]]["step"]
    w = [1.0] if n == 1 else [0.7 + 0.6 * i / (n - 1) for i in range(n)]
    tot, cum, out = sum(w), 0.0, []
    prev = g["start_value"]
    for i in range(n):
        cum += w[i]
        y, m = a.year + (a.month - 1 + i) // 12, (a.month - 1 + i) % 12 + 1
        t = g["target_value"] if i == n - 1 else round_step(g["start_value"] + delta(g) * cum / tot, step)
        out.append({"month": "%04d-%02d" % (y, m), "label_th": "%s %d" % (MONTHS_TH[m - 1], (y + 543) % 100), "target": t,
                    "delta": round(t - prev, 2), "pct": round(100 * (t - g["start_value"]) / delta(g))})
        prev = t
    return {"goal_id": g["id"], "months": n, "unit": g["unit"], "milestones": out}


def weekly_habit(g):
    """Turn the yearly target into one tiny weekly action (and a per-day hint)."""
    days = (d(g["deadline"]) - d(g["start"])).days + 1
    weeks = math.ceil(days / 7); step = UNITS[g["unit"]]["step"]; u = g["unit"]
    per_week = ceil_step(delta(g) / weeks, WEEK_STEP.get(u, 1))
    if u == "THB":
        txt = "เก็บสัปดาห์ละ {:,.0f} บาท (วันละ ~{:,.0f} บาท)".format(per_week, math.ceil(per_week / 7))
    elif u == "kg_loss":
        kcal = round(per_week * 7700 / 7 / 50) * 50
        txt = "ลดสัปดาห์ละ {:g} กก. ≈ กินน้อยลง/ขยับมากขึ้น ~{} kcal ต่อวัน".format(per_week, kcal)
    elif u == "book":
        pages = math.ceil(delta(g) * 250 / days)
        txt = "อ่านวันละ ~{} หน้า (เล่มละ ~250 หน้า)".format(pages)
    elif u == "km":
        txt = "วิ่ง/เดินสัปดาห์ละ {:g} กม. (แบ่ง 3 วัน วันละ ~{:g} กม.)".format(per_week, round(per_week / 3, 1))
    elif u == "trip":
        txt = "วางแผนทริปทุก ~{} สัปดาห์".format(weeks // max(1, int(delta(g))))
    else:
        txt = "สัปดาห์ละ {:g} {}".format(per_week, UNITS[u]["name_th"])
    return {"goal_id": g["id"], "weeks": weeks, "per_week": per_week, "unit": u, "text_th": txt}


def layout(goals, theme="sunrise", device="iphone"):
    """Place 1–6 goal tiles on a lock screen / desktop wallpaper, never under the clock or the bottom buttons."""
    if not 1 <= len(goals) <= 6:
        raise ValueError("1–6 goals per board")
    if theme not in THEMES or device not in DEVICES:
        raise ValueError("unknown theme/device")
    W, H, top, bot = DEVICES[device]
    m, gap = 48, 32
    x0, y0, x1, y1 = m, int(H * top) + (m if device != "desktop" else int(H * 0.12)), W - m, int(H * (1 - bot)) - m
    if device == "desktop":
        x0 = int(W * 0.42)                    # keep the left side free for desktop icons
    n = len(goals)
    cols = 1 if n == 1 else (2 if device != "desktop" or n <= 4 else 3)
    rows = math.ceil(n / cols)
    tw = (x1 - x0 - gap * (cols - 1)) // cols; th = (y1 - y0 - gap * (rows - 1)) // rows
    pal = THEMES[theme][1]; tiles = []
    for i, g in enumerate(goals):
        r, c = divmod(i, cols)
        w = tw
        if i == n - 1 and n % cols and cols == 2:   # odd last tile spans the full width
            w = x1 - x0
        tiles.append({"goal_id": g["id"], "x": x0 + c * (tw + gap), "y": y0 + r * (th + gap), "w": w, "h": th,
                      "color": pal[i % len(pal)], "category": g["category"]})
    return {"device": device, "theme": theme, "w": W, "h": H, "safe_top": int(H * top), "safe_bottom": int(H * (1 - bot)), "tiles": tiles}


def overlaps(a, b):
    return a["x"] < b["x"] + b["w"] and b["x"] < a["x"] + a["w"] and a["y"] < b["y"] + b["h"] and b["y"] < a["y"] + a["h"]


def word_of_year(goals):
    count = {}
    for g in goals:
        count[g["category"]] = count.get(g["category"], 0) + 1
    best = max(goals, key=lambda g: (count[g["category"]], -goals.index(g)))["category"]
    th, en = WORDS[best]
    return {"category": best, "word_th": th, "word_en": en, "line_th": "คำประจำปี 2570 ของฉัน: " + th}


def countdown(today):
    t = d(today); ny = _date(t.year + 1, 1, 1); y0 = _date(t.year, 1, 1)
    days_year = (ny - y0).days
    return {"date": t.isoformat(), "days_to_new_year": (ny - t).days, "days_passed": (t - y0).days, "year_pct": round(100 * (t - y0).days / days_year)}


def week_key(x):
    y, w, _ = d(x).isocalendar()
    return (y, w)


def streak(checkins, today):
    """Weekly check-in streak. Last week still counts if this week has no check-in yet."""
    weeks = {week_key(c) for c in checkins}
    t = d(today); cur = week_key(t)
    k = 0; day = t if cur in weeks else t - timedelta(days=7)
    while week_key(day) in weeks:
        k += 1; day -= timedelta(days=7)
    new = BADGES.get(k) if cur in weeks else None
    return {"weeks": k, "this_week_done": cur in weeks, "badge_th": new, "next_badge_at": min([b for b in BADGES if b > k], default=None)}


def expected_at(g, today):
    """Target the roadmap expects on a given day (linear inside the current month)."""
    rm = roadmap(g)["milestones"]; t = d(today); prev = g["start_value"]
    for ms in rm:
        y, m = map(int, ms["month"].split("-"))
        if (t.year, t.month) == (y, m):
            dim = ((_date(y + (m == 12), m % 12 + 1, 1)) - _date(y, m, 1)).days
            return round(prev + (ms["target"] - prev) * t.day / dim, 2)
        prev = ms["target"]
    return g["target_value"] if t > d(g["deadline"]) else g["start_value"]


def progress(g, logs, today):
    done = round(sum(l["amount"] for l in logs if d(l["date"]) <= d(today)), 2)
    pct = min(100, round(100 * done / delta(g)))
    exp = round(expected_at(g, today) - g["start_value"], 2)
    if pct >= 100: status = "done"
    elif exp <= 0 or done >= exp * 1.1: status = "ahead"
    elif done >= exp * 0.9: status = "on_track"
    else: status = "behind"
    msg = {"done": "สำเร็จแล้ว! ภูมิใจในตัวเองได้เต็มที่", "ahead": "นำแผนอยู่ เก่งมาก รักษาจังหวะนี้ไว้",
           "on_track": "ตรงแผนพอดี ค่อย ๆ ไปแบบนี้แหละ", "behind": "ช้ากว่าแผนนิดหน่อย ไม่เป็นไร สัปดาห์นี้ลองก้าวเล็ก ๆ อีกครั้ง"}[status]
    return {"goal_id": g["id"], "done": done, "expected": exp, "pct": pct, "status": status, "glow": min(5, pct // 20), "message_th": msg}


def board_glow(progs):
    """The wallpaper 'lights up' as you progress: each tile glows 0–5, the whole board gets a level."""
    avg = round(sum(p["pct"] for p in progs) / len(progs))
    return {"overall_pct": avg, "level": min(5, avg // 20), "lit_tiles": sum(1 for p in progs if p["glow"] >= 1),
            "tiles": [{"goal_id": p["goal_id"], "glow": p["glow"]} for p in progs]}


def review(goals, progs, period="year"):
    if period not in ("mid_year", "year"):
        raise ValueError("period")
    by = {p["goal_id"]: p for p in progs}
    best = max(goals, key=lambda g: (by[g["id"]]["pct"], -goals.index(g)))
    done = sum(1 for p in progs if p["pct"] >= 100)
    avg = round(sum(p["pct"] for p in progs) / len(progs))
    title = "ทบทวนครึ่งปี" if period == "mid_year" else "สรุปปีของฉัน"
    note = "ทุกก้าวนับหมด ปีหน้าเอาใหม่ได้เสมอ" if avg < 50 else "ปีนี้ไปได้ไกลกว่าที่คิด"
    return {"period": period, "title_th": title, "goals": len(goals), "goals_done": done, "overall_pct": avg,
            "best_goal_id": best["id"], "best_title_th": best["title_th"], "note_th": note}


def buddy_card(owner_th, buddy_th, goals, private=True):
    items = []
    for g in goals:
        sens = g["unit"] in ("THB", "kg_loss")
        items.append({"title_th": g["category_th"] if (private and sens) else g["title_th"], "amount_hidden": private and sens})
    return {"owner_th": owner_th, "buddy_th": buddy_th, "pact_th": "%s กับ %s สัญญาว่าจะเช็กอินกันทุกวันอาทิตย์" % (owner_th, buddy_th),
            "items": items, "private": private}


def share_card(kind, glow=None, word=None):
    if kind not in ("board", "progress", "review"):
        raise ValueError("kind")
    return {"kind": kind, "size": "1080x1350", "amounts_hidden_default": True, "faces_blurred": True,
            "glow_level": glow, "word_th": word, "watermark": "DreamBoard · AI วันละแอป"}


def reel_plan(seconds=24):
    if not 15 <= seconds <= 30:
        raise ValueError("15–30 s")
    t, shots = 0.0, []
    for k, cap, frac in REEL_SHOTS:
        e = round(t + seconds * frac, 1) if k != "cta" else float(seconds)
        shots.append({"kind": k, "start": round(t, 1), "end": e, "caption_th": cap}); t = e
    return {"seconds": seconds, "ratio": "9:16", "bpm": 100, "shots": shots, "watermark": "DreamBoard · AI วันละแอป"}


def quota(used, plan="free"):
    per = {"free": 3, "plus": 30}[plan]
    return {"plan": plan, "boards_per_day": per, "used": used, "left": max(0, per - used), "blocked": used >= per}


def safety_guard(flag=None):
    lv, msg = GUARD[flag]
    return {"flag": flag, "level": lv, "message_th": msg, "block": lv == "stop"}


def privacy_check(flags=(), age=25, parent_mode=False):
    fl = list(flags) + (["minor"] if age < 13 else [])
    levels = [GUARD[f][0] for f in fl] or ["ok"]
    lv = "stop" if "stop" in levels else ("warn" if "warn" in levels else "ok")
    msgs = [GUARD[f][1] for f in fl] or [GUARD[None][1]]
    share = lv != "stop" and (age >= 13 or parent_mode)
    return {"allowed": lv != "stop", "level": lv, "flags": fl, "messages_th": msgs, "share_allowed": share}
