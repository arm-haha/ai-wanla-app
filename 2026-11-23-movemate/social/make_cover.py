"""Procedural cover: left = unlabeled messy boxes (BEFORE), right = labeled MM-B04 + find-my-item (AFTER). Illustration only — no real homes or people."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
G='/usr/share/fonts/truetype/sand-box/google/'
F=lambda w,s: ImageFont.truetype(G+'Kanit/Kanit-'+w+'.ttf',s,layout_engine=ImageFont.Layout.RAQM)
NAVY=(26,35,48); ORANGE=(249,115,22); CREAM=(247,241,229); TAPE=(245,196,81)
INK=(17,24,39); AMBER=(255,196,64); WHITE=(255,255,255); GREEN=(22,163,74)

def bg(W,H,top,bot,noise,seed):
    yy=np.linspace(0,1,H)[:,None,None]; a=np.array(top)*(1-yy)+np.array(bot)*yy; a=np.repeat(a,W,axis=1)
    a+=np.random.default_rng(seed).normal(0,noise,(H,W,1))
    return Image.fromarray(np.clip(a,0,255).astype('uint8')).convert('RGBA')

def carton(im,x,y,w,h,label=None,tilt=0,closed=True):
    c=Image.new('RGBA',(w+30,h+30),(0,0,0,0)); d=ImageDraw.Draw(c)
    ox,oy=15,15
    d.polygon([(ox,oy+int(h*0.18)),(ox+int(w*0.5),oy),(ox+w,oy+int(h*0.18)),(ox+w,oy+h),(ox,oy+h)], fill=(198,154,92,255), outline=(90,60,30,255))
    d.polygon([(ox,oy+int(h*0.18)),(ox+int(w*0.5),oy+int(h*0.32)),(ox+w,oy+int(h*0.18)),(ox+int(w*0.5),oy)], fill=(214,176,112,255))
    # tape
    d.rectangle([ox+w//2-6, oy+int(h*0.18), ox+w//2+6, oy+h], fill=TAPE+(255,))
    d.rectangle([ox, oy+int(h*0.46), ox+w, oy+int(h*0.54)], fill=TAPE+(255,))
    if label:
        lw,lh=int(w*0.72),int(h*0.28)
        lx,ly=ox+w//2-lw//2, oy+int(h*0.58)
        d.rounded_rectangle([lx,ly,lx+lw,ly+lh], radius=6, fill=CREAM+(255,), outline=ORANGE+(255,), width=3)
        d.text((lx+lw//2, ly+int(lh*0.38)), label, font=F('Bold', max(14,w//8)), fill=NAVY, anchor='mm')
        d.text((lx+lw//2, ly+int(lh*0.78)), "ห้องนอน", font=F('Medium', max(11,w//12)), fill=ORANGE, anchor='mm')
    if tilt:
        c=c.rotate(tilt, expand=True, resample=Image.Resampling.BICUBIC)
    im.alpha_composite(c,(x,y))

def make(W,H,name):
    port=H>W; m=W//2; S=int(W*(0.20 if port else 0.17))
    left=bg(W,H,(48,42,36),(24,20,18),3,1)
    carton(left, int(m*0.06), int(H*0.20), int(S*1.45), int(S*1.25), None, -12)
    carton(left, int(m*0.36), int(H*0.16), int(S*1.25), int(S*1.10), None, 10)
    carton(left, int(m*0.16), int(H*0.36), int(S*1.50), int(S*1.28), None, -3)

    right=bg(W,H,(28,38,52),(14,20,28),2,2)
    rd=ImageDraw.Draw(right)
    # labeled box
    carton(right, m+int(m*0.18), int(H*0.15), int(S*1.55), int(S*1.35), "MM-B04", 0)
    # search card
    cx=m+m//2
    pw=int(m*0.84); ph=int(S*1.15)
    px,py=cx-pw//2, int(H*(0.42 if port else 0.44))
    rd.rounded_rectangle([px,py,px+pw,py+ph], radius=22, fill=CREAM+(255,), outline=ORANGE+(255,), width=5)
    rd.text((cx, py+int(S*0.28)), 'ค้น "ที่ชาร์จ"', font=F('SemiBold', int(S*0.18)), fill=NAVY, anchor='mm')
    rd.text((cx, py+int(S*0.58)), "อยู่ใน MM-B04 · ห้องนอน", font=F('Bold', int(S*0.17)), fill=ORANGE, anchor='mm')
    rd.text((cx, py+int(S*0.88)), "ที่ชาร์จมือถือ · สาย USB", font=F('Regular', int(S*0.14)), fill=(70,80,90), anchor='mm')

    im=right.copy(); im.paste(left.crop((0,0,m,H)),(0,0))
    ov=Image.new('RGBA',(W,H),(0,0,0,0)); od=ImageDraw.Draw(ov); gh=int(H*0.42)
    for i in range(gh): od.line([(0,H-gh+i),(W,H-gh+i)], fill=(10,14,20,int(245*(i/gh)**1.2)))
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
    pill(m//2,chip_y,'กล่องไร้ป้าย ของหาย',(0,0,0,150),'white',F('Medium',26),'mm')
    pill(m+m//2,chip_y,'10 กล่อง · หาของเจอ',(255,255,255,240),NAVY,F('Medium',25),'mm')
    pill(m+m//2,chip_y+70,'ประมาณ ฿3,030',ORANGE+(255,),WHITE,F('SemiBold',29),'mm')
    s=1.0 if port else 0.85
    y=H-int(60*s)
    d.text((W//2,y),'Label every box, then find anything in seconds',font=F('Regular',int(36*s)),fill=(220,225,230),anchor='ms'); y-=int(76*s)
    d.text((W//2,y),'ย้ายบ้านไม่ป่วน ของอยู่ในกล่องไหนรู้ทันที',font=F('SemiBold',int(44*s)),fill=(255,205,90),anchor='ms'); y-=int(100*s)
    d.text((W//2,y),'MoveMate',font=F('Bold',int(110*s)),fill='white',anchor='ms',stroke_width=2,stroke_fill=(0,0,0))
    im.convert('RGB').save(name)

make(1080,1350,'cover_1080x1350.png'); make(1080,1080,'cover_1080x1080.png')
