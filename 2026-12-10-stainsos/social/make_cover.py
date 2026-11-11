"""Procedural cover: left = white shirt with a Thai-tea stain (BEFORE), right = clean shirt + rescue steps card (AFTER). Illustration only — no real people or brands."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
G='/usr/share/fonts/truetype/sand-box/google/'
F=lambda w,s: ImageFont.truetype(G+'Kanit/Kanit-'+w+'.ttf',s,layout_engine=ImageFont.Layout.RAQM)
AMBER=(255,196,64); WHITE=(255,255,255); SKY=(14,165,233); GREEN=(22,163,74); TEA=(217,119,6)
INK=(15,23,42); CREAM=(247,247,242)

def bg(W,H,top,bot,noise,seed):
    yy=np.linspace(0,1,H)[:,None,None]; a=np.array(top)*(1-yy)+np.array(bot)*yy; a=np.repeat(a,W,axis=1)
    a+=np.random.default_rng(seed).normal(0,noise,(H,W,1))
    return Image.fromarray(np.clip(a,0,255).astype('uint8')).convert('RGBA')

def pill(d,x,y,t,bgc,fg,font,anchor):
    b=d.textbbox((x,y),t,font=font,anchor=anchor); p=14
    d.rounded_rectangle([b[0]-p*1.6,b[1]-p,b[2]+p*1.6,b[3]+p], radius=40, fill=bgc); d.text((x,y),t,font=font,fill=fg,anchor=anchor)

def shirt(im,cx,top,w,stain):
    h=int(w*1.05); c=Image.new('RGBA',im.size,(0,0,0,0)); d=ImageDraw.Draw(c)
    x0,x1=cx-w//2,cx+w//2; sl=int(w*0.28)
    body=[(x0+sl//2,top+int(h*0.12)),(cx-int(w*0.12),top),(cx+int(w*0.12),top),(x1-sl//2,top+int(h*0.12)),
          (x1+sl//3,top+int(h*0.34)),(x1-sl//3,top+int(h*0.42)),(x1-sl//2,top+int(h*0.32)),(x1-sl//2,top+h),
          (x0+sl//2,top+h),(x0+sl//2,top+int(h*0.32)),(x0+sl//3,top+int(h*0.42)),(x0-sl//3,top+int(h*0.34))]
    d.polygon(body, fill=(250,250,248,255), outline=(200,205,215,255))
    d.line([(cx,top+int(h*0.06)),(cx,top+h)], fill=(215,218,225,255), width=3)
    for k in range(5):
        y=top+int(h*(0.18+0.16*k)); d.ellipse([cx-7,y-7,cx+7,y+7], fill=(225,228,235,255))
    d.chord([cx-int(w*0.12),top-int(w*0.08),cx+int(w*0.12),top+int(w*0.10)],0,180,fill=(235,238,243,255))
    if stain:
        s=Image.new('RGBA',im.size,(0,0,0,0)); sd=ImageDraw.Draw(s); rng=np.random.default_rng(3)
        sx,sy=cx-int(w*0.18),top+int(h*0.45); r=int(w*0.13)
        sd.ellipse([sx-r,sy-int(r*0.8),sx+r,sy+int(r*0.9)], fill=TEA+(200,))
        for _ in range(9):
            a=rng.uniform(0,6.28); dd=rng.uniform(r*0.9,r*1.7); rr=int(rng.uniform(r*0.10,r*0.28))
            px,py=int(sx+dd*np.cos(a)),int(sy+dd*np.sin(a)); sd.ellipse([px-rr,py-rr,px+rr,py+rr], fill=TEA+(170,))
        s=s.filter(ImageFilter.GaussianBlur(3)); c.alpha_composite(s)
    im.alpha_composite(c)

def make(W,H,name):
    port=H>W; m=W//2; S=int(W*(0.20 if port else 0.17))
    left=bg(W,H,(60,44,30),(28,20,14),3,1)
    shirt(left, m//2, int(H*0.17), int(m*0.78), True)
    right=bg(W,H,(12,74,110),(8,30,50),2,2); rd=ImageDraw.Draw(right)
    shirt(right, m+m//2, int(H*0.15), int(m*0.62), False)
    # bubbles
    rng=np.random.default_rng(7)
    for _ in range(18):
        bx=int(rng.uniform(m+20,W-20)); by=int(rng.uniform(H*0.10,H*0.55)); br=int(rng.uniform(6,22))
        rd.ellipse([bx-br,by-br,bx+br,by+br], outline=(224,242,254,200), width=3)
    cx=m+m//2; pw=int(m*0.86); px=cx-pw//2; py=int(H*(0.40 if port else 0.37)); ph=int(S*1.55)
    rd.rounded_rectangle([px,py,px+pw,py+ph], radius=22, fill=CREAM+(245,), outline=SKY+(255,), width=4)
    rows=[("1","ซับ ห้ามขยี้",SKY),("2","น้ำยาล้างจาน 3 นาที",SKY),("3","แช่ 30 นาที",GREEN)]
    y=py+int(S*0.12); rh=int((ph-int(S*0.2))/3)
    for n,t,col in rows:
        rd.ellipse([px+16,y+6,px+16+rh-16,y+rh-10], fill=col+(255,))
        rd.text((px+16+(rh-16)//2,y+(rh-4)//2),n,font=F('SemiBold',int(rh*0.42)),fill=WHITE,anchor='mm')
        rd.text((px+rh+10,y+(rh-4)//2),t,font=F('Medium',int(S*0.14)),fill=INK,anchor='lm'); y+=rh
    im=right.copy(); im.paste(left.crop((0,0,m,H)),(0,0))
    ov=Image.new('RGBA',(W,H),(0,0,0,0)); od=ImageDraw.Draw(ov); gh=int(H*0.40)
    for i in range(gh):
        od.line([(0,H-gh+i),(W,H-gh+i)], fill=(6,12,20,int(245*(i/gh)**1.2)))
    im=Image.alpha_composite(im,ov); d=ImageDraw.Draw(im)
    d.rectangle([m-3,0,m+3,H], fill='white')
    cy2=int(H*0.32); d.ellipse([m-34,cy2-34,m+34,cy2+34], fill='white', outline=(0,0,0,60), width=2)
    d.text((m-14,cy2),'◀',font=F('Regular',26),fill=(40,40,40),anchor='mm'); d.text((m+14,cy2),'▶',font=F('Regular',26),fill=(40,40,40),anchor='mm')
    top=int(H*0.10) if port else 120
    pill(d,m//2,top,'BEFORE',(0,0,0,170),'white',F('SemiBold',34),'mm')
    pill(d,m+m//2,top,'AFTER',AMBER+(255,),(30,20,0),F('SemiBold',34),'mm')
    pill(d,W//2,52,'AI วันละแอป · แจกฟรี / Free',(255,255,255,235),(25,25,25),F('Medium',32),'mm')
    chip_y=py+ph+int(H*0.04)
    pill(d,m//2,chip_y,'ชาไทยหก! · ความยาก 50',(0,0,0,160),'white',F('Medium',26),'mm')
    pill(d,m+m//2,chip_y,'ของในบ้าน 36 นาที',(255,255,255,240),(20,30,40),F('Medium',26),'mm')
    sc=1.0 if port else 0.85; y=H-int(60*sc)
    d.text((W//2,y),'Snap the stain, get step-by-step rescue',font=F('Regular',int(36*sc)),fill=(220,230,240),anchor='ms'); y-=int(76*sc)
    d.text((W//2,y),'เสื้อเลอะ ถ่ายปุ๊บ รู้วิธีขจัดคราบ',font=F('SemiBold',int(46*sc)),fill=(255,205,90),anchor='ms'); y-=int(100*sc)
    d.text((W//2,y),'StainSOS',font=F('Bold',int(110*sc)),fill='white',anchor='ms',stroke_width=2,stroke_fill=(0,0,0))
    im.convert('RGB').save(name)

make(1080,1350,'cover_1080x1350.png'); make(1080,1080,'cover_1080x1080.png')
print('covers written')
