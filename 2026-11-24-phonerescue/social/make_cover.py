"""Procedural cover: left = almost-full storage (BEFORE), right = cleanup plan + free space (AFTER). Illustration only — no real devices, screens or people."""
from PIL import Image, ImageDraw, ImageFont
import numpy as np
G='/usr/share/fonts/truetype/sand-box/google/'
F=lambda w,s: ImageFont.truetype(G+'Kanit/Kanit-'+w+'.ttf',s,layout_engine=ImageFont.Layout.RAQM)
NAVY=(15,23,42); GREEN=(34,197,94); RED=(220,38,38)
AMBER=(255,196,64); WHITE=(255,255,255)

def bg(W,H,top,bot,noise,seed):
    yy=np.linspace(0,1,H)[:,None,None]; a=np.array(top)*(1-yy)+np.array(bot)*yy; a=np.repeat(a,W,axis=1)
    a+=np.random.default_rng(seed).normal(0,noise,(H,W,1))
    return Image.fromarray(np.clip(a,0,255).astype('uint8')).convert('RGBA')

def phone_frame(im, x, y, w, h, fill):
    d=ImageDraw.Draw(im)
    d.rounded_rectangle([x,y,x+w,y+h], radius=36, fill=(20,24,32,255), outline=(80,90,110,255), width=5)
    d.rounded_rectangle([x+10,y+10,x+w-10,y+h-10], radius=28, fill=fill)
    d.rounded_rectangle([x+w//2-28, y+16, x+w//2+28, y+26], radius=4, fill=(30,34,42,255))

def gauge(im, cx, cy, r, used_pct, col, label, sub):
    d=ImageDraw.Draw(im)
    d.ellipse([cx-r,cy-r,cx+r,cy+r], outline=(50,60,80,255), width=int(r*0.22))
    start=-90; end=-90+int(360*used_pct/100)
    d.arc([cx-r,cy-r,cx+r,cy+r], start, end, fill=col, width=int(r*0.22))
    d.text((cx, cy-int(r*0.08)), label, font=F('Bold', int(r*0.42)), fill=WHITE, anchor='mm')
    d.text((cx, cy+int(r*0.38)), sub, font=F('Medium', int(r*0.18)), fill=(200,210,220), anchor='mm')

def pill(d,x,y,t,bgc,fg,font,anchor):
    b=d.textbbox((x,y),t,font=font,anchor=anchor); p=14
    d.rounded_rectangle([b[0]-p*1.6,b[1]-p,b[2]+p*1.6,b[3]+p], radius=40, fill=bgc); d.text((x,y),t,font=font,fill=fg,anchor=anchor)

def make(W,H,name):
    port=H>W; m=W//2; S=int(W*(0.20 if port else 0.16))
    left=bg(W,H,(22,18,32),(10,10,16),3,1)
    pw,ph=int(S*2.15), int(S*(3.15 if port else 2.95))
    px,py=m//2-pw//2, int(H*(0.15 if port else 0.17))
    phone_frame(left, px, py, pw, ph, (16,18,28,255))
    gauge(left, m//2, py+int(ph*0.44), int(S*0.70), 99, RED, "99%", "127 / 128 GB")
    ld=ImageDraw.Draw(left)
    ld.text((m//2, py+int(ph*0.80)), "เหลือ 1 GB", font=F('SemiBold', int(S*0.20)), fill=RED, anchor='mm')

    right=bg(W,H,(12,28,28),(8,16,18),2,2)
    rd=ImageDraw.Draw(right)
    cx=m+m//2
    cw,ch=int(m*0.84), int(H*(0.42 if port else 0.36))
    x0,y0=cx-cw//2, int(H*(0.15 if port else 0.17))
    rd.rounded_rectangle([x0,y0,x0+cw,y0+ch], radius=26, fill=(8,24,24,255), outline=GREEN+(255,), width=5)
    rd.text((cx, y0+int(S*0.28)), "เก็บได้ ~16.8 GB", font=F('SemiBold', int(S*0.20)), fill=GREEN, anchor='mm')
    rows=[("รูปซ้ำ", "6.2 GB"), ("สำรองแชท", "4.0 GB"), ("แคปจอ", "3.1 GB")]
    yy=y0+int(S*0.52)
    gap=int(S*(0.36 if port else 0.32))
    for i,(t,g) in enumerate(rows):
        y=yy+i*gap
        rd.text((x0+28, y), t, font=F('Medium', int(S*0.16)), fill=WHITE, anchor='lm')
        rd.text((x0+cw-28, y), g, font=F('SemiBold', int(S*0.16)), fill=GREEN, anchor='rm')
    bar_h=int(S*0.38)
    rd.rounded_rectangle([x0+20, y0+ch-bar_h-16, x0+cw-20, y0+ch-16], radius=14, fill=GREEN+(255,))
    rd.text((cx, y0+ch-16-bar_h//2), "เหลือว่าง ~17.8 GB", font=F('Bold', int(S*0.15)), fill=NAVY, anchor='mm')

    im=right.copy(); im.paste(left.crop((0,0,m,H)),(0,0))
    ov=Image.new('RGBA',(W,H),(0,0,0,0)); od=ImageDraw.Draw(ov); gh=int(H*0.40)
    for i in range(gh): od.line([(0,H-gh+i),(W,H-gh+i)], fill=(6,10,18,int(245*(i/gh)**1.2)))
    im=Image.alpha_composite(im,ov); d=ImageDraw.Draw(im)
    d.rectangle([m-3,0,m+3,H], fill='white')
    cy2=int(H*0.30); d.ellipse([m-34,cy2-34,m+34,cy2+34], fill='white', outline=(0,0,0,60), width=2)
    d.text((m-14,cy2),'◀',font=F('Regular',26),fill=(40,40,40),anchor='mm'); d.text((m+14,cy2),'▶',font=F('Regular',26),fill=(40,40,40),anchor='mm')
    top=int(H*0.09) if port else 100
    pill(d,m//2,top,'BEFORE',(0,0,0,170),'white',F('SemiBold',34),'mm')
    pill(d,m+m//2,top,'AFTER',AMBER+(255,),(30,20,0),F('SemiBold',34),'mm')
    pill(d,W//2,48,'AI วันละแอป · แจกฟรี / Free',(255,255,255,235),(25,25,25),F('Medium',32),'mm')
    # chips sit clearly below phone / card, above the title block
    phone_bottom = py+ph
    card_bottom = y0+ch
    chip_y = max(phone_bottom, card_bottom) + (52 if port else 42)
    pill(d,m//2,chip_y,'เครื่องเต็ม · แบตไม่ถึงวัน',(0,0,0,170),'white',F('Medium',24),'mm')
    pill(d,m+m//2,chip_y,'แบต 86% ยังใช้ได้',(255,255,255,240),NAVY,F('Medium',25),'mm')
    pill(d,m+m//2,chip_y+(62 if port else 56),'เก็บข้อมูลก่อน เปลี่ยนเครื่อง',GREEN+(255,),NAVY,F('SemiBold',24),'mm')
    s=1.0 if port else 0.85
    y=H-int(56*s)
    d.text((W//2,y),'Snap your settings → a cleanup plan in seconds',font=F('Regular',int(34*s)),fill=(210,220,230),anchor='ms'); y-=int(72*s)
    d.text((W//2,y),'ถ่ายหน้าตั้งค่า รู้เลยว่าต้องทำอะไร',font=F('SemiBold',int(46*s)),fill=(255,205,90),anchor='ms'); y-=int(96*s)
    d.text((W//2,y),'PhoneRescue',font=F('Bold',int(100*s)),fill='white',anchor='ms',stroke_width=2,stroke_fill=(0,0,0))
    im.convert('RGB').save(name)

make(1080,1350,'cover_1080x1350.png'); make(1080,1080,'cover_1080x1080.png')
