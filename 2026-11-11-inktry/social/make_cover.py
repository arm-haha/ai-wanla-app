from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math, numpy as np
K='/usr/share/fonts/truetype/sand-box/google/Kanit/Kanit-'
F=lambda w,s: ImageFont.truetype(K+w+'.ttf',s,layout_engine=ImageFont.Layout.RAQM)
INK=(17,17,17)
GOLD=(201,163,106)
CREAM=(244,239,230)
SKIN=(232,184,154)
SKIN2=(214,154,122)
AMBER=(255,205,90)

def bg(W,H,top,bot,noise=3,seed=7):
    yy=np.linspace(0,1,H).reshape(H,1,1)
    a=np.array(top)*(1-yy)+np.array(bot)*yy
    a=np.repeat(a,W,axis=1)
    a+=np.random.default_rng(seed).normal(0,noise,(H,W,1))
    return Image.fromarray(np.clip(a,0,255).astype('uint8')).convert('RGBA')

def arm(im, cx, cy, scale, tattoo=False, faded=False):
    """Stylised left inner forearm, no real person."""
    d=ImageDraw.Draw(im)
    # upper arm / elbow to wrist, slightly tapered
    pts=[]
    L=int(420*scale); W0=int(86*scale); W1=int(58*scale)
    # left and right edges
    left=[]; right=[]
    for i in range(24):
        t=i/23
        y=cy-L//2 + int(L*t)
        # slight curve
        xoff=int(math.sin(t*math.pi)*12*scale)
        wl=int(W0*(1-t)+W1*t)
        left.append((cx-wl+xoff,y)); right.append((cx+wl+xoff,y))
    poly=left+right[::-1]
    # shadow
    sh=[(x+int(10*scale),y+int(8*scale)) for x,y in poly]
    d.polygon(sh, fill=(40,28,22,80))
    d.polygon(poly, fill=SKIN+(255,))
    # inner highlight
    d.line([(p[0]+int(18*scale),p[1]) for p in left], fill=(245,210,185,180), width=max(3,int(6*scale)))
    # rounded wrist cap (no hand, keeps it a clean illustrated forearm)
    x0,y0=right[-1]; x1,y1=left[-1]
    d.ellipse([min(x0,x1)-2, y1-int(22*scale), max(x0,x1)+2, y1+int(22*scale)], fill=SKIN+(255,))
    if tattoo:
        # fine-line olive sprig
        col = (90,70,50,200) if faded else (25,28,22,255)
        w = max(2, int((2 if faded else 3)*scale))
        spr=Image.new('RGBA', im.size, (0,0,0,0)); sd=ImageDraw.Draw(spr)
        y0s=cy-int(L*0.30); y1s=cy+int(L*0.24)
        # curved stem as many short segments
        pts=[]
        for i in range(20):
            tt=i/19
            x=cx+int((6-18*tt)*scale)
            y=y0s+int((y1s-y0s)*tt)
            pts.append((x,y))
        sd.line(pts, fill=col, width=w, joint='curve')
        def leaf(ax,ay,ang,length,width,outline_only=False):
            ca,sa=math.cos(ang),math.sin(ang)
            # ellipse-like polygon along angle
            pts=[]
            for k in range(16):
                a=k/16*2*math.pi
                px=length*math.cos(a); py=width*math.sin(a)
                pts.append((ax+px*ca-py*sa, ay+px*sa+py*ca))
            if outline_only:
                sd.polygon(pts, outline=col, width=max(1,w-1))
            else:
                sd.polygon(pts, outline=col, width=w)
        for i,tt in enumerate((0.12,0.26,0.40,0.54,0.68,0.82)):
            x=cx+int((6-18*tt)*scale)
            y=y0s+int((y1s-y0s)*tt)
            side=1 if i%2==0 else -1
            ang=(-0.35 if side>0 else math.pi+0.35) + (tt-0.5)*0.3
            leaf(x+int(side*22*scale), y, ang, 28*scale, 10*scale, faded)
        if faded:
            spr=spr.filter(ImageFilter.GaussianBlur(max(1,int(2.2*scale))))
            # fade alpha
            a=np.array(spr)
            a[...,3]= (a[...,3]*0.40).astype(a.dtype)
            spr=Image.fromarray(a)
        im.alpha_composite(spr)
    return im

def make(W,H,name):
    port=H>W; m=W//2
    scale=W/1080
    left=bg(W,H,(48,36,32),(18,14,12),3,1)
    right=bg(W,H,(42,38,32),(16,14,12),2,2)
    cy=int(H*(0.42 if port else 0.44))
    arm(left, m//2, cy, 1.05 if port else 0.92, tattoo=False)
    arm(right, m+m//2, cy, 1.05 if port else 0.92, tattoo=True, faded=False)
    im=right.copy(); im.paste(left.crop((0,0,m,H)),(0,0))
    ov=Image.new('RGBA',(W,H),(0,0,0,0)); od=ImageDraw.Draw(ov); gh=int(H*0.42)
    for i in range(gh):
        od.line([(0,H-gh+i),(W,H-gh+i)],fill=(12,9,7,int(245*(i/gh)**1.2)))
    im=Image.alpha_composite(im,ov); d=ImageDraw.Draw(im)
    d.rectangle([m-3,0,m+3,H],fill='white')
    cy2=int(H*0.32); d.ellipse([m-34,cy2-34,m+34,cy2+34],fill='white',outline=(0,0,0,60),width=2)
    d.text((m-14,cy2),'◀',font=F('Regular',26),fill=(40,40,40),anchor='mm')
    d.text((m+14,cy2),'▶',font=F('Regular',26),fill=(40,40,40),anchor='mm')
    def pill(x,y,t,bgc,fg,font,anchor):
        b=d.textbbox((x,y),t,font=font,anchor=anchor); p=14
        d.rounded_rectangle([b[0]-p*1.6,b[1]-p,b[2]+p*1.6,b[3]+p],radius=40,fill=bgc); d.text((x,y),t,font=font,fill=fg,anchor=anchor)
    top=int(H*0.10) if port else 120
    pill(m//2,top,'BEFORE',(0,0,0,170),'white',F('SemiBold',34),'mm')
    pill(m+m//2,top,'AFTER',GOLD+(255,),(30,20,0),F('SemiBold',34),'mm')
    pill(W//2,52,'AI วันละแอป · แจกฟรี / Free',(255,255,255,235),(25,25,25),F('Medium',32),'mm')
    chip_y=int(H*(0.60 if port else 0.585))
    pill(m//2,chip_y,'แขนเปล่า · ยังไม่กล้าสัก',(0,0,0,150),'white',F('Medium',28),'mm')
    pill(m+m//2,chip_y,'ช่อโอลิฟ์ 8 ซม. · ขาวดำ',(255,255,255,240),(40,30,10),F('Medium',25),'mm')
    pill(m+m//2,chip_y+70,'5 ปี · จาง 60% (จำลอง)',GOLD+(255,),(30,20,0),F('SemiBold',29),'mm')
    s=1.0 if port else 0.85
    y=H-int(60*s)
    d.text((W//2,y),'Try the tattoo on your skin before you ink',font=F('Regular',int(40*s)),fill=(235,230,220),anchor='ms'); y-=int(76*s)
    d.text((W//2,y),'ลองรอยสักบนตัวก่อนสักจริง',font=F('SemiBold',int(56*s)),fill=AMBER,anchor='ms'); y-=int(100*s)
    d.text((W//2,y),'InkTry',font=F('Bold',int(120*s)),fill='white',anchor='ms',stroke_width=2,stroke_fill=(0,0,0))
    im.convert('RGB').save(name)

if __name__=='__main__':
    make(1080,1350,'cover_1080x1350.png'); make(1080,1080,'cover_1080x1080.png')
    print('covers written')
