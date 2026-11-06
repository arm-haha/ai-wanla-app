"""CardReady deterministic logic (no AI calls). Specs/weights are app-chosen example values — not government certification."""
import math, re

# Thai common ID/pass photo sizes at 300 dpi (1 inch = 25.4 mm)
DPI_DEFAULT = 300
SIZE_PRESETS = {
    "1_inch": {"label_th": "1 นิ้ว", "mm_w": 25.0, "mm_h": 35.0, "docs": ["national_id", "job_th", "student"]},
    "2_inch": {"label_th": "2 นิ้ว", "mm_w": 40.0, "mm_h": 60.0, "docs": ["job_th", "student"]},
    "passport": {"label_th": "พาสปอร์ต", "mm_w": 35.0, "mm_h": 45.0, "docs": ["passport", "visa"]},
    "visa": {"label_th": "วีซ่า", "mm_w": 35.0, "mm_h": 45.0, "docs": ["visa"]},
    "job_th": {"label_th": "ใบสมัครงานไทย", "mm_w": 25.0, "mm_h": 35.0, "docs": ["job_th"]},
}

BG_PRESETS = {
    "white": {"hex": "#FFFFFF", "label_th": "ขาว"},
    "gov_blue": {"hex": "#1E4D8C", "label_th": "ฟ้ากรมการ"},
    "red": {"hex": "#C8102E", "label_th": "แดง"},
}

DOC_TYPES = ["national_id", "passport", "visa", "job_th", "student"]
DOC_LABEL_TH = {
    "national_id": "บัตรประชาชน",
    "passport": "พาสปอร์ต",
    "visa": "วีซ่า",
    "job_th": "สมัครงาน",
    "student": "นักเรียน/นักศึกษา",
}

# Doc → preferred size key + preferred bg + checklist item ids
DOC_RULES = {
    "national_id": {"size": "1_inch", "bg": "white", "checks": ["face_front", "eyes_open", "neutral", "even_light", "bg_plain", "no_hat", "no_glasses_tint", "head_ratio"]},
    "passport": {"size": "passport", "bg": "white", "checks": ["face_front", "eyes_open", "neutral", "even_light", "bg_plain", "no_hat", "no_glasses_tint", "head_ratio", "ears_visible"]},
    "visa": {"size": "visa", "bg": "white", "checks": ["face_front", "eyes_open", "neutral", "even_light", "bg_plain", "no_hat", "head_ratio"]},
    "job_th": {"size": "1_inch", "bg": "white", "checks": ["face_front", "eyes_open", "neutral", "even_light", "bg_plain", "formal_wear"]},
    "student": {"size": "1_inch", "bg": "gov_blue", "checks": ["face_front", "eyes_open", "neutral", "even_light", "bg_plain", "no_hat"]},
}

CHECK_LABEL_TH = {
    "face_front": "หันหน้าตรง",
    "eyes_open": "ลืมตาชัด",
    "neutral": "สีหน้าปกติ ไม่ยิ้มกว้าง",
    "even_light": "แสงสม่ำเสมอ ไม่มีเงาบนหน้า",
    "bg_plain": "พื้นหลังเรียบตามที่กำหนด",
    "no_hat": "ไม่สวมหมวก/ผ้าคลุมที่บังหน้า",
    "no_glasses_tint": "แว่นไม่มีเลนส์สี / ไม่สะท้อน",
    "head_ratio": "สัดส่วนศีรษะอยู่ในกรอบ",
    "ears_visible": "เห็นใบหูทั้งสองข้าง",
    "formal_wear": "ชุดสุภาพ (ปกเสื้อมองเห็น)",
}

# Pass score weights (selfie quality → ID readiness). Higher input = worse for "mess" keys.
MESS_W = {"yellow_cast": 0.20, "shadow": 0.20, "clutter_bg": 0.25, "blur": 0.15, "tilt": 0.10, "crop_tight": 0.10}
PASS_LEVELS = [(50, "fail", "ยังไม่ผ่าน"), (75, "warn", "เกือบผ่าน"), (101, "pass", "ผ่าน")]

# Soft-light: mild only — no reshape / no plastic beauty
SOFT_LIGHT_MAX = 0.35  # max strength allowed
BLEMISH_MAX = 0.25
A4_MM = (210.0, 297.0)
HEX_RE = re.compile(r"^#?[0-9A-Fa-f]{6}$")
WATERMARK = "Made with CardReady · not a government certificate"
FREE_EXPORTS_PER_DAY = 5


def mm_to_px(mm, dpi=DPI_DEFAULT):
    return max(1, round(mm / 25.4 * dpi))


def size_spec(key, dpi=DPI_DEFAULT):
    """Return full size preset with px at given dpi."""
    if key not in SIZE_PRESETS:
        raise KeyError(f"unknown size preset: {key}")
    p = SIZE_PRESETS[key]
    return {
        "key": key,
        "label_th": p["label_th"],
        "mm_w": p["mm_w"],
        "mm_h": p["mm_h"],
        "dpi": dpi,
        "px_w": mm_to_px(p["mm_w"], dpi),
        "px_h": mm_to_px(p["mm_h"], dpi),
        "docs": list(p["docs"]),
    }


def list_size_presets(dpi=DPI_DEFAULT):
    return [size_spec(k, dpi) for k in SIZE_PRESETS]


def resolve_bg(preset_or_hex):
    """Accept preset key or custom #hex → {preset, hex, label_th, custom}."""
    if preset_or_hex in BG_PRESETS:
        b = BG_PRESETS[preset_or_hex]
        return {"preset": preset_or_hex, "hex": b["hex"], "label_th": b["label_th"], "custom": False}
    h = preset_or_hex if str(preset_or_hex).startswith("#") else f"#{preset_or_hex}"
    if not HEX_RE.match(h):
        raise ValueError("invalid hex color")
    return {"preset": "custom", "hex": h.upper() if h[1:].isupper() or True else h, "label_th": "กำหนดเอง", "custom": True}


def normalize_hex(h):
    h = h if h.startswith("#") else f"#{h}"
    if not HEX_RE.match(h):
        raise ValueError("invalid hex")
    return "#" + h.lstrip("#").upper()


def resolve_bg_safe(preset_or_hex):
    if preset_or_hex in BG_PRESETS:
        b = BG_PRESETS[preset_or_hex]
        return {"preset": preset_or_hex, "hex": b["hex"], "label_th": b["label_th"], "custom": False}
    hx = normalize_hex(str(preset_or_hex))
    return {"preset": "custom", "hex": hx, "label_th": "กำหนดเอง", "custom": True}


def id_crop_box(px_w, px_h, face_cx, face_cy, face_h, size_key, head_ratio=0.70):
    """
    Compute crop box (x0,y0,x1,y1) in source pixels for target size aspect.
    face_cx/cy/face_h are normalized 0..1 relative to source.
    head_ratio: fraction of photo height the head should occupy (app-chosen ~0.65–0.75).
    """
    spec = size_spec(size_key)
    aspect = spec["mm_w"] / spec["mm_h"]  # width/height
    # Desired crop height in source px so head fills head_ratio of crop
    face_h_px = face_h * px_h
    crop_h = face_h_px / max(0.4, min(0.85, head_ratio))
    crop_w = crop_h * aspect
    # Center on face, bias slightly up so more space below chin
    cx, cy = face_cx * px_w, face_cy * px_h - crop_h * 0.05
    x0 = cx - crop_w / 2
    y0 = cy - crop_h / 2
    # Clamp inside image; if crop larger than image, shrink
    if crop_w > px_w or crop_h > px_h:
        scale = min(px_w / crop_w, px_h / crop_h)
        crop_w *= scale
        crop_h *= scale
        x0 = cx - crop_w / 2
        y0 = cy - crop_h / 2
    x0 = max(0, min(x0, px_w - crop_w))
    y0 = max(0, min(y0, px_h - crop_h))
    return {
        "x0": round(x0), "y0": round(y0),
        "x1": round(x0 + crop_w), "y1": round(y0 + crop_h),
        "out_px_w": spec["px_w"], "out_px_h": spec["px_h"],
        "size_key": size_key, "aspect": round(aspect, 4),
    }


def mess_penalty(mess):
    """mess dict 0..1 higher=worse → penalty 0..1."""
    return sum(MESS_W[k] * max(0.0, min(1.0, mess.get(k, 0))) for k in MESS_W)


def pass_score(mess, soft_light_on=True, bg_removed=True, size_ok=True, checks_pass=None):
    """
    Overall Pass Score 0–100. Demo target for Mint messy dorm selfie → ~92 after processing.
    Base = 100*(1 - mess_penalty); bonuses for soft_light, bg_removed, size_ok; checks average.
    """
    base = 100 * (1 - mess_penalty(mess))
    bonus = 0.0
    if soft_light_on: bonus += 8
    if bg_removed: bonus += 12
    if size_ok: bonus += 5
    if checks_pass is not None and len(checks_pass) > 0:
        ratio = sum(1 for c in checks_pass if c) / len(checks_pass)
        bonus += 10 * ratio
    # Soft light / bg remove assume they fix a lot of mess visually for scoring after pipeline
    after = base
    if soft_light_on:
        after = after + mess.get("yellow_cast", 0) * 100 * MESS_W["yellow_cast"] * 0.85
        after = after + mess.get("shadow", 0) * 100 * MESS_W["shadow"] * 0.70
    if bg_removed:
        after = after + mess.get("clutter_bg", 0) * 100 * MESS_W["clutter_bg"] * 0.95
    sc = round(min(100, after + (5 if size_ok else 0)))
    for cut, lv, th in PASS_LEVELS:
        if sc < cut:
            return sc, lv, th
    return sc, "pass", "ผ่าน"


def soft_light_plan(strength, blemish=0.15):
    """Clamp soft-light + blemish; forbid reshape / plastic beauty."""
    s = max(0.0, min(SOFT_LIGHT_MAX, float(strength)))
    b = max(0.0, min(BLEMISH_MAX, float(blemish)))
    return {
        "strength": round(s, 3),
        "blemish_calm": round(b, 3),
        "even_lighting": True,
        "reshape": False,
        "plastic_beauty": False,
        "whitelist": ["even_light", "mild_blemish", "color_cast_fix"],
        "blocked": ["face_reshape", "skin_plastic", "eye_enlarge", "slim_face", "heavy_makeup"],
    }


def dpi_check(px_w, px_h, mm_w, mm_h, min_dpi=300):
    dpi_w = px_w / (mm_w / 25.4)
    dpi_h = px_h / (mm_h / 25.4)
    dpi = round(min(dpi_w, dpi_h))  # round so mm_to_px(round) targets stay at nominal dpi
    return {"dpi": dpi, "ok": dpi >= min_dpi, "min_dpi": min_dpi}


def print_sheet_layout(size_key, copies, margin_mm=8.0, gap_mm=4.0, dpi=DPI_DEFAULT):
    """
    Pack N copies of the ID photo onto A4 with cut guides.
    Returns rows, cols, placed, dpi_ok, positions.
    """
    if copies < 1 or copies > 24:
        raise ValueError("copies must be 1–24")
    spec = size_spec(size_key, dpi)
    usable_w = A4_MM[0] - 2 * margin_mm
    usable_h = A4_MM[1] - 2 * margin_mm
    cols = max(1, int((usable_w + gap_mm) // (spec["mm_w"] + gap_mm)))
    rows = max(1, int((usable_h + gap_mm) // (spec["mm_h"] + gap_mm)))
    capacity = cols * rows
    placed = min(copies, capacity)
    positions = []
    for i in range(placed):
        r, c = divmod(i, cols) if False else (i // cols, i % cols)
        x = margin_mm + c * (spec["mm_w"] + gap_mm)
        y = margin_mm + r * (spec["mm_h"] + gap_mm)
        positions.append({"index": i + 1, "x_mm": round(x, 2), "y_mm": round(y, 2),
                          "w_mm": spec["mm_w"], "h_mm": spec["mm_h"]})
    a4_px_w = mm_to_px(A4_MM[0], dpi)
    a4_px_h = mm_to_px(A4_MM[1], dpi)
    chk = dpi_check(spec["px_w"], spec["px_h"], spec["mm_w"], spec["mm_h"], min_dpi=dpi)
    return {
        "size_key": size_key,
        "copies_requested": copies,
        "copies_placed": placed,
        "capacity": capacity,
        "rows": rows,
        "cols": cols,
        "margin_mm": margin_mm,
        "gap_mm": gap_mm,
        "a4_px_w": a4_px_w,
        "a4_px_h": a4_px_h,
        "cut_guides": True,
        "dpi_check": chk,
        "positions": positions,
    }


def doc_checklist(doc_type, signals):
    """
    signals: dict of check_id -> bool (True = pass).
    Returns items with pass/fail + overall meter 0–100.
    """
    if doc_type not in DOC_RULES:
        raise KeyError(f"unknown doc: {doc_type}")
    rule = DOC_RULES[doc_type]
    items = []
    for cid in rule["checks"]:
        ok = bool(signals.get(cid, False))
        items.append({"id": cid, "label_th": CHECK_LABEL_TH[cid], "pass": ok})
    passed = sum(1 for i in items if i["pass"])
    meter = round(100 * passed / len(items)) if items else 0
    level = "pass" if meter >= 80 else ("warn" if meter >= 50 else "fail")
    return {
        "doc_type": doc_type,
        "label_th": DOC_LABEL_TH[doc_type],
        "preferred_size": rule["size"],
        "preferred_bg": rule["bg"],
        "items": items,
        "passed": passed,
        "total": len(items),
        "meter": meter,
        "level": level,
        "disclaimer_th": "เป็นแนวทางทั่วไป ไม่ใช่การรับรองจากหน่วยงานราชการ",
    }


def export_pack(formats, size_key, include_print_pdf=True):
    """formats: subset of jpg/png; always can add print pdf."""
    allowed = {"jpg", "png"}
    out = []
    spec = size_spec(size_key)
    for f in formats:
        if f not in allowed:
            raise ValueError(f"unsupported format: {f}")
        out.append({
            "format": f,
            "filename": f"cardready_{size_key}.{f}",
            "px_w": spec["px_w"],
            "px_h": spec["px_h"],
            "dpi": spec["dpi"],
            "bg_alpha": f == "png",
        })
    if include_print_pdf:
        out.append({
            "format": "pdf",
            "filename": f"cardready_{size_key}_a4.pdf",
            "px_w": mm_to_px(A4_MM[0]),
            "px_h": mm_to_px(A4_MM[1]),
            "dpi": DPI_DEFAULT,
            "bg_alpha": False,
        })
    return {"files": out, "watermark": WATERMARK, "count": len(out)}


def share_card(name_th, size_key, pass_sc, bg_label):
    spec = size_spec(size_key)
    return {
        "title_th": "CardReady",
        "headline_th": f"{name_th} · {spec['label_th']} พื้น{bg_label} · Pass {pass_sc}",
        "hook_th": "เซลฟี่มั่ว ๆ → รูปติดบัตรพื้นขาวคมชัดใน 3 วินาที",
        "badges": ["bg_remove", "soft_light", "size_ok"],
        "watermark": WATERMARK,
        "cta_th": "ลองทำรูปติดบัตรของคุณ ลิงก์ในไบโอ",
        "size_label_th": spec["label_th"],
        "pass_score": pass_sc,
    }


def quota(used_today, wanted, pro=False):
    if pro:
        return {"allowed": wanted, "left_after": None, "paywall": False}
    left = max(0, FREE_EXPORTS_PER_DAY - used_today)
    allowed = min(left, wanted)
    return {"allowed": allowed, "left_after": left - allowed, "paywall": wanted > allowed}


def history_entry(photo_id, size_key, bg, pass_sc, created_at):
    return {
        "photo_id": photo_id,
        "size_key": size_key,
        "bg": resolve_bg_safe(bg),
        "pass_score": pass_sc,
        "created_at": created_at,
        "on_device": True,
    }


def batch_profiles(members):
    """members: list of {id, name_th, relation_th} — fictional family only."""
    if len(members) > 8:
        raise ValueError("max 8 profiles")
    return {"count": len(members), "members": list(members), "note_th": "โปรไฟล์สมมติ เก็บในเครื่อง"}


def pipeline_steps(mess, soft_light_on=True):
    steps = ["face_detect", "auto_crop", "bg_remove"]
    if mess.get("tilt", 0) >= 0.15:
        steps.insert(1, "deskew")
    if soft_light_on:
        steps.append("soft_light")
    if mess.get("yellow_cast", 0) >= 0.3:
        steps.append("color_cast_fix")
    steps += ["size_fit", "dpi_tag"]
    return steps
