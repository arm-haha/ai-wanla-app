"""PawTalk (แมวหมาพูดได้) — deterministic core engine.
AI only proposes body-language cue tags (from the enum) and may restyle a caption.
Moods, percentages, triage levels, schedules and numbers always come from this file.
Entertainment + care helper, NOT a veterinary diagnosis."""
from datetime import date, timedelta, datetime

MOODS = ["happy", "chill", "hungry", "annoyed", "scared", "playful", "needy"]
# tie-break priority: safety-relevant moods win ties
PRIORITY = ["scared", "annoyed", "hungry", "needy", "playful", "happy", "chill"]
MOOD_TH = {"happy": "แฮปปี้", "chill": "ชิลล์", "hungry": "หิว", "annoyed": "หงุดหงิด",
           "scared": "กลัว/เครียด", "playful": "อยากเล่น", "needy": "อยากให้สนใจ"}
MOOD_EMOJI = {"happy": "😸", "chill": "😌", "hungry": "🍗", "annoyed": "😾",
              "scared": "🙀", "playful": "🧶", "needy": "🥺"}
VIBE_W = {"happy": 1.0, "chill": 1.0, "playful": 1.0, "needy": 0.5, "hungry": 0.5, "annoyed": 0.0, "scared": 0.0}

CUES = {
    "cat": {
        "ears_forward": {"happy": 1, "playful": 2, "chill": 1},
        "ears_flat": {"scared": 3, "annoyed": 2},
        "ears_sideways": {"annoyed": 2},
        "slow_blink": {"chill": 3, "happy": 2},
        "pupils_wide": {"scared": 2, "playful": 2},
        "tail_up": {"happy": 3, "needy": 1},
        "tail_puffed": {"scared": 3},
        "tail_flick": {"annoyed": 3},
        "belly_up": {"chill": 2, "happy": 1},
        "loaf": {"chill": 3},
        "staring_at_bowl": {"hungry": 4},
        "meow_loud": {"hungry": 2, "needy": 2},
        "purr": {"happy": 2, "chill": 2, "needy": 1},
        "hiss": {"scared": 2, "annoyed": 3},
        "kneading": {"happy": 2, "needy": 2},
        "crouch_wiggle": {"playful": 4},
    },
    "dog": {
        "tail_wag_loose": {"happy": 3, "playful": 1},
        "tail_tucked": {"scared": 4},
        "play_bow": {"playful": 4},
        "ears_back": {"scared": 2, "needy": 1},
        "whale_eye": {"scared": 2, "annoyed": 2},
        "yawn_lip_lick": {"scared": 1, "annoyed": 1},
        "belly_up": {"chill": 2, "needy": 2},
        "staring_at_food": {"hungry": 4},
        "whine": {"needy": 3, "hungry": 1},
        "growl": {"annoyed": 4},
        "zoomies": {"playful": 3, "happy": 2},
        "lying_relaxed": {"chill": 4},
        "bringing_toy": {"playful": 3, "needy": 2},
        "bark_at_door": {"needy": 2, "annoyed": 1},
    },
}
CUE_TH = {
    "ears_forward": "หูตั้งไปข้างหน้า", "ears_flat": "หูแบนลู่", "ears_sideways": "หูกางข้าง", "slow_blink": "กะพริบตาช้า",
    "pupils_wide": "รูม่านตาขยาย", "tail_up": "หางชี้ตรง", "tail_puffed": "หางพอง", "tail_flick": "หางสะบัด",
    "belly_up": "นอนหงายโชว์พุง", "loaf": "นั่งท่าขนมปัง", "staring_at_bowl": "จ้องชามข้าว", "meow_loud": "ร้องเสียงดัง",
    "purr": "ครางครืดๆ", "hiss": "ขู่ฟ่อ", "kneading": "นวดแป้ง", "crouch_wiggle": "หมอบส่ายก้น",
    "tail_wag_loose": "ส่ายหางหลวมๆ", "tail_tucked": "หางซุกขา", "play_bow": "ก้มหน้ายกก้น", "ears_back": "หูพับหลัง",
    "whale_eye": "เหลือบตาเห็นตาขาว", "yawn_lip_lick": "หาว/เลียปาก", "staring_at_food": "จ้องอาหาร", "whine": "ครางหงิงๆ",
    "growl": "คำราม", "zoomies": "วิ่งรอบบ้าน", "lying_relaxed": "นอนสบาย", "bringing_toy": "คาบของเล่นมาให้", "bark_at_door": "เห่าที่ประตู",
}
MEAL_BONUS = 2          # hungry bonus when <= 60 min before a meal time
MEAL_WINDOW_MIN = 60


def _alloc_pct(points):
    """Largest-remainder rounding so percentages sum to exactly 100. Ties: PRIORITY order."""
    total = sum(points.values())
    if total == 0:
        return {}
    raw = {m: points[m] * 100 / total for m in points}
    base = {m: int(raw[m]) for m in raw}
    left = 100 - sum(base.values())
    order = sorted(raw, key=lambda m: (-(raw[m] - base[m]), PRIORITY.index(m)))
    for m in order[:left]:
        base[m] += 1
    return base


def minutes_to_next_meal(at_hhmm, meal_times):
    h, m = map(int, at_hhmm.split(":")); now = h * 60 + m
    diffs = []
    for t in meal_times:
        th, tm = map(int, t.split(":")); d = (th * 60 + tm - now) % 1440
        diffs.append(d)
    return min(diffs) if diffs else None


def read_mood(species, cues, at_hhmm=None, meal_times=()):
    table = CUES[species]
    bad = [c for c in cues if c not in table]
    if bad:
        raise ValueError(f"unknown cues for {species}: {bad}")
    cues = [c for c in table if c in set(cues)]   # canonical order, dedupe
    pts = {m: 0 for m in MOODS}
    for c in cues:
        for m, w in table[c].items():
            pts[m] += w
    meal_min = minutes_to_next_meal(at_hhmm, meal_times) if at_hhmm and meal_times else None
    meal_bonus = meal_min is not None and meal_min <= MEAL_WINDOW_MIN
    if meal_bonus:
        pts["hungry"] += MEAL_BONUS
    pts = {m: p for m, p in pts.items() if p > 0}
    pct = _alloc_pct(pts)
    moods = sorted(pct, key=lambda m: (-pts[m], PRIORITY.index(m)))
    total = sum(pts.values())
    vibe = round(100 * sum(pts[m] * VIBE_W[m] for m in pts) / total) if total else 50
    top = moods[0] if moods else "chill"
    return {
        "species": species, "cues": cues, "meal_bonus": meal_bonus, "minutes_to_meal": meal_min,
        "moods": [{"mood": m, "points": pts[m], "pct": pct[m], "label_th": MOOD_TH[m], "emoji": MOOD_EMOJI[m]} for m in moods],
        "top_mood": top, "vibe_score": vibe,
        "vibe_label": "ฟินมาก" if vibe >= 80 else "โอเค" if vibe >= 50 else "ระวังนะ",
        "safety_hint": "ให้พื้นที่ อย่าเพิ่งอุ้ม/ลูบ" if top in ("scared", "annoyed") else None,
    }


PERSONAS = ["boss", "drama", "sweet"]
PERSONA_TH = {"boss": "เจ้านาย", "drama": "ดราม่าควีน", "sweet": "ขี้อ้อน"}
BUBBLES = {
    "hungry": {"boss": ["ทาสสส อีก {soon} นาทีข้าวต้องมา ช้า 1 วิหักเงินเดือน", "ชามว่างคือการดูหมิ่นข้า", "เติมข้าวเดี๋ยวนี้ แล้วจะยกโทษให้ครึ่งนึง"],
               "drama": ["ไม่ได้กินมา 300 ปีแล้ว…จะเป็นลมแล้วนะ{owner}", "ชามว่าง…เหมือนหัวใจข้าตอนนี้", "ถ้าข้าหิวตาย ให้สลักป้ายว่า 'เพราะทาสลืม'"],
               "sweet": ["{owner}ขา หนูหิวนิดนึงงง", "ข้าวมาเมื่อไหร่ หนูจะหอมแก้มให้", "หนูนั่งรอตรงนี้นะ ไม่ไปไหนเลย"]},
    "annoyed": {"boss": ["อย่าแตะ ข้ากำลังประชุม", "อีกครั้งเดียว ข่วนนะ", "ใครอนุญาตให้ย้ายที่นอนข้า"],
                "drama": ["ทำไมโลกนี้ไม่มีใครเข้าใจข้า", "พอเถอะ ข้าเหนื่อยกับมนุษย์", "นี่คือวันที่แย่ที่สุดในชีวิตแมว"],
                "sweet": ["ขอเวลาส่วนตัวแป๊บนะ เดี๋ยวกลับมารัก", "ตอนนี้งอนอยู่ ง้อด้วยขนมได้", "อย่าเพิ่งจับนะ ใจยังไม่พร้อม"]},
    "scared": {"boss": ["เสียงอะไร ทาสไปตรวจดูซิ", "ข้าไม่ได้กลัว แค่ถอยไปวางแผน", "ปกป้องข้าด้วย นี่คือคำสั่ง"],
               "drama": ["นี่คือจุดจบแล้วใช่ไหม", "ข้าเห็นผี…ไม่ใช่ เห็นเครื่องดูดฝุ่น", "อย่าทิ้งข้าไว้คนเดียวนะ"],
               "sweet": ["หนูกลัวว อยู่ใกล้ๆ หนูหน่อย", "ขอซุกตรงนี้ได้ไหม", "{owner}อย่าไปไหนนะ"]},
    "needy": {"boss": ["วางโทรศัพท์ แล้วมองข้า", "ถึงเวลาลูบหัวข้าแล้ว", "ข้าอนุญาตให้เจ้ากอดได้ 3 วินาที"],
              "drama": ["ไม่มีใครรักข้าเลยใช่ไหม", "เจ้าเล่นมือถือมากกว่าเล่นกับข้า", "ข้าจะนั่งทับคีย์บอร์ดจนกว่าเจ้าจะสนใจ"],
              "sweet": ["รักนะ รักที่สุดเลย", "กอดหน่อยสิ", "อยู่กับหนูทั้งวันได้ไหม"]},
    "playful": {"boss": ["ไม้ตกแมวอยู่ไหน ข้าสั่งให้เล่น", "วันนี้ข้าจะล่า…ถุงเท้าเจ้า", "พร้อมแล้ว โยนมาเลย"],
                "drama": ["ถ้าไม่เล่นกับข้า ข้าจะพังแจกัน", "ชีวิตนี้ขาดการเล่นไม่ได้", "ข้าคือนักล่าผู้ยิ่งใหญ่…ของจุดเลเซอร์"],
                "sweet": ["เล่นกันน้าา", "หนูเอาของเล่นมาให้แล้ว", "วิ่งไล่หนูหน่อย ฮิ้ววว"]},
    "happy": {"boss": ["วันนี้เจ้าทำงานดี ข้าพอใจ", "บ้านนี้ผ่านการประเมิน", "ข้าจะขึ้นเงินเดือนให้ เป็นขนม"],
              "drama": ["นี่คือวันที่ดีที่สุดในชีวิต!", "ข้ารักโลกใบนี้ (แค่วันนี้)", "ความสุขล้นจนต้องกลิ้งพื้น"],
              "sweet": ["มีความสุขจังเลย", "อยู่กับ{owner}แล้วอุ่นใจ", "วันนี้ดีมากๆ เลยน้า"]},
    "chill": {"boss": ["อย่ารบกวน ข้ากำลังพักผ่อนระดับ CEO", "งีบที่ 7 ของวัน", "ห้องนี้อุณหภูมิผ่าน"],
              "drama": ["ปล่อยวางแล้ว…ทุกอย่าง", "ขอนอนต่อ 12 ชั่วโมง", "โลกจะแตกก็ช่าง ขอนอนก่อน"],
              "sweet": ["ง่วงจัง นอนด้วยกันไหม", "สบายจังเลยตรงนี้", "อุ่นๆ หลับปุ๋ย"]},
}


def bubble_index(pet_id, on_iso, mood, persona):
    """Deterministic pick: sum of UTF-16 code units of pet_id|date|mood|persona, mod 3 (same in JS)."""
    key = f"{pet_id}|{on_iso}|{mood}|{persona}"
    return sum(ord(ch) for ch in key) % 3


def thought_bubble(pet, mood_result, persona, owner_name, on_iso):
    if persona not in PERSONAS:
        raise ValueError(persona)
    mood = mood_result["top_mood"]
    i = bubble_index(pet["id"], on_iso, mood, persona)
    soon = mood_result.get("minutes_to_meal")
    text = BUBBLES[mood][persona][i].format(owner=owner_name, pet=pet["name"], soon=soon if soon is not None else "ไม่กี่")
    return {"pet_id": pet["id"], "mood": mood, "persona": persona, "persona_th": PERSONA_TH[persona],
            "template_index": i, "text_th": text, "emoji": MOOD_EMOJI[mood],
            "badge_th": f"{MOOD_EMOJI[mood]} {MOOD_TH[mood]} {mood_result['moods'][0]['pct'] if mood_result['moods'] else 0}%",
            "disclaimer_th": "แปลเพื่อความบันเทิงจากภาษากาย ไม่ใช่การอ่านใจจริง"}


def duet(pet_a, mood_a, pet_b, mood_b, persona_a, persona_b, owner, on_iso):
    """Two pets 'chatting': A speaks, B replies, A closes with a 2nd template (index+1)."""
    a1 = thought_bubble(pet_a, mood_a, persona_a, owner, on_iso)
    b1 = thought_bubble(pet_b, mood_b, persona_b, owner, on_iso)
    j = (a1["template_index"] + 1) % 3
    soon = mood_a.get("minutes_to_meal")
    a2 = BUBBLES[mood_a["top_mood"]][persona_a][j].format(owner=owner, pet=pet_a["name"], soon=soon if soon is not None else "ไม่กี่")
    return [{"pet_id": pet_a["id"], "text_th": a1["text_th"]}, {"pet_id": pet_b["id"], "text_th": b1["text_th"]},
            {"pet_id": pet_a["id"], "text_th": a2}]


# ---------- Care schedule ----------
DUE_SOON_DAYS = 3

def care_status(item, on):
    last = date.fromisoformat(item["last_done"])
    due = last + timedelta(days=item["interval_days"])
    left = (due - on).days
    status = "overdue" if left < 0 else "due_soon" if left <= DUE_SOON_DAYS else "ok"
    return {"task_id": item["id"], "pet_id": item["pet_id"], "kind": item["kind"], "label_th": item["label_th"],
            "due_on": due.isoformat(), "days_left": left, "status": status}


def care_board(items, on):
    rows = [care_status(i, on) for i in items]
    rank = {"overdue": 0, "due_soon": 1, "ok": 2}
    return sorted(rows, key=lambda r: (rank[r["status"]], r["days_left"], r["task_id"]))


def next_meal(at_hhmm, meal_times):
    m = minutes_to_next_meal(at_hhmm, meal_times)
    h, mm = map(int, at_hhmm.split(":")); t = (h * 60 + mm + m) % 1440
    return {"at": f"{t // 60:02d}:{t % 60:02d}", "in_min": m}


# ---------- Health check (triage, not diagnosis) ----------
SYMPTOMS = {
    # id: (level, species or None for both, label_th)
    "straining_no_urine": ("emergency", "cat", "เบ่งฉี่แต่ไม่ออก/ออกน้อย"),
    "open_mouth_breathing": ("emergency", "cat", "หายใจอ้าปาก"),
    "hard_breathing": ("emergency", None, "หายใจลำบาก/หอบผิดปกติ"),
    "seizure": ("emergency", None, "ชัก"),
    "ate_toxic": ("emergency", None, "กินของมีพิษ (เช่น ลิลลี่, ช็อกโกแลต, องุ่น, ยาคน)"),
    "collapse": ("emergency", None, "ทรุด/ลุกไม่ขึ้น"),
    "bloated_belly_retching": ("emergency", "dog", "ท้องอืดแน่น + พยายามอาเจียนแต่ไม่ออก"),
    "blood_vomit_stool": ("soon", None, "มีเลือดในอาเจียน/อุจจาระ"),
    "not_eating_24h": ("soon", None, "ไม่กินข้าวเกิน 24 ชม."),
    "vomit_3plus": ("soon", None, "อาเจียน 3 ครั้งขึ้นไปใน 24 ชม."),
    "limping": ("soon", None, "เดินกะเผลก"),
    "eye_discharge_squint": ("soon", None, "ตาแฉะ/หรี่ตาข้างเดียว"),
    "lethargic_24h": ("soon", None, "ซึมผิดปกติเกิน 24 ชม."),
    "vomit_once": ("watch", None, "อาเจียน 1 ครั้งแล้วปกติ"),
    "hairball": ("watch", "cat", "ขย้อนก้อนขน"),
    "sneeze_mild": ("watch", None, "จามเล็กน้อย กินได้ปกติ"),
    "scratching_more": ("watch", None, "เกาบ่อยขึ้น"),
    "soft_stool_once": ("watch", None, "ถ่ายเหลว 1 ครั้ง"),
}
LEVEL_RANK = {"emergency": 0, "soon": 1, "watch": 2, "ok": 3}
LEVEL_TH = {"emergency": "🚨 ไปโรงพยาบาลสัตว์ทันที", "soon": "🟠 พบสัตวแพทย์ภายใน 24 ชม.",
            "watch": "🟢 เฝ้าดูที่บ้าน 24–48 ชม.", "ok": "✅ ยังไม่พบสัญญาณผิดปกติ"}
ESCALATE_IF_KITTEN_PUPPY = True   # 'watch' -> 'soon' for age < 0.5y


def health_check(pet, symptom_ids):
    for s in symptom_ids:
        if s not in SYMPTOMS:
            raise ValueError(s)
        sp = SYMPTOMS[s][1]
        if sp and sp != pet["species"]:
            raise ValueError(f"{s} is {sp}-only")
    ids = [s for s in SYMPTOMS if s in set(symptom_ids)]
    levels = [SYMPTOMS[s][0] for s in ids]
    level = min(levels, key=lambda l: LEVEL_RANK[l]) if levels else "ok"
    escalated = False
    if level == "watch" and ESCALATE_IF_KITTEN_PUPPY and pet["age_years"] < 0.5:
        level, escalated = "soon", True
    if "watch" in levels and len([l for l in levels if l == "watch"]) >= 3 and level == "watch":
        level, escalated = "soon", True
    return {"pet_id": pet["id"], "symptoms": [{"id": s, "level": SYMPTOMS[s][0], "label_th": SYMPTOMS[s][2]} for s in ids],
            "level": level, "level_th": LEVEL_TH[level], "escalated": escalated,
            "show_vet_finder": level in ("emergency", "soon"),
            "disclaimer_th": "นี่คือการคัดกรองเบื้องต้น ไม่ใช่การวินิจฉัย หากไม่แน่ใจให้ปรึกษาสัตวแพทย์"}


# ---------- Food calculator ----------
FACTOR = {("cat", "neutered"): 1.2, ("cat", "intact"): 1.4, ("cat", "young"): 2.5, ("cat", "weight_loss"): 0.8,
          ("dog", "neutered"): 1.6, ("dog", "intact"): 1.8, ("dog", "young"): 2.5, ("dog", "weight_loss"): 1.0}


def food_plan(pet, kcal_per_100g, meals_per_day):
    stage = "young" if pet["age_years"] < 1 else pet.get("goal") or ("neutered" if pet["neutered"] else "intact")
    rer = 70 * pet["weight_kg"] ** 0.75
    kcal = round(rer * FACTOR[(pet["species"], stage)])
    grams = round(kcal * 100 / kcal_per_100g)
    per_meal = round(grams / meals_per_day)
    return {"pet_id": pet["id"], "stage": stage, "rer_kcal": round(rer), "factor": FACTOR[(pet["species"], stage)],
            "kcal_per_day": kcal, "grams_per_day": grams, "meals_per_day": meals_per_day, "grams_per_meal": per_meal,
            "note_th": "ค่าประมาณจากสูตร RER = 70 × น้ำหนัก^0.75 ตรวจกับฉลากอาหารและสัตวแพทย์"}


# ---------- Human age ----------
DOG_STEP = {"small": 4, "medium": 5, "large": 6}

def human_age(pet):
    y = pet["age_years"]
    if y <= 1:
        h = round(15 * y)
    elif y <= 2:
        h = round(15 + 9 * (y - 1))
    else:
        step = 4 if pet["species"] == "cat" else DOG_STEP[pet.get("size", "medium")]
        h = round(24 + step * (y - 2))
    return {"pet_id": pet["id"], "pet_years": y, "human_years": h,
            "note_th": "ค่าประมาณแบบตารางทั่วไป ไม่ใช่ค่าทางการแพทย์"}


# ---------- Diary / streak / XP / Wrapped ----------
XP = {"snap": 10, "care_done": 15, "health_check": 5}

def streak(days_iso, on):
    s = set(days_iso); n = 0; d = on
    while d.isoformat() in s:
        n += 1; d -= timedelta(days=1)
    return n


def level_from_xp(xp):
    lvl = 1; need = 50
    while xp >= need:
        xp -= need; lvl += 1; need += 50
    return lvl


def progress(log, on):
    xp = sum(XP[e["kind"]] for e in log)
    snap_days = sorted({e["on"] for e in log if e["kind"] == "snap"})
    return {"xp": xp, "level": level_from_xp(xp), "streak_days": streak(snap_days, on)}


def wrapped(log, pet_id, month):
    snaps = [e for e in log if e["kind"] == "snap" and e["pet_id"] == pet_id and e["on"].startswith(month)]
    counts = {}
    for e in snaps:
        counts[e["mood"]] = counts.get(e["mood"], 0) + 1
    top = sorted(counts, key=lambda m: (-counts[m], PRIORITY.index(m)))[0] if counts else None
    wd = {}
    for e in snaps:
        if e["mood"] in ("annoyed", "scared"):
            k = datetime.fromisoformat(e["on"]).strftime("%a"); wd[k] = wd.get(k, 0) + 1
    grumpy_day = sorted(wd, key=lambda k: (-wd[k], k))[0] if wd else None
    happy = sum(counts.get(m, 0) for m in ("happy", "chill", "playful"))
    return {"pet_id": pet_id, "month": month, "snaps": len(snaps), "mood_counts": counts, "top_mood": top,
            "happy_pct": round(100 * happy / len(snaps)) if snaps else 0, "grumpiest_weekday": grumpy_day,
            "care_done": len([e for e in log if e["kind"] == "care_done" and e["pet_id"] == pet_id and e["on"].startswith(month)])}
