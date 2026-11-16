"""Procedural cover: left = an empty condo balcony with a wilted pot (BEFORE), right = the same balcony as a kitchen garden + sun/load chips (AFTER). Illustration only — no real people or brands."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np, math
G='/usr/share/fonts/truetype/sand-box/google/'
F=lambda w,s: ImageFont.truetype(G+'Kanit/Kanit-'+w+'.ttf',s,layout_engine=ImageFont.Layout.RAQM)
LEAF=(63,163,77); LEAF2=(110,200,100); LEAF3=(40,120,60); SUN=(255,181,71); CLAY=(200,105,63); INK=(31,58,43); WHITE=(255,255,255)

def bg(W,H,top,bot,noise,seed):
    yy=np.linspace(0,1,H)[:,None,None]; a=np.array(top)*(1-yy)+np.array(bot)*yy; a=np.repeat(a,W,axis=1)
    a+=np.random.default_rng(seed).normal(0,noise,(H,W,1))
    return Image.fromarray(np.clip(a,0,255).astype('uint8')).convert('RGBA')

def pill(d,x,y,t,bgc,fg,font,anchor):
    b=d.textbbox((x,y),t,font=font,anchor=anchor); p=14
    d.rounded_rectangle([b[0]-p*1.6,b[1]-p,b[2]+p*1.6,b[3]+p], radius=40, fill=bgc); d.text((x,y),t,font=font,fill=fg,anchor=anchor)

def balcony(im,x0,x1,floor_y,H,garden,seed):
    d=ImageDraw.Draw(im); w=x1-x0
    # far buildings
    rng=np.random.default_rng(seed)
    for k in range(5):
        bx=x0+int(w*k/5)+int(rng.uniform(-10,10)); bh=int(H*rng.uniform(0.18,0.32))
        col=(150,165,185,255) if not garden else (170,200,215,255)
        d.rectangle([bx,floor_y-int(H*0.10)-bh,bx+int(w/5)-14,floor_y-int(H*0.10)],fill=col)
        for r in range(4):
            for c in range(3):
                wx=bx+14+c*int((w/5-40)/3); wy=floor_y-int(H*0.10)-bh+16+r*34
                if wy<floor_y-int(H*0.12): d.rectangle([wx,wy,wx+18,wy+20],fill=(210,220,235,255))
    # floor
    d.polygon([(x0,floor_y),(x1,floor_y),(x1,H),(x0,H)],fill=(205,190,170,255) if garden else (170,165,160,255))
    for k in range(1,8):
        d.line([(x0,floor_y+k*40),(x1,floor_y+k*40)],fill=(185,170,150,255),width=2)
    # railing
    ry=floor_y-int(H*0.10)
    d.rectangle([x0,ry,x1,ry+10],fill=(90,95,100,255))
    for k in range(0,w,38): d.rectangle([x0+k,ry,x0+k+6,floor_y],fill=(110,115,120,255))
    if not garden:
        # clothes rack + wilted pot
        d.line([(x0+40,ry-120),(x0+w-40,ry-120)],fill=(200,200,200,255),width=5)
        for k,c in enumerate([(120,140,200),(220,220,220),(200,120,120)]):
            cx=x0+90+k*90; d.polygon([(cx-30,ry-118),(cx+30,ry-118),(cx+24,ry-40),(cx-24,ry-40)],fill=c+(255,))
        px=x0+w//2; py=floor_y+90
        d.polygon([(px-45,py-60),(px+45,py-60),(px+34,py+20),(px-34,py+20)],fill=CLAY+(255,))
        for a in (-0.9,-0.4,0.3,0.8):
            d.line([(px,py-60),(px+int(60*math.sin(a)),py-60+int(50*abs(math.cos(a))))],fill=(150,130,60,255),width=6)
            d.ellipse([px+int(60*math.sin(a))-12,py-60+int(50*abs(math.cos(a)))-6,px+int(60*math.sin(a))+12,py-60+int(50*abs(math.cos(a)))+8],fill=(170,150,70,255))
        return
    # string lights
    for k in range(9):
        lx=x0+30+k*int((w-60)/8); ly=ry-140+int(18*math.sin(k*0.8))
        d.ellipse([lx-8,ly-8,lx+8,ly+8],fill=(255,230,150,255))
    d.line([(x0+30,ry-140),(x1-30,ry-140)],fill=(80,70,60,255),width=2)
    # pots row along railing (inside) + front row
    pots=[(0.12,0.85,CLAY),(0.32,1.1,(240,240,235)),(0.52,0.9,CLAY),(0.72,1.2,(240,240,235)),(0.90,0.8,CLAY)]
    for i,(fx,sc,pc) in enumerate(pots):
        px=x0+int(w*fx); py=floor_y+40; s=int(46*sc)
        for j in range(14):
            ang=-math.pi*(0.05+0.9*j/13); L=s*rng.uniform(1.4,2.4)
            lx=px+int(L*math.cos(ang)); ly=py-s-int(L*0.9*abs(math.sin(ang)))
            col=[LEAF,LEAF2,LEAF3][j%3]
            d.ellipse([lx-int(s*0.35),ly-int(s*0.22),lx+int(s*0.35),ly+int(s*0.22)],fill=col+(255,))
            d.line([(px,py-s),(lx,ly)],fill=LEAF3+(255,),width=3)
        d.polygon([(px-s,py-s),(px+s,py-s),(px+int(s*0.75),py+int(s*0.6)),(px-int(s*0.75),py+int(s*0.6))],fill=pc+(255,))
        d.rectangle([px-s-4,py-s-8,px+s+4,py-s+4],fill=tuple(max(0,c-30) for c in pc)+(255,))
    # front planter box
    bx0,bx1=x0+int(w*0.18),x0+int(w*0.82); by=floor_y+170
    for k in range(22):
        lx=bx0+20+k*int((bx1-bx0-40)/21); d.ellipse([lx-16,by-60-(k%3)*14,lx+16,by-20-(k%3)*14],fill=[LEAF2,LEAF][k%2]+(255,))
    d.rounded_rectangle([bx0,by-24,bx1,by+40],radius=10,fill=(150,100,60,255))

def make(W,H,name):
    port=H>W; m=W//2
    floor_y=int(H*(0.50 if port else 0.50))
    left=bg(W,H,(170,180,190),(110,115,125),3,1); balcony(left,0,m,floor_y,H,False,3)
    right=bg(W,H,(255,226,160),(140,200,230),2,2); balcony(right,m,W,floor_y,H,True,3)
    rd=ImageDraw.Draw(right); sx,sy=W-110,int(H*0.17); rd.ellipse([sx-50,sy-50,sx+50,sy+50],fill=SUN+(255,))
    for k in range(12):
        a=k*math.pi/6; rd.line([(sx+62*math.cos(a),sy+62*math.sin(a)),(sx+84*math.cos(a),sy+84*math.sin(a))],fill=SUN+(255,),width=6)
    im=right.copy(); im.paste(left.crop((0,0,m,H)),(0,0))
    ov=Image.new('RGBA',(W,H),(0,0,0,0)); od=ImageDraw.Draw(ov); gh=int(H*0.40)
    for i in range(gh):
        od.line([(0,H-gh+i),(W,H-gh+i)], fill=(14,30,20,int(248*(i/gh)**1.1)))
    im=Image.alpha_composite(im,ov); d=ImageDraw.Draw(im)
    d.rectangle([m-3,0,m+3,H], fill='white')
    cy2=int(H*0.32); d.ellipse([m-34,cy2-34,m+34,cy2+34], fill='white', outline=(0,0,0,60), width=2)
    d.text((m-14,cy2),'◀',font=F('Regular',26),fill=(40,40,40),anchor='mm'); d.text((m+14,cy2),'▶',font=F('Regular',26),fill=(40,40,40),anchor='mm')
    top=int(H*0.10) if port else 120
    pill(d,m//2,top,'BEFORE',(0,0,0,170),'white',F('SemiBold',34),'mm')
    pill(d,m+m//2,top,'AFTER',LEAF+(255,),'white',F('SemiBold',34),'mm')
    pill(d,W//2,52,'AI วันละแอป · แจกฟรี / Free',(255,255,255,235),(25,25,25),F('Medium',32),'mm')
    chip_y=int(H*(0.60 if port else 0.63))
    pill(d,m//2,chip_y,'ปลูกอะไรก็ตาย',(0,0,0,170),'white',F('Medium',26),'mm')
    pill(d,m+m//2,chip_y,'แดด 3.8 ชม. · ผัก 5 อย่าง · ฿397',(255,255,255,240),INK,F('Medium',26),'mm')
    sc=1.0 if port else 0.85; y=H-int(60*sc)
    d.text((W//2,y),'Snap your balcony, see your herb garden first',font=F('Regular',int(36*sc)),fill=(225,245,225),anchor='ms'); y-=int(76*sc)
    d.text((W//2,y),'ถ่ายระเบียง เห็นสวนผักก่อนปลูก',font=F('SemiBold',int(46*sc)),fill=(170,235,150),anchor='ms'); y-=int(100*sc)
    d.text((W//2,y),'BalconyFarm',font=F('Bold',int(110*sc)),fill='white',anchor='ms',stroke_width=2,stroke_fill=(0,0,0))
    im.convert('RGB').save(name)

make(1080,1350,'cover_1080x1350.png'); make(1080,1080,'cover_1080x1080.png')
print('covers written')
