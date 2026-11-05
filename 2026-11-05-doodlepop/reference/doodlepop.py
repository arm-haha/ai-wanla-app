"""DoodlePop deterministic logic (no AI calls). All weights/limits are app-chosen example values."""
import math, datetime as dt
SCAN_W = {"shadow": 0.30, "blur": 0.35, "tilt": 0.15, "crop_cut": 0.20}
SCAN_LEVELS = [(40, "retake", "ถ่ายใหม่ดีกว่า"), (80, "ok", "ใช้ได้"), (101, "great", "ชัดมาก")]
PRESETS = ["wave", "jump", "dance", "walk", "spin", "sleep"]
PRESET_TH = {"wave": "โบกมือ", "jump": "กระโดด", "dance": "เต้น", "walk": "เดิน", "spin": "หมุนตัว", "sleep": "นอนหลับ", "hop": "กระดึ๊บ", "wiggle": "ส่ายตัว"}
PRESET_LEN_S = {"wave": 2.0, "jump": 1.5, "dance": 4.0, "walk": 2.0, "spin": 2.0, "sleep": 3.0, "hop": 1.5, "wiggle": 2.0}
FALLBACK = {"wave": "wiggle", "walk": "hop"}
BONES = {"head": 1, "body": 1, "arms": 2, "legs": 2, "tail": 2, "wings": 1}
EXPORTS = {"reel_mp4": (1080, 1920, 30), "square_mp4": (1080, 1080, 30), "gif": (480, 480, 12)}
GIF_MAX_S = 6
WATERMARK = "Made with DoodlePop"
STICKER_COUNTS = [8, 16, 24, 32, 40]
STICKER_BOX = (370, 320)
FREE_ANIM_PER_DAY = 3
FREE_STORY_PER_DAY = 1
PARENT_ONLY = {"share_public", "grandparent_link", "print_order", "export_video", "delete_drawing"}
PRODUCTS = {"mug": (20.0, 9.5, 200), "tshirt": (25.0, 30.0, 150), "poster_a4": (21.0, 29.7, 200), "sticker_7cm": (7.0, 7.0, 300)}
DRAW_PROMPTS = ["สัตว์ที่มีขา 6 ขา", "บ้านในฝันของหนู", "ไดโนเสาร์ใส่หมวก", "หุ่นยนต์ช่วยแม่ทำกับข้าว", "ปลาที่บินได้", "เพื่อนจากดาวอังคาร",
                "ช้างกินไอศกรีม", "รถที่วิ่งบนเมฆ", "แมวเป็นซูเปอร์ฮีโร่", "ต้นไม้ที่ออกผลเป็นขนม", "มังกรตัวจิ๋ว", "ครอบครัวของหนูเป็นสัตว์"]
PROMPT_NO_REPEAT_DAYS = 30

def scan_score(scan):
    """scan: dict 0..1 per SCAN_W key (higher = worse) -> (score 0-100 higher=better, level, level_th)."""
    pen = sum(SCAN_W[k] * max(0.0, min(1.0, scan.get(k, 0))) for k in SCAN_W)
    sc = round(100 * (1 - pen))
    for cut, lv, th in SCAN_LEVELS:
        if sc < cut: return sc, lv, th

def retake_reason(scan):
    if scan.get("crop_cut", 0) >= 0.3: return "รูปวาดโดนตัดขอบ ถอยกล้องออกนิดนึง"
    if scan.get("blur", 0) >= 0.6: return "ภาพเบลอ วางมือถือให้นิ่งแล้วถ่ายใหม่"
    if scan.get("shadow", 0) >= 0.8: return "เงามือบังรูป ลองหันกระดาษเข้าหาแสง"
    return None

def cleanup_steps(scan):
    steps = []
    if scan.get("tilt", 0) >= 0.1: steps.append("perspective")
    if scan.get("shadow", 0) >= 0.2: steps.append("deshadow")
    steps.append("remove_paper")
    if scan.get("blur", 0) >= 0.3: steps.append("sharpen_lines")
    steps += ["fill_gaps", "cutout"]
    return steps

def rig(parts):
    """parts: counts of head/body/arms/legs/tail/wings -> rig summary with presets available + fallbacks."""
    bones = sum(BONES[k] * parts.get(k, 0) for k in BONES)
    avail, swaps = [], {}
    for p in PRESETS:
        if p == "wave" and parts.get("arms", 0) < 1 and parts.get("wings", 0) < 1: swaps[p] = FALLBACK[p]; avail.append(FALLBACK[p])
        elif p == "walk" and parts.get("legs", 0) < 2: swaps[p] = FALLBACK[p]; avail.append(FALLBACK[p])
        else: avail.append(p)
    return {"bones": bones, "presets": avail, "fallbacks": swaps, "needs_manual_pins": parts.get("body", 0) < 1}

def clip(preset, fps=24, loops=1):
    s = PRESET_LEN_S[preset] * loops
    return {"preset": preset, "label_th": PRESET_TH[preset], "duration_s": s, "fps": fps, "frames": int(round(s * fps)), "loop": True}

def export_spec(fmt, total_s, anim_len_s):
    w, h, fps = EXPORTS[fmt]
    if fmt == "gif": total_s = min(total_s, GIF_MAX_S)
    loops = math.ceil(total_s / anim_len_s)
    return {"format": fmt, "w": w, "h": h, "fps": fps, "duration_s": total_s, "loops": loops, "frames": int(total_s * fps),
            "music": fmt != "gif", "watermark": WATERMARK}

def story_plan(age, n_chars):
    if not 1 <= n_chars <= 3: raise ValueError("ต้องเลือกตัวละคร 1–3 ตัว")
    pages = 4 if age <= 4 else 5 if age <= 6 else 6
    words = 25 if age <= 4 else 40 if age <= 6 else 60
    wps = 1.6 if age <= 6 else 2.0
    return {"pages": pages, "words_per_page": words, "total_words": pages * words, "narration_s": round(pages * words / wps)}

def age_at(birth, on):
    b, d = dt.date.fromisoformat(birth), dt.date.fromisoformat(on)
    m = (d.year - b.year) * 12 + d.month - b.month - (1 if d.day < b.day else 0)
    return {"years": m // 12, "months": m % 12, "label_th": f"{m // 12} ขวบ {m % 12} เดือน"}

def detail_score(d):
    return min(100, round(d["strokes"] / 4 + d["colors"] * 5 + sum(d["parts"].values()) * 2))

def gallery(drawings, kid_id):
    """Drawings of one kid, newest first."""
    return [x["id"] for x in sorted((x for x in drawings if x["kid_id"] == kid_id), key=lambda x: x["drawn_on"], reverse=True)]

def year_recap(drawings, kid, year):
    ds = sorted((x for x in drawings if x["kid_id"] == kid["id"] and x["drawn_on"].startswith(str(year))), key=lambda x: x["drawn_on"])
    if not ds: return None
    subj = {}
    for x in ds: subj[x["subject"]] = subj.get(x["subject"], 0) + 1
    top = sorted(subj.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]
    first, last = detail_score(ds[0]), detail_score(ds[-1])
    return {"kid_id": kid["id"], "year": year, "count": len(ds), "top_subject": top, "avg_colors": round(sum(x["colors"] for x in ds) / len(ds), 1),
            "first_detail": first, "last_detail": last, "growth_pct": round(100 * (last - first) / first) if first else None,
            "headline_th": f"ปี {year + 543} {kid['name_th']} วาด {len(ds)} รูป รายละเอียดเพิ่มขึ้น {round(100 * (last - first) / first)}%"}

def fit_box(w, h, bw=STICKER_BOX[0], bh=STICKER_BOX[1]):
    s = min(bw / w, bh / h); W, H = int(w * s), int(h * s)
    return W - W % 2, H - H % 2

def sticker_pack(drawing_ids, presets, n):
    if n not in STICKER_COUNTS: raise ValueError("LINE sticker sets are 8/16/24/32/40")
    combos = [(d, p) for p in presets for d in drawing_ids]
    if len(combos) < n: raise ValueError("not enough drawing×pose combos")
    return [{"drawing_id": d, "preset": p, "text_th": PRESET_TH[p]} for d, p in combos[:n]]

def coloring_line_px(age):
    return 8 if age <= 4 else 6 if age <= 6 else 4

def daily_prompt(on, history):
    """history: list of (iso_date, prompt). Skip prompts used in last PROMPT_NO_REPEAT_DAYS days."""
    d = dt.date.fromisoformat(on)
    recent = {p for day, p in history if 0 <= (d - dt.date.fromisoformat(day)).days < PROMPT_NO_REPEAT_DAYS}
    i = d.toordinal() % len(DRAW_PROMPTS)
    for k in range(len(DRAW_PROMPTS)):
        p = DRAW_PROMPTS[(i + k) % len(DRAW_PROMPTS)]
        if p not in recent: return p
    return DRAW_PROMPTS[i]

def share_link(created, days=7, allow_download=False):
    return {"expires_on": (dt.date.fromisoformat(created) + dt.timedelta(days=days)).isoformat(), "view_only": not allow_download,
            "allow_download": allow_download, "strip_location": True, "indexable": False}

def print_check(px_w, px_h, product):
    a, b, need = PRODUCTS[product]
    short_px, long_px = sorted((px_w, px_h)); sa, lb = sorted((a, b))
    dpi = int(min(short_px / (sa / 2.54), long_px / (lb / 2.54)))
    return {"product": product, "dpi": dpi, "need_dpi": need, "ok": dpi >= need}

def parent_gate(action, parent_unlocked):
    return {"action": action, "needs_parent": action in PARENT_ONLY, "allowed": parent_unlocked or action not in PARENT_ONLY}

def quota(kind, used_today, wanted, pro=False):
    cap = FREE_ANIM_PER_DAY if kind == "animate" else FREE_STORY_PER_DAY
    if pro: return {"kind": kind, "allowed": wanted, "left_after": None, "paywall": False}
    left = max(0, cap - used_today); allowed = min(left, wanted)
    return {"kind": kind, "allowed": allowed, "left_after": left - allowed, "paywall": wanted > allowed}

def share_card(drawing, kid, age_label, preset):
    return {"title_th": drawing["title_th"], "headline_th": f"รูปวาดของ{kid['name_th']} ({age_label}) {PRESET_TH[preset]}ได้แล้ว!",
            "preset": preset, "watermark": WATERMARK, "cta_th": "ลองปลุกรูปวาดลูกคุณ ลิงก์ในคอมเมนต์", "shows_child_face": False}
