"""Procedural cover: left = illustrated mat + dumbbells (BEFORE), right = 20-min plan card (AFTER).
Fictional illustration only — no real people or brands."""
from PIL import Image, ImageDraw, ImageFont
import numpy as np
G='/usr/share/fonts/truetype/sand-box/google/'
F=lambda w,s: ImageFont.truetype(G+'Kanit/Kanit-'+w+'.ttf',s,layout_engine=ImageFont.Layout.RAQM)
NAVY=(15,23,42); GREEN=(34,197,94); ORANGE=(249,115,22); WHITE=(255,255,255); WOOD=(180,140,90)

def bg(W,H,top,bot,noise,seed):
    yy=np.linspace(0,1,H)[:,None,None]; a=np.array(top)*(1-yy)+np.array(bot)*yy; a=np.repeat(a,W,axis=1)
    a+=np.random.default_rng(seed).normal(0,noise,(H,W,1))
    return Image.fromarray(np.clip(a,0,255).astype('uint8')).convert('RGBA')

def pill(d,x,y,t,bgc,fg,font,anchor):
    b=d.textbbox((x,y),t,font=font,anchor=anchor); p=14
    d.rounded_rectangle([b[0]-p*1.6,b[1]-p,b[2]+p*1.6,b[3]+p], radius=40, fill=bgc); d.text((x,y),t,font=font,fill=fg,anchor=anchor)

def gear(d, cx, cy, s):
    # mat
    d.rounded_rectangle([cx-int(s*1.15), cy-int(s*0.15), cx+int(s*1.15), cy+int(s*1.15)], radius=16, fill=(30,80,70), outline=GREEN, width=5)
    # two dumbbells
    for dx in (-int(s*0.45), int(s*0.45)):
        x=cx+dx; y=cy+int(s*0.45)
        d.rounded_rectangle([x-int(s*0.38), y-int(s*0.08), x+int(s*0.38), y+int(s*0.08)], radius=6, fill=WOOD, outline=NAVY, width=3)
        for sx in (-int(s*0.38), int(s*0.20)):
            d.rounded_rectangle([x+sx, y-int(s*0.22), x+sx+int(s*0.18), y+int(s*0.22)], radius=8, fill=(70,70,80), outline=NAVY, width=3)

def make(W,H,name):
    port=H>W; m=W//2; S=int(W*(0.20 if port else 0.16))
    left=bg(W,H,(15,23,42),(10,16,30),3,51)
    pw,ph=int(S*2.20), int(S*(3.15 if port else 2.95))
    px,py=m//2-pw//2, int(H*(0.15 if port else 0.17))
    ld=ImageDraw.Draw(left)
    ld.rounded_rectangle([px,py,px+pw,py+ph], radius=28, fill=(20,30,48,255), outline=(50,70,90,255), width=5)
    gear(ld, m//2, py+int(ph*0.32), int(S*0.72))
    ld.text((m//2, py+int(ph*0.88)), "เสื่อ + ดัมเบิล 4 กก.", font=F('SemiBold', int(S*0.15)), fill=WHITE, anchor='mm')

    right=bg(W,H,(6,40,30),(8,20,18),2,52)
    rd=ImageDraw.Draw(right)
    cx=m+m//2
    cw,ch=int(m*0.86), int(H*(0.46 if port else 0.40))
    x0,y0=cx-cw//2, int(H*(0.15 if port else 0.17))
    rd.rounded_rectangle([x0,y0,x0+cw,y0+ch], radius=26, fill=(8,24,24,255), outline=GREEN+(255,), width=5)
    rd.text((cx, y0+int(S*0.28)), "แผน 20 นาที", font=F('Bold', int(S*0.22)), fill=GREEN, anchor='mm')
    rd.text((cx, y0+int(S*0.52)), "beginner · 7 ท่า", font=F('Medium', int(S*0.14)), fill=WHITE, anchor='mm')
    rows=["1 เดินยกเข่า 2 นาที","2 สกวอตถือดัมเบิล","3 ดันพื้นเข่าลง","4 โรว์ดัมเบิล"]
    yy=y0+int(S*0.78)
    for i,t in enumerate(rows):
        rd.text((x0+28, yy+i*int(S*0.28)), t, font=F('Medium', int(S*0.13)), fill=WHITE, anchor='lm')
    rd.rounded_rectangle([x0+20, y0+ch-int(S*0.40)-14, x0+cw-20, y0+ch-14], radius=14, fill=ORANGE+(255,))
    rd.text((cx, y0+ch-14-int(S*0.20)), "จับเวลา 20:00", font=F('Bold', int(S*0.16)), fill=WHITE, anchor='mm')

    im=right.copy(); im.paste(left.crop((0,0,m,H)),(0,0))
    ov=Image.new('RGBA',(W,H),(0,0,0,0)); od=ImageDraw.Draw(ov); gh=int(H*0.40)
    for i in range(gh): od.line([(0,H-gh+i),(W,H-gh+i)], fill=(6,10,18,int(245*(i/gh)**1.2)))
    im=Image.alpha_composite(im,ov); d=ImageDraw.Draw(im)
    d.rectangle([m-3,0,m+3,H], fill='white')
    cy2=int(H*0.30); d.ellipse([m-34,cy2-34,m+34,cy2+34], fill='white', outline=(0,0,0,60), width=2)
    d.text((m-14,cy2),'◀',font=F('Regular',26),fill=(40,40,40),anchor='mm'); d.text((m+14,cy2),'▶',font=F('Regular',26),fill=(40,40,40),anchor='mm')
    top=int(H*0.09) if port else 100
    pill(d,m//2,top,'BEFORE',(0,0,0,170),'white',F('SemiBold',34),'mm')
    pill(d,m+m//2,top,'AFTER',(255,196,64,255),(30,20,0),F('SemiBold',34),'mm')
    pill(d,W//2,48,'AI วันละแอป · แจกฟรี / Free',(255,255,255,235),(25,25,25),F('Medium',32),'mm')
    chip_y = max(py+ph, y0+ch) + (48 if port else 38)
    pill(d,m//2,chip_y,'ของในบ้านมีแค่นี้',(0,0,0,170),'white',F('Medium',24),'mm')
    pill(d,m+m//2,chip_y,'ตาราง 20 นาทีพร้อมจับเวลา',(255,255,255,240),NAVY,F('Medium',22),'mm')
    s=1.0 if port else 0.85
    y=H-int(56*s)
    d.text((W//2,y),'Snap your gear → a 20-minute home plan',font=F('Regular',int(32*s)),fill=(200,230,210),anchor='ms'); y-=int(72*s)
    d.text((W//2,y),'ถ่ายอุปกรณ์ที่มี ได้ตารางออกกำลังที่บ้าน',font=F('SemiBold',int(40*s)),fill=(255,205,90),anchor='ms'); y-=int(92*s)
    d.text((W//2,y),'FitDeck',font=F('Bold',int(100*s)),fill='white',anchor='ms',stroke_width=2,stroke_fill=(0,0,0))
    im.convert('RGB').save(name)

make(1080,1350,'cover_1080x1350.png'); make(1080,1080,'cover_1080x1080.png')
print("covers written")
