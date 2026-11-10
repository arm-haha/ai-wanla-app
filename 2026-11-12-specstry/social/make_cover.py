from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math, numpy as np
K='/usr/share/fonts/truetype/sand-box/google/Kanit/Kanit-'
F=lambda w,s: ImageFont.truetype(K+w+'.ttf',s,layout_engine=ImageFont.Layout.RAQM)
GOLD=(201,163,106)
TEAL=(42,111,127)
AMBER=(255,205,90)
SKIN=(235,196,170)
HAIR=(42,36,40)
LIP=(196,110,110)

def bg(W,H,top,bot,noise=3,seed=7):
    yy=np.linspace(0,1,H).reshape(H,1,1)
    a=np.array(top)*(1-yy)+np.array(bot)*yy
    a=np.repeat(a,W,axis=1)
    a+=np.random.default_rng(seed).normal(0,noise,(H,W,1))
    return Image.fromarray(np.clip(a,0,255).astype('uint8')).convert('RGBA')

def face(im, cx, cy, s, glasses=False):
    """Stylised fictional adult face, not a likeness of anyone."""
    d=ImageDraw.Draw(im)
    # neck
    d.rectangle([cx-int(36*s), cy+int(70*s), cx+int(36*s), cy+int(150*s)], fill=(220,176,150,255))
    # shoulders / top
    d.ellipse([cx-int(160*s), cy+int(120*s), cx+int(160*s), cy+int(230*s)], fill=TEAL+(255,))
    # hair back
    d.ellipse([cx-int(92*s), cy-int(130*s), cx+int(92*s), cy+int(40*s)], fill=HAIR+(255,))
    # face oval
    d.ellipse([cx-int(72*s), cy-int(95*s), cx+int(72*s), cy+int(95*s)], fill=SKIN+(255,))
    # hair bangs
    d.pieslice([cx-int(92*s), cy-int(140*s), cx+int(92*s), cy+int(10*s)], 200, 340, fill=HAIR+(255,))
    # ears
    d.ellipse([cx-int(88*s), cy-int(10*s), cx-int(68*s), cy+int(28*s)], fill=SKIN+(255,))
    d.ellipse([cx+int(68*s), cy-int(10*s), cx+int(88*s), cy+int(28*s)], fill=SKIN+(255,))
    # brows
    d.arc([cx-int(48*s), cy-int(28*s), cx-int(14*s), cy-int(8*s)], 200, 340, fill=(60,40,35,255), width=max(3,int(4*s)))
    d.arc([cx+int(14*s), cy-int(28*s), cx+int(48*s), cy-int(8*s)], 200, 340, fill=(60,40,35,255), width=max(3,int(4*s)))
    # eyes
    d.ellipse([cx-int(42*s), cy-int(8*s), cx-int(18*s), cy+int(12*s)], fill=(250,250,252,255))
    d.ellipse([cx+int(18*s), cy-int(8*s), cx+int(42*s), cy+int(12*s)], fill=(250,250,252,255))
    d.ellipse([cx-int(34*s), cy-int(4*s), cx-int(22*s), cy+int(8*s)], fill=(40,70,80,255))
    d.ellipse([cx+int(22*s), cy-int(4*s), cx+int(34*s), cy+int(8*s)], fill=(40,70,80,255))
    # nose, mouth
    d.arc([cx-int(10*s), cy+int(8*s), cx+int(10*s), cy+int(32*s)], 20, 160, fill=(180,130,110,255), width=max(2,int(3*s)))
    d.arc([cx-int(16*s), cy+int(42*s), cx+int(16*s), cy+int(62*s)], 20, 160, fill=LIP+(255,), width=max(3,int(3*s)))
    if glasses:
        gl=Image.new('RGBA', im.size, (0,0,0,0)); gd=ImageDraw.Draw(gl)
        w=max(4,int(5*s))
        boxes=[]
        for sign in (-1,1):
            x=cx+int(sign*32*s)
            box=[x-int(30*s), cy-int(22*s), x+int(30*s), cy+int(22*s)]
            boxes.append(box)
            gd.ellipse(box, fill=(180,220,230,70), outline=GOLD+(255,), width=w)
        gd.line([(cx-int(6*s), cy), (cx+int(6*s), cy)], fill=GOLD+(255,), width=w)
        gd.line([(cx-int(62*s), cy-int(2*s)), (cx-int(86*s), cy+int(6*s))], fill=GOLD+(255,), width=max(3,int(4*s)))
        gd.line([(cx+int(62*s), cy-int(2*s)), (cx+int(86*s), cy+int(6*s))], fill=GOLD+(255,), width=max(3,int(4*s)))
        im.alpha_composite(gl)
    return im

def make(W,H,name):
    port=H>W; m=W//2; s=(1.15 if port else 1.0)* (W/1080)
    left=bg(W,H,(236,232,224),(210,200,188),3,1)
    right=bg(W,H,(232,236,234),(200,214,214),2,2)
    cy=int(H*(0.40 if port else 0.42))
    face(left, m//2, cy, s, glasses=False)
    face(right, m+m//2, cy, s, glasses=True)
    im=right.copy(); im.paste(left.crop((0,0,m,H)),(0,0))
    ov=Image.new('RGBA',(W,H),(0,0,0,0)); od=ImageDraw.Draw(ov); gh=int(H*0.42)
    for i in range(gh):
        od.line([(0,H-gh+i),(W,H-gh+i)],fill=(16,20,22,int(245*(i/gh)**1.2)))
    im=Image.alpha_composite(im,ov); d=ImageDraw.Draw(im)
    d.rectangle([m-3,0,m+3,H],fill='white')
    cy2=int(H*0.30); d.ellipse([m-34,cy2-34,m+34,cy2+34],fill='white',outline=(0,0,0,60),width=2)
    d.text((m-14,cy2),'◀',font=F('Regular',26),fill=(40,40,40),anchor='mm')
    d.text((m+14,cy2),'▶',font=F('Regular',26),fill=(40,40,40),anchor='mm')
    def pill(x,y,t,bgc,fg,font,anchor):
        b=d.textbbox((x,y),t,font=font,anchor=anchor); p=14
        d.rounded_rectangle([b[0]-p*1.6,b[1]-p,b[2]+p*1.6,b[3]+p],radius=40,fill=bgc); d.text((x,y),t,font=font,fill=fg,anchor=anchor)
    top=int(H*0.10) if port else 120
    pill(m//2,top,'BEFORE',(0,0,0,170),'white',F('SemiBold',34),'mm')
    pill(m+m//2,top,'AFTER',GOLD+(255,),(30,20,0),F('SemiBold',34),'mm')
    pill(W//2,52,'AI วันละแอป · แจกฟรี / Free',(255,255,255,235),(25,25,25),F('Medium',32),'mm')
    chip_y=int(H*(0.62 if port else 0.60))
    pill(m//2,chip_y,'ยังไม่รู้ทรงไหนเข้าหน้า',(0,0,0,150),'white',F('Medium',26),'mm')
    pill(m+m//2,chip_y,'หน้าไข่ · กรอบกลมบาง 96',(255,255,255,240),(20,40,45),F('Medium',25),'mm')
    pill(m+m//2,chip_y+70,'48-20-140 · PD ≈ 62 มม.',GOLD+(255,),(30,20,0),F('SemiBold',26),'mm')
    sc=1.0 if port else 0.85
    y=H-int(60*sc)
    d.text((W//2,y),'Try the frames on your face before you buy',font=F('Regular',int(40*sc)),fill=(235,238,236),anchor='ms'); y-=int(76*sc)
    d.text((W//2,y),'ลองแว่นบนหน้าตัวเองก่อนซื้อ',font=F('SemiBold',int(56*sc)),fill=AMBER,anchor='ms'); y-=int(100*sc)
    d.text((W//2,y),'SpecsTry',font=F('Bold',int(110*sc)),fill='white',anchor='ms',stroke_width=2,stroke_fill=(0,0,0))
    im.convert('RGB').save(name)

if __name__=='__main__':
    make(1080,1350,'cover_1080x1350.png'); make(1080,1080,'cover_1080x1080.png')
    print('covers written')
