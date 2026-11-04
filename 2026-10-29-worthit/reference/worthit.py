"""WorthIt (คุ้มไหมก่อนกดซื้อ) — deterministic core logic."""
from datetime import datetime, timedelta

def hourly_wage(monthly_income, work_days=22, hours_per_day=8):
    if monthly_income <= 0 or work_days <= 0 or hours_per_day <= 0:
        raise ValueError("income/days/hours must be > 0")
    return round(monthly_income / (work_days * hours_per_day), 2)

def work_time(price, profile):
    w = hourly_wage(profile["monthly_income"], profile.get("work_days", 22), profile.get("hours_per_day", 8))
    hrs = price / w
    hpd = profile.get("hours_per_day", 8)
    return {"price_thb": price, "hourly_wage": w, "hours": round(hrs, 1),
            "work_days": round(hrs / hpd, 1),
            "pct_of_month": round(price / profile["monthly_income"] * 100, 1),
            "label_th": f"ต้องทำงาน {fmt_hours(hrs)}"}

def fmt_hours(hrs):
    h = int(hrs); m = int(round((hrs - h) * 60))
    if m == 60: h, m = h + 1, 0
    if h == 0: return f"{m} นาที"
    return f"{h} ชม. {m} นาที" if m else f"{h} ชม."

def cost_per_use(price, uses_per_month, months_life):
    uses = uses_per_month * months_life
    if uses <= 0:
        return {"total_uses": 0, "per_use_thb": price, "tier": "red"}
    per = round(price / uses, 2)
    tier = "green" if per <= 20 else "amber" if per <= 100 else "red"
    return {"total_uses": uses, "per_use_thb": per, "tier": tier}

QUESTIONS = [  # (id, text, weight, yes_is_good)
    ("need", "ถ้าไม่ซื้อ ชีวิตลำบากขึ้นจริงไหม", 25, True),
    ("have_similar", "มีของคล้ายกันอยู่แล้วไหม", 20, False),
    ("want_30d", "ถ้าอีก 30 วันยังอยากได้อยู่ไหม", 20, True),
    ("cash_ready", "จ่ายเงินสดได้โดยไม่ผ่อน/ไม่รูดบัตรรอ", 20, True),
    ("sale_pressure", "ซื้อเพราะ 'ลดราคาวันนี้วันเดียว' ใช่ไหม", 15, False),
]

def verdict(answers, cpu_tier, pct_of_month):
    score = 0
    for qid, _, wgt, good in QUESTIONS:
        if qid not in answers: raise ValueError(f"missing answer {qid}")
        if answers[qid] == good: score += wgt
    score += {"green": 10, "amber": 0, "red": -10}[cpu_tier]
    if pct_of_month > 30: score -= 15
    elif pct_of_month > 10: score -= 5
    score = max(0, min(100, score))
    v = "buy" if score >= 70 else "wait" if score >= 40 else "skip"
    th = {"buy": "คุ้ม ซื้อได้", "wait": "รอก่อน ตั้ง Cool-off", "skip": "ข้ามไป เก็บเงินเข้าโหล"}[v]
    return {"score": score, "verdict": v, "verdict_th": th}

def cooloff_hours(price, pct_of_month):
    if pct_of_month >= 30 or price >= 10000: return 72
    if pct_of_month >= 5 or price >= 1000: return 24
    return 0

def cooloff_status(started_iso, hours, now_iso):
    start = datetime.fromisoformat(started_iso); now = datetime.fromisoformat(now_iso)
    end = start + timedelta(hours=hours)
    left = max(0.0, (end - now).total_seconds() / 3600)
    return {"ends_at": end.isoformat(), "hours_left": round(left, 1), "unlocked": left == 0}

def skip_jar(skips, goal_thb):
    total = round(sum(s["price_thb"] for s in skips), 2)
    pct = round(min(100.0, total / goal_thb * 100), 1) if goal_thb > 0 else 0.0
    return {"saved_thb": total, "count": len(skips), "goal_thb": goal_thb, "goal_pct": pct,
            "reached": total >= goal_thb > 0}

def month_report(decisions, profile):
    bought = [d for d in decisions if d["outcome"] == "bought"]
    skipped = [d for d in decisions if d["outcome"] == "skipped"]
    s = sum(d["price_thb"] for d in skipped)
    top = max(skipped, key=lambda d: d["price_thb"])["name_th"] if skipped else None
    w = hourly_wage(profile["monthly_income"], profile.get("work_days", 22), profile.get("hours_per_day", 8))
    return {"bought": len(bought), "skipped": len(skipped),
            "spent_thb": round(sum(d["price_thb"] for d in bought), 2),
            "saved_thb": round(s, 2), "hours_saved": round(s / w, 1), "biggest_skip": top}

def habit_cost(price, per_week, profile):
    """ของเล็กที่ซื้อซ้ำ เช่น กาแฟ: ต่อเดือน/ต่อปี เป็นเงินและชั่วโมงงาน (ใช้ 52/12 สัปดาห์ต่อเดือน)"""
    month = round(price * per_week * 52 / 12, 2); year = round(price * per_week * 52, 2)
    w = hourly_wage(profile["monthly_income"], profile.get("work_days", 22), profile.get("hours_per_day", 8))
    return {"per_month_thb": month, "per_year_thb": year, "hours_per_month": round(month / w, 1), "hours_per_year": round(year / w, 1)}
