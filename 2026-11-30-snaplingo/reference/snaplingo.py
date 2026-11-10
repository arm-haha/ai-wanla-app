"""SnapLingo deterministic logic (no AI calls).
Vocabulary and pronunciations are app-chosen study examples, not an official curriculum.
Object photos only — no child face is required.
"""
FREE_SCANS_PER_DAY = 3
MIN_CONF = 0.6
WATERMARK = "Made with SnapLingo · practice only, not a school curriculum"
SAFETY_DISCLAIMER_TH = "SnapLingo เป็นคลังคำศัพท์ตัวอย่างสำหรับเล่นกับของในบ้าน ไม่ใช่หลักสูตรโรงเรียน และไม่ตรวจการออกเสียงให้คะแนนทางการ ถ่ายของไม่ต้องมีใบหน้าเด็กในรูป"

WORDS = {
    "kettle":      {"id": "w01", "name_th": "กาต้มน้ำ", "name_en": "kettle", "ipa_en": "/ˈket.əl/", "th_en": "เคท-เทิล", "name_zh": "水壶", "pinyin": "shuǐhú", "th_zh": "สุ่ย-หู", "topic": "kitchen"},
    "cup":         {"id": "w02", "name_th": "แก้ว", "name_en": "cup", "ipa_en": "/kʌp/", "th_en": "คัพ", "name_zh": "杯子", "pinyin": "bēizi", "th_zh": "เปย-จึ", "topic": "kitchen"},
    "spoon":       {"id": "w03", "name_th": "ช้อน", "name_en": "spoon", "ipa_en": "/spuːn/", "th_en": "สปูน", "name_zh": "勺子", "pinyin": "sháozi", "th_zh": "เสา-จึ", "topic": "kitchen"},
    "plate":       {"id": "w04", "name_th": "จาน", "name_en": "plate", "ipa_en": "/pleɪt/", "th_en": "เพลต", "name_zh": "盘子", "pinyin": "pánzi", "th_zh": "ผาน-จึ", "topic": "kitchen"},
    "fridge":      {"id": "w05", "name_th": "ตู้เย็น", "name_en": "fridge", "ipa_en": "/frɪdʒ/", "th_en": "ฟริดจ์", "name_zh": "冰箱", "pinyin": "bīngxiāng", "th_zh": "ปิง-เซียง", "topic": "kitchen"},
    "rice_cooker": {"id": "w06", "name_th": "หม้อหุงข้าว", "name_en": "rice cooker", "ipa_en": "/raɪs ˈkʊk.ər/", "th_en": "ไรซ์ คุก-เคอร์", "name_zh": "电饭煲", "pinyin": "diànfànbāo", "th_zh": "เตี้ยน-ฟ้าน-ปาว", "topic": "kitchen"},
    "chair":       {"id": "w07", "name_th": "เก้าอี้", "name_en": "chair", "ipa_en": "/tʃeər/", "th_en": "แชร์", "name_zh": "椅子", "pinyin": "yǐzi", "th_zh": "อี่-จึ", "topic": "room"},
    "table":       {"id": "w08", "name_th": "โต๊ะ", "name_en": "table", "ipa_en": "/ˈteɪ.bəl/", "th_en": "เท-เบิล", "name_zh": "桌子", "pinyin": "zhuōzi", "th_zh": "จัว-จึ", "topic": "room"},
    "book":        {"id": "w09", "name_th": "หนังสือ", "name_en": "book", "ipa_en": "/bʊk/", "th_en": "บุ๊ก", "name_zh": "书", "pinyin": "shū", "th_zh": "ชู", "topic": "room"},
    "lamp":        {"id": "w10", "name_th": "โคมไฟ", "name_en": "lamp", "ipa_en": "/læmp/", "th_en": "แลมป์", "name_zh": "灯", "pinyin": "dēng", "th_zh": "เติง", "topic": "room"},
    "pillow":      {"id": "w11", "name_th": "หมอน", "name_en": "pillow", "ipa_en": "/ˈpɪl.oʊ/", "th_en": "พิล-โลว์", "name_zh": "枕头", "pinyin": "zhěntou", "th_zh": "เจิน-โถว", "topic": "room"},
    "clock":       {"id": "w12", "name_th": "นาฬิกา", "name_en": "clock", "ipa_en": "/klɒk/", "th_en": "คล็อก", "name_zh": "时钟", "pinyin": "shízhōng", "th_zh": "สือ-จง", "topic": "room"},
    "shoes":       {"id": "w13", "name_th": "รองเท้า", "name_en": "shoes", "ipa_en": "/ʃuːz/", "th_en": "ชูซ์", "name_zh": "鞋子", "pinyin": "xiézi", "th_zh": "เสีย-จึ", "topic": "daily"},
    "bag":         {"id": "w14", "name_th": "กระเป๋า", "name_en": "bag", "ipa_en": "/bæɡ/", "th_en": "แบ็ก", "name_zh": "包", "pinyin": "bāo", "th_zh": "ปาว", "topic": "daily"},
    "toothbrush":  {"id": "w15", "name_th": "แปรงสีฟัน", "name_en": "toothbrush", "ipa_en": "/ˈtuːθ.brʌʃ/", "th_en": "ทูธ-บรัช", "name_zh": "牙刷", "pinyin": "yáshuā", "th_zh": "หยา-ชัว", "topic": "daily"},
    "plant":       {"id": "w16", "name_th": "ต้นไม้", "name_en": "plant", "ipa_en": "/plɑːnt/", "th_en": "พลานท์", "name_zh": "植物", "pinyin": "zhíwù", "th_zh": "จือ-อู้", "topic": "daily"},
}

REWARD_STREAKS = {3: "star", 7: "sun", 14: "rainbow", 30: "trophy"}
REWARD_NAMES = {"star": "ดาว", "sun": "พระอาทิตย์", "rainbow": "รุ้ง", "trophy": "ถ้วยรางวัล"}


def scan_quality(glare, blur, crop, n_dets):
    for v in (glare, blur, crop):
        if not 0 <= v <= 1:
            raise ValueError("glare/blur/crop must be 0..1")
    score = round(100 * (1 - (0.35 * glare + 0.40 * blur + 0.25 * crop)))
    if n_dets == 0:
        score = max(0, score - 30)
    tips = []
    if glare > 0.5:
        tips.append("แสงสะท้อนบนของเยอะ ย้ายออกจากหน้าต่างแล้วถ่ายใหม่")
    if blur > 0.4:
        tips.append("ภาพเบลอ วางของนิ่งแล้วถ่ายใกล้ขึ้น")
    if crop > 0.45:
        tips.append("ของถูกครอป ถ่ายให้เห็นทั้งชิ้น")
    if n_dets == 0:
        tips.append("ยังไม่เจอของในรูป วาง 1–3 ชิ้นบนโต๊ะแล้วถ่ายใหม่")
    return {"score": score, "ok": score >= 60 and n_dets >= 1, "tips_th": tips}


def _keys(shot):
    keys = []
    for d in shot["detections"]:
        if d.get("confidence", 0) >= MIN_CONF and d.get("key") in WORDS:
            if d["key"] not in keys:
                keys.append(d["key"])
    return keys


def parse_scene(shot):
    keys = _keys(shot)
    q = scan_quality(shot["glare"], shot["blur"], shot["crop"], len(shot["detections"]))
    # quality uses raw dets; ok also needs at least one confident word
    ok = q["ok"] and len(keys) >= 1
    if not keys and q["ok"]:
        q = dict(q, ok=False)
        ok = False
    return {"shot_id": shot["id"], "quality": q, "ok": ok, "keys": keys, "count": len(keys),
            "message_th": f"เจอของ {len(keys)} ชิ้น" if keys else "ยังจับคำศัพท์จากรูปไม่ได้ ลองถ่ายใหม่หรือเลือกคำเอง"}


def label_card(key):
    if key not in WORDS:
        raise ValueError("unknown word " + key)
    w = WORDS[key]
    return {**w, "key": key,
            "headline_th": f"{w['name_th']} · {w['name_en']} · {w['name_zh']}",
            "en_line_th": f"{w['name_en']} {w['ipa_en']} อ่านว่า {w['th_en']}",
            "zh_line_th": f"{w['name_zh']} {w['pinyin']} อ่านว่า {w['th_zh']}"}


def labels(keys):
    cards = [label_card(k) for k in keys]
    return {"cards": cards, "count": len(cards),
            "headline_th": f"คำศัพท์ {len(cards)} คำ จากของในบ้าน"}


def flashcards(keys, lang="en"):
    if lang not in ("en", "zh"):
        raise ValueError("lang must be en or zh")
    cards = []
    for k in keys:
        c = label_card(k)
        if lang == "en":
            front, back, audio = c["name_th"], f"{c['name_en']} {c['ipa_en']}", c["th_en"]
        else:
            front, back, audio = c["name_th"], f"{c['name_zh']} {c['pinyin']}", c["th_zh"]
        cards.append({"key": k, "lang": lang, "front_th": front, "back": back, "say_th": audio})
    return {"lang": lang, "cards": cards, "count": len(cards)}


def _choices(correct, lang, pool):
    """Deterministic 3 choices: correct + next 2 words in stable WORDS order (wrap)."""
    keys = list(WORDS)
    i = keys.index(correct)
    opts = [correct]
    j = 1
    while len(opts) < 3:
        cand = keys[(i + j) % len(keys)]
        if cand not in opts:
            opts.append(cand)
        j += 1
        if j > len(keys):
            break
    # keep correct first then rotate based on index so position varies
    pos = i % 3
    rest = [k for k in opts if k != correct]
    arranged = rest[:]
    arranged.insert(pos, correct)
    out = []
    for k in arranged:
        w = WORDS[k]
        text = w["name_en"] if lang == "en" else w["name_zh"]
        out.append({"key": k, "text": text, "correct": k == correct})
    return out


def mini_quiz(keys, lang="en", answers=None):
    if not keys:
        raise ValueError("need words for quiz")
    if lang not in ("en", "zh"):
        raise ValueError("lang must be en or zh")
    questions = []
    for n, k in enumerate(keys, 1):
        w = WORDS[k]
        prompt = f"{w['name_th']} คือคำว่าอะไรเป็น" + ("ภาษาอังกฤษ" if lang == "en" else "ภาษาจีน")
        choices = _choices(k, lang, keys)
        ans = None if answers is None else answers[n - 1]
        ok = None if ans is None else ans == k
        questions.append({"n": n, "key": k, "prompt_th": prompt, "choices": choices,
                          "answer": ans, "correct": ok})
    answered = [q for q in questions if q["answer"] is not None]
    right = sum(1 for q in questions if q["correct"])
    total = len(questions)
    score_pct = 0 if not answered else round(100 * right / len(answered))
    return {"lang": lang, "questions": questions, "count": total,
            "answered": len(answered), "right": right, "score_pct": score_pct,
            "headline_th": f"ตอบถูก {right}/{len(answered) or total}" if answered else f"แบบทดสอบ {total} ข้อ"}


def progress(prev_streak, quiz, date=None):
    if quiz["answered"] == 0:
        raise ValueError("quiz not answered")
    passed = quiz["score_pct"] >= 50
    streak = (prev_streak + 1) if passed else 0
    rewards = []
    if passed:
        for n, key in REWARD_STREAKS.items():
            if streak == n:
                rewards.append({"at": n, "key": key, "name_th": REWARD_NAMES[key]})
    return {"date": date, "passed": passed, "streak": streak, "prev_streak": prev_streak,
            "score_pct": quiz["score_pct"], "right": quiz["right"], "answered": quiz["answered"],
            "rewards": rewards, "reward_count": len(rewards),
            "headline_th": f"ต่อเนื่อง {streak} วัน" if passed else "วันนี้ยังไม่ครบ ลองใหม่อีกครั้ง"}


def share_card(parent_th, child_th, labs, prog):
    return {"title_th": f"SnapLingo — {child_th}",
            "headline_th": labs["headline_th"],
            "hook_th": "ถ่ายของรอบบ้าน ได้คำศัพท์อังกฤษ/จีนให้ลูก",
            "parent_th": parent_th, "child_th": child_th,
            "count": labs["count"], "streak": prog["streak"] if prog else 0,
            "layout": "lingo_card", "sizes": ["1080x1350", "1080x1920", "1080x1080"],
            "watermark": WATERMARK, "cta_th": "คอมเมนต์ LINGO รับแพ็กฟรี"}


def quota(used_today, want, pro=False):
    if pro:
        return {"allowed": want, "left_after": None, "paywall": False}
    left = max(0, FREE_SCANS_PER_DAY - used_today)
    allowed = min(want, left)
    return {"allowed": allowed, "left_after": left - allowed, "paywall": allowed < want}


def safety_guard(child_face_in_frame=False, parent_ok=True):
    if child_face_in_frame and not parent_ok:
        return {"level": "stop", "message_th": "มีใบหน้าเด็กในรูป ต้องให้ผู้ปกครองยินยอม หรือถ่ายเฉพาะตัวของ " + SAFETY_DISCLAIMER_TH}
    if child_face_in_frame:
        return {"level": "warn", "message_th": "แนะนำให้ถ่ายเฉพาะตัวของ ไม่ต้องมีใบหน้าเด็ก " + SAFETY_DISCLAIMER_TH}
    return {"level": "ok", "message_th": SAFETY_DISCLAIMER_TH}
