"""Procedural cover: left = illustrated kitchen objects (BEFORE), right = 3-language vocab cards (AFTER).
Fictional illustration only — no real homes or children."""
from PIL import Image, ImageDraw, ImageFont
import numpy as np
G='/usr/share/fonts/truetype/sand-box/google/'
F=lambda w,s: ImageFont.truetype(G+'Kanit/Kanit-'+w+'.ttf',s,layout_engine=ImageFont.Layout.RAQM)
NAVY=(31,41,55); BLUE=(2,132,199); YELLOW=(254,249,195); WHITE=(255,255,255); STEEL=(160,170,180)

def bg(W,H,top,bot,noise,seed):
    yy=np.linspace(0,1,H)[:,None,None]; a=np.array(top)*(1-yy)+np.array(bot)*yy; a=np.repeat(a,W,axis=1)
    a+=np.random.default_rng(seed).normal(0,noise,(H,W,1))
    return Image.fromarray(np.clip(a,0,255).astype('uint8')).convert('RGBA')

def pill(d,x,y,t,bgc,fg,font,anchor):
    b=d.textbbox((x,y),t,font=font,anchor=anchor); p=14
    d.rounded_rectangle([b[0]-p*1.6,b[1]-p,b[2]+p*1.6,b[3]+p], radius=40, fill=bgc); d.text((x,y),t,font=font,fill=fg,anchor=anchor)

def kettle(d, cx, cy, s):
    d.ellipse([cx-int(s*0.55), cy-int(s*0.15), cx+int(s*0.55), cy+int(s*0.55)], fill=STEEL, outline=NAVY, width=4)
    d.rounded_rectangle([cx-int(s*0.38), cy-int(s*0.70), cx+int(s*0.38), cy], radius=8, fill=(190,198,205), outline=NAVY, width=4)
    d.polygon([(cx+int(s*0.38), cy-int(s*0.15)), (cx+int(s*0.80), cy-int(s*0.05)), (cx+int(s*0.38), cy+int(s*0.12))], fill=STEEL, outline=NAVY, width=3)
    d.arc([cx-int(s*0.85), cy-int(s*0.55), cx-int(s*0.10), cy+int(s*0.15)], 40, 220, fill=NAVY, width=5)
    d.ellipse([cx-int(s*0.12), cy-int(s*0.82), cx+int(s*0.12), cy-int(s*0.58)], outline=NAVY, width=4)

def cup(d, cx, cy, s):
    d.rounded_rectangle([cx-int(s*0.40), cy-int(s*0.35), cx+int(s*0.40), cy+int(s*0.45)], radius=10, fill=(255,245,230), outline=NAVY, width=4)
    d.arc([cx+int(s*0.25), cy-int(s*0.15), cx+int(s*0.70), cy+int(s*0.30)], 270, 90, fill=NAVY, width=5)

def spoon(d, cx, cy, s):
    d.ellipse([cx-int(s*0.28), cy-int(s*0.55), cx+int(s*0.28), cy+int(s*0.05)], fill=(210,215,220), outline=NAVY, width=3)
    d.rounded_rectangle([cx-int(s*0.07), cy, cx+int(s*0.07), cy+int(s*0.70)], radius=6, fill=(210,215,220), outline=NAVY, width=3)

def make(W,H,name):
    port=H>W; m=W//2; S=int(W*(0.20 if port else 0.16))
    left=bg(W,H,(255,251,230),(254,240,200),3,41)
    pw,ph=int(S*2.20), int(S*(3.15 if port else 2.95))
    px,py=m//2-pw//2, int(H*(0.15 if port else 0.17))
    ld=ImageDraw.Draw(left)
    ld.rounded_rectangle([px,py,px+pw,py+ph], radius=28, fill=(255,252,245,255), outline=(210,180,120,255), width=5)
    # table
    ld.rounded_rectangle([px+16, py+int(ph*0.62), px+pw-16, py+ph-20], radius=8, fill=(230,200,150,255))
    kettle(ld, m//2, py+int(ph*0.38), int(S*0.70))
    cup(ld, m//2-int(S*0.70), py+int(ph*0.58), int(S*0.38))
    spoon(ld, m//2+int(S*0.70), py+int(ph*0.55), int(S*0.38))
    ld.text((m//2, py+int(ph*0.90)), "ของในครัว", font=F('SemiBold', int(S*0.16)), fill=NAVY, anchor='mm')

    right=bg(W,H,(219,234,254),(186,230,253),2,42)
    rd=ImageDraw.Draw(right)
    cx=m+m//2
    cw,ch=int(m*0.86), int(H*(0.46 if port else 0.40))
    x0,y0=cx-cw//2, int(H*(0.15 if port else 0.17))
    rd.rounded_rectangle([x0,y0,x0+cw,y0+ch], radius=26, fill=WHITE+(255,), outline=BLUE+(255,), width=5)
    rows=[("กาต้มน้ำ","kettle","水壶"),("แก้ว","cup","杯子"),("ช้อน","spoon","勺子")]
    gap=int(ch/3)
    for i,(th,en,zh) in enumerate(rows):
        y=y0+int(gap*(i+0.5))
        rd.text((x0+24, y-int(S*0.12)), th, font=F('SemiBold', int(S*0.15)), fill=NAVY, anchor='lm')
        rd.text((x0+24, y+int(S*0.12)), f"{en} · {zh}", font=F('Medium', int(S*0.13)), fill=BLUE, anchor='lm')
        if i<2:
            rd.line([(x0+18, y0+(i+1)*gap),(x0+cw-18, y0+(i+1)*gap)], fill=(230,240,250), width=2)

    im=right.copy(); im.paste(left.crop((0,0,m,H)),(0,0))
    ov=Image.new('RGBA',(W,H),(0,0,0,0)); od=ImageDraw.Draw(ov); gh=int(H*0.40)
    for i in range(gh): od.line([(0,H-gh+i),(W,H-gh+i)], fill=(20,40,60,int(235*(i/gh)**1.2)))
    im=Image.alpha_composite(im,ov); d=ImageDraw.Draw(im)
    d.rectangle([m-3,0,m+3,H], fill='white')
    cy2=int(H*0.30); d.ellipse([m-34,cy2-34,m+34,cy2+34], fill='white', outline=(0,0,0,60), width=2)
    d.text((m-14,cy2),'◀',font=F('Regular',26),fill=(40,40,40),anchor='mm'); d.text((m+14,cy2),'▶',font=F('Regular',26),fill=(40,40,40),anchor='mm')
    top=int(H*0.09) if port else 100
    pill(d,m//2,top,'BEFORE',(0,0,0,170),'white',F('SemiBold',34),'mm')
    pill(d,m+m//2,top,'AFTER',(251,191,36,255),(30,20,0),F('SemiBold',34),'mm')
    pill(d,W//2,48,'AI วันละแอป · แจกฟรี / Free',(255,255,255,235),(25,25,25),F('Medium',32),'mm')
    chip_y = max(py+ph, y0+ch) + (48 if port else 38)
    pill(d,m//2,chip_y,'ถ่ายของ ไม่ถ่ายหน้าเด็ก',(0,0,0,170),'white',F('Medium',22),'mm')
    pill(d,m+m//2,chip_y,'ไทย · อังกฤษ · จีน + ควิซ',(255,255,255,240),NAVY,F('Medium',22),'mm')
    s=1.0 if port else 0.85
    y=H-int(56*s)
    d.text((W//2,y),'Snap household objects → English & Chinese words',font=F('Regular',int(30*s)),fill=(210,230,245),anchor='ms'); y-=int(72*s)
    d.text((W//2,y),'ถ่ายของรอบบ้าน ได้คำศัพท์ให้ลูก',font=F('SemiBold',int(42*s)),fill=(255,205,90),anchor='ms'); y-=int(92*s)
    d.text((W//2,y),'SnapLingo',font=F('Bold',int(100*s)),fill='white',anchor='ms',stroke_width=2,stroke_fill=(0,0,0))
    im.convert('RGB').save(name)

make(1080,1350,'cover_1080x1350.png'); make(1080,1080,'cover_1080x1080.png')
print("covers written")
