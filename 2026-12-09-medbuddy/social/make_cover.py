"""Procedural cover: left = messy fictional envelopes (BEFORE), right = clean morning/evening schedule (AFTER). Illustration only — no real meds, people or brands."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
G='/usr/share/fonts/truetype/sand-box/google/'
F=lambda w,s: ImageFont.truetype(G+'Kanit/Kanit-'+w+'.ttf',s,layout_engine=ImageFont.Layout.RAQM)
AMBER=(255,196,64); WHITE=(255,255,255); BLUE=(37,99,235); GREEN=(22,163,74)
INK=(17,24,39); CREAM=(246,248,251)

def bg(W,H,top,bot,noise,seed):
    yy=np.linspace(0,1,H)[:,None,None]; a=np.array(top)*(1-yy)+np.array(bot)*yy; a=np.repeat(a,W,axis=1)
    a+=np.random.default_rng(seed).normal(0,noise,(H,W,1))
    return Image.fromarray(np.clip(a,0,255).astype('uint8')).convert('RGBA')

def pill(d,x,y,t,bgc,fg,font,anchor):
    b=d.textbbox((x,y),t,font=font,anchor=anchor); p=14
    d.rounded_rectangle([b[0]-p*1.6,b[1]-p,b[2]+p*1.6,b[3]+p], radius=40, fill=bgc); d.text((x,y),t,font=font,fill=fg,anchor=anchor)

def envelope(im,x,y,w,h,tilt,title,sub,col):
    c=Image.new('RGBA',(w+30,h+30),(0,0,0,0)); d=ImageDraw.Draw(c)
    d.rounded_rectangle([8,8,w+8,h+8], radius=10, fill=col, outline=(255,255,255,200), width=3)
    d.rectangle([8,8,w+8,8+int(h*0.22)], fill=(255,255,255,80))
    d.text((8+w//2, 8+int(h*0.13)), title, font=F('SemiBold', max(14, w//9)), fill=WHITE, anchor='mm')
    d.text((8+w//2, 8+int(h*0.55)), sub, font=F('Medium', max(12, w//11)), fill=(255,255,255,230), anchor='mm')
    # small pill icon
    d.rounded_rectangle([8+w//2-16, 8+int(h*0.72), 8+w//2+16, 8+int(h*0.86)], radius=10, fill=(255,255,255,200))
    if tilt:
        c=c.rotate(tilt, expand=True, resample=Image.Resampling.BICUBIC)
    im.alpha_composite(c,(x,y))

def make(W,H,name):
    port=H>W; m=W//2; S=int(W*(0.20 if port else 0.17))
    left=bg(W,H,(40,36,48),(18,16,24),3,1)
    envelope(left, int(m*0.08), int(H*0.18), int(S*1.55), int(S*1.05), -16, "FictoPril", "5 mg ?", (90,80,120,255))
    envelope(left, int(m*0.22), int(H*0.30), int(S*1.60), int(S*1.05), 12, "FictoMet", "?? เม็ด", (80,100,90,255))
    envelope(left, int(m*0.10), int(H*0.42), int(S*1.50), int(S*1.00), -6, "FictoPain", "เมื่อปวด?", (120,80,80,255))

    right=bg(W,H,(20,36,64),(10,18,32),2,2)
    rd=ImageDraw.Draw(right)
    cx=m+m//2
    pw,ph=int(m*0.82), int(S*3.20)
    px,py=cx-pw//2, int(H*(0.14 if port else 0.16))
    rd.rounded_rectangle([px,py,px+pw,py+ph], radius=24, fill=CREAM+(255,), outline=BLUE+(255,), width=5)
    rd.text((cx, py+int(S*0.28)), "ตารางวันนี้", font=F('SemiBold', int(S*0.20)), fill=INK, anchor='mm')
    rows=[("เช้า", "FictoPril + FictoMet", BLUE),
          ("เย็น", "FictoMet 500 mg", (14,116,144)),
          ("เมื่อปวด", "FictoPain 500 mg", (180,120,40))]
    y=py+int(S*0.52)
    row_h=int((ph-int(S*0.70))/3)
    for label, body, col in rows:
        rd.rounded_rectangle([px+18, y, px+pw-18, y+row_h-12], radius=14, fill=col+(255,))
        rd.text((px+36, y+int(row_h*0.22)), label, font=F('SemiBold', int(S*0.16)), fill=WHITE, anchor='lt')
        rd.text((px+36, y+int(row_h*0.58)), body, font=F('Medium', int(S*0.13)), fill=(240,248,255), anchor='lt')
        y += row_h

    im=right.copy(); im.paste(left.crop((0,0,m,H)),(0,0))
    ov=Image.new('RGBA',(W,H),(0,0,0,0)); od=ImageDraw.Draw(ov); gh=int(H*0.42)
    for i in range(gh):
        od.line([(0,H-gh+i),(W,H-gh+i)], fill=(8,12,20,int(245*(i/gh)**1.2)))
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
    pill(d,m//2,chip_y,'ซองยากองบนโต๊ะ',(0,0,0,150),'white',F('Medium',26),'mm')
    pill(d,m+m//2,chip_y,'ตารางเช้า-เย็นครบ',(255,255,255,240),(20,30,40),F('Medium',24),'mm')
    pill(d,m+m//2,chip_y+70,'ห้ามเปลี่ยนขนาดยาเอง',(220,38,38,255),WHITE,F('SemiBold',22),'mm')
    sc=1.0 if port else 0.85
    y=H-int(60*sc)
    d.text((W//2,y),'Scan the envelope, get a family schedule',font=F('Regular',int(36*sc)),fill=(220,230,240),anchor='ms'); y-=int(76*sc)
    d.text((W//2,y),'ถ่ายซองยาพ่อแม่ ได้ตารางกินยา',font=F('SemiBold',int(46*sc)),fill=(255,205,90),anchor='ms'); y-=int(100*sc)
    d.text((W//2,y),'MedBuddy',font=F('Bold',int(110*sc)),fill='white',anchor='ms',stroke_width=2,stroke_fill=(0,0,0))
    im.convert('RGB').save(name)

make(1080,1350,'cover_1080x1350.png'); make(1080,1080,'cover_1080x1080.png')
print('covers written')
