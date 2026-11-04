"""MemoryFix deterministic logic (no AI calls). All weights are app-chosen example values."""
import math
DAMAGE_W = {"scratches": 0.25, "fading": 0.20, "tears": 0.25, "blur": 0.15, "stains": 0.15}
LEVELS = [(20, "light", "เบา"), (45, "medium", "กลาง"), (70, "heavy", "หนัก"), (101, "severe", "หนักมาก")]
PRINT_SIZES = {"4x6": (10.2, 15.2), "5x7": (12.7, 17.8), "8x10": (20.3, 25.4), "A4": (21.0, 29.7)}
FREE_PER_DAY = 3
STEPS = ["perspective", "deglare", "repair", "denoise", "face_enhance", "sharpen", "colorize", "upscale"]

def damage_score(scan):
    """scan: dict of 0..1 per DAMAGE_W key -> (score 0-100, level, level_th)."""
    sc = round(100 * sum(DAMAGE_W[k] * max(0.0, min(1.0, scan.get(k, 0))) for k in DAMAGE_W))
    for cut, lv, th in LEVELS:
        if sc < cut:
            return sc, lv, th

def restore_plan(scan, is_bw, faces, px_short, want_color=True, deglare_needed=False, skewed=False):
    steps = []
    if skewed: steps.append("perspective")
    if deglare_needed: steps.append("deglare")
    if scan.get("scratches", 0) >= 0.1 or scan.get("tears", 0) >= 0.1 or scan.get("stains", 0) >= 0.1: steps.append("repair")
    if scan.get("fading", 0) >= 0.2 or scan.get("blur", 0) >= 0.2: steps.append("denoise")
    if faces > 0: steps.append("face_enhance")
    steps.append("sharpen")
    if is_bw and want_color: steps.append("colorize")
    if px_short < 1200: steps.append("upscale")
    return [s for s in STEPS if s in steps]

def upscale_factor(px_short, target_short=1800):
    if px_short >= target_short: return 1
    return min(4, 2 ** math.ceil(math.log2(target_short / px_short)))

def print_options(px_w, px_h, min_dpi=200):
    """Which standard sizes print at >= min_dpi. Returns dict size -> dpi (int)."""
    short_px, long_px = sorted((px_w, px_h)); out = {}
    for name, (a, b) in PRINT_SIZES.items():
        dpi = int(min(short_px / (a / 2.54), long_px / (b / 2.54)))
        out[name] = {"dpi": dpi, "ok": dpi >= min_dpi}
    return out

def decade(year): return None if year is None else (year // 10) * 10

def timeline(photos):
    """Group photos by decade (year_est), unknown last. Returns list of {decade,label_th,ids}."""
    groups = {}
    for p in photos: groups.setdefault(decade(p.get("year_est")), []).append(p)
    keys = sorted(k for k in groups if k is not None) + ([None] if None in groups else [])
    res = []
    for k in keys:
        ids = [p["id"] for p in sorted(groups[k], key=lambda p: (p.get("year_est") or 9999, p["id"]))]
        res.append({"decade": k, "label_th": "ไม่ทราบปี" if k is None else f"ยุค {k + 543}s (ค.ศ. {k}s)", "ids": ids})
    return res

def people_index(photos):
    idx = {}
    for p in photos:
        for name in p.get("people", []): idx.setdefault(name, []).append(p["id"])
    return dict(sorted(idx.items(), key=lambda kv: (-len(kv[1]), kv[0])))

def years_ago(year_est, now_year): return None if year_est is None else now_year - year_est

def then_now_caption(person, then_year, now_year):
    return f"{person} ปี {then_year + 543} → {now_year + 543} ({now_year - then_year} ปี)"

def quota(used_today, restores_wanted, pro=False):
    if pro: return {"allowed": restores_wanted, "left_after": None, "paywall": False}
    left = max(0, FREE_PER_DAY - used_today); allowed = min(left, restores_wanted)
    return {"allowed": allowed, "left_after": left - allowed, "paywall": restores_wanted > allowed}

def motion_allowed(person_status, consent):
    """Live motion: deceased -> family owner consent; living adult -> that person's consent; minor -> never."""
    if person_status == "minor": return False
    return bool(consent)

def share_card(title, damage_before, years, steps):
    return {"title_th": title, "headline_th": f"รูปอายุ {years} ปี · ซ่อมจากความเสียหาย {damage_before}%", "badges": [s for s in steps if s in ("repair", "colorize", "face_enhance")],
            "watermark": "AI restored · MemoryFix", "cta_th": "ลองซ่อมรูปบ้านคุณ ลิงก์ในไบโอ"}
