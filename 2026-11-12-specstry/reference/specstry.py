"""SpecsTry deterministic logic (no AI calls). PD, sizes, fit scores and prices are app-chosen example values — not an eye exam, not a prescription, and not an optician."""
import urllib.parse as _up

MIN_CONF = 0.6
FREE_TRYONS_PER_DAY = 3
WATERMARK = "Made with SpecsTry · preview only, not an eye exam"
SAFETY_DISCLAIMER_TH = "SpecsTry เป็นภาพจำลองสำหรับลองกรอบแว่นเท่านั้น ไม่ใช่การตรวจสายตา ไม่ใช่ใบสั่งแว่น และไม่ใช่คำแนะนำจากแพทย์/นักทัศนมาตร วัด PD และค่าสายตาจริงที่ร้านแว่นหรือคลินิกก่อนตัดเลนส์"
PRICE_DISCLAIMER_TH = "ราคาเป็นช่วงประมาณการที่ตั้งเอง ไม่ใช่ราคาร้านจริง ขึ้นกับแบรนด์ เลนส์ เคลือบและพื้นที่"
UNDERTONES = ["warm", "cool", "neutral"]
REGION_MULT = {"bkk": 1.0, "province": 0.80, "tourist": 1.20}
FACE_SHAPES = ["oval", "round", "square", "heart", "oblong", "diamond"]
SHAPE_TH = {"oval": "หน้าไข่", "round": "หน้ากลม", "square": "หน้าเหลี่ยม", "heart": "หน้าหัวใจ", "oblong": "หน้ายาว", "diamond": "หน้าเพชร"}
LIFESTYLES = ["office", "outdoor", "sport", "casual", "fashion"]
LIFE_TH = {"office": "ออฟฟิศ", "outdoor": "กลางแจ้ง", "sport": "กีฬา", "casual": "ทุกวัน", "fashion": "แฟชั่น"}
LENS_TYPES = {
    "single": {"name_th": "เลนส์มองระยะเดียว", "add_thb": 900, "notes_th": "สำหรับค่าสายตาที่ร้านวัดให้ ไม่ใช่ค่าจากแอป"},
    "progressive": {"name_th": "เลนส์โปรเกรสซีฟ", "add_thb": 4500, "notes_th": "ต้องวัดและประกอบที่ร้านเท่านั้น"},
    "blue_light": {"name_th": "กรองแสงน้ำเงิน (ค่าประมาณ)", "add_thb": 1200, "notes_th": "เคลือบเพิ่ม ไม่ใช่การรักษาอาการตา"},
    "photochromic": {"name_th": "เลนส์ปรับแสง", "add_thb": 2500, "notes_th": "ความมืดในแดดจริงขึ้นกับยี่ห้อ"},
    "sun": {"name_th": "เลนส์กันแดด", "add_thb": 1500, "notes_th": "ไม่ใช่แว่นเซฟตี้หรือแว่นเชื่อม"},
}
MATERIALS = ["metal", "acetate", "titanium", "rimless"]
MAT_TH = {"metal": "โลหะ", "acetate": "อะซิเตท", "titanium": "ไทเทเนียม", "rimless": "ไร้ขอบ"}

# Frame library. Sizes in mm are example inventory, not a real catalogue.
FRAMES = {
    "f01": {"name_th": "กลมบางโลหะ", "name_en": "Thin metal round", "shape": "round", "material": "metal",
            "lens_width": 48, "bridge": 20, "temple": 140, "color": "gold", "base_thb": 2200,
            "best_shapes": ["oval", "square", "heart"], "lifestyle": ["office", "casual", "fashion"]},
    "f02": {"name_th": "เหลี่ยมอะซิเตทเข้ม", "name_en": "Dark acetate rectangle", "shape": "rectangle", "material": "acetate",
            "lens_width": 52, "bridge": 18, "temple": 145, "color": "black", "base_thb": 2800,
            "best_shapes": ["oval", "round", "oblong"], "lifestyle": ["office", "casual"]},
    "f03": {"name_th": "แคทอายลายหินอ่อน", "name_en": "Marble cat-eye", "shape": "cat_eye", "material": "acetate",
            "lens_width": 50, "bridge": 18, "temple": 140, "color": "tortoise", "base_thb": 3200,
            "best_shapes": ["oval", "heart", "diamond"], "lifestyle": ["fashion", "casual"]},
    "f04": {"name_th": "สแควร์ไทเทเนียม", "name_en": "Titanium square", "shape": "square", "material": "titanium",
            "lens_width": 51, "bridge": 19, "temple": 145, "color": "silver", "base_thb": 4900,
            "best_shapes": ["oval", "round"], "lifestyle": ["office", "fashion"]},
    "f05": {"name_th": "โบรว์ไลน์คลาสสิก", "name_en": "Classic browline", "shape": "browline", "material": "metal",
            "lens_width": 50, "bridge": 20, "temple": 145, "color": "black_gold", "base_thb": 3500,
            "best_shapes": ["oval", "round", "oblong"], "lifestyle": ["office", "casual"]},
    "f06": {"name_th": "เอวิเอเตอร์บาง", "name_en": "Slim aviator", "shape": "aviator", "material": "metal",
            "lens_width": 54, "bridge": 16, "temple": 140, "color": "silver", "base_thb": 2600,
            "best_shapes": ["oval", "square", "heart"], "lifestyle": ["outdoor", "fashion", "casual"]},
    "f07": {"name_th": "ไข่บางไร้ขอบ", "name_en": "Rimless oval", "shape": "oval", "material": "rimless",
            "lens_width": 49, "bridge": 19, "temple": 140, "color": "clear", "base_thb": 3800,
            "best_shapes": ["oval", "square", "diamond", "heart"], "lifestyle": ["office"]},
    "f08": {"name_th": "กลมอะซิเตทใหญ่", "name_en": "Chunky acetate round", "shape": "round", "material": "acetate",
            "lens_width": 50, "bridge": 22, "temple": 150, "color": "honey", "base_thb": 3000,
            "best_shapes": ["square", "heart", "diamond"], "lifestyle": ["fashion", "casual"]},
    "f09": {"name_th": "สปอร์ตโค้ง", "name_en": "Wrap sport", "shape": "wrap", "material": "acetate",
            "lens_width": 55, "bridge": 16, "temple": 130, "color": "black", "base_thb": 2400,
            "best_shapes": ["oval", "oblong", "square"], "lifestyle": ["sport", "outdoor"]},
    "f10": {"name_th": "เหลี่ยมแคบสั้น", "name_en": "Narrow short rectangle", "shape": "rectangle", "material": "metal",
            "lens_width": 44, "bridge": 18, "temple": 135, "color": "black", "base_thb": 1900,
            "best_shapes": ["round"], "lifestyle": ["office"]},
    "f11": {"name_th": " visor กว้างพิเศษ", "name_en": "Extra-wide fashion", "shape": "rectangle", "material": "acetate",
            "lens_width": 58, "bridge": 20, "temple": 150, "color": "clear", "base_thb": 3300,
            "best_shapes": ["oblong"], "lifestyle": ["fashion"]},
    "f12": {"name_th": "กลมมินิมอลเงิน", "name_en": "Minimal silver round", "shape": "round", "material": "titanium",
            "lens_width": 47, "bridge": 21, "temple": 140, "color": "silver", "base_thb": 4200,
            "best_shapes": ["oval", "square", "heart"], "lifestyle": ["office", "fashion", "casual"]},
}
# fix typo in f11 name
FRAMES["f11"]["name_th"] = "กรอบกว้างพิเศษ"

ENDPIECE_EACH = 8  # example mm added for both endpieces, not a real caliper

def frame_front_width(frame):
    return frame["lens_width"] * 2 + frame["bridge"] + ENDPIECE_EACH * 2

def scan_quality(glare, blur, tilt, face_fill, eyes_visible):
    for v in (glare, blur, tilt, face_fill, eyes_visible):
        if not 0 <= v <= 1:
            raise ValueError("quality inputs must be 0..1")
    score = round(100 * (1 - (0.25 * glare + 0.30 * blur + 0.20 * tilt + 0.15 * (1 - face_fill) + 0.10 * (1 - eyes_visible))))
    tips = []
    if glare > 0.5:
        tips.append("แสงสะท้อนบนหน้าเยอะ หันออกจากหน้าต่างหรือไฟ")
    if blur > 0.4:
        tips.append("ภาพเบลอ ถือนิ่ง แตะโฟกัสที่ดวงตา")
    if tilt > 0.35:
        tips.append("หน้าเอียงเกินไป ถ่ายหน้าตรง กล้องระดับสายตา")
    if face_fill < 0.55:
        tips.append("หน้าเล็กไปในกรอบ เข้าใกล้ขึ้นอีกนิด")
    if eyes_visible < 0.6:
        tips.append("ไม่เห็นตาทั้งสองข้าง ถอดหน้ากากและเก็บผมออกจากหน้า")
    ok = score >= 60 and eyes_visible >= 0.6 and face_fill >= 0.5
    if not ok and not tips:
        tips.append("ถ่ายใหม่ หน้าตรง แสงนุ่ม เห็นตาทั้งสองข้าง")
    return {"score": score, "ok": ok, "tips_th": tips}

def face_shape(length_mm, forehead_mm, cheek_mm, jaw_mm):
    for v in (length_mm, forehead_mm, cheek_mm, jaw_mm):
        if v <= 0:
            raise ValueError("measurements must be > 0")
    lw = length_mm / cheek_mm
    if lw >= 1.50:
        key = "oblong"
    elif lw <= 1.18 and abs(forehead_mm - jaw_mm) <= 8 and abs(cheek_mm - jaw_mm) <= 8:
        key = "round"
    elif abs(forehead_mm - cheek_mm) <= 6 and abs(jaw_mm - cheek_mm) <= 6 and lw <= 1.28:
        key = "square"
    elif forehead_mm >= cheek_mm - 2 and (cheek_mm - jaw_mm) >= 10:
        key = "heart"
    elif cheek_mm >= forehead_mm + 6 and cheek_mm >= jaw_mm + 6 and lw >= 1.22:
        key = "diamond"
    else:
        key = "oval"
    return {
        "shape": key, "shape_th": SHAPE_TH[key],
        "length_mm": length_mm, "forehead_mm": forehead_mm, "cheek_mm": cheek_mm, "jaw_mm": jaw_mm,
        "length_to_width": round(lw, 2),
        "advice_th": {
            "oval": "หน้าไข่เข้าได้หลายทรง ลองทั้งกลมและเหลี่ยมแล้วเทียบกัน",
            "round": "เลือกทรงเหลี่ยมหรือสแควร์ เพื่อเพิ่มเส้นมุม",
            "square": "เลือกทรงกลมหรือไข่ เพื่อทำให้นุ่มขึ้น",
            "heart": "เลือกแคทอาย กลม หรือไร้ขอบ เลี่ยงบนกว้างล่างแคบเกิน",
            "oblong": "เลือกกรอบสูงหรือมีคิ้วบน เพื่อไม่ให้หน้าดูยาวขึ้น",
            "diamond": "เลือกไข่ แคทอาย หรือไร้ขอบ เพื่อสมดุลโหนกแก้ม",
        }[key],
    }

def identify_face(photo, min_conf=MIN_CONF):
    conf = photo["face_confidence"]
    if conf < min_conf:
        return {"ok": False, "uncertain": True, "shape": None, "message_th": "ยังไม่แน่ใจว่านี่คือใบหน้าตรง ลองถ่ายใหม่หรือยืนยันเอง"}
    m = photo["measures"]
    return {"ok": True, "uncertain": False, "shape": face_shape(m["length_mm"], m["forehead_mm"], m["cheek_mm"], m["jaw_mm"]), "message_th": ""}

def face_scan(photo):
    q = scan_quality(photo["glare"], photo["blur"], photo["tilt"], photo["face_fill"], photo["eyes_visible"])
    ident = identify_face(photo)
    pd = photo.get("pd_mm")
    return {
        "photo_id": photo["id"], "quality": q, "undertone": photo.get("undertone", "neutral"),
        "pd_mm": pd, "face": ident["shape"] if ident["ok"] else None,
        "uncertain": ident["uncertain"], "ok": q["ok"] and ident["ok"],
        "message_th": ident["message_th"],
    }

def pipeline_steps(photo):
    s = ["face_detect"]
    if photo["glare"] > 0.5:
        s.append("deglare")
    if photo["tilt"] > 0.35:
        s.append("deskew")
    s += ["shape_classify", "pd_estimate", "frame_tryon", "size_check", "optician_card"]
    return s

def pd_status(pd_mm):
    if pd_mm is None or pd_mm <= 0:
        raise ValueError("pd_mm must be > 0")
    if 58 <= pd_mm <= 68:
        verdict, message_th = "typical", "ค่า PD นี้อยู่ในช่วงที่พบบ่อย แต่ยังต้องให้ร้านวัดจริงก่อนตัดเลนส์"
    elif 54 <= pd_mm <= 74:
        verdict, message_th = "check", "ค่า PD นี้อยู่นอกช่วงเฉลี่ยเล็กน้อย ให้ร้านวัดซ้ำด้วยเครื่องวัด PD"
    else:
        verdict, message_th = "out_of_range", "ค่า PD จากรูปผิดปกติมาก อย่าใช้ตัดเลนส์ ต้องวัดที่ร้านเท่านั้น"
    return {"pd_mm": pd_mm, "verdict": verdict, "message_th": message_th, "disclaimer_th": "PD จากเซลฟี่เป็นค่าประมาณ ไม่ใช่ค่าวัดจริง"}

def size_check(pd_mm, face_width_mm, frame_id):
    if frame_id not in FRAMES:
        raise ValueError("unknown frame " + frame_id)
    if face_width_mm <= 0:
        raise ValueError("face_width_mm must be > 0")
    fr = FRAMES[frame_id]
    front = frame_front_width(fr)
    delta = front - face_width_mm
    if abs(delta) <= 4:
        verdict, fit_th = "ok", "ความกว้างกรอบใกล้เคียงความกว้างหน้า"
    elif delta > 4:
        verdict, fit_th = "too_wide", "กรอบกว้างกว่าหน้า อาจหลวมหรือล้นโหนกแก้ม"
    else:
        verdict, fit_th = "too_narrow", "กรอบแคบกว่าหน้า อาจบีบขมับ"
    pd = pd_status(pd_mm)
    # Optical-center hint (example only): distance between lens centres ≈ lens_width + bridge
    centres = fr["lens_width"] + fr["bridge"]
    offset = round(centres - pd_mm, 1)
    return {
        "frame_id": frame_id, "pd_mm": pd_mm, "pd_verdict": pd["verdict"],
        "face_width_mm": face_width_mm, "frame_front_mm": front,
        "lens_width": fr["lens_width"], "bridge": fr["bridge"], "temple": fr["temple"],
        "delta_mm": round(delta, 1), "verdict": verdict, "fit_th": fit_th,
        "centres_mm": centres, "center_offset_mm": offset,
        "message_th": fit_th + " · " + pd["message_th"],
        "disclaimer_th": "ขนาดจากรูปเป็นค่าประมาณ ให้ร้านวัดหัวและ PD จริงก่อนสั่งทำ",
    }

def contrast_score(undertone, color):
    warm_colors = {"gold", "honey", "tortoise"}
    cool_colors = {"silver", "black", "clear"}
    base = 72
    if color in warm_colors:
        base += 12 if undertone == "warm" else 4 if undertone == "neutral" else 0
    elif color in cool_colors:
        base += 12 if undertone == "cool" else 6 if undertone == "neutral" else 2
    else:
        base += 6
    return max(40, min(96, base))

def fit_score(shape_key, frame_id, size, undertone, lifestyle):
    if frame_id not in FRAMES:
        raise ValueError("unknown frame " + frame_id)
    if lifestyle not in LIFESTYLES:
        raise ValueError("unknown lifestyle")
    fr = FRAMES[frame_id]
    face_pts = 40 if shape_key in fr["best_shapes"] else 18
    if size["verdict"] == "ok":
        size_pts = 30
    elif abs(size["delta_mm"]) <= 8:
        size_pts = 18
    else:
        size_pts = 8
    col_pts = round(contrast_score(undertone, fr["color"]) / 96 * 15)
    life_pts = 15 if lifestyle in fr["lifestyle"] else 6
    total = face_pts + size_pts + col_pts + life_pts
    reasons = []
    if face_pts == 40:
        reasons.append("ทรงกรอบเข้ากับทรงหน้า")
    else:
        reasons.append("ทรงกรอบไม่ใช่กลุ่มที่แนะนำสำหรับทรงหน้านี้ แต่ลองได้")
    reasons.append(size["fit_th"])
    if life_pts == 15:
        reasons.append("เข้ากับไลฟ์สไตล์ที่เลือก")
    return {
        "frame_id": frame_id, "score": total, "face_pts": face_pts, "size_pts": size_pts,
        "contrast_pts": col_pts, "lifestyle_pts": life_pts, "reasons_th": reasons,
    }

def overlay_tryon(photo, frame_id, lifestyle="casual"):
    if frame_id not in FRAMES:
        raise ValueError("unknown frame " + frame_id)
    scan = face_scan(photo)
    if not scan["face"]:
        raise ValueError("face not identified")
    fr = FRAMES[frame_id]
    face_w = photo["measures"]["cheek_mm"]
    size = size_check(photo["pd_mm"], face_w, frame_id)
    fit = fit_score(scan["face"]["shape"], frame_id, size, photo.get("undertone", "neutral"), lifestyle)
    return {
        "photo_id": photo["id"], "frame_id": frame_id, "name_th": fr["name_th"],
        "shape": fr["shape"], "material": fr["material"], "color": fr["color"],
        "face_shape": scan["face"]["shape"], "face_shape_th": scan["face"]["shape_th"],
        "pd_mm": photo["pd_mm"], "size_verdict": size["verdict"], "fit_score": fit["score"],
        "quality": scan["quality"], "watermark": WATERMARK, "disclaimer_th": SAFETY_DISCLAIMER_TH,
    }

def tryon_grid(photo, frame_ids, lifestyle="casual"):
    if not 1 <= len(frame_ids) <= 9:
        raise ValueError("grid must have 1..9 frames")
    items = [overlay_tryon(photo, fid, lifestyle) for fid in frame_ids]
    items.sort(key=lambda t: (-t["fit_score"], t["frame_id"]))
    return {"photo_id": photo["id"], "count": len(items), "ranked": items, "top_id": items[0]["frame_id"]}

def compare_grid(photo, frame_ids, lifestyle="casual"):
    if not 2 <= len(frame_ids) <= 4:
        raise ValueError("compare 2..4 frames")
    items = [overlay_tryon(photo, fid, lifestyle) for fid in frame_ids]
    return {"photo_id": photo["id"], "frames": items, "count": len(items)}

def _round50(x):
    return int(round(x / 50.0) * 50)

def price_range(frame_id, region, lens="single"):
    if frame_id not in FRAMES:
        raise ValueError("unknown frame " + frame_id)
    if region not in REGION_MULT:
        raise ValueError("unknown region")
    if lens not in LENS_TYPES:
        raise ValueError("unknown lens")
    fr = FRAMES[frame_id]
    mid = _round50((fr["base_thb"] + LENS_TYPES[lens]["add_thb"]) * REGION_MULT[region])
    mn = max(1500, _round50(mid * 0.80))
    mx = _round50(mid * 1.35)
    if mx <= mn:
        mx = mn + 500
    return {
        "frame_id": frame_id, "name_th": fr["name_th"], "region": region, "lens": lens, "lens_th": LENS_TYPES[lens]["name_th"],
        "mid_thb": mid, "min_thb": mn, "max_thb": mx, "currency": "THB", "disclaimer_th": PRICE_DISCLAIMER_TH,
    }

def quote_check(quote_thb, frame_id, region, lens="single"):
    if quote_thb < 0:
        raise ValueError("quote must be >= 0")
    pr = price_range(frame_id, region, lens)
    q = quote_thb
    if q < pr["min_thb"] * 0.85:
        verdict, message_th = "low", "ต่ำกว่าช่วงประมาณการมาก เช็กยี่ห้อเลนส์ วัสดุกรอบ และสิ่งที่รวมในราคา"
    elif q <= pr["max_thb"]:
        if q < pr["min_thb"]:
            verdict, message_th = "low", "ต่ำกว่าช่วงเล็กน้อย ถามรายละเอียดเลนส์และรับประกัน"
        elif q <= pr["mid_thb"] * 1.15:
            verdict, message_th = "fair", "อยู่ในช่วงสมเหตุสมผลเมื่อเทียบกับค่าประมาณการของแอป"
        else:
            verdict, message_th = "high", "ค่อนข้างสูงกว่าค่ากลาง ยังอยู่ในช่วง แต่ควรถามส่วนลดชุดกรอบ+เลนส์"
    else:
        verdict, message_th = "very_high", "สูงกว่าช่วงประมาณการมาก ขอใบเสนอราคาแยกกรอบ เลนส์ และเคลือบ"
    questions = [
        "ราคานี้รวมเลนส์ ค่าตรวจ และเคลือบหรือยัง",
        "ค่า PD และม่านตาที่วัดได้เท่าไร ขอดูใบวัด",
        "กรอบนี้ปรับจมูกและขาได้ไหม มีรับประกันกี่เดือน",
        "ถ้าค่าสายตาเปลี่ยนใน 3 เดือน เปลี่ยนเลนส์ได้เท่าไร",
    ]
    return {"quote_thb": q, "min_thb": pr["min_thb"], "max_thb": pr["max_thb"], "mid_thb": pr["mid_thb"],
            "verdict": verdict, "message_th": message_th, "questions_th": questions, "disclaimer_th": PRICE_DISCLAIMER_TH}

def lens_advice(lens, age, lifestyle):
    if lens not in LENS_TYPES:
        raise ValueError("unknown lens")
    info = LENS_TYPES[lens]
    warn = []
    if lens == "progressive" and age < 35:
        warn.append("โปรเกรสซีฟมักใช้เมื่อเริ่มมีปัญหาเห็นใกล้ ต้องให้ร้าน/แพทย์ประเมิน ไม่เลือกเองจากอายุอย่างเดียว")
    if lens == "blue_light":
        warn.append("เลนส์กรองแสงน้ำเงินไม่แทนการพักสายตาหรือการตรวจตา")
    return {"lens": lens, "name_th": info["name_th"], "add_thb": info["add_thb"], "notes_th": info["notes_th"],
            "warnings_th": warn, "lifestyle": lifestyle, "disclaimer_th": SAFETY_DISCLAIMER_TH}

def optician_card(person, scan, tryon, price, size, note_th=""):
    fr = FRAMES[tryon["frame_id"]]
    text = (
        f"SpecsTry — การ์ดยื่นร้านแว่น\n"
        f"{person['name_th']} · ทรงหน้า {tryon['face_shape_th']}\n"
        f"กรอบ: {tryon['name_th']} ({fr['lens_width']}-{fr['bridge']}-{fr['temple']})\n"
        f"PD ประมาณ (จากรูป ห้ามใช้ตัดเลนส์): {tryon['pd_mm']} มม.\n"
        f"งบประมาณโดยประมาณ: ฿{price['min_thb']:,}–{price['max_thb']:,}\n"
        f"{note_th}".strip()
    )
    return {
        "title_th": "การ์ดยื่นร้านแว่น",
        "name_th": person["name_th"],
        "face_shape": tryon["face_shape"],
        "face_shape_th": tryon["face_shape_th"],
        "frame_id": tryon["frame_id"],
        "frame_th": tryon["name_th"],
        "lens_width": fr["lens_width"],
        "bridge": fr["bridge"],
        "temple": fr["temple"],
        "pd_mm": tryon["pd_mm"],
        "fit_score": tryon["fit_score"],
        "size_verdict": size["verdict"],
        "budget_min_thb": price["min_thb"],
        "budget_max_thb": price["max_thb"],
        "note_th": note_th,
        "line_share_url": "https://line.me/R/share?text=" + _up.quote(text),
        "disclaimer_th": SAFETY_DISCLAIMER_TH + " " + PRICE_DISCLAIMER_TH,
    }

def share_card(name_th, tryon):
    return {
        "title_th": f"SpecsTry — {name_th}",
        "headline_th": f"{tryon['name_th']} · เข้ากับ{tryon['face_shape_th']} {tryon['fit_score']} คะแนน",
        "hook_th": "ลองแว่นบนหน้าตัวเองก่อนซื้อ",
        "frame_id": tryon["frame_id"],
        "face_shape": tryon["face_shape"],
        "layout": "tryon_result",
        "sizes": ["1080x1350", "1080x1920", "1080x1080"],
        "watermark": WATERMARK,
        "cta_th": "คอมเมนต์ SPECS รับแพ็กฟรี",
    }

def quota(used_today, want, pro=False):
    if pro:
        return {"allowed": want, "left_after": None, "paywall": False}
    left = max(0, FREE_TRYONS_PER_DAY - used_today)
    allowed = min(want, left)
    return {"allowed": allowed, "left_after": left - allowed, "paywall": allowed < want}

def safety_guard(ok=True):
    if not ok:
        return {"level": "stop", "message_th": "ยังใช้ค่าจากรูปตัดเลนส์ไม่ได้ " + SAFETY_DISCLAIMER_TH}
    return {"level": "ok", "message_th": SAFETY_DISCLAIMER_TH}

def frame_info(frame_id):
    if frame_id not in FRAMES:
        raise ValueError("unknown frame " + frame_id)
    fr = dict(FRAMES[frame_id])
    fr["id"] = frame_id
    fr["front_mm"] = frame_front_width(fr)
    fr["material_th"] = MAT_TH[fr["material"]]
    return fr

def diary_entry(eid, person_id, date, frame_id, shop_th, cost_thb, status, on_device=True):
    if status not in ("wishlist", "tried", "bought"):
        raise ValueError("bad status")
    return {"id": eid, "person_id": person_id, "date": date, "frame_id": frame_id,
            "shop_th": shop_th, "cost_thb": cost_thb, "status": status, "on_device": on_device}

def diary_stats(entries):
    if not entries:
        return {"count": 0, "total_thb": 0, "avg_thb": 0, "last_date": None, "top_frame": None}
    bought = [e for e in entries if e["status"] == "bought"]
    total = sum(e["cost_thb"] for e in bought)
    last = max(entries, key=lambda e: e["date"])["date"]
    from collections import Counter
    c = Counter(e["frame_id"] for e in entries)
    return {"count": len(entries), "total_thb": total, "avg_thb": int(round(total / len(bought))) if bought else 0,
            "last_date": last, "top_frame": c.most_common(1)[0][0]}
