"""PhoneRescue deterministic logic (no AI calls). GB saved and repair prices are app-chosen examples — not a shop or a repair quote."""
FREE_SCANS_PER_DAY = 3
MIN_CONF = 0.6
WATERMARK = "Made with PhoneRescue · guidance only, not a repair quote"
SAFETY_DISCLAIMER_TH = "PhoneRescue เป็นคำแนะนำเบื้องต้นจากการอ่านหน้าจอตั้งค่า ไม่ใช่ร้านซ่อมและไม่ใช่ใบเสนอราคา สำรองข้อมูลก่อนลบ และอย่ารีเซ็ตเครื่องถ้ายังไม่ได้สำรอง"
PRICE_DISCLAIMER_TH = "ราคาเป็นช่วงประมาณการที่ตั้งเอง ไม่ใช่ราคาศูนย์หรือร้านซ่อมจริง"

CLEANUP = {
    "duplicates": {"id": "c01", "name_th": "รูปซ้ำและรูปคล้าย", "gb": 6.2, "priority": 1,
                   "how_th": "เปิดอัลบั้ม ดูกลุ่มรูปคล้าย เก็บแค่ใบที่ดีที่สุดแล้วลบที่เหลือ"},
    "screenshots": {"id": "c02", "name_th": "แคปจอและรูปต่อเนื่อง", "gb": 3.1, "priority": 2,
                    "how_th": "กรองอัลบั้มเป็นแคปจอและเบิร์สต์ ลบที่อ่านแล้วหรือเบลอ"},
    "chat_backup": {"id": "c03", "name_th": "ไฟล์สำรองแชทในเครื่อง", "gb": 4.0, "priority": 3,
                    "how_th": "ย้ายสำรองแชทขึ้นคลาวด์ที่ไว้ใจหรือลบไฟล์เก่าหลังยืนยันว่าสำรองแล้ว"},
    "unused_apps": {"id": "c04", "name_th": "แอปที่ไม่ได้เปิดนาน", "gb": 2.4, "priority": 4,
                    "how_th": "ถอดโหลดหรือลบแอปที่ไม่ได้ใช้ 90 วัน ของในแอปควรสำรองก่อน"},
    "cache": {"id": "c05", "name_th": "แคชแอปและไฟล์ชั่วคราว", "gb": 1.1, "priority": 5,
              "how_th": "ล้างแคชแอปวิดีโอและเบราว์เซอร์ อย่าลบโฟลเดอร์ดาวน์โหลดทั้งก้อนโดยไม่ดู"},
}
BATTERY_REPAIR = {"min": 1900, "max": 3500, "mid": 2500}
NEW_PHONE = {"min": 12900, "max": 19900, "mid": 15900}

DUP_STEPS = [
    "สำรองรูปสำคัญขึ้นคลาวด์หรือสายคอมพิวเตอร์ก่อนลบ",
    "เปิดอัลบั้มแล้วกรองเป็นรูปคล้ายหรือเบิร์สต์",
    "ในแต่ละกลุ่มเก็บ 1 ใบที่คมและสว่างที่สุด",
    "ลบรูปที่เหลือในกลุ่ม แล้วลบถังขยะรูปด้วย",
    "เช็กพื้นที่ว่างอีกครั้งในหน้าตั้งค่า",
]

def scan_quality(glare, blur, crop, n_dets):
    for v in (glare, blur, crop):
        if not 0 <= v <= 1:
            raise ValueError("glare/blur/crop must be 0..1")
    score = round(100 * (1 - (0.35 * glare + 0.40 * blur + 0.25 * crop)))
    if n_dets == 0:
        score = max(0, score - 30)
    tips = []
    if glare > 0.5:
        tips.append("แสงสะท้อนบนจอเยอะ ลดความสว่างจอหรือถ่ายในที่ร่ม")
    if blur > 0.4:
        tips.append("ภาพเบลอ แคปจอจากเครื่องโดยตรงจะอ่านง่ายกว่าการถ่ายหน้าจอ")
    if crop > 0.45:
        tips.append("ตัวเลขถูกครอป เลื่อนหน้าตั้งค่าให้เห็นทั้งปริมาณที่ใช้และทั้งหมด")
    if n_dets == 0:
        tips.append("ไม่เจอตัวเลขพื้นที่หรือแบต เปิดหน้าตั้งค่าพื้นที่ว่างหรือสุขภาพแบตแล้วแคปใหม่")
    return {"score": score, "ok": score >= 60 and n_dets >= 1, "tips_th": tips}

def _num(dets, key, default=None):
    for d in dets:
        if d.get("key") == key and d.get("confidence", 0) >= MIN_CONF:
            return d["value"]
    return default

def parse_storage(shot):
    q = scan_quality(shot["glare"], shot["blur"], shot["crop"], len(shot["detections"]))
    used = _num(shot["detections"], "used_gb")
    total = _num(shot["detections"], "total_gb")
    if used is None or total is None or total <= 0:
        return {"shot_id": shot["id"], "quality": q, "ok": False, "used_gb": used, "total_gb": total,
                "free_gb": None, "percent": None, "breakdown": {}, "message_th": "อ่านตัวเลขพื้นที่ไม่ครบ ลองแคปหน้าตั้งค่าพื้นที่ว่างใหม่"}
    free = round(total - used, 1)
    pct = int(round(100 * used / total))
    breakdown = {}
    for k in ("photos_gb", "apps_gb", "system_gb", "other_gb"):
        v = _num(shot["detections"], k)
        if v is not None:
            breakdown[k] = v
    return {"shot_id": shot["id"], "quality": q, "ok": q["ok"], "used_gb": used, "total_gb": total,
            "free_gb": free, "percent": pct, "breakdown": breakdown,
            "message_th": f"ใช้ไป {used:g}/{total:g} GB ({pct}%) เหลือ {free:g} GB"}

def parse_battery(shot):
    q = scan_quality(shot["glare"], shot["blur"], shot["crop"], len(shot["detections"]))
    health = _num(shot["detections"], "health_pct")
    if health is None:
        return {"shot_id": shot["id"], "quality": q, "ok": False, "health_pct": None, "screen_on_h": None,
                "last_charge_h": None, "brightness_pct": None, "background_refresh": None, "low_power": None,
                "message_th": "อ่านสุขภาพแบตไม่ครบ เปิดหน้าแบตเตอรี่แล้วแคปใหม่"}
    return {"shot_id": shot["id"], "quality": q, "ok": q["ok"], "health_pct": int(health),
            "screen_on_h": _num(shot["detections"], "screen_on_h"),
            "last_charge_h": _num(shot["detections"], "last_charge_h"),
            "brightness_pct": _num(shot["detections"], "brightness_pct"),
            "background_refresh": _num(shot["detections"], "background_refresh"),
            "low_power": _num(shot["detections"], "low_power"),
            "message_th": f"สุขภาพแบตประมาณ {int(health)}%"}

def pipeline_steps(shot):
    s = ["screen_detect"]
    if shot["glare"] > 0.5:
        s.append("deglare")
    if shot["crop"] > 0.45:
        s.append("recrop")
    kinds = {d.get("key", "").split("_")[0] for d in shot["detections"]}
    if any(k in (d.get("key") or "") for d in shot["detections"] for k in ("used_gb", "total_gb", "photos_gb")):
        s += ["ocr_storage", "cleanup_plan"]
    if any("health" in (d.get("key") or "") or "charge" in (d.get("key") or "") or "brightness" in (d.get("key") or "") for d in shot["detections"]):
        s += ["ocr_battery", "battery_tips", "repair_check"]
    if len(s) == 1:
        s.append("need_settings_page")
    return s

def cleanup_plan(storage, include=None):
    if not storage.get("ok"):
        raise ValueError("storage not ok")
    keys = include or list(CLEANUP)
    for k in keys:
        if k not in CLEANUP:
            raise ValueError("unknown action " + k)
    actions = []
    saved = 0.0
    for k in sorted(keys, key=lambda x: CLEANUP[x]["priority"]):
        c = CLEANUP[k]
        gb = c["gb"]
        # scale slightly if the device has fewer photos than the demo? keep fixed example values
        saved += gb
        actions.append({"id": c["id"], "key": k, "name_th": c["name_th"], "gb": gb, "priority": c["priority"],
                        "how_th": c["how_th"], "n": len(actions) + 1})
    saved = round(saved, 1)
    after_used = round(max(0.0, storage["used_gb"] - saved), 1)
    after_free = round(storage["total_gb"] - after_used, 1)
    return {"used_gb": storage["used_gb"], "total_gb": storage["total_gb"], "free_gb": storage["free_gb"],
            "saved_gb": saved, "after_used_gb": after_used, "after_free_gb": after_free,
            "actions": actions, "count": len(actions),
            "headline_th": f"เก็บพื้นที่ได้ประมาณ {saved:g} GB · เหลือว่าง ~{after_free:g} GB"}

def duplicate_guide():
    return {"title_th": "คู่มือลบรูปซ้ำ", "steps": [{"n": i + 1, "text_th": t} for i, t in enumerate(DUP_STEPS)],
            "disclaimer_th": "สำรองก่อนลบเสมอ " + SAFETY_DISCLAIMER_TH}

def battery_tips(battery):
    if not battery.get("ok") or battery.get("health_pct") is None:
        raise ValueError("battery not ok")
    tips, keys = [], []
    h = battery["health_pct"]
    if h >= 85:
        keys.append("health_ok"); tips.append("สุขภาพแบตยังอยู่ในเกณฑ์ที่ใช้ได้ ยังไม่จำเป็นต้องเปลี่ยนทันที")
    elif h >= 80:
        keys.append("health_watch"); tips.append("สุขภาพแบตเริ่มอ่อนตัว ลองปรับการใช้งานก่อน แล้วค่อยเทียบราคาเปลี่ยนแบต")
    else:
        keys.append("health_low"); tips.append("สุขภาพแบตต่ำกว่า 80% การเปลี่ยนแบตอาจช่วยให้ใช้งานได้ทั้งวัน")
    if (battery.get("brightness_pct") or 0) >= 70:
        keys.append("brightness"); tips.append("ความสว่างจอค่อนข้างสูง ลองลดลงหรือใช้ปรับอัตโนมัติ")
    if battery.get("background_refresh"):
        keys.append("background"); tips.append("ปิดการรีเฟรชพื้นหลังของแอปที่ไม่ได้ใช้ เพื่อประหยัดแบต")
    if battery.get("low_power") is False:
        keys.append("low_power"); tips.append("เปิดโหมดประหยัดพลังงานตอนออกจากบ้านหรือแบตเหลือน้อย")
    if (battery.get("screen_on_h") or 0) >= 6:
        keys.append("screen_on"); tips.append("เวลาหน้าจอเปิดสูง ลดเวลาปิดจออัตโนมัติและแจ้งเตือนที่ไม่จำเป็น")
    return {"health_pct": h, "keys": keys, "tips_th": tips, "count": len(tips),
            "headline_th": f"สุขภาพแบต ~{h}% · {len(tips)} ข้อที่ปรับได้"}

def repair_or_replace(storage, battery):
    if not storage.get("ok") or not battery.get("ok"):
        raise ValueError("need storage and battery")
    h = battery["health_pct"]
    free = storage["free_gb"]
    if free <= 5 and h >= 85:
        verdict, msg = "cleanup", "พื้นที่เกือบเต็มเป็นปัญหาหลัก สุขภาพแบตยังใช้ได้ ลองเก็บข้อมูลก่อนคิดเปลี่ยนเครื่อง"
    elif free <= 5 and h >= 80:
        verdict, msg = "cleanup_then_watch", "เก็บข้อมูลก่อน แล้วเฝ้าดูแบต ถ้าหมดเร็วขึ้นค่อยเทียบราคาเปลี่ยนแบต"
    elif h < 70:
        verdict, msg = "replace_or_repair", "สุขภาพแบตต่ำมาก เทียบราคาเปลี่ยนแบตกับเครื่องใหม่ก่อนตัดสินใจ"
    elif h < 80:
        verdict, msg = "repair_battery", "การเปลี่ยนแบตอาจคุ้มกว่าซื้อเครื่องใหม่ ถ้าเครื่องอื่นยังใช้ดี"
    else:
        verdict, msg = "watch", "ยังไม่จำเป็นต้องซ่อมหรือเปลี่ยนทันที ปรับการใช้งานและสำรองข้อมูลเป็นประจำ"
    return {"verdict": verdict, "message_th": msg, "health_pct": h, "free_gb": free,
            "battery_min_thb": BATTERY_REPAIR["min"], "battery_max_thb": BATTERY_REPAIR["max"],
            "phone_min_thb": NEW_PHONE["min"], "phone_max_thb": NEW_PHONE["max"],
            "disclaimer_th": PRICE_DISCLAIMER_TH}

def share_card(name_th, storage, plan, battery):
    return {"title_th": f"PhoneRescue — {name_th}",
            "headline_th": plan["headline_th"] if plan else storage["message_th"],
            "hook_th": "มือถือเต็มหรือแบตหมดไว ถ่ายหน้าตั้งค่ารู้เลยว่าต้องทำอะไร",
            "used_gb": storage["used_gb"], "total_gb": storage["total_gb"], "saved_gb": plan["saved_gb"] if plan else 0,
            "health_pct": battery["health_pct"] if battery else None,
            "layout": "rescue_card", "sizes": ["1080x1350", "1080x1920", "1080x1080"],
            "watermark": WATERMARK, "cta_th": "คอมเมนต์ PHONE รับแพ็กฟรี"}

def quota(used_today, want, pro=False):
    if pro:
        return {"allowed": want, "left_after": None, "paywall": False}
    left = max(0, FREE_SCANS_PER_DAY - used_today)
    allowed = min(want, left)
    return {"allowed": allowed, "left_after": left - allowed, "paywall": allowed < want}

def safety_guard(wants_reset=False, backed_up=False):
    if wants_reset and not backed_up:
        return {"level": "stop", "message_th": "อย่ารีเซ็ตเครื่องจนกว่าจะสำรองรูปและแชทแล้ว " + SAFETY_DISCLAIMER_TH}
    if wants_reset:
        return {"level": "warn", "message_th": "รีเซ็ตแล้วของในเครื่องจะหาย ตรวจสำรองอีกครั้ง " + SAFETY_DISCLAIMER_TH}
    return {"level": "ok", "message_th": SAFETY_DISCLAIMER_TH}
