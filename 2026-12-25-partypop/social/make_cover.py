"""Cover art for PartyPop — fully procedural (PIL). No real people, photos or brands.
Left = an ordinary, plain living room on a weekday night (BEFORE),
right = the same room decorated for a New Year countdown party: garland, balloons, fairy lights,
foil "2027" balloons, a tinsel photo corner and a suki table (AFTER), with a budget chip."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math, random
G = '/usr/share/fonts/truetype/sand-box/google/'
K = G + 'Kanit/Kanit-'
F = lambda w, s: ImageFont.truetype(K + w + '.ttf', s, layout_engine=ImageFont.Layout.RAQM)


def room(W, H, night=False):
    """Shared geometry: back wall, floor, window, sofa, low table, so before/after match."""
    im = Image.new('RGBA', (W, H)); d = ImageDraw.Draw(im)
    fy = int(H * 0.66)                                                       # floor line
    for y in range(fy):
        t = y / fy
        c = (int(70 + 30 * t), int(58 + 26 * t), int(96 + 20 * t)) if night else (int(214 - 20 * t), int(206 - 20 * t), int(192 - 20 * t))
        d.line([(0, y), (W, y)], fill=c + (255,))
    for y in range(fy, H):
        t = (y - fy) / (H - fy)
        c = (int(88 - 30 * t), int(62 - 22 * t), int(52 - 18 * t)) if night else (int(168 - 40 * t), int(134 - 34 * t), int(100 - 28 * t))
        d.line([(0, y), (W, y)], fill=c + (255,))
    for k in range(-6, 14):                                                  # floor planks
        x0 = W / 2 + k * W * 0.11
        d.line([(W / 2 + (x0 - W / 2) * 0.35, fy), (x0 + (x0 - W / 2) * 0.9, H)], fill=(0, 0, 0, 28), width=2)
    wx0, wy0, wx1, wy1 = int(W * 0.60), int(H * 0.16), int(W * 0.90), int(H * 0.42)   # window
    d.rectangle([wx0 - 8, wy0 - 8, wx1 + 8, wy1 + 8], fill=(240, 236, 228, 255) if not night else (60, 50, 80, 255))
    for y in range(wy0, wy1):
        t = (y - wy0) / (wy1 - wy0)
        c = (int(20 + 20 * t), int(22 + 18 * t), int(60 + 30 * t)) if night else (int(170 + 30 * t), int(200 + 20 * t), int(230))
        d.line([(wx0, y), (wx1, y)], fill=c + (255,))
    d.line([((wx0 + wx1) // 2, wy0), ((wx0 + wx1) // 2, wy1)], fill=(240, 236, 228, 255) if not night else (60, 50, 80, 255), width=8)
    sx0, sy0, sx1, sy1 = int(W * 0.06), int(H * 0.50), int(W * 0.56), int(H * 0.72)  # sofa
    sofa = (120, 128, 140) if not night else (70, 80, 120)
    d.rounded_rectangle([sx0, sy0, sx1, sy1 - int(H * 0.06)], 26, fill=sofa + (255,))
    d.rounded_rectangle([sx0 - 14, sy0 + int(H * 0.06), sx0 + 40, sy1], 18, fill=tuple(c - 18 for c in sofa) + (255,))
    d.rounded_rectangle([sx1 - 40, sy0 + int(H * 0.06), sx1 + 14, sy1], 18, fill=tuple(c - 18 for c in sofa) + (255,))
    d.rounded_rectangle([sx0 + 30, sy0 + int(H * 0.09), sx1 - 30, sy1], 16, fill=tuple(c + 14 for c in sofa) + (255,))
    tx0, ty0, tx1, ty1 = int(W * 0.18), int(H * 0.78), int(W * 0.82), int(H * 0.84)   # low table
    return im, (fy, (wx0, wy0, wx1, wy1), (sx0, sy0, sx1, sy1), (tx0, ty0, tx1, ty1))


def before(W, H):
    im, (fy, win, sofa, tab) = room(W, H)
    d = ImageDraw.Draw(im)
    tx0, ty0, tx1, ty1 = tab
    d.rectangle([tx0, ty0, tx1, ty1], fill=(150, 112, 80, 255)); d.rectangle([tx0 + 10, ty1, tx0 + 24, ty1 + 50], fill=(120, 88, 60, 255))
    d.rectangle([tx1 - 24, ty1, tx1 - 10, ty1 + 50], fill=(120, 88, 60, 255))
    d.rounded_rectangle([tx0 + 40, ty0 - 22, tx0 + 100, ty0], 6, fill=(230, 230, 230, 255))     # lonely remote / mug
    d.ellipse([tx1 - 110, ty0 - 30, tx1 - 70, ty0 + 2], fill=(240, 240, 240, 255))
    ov = Image.new('RGBA', (W, H), (40, 40, 60, 60)); im.alpha_composite(ov)
    return im.convert('RGB')


def balloon(d, x, y, r, col):
    d.line([(x, y + r * 1.15), (x + 6, y + r * 3.2)], fill=(255, 255, 255, 140), width=2)
    d.ellipse([x - r, y - r * 1.15, x + r, y + r * 1.15], fill=col + (255,))
    d.ellipse([x - r * 0.45, y - r * 0.8, x - r * 0.1, y - r * 0.35], fill=(255, 255, 255, 110))


def after(W, H):
    im, (fy, win, sofa, tab) = room(W, H, night=True)
    rnd = random.Random(7)
    glow = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
    d = ImageDraw.Draw(im)
    wx0, wy0, wx1, wy1 = win
    for _ in range(18):                                                      # fireworks outside the window
        cx, cy = rnd.uniform(wx0 + 20, wx1 - 20), rnd.uniform(wy0 + 20, wy1 - 30); col = rnd.choice([(255, 196, 64), (255, 107, 139), (120, 220, 255)])
        for a in range(0, 360, 30):
            r = rnd.uniform(10, 22)
            d.line([(cx, cy), (cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a)))], fill=col + (200,), width=2)
    # fairy lights: two sagging strings
    for k, yb in enumerate((int(H * 0.08), int(H * 0.13))):
        pts = [(x, yb + 26 * math.sin(math.pi * x / W * 2)) for x in range(0, W + 1, 8)]
        d.line(pts, fill=(60, 50, 40, 255), width=2)
        for i, (x, y) in enumerate(pts[::4]):
            col = [(255, 210, 90), (255, 120, 150), (130, 220, 255)][(i + k) % 3]
            gd.ellipse([x - 12, y - 12, x + 12, y + 12], fill=col + (180,)); d.ellipse([x - 5, y - 5, x + 5, y + 5], fill=col + (255,))
    # garland pennants with HAPPY NEW YEAR
    word = 'HAPPY NEW YEAR'; n = len(word); y0 = int(H * 0.19)
    for i, ch in enumerate(word):
        x = int(W * 0.05) + i * (W * 0.9) / n; sag = 18 * math.sin(math.pi * i / (n - 1))
        col = [(255, 196, 64), (30, 24, 60), (255, 107, 139)][i % 3]
        d.polygon([(x, y0 + sag), (x + W * 0.9 / n - 4, y0 + sag), (x + W * 0.45 / n - 2, y0 + sag + 48)], fill=col + (255,))
        if ch != ' ':
            d.text((x + W * 0.45 / n - 2, y0 + sag + 16), ch, font=F('Bold', 20), fill=(255, 255, 255) if col != (255, 196, 64) else (30, 24, 60), anchor='mm')
    d.line([(int(W * 0.05), y0), (int(W * 0.95), y0)], fill=(240, 220, 160, 255), width=2)
    # tinsel photo corner (left wall)
    bx0, by0, bx1, by1 = int(W * 0.12), int(H * 0.27), int(W * 0.52), int(H * 0.50)
    d.rectangle([bx0, by0, bx1, by1], fill=(40, 26, 70, 255))
    for x in range(bx0, bx1, 9):
        c = rnd.choice([(255, 210, 90), (240, 180, 60), (255, 230, 150), (255, 140, 170)])
        d.line([(x, by0), (x + rnd.randint(-3, 3), by1)], fill=c + (150,), width=2)
        gd.line([(x, by0), (x, by1)], fill=c + (60,), width=4)
    # foil 2027
    for i, ch in enumerate('2027'):
        x = bx0 + 34 + i * (bx1 - bx0 - 40) / 4 + 6
        d.text((x + 4, int(H * 0.385) + 4), ch, font=F('Bold', int(W * 0.13)), fill=(20, 10, 30), anchor='mm')
        d.text((x, int(H * 0.385)), ch, font=F('Bold', int(W * 0.13)), fill=(255, 205, 80), anchor='mm', stroke_width=3, stroke_fill=(255, 240, 190))
    # balloons clusters
    for (x, y, r, col) in [(W * 0.88, H * 0.50, 30, (255, 196, 64)), (W * 0.80, H * 0.55, 26, (255, 107, 139)), (W * 0.93, H * 0.58, 24, (30, 24, 60)),
                           (W * 0.48, H * 0.47, 22, (255, 196, 64)), (W * 0.55, H * 0.43, 20, (255, 255, 255))]:
        balloon(d, x, y, r, col)
    # suki table with gold tablecloth
    tx0, ty0, tx1, ty1 = tab
    d.rectangle([tx0 - 10, ty0, tx1 + 10, ty1 + 30], fill=(214, 168, 60, 255))
    for x in range(tx0 - 10, tx1 + 10, 18):
        d.polygon([(x, ty1 + 30), (x + 18, ty1 + 30), (x + 9, ty1 + 44)], fill=(214, 168, 60, 255))
    px = (tx0 + tx1) // 2
    d.ellipse([px - 60, ty0 - 34, px + 60, ty0 + 6], fill=(70, 70, 80, 255)); d.ellipse([px - 52, ty0 - 30, px + 52, ty0 - 2], fill=(200, 90, 50, 255))
    for k in range(3):                                                       # steam
        sx = px - 24 + k * 24
        d.line([(sx, ty0 - 40), (sx + 8, ty0 - 62), (sx - 4, ty0 - 84)], fill=(255, 255, 255, 120), width=3)
    for k, col in enumerate([(240, 120, 120), (120, 200, 120), (250, 220, 160), (240, 160, 200)]):
        x = tx0 + 20 + k * 40 if k < 2 else tx1 - 20 - (k - 2) * 40
        d.ellipse([x - 18, ty0 - 16, x + 18, ty0 + 2], fill=(250, 250, 250, 255)); d.ellipse([x - 12, ty0 - 13, x + 12, ty0 - 2], fill=col + (255,))
    # confetti
    for _ in range(140):
        x, y = rnd.uniform(0, W), rnd.uniform(H * 0.2, H)
        d.rectangle([x, y, x + rnd.uniform(4, 9), y + rnd.uniform(2, 5)], fill=rnd.choice([(255, 196, 64), (255, 107, 139), (130, 220, 255), (255, 255, 255)]) + (220,))
    im.alpha_composite(glow.filter(ImageFilter.GaussianBlur(10)))
    warm = Image.new('RGBA', (W, H), (255, 170, 80, 26)); im.alpha_composite(warm)
    return im.convert('RGB')


def make(W, H, name):
    m = W // 2
    im = Image.new('RGB', (W, H))
    im.paste(before(m, H), (0, 0)); im.paste(after(W - m, H), (m, 0))
    ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    gh = int(H * 0.36)
    for i in range(gh):
        od.line([(0, H - gh + i), (W, H - gh + i)], fill=(20, 14, 40, int(250 * min(1, (i / gh) * 1.25) ** 1.2)))
    im = Image.alpha_composite(im.convert('RGBA'), ov); d = ImageDraw.Draw(im)
    d.rectangle([m - 2, 0, m + 2, H], fill='white')
    cy = int(H * 0.40); d.ellipse([m - 34, cy - 34, m + 34, cy + 34], fill='white', outline=(0, 0, 0, 60), width=2)
    d.text((m - 14, cy), '◀', font=F('Regular', 26), fill=(40, 40, 40), anchor='mm'); d.text((m + 14, cy), '▶', font=F('Regular', 26), fill=(40, 40, 40), anchor='mm')

    def pill(x, y, t, bg, fg, font, anchor):
        bb = d.textbbox((x, y), t, font=font, anchor=anchor); p = 14
        d.rounded_rectangle([bb[0] - p * 1.6, bb[1] - p, bb[2] + p * 1.6, bb[3] + p], radius=40, fill=bg); d.text((x, y), t, font=font, fill=fg, anchor=anchor)
    top = int(H * 0.115) if H > W else 118
    pill(m - 170, top, 'ห้องเดิม ๆ', (0, 0, 0, 175), 'white', F('SemiBold', 32), 'mm')
    pill(m + 170, top, 'ปาร์ตี้ปีใหม่!', (255, 196, 64, 255), (30, 20, 0), F('SemiBold', 32), 'mm')
    pill(W // 2, 52, 'AI วันละแอป · แจกฟรี / Free', (255, 255, 255, 235), (25, 25, 25), F('Medium', 32), 'mm')
    s = 1.0 if H > W else 0.85
    chip_y = int(H * 0.585) if H > W else int(H * 0.55)
    pill(W - 190, chip_y, '12 คน · งบ 4,000 ฿ · ครบ', (255, 255, 255, 235), (40, 30, 60), F('SemiBold', int(26 * s)), 'mm')
    y = H - int(60 * s)
    d.text((W // 2, y), 'Snap your room, see the party before you buy a thing', font=F('Regular', int(38 * s)), fill=(235, 235, 235), anchor='ms'); y -= int(76 * s)
    d.text((W // 2, y), 'ถ่ายห้อง 1 รูป เห็นปาร์ตี้ปีใหม่ ครบในงบ', font=F('SemiBold', int(58 * s)), fill=(255, 205, 90), anchor='ms'); y -= int(100 * s)
    d.text((W // 2, y), 'PartyPop', font=F('Bold', int(120 * s)), fill='white', anchor='ms', stroke_width=2, stroke_fill=(0, 0, 0))
    im.convert('RGB').save(name)


make(1080, 1350, 'cover_1080x1350.png'); make(1080, 1080, 'cover_1080x1080.png')
