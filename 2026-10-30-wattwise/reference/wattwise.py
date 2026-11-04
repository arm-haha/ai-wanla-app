"""WattWise core logic — deterministic, no network. All rates are user-set (from their own bill)."""
from datetime import date
import calendar

def r2(x): return round(x + 1e-9, 2)

def kwh_month(watt=None, hours_per_day=0.0, days=30, kwh_per_day=None):
    if kwh_per_day is not None:
        if kwh_per_day < 0: raise ValueError("kwh_per_day < 0")
        return r2(kwh_per_day * days)
    if watt is None or watt < 0 or hours_per_day < 0 or hours_per_day > 24: raise ValueError("bad watt/hours")
    return r2(watt * hours_per_day * days / 1000)

def tier_of(cost):
    return "green" if cost < 100 else ("amber" if cost < 400 else "red")

def appliance_cost(app, rate, days=30):
    if rate <= 0: raise ValueError("rate must be > 0")
    k = kwh_month(app.get("watt"), app.get("hours_per_day", 0), days, app.get("kwh_per_day"))
    c = r2(k * rate)
    return {"appliance_id": app["id"], "kwh_month": k, "cost_month_thb": c, "cost_year_thb": r2(c * 12),
            "cost_per_hour_thb": r2((app["watt"] / 1000) * rate) if app.get("watt") else None, "tier": tier_of(c)}

def ac_temp_sim(base_cost, from_c, to_c, pct_per_deg=0.10):
    """Rule-of-thumb: each +1°C ≈ pct_per_deg less AC energy (user-adjustable assumption)."""
    if not (16 <= from_c <= 30 and 16 <= to_c <= 30): raise ValueError("temp 16-30")
    new = r2(base_cost * (1 - pct_per_deg) ** (to_c - from_c))
    return {"from_c": from_c, "to_c": to_c, "pct_per_deg": pct_per_deg, "base_cost_thb": base_cost,
            "new_cost_thb": new, "save_month_thb": r2(base_cost - new), "save_year_thb": r2((base_cost - new) * 12),
            "assumption_th": f"สมมติฐาน: ปรับ 1°C ประหยัด ~{int(pct_per_deg*100)}% (ตั้งค่าได้)"}

def bill_breakdown(bill, apps, rate):
    units, total = bill["units_kwh"], bill["total_thb"]
    if units <= 0: raise ValueError("units must be > 0")
    rows = [appliance_cost(a, rate) for a in apps]
    est = r2(sum(r["kwh_month"] for r in rows))
    slices = sorted(({"appliance_id": r["appliance_id"], "kwh": r["kwh_month"], "pct": r2(r["kwh_month"] / units * 100),
                      "thb": r2(r["kwh_month"] / units * total)} for r in rows), key=lambda s: -s["kwh"])
    unexplained = r2(max(units - est, 0))
    return {"bill_units": units, "bill_thb": total, "effective_rate": r2(total / units), "estimated_kwh": est,
            "unexplained_kwh": unexplained, "unexplained_pct": r2(unexplained / units * 100),
            "over_estimated": est > units, "top_appliance_id": slices[0]["appliance_id"] if slices else None, "slices": slices}

def standby_leak(items, rate):
    w = sum(i["standby_watt"] for i in items)
    k = kwh_month(w, 24)
    return {"total_standby_watt": w, "kwh_month": k, "cost_month_thb": r2(k * rate), "cost_year_thb": r2(k * rate * 12),
            "worst_id": max(items, key=lambda i: i["standby_watt"])["id"] if items else None}

def goal_track(readings, goal_thb, rate, today):
    """readings: [{date, meter_kwh}] ascending within the billing month."""
    if len(readings) < 2: raise ValueError("need >= 2 readings")
    d0, d1 = date.fromisoformat(readings[0]["date"]), date.fromisoformat(readings[-1]["date"])
    used = r2(readings[-1]["meter_kwh"] - readings[0]["meter_kwh"])
    if used < 0: raise ValueError("meter went backwards")
    days = max((d1 - d0).days, 1)
    t = date.fromisoformat(today); dim = calendar.monthrange(t.year, t.month)[1]
    per_day = r2(used / days); proj_kwh = r2(per_day * dim); proj = r2(proj_kwh * rate)
    budget_per_day = r2(goal_thb / rate / dim)
    return {"used_kwh": used, "days": days, "per_day_kwh": per_day, "projected_kwh": proj_kwh, "projected_thb": proj,
            "goal_thb": goal_thb, "budget_per_day_kwh": budget_per_day, "on_track": proj <= goal_thb, "gap_thb": r2(proj - goal_thb)}

def room_split(bill_thb, rooms):
    """rooms: [{name, kwh}] — split by metered/estimated share."""
    tot = sum(r["kwh"] for r in rooms)
    if tot <= 0: raise ValueError("no usage")
    out = [{"name": r["name"], "kwh": r["kwh"], "pct": r2(r["kwh"] / tot * 100), "thb": r2(r["kwh"] / tot * bill_thb)} for r in rooms]
    diff = r2(bill_thb - sum(o["thb"] for o in out)); out[0]["thb"] = r2(out[0]["thb"] + diff)  # penny fix
    return out

def swap_payback(old_watt, new_watt, hours_per_day, new_price, rate):
    save = r2((old_watt - new_watt) * hours_per_day * 30 / 1000 * rate)
    return {"save_month_thb": save, "payback_months": r2(new_price / save) if save > 0 else None}

def fmt_thb(x): return f"฿{x:,.0f}"
