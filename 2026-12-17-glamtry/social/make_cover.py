"""Procedural cover: one stylised (fictional, drawn) face split by a before/after slider — left = bare skin (BEFORE),
right = the same face in the 'Korean glass skin' look (AFTER) + a strip of 6 look chips and a shade/price chip.
Illustration only — no real people, celebrities or brands."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
G='/usr/share/fonts/truetype/sand-box/google/'
F=lambda w,s: ImageFont.truetype(G+'Kanit/Kanit-'+w+'.ttf',s,layout_engine=ImageFont.Layout.RAQM)
ROSE=(232,135,155); PLUM=(43,34,56); INK=(30,22,40); WHITE=(255,255,255)
SKIN=(214,170,140); SKIN_SH=(188,142,114); HAIR=(42,30,28)
LIP_BARE=(196,128,118); LIP=(224,108,113); BLUSH=(241,160,159); EYE=(233,183,166)
LOOKS=[('เนเชอรัล',(201,123,110)),('เกาหลี',(224,108,113)),('เจ้าสาว',(181,72,90)),('ปาร์ตี้',(142,31,47)),('ออฟฟิศ',(184,100,90)),('Y2K',(229,143,176))]
SS=2

def bg(W,H,top,bot,noise,seed):
    yy=np.linspace(0,1,H)[:,None,None]; a=np.array(top)*(1-yy)+np.array(bot)*yy; a=np.repeat(a,W,axis=1)
    a+=np.random.default_rng(seed).normal(0,noise,(H,W,1))
    return Image.fromarray(np.clip(a,0,255).astype('uint8')).convert('RGBA')

def pill(d,x,y,t,bgc,fg,font,anchor):
    b=d.textbbox((x,y),t,font=font,anchor=anchor); p=14
    d.rounded_rectangle([b[0]-p*1.6,b[1]-p,b[2]+p*1.6,b[3]+p], radius=40, fill=bgc); d.text((x,y),t,font=font,fill=fg,anchor=anchor)

def glow(im,box,col,blur):
    g=Image.new('RGBA',im.size,col[:3]+(0,)); ImageDraw.Draw(g).ellipse(box,fill=col); im.alpha_composite(g.filter(ImageFilter.GaussianBlur(blur)))

def face(W,H,cy,after):
    w,h=W*SS,H*SS; S=w/1080; c=w//2; y0=cy*SS
    im=bg(w,h,(236,226,218) if not after else (255,226,232),(205,192,184) if not after else (246,180,196),2,1 if not after else 2)
    d=ImageDraw.Draw(im)
    if after:
        rng=np.random.default_rng(3)
        for _ in range(40):
            x,y,r=rng.uniform(0,w),rng.uniform(0,h*0.7),rng.uniform(3,9)*S
            d.ellipse([x-r,y-r,x+r,y+r],fill=(255,255,255,150))
    P=lambda x,y:(c+x*S,y0+y*S)
    box=lambda x1,y1,x2,y2:[c+x1*S,y0+y1*S,c+x2*S,y0+y2*S]
    # hair back + shoulders
    d.ellipse(box(-300,-360,300,260),fill=HAIR+(255,))
    d.rectangle(box(-300,-50,300,420),fill=HAIR+(255,))
    d.rounded_rectangle(box(-380,330,380,900),radius=int(200*S),fill=(250,245,240,255) if not after else (255,250,252,255))
    d.rectangle(box(-80,200,80,360),fill=SKIN_SH+(255,))
    # face
    d.ellipse(box(-215,-270,215,300),fill=SKIN+(255,))
    # fringe
    d.chord(box(-235,-330,235,40),180,360,fill=HAIR+(255,))
    d.rectangle(box(-235,-150,-185,120),fill=HAIR+(255,)); d.rectangle(box(185,-150,235,120),fill=HAIR+(255,))
    if after:
        glow(im,box(-180,40,-70,120),BLUSH+(190,),int(22*S)); glow(im,box(70,40,180,120),BLUSH+(190,),int(22*S))
        glow(im,box(-14,-30,14,60),(255,240,230,140),int(10*S))  # glass-skin glow on nose bridge
        glow(im,box(-160,10,-110,45),(255,245,240,170),int(10*S)); glow(im,box(110,10,160,45),(255,245,240,170),int(10*S))
        d=ImageDraw.Draw(im)
    # brows
    for sx in (-1,1):
        d.line([P(sx*150,-80),P(sx*100,-95),P(sx*50,-88)],fill=(70,48,40,255),width=int(12*S),joint='curve')
    # eyes
    for sx in (-1,1):
        ex=sx*100
        if after: d.ellipse(box(ex-58,-62,ex+58,-8),fill=EYE+(220,))
        d.ellipse(box(ex-42,-45,ex+42,-15),fill=(255,255,255,255))
        d.ellipse(box(ex-17,-48,ex+17,-14),fill=(60,40,34,255))
        d.ellipse(box(ex-5,-40,ex+3,-32),fill=(255,255,255,255))
        lw=int((7 if after else 4)*S)
        d.arc(box(ex-44,-55,ex+44,-5),190,350,fill=(30,20,20,255),width=lw)
        if after:
            for k in range(5):
                lx=ex-30+k*15; d.line([P(lx,-48),P(lx+sx*3-2,-62)],fill=(30,20,20,255),width=int(3*S))
    # nose
    d.line([P(0,-10),P(-8,60),P(8,66)],fill=SKIN_SH+(255,),width=int(5*S))
    # lips
    lip=LIP if after else LIP_BARE
    d.chord(box(-62,105,62,165),0,180,fill=lip+(255,))
    d.chord(box(-62,85,62,135),180,360,fill=tuple(max(0,v-18) for v in lip)+(255,))
    if after: d.ellipse(box(-20,128,10,142),fill=(255,220,225,200))
    return im.resize((W,H),Image.LANCZOS)

def make(W,H,name):
    port=H>W; m=W//2
    cy=int(H*(0.40 if port else 0.40))
    left=face(W,H,cy,False); right=face(W,H,cy,True)
    im=right.copy(); im.paste(left.crop((0,0,m,H)),(0,0))
    ov=Image.new('RGBA',(W,H),(0,0,0,0)); od=ImageDraw.Draw(ov); gh=int(H*0.40)
    for i in range(gh):
        od.line([(0,H-gh+i),(W,H-gh+i)], fill=(36,20,40,int(250*(i/gh)**1.1)))
    im=Image.alpha_composite(im,ov); d=ImageDraw.Draw(im)
    d.rectangle([m-3,0,m+3,H], fill='white')
    cy2=int(H*0.30); d.ellipse([m-34,cy2-34,m+34,cy2+34], fill='white', outline=(0,0,0,60), width=2)
    d.text((m-14,cy2),'◀',font=F('Regular',26),fill=(40,40,40),anchor='mm'); d.text((m+14,cy2),'▶',font=F('Regular',26),fill=(40,40,40),anchor='mm')
    top=int(H*0.11) if port else 125
    pill(d,m//2,top,'BEFORE',(0,0,0,170),'white',F('SemiBold',34),'mm')
    pill(d,m+m//2,top,'AFTER',ROSE+(255,),INK,F('SemiBold',34),'mm')
    pill(d,W//2,52,'AI วันละแอป · แจกฟรี / Free',(255,255,255,235),(25,25,25),F('Medium',32),'mm')
    chip_y=int(H*(0.19 if port else 0.22))
    pill(d,m//2,chip_y,'หน้าสด',(0,0,0,150),'white',F('Medium',26),'mm')
    pill(d,m+m//2,chip_y,'เกาหลีผิวฉ่ำ',(255,255,255,240),INK,F('Medium',26),'mm')
    # 6 look chips
    ly=int(H*(0.62 if port else 0.585)); n=len(LOOKS); gap=W//(n+1); fs=F('Medium',22)
    for k,(t,col) in enumerate(LOOKS):
        x=gap*(k+1); r=30 if port else 26
        d.ellipse([x-r-4,ly-r-4,x+r+4,ly+r+4],fill=(255,255,255,255) if k==1 else (255,255,255,120)); d.ellipse([x-r,ly-r,x+r,ly+r],fill=col+(255,))
        d.text((x,ly+r+22),t,font=fs,fill='white',anchor='mm',stroke_width=2,stroke_fill=(40,20,40))
    chip2=int(H*(0.715 if port else 0.70))
    pill(d,W//2,chip2,'6 ลุคจากเซลฟี่เดียว · เฉดผิวโดยประมาณ 2W · ชุดของ ~฿584',(255,255,255,240),INK,F('Medium',25),'mm')
    sc=1.0 if port else 0.85; y=H-int(60*sc)
    d.text((W//2,y),'One selfie, try 6 makeup looks before you buy',font=F('Regular',int(36*sc)),fill=(250,225,232),anchor='ms'); y-=int(76*sc)
    d.text((W//2,y),'เซลฟี่เดียว ลองแต่งหน้าก่อนซื้อ',font=F('SemiBold',int(48*sc)),fill=ROSE,anchor='ms'); y-=int(100*sc)
    d.text((W//2,y),'GlamTry',font=F('Bold',int(116*sc)),fill='white',anchor='ms',stroke_width=2,stroke_fill=(0,0,0))
    im.convert('RGB').save(name)

make(1080,1350,'cover_1080x1350.png'); make(1080,1080,'cover_1080x1080.png')
print('covers written')
