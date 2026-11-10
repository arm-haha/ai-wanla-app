"""Procedural cover: left = illustrated mic (BEFORE), right = pitch/timing score card (AFTER).
Fictional illustration only — no real singers, no copyrighted song art."""
from PIL import Image, ImageDraw, ImageFont
import numpy as np
G='/usr/share/fonts/truetype/sand-box/google/'
F=lambda w,s: ImageFont.truetype(G+'Kanit/Kanit-'+w+'.ttf',s,layout_engine=ImageFont.Layout.RAQM)
NAVY=(17,24,39); PINK=(244,114,182); GOLD=(251,191,36); WHITE=(255,255,255); PURPLE=(167,139,250)

def bg(W,H,top,bot,noise,seed):
    yy=np.linspace(0,1,H)[:,None,None]; a=np.array(top)*(1-yy)+np.array(bot)*yy; a=np.repeat(a,W,axis=1)
    a+=np.random.default_rng(seed).normal(0,noise,(H,W,1))
    return Image.fromarray(np.clip(a,0,255).astype('uint8')).convert('RGBA')

def pill(d,x,y,t,bgc,fg,font,anchor):
    b=d.textbbox((x,y),t,font=font,anchor=anchor); p=14
    d.rounded_rectangle([b[0]-p*1.6,b[1]-p,b[2]+p*1.6,b[3]+p], radius=40, fill=bgc); d.text((x,y),t,font=font,fill=fg,anchor=anchor)

def mic(d, cx, cy, s):
    # head
    d.rounded_rectangle([cx-int(s*0.38), cy-int(s*1.05), cx+int(s*0.38), cy-int(s*0.15)], radius=int(s*0.38), fill=(220,220,230), outline=WHITE, width=4)
    for i in range(-2, 3):
        d.line([(cx+i*int(s*0.10), cy-int(s*0.95)), (cx+i*int(s*0.10), cy-int(s*0.25))], fill=(80,80,100), width=3)
    # stem
    d.rectangle([cx-int(s*0.08), cy-int(s*0.15), cx+int(s*0.08), cy+int(s*0.55)], fill=(60,60,80), outline=WHITE, width=2)
    # stand base
    d.polygon([(cx-int(s*0.55), cy+int(s*0.85)), (cx+int(s*0.55), cy+int(s*0.85)), (cx+int(s*0.20), cy+int(s*0.55)), (cx-int(s*0.20), cy+int(s*0.55))], fill=(40,40,55), outline=WHITE, width=3)
    # sound rings
    for r in (int(s*0.70), int(s*0.95)):
        d.arc([cx-r, cy-int(s*0.70)-r//2, cx+r, cy-int(s*0.70)+r//2], 300, 60, fill=PINK, width=4)

def make(W,H,name):
    port=H>W; m=W//2; S=int(W*(0.20 if port else 0.16))
    left=bg(W,H,(40,20,50),(17,24,39),3,61)
    pw,ph=int(S*2.20), int(S*(3.15 if port else 2.95))
    px,py=m//2-pw//2, int(H*(0.15 if port else 0.17))
    ld=ImageDraw.Draw(left)
    ld.rounded_rectangle([px,py,px+pw,py+ph], radius=28, fill=(24,18,40,255), outline=PURPLE+(255,), width=5)
    mic(ld, m//2, py+int(ph*0.50), int(S*0.72))
    ld.text((m//2, py+int(ph*0.90)), "ฮัมสเกลรัน C", font=F('SemiBold', int(S*0.16)), fill=WHITE, anchor='mm')

    right=bg(W,H,(20,10,30),(40,15,50),2,62)
    rd=ImageDraw.Draw(right)
    cx=m+m//2
    cw,ch=int(m*0.86), int(H*(0.46 if port else 0.40))
    x0,y0=cx-cw//2, int(H*(0.15 if port else 0.17))
    rd.rounded_rectangle([x0,y0,x0+cw,y0+ch], radius=26, fill=(20,12,32,255), outline=PINK+(255,), width=5)
    rd.text((cx, y0+int(S*0.28)), "คะแนนรวม", font=F('Medium', int(S*0.14)), fill=WHITE, anchor='mm')
    rd.text((cx, y0+int(S*0.62)), "79", font=F('Bold', int(S*0.55)), fill=GOLD, anchor='mm')
    # two stats
    yy=y0+int(S*1.10)
    for i,(lab,val) in enumerate((("เสียง","82"),("จังหวะ","74"))):
        x=x0+int(cw*(0.28+i*0.44))
        rd.text((x, yy), val, font=F('Bold', int(S*0.22)), fill=PINK, anchor='mm')
        rd.text((x, yy+int(S*0.28)), lab, font=F('Medium', int(S*0.13)), fill=WHITE, anchor='mm')
    rd.rounded_rectangle([x0+20, y0+ch-int(S*0.38)-14, x0+cw-20, y0+ch-14], radius=14, fill=PURPLE+(255,))
    rd.text((cx, y0+ch-14-int(S*0.19)), "คีย์ C major", font=F('Bold', int(S*0.15)), fill=WHITE, anchor='mm')

    im=right.copy(); im.paste(left.crop((0,0,m,H)),(0,0))
    ov=Image.new('RGBA',(W,H),(0,0,0,0)); od=ImageDraw.Draw(ov); gh=int(H*0.40)
    for i in range(gh): od.line([(0,H-gh+i),(W,H-gh+i)], fill=(10,6,16,int(245*(i/gh)**1.2)))
    im=Image.alpha_composite(im,ov); d=ImageDraw.Draw(im)
    d.rectangle([m-3,0,m+3,H], fill='white')
    cy2=int(H*0.30); d.ellipse([m-34,cy2-34,m+34,cy2+34], fill='white', outline=(0,0,0,60), width=2)
    d.text((m-14,cy2),'◀',font=F('Regular',26),fill=(40,40,40),anchor='mm'); d.text((m+14,cy2),'▶',font=F('Regular',26),fill=(40,40,40),anchor='mm')
    top=int(H*0.09) if port else 100
    pill(d,m//2,top,'BEFORE',(0,0,0,170),'white',F('SemiBold',34),'mm')
    pill(d,m+m//2,top,'AFTER',GOLD+(255,),(30,20,0),F('SemiBold',34),'mm')
    pill(d,W//2,48,'AI วันละแอป · แจกฟรี / Free',(255,255,255,235),(25,25,25),F('Medium',32),'mm')
    chip_y = max(py+ph, y0+ch) + (48 if port else 38)
    pill(d,m//2,chip_y,'แบบฝึกต้นฉบับ ไม่มีเนื้อเพลง',(0,0,0,170),'white',F('Medium',20),'mm')
    pill(d,m+m//2,chip_y,'เสียง 82 · จังหวะ 74',(255,255,255,240),NAVY,F('Medium',22),'mm')
    s=1.0 if port else 0.85
    y=H-int(56*s)
    d.text((W//2,y),'Score your pitch and timing — no bundled lyrics',font=F('Regular',int(30*s)),fill=(230,210,240),anchor='ms'); y-=int(72*s)
    d.text((W//2,y),'ร้องแล้วให้คะแนน + โค้ชเสียง',font=F('SemiBold',int(44*s)),fill=(255,205,90),anchor='ms'); y-=int(92*s)
    d.text((W//2,y),'SingScore',font=F('Bold',int(100*s)),fill='white',anchor='ms',stroke_width=2,stroke_fill=(0,0,0))
    im.convert('RGB').save(name)

make(1080,1350,'cover_1080x1350.png'); make(1080,1080,'cover_1080x1080.png')
print("covers written")
