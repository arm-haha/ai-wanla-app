"""GiftGenie deterministic logic (no AI calls). Prices and ideas are app-chosen examples — not a shop or a real voucher."""
import datetime as _dt

RELS = ["partner", "parent", "friend", "sibling", "colleague", "kid"]
AGE_BANDS = ["0-12", "13-17", "18-24", "25-34", "35-49", "50+"]
VIBES = ["cozy", "practical", "playful", "luxe", "sporty", "creative"]
HOBBIES = ["cafe", "fashion", "cooking", "books", "plants", "games", "travel", "music", "fitness", "home"]
OCCASIONS = ["birthday", "anniversary", "thank_you", "housewarming", "new_job", "condolence", "just_because"]
TONES = ["sweet", "funny", "formal", "short"]
MINOR_BANDS = {"0-12", "13-17"}
FREE_RUNS_PER_DAY = 3
WATERMARK = "Made with GiftGenie · ideas only, not a shop"
SAFETY_DISCLAIMER_TH = "GiftGenie เป็นไอเดียของขวัญเบื้องต้น ไม่ใช่ร้านค้าและไม่ใช่คูปองจริง ราคาเป็นช่วงประมาณ ตรวจอายุผู้รับก่อนเลือกของ และห้ามแนะนำของผิดกฎหมาย"
PRICE_DISCLAIMER_TH = "ราคาเป็นช่วงประมาณการที่ตั้งเอง ไม่ใช่ราคาร้านจริง"

GIFTS = {
    "g01": {"name_th": "เสื้อโอเวอร์ไซส์ FictoSoft", "name_en": "FictoSoft oversized shirt", "min": 690, "max": 1290, "mid": 890,
            "rel": ["partner", "friend", "sibling"], "age": ["18-24", "25-34", "35-49"], "vibe": ["cozy"], "hobby": ["fashion"],
            "occasions": ["birthday", "just_because", "anniversary"], "adult_only": False,
            "why_th": "เข้ากับลุคสบาย ๆ และอยู่ในงบ"},
    "g02": {"name_th": "บัตรของขวัญคาเฟ่ FictoBean 2 ที่", "name_en": "FictoBean cafe card for two", "min": 500, "max": 800, "mid": 650,
            "rel": ["partner", "friend", "colleague"], "age": ["18-24", "25-34", "35-49", "50+"], "vibe": ["cozy"], "hobby": ["cafe"],
            "occasions": ["birthday", "anniversary", "thank_you", "just_because"], "adult_only": False,
            "why_th": "ไปคาเฟ่ด้วยกันได้เลย ไม่ต้องเดาไซส์"},
    "g03": {"name_th": "พวงกุญแจกล้องฟิล์ม FictoClick", "name_en": "FictoClick film-camera keychain", "min": 190, "max": 390, "mid": 290,
            "rel": ["partner", "friend", "sibling", "kid"], "age": ["13-17", "18-24", "25-34"], "vibe": ["playful", "creative"], "hobby": ["cafe", "travel"],
            "occasions": ["birthday", "just_because", "thank_you"], "adult_only": False,
            "why_th": "ของจิ๋วน่ารัก ใช้งบเหลือจากของชิ้นหลัก"},
    "g04": {"name_th": "ชุดเทียนหอม FictoGlow", "name_en": "FictoGlow candle set", "min": 350, "max": 690, "mid": 490,
            "rel": ["partner", "friend", "parent"], "age": ["18-24", "25-34", "35-49", "50+"], "vibe": ["cozy", "luxe"], "hobby": ["home"],
            "occasions": ["birthday", "housewarming", "thank_you"], "adult_only": False,
            "why_th": "เพิ่มบรรยากาศบ้านโดยไม่ต้องเดาไซส์เสื้อผ้า"},
    "g05": {"name_th": "หนังสือภาพคาเฟ่ FictoPages", "name_en": "FictoPages cafe photobook", "min": 320, "max": 520, "mid": 420,
            "rel": ["partner", "friend"], "age": ["18-24", "25-34", "35-49"], "vibe": ["cozy", "creative"], "hobby": ["cafe", "books"],
            "occasions": ["birthday", "just_because"], "adult_only": False,
            "why_th": "เข้าทั้งคาเฟ่และสายหนังสือ"},
    "g06": {"name_th": "กล่องกาแฟดริป FictoBrew", "name_en": "FictoBrew drip box", "min": 390, "max": 690, "mid": 550,
            "rel": ["partner", "friend", "colleague", "parent"], "age": ["18-24", "25-34", "35-49", "50+"], "vibe": ["practical", "cozy"], "hobby": ["cafe", "cooking"],
            "occasions": ["thank_you", "new_job", "birthday"], "adult_only": False,
            "why_th": "ใช้ได้ทุกเช้า ของปฏิบัติที่ได้จริง"},
    "g07": {"name_th": "กระถางต้นไม้เล็ก FictoLeaf", "name_en": "FictoLeaf mini planter", "min": 250, "max": 550, "mid": 390,
            "rel": ["friend", "colleague", "parent"], "age": ["18-24", "25-34", "35-49", "50+"], "vibe": ["practical", "cozy"], "hobby": ["plants", "home"],
            "occasions": ["housewarming", "thank_you", "new_job"], "adult_only": False,
            "why_th": "เหมาะกับบ้านใหม่หรือโต๊ะทำงาน"},
    "g08": {"name_th": "สมุดแพลนเนอร์ FictoPlan", "name_en": "FictoPlan planner", "min": 280, "max": 480, "mid": 350,
            "rel": ["colleague", "friend", "sibling"], "age": ["18-24", "25-34", "35-49"], "vibe": ["practical"], "hobby": ["books"],
            "occasions": ["new_job", "thank_you", "birthday"], "adult_only": False,
            "why_th": "ของใช้จริงสำหรับเริ่มงานใหม่"},
    "g09": {"name_th": "ดัมเบลผ้า FictoFit", "name_en": "FictoFit fabric dumbbells", "min": 450, "max": 890, "mid": 690,
            "rel": ["partner", "friend", "sibling"], "age": ["18-24", "25-34", "35-49"], "vibe": ["sporty", "practical"], "hobby": ["fitness"],
            "occasions": ["birthday", "just_because", "new_job"], "adult_only": False,
            "why_th": "เข้ากับสายออกกำลังกายโดยไม่เทอะทะ"},
    "g10": {"name_th": "หูฟัง FictoBeat", "name_en": "FictoBeat earphones", "min": 790, "max": 1590, "mid": 1190,
            "rel": ["partner", "friend", "sibling"], "age": ["13-17", "18-24", "25-34", "35-49"], "vibe": ["practical", "luxe"], "hobby": ["music", "games", "travel"],
            "occasions": ["birthday", "new_job"], "adult_only": False,
            "why_th": "ของที่ใช้บ่อย ถ้างบครอบคลุม"},
    "g11": {"name_th": "ชุดเครื่องครัวเล็ก FictoPan", "name_en": "FictoPan starter set", "min": 650, "max": 1400, "mid": 990,
            "rel": ["friend", "sibling", "partner"], "age": ["18-24", "25-34", "35-49"], "vibe": ["practical"], "hobby": ["cooking", "home"],
            "occasions": ["housewarming", "birthday"], "adult_only": False,
            "why_th": "เหมาะกับบ้านใหม่สายทำอาหาร"},
    "g12": {"name_th": "กล่องขนม FictoTreat (ไม่มีแอลกอฮอล์)", "name_en": "FictoTreat snack box", "min": 250, "max": 550, "mid": 390,
            "rel": ["colleague", "friend", "parent", "kid", "sibling"], "age": ["0-12", "13-17", "18-24", "25-34", "35-49", "50+"], "vibe": ["playful", "cozy"], "hobby": ["cafe"],
            "occasions": ["thank_you", "birthday", "just_because"], "adult_only": False,
            "why_th": "ของกินแบ่งได้ ใช้ได้ทุกวัย"},
    "g13": {"name_th": "ชุดชงชา FictoTea", "name_en": "FictoTea set", "min": 490, "max": 990, "mid": 750,
            "rel": ["parent", "partner", "friend"], "age": ["35-49", "50+", "25-34"], "vibe": ["cozy", "luxe"], "hobby": ["cafe", "home"],
            "occasions": ["thank_you", "birthday", "anniversary"], "adult_only": False,
            "why_th": "โทนสุภาพ สำหรับผู้ใหญ่หรือคนที่ชอบของบ้าน"},
    "g14": {"name_th": "เกมตั้งโต๊ะ FictoQuest", "name_en": "FictoQuest board game", "min": 590, "max": 1200, "mid": 850,
            "rel": ["friend", "sibling", "partner", "kid"], "age": ["0-12", "13-17", "18-24", "25-34"], "vibe": ["playful"], "hobby": ["games"],
            "occasions": ["birthday", "housewarming", "just_because"], "adult_only": False,
            "why_th": "เล่นด้วยกันได้ทั้งบ้าน"},
    "g15": {"name_th": "ชุดไวน์ FictoVine (21+ เท่านั้น)", "name_en": "FictoVine wine set (21+ only)", "min": 890, "max": 1800, "mid": 1290,
            "rel": ["partner", "friend", "parent"], "age": ["25-34", "35-49", "50+"], "vibe": ["luxe"], "hobby": ["cooking", "home"],
            "occasions": ["anniversary", "thank_you", "housewarming"], "adult_only": True,
            "why_th": "ของพิเศษสำหรับผู้ใหญ่ในโอกาสสำคัญ"},
    "g16": {"name_th": "ตุ๊กตาผ้า FictoBuddy", "name_en": "FictoBuddy plush", "min": 290, "max": 590, "mid": 390,
            "rel": ["kid", "sibling"], "age": ["0-12", "13-17"], "vibe": ["playful", "cozy"], "hobby": ["games"],
            "occasions": ["birthday", "just_because"], "adult_only": False,
            "why_th": "นุ่ม ปลอดภัย สำหรับเด็ก (ไม่มีชิ้นเล็กหลุดง่ายในชุดตัวอย่าง)"},
}

CARD_BANK = {
    "sweet": {
        "birthday": ["สุขสันต์วันเกิดนะ ขอให้ปีนี้มีวันที่สบายใจมากกว่าเดิม", "เกิดมาเพื่อให้คนข้าง ๆ ยิ้มได้ง่าย ๆ — สุขสันต์วันเกิด"],
        "anniversary": ["อีกปีที่ผ่านมาด้วยกัน ขอบคุณที่เป็นบ้านของกันและกัน", "ครบรอบนี้ขอถือมือต่ออีกยาว ๆ"],
        "thank_you": ["ขอบคุณที่อยู่ตรงนี้ ไม่ว่าวันไหนก็ตาม", "ของเล็ก ๆ ชิ้นนี้แทนคำขอบคุณที่พูดไม่หมด"],
        "housewarming": ["ขอให้บ้านใหม่อบอุ่น ปลอดภัย และมีเสียงหัวเราะบ่อย ๆ", "บ้านใหม่นี้ขอให้เป็นที่พักใจทุกวัน"],
        "new_job": ["ขอให้งานใหม่ได้ใช้สิ่งที่ถนัด และเจอคนดี ๆ", "เริ่มงานใหม่วันนี้ เก่งกว่าที่คิดอีกนิดเสมอ"],
        "condolence": ["ขอเป็นกำลังใจให้อย่างเงียบ ๆ นะ", "อยู่ตรงนี้ถ้าต้องการคนฟัง"],
        "just_because": ["ไม่มีเหตุผลพิเศษ นอกจากคิดถึง", "เห็นแล้วอยากให้ยิ้มเลยส่งมา"],
    },
    "funny": {
        "birthday": ["อายุเพิ่ม แต่ความขี้ลืมยังคงที่ สุขสันต์วันเกิด", "วันเกิดนี้ขอให้ของขวัญถูกใจกว่าเค้กที่กินไม่หมด"],
        "anniversary": ["อีกปีแล้วยังไม่หนีกัน ถือว่าเก่งมาก", "ครบรอบนี้ของไม่แพง แต่คำอวยพรแพงขึ้นทุกปี"],
        "thank_you": ["ขอบคุณที่ช่วยไว้ ถ้าไม่ได้ช่วย คงยังนั่งทำอยู่ตอนนี้", "ของชิ้นนี้แลกกับการช่วยงานรอบที่แล้ว — คุ้มทั้งสองฝ่าย"],
        "housewarming": ["บ้านใหม่นี้ขอให้รีโมทอยู่ครบทุกชิ้น", "ขอให้ย้ายเข้าแล้วหาสายชาร์จเจอทุกครั้ง"],
        "new_job": ["งานใหม่นี้ขอให้มีประชุมน้อยกว่ากาแฟ", "ขอให้ล็อกอินวันแรกผ่านตั้งแต่รอบแรก"],
        "condolence": ["ช่วงนี้อยากให้ใจเบาที่สุดเท่าที่จะเป็นไปได้", "ไม่ต้องตอบอะไรก็ได้ แค่อยากให้รู้ว่ามีคนคิดถึง"],
        "just_because": ["ส่งของมาเพราะคิดถึง ไม่ใช่เพราะลืมวันสำคัญ — ครั้งนี้จริง", "ไม่มีโอกาสพิเศษ ก็แปลว่าพิเศษได้อยู่ดี"],
    },
    "formal": {
        "birthday": ["ขออวยพรเนื่องในวันคล้ายวันเกิดให้สุขภาพแข็งแรงและสมหวังในสิ่งที่ตั้งใจ", "สุขสันต์วันเกิด ขอให้ปีนี้เต็มไปด้วยกำลังใจดี ๆ"],
        "anniversary": ["ขออวยพรเนื่องในวันครบรอบ ให้ความสัมพันธ์มั่นคงและอบอุ่น", "ยินดีกับวันครบรอบ และขอบคุณที่ดูแลกันมาโดยตลอด"],
        "thank_you": ["ขอขอบคุณสำหรับความช่วยเหลือและความปรารถนาดี", "สิ่งนี้เป็นเพียงของแทนความรู้สึกขอบคุณอย่างจริงใจ"],
        "housewarming": ["ขออวยพรให้บ้านใหม่เป็นสิริมงคล ปลอดภัย และอบอุ่น", "ยินดีกับบ้านใหม่ ขอให้ทุกคนในบ้านอยู่เย็นเป็นสุข"],
        "new_job": ["ขออวยพรให้การเริ่มงานใหม่ราบรื่นและได้ใช้ความสามารถอย่างเต็มที่", "ยินดีกับงานใหม่ ขอให้ทุกก้าวมั่นคง"],
        "condolence": ["ขอแสดงความเสียใจ และเป็นกำลังใจให้ครอบครัวผ่านช่วงเวลานี้", "ขอให้ท่านและครอบครัวได้รับความอบอุ่นจากคนรอบข้าง"],
        "just_because": ["ขอส่งของเล็กน้อยเพื่อแสดงความปรารถนาดี", "หวังว่าของชิ้นนี้จะเป็นประโยชน์และสร้างรอยยิ้ม"],
    },
    "short": {
        "birthday": ["สุขสันต์วันเกิดนะ", "เกิดมาดีแล้ว ปีนี้ดีกว่าเดิมอีก"],
        "anniversary": ["ครบรอบนี้ รักเท่าเดิม", "ขอบคุณที่ยังเดินด้วยกัน"],
        "thank_you": ["ขอบคุณมากนะ", "จำน้ำใจนี้ไว้เสมอ"],
        "housewarming": ["ยินดีกับบ้านใหม่", "ขอให้อบอุ่นนะ"],
        "new_job": ["ยินดีกับงานใหม่", "สู้ ๆ นะ เก่งมาก"],
        "condolence": ["เป็นกำลังใจให้นะ", "อยู่ตรงนี้นะ"],
        "just_because": ["คิดถึง", "ให้ยิ้มหน่อย"],
    },
}

WRAPS = {
    "low": {"band": "low", "max_thb": 500, "ideas_th": ["ถุงกระดาษคราฟท์ + โบว์ผ้า", "ห่อผ้าเก่าที่สะอาด ผูกเชือกป่าน", "ซองจดหมายใหญ่เขียนข้อความหน้าซอง"]},
    "mid": {"band": "mid", "max_thb": 1500, "ideas_th": ["กล่องคราฟท์ + ดอกไม้แห้ง 1 กิ่ง + การ์ดเขียนมือ", "ถุงผ้าขาว + โบว์สีอ่อน", "ห่อผ้าสีพื้น ติดป้ายชื่อผู้รับ"]},
    "high": {"band": "high", "max_thb": 3000, "ideas_th": ["กล่องฝาปิดแม่เหล็ก + กระดาษรองสีครีม", "ผ้าห่อของแบบของขวัญ + โบว์กำมะหยี่", "ใส่ตะกร้าเล็กพร้อมการ์ด"]},
    "luxe": {"band": "luxe", "max_thb": None, "ideas_th": ["กล่องแข็งบุผ้า + การ์ดปั๊มนูน", "ผ้าห่อของสีเข้ม + โบว์ไหม", "จัดเป็นชุดบนถาด แล้วคลุมด้วยผ้าโปร่ง"]},
}

SOON_DAYS, DUE_DAYS = 21, 7

def persona_quiz(relationship, age_band, vibe, hobbies, occasion, budget_thb, receiver_name_th):
    if relationship not in RELS:
        raise ValueError("unknown relationship")
    if age_band not in AGE_BANDS:
        raise ValueError("unknown age_band")
    if vibe not in VIBES:
        raise ValueError("unknown vibe")
    if occasion not in OCCASIONS:
        raise ValueError("unknown occasion")
    if budget_thb < 0:
        raise ValueError("budget < 0")
    if not hobbies or any(h not in HOBBIES for h in hobbies):
        raise ValueError("bad hobbies")
    # unique preserve order
    seen, hs = set(), []
    for h in hobbies:
        if h not in seen:
            seen.add(h); hs.append(h)
    return {"relationship": relationship, "age_band": age_band, "vibe": vibe, "hobbies": hs,
            "occasion": occasion, "budget_thb": budget_thb, "receiver_name_th": receiver_name_th,
            "is_minor": age_band in MINOR_BANDS}

def gift_score(gift, quiz):
    if gift["mid"] > quiz["budget_thb"]:
        return 0
    if gift["adult_only"] and quiz["is_minor"]:
        return 0
    s = 0
    if quiz["relationship"] in gift["rel"]:
        s += 25
    if quiz["age_band"] in gift["age"]:
        s += 20
    if quiz["vibe"] in gift["vibe"]:
        s += 20
    overlap = [h for h in quiz["hobbies"] if h in gift["hobby"]]
    s += 10 * min(2, len(overlap))
    if quiz["occasion"] in gift["occasions"]:
        s += 15
    if gift["mid"] >= quiz["budget_thb"] * 0.5:
        s += 10
    return min(100, s)

def budget_picks(quiz, limit=5):
    scored = []
    for gid, g in GIFTS.items():
        sc = gift_score(g, quiz)
        if sc <= 0:
            continue
        why = g["why_th"]
        if quiz["budget_thb"] < g["min"]:
            continue
        scored.append({
            "gift_id": gid, "name_th": g["name_th"], "name_en": g["name_en"],
            "min_thb": g["min"], "max_thb": g["max"], "mid_thb": g["mid"],
            "score": sc, "why_th": why, "adult_only": g["adult_only"],
            "disclaimer_th": PRICE_DISCLAIMER_TH,
        })
    scored.sort(key=lambda x: (-x["score"], -x["mid_thb"], x["gift_id"]))
    return {"receiver_name_th": quiz["receiver_name_th"], "budget_thb": quiz["budget_thb"],
            "picks": scored[:limit], "count": min(limit, len(scored)), "filtered_out": len(GIFTS) - len(scored)}

def already_has_swap(quiz, exclude_ids, limit=3):
    picks = budget_picks(quiz, limit=20)
    remain = [p for p in picks["picks"] if p["gift_id"] not in exclude_ids]
    return {"picks": remain[:limit], "count": min(limit, len(remain))}

def card_messages(occasion, tone, receiver_name_th, n=2):
    if occasion not in OCCASIONS:
        raise ValueError("unknown occasion")
    if tone not in TONES:
        raise ValueError("unknown tone")
    bank = CARD_BANK[tone][occasion]
    start = (sum(ord(ch) for ch in receiver_name_th) + 1) % len(bank)
    picked = [bank[(start + i) % len(bank)] for i in range(n)]
    return [{"n": i + 1, "occasion": occasion, "tone": tone, "receiver_name_th": receiver_name_th, "text_th": t}
            for i, t in enumerate(picked)]

def wrap_ideas(budget_thb):
    if budget_thb < 0:
        raise ValueError("budget < 0")
    if budget_thb <= 500:
        key = "low"
    elif budget_thb <= 1500:
        key = "mid"
    elif budget_thb <= 3000:
        key = "high"
    else:
        key = "luxe"
    w = WRAPS[key]
    return {"band": w["band"], "budget_thb": budget_thb, "ideas_th": list(w["ideas_th"]),
            "tip_th": "ห่อเองที่บ้านก็ได้ ไม่ต้องแพงกว่าของข้างใน", "disclaimer_th": PRICE_DISCLAIMER_TH}

def reminder_status(event_date, today):
    days = (_dt.date.fromisoformat(event_date) - _dt.date.fromisoformat(today)).days
    if days < 0:
        status = "past"
    elif days <= DUE_DAYS:
        status = "due"
    elif days <= SOON_DAYS:
        status = "soon"
    else:
        status = "ok"
    return {"event_date": event_date, "today": today, "days_left": days, "status": status}

def occasion_event(eid, receiver_name_th, occasion, event_date, budget_thb, today):
    if occasion not in OCCASIONS:
        raise ValueError("unknown occasion")
    st = reminder_status(event_date, today)
    return {"id": eid, "receiver_name_th": receiver_name_th, "occasion": occasion, "event_date": event_date,
            "budget_thb": budget_thb, "days_left": st["days_left"], "status": st["status"]}

def calendar_stats(events):
    if not events:
        return {"count": 0, "due": 0, "soon": 0, "next_id": None}
    due = sum(1 for e in events if e["status"] == "due")
    soon = sum(1 for e in events if e["status"] == "soon")
    upcoming = [e for e in events if e["days_left"] >= 0]
    nxt = sorted(upcoming, key=lambda e: (e["days_left"], e["id"]))[0]["id"] if upcoming else None
    return {"count": len(events), "due": due, "soon": soon, "next_id": nxt}

def share_card(quiz, top_pick, message_th):
    return {"title_th": f"GiftGenie — ของขวัญให้ {quiz['receiver_name_th']}",
            "headline_th": top_pick["name_th"] if top_pick else "ยังไม่มีไอเดียในงบนี้",
            "hook_th": "คิดของขวัญไม่ออก ตอบ 5 ข้อได้ไอเดียตามงบ",
            "budget_thb": quiz["budget_thb"], "score": top_pick["score"] if top_pick else 0,
            "message_th": message_th, "layout": "gift_card",
            "sizes": ["1080x1350", "1080x1920", "1080x1080"], "watermark": WATERMARK,
            "cta_th": f"งบ ฿{quiz['budget_thb']:,} · คอมเมนต์ GIFT รับแพ็กฟรี"}

def quota(used_today, want, pro=False):
    if pro:
        return {"allowed": want, "left_after": None, "paywall": False}
    left = max(0, FREE_RUNS_PER_DAY - used_today)
    allowed = min(want, left)
    return {"allowed": allowed, "left_after": left - allowed, "paywall": allowed < want}

def safety_guard(is_minor, adult_item=False):
    if is_minor and adult_item:
        return {"level": "stop", "message_th": "ไม่แนะนำของสำหรับผู้ใหญ่ให้ผู้รับที่เป็นเด็ก " + SAFETY_DISCLAIMER_TH}
    if is_minor:
        return {"level": "warn", "message_th": "ผู้รับยังไม่บรรลุนิติภาวะ เลี่ยงของที่มีแอลกอฮอล์ ของมีคม และของเล็กที่กลืนได้ " + SAFETY_DISCLAIMER_TH}
    return {"level": "ok", "message_th": SAFETY_DISCLAIMER_TH}
