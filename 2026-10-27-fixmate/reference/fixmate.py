"""FixMate core logic (deterministic, no AI). Vision/LLM only fill Diagnosis JSON; rules here decide safety, cost, verdict."""
from datetime import date, timedelta
STOP, CAUTION, OK = "stop", "caution", "ok"
STOP_TAGS = {"gas_smell","burn_mark","sparking","water_near_power","ceiling_sag","structural_crack","main_panel","refrigerant","hot_surface_smell"}
CAUTION_TAGS = {"ladder_over_2m","power_tool","sharp_edge","heavy_lift","shutoff_unknown"}
STOP_MSG = {"gas_smell":"กลิ่นแก๊ส: ปิดวาล์ว เปิดหน้าต่าง ห้ามกดสวิตช์ ออกจากห้องแล้วโทรช่าง/นิติ",
            "burn_mark":"รอยไหม้ที่ปลั๊ก/สายไฟ: ตัดเบรกเกอร์ก่อน ให้ช่างไฟมาดู",
            "sparking":"มีประกายไฟ: ตัดไฟทันที ห้ามแตะ",
            "water_near_power":"น้ำใกล้ไฟฟ้า: ตัดเบรกเกอร์โซนนั้นก่อน",
            "ceiling_sag":"ฝ้าย้อย/บวมน้ำ: อาจถล่ม ออกจากใต้จุดนั้น แจ้งนิติ/ช่าง",
            "structural_crack":"รอยร้าวโครงสร้าง: ให้วิศวกร/ช่างประเมิน",
            "main_panel":"ตู้ไฟหลัก: งานช่างไฟเท่านั้น",
            "refrigerant":"น้ำยาแอร์: ต้องช่างแอร์ที่มีเครื่องมือ",
            "hot_surface_smell":"กลิ่นไหม้จากเครื่องใช้ไฟฟ้า: ถอดปลั๊ก หยุดใช้"}

def safety_gate(diag):
    tags = set(diag.get("hazard_tags", []))
    stop = sorted(tags & STOP_TAGS)
    if stop:
        return {"level": STOP, "reasons": [STOP_MSG[t] for t in stop], "allow_diy": False}
    reasons = sorted(tags & CAUTION_TAGS)
    if diag["confidence"] < 0.6:
        reasons.append("low_confidence: ขอรูปเพิ่มอีก 1-2 มุม")
    if reasons:
        return {"level": CAUTION, "reasons": reasons, "allow_diy": diag["difficulty"] <= 3}
    return {"level": OK, "reasons": [], "allow_diy": diag["difficulty"] <= 3}

def diy_cost(parts, tools, owned):
    p = sum(x["price_thb"] * x.get("qty", 1) for x in parts)
    missing = [t for t in tools if t["id"] not in owned]
    return {"parts_thb": p, "missing_tools": [t["id"] for t in missing],
            "tools_thb": sum(t["price_thb"] for t in missing),
            "total_thb": p + sum(t["price_thb"] for t in missing)}

def verdict(diag, parts, tools, owned, pro_quote_thb):
    if pro_quote_thb <= 0: raise ValueError("pro quote must be > 0")
    g = safety_gate(diag); c = diy_cost(parts, tools, owned)
    if not g["allow_diy"]:
        v = "call_pro"
    elif diag["confidence"] < 0.6:
        v = "need_photo"
    elif c["total_thb"] >= pro_quote_thb:
        v = "call_pro"
    else:
        v = "diy"
    return {"verdict": v, "safety": g["level"], "diy_total_thb": c["total_thb"],
            "pro_quote_thb": pro_quote_thb, "minutes": diag["minutes"],
            "save_thb": max(0, pro_quote_thb - c["total_thb"]) if v == "diy" else 0,
            "missing_tools": c["missing_tools"]}

def drip_waste(drips_per_min, ml_per_drip=0.05):
    if drips_per_min < 0: raise ValueError
    lpm = drips_per_min * ml_per_drip * 60 * 24 * 30 / 1000
    return {"liters_month": round(lpm), "buckets_10l": round(lpm / 10)}

def step_progress(steps, done_ids):
    done = [s for s in steps if s["id"] in done_ids]
    left = sum(s["minutes"] for s in steps if s["id"] not in done_ids)
    nxt = next((s["id"] for s in steps if s["id"] not in done_ids), None)
    return {"done": len(done), "total": len(steps), "pct": round(100 * len(done) / len(steps)),
            "minutes_left": left, "next_step": nxt}

def care_schedule(tasks, today):
    out = []
    for t in tasks:
        due = date.fromisoformat(t["last_done"]) + timedelta(days=t["every_days"])
        out.append({"id": t["id"], "title_th": t["title_th"], "next_due": due.isoformat(),
                    "overdue_days": max(0, (today - due).days), "due_in_days": max(0, (due - today).days)})
    return sorted(out, key=lambda x: (-x["overdue_days"], x["due_in_days"]))

def savings_tally(fixes):
    diy = [f for f in fixes if f["verdict"] == "diy" and f["status"] == "fixed"]
    return {"fixes": len(diy), "saved_thb": sum(f["save_thb"] for f in diy),
            "minutes": sum(f["minutes"] for f in diy),
            "badge": "ช่างประจำบ้าน" if len(diy) >= 3 else ("มือใหม่ซ่อมเป็น" if diy else None)}

def pro_message(diag, location, photos):
    return (f"สวัสดีครับ/ค่ะ รบกวนสอบถามค่าซ่อม: {diag['title_th']} ที่{location} "
            f"อาการ: {diag['symptom_th']} (แนบรูป {photos} รูป) สะดวกเข้ามาดูวันไหน และประมาณราคาเท่าไหร่คะ/ครับ")
