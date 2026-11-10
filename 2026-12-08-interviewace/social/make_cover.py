"""Procedural cover: left = messy interview notes (BEFORE), right = score 72 + STAR card (AFTER). Illustration only — no real people."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np, math
G='/usr/share/fonts/truetype/sand-box/google/'
F=lambda w,s: ImageFont.truetype(G+'Kanit/Kanit-'+w+'.ttf',s,layout_engine=ImageFont.Layout.RAQM)
AMBER=(255,196,64); WHITE=(255,255,255); CYAN=(56,189,248); GREEN=(52,211,153)
NAVY=(16,24,40); INK=(15,20,30)

def bg(W,H,top,bot,noise,seed):
    yy=np.linspace(0,1,H)[:,None,None]; a=np.array(top)*(1-yy)+np.array(bot)*yy; a=np.repeat(a,W,axis=1)
    a+=np.random.default_rng(seed).normal(0,noise,(H,W,1))
    return Image.fromarray(np.clip(a,0,255).astype('uint8')).convert('RGBA')

def pill(d,x,y,t,bgc,fg,font,anchor):
    b=d.textbbox((x,y),t,font=font,anchor=anchor); p=14
    d.rounded_rectangle([b[0]-p*1.6,b[1]-p,b[2]+p*1.6,b[3]+p], radius=40, fill=bgc); d.text((x,y),t,font=font,fill=fg,anchor=anchor)

def gauge(im,cx,cy,r,val,col,label):
    d=ImageDraw.Draw(im)
    d.ellipse([cx-r,cy-r,cx+r,cy+r], outline=(40,55,80,255), width=int(r*0.18))
    d.arc([cx-r,cy-r,cx+r,cy+r], -90, -90+int(360*val/100), fill=col, width=int(r*0.18))
    d.text((cx, cy-int(r*0.08)), str(val), font=F('Bold', int(r*0.55)), fill=WHITE, anchor='mm')
    d.text((cx, cy+int(r*0.42)), label, font=F('Medium', int(r*0.18)), fill=(200,220,235), anchor='mm')

def make(W,H,name):
    port=H>W; m=W//2; S=int(W*(0.20 if port else 0.17))
    left=bg(W,H,(28,24,40),(12,12,20),3,1)
    ld=ImageDraw.Draw(left)
    # sticky notes + mic
    notes=[(-12, (255,236,170), "STAR??"), (10, (255,200,200), "อ่า เอ่อ..."), (-6, (200,230,255), "ยาวไปไหม")]
    nx0,ny0=int(m*0.16), int(H*(0.20 if port else 0.22))
    for i,(tilt,col,txt) in enumerate(notes):
        nw,nh=int(S*1.35), int(S*1.15)
        c=Image.new('RGBA',(nw+20,nh+20),(0,0,0,0)); d=ImageDraw.Draw(c)
        d.rounded_rectangle([6,6,nw,nh], radius=8, fill=col+(255,), outline=(80,70,50,80), width=2)
        d.text(((nw+6)//2, (nh+6)//2), txt, font=F('Medium', int(S*0.16)), fill=(60,40,30), anchor='mm')
        c=c.rotate(tilt, expand=True, resample=Image.Resampling.BICUBIC)
        left.alpha_composite(c,(nx0+i*int(S*0.15), ny0+i*int(S*0.42)))
    # simple mic
    ld=ImageDraw.Draw(left)
    mx,my=m//2, int(H*(0.58 if port else 0.60))
    ld.rounded_rectangle([mx-int(S*0.22), my-int(S*0.45), mx+int(S*0.22), my+int(S*0.10)], radius=24, fill=(80,90,110,255))
    ld.rectangle([mx-6, my+int(S*0.08), mx+6, my+int(S*0.38)], fill=(180,190,200,255))
    ld.ellipse([mx-int(S*0.22), my+int(S*0.34), mx+int(S*0.22), my+int(S*0.42)], fill=(180,190,200,255))

    right=bg(W,H,(14,28,48),(8,14,26),2,2)
    cx=m+m//2
    gauge(right, cx, int(H*(0.30 if port else 0.32)), int(S*0.95), 72, CYAN, "คะแนนรวม")
    rd=ImageDraw.Draw(right)
    # STAR boxes
    labels=[("S","สถานการณ์"),("T","งานที่ได้รับ"),("A","สิ่งที่ทำ"),("R","ผลลัพธ์")]
    box_w=int(m*0.78); bx=cx-box_w//2; by=int(H*(0.48 if port else 0.50)); bh=int(S*0.38)
    for i,(k,th) in enumerate(labels):
        y=by+i*int(bh*1.15)
        fill = (52,211,153,230) if k!="R" else (248,180,80,230)
        rd.rounded_rectangle([bx,y,bx+box_w,y+bh], radius=12, fill=fill)
        mark = "ครบ" if k!="R" else "ยังขาด"
        rd.text((bx+int(S*0.22), y+bh//2), f"{k}  {th}  · {mark}", font=F('SemiBold', int(S*0.15)), fill=INK, anchor='lm')

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
    chip_y=int(H*(0.58 if port else 0.56))
    pill(d,m//2,chip_y,'ตอบแล้วไม่รู้ผล',(0,0,0,150),'white',F('Medium',26),'mm')
    # right chips sit just under the gauge, above the STAR list
    pill(d,m+m//2,int(H*(0.445 if port else 0.445)),'คะแนน 72 · พร้อมปานกลาง',(255,255,255,240),(20,30,40),F('Medium',22),'mm')
    sc=1.0 if port else 0.85
    y=H-int(60*sc)
    d.text((W//2,y),'Practise interviews, get a score',font=F('Regular',int(40*sc)),fill=(220,230,240),anchor='ms'); y-=int(76*sc)
    d.text((W//2,y),'ซ้อมสัมภาษณ์งานกับ AI',font=F('SemiBold',int(52*sc)),fill=(255,205,90),anchor='ms'); y-=int(100*sc)
    d.text((W//2,y),'InterviewAce',font=F('Bold',int(100*sc)),fill='white',anchor='ms',stroke_width=2,stroke_fill=(0,0,0))
    im.convert('RGB').save(name)

make(1080,1350,'cover_1080x1350.png'); make(1080,1080,'cover_1080x1080.png')
print('covers written')
