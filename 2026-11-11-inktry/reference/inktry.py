"""InkTry deterministic logic (no AI calls). Sizes, fade, pain and prices are app-chosen example values — not a tattoo artist, not medical advice, and not a real tattoo."""
import datetime as _dt
import urllib.parse as _up

MIN_CONF = 0.6
FREE_TRYONS_PER_DAY = 3
WATERMARK = "Made with InkTry · preview only, not a real tattoo"
SAFETY_DISCLAIMER_TH = "InkTry เป็นภาพจำลอง ไม่ใช่รอยสักจริง และไม่ใช่คำแนะนำทางการแพทย์ ปรึกษาช่างสักที่มีใบอนุญาตและแพทย์หากมีโรคผิวหนังหรือประวัติคีลอยด์ ผู้ใช้ต้องอายุ 18 ปีขึ้นไป"
PRICE_DISCLAIMER_TH = "ราคาเป็นช่วงประมาณการที่ตั้งเอง ไม่ใช่ราคาร้านจริง ขึ้นกับช่าง รายละเอียดลาย พื้นที่ และคิวงาน"
COLOR_MODES = ["color", "bw"]
UNDERTONES = ["warm", "cool", "neutral"]
REGION_MULT = {"bkk": 1.0, "province": 0.75, "tourist": 1.15}
LEVELS = {"green": "เขียว · ลองได้", "yellow": "เหลือง · ระวัง/ปรึกษาช่าง", "red": "แดง · ยังไม่ควรสัก"}
LEVEL_RANK = {"green": 1, "yellow": 2, "red": 3}

# Placement library. pain_0_10, heal_days, size range cm, sun_factor and fade_mult are example values.
PLACEMENTS = {
    "inner_forearm": {"id": "pl01", "name_th": "แขนด้านใน", "name_en": "Inner forearm", "pain": 4, "heal_days": 14, "min_cm": 4, "max_cm": 18, "sun": 1.00, "fade_mult": 1.00, "notes_th": "เห็นง่าย ซ่อนด้วยแขนยาวได้ นิยมงานเส้นบาง"},
    "outer_forearm": {"id": "pl02", "name_th": "แขนด้านนอก", "name_en": "Outer forearm", "pain": 4, "heal_days": 14, "min_cm": 4, "max_cm": 20, "sun": 1.35, "fade_mult": 1.20, "notes_th": "โดนแดดบ่อย ต้องทาครีมกันแดดหลังสัก"},
    "wrist": {"id": "pl03", "name_th": "ข้อมือ", "name_en": "Wrist", "pain": 6, "heal_days": 14, "min_cm": 2, "max_cm": 8, "sun": 1.40, "fade_mult": 1.25, "notes_th": "พื้นที่แคบ ลายใหญ่จะเบียด"},
    "upper_arm": {"id": "pl04", "name_th": "ต้นแขน", "name_en": "Upper arm", "pain": 3, "heal_days": 14, "min_cm": 5, "max_cm": 25, "sun": 0.95, "fade_mult": 0.95, "notes_th": "เจ็บน้อย เหมาะลายขนาดกลาง–ใหญ่"},
    "shoulder": {"id": "pl05", "name_th": "หัวไหล่", "name_en": "Shoulder", "pain": 4, "heal_days": 16, "min_cm": 6, "max_cm": 22, "sun": 1.10, "fade_mult": 1.05, "notes_th": "โค้งตามหัวไหล่ ต้องให้ช่างจัดวาง"},
    "ankle": {"id": "pl06", "name_th": "ข้อเท้า", "name_en": "Ankle", "pain": 7, "heal_days": 18, "min_cm": 2, "max_cm": 10, "sun": 1.20, "fade_mult": 1.15, "notes_th": "ผิวบาง เจ็บกว่าแขน รองเท้าอาจเสียดสี"},
    "calf": {"id": "pl07", "name_th": "น่อง", "name_en": "Calf", "pain": 3, "heal_days": 16, "min_cm": 6, "max_cm": 28, "sun": 1.05, "fade_mult": 1.00, "notes_th": "พื้นที่กว้าง เจ็บน้อย"},
    "thigh": {"id": "pl08", "name_th": "ต้นขา", "name_en": "Thigh", "pain": 3, "heal_days": 16, "min_cm": 6, "max_cm": 30, "sun": 0.85, "fade_mult": 0.90, "notes_th": "ซ่อนง่าย เหมาะลายใหญ่"},
    "back": {"id": "pl09", "name_th": "แผ่นหลัง", "name_en": "Back", "pain": 3, "heal_days": 21, "min_cm": 8, "max_cm": 40, "sun": 0.80, "fade_mult": 0.85, "notes_th": "พื้นที่กว้างที่สุด หายช้ากว่าเพราะนอนทับได้"},
    "nape": {"id": "pl10", "name_th": "ท้ายทอย", "name_en": "Nape", "pain": 6, "heal_days": 14, "min_cm": 2, "max_cm": 10, "sun": 1.25, "fade_mult": 1.15, "notes_th": "ผมสั้นจะโชว์ ผมยาวซ่อนได้"},
    "ribs": {"id": "pl11", "name_th": "ซี่โครง", "name_en": "Ribs", "pain": 8, "heal_days": 21, "min_cm": 5, "max_cm": 25, "sun": 0.85, "fade_mult": 0.95, "notes_th": "เจ็บมาก หายใจแล้วผิวขยับ ควรมีประสบการณ์ก่อน"},
    "collarbone": {"id": "pl12", "name_th": "ไหปลาร้า", "name_en": "Collarbone", "pain": 7, "heal_days": 16, "min_cm": 3, "max_cm": 16, "sun": 1.20, "fade_mult": 1.10, "notes_th": "ผิวบางใกล้กระดูก ลายเส้นบางดูดี"},
    "hand": {"id": "pl13", "name_th": "หลังมือ", "name_en": "Hand", "pain": 8, "heal_days": 18, "min_cm": 2, "max_cm": 10, "sun": 1.50, "fade_mult": 1.45, "notes_th": "จางเร็ว เพราะใช้มือทั้งวันและโดนแดด"},
    "finger": {"id": "pl14", "name_th": "นิ้ว", "name_en": "Finger", "pain": 7, "heal_days": 14, "min_cm": 1, "max_cm": 4, "sun": 1.55, "fade_mult": 1.50, "notes_th": "จางเร็วมาก มักต้องสักซ้ำ"},
    "behind_ear": {"id": "pl15", "name_th": "หลังใบหู", "name_en": "Behind the ear", "pain": 6, "heal_days": 12, "min_cm": 1, "max_cm": 5, "sun": 1.15, "fade_mult": 1.10, "notes_th": "ลายเล็กเท่านั้น ซ่อนง่าย"},
}

STYLES = {
    "fine_line": {"id": "st01", "name_th": "เส้นบาง (Fine line)", "name_en": "Fine line", "color_ok": True, "bw_ok": True, "price_mult": 1.00, "fade_per_year": 12, "spread_mult": 1.30, "notes_th": "ดูบางและเรียบ แต่จางและเบลอเร็วกว่างานเส้นหนา"},
    "traditional": {"id": "st02", "name_th": "แบบดั้งเดิม (Traditional)", "name_en": "Traditional", "color_ok": True, "bw_ok": True, "price_mult": 1.20, "fade_per_year": 6, "spread_mult": 0.90, "notes_th": "เส้นหนา สีแน่น อยู่ทน"},
    "watercolor": {"id": "st03", "name_th": "สีน้ำ (Watercolor)", "name_en": "Watercolor", "color_ok": True, "bw_ok": False, "price_mult": 1.30, "fade_per_year": 15, "spread_mult": 1.40, "notes_th": "สีฟุ้งสวยตอนใหม่ แต่จางเร็ว ต้องเก็บรายละเอียด"},
    "geometric": {"id": "st04", "name_th": "เรขาคณิต", "name_en": "Geometric", "color_ok": True, "bw_ok": True, "price_mult": 1.10, "fade_per_year": 7, "spread_mult": 1.00, "notes_th": "ต้องวางให้สมมาตรตามส่วนโค้งของร่างกาย"},
    "script": {"id": "st05", "name_th": "ตัวอักษร", "name_en": "Script", "color_ok": True, "bw_ok": True, "price_mult": 0.95, "fade_per_year": 10, "spread_mult": 1.20, "notes_th": "ตัวเล็กเกินไปจะอ่านไม่ออกเมื่อจาง"},
    "floral": {"id": "st06", "name_th": "ดอกไม้ / พฤกษา", "name_en": "Floral / botanical", "color_ok": True, "bw_ok": True, "price_mult": 1.10, "fade_per_year": 8, "spread_mult": 1.10, "notes_th": "นิยมเส้นบางหรือสีอ่อน ควรเว้นระยะให้ดอกไม่ชนกัน"},
    "animal": {"id": "st07", "name_th": "สัตว์ / เหมือนจริง", "name_en": "Animal / realism", "color_ok": True, "bw_ok": True, "price_mult": 1.35, "fade_per_year": 7, "spread_mult": 1.00, "notes_th": "ใช้เวลาเยอะ ราคาสูงกว่า เพราะรายละเอียดมาก"},
    "minimal": {"id": "st08", "name_th": "มินิมอล", "name_en": "Minimal", "color_ok": True, "bw_ok": True, "price_mult": 0.90, "fade_per_year": 11, "spread_mult": 1.25, "notes_th": "ลายเล็กเรียบ แต่ง่ายจาง ต้องไม่เล็กเกิน"},
    "blackwork": {"id": "st09", "name_th": "แบล็ควอร์ก เข้ม", "name_en": "Blackwork", "color_ok": False, "bw_ok": True, "price_mult": 1.25, "fade_per_year": 5, "spread_mult": 0.85, "notes_th": "พื้นที่ดำแน่น อยู่ทน แต่เจ็บและบวมกว่า"},
    "dotwork": {"id": "st10", "name_th": "จุด (Dotwork)", "name_en": "Dotwork", "color_ok": True, "bw_ok": True, "price_mult": 1.15, "fade_per_year": 8, "spread_mult": 1.05, "notes_th": "เงาจากจุด ใช้เวลา ต้องช่างที่ถนัดเทคนิคนี้"},
}

DESIGNS = {
    "d01": {"name_th": "ช่อใบโอลิฟ์เส้นบาง", "name_en": "Fine-line olive sprig", "style": "fine_line", "default_mode": "bw", "tags": ["botanical", "fine"]},
    "d02": {"name_th": "ดอกโบตั๋น", "name_en": "Peony", "style": "floral", "default_mode": "color", "tags": ["floral", "color"]},
    "d03": {"name_th": "พระจันทร์บาง", "name_en": "Slim crescent", "style": "minimal", "default_mode": "bw", "tags": ["minimal", "moon"]},
    "d04": {"name_th": "คลื่นเรขา", "name_en": "Geometric wave", "style": "geometric", "default_mode": "bw", "tags": ["geo"]},
    "d05": {"name_th": "มังกรเล็ก", "name_en": "Small dragon", "style": "traditional", "default_mode": "color", "tags": ["animal", "classic"]},
    "d06": {"name_th": "ข้อความสั้น", "name_en": "Short script", "style": "script", "default_mode": "bw", "tags": ["text"]},
    "d07": {"name_th": "นกกระเรียน", "name_en": "Crane", "style": "watercolor", "default_mode": "color", "tags": ["bird", "wash"]},
    "d08": {"name_th": "แมวเส้นบาง", "name_en": "Fine-line cat", "style": "fine_line", "default_mode": "bw", "tags": ["animal", "fine"]},
    "d09": {"name_th": "แถบแบล็ควork", "name_en": "Blackwork band", "style": "blackwork", "default_mode": "bw", "tags": ["band"]},
    "d10": {"name_th": "ดาวจุด", "name_en": "Dotwork star", "style": "dotwork", "default_mode": "bw", "tags": ["star"]},
    "d11": {"name_th": "เถาวัลย์ข้อมือ", "name_en": "Wrist vine", "style": "fine_line", "default_mode": "bw", "tags": ["botanical", "wrap"]},
    "d12": {"name_th": "ปลาคราฟ", "name_en": "Koi", "style": "traditional", "default_mode": "color", "tags": ["animal"]},
}

SIZE_BANDS = (
    (3, "tiny", "จิ๋ว"),
    (8, "small", "เล็ก"),
    (15, "medium", "กลาง"),
    (25, "large", "ใหญ่"),
    (999, "xl", "ใหญ่พิเศษ / แขน"),
)

CONTRA = {
    "under_18": {"level": "red", "text_th": "ผู้ใช้ต้องอายุ 18 ปีขึ้นไป จึงยังไม่ควรสัก"},
    "pregnancy": {"level": "red", "text_th": "ตั้งครรภ์หรือให้นม ควรเลื่อนและปรึกษาแพทย์ก่อน"},
    "keloid": {"level": "red", "text_th": "มีประวัติคีลอยด์ — ปรึกษาแพทย์ผิวหนังและช่างก่อน ไม่ควรสักเองตามแฟชั่น"},
    "infection": {"level": "red", "text_th": "มีแผลติดเชื้อหรือผิวหนังอักเสบในจุดที่จะสัก — รักษาให้หายก่อน"},
    "blood_thinner": {"level": "yellow", "text_th": "ใช้ยาละลายลิ่มเลือดหรือมีโรคเลือด — ต้องให้แพทย์อนุญาตก่อน"},
    "allergy_ink": {"level": "yellow", "text_th": "เคยแพ้สีสักหรือนิเกิล — ขอปatch test กับช่าง"},
    "sunburn": {"level": "yellow", "text_th": "ผิวไหม้แดดหรือเพิ่งผลัดผิวในจุดนั้น — รอให้ผิวฟื้นก่อน"},
    "none": {"level": "green", "text_th": "ไม่มีข้อควรระวังที่เลือกไว้ แต่ยังต้องให้ช่างประเมินผิวจริง"},
}

AFTERCARE = [
    "ล้างมือก่อนแตะรอยสัก ล้างด้วยน้ำสะอาดและสบู่อ่อนตามที่ช่างแนะนำ",
    "เช็ดซับ ไม่ถู และทาครีมที่ช่างให้ในชั้นบาง ๆ",
    "อย่าแกะสะเก็ด อย่าแช่น้ำนาน งดสระในสระ/ทะเลอย่างน้อย 2 สัปดาห์ (ตามช่าง)",
    "ใส่เสื้อหลวม ไม่ให้ผ้าเสียดสีโดยตรงช่วงแรก",
    "กันแดดเมื่อผิวปิดแล้ว ทาครีมกันแดดทุกครั้งที่ออกแดด เพื่อให้สีนานขึ้น",
    "ถ้าบวม แดง ร้อนขึ้น หรือมีหนอง ให้พบแพทย์ ไม่ทายาเองมั่ว",
]

ARTIST_QUESTIONS = [
    "ช่างมีใบอนุญาตและใช้เข็ม/สีแบบสักครั้งเดียวทิ้งหรือไม่",
    "ลายนี้ปรับขนาดและวางบนส่วนโค้งของฉันอย่างไร",
    "สีนี้จางประมาณกี่ปี และมีรอบเติมฟรีหรือคิดเท่าไร",
    "ช่วงพักฟื้นกี่วัน ห้ามทำอะไรบ้าง",
    "ราคานี้รวมออกแบบ ลงสี และภาษีแล้วหรือยัง",
]

BASE_PER_CM = 400
MIN_CHARGE = 1500


def size_band(size_cm):
    if size_cm <= 0:
        raise ValueError("size_cm must be > 0")
    for limit, key, label in SIZE_BANDS:
        if size_cm <= limit:
            return {"key": key, "label_th": label}
    return {"key": "xl", "label_th": "ใหญ่พิเศษ / แขน"}


def scan_quality(glare, blur, tilt, skin_visible):
    for v in (glare, blur, tilt, skin_visible):
        if not 0 <= v <= 1:
            raise ValueError("glare/blur/tilt/skin_visible must be 0..1")
    score = round(100 * (1 - (0.35 * glare + 0.35 * blur + 0.20 * tilt + 0.10 * (1 - skin_visible))))
    tips = []
    if glare > 0.5:
        tips.append("แสงสะท้อนบนผิวเยอะ ลองหันออกจากไฟหรือบังแดด")
    if blur > 0.4:
        tips.append("ภาพเบลอ ถือมือถือให้นิ่ง แตะโฟกัสที่ผิว")
    if tilt > 0.4:
        tips.append("ถ่ายเอียงเกินไป ถ่ายตั้งฉากกับผิว")
    if skin_visible < 0.5:
        tips.append("เห็นผิวน้อยไป ดึงแขนเสื้อ/จัดมุมให้ผิวที่ต้องการสักเต็มกรอบ")
    ok = score >= 60 and skin_visible >= 0.5
    if not ok and not tips:
        tips.append("ถ่ายใหม่ให้ผิวชัด แสงนุ่ม และตั้งฉากกับกล้อง")
    return {"score": score, "ok": ok, "tips_th": tips}


def identify_placement(photo, min_conf=MIN_CONF):
    found, uncertain = [], []
    for d in photo["detections"]:
        pl = d["placement"]
        if pl not in PLACEMENTS:
            raise ValueError("unknown placement " + pl)
        if d["confidence"] < min_conf:
            uncertain.append(pl)
            continue
        info = PLACEMENTS[pl]
        found.append({
            "placement": pl, "name_th": info["name_th"], "name_en": info["name_en"],
            "confidence": d["confidence"], "side": d.get("side", "unknown"),
        })
    return {"placements": found, "uncertain": uncertain}


def skin_scan(photo):
    q = scan_quality(photo["glare"], photo["blur"], photo["tilt"], photo["skin_visible"])
    ident = identify_placement(photo)
    return {
        "photo_id": photo["id"], "quality": q, "placements": ident["placements"],
        "uncertain": ident["uncertain"], "placement_count": len(ident["placements"]),
        "undertone": photo.get("undertone", "neutral"),
    }


def pipeline_steps(photo):
    s = ["skin_detect"]
    if photo["glare"] > 0.5:
        s.append("deglare")
    if photo["tilt"] > 0.4:
        s.append("deskew")
    s += ["placement_classify", "overlay", "size_check", "aging_preview", "artist_card"]
    return s


def _require(placement, style, color_mode):
    if placement not in PLACEMENTS:
        raise ValueError("unknown placement " + placement)
    if style not in STYLES:
        raise ValueError("unknown style " + style)
    if color_mode not in COLOR_MODES:
        raise ValueError("color_mode must be color or bw")
    st = STYLES[style]
    if color_mode == "color" and not st["color_ok"]:
        raise ValueError(style + " does not support color")
    if color_mode == "bw" and not st["bw_ok"]:
        raise ValueError(style + " does not support black and white")
    return PLACEMENTS[placement], st


def size_check(placement, size_cm):
    if placement not in PLACEMENTS:
        raise ValueError("unknown placement " + placement)
    if size_cm <= 0:
        raise ValueError("size_cm must be > 0")
    p = PLACEMENTS[placement]
    band = size_band(size_cm)
    in_range = p["min_cm"] <= size_cm <= p["max_cm"]
    if size_cm < p["min_cm"]:
        verdict = "too_small"
        message_th = f"เล็กไปสำหรับ{p['name_th']} แนะนำ {p['min_cm']}–{p['max_cm']} ซม. จะได้ไม่จางจนอ่านไม่ออก"
    elif size_cm > p["max_cm"]:
        verdict = "too_big"
        message_th = f"ใหญ่ไปสำหรับ{p['name_th']} แนะนำ {p['min_cm']}–{p['max_cm']} ซม. หรือย้ายไปตำแหน่งที่กว้างกว่า"
    else:
        verdict = "ok"
        message_th = f"ขนาด {size_cm} ซม. อยู่ในช่วงที่เหมาะกับ{p['name_th']} ({p['min_cm']}–{p['max_cm']} ซม.)"
    wrap_th = "ส่วนนี้โค้ง ต้องให้ช่างวางลายตามแนวกระดูก/กล้ามเนื้อ" if placement in ("wrist", "ankle", "shoulder", "collarbone", "finger", "nape") else "ผิวค่อนข้างเรียบ วางลายตรงได้"
    return {
        "placement": placement, "size_cm": size_cm, "band": band["key"], "band_th": band["label_th"],
        "min_cm": p["min_cm"], "max_cm": p["max_cm"], "in_range": in_range, "verdict": verdict,
        "message_th": message_th, "wrap_th": wrap_th,
    }


def contrast_score(undertone, color_mode, style):
    if undertone not in UNDERTONES:
        raise ValueError("unknown undertone")
    base = 78
    if color_mode == "bw":
        base += 6 if undertone == "warm" else 4 if undertone == "neutral" else 2
    else:
        base += 8 if undertone == "cool" else 5 if undertone == "neutral" else 2
        if style == "watercolor":
            base += 2
        if style == "blackwork":
            base -= 4
    if style in ("fine_line", "minimal", "script"):
        base -= 4
    return max(40, min(96, base))


def color_variants(design_id, undertone, placement, size_cm):
    if design_id not in DESIGNS:
        raise ValueError("unknown design " + design_id)
    d = DESIGNS[design_id]
    style = d["style"]
    variants = []
    st = STYLES[style]
    for mode in COLOR_MODES:
        if mode == "color" and not st["color_ok"]:
            continue
        if mode == "bw" and not st["bw_ok"]:
            continue
        variants.append({
            "design_id": design_id, "style": style, "color_mode": mode,
            "label_th": "ขาวดำ" if mode == "bw" else "ลงสี",
            "contrast": contrast_score(undertone, mode, style),
            "recommended": mode == d["default_mode"],
        })
    variants.sort(key=lambda v: (-v["contrast"], v["color_mode"]))
    return {
        "design_id": design_id, "name_th": d["name_th"], "style": style, "undertone": undertone,
        "placement": placement, "size_cm": size_cm, "variants": variants,
        "best_mode": variants[0]["color_mode"] if variants else None,
    }


def overlay_tryon(photo, design_id, placement, size_cm, color_mode):
    if design_id not in DESIGNS:
        raise ValueError("unknown design " + design_id)
    d = DESIGNS[design_id]
    style = d["style"]
    _require(placement, style, color_mode)
    scan = skin_scan(photo)
    chk = size_check(placement, size_cm)
    contrast = contrast_score(photo.get("undertone", "neutral"), color_mode, style)
    matched = any(p["placement"] == placement for p in scan["placements"])
    return {
        "photo_id": photo["id"], "design_id": design_id, "name_th": d["name_th"],
        "placement": placement, "placement_th": PLACEMENTS[placement]["name_th"],
        "size_cm": size_cm, "style": style, "color_mode": color_mode,
        "contrast": contrast, "size_verdict": chk["verdict"],
        "placement_matched": matched, "quality": scan["quality"],
        "watermark": WATERMARK, "disclaimer_th": SAFETY_DISCLAIMER_TH,
    }


def aging_preview(style, color_mode, placement, years, size_cm=8):
    p, st = _require(placement, style, color_mode)
    if years not in (1, 5, 10) and not (isinstance(years, int) and 1 <= years <= 15):
        raise ValueError("years must be 1..15")
    color_f = 1.15 if color_mode == "color" else 1.0
    # Fine / small work fades a little faster.
    size_f = 1.15 if size_cm <= 3 else 1.0
    fade = min(90, int(round(st["fade_per_year"] * years * p["fade_mult"] * p["sun"] * color_f * size_f / 1.0)))
    spread_mm = round(0.15 * years * st["spread_mult"] * (1.1 if size_cm <= 3 else 1.0), 2)
    sharpness = max(10, 100 - fade)
    if fade >= 70:
        look_th = "จางและเบลอชัด อาจอ่านรายละเอียดเล็กไม่ออก ควรคุยเรื่องเติมลาย"
    elif fade >= 45:
        look_th = "สีซีดลง ขอบลายเริ่มนุ่ม ยังมองออกแต่ไม่คมเท่าวันสัก"
    else:
        look_th = "ยังคมอยู่ อาจซีดเล็กน้อยตามแดดและการดูแล"
    return {
        "style": style, "color_mode": color_mode, "placement": placement, "years": years, "size_cm": size_cm,
        "fade_pct": fade, "spread_mm": spread_mm, "sharpness_left": sharpness,
        "look_th": look_th,
        "care_th": "ทาครีมกันแดดและเลี่ยงการแกะสะเก็ดจะช่วยให้จางช้าลง (ค่าจำลอง ไม่ใช่ผลจริง)",
        "disclaimer_th": "การจำลองความเก่าเป็นค่าตัวอย่าง ไม่ใช่ผลที่รับประกันบนผิวจริง",
    }


def pain_guide(placement):
    if placement not in PLACEMENTS:
        raise ValueError("unknown placement " + placement)
    p = PLACEMENTS[placement]
    if p["pain"] >= 7:
        level, tip = "high", "เจ็บมากเป็นปกติในจุดที่ผิวบางหรือใกล้กระดูก พักได้ และอย่าฝืนหิว"
    elif p["pain"] >= 5:
        level, tip = "medium", "เจ็บปานกลาง หายใจช้า ๆ และบอกช่างถ้าต้องการพัก"
    else:
        level, tip = "low", "โดยทั่วไปเจ็บน้อยกว่าจุดอื่น แต่ความทนของแต่ละคนต่างกัน"
    return {
        "placement": placement, "name_th": p["name_th"], "pain": p["pain"], "pain_max": 10,
        "level": level, "heal_days": p["heal_days"], "tip_th": tip, "notes_th": p["notes_th"],
        "disclaimer_th": "ระดับความเจ็บเป็นค่าเฉลี่ยอย่างหยาบ แต่ละคนต่างกัน ไม่ใช่การวินิจฉัย",
    }


def aftercare_guide():
    return {
        "title_th": "ดูแลรอยสักช่วงแรก",
        "days": 14,
        "steps": [{"n": i + 1, "text_th": t} for i, t in enumerate(AFTERCARE)],
        "disclaimer_th": "ทำตามคำช่างและแพทย์เป็นหลัก คู่มือนี้เป็นแนวทางทั่วไป",
    }


def _round50(x):
    return int(round(x / 50.0) * 50)


def price_range(size_cm, style, region, color_mode, placement="inner_forearm"):
    p, st = _require(placement, style, color_mode)
    if region not in REGION_MULT:
        raise ValueError("unknown region")
    if size_cm <= 0:
        raise ValueError("size_cm must be > 0")
    raw = size_cm * BASE_PER_CM * st["price_mult"] * (1.15 if color_mode == "color" else 1.0) * REGION_MULT[region]
    mid = max(MIN_CHARGE, _round50(raw))
    # Tiny floor stays 1500; range around mid.
    mn = max(MIN_CHARGE, _round50(mid * 0.80))
    mx = _round50(mid * 1.40)
    if mx <= mn:
        mx = mn + 500
    return {
        "style": style, "placement": placement, "size_cm": size_cm, "region": region, "color_mode": color_mode,
        "mid_thb": mid, "min_thb": mn, "max_thb": mx, "currency": "THB",
        "name_th": st["name_th"], "disclaimer_th": PRICE_DISCLAIMER_TH,
    }


def quote_check(quote_thb, size_cm, style, region, color_mode, placement="inner_forearm"):
    if quote_thb < 0:
        raise ValueError("quote must be >= 0")
    pr = price_range(size_cm, style, region, color_mode, placement)
    q = quote_thb
    if q < pr["min_thb"] * 0.85:
        verdict, message_th = "low", "ต่ำกว่าช่วงประมาณการมาก ถามให้ชัดว่า inclusive อะไร และมาตรฐานความสะอาด"
    elif q <= pr["max_thb"]:
        if q < pr["min_thb"]:
            verdict, message_th = "low", "ต่ำกว่าช่วงประมาณการเล็กน้อย เช็กประสบการณ์ช่างและสิ่งที่รวมในราคา"
        elif q <= pr["mid_thb"] * 1.15:
            verdict, message_th = "fair", "อยู่ในช่วงสมเหตุสมผลเมื่อเทียบกับค่าประมาณการของแอป"
        else:
            verdict, message_th = "high", "ค่อนข้างสูงกว่าค่ากลาง ยังอยู่ในช่วง แต่ควรถามรายละเอียดงานและรอบเติม"
    else:
        verdict, message_th = "very_high", "สูงกว่าช่วงประมาณการมาก ขอใบเสนอราคาแยกออกแบบ/ลงสี/เติมลาย"
    return {
        "quote_thb": q, "min_thb": pr["min_thb"], "max_thb": pr["max_thb"], "mid_thb": pr["mid_thb"],
        "verdict": verdict, "message_th": message_th, "questions_th": ARTIST_QUESTIONS,
        "disclaimer_th": PRICE_DISCLAIMER_TH,
    }


def safety_from_flags(flags, age):
    flags = list(flags) or ["none"]
    if age < 18 or "under_18" in flags:
        flags = [f for f in flags if f != "none"]
        if "under_18" not in flags:
            flags = ["under_18"] + flags
    unknown = [f for f in flags if f not in CONTRA]
    if unknown:
        raise ValueError("unknown flag " + unknown[0])
    ranked = flags if flags else ["none"]
    top = max(ranked, key=lambda f: LEVEL_RANK[CONTRA[f]["level"]])
    reasons = [CONTRA[f]["text_th"] for f in ranked if f != "none" or len(ranked) == 1]
    return {
        "level": CONTRA[top]["level"], "can_book": CONTRA[top]["level"] != "red",
        "flags": ranked, "reasons_th": reasons, "disclaimer_th": SAFETY_DISCLAIMER_TH,
    }


def safety_guard(level):
    if level == "red":
        return {"level": "stop", "message_th": "ยังไม่ควรนัดสักในตอนนี้ " + SAFETY_DISCLAIMER_TH}
    if level == "yellow":
        return {"level": "warn", "message_th": "ควรปรึกษาแพทย์หรือช่างก่อนนัด " + SAFETY_DISCLAIMER_TH}
    return {"level": "ok", "message_th": SAFETY_DISCLAIMER_TH}


def artist_card(person, tryon, price, aging5, flags=(), note_th=""):
    rec = safety_from_flags(flags, person["age"])
    text = (
        f"InkTry — บรีฟช่างสัก\n"
        f"{person['name_th']} · {tryon['name_th']} ({tryon['style']}, {'ขาวดำ' if tryon['color_mode']=='bw' else 'ลงสี'})\n"
        f"ตำแหน่ง: {tryon['placement_th']} · ขนาด {tryon['size_cm']} ซม.\n"
        f"งบประมาณโดยประมาณ: ฿{price['min_thb']:,}–{price['max_thb']:,}\n"
        f"พรีวิวอายุ 5 ปี (จำลอง): จาง {aging5['fade_pct']}% เบลอ {aging5['spread_mm']} มม.\n"
        f"{note_th}".strip()
    )
    return {
        "title_th": "การ์ดบรีฟช่างสัก",
        "name_th": person["name_th"],
        "design_th": tryon["name_th"],
        "style": tryon["style"],
        "color_mode": tryon["color_mode"],
        "placement": tryon["placement"],
        "placement_th": tryon["placement_th"],
        "size_cm": tryon["size_cm"],
        "budget_min_thb": price["min_thb"],
        "budget_max_thb": price["max_thb"],
        "aging_5y_fade_pct": aging5["fade_pct"],
        "note_th": note_th,
        "questions_th": ARTIST_QUESTIONS,
        "line_share_url": "https://line.me/R/share?text=" + _up.quote(text),
        "can_book": rec["can_book"],
        "disclaimer_th": SAFETY_DISCLAIMER_TH + " " + PRICE_DISCLAIMER_TH,
    }


def share_card(name_th, tryon, aging5=None):
    hook = "ลองรอยสักบนตัวก่อนสักจริง"
    if aging5:
        hook = f"พรีวิว 5 ปี · จาง {aging5['fade_pct']}% (จำลอง)"
    return {
        "title_th": f"InkTry — {name_th}",
        "headline_th": f"{tryon['name_th']} ที่{tryon['placement_th']} {tryon['size_cm']} ซม.",
        "hook_th": hook,
        "placement": tryon["placement"],
        "style": tryon["style"],
        "color_mode": tryon["color_mode"],
        "layout": "tryon_result",
        "sizes": ["1080x1350", "1080x1920", "1080x1080"],
        "watermark": WATERMARK,
        "cta_th": "คอมเมนต์ INK รับแพ็กฟรี",
    }


def quota(used_today, want, pro=False):
    if pro:
        return {"allowed": want, "left_after": None, "paywall": False}
    left = max(0, FREE_TRYONS_PER_DAY - used_today)
    allowed = min(want, left)
    return {"allowed": allowed, "left_after": left - allowed, "paywall": allowed < want}


def design_info(design_id):
    if design_id not in DESIGNS:
        raise ValueError("unknown design " + design_id)
    d = DESIGNS[design_id]
    st = STYLES[d["style"]]
    return {
        "id": design_id, "name_th": d["name_th"], "name_en": d["name_en"],
        "style": d["style"], "style_th": st["name_th"], "default_mode": d["default_mode"],
        "tags": d["tags"], "color_ok": st["color_ok"], "bw_ok": st["bw_ok"], "notes_th": st["notes_th"],
    }


def placement_info(placement):
    if placement not in PLACEMENTS:
        raise ValueError("unknown placement " + placement)
    p = PLACEMENTS[placement]
    return {
        "id": p["id"], "placement": placement, "name_th": p["name_th"], "name_en": p["name_en"],
        "pain": p["pain"], "heal_days": p["heal_days"], "min_cm": p["min_cm"], "max_cm": p["max_cm"],
        "notes_th": p["notes_th"],
    }


def diary_entry(eid, person_id, date, design_id, placement, size_cm, status, shop_th, cost_thb, on_device=True):
    if status not in ("wishlist", "booked", "done", "touch_up"):
        raise ValueError("bad status")
    return {
        "id": eid, "person_id": person_id, "date": date, "design_id": design_id,
        "placement": placement, "size_cm": size_cm, "status": status,
        "shop_th": shop_th, "cost_thb": cost_thb, "on_device": on_device,
    }


def diary_stats(entries):
    if not entries:
        return {"count": 0, "total_thb": 0, "avg_thb": 0, "last_date": None, "top_placement": None}
    done = [e for e in entries if e["status"] in ("done", "touch_up")]
    total = sum(e["cost_thb"] for e in done)
    last = max(entries, key=lambda e: e["date"])["date"]
    from collections import Counter
    c = Counter(e["placement"] for e in entries)
    top = c.most_common(1)[0][0] if c else None
    return {
        "count": len(entries), "total_thb": total,
        "avg_thb": int(round(total / len(done))) if done else 0,
        "last_date": last, "top_placement": top,
    }
