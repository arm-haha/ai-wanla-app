"""Procedural cover: left = illustrated desk lamp (BEFORE), right = listing card with price (AFTER).
Fictional illustration only — no real products, logos or people."""
from PIL import Image, ImageDraw, ImageFont
import numpy as np
G='/usr/share/fonts/truetype/sand-box/google/'
F=lambda w,s: ImageFont.truetype(G+'Kanit/Kanit-'+w+'.ttf',s,layout_engine=ImageFont.Layout.RAQM)
NAVY=(31,41,55); GREEN=(22,163,74); AMBER=(245,158,11)
CREAM=(255,251,235); WHITE=(255,255,255); SHADE=(245,230,200)

def bg(W,H,top,bot,noise,seed):
    yy=np.linspace(0,1,H)[:,None,None]; a=np.array(top)*(1-yy)+np.array(bot)*yy; a=np.repeat(a,W,axis=1)
    a+=np.random.default_rng(seed).normal(0,noise,(H,W,1))
    return Image.fromarray(np.clip(a,0,255).astype('uint8')).convert('RGBA')

def pill(d,x,y,t,bgc,fg,font,anchor):
    b=d.textbbox((x,y),t,font=font,anchor=anchor); p=14
    d.rounded_rectangle([b[0]-p*1.6,b[1]-p,b[2]+p*1.6,b[3]+p], radius=40, fill=bgc); d.text((x,y),t,font=font,fill=fg,anchor=anchor)

def lamp(im, cx, cy, s):
    d=ImageDraw.Draw(im)
    # glow
    d.ellipse([cx-int(s*1.15), cy-int(s*1.35), cx+int(s*1.15), cy+int(s*0.15)], fill=(255,236,180,255))
    # shade
    d.polygon([(cx-int(s*0.95), cy-int(s*0.15)), (cx+int(s*0.95), cy-int(s*0.15)),
               (cx+int(s*0.62), cy-int(s*1.05)), (cx-int(s*0.62), cy-int(s*1.05))], fill=(232,210,170), outline=NAVY, width=4)
    # inner
    d.ellipse([cx-int(s*0.55), cy-int(s*0.28), cx+int(s*0.55), cy+int(s*0.02)], fill=(255,248,220), outline=NAVY, width=3)
    # stem
    d.rounded_rectangle([cx-int(s*0.07), cy, cx+int(s*0.07), cy+int(s*1.05)], radius=6, fill=(160,140,110), outline=NAVY, width=3)
    # base
    d.ellipse([cx-int(s*0.55), cy+int(s*0.90), cx+int(s*0.55), cy+int(s*1.22)], fill=(170,150,120), outline=NAVY, width=4)
    # tiny scratch mark on base (the demo defect)
    d.line([(cx+int(s*0.10), cy+int(s*1.02)), (cx+int(s*0.28), cy+int(s*1.08))], fill=(120,90,70), width=3)

def make(W,H,name):
    port=H>W; m=W//2; S=int(W*(0.20 if port else 0.16))
    left=bg(W,H,(255,244,220),(245,230,200),3,21)
    pw,ph=int(S*2.15), int(S*(3.15 if port else 2.95))
    px,py=m//2-pw//2, int(H*(0.15 if port else 0.17))
    ld=ImageDraw.Draw(left)
    ld.rounded_rectangle([px,py,px+pw,py+ph], radius=28, fill=(255,252,245,255), outline=(210,190,160,255), width=5)
    lamp(left, m//2, py+int(ph*0.46), int(S*0.72))
    ld.text((m//2, py+int(ph*0.88)), "โคมไฟตั้งโต๊ะ", font=F('SemiBold', int(S*0.16)), fill=NAVY, anchor='mm')

    right=bg(W,H,(236,253,245),(220,240,230),2,22)
    rd=ImageDraw.Draw(right)
    cx=m+m//2
    cw,ch=int(m*0.84), int(H*(0.46 if port else 0.40))
    x0,y0=cx-cw//2, int(H*(0.15 if port else 0.17))
    rd.rounded_rectangle([x0,y0,x0+cw,y0+ch], radius=26, fill=(255,255,255,255), outline=GREEN+(255,), width=5)
    rd.text((cx, y0+int(S*0.28)), "โคมไฟตั้งโต๊ะ สีครีม", font=F('SemiBold', int(S*0.17)), fill=NAVY, anchor='mm')
    rd.text((cx, y0+int(S*0.52)), "สภาพดี", font=F('Medium', int(S*0.15)), fill=(80,90,100), anchor='mm')
    # grade chip
    gx,gy=cx, y0+int(S*0.80)
    rd.rounded_rectangle([gx-int(S*0.55), gy-int(S*0.16), gx+int(S*0.55), gy+int(S*0.16)], radius=18, fill=AMBER+(255,))
    rd.text((gx, gy), "สภาพ B", font=F('Bold', int(S*0.16)), fill=NAVY, anchor='mm')
    rd.text((cx, y0+int(S*1.18)), "฿450–750", font=F('Bold', int(S*0.36)), fill=GREEN, anchor='mm')
    rd.text((cx, y0+int(S*1.48)), "แนะนำกลาง ฿600", font=F('Medium', int(S*0.14)), fill=(80,90,100), anchor='mm')
    rd.rounded_rectangle([x0+20, y0+ch-int(S*0.42)-16, x0+cw-20, y0+ch-16], radius=14, fill=GREEN+(255,))
    rd.text((cx, y0+ch-16-int(S*0.21)), "คัดลอกโพสต์ขาย", font=F('Bold', int(S*0.15)), fill=WHITE, anchor='mm')

    im=right.copy(); im.paste(left.crop((0,0,m,H)),(0,0))
    ov=Image.new('RGBA',(W,H),(0,0,0,0)); od=ImageDraw.Draw(ov); gh=int(H*0.40)
    for i in range(gh): od.line([(0,H-gh+i),(W,H-gh+i)], fill=(20,30,20,int(235*(i/gh)**1.2)))
    im=Image.alpha_composite(im,ov); d=ImageDraw.Draw(im)
    d.rectangle([m-3,0,m+3,H], fill='white')
    cy2=int(H*0.30); d.ellipse([m-34,cy2-34,m+34,cy2+34], fill='white', outline=(0,0,0,60), width=2)
    d.text((m-14,cy2),'◀',font=F('Regular',26),fill=(40,40,40),anchor='mm'); d.text((m+14,cy2),'▶',font=F('Regular',26),fill=(40,40,40),anchor='mm')
    top=int(H*0.09) if port else 100
    pill(d,m//2,top,'BEFORE',(0,0,0,170),'white',F('SemiBold',34),'mm')
    pill(d,m+m//2,top,'AFTER',AMBER+(255,),(30,20,0),F('SemiBold',34),'mm')
    pill(d,W//2,48,'AI วันละแอป · แจกฟรี / Free',(255,255,255,235),(25,25,25),F('Medium',32),'mm')
    chip_y = max(py+ph, y0+ch) + (48 if port else 38)
    pill(d,m//2,chip_y,'ของมือสองในบ้าน',(0,0,0,170),'white',F('Medium',24),'mm')
    pill(d,m+m//2,chip_y,'โพสต์พร้อมราคาใน 3 วิ',(255,255,255,240),NAVY,F('Medium',24),'mm')
    s=1.0 if port else 0.85
    y=H-int(56*s)
    d.text((W//2,y),'Snap it → a listing with a fair price range',font=F('Regular',int(32*s)),fill=(210,230,210),anchor='ms'); y-=int(72*s)
    d.text((W//2,y),'ถ่ายของมือสอง ได้โพสต์ขายพร้อมราคา',font=F('SemiBold',int(42*s)),fill=(255,205,90),anchor='ms'); y-=int(92*s)
    d.text((W//2,y),'SellSnap',font=F('Bold',int(100*s)),fill='white',anchor='ms',stroke_width=2,stroke_fill=(0,0,0))
    im.convert('RGB').save(name)

make(1080,1350,'cover_1080x1350.png'); make(1080,1080,'cover_1080x1080.png')
print("covers written")
