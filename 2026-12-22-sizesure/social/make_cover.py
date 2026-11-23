"""Cover art for SizeSure — fully procedural (PIL). No real people, photos or brands; the body is a graphic silhouette.
Left = parcel with a shirt that doesn't fit + a confusing size chart (BEFORE), right = phone measuring a silhouette with a fit meter (AFTER)."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
G = '/usr/share/fonts/truetype/sand-box/google/'
K = G + 'Kanit/Kanit-'
F = lambda w, s: ImageFont.truetype(K + w + '.ttf', s, layout_engine=ImageFont.Layout.RAQM)
TAPE = (255, 200, 61)


def tshirt(d, cx, cy, w, color, outline):
    h = w * 0.95
    pts = [(cx - w * 0.22, cy - h / 2), (cx - w * 0.5, cy - h * 0.32), (cx - w * 0.38, cy - h * 0.12), (cx - w * 0.28, cy - h * 0.2),
           (cx - w * 0.28, cy + h / 2), (cx + w * 0.28, cy + h / 2), (cx + w * 0.28, cy - h * 0.2), (cx + w * 0.38, cy - h * 0.12),
           (cx + w * 0.5, cy - h * 0.32), (cx + w * 0.22, cy - h / 2), (cx + w * 0.1, cy - h * 0.42), (cx - w * 0.1, cy - h * 0.42)]
    d.polygon(pts, fill=color, outline=outline, width=4)
    d.arc([cx - w * 0.11, cy - h * 0.56, cx + w * 0.11, cy - h * 0.36], 0, 180, fill=outline, width=4)


def before(W, H):
    im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im)
    for y in range(H):
        t = y / H; d.line([(0, y), (W, y)], fill=(int(250 - 20 * t), int(222 - 30 * t), int(214 - 30 * t)))
    # open parcel box
    bx, by, bw, bh = int(W * 0.12), int(H * 0.50), int(W * 0.76), int(H * 0.26)
    d.polygon([(bx, by), (bx + bw, by), (bx + bw - 20, by + bh), (bx + 20, by + bh)], fill=(196, 150, 98), outline=(140, 100, 60))
    d.polygon([(bx, by), (bx - 40, by - 70), (bx + bw * 0.45, by - 70), (bx + bw * 0.5, by)], fill=(214, 170, 116), outline=(140, 100, 60))
    d.polygon([(bx + bw, by), (bx + bw + 40, by - 70), (bx + bw * 0.55, by - 70), (bx + bw * 0.5, by)], fill=(206, 160, 106), outline=(140, 100, 60))
    d.rectangle([bx + bw * 0.3, by + bh * 0.35, bx + bw * 0.7, by + bh * 0.62], fill=(255, 255, 255), outline=(120, 90, 60), width=2)
    d.text((bx + bw * 0.5, by + bh * 0.485), 'พัสดุ #12.12', font=F('Medium', 24), fill=(60, 50, 40), anchor='mm')
    # the shirt that came too small, sticking out of the box
    tshirt(d, int(W * 0.56), int(H * 0.47), int(W * 0.46), (255, 107, 139), (170, 50, 80))
    d.text((W * 0.56, H * 0.48), 'S', font=F('Bold', 40), fill='white', anchor='mm')
    # size chart card, tilted
    card = Image.new('RGBA', (int(W * 0.56), int(H * 0.21)), (0, 0, 0, 0)); cd = ImageDraw.Draw(card)
    cw, ch = card.size
    cd.rounded_rectangle([0, 0, cw - 1, ch - 1], 18, fill=(255, 255, 255, 250), outline=(200, 200, 210), width=2)
    cd.text((cw // 2, 30), 'ตารางไซซ์ (นิ้ว)', font=F('SemiBold', 26), fill=(40, 40, 60), anchor='mm')
    for i, (sz, ch_in) in enumerate((('S', 17), ('M', 18), ('L', 19), ('XL', 20))):
        y = 66 + i * ((ch - 80) // 4)
        cd.text((30, y), sz, font=F('Medium', 24), fill=(60, 60, 80), anchor='lm')
        cd.text((cw * 0.42, y), 'อก %d"' % ch_in, font=F('Regular', 24), fill=(60, 60, 80), anchor='lm')
    cd.text((cw - 40, ch * 0.62), '?', font=F('Bold', 70), fill=(230, 72, 77), anchor='mm')
    card = card.rotate(-8, expand=True, resample=Image.BICUBIC)
    sh = Image.new('RGBA', card.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, 70), (0, 0), card)
    x, y = int(W * 0.04), int(H * 0.14)
    im.paste(sh.filter(ImageFilter.GaussianBlur(6)), (x + 8, y + 10), sh.filter(ImageFilter.GaussianBlur(6))); im.paste(card, (x, y), card)
    for k, (qx, qy, s) in enumerate(((0.84, 0.18, 64), (0.18, 0.44, 48), (0.90, 0.40, 40))):
        d = ImageDraw.Draw(im); d.text((W * qx, H * qy), '?', font=F('Bold', s), fill=(230, 72, 77), anchor='mm')
    return im


def silhouette(d, cx, top, h, fill):
    u = h / 8.0
    d.ellipse([cx - u * 0.55, top, cx + u * 0.55, top + u * 1.1], fill=fill)                         # head
    d.rectangle([cx - u * 0.22, top + u * 1.0, cx + u * 0.22, top + u * 1.35], fill=fill)            # neck
    d.polygon([(cx - u * 1.15, top + u * 1.4), (cx + u * 1.15, top + u * 1.4), (cx + u * 0.95, top + u * 2.6),
               (cx + u * 0.72, top + u * 3.4), (cx + u * 1.0, top + u * 4.3), (cx - u * 1.0, top + u * 4.3),
               (cx - u * 0.72, top + u * 3.4), (cx - u * 0.95, top + u * 2.6)], fill=fill)            # torso
    for s in (-1, 1):
        d.polygon([(cx + s * u * 1.1, top + u * 1.45), (cx + s * u * 1.55, top + u * 3.9), (cx + s * u * 1.3, top + u * 3.95),
                   (cx + s * u * 0.92, top + u * 2.1)], fill=fill)                                    # arms
        d.polygon([(cx + s * u * 0.05, top + u * 4.2), (cx + s * u * 1.0, top + u * 4.2), (cx + s * u * 0.7, top + u * 7.8),
                   (cx + s * u * 0.25, top + u * 7.8)], fill=fill)                                    # legs
    return u


def phone(W, H):
    im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im)
    for y in range(H):
        t = y / H; d.line([(0, y), (W, y)], fill=(int(214 - 30 * t), int(236 - 30 * t), int(255 - 20 * t)))
    pw, ph = int(W * 0.82), int(H * 0.64)
    px, py = (W - pw) // 2, int(H * 0.15)
    d.rounded_rectangle([px + 10, py + 14, px + pw + 10, py + ph + 14], 50, fill=(90, 110, 150))
    d.rounded_rectangle([px, py, px + pw, py + ph], 50, fill=(25, 25, 32))
    sx, sy, sw, sh = px + 18, py + 18, pw - 36, ph - 36
    d.rounded_rectangle([sx, sy, sx + sw, sy + sh], 36, fill=(250, 250, 247))
    d.text((sx + sw // 2, sy + 44), 'SizeSure', font=F('SemiBold', 28), fill=(31, 42, 68), anchor='mm')
    fh = int(sh * 0.50); top = sy + 80; cx = sx + int(sw * 0.33)
    u = silhouette(d, cx, top, fh, (190, 200, 222))
    ly = None
    for k, (yy, wid, lab, val) in enumerate(((2.15, 1.0, 'อก', '84.6'), (3.35, 0.74, 'เอว', '68.0'), (4.1, 1.0, 'สะโพก', '93.6'))):
        y = top + u * yy
        ty = y if ly is None else max(y, ly + 66); ly = ty
        d.ellipse([cx - u * wid - 6, y - 9, cx + u * wid + 6, y + 9], outline=TAPE, width=5)
        d.line([(cx + u * wid + 6, y), (sx + sw * 0.58, y), (sx + sw * 0.62, ty)], fill=(31, 42, 68), width=2)
        d.text((sx + sw * 0.64, ty - 14), lab, font=F('Regular', 20), fill=(90, 100, 120), anchor='lm')
        d.text((sx + sw * 0.64, ty + 12), val, font=F('SemiBold', 28), fill=(31, 42, 68), anchor='lm')
    y = top + fh + 20
    d.rounded_rectangle([sx + 24, y, sx + sw - 24, y + 62], 22, fill=(34, 160, 107))
    d.text((sx + sw // 2, y + 31), 'แนะนำไซซ์ M · พอดี', font=F('SemiBold', 28), fill='white', anchor='mm')
    y += 84
    bw = sw - 60; bx = sx + 30
    segs = ((0.33, (240, 127, 29), 'คับ'), (0.34, (34, 160, 107), 'พอดี'), (0.33, (59, 130, 246), 'หลวม'))
    xx = bx
    for frac, col, lab in segs:
        d.rectangle([xx, y, xx + bw * frac, y + 18], fill=col)
        d.text((xx + bw * frac / 2, y + 40), lab, font=F('Regular', 20), fill=(80, 80, 90), anchor='mm'); xx += bw * frac
    pin = bx + bw * 0.52
    if y + 60 < sy + sh:
        d.ellipse([pin - 14, y - 5, pin + 14, y + 23], fill='white', outline=(31, 42, 68), width=4)
    return im


def make(W, H, name):
    m = W // 2
    im = Image.new('RGB', (W, H))
    im.paste(before(m, H), (0, 0)); im.paste(phone(W - m, H), (m, 0))
    ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    gh = int(H * 0.44)
    for i in range(gh):
        od.line([(0, H - gh + i), (W, H - gh + i)], fill=(14, 16, 30, int(250 * min(1, (i / gh) * 1.25) ** 1.2)))
    im = Image.alpha_composite(im.convert('RGBA'), ov); d = ImageDraw.Draw(im)
    d.rectangle([m - 2, 0, m + 2, H], fill='white')
    cy = int(H * 0.40); d.ellipse([m - 34, cy - 34, m + 34, cy + 34], fill='white', outline=(0, 0, 0, 60), width=2)
    d.text((m - 14, cy), '◀', font=F('Regular', 26), fill=(40, 40, 40), anchor='mm'); d.text((m + 14, cy), '▶', font=F('Regular', 26), fill=(40, 40, 40), anchor='mm')

    def pill(x, y, t, bg, fg, font, anchor):
        bb = d.textbbox((x, y), t, font=font, anchor=anchor); p = 14
        d.rounded_rectangle([bb[0] - p * 1.6, bb[1] - p, bb[2] + p * 1.6, bb[3] + p], radius=40, fill=bg); d.text((x, y), t, font=font, fill=fg, anchor=anchor)
    top = int(H * 0.12) if H > W else 120
    pill(m - 170, top, 'สั่งมาใส่ไม่ได้', (0, 0, 0, 175), 'white', F('SemiBold', 32), 'mm')
    pill(m + 170, top, 'รู้ไซซ์ก่อนสั่ง', (255, 196, 64, 255), (30, 20, 0), F('SemiBold', 32), 'mm')
    pill(W // 2, 52, 'AI วันละแอป · แจกฟรี / Free', (255, 255, 255, 235), (25, 25, 25), F('Medium', 32), 'mm')
    s = 1.0 if H > W else 0.85
    y = H - int(60 * s)
    d.text((W // 2, y), 'Two photos, your size before you order', font=F('Regular', int(42 * s)), fill=(235, 235, 235), anchor='ms'); y -= int(76 * s)
    d.text((W // 2, y), 'ถ่าย 2 รูป รู้ไซซ์ก่อนกดสั่ง', font=F('SemiBold', int(60 * s)), fill=(255, 205, 90), anchor='ms'); y -= int(100 * s)
    d.text((W // 2, y), 'SizeSure', font=F('Bold', int(120 * s)), fill='white', anchor='ms', stroke_width=2, stroke_fill=(0, 0, 0))
    im.convert('RGB').save(name)


make(1080, 1350, 'cover_1080x1350.png'); make(1080, 1080, 'cover_1080x1080.png')
