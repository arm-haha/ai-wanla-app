"""Cover art for BrickBuddy — fully procedural (PIL). No real people, photos or brands; generic stud bricks only.
Left = messy pile of bricks on the floor (BEFORE), right = phone showing the duck you can build + idea cards (AFTER)."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
G = '/usr/share/fonts/truetype/sand-box/google/'
K = G + 'Kanit/Kanit-'
F = lambda w, s: ImageFont.truetype(K + w + '.ttf', s, layout_engine=ImageFont.Layout.RAQM)
COL = [(208, 49, 45), (30, 90, 168), (246, 194, 28), (46, 139, 62), (244, 244, 244), (240, 127, 29), (27, 27, 27), (242, 156, 192)]


def shade(c, k):
    return tuple(max(0, min(255, int(v * k))) for v in c)


def brick_top(w, h, color, u=34):
    """top-down brick w×h studs."""
    im = Image.new('RGBA', (w * u + 8, h * u + 8), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([4, 4, 4 + w * u, 4 + h * u], 5, fill=color + (255,), outline=shade(color, 0.7) + (255,), width=2)
    for i in range(w):
        for j in range(h):
            cx, cy = 4 + i * u + u // 2, 4 + j * u + u // 2; r = int(u * 0.31)
            d.ellipse([cx - r + 2, cy - r + 3, cx + r + 2, cy + r + 3], fill=shade(color, 0.72) + (255,))
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=shade(color, 1.12) + (255,), outline=shade(color, 0.85) + (255,), width=1)
            d.arc([cx - r + 3, cy - r + 3, cx + r - 3, cy + r - 3], 200, 290, fill=(255, 255, 255, 150), width=2)
    return im


def pile(W, H):
    rnd = random.Random(21)
    im = Image.new('RGB', (W, H), (226, 206, 172)); d = ImageDraw.Draw(im)
    for x in range(0, W, 90):  # wooden floor boards
        d.rectangle([x, 0, x + 88, H], fill=(222 - rnd.randint(0, 14), 200 - rnd.randint(0, 14), 164 - rnd.randint(0, 10)))
        for _ in range(6):
            yy = rnd.randint(0, H); d.line([(x + 6, yy), (x + 80, yy + rnd.randint(-8, 8))], fill=(200, 176, 140), width=1)
    sizes = [(4, 2), (2, 2), (2, 1), (4, 1), (1, 1), (3, 2), (2, 2), (1, 1)]
    for k in range(95):
        w, h = rnd.choice(sizes); c = rnd.choice(COL)
        b = brick_top(w, h, c, rnd.choice((30, 34, 38))).rotate(rnd.uniform(0, 360), expand=True, resample=Image.BICUBIC)
        x = int(rnd.gauss(W * 0.5, W * 0.28)) - b.width // 2; y = int(rnd.gauss(H * 0.55, H * 0.24)) - b.height // 2
        sh = Image.new('RGBA', b.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, 90), (0, 0), b)
        im.paste(sh.filter(ImageFilter.GaussianBlur(4)), (x + 6, y + 8), sh.filter(ImageFilter.GaussianBlur(4)))
        im.paste(b, (x, y), b)
    return im


def front_brick(d, x, y, w, color, u=26, hgt=30):
    """front view brick of w studs at (x,y)=top-left of body."""
    for i in range(w):
        sx = x + i * u + u // 2
        d.rectangle([sx - 8, y - 7, sx + 8, y], fill=shade(color, 1.05), outline=shade(color, 0.75))
    d.rectangle([x, y, x + w * u, y + hgt], fill=color, outline=shade(color, 0.7), width=2)
    d.line([(x + 3, y + 4), (x + w * u - 3, y + 4)], fill=shade(color, 1.18), width=2)


def star(d, cx, cy, r, fill):
    import math
    pts = [(cx + (r if i % 2 == 0 else r * 0.45) * math.sin(math.pi * i / 5), cy - (r if i % 2 == 0 else r * 0.45) * math.cos(math.pi * i / 5)) for i in range(10)]
    d.polygon(pts, fill=fill)


def sparkle(d, cx, cy, r, fill):
    d.polygon([(cx, cy - r), (cx + r * 0.25, cy - r * 0.25), (cx + r, cy), (cx + r * 0.25, cy + r * 0.25), (cx, cy + r), (cx - r * 0.25, cy + r * 0.25), (cx - r, cy), (cx - r * 0.25, cy - r * 0.25)], fill=fill)


def phone(W, H):
    im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im)
    for y in range(H):
        t = y / H; d.line([(0, y), (W, y)], fill=(int(255 - 10 * t), int(236 - 40 * t), int(170 - 60 * t)))
    pw, ph = int(W * 0.82), int(H * 0.64)
    px, py = (W - pw) // 2, int(H * 0.15)
    d.rounded_rectangle([px + 10, py + 14, px + pw + 10, py + ph + 14], 50, fill=(170, 120, 60))
    d.rounded_rectangle([px, py, px + pw, py + ph], 50, fill=(25, 25, 32))
    sx, sy, sw, sh = px + 18, py + 18, pw - 36, ph - 36
    d.rounded_rectangle([sx, sy, sx + sw, sy + sh], 36, fill=(255, 248, 236))
    d.text((sx + sw // 2, sy + 44), 'BrickBuddy', font=F('SemiBold', 28), fill=(40, 40, 40), anchor='mm')
    d.rounded_rectangle([sx + 30, sy + 74, sx + sw - 30, sy + 122], 24, fill=(46, 139, 62))
    d.text((sx + sw // 2, sy + 98), 'นับได้ 61 ชิ้น · ต่อได้ 11 แบบ', font=F('Medium', 26), fill='white', anchor='mm')
    # the duck, built from front-view bricks
    Y, R, O = (246, 194, 28), (208, 49, 45), (240, 127, 29)
    u = max(20, int(sw / 13)); bx = sx + (sw - 7 * u) // 2; base = sy + int(sh * 0.62)
    hg = int(u * 1.15)
    front_brick(d, bx, base - hg, 7, Y, u, hg)
    front_brick(d, bx + u, base - 2 * hg, 4, Y, u, hg)
    front_brick(d, bx + 4 * u, base - 3 * hg, 3, Y, u, hg)
    front_brick(d, bx + 4 * u, base - 4 * hg, 2, Y, u, hg)
    d.polygon([(bx + 6 * u, base - 3 * hg + 8), (bx + 7 * u + 26, base - 3 * hg + hg // 2 + 4), (bx + 6 * u, base - 2 * hg - 4)], fill=O, outline=shade(O, 0.7))
    ex, ey = bx + 5 * u + 4, base - 4 * hg + hg // 2
    d.ellipse([ex - 10, ey - 10, ex + 10, ey + 10], fill='white', outline=(30, 30, 30), width=2); d.ellipse([ex - 4, ey - 4, ex + 6, ey + 6], fill=(20, 20, 20))
    front_brick(d, bx - u // 2, base, 8, R, u, int(hg * 0.4))
    for k, (cx, cy) in enumerate(((sx + 40, base - 4 * hg), (sx + sw - 50, base - 3 * hg - 30), (sx + 60, base - 2 * hg))):
        sparkle(d, cx, cy, 18 - k * 3, (255, 180, 40))
    d.text((sx + sw // 2, base - 5 * hg - 10), 'ไอเดียที่ 1 จาก 6', font=F('Regular', 22), fill=(120, 110, 100), anchor='mm')
    t = 'เป็ดน้อย · 5 ขั้น'; f = F('Medium', 26); tw = d.textlength(t, font=f); ty = base + int(hg * 0.4) + 34
    x0 = sx + (sw - tw - 4 * 26) // 2
    d.text((x0, ty), t, font=f, fill=(60, 50, 40), anchor='lm')
    for k in range(4):
        star(d, x0 + tw + 18 + k * 26, ty, 11, (255, 176, 0))
    cy = base + int(hg * 0.4) + 74
    for i, (t, c) in enumerate((('รถแข่ง', (30, 90, 168)), ('จรวด', (208, 49, 45)), ('ต้นคริสต์มาส', (46, 139, 62)))):
        cw = (sw - 48) // 3; cx = sx + 18 + i * (cw + 6)
        if cy + 50 < sy + sh - 10:
            d.rounded_rectangle([cx, cy, cx + cw, cy + 50], 18, fill=c)
            d.text((cx + cw // 2, cy + 25), t, font=F('Medium', 21), fill='white', anchor='mm')
    return im


def make(W, H, name):
    m = W // 2
    im = Image.new('RGB', (W, H))
    im.paste(pile(m, H), (0, 0)); im.paste(phone(W - m, H), (m, 0))
    ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    gh = int(H * 0.44)
    for i in range(gh):
        od.line([(0, H - gh + i), (W, H - gh + i)], fill=(20, 14, 10, int(250 * min(1, (i / gh) * 1.25) ** 1.2)))
    im = Image.alpha_composite(im.convert('RGBA'), ov); d = ImageDraw.Draw(im)
    d.rectangle([m - 2, 0, m + 2, H], fill='white')
    cy = int(H * 0.40); d.ellipse([m - 34, cy - 34, m + 34, cy + 34], fill='white', outline=(0, 0, 0, 60), width=2)
    d.text((m - 14, cy), '◀', font=F('Regular', 26), fill=(40, 40, 40), anchor='mm'); d.text((m + 14, cy), '▶', font=F('Regular', 26), fill=(40, 40, 40), anchor='mm')

    def pill(x, y, t, bg, fg, font, anchor):
        bb = d.textbbox((x, y), t, font=font, anchor=anchor); p = 14
        d.rounded_rectangle([bb[0] - p * 1.6, bb[1] - p, bb[2] + p * 1.6, bb[3] + p], radius=40, fill=bg); d.text((x, y), t, font=font, fill=fg, anchor=anchor)
    top = int(H * 0.12) if H > W else 120
    pill(m - 170, top, 'กองนี้ต่ออะไรดี?', (0, 0, 0, 175), 'white', F('SemiBold', 32), 'mm')
    pill(m + 170, top, 'ต่อได้ทันที!', (255, 196, 64, 255), (30, 20, 0), F('SemiBold', 32), 'mm')
    pill(W // 2, 52, 'AI วันละแอป · แจกฟรี / Free', (255, 255, 255, 235), (25, 25, 25), F('Medium', 32), 'mm')
    s = 1.0 if H > W else 0.85
    y = H - int(60 * s)
    d.text((W // 2, y), 'Snap your brick pile, see what to build', font=F('Regular', int(42 * s)), fill=(235, 235, 235), anchor='ms'); y -= int(76 * s)
    d.text((W // 2, y), 'ถ่ายกองตัวต่อ รู้เลยต่ออะไรได้', font=F('SemiBold', int(58 * s)), fill=(255, 205, 90), anchor='ms'); y -= int(100 * s)
    d.text((W // 2, y), 'BrickBuddy', font=F('Bold', int(120 * s)), fill='white', anchor='ms', stroke_width=2, stroke_fill=(0, 0, 0))
    im.convert('RGB').save(name)


make(1080, 1350, 'cover_1080x1350.png'); make(1080, 1080, 'cover_1080x1080.png')
