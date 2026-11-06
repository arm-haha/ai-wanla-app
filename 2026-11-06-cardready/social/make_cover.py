"""Procedural cover: left = messy yellow-lit selfie illustration (BEFORE), right = clean white-bg ID photo (AFTER). Fictional illustrated portrait only — no real faces."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np, random, math
G='/usr/share/fonts/truetype/sand-box/google/'
F=lambda w,s: ImageFont.truetype(G+'Kanit/Kanit-'+w+'.ttf',s,layout_engine=ImageFont.Layout.RAQM)
MINT=(45,212,191); SKY=(232,243,255); INK=(26,26,26)
SKIN=(236,190,160); HAIR=(38,28,26); SHIRT=(250,250,250); SHIRT_SH=(215,222,232)

def ell(cx,cy,rx,ry,n=80): return [(cx+rx*math.cos(2*math.pi*i/n),cy+ry*math.sin(2*math.pi*i/n)) for i in range(n)]

def portrait(d,cx,cy,S,tilt=0.0,shadow=False,yellow=False):
    """Simple flat illustrated person (fictional). S = head height scale."""
    skin=SKIN; hair=HAIR; shirt=SHIRT
    if yellow:
        skin=(238,196,120); shirt=(235,215,150)
    # shoulders / body
    d.polygon([(cx-S*1.25,cy+S*1.9),(cx-S*0.95,cy+S*1.0),(cx-S*0.35,cy+S*0.78),(cx+S*0.35,cy+S*0.78),(cx+S*0.95,cy+S*1.0),(cx+S*1.25,cy+S*1.9)],fill=shirt)
    # collar V
    d.polygon([(cx-S*0.3,cy+S*0.8),(cx,cy+S*1.15),(cx+S*0.3,cy+S*0.8)],fill=(skin[0]-8,skin[1]-10,skin[2]-10))
    # neck
    d.rounded_rectangle([cx-S*0.2,cy+S*0.45,cx+S*0.2,cy+S*0.85],radius=int(S*0.08),fill=(skin[0]-10,skin[1]-14,skin[2]-14))
    # hair back
    d.ellipse([cx-S*0.62,cy-S*0.72,cx+S*0.62,cy+S*0.5],fill=hair)
    # face
    d.ellipse([cx-S*0.48,cy-S*0.55,cx+S*0.48,cy+S*0.62],fill=skin)
    # hair fringe
    d.pieslice([cx-S*0.55,cy-S*0.78,cx+S*0.55,cy+S*0.2],180,360,fill=hair)
    d.polygon([(cx-S*0.5,cy-S*0.1),(cx-S*0.2,cy-S*0.45),(cx+S*0.1,cy-S*0.5),(cx+S*0.5,cy-S*0.1),(cx+S*0.5,cy-S*0.3),(cx,cy-S*0.62),(cx-S*0.5,cy-S*0.3)],fill=hair)
    # ears
    for sx in (-1,1): d.ellipse([cx+sx*S*0.5-S*0.06,cy-S*0.03,cx+sx*S*0.5+S*0.06,cy+S*0.2],fill=(skin[0]-6,skin[1]-8,skin[2]-8))
    # eyes
    for sx in (-1,1):
        x=cx+sx*S*0.2; y=cy+S*0.02
        d.ellipse([x-S*0.075,y-S*0.045,x+S*0.075,y+S*0.045],fill='white')
        d.ellipse([x-S*0.035,y-S*0.04,x+S*0.035,y+S*0.04],fill=(40,30,28))
        d.line([x-S*0.1,y-S*0.1,x+S*0.1,y-S*0.1],fill=hair,width=max(2,int(S*0.025)))
    # nose + mouth (neutral)
    d.line([cx,cy+S*0.1,cx-S*0.025,cy+S*0.22],fill=(skin[0]-30,skin[1]-34,skin[2]-34),width=max(2,int(S*0.02)))
    d.arc([cx-S*0.12,cy+S*0.26,cx+S*0.12,cy+S*0.42],20,160,fill=(190,90,90),width=max(3,int(S*0.03)))
    if shadow:  # harsh side shadow
        ov=Image.new('RGBA',(int(S*3),int(S*3)),(0,0,0,0)); od=ImageDraw.Draw(ov)
        od.ellipse([S*1.5,S*0.9,S*2.2,S*2.1],fill=(60,30,0,90))

def messy(W,H,S,cx,cy):
    rnd=random.Random(7)
    a=np.zeros((H,W,3)); yy,xx=np.mgrid[0:H,0:W]
    a[:]=np.array([226,188,110]); a*= (1-0.28*(xx/W))[...,None]  # yellow lamp gradient
    im=Image.fromarray(np.clip(a,0,255).astype('uint8')).convert('RGBA'); d=ImageDraw.Draw(im)
    # clutter: shelves, posters, plant, clothes
    d.rectangle([W*0.03,H*0.12,W*0.30,H*0.30],fill=(150,98,60)); d.rectangle([W*0.06,H*0.15,W*0.27,H*0.27],fill=(210,150,90))
    for i in range(4): d.rectangle([W*0.07+i*W*0.05,H*0.16,W*0.07+i*W*0.05+W*0.03,H*0.26],fill=rnd.choice([(190,60,60),(60,120,190),(60,160,90),(230,200,60)]))
    d.rectangle([W*0.34,H*0.08,W*0.48,H*0.28],fill=(240,230,190),outline=(120,90,40),width=4)
    for i in range(5): d.line([W*0.36,H*0.11+i*H*0.03,W*0.46,H*0.11+i*H*0.03],fill=(150,120,70),width=3)
    d.polygon([(W*0.0,H*0.62),(W*0.18,H*0.55),(W*0.34,H*0.7),(W*0.12,H*0.86),(0,H*0.8)],fill=(180,70,90))  # pile of clothes
    d.polygon([(W*0.1,H*0.7),(W*0.3,H*0.62),(W*0.4,H*0.78),(W*0.2,H*0.9)],fill=(80,110,170))
    d.ellipse([W*0.84,H*0.62,W*0.98,H*0.78],fill=(150,90,50)); 
    for ang in range(0,360,45): d.polygon([(W*0.91,H*0.62),(W*0.91+60*math.cos(math.radians(ang)),H*0.5+60*math.sin(math.radians(ang))),(W*0.91+20,H*0.55)],fill=(60,130,70))
    # tilt person slightly
    pl=Image.new('RGBA',(W,H),(0,0,0,0)); pd=ImageDraw.Draw(pl); portrait(pd,cx,cy,S,yellow=True)
    pl=pl.rotate(7,center=(cx,cy+S)); im.alpha_composite(pl)
    # side shadow on face
    sh=Image.new('RGBA',(W,H),(0,0,0,0)); sd=ImageDraw.Draw(sh); sd.ellipse([cx+S*0.05,cy-S*0.5,cx+S*0.7,cy+S*0.65],fill=(80,40,0,95)); sh=sh.filter(ImageFilter.GaussianBlur(S*0.08)); im.alpha_composite(sh)
    # amber cast + noise
    cast=Image.new('RGBA',(W,H),(255,170,40,50)); im.alpha_composite(cast)
    n=np.random.default_rng(3).normal(0,7,(H,W,1)); arr=np.asarray(im.convert('RGB')).astype(float)+n; im=Image.fromarray(np.clip(arr,0,255).astype('uint8')).convert('RGBA')
    return im.filter(ImageFilter.GaussianBlur(1.2))

def clean(W,H,S,cx,cy):
    im=Image.new('RGBA',(W,H),(255,255,255,255)); d=ImageDraw.Draw(im)
    portrait(d,cx,cy,S); return im

def make(W,H,name):
    S=int(min(W,H)*(0.15 if H>W else 0.14)); m=W//2; cy=int(H*(0.38 if H>W else 0.34)); cxl=m//2; cxr=m+m//2
    bef=messy(W,H,S,cxl,cy); im=clean(W,H,S,cxr,cy); cx=cxr
    # ID crop frame + dimension guides on AFTER half
    d0=ImageDraw.Draw(im); fw=int(S*1.9); fh=int(fw*35/25)
    d0.rounded_rectangle([cx-fw//2,cy-int(fh*0.46),cx+fw//2,cy-int(fh*0.46)+fh],radius=8,outline=MINT+(255,),width=5)
    im.paste(bef.crop((0,0,m,H)),(0,0))
    ov=Image.new('RGBA',(W,H),(0,0,0,0)); od=ImageDraw.Draw(ov); gh=int(H*0.42)
    for i in range(gh): od.line([(0,H-gh+i),(W,H-gh+i)],fill=(10,30,50,int(240*(i/gh)**1.3)))
    im=Image.alpha_composite(im,ov); d=ImageDraw.Draw(im)
    d.rectangle([m-3,0,m+3,H],fill='white')
    cy2=int(H*0.30); d.ellipse([m-34,cy2-34,m+34,cy2+34],fill='white',outline=(0,0,0,60),width=2)
    d.text((m-14,cy2),'◀',font=F('Regular',26),fill=(40,40,40),anchor='mm'); d.text((m+14,cy2),'▶',font=F('Regular',26),fill=(40,40,40),anchor='mm')
    def pill(x,y,t,bg,fg,font,anchor):
        b=d.textbbox((x,y),t,font=font,anchor=anchor); p=14
        d.rounded_rectangle([b[0]-p*1.6,b[1]-p,b[2]+p*1.6,b[3]+p],radius=40,fill=bg); d.text((x,y),t,font=font,fill=fg,anchor=anchor)
    top=int(H*0.10) if H>W else 120
    pill(cxl,top,'BEFORE',(0,0,0,170),'white',F('SemiBold',34),'mm')
    pill(cxr,top,'AFTER',MINT+(255,),(10,40,40),F('SemiBold',34),'mm')
    pill(W//2,52,'AI วันละแอป · แจกฟรี / Free',(255,255,255,235),(25,25,25),F('Medium',32),'mm')
    # spec chips
    chip_y=int(H*(0.58 if H>W else 0.56))
    pill(cxr,chip_y,'พื้นขาว · 295×413 px',(255,255,255,235),(20,60,70),F('Medium',28),'mm')
    pill(cxr,chip_y+70,'Pass Score 92 · ผ่าน',(45,212,191,255),(5,40,40),F('SemiBold',30),'mm')
    pill(cxl,chip_y,'แสงเหลือง · พื้นรก',(0,0,0,150),'white',F('Medium',28),'mm')
    s=1.0 if H>W else 0.85
    y=H-int(60*s)
    d.text((W//2,y),'Messy selfie → ID photo in 3 seconds',font=F('Regular',int(44*s)),fill=(235,240,245),anchor='ms'); y-=int(76*s)
    d.text((W//2,y),'เซลฟี่มั่ว ๆ → รูปติดบัตรใน 3 วิ',font=F('SemiBold',int(60*s)),fill=MINT,anchor='ms'); y-=int(100*s)
    d.text((W//2,y),'CardReady',font=F('Bold',int(120*s)),fill='white',anchor='ms',stroke_width=2,stroke_fill=(0,0,0))
    im.convert('RGB').save(name)
make(1080,1350,'cover_1080x1350.png'); make(1080,1080,'cover_1080x1080.png')
