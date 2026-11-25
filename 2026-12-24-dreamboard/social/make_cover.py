"""Cover art for DreamBoard — fully procedural (PIL). No real people, photos or brands.
Left = last year's New Year resolutions on a crumpled sticky note, crossed out and forgotten (BEFORE),
right = the same goals as a glowing lock-screen vision board with progress rings on a phone (AFTER)."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math, random
G = '/usr/share/fonts/truetype/sand-box/google/'
K = G + 'Kanit/Kanit-'
F = lambda w, s: ImageFont.truetype(K + w + '.ttf', s, layout_engine=ImageFont.Layout.RAQM)
try:
    HAND = lambda s: ImageFont.truetype(G + 'Mali/Mali-Medium.ttf', s, layout_engine=ImageFont.Layout.RAQM)
    HAND(10)
except OSError:
    HAND = lambda s: F('Light', s)
GOALS = [("เก็บเงิน 60,000", "฿", (255, 196, 64), 38), ("ลด 6 กก.", "♥", (46, 196, 182), 92),
         ("อ่าน 24 เล่ม", "✎", (91, 141, 239), 25), ("วิ่ง 300 กม.", "➶", (255, 140, 66), 55), ("พาแม่เที่ยว 4 ทริป", "✈", (255, 107, 139), 25)]


def before(W, H):
    im = Image.new('RGBA', (W, H)); d = ImageDraw.Draw(im)
    for y in range(H):
        t = y / H; d.line([(0, y), (W, y)], fill=(int(120 - 40 * t), int(110 - 40 * t), int(120 - 30 * t), 255))
    rnd = random.Random(3)
    for _ in range(900):                                                     # desk texture
        x, y = rnd.randint(0, W), rnd.randint(0, H); c = rnd.randint(-12, 12)
        d.point((x, y), fill=(110 + c, 100 + c, 110 + c, 255))
    pw, ph = int(W * 0.80), int(W * 0.92)
    note = Image.new('RGBA', (pw, ph), (255, 236, 140, 255)); nd = ImageDraw.Draw(note)
    for k in range(9):                                                       # crumple creases
        x0 = rnd.uniform(0, pw); nd.line([(x0, 0), (x0 + rnd.uniform(-80, 80), ph)], fill=(235, 210, 110, 255), width=2)
    nd.text((28, 40), 'ปีใหม่นี้จะ…', font=HAND(40), fill=(60, 50, 40), anchor='lm')
    ys = 108
    for g, _, _, _ in GOALS:
        nd.ellipse([36, ys - 5, 46, ys + 5], fill=(70, 60, 50))
        nd.text((58, ys), g, font=HAND(30), fill=(70, 60, 50), anchor='lm')
        bb = nd.textbbox((58, ys), g, font=HAND(30), anchor='lm')
        nd.line([(bb[0] - 4, ys + 2), (bb[2] + 6, ys - 4)], fill=(200, 40, 40, 255), width=4)
        ys += 62
    nd.text((pw - 30, ph - 46), 'ก.พ. … ลืมแล้ว', font=HAND(30), fill=(200, 40, 40), anchor='rm')
    note = note.rotate(-7, expand=True, resample=Image.BICUBIC)
    sh = Image.new('RGBA', note.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, 90), (0, 0), note)
    x, y = (W - note.size[0]) // 2, int(H * 0.20)
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)), (x + 12, y + 16)); im.alpha_composite(note, (x, y))
    d = ImageDraw.Draw(im)
    d.rectangle([x + note.size[0] // 2 - 50, y - 8, x + note.size[0] // 2 + 50, y + 26], fill=(230, 230, 220, 200))   # tape
    return im.convert('RGB')


def ring(d, cx, cy, r, pct, col, w=10):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255, 70), width=w)
    d.arc([cx - r, cy - r, cx + r, cy + r], -90, -90 + 360 * pct / 100, fill=col + (255,), width=w)


def after(W, H):
    im = Image.new('RGBA', (W, H)); d = ImageDraw.Draw(im)
    for y in range(H):
        t = y / H; d.line([(0, y), (W, y)], fill=(int(40 + 30 * t), int(24 + 10 * t), int(80 + 20 * t), 255))
    rnd = random.Random(11)
    for _ in range(70):                                                      # sparkles / fireworks dots
        x, y, r = rnd.uniform(0, W), rnd.uniform(0, H * 0.5), rnd.uniform(1, 3.2)
        d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 230, 160, rnd.randint(120, 255)))
    pw = int(W * 0.78); ph = int(pw * 2.05); px, py = (W - pw) // 2, int(H * 0.15)
    phone = Image.new('RGBA', (pw, ph), (0, 0, 0, 0)); pd = ImageDraw.Draw(phone)
    pd.rounded_rectangle([0, 0, pw - 1, ph - 1], 54, fill=(18, 18, 24, 255))
    sw, sh_ = pw - 24, ph - 24
    scr = Image.new('RGBA', (sw, sh_)); sd = ImageDraw.Draw(scr)
    for y in range(sh_):
        t = y / sh_; sd.line([(0, y), (sw, y)], fill=(int(255 - 60 * t), int(150 - 70 * t), int(98 + 40 * t), 255))
    sd.rounded_rectangle([sw // 2 - 50, 14, sw // 2 + 50, 40], 14, fill=(0, 0, 0, 255))      # notch
    sd.text((sw // 2, 92), 'วันศุกร์ 1 มกราคม', font=F('Medium', 22), fill=(255, 255, 255), anchor='mm')
    sd.text((sw // 2, 156), '00:01', font=F('SemiBold', 84), fill=(255, 255, 255), anchor='mm')
    sd.text((sw // 2, 222), 'คำประจำปี: แข็งแรง', font=F('Medium', 20), fill=(255, 245, 200), anchor='mm')
    m, gap = 16, 12; tw = (sw - 2 * m - gap) // 2; th = 120; y0 = 256
    glow = Image.new('RGBA', (sw, sh_), (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
    for i, (g, ic, col, p) in enumerate(GOALS):
        r_, c_ = divmod(i, 2); w = tw if i < 4 else sw - 2 * m
        x = m + c_ * (tw + gap); y = y0 + r_ * (th + gap)
        if p >= 50: gd.rounded_rectangle([x - 6, y - 6, x + w + 6, y + th + 6], 26, fill=col + (150,))
    scr.alpha_composite(glow.filter(ImageFilter.GaussianBlur(9)))
    sd = ImageDraw.Draw(scr)
    for i, (g, ic, col, p) in enumerate(GOALS):
        r_, c_ = divmod(i, 2); w = tw if i < 4 else sw - 2 * m
        x = m + c_ * (tw + gap); y = y0 + r_ * (th + gap)
        sd.rounded_rectangle([x, y, x + w, y + th], 22, fill=(255, 255, 255, 215 if p >= 50 else 150))
        ring(sd, x + 40, y + 46, 25, p, col, 7)
        sd.text((x + 40, y + 46), '%d%%' % p, font=F('SemiBold', 15), fill=(40, 30, 60), anchor='mm')
        sd.text((x + 76, y + 46), g if i == 4 else g.split(' ')[0], font=F('SemiBold', 19), fill=(40, 30, 60), anchor='lm')
        if i < 4: sd.text((x + 76, y + 74), ' '.join(g.split(' ')[1:]), font=F('Regular', 17), fill=(80, 70, 100), anchor='lm')
        sd.rounded_rectangle([x + 14, y + th - 22, x + w - 14, y + th - 12], 5, fill=(0, 0, 0, 30))
        sd.rounded_rectangle([x + 14, y + th - 22, x + 14 + (w - 28) * p / 100, y + th - 12], 5, fill=col + (255,))
    sd.text((sw // 2, sh_ - 40), 'สัปดาห์นี้: เก็บ 1,150 บาท · อ่าน 17 หน้า/วัน', font=F('Regular', 17), fill=(255, 255, 255), anchor='mm')
    mask = Image.new('L', (sw, sh_), 0); ImageDraw.Draw(mask).rounded_rectangle([0, 0, sw - 1, sh_ - 1], 44, fill=255)
    phone.paste(scr, (12, 12), mask)
    shadow = Image.new('RGBA', phone.size, (0, 0, 0, 0)); shadow.paste((0, 0, 0, 120), (0, 0), phone)
    im.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(14)), (px + 10, py + 16)); im.alpha_composite(phone, (px, py))
    return im.convert('RGB')


def make(W, H, name):
    m = W // 2
    im = Image.new('RGB', (W, H))
    im.paste(before(m, H), (0, 0)); im.paste(after(W - m, H), (m, 0))
    ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    gh = int(H * 0.36)
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
    pill(m - 170, top, 'เป้าปีใหม่ที่ลืม', (0, 0, 0, 175), 'white', F('SemiBold', 32), 'mm')
    pill(m + 170, top, 'บอร์ดที่ทำได้จริง', (255, 196, 64, 255), (30, 20, 0), F('SemiBold', 32), 'mm')
    pill(W // 2, 52, 'AI วันละแอป · แจกฟรี / Free', (255, 255, 255, 235), (25, 25, 25), F('Medium', 32), 'mm')
    s = 1.0 if H > W else 0.85
    y = H - int(60 * s)
    d.text((W // 2, y), 'New Year goals that light up your lock screen', font=F('Regular', int(40 * s)), fill=(235, 235, 235), anchor='ms'); y -= int(76 * s)
    d.text((W // 2, y), 'เป้าปีใหม่ กลายเป็นวอลล์ที่พาไปถึงจริง', font=F('SemiBold', int(58 * s)), fill=(255, 205, 90), anchor='ms'); y -= int(100 * s)
    d.text((W // 2, y), 'DreamBoard', font=F('Bold', int(120 * s)), fill='white', anchor='ms', stroke_width=2, stroke_fill=(0, 0, 0))
    im.convert('RGB').save(name)


make(1080, 1350, 'cover_1080x1350.png'); make(1080, 1080, 'cover_1080x1080.png')
