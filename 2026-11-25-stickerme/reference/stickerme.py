"""StickerMe deterministic logic (no AI calls).
LINE size numbers are app-chosen copies of commonly published Creators specs —
always re-check the official LINE Creators Studio guide before uploading.
Not affiliated with LINE. Stickers are AI illustrations, not photographs.
"""
FREE_SCANS_PER_DAY = 3
MIN_CONF = 0.6
WATERMARK = "Made with StickerMe · AI illustration, not a LINE product"
SAFETY_DISCLAIMER_TH = "StickerMe สร้างภาพประกอบจากเซลฟี่ ไม่ใช่รูปถ่ายจริง และไม่ใช่ผลิตภัณฑ์ของ LINE ใช้ได้เฉพาะใบหน้าของตนเอง (ถ้าดูเป็นผู้เยาว์ต้องได้รับความยินยอมจากผู้ปกครอง) ตรวจสเปกอีกครั้งใน LINE Creators Studio ก่อนอัปโหลด"

# Commonly published static sticker sizes. Verify against official docs before upload.
LINE_SPEC = {
    "sticker_w": 370, "sticker_h": 320,
    "main_w": 240, "main_h": 240,
    "tab_w": 96, "tab_h": 74,
    "allowed_counts": (8, 16, 24),
    "format": "png",
    "transparent": True,
    "max_kb_per_sticker": 1000,
    "source_th": "ค่าตัวอย่างที่อ้างอิงสเปกที่เผยแพร่ทั่วไป ต้องตรวจกับคู่มือทางการของ LINE Creators Studio ก่อนอัปโหลด",
}

EMOTIONS = {
    "happy":     {"id": "e01", "name_th": "ยิ้มแย้ม", "name_en": "happy", "priority": 1},
    "laugh":     {"id": "e02", "name_th": "หัวเราะ", "name_en": "laugh", "priority": 2},
    "love":      {"id": "e03", "name_th": "หัวใจ", "name_en": "love", "priority": 3},
    "wink":      {"id": "e04", "name_th": "ขยิบตา", "name_en": "wink", "priority": 4},
    "ok":        {"id": "e05", "name_th": "โอเค", "name_en": "ok", "priority": 5},
    "thumbs":    {"id": "e06", "name_th": "ยกนิ้ว", "name_en": "thumbs up", "priority": 6},
    "sad":       {"id": "e07", "name_th": "เศร้า", "name_en": "sad", "priority": 7},
    "cry":       {"id": "e08", "name_th": "ร้องไห้", "name_en": "cry", "priority": 8},
    "angry":     {"id": "e09", "name_th": "โกรธ", "name_en": "angry", "priority": 9},
    "shocked":   {"id": "e10", "name_th": "ตกใจ", "name_en": "shocked", "priority": 10},
    "sleepy":    {"id": "e11", "name_th": "ง่วง", "name_en": "sleepy", "priority": 11},
    "think":     {"id": "e12", "name_th": "กำลังคิด", "name_en": "thinking", "priority": 12},
    "sorry":     {"id": "e13", "name_th": "ขอโทษ", "name_en": "sorry", "priority": 13},
    "celebrate": {"id": "e14", "name_th": "ฉลอง", "name_en": "celebrate", "priority": 14},
    "tired":     {"id": "e15", "name_th": "เหนื่อย", "name_en": "tired", "priority": 15},
    "please":    {"id": "e16", "name_th": "ขอร้อง", "name_en": "please", "priority": 16},
    "wave":      {"id": "e17", "name_th": "โบกมือ", "name_en": "wave", "priority": 17},
    "cool":      {"id": "e18", "name_th": "เท่", "name_en": "cool", "priority": 18},
    "shy":       {"id": "e19", "name_th": "เขิน", "name_en": "shy", "priority": 19},
    "wow":       {"id": "e20", "name_th": "ว้าว", "name_en": "wow", "priority": 20},
    "hungry":    {"id": "e21", "name_th": "หิว", "name_en": "hungry", "priority": 21},
    "ok_wait":   {"id": "e22", "name_th": "รอแป๊บ", "name_en": "wait", "priority": 22},
    "missyou":   {"id": "e23", "name_th": "คิดถึง", "name_en": "miss you", "priority": 23},
    "goodnight": {"id": "e24", "name_th": "ราตรีสวัสดิ์", "name_en": "good night", "priority": 24},
}

DEFAULT_SET_16 = [
    "happy", "laugh", "love", "wink", "ok", "thumbs", "sad", "cry",
    "angry", "shocked", "sleepy", "think", "sorry", "celebrate", "tired", "please",
]

BUBBLES = {
    "got_it":      {"id": "b01", "text_th": "เข้าใจแล้ว", "max_chars": 12},
    "on_my_way":   {"id": "b02", "text_th": "กำลังไป!", "max_chars": 12},
    "eaten_yet":   {"id": "b03", "text_th": "กินข้าวยัง?", "max_chars": 12},
    "ok_coming":   {"id": "b04", "text_th": "โอเค เดี๋ยวมา", "max_chars": 14},
    "love_you":    {"id": "b05", "text_th": "รักนะ", "max_chars": 12},
    "no_worries":  {"id": "b06", "text_th": "ไม่เป็นไร", "max_chars": 12},
    "awesome":     {"id": "b07", "text_th": "สุดยอด!", "max_chars": 12},
    "wait":        {"id": "b08", "text_th": "รอแป๊บ", "max_chars": 12},
}

# Default pairing of the first 8 stickers in a 16-pack with Thai bubbles.
DEFAULT_BUBBLE_MAP = {
    "happy": "got_it", "laugh": "awesome", "love": "love_you", "wink": "ok_coming",
    "ok": "got_it", "thumbs": "awesome", "sad": "no_worries", "cry": "no_worries",
}

STYLES = {
    "chibi":      {"id": "st01", "name_th": "จิ๋วหัวโต", "name_en": "chibi", "outline": True},
    "comic":      {"id": "st02", "name_th": "การ์ตูนเส้นหนา", "name_en": "comic", "outline": True},
    "watercolor": {"id": "st03", "name_th": "สีน้ำ", "name_en": "watercolor", "outline": False},
    "pop":        {"id": "st04", "name_th": "ป๊อปอาร์ต", "name_en": "pop art", "outline": True},
    "pixel":      {"id": "st05", "name_th": "พิกเซล", "name_en": "pixel", "outline": True},
    "clay":       {"id": "st06", "name_th": "ดินปั้น", "name_en": "clay", "outline": False},
    "lineart":    {"id": "st07", "name_th": "เส้นบาง", "name_en": "line art", "outline": True},
    "gloss":      {"id": "st08", "name_th": "สติกเกอร์เงา", "name_en": "gloss sticker", "outline": True},
}


def scan_quality(glare, blur, crop, face_conf, face_frac):
    for v in (glare, blur, crop, face_conf, face_frac):
        if not 0 <= v <= 1:
            raise ValueError("glare/blur/crop/face_conf/face_frac must be 0..1")
    score = round(100 * (1 - (0.30 * glare + 0.35 * blur + 0.20 * crop + 0.15 * (1 - face_frac))))
    if face_conf < MIN_CONF:
        score = max(0, score - 30)
    tips = []
    if glare > 0.5:
        tips.append("แสงสะท้อนบนหน้าเยอะ หันออกจากหน้าต่างหรือปิดแฟลช")
    if blur > 0.4:
        tips.append("ภาพเบลอ ถือกล้องนิ่งหรือถ่ายใหม่ในที่สว่าง")
    if crop > 0.45 or face_frac < 0.25:
        tips.append("ใบหน้าเล็กหรือถูกครอป ถ่ายใกล้ขึ้นให้เห็นทั้งหน้าและไหล่")
    if face_conf < MIN_CONF:
        tips.append("ไม่มั่นใจว่าเป็นใบหน้า ลองถ่ายใหม่ในพื้นเรียบ แสงหน้าตรง")
    return {"score": score, "ok": score >= 60 and face_conf >= MIN_CONF and face_frac >= 0.2, "tips_th": tips}


def consent_guard(own_face=False, other_person=False, apparent_minor=False, guardian_consent=False, celebrity_likeness=False):
    if other_person:
        return {"level": "stop", "code": "other_person",
                "message_th": "ใช้ได้เฉพาะใบหน้าของตนเอง ไม่สร้างสติกเกอร์จากรูปคนอื่น " + SAFETY_DISCLAIMER_TH}
    if celebrity_likeness:
        return {"level": "stop", "code": "celebrity",
                "message_th": "ห้ามสร้างสติกเกอร์เลียนแบบคนดังหรือตัวละครที่มีลิขสิทธิ์ " + SAFETY_DISCLAIMER_TH}
    if apparent_minor and not guardian_consent:
        return {"level": "stop", "code": "minor_no_guardian",
                "message_th": "ถ้าดูเหมือนผู้เยาว์ ต้องได้รับความยินยอมจากผู้ปกครองก่อนสร้างชุด " + SAFETY_DISCLAIMER_TH}
    if not own_face:
        return {"level": "stop", "code": "no_consent",
                "message_th": "ต้องยืนยันว่าเป็นใบหน้าของตนเองก่อนสร้างสติกเกอร์ " + SAFETY_DISCLAIMER_TH}
    if apparent_minor and guardian_consent:
        return {"level": "warn", "code": "minor_with_guardian",
                "message_th": "สร้างได้เพราะผู้ปกครองยินยอม ภาพเป็นภาพประกอบ ไม่ใช่รูปเด็กจริง " + SAFETY_DISCLAIMER_TH}
    return {"level": "ok", "code": "ok", "message_th": SAFETY_DISCLAIMER_TH}


def bubble_check(text_th, max_chars=14):
    t = (text_th or "").strip()
    if not t:
        return {"ok": False, "text_th": t, "chars": 0, "max_chars": max_chars, "message_th": "ใส่ข้อความสั้น ๆ ก่อนติดบนสติกเกอร์"}
    if len(t) > max_chars:
        return {"ok": False, "text_th": t, "chars": len(t), "max_chars": max_chars,
                "message_th": f"ข้อความยาวเกิน {max_chars} ตัวอักษร ตัดให้สั้นลงเพื่อให้อ่านบนสติกเกอร์"}
    return {"ok": True, "text_th": t, "chars": len(t), "max_chars": max_chars, "message_th": "ข้อความสั้นพอดี"}


def make_sticker(emotion_key, style_key, w, h, bubble_key=None, custom_text=None):
    if emotion_key not in EMOTIONS:
        raise ValueError("unknown emotion " + emotion_key)
    if style_key not in STYLES:
        raise ValueError("unknown style " + style_key)
    emo = EMOTIONS[emotion_key]
    style = STYLES[style_key]
    text = None
    bubble_id = None
    if custom_text is not None:
        chk = bubble_check(custom_text)
        if not chk["ok"]:
            raise ValueError(chk["message_th"])
        text = chk["text_th"]
        bubble_id = "custom"
    elif bubble_key:
        if bubble_key not in BUBBLES:
            raise ValueError("unknown bubble " + bubble_key)
        text = BUBBLES[bubble_key]["text_th"]
        bubble_id = BUBBLES[bubble_key]["id"]
        chk = bubble_check(text, BUBBLES[bubble_key]["max_chars"])
        if not chk["ok"]:
            raise ValueError(chk["message_th"])
    return {
        "emotion": emotion_key,
        "emotion_id": emo["id"],
        "name_th": emo["name_th"],
        "style": style_key,
        "style_id": style["id"],
        "w": w, "h": h,
        "format": "png",
        "transparent": True,
        "bubble_id": bubble_id,
        "text_th": text,
        "watermark": WATERMARK,
    }


def make_pack(scan, style_key, consent, emotions=None, bubble_map=None, count=16):
    if not scan.get("ok"):
        raise ValueError("scan not ok")
    if consent.get("level") == "stop":
        raise ValueError("consent blocked: " + consent.get("code", ""))
    if count not in LINE_SPEC["allowed_counts"]:
        raise ValueError("count must be 8, 16 or 24")
    keys = list(emotions) if emotions is not None else list(DEFAULT_SET_16)
    if len(keys) != count:
        raise ValueError("emotion count must match pack size")
    for k in keys:
        if k not in EMOTIONS:
            raise ValueError("unknown emotion " + k)
    seen = set()
    for k in keys:
        if k in seen:
            raise ValueError("duplicate emotion " + k)
        seen.add(k)
    bmap = DEFAULT_BUBBLE_MAP if bubble_map is None else bubble_map
    stickers = []
    for k in keys:
        stickers.append(make_sticker(k, style_key, LINE_SPEC["sticker_w"], LINE_SPEC["sticker_h"], bubble_key=bmap.get(k)))
    with_text = sum(1 for s in stickers if s["text_th"])
    return {
        "style": style_key,
        "style_name_th": STYLES[style_key]["name_th"],
        "count": count,
        "with_text": with_text,
        "stickers": stickers,
        "main": {"w": LINE_SPEC["main_w"], "h": LINE_SPEC["main_h"], "format": "png"},
        "tab": {"w": LINE_SPEC["tab_w"], "h": LINE_SPEC["tab_h"], "format": "png"},
        "headline_th": f"ชุดสติกเกอร์ {STYLES[style_key]['name_th']} {count} ใบ · มีข้อความไทย {with_text} ใบ",
        "watermark": WATERMARK,
        "consent_code": consent.get("code"),
    }


def export_spec(pack):
    checks = []
    def add(key, ok, detail_th):
        checks.append({"key": key, "ok": ok, "detail_th": detail_th})
    add("count", pack["count"] in LINE_SPEC["allowed_counts"],
        f"จำนวนสติกเกอร์ {pack['count']} ใบ (ต้องเป็น 8, 16 หรือ 24)")
    sizes_ok = all(s["w"] == LINE_SPEC["sticker_w"] and s["h"] == LINE_SPEC["sticker_h"] for s in pack["stickers"])
    add("sticker_size", sizes_ok, f"ขนาดสติกเกอร์ {LINE_SPEC['sticker_w']}×{LINE_SPEC['sticker_h']} พิกเซล")
    add("main_size", pack["main"]["w"] == LINE_SPEC["main_w"] and pack["main"]["h"] == LINE_SPEC["main_h"],
        f"รูปหลัก {LINE_SPEC['main_w']}×{LINE_SPEC['main_h']} พิกเซล")
    add("tab_size", pack["tab"]["w"] == LINE_SPEC["tab_w"] and pack["tab"]["h"] == LINE_SPEC["tab_h"],
        f"แท็บ {LINE_SPEC['tab_w']}×{LINE_SPEC['tab_h']} พิกเซล")
    add("format", all(s["format"] == "png" and s["transparent"] for s in pack["stickers"]),
        "ไฟล์ PNG พื้นโปร่งใส")
    add("official_recheck", True, LINE_SPEC["source_th"])
    passed = sum(1 for c in checks if c["ok"])
    all_ok = all(c["ok"] for c in checks)
    return {
        "ready": all_ok,
        "passed": passed,
        "total": len(checks),
        "checks": checks,
        "sticker_w": LINE_SPEC["sticker_w"], "sticker_h": LINE_SPEC["sticker_h"],
        "main_w": LINE_SPEC["main_w"], "main_h": LINE_SPEC["main_h"],
        "tab_w": LINE_SPEC["tab_w"], "tab_h": LINE_SPEC["tab_h"],
        "max_kb_per_sticker": LINE_SPEC["max_kb_per_sticker"],
        "headline_th": "พร้อมส่งตรวจใน Creators Studio" if all_ok else "ยังไม่ครบสเปก ตรวจรายการที่ยังไม่ผ่าน",
        "disclaimer_th": LINE_SPEC["source_th"],
    }


def chat_preview(pack, sample_n=4):
    n = min(sample_n, pack["count"])
    bubbles = [s for s in pack["stickers"] if s["text_th"]][:n]
    if len(bubbles) < n:
        rest = [s for s in pack["stickers"] if not s["text_th"]]
        bubbles = (bubbles + rest)[:n]
    return {
        "layout": "chat_mock",
        "style": pack["style"],
        "items": [{"name_th": s["name_th"], "text_th": s["text_th"]} for s in bubbles],
        "count": n,
        "watermark": WATERMARK,
    }


def share_card(name_th, pack, export):
    return {
        "title_th": f"StickerMe — {name_th}",
        "headline_th": pack["headline_th"],
        "hook_th": "เซลฟี่เดียว ได้สติกเกอร์ LINE หน้าตัวเองทั้งเซ็ต",
        "style": pack["style"],
        "count": pack["count"],
        "with_text": pack["with_text"],
        "export_ready": export["ready"],
        "layout": "sticker_card",
        "sizes": ["1080x1350", "1080x1920", "1080x1080"],
        "watermark": WATERMARK,
        "cta_th": "คอมเมนต์ STICKER รับแพ็กฟรี",
    }


def quota(used_today, want, pro=False):
    if pro:
        return {"allowed": want, "left_after": None, "paywall": False}
    left = max(0, FREE_SCANS_PER_DAY - used_today)
    allowed = min(want, left)
    return {"allowed": allowed, "left_after": left - allowed, "paywall": allowed < want}


def safety_guard(consent=None):
    if consent is None:
        return {"level": "ok", "message_th": SAFETY_DISCLAIMER_TH}
    return {"level": consent["level"], "message_th": consent["message_th"]}


def style_library():
    return [{"key": k, **v} for k, v in STYLES.items()]


def emotion_library():
    return [{"key": k, **v} for k, v in EMOTIONS.items()]
