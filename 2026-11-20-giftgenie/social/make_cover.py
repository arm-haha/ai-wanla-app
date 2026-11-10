"""Procedural cover: left = empty-handed gift panic (BEFORE), right = ranked ideas in budget (AFTER). Illustration only — no real photos, people or brands."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np, math
G='/usr/share/fonts/truetype/sand-box/google/'
F=lambda w,s: ImageFont.truetype(G+'Kanit/Kanit-'+w+'.ttf',s,layout_engine=ImageFont.Layout.RAQM)
WINE=(59,29,42); CREAM=(248,239,230); PINK=(232,90,113); GOLD=(224,178,94)
INK=(43,26,31); AMBER=(255,196,64); TEAL=(42,157,143); WHITE=(255,255,255)

def bg(W,H,top,bot,noise,seed):
    yy=np.linspace(0,1,H)[:,None,None]; a=np.array(top)*(1-yy)+np.array(bot)*yy; a=np.repeat(a,W,axis=1)
    a+=np.random.default_rng(seed).normal(0,noise,(H,W,1))
    return Image.fromarray(np.clip(a,0,255).astype('uint8')).convert('RGBA')

def box(im,x,y,w,h,lid,body,ribbon,tilt=0,q=False):
    c=Image.new('RGBA',(w+40,h+40),(0,0,0,0)); d=ImageDraw.Draw(c)
    ox,oy=20,20
    d.rounded_rectangle([ox,oy+int(h*0.22),ox+w,oy+h], radius=8, fill=body)
    d.rounded_rectangle([ox-6,oy,ox+w+6,oy+int(h*0.28)], radius=8, fill=lid)
    d.rectangle([ox+w//2-7,oy,ox+w//2+7,oy+h], fill=ribbon)
    d.rectangle([ox,oy+int(h*0.16),ox+w,oy+int(h*0.28)], fill=ribbon)
    # bow
    d.ellipse([ox+w//2-22,oy-10,ox+w//2-2,oy+16], fill=ribbon)
    d.ellipse([ox+w//2+2,oy-10,ox+w//2+22,oy+16], fill=ribbon)
    if q:
        d.text((ox+w//2, oy+int(h*0.62)), "?", font=F('Bold', int(h*0.42)), fill=(255,255,255,200), anchor='mm')
    if tilt:
        c=c.rotate(tilt, expand=True, resample=Image.Resampling.BICUBIC)
    im.alpha_composite(c,(x,y))

def make(W,H,name):
    port=H>W; m=W//2; S=int(W*(0.20 if port else 0.17))
    left=bg(W,H,(90,40,55),(40,20,30),3,1)
    # scattered empty/confused boxes
    box(left, int(m*0.08), int(H*0.20), int(S*1.15), int(S*1.15), (180,90,100), (140,60,70), (230,190,120), -14, True)
    box(left, int(m*0.38), int(H*0.16), int(S*0.95), int(S*0.95), (120,80,100), (90,50,70), (200,160,100), 12, True)
    box(left, int(m*0.18), int(H*0.38), int(S*1.05), int(S*1.00), (160,70,90), (110,45,60), (240,210,150), -4, True)

    right=bg(W,H,(72,32,48),(36,18,28),2,2)
    rd=ImageDraw.Draw(right)
    cx=m+m//2
    pw,ph=int(m*0.84), int(H*(0.44 if port else 0.42))
    px,py=cx-pw//2, int(H*(0.16 if port else 0.18))
    rd.rounded_rectangle([px,py,px+pw,py+ph], radius=28, fill=CREAM+(255,), outline=PINK+(255,), width=5)
    rd.text((cx, py+int(S*0.28)), "งบ ฿1,500", font=F('SemiBold', int(S*0.22)), fill=WINE, anchor='mm')
    rows=[("100", "เสื้อโอเวอร์ไซส์", "FictoSoft  ·  ฿890"),
          ("100", "ชุดชงชา", "FictoTea  ·  ฿750"),
          ("90", "บัตรคาเฟ่ 2 ที่", "FictoBean  ·  ฿650")]
    y=py+int(S*0.52)
    for i,(sc,t,sub) in enumerate(rows):
        yy=y+i*int(S*0.48)
        rd.rounded_rectangle([px+18,yy,px+18+int(S*0.62),yy+int(S*0.36)], radius=14, fill=PINK+(255,))
        rd.text((px+18+int(S*0.31), yy+int(S*0.18)), sc, font=F('Bold', int(S*0.20)), fill=WHITE, anchor='mm')
        rd.text((px+28+int(S*0.68), yy+int(S*0.10)), t, font=F('SemiBold', int(S*0.16)), fill=WINE, anchor='lm')
        rd.text((px+28+int(S*0.68), yy+int(S*0.28)), sub, font=F('Regular', int(S*0.13)), fill=(90,60,70), anchor='lm')

    im=right.copy(); im.paste(left.crop((0,0,m,H)),(0,0))
    ov=Image.new('RGBA',(W,H),(0,0,0,0)); od=ImageDraw.Draw(ov); gh=int(H*0.42)
    for i in range(gh): od.line([(0,H-gh+i),(W,H-gh+i)], fill=(28,12,18,int(245*(i/gh)**1.2)))
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
    pill(m//2,chip_y,'คิดของขวัญไม่ออก',(0,0,0,150),'white',F('Medium',28),'mm')
    pill(m+m//2,chip_y,'ตอบ 5 ข้อ · ตามงบ',(255,255,255,240),WINE,F('Medium',25),'mm')
    pill(m+m//2,chip_y+70,'คะแนน 100 · ฿890',PINK+(255,),WHITE,F('SemiBold',29),'mm')
    s=1.0 if port else 0.85
    y=H-int(60*s)
    d.text((W//2,y),'5 questions + a budget → gift ideas that fit',font=F('Regular',int(36*s)),fill=(240,220,225),anchor='ms'); y-=int(76*s)
    d.text((W//2,y),'ตอบ 5 ข้อ ได้ไอเดียของขวัญตามงบ',font=F('SemiBold',int(48*s)),fill=(255,205,90),anchor='ms'); y-=int(100*s)
    d.text((W//2,y),'GiftGenie',font=F('Bold',int(110*s)),fill='white',anchor='ms',stroke_width=2,stroke_fill=(0,0,0))
    im.convert('RGB').save(name)

make(1080,1350,'cover_1080x1350.png'); make(1080,1080,'cover_1080x1080.png')
