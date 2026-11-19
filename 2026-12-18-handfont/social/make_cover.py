"""Cover art for HandFont — fully procedural (PIL). No real people, photos or brands.
Left = handwriting template sheet (BEFORE), right = phone typing in that handwriting (AFTER)."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
G = '/usr/share/fonts/truetype/sand-box/google/'
K = G + 'Kanit/Kanit-'
F = lambda w, s: ImageFont.truetype(K + w + '.ttf', s, layout_engine=ImageFont.Layout.RAQM)
HW = lambda s: ImageFont.truetype(G + 'Sriracha/Sriracha-Regular.ttf', s, layout_engine=ImageFont.Layout.RAQM)
INK = (28, 46, 120)
CHARS = list("กขคงจฉชซญฐณดตถทธนบปผฝพฟภมยรลวศษสหฬอฮ") + list("ABCDEFGHabcdefgh123")


def sheet(W, H):
    rnd = random.Random(18)
    im = Image.new('RGB', (W, H), (250, 247, 238)); d = ImageDraw.Draw(im)
    for y in range(0, H, 3):  # paper grain
        d.line([(0, y), (W, y)], fill=(247 - rnd.randint(0, 4), 244 - rnd.randint(0, 4), 234 - rnd.randint(0, 4)))
    cols, cell = 4, W // 4 - 6
    x0, y0 = (W - cols * cell) // 2, int(H * 0.17)
    rows = (H - y0) // cell + 1
    k = 0
    for r in range(rows):
        for c in range(cols):
            x, y = x0 + c * cell, y0 + r * cell
            d.rectangle([x, y, x + cell, y + cell], outline=(170, 190, 215), width=2)
            d.line([(x + 6, y + int(cell * 0.72)), (x + cell - 6, y + int(cell * 0.72))], fill=(205, 215, 232), width=1)
            ch = CHARS[k % len(CHARS)]; k += 1
            d.text((x + 10, y + 6), ch, font=F('Regular', 18), fill=(150, 160, 180))
            g = Image.new('RGBA', (cell, cell), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
            gd.text((cell // 2 + rnd.randint(-5, 5), int(cell * 0.70) + rnd.randint(-4, 4)), ch, font=HW(int(cell * 0.62)), fill=INK + (235,), anchor='ms')
            g = g.rotate(rnd.uniform(-7, 7), resample=Image.BICUBIC)
            im.paste(g, (x, y), g)
    return im.filter(ImageFilter.GaussianBlur(0.4))


def phone(W, H):
    im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im)
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=(int(255 - 20 * t), int(214 - 40 * t), int(222 - 10 * t)))
    pw, ph = int(W * 0.80), int(H * 0.62)
    px, py = (W - pw) // 2, int(H * 0.16)
    d.rounded_rectangle([px + 10, py + 14, px + pw + 10, py + ph + 14], 50, fill=(160, 110, 125))
    d.rounded_rectangle([px, py, px + pw, py + ph], 50, fill=(25, 25, 32))
    sx, sy, sw, sh = px + 18, py + 18, pw - 36, ph - 36
    d.rounded_rectangle([sx, sy, sx + sw, sy + sh], 36, fill=(255, 253, 245))
    for yy in range(sy + 128, sy + sh - 170, 124):
        d.line([(sx + 24, yy), (sx + sw - 24, yy)], fill=(200, 214, 236), width=2)
    d.text((sx + sw // 2, sy + 52), 'HandFont-Mint', font=F('Medium', 26), fill=(120, 110, 130), anchor='mm')
    y = sy + 120
    kb = sy + sh - 150
    lines = [l for i, l in enumerate(('สุขสันต์', 'วันเกิดนะแก', 'ปีนี้ต้องปัง!', 'Love you!')) if sy + 120 + i * 124 < kb - 20]
    lines[-1] = lines[-1] if len(lines) == 4 else 'ปีนี้ต้องปัง!'
    for line in lines:
        d.text((sx + 34, y), line, font=HW(int(sw * 0.13)), fill=INK, anchor='ls'); y += 124
    cx = sx + 34 + d.textlength(lines[-1], font=HW(int(sw * 0.13))) + 14
    d.rectangle([cx, y - 124 - 52, cx + 4, y - 124 + 6], fill=(230, 80, 110))
    kb = sy + sh - 150
    d.rounded_rectangle([sx + 12, kb, sx + sw - 12, sy + sh - 12], 24, fill=(232, 228, 236))
    for i, ch in enumerate('กขคงจฉช'):
        kx = sx + 26 + i * ((sw - 52) // 7)
        d.rounded_rectangle([kx, kb + 18, kx + (sw - 52) // 7 - 8, kb + 74], 10, fill='white')
        d.text((kx + ((sw - 52) // 7 - 8) // 2, kb + 46), ch, font=HW(34), fill=INK, anchor='mm')
    return im


def make(W, H, name):
    m = W // 2
    im = Image.new('RGB', (W, H))
    im.paste(sheet(m, H), (0, 0)); im.paste(phone(W - m, H), (m, 0))
    ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    gh = int(H * 0.46)
    for i in range(gh):
        od.line([(0, H - gh + i), (W, H - gh + i)], fill=(18, 12, 30, int(250 * min(1, (i / gh) * 1.25) ** 1.2)))
    im = Image.alpha_composite(im.convert('RGBA'), ov); d = ImageDraw.Draw(im)
    d.rectangle([m - 2, 0, m + 2, H], fill='white')
    cy = int(H * 0.40); d.ellipse([m - 34, cy - 34, m + 34, cy + 34], fill='white', outline=(0, 0, 0, 60), width=2)
    d.text((m - 14, cy), '◀', font=F('Regular', 26), fill=(40, 40, 40), anchor='mm'); d.text((m + 14, cy), '▶', font=F('Regular', 26), fill=(40, 40, 40), anchor='mm')

    def pill(x, y, t, bg, fg, font, anchor):
        bb = d.textbbox((x, y), t, font=font, anchor=anchor); p = 14
        d.rounded_rectangle([bb[0] - p * 1.6, bb[1] - p, bb[2] + p * 1.6, bb[3] + p], radius=40, fill=bg); d.text((x, y), t, font=font, fill=fg, anchor=anchor)
    top = int(H * 0.12) if H > W else 120
    pill(m - 170, top, 'เขียน 1 แผ่น', (0, 0, 0, 175), 'white', F('SemiBold', 32), 'mm')
    pill(m + 170, top, 'ได้ฟอนต์ตัวเอง', (255, 196, 64, 255), (30, 20, 0), F('SemiBold', 32), 'mm')
    pill(W // 2, 52, 'AI วันละแอป · แจกฟรี / Free', (255, 255, 255, 235), (25, 25, 25), F('Medium', 32), 'mm')
    s = 1.0 if H > W else 0.85
    y = H - int(60 * s)
    d.text((W // 2, y), 'Turn your handwriting into a font', font=F('Regular', int(44 * s)), fill=(235, 235, 235), anchor='ms'); y -= int(76 * s)
    d.text((W // 2, y), 'เขียนลายมือแผ่นเดียว ได้ฟอนต์ของตัวเอง', font=F('SemiBold', int(56 * s)), fill=(255, 205, 90), anchor='ms'); y -= int(100 * s)
    d.text((W // 2, y), 'HandFont', font=F('Bold', int(120 * s)), fill='white', anchor='ms', stroke_width=2, stroke_fill=(0, 0, 0))
    im.convert('RGB').save(name)


make(1080, 1350, 'cover_1080x1350.png'); make(1080, 1080, 'cover_1080x1080.png')
