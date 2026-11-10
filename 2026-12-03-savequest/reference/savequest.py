"""SaveQuest deterministic logic (no AI calls). Game-like saving helper — not a bank or investment advice."""
import datetime as _dt
import random as _random

GOALS = {
    "japan_trip": {
        "id": "g01", "name_th": "เที่ยวญี่ปุ่น", "name_en": "Japan trip",
        "icon": "fuji", "hint_th": "เก็บให้ครบก่อนจองตั๋ว และเผื่อค่าเดินทางอีกนิด",
        "sample_thb": 45000,
    },
    "emergency": {
        "id": "g02", "name_th": "กองฉุกเฉิน 3 เดือน", "name_en": "Emergency fund",
        "icon": "shield", "hint_th": "เก็บแยกต่างหาก อย่าหยิบมาใช้กับของอยากได้",
        "sample_thb": 30000,
    },
    "gadget": {
        "id": "g03", "name_th": "Gadgets ที่ตั้งใจซื้อ", "name_en": "Gadget",
        "icon": "phone", "hint_th": "ตั้งเป้าตามราคาจริง รวมเคสและประกัน",
        "sample_thb": 15000,
    },
    "wedding": {
        "id": "g04", "name_th": "งานแต่งงาน", "name_en": "Wedding",
        "icon": "ring", "hint_th": "แยกงบของชำร่วย ชุด และสถานที่ จะได้เห็นชัด",
        "sample_thb": 150000,
    },
    "tuition": {
        "id": "g05", "name_th": "ค่าเทอม / คอร์ส", "name_en": "Tuition",
        "icon": "book", "hint_th": "นับจากวันปิดรับสมัคร จะได้ไม่เก็บไม่ทัน",
        "sample_thb": 25000,
    },
    "down_payment": {
        "id": "g06", "name_th": "ดาวน์รถ / ดาวน์บ้าน", "name_en": "Down payment",
        "icon": "key", "hint_th": "อย่านับเงินกู้เป็นเงินออม และเผื่อค่าธรรมเนียม",
        "sample_thb": 80000,
    },
    "concert": {
        "id": "g07", "name_th": "ตั๋วคอนเสิร์ต", "name_en": "Concert ticket",
        "icon": "ticket", "hint_th": "เผื่องบเดินทางและของที่ระลึกด้วย",
        "sample_thb": 8000,
    },
}
GOAL_IDS = list(GOALS)

CHALLENGES = {
    "skip_cafe": {"id": "c01", "name_th": "งดกาแฟร้าน", "save_thb": 85, "xp": 10, "hint_th": "ชงเองที่บ้านหรือพกแก้วมา"},
    "cook_home": {"id": "c02", "name_th": "ทำข้าวกล่องเอง", "save_thb": 60, "xp": 10, "hint_th": "ทำเผื่อพรุ่งด้วยจะประหยัดกว่า"},
    "no_delivery": {"id": "c03", "name_th": "งดเดลิเวอรี่", "save_thb": 120, "xp": 15, "hint_th": "ค่าส่งกับขั้นต่ำทำให้แพงกว่าที่คิด"},
    "walk_not_grab": {"id": "c04", "name_th": "เดินแทนแกร็บระยะใกล้", "save_thb": 45, "xp": 10, "hint_th": "ระยะไม่เกิน 1 กม. เดินได้ถ้าปลอดภัย"},
    "pack_water": {"id": "c05", "name_th": "พกขวดน้ำ", "save_thb": 20, "xp": 5, "hint_th": "ขวดเล็ก ๆ ในกระเป๋าก็พอ"},
    "no_snack": {"id": "c06", "name_th": "งดขนมออฟฟิศ", "save_thb": 35, "xp": 5, "hint_th": "พกผลไม้หรือถั่วมาเอง"},
    "unsubscribe": {"id": "c07", "name_th": "ยกเลิกสมาชิกที่ไม่ได้ใช้", "save_thb": 149, "xp": 20, "hint_th": "เช็กใบเสร็จย้อนหลัง 30 วัน"},
    "market_not_mall": {"id": "c08", "name_th": "ซื้อของในตลาดแทนห้าง", "save_thb": 80, "xp": 10, "hint_th": "เทียบราคา 3 อย่างที่ซื้อประจำ"},
}
CHALLENGE_IDS = list(CHALLENGES)
MARKS = (25, 50, 75, 100)
FREE_GENS_PER_DAY = 3
WATERMARK = "Made with SaveQuest · not a bank, not investment advice"
SAFETY_DISCLAIMER_TH = "SaveQuest เป็นเกมช่วยออมเงิน ไม่ใช่บัญชีธนาคาร ไม่ใช่คำแนะนำการลงทุน และไม่รับฝากเงินจริง จำนวนเงินในแอปเป็นค่าที่ผู้ใช้กรอกหรือค่าตัวอย่าง"
WEEK52_MAX = 52

def scan_quality(glare, blur, crop):
    for v in (glare, blur, crop):
        if not 0 <= v <= 1:
            raise ValueError("glare/blur/crop must be 0..1")
    score = int(round(100 * (1 - (0.30 * glare + 0.40 * blur + 0.30 * crop))))
    tips = []
    if glare > 0.5:
        tips.append("รูปสะท้อนแสง ถ่ายใหม่ในที่ร่มหรือหันจากหน้าต่าง")
    if blur > 0.4:
        tips.append("ภาพเบลอ ถือนิ่งแล้วถ่ายอีกครั้ง")
    if crop > 0.45:
        tips.append("เป้าหมายในรูปถูกตัด จัดให้อยู่กลางกรอบ")
    return {"score": score, "ok": score >= 60, "tips_th": tips}


def photo_scan(photo):
    q = scan_quality(photo["glare"], photo["blur"], photo["crop"])
    return {"photo_id": photo["id"], "quality": q, "goal_id": photo.get("goal_id")}


def pipeline_steps(photo):
    s = ["goal_photo"]
    if photo["glare"] > 0.5:
        s.append("deglare")
    if photo["crop"] > 0.45:
        s.append("recrop")
    s += ["jar_fill", "plan", "challenge", "milestone"]
    return s


def goal_info(goal_id):
    if goal_id not in GOALS:
        raise ValueError("unknown goal")
    g = GOALS[goal_id]
    return {"id": g["id"], "goal_id": goal_id, "name_th": g["name_th"], "name_en": g["name_en"],
            "icon": g["icon"], "hint_th": g["hint_th"], "sample_thb": g["sample_thb"]}


def jar_level(pct):
    if pct < 10:
        return "empty", "แทบยังไม่เริ่ม"
    if pct < 50:
        return "growing", "กระปุกกำลังโต"
    if pct < 75:
        return "halfway", "ถึงครึ่งทางแล้ว"
    if pct < 100:
        return "almost", "อีกนิดก็เต็ม"
    return "full", "เต็มเป้าแล้ว"


def jar_fill(saved, goal):
    if goal <= 0:
        raise ValueError("goal must be > 0")
    if saved < 0:
        raise ValueError("saved must be >= 0")
    pct = min(100, int(round(100 * saved / goal)))
    remaining = max(0, goal - saved)
    level, label = jar_level(pct)
    return {
        "saved_thb": saved, "goal_thb": goal, "remaining_thb": remaining, "pct": pct,
        "level": level, "label_th": label,
        "headline_th": f"กระปุกโตถึง {pct}%" if pct < 100 else "กระปุกเต็มเป้าแล้ว",
    }


def milestones(saved, goal):
    fill = jar_fill(saved, goal)
    pct = fill["pct"]
    reached = [m for m in MARKS if pct >= m]
    nxt = next((m for m in MARKS if pct < m), None)
    next_amount = None if nxt is None else int(round(goal * nxt / 100))
    need = None if next_amount is None else max(0, next_amount - saved)
    return {
        "pct": pct, "reached": reached, "next_mark": nxt,
        "next_amount_thb": next_amount, "need_thb": need,
        "message_th": (
            "ถึงเป้าแล้ว ฉลองด้วยการ์ดแชร์ได้เลย" if nxt is None
            else f"อีก ฿{need:,} จะถึงไมล์สโตน {nxt}%"
        ).replace(",", ","),
    }


def week52_amount(week, base=100):
    if week not in range(1, WEEK52_MAX + 1):
        raise ValueError("week must be 1..52")
    if base < 1:
        raise ValueError("base must be >= 1")
    return week * base


def week52_cumulative(week, base=100):
    if week not in range(1, WEEK52_MAX + 1):
        raise ValueError("week must be 1..52")
    if base < 1:
        raise ValueError("base must be >= 1")
    return base * week * (week + 1) // 2


def week52_total(base=100):
    return week52_cumulative(WEEK52_MAX, base)


def week52_fit_base(goal):
    if goal < 1:
        raise ValueError("goal must be > 0")
    return max(1, (goal + 1377) // 1378)


def week52_plan(week, base=100):
    amt = week52_amount(week, base)
    cum = week52_cumulative(week, base)
    total = week52_total(base)
    return {
        "kind": "week52", "week": week, "base_thb": base, "amount_thb": amt,
        "cumulative_thb": cum, "plan_total_thb": total,
        "label_th": f"สัปดาห์ที่ {week} ออม ฿{amt}",
    }


def random_week_order(seed):
    weeks = list(range(1, WEEK52_MAX + 1))
    _random.Random(str(seed)).shuffle(weeks)
    return weeks


def random_plan(week, base, seed):
    if week not in range(1, WEEK52_MAX + 1):
        raise ValueError("week must be 1..52")
    if base < 1:
        raise ValueError("base must be >= 1")
    order = random_week_order(seed)
    multiplier = order[week - 1]
    amt = multiplier * base
    # cumulative following the shuffled order through this week
    cum = sum(x * base for x in order[:week])
    return {
        "kind": "random", "week": week, "base_thb": base, "seed": str(seed),
        "multiplier": multiplier, "amount_thb": amt, "cumulative_thb": cum,
        "plan_total_thb": week52_total(base),
        "label_th": f"สุ่มสัปดาห์ที่ {week} ได้ตัวคูณ {multiplier} ออม ฿{amt}",
    }


def daily_challenge(date_iso, user_id):
    keys = CHALLENGE_IDS
    i = (sum(ord(ch) for ch in f"{date_iso}:{user_id}")) % len(keys)
    c = CHALLENGES[keys[i]]
    return {**c, "date": date_iso, "suggested": True}


def complete_challenge(challenge_id, date_iso):
    if challenge_id not in CHALLENGES:
        raise ValueError("unknown challenge")
    c = CHALLENGES[challenge_id]
    return {
        "id": c["id"], "challenge_id": challenge_id, "name_th": c["name_th"],
        "save_thb": c["save_thb"], "xp": c["xp"], "date": date_iso, "done": True,
        "message_th": f"สำเร็จ {c['name_th']} เก็บได้ ฿{c['save_thb']}",
    }


def _as_date(s):
    return _dt.date.fromisoformat(s)


def streak(dates, today, frozen_dates=None):
    frozen = set(frozen_dates or [])
    ds = set(dates)
    t = _as_date(today)
    start = t if (today in ds or today in frozen) else t - _dt.timedelta(days=1)
    days = 0
    frozen_used = 0
    cur = start
    while True:
        iso = cur.isoformat()
        if iso in ds:
            days += 1
        elif iso in frozen:
            days += 1
            frozen_used += 1
        else:
            break
        cur -= _dt.timedelta(days=1)
    badge = "ไฟลุก" if days >= 7 else "กำลังเริ่ม" if days >= 1 else "ยังไม่เริ่ม"
    return {
        "days": days, "frozen_used": frozen_used, "badge_th": badge,
        "today_saved": today in ds, "message_th": f"สตรีค {days} วัน" if days else "ยังไม่มีสตรีค เริ่มออมวันนี้ได้เลย",
    }


def round_up(amount, step=10):
    if amount < 0:
        raise ValueError("amount must be >= 0")
    if step < 1:
        raise ValueError("step must be >= 1")
    rem = int(amount) % step
    extra = 0 if rem == 0 else step - rem
    return {"amount_thb": int(amount), "step_thb": step, "extra_thb": extra, "rounded_thb": int(amount) + extra}


def team_jar(goal, contributions):
    if not contributions:
        raise ValueError("no contributions")
    if any(c["amount_thb"] < 0 for c in contributions):
        raise ValueError("amount must be >= 0")
    total = sum(c["amount_thb"] for c in contributions)
    fill = jar_fill(total, goal)
    shares = []
    for c in contributions:
        shares.append({
            "name_th": c["name_th"], "amount_thb": c["amount_thb"],
            "pct": int(round(100 * c["amount_thb"] / goal)),
        })
    return {
        "goal_thb": goal, "saved_thb": total, "remaining_thb": fill["remaining_thb"],
        "pct": fill["pct"], "level": fill["level"], "members": shares, "member_count": len(shares),
        "headline_th": f"กระปุกร่วม โตถึง {fill['pct']}%",
    }


def share_card(name_th, goal_name_th, pct, streak_days):
    return {
        "title_th": f"SaveQuest — {name_th}",
        "headline_th": f"{goal_name_th} · กระปุกโตถึง {pct}%",
        "hook_th": "ออมเงินแบบเกม เห็นกระปุกโต",
        "pct": pct, "streak_days": streak_days,
        "layout": "jar_milestone", "sizes": ["1080x1350", "1080x1920", "1080x1080"],
        "watermark": WATERMARK,
        "cta_th": f"คอมเมนต์ SAVE รับแพ็กฟรี · สตรีค {streak_days} วัน",
    }


def quota(used_today, want, pro=False):
    if pro:
        return {"allowed": want, "left_after": None, "paywall": False}
    left = max(0, FREE_GENS_PER_DAY - used_today)
    allowed = min(want, left)
    return {"allowed": allowed, "left_after": left - allowed, "paywall": allowed < want}


def safety_guard(ok=True):
    if not ok:
        return {"level": "stop", "message_th": "ยังตั้งเป้าไม่ได้ " + SAFETY_DISCLAIMER_TH}
    return {"level": "ok", "message_th": SAFETY_DISCLAIMER_TH}
