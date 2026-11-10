"""Procedural cover: left = illustrated closet (BEFORE), right = Friday-blue outfit + colour card (AFTER).
Fictional illustration only — no real people or wardrobes."""
from PIL import Image, ImageDraw, ImageFont
import numpy as np
G='/usr/share/fonts/truetype/sand-box/google/'
F=lambda w,s: ImageFont.truetype(G+'Kanit/Kanit-'+w+'.ttf',s,layout_engine=ImageFont.Layout.RAQM)
NAVY=(31,41,55); BLUE=(56,189,248); SKY=(224,242,254)
WHITE=(255,255,255); PINK=(236,72,153); BEIGE=(237,220,196); BLACK=(30,30,30)

def bg(W,H,top,bot,noise,seed):
    yy=np.linspace(0,1,H)[:,None,None]; a=np.array(top)*(1-yy)+np.array(bot)*yy; a=np.repeat(a,W,axis=1)
    a+=np.random.default_rng(seed).normal(0,noise,(H,W,1))
    return Image.fromarray(np.clip(a,0,255).astype('uint8')).convert('RGBA')

def pill(d,x,y,t,bgc,fg,font,anchor):
    b=d.textbbox((x,y),t,font=font,anchor=anchor); p=14
    d.rounded_rectangle([b[0]-p*1.6,b[1]-p,b[2]+p*1.6,b[3]+p], radius=40, fill=bgc); d.text((x,y),t,font=font,fill=fg,anchor=anchor)

def hanger(d, x, y, w, h, fill, outline=NAVY):
    # hook
    d.arc([x+w//2-12, y-16, x+w//2+12, y+10], 200, 340, fill=outline, width=4)
    d.line([(x+8,y+8),(x+w-8,y+8)], fill=outline, width=4)
    # garment
    d.rounded_rectangle([x, y+8, x+w, y+h], radius=10, fill=fill, outline=outline, width=3)

def make(W,H,name):
    port=H>W; m=W//2; S=int(W*(0.20 if port else 0.16))
    left=bg(W,H,(255,251,245),(245,236,220),3,31)
    pw,ph=int(S*2.20), int(S*(3.15 if port else 2.95))
    px,py=m//2-pw//2, int(H*(0.15 if port else 0.17))
    ld=ImageDraw.Draw(left)
    ld.rounded_rectangle([px,py,px+pw,py+ph], radius=24, fill=(255,252,248,255), outline=(200,180,150,255), width=5)
    # rail
    ld.line([(px+24, py+int(S*0.45)), (px+pw-24, py+int(S*0.45))], fill=(160,140,120), width=6)
    gw,gh=int(S*0.55), int(S*1.15)
    gap=int(S*0.12)
    start=px+int(S*0.22)
    cols=[(WHITE,"ขาว"),(PINK,"ชมพู"),(BEIGE,"เบจ")]
    for i,(col,lab) in enumerate(cols):
        x=start+i*(gw+gap); y=py+int(S*0.55)
        hanger(ld, x, y, gw, gh, col)
    # skirt hint + bag
    sx=px+int(pw*0.28); sy=py+int(ph*0.62)
    ld.polygon([(sx,sy),(sx+int(S*0.9),sy),(sx+int(S*0.75),sy+int(S*0.70)),(sx+int(S*0.15),sy+int(S*0.70))], fill=BLUE, outline=NAVY, width=3)
    ld.text((m//2, py+int(ph*0.92)), "ตู้เสื้อผ้า", font=F('SemiBold', int(S*0.16)), fill=NAVY, anchor='mm')

    right=bg(W,H,(186,230,253),(14,116,144),2,32)
    rd=ImageDraw.Draw(right)
    cx=m+m//2
    cw,ch=int(m*0.84), int(H*(0.46 if port else 0.40))
    x0,y0=cx-cw//2, int(H*(0.15 if port else 0.17))
    rd.rounded_rectangle([x0,y0,x0+cw,y0+ch], radius=26, fill=(255,255,255,255), outline=BLUE+(255,), width=5)
    rd.rounded_rectangle([x0+18, y0+18, x0+cw-18, y0+int(S*0.70)], radius=18, fill=BLUE+(255,))
    rd.text((cx, y0+int(S*0.28)), "สีมงคลวันศุกร์", font=F('Medium', int(S*0.14)), fill=NAVY, anchor='mm')
    rd.text((cx, y0+int(S*0.50)), "ฟ้า", font=F('Bold', int(S*0.28)), fill=WHITE, anchor='mm')
    rows=[("เสื้อเชิ้ตขาว","กลาง"),("กระโปรงฟ้า","สีมงคล"),("กระเป๋าเบจ","กลาง")]
    yy=y0+int(S*0.86)
    for i,(t,tag) in enumerate(rows):
        y=yy+i*int(S*0.32)
        rd.text((x0+28, y), t, font=F('Medium', int(S*0.14)), fill=NAVY, anchor='lm')
        col = BLUE if tag=="สีมงคล" else (200,200,200)
        fg = NAVY if tag=="สีมงคล" else NAVY
        tw=rd.textbbox((0,0),tag,font=F('SemiBold', int(S*0.11)))
        rd.rounded_rectangle([x0+cw-28-(tw[2]-tw[0])-16, y-16, x0+cw-28, y+16], radius=12, fill=col+(255,) if tag=="สีมงคล" else (240,240,240,255))
        rd.text((x0+cw-36, y), tag, font=F('SemiBold', int(S*0.11)), fill=WHITE if tag=="สีมงคล" else NAVY, anchor='rm')
    rd.text((cx, y0+ch-int(S*0.22)), "คะแนนแมตช์ 67", font=F('Bold', int(S*0.16)), fill=BLUE, anchor='mm')

    im=right.copy(); im.paste(left.crop((0,0,m,H)),(0,0))
    ov=Image.new('RGBA',(W,H),(0,0,0,0)); od=ImageDraw.Draw(ov); gh=int(H*0.40)
    for i in range(gh): od.line([(0,H-gh+i),(W,H-gh+i)], fill=(8,30,50,int(235*(i/gh)**1.2)))
    im=Image.alpha_composite(im,ov); d=ImageDraw.Draw(im)
    d.rectangle([m-3,0,m+3,H], fill='white')
    cy2=int(H*0.30); d.ellipse([m-34,cy2-34,m+34,cy2+34], fill='white', outline=(0,0,0,60), width=2)
    d.text((m-14,cy2),'◀',font=F('Regular',26),fill=(40,40,40),anchor='mm'); d.text((m+14,cy2),'▶',font=F('Regular',26),fill=(40,40,40),anchor='mm')
    top=int(H*0.09) if port else 100
    pill(d,m//2,top,'BEFORE',(0,0,0,170),'white',F('SemiBold',34),'mm')
    pill(d,m+m//2,top,'AFTER',(251,191,36,255),(30,20,0),F('SemiBold',34),'mm')
    pill(d,W//2,48,'AI วันละแอป · แจกฟรี / Free',(255,255,255,235),(25,25,25),F('Medium',32),'mm')
    chip_y = max(py+ph, y0+ch) + (48 if port else 38)
    pill(d,m//2,chip_y,'เกิดวันศุกร์',(0,0,0,170),'white',F('Medium',24),'mm')
    pill(d,m+m//2,chip_y,'สีฟ้า · วอลเปเปอร์พร้อมใช้',(255,255,255,240),NAVY,F('Medium',24),'mm')
    s=1.0 if port else 0.85
    y=H-int(56*s)
    d.text((W//2,y),'Your lucky colour, an outfit and a wallpaper',font=F('Regular',int(32*s)),fill=(200,230,245),anchor='ms'); y-=int(72*s)
    d.text((W//2,y),'สีมงคลประจำวัน + วอลเปเปอร์สายมู',font=F('SemiBold',int(42*s)),fill=(255,205,90),anchor='ms'); y-=int(92*s)
    d.text((W//2,y),'LuckyHue',font=F('Bold',int(100*s)),fill='white',anchor='ms',stroke_width=2,stroke_fill=(0,0,0))
    im.convert('RGB').save(name)

make(1080,1350,'cover_1080x1350.png'); make(1080,1080,'cover_1080x1080.png')
print("covers written")
