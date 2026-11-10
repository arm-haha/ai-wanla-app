"""Procedural cover: left = messy saved screenshots (BEFORE), right = clean day-by-day trip card (AFTER). Illustration only — no real photos, people or venues."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
G='/usr/share/fonts/truetype/sand-box/google/'
F=lambda w,s: ImageFont.truetype(G+'Kanit/Kanit-'+w+'.ttf',s,layout_engine=ImageFont.Layout.RAQM)
NAVY=(15,40,64); TEAL=(20,184,166); GOLD=(245,196,81); CREAM=(247,241,229)
INK=(16,32,51); AMBER=(255,196,64); WHITE=(255,255,255)

def bg(W,H,top,bot,noise,seed):
    yy=np.linspace(0,1,H)[:,None,None]; a=np.array(top)*(1-yy)+np.array(bot)*yy; a=np.repeat(a,W,axis=1)
    a+=np.random.default_rng(seed).normal(0,noise,(H,W,1))
    return Image.fromarray(np.clip(a,0,255).astype('uint8')).convert('RGBA')

def phone_shot(im, x, y, w, h, rot, title, sub, kind, seed):
    card=Image.new('RGBA',(w,h),(0,0,0,0)); d=ImageDraw.Draw(card)
    d.rounded_rectangle([0,0,w-1,h-1], radius=22, fill=(250,250,252,255), outline=(40,50,60,255), width=4)
    d.rounded_rectangle([8,8,w-9,int(h*0.58)], radius=14, fill=(kind[0]))
    # fake map / ig pattern
    rng=np.random.default_rng(seed)
    if kind[1]=='map':
        for i in range(5):
            y1=int(h*0.12)+i*int(h*0.08)
            d.line([(20,y1),(w-20,y1+int(rng.integers(-8,8)))], fill=(180,210,200,255), width=4)
        d.ellipse([w//2-10,int(h*0.28)-16,w//2+10,int(h*0.28)+16], fill=GOLD+(255,))
        d.polygon([(w//2,int(h*0.22)),(w//2-14,int(h*0.32)),(w//2+14,int(h*0.32))], fill=(220,60,60,255))
    else:
        d.rounded_rectangle([18,18,w-18,int(h*0.50)], radius=10, fill=kind[0])
        d.ellipse([18,18,54,54], fill=(255,255,255,80))
        # landscape blocks
        d.rectangle([18,int(h*0.22),w-18,int(h*0.50)], fill=(40,80,90,180))
        d.ellipse([w//2-16,int(h*0.30),w//2+22,int(h*0.42)], fill=(255,220,140,200))
    d.text((w//2,int(h*0.70)), title, font=F('SemiBold', max(16,w//11)), fill=INK, anchor='mm')
    d.text((w//2,int(h*0.84)), sub, font=F('Regular', max(14,w//14)), fill=(80,90,100), anchor='mm')
    card=card.rotate(rot, expand=True, resample=Image.Resampling.BICUBIC)
    im.alpha_composite(card, (x, y))

def make(W,H,name):
    port=H>W; m=W//2; S=int(W*(0.20 if port else 0.17))
    # BEFORE: messy album of screenshots
    left=bg(W,H,(36,48,62),(18,24,32),3,1)
    # faint album grid
    ld=ImageDraw.Draw(left)
    shots=[
        (int(m*0.08), int(H*0.14), int(S*1.45), int(S*1.95), -16, "FictoBean", "IG · นิมมาน", ((70,140,150,255),'ig'), 1),
        (int(m*0.30), int(H*0.18), int(S*1.45), int(S*1.95), 10, "ท่าแพ", "แผนที่", ((90,150,130,255),'map'), 2),
        (int(m*0.12), int(H*0.32), int(S*1.40), int(S*1.85), -6, "ดอยสุเทพ", "แผนที่", ((80,120,140,255),'map'), 3),
    ]
    for sh in shots:
        phone_shot(left, *sh)

    # AFTER: clean trip card
    right=bg(W,H,(18,46,62),(10,24,36),2,2)
    rd=ImageDraw.Draw(right)
    cx=m+m//2
    pw,ph=int(m*0.82), int(H*(0.42 if port else 0.40))
    px,py=cx-pw//2, int(H*(0.17 if port else 0.19))
    rd.rounded_rectangle([px,py,px+pw,py+ph], radius=28, fill=CREAM+(255,), outline=TEAL+(255,), width=5)
    rd.text((cx, py+int(S*0.32)), "เชียงใหม่ · 4 วัน", font=F('SemiBold', int(S*0.22)), fill=NAVY, anchor='mm')
    days=[("วัน 1", "นิมมาน", "คาเฟ่ + ข้าวซอย"),
          ("วัน 2", "เมืองเก่า", "ท่าแพ + ไนท์บาซาร์"),
          ("วัน 3", "ดอยสุเทพ", "เข้าวัดเช้า"),
          ("วัน 4", "แม่ริม", "คาเฟ่บนเขา")]
    y=py+int(S*0.55)
    for i,(d,a,t) in enumerate(days):
        yy=y+i*int(S*0.36)
        rd.rounded_rectangle([px+22,yy,px+22+int(S*0.70),yy+int(S*0.32)], radius=12, fill=TEAL+(255,))
        rd.text((px+22+int(S*0.35), yy+int(S*0.16)), d, font=F('SemiBold', int(S*0.14)), fill=WHITE, anchor='mm')
        rd.text((px+28+int(S*0.78), yy+int(S*0.08)), a, font=F('SemiBold', int(S*0.15)), fill=NAVY, anchor='lm')
        rd.text((px+28+int(S*0.78), yy+int(S*0.24)), t, font=F('Regular', int(S*0.13)), fill=(70,80,90), anchor='lm')
    # budget bar
    by=py+ph-int(S*0.55)
    rd.rounded_rectangle([px+22,by,px+pw-22,by+int(S*0.38)], radius=14, fill=NAVY+(255,))
    rd.text((cx, by+int(S*0.19)), "งบ ~฿7,800  ·  อยู่ในงบ", font=F('SemiBold', int(S*0.16)), fill=GOLD, anchor='mm')

    im=right.copy(); im.paste(left.crop((0,0,m,H)),(0,0))
    ov=Image.new('RGBA',(W,H),(0,0,0,0)); od=ImageDraw.Draw(ov); gh=int(H*0.42)
    for i in range(gh): od.line([(0,H-gh+i),(W,H-gh+i)], fill=(8,16,24,int(245*(i/gh)**1.2)))
    im=Image.alpha_composite(im,ov); d=ImageDraw.Draw(im)
    d.rectangle([m-3,0,m+3,H], fill='white')
    cy2=int(H*0.32); d.ellipse([m-34,cy2-34,m+34,cy2+34], fill='white', outline=(0,0,0,60), width=2)
    d.text((m-14,cy2),'◀',font=F('Regular',26),fill=(40,40,40),anchor='mm'); d.text((m+14,cy2),'▶',font=F('Regular',26),fill=(40,40,40),anchor='mm')
    def pill(x,y,t,bgc,fg,font,anchor):
        b=d.textbbox((x,y),t,font=font,anchor=anchor); p=14
        d.rounded_rectangle([b[0]-p*1.6,b[1]-p,b[2]+p*1.6,b[3]+p], radius=40, fill=bgc); d.text((x,y),t,font=font,fill=fg,anchor=anchor)
    top=int(H*0.10) if port else 120
    pill(m//2,top,'BEFORE',(0,0,0,170),'white',F('SemiBold',34),'mm')
    pill(m+m//2,top,'AFTER',AMBER+(255,),(30,20,0),F('SemiBold',34),'mm')
    pill(W//2,52,'AI วันละแอป · แจกฟรี / Free',(255,255,255,235),(25,25,25),F('Medium',32),'mm')
    chip_y=int(H*(0.62 if port else 0.60))
    pill(m//2,chip_y,'แคปจอเต็มอัลบั้ม',(0,0,0,150),'white',F('Medium',28),'mm')
    pill(m+m//2,chip_y,'4 วัน · 6 จุด · สองคน',(255,255,255,240),(16,32,51),F('Medium',25),'mm')
    pill(m+m//2,chip_y+70,'อยู่ในงบ ฿7,800',TEAL+(255,),WHITE,F('SemiBold',29),'mm')
    s=1.0 if port else 0.85
    y=H-int(60*s)
    d.text((W//2,y),'Saved screenshots → a trip you can actually take',font=F('Regular',int(36*s)),fill=(220,230,235),anchor='ms'); y-=int(76*s)
    d.text((W//2,y),'แคปจอที่เซฟไว้ กลายเป็นทริปพร้อมเที่ยว',font=F('SemiBold',int(46*s)),fill=(255,205,90),anchor='ms'); y-=int(100*s)
    d.text((W//2,y),'TripStitch',font=F('Bold',int(110*s)),fill='white',anchor='ms',stroke_width=2,stroke_fill=(0,0,0))
    im.convert('RGB').save(name)

make(1080,1350,'cover_1080x1350.png'); make(1080,1080,'cover_1080x1080.png')
