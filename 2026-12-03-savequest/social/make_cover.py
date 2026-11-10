"""Procedural cover: left = nearly empty jar (BEFORE), right = jar at 42% with a Japan-trip goal (AFTER). Illustration only — no real photos, people or brands."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np, math
G='/usr/share/fonts/truetype/sand-box/google/'
F=lambda w,s: ImageFont.truetype(G+'Kanit/Kanit-'+w+'.ttf',s,layout_engine=ImageFont.Layout.RAQM)
AMBER=(255,196,64); WHITE=(255,255,255); CREAM=(248,241,227)
GOLD=(245,200,76); ORANGE=(232,119,46); INK=(26,20,35)

def bg(W,H,top,bot,noise,seed):
    yy=np.linspace(0,1,H)[:,None,None]; a=np.array(top)*(1-yy)+np.array(bot)*yy; a=np.repeat(a,W,axis=1)
    a+=np.random.default_rng(seed).normal(0,noise,(H,W,1))
    return Image.fromarray(np.clip(a,0,255).astype('uint8')).convert('RGBA')

def jar(im, cx, cy, s, fill_pct, fill_col, lid_col, glow=False):
    """Stylized glass jar with a lid and fill level 0-100."""
    layer=Image.new('RGBA', im.size, (0,0,0,0)); d=ImageDraw.Draw(layer)
    body=[cx-int(s*0.70), cy-int(s*0.55), cx+int(s*0.70), cy+int(s*1.15)]
    # glow
    if glow:
        g=Image.new('RGBA', im.size, (0,0,0,0)); gd=ImageDraw.Draw(g)
        gd.ellipse([cx-int(s*1.15), cy-int(s*0.9), cx+int(s*1.15), cy+int(s*1.35)], fill=fill_col[:3]+(55,))
        im.alpha_composite(g.filter(ImageFilter.GaussianBlur(28)))
        d=ImageDraw.Draw(layer)
    # glass body
    d.rounded_rectangle(body, radius=int(s*0.28), fill=(230,235,240,210), outline=(255,255,255,230), width=5)
    # fill from the bottom
    x0,y0,x1,y1=body
    inner=4
    h=y1-y0-inner*2
    fy1=y1-inner
    fy0=fy1-int(h*fill_pct/100)
    if fill_pct>0:
        d.rounded_rectangle([x0+inner, fy0, x1-inner, fy1], radius=int(s*0.18), fill=fill_col)
        # coins as little ellipses in the fill
        rng=np.random.default_rng(7+int(fill_pct))
        for _ in range(max(2, fill_pct//8)):
            x=int(rng.integers(x0+20, x1-20)); y=int(rng.integers(max(fy0+8,y0), fy1-8))
            r=int(s*0.07)
            d.ellipse([x-r,y-int(r*0.7),x+r,y+int(r*0.7)], fill=(255,220,90,230), outline=(200,140,30,255))
    # glass shine
    d.arc([x0+12, y0+16, x0+int(s*0.35), y0+int(s*0.90)], 200, 340, fill=(255,255,255,160), width=6)
    # neck + lid
    nw=int(s*0.55); nh=int(s*0.18)
    d.rectangle([cx-nw//2, y0-nh+6, cx+nw//2, y0+8], fill=(210,215,220,255), outline=(255,255,255,200), width=2)
    d.rounded_rectangle([cx-int(s*0.42), y0-nh-int(s*0.28), cx+int(s*0.42), y0-nh+12], radius=10, fill=lid_col, outline=(90,40,20,255), width=3)
    im.alpha_composite(layer)

def fuji(im, cx, cy, s):
    """Tiny illustrated goal 'photo' — Mount Fuji + sun, clearly a drawing."""
    card=Image.new('RGBA', im.size, (0,0,0,0)); d=ImageDraw.Draw(card)
    w,h=int(s*1.15), int(s*0.85)
    x,y=cx-w//2, cy-h//2
    d.rounded_rectangle([x,y,x+w,y+h], radius=16, fill=(186,214,232,255), outline=(255,255,255,240), width=5)
    # sun
    d.ellipse([x+int(w*0.62), y+int(h*0.10), x+int(w*0.88), y+int(h*0.42)], fill=(255,196,80,255))
    # mountain
    d.polygon([(x+8,y+h-10),(x+w//2,y+int(h*0.28)),(x+w-8,y+h-10)], fill=(70,80,110,255))
    d.polygon([(x+int(w*0.38),y+int(h*0.42)),(x+w//2,y+int(h*0.28)),(x+int(w*0.62),y+int(h*0.42))], fill=(250,250,255,255))
    im.alpha_composite(card)

def faded_goal(im, cx, cy, s):
    card=Image.new('RGBA', im.size, (0,0,0,0)); d=ImageDraw.Draw(card)
    w,h=int(s*0.95), int(s*0.70)
    x,y=cx-w//2, cy-h//2
    d.rounded_rectangle([x,y,x+w,y+h], radius=14, fill=(80,70,85,160), outline=(120,110,125,200), width=3)
    d.line([x+14,y+h-16,x+w-14,y+14], fill=(160,150,155,200), width=6)
    d.line([x+14,y+14,x+w-14,y+h-16], fill=(160,150,155,200), width=6)
    im.alpha_composite(card)

def pill(d,x,y,t,bgc,fg,font,anchor):
    b=d.textbbox((x,y),t,font=font,anchor=anchor); p=14
    d.rounded_rectangle([b[0]-p*1.6,b[1]-p,b[2]+p*1.6,b[3]+p], radius=40, fill=bgc); d.text((x,y),t,font=font,fill=fg,anchor=anchor)

def make(W,H,name):
    port=H>W; m=W//2; S=int(W*(0.20 if port else 0.17))
    # BEFORE: dim room, tiny empty jar, crossed-out goal
    left=bg(W,H,(40,32,48),(18,14,24),3,1)
    jar(left, m//2, int(H*(0.38 if port else 0.40)), int(S*0.95), 6, (180,140,80,200), (90,70,80,255), glow=False)
    faded_goal(left, m//2, int(H*(0.20 if port else 0.22)), S)

    # AFTER: warm glow, big jar 42%, fuji card
    right=bg(W,H,(58,28,22),(24,14,18),2,2)
    cx=m+m//2
    fuji(right, cx, int(H*(0.19 if port else 0.20)), int(S*1.15))
    jar(right, cx, int(H*(0.40 if port else 0.42)), int(S*1.15), 42, (232,140,50,230), (180,70,40,255), glow=True)

    im=right.copy(); im.paste(left.crop((0,0,m,H)),(0,0))
    ov=Image.new('RGBA',(W,H),(0,0,0,0)); od=ImageDraw.Draw(ov); gh=int(H*0.42)
    for i in range(gh):
        od.line([(0,H-gh+i),(W,H-gh+i)], fill=(16,10,8,int(245*(i/gh)**1.2)))
    im=Image.alpha_composite(im,ov); d=ImageDraw.Draw(im)
    d.rectangle([m-3,0,m+3,H], fill='white')
    cy2=int(H*0.32); d.ellipse([m-34,cy2-34,m+34,cy2+34], fill='white', outline=(0,0,0,60), width=2)
    d.text((m-14,cy2),'◀',font=F('Regular',26),fill=(40,40,40),anchor='mm')
    d.text((m+14,cy2),'▶',font=F('Regular',26),fill=(40,40,40),anchor='mm')
    top=int(H*0.10) if port else 120
    pill(d,m//2,top,'BEFORE',(0,0,0,170),'white',F('SemiBold',34),'mm')
    pill(d,m+m//2,top,'AFTER',AMBER+(255,),(30,20,0),F('SemiBold',34),'mm')
    pill(d,W//2,52,'AI วันละแอป · แจกฟรี / Free',(255,255,255,235),(25,25,25),F('Medium',32),'mm')
    chip_y=int(H*(0.60 if port else 0.585))
    pill(d,m//2,chip_y,'กระปุกเกือบว่าง',(0,0,0,150),'white',F('Medium',28),'mm')
    pill(d,m+m//2,chip_y,'เที่ยวญี่ปุ่น · 42%',(255,255,255,240),(40,30,10),F('Medium',26),'mm')
    pill(d,m+m//2,chip_y+70,'กระปุกโตถึง 42%',GOLD+(255,),INK,F('SemiBold',29),'mm')
    sc=1.0 if port else 0.85
    y=H-int(60*sc)
    d.text((W//2,y),'Set a goal photo, watch the jar grow',font=F('Regular',int(40*sc)),fill=(235,230,220),anchor='ms'); y-=int(76*sc)
    d.text((W//2,y),'ออมเงินแบบเกม เห็นกระปุกโต',font=F('SemiBold',int(52*sc)),fill=(255,205,90),anchor='ms'); y-=int(100*sc)
    d.text((W//2,y),'SaveQuest',font=F('Bold',int(110*sc)),fill='white',anchor='ms',stroke_width=2,stroke_fill=(0,0,0))
    im.convert('RGB').save(name)

make(1080,1350,'cover_1080x1350.png'); make(1080,1080,'cover_1080x1080.png')
print('covers written')
