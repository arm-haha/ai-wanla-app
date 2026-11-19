"""HandFont reference logic — deterministic, no network. Turns a photographed handwriting template sheet into a personal font
(Thai + English). Glyph extraction is done by the vision model / vectoriser in the real app; this module holds the rules:
scan quality, per-cell checks, coverage, Thai mark placement, style tuning, layout, cards, practice, diary, quota and guard.
Your OWN handwriting only. The font is for personal/creative use — never for signatures, forged documents or imitating someone else."""
import datetime as _dt

TH_CONS = list("กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธนบปผฝพฟภมยรลวศษสหฬอฮ")          # 44
TH_UPPER = list("\u0e31\u0e34\u0e35\u0e36\u0e37\u0e47\u0e4c\u0e4d")        # ั ิ ี ึ ื ็ ์ ํ
TH_LOWER = list("\u0e38\u0e39\u0e3a")                                      # ุ ู ฺ
TH_TONE = list("\u0e48\u0e49\u0e4a\u0e4b")                                 # ่ ้ ๊ ๋
TH_SPACING = list("ะาำเแโใไๅๆฯฤฦ")                                         # spacing vowels / signs
TH_DIGITS = list("๐๑๒๓๔๕๖๗๘๙")
LAT_UPPER = [chr(c) for c in range(65, 91)]
LAT_LOWER = [chr(c) for c in range(97, 123)]
DIGITS = list("0123456789")
PUNCT = list(".,!?:;'\"()-/@#&฿%")
ASCENDER = set("ปฝฟฬ")          # tall: upper marks shift left
DESCENDER_CUT = set("ญฐ")       # tail removed when a lower vowel is attached
DESCENDER = set("ฎฏ")           # lower vowels shift down
TEMPLATES = {  # cells per A4 sheet = 80
    "thai_quick":  {"th": "ไทยด่วน (1 แผ่น)",     "sets": ["TH_CONS", "TH_UPPER", "TH_LOWER", "TH_TONE", "TH_SPACING"], "pages": 1},
    "thai_full":   {"th": "ไทยครบ + เลข + เครื่องหมาย", "sets": ["TH_CONS", "TH_UPPER", "TH_LOWER", "TH_TONE", "TH_SPACING", "TH_DIGITS", "DIGITS", "PUNCT"], "pages": 2},
    "english":     {"th": "อังกฤษ",               "sets": ["LAT_UPPER", "LAT_LOWER", "DIGITS", "PUNCT"], "pages": 1},
    "bilingual":   {"th": "ไทย + อังกฤษ ครบชุด",   "sets": ["TH_CONS", "TH_UPPER", "TH_LOWER", "TH_TONE", "TH_SPACING", "TH_DIGITS", "LAT_UPPER", "LAT_LOWER", "DIGITS", "PUNCT"], "pages": 3},
}
SETS = {"TH_CONS": TH_CONS, "TH_UPPER": TH_UPPER, "TH_LOWER": TH_LOWER, "TH_TONE": TH_TONE, "TH_SPACING": TH_SPACING,
        "TH_DIGITS": TH_DIGITS, "LAT_UPPER": LAT_UPPER, "LAT_LOWER": LAT_LOWER, "DIGITS": DIGITS, "PUNCT": PUNCT}
CORE = {"TH_CONS", "TH_UPPER", "TH_LOWER", "TH_TONE", "TH_SPACING", "LAT_UPPER", "LAT_LOWER"}
CELLS_PER_PAGE = 80
WEIGHTS = {"thin": 2, "regular": 4, "bold": 7}            # stroke px at 1000 upm / 100
ROUGH = {"clean": 0.0, "natural": 0.35, "sketchy": 0.7}
PAPERS = {"plain": "#FFFFFF", "lined": "#FFFDF5", "grid": "#FAFCFF", "kraft": "#E9D6B8", "pastel_pink": "#FDE7EC", "notebook_blue": "#EEF4FF"}
INKS = {"black": "#1F1F1F", "blue_pen": "#1F3FBF", "red_pen": "#C62828", "pencil": "#6B6B6B", "brown": "#5D4037", "white_on_dark": "#FFFFFF"}
CARDS = {  # occasion, size, max chars, default paper/ink
    "birthday":   {"th": "การ์ดวันเกิด",        "size": "A6", "max": 160, "paper": "pastel_pink",  "ink": "black"},
    "thank_you":  {"th": "การ์ดขอบคุณ",         "size": "A6", "max": 140, "paper": "kraft",        "ink": "brown"},
    "love_note":  {"th": "โน้ตบอกรัก",          "size": "A6", "max": 120, "paper": "pastel_pink",  "ink": "red_pen"},
    "wedding":    {"th": "การ์ดอวยพรงานแต่ง",    "size": "A5", "max": 220, "paper": "plain",        "ink": "black"},
    "new_year":   {"th": "ส.ค.ส. ปีใหม่",        "size": "A6", "max": 160, "paper": "kraft",        "ink": "black"},
    "teacher":    {"th": "การ์ดวันครู",          "size": "A6", "max": 140, "paper": "lined",        "ink": "blue_pen"},
    "shop_note":  {"th": "โน้ตขอบคุณลูกค้า (ร้านออนไลน์)", "size": "A7", "max": 90, "paper": "kraft", "ink": "black"},
}
EXPORTS = {"ttf": "ฟอนต์ติดตั้งในคอม/มือถือ", "otf": "ฟอนต์ OpenType (มี alternates)", "woff2": "ใช้บนเว็บ",
           "png_sticker": "สติกเกอร์ข้อความพื้นใส", "pdf_card": "การ์ดพร้อมพิมพ์", "pdf_practice": "แบบฝึกคัดลายมือ"}
GUARD = {None: ("ok", "ฟอนต์ลายมือนี้เพื่อใช้ส่วนตัว/งานสร้างสรรค์ ไม่ใช่ลายเซ็นและไม่ใช้แทนการเซ็นเอกสาร"),
         "not_own_handwriting": ("stop", "ใช้ได้เฉพาะลายมือของคุณเอง ห้ามสแกนลายมือคนอื่นมาทำฟอนต์"),
         "signature_detected": ("stop", "ตรวจพบลายเซ็น — แอปไม่ทำฟอนต์/สติกเกอร์จากลายเซ็นเพื่อป้องกันการปลอมแปลง"),
         "document_forgery": ("stop", "ห้ามใช้ฟอนต์ลายมือปลอมเอกสาร ใบรับรอง ใบลา หรือข้อความแทนผู้อื่น"),
         "under_13_no_parent": ("stop", "อายุต่ำกว่า 13 ปี ต้องให้ผู้ปกครองยืนยันก่อนใช้"),
         "personal_data_on_sheet": ("warn", "มีเลขบัตร/เบอร์โทร/ที่อยู่บนแผ่น ระบบจะเบลอก่อนประมวลผล"),
         "low_coverage": ("warn", "ตัวอักษรยังไม่ครบ ฟอนต์จะใช้ตัวสำรองแทนช่องที่ขาด"),
         "commercial_resale": ("warn", "ขายฟอนต์ลายมือตัวเองได้ แต่ห้ามอ้างว่าเป็นลายมือคนอื่นหรือคนดัง")}
REEL_SHOTS = [("blank_sheet", "แผ่นเปล่า + ปากกา \"ลายมือเราเป็นฟอนต์ได้ไหม?\""), ("writing", "เขียนเร่งสปีด 44 พยัญชนะ"),
              ("scan", "ถ่ายรูป ประกายสแกนทีละช่อง"), ("typing", "พิมพ์ในมือถือ ออกมาเป็นลายมือเรา"),
              ("card", "การ์ดวันเกิด + สติกเกอร์ IG Story"), ("cta", "คอมเมนต์ FONT รับแพ็กฟรี")]


def _r(x, n=2):
    return round(x + 0.0, n)


def template_chars(template):
    if template not in TEMPLATES:
        raise ValueError("unknown template")
    out = []
    for s in TEMPLATES[template]["sets"]:
        out += SETS[s]
    return out


def template_sheet(template):
    ch = template_chars(template)
    pages = -(-len(ch) // CELLS_PER_PAGE)
    return {"template": template, "name_th": TEMPLATES[template]["th"], "cells": len(ch), "pages": pages,
            "sets": list(TEMPLATES[template]["sets"]), "guide": "baseline+xheight+ascender",
            "tips_th": ["ใช้ปากกาหมึกดำหัว 0.5–0.7 มม.", "เขียนกลางช่อง ไม่ล้นเส้นกรอบ", "สระ/วรรณยุกต์เขียนในช่องของตัวเองตามเส้นไกด์"]}


def scan_quality(light, blur, skew_deg, ink_contrast):
    for v in (light, blur, ink_contrast):
        if not 0 <= v <= 1:
            raise ValueError("0..1")
    score = 100 - int(max(0, 0.7 - light) * 80) - int(blur * 60) - int(min(abs(skew_deg), 20) * 1.5) - int(max(0, 0.6 - ink_contrast) * 70)
    score = max(0, min(100, score))
    tips = []
    if light < 0.6: tips.append("แสงน้อย/มีเงา ถ่ายใกล้หน้าต่าง หรือเปิดไฟเพดาน ไม่ใช้แฟลช")
    if blur > 0.3: tips.append("ภาพเบลอ วางกระดาษบนโต๊ะ ถือมือถือให้นิ่ง แตะโฟกัสก่อนถ่าย")
    if abs(skew_deg) > 8: tips.append("กระดาษเอียง ให้มุมทั้ง 4 อยู่ในกรอบ (มีตัวช่วยจัดมุมอัตโนมัติ)")
    if ink_contrast < 0.5: tips.append("หมึกจางไป ใช้ปากกาหมึกดำเข้ม ไม่ใช้ดินสอ")
    return {"score": score, "ok": score >= 70, "tips_th": tips}


def sheet_scan(photo):
    return {"photo_id": photo["id"], "quality": scan_quality(photo["light"], photo["blur"], photo["skew_deg"], photo["ink_contrast"])}


def glyph_check(cell):
    """cell: char, ink (0..1 share of cell inked), touches_border bool, strokes int, extra_blobs int"""
    ink, st = cell["ink"], "ok"
    if ink < 0.01: st = "empty"
    elif ink < 0.03: st = "too_faint"
    elif cell["touches_border"]: st = "overflow"
    elif cell["extra_blobs"] > 2 or ink > 0.45: st = "messy"
    fix = {"ok": None, "empty": "ยังไม่ได้เขียนช่องนี้", "too_faint": "เส้นจางไป เขียนทับให้เข้มขึ้น",
           "overflow": "ตัวอักษรล้นกรอบ เขียนเล็กลงแล้วถ่ายใหม่เฉพาะช่องนี้", "messy": "มีรอยเลอะ/ขีดฆ่า เขียนใหม่ในช่องสำรอง"}[st]
    return {"char": cell["char"], "status": st, "usable": st == "ok", "fix_th": fix}


def coverage(template, checks):
    need = template_chars(template)
    good = {c["char"] for c in checks if c["usable"]}
    missing = [c for c in need if c not in good]
    core_need = [c for s in TEMPLATES[template]["sets"] if s in CORE for c in SETS[s]]
    core_have = sum(1 for c in core_need if c in good)
    pct = int(round(100 * (len(need) - len(missing)) / len(need)))
    core_pct = int(round(100 * core_have / len(core_need))) if core_need else 100
    return {"template": template, "total": len(need), "usable": len(need) - len(missing), "percent": pct,
            "core_percent": core_pct, "missing": missing[:40], "can_build": core_pct >= 90,
            "fallback_th": None if not missing else "ช่องที่ขาดจะใช้ตัวอักษรสำรองสไตล์ใกล้เคียงชั่วคราว ถ่ายเพิ่มทีหลังได้"}


def mark_kind(ch):
    if ch in TH_UPPER: return "upper_vowel"
    if ch in TH_LOWER: return "lower_vowel"
    if ch in TH_TONE: return "tone"
    return None


def clusters(text):
    """Split Thai/Latin text into display clusters: base char + attached marks."""
    out = []
    for ch in text:
        if mark_kind(ch) and out and out[-1]["base"] in TH_CONS + ["ฤ", "ฦ"]:
            out[-1]["marks"].append(ch)
        else:
            out.append({"base": ch, "marks": []})
    return out


def mark_placement(base, marks):
    """Thai typography rules for stacking marks on handwritten glyphs (units = % of em)."""
    has_upper = any(mark_kind(m) == "upper_vowel" for m in marks)
    res = []
    for m in marks:
        k = mark_kind(m)
        dx, dy, note = 0, 0, None
        if k in ("upper_vowel", "tone"):
            if base in ASCENDER:
                dx, note = -12, "หลบหางตัวสูง (ป ฝ ฟ ฬ)"
            if k == "tone":
                dy = 18 if has_upper else 0
                note = (note + " · " if note else "") + ("วรรณยุกต์ลอยเหนือสระบน" if has_upper else "วรรณยุกต์วางต่ำชิดตัวอักษร")
        elif k == "lower_vowel":
            if base in DESCENDER:
                dy, note = -10, "เลื่อนสระล่างลงให้พ้นหาง (ฎ ฏ)"
            elif base in DESCENDER_CUT:
                note = "ตัดเชิงล่างของ ญ/ฐ เมื่อมีสระล่าง"
        res.append({"mark": m, "kind": k, "dx": dx, "dy": dy, "note_th": note})
    return {"base": base, "cut_descender": base in DESCENDER_CUT and any(mark_kind(m) == "lower_vowel" for m in marks), "marks": res}


def style_params(weight="regular", slant=0, roughness="natural", tracking=0, baseline_jitter=None):
    if weight not in WEIGHTS or roughness not in ROUGH:
        raise ValueError("bad style")
    if not -15 <= slant <= 15 or not -50 <= tracking <= 100:
        raise ValueError("range")
    j = baseline_jitter if baseline_jitter is not None else {"clean": 0, "natural": 3, "sketchy": 6}[roughness]
    return {"weight": weight, "stroke": WEIGHTS[weight], "slant": slant, "roughness": roughness, "rough": ROUGH[roughness],
            "tracking": tracking, "baseline_jitter": j, "alternates": 1 if roughness == "clean" else 3}


def font_name(name_en):
    clean = "".join(c for c in name_en if c.isalnum())[:20] or "Me"
    return "HandFont-" + clean[0].upper() + clean[1:]


def font_build(person, template, cov, style, fmt="ttf"):
    if fmt not in EXPORTS:
        raise ValueError("format")
    if not cov["can_build"]:
        return {"ok": False, "family": font_name(person["name_en"]), "format": fmt, "glyphs": cov["usable"],
                "alternates": 0, "size_kb": 0, "reason_th": "ตัวหลักยังไม่ถึง 90% เขียนช่องที่ขาดเพิ่มก่อน"}
    alt = cov["usable"] * (style["alternates"] - 1)
    size = int((cov["usable"] + alt) * (1.6 if fmt == "otf" else 1.2 if fmt == "ttf" else 0.7)) + 8
    return {"ok": True, "family": font_name(person["name_en"]), "format": fmt, "glyphs": cov["usable"], "alternates": alt,
            "size_kb": size, "reason_th": None}


def pick_alternates(text, n_alt=3):
    """Deterministic alternate choice so repeated letters never look copy-pasted: index cycles per character."""
    seen, out = {}, []
    for ch in text:
        if ch.isspace():
            out.append(0); continue
        i = seen.get(ch, 0)
        out.append(i % n_alt); seen[ch] = i + 1
    return out


def adv_width(ch):
    if ch.isspace(): return 30
    if mark_kind(ch): return 0
    if ch in "ำ": return 55
    if ch in TH_CONS: return 58
    if ch in "เแโใไ": return 34 if ch != "แ" else 62
    if ch.isupper(): return 62
    if ch in DIGITS + TH_DIGITS: return 52
    if ch in PUNCT: return 24
    return 48


def text_preview(text, style, size_pt=24, max_width_mm=80):
    """Rough layout: width units → mm at size; wraps by words (spaces) — Thai without spaces wraps by cluster."""
    unit_mm = size_pt * 0.3528 / 100
    lines, cur, w = [], "", 0.0
    tokens = text.split(" ") if " " in text else [c["base"] + "".join(c["marks"]) for c in clusters(text)]
    sep = " " if " " in text else ""
    for t in tokens:
        tw = sum(adv_width(c) + style["tracking"] / 10 for c in t) * unit_mm
        add = tw + (adv_width(" ") * unit_mm if cur and sep else 0)
        if cur and w + add > max_width_mm:
            lines.append(cur); cur, w = t, tw
        else:
            cur = cur + sep + t if cur else t; w += add
    if cur: lines.append(cur)
    return {"text": text, "size_pt": size_pt, "lines": lines, "line_count": len(lines),
            "clusters": len(clusters(text)), "alternates_used": max(pick_alternates(text, style["alternates"]) + [0]) + 1}


def card_layout(kind, message, paper=None, ink=None):
    if kind not in CARDS:
        raise ValueError("card")
    c = CARDS[kind]
    paper, ink = paper or c["paper"], ink or c["ink"]
    if paper not in PAPERS or ink not in INKS:
        raise ValueError("paper/ink")
    too_long = len(message) > c["max"]
    size_pt = 28 if len(message) <= c["max"] * 0.4 else 22 if len(message) <= c["max"] * 0.75 else 18
    return {"kind": kind, "name_th": c["th"], "size": c["size"], "paper": paper, "paper_hex": PAPERS[paper], "ink": ink,
            "ink_hex": INKS[ink], "chars": len(message), "max_chars": c["max"], "fits": not too_long, "font_pt": size_pt,
            "warning_th": "ข้อความยาวเกิน ตัดให้สั้นลงหรือเปลี่ยนเป็นขนาด A5" if too_long else None}


def sticker_export(text, ink="black", outline=True):
    if ink not in INKS:
        raise ValueError("ink")
    w = sum(adv_width(c) for c in text) * 4 + 80
    return {"text": text, "format": "png_sticker", "ink_hex": INKS[ink], "outline": outline,
            "width_px": min(w, 1600), "height_px": 360 if len(text) <= 24 else 560, "transparent": True}


def practice_sheet(text, rows=6, mode="trace"):
    if mode not in ("trace", "copy", "free") or not 1 <= rows <= 12:
        raise ValueError("practice")
    return {"text": text, "rows": rows, "mode": mode, "guide_lines": 4 if any(c in TH_CONS for c in text) else 3,
            "opacity": {"trace": 0.25, "copy": 0.0, "free": 0.0}[mode], "paper": "A4"}


def practice_score(samples):
    """samples: list of {height_var, baseline_var, spacing_var, slant_var} 0..1 (lower = steadier)."""
    if not samples:
        raise ValueError("no samples")
    keys = ("height_var", "baseline_var", "spacing_var", "slant_var")
    avg = {k: sum(s[k] for s in samples) / len(samples) for k in keys}
    score = max(0, min(100, int(round(100 - 100 * (0.35 * avg["height_var"] + 0.3 * avg["baseline_var"] + 0.2 * avg["spacing_var"] + 0.15 * avg["slant_var"])))))
    worst = max(keys, key=lambda k: avg[k])
    tip = {"height_var": "ขนาดตัวไม่เท่ากัน ลองให้หัวตัวอักษรแตะเส้นกลางทุกตัว", "baseline_var": "ตัวอักษรลอย/จม เขียนให้ฐานวางบนเส้นบรรทัด",
           "spacing_var": "ช่องไฟไม่สม่ำเสมอ เว้นระยะเท่ากับความกว้างหัวตัว ก", "slant_var": "ตัวเอียงไม่เท่ากัน ลองวางกระดาษให้ตรงกับแขน"}[worst]
    grade = "A" if score >= 85 else "B" if score >= 70 else "C" if score >= 55 else "D"
    return {"samples": len(samples), "score": score, "grade": grade, "focus": worst, "tip_th": tip}


def reel_plan(family, seconds=20):
    if not 15 <= seconds <= 30:
        raise ValueError("15-30s")
    per = seconds / len(REEL_SHOTS)
    shots, t = [], 0.0
    for k, cap in REEL_SHOTS:
        shots.append({"kind": k, "start": _r(t, 1), "end": _r(t + per, 1), "caption_th": cap}); t += per
    return {"family": family, "seconds": seconds, "ratio": "9:16", "bpm": 112, "shots": shots, "watermark": "HandFont · AI วันละแอป"}


def diary_summary(entries, today):
    d0 = _dt.date.fromisoformat(today)
    builds = [e for e in entries if e["kind"] == "build"]
    practice = sorted({e["date"] for e in entries if e["kind"] == "practice"})
    streak, day = 0, d0
    while day.isoformat() in practice:
        streak += 1; day -= _dt.timedelta(days=1)
    scores = [e["score"] for e in entries if e["kind"] == "practice" and "score" in e]
    return {"today": today, "fonts_built": len(builds), "cards_made": sum(1 for e in entries if e["kind"] == "card"),
            "stickers_made": sum(1 for e in entries if e["kind"] == "sticker"), "practice_streak": streak,
            "best_score": max(scores) if scores else None, "improvement": (scores[-1] - scores[0]) if len(scores) >= 2 else 0,
            "latest_version": max([e.get("version", 1) for e in builds] + [0])}


def share_card(family, sample, layout="before_after"):
    if layout not in ("before_after", "alphabet_grid", "typed_note"):
        raise ValueError("layout")
    return {"family": family, "sample_text": sample, "layout": layout, "size": "1080x1350",
            "watermark": "HandFont · AI วันละแอป", "badge_th": "ลายมือจริงของเจ้าของ แปลงเป็นฟอนต์"}


def quota(used_today, plan="free"):
    lim = {"free": 2, "plus": 20}[plan]
    return {"plan": plan, "builds_per_day": lim, "used": used_today, "left": max(0, lim - used_today), "blocked": used_today >= lim}


def consent_check(age, own_handwriting, parent_ok=False, signature=False, purpose="personal"):
    flags = []
    if not own_handwriting: flags.append("not_own_handwriting")
    if signature: flags.append("signature_detected")
    if purpose == "forgery": flags.append("document_forgery")
    if age < 13 and not parent_ok: flags.append("under_13_no_parent")
    if purpose == "resale": flags.append("commercial_resale")
    level = "stop" if any(GUARD[f][0] == "stop" for f in flags) else "warn" if flags else "ok"
    return {"allowed": level != "stop", "level": level, "flags": flags, "messages_th": [GUARD[f][1] for f in flags] or [GUARD[None][1]]}


def safety_guard(flag=None):
    lv, msg = GUARD[flag]
    return {"flag": flag, "level": lv, "message_th": msg, "block": lv == "stop"}
