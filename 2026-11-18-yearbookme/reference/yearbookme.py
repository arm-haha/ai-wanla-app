"""YearbookMe deterministic logic (no AI calls). Styling recipes are app-chosen examples — not a real yearbook or school."""
import datetime as _dt
import urllib.parse as _up

ERAS = {
    "80s": {
        "id": "e80", "name_th": "ยุค 80s", "name_en": "1980s", "year_label": "Class of '86",
        "grade_th": "แสงนีออน ฟิล์มอบอุ่น ผมวอลุ่มสูง", "palette": ["#FF2E97", "#7C3AED", "#22D3EE", "#FDE68A"],
        "typography": "bold-italic-neon", "grain": 0.45, "flash": 0.20, "frame": "neon_studio",
        "props_th": ["ที่คาดผมนีออน", "แจ็กเก็ตโลโก้ใหญ่", "ต่างหูห่วงโต", "เลนส์ไล่สีชมพูฟ้า"],
        "hair_th": "ผมวอลุ่ม ดัดลอน หรือไซด์พาร์ทสูง", "clothes_th": "นีออน / ไหล่ตั้ง / แจ็กเก็ตแข่ง",
        "trait_weights": {"warm_tone": 0.30, "high_volume_hair": 0.30, "neon_pref": 0.20, "soft_glam": 0.20},
    },
    "90s": {
        "id": "e90", "name_th": "ยุค 90s", "name_en": "1990s", "year_label": "Class of '97",
        "grade_th": "ฟิล์มโทนเย็น ลายจุดปีบุ๊ก ขอบขาว", "palette": ["#1E3A5F", "#C4A574", "#F4EFE6", "#4B5563"],
        "typography": "serif-yearbook", "grain": 0.55, "flash": 0.10, "frame": "white_yearbook",
        "props_th": ["เดนิมแจ็กเก็ต", "สครับชี่", "สร้อยเงินเล็ก", "กล้องฟิล์มจุด"],
        "hair_th": "ผมตรงกลาง parted หรือชาร์จิ้นทิป", "clothes_th": "เดนิม ลายสก็อต เสื้อเชิ้ตโอเวอร์ไซส์",
        "trait_weights": {"cool_tone": 0.30, "straight_hair": 0.30, "film_pref": 0.20, "casual": 0.20},
    },
    "y2k": {
        "id": "e2k", "name_th": "ยุค Y2K", "name_en": "Y2K", "year_label": "Class of '02",
        "grade_th": "แฟลชตรง โทนเงินเมทัลลิก สkin โกลว์", "palette": ["#E5E7EB", "#F472B6", "#38BDF8", "#A3E635"],
        "typography": "thin-chrome", "grain": 0.25, "flash": 0.80, "frame": "chrome_polaroid",
        "props_th": ["มือถือฝาพับ", "แว่นแบบบาง", "กระเป๋ากะพริบ", "โลว์ไรส์เบลต์"],
        "hair_th": "ไฮไลต์ชิ้นเล็ก คิ้วบาง ผมตรงเงา", "clothes_th": "เมทัลลิก เสื้อครอป วอร์มแถบข้าง",
        "trait_weights": {"flash": 0.30, "glossy": 0.30, "thin_brows": 0.20, "metallic": 0.20},
    },
}
ERA_IDS = list(ERAS)
TONES = ["sweet", "funny", "proud", "nostalgic"]
ROLES = {
    "class_president": "ประธานรุ่น", "yearbook_club": "ชมรมปีบุ๊ก", "most_likely_friend": "เพื่อนที่ขาดไม่ได้",
    "most_likely_travel": "คนที่ทุกทริปต้องมี", "quiet_star": "คนเงียบแต่เด่นในรูป", "mc": "คนรับไมค์ทุกรอบ",
}
MIN_CONF = 0.6
MIN_AGE_SOLO = 13
ADULT_AGE = 18
FREE_GENS_PER_DAY = 3
WATERMARK = "Made with YearbookMe · styling only, not a real yearbook"
CONSENT_DISCLAIMER_TH = "YearbookMe ใช้ได้เฉพาะรูปของตนเอง (หรือรูปที่ทุกคนในภาพยินยอมแล้ว) ไม่ใช่รูปโรงเรียนจริง และไม่ใช่การยืนยันตัวตน"
SAFETY_DISCLAIMER_TH = "เป็นสไตล์จำลองเพื่อความบันเทิง ไม่ใช่สมุดรุ่นทางการ ห้ามใช้รูปคนอื่นโดยไม่ได้รับอนุญาต และห้ามใช้รูปเด็กโดยไม่มีผู้ปกครองยินยอม"

QUOTE_BANK = {
    "80s": {
        "sweet": ["เก็บรอยยิ้มนี้ไว้ในเทปเพลงโปรด แล้วมาเปิดฟังด้วยกันอีกสิบปี", "นีออนนี้จะทำให้จำได้ว่าเราเคยเสียงดังด้วยกันแค่ไหน"],
        "funny": ["ผมตั้งแล้ว แต่ใจยังไม่ทันตั้ง — ไว้รุ่นหน้าค่อยเรียบร้อย", "ถ้าเทปนี้กินแล้ว อย่าลืมว่าใครยืมวอล์กแมนไป"],
        "proud": ["รุ่นนี้เต้นไม่เป็น แต่รวมตัวไวที่สุดในโรงเรียน", "เก็บหน้านี้ไว้ แล้วบอกตัวเองในอนาคตว่าเริ่มจากตรงนี้"],
        "nostalgic": ["แสงนีออนจะดับ แต่เสียงหัวเราะในห้องนี้ยังวนอยู่ในหัว", "ถ้าเจอเทปม้วนนี้ในกล่องอีกสิบปี ขอให้ยิ้มก่อนเปิด"],
    },
    "90s": {
        "sweet": ["เพื่อนที่ขาดไม่ได้ของรุ่นนี้ — ไว้เจอกันอีกสิบปีนะ", "เก็บหน้านี้ไว้ในหน้าปีบุ๊ก แล้วอย่าลืมว่าเราเคยผ่านด้วยกัน"],
        "funny": ["หน้านี้คือหลักฐานว่าทรงผมปีนั้นกล้ามาก และยังกล้าเป็นเพื่อนกันอยู่", "ถ้ารุ่นหน้าถามว่าใครทำไมล์เยอะสุด ชี้มาที่รูปนี้ได้เลย"],
        "proud": ["ไม่ได้เรียนเก่งที่สุด แต่เป็นคนที่ทุกกลุ่มอยากให้มา", "เก็บความมุ่งมั่นปีนี้ไว้ แล้วไปโชว์รุ่นหลัง"],
        "nostalgic": ["ฟิล์มจะซีด แต่คำว่าเพื่อนในหน้านี้ยังชัด", "ถ้าเปิดสมุดนี้ในอีกยี่สิบปี ขอให้ยังจำกลิ่นห้องนั้นได้"],
    },
    "y2k": {
        "sweet": ["ส่งข้อความนี้ผ่านมือถือฝาพับ แล้วมาเปิดดูด้วยกันอีกรอบ", "โกลว์นี้เก็บไว้ให้วันที่ต้องการยิ้มแบบเดิม"],
        "funny": ["แบตมือถือฝาพับหมดไว แต่แบตความจำเพื่อนยังเต็ม", "ถ่ายด้วยแฟลชตรง เพราะตอนนั้นคิดว่ามันเจ๋งมาก — และก็ยังเจ๋ง"],
        "proud": ["รุ่นนี้โหลดเพลงช้า แต่ฝันเร็ว", "เก็บลุคนี้ไว้เป็นหลักฐานว่าเราเคยกล้ามาก"],
        "nostalgic": ["ก่อนสตอรี่จะมีแค่บล็อกและข้อความสั้น ๆ — แล้วก็มีเรากับเพื่อน", "ถ้าเจอรูปนี้ในโฟลเดอร์เก่า ขอให้กดเซฟอีกครั้ง"],
    },
}

WRAP_HOOKS = {
    "80s": "เซลฟี่เดียว กลายเป็นรูปรุ่นยุค 80s",
    "90s": "เซลฟี่เดียว กลายเป็นรูปรุ่นยุค 90s",
    "y2k": "เซลฟี่เดียว กลายเป็นรูปรุ่นยุค Y2K",
}

# ---------- Photo quality ----------
def scan_quality(glare, blur, crop, n_faces):
    for v in (glare, blur, crop):
        if not 0 <= v <= 1:
            raise ValueError("glare/blur/crop must be 0..1")
    score = round(100 * (1 - (0.30 * glare + 0.40 * blur + 0.30 * crop)))
    if n_faces == 0:
        score = max(0, score - 35)
    tips = []
    if glare > 0.5:
        tips.append("แสงสะท้อนบนหน้าเยอะ หันออกจากหน้าต่างหรือปิดแฟลชแรง ๆ")
    if blur > 0.4:
        tips.append("ภาพเบลอ ถือนิ่ง หรือวางมือถือพิงของแล้วนับ 1-2-3")
    if crop > 0.45:
        tips.append("ใบหน้าถูกครอป ถ่ายให้หัวถึงไหล่ครบในกรอบ")
    if n_faces == 0:
        tips.append("ไม่เจอใบหน้า ถ่ายเซลฟี่ให้เห็นหน้าชัดในแสงธรรมชาติ")
    if n_faces > 1:
        tips.append("มีหลายใบหน้า จะใช้โหมดหน้ารุ่นได้เมื่อทุกคนยินยอม")
    return {"score": score, "ok": score >= 60 and n_faces >= 1, "tips_th": tips, "face_count": n_faces}


def identify_faces(photo, min_conf=MIN_CONF):
    faces, uncertain = [], []
    for d in photo["detections"]:
        if d["confidence"] < min_conf:
            uncertain.append(d.get("label", "unknown"))
            continue
        faces.append({
            "label": d.get("label", "face"), "confidence": d["confidence"],
            "own_face": bool(d.get("own_face", False)),
            "celebrity_likely": bool(d.get("celebrity_likely", False)),
            "age_apparent": d.get("age_apparent"),
        })
    return {"photo_id": photo["id"], "faces": faces, "uncertain": uncertain, "face_count": len(faces)}


def photo_scan(photo):
    ident = identify_faces(photo)
    q = scan_quality(photo["glare"], photo["blur"], photo["crop"], len(photo["detections"]))
    # quality uses raw detections count (including low conf) like DashDoc n_lights
    return {"photo_id": photo["id"], "quality": q, "faces": ident["faces"], "uncertain": ident["uncertain"],
            "face_count": ident["face_count"]}


def pipeline_steps(photo):
    s = ["face_detect"]
    if photo["glare"] > 0.5:
        s.append("deglare")
    if photo["crop"] > 0.45:
        s.append("recrop")
    s += ["consent_check", "era_score", "style_render", "caption"]
    return s


# ---------- Consent guard ----------
def consent_guard(photo, profile):
    reasons, blocks = [], []
    own = bool(profile.get("own_photo"))
    confirmed = bool(profile.get("consent_confirmed"))
    age = profile.get("age")
    guardian_ok = bool(profile.get("guardian_ok"))
    ident = identify_faces(photo)
    celeb = any(f["celebrity_likely"] for f in ident["faces"]) or bool(profile.get("celebrity_likely"))
    other_faces = [f for f in ident["faces"] if not f["own_face"]]
    all_consented = bool(profile.get("all_consented"))

    if not confirmed:
        blocks.append("ยังไม่ได้ยืนยันว่าเป็นรูปของตนเองหรือได้รับอนุญาต")
    if not own:
        blocks.append("ใช้ได้เฉพาะรูปของตนเอง — ห้ามอัปโหลดรูปคนอื่นมาแปลง")
    if celeb:
        blocks.append("ระบบสงสัยว่าเป็นบุคคลสาธารณะ จึงไม่แปลงรูปนี้")
    if other_faces and not all_consented:
        blocks.append("มีคนอื่นในภาพ ต้องได้รับการยินยอมจากทุกคนก่อนทำหน้ารุ่น")
    if age is None:
        blocks.append("ยังไม่ได้ยืนยันอายุ")
    elif age < MIN_AGE_SOLO:
        blocks.append("แอปนี้ไม่รับรูปผู้ที่มีอายุต่ำกว่า 13 ปี")
    elif age < ADULT_AGE and not guardian_ok:
        blocks.append("อายุ 13–17 ปี ต้องมีผู้ปกครองยินยอมก่อน")
    if ident["face_count"] == 0:
        reasons.append("ยังไม่เจอใบหน้าชัดพอ")

    ok = not blocks
    level = "ok" if ok else "block"
    msg = "ผ่านการตรวจยินยอม พร้อมแปลงสไตล์ได้" if ok else "ยังแปลงไม่ได้: " + " · ".join(blocks)
    return {"ok": ok, "level": level, "reasons_th": reasons, "blocks_th": blocks, "message_th": msg,
            "face_count": ident["face_count"], "disclaimer_th": CONSENT_DISCLAIMER_TH}


# ---------- Era studio ----------
def era_score(traits, era):
    if era not in ERAS:
        raise ValueError("unknown era " + str(era))
    weights = ERAS[era]["trait_weights"]
    num = sum(traits.get(k, 0) * w for k, w in weights.items())
    den = sum(weights.values())
    return int(round(20 + 80 * (num / den)))


def style_render(photo, era, traits, name_th):
    if era not in ERAS:
        raise ValueError("unknown era")
    e = ERAS[era]
    score = era_score(traits, era)
    badge = "เข้าสุด" if score >= 75 else "ใช้ได้ดี" if score >= 55 else "ลุคทดลอง"
    return {
        "photo_id": photo["id"], "era": era, "name_th": e["name_th"], "name_en": e["name_en"],
        "year_label": e["year_label"], "score": score, "badge_th": badge, "grade_th": e["grade_th"],
        "palette": list(e["palette"]), "typography": e["typography"], "grain": e["grain"], "flash": e["flash"],
        "frame": e["frame"], "props_th": list(e["props_th"]), "hair_th": e["hair_th"], "clothes_th": e["clothes_th"],
        "headline_th": f"{name_th} · {e['year_label']}", "hook_th": WRAP_HOOKS[era],
    }


def era_studio(photo, traits, name_th):
    renders = [style_render(photo, era, traits, name_th) for era in ERA_IDS]
    renders.sort(key=lambda r: (-r["score"], r["era"]))
    top = renders[0]
    return {"photo_id": photo["id"], "name_th": name_th, "top_era": top["era"], "top_score": top["score"],
            "renders": renders, "count": len(renders)}


def era_info(era):
    if era not in ERAS:
        raise ValueError("unknown era")
    e = ERAS[era]
    return {"id": e["id"], "era": era, "name_th": e["name_th"], "name_en": e["name_en"], "year_label": e["year_label"],
            "grade_th": e["grade_th"], "palette": list(e["palette"]), "typography": e["typography"],
            "props_th": list(e["props_th"]), "hair_th": e["hair_th"], "clothes_th": e["clothes_th"]}


def prop_kit(era):
    e = era_info(era)
    return {"era": era, "name_th": e["name_th"], "props_th": e["props_th"], "frame": ERAS[era]["frame"],
            "tip_th": f"เลือก 1–2 ชิ้นก็พอ จะได้ไม่แย่งหน้า {e['name_th']}"}


# ---------- Quotes + autograph ----------
def caption_quotes(era, tone, name_th, n=3):
    if era not in ERAS:
        raise ValueError("unknown era")
    if tone not in TONES:
        raise ValueError("unknown tone")
    bank = QUOTE_BANK[era][tone]
    # deterministic rotate by name length so demos are stable
    start = (sum(ord(ch) for ch in name_th) + 1) % len(bank)
    picked = [bank[(start + i) % len(bank)] for i in range(min(n, len(bank)))]
    # if n > bank, repeat with slight prefix? just cycle
    while len(picked) < n:
        picked.append(bank[len(picked) % len(bank)])
    return [{"n": i + 1, "era": era, "tone": tone, "text_th": t, "for_name_th": name_th} for i, t in enumerate(picked[:n])]


def autograph(from_name_th, to_name_th, era, tone="sweet"):
    q = caption_quotes(era, tone, to_name_th, n=1)[0]["text_th"]
    text = f"ถึง {to_name_th}\n{q}\n— {from_name_th}"
    return {"from_name_th": from_name_th, "to_name_th": to_name_th, "era": era, "tone": tone,
            "text_th": text, "char_count": len(text)}


# ---------- Group yearbook page ----------
def member_slot(person, era, traits, role):
    if role not in ROLES:
        raise ValueError("unknown role")
    render = style_render(person["photo"], era, traits, person["name_th"])
    return {
        "id": person["id"], "name_th": person["name_th"], "name_en": person["name_en"],
        "nickname_th": person["nickname_th"], "role": role, "role_th": ROLES[role],
        "era": era, "score": render["score"], "headline_th": render["headline_th"],
        "consented": bool(person.get("consented", False)),
    }


def yearbook_page(title_th, school_th, year, era, slots):
    if era not in ERAS:
        raise ValueError("unknown era")
    if not slots:
        raise ValueError("no members")
    if not all(s["consented"] for s in slots):
        raise ValueError("every member must consent")
    e = ERAS[era]
    n = len(slots)
    cols = 2 if n <= 4 else 3
    rows = (n + cols - 1) // cols
    return {
        "title_th": title_th, "school_th": school_th, "year": year, "era": era,
        "year_label": e["year_label"], "frame": e["frame"], "palette": list(e["palette"]),
        "members": slots, "member_count": n, "cols": cols, "rows": rows,
        "disclaimer_th": "หน้ารุ่นจำลองจากรูปที่ทุกคนยินยอม ไม่ใช่สมุดรุ่นของโรงเรียนจริง",
    }


# ---------- Print + share + quota ----------
def print_sheet(name_th, era, quote_th, layout="portrait_a4"):
    layouts = {
        "portrait_a4": {"label_th": "A4 รูปเดี่ยว + คำคม", "sizes": ["A4", "1080x1350"]},
        "four_up": {"label_th": "A4 สี่รูป (80s / 90s / Y2K / ช่องว่างเซ็น)", "sizes": ["A4"]},
        "sticker": {"label_th": "สติกเกอร์ 5×5 ซม. 6 ชิ้น", "sizes": ["A4"]},
    }
    if layout not in layouts:
        raise ValueError("unknown layout")
    L = layouts[layout]
    return {"name_th": name_th, "era": era, "year_label": ERAS[era]["year_label"], "quote_th": quote_th,
            "layout": layout, "label_th": L["label_th"], "sizes": L["sizes"],
            "bleed_mm": 3, "watermark": WATERMARK, "cta_th": f"พิมพ์รูปรุ่น {ERAS[era]['name_th']} ของ {name_th}"}


def share_card(name_th, era, score, quote_th):
    e = ERAS[era]
    return {"title_th": f"YearbookMe — {name_th}", "headline_th": f"{e['year_label']} · {e['name_th']}",
            "hook_th": WRAP_HOOKS[era], "era": era, "score": score, "quote_th": quote_th,
            "layout": "era_portrait", "sizes": ["1080x1350", "1080x1920", "1080x1080"],
            "watermark": WATERMARK, "cta_th": f"คอมเมนต์ YEARBOOK รับแพ็กฟรี · คะแนนลุค {score}"}


def quota(used_today, want, pro=False):
    if pro:
        return {"allowed": want, "left_after": None, "paywall": False}
    left = max(0, FREE_GENS_PER_DAY - used_today)
    allowed = min(want, left)
    return {"allowed": allowed, "left_after": left - allowed, "paywall": allowed < want}


def safety_guard(consent_ok, age=None):
    if not consent_ok:
        return {"level": "stop", "message_th": "ยังแปลงไม่ได้ จนกว่าจะยืนยันว่าเป็นรูปของตนเอง " + SAFETY_DISCLAIMER_TH}
    if age is not None and age < MIN_AGE_SOLO:
        return {"level": "stop", "message_th": SAFETY_DISCLAIMER_TH}
    if age is not None and age < ADULT_AGE:
        return {"level": "warn", "message_th": "ต้องมีผู้ปกครองยินยอมสำหรับผู้ใช้ที่ยังไม่บรรลุนิติภาวะ " + SAFETY_DISCLAIMER_TH}
    return {"level": "ok", "message_th": SAFETY_DISCLAIMER_TH}
