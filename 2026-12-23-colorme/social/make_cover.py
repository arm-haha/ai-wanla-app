"""Cover art for ColorMe — fully procedural (PIL). No real people, photos or brands; the cat is a drawn graphic.
Left = a colourful phone photo of a pet cat (BEFORE), right = the same picture as a printed colour-by-number page,
half coloured with crayon strokes (AFTER)."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math, random
G = '/usr/share/fonts/truetype/sand-box/google/'
K = G + 'Kanit/Kanit-'
F = lambda w, s: ImageFont.truetype(K + w + '.ttf', s, layout_engine=ImageFont.Layout.RAQM)
COL = {"sky": (120, 190, 240), "lime": (150, 210, 80), "green": (40, 150, 70), "yellow": (255, 214, 10), "orange": (247, 140, 40),
       "red": (230, 57, 70), "brown": (140, 90, 50), "black": (30, 30, 30), "pink": (255, 140, 180)}
NUM = {"red": 1, "orange": 2, "yellow": 3, "lime": 4, "sky": 5, "brown": 6}


def scene(W, H, line=False):
    """The cat picture in a W×H box. line=True → white regions with black outlines (coloring page)."""
    s = W / 100.0
    im = Image.new('RGB', (W, H), (255, 255, 255)); d = ImageDraw.Draw(im)
    lw = max(3, int(s * 0.9)); ol = (35, 35, 40)
    f = lambda c: (255, 255, 255) if line else COL[c]
    o = lambda: ol if line else None
    w = lw if line else 0
    gy = H * 0.64
    if not line:
        for y in range(int(gy)):
            t = y / gy; d.line([(0, y), (W, y)], fill=(int(150 - 40 * t), int(205 - 20 * t), int(250 - 10 * t)))
        d.rectangle([0, gy, W, H], fill=COL["lime"])
    else:
        d.line([(0, gy), (W, gy)], fill=ol, width=w)
    d.ellipse([W * 0.70, H * 0.05, W * 0.92, H * 0.05 + W * 0.22], fill=f("yellow"), outline=o(), width=w)            # sun
    if not line:
        for a in range(0, 360, 30):
            cx, cy, r = W * 0.81, H * 0.05 + W * 0.11, W * 0.15
            d.line([(cx + math.cos(math.radians(a)) * r * 0.82, cy + math.sin(math.radians(a)) * r * 0.82),
                    (cx + math.cos(math.radians(a)) * r, cy + math.sin(math.radians(a)) * r)], fill=COL["yellow"], width=int(s))
    for gx in range(6, 100, 18):                                                                                       # grass tufts
        x = W * gx / 100
        d.polygon([(x, H * 0.80), (x + s * 2, H * 0.74), (x + s * 4, H * 0.80)], fill=f("green"), outline=o(), width=w)
    cx = W * 0.47
    d.ellipse([cx - W * 0.28, H * 0.46, cx + W * 0.28, H * 0.84], fill=f("orange"), outline=o(), width=w)                # body
    d.ellipse([cx + W * 0.18, H * 0.50, cx + W * 0.34, H * 0.56], fill=f("orange"), outline=o(), width=w)                # tail
    for sy in (0.58, 0.67):                                                                                             # stripes
        d.rounded_rectangle([cx - W * 0.20, H * sy, cx + W * 0.20, H * sy + H * 0.035], radius=int(s * 2), fill=f("brown"), outline=o(), width=w)
    for sx in (-1, 1):                                                                                                  # ears
        d.polygon([(cx + sx * W * 0.08, H * 0.22), (cx + sx * W * 0.22, H * 0.10), (cx + sx * W * 0.20, H * 0.30)], fill=f("orange"), outline=o(), width=w)
    d.ellipse([cx - W * 0.21, H * 0.17, cx + W * 0.21, H * 0.47], fill=f("orange"), outline=o(), width=w)                # head
    d.rounded_rectangle([cx - W * 0.17, H * 0.44, cx + W * 0.17, H * 0.48], radius=int(s * 1.5), fill=f("red"), outline=o(), width=w)  # collar
    for sx in (-1, 1):
        d.ellipse([cx + sx * W * 0.08 - s * 2.4, H * 0.28, cx + sx * W * 0.08 + s * 2.4, H * 0.28 + s * 6], fill=COL["black"])
        if not line:
            d.ellipse([cx + sx * W * 0.08 - s * 0.6, H * 0.29, cx + sx * W * 0.08 + s * 1.2, H * 0.29 + s * 1.8], fill='white')
    d.polygon([(cx - s * 2, H * 0.36), (cx + s * 2, H * 0.36), (cx, H * 0.38)], fill=COL["pink"] if not line else ol)
    d.arc([cx - s * 5, H * 0.36, cx, H * 0.41], 20, 160, fill=ol if line else COL["black"], width=max(2, int(s * 0.5)))
    d.arc([cx, H * 0.36, cx + s * 5, H * 0.41], 20, 160, fill=ol if line else COL["black"], width=max(2, int(s * 0.5)))
    for sx in (-1, 1):
        for k in (-1, 0, 1):
            d.line([(cx + sx * s * 6, H * 0.37 + k * s), (cx + sx * s * 15, H * 0.36 + k * s * 2.5)], fill=ol if line else (90, 60, 40), width=max(2, int(s * 0.35)))
    if line:
        fnt = F('Medium', int(s * 4.2))
        for c, (x, y) in (("sky", (0.18, 0.18)), ("sky", (0.60, 0.40)), ("yellow", (0.81, 0.14)), ("orange", (0.47, 0.25)), ("orange", (0.32, 0.53)),
                          ("brown", (0.47, 0.595)), ("brown", (0.47, 0.685)), ("orange", (0.47, 0.77)), ("red", (0.60, 0.46)), ("lime", (0.15, 0.90)), ("lime", (0.85, 0.90))):
            d.text((W * x, H * y), str(NUM[c]), font=fnt, fill=(120, 120, 130), anchor='mm')
    return im


def before(W, H):
    im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im)
    for y in range(H):
        t = y / H; d.line([(0, y), (W, y)], fill=(int(255 - 20 * t), int(236 - 30 * t), int(214 - 30 * t)))
    pw, ph = int(W * 0.80), int(H * 0.60); px, py = (W - pw) // 2, int(H * 0.16)
    d.rounded_rectangle([px + 10, py + 14, px + pw + 10, py + ph + 14], 50, fill=(170, 130, 100))
    d.rounded_rectangle([px, py, px + pw, py + ph], 50, fill=(25, 25, 32))
    sx, sy, sw, sh = px + 16, py + 16, pw - 32, ph - 32
    scr = Image.new('RGB', (sw, sh), (20, 20, 24)); sd = ImageDraw.Draw(scr)
    sd.text((24, 40), 'คลังรูปภาพ', font=F('SemiBold', 26), fill='white', anchor='lm')
    photo = scene(sw - 32, int((sw - 32) * 1.18))
    photo = photo.filter(ImageFilter.GaussianBlur(1.2))
    scr.paste(photo, (16, 80))
    ty = 80 + photo.size[1] + 16; tw = (sw - 32 - 16) // 3
    for i, c in enumerate(((255, 190, 120), (170, 210, 250), (200, 230, 160))):
        sd.rounded_rectangle([16 + i * (tw + 8), ty, 16 + i * (tw + 8) + tw, ty + tw], 10, fill=c)
    mask = Image.new('L', (sw, sh), 0); ImageDraw.Draw(mask).rounded_rectangle([0, 0, sw - 1, sh - 1], 36, fill=255)
    im.paste(scr, (sx, sy), mask)
    return im


def crayon(d, x, y, ang, col, L=170, Wd=30):
    ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    P = lambda u, v: (x + u * ca - v * sa, y + u * sa + v * ca)
    d.polygon([P(0, -Wd / 2), P(L, -Wd / 2), P(L, Wd / 2), P(0, Wd / 2)], fill=col, outline=(0, 0, 0, 90))
    d.polygon([P(L, -Wd / 2), P(L + 34, -Wd / 6), P(L + 34, Wd / 6), P(L, Wd / 2)], fill=col)
    d.polygon([P(L * 0.25, -Wd / 2), P(L * 0.75, -Wd / 2), P(L * 0.75, Wd / 2), P(L * 0.25, Wd / 2)], fill=(255, 255, 255, 140))


def after(W, H):
    im = Image.new('RGBA', (W, H)); d = ImageDraw.Draw(im)
    for y in range(H):
        t = y / H; d.line([(0, y), (W, y)], fill=(int(220 - 30 * t), int(236 - 30 * t), int(255 - 20 * t), 255))
    pw = int(W * 0.84); ph = int(pw * 1.36)
    paper = Image.new('RGBA', (pw, ph), (255, 255, 255, 255)); pd = ImageDraw.Draw(paper)
    pd.text((pw // 2, 36), 'สมุดระบายสีของน้องข้าวปั้น', font=F('SemiBold', 26), fill=(40, 40, 60), anchor='mm')
    aw, ah = pw - 44, int((pw - 44) * 1.12)
    col, ln = scene(aw, ah), scene(aw, ah, line=True)
    rnd = random.Random(7); mask = Image.new('L', (aw, ah), 0); md = ImageDraw.Draw(mask)
    for k in range(260):                                                     # crayon strokes over the left/bottom part
        x0 = rnd.uniform(-40, aw * 0.62); y0 = rnd.uniform(ah * 0.0, ah)
        if x0 + (ah - y0) * 0.3 > aw * 0.66: continue
        md.line([(x0, y0), (x0 + 70, y0 - 26)], fill=235, width=rnd.randint(9, 14))
    col_l = Image.composite(col, ln, mask.filter(ImageFilter.GaussianBlur(1)))
    lnm = ln.convert('L').point(lambda v: 255 if v < 110 else 0)              # keep outlines on top
    col_l.paste(ln, (0, 0), lnm)
    paper.paste(col_l, (22, 64))
    ly = 64 + ah + 18; fx = 28
    for c, n in sorted(NUM.items(), key=lambda kv: kv[1]):
        pd.ellipse([fx, ly, fx + 34, ly + 34], fill=COL[c], outline=(40, 40, 40), width=2)
        pd.text((fx + 17, ly + 17), str(n), font=F('SemiBold', 20), fill='white' if c not in ('yellow', 'lime', 'sky') else (30, 30, 30), anchor='mm')
        fx += (pw - 56) // 6
    paper = paper.rotate(4, expand=True, resample=Image.BICUBIC)
    sh = Image.new('RGBA', paper.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, 80), (0, 0), paper)
    x, y = (W - paper.size[0]) // 2, int(H * 0.14)
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)), (x + 10, y + 14)); im.alpha_composite(paper, (x, y))
    d = ImageDraw.Draw(im)
    crayon(d, W * 0.52, y + paper.size[1] * 0.80, -38, (247, 140, 40, 255))
    crayon(d, W * 0.50, y + paper.size[1] * 1.0, -6, (40, 150, 70, 255), 150)
    return im.convert('RGB')


def make(W, H, name):
    m = W // 2
    im = Image.new('RGB', (W, H))
    im.paste(before(m, H), (0, 0)); im.paste(after(W - m, H), (m, 0))
    ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    gh = int(H * 0.40)
    for i in range(gh):
        od.line([(0, H - gh + i), (W, H - gh + i)], fill=(18, 14, 36, int(250 * min(1, (i / gh) * 1.25) ** 1.2)))
    im = Image.alpha_composite(im.convert('RGBA'), ov); d = ImageDraw.Draw(im)
    d.rectangle([m - 2, 0, m + 2, H], fill='white')
    cy = int(H * 0.40); d.ellipse([m - 34, cy - 34, m + 34, cy + 34], fill='white', outline=(0, 0, 0, 60), width=2)
    d.text((m - 14, cy), '◀', font=F('Regular', 26), fill=(40, 40, 40), anchor='mm'); d.text((m + 14, cy), '▶', font=F('Regular', 26), fill=(40, 40, 40), anchor='mm')

    def pill(x, y, t, bg, fg, font, anchor):
        bb = d.textbbox((x, y), t, font=font, anchor=anchor); p = 14
        d.rounded_rectangle([bb[0] - p * 1.6, bb[1] - p, bb[2] + p * 1.6, bb[3] + p], radius=40, fill=bg); d.text((x, y), t, font=font, fill=fg, anchor=anchor)
    top = int(H * 0.115) if H > W else 118
    pill(m - 170, top, 'รูปในมือถือ', (0, 0, 0, 175), 'white', F('SemiBold', 32), 'mm')
    pill(m + 170, top, 'สมุดระบายสี', (255, 196, 64, 255), (30, 20, 0), F('SemiBold', 32), 'mm')
    pill(W // 2, 52, 'AI วันละแอป · แจกฟรี / Free', (255, 255, 255, 235), (25, 25, 25), F('Medium', 32), 'mm')
    s = 1.0 if H > W else 0.85
    y = H - int(60 * s)
    d.text((W // 2, y), 'Any photo becomes a coloring page', font=F('Regular', int(42 * s)), fill=(235, 235, 235), anchor='ms'); y -= int(76 * s)
    d.text((W // 2, y), 'รูปไหนก็ได้ กลายเป็นหน้าระบายสี', font=F('SemiBold', int(60 * s)), fill=(255, 205, 90), anchor='ms'); y -= int(100 * s)
    d.text((W // 2, y), 'ColorMe', font=F('Bold', int(120 * s)), fill='white', anchor='ms', stroke_width=2, stroke_fill=(0, 0, 0))
    im.convert('RGB').save(name)


make(1080, 1350, 'cover_1080x1350.png'); make(1080, 1080, 'cover_1080x1080.png')
