"""ColorMe — deterministic reference logic (port to TypeScript; tests.py is the contract).
A "picture" is a list of rows of (r, g, b) tuples. In the real app the photo is first cleaned by the
image model (background simplified, subject kept) and downscaled on the device to a small working grid;
everything below — palette, regions, numbering, simplification, dots, scoring — is plain code, never an LLM guess."""
import math
from collections import deque
from datetime import date as _date

# 13 crayon colours that every Thai stationery shop sells (key, Thai name, English name, rgb)
CRAYONS = [("red", "แดง", "Red", (230, 57, 70)), ("orange", "ส้ม", "Orange", (247, 140, 40)),
           ("yellow", "เหลือง", "Yellow", (255, 214, 10)), ("lime", "เขียวอ่อน", "Light green", (150, 210, 80)),
           ("green", "เขียว", "Green", (40, 150, 70)), ("sky", "ฟ้า", "Sky blue", (120, 190, 240)),
           ("blue", "น้ำเงิน", "Blue", (30, 80, 190)), ("purple", "ม่วง", "Purple", (140, 80, 190)),
           ("pink", "ชมพู", "Pink", (255, 140, 180)), ("brown", "น้ำตาล", "Brown", (140, 90, 50)),
           ("gray", "เทา", "Gray", (150, 150, 155)), ("black", "ดำ", "Black", (30, 30, 30)),
           ("white", "ขาว (เว้นไว้)", "White (leave blank)", (250, 250, 250))]
KEYS = [c[0] for c in CRAYONS]
CRAYON = {c[0]: c for c in CRAYONS}
# difficulty by age: how many colours, smallest region kept (cells of the working grid), max regions, line width, numbers?
LEVELS = {"tiny": {"ages": (3, 5), "name_th": "ตัวจิ๋ว 3–5 ขวบ", "max_colors": 4, "min_area": 24, "max_regions": 12, "line_px": 8, "numbers": False, "dots": 10},
          "kid": {"ages": (6, 8), "name_th": "ประถมต้น 6–8 ขวบ", "max_colors": 7, "min_area": 6, "max_regions": 30, "line_px": 5, "numbers": True, "dots": 20},
          "big": {"ages": (9, 12), "name_th": "ประถมปลาย 9–12 ปี", "max_colors": 8, "min_area": 2, "max_regions": 60, "line_px": 3, "numbers": True, "dots": 40},
          "calm": {"ages": (13, 120), "name_th": "ผู้ใหญ่ระบายคลายเครียด", "max_colors": 12, "min_area": 1, "max_regions": 200, "line_px": 2, "numbers": True, "dots": 80}}
MODES = ("lineart", "numbers")
THEMES = ["น้องหมาน้องแมวที่บ้าน", "อาหารจานโปรด", "ของเล่นชิ้นโปรด", "วิวหน้าบ้าน", "ผลไม้ในตู้เย็น", "รองเท้าของเรา", "ต้นไม้ใกล้บ้าน",
          "ท้องฟ้าวันนี้", "ขนมไทย", "รถคันโปรด", "ห้องนอนของเรา", "ที่เที่ยวปิดเทอม", "ตุ๊กตาตัวโปรด", "ของขวัญปีใหม่"]
STICKERS = {3: "ดินสอสีทอง", 7: "จานสีสายรุ้ง", 14: "มงกุฎศิลปิน", 30: "ถ้วยจิตรกรน้อย"}
A4_PX = (2480, 3508)  # 300 dpi
GUARD = {None: ("ok", "ใช้รูปที่เราถ่ายเองหรือได้รับอนุญาต ประมวลผลบนเครื่อง รูปต้นฉบับไม่ถูกอัปโหลด"),
         "nudity": ("stop", "รูปนี้ใช้ไม่ได้ เลือกรูปที่ทุกคนแต่งตัวเรียบร้อย"),
         "id_document": ("stop", "ดูเหมือนบัตรประชาชน/สลิป/เอกสาร มีข้อมูลส่วนตัว ไม่แปลงเป็นหน้าระบายสี"),
         "violent": ("stop", "เนื้อหาไม่เหมาะกับเด็ก เลือกรูปอื่นนะ"),
         "other_child_face": ("warn", "มีหน้าเด็กคนอื่นในรูป ใช้ในบ้านได้ แต่ก่อนแชร์ต้องได้รับอนุญาตจากผู้ปกครองของเขา (การ์ดแชร์จะซ่อนหน้าให้)"),
         "copyright_character": ("warn", "เจอตัวการ์ตูน/โลโก้ที่มีลิขสิทธิ์ ระบายเล่นในบ้านได้ ห้ามพิมพ์ขาย — แนะนำแปลงเป็นตัวละครทั่วไป"),
         "selling_pages": ("warn", "พิมพ์ขายได้เฉพาะหน้าที่มาจากรูปของเราเอง และไม่มีตัวการ์ตูนลิขสิทธิ์"),
         "screen_time": ("warn", "ระบายบนจอมา 30 นาทีแล้ว พักสายตา แล้วไประบายบนกระดาษกันต่อนะ"),
         "under_3": ("stop", "เด็กต่ำกว่า 3 ขวบยังไม่เหมาะ (สีเทียนชิ้นเล็ก) ให้ผู้ใหญ่เล่นด้วยใกล้ ๆ ในโหมดตัวจิ๋ว")}
REEL_SHOTS = [("hook", "ปิดเทอม ลูกเบื่อ ติดจอ? \"เอารูปน้องแมวมาระบายสีกัน\""), ("build", "ตัดเร่งตอนสร้างแอปด้วย AI จากแพ็กนี้"),
              ("magic", "เลือกรูปในมือถือ → เส้นวาดค่อย ๆ ขึ้น กลายเป็นหน้าระบายสี"), ("numbers", "สลับโหมดระบายตามเลข + พิมพ์ A4"),
              ("reveal", "ลูกระบายเสร็จ สแกน → ดาว 3 ดวง + ภาพก่อน/หลังคู่กัน"), ("cta", "คอมเมนต์ COLOR รับแพ็กฟรี")]
WATERMARK = "ColorMe · AI วันละแอป"


def _r(x, n=1):
    return round(x + 0.0, n)


def _hex(rgb):
    return "#%02X%02X%02X" % rgb


def photo_check(light, sharp, subject, busy):
    """All inputs 0..1 from on-device checks: light, sharpness, subject size in frame, background clutter."""
    for v in (light, sharp, subject, busy):
        if not 0 <= v <= 1:
            raise ValueError("0..1")
    score = int(round(100 * (0.3 * light + 0.3 * sharp + 0.25 * subject + 0.15 * (1 - busy))))
    tips = []
    if light < 0.5: tips.append("รูปมืดไป เลือกรูปที่สว่างกว่านี้")
    if sharp < 0.5: tips.append("รูปเบลอ เส้นจะขาด ๆ เลือกรูปที่ชัดกว่า")
    if subject < 0.3: tips.append("ตัวหลักเล็กไป ครอปให้ใหญ่ขึ้น")
    if busy > 0.7: tips.append("พื้นหลังรกมาก เปิด 'ลบพื้นหลัง' จะได้เส้นสวยขึ้น")
    return {"score": score, "ok": score >= 60, "tips_th": tips}


def level_for_age(age):
    if age < 3:
        raise ValueError("under_3")
    for k, v in LEVELS.items():
        if v["ages"][0] <= age <= v["ages"][1]:
            return k
    raise ValueError("age")


def nearest(rgb, keys=KEYS):
    return min(keys, key=lambda k: (sum((a - b) ** 2 for a, b in zip(rgb, CRAYON[k][3])), KEYS.index(k)))


def despeckle(grid):
    """Remove dust / JPEG specks: a cell with no same-colour 4-neighbour takes the majority colour of its 3×3 window."""
    h, w = len(grid), len(grid[0]); out = [row[:] for row in grid]
    for y in range(h):
        for x in range(w):
            if any(0 <= j < h and 0 <= i < w and grid[j][i] == grid[y][x] for j, i in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1))):
                continue
            win = [grid[j][i] for j in range(max(0, y - 1), min(h, y + 2)) for i in range(max(0, x - 1), min(w, x + 2)) if (j, i) != (y, x)]
            out[y][x] = sorted(set(win), key=lambda c: (-win.count(c), KEYS.index(c)))[0]
    return out


def pick_palette(pic, k):
    """k most common crayon colours after despeckling, in crayon order (so numbers are stable)."""
    cnt = {}
    for row in despeckle([[nearest(px) for px in row] for row in pic]):
        for n in row:
            cnt[n] = cnt.get(n, 0) + 1
    top = sorted(cnt, key=lambda c: (-cnt[c], KEYS.index(c)))[:k]
    return sorted(top, key=KEYS.index)


def quantize(pic, keys):
    return [[nearest(px, keys) for px in row] for row in pic]


def regions(grid):
    """4-connected same-colour regions, numbered in row-major order of their first cell."""
    h, w = len(grid), len(grid[0]); lab = [[0] * w for _ in range(h)]; out = []
    for y in range(h):
        for x in range(w):
            if lab[y][x]:
                continue
            rid = len(out) + 1; col = grid[y][x]; q = deque([(y, x)]); lab[y][x] = rid; cells = []
            while q:
                cy, cx = q.popleft(); cells.append((cy, cx))
                for ny, nx in ((cy - 1, cx), (cy + 1, cx), (cy, cx - 1), (cy, cx + 1)):
                    if 0 <= ny < h and 0 <= nx < w and not lab[ny][nx] and grid[ny][nx] == col:
                        lab[ny][nx] = rid; q.append((ny, nx))
            out.append({"id": rid, "color": col, "area": len(cells), "cells": cells})
    return out, lab


def merge_small(grid, min_area):
    """Repaint every region smaller than min_area with its most common neighbour colour (smallest first)."""
    g = [row[:] for row in grid]; h, w = len(g), len(g[0])
    while True:
        regs, lab = regions(g)
        small = sorted((r for r in regs if r["area"] < min_area), key=lambda r: (r["area"], r["id"]))
        if not small or len(regs) == 1:
            return g
        r = small[0]; nb = {}
        for cy, cx in r["cells"]:
            for ny, nx in ((cy - 1, cx), (cy + 1, cx), (cy, cx - 1), (cy, cx + 1)):
                if 0 <= ny < h and 0 <= nx < w and lab[ny][nx] != r["id"]:
                    nb[g[ny][nx]] = nb.get(g[ny][nx], 0) + 1
        col = sorted(nb, key=lambda c: (-nb[c], KEYS.index(c)))[0]
        for cy, cx in r["cells"]:
            g[cy][cx] = col


def outline(grid):
    """Line art: cells whose right or lower neighbour has another colour."""
    h, w = len(grid), len(grid[0]); e = set()
    for y in range(h):
        for x in range(w):
            if (x + 1 < w and grid[y][x + 1] != grid[y][x]) or (y + 1 < h and grid[y + 1][x] != grid[y][x]):
                e.add((y, x))
    return e


def label_point(region, lab, h, w):
    """Cell deepest inside the region (max BFS distance from its edge), so the number never sits on a line."""
    rid = region["id"]; cells = set(region["cells"]); dist = {}; q = deque()
    for cy, cx in region["cells"]:
        for ny, nx in ((cy - 1, cx), (cy + 1, cx), (cy, cx - 1), (cy, cx + 1)):
            if not (0 <= ny < h and 0 <= nx < w) or lab[ny][nx] != rid:
                dist[(cy, cx)] = 0; q.append((cy, cx)); break
    while q:
        cy, cx = q.popleft()
        for n in ((cy - 1, cx), (cy + 1, cx), (cy, cx - 1), (cy, cx + 1)):
            if n in cells and n not in dist:
                dist[n] = dist[(cy, cx)] + 1; q.append(n)
    best = max(region["cells"], key=lambda c: (dist[c], -c[0], -c[1]))
    return best, dist[best]


def make_page(pic, age, mode="numbers"):
    """Photo → coloring page. Auto-simplifies until the region count suits the child's age."""
    if mode not in MODES:
        raise ValueError("mode")
    lv = level_for_age(age); L = LEVELS[lv]
    keys = pick_palette(pic, L["max_colors"]); g = despeckle(quantize(pic, keys))
    min_area, passes = L["min_area"], 0
    while True:
        g2 = merge_small(g, min_area); regs, lab = regions(g2)
        if len(regs) <= L["max_regions"] or passes >= 4:
            break
        min_area *= 2; passes += 1
    h, w = len(g2), len(g2[0])
    used = sorted({r["color"] for r in regs}, key=KEYS.index)
    num = {k: i + 1 for i, k in enumerate(used)}
    numbers = mode == "numbers" and L["numbers"]
    labels = []
    for r in regs:
        (y, x), d = label_point(r, lab, h, w)
        labels.append({"region": r["id"], "num": num[r["color"]], "x": x, "y": y, "fits": d >= 1 or r["area"] >= 4})
    legend = [{"num": num[k], "key": k, "name_th": CRAYON[k][1], "hex": _hex(CRAYON[k][3]), "regions": sum(1 for r in regs if r["color"] == k)} for k in used]
    e = outline(g2)
    return {"level": lv, "mode": mode, "w": w, "h": h, "colors": len(used), "regions": len(regs), "min_area": min_area,
            "simplify_passes": passes, "line_px": L["line_px"], "show_numbers": numbers, "edge_ratio": _r(len(e) / (w * h), 3),
            "legend": legend, "labels": labels if numbers else [], "grid": g2}


def page_public(page):
    """Page without the raw grid (what the API returns / the share link stores)."""
    return {k: v for k, v in page.items() if k != "grid"}


def dot_to_dot(points, age):
    """Evenly spaced numbered dots along a closed outline (polygon of (x, y) in 0..100 units)."""
    n = LEVELS[level_for_age(age)]["dots"]
    if len(points) < 3:
        raise ValueError("need a polygon")
    segs = [(points[i], points[(i + 1) % len(points)]) for i in range(len(points))]
    lens = [math.dist(a, b) for a, b in segs]; per = sum(lens); step = per / n; out = []
    for i in range(n):
        t = i * step; j = 0
        while t > lens[j]:
            t -= lens[j]; j += 1
        (ax, ay), (bx, by) = segs[j]; f = t / lens[j] if lens[j] else 0
        out.append({"num": i + 1, "x": _r(ax + (bx - ax) * f), "y": _r(ay + (by - ay) * f)})
    return {"level": level_for_age(age), "dots": out, "perimeter": _r(per), "spacing": _r(step), "closed": True}


def ink_pct(page, ink_saver=False):
    lp = max(2, page["line_px"] // 2) if ink_saver else page["line_px"]
    return min(35.0, _r(page["edge_ratio"] * lp * 6, 1)), lp


def booklet(pages, child_name_th, ink_saver=False):
    """A4 printable book: a cover with the child's name + 1–12 pages (300 dpi)."""
    if not 1 <= len(pages) <= 12:
        raise ValueError("1–12 pages")
    inks = [ink_pct(p, ink_saver) for p in pages]
    return {"title_th": "สมุดระบายสีของ" + child_name_th, "pages": len(pages) + 1, "sheets_double_sided": math.ceil((len(pages) + 1) / 2),
            "paper": "A4", "dpi": 300, "px": list(A4_PX), "ink_saver": ink_saver, "line_px": inks[0][1],
            "ink_pct": _r(sum(i[0] for i in inks) / len(inks), 1), "has_answer_key": any(p["show_numbers"] for p in pages)}


def progress_check(page, scan):
    """scan: grid of crayon keys or None (blank) from the scanned/photographed finished page. Praise only, never a fail."""
    g = page["grid"]; regs, _ = regions(g); paint = [r for r in regs if r["color"] != "white"]
    colored = matched = cells_col = in_lines = 0; favs = {}
    for r in paint:
        got = [scan[y][x] for y, x in r["cells"] if scan[y][x] is not None]
        for c in got:
            favs[c] = favs.get(c, 0) + 1
        if len(got) >= 0.6 * r["area"]:
            colored += 1
            top = sorted(set(got), key=lambda c: (-got.count(c), KEYS.index(c)))[0]
            matched += top == r["color"]
            cells_col += len(got); in_lines += got.count(top)
    cov = colored / len(paint) if paint else 1.0
    stars = 1 + (cov >= 0.5) + (cov >= 0.9)
    fav = sorted(favs, key=lambda c: (-favs[c], KEYS.index(c)))[0] if favs else None
    praise = {1: "เริ่มต้นได้สวยมาก! ระบายต่ออีกนิดนะ", 2: "เกินครึ่งแล้ว สีสดใสมาก!", 3: "เสร็จแล้ว! ผลงานศิลปินตัวจริง"}[stars]
    if fav:
        praise += " ชอบสี" + CRAYON[fav][1].split(" ")[0] + "ที่เลือกจัง"
    return {"coverage_pct": int(round(cov * 100)), "in_lines_pct": int(round(100 * in_lines / cells_col)) if cells_col else 100,
            "match_pct": int(round(100 * matched / colored)) if (colored and page["show_numbers"]) else None,
            "stars": stars, "favorite": fav, "praise_th": praise, "done": cov >= 0.9}


def quest(today, history):
    """Daily theme + streak. history: list of ISO dates with a finished page."""
    d = _date.fromisoformat(today); s = set(history); done = today in s
    k = 0; cur = d if done else _date.fromordinal(d.toordinal() - 1)
    while cur.isoformat() in s:
        k += 1; cur = _date.fromordinal(cur.toordinal() - 1)
    return {"date": today, "theme_th": THEMES[d.toordinal() % len(THEMES)], "streak": k, "done_today": done,
            "new_sticker": STICKERS.get(k) if done else None}


def gallery_summary(entries, month):
    es = [e for e in entries if e["date"].startswith(month)]
    cnt = {}
    for e in es:
        if e["favorite"]:
            cnt[e["favorite"]] = cnt.get(e["favorite"], 0) + 1
    fav = sorted(cnt, key=lambda c: (-cnt[c], KEYS.index(c)))[0] if cnt else None
    return {"month": month, "pages": len(es), "stars": sum(e["stars"] for e in es), "favorite_th": CRAYON[fav][1] if fav else None,
            "art_book_ready": len(es) >= 8, "note_th": "ครบ 8 หน้า ทำสมุดผลงานประจำเดือนได้แล้ว!" if len(es) >= 8 else "อีก %d หน้า จะได้สมุดผลงานประจำเดือน" % (8 - len(es))}


def share_card(page, progress=None, layout="before_after"):
    if layout not in ("before_after", "reveal", "booklet"):
        raise ValueError("layout")
    return {"layout": layout, "size": "1080x1350", "child_face_hidden": True, "stars": progress["stars"] if progress else None,
            "level_th": LEVELS[page["level"]]["name_th"], "watermark": WATERMARK, "badge_th": "รูปในมือถือ → สมุดระบายสีของหนู"}


def reel_plan(seconds=20):
    if not 15 <= seconds <= 30:
        raise ValueError("Reel must be 15–30 s")
    n = len(REEL_SHOTS); cut = [round(seconds * i / n, 1) for i in range(n + 1)]
    return {"seconds": seconds, "ratio": "9:16", "bpm": 110,
            "shots": [{"kind": k, "start": cut[i], "end": cut[i + 1], "caption_th": c} for i, (k, c) in enumerate(REEL_SHOTS)], "watermark": WATERMARK}


def quota(used_today, plan="free"):
    limit = {"free": 5, "plus": 50}[plan]
    return {"plan": plan, "pages_per_day": limit, "used": used_today, "left": max(0, limit - used_today), "blocked": used_today >= limit}


def privacy_check(own_photo, parent_mode, found=()):
    """found: flags from the vision check (nudity, id_document, violent, other_child_face, copyright_character)."""
    flags = list(found)
    if not own_photo and "other_child_face" not in flags:
        flags.append("other_child_face")
    levels = [GUARD[f][0] for f in flags]
    level = "stop" if "stop" in levels else "warn" if "warn" in levels else "ok"
    msgs = [GUARD[f][1] for f in flags] or [GUARD[None][1]]
    return {"allowed": level != "stop", "level": level, "flags": flags, "messages_th": msgs, "parent_mode": parent_mode,
            "share_allowed": level == "ok" and parent_mode}


def safety_guard(flag=None):
    level, msg = GUARD[flag]
    return {"flag": flag, "level": level, "message_th": msg, "block": level == "stop"}
