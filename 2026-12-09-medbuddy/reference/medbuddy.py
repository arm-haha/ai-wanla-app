"""MedBuddy deterministic logic (no AI calls). Caregiver med schedule helper — not a pharmacist, never changes doses."""
import datetime as _dt

SLOTS = {
    "morning": "เช้า",
    "noon": "กลางวัน",
    "evening": "เย็น",
    "bedtime": "ก่อนนอน",
    "as_needed": "เมื่อปวด / เมื่อมีอาการ",
}
FOOD = {
    "before_food": "ก่อนอาหาร",
    "after_food": "หลังอาหาร",
    "with_food": "พร้อมอาหาร",
    "any": "ไม่ระบุมื้อ",
}
# Fictional library only — not real medicines or dosing advice
LIBRARY = {
    "FictoPril": {"id": "m01", "kind_th": "ตัวอย่างยาความดันในแอป", "form_th": "เม็ด"},
    "FictoMet": {"id": "m02", "kind_th": "ตัวอย่างยาเบาหวานในแอป", "form_th": "เม็ด"},
    "FictoPain": {"id": "m03", "kind_th": "ตัวอย่างยาแก้ปวดในแอป", "form_th": "เม็ด"},
    "FictoCough": {"id": "m04", "kind_th": "ตัวอย่างยาแก้ไอในแอป", "form_th": "น้ำ"},
    "FictoVit": {"id": "m05", "kind_th": "ตัวอย่างวิตามินในแอป", "form_th": "เม็ด"},
}
MIN_CONF = 0.6
SOON_DAYS = 14
FREE_GENS_PER_DAY = 3
WATERMARK = "Made with MedBuddy · confirm with a pharmacist, never change doses"
SAFETY_DISCLAIMER_TH = "MedBuddy เป็นตารางช่วยเตือนเท่านั้น ไม่ใช่เภสัชกร ไม่ใช่แพทย์ และไม่ใช่ใบสั่งยา ห้ามเปลี่ยนขนาดยาเอง ทุกครั้งต้องยืนยันกับเภสัชกรหรือแพทย์ก่อนใช้จริง หากมีอาการผิดปกติให้หยุดแล้วปรึกษาแพทย์ทันที"
CONFIRM_DISCLAIMER_TH = "ช่องที่ความมั่นใจต่ำกว่า 0.6 ต้องให้ผู้ใช้ยืนยันกับซองยาก่อนบันทึก ห้ามเดาขนาดยา"

def scan_quality(glare, blur, crop):
    for v in (glare, blur, crop):
        if not 0 <= v <= 1:
            raise ValueError("glare/blur/crop must be 0..1")
    score = int(round(100 * (1 - (0.30 * glare + 0.40 * blur + 0.30 * crop))))
    tips = []
    if glare > 0.5:
        tips.append("ซองยามีแสงสะท้อน ถ่ายในที่ร่มและวางราบ")
    if blur > 0.4:
        tips.append("ตัวอักษรบนซองเบลอ ถือนิ่งแล้วถ่ายใหม่ให้เห็นชื่อยาและขนาดชัด")
    if crop > 0.45:
        tips.append("ซองถูกตัด จัดให้เห็นทั้งซอง รวมวิธีการกินและจำนวนเม็ด")
    return {"score": score, "ok": score >= 60, "tips_th": tips}


def photo_scan(photo):
    q = scan_quality(photo["glare"], photo["blur"], photo["crop"])
    return {"photo_id": photo["id"], "quality": q}


def pipeline_steps(photo, labels):
    s = ["label_photo"]
    if photo["glare"] > 0.5:
        s.append("deglare")
    if photo["crop"] > 0.45:
        s.append("recrop")
    s += ["parse_label", "confirm_low_conf", "schedule", "refill", "safety"]
    if any(x["confidence"] < MIN_CONF for x in labels):
        s.append("ask_user_confirm")
    return s


def library_info(name):
    if name not in LIBRARY:
        raise ValueError("unknown library item")
    item = LIBRARY[name]
    return {"id": item["id"], "name": name, "kind_th": item["kind_th"], "form_th": item["form_th"],
            "disclaimer_th": "รายการในคลังเป็นชื่อสมมติสำหรับเดโมเท่านั้น ไม่ใช่ยาจริง"}


def parse_label(raw):
    """Accept structured extraction; flag any field below MIN_CONF for confirmation. Never invent a dose."""
    required = ("name", "strength_th", "dose_th", "slots", "food", "qty", "confidence")
    for k in required:
        if k not in raw:
            raise ValueError("missing field " + k)
    if raw["food"] not in FOOD:
        raise ValueError("unknown food timing")
    if not raw["slots"] or any(sl not in SLOTS for sl in raw["slots"]):
        raise ValueError("unknown or empty slots")
    if raw["qty"] < 0:
        raise ValueError("qty must be >= 0")
    if not 0 <= raw["confidence"] <= 1:
        raise ValueError("confidence must be 0..1")
    needs = raw["confidence"] < MIN_CONF
    return {
        "name": raw["name"], "strength_th": raw["strength_th"], "dose_th": raw["dose_th"],
        "slots": list(raw["slots"]), "food": raw["food"], "food_th": FOOD[raw["food"]],
        "qty": raw["qty"], "daily_units": raw.get("daily_units"),
        "confidence": raw["confidence"], "needs_confirm": needs,
        "prn_max_per_day": raw.get("prn_max_per_day"),
        "message_th": (
            "ความมั่นใจต่ำ ต้องยืนยันทุกช่องกับซองยาและเภสัชกร ห้ามบันทึกขนาดยาที่ยังไม่ชัด"
            if needs else "อ่านซองได้ แต่ยังต้องให้เภสัชกรหรือผู้ใช้ยืนยันก่อนใช้จริง"
        ),
        "disclaimer_th": SAFETY_DISCLAIMER_TH,
    }


def schedule(meds):
    if not meds:
        raise ValueError("no medicines")
    if any(m["needs_confirm"] for m in meds):
        raise ValueError("confirm low-confidence labels before scheduling")
    by = {k: [] for k in SLOTS}
    for m in meds:
        for sl in m["slots"]:
            by[sl].append({
                "name": m["name"], "strength_th": m["strength_th"], "dose_th": m["dose_th"],
                "food_th": m["food_th"],
            })
    slots = [{"slot": k, "slot_th": SLOTS[k], "items": by[k], "count": len(by[k])} for k in SLOTS if by[k]]
    return {
        "slots": slots, "med_count": len(meds), "slot_count": len(slots),
        "headline_th": f"ตารางกินยา {len(meds)} รายการ",
        "disclaimer_th": SAFETY_DISCLAIMER_TH,
    }


def _as_date(s):
    return _dt.date.fromisoformat(s)


def refill_status(days_left, qty, prn=False):
    if prn:
        return "ask" if qty <= 10 else "ok"
    if days_left is None:
        return "ask"
    if days_left <= 0:
        return "due"
    if days_left <= SOON_DAYS:
        return "soon"
    return "ok"


def refill(med, start_date, today):
    prn = med["slots"] == ["as_needed"]
    if prn:
        days = None
        due = None
        status = refill_status(None, med["qty"], prn=True)
        msg = f"ยาใช้เมื่อมีอาการ เหลือ {med['qty']} หน่วย ให้ถามเภสัชกรก่อนซื้อเพิ่ม ห้ามเพิ่มขนาดเอง"
    else:
        daily = med["daily_units"]
        if daily is None or daily <= 0:
            raise ValueError("daily_units required for scheduled meds")
        days = med["qty"] // daily
        start = _as_date(start_date)
        # days left from today, assuming the remaining qty is counted today
        due = ( _as_date(today) + _dt.timedelta(days=days) ).isoformat()
        status = refill_status(days, med["qty"], prn=False)
        label = {"ok": "ยังไม่ใกล้หมด", "soon": "ใกล้หมด ควรให้เภสัชกรช่วยเช็กการซื้อเพิ่ม", "due": "หมดแล้ว อย่าปรับขนาดเอง ให้ปรึกษาเภสัชกรหรือแพทย์"}
        msg = f"เหลือประมาณ {days} วัน (ถึง {due}) · {label[status]}"
    return {
        "name": med["name"], "qty": med["qty"], "daily_units": med.get("daily_units"),
        "days_left": days, "due_date": due, "status": status, "prn": prn,
        "message_th": msg, "disclaimer_th": SAFETY_DISCLAIMER_TH,
    }


def missed_dose_guide(slot):
    if slot not in SLOTS:
        raise ValueError("unknown slot")
    return {
        "slot": slot, "slot_th": SLOTS[slot],
        "steps_th": [
            "อย่ากินเพิ่มเป็นสองเท่า และอย่าเปลี่ยนขนาดเอง",
            "ดูฉลากซองยาว่ามีคำแนะนำเมื่อลืมหรือไม่",
            "โทรถามเภสัชกรหรือแพทย์ก่อนกินมื้อถัดไป",
        ],
        "headline_th": "ลืมกินยา — อย่าเพิ่มขนาดเอง",
        "disclaimer_th": SAFETY_DISCLAIMER_TH,
    }


def interaction_flag(meds):
    names = [m["name"] for m in meds]
    if len(set(names)) >= 2:
        return {
            "level": "ask", "med_count": len(set(names)),
            "message_th": "มียาหลายชนิดในตาราง ให้เภสัชกรช่วยเช็กร่วมกัน ห้ามเพิ่ม ลด หรือหยุดยาเอง",
            "disclaimer_th": SAFETY_DISCLAIMER_TH,
        }
    return {
        "level": "ok", "med_count": len(set(names)),
        "message_th": "ยังมีรายการเดียวในตาราง แต่ทุกครั้งที่เพิ่มยาใหม่ให้เภสัชกรช่วยเช็ก",
        "disclaimer_th": SAFETY_DISCLAIMER_TH,
    }


def visit_card(patient_th, meds, clinic_th, doctor_th, visit_date, note_th=""):
    if not meds:
        raise ValueError("no medicines")
    lines = [f"{m['name']} {m['strength_th']} · {m['dose_th']} · {m['food_th']}" for m in meds]
    return {
        "patient_th": patient_th, "clinic_th": clinic_th, "doctor_th": doctor_th, "visit_date": visit_date,
        "meds": lines, "med_count": len(lines), "note_th": note_th,
        "headline_th": f"รายการยาของ {patient_th} สำหรับนัด {visit_date}",
        "disclaimer_th": "การ์ดนี้เป็นรายการที่ผู้ใช้บันทึก ไม่ใช่ใบสั่งยา ให้นำซองยาจริงไปด้วยและให้แพทย์หรือเภสัชกรตรวจอีกครั้ง",
    }


def caregiver_share(caregiver_th, patient_th, schedule_obj, today):
    pending = [s["slot_th"] for s in schedule_obj["slots"] if s["slot"] != "as_needed"]
    return {
        "caregiver_th": caregiver_th, "patient_th": patient_th, "date": today,
        "pending_slots_th": pending, "slot_count": len(pending),
        "headline_th": f"วันนี้ {patient_th} มี {len(pending)} ช่วงเวลากินยา",
        "cta_th": "ติ๊กเมื่อกินแล้ว แล้วส่งให้ลูกในครอบครัวได้",
        "disclaimer_th": SAFETY_DISCLAIMER_TH,
    }


def share_card(patient_th, med_count, headline_th):
    return {
        "title_th": f"MedBuddy — {patient_th}",
        "headline_th": headline_th,
        "hook_th": "ถ่ายซองยาพ่อแม่ ได้ตารางกินยาและเตือนลูก",
        "med_count": med_count,
        "layout": "schedule_card", "sizes": ["1080x1350", "1080x1920", "1080x1080"],
        "watermark": WATERMARK,
        "cta_th": f"คอมเมนต์ MED รับแพ็กฟรี · {patient_th}",
        "disclaimer_th": SAFETY_DISCLAIMER_TH,
    }


def quota(used_today, want, pro=False):
    if pro:
        return {"allowed": want, "left_after": None, "paywall": False}
    left = max(0, FREE_GENS_PER_DAY - used_today)
    allowed = min(want, left)
    return {"allowed": allowed, "left_after": left - allowed, "paywall": allowed < want}


def safety_guard(confirmed=True):
    if not confirmed:
        return {"level": "stop", "message_th": "ยังใช้ตารางไม่ได้ จนกว่าจะยืนยันกับซองยาและเภสัชกร " + SAFETY_DISCLAIMER_TH}
    return {"level": "ok", "message_th": SAFETY_DISCLAIMER_TH}
