"""ParkPin deterministic logic (no AI calls). Fees, hours and walking steps are app-chosen examples — not official mall rates, and plates must not be stored."""
import datetime as _dt
import urllib.parse as _up

MIN_CONF = 0.6
FREE_PINS_PER_DAY = 3
WATERMARK = "Made with ParkPin · example rates only, no plate"
SAFETY_DISCLAIMER_TH = "ParkPin ช่วยจำที่จอดและประมาณค่าจอดจากตารางตัวอย่าง ไม่ใช่อัตราทางการของห้าง และไม่ใช่ระบบนำทางสด ห้ามถ่ายหรือเก็บแผ่นป้ายทะเบียน"
FEE_DISCLAIMER_TH = "ค่าจอดเป็นตารางตัวอย่างที่ตั้งเอง ไม่ใช่ราคาห้างจริง ตรวจป้ายอัตราที่ลานก่อนออก"
FLOOR_KINDS = ["B3","B2","B1","G","1F","2F","3F","4F","5F","6F","rooftop"]
COLORS = ["green","yellow","red","blue","orange","purple","white"]
COLOR_TH = {"green":"เขียว","yellow":"เหลือง","red":"แดง","blue":"ฟ้า","orange":"ส้ม","purple":"ม่วง","white":"ขาว"}

# Example rate cards (not real mall tariffs).
MALLS = {
    "fictomall_bangna": {
        "id": "m01", "name_th": "FictoMall บางนา", "close_hhmm": "22:00", "grace_min": 15,
        "per_hour_thb": 20, "cap_thb": 200, "lost_ticket_thb": 300,
        "landmarks_th": ["ลิฟต์ฝั่งศูนย์อาหาร", "ประตู 3", "ทางเชื่อม BTS จำลอง"],
    },
    "fictoplex_siri": {
        "id": "m02", "name_th": "FictoPlex สิริ", "close_hhmm": "21:30", "grace_min": 10,
        "per_hour_thb": 25, "cap_thb": 250, "lost_ticket_thb": 400,
        "landmarks_th": ["ลิฟต์ฝั่งโรงหนัง", "เสาธงลานหน้า"],
    },
    "fictoworld_chiangmai": {
        "id": "m03", "name_th": "FictoWorld เชียงใหม่", "close_hhmm": "21:00", "grace_min": 30,
        "per_hour_thb": 15, "cap_thb": 120, "lost_ticket_thb": 200,
        "landmarks_th": ["ทางเข้าตลาดจำลอง", "ลิฟต์แก้ว"],
    },
    "fictopark_airport": {
        "id": "m04", "name_th": "FictoPark สนามบิน", "close_hhmm": "23:59", "grace_min": 0,
        "per_hour_thb": 40, "cap_thb": 400, "lost_ticket_thb": 500,
        "landmarks_th": ["สะพานลอยทางเดิน", "ประตู 4"],
    },
}

def _parse_hhmm(s):
    hh, mm = s.split(":")
    return int(hh), int(mm)

def scan_quality(glare, blur, tilt, sign_fill):
    for v in (glare, blur, tilt, sign_fill):
        if not 0 <= v <= 1:
            raise ValueError("quality inputs must be 0..1")
    score = round(100 * (1 - (0.30 * glare + 0.35 * blur + 0.20 * tilt + 0.15 * (1 - sign_fill))))
    tips = []
    if glare > 0.5:
        tips.append("แสงสะท้อนบนป้าย/เสา ขยับมุมหรือปิดแฟลช")
    if blur > 0.4:
        tips.append("ภาพเบลอ ถ่ายเสาหรือป้ายชั้นให้นิ่ง")
    if tilt > 0.4:
        tips.append("ถ่ายเอียงเกินไป ถ่ายป้ายชั้นและเสาให้ตั้งตรง")
    if sign_fill < 0.5:
        tips.append("ป้ายชั้นหรือเสาไม่เต็มกรอบ ถ่ายให้เห็นตัวอักษรและสีโซน")
    ok = score >= 60 and sign_fill >= 0.5
    if not ok and not tips:
        tips.append("ถ่ายใหม่ให้เห็นชั้น โซน และเสาชัด")
    return {"score": score, "ok": ok, "tips_th": tips}

def identify_pin(photo, min_conf=MIN_CONF):
    conf = photo["confidence"]
    if conf < min_conf:
        return {"ok": False, "uncertain": True, "message_th": "ยังอ่านป้ายชั้น/เสาไม่ชัด เลือกเองหรือถ่ายใหม่"}
    if photo["floor"] not in FLOOR_KINDS:
        raise ValueError("unknown floor")
    if photo["color"] not in COLORS:
        raise ValueError("unknown color")
    return {"ok": True, "uncertain": False, "message_th": ""}

def pin_scan(photo):
    q = scan_quality(photo["glare"], photo["blur"], photo["tilt"], photo["sign_fill"])
    ident = identify_pin(photo)
    return {
        "photo_id": photo["id"], "mall_id": photo["mall_id"],
        "mall_th": MALLS[photo["mall_id"]]["name_th"] if photo["mall_id"] in MALLS else "",
        "floor": photo["floor"], "zone": photo["zone"], "color": photo["color"],
        "color_th": COLOR_TH[photo["color"]], "pillar": photo["pillar"],
        "quality": q, "ok": q["ok"] and ident["ok"], "uncertain": ident["uncertain"],
        "message_th": ident["message_th"], "has_plate": bool(photo.get("has_plate", False)),
        "disclaimer_th": SAFETY_DISCLAIMER_TH,
    }

def pipeline_steps(photo):
    s = ["sign_detect"]
    if photo["glare"] > 0.5:
        s.append("deglare")
    if photo["tilt"] > 0.4:
        s.append("deskew")
    if photo.get("has_plate"):
        s.append("plate_blur")
    s += ["floor_read", "zone_color", "pin_save", "fee_timer", "walkback"]
    return s

def _require_mall(mall_id):
    if mall_id not in MALLS:
        raise ValueError("unknown mall " + mall_id)
    return MALLS[mall_id]

def elapsed_minutes(parked_at, now):
    t0 = _dt.datetime.fromisoformat(parked_at)
    t1 = _dt.datetime.fromisoformat(now)
    if t1 < t0:
        raise ValueError("now is before parked_at")
    return int((t1 - t0).total_seconds() // 60)

def fee_estimate(mall_id, parked_at, now):
    mall = _require_mall(mall_id)
    mins = elapsed_minutes(parked_at, now)
    if mins <= mall["grace_min"]:
        hours = 0
        fee = 0
    else:
        import math
        hours = int(math.ceil((mins - mall["grace_min"]) / 60.0))
        fee = min(mall["cap_thb"], hours * mall["per_hour_thb"])
    # next jump
    if fee >= mall["cap_thb"] or mins <= mall["grace_min"] and mins < mall["grace_min"]:
        pass
    if mins <= mall["grace_min"]:
        next_in = mall["grace_min"] - mins
        next_fee = mall["per_hour_thb"]
    elif fee >= mall["cap_thb"]:
        next_in = None
        next_fee = mall["cap_thb"]
    else:
        billed = mins - mall["grace_min"]
        rem = 60 - (billed % 60)
        if rem == 60:
            rem = 60
        next_in = rem
        next_fee = min(mall["cap_thb"], fee + mall["per_hour_thb"])
    return {
        "mall_id": mall_id, "mall_th": mall["name_th"], "minutes": mins, "hours_billed": hours,
        "fee_thb": fee, "cap_thb": mall["cap_thb"], "per_hour_thb": mall["per_hour_thb"],
        "grace_min": mall["grace_min"], "next_jump_min": next_in, "next_fee_thb": next_fee,
        "lost_ticket_thb": mall["lost_ticket_thb"],
        "disclaimer_th": FEE_DISCLAIMER_TH,
    }

def close_reminder(mall_id, now):
    mall = _require_mall(mall_id)
    hh, mm = _parse_hhmm(mall["close_hhmm"])
    t = _dt.datetime.fromisoformat(now)
    close = t.replace(hour=hh, minute=mm, second=0, microsecond=0)
    # 23:59 special
    minutes_left = int((close - t).total_seconds() // 60)
    if minutes_left < 0:
        status, message_th = "after_close", "เลยเวลาปิดลานตามตารางตัวอย่างแล้ว ตรวจป้ายจริงก่อนออก"
    elif minutes_left <= 30:
        status, message_th = "soon", f"อีก {minutes_left} นาทีจะถึงเวลาปิดลานตามตารางตัวอย่าง ({mall['close_hhmm']})"
    else:
        status, message_th = "ok", f"ลานตามตารางตัวอย่างปิด {mall['close_hhmm']} เหลืออีก {minutes_left} นาที"
    return {
        "mall_id": mall_id, "close_hhmm": mall["close_hhmm"], "minutes_left": minutes_left,
        "status": status, "message_th": message_th, "disclaimer_th": "เวลาปิดเป็นค่าตัวอย่าง ไม่ใช่เวลาห้างจริง",
    }

def walkback_guide(photo, parked_hint_th=""):
    mall = _require_mall(photo["mall_id"])
    steps = [
        f"กลับเข้า{mall['name_th']} จากจุดที่จำได้ เช่น {mall['landmarks_th'][0]}",
        f"ขึ้น/ลงไปชั้น {photo['floor']}",
        f"ตามโซนสี{COLOR_TH[photo['color']]} โซน {photo['zone']}",
        f"หาเสา {photo['pillar']}",
    ]
    if parked_hint_th:
        steps.append(parked_hint_th)
    steps.append("ถ้าหาไม่เจอ เปิดโหมดรถหายในแอปแล้วย้อนรูปป้ายที่ปักไว้ อย่าเดินในเลนรถ")
    return {
        "mall_th": mall["name_th"], "floor": photo["floor"], "zone": photo["zone"],
        "color": photo["color"], "color_th": COLOR_TH[photo["color"]], "pillar": photo["pillar"],
        "steps": [{"n": i + 1, "text_th": t} for i, t in enumerate(steps)],
        "disclaimer_th": "เป็นคำใบ้จากป้ายที่คุณปักไว้ ไม่ใช่ระบบนำทางสด",
    }

def save_pin(pid, person_id, photo, parked_at, hint_th="", plate_note=""):
    if plate_note:
        raise ValueError("do not store license plates")
    scan = pin_scan(photo)
    if photo.get("has_plate"):
        # still allow the pin but flag it must be blurred
        flag = True
    else:
        flag = False
    return {
        "id": pid, "person_id": person_id, "photo_id": photo["id"], "mall_id": photo["mall_id"],
        "mall_th": scan["mall_th"], "floor": photo["floor"], "zone": photo["zone"],
        "color": photo["color"], "pillar": photo["pillar"], "parked_at": parked_at,
        "hint_th": hint_th, "needs_plate_blur": flag, "on_device": True,
    }

def lost_car(pin, now, photo):
    fee = fee_estimate(pin["mall_id"], pin["parked_at"], now)
    walk = walkback_guide(photo, pin.get("hint_th", ""))
    return {
        "pin_id": pin["id"], "mall_th": pin["mall_th"], "floor": pin["floor"],
        "zone": pin["zone"], "pillar": pin["pillar"], "minutes": fee["minutes"],
        "fee_thb": fee["fee_thb"], "walkback": walk,
        "message_th": f"ปักไว้ชั้น {pin['floor']} โซน {pin['zone']} เสา {pin['pillar']} เมื่อ {fee['minutes']} นาทีที่แล้ว",
        "disclaimer_th": SAFETY_DISCLAIMER_TH,
    }

def family_share(person, pin, fee, walk, note_th=""):
    text = (
        f"ParkPin — ที่จอดรถ\n"
        f"{pin['mall_th']} ชั้น {pin['floor']} โซน {pin['zone']} เสา {pin['pillar']}\n"
        f"จอดมา {fee['minutes']} นาที ค่าจอดอย่างคร่าว ฿{fee['fee_thb']:,} (ตารางตัวอย่าง)\n"
        f"{note_th}".strip()
    )
    return {
        "title_th": "แชร์ที่จอดกับครอบครัว",
        "name_th": person["name_th"],
        "mall_th": pin["mall_th"],
        "floor": pin["floor"],
        "zone": pin["zone"],
        "pillar": pin["pillar"],
        "minutes": fee["minutes"],
        "fee_thb": fee["fee_thb"],
        "steps_count": len(walk["steps"]),
        "note_th": note_th,
        "line_share_url": "https://line.me/R/share?text=" + _up.quote(text),
        "disclaimer_th": SAFETY_DISCLAIMER_TH + " " + FEE_DISCLAIMER_TH,
    }

def share_card(name_th, pin, fee):
    return {
        "title_th": f"ParkPin — {name_th}",
        "headline_th": f"{pin['mall_th']} · {pin['floor']} โซน {pin['zone']} เสา {pin['pillar']}",
        "hook_th": f"จอดมา {fee['minutes']} นาที · ประมาณ ฿{fee['fee_thb']:,}",
        "floor": pin["floor"], "layout": "pin_card",
        "sizes": ["1080x1350", "1080x1920", "1080x1080"],
        "watermark": WATERMARK, "cta_th": "คอมเมนต์ PARK รับแพ็กฟรี",
    }

def quota(used_today, want, pro=False):
    if pro:
        return {"allowed": want, "left_after": None, "paywall": False}
    left = max(0, FREE_PINS_PER_DAY - used_today)
    allowed = min(want, left)
    return {"allowed": allowed, "left_after": left - allowed, "paywall": allowed < want}

def safety_guard(has_plate=False):
    if has_plate:
        return {"level": "warn", "message_th": "ตรวจพบว่าในรูปอาจมีป้ายทะเบียน ให้เบลอก่อนบันทึก " + SAFETY_DISCLAIMER_TH}
    return {"level": "ok", "message_th": SAFETY_DISCLAIMER_TH}

def mall_info(mall_id):
    m = dict(_require_mall(mall_id))
    return m

def history_stats(pins):
    if not pins:
        return {"count": 0, "malls": 0, "last_parked_at": None, "top_mall": None}
    last = max(pins, key=lambda p: p["parked_at"])["parked_at"]
    from collections import Counter
    c = Counter(p["mall_id"] for p in pins)
    return {"count": len(pins), "malls": len(c), "last_parked_at": last, "top_mall": c.most_common(1)[0][0]}
