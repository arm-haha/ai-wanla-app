"""Procedural cover: left = messy handwritten promo note (BEFORE), right = clean Ficto Café poster (AFTER). Illustration only — no real shops or logos."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
G='/usr/share/fonts/truetype/sand-box/google/'
F=lambda w,s: ImageFont.truetype(G+'Kanit/Kanit-'+w+'.ttf',s,layout_engine=ImageFont.Layout.RAQM)
# a slightly looser hand-like Thai/Latin fallback — Kanit Italic for the note
FI=lambda s: ImageFont.truetype(G+'Kanit/Kanit-MediumItalic.ttf',s,layout_engine=ImageFont.Layout.RAQM)
AMBER=(255,196,64); WHITE=(255,255,255); CREAM=(248,241,227)
BROWN=(74,44,42); ORANGE=(232,119,46); INK=(40,24,22)

def bg(W,H,top,bot,noise,seed):
    yy=np.linspace(0,1,H)[:,None,None]; a=np.array(top)*(1-yy)+np.array(bot)*yy; a=np.repeat(a,W,axis=1)
    a+=np.random.default_rng(seed).normal(0,noise,(H,W,1))
    return Image.fromarray(np.clip(a,0,255).astype('uint8')).convert('RGBA')

def pill(d,x,y,t,bgc,fg,font,anchor):
    b=d.textbbox((x,y),t,font=font,anchor=anchor); p=14
    d.rounded_rectangle([b[0]-p*1.6,b[1]-p,b[2]+p*1.6,b[3]+p], radius=40, fill=bgc); d.text((x,y),t,font=font,fill=fg,anchor=anchor)

def make(W,H,name):
    port=H>W; m=W//2; S=int(W*(0.20 if port else 0.17))
    left=bg(W,H,(70,58,50),(30,24,22),3,1)
    ld=ImageDraw.Draw(left)
    # torn paper note
    nw,nh=int(S*2.15), int(S*2.55)
    nx,ny=m//2-nw//2, int(H*(0.18 if port else 0.20))
    ld.polygon([(nx,ny+20),(nx+18,ny),(nx+nw,ny+12),(nx+nw-10,ny+nh),(nx+8,ny+nh-16)], fill=(236,226,206,255), outline=(90,70,50,255))
    # ruled lines
    for i in range(6):
        yy=ny+int(S*0.55)+i*int(S*0.28)
        ld.line([nx+20,yy,nx+nw-20,yy], fill=(200,190,170,255), width=2)
    ld.text((m//2, ny+int(S*0.45)), "ศุกร์นี้...", font=FI(int(S*0.26)), fill=(90,70,60), anchor='mm')
    ld.text((m//2, ny+int(S*1.05)), "1 แถม 1??", font=FI(int(S*0.32)), fill=(90,40,30), anchor='mm')
    ld.text((m//2, ny+int(S*1.55)), "เก้าโมง-เย็น", font=FI(int(S*0.20)), fill=(90,70,60), anchor='mm')
    ld.text((m//2, ny+int(S*1.95)), "ซอย... (ลืมเลข)", font=FI(int(S*0.18)), fill=(120,80,70), anchor='mm')

    right=bg(W,H,(58,32,28),(28,16,14),2,2)
    rd=ImageDraw.Draw(right)
    cx=m+m//2
    pw,ph=int(m*0.78), int(S*3.25)
    px,py=cx-pw//2, int(H*(0.14 if port else 0.16))
    rd.rounded_rectangle([px,py,px+pw,py+ph], radius=18, fill=CREAM+(255,), outline=BROWN+(255,), width=8)
    # badge
    rd.rounded_rectangle([px+int(S*0.22), py+int(S*0.22), px+pw-int(S*0.22), py+int(S*0.55)], radius=20, fill=ORANGE+(255,))
    rd.text((cx, py+int(S*0.38)), "ทุกวันศุกร์", font=F('SemiBold', int(S*0.16)), fill=WHITE, anchor='mm')
    rd.text((cx, py+int(S*0.90)), "โปรศุกร์", font=F('Bold', int(S*0.30)), fill=BROWN, anchor='mm')
    rd.text((cx, py+int(S*1.28)), "1 แถม 1", font=F('Bold', int(S*0.42)), fill=ORANGE, anchor='mm')
    rd.text((cx, py+int(S*1.70)), "เครื่องดื่มทุกแก้ว", font=F('Medium', int(S*0.18)), fill=BROWN, anchor='mm')
    rd.line([px+int(S*0.35), py+int(S*1.92), px+pw-int(S*0.35), py+int(S*1.92)], fill=BROWN+(180,), width=2)
    rd.text((cx, py+int(S*2.15)), "09:00–18:00", font=F('SemiBold', int(S*0.20)), fill=BROWN, anchor='mm')
    rd.text((cx, py+int(S*2.42)), "ซอยสุขใจ 12", font=F('Medium', int(S*0.16)), fill=BROWN, anchor='mm')
    # fake QR
    q=int(S*0.42); qx,qy=cx-q//2, py+ph-int(S*0.70)
    rd.rounded_rectangle([qx,qy,qx+q,qy+q], radius=4, fill=(30,20,18,255))
    for i in range(3):
        for j in range(3):
            if (i+j)%2==0:
                rd.rectangle([qx+8+i*(q-16)//3, qy+8+j*(q-16)//3, qx+8+(i+1)*(q-16)//3-4, qy+8+(j+1)*(q-16)//3-4], fill=(240,230,210,255))

    im=right.copy(); im.paste(left.crop((0,0,m,H)),(0,0))
    ov=Image.new('RGBA',(W,H),(0,0,0,0)); od=ImageDraw.Draw(ov); gh=int(H*0.42)
    for i in range(gh):
        od.line([(0,H-gh+i),(W,H-gh+i)], fill=(20,10,8,int(245*(i/gh)**1.2)))
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
    pill(d,m//2,chip_y,'โน้ตเขียนลวก ๆ',(0,0,0,150),'white',F('Medium',28),'mm')
    pill(d,m+m//2,chip_y,'โปสเตอร์พร้อมลง',(255,255,255,240),(40,30,10),F('Medium',26),'mm')
    pill(d,m+m//2,chip_y+70,'โปรศุกร์ 1 แถม 1',ORANGE+(255,),WHITE,F('SemiBold',26),'mm')
    sc=1.0 if port else 0.85
    y=H-int(60*sc)
    d.text((W//2,y),'Type the brief, get a Thai poster',font=F('Regular',int(40*sc)),fill=(235,230,220),anchor='ms'); y-=int(76*sc)
    d.text((W//2,y),'พิมพ์รายละเอียดงาน ได้โปสเตอร์สวยทันที',font=F('SemiBold',int(44*sc)),fill=(255,205,90),anchor='ms'); y-=int(100*sc)
    d.text((W//2,y),'PosterPop',font=F('Bold',int(110*sc)),fill='white',anchor='ms',stroke_width=2,stroke_fill=(0,0,0))
    im.convert('RGB').save(name)

make(1080,1350,'cover_1080x1350.png'); make(1080,1080,'cover_1080x1080.png')
print('covers written')
