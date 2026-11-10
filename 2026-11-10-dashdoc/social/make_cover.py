"""Procedural cover: left = illustrated dashboard with scary warning lights (BEFORE), right = DashDoc urgency meter + verdict (AFTER). Illustration only — no real photos or people."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np, math
G='/usr/share/fonts/truetype/sand-box/google/'
F=lambda w,s: ImageFont.truetype(G+'Kanit/Kanit-'+w+'.ttf',s,layout_engine=ImageFont.Layout.RAQM)
ORANGE=(255,159,28); AMBER=(255,193,7); RED=(220,38,38); GREEN=(22,163,74); INK=(18,22,32); BLUE=(37,99,235); WHITE=(255,255,255)

def bg(W,H,top,bot,noise,seed):
    yy=np.linspace(0,1,H)[:,None,None]; a=np.array(top)*(1-yy)+np.array(bot)*yy; a=np.repeat(a,W,axis=1)
    a+=np.random.default_rng(seed).normal(0,noise,(H,W,1))
    return Image.fromarray(np.clip(a,0,255).astype('uint8')).convert('RGBA')

def glow(im,cx,cy,r,col,a=150):
    g=Image.new('RGBA',im.size,(0,0,0,0)); ImageDraw.Draw(g).ellipse([cx-r,cy-r,cx+r,cy+r],fill=col+(a,))
    im.alpha_composite(g.filter(ImageFilter.GaussianBlur(r*0.45)))

def engine_icon(d,cx,cy,s,col,w=None):
    w=w or max(4,int(s*0.07))
    d.rounded_rectangle([cx-s*0.50,cy-s*0.28,cx+s*0.30,cy+s*0.38],radius=int(s*0.08),outline=col,width=w)   # block
    d.rectangle([cx-s*0.30,cy-s*0.44,cx+s*0.08,cy-s*0.28],outline=col,width=w)                                # intake
    d.line([(cx-s*0.50,cy),(cx-s*0.66,cy)],fill=col,width=w); d.line([(cx-s*0.66,cy-s*0.12),(cx-s*0.66,cy+s*0.12)],fill=col,width=w)
    d.polygon([(cx+s*0.30,cy-s*0.12),(cx+s*0.52,cy-s*0.12),(cx+s*0.52,cy+s*0.26),(cx+s*0.30,cy+s*0.26)],outline=col,width=w)
    d.line([(cx-s*0.2,cy+s*0.38),(cx-s*0.12,cy+s*0.52),(cx+s*0.2,cy+s*0.52)],fill=col,width=w)

def tire_icon(d,cx,cy,s,col,w=None):
    w=w or max(4,int(s*0.07))
    d.arc([cx-s*0.45,cy-s*0.45,cx+s*0.45,cy+s*0.45],-215,35,fill=col,width=w)
    for k in range(7):
        a=math.radians(-210+k*40); x=cx+math.cos(a)*s*0.5; y=cy+math.sin(a)*s*0.5
        d.line([(cx+math.cos(a)*s*0.42,cy+math.sin(a)*s*0.42),(x,y)],fill=col,width=max(2,w//2))
    d.line([(cx,cy-s*0.25),(cx,cy+s*0.05)],fill=col,width=w); d.ellipse([cx-w*0.6,cy+s*0.13,cx+w*0.6,cy+s*0.13+w*1.2],fill=col)

def oil_icon(d,cx,cy,s,col,w=None):
    w=w or max(4,int(s*0.07))
    d.arc([cx-s*0.45,cy-s*0.05,cx-s*0.1,cy+s*0.3],90,270,fill=col,width=w)
    d.rounded_rectangle([cx-s*0.3,cy-s*0.1,cx+s*0.35,cy+s*0.3],radius=int(s*0.06),outline=col,width=w)
    d.polygon([(cx+s*0.4,cy+s*0.0),(cx+s*0.55,cy+s*0.2),(cx+s*0.25,cy+s*0.2)],outline=col,width=max(2,w//2))

def dial(im,cx,cy,r,col=(70,80,100),ticks=True):
    d=ImageDraw.Draw(im); d.ellipse([cx-r,cy-r,cx+r,cy+r],fill=(10,12,18,255),outline=col+(255,),width=max(3,int(r*0.04)))
    if ticks:
        for k in range(21):
            a=math.radians(135+k*13.5); r1=r*0.82; r2=r*(0.92 if k%5==0 else 0.88)
            d.line([(cx+math.cos(a)*r1,cy+math.sin(a)*r1),(cx+math.cos(a)*r2,cy+math.sin(a)*r2)],fill=(200,205,215) if k%5==0 else (110,118,135),width=max(2,int(r*0.025)))
        a=math.radians(135+9*13.5); d.line([(cx,cy),(cx+math.cos(a)*r*0.7,cy+math.sin(a)*r*0.7)],fill=(255,80,60),width=max(3,int(r*0.04)))
        d.ellipse([cx-r*0.07,cy-r*0.07,cx+r*0.07,cy+r*0.07],fill=(230,230,235))

def dashboard(W,H,calm,port):
    im=bg(W,H,(26,30,44),(8,10,16),2,3 if calm else 4)
    S=int(min(W,H)*0.19); cy=int(H*0.30)
    mw=W//2
    for cx in (mw//2-int(S*0.05),):
        pass
    return im,S,cy

def make(W,H,name):
    port=H>W; m=W//2; S=int(W*(0.205 if port else 0.17)); cy=int(H*(0.34 if port else 0.40))
    # BEFORE (left): dark dash, glowing orange lights
    left=bg(W,H,(30,28,36),(8,8,12),3,1)
    dial(left,m//2,cy+int(S*0.55),int(S*0.95)); dial(left,m//2+int(S*0.1),cy+int(S*0.55),int(S*0.62),(50,58,74),ticks=False)
    glow(left,m//2-int(S*0.45),cy-int(S*0.55),int(S*0.8),ORANGE,170); glow(left,m//2+int(S*0.55),cy-int(S*0.5),int(S*0.8),AMBER,150)
    ld=ImageDraw.Draw(left)
    engine_icon(ld,m//2-int(S*0.45),cy-int(S*0.55),S*0.95,ORANGE,int(S*0.075)); tire_icon(ld,m//2+int(S*0.55),cy-int(S*0.5),S*0.8,AMBER,int(S*0.07))
    # AFTER (right): same dash + verdict card with urgency meter
    right=bg(W,H,(24,34,48),(8,12,18),2,2)
    dial(right,m+m//2,cy+int(S*0.55),int(S*0.95)); dial(right,m+m//2+int(S*0.1),cy+int(S*0.55),int(S*0.62),(50,58,74),ticks=False)
    rd=ImageDraw.Draw(right)
    cw=int(m*0.80); cx0=m+(m-cw)//2; cy0=cy-int(S*1.3); ch=int(S*1.65)
    rd.rounded_rectangle([cx0,cy0,cx0+cw,cy0+ch],radius=26,fill=(255,255,255,245),outline=AMBER+(255,),width=5)
    # meter arc red/yellow/green
    mx=cx0+cw//2; my=cy0+int(ch*0.60); R=int(cw*0.34); aw=int(R*0.26)
    for a0,a1,col in ((180,240,GREEN),(240,300,AMBER),(300,360,RED)):
        rd.arc([mx-R,my-R,mx+R,my+R],a0,a1,fill=col,width=aw)
    ang=math.radians(180+1.8*48); rd.line([(mx,my),(mx+math.cos(ang)*R*0.78,my+math.sin(ang)*R*0.78)],fill=INK,width=max(5,int(R*0.07)))
    rd.ellipse([mx-R*0.1,my-R*0.1,mx+R*0.1,my+R*0.1],fill=INK)
    rd.text((mx,cy0+int(ch*0.12)),'URGENCY 48 / 100',font=F('SemiBold',int(S*0.17)),fill=(80,60,0),anchor='mm')
    rd.text((mx,my+int(R*0.30)),'ขับต่อได้ ~50 กม.',font=F('Bold',int(S*0.27)),fill=INK,anchor='mm')
    rd.text((mx,my+int(R*0.62)),'≤ 80 กม./ชม. · ไปอู่ภายใน 1 วัน',font=F('Medium',int(S*0.15)),fill=(90,70,10),anchor='mm')
    im=right.copy(); im.paste(left.crop((0,0,m,H)),(0,0))
    ov=Image.new('RGBA',(W,H),(0,0,0,0)); od=ImageDraw.Draw(ov); gh=int(H*0.42)
    for i in range(gh): od.line([(0,H-gh+i),(W,H-gh+i)],fill=(6,8,14,int(245*(i/gh)**1.2)))
    im=Image.alpha_composite(im,ov); d=ImageDraw.Draw(im)
    d.rectangle([m-3,0,m+3,H],fill='white')
    cy2=int(H*0.30); d.ellipse([m-34,cy2-34,m+34,cy2+34],fill='white',outline=(0,0,0,60),width=2)
    d.text((m-14,cy2),'◀',font=F('Regular',26),fill=(40,40,40),anchor='mm'); d.text((m+14,cy2),'▶',font=F('Regular',26),fill=(40,40,40),anchor='mm')
    def pill(x,y,t,bgc,fg,font,anchor):
        b=d.textbbox((x,y),t,font=font,anchor=anchor); p=14
        d.rounded_rectangle([b[0]-p*1.6,b[1]-p,b[2]+p*1.6,b[3]+p],radius=40,fill=bgc); d.text((x,y),t,font=font,fill=fg,anchor=anchor)
    top=int(H*0.10) if port else 120
    pill(m//2,top,'BEFORE',(0,0,0,170),'white',F('SemiBold',34),'mm')
    pill(m+m//2,top,'AFTER',AMBER+(255,),(30,20,0),F('SemiBold',34),'mm')
    pill(W//2,52,'AI วันละแอป · แจกฟรี / Free',(255,255,255,235),(25,25,25),F('Medium',32),'mm')
    chip_y=int(H*(0.60 if port else 0.585))
    pill(m//2,chip_y,'ไฟส้มขึ้น · ขับต่อดีไหม?',(0,0,0,150),'white',F('Medium',28),'mm')
    pill(m+m//2,chip_y,'เช็กเครื่อง + ลมยางอ่อน · ~฿300–950',(255,255,255,240),(60,45,0),F('Medium',25),'mm')
    pill(m+m//2,chip_y+70,'เหลือง · ไปอู่ได้',AMBER+(255,),(30,20,0),F('SemiBold',29),'mm')
    s=1.0 if port else 0.85
    y=H-int(60*s)
    d.text((W//2,y),'One dashboard photo → can I keep driving? in 3 sec',font=F('Regular',int(40*s)),fill=(235,238,245),anchor='ms'); y-=int(76*s)
    d.text((W//2,y),'ถ่ายรูปเดียว รู้ใน 3 วิ ขับต่อได้ไหม',font=F('SemiBold',int(56*s)),fill=(255,205,90),anchor='ms'); y-=int(100*s)
    d.text((W//2,y),'DashDoc',font=F('Bold',int(120*s)),fill='white',anchor='ms',stroke_width=2,stroke_fill=(0,0,0))
    im.convert('RGB').save(name)
make(1080,1350,'cover_1080x1350.png'); make(1080,1080,'cover_1080x1080.png')
