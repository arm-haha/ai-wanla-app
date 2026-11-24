"""Fictional demo data only — no real people, no real photos. The 'photo' is generated procedurally:
an orange cat (น้องส้มจี๊ด) sitting on grass under a blue sky with a sun, plus camera noise and dust specks."""
from colorme import *

TODAY = "2026-12-23"
W, H = 24, 30
KIDS = [{"id": "k01", "name_th": "น้องข้าวปั้น", "name_en": "Khaopan", "age": 6, "city_th": "นนทบุรี"},
        {"id": "k02", "name_th": "น้องไข่ตุ๋น", "name_en": "Khaitun", "age": 4, "city_th": "เชียงใหม่"},
        {"id": "k03", "name_th": "น้องภูผา", "name_en": "Phupha", "age": 10, "city_th": "ขอนแก่น"},
        {"id": "k04", "name_th": "คุณแม่ฝน", "name_en": "Fon", "age": 36, "city_th": "นนทบุรี"}]


def _lcg(seed):
    while True:
        seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
        yield seed


def cat_photo(noise=True):
    C = {k: v[3] for k, v in CRAYON.items()}
    pic = []
    for y in range(H):
        row = []
        for x in range(W):
            c = C["sky"] if y < 19 else C["lime"]
            if y >= 22 and x % 5 == 1 and y % 4 in (0, 1, 2): c = C["green"]               # grass tufts
            if (x - 19) ** 2 + (y - 4) ** 2 <= 9: c = C["yellow"]                          # sun
            if ((x - 12) / 6.5) ** 2 + ((y - 20) / 6) ** 2 <= 1: c = C["orange"]           # body
            if (x - 12) ** 2 + (y - 10) ** 2 <= 22: c = C["orange"]                        # head
            if (7 <= x <= 9 and 4 <= y <= 7 and x - 7 >= 7 - y) or (15 <= x <= 17 and 4 <= y <= 7 and 17 - x >= 7 - y): c = C["orange"]  # ears
            if 9 <= x <= 15 and y == 15: c = C["red"]                                       # collar
            if y in (19, 22) and 8 <= x <= 16: c = C["brown"]                               # stripes
            if (x, y) in ((10, 9), (14, 9), (10, 10), (14, 10)): c = C["black"]             # eyes
            if (x, y) == (12, 11): c = C["pink"]                                            # nose
            if 18 <= x <= 20 and 16 <= y <= 24 and ((x - 19) ** 2 + (y - 20) ** 2) > 2: c = C["orange"]   # tail
            row.append(c)
        pic.append(row)
    if noise:
        g = _lcg(2312)
        for y in range(H):
            for x in range(W):
                r = next(g)
                if r % 97 == 0:
                    pic[y][x] = C["purple"]                                                # dust speck
                else:
                    pic[y][x] = tuple(max(0, min(255, v + (next(g) % 25) - 12)) for v in pic[y][x])
    return pic


PIC = cat_photo()
PAGE_KID = make_page(PIC, 6)            # น้องข้าวปั้น 6 ขวบ, ระบายตามเลข
PAGE_TINY = make_page(PIC, 4)           # น้องไข่ตุ๋น 4 ขวบ, เส้นหนา ช่องใหญ่
PAGE_BIG = make_page(PIC, 10)
PAGE_CALM = make_page(PIC, 36)
PAGE_LINE = make_page(PIC, 6, "lineart")
# outline of the cat for dot-to-dot (0..100 units)
CAT_OUTLINE = [(30, 20), (35, 5), (42, 15), (58, 15), (65, 5), (70, 20), (72, 40), (85, 60), (80, 90), (20, 90), (15, 60), (28, 40)]


def scan_of(page, frac, wrong_every=0, spill=0):
    """Simulated scan: the child coloured the first `frac` of regions (by id); every Nth coloured region in a different colour."""
    regs, _ = regions(page["grid"]); paint = [r for r in regs if r["color"] != "white"]
    s = [[None] * page["w"] for _ in range(page["h"])]; n = int(round(len(paint) * frac))
    for i, r in enumerate(paint[:n]):
        col = r["color"] if not (wrong_every and (i + 1) % wrong_every == 0) else ("purple" if r["color"] != "purple" else "pink")
        for y, x in r["cells"]:
            s[y][x] = col
    for y, x in (paint[0]["cells"][:spill] if spill and n else []):
        s[y][x] = "orange" if paint[0]["color"] != "orange" else "red"      # crayon went over the line
    return s


SCAN_DONE = scan_of(PAGE_KID, 1.0)
SCAN_HALF = scan_of(PAGE_KID, 0.5, wrong_every=3)
SCAN_START = scan_of(PAGE_KID, 0.2)
HISTORY = ["2026-12-17", "2026-12-18", "2026-12-19", "2026-12-21", "2026-12-22", "2026-12-23"]
GALLERY = [{"date": "2026-12-%02d" % d, "title_th": t, "stars": s, "favorite": f} for d, t, s, f in
           ((5, "น้องส้มจี๊ด", 3, "orange"), (8, "บ้านคุณยาย", 2, "red"), (11, "ไอติมแท่ง", 3, "pink"), (14, "รถคันโปรด", 2, "blue"),
            (17, "ต้นมะม่วง", 3, "green"), (19, "ทะเลหัวหิน", 3, "sky"), (21, "ขนมครก", 1, "orange"), (23, "น้องส้มจี๊ด", 3, "orange"))]
