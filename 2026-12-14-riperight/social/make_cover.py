"""Procedural cover: left = a hard, pale avocado cut too early + guessing chat (BEFORE), right = ripe mango under a 0–100 ripeness meter + chips (AFTER). Illustration only — no real people or brands."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np, math
G='/usr/share/fonts/truetype/sand-box/google/'
F=lambda w,s: ImageFont.truetype(G+'Kanit/Kanit-'+w+'.ttf',s,layout_engine=ImageFont.Layout.RAQM)
GREEN=(107,191,89); YEL=(255,201,60); ORANGE=(255,138,61); BROWN=(139,90,43); INK=(43,33,64); WHITE=(255,255,255)

def bg(W,H,top,bot,noise,seed):
    yy=np.linspace(0,1,H)[:,None,None]; a=np.array(top)*(1-yy)+np.array(bot)*yy; a=np.repeat(a,W,axis=1)
    a+=np.random.default_rng(seed).normal(0,noise,(H,W,1))
    return Image.fromarray(np.clip(a,0,255).astype('uint8')).convert('RGBA')

def pill(d,x,y,t,bgc,fg,font,anchor):
    b=d.textbbox((x,y),t,font=font,anchor=anchor); p=14
    d.rounded_rectangle([b[0]-p*1.6,b[1]-p,b[2]+p*1.6,b[3]+p], radius=40, fill=bgc); d.text((x,y),t,font=font,fill=fg,anchor=anchor)

def bubbles(im,cx,top,w,S):
    d=ImageDraw.Draw(im); y=top; f=F('Regular',int(S*0.15))
    for t in ("ลูกนี้สุกยัง?","ผ่าแล้วแข็งโป๊ก","ซื้อมา ฿110 ทิ้งอีกแล้ว"):
        b=d.textbbox((0,0),t,font=f); tw=b[2]-b[0]; th=b[3]-b[1]
        x0=cx-w//2+10; d.rounded_rectangle([x0,y,x0+tw+44,y+th+40],radius=26,fill=(255,255,255,235))
        d.text((x0+22,y+20+th//2),t,font=f,fill=INK,anchor='lm'); y+=th+62
    return y

def avocado_half(im,cx,cy,s):
    c=Image.new('RGBA',im.size,(0,0,0,0)); d=ImageDraw.Draw(c)
    d.ellipse([cx-int(s*0.62),cy-s,cx+int(s*0.62),cy+s],fill=(60,90,40,255))           # skin
    d.ellipse([cx-int(s*0.55),cy-int(s*0.92),cx+int(s*0.55),cy+int(s*0.92)],fill=(214,226,150,255))  # pale hard flesh
    d.ellipse([cx-int(s*0.26),cy-int(s*0.05),cx+int(s*0.26),cy+int(s*0.47)],fill=(150,95,55,255))   # pit
    for k in range(5):  # crack lines = too hard
        a=k*1.1; d.line([(cx+int(s*0.3*math.cos(a)),cy-int(s*0.5)+int(s*0.2*math.sin(a))),(cx+int(s*0.45*math.cos(a)),cy-int(s*0.62)+int(s*0.3*math.sin(a)))],fill=(170,180,110,255),width=4)
    im.alpha_composite(c.filter(ImageFilter.GaussianBlur(1)))

def mango(im,cx,cy,s):
    c=Image.new('RGBA',im.size,(0,0,0,0)); d=ImageDraw.Draw(c)
    d.ellipse([cx-int(s*1.0),cy-int(s*0.62),cx+int(s*1.0),cy+int(s*0.62)],fill=(255,196,50,255))
    d.ellipse([cx-int(s*0.2),cy-int(s*0.55),cx+int(s*0.95),cy+int(s*0.3)],fill=(255,214,90,255))
    d.ellipse([cx+int(s*0.35),cy-int(s*0.45),cx+int(s*0.75),cy-int(s*0.2)],fill=(255,240,180,200))   # shine
    d.ellipse([cx-int(s*1.02),cy-int(s*0.15),cx-int(s*0.82),cy+int(s*0.05)],fill=(120,150,60,255))  # stem end
    d.polygon([(cx-int(s*0.95),cy-int(s*0.1)),(cx-int(s*1.5),cy-int(s*0.55)),(cx-int(s*1.05),cy-int(s*0.3))],fill=(90,160,70,255))   # leaf
    for k in range(6):
        d.ellipse([cx-int(s*0.5)+k*int(s*0.17),cy+int(s*0.3)-(k%2)*12,cx-int(s*0.5)+k*int(s*0.17)+7,cy+int(s*0.3)-(k%2)*12+7],fill=(200,130,40,255))
    sh=Image.new('RGBA',im.size,(0,0,0,0)); ImageDraw.Draw(sh).ellipse([cx-int(s*1.0),cy+int(s*0.5),cx+int(s*1.0),cy+int(s*0.8)],fill=(0,0,0,90))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14))); im.alpha_composite(c)

def gauge(im,cx,cy,r,val):
    d=ImageDraw.Draw(im); w=int(r*0.26)
    d.pieslice([cx-r-14,cy-r-14,cx+r+14,cy+r+14],180,360,fill=(255,255,255,235))
    zones=[(0,35,GREEN),(35,60,YEL),(60,85,ORANGE),(85,100,BROWN)]
    for a,b,col in zones:
        d.arc([cx-r,cy-r,cx+r,cy+r],180+a*1.8,180+b*1.8,fill=col+(255,),width=w)
    for t,v in (("ดิบ",17),("ใกล้",48),("พอดี",72),("เกิน",93)):
        ang=math.radians(180+v*1.8); rr=r-w//2
        d.text((cx+rr*math.cos(ang),cy+rr*math.sin(ang)),t,font=F('SemiBold',int(r*0.11)),fill=INK,anchor='mm')
    ang=math.radians(180+val*1.8); L=r-w-10
    d.line([(cx,cy),(cx+L*math.cos(ang),cy+L*math.sin(ang))],fill=INK+(255,),width=10)
    d.ellipse([cx-18,cy-18,cx+18,cy+18],fill=INK+(255,))
    d.text((cx,cy-int(r*0.28)),str(val),font=F('Bold',int(r*0.34)),fill=INK,anchor='ms')

def make(W,H,name):
    port=H>W; m=W//2; S=int(W*(0.20 if port else 0.17))
    left=bg(W,H,(96,110,96),(36,44,40),3,1)
    yb=bubbles(left, m//2, int(H*(0.17 if port else 0.19)), int(m*0.86), S)
    avocado_half(left, m//2, yb+int(H*(0.12 if port else 0.08)), int(m*(0.30 if port else 0.20)))
    right=bg(W,H,(255,236,190),(230,120,60),2,2)
    rd=ImageDraw.Draw(right); rng=np.random.default_rng(5)
    for _ in range(36):
        bx=int(rng.uniform(m+10,W-10)); by=int(rng.uniform(H*0.08,H*0.6)); col=[YEL,ORANGE,GREEN,WHITE][int(rng.integers(4))]
        rd.ellipse([bx,by,bx+12,by+12],fill=col+(200,))
    gr=int(m*0.36); gy=int(H*(0.33 if port else 0.36))
    gauge(right, m+m//2, gy, gr, 75)
    mango(right, m+m//2, gy+int(H*(0.13 if port else 0.12)), int(m*(0.24 if port else 0.19)))
    im=right.copy(); im.paste(left.crop((0,0,m,H)),(0,0))
    ov=Image.new('RGBA',(W,H),(0,0,0,0)); od=ImageDraw.Draw(ov); gh=int(H*0.38)
    for i in range(gh):
        od.line([(0,H-gh+i),(W,H-gh+i)], fill=(30,18,20,int(245*(i/gh)**1.2)))
    im=Image.alpha_composite(im,ov); d=ImageDraw.Draw(im)
    d.rectangle([m-3,0,m+3,H], fill='white')
    cy2=int(H*0.32) if port else int(H*0.52); d.ellipse([m-34,cy2-34,m+34,cy2+34], fill='white', outline=(0,0,0,60), width=2)
    d.text((m-14,cy2),'◀',font=F('Regular',26),fill=(40,40,40),anchor='mm'); d.text((m+14,cy2),'▶',font=F('Regular',26),fill=(40,40,40),anchor='mm')
    top=int(H*0.10) if port else 120
    pill(d,m//2,top,'BEFORE',(0,0,0,170),'white',F('SemiBold',34),'mm')
    pill(d,m+m//2,top,'AFTER',ORANGE+(255,),(60,20,0),F('SemiBold',34),'mm')
    pill(d,W//2,52,'AI วันละแอป · แจกฟรี / Free',(255,255,255,235),(25,25,25),F('Medium',32),'mm')
    chip_y=int(H*(0.60 if port else 0.66))
    pill(d,m//2,chip_y,'เดาเอง ผ่าแล้วดิบ',(0,0,0,160),'white',F('Medium',26),'mm')
    pill(d,m+m//2,chip_y,'มะม่วง 75/100 · สุกพอดี',(255,255,255,240),(60,30,10),F('Medium',26),'mm')
    sc=1.0 if port else 0.85; y=H-int(60*sc)
    d.text((W//2,y),'Snap a fruit, know if it is ripe right now',font=F('Regular',int(36*sc)),fill=(250,232,210),anchor='ms'); y-=int(76*sc)
    d.text((W//2,y),'ถ่ายผลไม้ รู้เลยสุกพอดีไหม',font=F('SemiBold',int(46*sc)),fill=(255,205,120),anchor='ms'); y-=int(100*sc)
    d.text((W//2,y),'RipeRight',font=F('Bold',int(110*sc)),fill='white',anchor='ms',stroke_width=2,stroke_fill=(0,0,0))
    im.convert('RGB').save(name)

make(1080,1350,'cover_1080x1350.png'); make(1080,1080,'cover_1080x1080.png')
print('covers written')
