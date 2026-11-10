"""Procedural cover: left = messy photo stack (BEFORE), right = month-8 milestone card (AFTER). Illustration only — footprints/teddy/card, no real children."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
G='/usr/share/fonts/truetype/sand-box/google/'
F=lambda w,s: ImageFont.truetype(G+'Kanit/Kanit-'+w+'.ttf',s,layout_engine=ImageFont.Layout.RAQM)
AMBER=(255,196,64); WHITE=(255,255,255); CREAM=(247,239,230)
PINK=(242,184,198); MINT=(143,203,179); INK=(59,47,47); BROWN=(196,164,132)

def bg(W,H,top,bot,noise,seed):
    yy=np.linspace(0,1,H)[:,None,None]; a=np.array(top)*(1-yy)+np.array(bot)*yy; a=np.repeat(a,W,axis=1)
    a+=np.random.default_rng(seed).normal(0,noise,(H,W,1))
    return Image.fromarray(np.clip(a,0,255).astype('uint8')).convert('RGBA')

def polaroid(im,x,y,w,h,tilt,fill,label=None):
    c=Image.new('RGBA',(w+40,h+60),(0,0,0,0)); d=ImageDraw.Draw(c)
    d.rounded_rectangle([8,8,w+8,h+28], radius=10, fill=(252,248,242,255), outline=(230,220,210,255), width=3)
    d.rounded_rectangle([20,20,w-4,h-10], radius=6, fill=fill)
    if label:
        d.text(((w+16)//2, h+10), label, font=F('Medium', max(16,w//10)), fill=INK+(255,), anchor='mm')
    if tilt:
        c=c.rotate(tilt, expand=True, resample=Image.Resampling.BICUBIC)
    im.alpha_composite(c,(x,y))

def footprint(d,x,y,s,fill,flip=1):
    d.ellipse([x, y, x+int(s*0.55), y+int(s*1.05)], fill=fill)
    for i,ox in enumerate((-0.08, 0.10, 0.30, 0.46)):
        r=int(s*(0.16 if i in (1,2) else 0.13))
        d.ellipse([x+int(s*ox*flip), y-int(s*0.22), x+int(s*ox*flip)+r, y-int(s*0.22)+r], fill=fill)

def teddy(im,cx,cy,s):
    d=ImageDraw.Draw(im)
    d.ellipse([cx-int(s*0.55), cy-int(s*0.70), cx+int(s*0.55), cy+int(s*0.50)], fill=(210,160,120,255))
    d.ellipse([cx-int(s*0.70), cy-int(s*0.85), cx-int(s*0.30), cy-int(s*0.40)], fill=(190,140,105,255))
    d.ellipse([cx+int(s*0.30), cy-int(s*0.85), cx+int(s*0.70), cy-int(s*0.40)], fill=(190,140,105,255))
    d.ellipse([cx-int(s*0.22), cy-int(s*0.15), cx+int(s*0.22), cy+int(s*0.22)], fill=(240,220,200,255))
    d.ellipse([cx-int(s*0.22), cy-int(s*0.38), cx-int(s*0.08), cy-int(s*0.22)], fill=INK+(255,))
    d.ellipse([cx+int(s*0.08), cy-int(s*0.38), cx+int(s*0.22), cy-int(s*0.22)], fill=INK+(255,))
    d.ellipse([cx-int(s*0.08), cy-int(s*0.12), cx+int(s*0.08), cy+int(s*0.04)], fill=(120,80,60,255))

def pill(d,x,y,t,bgc,fg,font,anchor):
    b=d.textbbox((x,y),t,font=font,anchor=anchor); p=14
    d.rounded_rectangle([b[0]-p*1.6,b[1]-p,b[2]+p*1.6,b[3]+p], radius=40, fill=bgc); d.text((x,y),t,font=font,fill=fg,anchor=anchor)

def make(W,H,name):
    port=H>W; m=W//2; S=int(W*(0.20 if port else 0.17))
    left=bg(W,H,(90,70,75),(40,30,36),3,1)
    # messy scattered polaroids — abstract fills, no faces
    polaroid(left, int(m*0.06), int(H*0.16), int(S*1.35), int(S*1.45), -16, (186,160,150,255), "??")
    polaroid(left, int(m*0.22), int(H*0.28), int(S*1.45), int(S*1.55), 10, (160,170,150,255), "??")
    polaroid(left, int(m*0.10), int(H*0.36), int(S*1.30), int(S*1.40), -6, (170,150,165,255))

    right=bg(W,H,(120,70,85),(50,30,40),2,2)
    rd=ImageDraw.Draw(right)
    cx=m+m//2
    pw,ph=int(m*0.80), int(S*3.15)
    px,py=cx-pw//2, int(H*(0.15 if port else 0.16))
    # soft glow
    g=Image.new('RGBA',right.size,(0,0,0,0)); gd=ImageDraw.Draw(g)
    gd.rounded_rectangle([px-20,py-20,px+pw+20,py+ph+20], radius=36, fill=(255,230,220,80))
    right.alpha_composite(g.filter(ImageFilter.GaussianBlur(20)))
    rd=ImageDraw.Draw(right)
    rd.rounded_rectangle([px,py,px+pw,py+ph], radius=28, fill=CREAM+(255,), outline=PINK+(255,), width=6)
    rd.text((cx, py+int(S*0.32)), "เดือนที่ 8", font=F('SemiBold', int(S*0.28)), fill=INK, anchor='mm')
    rd.text((cx, py+int(S*0.62)), "นั่งทรงตัวได้", font=F('Bold', int(S*0.24)), fill=(160,70,90), anchor='mm')
    # decorative footprints + teddy, no baby
    footprint(rd, px+int(S*0.28), py+int(S*1.15), int(S*0.42), PINK+(255,), 1)
    footprint(rd, px+pw-int(S*0.70), py+int(S*1.15), int(S*0.42), MINT+(255,), -1)
    teddy(right, cx, py+int(S*1.95), int(S*0.55))
    rd=ImageDraw.Draw(right)
    rd.text((cx, py+ph-int(S*0.38)), "น้องภู", font=F('Medium', int(S*0.22)), fill=INK, anchor='mm')

    im=right.copy(); im.paste(left.crop((0,0,m,H)),(0,0))
    ov=Image.new('RGBA',(W,H),(0,0,0,0)); od=ImageDraw.Draw(ov); gh=int(H*0.42)
    for i in range(gh):
        od.line([(0,H-gh+i),(W,H-gh+i)], fill=(28,16,18,int(245*(i/gh)**1.2)))
    im=Image.alpha_composite(im,ov); d=ImageDraw.Draw(im)
    d.rectangle([m-3,0,m+3,H], fill='white')
    cy2=int(H*0.32); d.ellipse([m-34,cy2-34,m+34,cy2+34], fill='white', outline=(0,0,0,60), width=2)
    d.text((m-14,cy2),'◀',font=F('Regular',26),fill=(40,40,40),anchor='mm')
    d.text((m+14,cy2),'▶',font=F('Regular',26),fill=(40,40,40),anchor='mm')
    top=int(H*0.10) if port else 120
    pill(d,m//2,top,'BEFORE',(0,0,0,170),'white',F('SemiBold',34),'mm')
    pill(d,m+m//2,top,'AFTER',AMBER+(255,),(30,20,0),F('SemiBold',34),'mm')
    pill(d,W//2,52,'AI วันละแอป · แจกฟรี / Free',(255,255,255,235),(25,25,25),F('Medium',32),'mm')
    chip_y=int(H*(0.60 if port else 0.585))
    pill(d,m//2,chip_y,'รูปกองในเครื่อง',(0,0,0,150),'white',F('Medium',28),'mm')
    pill(d,m+m//2,chip_y,'การ์ดเดือนที่ 8',(255,255,255,240),(40,30,10),F('Medium',26),'mm')
    pill(d,m+m//2,chip_y+70,'นั่งทรงตัวได้',PINK+(255,),INK,F('SemiBold',29),'mm')
    sc=1.0 if port else 0.85
    y=H-int(60*sc)
    d.text((W//2,y),'Monthly milestone cards from one photo',font=F('Regular',int(38*sc)),fill=(235,230,220),anchor='ms'); y-=int(76*sc)
    d.text((W//2,y),'การ์ดพัฒนาการลูกรายเดือนจากรูป',font=F('SemiBold',int(48*sc)),fill=(255,205,90),anchor='ms'); y-=int(100*sc)
    d.text((W//2,y),'TinySteps',font=F('Bold',int(110*sc)),fill='white',anchor='ms',stroke_width=2,stroke_fill=(0,0,0))
    im.convert('RGB').save(name)

make(1080,1350,'cover_1080x1350.png'); make(1080,1080,'cover_1080x1080.png')
print('covers written')
