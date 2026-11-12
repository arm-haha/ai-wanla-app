"""Procedural cover: left = a rough chat idea for a dinosaur cake (BEFORE), right = AI cake mock-up + price/servings chips (AFTER). Illustration only — no real people or brands."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
G='/usr/share/fonts/truetype/sand-box/google/'
F=lambda w,s: ImageFont.truetype(G+'Kanit/Kanit-'+w+'.ttf',s,layout_engine=ImageFont.Layout.RAQM)
PINK=(249,168,212); WHITE=(255,255,255); GREEN=(124,195,107); YEL=(244,211,94); DGREEN=(91,140,58)
INK=(30,27,46); CREAM=(255,248,240); CHOC=(92,58,40)

def bg(W,H,top,bot,noise,seed):
    yy=np.linspace(0,1,H)[:,None,None]; a=np.array(top)*(1-yy)+np.array(bot)*yy; a=np.repeat(a,W,axis=1)
    a+=np.random.default_rng(seed).normal(0,noise,(H,W,1))
    return Image.fromarray(np.clip(a,0,255).astype('uint8')).convert('RGBA')

def pill(d,x,y,t,bgc,fg,font,anchor):
    b=d.textbbox((x,y),t,font=font,anchor=anchor); p=14
    d.rounded_rectangle([b[0]-p*1.6,b[1]-p,b[2]+p*1.6,b[3]+p], radius=40, fill=bgc); d.text((x,y),t,font=font,fill=fg,anchor=anchor)

def bubbles(im,cx,top,w,S):
    d=ImageDraw.Draw(im)
    msgs=[("อยากได้เค้กไดโนเสาร์",False),("แขก 18 คน ต้องกี่ปอนด์?",False),("เขียนว่า HBD น้องภูมิ 5 ขวบ",False),("ราคาเท่าไหร่ดี ???",False)]
    y=top; f=F('Regular',int(S*0.15))
    for t,_ in msgs:
        b=d.textbbox((0,0),t,font=f); tw=b[2]-b[0]; th=b[3]-b[1]
        x0=cx-w//2+10; d.rounded_rectangle([x0,y,x0+tw+44,y+th+40],radius=26,fill=(255,255,255,235))
        d.text((x0+22,y+20+th//2),t,font=f,fill=INK,anchor='lm'); y+=th+62
    if im.size[1]<=im.size[0]: return
    # scribble sketch
    sx,sy=cx,y+int(S*0.55); r=int(w*0.28)
    d.rectangle([sx-r,sy-int(r*0.35),sx+r,sy+int(r*0.45)],outline=(255,255,255,200),width=4)
    d.line([(sx-r//2,sy-int(r*0.35)),(sx-r//3,sy-int(r*0.8)),(sx,sy-int(r*0.55)),(sx+r//4,sy-int(r*0.9))],fill=(255,255,255,200),width=4)
    d.text((sx,sy+int(r*0.05)),'???',font=F('Medium',int(S*0.2)),fill=(255,255,255,200),anchor='mm')

def cake(im,cx,base,w):
    c=Image.new('RGBA',im.size,(0,0,0,0)); d=ImageDraw.Draw(c)
    h=int(w*0.55); x0,x1=cx-w//2,cx+w//2; top=base-h; e=int(w*0.13)
    d.ellipse([x0-30,base-e+20,x1+30,base+e+40],fill=(255,255,255,235))  # plate
    d.rectangle([x0,top,x1,base],fill=GREEN+(255,)); d.ellipse([x0,base-e,x1,base+e],fill=GREEN+(255,))
    # drip
    for k in range(9):
        dx=x0+int(w*(0.06+0.11*k)); dl=int(h*(0.18+0.12*((k*37)%5)/4))
        d.rounded_rectangle([dx-14,top,dx+14,top+dl],radius=14,fill=YEL+(255,))
    d.ellipse([x0,top-e,x1,top+e],fill=YEL+(255,))
    d.ellipse([x0+18,top-e+12,x1-18,top+e-12],fill=(252,236,170,255))
    # dots
    for k in range(7):
        d.ellipse([x0+40+k*int(w/8)-12,base-int(h*0.35)-12,x0+40+k*int(w/8)+12,base-int(h*0.35)+12],fill=DGREEN+(255,))
    # dino topper
    dx,dy=cx+int(w*0.12),top-int(e*0.2); s=int(w*0.12)
    d.ellipse([dx-s,dy-s*1.3,dx+s,dy+s*0.2],fill=DGREEN+(255,))
    d.rounded_rectangle([dx+int(s*0.4),dy-s*2.6,dx+int(s*1.0),dy-s*0.8],radius=18,fill=DGREEN+(255,))
    d.ellipse([dx+int(s*0.3),dy-s*3.1,dx+int(s*1.6),dy-s*2.3],fill=DGREEN+(255,))
    d.ellipse([dx+int(s*1.05),dy-s*2.9,dx+int(s*1.25),dy-s*2.7],fill=(20,20,20,255))
    d.polygon([(dx-s,dy-s*0.6),(dx-int(s*2.2),dy+int(s*0.1)),(dx-s,dy)],fill=DGREEN+(255,))
    for k in range(4):
        px=dx-int(s*0.7)+k*int(s*0.45); d.polygon([(px,dy-int(s*1.2)),(px+int(s*0.22),dy-int(s*1.75)),(px+int(s*0.44),dy-int(s*1.15))],fill=YEL+(255,))
    # candles
    for k,cx2 in enumerate([cx-int(w*0.28),cx-int(w*0.18)]):
        d.rectangle([cx2-7,top-int(e*0.4)-70,cx2+7,top-int(e*0.4)],fill=(255,255,255,255))
        d.ellipse([cx2-10,top-int(e*0.4)-100,cx2+10,top-int(e*0.4)-68],fill=(255,170,60,255))
    sh=c.filter(ImageFilter.GaussianBlur(10)); im.alpha_composite(c)

def make(W,H,name):
    port=H>W; m=W//2; S=int(W*(0.20 if port else 0.17))
    left=bg(W,H,(120,96,140),(40,32,58),3,1)
    bubbles(left, m//2, int(H*(0.17 if port else 0.19)), int(m*0.86), S)
    right=bg(W,H,(255,214,232),(150,80,130),2,2); rd=ImageDraw.Draw(right)
    rng=np.random.default_rng(5)
    for _ in range(40):
        bx=int(rng.uniform(m+10,W-10)); by=int(rng.uniform(H*0.08,H*0.6)); col=[PINK,YEL,GREEN,WHITE][int(rng.integers(4))]
        rd.rectangle([bx,by,bx+10,by+18],fill=col+(220,))
    cake(right, m+m//2, int(H*(0.50 if port else 0.55)), int(m*0.66))
    im=right.copy(); im.paste(left.crop((0,0,m,H)),(0,0))
    ov=Image.new('RGBA',(W,H),(0,0,0,0)); od=ImageDraw.Draw(ov); gh=int(H*0.38)
    for i in range(gh):
        od.line([(0,H-gh+i),(W,H-gh+i)], fill=(25,12,30,int(245*(i/gh)**1.2)))
    im=Image.alpha_composite(im,ov); d=ImageDraw.Draw(im)
    d.rectangle([m-3,0,m+3,H], fill='white')
    cy2=int(H*0.32); d.ellipse([m-34,cy2-34,m+34,cy2+34], fill='white', outline=(0,0,0,60), width=2)
    d.text((m-14,cy2),'◀',font=F('Regular',26),fill=(40,40,40),anchor='mm'); d.text((m+14,cy2),'▶',font=F('Regular',26),fill=(40,40,40),anchor='mm')
    top=int(H*0.10) if port else 120
    pill(d,m//2,top,'BEFORE',(0,0,0,170),'white',F('SemiBold',34),'mm')
    pill(d,m+m//2,top,'AFTER',PINK+(255,),(60,10,40),F('SemiBold',34),'mm')
    pill(d,W//2,52,'AI วันละแอป · แจกฟรี / Free',(255,255,255,235),(25,25,25),F('Medium',32),'mm')
    chip_y=int(H*(0.60 if port else 0.66))
    pill(d,m//2,chip_y,'ไอเดียลอย ๆ ในแชต',(0,0,0,160),'white',F('Medium',26),'mm')
    pill(d,m+m//2,chip_y,'2 ปอนด์ · 14 ชิ้น · ~฿1,300',(255,255,255,240),(40,20,40),F('Medium',26),'mm')
    sc=1.0 if port else 0.85; y=H-int(60*sc)
    d.text((W//2,y),'Describe it, see your dream cake, order it',font=F('Regular',int(36*sc)),fill=(240,225,240),anchor='ms'); y-=int(76*sc)
    d.text((W//2,y),'บอกธีม เห็นเค้กในฝัน สั่งร้านได้เลย',font=F('SemiBold',int(46*sc)),fill=(255,190,225),anchor='ms'); y-=int(100*sc)
    d.text((W//2,y),'CakeDream',font=F('Bold',int(110*sc)),fill='white',anchor='ms',stroke_width=2,stroke_fill=(0,0,0))
    im.convert('RGB').save(name)

make(1080,1350,'cover_1080x1350.png'); make(1080,1080,'cover_1080x1080.png')
print('covers written')
