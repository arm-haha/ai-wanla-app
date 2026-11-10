"""PosterPop deterministic logic (no AI calls). Auto Thai poster layout — not a print shop, no real brand logos."""
import math as _math

TEMPLATES = {
    "sale": {
        "id": "t01", "name_th": "โปรลดราคา", "name_en": "Sale",
        "mood_th": "ตัวหนา ชัด ดึงสายตา", "zones": ["badge", "title", "offer", "details", "cta", "qr"],
        "default_palette": ["#4A2C2A", "#F8F1E3", "#E8772E", "#FFFFFF"],
    },
    "event": {
        "id": "t02", "name_th": "งานอีเวนต์", "name_en": "Event",
        "mood_th": "วันที่และสถานที่เด่น อ่านง่าย", "zones": ["kicker", "title", "datetime", "place", "details", "cta", "qr"],
        "default_palette": ["#1E3A5F", "#F4EFE6", "#C4A574", "#FFFFFF"],
    },
    "menu": {
        "id": "t03", "name_th": "เมนูร้าน", "name_en": "Menu",
        "mood_th": "รายการและราคาเป็นคอลัมน์อ่านชัด", "zones": ["logo", "title", "grid", "note", "qr"],
        "default_palette": ["#2C1810", "#FFF8EE", "#8B5A2B", "#1A1A1A"],
    },
}
TEMPLATE_IDS = list(TEMPLATES)
SIZES = {
    "ig_portrait": {"id": "s01", "w": 1080, "h": 1350, "label_th": "IG โพสต์แนวตั้ง", "kind": "social"},
    "ig_square": {"id": "s02", "w": 1080, "h": 1080, "label_th": "IG สี่เหลี่ยม", "kind": "social"},
    "ig_story": {"id": "s03", "w": 1080, "h": 1920, "label_th": "IG สตอรี่ / Reels", "kind": "social"},
    "fb_post": {"id": "s04", "w": 1080, "h": 1350, "label_th": "Facebook โพสต์", "kind": "social"},
    "a4": {"id": "s05", "w": 2480, "h": 3508, "label_th": "พิมพ์ A4 300dpi", "kind": "print"},
    "a3": {"id": "s06", "w": 3508, "h": 4961, "label_th": "พิมพ์ A3 300dpi", "kind": "print"},
}
SIZE_IDS = list(SIZES)
FONTS = {"heading": "Kanit", "body": "Sarabun"}
FREE_GENS_PER_DAY = 3
WATERMARK = "Made with PosterPop · check rights to photos and text"
SAFETY_DISCLAIMER_TH = "PosterPop ช่วยจัดเลย์เอาต์เท่านั้น ไม่ใช่โรงพิมพ์และไม่ใช่โลโก้แบรนด์สำเร็จ ผู้ใช้ต้องมีสิทธิ์ในข้อความ รูป และเครื่องหมายการค้าที่ใส่ และควรตรวจคำและราคาอีกครั้งก่อนโพสต์หรือพิมพ์"

def _hex_rgb(h):
    h = h.lstrip("#")
    if len(h) != 6:
        raise ValueError("color must be #RRGGBB")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def rel_luminance(rgb):
    def f(c):
        c = c / 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = rgb
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def contrast_ratio(fg_hex, bg_hex):
    L1, L2 = rel_luminance(_hex_rgb(fg_hex)), rel_luminance(_hex_rgb(bg_hex))
    lighter, darker = max(L1, L2), min(L1, L2)
    return round((lighter + 0.05) / (darker + 0.05), 2)


def contrast_check(fg_hex, bg_hex, kind="body"):
    ratio = contrast_ratio(fg_hex, bg_hex)
    need = 3.0 if kind == "large" else 4.5
    ok = ratio >= need
    return {
        "fg": fg_hex, "bg": bg_hex, "kind": kind, "ratio": ratio, "need": need, "ok": ok,
        "level_th": "ผ่าน AA" if ok else "ไม่ผ่าน AA",
        "tip_th": "ตัวอักษรอ่านชัด" if ok else "ปรับสีให้อ่านชัดขึ้น อย่างน้อยคอนทราสต์ " + str(need),
    }


def title_size(title, canvas_w):
    n = len(title)
    if n <= 12:
        size = 96
    elif n <= 20:
        size = 72
    elif n <= 32:
        size = 56
    else:
        size = 44
    # scale slightly for smaller canvases (square/story still 1080 wide)
    if canvas_w < 1080:
        size = int(size * canvas_w / 1080)
    return size


def template_info(template_id):
    if template_id not in TEMPLATES:
        raise ValueError("unknown template")
    t = TEMPLATES[template_id]
    return {"id": t["id"], "template": template_id, "name_th": t["name_th"], "name_en": t["name_en"],
            "mood_th": t["mood_th"], "zones": list(t["zones"]), "default_palette": list(t["default_palette"])}


def size_info(size_id):
    if size_id not in SIZES:
        raise ValueError("unknown size")
    s = SIZES[size_id]
    return {"id": s["id"], "size_id": size_id, "w": s["w"], "h": s["h"], "label_th": s["label_th"], "kind": s["kind"]}


def brand_kit(name_th, colors, heading="Kanit", body="Sarabun"):
    if len(colors) < 2:
        raise ValueError("brand needs at least 2 colors")
    for c in colors:
        _hex_rgb(c)
    check = contrast_check(colors[0], colors[1], "large")
    return {
        "name_th": name_th, "colors": list(colors), "heading_font": heading, "body_font": body,
        "contrast": check, "tip_th": "ใช้สีหลักกับสีพื้นสำหรับหัวข้อ " + check["level_th"],
    }


def qr_block(url, position="footer_right"):
    if not url or not isinstance(url, str):
        raise ValueError("url required")
    positions = {"footer_right", "footer_left", "footer_center"}
    if position not in positions:
        raise ValueError("unknown qr position")
    return {"url": url, "position": position, "size_px": 220, "label_th": "สแกนเพื่อดูเพิ่ม", "kind": "qr"}


def menu_grid(items):
    if not items:
        raise ValueError("no menu items")
    if any(i["price_thb"] < 0 for i in items):
        raise ValueError("price must be >= 0")
    rows = [{"name_th": i["name_th"], "price_thb": i["price_thb"],
             "price_label_th": f"฿{i['price_thb']}"} for i in items]
    return {"rows": rows, "count": len(rows), "cols": 1 if len(rows) <= 6 else 2}


def auto_layout(template_id, size_id, title, subtitle, details, date_th, place_th, cta_th, brand, qr=None):
    if template_id not in TEMPLATES:
        raise ValueError("unknown template")
    info = size_info(size_id)
    t = template_info(template_id)
    colors = list(brand["colors"])
    fg, bg = colors[0], colors[1]
    title_chk = contrast_check(fg, bg, "large")
    body_chk = contrast_check(fg, bg, "body")
    ts = title_size(title, info["w"])
    zones = []
    y = 0.08
    for z in t["zones"]:
        h = {"title": 0.18, "offer": 0.14, "grid": 0.40}.get(z, 0.10)
        zones.append({"id": z, "y": round(y, 2), "h": h})
        y += h
    return {
        "template": template_id, "size_id": size_id, "w": info["w"], "h": info["h"],
        "title_th": title, "subtitle_th": subtitle, "details_th": details,
        "date_th": date_th, "place_th": place_th, "cta_th": cta_th,
        "title_px": ts, "heading_font": brand["heading_font"], "body_font": brand["body_font"],
        "colors": colors, "zones": zones, "qr": qr,
        "title_contrast": title_chk, "body_contrast": body_chk,
        "headline_th": title,
        "ok_contrast": title_chk["ok"],
        "disclaimer_th": SAFETY_DISCLAIMER_TH,
    }


def share_card(name_th, title, template_id, size_id):
    return {
        "title_th": f"PosterPop — {name_th}",
        "headline_th": title,
        "hook_th": "พิมพ์รายละเอียดงาน ได้โปสเตอร์สวยทันที",
        "template": template_id, "size_id": size_id,
        "layout": "poster_preview", "sizes": ["1080x1350", "1080x1920", "1080x1080"],
        "watermark": WATERMARK,
        "cta_th": f"คอมเมนต์ POSTER รับแพ็กฟรี · {title}",
    }


def quota(used_today, want, pro=False):
    if pro:
        return {"allowed": want, "left_after": None, "paywall": False}
    left = max(0, FREE_GENS_PER_DAY - used_today)
    allowed = min(want, left)
    return {"allowed": allowed, "left_after": left - allowed, "paywall": allowed < want}


def safety_guard(rights_ok=True):
    if not rights_ok:
        return {"level": "stop", "message_th": "ยังส่งออกไม่ได้ จนกว่าจะยืนยันสิทธิ์ในข้อความและรูป " + SAFETY_DISCLAIMER_TH}
    return {"level": "ok", "message_th": SAFETY_DISCLAIMER_TH}


def pipeline_steps(template_id, has_qr=True, contrast_ok=True):
    if template_id not in TEMPLATES:
        raise ValueError("unknown template")
    s = ["brief", "template_" + template_id, "brand_kit", "auto_layout"]
    if not contrast_ok:
        s.append("contrast_fix")
    if has_qr:
        s.append("qr")
    s += ["export"]
    return s
