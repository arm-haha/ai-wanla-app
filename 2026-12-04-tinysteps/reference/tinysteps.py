"""TinySteps deterministic logic (no AI calls). Milestone photo cards — not medical or developmental advice."""
import datetime as _dt

FIRSTS = {
    "smile": {"id": "f01", "name_th": "ยิ้มครั้งแรก", "example_month": 2, "range": (1, 3)},
    "roll": {"id": "f02", "name_th": "พลิกตัว", "example_month": 5, "range": (4, 6)},
    "sit": {"id": "f03", "name_th": "นั่งทรงตัวได้", "example_month": 8, "range": (6, 9)},
    "crawl": {"id": "f04", "name_th": "คลาน", "example_month": 9, "range": (7, 11)},
    "stand": {"id": "f05", "name_th": "ยืนกำกำ", "example_month": 10, "range": (8, 12)},
    "wave": {"id": "f06", "name_th": "โบกมือ", "example_month": 10, "range": (8, 13)},
    "walk": {"id": "f07", "name_th": "ก้าวแรก", "example_month": 13, "range": (10, 18)},
    "word": {"id": "f08", "name_th": "คำแรก", "example_month": 12, "range": (10, 16)},
}
FIRST_IDS = list(FIRSTS)
CAPTION_BANK = {
    "smile": ["ยิ้มนี้คือของขวัญทั้งบ้าน", "เก็บรอยยิ้มแรกไว้ให้ดูอีกสิบปี"],
    "roll": ["พลิกได้แล้ว โลกกว้างขึ้นอีกนิด", "วันนี้พลิกเองได้ ทั้งบ้านปรบมือ"],
    "sit": ["เดือนนี้เพิ่งนั่งทรงตัวได้ เก็บช่วงนี้ไว้ในอัลบั้มนะ", "นั่งได้เองแล้ว โลกมองสูงขึ้น"],
    "crawl": ["คลานสำรวจบ้าน เริ่มยุคที่ของต้องยกสูง", "มือแล้วเท้าแล้ว ไปได้เองแล้วนะ"],
    "stand": ["ยืนกำกำได้แล้ว สูงขึ้นอีกนิด", "ยืนได้แล้ว ยังต้องมีมือจับอยู่"],
    "wave": ["โบกมือบ๊ายบาย ได้คลิปน่ารักทั้งครอบครัว", "โบกมือได้แล้ว ทักทายทั้งบ้าน"],
    "walk": ["ก้าวแรกของเรา บ้านนี้ไม่เหมือนเดิมแล้ว", "ก้าวเล็ก ๆ ที่ทั้งบ้านจำได้"],
    "word": ["คำแรกในบ้านนี้ ขอเก็บไว้ในอัลบั้ม", "พูดได้แล้วนะ คำแรกของเรา"],
}
PLAY_IDEAS = {
    1: ["คุยและยิ้มให้ลูกขณะอุ้ม", "วางให้นอนคว่ำสั้น ๆ ใต้สายตาผู้ใหญ่"],
    8: ["นั่งเล่นกับหมอนค้ำด้านข้าง", "ให้หยิบของชิ้นใหญ่ด้วยสองมือ"],
    12: ["อ่านหนังสือภาพสั้น ๆ ทุกวัน", "ร้องเพลงและปรบมือตามจังหวะ"],
}
FREE_GENS_PER_DAY = 3
WATERMARK = "Made with TinySteps · not medical advice"
SAFETY_DISCLAIMER_TH = "TinySteps เป็นการ์ดความทรงจำ ไม่ใช่คำแนะนำทางการแพทย์ ไม่ใช่แบบประเมินพัฒนาการ และไม่ใช่กราฟการเจริญเติบโตทางการ ถ้ากังวลเรื่องสุขภาพหรือพัฒนาการของลูก ให้ปรึกษาแพทย์"
CONSENT_DISCLAIMER_TH = "ใช้ได้เฉพาะรูปของลูกตนเอง (หรือรูปที่ผู้ปกครองทุกคนยินยอม) ห้ามอัปโหลดรูปเด็กคนอื่น และควรคิดก่อนแชร์รูปเด็กในที่สาธารณะ"

def scan_quality(glare, blur, crop):
    for v in (glare, blur, crop):
        if not 0 <= v <= 1:
            raise ValueError("glare/blur/crop must be 0..1")
    score = int(round(100 * (1 - (0.30 * glare + 0.40 * blur + 0.30 * crop))))
    tips = []
    if glare > 0.5:
        tips.append("แสงสะท้อนบนหน้า หันจากหน้าต่างหรือปิดแฟลชแรง ๆ")
    if blur > 0.4:
        tips.append("ภาพเบลอ ถือนิ่งหรือใช้โหมดถ่ายต่อเนื่อง")
    if crop > 0.45:
        tips.append("ถูกครอป จัดให้เห็นหัวถึงลำตัวในกรอบ")
    return {"score": score, "ok": score >= 60, "tips_th": tips}


def photo_scan(photo):
    q = scan_quality(photo["glare"], photo["blur"], photo["crop"])
    return {"photo_id": photo["id"], "quality": q, "child_id": photo.get("child_id")}


def pipeline_steps(photo):
    s = ["photo"]
    if photo["glare"] > 0.5:
        s.append("deglare")
    if photo["crop"] > 0.45:
        s.append("recrop")
    s += ["age_months", "milestone_card", "caption"]
    return s


def age_months(birth, on_date):
    b, d = _dt.date.fromisoformat(birth), _dt.date.fromisoformat(on_date)
    if d < b:
        raise ValueError("date is before birth")
    months = (d.year - b.year) * 12 + (d.month - b.month)
    if d.day < b.day:
        months -= 1
    return months


def example_band(month):
    """Invented UI bands only — not a clinical growth standard."""
    if month not in range(0, 37):
        raise ValueError("month must be 0..36")
    w_mid = round(3.2 + month * 0.65, 1)
    h_mid = round(50 + month * 2.5, 1)
    return {
        "month": month,
        "weight_lo_kg": round(w_mid - 1.5, 1), "weight_mid_kg": w_mid, "weight_hi_kg": round(w_mid + 1.5, 1),
        "height_lo_cm": round(h_mid - 4, 1), "height_mid_cm": h_mid, "height_hi_cm": round(h_mid + 4, 1),
        "disclaimer_th": "แถบตัวอย่างในแอปเท่านั้น ไม่ใช่เกณฑ์แพทย์",
    }


def _pos(value, lo, hi):
    if value < lo:
        return "below"
    if value > hi:
        return "above"
    return "in"


def growth_entry(month, weight_kg, height_cm):
    if weight_kg <= 0 or height_cm <= 0:
        raise ValueError("weight/height must be > 0")
    band = example_band(month)
    w_pos = _pos(weight_kg, band["weight_lo_kg"], band["weight_hi_kg"])
    h_pos = _pos(height_cm, band["height_lo_cm"], band["height_hi_cm"])
    label = {
        "below": "ต่ำกว่าแถบตัวอย่างในแอป",
        "in": "อยู่ในแถบตัวอย่างในแอป",
        "above": "สูงกว่าแถบตัวอย่างในแอป",
    }
    return {
        "month": month, "weight_kg": weight_kg, "height_cm": height_cm,
        "weight_pos": w_pos, "height_pos": h_pos,
        "weight_label_th": label[w_pos], "height_label_th": label[h_pos],
        "band": band, "disclaimer_th": SAFETY_DISCLAIMER_TH,
    }


def first_info(kind):
    if kind not in FIRSTS:
        raise ValueError("unknown first")
    f = FIRSTS[kind]
    return {"id": f["id"], "kind": kind, "name_th": f["name_th"],
            "example_month": f["example_month"], "range_lo": f["range"][0], "range_hi": f["range"][1],
            "disclaimer_th": "ช่วงเดือนเป็นตัวอย่างในแอป ไม่ใช่กำหนดแพทย์ และไม่ใช่เส้นตาย"}


def log_first(kind, month, note_th=""):
    info = first_info(kind)
    lo, hi = info["range_lo"], info["range_hi"]
    if month < lo or month > hi:
        flag = "outside_example"
        tip = "อยู่นอกช่วงตัวอย่างในแอป — ไม่ได้แปลว่าช้าหรือเร็ว ถ้ากังวลให้ปรึกษาแพทย์"
    else:
        flag = "in_example"
        tip = "อยู่ในช่วงตัวอย่างในแอป ซึ่งไม่ใช่เกณฑ์แพทย์"
    return {**info, "logged_month": month, "flag": flag, "tip_th": tip, "note_th": note_th}


def timeline(entries):
    if not entries:
        raise ValueError("no moments")
    ordered = sorted(entries, key=lambda e: (e["logged_month"], e["kind"]))
    return {"count": len(ordered), "entries": ordered, "disclaimer_th": SAFETY_DISCLAIMER_TH}


def captions(kind, name_th, n=2):
    if kind not in CAPTION_BANK:
        raise ValueError("unknown first")
    bank = CAPTION_BANK[kind]
    start = (sum(ord(ch) for ch in name_th) + 1) % len(bank)
    picked = [bank[(start + i) % len(bank)] for i in range(min(n, len(bank)))]
    while len(picked) < n:
        picked.append(bank[len(picked) % len(bank)])
    return [{"n": i + 1, "kind": kind, "for_name_th": name_th, "text_th": t} for i, t in enumerate(picked[:n])]


def milestone_card(child_name_th, month, kind, photo_id):
    info = first_info(kind)
    cap = captions(kind, child_name_th, 1)[0]["text_th"]
    title = f"เดือนที่ {month} · {info['name_th']}"
    return {
        "photo_id": photo_id, "name_th": child_name_th, "month": month, "kind": kind,
        "title_th": title, "caption_th": cap, "layout": "month_card",
        "sizes": ["1080x1350", "1080x1080", "1080x1920"],
        "watermark": WATERMARK, "disclaimer_th": SAFETY_DISCLAIMER_TH,
        "headline_th": f"{child_name_th} · {title}",
    }


def month_ideas(month):
    if month not in range(0, 37):
        raise ValueError("month must be 0..36")
    ideas = PLAY_IDEAS.get(month, ["อ่านนิทานสั้น ๆ ด้วยกัน", "เล่นจ๊ะเอ๋และร้องเพลง"])
    return {"month": month, "ideas_th": list(ideas),
            "disclaimer_th": "ไอเดียเล่นเป็นตัวอย่างในแอป ไม่ใช่แบบฝึกแพทย์"}


def collage(title_th, slots):
    if not slots:
        raise ValueError("no photos")
    n = len(slots)
    cols = 2 if n <= 4 else 3
    rows = (n + cols - 1) // cols
    return {"title_th": title_th, "slots": slots, "count": n, "cols": cols, "rows": rows,
            "disclaimer_th": CONSENT_DISCLAIMER_TH, "layout": "monthly_grid"}


def print_sheet(name_th, month, caption_th, layout="portrait_a4"):
    layouts = {
        "portrait_a4": {"label_th": "A4 การ์ดเดี่ยว", "sizes": ["A4", "1080x1350"]},
        "book_20": {"label_th": "หน้าอัลบั้ม 20×20 ซม.", "sizes": ["20x20cm"]},
        "collage_a4": {"label_th": "A4 คอลลาจรายเดือน", "sizes": ["A4"]},
    }
    if layout not in layouts:
        raise ValueError("unknown layout")
    L = layouts[layout]
    return {"name_th": name_th, "month": month, "caption_th": caption_th, "layout": layout,
            "label_th": L["label_th"], "sizes": L["sizes"], "bleed_mm": 3, "watermark": WATERMARK}


def share_card(name_th, month, kind, caption_th):
    info = first_info(kind)
    return {
        "title_th": f"TinySteps — {name_th}",
        "headline_th": f"เดือนที่ {month} · {info['name_th']}",
        "hook_th": "การ์ดพัฒนาการลูกรายเดือนจากรูป",
        "caption_th": caption_th, "month": month, "kind": kind,
        "layout": "milestone_card", "sizes": ["1080x1350", "1080x1920", "1080x1080"],
        "watermark": WATERMARK, "cta_th": f"คอมเมนต์ STEPS รับแพ็กฟรี · {name_th}",
        "disclaimer_th": SAFETY_DISCLAIMER_TH,
    }


def quota(used_today, want, pro=False):
    if pro:
        return {"allowed": want, "left_after": None, "paywall": False}
    left = max(0, FREE_GENS_PER_DAY - used_today)
    allowed = min(want, left)
    return {"allowed": allowed, "left_after": left - allowed, "paywall": allowed < want}


def consent_guard(own_child, parent_confirmed, age_parent, all_guardians_ok=True):
    blocks = []
    if not parent_confirmed:
        blocks.append("ยังไม่ได้ยืนยันว่าเป็นผู้ปกครอง")
    if not own_child:
        blocks.append("ใช้ได้เฉพาะรูปของลูกตนเอง")
    if age_parent is None:
        blocks.append("ยังไม่ได้ยืนยันอายุผู้ปกครอง")
    elif age_parent < 18:
        blocks.append("ผู้ใช้ต้องเป็นผู้ปกครองอายุ 18 ปีขึ้นไป")
    if not all_guardians_ok:
        blocks.append("ต้องได้รับความยินยอมจากผู้ปกครองที่เกี่ยวข้องก่อนแชร์")
    ok = not blocks
    return {"ok": ok, "level": "ok" if ok else "block", "blocks_th": blocks,
            "message_th": "ผ่านการตรวจยินยอม พร้อมทำบัตรได้" if ok else "ยังทำบัตรไม่ได้: " + " · ".join(blocks),
            "disclaimer_th": CONSENT_DISCLAIMER_TH}


def safety_guard(consent_ok=True):
    if not consent_ok:
        return {"level": "stop", "message_th": "ยังทำบัตรไม่ได้ " + SAFETY_DISCLAIMER_TH}
    return {"level": "ok", "message_th": SAFETY_DISCLAIMER_TH}
