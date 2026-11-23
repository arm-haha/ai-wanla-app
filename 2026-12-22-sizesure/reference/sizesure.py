"""SizeSure reference logic — deterministic, no network. Two photos (front + side, fitted clothes) + your height →
body measurements (ellipse model from width × depth), shop size-chart normaliser (inch→cm, flat-lay ×2), size pick with a
per-area fit meter, shoe size from a foot on A4 paper, size passport, gift helper, return-risk, measurement log, share/Reel,
quota and a privacy & safety guard. Estimates only — always compare with the shop's own chart. No body judgement, ever."""
import math
import datetime as _dt

A4_CM = (21.0, 29.7)
INCH = 2.54
CALIB = {"chest": 1.03, "waist": 1.0, "hip": 1.02}          # ellipse → real body perimeter
CLOTH_EASE = {"fitted": 0.0, "normal": 2.0, "loose": 5.0, "bulky": 9.0}   # cm to subtract from circumference
CLOTH_ERR = {"fitted": 2.0, "normal": 3.0, "loose": 5.0, "bulky": 8.0}    # ± cm margin
CIRC = ("chest", "waist", "hip")
AREA_TH = {"chest": "รอบอก", "waist": "เอว", "hip": "สะโพก"}
LINEAR = ("length", "shoulder", "inseam", "sleeve")
KINDS = {  # target ease (garment − body, cm) per area by fit preference
    "top":    {"slim": {"chest": 4, "waist": 4, "hip": 4}, "regular": {"chest": 8, "waist": 8, "hip": 8}, "oversize": {"chest": 16, "waist": 16, "hip": 16}},
    "dress":  {"slim": {"chest": 3, "waist": 3, "hip": 4}, "regular": {"chest": 6, "waist": 6, "hip": 7}, "oversize": {"chest": 12, "waist": 14, "hip": 14}},
    "bottom": {"slim": {"waist": 0, "hip": 2, "chest": 0}, "regular": {"waist": 2, "hip": 5, "chest": 0}, "oversize": {"waist": 6, "hip": 10, "chest": 0}},
}
STRETCH = {"none": 0, "some": 3, "high": 6}
GENERIC = {  # built-in body chart (cm) — TH/Asian unisex tops, used when the shop has no chart
    "S": {"chest": [84, 89], "waist": [68, 73], "hip": [88, 93]}, "M": {"chest": [90, 95], "waist": [74, 79], "hip": [94, 99]},
    "L": {"chest": [96, 101], "waist": [80, 85], "hip": [100, 105]}, "XL": {"chest": [102, 107], "waist": [86, 91], "hip": [106, 111]},
    "2XL": {"chest": [108, 113], "waist": [92, 97], "hip": [112, 117]},
}
SHOES = [  # foot length cm → EU, US women, US men, UK (approximate, brand charts vary)
    (22.0, 35, 5, 3.5, 2.5), (22.5, 35.5, 5.5, 4, 3), (23.0, 36, 6, 4.5, 3.5), (23.5, 37, 6.5, 5, 4), (24.0, 38, 7, 5.5, 4.5),
    (24.5, 38.5, 7.5, 6, 5), (25.0, 39, 8, 6.5, 5.5), (25.5, 40, 8.5, 7, 6), (26.0, 40.5, 9, 7.5, 6.5), (26.5, 41, 9.5, 8, 7),
    (27.0, 42, 10, 8.5, 7.5), (27.5, 42.5, 10.5, 9, 8), (28.0, 43, 11, 9.5, 8.5), (28.5, 44, 11.5, 10, 9), (29.0, 44.5, 12, 10.5, 9.5),
    (29.5, 45, 12.5, 11, 10), (30.0, 46, 13, 12, 11)]
GUARD = {None: ("ok", "ตัวเลขเป็นค่าประมาณ ใช้เลือกไซซ์ประกอบตารางของร้านเสมอ รูปถูกลบหลังวัด"),
         "nudity": ("stop", "ต้องใส่เสื้อผ้าพอดีตัว (เช่น เสื้อยืด+เลกกิ้ง) ห้ามถ่ายแบบไม่ใส่เสื้อผ้าหรือชุดชั้นในอย่างเดียว"),
         "minor_photo": ("stop", "อายุต่ำกว่า 18 ปี ไม่ใช้การวัดจากรูป — ให้ผู้ปกครองวัดด้วยสายวัดแล้วกรอกตัวเลขแทน"),
         "other_person": ("stop", "วัดได้เฉพาะตัวเอง หรือคนที่อยู่ด้วยและยินยอมเท่านั้น ห้ามใช้รูปคนอื่นจากโซเชียล"),
         "multiple_people": ("warn", "เห็นหลายคนในรูป ให้ถ่ายทีละคน"),
         "body_shaming": ("stop", "แอปไม่ให้คะแนนรูปร่าง ไม่คำนวณ 'หุ่นดี/ไม่ดี' และไม่แนะนำลดน้ำหนัก"),
         "loose_clothes": ("warn", "เสื้อผ้าหลวม ตัวเลขอาจคลาด ±5 ซม. ใส่ชุดพอดีตัวแล้วถ่ายใหม่จะแม่นขึ้น"),
         "medical_use": ("warn", "ไม่ใช้แทนการวัดทางการแพทย์หรือตัดชุดพิธีที่ต้องเป๊ะ ให้ช่างวัดจริง")}
REEL_SHOTS = [("problem", "กล่องพัสดุ + เสื้อคับ \"สั่งออนไลน์ไซซ์ไม่เคยพอดี?\""), ("photos", "ถ่ายหน้า-ข้าง 2 รูป เส้นวัดวิ่งบนตัว"),
              ("numbers", "ตัวเลขรอบอก เอว สะโพกเด้งขึ้น"), ("chart", "แคปตารางไซซ์ร้าน → ไฮไลต์ M พอดี"),
              ("fit", "มิเตอร์ พอดี/คับ/หลวม รายจุด + รองเท้าบน A4"), ("cta", "คอมเมนต์ SIZE รับแพ็กฟรี")]


def _r(x, n=1):
    return round(x + 0.0, n)


def photo_check(light, full_body, pose_ok, clothing, ref_visible):
    if not 0 <= light <= 1:
        raise ValueError("light 0..1")
    if clothing not in CLOTH_EASE:
        raise ValueError("clothing")
    score = round(100 * (0.3 * light + 0.25 * full_body + 0.2 * pose_ok + 0.15 * (1 - list(CLOTH_EASE).index(clothing) / 3) + 0.1 * ref_visible))
    tips = []
    if light < 0.6: tips.append("ยืนหันหน้าเข้าหาแสง เปิดไฟให้สว่าง")
    if not full_body: tips.append("ถอยให้เห็นตั้งแต่หัวจรดเท้า วางมือถือระดับเอว")
    if not pose_ok: tips.append("ยืนตรง แขนกางออกเล็กน้อย เท้าห่างกันราวช่วงไหล่")
    if clothing in ("loose", "bulky"): tips.append("เปลี่ยนเป็นเสื้อยืดพอดีตัว + เลกกิ้ง/กางเกงรัดรูป")
    if not ref_visible: tips.append("แปะกระดาษ A4 ไว้ที่ผนังข้างตัวเพื่อช่วยเช็กสเกล")
    return {"score": score, "ok": score >= 75 and not tips, "tips_th": tips}


def ellipse_circ(width, depth):
    """Ramanujan perimeter of an ellipse with axes width × depth (cm)."""
    a, b = width / 2, depth / 2
    return math.pi * (3 * (a + b) - math.sqrt((3 * a + b) * (a + 3 * b)))


def measure_body(ai, height_cm):
    """ai = AiBodyMeasure (pixel widths from front & side photos). Height is typed by the user; A4 on the wall cross-checks scale."""
    if not 100 <= height_cm <= 220:
        raise ValueError("height 100–220 cm")
    f, sd = ai["front"], ai["side"]
    sf, ss = height_cm / f["height_px"], height_cm / sd["height_px"]
    scale_note, warn = None, []
    if ai.get("a4_px"):
        sa = A4_CM[1] / ai["a4_px"]
        dev = abs(sa - sf) / sf
        if dev > 0.05:
            warn.append("scale_mismatch"); scale_note = "สเกลจาก A4 ต่างจากส่วนสูง %d%% ใช้ค่าเฉลี่ย" % round(dev * 100)
            sf = (sf + sa) / 2
    cloth = ai["clothing"]
    out = {}
    for k in CIRC:
        c = ellipse_circ(f[k + "_px"] * sf, sd[k + "_px"] * ss) * CALIB[k] - CLOTH_EASE[cloth]
        out[k] = _r(c)
    out["shoulder"] = _r(f["shoulder_px"] * sf)
    out["inseam"] = _r(f["inseam_px"] * sf)
    out["sleeve"] = _r(f["arm_px"] * sf)
    if cloth in ("loose", "bulky"):
        warn.append("loose_clothes")
    return {"height_cm": height_cm, "cm": out, "margin_cm": CLOTH_ERR[cloth], "clothing": cloth, "warnings": warn, "scale_note_th": scale_note,
            "source": "photo"}


def override(meas, tape):
    """tape-measure values win; margin drops to ±1 cm for those areas."""
    m = {"height_cm": meas["height_cm"], "cm": dict(meas["cm"]), "margin_cm": meas["margin_cm"], "clothing": meas["clothing"],
         "warnings": list(meas["warnings"]), "scale_note_th": meas["scale_note_th"], "source": meas["source"]}
    for k, v in tape.items():
        if k not in m["cm"]:
            raise ValueError("unknown area " + k)
        m["cm"][k] = _r(v)
    if tape:
        m["source"] = "tape" if set(tape) >= set(CIRC) else "mixed"
        if m["source"] == "tape":
            m["margin_cm"] = 1.0
    return m


def to_inch(cm):
    return _r(cm / INCH)


def normalize_chart(chart):
    """AiChartRead → rows in cm with [lo, hi] ranges. unit inch → ×2.54; method 'flat' (วัดแบบวางราบ) → circumference ×2."""
    unit, method = chart["unit"], chart["method"]
    if unit not in ("cm", "inch") or method not in ("body", "garment", "flat"):
        raise ValueError("unit/method")
    rows = []
    for r in chart["rows"]:
        vals = {}
        for k, v in r["values"].items():
            lo, hi = (v, v) if not isinstance(v, list) else v
            f = (INCH if unit == "inch" else 1) * (2 if method == "flat" and k in CIRC else 1)
            vals[k] = [_r(lo * f), _r(hi * f)]
        rows.append({"label": r["label"], "cm": vals})
    return {"shop_th": chart.get("shop_th", ""), "kind": "body" if method == "body" else "garment", "rows": rows,
            "converted": unit == "inch" or method == "flat", "note_th": ("ตารางวัดแบบวางราบ คูณ 2 ให้แล้ว" if method == "flat" else None)}


def _area_fit(area, body, rng, chart_kind, kind, fit, stretch, margin):
    lo, hi = rng
    if chart_kind == "body":
        tol_tight = 1.5 + STRETCH[stretch] / 2   # stretchy fabric forgives a bit of tightness
        if body < lo - 1.5:
            d = body - lo; label = "loose"
        elif body > hi + tol_tight:
            d = body - hi; label = "tight"
        else:
            d = 0.0; label = "good"
        ease = _r((lo + hi) / 2 - body)
        dev = abs(d) + (3 if label == "tight" else 1 if label == "loose" else 0)
    else:
        mid = (lo + hi) / 2
        ease = _r(mid - body)
        tgt = KINDS[kind][fit][area]
        low, high = tgt - 4 - STRETCH[stretch], tgt + 6
        label = "tight" if ease < low else ("loose" if ease > high else "good")
        dev = abs(ease - tgt) if label == "good" else abs(ease - tgt) + 3
    return {"area": area, "body_cm": body, "range_cm": [lo, hi], "ease_cm": ease, "label": label}, dev


def recommend(meas, chart, kind="top", fit="regular", stretch="none"):
    """pick the row with the smallest weighted deviation over the areas present in both chart and body."""
    if kind not in KINDS or fit not in KINDS[kind] or stretch not in STRETCH:
        raise ValueError("kind/fit/stretch")
    weights = {"top": {"chest": 3, "waist": 1, "hip": 1}, "dress": {"chest": 2, "waist": 2, "hip": 2}, "bottom": {"chest": 0, "waist": 3, "hip": 2}}[kind]
    scored = []
    for r in chart["rows"]:
        areas, total = [], 0.0
        for a in CIRC:
            if a in r["cm"] and a in meas["cm"] and weights[a]:
                fa, dev = _area_fit(a, meas["cm"][a], r["cm"][a], chart["kind"], kind, fit, stretch, meas["margin_cm"])
                areas.append(fa); total += dev * weights[a]
        if areas:
            scored.append((round(total, 2), r["label"], areas))
    if not scored:
        raise ValueError("chart has no usable areas")
    order = sorted(range(len(scored)), key=lambda i: (scored[i][0], i))
    best = scored[order[0]]; second = scored[order[1]] if len(order) > 1 else None
    tight = [a["area"] for a in best[2] if a["label"] == "tight"]
    loose = [a["area"] for a in best[2] if a["label"] == "loose"]
    between = second is not None and second[0] - best[0] < 3.0
    conf = "high" if meas["margin_cm"] <= 2 and not tight and not loose and not between else ("low" if meas["margin_cm"] >= 5 or len(tight) + len(loose) >= 2 else "medium")
    th = lambda xs: "/".join(AREA_TH[x] for x in xs)
    if tight:
        adv = "ไซซ์ %s ยังคับที่%s ลองไซซ์ใหญ่ขึ้นหรือเลือกผ้ายืด" % (best[1], th(tight))
    elif between:
        s_tight = [a["area"] for a in second[2] if a["label"] == "tight"]
        if s_tight:
            adv = "อยู่ระหว่าง %s กับ %s — แนะนำ %s เพราะ %s คับที่%s" % (best[1], second[1], best[1], second[1], th(s_tight))
        else:
            labels = [r["label"] for r in chart["rows"]]
            small, big = sorted([best[1], second[1]], key=labels.index)
            adv = "อยู่ระหว่าง %s กับ %s — ชอบพอดีตัวเลือก %s ชอบหลวมสบายเลือก %s" % (small, big, small, big)
    elif loose:
        adv = "แนะนำไซซ์ %s (หลวมนิดที่%s)" % (best[1], th(loose))
    else:
        adv = "แนะนำไซซ์ %s พอดีทุกจุดที่วัด" % best[1]
    return {"best": best[1], "second": second[1] if second else None, "fit": best[2], "between_sizes": between, "confidence": conf, "advice_th": adv,
            "kind": kind, "fit_pref": fit, "stretch": stretch}


def shoe_size(foot_px, a4_px, width_px=None):
    """foot standing on A4 paper (long side 29.7 cm): length in cm → sizes; +0.5 cm toe room, rounded up to 0.5."""
    if a4_px <= 0 or foot_px <= 0:
        raise ValueError("pixels must be > 0")
    L = foot_px * A4_CM[1] / a4_px
    if not 12 <= L <= 32:
        raise ValueError("foot length out of range: %.1f" % L)
    fit_cm = math.ceil((L + 0.5) * 2) / 2
    row = min(SHOES, key=lambda r: (abs(r[0] - fit_cm), r[0]))
    width = None
    if width_px:
        ratio = width_px / foot_px
        width = "narrow" if ratio < 0.36 else ("regular" if ratio < 0.40 else "wide")
    out_of_table = fit_cm < SHOES[0][0] or fit_cm > SHOES[-1][0]
    return {"foot_cm": _r(L), "shoe_cm": fit_cm, "eu": row[1], "us_women": row[2], "us_men": row[3], "uk": row[4], "width": width,
            "approx": True, "note_th": "เด็ก/เท้าเล็กกว่าตาราง ใช้ตารางเด็กของร้าน" if out_of_table else ("หน้าเท้ากว้าง เลือกรุ่นหน้ากว้าง (Wide) หรือขยับขึ้นครึ่งไซซ์" if width == "wide" else None)}


def passport(person, meas, shoe=None):
    """one card with everything needed to shop: generic top size, Thai jeans waist in inches, shoe sizes."""
    gen = {"kind": "body", "rows": [{"label": k, "cm": v} for k, v in GENERIC.items()]}
    top = recommend(meas, gen, "top")["best"]
    waist_in = round(meas["cm"]["waist"] / INCH)
    return {"name_th": person["name_th"], "updated": person.get("updated", ""), "top": top, "jeans_waist_in": waist_in,
            "cm": {k: meas["cm"][k] for k in ("chest", "waist", "hip")}, "inch": {k: to_inch(meas["cm"][k]) for k in ("chest", "waist", "hip")},
            "shoe_eu": shoe["eu"] if shoe else None, "margin_cm": meas["margin_cm"], "share_numbers": False}


def gift_pick(pp, kind="top", fit="regular"):
    """buying for someone else from their shared passport: size up when between sizes for tops, keep receipt for exchange."""
    order = list(GENERIC)
    size = pp["top"]
    if kind == "top" and fit == "oversize" and order.index(size) < len(order) - 1:
        size = order[order.index(size) + 1]
    return {"for_th": pp["name_th"], "kind": kind, "size": size, "jeans_waist_in": pp["jeans_waist_in"] if kind == "bottom" else None,
            "shoe_eu": pp["shoe_eu"] if kind == "shoes" else None,
            "tip_th": "ถามร้านเรื่องเปลี่ยนไซซ์ได้ไหมก่อนซื้อ และเก็บใบเสร็จ/ป้ายไว้"}


def return_risk(rec, chart_converted, reviews=None):
    """reviews: 'true_to_size' | 'runs_small' | 'runs_large' | None → low / medium / high."""
    pts, why = 0, []
    if rec["confidence"] == "low": pts += 2; why.append("ตัวเลขคลาดเคลื่อนสูง")
    elif rec["confidence"] == "medium": pts += 1
    if rec["between_sizes"]: pts += 1; why.append("อยู่ระหว่างสองไซซ์")
    if any(a["label"] != "good" for a in rec["fit"]): pts += 2; why.append("บางจุดคับ/หลวม")
    if reviews == "runs_small": pts += 1; why.append("รีวิวบอกไซซ์เล็กกว่าปกติ — ขยับขึ้น 1 ไซซ์")
    if reviews == "runs_large": pts += 1; why.append("รีวิวบอกไซซ์ใหญ่กว่าปกติ")
    if not chart_converted and reviews is None: pts += 0
    level = "low" if pts <= 1 else ("medium" if pts <= 3 else "high")
    return {"level": level, "points": pts, "reasons_th": why, "tip_th": {"low": "สั่งได้เลย", "medium": "เช็กนโยบายเปลี่ยนคืนก่อนสั่ง", "high": "แชตถามร้านพร้อมตัวเลขของคุณก่อนสั่ง"}[level]}


def log_summary(entries, today, hide_numbers=False):
    """measurement log: neutral wording, no weight/BMI, optional hidden numbers."""
    es = sorted(entries, key=lambda e: e["date"])
    last = es[-1] if es else None
    prev = es[-2] if len(es) > 1 else None
    change = {k: _r(last["cm"][k] - prev["cm"][k]) for k in CIRC} if prev else {}
    days = (_dt.date.fromisoformat(today) - _dt.date.fromisoformat(last["date"])).days if last else None
    return {"today": today, "entries": len(es), "last_date": last["date"] if last else None, "days_since": days,
            "change_cm": {} if hide_numbers else change, "hidden": hide_numbers,
            "remeasure": days is None or days >= 90, "note_th": "ไซซ์เปลี่ยนได้ตามฤดูและเสื้อผ้า วัดใหม่ทุก 3 เดือนหรือก่อนช้อปใหญ่"}


def share_card(pp, layout="size_card"):
    if layout not in ("size_card", "before_after", "fit_meter"):
        raise ValueError("layout")
    return {"layout": layout, "size": "1080x1350", "shows_numbers": False, "top": pp["top"], "shoe_eu": pp["shoe_eu"],
            "watermark": "SizeSure · AI วันละแอป", "badge_th": "สั่งออนไลน์ ไซซ์พอดีตั้งแต่ครั้งแรก"}


def reel_plan(seconds=20):
    if not 15 <= seconds <= 30:
        raise ValueError("Reel must be 15–30 s")
    n = len(REEL_SHOTS); cut = [round(seconds * i / n, 1) for i in range(n + 1)]
    return {"seconds": seconds, "ratio": "9:16", "bpm": 120,
            "shots": [{"kind": k, "start": cut[i], "end": cut[i + 1], "caption_th": c} for i, (k, c) in enumerate(REEL_SHOTS)],
            "watermark": "SizeSure · AI วันละแอป"}


def quota(used_today, plan="free"):
    limit = {"free": 3, "plus": 30}[plan]
    return {"plan": plan, "measures_per_day": limit, "used": used_today, "left": max(0, limit - used_today), "blocked": used_today >= limit}


def privacy_check(age, self_or_consented, found=()):
    """found: flags from the vision model ('nudity', 'multiple_people', 'loose_clothes')."""
    flags = []
    if age < 18: flags.append("minor_photo")
    if not self_or_consented: flags.append("other_person")
    for f in ("nudity", "multiple_people", "loose_clothes"):
        if f in found: flags.append(f)
    level = "stop" if any(GUARD[f][0] == "stop" for f in flags) else ("warn" if flags else "ok")
    return {"allowed": level != "stop", "level": level, "flags": flags, "messages_th": [GUARD[f][1] for f in flags] or [GUARD[None][1]],
            "manual_entry_ok": True}


def safety_guard(flag=None):
    level, msg = GUARD[flag]
    return {"flag": flag, "level": level, "message_th": msg, "block": level == "stop"}
