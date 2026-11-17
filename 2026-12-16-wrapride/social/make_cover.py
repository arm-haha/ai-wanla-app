"""Procedural cover: one hatchback in side view split by a before/after slider — left = original white gloss (BEFORE),
right = the same car wrapped mint-green matte with a black two-tone roof, black 5-spoke rims and a side stripe (AFTER) + price/legal chips.
Illustration only — no real people, plates or brands."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np, math
G='/usr/share/fonts/truetype/sand-box/google/'
F=lambda w,s: ImageFont.truetype(G+'Kanit/Kanit-'+w+'.ttf',s,layout_engine=ImageFont.Layout.RAQM)
MINT=(127,209,174); MINT_SH=(102,167,139); MINT_HI=(142,215,184); BLACK=(27,27,27); WHITE=(255,255,255); INK=(20,32,40)
PEARL=(242,240,234); PEARL_SH=(190,192,196); SILVER=(201,205,210)
SS=2  # supersample

def bg(W,H,top,bot,noise,seed):
    yy=np.linspace(0,1,H)[:,None,None]; a=np.array(top)*(1-yy)+np.array(bot)*yy; a=np.repeat(a,W,axis=1)
    a+=np.random.default_rng(seed).normal(0,noise,(H,W,1))
    return Image.fromarray(np.clip(a,0,255).astype('uint8')).convert('RGBA')

def pill(d,x,y,t,bgc,fg,font,anchor):
    b=d.textbbox((x,y),t,font=font,anchor=anchor); p=14
    d.rounded_rectangle([b[0]-p*1.6,b[1]-p,b[2]+p*1.6,b[3]+p], radius=40, fill=bgc); d.text((x,y),t,font=font,fill=fg,anchor=anchor)

def scene(W,H,gy,after):
    """Street/garage backdrop + floor + car, drawn at SS scale then downsampled."""
    w,h=W*SS,H*SS; g=gy*SS
    im=bg(w,h,(60,70,84) if not after else (255,214,170),(150,155,165) if not after else (255,150,170),2,1 if not after else 2)
    d=ImageDraw.Draw(im)
    # backdrop: garage panels (before) / neon city at sunset (after)
    rng=np.random.default_rng(5)
    for k in range(7):
        bx=int(w*k/7); bh=int(h*rng.uniform(0.18,0.34)); col=(80,90,105,255) if not after else (120,80,140,255)
        d.rectangle([bx+6,g-int(h*0.08)-bh,bx+int(w/7)-6,g-int(h*0.08)],fill=col)
        for r in range(5):
            for c in range(3):
                wx=bx+30+c*int((w/7-70)/3); wy=g-int(h*0.08)-bh+30+r*70
                if wy<g-int(h*0.10): d.rectangle([wx,wy,wx+30,wy+36],fill=(110,120,135,255) if not after else (255,220,120,255))
    # floor
    d.rectangle([0,g-int(h*0.08),w,h],fill=(95,98,104,255) if not after else (70,60,90,255))
    for k in range(8):
        d.line([(0,g+k*int(h*0.04)),(w,g+k*int(h*0.04))],fill=(110,113,120,255) if not after else (95,80,120,255),width=3)
    car(im,w,g,after)
    return im.resize((W,H),Image.LANCZOS)

def car(im,w,g,after):
    d=ImageDraw.Draw(im); S=w/1080
    P=lambda pts:[(x*S,y*S+g-560*S) for x,y in pts]
    body=PEARL if not after else MINT; sh=PEARL_SH if not after else MINT_SH; hi=WHITE if not after else MINT_HI
    roof=PEARL if not after else BLACK
    # shadow
    sh_im=Image.new('RGBA',im.size,(0,0,0,0)); sd=ImageDraw.Draw(sh_im)
    sd.ellipse([110*S,g-40*S,970*S,g+40*S],fill=(0,0,0,150)); sh_im=sh_im.filter(ImageFilter.GaussianBlur(18*S)); im.alpha_composite(sh_im)
    # lower body
    d.polygon(P([(110,470),(130,395),(250,370),(380,350),(800,345),(920,370),(975,410),(985,480),(960,520),(130,520)]),fill=body+(255,))
    d.polygon(P([(130,470),(985,470),(960,520),(130,520)]),fill=sh+(255,))
    # cabin
    d.polygon(P([(330,352),(430,240),(470,228),(760,228),(800,240),(880,352)]),fill=roof+(255,))
    # windows
    d.polygon(P([(375,345),(455,255),(600,255),(600,345)]),fill=(40,60,75,255))
    d.polygon(P([(615,345),(615,255),(770,255),(830,345)]),fill=(40,60,75,255))
    d.polygon(P([(470,262),(520,262),(440,340),(400,340)]),fill=(120,150,170,170))
    # pillars
    d.rectangle(P([(600,250),(615,350)]),fill=roof+(255,))
    # highlight line along shoulder (gloss strong / matte soft)
    d.line(P([(150,400),(400,372),(900,372),(960,405)]),fill=hi+(255,),width=int((10 if not after else 4)*S))
    # side stripe (after)
    if after:
        d.polygon(P([(140,440),(970,440),(972,452),(140,452)]),fill=BLACK+(255,))
        # mirror cap
        d.polygon(P([(330,355),(370,330),(395,345),(360,368)]),fill=BLACK+(255,))
    else:
        d.polygon(P([(330,355),(370,330),(395,345),(360,368)]),fill=PEARL_SH+(255,))
    # door lines + handles
    d.line(P([(605,350),(605,505)]),fill=sh+(255,),width=int(3*S)); d.line(P([(395,360),(390,500)]),fill=sh+(255,),width=int(3*S))
    for hx in (520,720): d.rounded_rectangle(P([(hx,395),(hx+45,405)]),radius=int(4*S),fill=sh+(255,))
    # lights (always uncovered)
    d.polygon(P([(940,380),(980,400),(982,425),(945,420)]),fill=(255,240,200,255))
    d.polygon(P([(112,420),(140,400),(150,440),(115,445)]),fill=(220,40,40,255))
    # wheels
    for cx in (270,820):
        d.ellipse(P([(cx-100,430),(cx+100,630)]),fill=sh+(255,))
        d.ellipse(P([(cx-84,446),(cx+84,614)]),fill=(18,18,20,255))
        d.ellipse(P([(cx-54,476),(cx+54,584)]),fill=(SILVER if not after else (30,30,32))+(255,))
        cy=530
        for k in range(5 if after else 10):
            a=k*2*math.pi/(5 if after else 10)
            col=(150,155,160,255) if not after else (60,60,64,255)
            d.line([((cx+12*math.cos(a))*S,(cy+12*math.sin(a))*S+g-560*S),((cx+50*math.cos(a))*S,(cy+50*math.sin(a))*S+g-560*S)],fill=col,width=int((7 if not after else 16)*S))
        d.ellipse(P([(cx-14,cy-14),(cx+14,cy+14)]),fill=(90,90,95,255) if not after else (140,220,190,255))

def make(W,H,name):
    port=H>W; m=W//2
    gy=int(H*(0.58 if port else 0.60))
    left=scene(W,H,gy,False); right=scene(W,H,gy,True)
    im=right.copy(); im.paste(left.crop((0,0,m,H)),(0,0))
    ov=Image.new('RGBA',(W,H),(0,0,0,0)); od=ImageDraw.Draw(ov); gh=int(H*0.36)
    for i in range(gh):
        od.line([(0,H-gh+i),(W,H-gh+i)], fill=(10,18,24,int(250*(i/gh)**1.1)))
    im=Image.alpha_composite(im,ov); d=ImageDraw.Draw(im)
    d.rectangle([m-3,0,m+3,H], fill='white')
    cy2=int(H*0.30); d.ellipse([m-34,cy2-34,m+34,cy2+34], fill='white', outline=(0,0,0,60), width=2)
    d.text((m-14,cy2),'◀',font=F('Regular',26),fill=(40,40,40),anchor='mm'); d.text((m+14,cy2),'▶',font=F('Regular',26),fill=(40,40,40),anchor='mm')
    top=int(H*0.11) if port else 125
    pill(d,m//2,top,'BEFORE',(0,0,0,170),'white',F('SemiBold',34),'mm')
    pill(d,m+m//2,top,'AFTER',MINT+(255,),INK,F('SemiBold',34),'mm')
    pill(d,W//2,52,'AI วันละแอป · แจกฟรี / Free',(255,255,255,235),(25,25,25),F('Medium',32),'mm')
    chip_y=int(H*(0.19 if port else 0.22))
    pill(d,m//2,chip_y,'ขาวเดิม ๆ',(0,0,0,150),'white',F('Medium',26),'mm')
    pill(d,m+m//2,chip_y,'มิ้นต์ด้าน+หลังคาดำ',(255,255,255,240),INK,F('Medium',26),'mm')
    chip2=int(H*(0.665 if port else 0.70))
    pill(d,W//2,chip2,'ราคาประมาณ ฿19,000–38,000 · เช็กขนส่งก่อนเปลี่ยนสี',(255,255,255,240),INK,F('Medium',26),'mm')
    sc=1.0 if port else 0.85; y=H-int(60*sc)
    d.text((W//2,y),'Snap your ride, try a new wrap before you pay',font=F('Regular',int(36*sc)),fill=(220,240,235),anchor='ms'); y-=int(76*sc)
    d.text((W//2,y),'ถ่ายรถ ลองสีใหม่ก่อนจ่ายจริง',font=F('SemiBold',int(48*sc)),fill=MINT,anchor='ms'); y-=int(100*sc)
    d.text((W//2,y),'WrapRide',font=F('Bold',int(116*sc)),fill='white',anchor='ms',stroke_width=2,stroke_fill=(0,0,0))
    im.convert('RGB').save(name)

make(1080,1350,'cover_1080x1350.png'); make(1080,1080,'cover_1080x1080.png')
print('covers written')
