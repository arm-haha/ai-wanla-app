"""ReelForge reference engine (pure, deterministic).
Mirror in lib/parseIdea.ts, lib/blueprint.ts, lib/hooks.ts, lib/captions.ts, lib/overlays.ts, lib/film.ts.
"""
from __future__ import annotations
import re
from typing import Any

# ---------- style templates (fixed beat skeletons) ----------
# Each style maps to a list of beats: (beat_id, role, duration_weight, overlay_template_key)
# Durations are allocated proportionally to duration_target, then snapped so sum == target.

STYLES = {
    "soft_sell_before_after": {
        "id": "soft_sell_before_after",
        "label_th": "ก่อน/หลัง · Soft sell",
        "emoji": "✨",
        "bgm_mood": "warm_upbeat",
        "bgm_mood_th": "อบอุ่น มีจังหวะเบา",
        "beats": [
            ("hook", "hook", 3, "hook"),
            ("problem", "problem", 6, "problem"),
            ("reveal", "product_reveal", 8, "reveal"),
            ("howto", "howto", 8, "howto"),
            ("cta", "cta", 5, "cta"),
        ],
    },
    "teach_3_steps": {
        "id": "teach_3_steps",
        "label_th": "สอน 3 ขั้น",
        "emoji": "📚",
        "bgm_mood": "focus_soft",
        "bgm_mood_th": "โฟกัส นุ่ม",
        "beats": [
            ("hook", "hook", 3, "hook"),
            ("step1", "step", 7, "step1"),
            ("step2", "step", 8, "step2"),
            ("step3", "step", 7, "step3"),
            ("cta", "cta", 5, "cta"),
        ],
    },
    "storytime": {
        "id": "storytime",
        "label_th": "Storytime",
        "emoji": "📖",
        "bgm_mood": "story_soft",
        "bgm_mood_th": "เล่าเรื่อง นุ่มลึก",
        "beats": [
            ("hook", "hook", 4, "hook"),
            ("setup", "setup", 6, "setup"),
            ("twist", "twist", 10, "twist"),
            ("lesson", "lesson", 6, "lesson"),
            ("cta", "cta", 4, "cta"),
        ],
    },
    "unboxing": {
        "id": "unboxing",
        "label_th": "Unboxing",
        "emoji": "📦",
        "bgm_mood": "curious_pop",
        "bgm_mood_th": "อยากรู้ มีป๊อป",
        "beats": [
            ("hook", "hook", 3, "hook"),
            ("box", "box", 5, "box"),
            ("reveal", "product_reveal", 10, "reveal"),
            ("details", "details", 7, "details"),
            ("cta", "cta", 5, "cta"),
        ],
    },
    "soft_sell": {
        "id": "soft_sell",
        "label_th": "Soft sell",
        "emoji": "🍪",
        "bgm_mood": "cozy_sell",
        "bgm_mood_th": "อบอุ่น ชวนซื้อ",
        "beats": [
            ("hook", "hook", 3, "hook"),
            ("product", "product_reveal", 10, "reveal"),
            ("benefit", "benefit", 7, "benefit"),
            ("proof", "proof", 5, "proof"),
            ("cta", "cta", 5, "cta"),
        ],
    },
}

STYLE_IDS = list(STYLES.keys())

# ---------- category / keyword detection ----------
CATEGORY_RULES = [
    # (keywords_any, category, label_th, emoji, cta_keyword_default)
    (["คุกกี้", "cookie", "ขนม", "เค้ก", "บราวนี่", "มาการอง", "ขนมปัง", "เบเกอรี่", "butter"], "snacks", "ขนม/เบเกอรี่", "🍪", "คุกกี้"),
    (["สกินแคร์", "ครีม", "เซรั่ม", "lipstick", "ลิป", "เครื่องสำอาง", "beauty", "สกิน"], "beauty", "ความงาม", "💄", "สวย"),
    (["อ่านหนังสือ", "ติว", "สอบ", "เรียน", "study", "notebook", "สรุป"], "study", "เรียน/ติว", "📚", "ติว"),
    (["เสื้อ", "กางเกง", "แฟชั่น", "รองเท้า", "กระเป๋า", "ootd"], "fashion", "แฟชั่น", "👗", "ใส่"),
    (["กาแฟ", "ชา", "เครื่องดื่ม", "cafe", "คาเฟ่", "ชานม"], "drink", "เครื่องดื่ม", "☕", "กาแฟ"),
    (["ฟิตเนส", "ออกกำลัง", "โยคะ", "วิ่ง", "workout"], "fitness", "ฟิตเนส", "💪", "ฟิต"),
    (["มือถือ", "gadget", "หูฟัง", "โน้ตบุ๊ก", "tech"], "tech", "แกดเจ็ต", "📱", "แกดเจ็ต"),
    (["ดอกไม้", "ของขวัญ", "gift", "ช่อ"], "gift", "ของขวัญ", "🎁", "ของขวัญ"),
]

CHANNEL_HINTS = [
    (["line", "ไลน์"], "LINE"),
    (["ig", "instagram", "ไอจี"], "IG"),
    (["tiktok", "ติ๊กต็อก", "ติ๊กต๊อก"], "TikTok"),
    (["shopee", "ช้อปปี้"], "Shopee"),
    (["lazada", "ลาซาด้า"], "Lazada"),
    (["facebook", "เฟส", "fb"], "Facebook"),
]

PRICE_RE = [
    re.compile(r"ชิ้นละ\s*(\d+(?:\.\d+)?)\s*บาท"),
    re.compile(r"ขวดละ\s*(\d+(?:\.\d+)?)\s*บาท"),
    re.compile(r"กล่องละ\s*(\d+(?:\.\d+)?)\s*บาท"),
    re.compile(r"ราคา\s*(\d+(?:\.\d+)?)\s*บาท"),
    re.compile(r"(\d+(?:\.\d+)?)\s*บาท/?ชิ้น"),
    re.compile(r"฿\s*(\d+(?:\.\d+)?)"),
]
SET_RE = [
    re.compile(r"เซ[็ต]{1,2}\s*(\d+)\s*ชิ้น\s*(\d+(?:\.\d+)?)"),
    re.compile(r"(\d+)\s*ชิ้น\s*(\d+(?:\.\d+)?)\s*บาท"),
]
AREA_RE = re.compile(r"(ทั้ง)?(กรุงเทพ|กทม\.?|เชียงใหม่|ขอนแก่น|ภูเก็ต|พัทยา|นนทบุรี|ปทุมธานี|สมุทรปราการ)")

def _norm_ws(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").strip())


def parse_idea(raw: str) -> dict[str, Any]:
    """Normalize idea text and detect product/category/price/channel/area. Deterministic."""
    text = _norm_ws(raw)
    lower = text.lower()
    category = "other"
    label_th = "ทั่วไป"
    emoji = "🎬"
    cta_kw = "สนใจ"
    matched_kw = None
    for kws, cat, lab, em, cta in CATEGORY_RULES:
        for kw in kws:
            if kw.lower() in lower or kw in text:
                category, label_th, emoji, cta_kw, matched_kw = cat, lab, em, cta, kw
                break
        if matched_kw:
            break

    # product hint: prefer cookie/snack noun phrases, else first 24 chars
    product = None
    for pat in [
        r"(คุกกี้เนยสด|คุกกี้[^\s,]{0,12})",
        r"(ขนม[^\s,]{0,16})",
        r"(ครีม[^\s,]{0,12}|เซรั่ม[^\s,]{0,12})",
    ]:
        m = re.search(pat, text)
        if m:
            product = m.group(1)
            break
    if not product:
        product = text[:28] + ("…" if len(text) > 28 else "")

    price_unit = None
    for r in PRICE_RE:
        m = r.search(text)
        if m:
            price_unit = float(m.group(1))
            break

    price_set = None
    set_qty = None
    for r in SET_RE:
        m = r.search(text)
        if m:
            set_qty = int(m.group(1))
            price_set = float(m.group(2))
            break

    channel = None
    for kws, ch in CHANNEL_HINTS:
        if any(k in lower for k in kws):
            channel = ch
            break

    area = None
    m = AREA_RE.search(text)
    if m:
        area = m.group(2)
        if area.startswith("กทม"):
            area = "กรุงเทพ"

    # refine CTA keyword from product if snacks
    if category == "snacks" and product and "คุกกี้" in product:
        cta_kw = "คุกกี้"
    elif product and len(product) <= 10:
        # use short product as CTA if sensible
        pass

    return {
        "raw": raw,
        "normalized": text,
        "product": product,
        "category": category,
        "category_label_th": label_th,
        "emoji": emoji,
        "matched_keyword": matched_kw,
        "price_unit": price_unit,
        "price_set": price_set,
        "set_qty": set_qty,
        "channel": channel,
        "area": area,
        "cta_keyword": cta_kw,
        "lang": "th",
    }


def allocate_durations(weights: list[int], target: int) -> list[int]:
    """Allocate integer seconds so sum == target, proportional to weights. Deterministic."""
    assert target >= len(weights) >= 1
    total_w = sum(weights)
    raw = [w * target / total_w for w in weights]
    # floor then distribute remainder to largest fractional parts
    floors = [int(x) for x in raw]
    # ensure each at least 1
    floors = [max(1, f) for f in floors]
    # if sum > target due to min-1, shrink largest
    while sum(floors) > target:
        i = max(range(len(floors)), key=lambda i: floors[i])
        if floors[i] > 1:
            floors[i] -= 1
        else:
            break
    rem = target - sum(floors)
    fracs = sorted(range(len(raw)), key=lambda i: -(raw[i] - int(raw[i])), reverse=False)
    # sort by fractional part descending
    fracs = sorted(range(len(raw)), key=lambda i: (raw[i] - int(raw[i])), reverse=True)
    for i in fracs:
        if rem <= 0:
            break
        floors[i] += 1
        rem -= 1
    # final safety
    while sum(floors) < target:
        floors[0] += 1
    while sum(floors) > target:
        i = max(range(len(floors)), key=lambda j: floors[j])
        if floors[i] > 1:
            floors[i] -= 1
        else:
            break
    assert sum(floors) == target
    return floors


# ---------- hook templates per category/style ----------
def _default_hooks(idea: dict, style_id: str) -> list[dict]:
    """Generate 3 deterministic hook candidates from idea + style."""
    p = idea["product"] or "สินค้า"
    price = idea["price_unit"]
    price_s = f"ชิ้นละ {int(price) if price and price == int(price) else price} บาท" if price else ""
    ch = idea["channel"] or "แชท"
    cta = idea["cta_keyword"]

    if style_id == "soft_sell_before_after" or style_id == "soft_sell":
        a = f"โพสต์ข้อความอย่างเดียว vs คลิป 30 วิ — อันไหนขายได้มากกว่า?"
        b = f"แม่ค้าขนมบ้านหยุดโพสต์ข้อความ เปิดกล้อง 30 วิ แล้วยอดทักพุ่ง"
        c = f"{p}{(' ' + price_s) if price_s else ''} แต่คนไม่เห็น เพราะโพสต์นิ่งๆ"
    elif style_id == "teach_3_steps":
        a = f"ทำ {p} ให้คนทักใน 3 ขั้น (จับเวลา 30 วิ)"
        b = f"อย่าเปิดคลิปยาว — สอนขาย {p} แบบสั้นๆ 3 ช็อต"
        c = f"มือใหม่ก็ถ่ายได้: 3 ขั้นก่อนกดโพสต์ {p}"
    elif style_id == "storytime":
        a = f"เรื่องจริง: โพสต์ข้อความทั้งอาทิตย์ ไม่มีใครทัก แล้วฉันลองถ่ายคลิป…"
        b = f"จากแม่บ้าน → แม่ค้า {p} ใน 30 วิ"
        c = f"เคยขายไม่ออก จนเปลี่ยนวิธีเปิดคลิป"
    elif style_id == "unboxing":
        a = f"เปิดกล่อง {p} กับตา — ทำไมคนถึงสั่งซ้ำ?"
        b = f"Unbox {p} ใน 30 วิ แล้วตัดสินใจสั่งเลย"
        c = f"แกะดูใกล้ๆ: {p} {price_s}".strip()
    else:
        a = f"ไอเดียในหัวแต่ไม่รู้จะเปิดคลิปยังไง? เริ่มที่ {p}"
        b = f"30 วิ พอ: ฮุค → โชว์ → สั่ง {ch}"
        c = f"คอมเมนต์ 「{cta}」 ถ้าอยากได้สูตรเปิดคลิป"

    return [
        {"id": "hook_a", "text_th": a, "angle": "contrast"},
        {"id": "hook_b", "text_th": b, "angle": "transformation"},
        {"id": "hook_c", "text_th": c, "angle": "product_pain"},
    ]


# Keyword heuristics for ranking
CURIOSITY_KW = ["vs", "หรือ", "อันไหน", "ทำไม", "เปิดกล่อง", "เรื่องจริง", "…", "?", "ไหม", "มากกว่า"]
CLARITY_KW = ["30 วิ", "3 ขั้น", "ชิ้นละ", "บาท", "สั่ง", "ไลน์", "line", "คลิป", "ฮุค", "ก่อน", "หลัง"]
EMOTION_KW = ["พุ่ง", "ขายได้", "ไม่ออก", "หยุด", "แม่ค้า", "มือใหม่", "ซ้ำ", "ทัก", "ใจ", "จริง"]


def _score_axis(text: str, keywords: list[str], base: int = 40) -> int:
    t = text.lower()
    hits = sum(1 for k in keywords if k.lower() in t or k in text)
    # length bonus: 18–60 chars sweet spot
    n = len(text)
    length_bonus = 10 if 18 <= n <= 70 else (5 if 10 <= n <= 90 else 0)
    punct = 8 if ("?" in text or "!" in text or "—" in text or "vs" in t) else 0
    score = base + hits * 12 + length_bonus + punct
    return max(0, min(100, score))


def rank_hooks(hooks: list[dict]) -> list[dict]:
    """Score curiosity/clarity/emotion; sort by total desc, then id asc for stability.
    Returns hooks with scores + rank (1 = best).
    """
    scored = []
    for h in hooks:
        text = h["text_th"]
        curiosity = _score_axis(text, CURIOSITY_KW, 38)
        clarity = _score_axis(text, CLARITY_KW, 42)
        emotion = _score_axis(text, EMOTION_KW, 36)
        # contrast/vs hooks get curiosity bump
        if "vs" in text.lower() or "อันไหน" in text:
            curiosity = min(100, curiosity + 14)
        if "30 วิ" in text or "3 ขั้น" in text:
            clarity = min(100, clarity + 10)
        if any(w in text for w in ["พุ่ง", "ขายได้", "ไม่ออก", "แม่ค้า"]):
            emotion = min(100, emotion + 12)
        total = curiosity + clarity + emotion
        scored.append({
            **h,
            "scores": {
                "curiosity": curiosity,
                "clarity": clarity,
                "emotion": emotion,
                "total": total,
            },
        })
    scored.sort(key=lambda x: (-x["scores"]["total"], x["id"]))
    for i, h in enumerate(scored, 1):
        h["rank"] = i
        h["is_winner"] = i == 1
    return scored


def _shot_lines(idea: dict, style_id: str, role: str, hook_text: str) -> dict:
    """Deterministic VO + overlay + prompt card per role."""
    p = idea["product"] or "สินค้า"
    price = idea["price_unit"]
    price_s = f"ชิ้นละ {int(price)} บาท" if price and float(price) == int(price) else (f"ชิ้นละ {price} บาท" if price else "")
    set_s = ""
    if idea.get("set_qty") and idea.get("price_set"):
        ps = idea["price_set"]
        ps_s = int(ps) if float(ps) == int(ps) else ps
        set_s = f"เซ็ต {idea['set_qty']} ชิ้น {ps_s} บาท"
    ch = idea["channel"] or "แชท"
    area = idea["area"] or "ใกล้บ้าน"
    cta = idea["cta_keyword"]

    table = {
        "hook": {
            "overlay_th": hook_text if len(hook_text) <= 42 else hook_text[:40] + "…",
            "vo_th": hook_text,
            "prompt_th": "มองกล้อง · พูดฮุคช้าๆ ชัดๆ · ยิ้มนิด",
            "title_th": "ฮุค 0–3 วิ",
        },
        "problem": {
            "overlay_th": "ก่อน: โพสต์ข้อความอย่างเดียว",
            "vo_th": f"ก่อนหน้านี้ฉันโพสต์ข้อความกับรูปนิ่ง รอคนทักเอง — {p} ก็เงียบ",
            "prompt_th": "โชว์มือถือหน้าโพสต์ข้อความ · ส่ายหัวเบาๆ",
            "title_th": "ปัญหา",
        },
        "product_reveal": {
            "overlay_th": f"{p}" + (f" · {price_s}" if price_s else ""),
            "vo_th": f"นี่เลย {p}" + (f" {price_s}" if price_s else "") + (f" หรือ {set_s}" if set_s else "") + " อบใหม่ทุกวัน",
            "prompt_th": "ยกสินค้าเข้ากล้อง · หมุนช้าๆ ให้เห็นเนื้อ",
            "title_th": "โชว์สินค้า",
        },
        "howto": {
            "overlay_th": f"สั่ง {ch} · ส่ง{area}",
            "vo_th": f"อยากได้ทัก {ch} ได้เลย ส่งถึง{area}" + (f" — {set_s} ก็มี" if set_s else ""),
            "prompt_th": f"ชี้ไปที่ไอคอน {ch} หรือพิมพ์ตัวอย่างข้อความ",
            "title_th": "วิธีสั่ง",
        },
        "cta": {
            "overlay_th": f'คอมเมนต์ 「{cta}」 รับเมนู',
            "vo_th": f"คอมเมนต์คำว่า {cta} เดี๋ยวส่งรายละเอียดให้ — รีบก่อนหมดเตา",
            "prompt_th": "ชี้คอมเมนต์ · ยิ้ม · พูด CTA ชัด",
            "title_th": "CTA",
        },
        "step": {
            "overlay_th": f"ขั้นต่อไปกับ {p}",
            "vo_th": f"ทำตามขั้นนี้กับ {p}",
            "prompt_th": "ชี้ overlay · พูดสั้นๆ",
            "title_th": "ขั้น",
        },
        "step1": {
            "overlay_th": "ขั้น 1: เปิดด้วยฮุค",
            "vo_th": "ขั้นหนึ่ง เปิดด้วยประโยคที่คนอยากรู้ต่อ",
            "prompt_th": "พูดฮุค · มือถือตั้ง",
            "title_th": "ขั้น 1",
        },
        "step2": {
            "overlay_th": f"ขั้น 2: โชว์ {p}",
            "vo_th": f"ขั้นสอง โชว์ {p} ให้เห็นของจริง",
            "prompt_th": "ยกสินค้า · ใกล้เลนส์",
            "title_th": "ขั้น 2",
        },
        "step3": {
            "overlay_th": f"ขั้น 3: บอกทางสั่ง {ch}",
            "vo_th": f"ขั้นสาม บอกว่าสั่งยังไงทาง {ch}",
            "prompt_th": "ชี้ช่องทาง · พูดช้า",
            "title_th": "ขั้น 3",
        },
        "setup": {
            "overlay_th": "ตอนนั้นฉันโพสต์อย่างเดียว",
            "vo_th": "ตอนนั้นฉันคิดว่าพิมพ์ดีๆ ก็พอ",
            "prompt_th": "เล่าใกล้กล้อง · น้ำเสียงจริง",
            "title_th": "เริ่มเรื่อง",
        },
        "twist": {
            "overlay_th": "จนฉันลองเปิดกล้อง 30 วิ",
            "vo_th": f"จนวันหนึ่งลองถ่าย {p} สั้นๆ — คนทักรัว",
            "prompt_th": "เปลี่ยนมุม · ยิ้มกว้างขึ้น",
            "title_th": "พลิก",
        },
        "lesson": {
            "overlay_th": "บทเรียน: คนซื้อของที่เห็น",
            "vo_th": "คนอยากเห็นของจริง ไม่ใช่แค่ตัวอักษร",
            "prompt_th": "พูดสรุป · พยักหน้า",
            "title_th": "บทเรียน",
        },
        "box": {
            "overlay_th": "กล่องมาถึงแล้ว",
            "vo_th": "กล่องมาถึงแล้ว แกะด้วยกัน",
            "prompt_th": "ถือกล่องเขย่าเบาๆ",
            "title_th": "กล่อง",
        },
        "details": {
            "overlay_th": price_s or "รายละเอียดใกล้ๆ",
            "vo_th": f"เนื้อสัมผัส กลิ่น" + (f" และราคา {price_s}" if price_s else ""),
            "prompt_th": "ซูมรายละเอียด · พูดช้า",
            "title_th": "รายละเอียด",
        },
        "benefit": {
            "overlay_th": "อบใหม่ · ส่งถึงบ้าน",
            "vo_th": f"{p} อบใหม่ ส่งถึงบ้านผ่าน {ch}",
            "prompt_th": "ยิ้ม · โชว์ประโยชน์สั้นๆ",
            "title_th": "ประโยชน์",
        },
        "proof": {
            "overlay_th": "ลูกค้าสั่งซ้ำทุกอาทิตย์",
            "vo_th": "มีคนสั่งซ้ำทุกอาทิตย์ เพราะอร่อยจริง",
            "prompt_th": "โชว์รีวิว/แชท (เบลอชื่อ)",
            "title_th": "หลักฐาน",
        },
    }
    # map role aliases
    key = role
    if role == "product_reveal":
        key = "product_reveal"
    return table.get(key) or table.get(role) or {
        "overlay_th": p,
        "vo_th": p,
        "prompt_th": "มองกล้อง พูดชัด",
        "title_th": role,
    }


def build_blueprint(idea: dict | str, style: str = "soft_sell_before_after", duration_target: int = 30, selected_hook_id: str | None = None) -> dict:
    """Build structured Reel blueprint from idea + style. Deterministic templates."""
    if isinstance(idea, str):
        idea = parse_idea(idea)
    if style not in STYLES:
        style = "soft_sell_before_after"
    st = STYLES[style]
    hooks_raw = _default_hooks(idea, style)
    ranked = rank_hooks(hooks_raw)
    winner = ranked[0]
    if selected_hook_id:
        for h in ranked:
            if h["id"] == selected_hook_id:
                winner = h
                break

    weights = [b[2] for b in st["beats"]]
    durs = allocate_durations(weights, duration_target)
    shots = []
    t0 = 0
    for i, ((beat_id, role, _w, overlay_key), dur) in enumerate(zip(st["beats"], durs), 1):
        lines = _shot_lines(idea, style, overlay_key if overlay_key in ("step1", "step2", "step3") else role, winner["text_th"])
        # for step roles use overlay_key
        if overlay_key in ("step1", "step2", "step3"):
            lines = _shot_lines(idea, style, overlay_key, winner["text_th"])
        shot = {
            "n": i,
            "shot_id": f"shot_{i:02d}_{beat_id}",
            "beat_id": beat_id,
            "role": role,
            "start_s": t0,
            "duration_s": dur,
            "end_s": t0 + dur,
            "title_th": lines["title_th"],
            "overlay_th": lines["overlay_th"],
            "vo_th": lines["vo_th"],
            "prompt_th": lines["prompt_th"],
            "camera_th": "แนวตั้ง 9:16 · มือถือระดับอก",
        }
        shots.append(shot)
        t0 += dur

    assert shots[-1]["end_s"] == duration_target
    assert sum(s["duration_s"] for s in shots) == duration_target

    return {
        "blueprint_id": f"bp_{style}_{duration_target}_{idea['category']}",
        "idea": idea,
        "style": style,
        "style_label_th": st["label_th"],
        "style_emoji": st["emoji"],
        "duration_target_s": duration_target,
        "duration_total_s": duration_target,
        "bgm_mood": st["bgm_mood"],
        "bgm_mood_th": st["bgm_mood_th"],
        "hook": {
            "id": winner["id"],
            "text_th": winner["text_th"],
            "angle": winner["angle"],
            "scores": winner["scores"],
            "rank": winner["rank"],
        },
        "hooks_ranked": ranked,
        "shots": shots,
        "shot_count": len(shots),
        "cta_keyword": idea["cta_keyword"],
        "created_from": "deterministic_v1",
    }


HASHTAG_POOLS = {
    "snacks": ["#คุกกี้", "#ขนมบ้าน", "#ของกินอร่อย", "#แม่ค้าออนไลน์", "#เบเกอรี่", "#รีลขายของ", "#สายกิน", "#อบเอง"],
    "beauty": ["#ความงาม", "#สกินแคร์", "#รีวิวเครื่องสำอาง", "#แม่ค้าออนไลน์", "#รีลขายของ", "#สวยง่าย", "#เมคอัพ"],
    "study": ["#ติวสอบ", "#สรุปสั้น", "#นักเรียนไทย", "#รีลเรียน", "#เทคนิคเรียน", "#สอบเข้า"],
    "fashion": ["#แฟชั่น", "#OOTD", "#สไตล์วันนี้", "#รีลขายของ", "#เสื้อผ้า"],
    "drink": ["#กาแฟ", "#ชาไข่มุก", "#คาเฟ่", "#รีลขายของ", "#เครื่องดื่ม"],
    "fitness": ["#ฟิตเนส", "#ออกกำลังกาย", "#สุขภาพ", "#เวิร์คเอาท์"],
    "tech": ["#แกดเจ็ต", "#รีวิวมือถือ", "#เทค"],
    "gift": ["#ของขวัญ", "#ดอกไม้", "#เซอร์ไพรส์"],
    "other": ["#รีลไทย", "#คอนเทนต์ครีเอเตอร์", "#แม่ค้าออนไลน์", "#AIวันละแอป", "#รีลขายของ"],
}

COMMON_TAGS = ["#รีลไทย", "#คอนเทนต์มือใหม่", "#AIวันละแอป", "#ReelForge", "#ถ่ายรีล"]


def build_caption_pack(blueprint: dict) -> dict:
    """Thai captions + hashtags + comment CTA from blueprint. Deterministic pools."""
    idea = blueprint["idea"]
    hook = blueprint["hook"]["text_th"]
    p = idea["product"] or "สินค้า"
    cta = blueprint["cta_keyword"]
    ch = idea["channel"] or "แชท"
    price = idea["price_unit"]
    price_bit = f" ชิ้นละ {int(price)} บาท" if price and float(price) == int(price) else ""
    set_bit = ""
    if idea.get("set_qty") and idea.get("price_set"):
        ps = idea["price_set"]
        set_bit = f" เซ็ต {idea['set_qty']} ชิ้น {int(ps) if float(ps)==int(ps) else ps} บาท"

    short = f"{hook} {p}{price_bit} สั่ง {ch} ได้เลย คอมเมนต์ 「{cta}」"
    # keep short reasonably short
    if len(short) > 120:
        short = f"{p}{price_bit} — เปิดคลิป 30 วิ สั่ง {ch} คอมเมนต์ 「{cta}」"

    long = (
        f"{hook}\n\n"
        f"วันนี้ขอเปิดกล้องขาย{p} สั้นๆ 30 วิ"
        f"{price_bit}{set_bit}\n"
        f"ส่ง{idea['area'] or 'ใกล้บ้าน'} ทาง {ch}\n\n"
        f"ถ้าอยากได้รายละเอียด คอมเมนต์คำว่า 「{cta}」 ไว้เลย "
        f"เดี๋ยวส่งเมนู/ลิงก์ให้ในคอมเมนต์ 🍪\n\n"
        f"(ตัวอย่างจากช่อง AI วันละแอป · ReelForge)"
    )

    pool = list(HASHTAG_POOLS.get(idea["category"], HASHTAG_POOLS["other"]))
    tags = []
    for t in pool + COMMON_TAGS:
        if t not in tags:
            tags.append(t)
        if len(tags) >= 12:
            break
    # ensure at least 8
    while len(tags) < 8:
        tags.append(f"#รีล{len(tags)}")

    return {
        "caption_short_th": short,
        "caption_long_th": long,
        "hashtags": tags[:12],
        "comment_cta_keyword": cta,
        "comment_cta_line_th": f'คอมเมนต์ 「{cta}」 รับรายละเอียด',
        "lang": "th",
        "char_count_short": len(short),
        "char_count_long": len(long),
    }


def build_overlays(blueprint: dict) -> dict:
    """Per-shot overlay lines + 3 cover variants 1080×1920."""
    idea = blueprint["idea"]
    p = idea["product"] or "สินค้า"
    cta = blueprint["cta_keyword"]
    price = idea["price_unit"]
    price_s = f"ชิ้นละ {int(price)}฿" if price and float(price) == int(price) else ""
    hook = blueprint["hook"]["text_th"]

    per_shot = []
    for s in blueprint["shots"]:
        per_shot.append({
            "shot_id": s["shot_id"],
            "n": s["n"],
            "overlay_th": s["overlay_th"],
            "font_hint": "bold_sans",
            "safe_zone": "center_upper",
            "max_chars": 42,
        })

    covers = [
        {
            "id": "cover_a",
            "variant": "contrast",
            "size": [1080, 1920],
            "title_th": "ข้อความ vs คลิป 30 วิ",
            "subtitle_th": f"{p} ขายได้ต่างกันยังไง",
            "badge_th": "ก่อน/หลัง",
            "bg": "#0F0A1A",
            "accent": "#E11D48",
        },
        {
            "id": "cover_b",
            "variant": "product",
            "size": [1080, 1920],
            "title_th": p,
            "subtitle_th": (price_s + " · ส่งถึงบ้าน") if price_s else "อบใหม่ · ส่งถึงบ้าน",
            "badge_th": "Soft sell",
            "bg": "#0F0A1A",
            "accent": "#8B5CF6",
        },
        {
            "id": "cover_c",
            "variant": "cta",
            "size": [1080, 1920],
            "title_th": f"คอมเมนต์ 「{cta}」",
            "subtitle_th": "รับเมนู · พร้อมถ่ายตาม",
            "badge_th": "CTA",
            "bg": "#0F0A1A",
            "accent": "#FBBF24",
        },
    ]

    return {
        "per_shot": per_shot,
        "covers": covers,
        "hook_line_th": hook if len(hook) <= 48 else hook[:46] + "…",
        "export_format": "png",
        "export_size": [1080, 1920],
    }


# ---------- film mode timing ----------
def film_progress(shots: list[dict], elapsed_s: float) -> dict:
    """Given elapsed seconds into film mode, return current shot + progress. Deterministic."""
    total = sum(s["duration_s"] for s in shots)
    if elapsed_s < 0:
        elapsed_s = 0.0
    if elapsed_s >= total:
        last = shots[-1]
        return {
            "total_s": total,
            "elapsed_s": total,
            "remaining_s": 0,
            "done": True,
            "shot_index": len(shots) - 1,
            "shot": last,
            "shot_elapsed_s": last["duration_s"],
            "shot_remaining_s": 0,
            "shot_progress": 1.0,
            "overall_progress": 1.0,
        }
    acc = 0.0
    for i, s in enumerate(shots):
        if elapsed_s < acc + s["duration_s"]:
            se = elapsed_s - acc
            return {
                "total_s": total,
                "elapsed_s": elapsed_s,
                "remaining_s": round(total - elapsed_s, 3),
                "done": False,
                "shot_index": i,
                "shot": s,
                "shot_elapsed_s": round(se, 3),
                "shot_remaining_s": round(s["duration_s"] - se, 3),
                "shot_progress": round(se / s["duration_s"], 4) if s["duration_s"] else 1.0,
                "overall_progress": round(elapsed_s / total, 4) if total else 1.0,
            }
        acc += s["duration_s"]
    # fallback
    return film_progress(shots, total)


def swap_hook(blueprint: dict, hook_id: str) -> dict:
    """One-tap swap: rebuild blueprint with selected hook as winner text on shot 1."""
    return build_blueprint(blueprint["idea"], blueprint["style"], blueprint["duration_target_s"], selected_hook_id=hook_id)


def suggest_trend_angles(idea: dict) -> list[dict]:
    """Thai-friendly trend angles — deterministic list from category."""
    cat = idea["category"]
    p = idea["product"] or "สินค้า"
    base = [
        {"id": "angle_before_after", "title_th": "ก่อน/หลังชัดๆ", "desc_th": f"โชว์โพสต์ข้อความ vs คลิป {p}", "style": "soft_sell_before_after"},
        {"id": "angle_3steps", "title_th": "สอน 3 ขั้น", "desc_th": "มือใหม่ทำตามได้ในคลิปเดียว", "style": "teach_3_steps"},
        {"id": "angle_story", "title_th": "Storytime สั้น", "desc_th": "เล่าว่าทำไมถึงเริ่มขาย", "style": "storytime"},
        {"id": "angle_unbox", "title_th": "Unboxing / แกะดู", "desc_th": f"เปิดใกล้ๆ ให้เห็น {p}", "style": "unboxing"},
        {"id": "angle_soft", "title_th": "Soft sell อบอุ่น", "desc_th": "ไม่แข็งขาย โชว์ของ + CTA", "style": "soft_sell"},
    ]
    # reorder: put matching category preference first
    if cat == "snacks":
        order = ["angle_before_after", "angle_soft", "angle_unbox", "angle_3steps", "angle_story"]
    elif cat == "study":
        order = ["angle_3steps", "angle_story", "angle_before_after", "angle_soft", "angle_unbox"]
    elif cat == "beauty":
        order = ["angle_unbox", "angle_before_after", "angle_soft", "angle_3steps", "angle_story"]
    else:
        order = [a["id"] for a in base]
    by = {a["id"]: a for a in base}
    return [by[i] for i in order if i in by]


def film_rewind(shots: list[dict], shot_index: int) -> dict:
    """Rewind to start of given shot index."""
    idx = max(0, min(shot_index, len(shots) - 1))
    start = sum(s["duration_s"] for s in shots[:idx])
    return film_progress(shots, float(start))
