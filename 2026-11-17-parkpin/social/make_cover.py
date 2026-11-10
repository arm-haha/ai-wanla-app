from PIL import Image, ImageDraw, ImageFont
import numpy as np
K='/usr/share/fonts/truetype/sand-box/google/Kanit/Kanit-'
F=lambda w,s: ImageFont.truetype(K+w+'.ttf',s,layout_engine=ImageFont.Layout.RAQM)
AMBER=(255,205,90)
YELLOW=(245,197,24)
GREEN=(22,163,74)
INK=(28,36,48)

def bg(W,H,top,bot,noise=3,seed=7):
    yy=np.linspace(0,1,H).reshape(H,1,1)
    a=np.array(top)*(1-yy)+np.array(bot)*yy
    a=np.repeat(a,W,axis=1)
    a+=np.random.default_rng(seed).normal(0,noise,(H,W,1))
    return Image.fromarray(np.clip(a,0,255).astype('uint8')).convert('RGBA')

def garage(im, cx, cy, s, pinned=False):
    d=ImageDraw.Draw(im)
    # concrete wall
    x0,y0=cx-int(200*s), cy-int(220*s)
    x1,y1=cx+int(200*s), cy+int(220*s)
    d.rectangle([x0,y0,x1,y1], fill=(70,78,88,255))
    # floor
    d.polygon([(x0,y1-int(80*s)),(x1,y1-int(80*s)),(x1,y1+int(40*s)),(x0,y1+int(40*s))], fill=(50,56,64,255))
    # stall lines
    for i in range(-2,3):
        xx=cx+int(i*70*s)
        d.line([(xx, y1-int(70*s)),(xx+int(18*s), y1+int(20*s))], fill=YELLOW+(255,), width=max(3,int(4*s)))
    # pillar
    px=cx-int(20*s); py=cy-int(40*s)
    d.rectangle([px-int(36*s), py-int(140*s), px+int(36*s), py+int(160*s)], fill=(200,202,206,255) if not pinned else (210,220,210,255))
    # color band
    band = GREEN if pinned else (140,140,148)
    d.rectangle([px-int(36*s), py-int(20*s), px+int(36*s), py+int(40*s)], fill=band+(255,))
    label = 'C-14' if pinned else '??'
    d.text((px, py+int(10*s)), label, font=F('Bold', int(28*s)), fill='white' if pinned else (40,40,40), anchor='mm')
    # floor sign
    sx,sy=cx+int(90*s), cy-int(130*s)
    d.rounded_rectangle([sx-int(70*s),sy-int(50*s),sx+int(70*s),sy+int(50*s)], radius=12, fill=(20,24,30,255), outline=YELLOW+(255,), width=4)
    d.text((sx, sy-int(12*s)), 'B2' if pinned else 'B?', font=F('Bold', int(36*s)), fill=YELLOW+(255,), anchor='mm')
    d.text((sx, sy+int(22*s)), 'โซนเขียว' if pinned else 'โซน ?', font=F('Medium', int(16*s)), fill='white', anchor='mm')
    if pinned:
        # pin card
        cx0=cx; cy0=cy+int(150*s)
        d.rounded_rectangle([cx0-int(170*s), cy0-int(48*s), cx0+int(170*s), cy0+int(48*s)], radius=18, fill=(255,255,255,245), outline=GREEN+(255,), width=4)
        d.text((cx0, cy0-int(16*s)), '150 นาที · ≈ ฿60', font=F('Bold', int(24*s)), fill=INK+(255,), anchor='mm')
        d.text((cx0, cy0+int(16*s)), 'อีก 45 นาทีขยับเป็น ฿80', font=F('Medium', int(16*s)), fill=(80,80,20,255), anchor='mm')
    return im

def make(W,H,name):
    port=H>W; m=W//2
    s=(0.95 if port else 0.82)*(W/1080)
    left=bg(W,H,(40,46,56),(16,18,22),3,1)
    right=bg(W,H,(36,50,44),(14,20,18),2,2)
    cy=int(H*(0.40 if port else 0.42))
    garage(left, m//2, cy, s, pinned=False)
    garage(right, m+m//2, cy, s, pinned=True)
    im=right.copy(); im.paste(left.crop((0,0,m,H)),(0,0))
    ov=Image.new('RGBA',(W,H),(0,0,0,0)); od=ImageDraw.Draw(ov); gh=int(H*0.42)
    for i in range(gh):
        od.line([(0,H-gh+i),(W,H-gh+i)],fill=(8,10,14,int(245*(i/gh)**1.2)))
    im=Image.alpha_composite(im,ov); d=ImageDraw.Draw(im)
    d.rectangle([m-3,0,m+3,H],fill='white')
    cy2=int(H*0.28); d.ellipse([m-34,cy2-34,m+34,cy2+34],fill='white',outline=(0,0,0,60),width=2)
    d.text((m-14,cy2),'◀',font=F('Regular',26),fill=(40,40,40),anchor='mm')
    d.text((m+14,cy2),'▶',font=F('Regular',26),fill=(40,40,40),anchor='mm')
    def pill(x,y,t,bgc,fg,font,anchor):
        b=d.textbbox((x,y),t,font=font,anchor=anchor); p=14
        d.rounded_rectangle([b[0]-p*1.6,b[1]-p,b[2]+p*1.6,b[3]+p],radius=40,fill=bgc); d.text((x,y),t,font=font,fill=fg,anchor=anchor)
    top=int(H*0.10) if port else 120
    pill(m//2,top,'BEFORE',(0,0,0,170),'white',F('SemiBold',34),'mm')
    pill(m+m//2,top,'AFTER',GREEN+(255,),'white',F('SemiBold',34),'mm')
    pill(W//2,52,'AI วันละแอป · แจกฟรี / Free',(255,255,255,235),(25,25,25),F('Medium',32),'mm')
    chip_y=int(H*(0.62 if port else 0.60))
    pill(m//2,chip_y,'ลืมชั้น ลืมเสา',(0,0,0,150),'white',F('Medium',28),'mm')
    pill(m+m//2,chip_y,'B2 · โซนเขียว · เสา C-14',(255,255,255,240),(20,40,25),F('Medium',24),'mm')
    pill(m+m//2,chip_y+70,'ค่าจอดอย่างคร่าว ฿60',YELLOW+(255,),(30,20,0),F('SemiBold',26),'mm')
    sc=1.0 if port else 0.85
    y=H-int(60*sc)
    d.text((W//2,y),'Pin your parking spot before you forget it',font=F('Regular',int(38*sc)),fill=(230,235,240),anchor='ms'); y-=int(76*sc)
    d.text((W//2,y),'จำที่จอดในห้างได้ในรูปเดียว',font=F('SemiBold',int(52*sc)),fill=AMBER,anchor='ms'); y-=int(100*sc)
    d.text((W//2,y),'ParkPin',font=F('Bold',int(110*sc)),fill='white',anchor='ms',stroke_width=2,stroke_fill=(0,0,0))
    im.convert('RGB').save(name)

if __name__=='__main__':
    make(1080,1350,'cover_1080x1350.png'); make(1080,1080,'cover_1080x1080.png')
    print('covers written')
