"""Procedural cover: left = bare natural nails (BEFORE), right = same illustrated hand with AI try-on nails + 9-design mini grid (AFTER). Fictional illustrated hand only — no real photos."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np, math
G='/usr/share/fonts/truetype/sand-box/google/'
F=lambda w,s: ImageFont.truetype(G+'Kanit/Kanit-'+w+'.ttf',s,layout_engine=ImageFont.Layout.RAQM)
PINK=(232,69,122); CREAM=(255,247,243); INK=(42,30,34); GOLD=(201,162,77)
SKIN=(234,190,158); SKIN_SH=(214,166,134); NAIL_BARE=(240,205,192)
GRID=[('#F3DCCB','#FFF6EE'),('#F7E1D7','#FFFFFF'),('#E9D3A6','#C9A24D'),('#C0603F','#C0603F'),('#D9BFA6','#D9BFA6'),
      ('#6B7B4B','#6B7B4B'),('#F59E7E','#FFE1D2'),('#F9D5DC','#FFFFFF'),('#7FD3E6','#F6A6C1')]
# AFTER hand mixes 5 of the 9 try-on designs: thumb=top pick milky nude pearl, then cherry red, gold chrome, lavender, songkran
MIX=[('#F3DCCB','#FFFFFF'),('#B3122E','#B3122E'),('#C9A24D','#E9D3A6'),('#B79FDB','#B79FDB'),('#7FD3E6','#F6A6C1')]
hx=lambda h:tuple(int(h[i:i+2],16) for i in (1,3,5))

def nail(d,x,y,w,h,fill,tip=None,painted=False):
    """Squoval nail with base at (x,y) bottom-centre, growing upward."""
    d.rounded_rectangle([x-w/2,y-h,x+w/2,y],radius=int(w*0.42),fill=fill,outline=(196,140,130) if painted else None,width=max(1,int(w*0.04)))
    if tip:  # french / ombré tip
        d.rounded_rectangle([x-w/2,y-h,x+w/2,y-h*0.62],radius=int(w*0.42),fill=tip)
    if painted:  # glossy highlight
        d.rounded_rectangle([x-w*0.28,y-h*0.86,x-w*0.12,y-h*0.25],radius=int(w*0.08),fill=(255,255,255,170))
        if w>30:
            for fx,fy in ((0.18,0.5),(0.05,0.3),(0.25,0.75)): d.ellipse([x+w*fx-2,y-h*fy-2,x+w*fx+2,y-h*fy+2],fill=(255,250,235,230))
    else:
        d.arc([x-w*0.45,y-h*0.35,x+w*0.45,y+h*0.05],200,340,fill=(250,235,228),width=max(2,int(w*0.06)))

def hand(W,H,cx,cy,S,paint=None):
    """Back of a left hand, fingers up. paint=list of 5 (base,tip) hex pairs [thumb,index,middle,ring,pinky] or None for bare nails."""
    L=Image.new('RGBA',(W,H),(0,0,0,0))
    # fingers: (dx from palm centre, angle deg, length, width)
    fingers=[(-0.78,14,1.55,0.42),(-0.27,4,1.85,0.46),(0.25,-3,1.95,0.47),(0.74,-11,1.7,0.44)]
    for fi,(dx,ang,ln,wd) in enumerate(fingers):
        f=Image.new('RGBA',(W,H),(0,0,0,0)); fd=ImageDraw.Draw(f)
        bx=cx+dx*S; by=cy-S*0.55; w=wd*S; l=ln*S
        fd.rounded_rectangle([bx-w/2,by-l,bx+w/2,by+S*0.3],radius=int(w/2),fill=SKIN)
        for k in (0.35,0.65): fd.arc([bx-w*0.3,by-l*k-w*0.12,bx+w*0.3,by-l*k+w*0.12],200,340,fill=SKIN_SH,width=max(2,int(S*0.02)))
        nw,nh=w*0.74,l*0.33; ny=by-l+w*0.18+nh
        if paint: pb,pt=paint[fi+1]; nail(fd,bx,ny,nw,nh,hx(pb),hx(pt) if pt!=pb else None,True)
        else: nail(fd,bx,ny,nw,nh,NAIL_BARE)
        L.alpha_composite(f.rotate(ang,center=(bx,by+S*0.2),resample=Image.BICUBIC))
    d=ImageDraw.Draw(L)
    # palm + wrist
    d.rounded_rectangle([cx-S*1.05,cy-S*0.75,cx+S*1.05,cy+S*1.05],radius=int(S*0.55),fill=SKIN)
    d.rounded_rectangle([cx-S*0.8,cy+S*0.6,cx+S*0.75,cy+S*2.6],radius=int(S*0.3),fill=SKIN)
    for i,dx in enumerate((-0.6,-0.2,0.22,0.62)): d.arc([cx+dx*S-S*0.12,cy-S*0.7,cx+dx*S+S*0.12,cy-S*0.5],200,340,fill=SKIN_SH,width=max(2,int(S*0.025)))
    # thumb (on the right for back of left hand)
    t=Image.new('RGBA',(W,H),(0,0,0,0)); td=ImageDraw.Draw(t)
    bx=cx+S*1.0; by=cy+S*0.35; w=S*0.5; l=S*1.35
    td.rounded_rectangle([bx-w/2,by-l,bx+w/2,by+S*0.2],radius=int(w/2),fill=SKIN)
    nw,nh=w*0.74,l*0.34; ny=by-l+w*0.18+nh
    if paint: pb,pt=paint[0]; nail(td,bx,ny,nw,nh,hx(pb),hx(pt) if pt!=pb else None,True)
    else: nail(td,bx,ny,nw,nh,NAIL_BARE)
    L.alpha_composite(t.rotate(-38,center=(bx,by),resample=Image.BICUBIC))
    # soft shadow under hand
    sh=L.split()[3].filter(ImageFilter.GaussianBlur(S*0.12)).point(lambda a:int(a*0.35))
    base=Image.new('RGBA',(W,H),(60,30,30,0)); base.putalpha(sh); base=base.transform((W,H),Image.AFFINE,(1,0,-S*0.06,0,1,-S*0.08))
    base.alpha_composite(L); return base

def bg(W,H,col,noise,seed):
    a=np.zeros((H,W,3)); a[:]=np.array(col); yy,xx=np.mgrid[0:H,0:W]
    a*= (1-0.10*(yy/H))[...,None]; a+=np.random.default_rng(seed).normal(0,noise,(H,W,1))
    return Image.fromarray(np.clip(a,0,255).astype('uint8')).convert('RGBA')

def make(W,H,name):
    port=H>W; m=W//2; S=int(min(W,H)*(0.105 if port else 0.088)); cy=int(H*(0.40 if port else 0.40))
    cxl=m//2-S*0.1; cxr=m+m//2-S*0.1
    left=bg(W,H,(222,206,190),5,1); left.alpha_composite(hand(W,H,cxl,cy,S))
    right=bg(W,H,CREAM,2,2); rd=ImageDraw.Draw(right)
    for i,(x,y,r) in enumerate([(0.62,0.16,9),(0.92,0.24,6),(0.58,0.48,7),(0.95,0.52,10),(0.70,0.08,5)]):
        X,Y=W*x,H*y; rd.polygon([(X,Y-r*2),(X+r*0.5,Y-r*0.5),(X+r*2,Y),(X+r*0.5,Y+r*0.5),(X,Y+r*2),(X-r*0.5,Y+r*0.5),(X-r*2,Y),(X-r*0.5,Y-r*0.5)],fill=GOLD+(200,))
    right.alpha_composite(hand(W,H,cxr,cy,S,paint=MIX))
    im=right.copy(); im.paste(left.crop((0,0,m,H)),(0,0))
    d=ImageDraw.Draw(im)
    # mini 3x3 try-on grid card (bottom-right of AFTER half)
    cs=int(S*0.46); gp=int(cs*0.22); gw=3*cs+4*gp
    gx=W-gw-int(W*0.03); gy=int(H*(0.60 if port else 0.585))-50-gw
    d.rounded_rectangle([gx,gy,gx+gw,gy+gw],radius=18,fill=(255,255,255,240),outline=PINK+(255,),width=3)
    for i,(b,t) in enumerate(GRID):
        r,c=divmod(i,3); x=gx+gp+c*(cs+gp); y=gy+gp+r*(cs+gp)
        d.rounded_rectangle([x,y,x+cs,y+cs],radius=8,fill=(244,232,226))
        nail(d,x+cs/2,y+cs*0.9,cs*0.5,cs*0.78,hx(b),hx(t) if t!=b else None,True)
        if i==0: d.rounded_rectangle([x-3,y-3,x+cs+3,y+cs+3],radius=10,outline=PINK+(255,),width=4)
    ov=Image.new('RGBA',(W,H),(0,0,0,0)); od=ImageDraw.Draw(ov); gh=int(H*0.40)
    for i in range(gh): od.line([(0,H-gh+i),(W,H-gh+i)],fill=(45,15,30,int(240*(i/gh)**1.3)))
    im=Image.alpha_composite(im,ov); d=ImageDraw.Draw(im)
    d.rectangle([m-3,0,m+3,H],fill='white')
    cy2=int(H*0.30); d.ellipse([m-34,cy2-34,m+34,cy2+34],fill='white',outline=(0,0,0,60),width=2)
    d.text((m-14,cy2),'◀',font=F('Regular',26),fill=(40,40,40),anchor='mm'); d.text((m+14,cy2),'▶',font=F('Regular',26),fill=(40,40,40),anchor='mm')
    def pill(x,y,t,bg,fg,font,anchor):
        b=d.textbbox((x,y),t,font=font,anchor=anchor); p=14
        d.rounded_rectangle([b[0]-p*1.6,b[1]-p,b[2]+p*1.6,b[3]+p],radius=40,fill=bg); d.text((x,y),t,font=font,fill=fg,anchor=anchor)
    top=int(H*0.10) if port else 120
    pill(m//2,top,'BEFORE',(0,0,0,170),'white',F('SemiBold',34),'mm')
    pill(m+m//2,top,'AFTER',PINK+(255,),'white',F('SemiBold',34),'mm')
    pill(W//2,52,'AI วันละแอป · แจกฟรี / Free',(255,255,255,235),(25,25,25),F('Medium',32),'mm')
    chip_y=int(H*(0.60 if port else 0.585))
    pill(m//2,chip_y,'เล็บเปล่า · ไม่รู้จะทำสีไหน',(0,0,0,150),'white',F('Medium',28),'mm')
    pill(m+m//2,chip_y,'อันดับ 1 นู้ดมิลค์กี้มุก · ~฿450–850',(255,255,255,240),(90,30,50),F('Medium',25),'mm')
    pill(m+m//2,chip_y+70,'Fit 100 · เพื่อนโหวต 60%',PINK+(255,),'white',F('SemiBold',29),'mm')
    s=1.0 if port else 0.85
    y=H-int(60*s)
    d.text((W//2,y),'1 hand photo → 9 nail designs in seconds',font=F('Regular',int(42*s)),fill=(245,235,240),anchor='ms'); y-=int(76*s)
    d.text((W//2,y),'ถ่ายมือ 1 รูป → ลองเล็บ 9 แบบในไม่กี่วิ',font=F('SemiBold',int(56*s)),fill=(255,170,200),anchor='ms'); y-=int(100*s)
    d.text((W//2,y),'NailPop',font=F('Bold',int(120*s)),fill='white',anchor='ms',stroke_width=2,stroke_fill=(0,0,0))
    im.convert('RGB').save(name)
make(1080,1350,'cover_1080x1350.png'); make(1080,1080,'cover_1080x1080.png')
