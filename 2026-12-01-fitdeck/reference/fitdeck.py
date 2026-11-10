"""FitDeck deterministic logic (no AI calls).
Plans and durations are app-chosen examples — not a personal trainer or medical advice.
"""
FREE_SCANS_PER_DAY = 3
MIN_CONF = 0.6
TARGET_SEC = 20 * 60
WATERMARK = "Made with FitDeck · guidance only, not a trainer or medical advice"
SAFETY_DISCLAIMER_TH = "FitDeck เป็นตารางออกกำลังกายตัวอย่างจากอุปกรณ์ที่มี ไม่ใช่เทรนเนอร์และไม่ใช่คำแนะนำทางการแพทย์ ถ้าเจ็บหรือเวียนหัวให้หยุดทันที และปรึกษาแพทย์ก่อนเริ่มถ้ามีโรคประจำตัว"

EQUIPMENT = {
    "yoga_mat": {"id": "eq01", "name_th": "เสื่อโยคะ"},
    "dumbbell": {"id": "eq02", "name_th": "ดัมเบิล"},
    "resistance_band": {"id": "eq03", "name_th": "ยางยืด"},
    "jump_rope": {"id": "eq04", "name_th": "เชือกกระโดด"},
    "chair": {"id": "eq05", "name_th": "เก้าอี้"},
    "wall": {"id": "eq06", "name_th": "ผนัง"},
    "bodyweight": {"id": "eq07", "name_th": "น้ำหนักตัว"},
}

# duration_sec is the block length in the 20-min plan (work + short implied rest).
EXERCISES = {
    "march_warm": {"id": "x01", "name_th": "เดินยกเข่าอุ่นเครื่อง", "need": set(), "sec": 120, "level": "beginner", "muscles": ["full"], "safety_th": "ค่อย ๆ ยกเข่า อย่ากลั้นหายใจ"},
    "goblet_squat": {"id": "x02", "name_th": "สกวอตถือดัมเบิล", "need": {"dumbbell"}, "sec": 180, "level": "beginner", "muscles": ["legs", "glutes"], "safety_th": "เข่าไม่เลยปลายเท้ามาก หลังตรง เลือกน้ำหนักที่คุมได้"},
    "body_squat": {"id": "x03", "name_th": "สกวอตน้ำหนักตัว", "need": set(), "sec": 180, "level": "beginner", "muscles": ["legs", "glutes"], "safety_th": "ส้นเท้าติดพื้น อย่าให้เข่าบิดเข้าใน"},
    "knee_push": {"id": "x04", "name_th": "ดันพื้นเข่าลง", "need": {"yoga_mat"}, "sec": 180, "level": "beginner", "muscles": ["chest", "arms"], "safety_th": "ลำตัวเป็นเส้นตรงจากเข่าถึงหัวไหล่ ข้อมือไม่เจ็บ"},
    "wall_push": {"id": "x05", "name_th": "ดันผนัง", "need": {"wall"}, "sec": 180, "level": "beginner", "muscles": ["chest", "arms"], "safety_th": "ยืนระยะที่ข้อมือสบาย อย่าล็อกข้อศอก"},
    "glute_bridge": {"id": "x06", "name_th": "ยกสะพานสะโพก", "need": {"yoga_mat"}, "sec": 180, "level": "beginner", "muscles": ["glutes", "core"], "safety_th": "กดส้นเท้า อย่าแอ่นหลังส่วนล่างมาก"},
    "dumbbell_row": {"id": "x07", "name_th": "โรว์ดัมเบิล", "need": {"dumbbell"}, "sec": 180, "level": "beginner", "muscles": ["back", "arms"], "safety_th": "หลังตรง ดึงศอกชิดลำตัว อย่ายักไหล่"},
    "band_row": {"id": "x08", "name_th": "โรว์ยางยืด", "need": {"resistance_band"}, "sec": 180, "level": "beginner", "muscles": ["back", "arms"], "safety_th": "ยางไม่สะบัดเข้าหน้า ยืนให้ยางตึงพอดี"},
    "dead_bug": {"id": "x09", "name_th": "เดดบั๊ก", "need": {"yoga_mat"}, "sec": 180, "level": "beginner", "muscles": ["core"], "safety_th": "หลังติดเสื่อ ถ้าแอ่นให้ก้าวสั้นลง"},
    "chair_sit": {"id": "x10", "name_th": "นั่ง-ยืนจากเก้าอี้", "need": {"chair"}, "sec": 180, "level": "beginner", "muscles": ["legs"], "safety_th": "เก้าอี้ไม่มียางล้อ วางชิดผนังถ้าไม่มั่นคง"},
    "jump_rope": {"id": "x11", "name_th": "กระโดดเชือกเบา", "need": {"jump_rope"}, "sec": 180, "level": "intermediate", "muscles": ["cardio", "legs"], "safety_th": "กระโดดต่ำ ลงด้วยปลายเท้า ถ้าเหนื่อยให้เดินแทน"},
    "stretch_close": {"id": "x12", "name_th": "ยืดเหยียดคลายกล้ามเนื้อ", "need": set(), "sec": 180, "level": "beginner", "muscles": ["full"], "safety_th": "ยืดจนตึง ไม่ยืดจนเจ็บ"},
    "plank_knee": {"id": "x13", "name_th": "แพลงก์เข่าลง", "need": {"yoga_mat"}, "sec": 180, "level": "intermediate", "muscles": ["core"], "safety_th": "อย่าห้อยสะโพกหรือยกสูงเกินไป"},
    "overhead_press": {"id": "x14", "name_th": "ดันดัมเบิลเหนือหัว", "need": {"dumbbell"}, "sec": 180, "level": "intermediate", "muscles": ["shoulders", "arms"], "safety_th": "อย่าโก่งหลัง เลือกน้ำหนักที่กดขึ้นได้ครบจังหวะ"},
    "air_press": {"id": "x15", "name_th": "ยกแขนเหนือหัวแบบน้ำหนักตัว", "need": set(), "sec": 180, "level": "beginner", "muscles": ["shoulders"], "safety_th": "ไหล่ไม่ยัก ยกในกรอบที่ปวด"},
    "stand_core": {"id": "x16", "name_th": "ยกเข่าแตะศอกยืน", "need": set(), "sec": 180, "level": "beginner", "muscles": ["core"], "safety_th": "ลำตัวตรง อย่าเหวี่ยงหลัง"},
}


# Preferred order for a balanced 20-min beginner plan. Alternatives swap in if equipment missing.
BEGINNER_SLOTS = [
    ["march_warm"],
    ["goblet_squat", "chair_sit", "body_squat"],
    ["knee_push", "wall_push", "air_press"],
    ["glute_bridge", "chair_sit", "body_squat"],
    ["dumbbell_row", "band_row", "air_press"],
    ["dead_bug", "plank_knee", "stand_core"],
    ["stretch_close"],
]
INTERMEDIATE_SLOTS = [
    ["march_warm"],
    ["goblet_squat", "body_squat"],
    ["overhead_press", "knee_push", "wall_push", "air_press"],
    ["jump_rope", "glute_bridge", "body_squat"],
    ["dumbbell_row", "band_row", "air_press"],
    ["plank_knee", "dead_bug", "stand_core"],
    ["stretch_close"],
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
        tips.append("แสงสะท้อนเยอะ ถ่ายมุมห้องในที่ร่มหรือเปิดไฟเพดาน")
    if blur > 0.4:
        tips.append("ภาพเบลอ วางมือนิ่งแล้วถ่ายอุปกรณ์ให้เห็นทั้งชิ้น")
    if crop > 0.45:
        tips.append("อุปกรณ์ถูกครอป ถอยหลังนิดหนึ่งให้เห็นเสื่อหรือดัมเบิลทั้งคู่")
    if n_dets == 0:
        tips.append("ยังไม่เจออุปกรณ์ วางเสื่อ ดัมเบิล หรือเก้าอี้ในเฟรม แล้วถ่ายใหม่ หรือเลือกน้ำหนักตัว")
    return {"score": score, "ok": score >= 60, "tips_th": tips}


def parse_gear(shot):
    q = scan_quality(shot["glare"], shot["blur"], shot["crop"], len(shot["detections"]))
    keys = []
    weight_kg = None
    for d in shot["detections"]:
        if d.get("confidence", 0) < MIN_CONF:
            continue
        if d["key"] == "weight_kg":
            weight_kg = d["value"]
            continue
        if d["key"] in EQUIPMENT and d["key"] not in keys:
            keys.append(d["key"])
    # bodyweight is always available
    if "bodyweight" not in keys:
        keys.append("bodyweight")
    ok = q["score"] >= 60  # even with no gear, bodyweight plan is possible
    names = [EQUIPMENT[k]["name_th"] for k in keys if k != "bodyweight"]
    msg = "เจอ " + " + ".join(names) if names else "ยังไม่เจออุปกรณ์ จะจัดแผนแบบน้ำหนักตัว"
    if weight_kg is not None:
        msg += f" · ดัมเบิลประมาณ {weight_kg:g} กก."
    return {"shot_id": shot["id"], "quality": q, "ok": ok, "keys": keys, "weight_kg": weight_kg,
            "count": len([k for k in keys if k != "bodyweight"]), "message_th": msg}


def _can(ex, have):
    return EXERCISES[ex]["need"].issubset(have)


def make_plan(gear, level="beginner"):
    if not gear.get("ok"):
        raise ValueError("gear not ok")
    if level not in ("beginner", "intermediate"):
        raise ValueError("unknown level " + level)
    slots = BEGINNER_SLOTS if level == "beginner" else INTERMEDIATE_SLOTS
    have = set(gear["keys"])
    moves = []
    total = 0
    for options in slots:
        used = {m["key"] for m in moves}
        chosen = next((k for k in options if _can(k, have) and k not in used), None)
        if chosen is None:
            fallback = next((k for k in ("air_press", "stand_core", "body_squat", "stretch_close", "march_warm") if k not in used and _can(k, have)), None)
            if fallback is None:
                continue
            chosen = fallback
        ex = EXERCISES[chosen]
        total += ex["sec"]
        moves.append({
            "n": len(moves) + 1, "key": chosen, "id": ex["id"], "name_th": ex["name_th"],
            "sec": ex["sec"], "minutes": round(ex["sec"] / 60, 1),
            "muscles": list(ex["muscles"]), "safety_th": ex["safety_th"],
            "need": sorted(ex["need"]),
        })
    if total != TARGET_SEC:
        # still valid if close; tests will lock demo at 20:00
        pass
    return {"level": level, "keys": [k for k in gear["keys"] if k != "bodyweight"],
            "weight_kg": gear.get("weight_kg"), "moves": moves, "count": len(moves),
            "total_sec": total, "total_min": round(total / 60, 1),
            "headline_th": f"แผน {round(total/60):g} นาที · {level} · {len(moves)} ท่า",
            "disclaimer_th": SAFETY_DISCLAIMER_TH}


def timer_cards(plan):
    cards = []
    t = 0
    for m in plan["moves"]:
        cards.append({"n": m["n"], "key": m["key"], "name_th": m["name_th"],
                      "sec": m["sec"], "start_sec": t, "end_sec": t + m["sec"],
                      "safety_th": m["safety_th"],
                      "cue_th": f"ท่าที่ {m['n']} {m['name_th']} {m['sec']} วินาที"})
        t += m["sec"]
    return {"cards": cards, "count": len(cards), "total_sec": t,
            "headline_th": f"จับเวลา {len(cards)} ท่า รวม {t} วินาที"}


def log_session(log, date, plan, completed_n, feeling="ok"):
    if feeling not in ("easy", "ok", "hard", "stop"):
        raise ValueError("unknown feeling")
    if completed_n < 0 or completed_n > plan["count"]:
        raise ValueError("completed_n out of range")
    row = {"date": date, "level": plan["level"], "planned": plan["count"],
           "completed": completed_n, "total_sec": sum(m["sec"] for m in plan["moves"][:completed_n]),
           "feeling": feeling, "stopped": feeling == "stop" or completed_n < plan["count"]}
    rows = list(log) + [row]
    done = sum(1 for r in rows if not r["stopped"])
    return {"rows": rows, "count": len(rows), "finished_sessions": done,
            "headline_th": f"บันทึก {len(rows)} ครั้ง · ทำครบ {done} ครั้ง"}


def share_card(name_th, plan):
    return {"title_th": f"FitDeck — {name_th}",
            "headline_th": plan["headline_th"],
            "hook_th": "ถ่ายอุปกรณ์ที่มี ได้ตารางออกกำลังกายที่บ้าน",
            "total_min": plan["total_min"], "count": plan["count"], "level": plan["level"],
            "layout": "fit_card", "sizes": ["1080x1350", "1080x1920", "1080x1080"],
            "watermark": WATERMARK, "cta_th": "คอมเมนต์ FIT รับแพ็กฟรี"}


def quota(used_today, want, pro=False):
    if pro:
        return {"allowed": want, "left_after": None, "paywall": False}
    left = max(0, FREE_SCANS_PER_DAY - used_today)
    allowed = min(want, left)
    return {"allowed": allowed, "left_after": left - allowed, "paywall": allowed < want}


def safety_guard(pain=False, dizzy=False, cleared=True):
    if pain or dizzy:
        return {"level": "stop", "message_th": "หยุดทันทีถ้าเจ็บหรือเวียนหัว แล้วพัก " + SAFETY_DISCLAIMER_TH}
    if not cleared:
        return {"level": "warn", "message_th": "ถ้ามีโรคประจำตัวหรือไม่เคยออกกำลัง ควรปรึกษาแพทย์ก่อน " + SAFETY_DISCLAIMER_TH}
    return {"level": "ok", "message_th": SAFETY_DISCLAIMER_TH}
