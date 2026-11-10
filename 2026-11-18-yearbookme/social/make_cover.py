"""Procedural cover: left = plain illustrated selfie (BEFORE), right = 90s yearbook portrait (AFTER). Illustration only — no real photos or people."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
G='/usr/share/fonts/truetype/sand-box/google/'
F=lambda w,s: ImageFont.truetype(G+'Kanit/Kanit-'+w+'.ttf',s,layout_engine=ImageFont.Layout.RAQM)
NAVY=(30,58,95); GOLD=(196,165,116); INK=(31,41,55); AMBER=(255,196,64); WHITE=(255,255,255)

def bg(W,H,top,bot,noise,seed):
    yy=np.linspace(0,1,H)[:,None,None]; a=np.array(top)*(1-yy)+np.array(bot)*yy; a=np.repeat(a,W,axis=1)
    a+=np.random.default_rng(seed).normal(0,noise,(H,W,1))
    return Image.fromarray(np.clip(a,0,255).astype('uint8')).convert('RGBA')

def grain(im, seed, sigma=10):
    a=np.asarray(im).astype(np.int16)
    a[:,:,:3]+=np.random.default_rng(seed).normal(0,sigma,a[:,:,:3].shape).astype(np.int16)
    return Image.fromarray(np.clip(a,0,255).astype('uint8'))

def face(im, cx, cy, s, skin, hair, lip, eye, shirt, blush=True):
    """Stylized geometric portrait — clearly an illustration."""
    d=ImageDraw.Draw(im)
    d.ellipse([cx-s*0.72, cy-s*1.05, cx+s*0.72, cy+s*0.55], fill=hair)
    d.rectangle([cx-s*0.16, cy+s*0.55, cx+s*0.16, cy+s*0.95], fill=skin)
    d.polygon([(cx-s*0.85,cy+s*1.55),(cx-s*0.70,cy+s*0.86),(cx-s*0.22,cy+s*0.92),
               (cx,cy+s*1.18),(cx+s*0.22,cy+s*0.92),(cx+s*0.70,cy+s*0.86),(cx+s*0.85,cy+s*1.55)], fill=shirt)
    d.ellipse([cx-s*0.58, cy-s*0.78, cx+s*0.58, cy+s*0.68], fill=skin)
    d.pieslice([cx-s*0.62, cy-s*1.12, cx+s*0.62, cy+s*0.15], 200, 20, fill=hair)
    d.polygon([(cx-s*0.05,cy-s*0.70),(cx+s*0.58,cy-s*0.55),(cx+s*0.50,cy-s*0.05),(cx+s*0.10,cy-s*0.25)], fill=hair)
    d.ellipse([cx-s*0.68, cy-s*0.10, cx-s*0.50, cy+s*0.22], fill=skin)
    d.ellipse([cx+s*0.50, cy-s*0.10, cx+s*0.68, cy+s*0.22], fill=skin)
    if blush:
        br=Image.new('RGBA',im.size,(0,0,0,0)); bd=ImageDraw.Draw(br)
        bd.ellipse([cx-s*0.48,cy+s*0.12,cx-s*0.18,cy+s*0.32], fill=(230,120,130,90))
        bd.ellipse([cx+s*0.18,cy+s*0.12,cx+s*0.48,cy+s*0.32], fill=(230,120,130,90))
        im.alpha_composite(br.filter(ImageFilter.GaussianBlur(int(s*0.04))))
        d=ImageDraw.Draw(im)
    d.ellipse([cx-s*0.32, cy-s*0.12, cx-s*0.12, cy+s*0.10], fill=WHITE)
    d.ellipse([cx+s*0.12, cy-s*0.12, cx+s*0.32, cy+s*0.10], fill=WHITE)
    d.ellipse([cx-s*0.27, cy-s*0.07, cx-s*0.15, cy+s*0.07], fill=eye)
    d.ellipse([cx+s*0.15, cy-s*0.07, cx+s*0.27, cy+s*0.07], fill=eye)
    d.ellipse([cx-s*0.20, cy-s*0.05, cx-s*0.16, cy-s*0.01], fill=WHITE)
    d.ellipse([cx+s*0.22, cy-s*0.05, cx+s*0.26, cy-s*0.01], fill=WHITE)
    d.arc([cx-s*0.36, cy-s*0.28, cx-s*0.08, cy-s*0.02], 200, 340, fill=hair, width=max(3,int(s*0.04)))
    d.arc([cx+s*0.08, cy-s*0.28, cx+s*0.36, cy-s*0.02], 200, 340, fill=hair, width=max(3,int(s*0.04)))
    d.arc([cx-s*0.06, cy+s*0.02, cx+s*0.06, cy+s*0.22], 20, 160, fill=(160,110,100), width=max(2,int(s*0.03)))
    d.arc([cx-s*0.18, cy+s*0.22, cx+s*0.18, cy+s*0.48], 20, 160, fill=lip, width=max(3,int(s*0.045)))

def make(W,H,name):
    port=H>W; m=W//2; S=int(W*(0.20 if port else 0.17)); cy=int(H*(0.38 if port else 0.42))
    # BEFORE: soft modern selfie on a white phone card
    left=bg(W,H,(236,228,220),(210,200,192),3,1)
    g=Image.new('RGBA',left.size,(0,0,0,0)); gd=ImageDraw.Draw(g)
    gd.ellipse([m//2-int(S*1.8), cy-int(S*2.4), m//2+int(S*1.8), cy+int(S*0.2)], fill=(255,248,230,80))
    left.alpha_composite(g.filter(ImageFilter.GaussianBlur(42)))
    ld=ImageDraw.Draw(left)
    fw,fh=int(S*2.20),int(S*2.70); fx,fy=m//2-fw//2, cy-int(S*1.05)
    ld.rounded_rectangle([fx-12,fy-12,fx+fw+12,fy+fh+12], radius=36, fill=(250,250,252,255), outline=(230,230,235,255), width=4)
    face(left, m//2, cy, S, skin=(232,196,176), hair=(42,32,30), lip=(180,80,90), eye=(50,40,40), shirt=(40,55,80))

    # AFTER: cream yearbook page, navy double frame, cooler grade — frame sits below the AFTER pill
    right=bg(W,H,(232,224,208),(200,188,168),2,2)
    rng=np.random.default_rng(9); rd=ImageDraw.Draw(right)
    for _ in range(220):
        x=int(rng.integers(m+8,W-8)); y=int(rng.integers(int(H*0.16),int(H*0.72)))
        r=int(rng.integers(1,3)); rd.ellipse([x,y,x+r,y+r], fill=(196,165,116,80))
    cx=m+m//2
    # yearbook plate
    pw,ph=int(m*0.78),int(S*3.35)
    px,py=cx-pw//2, int(H*(0.16 if port else 0.18))
    rd.rectangle([px-10,py-10,px+pw+10,py+ph+10], fill=(252,248,238,255), outline=NAVY+(255,), width=8)
    rd.rectangle([px,py,px+pw,py+ph], fill=(252,248,238,255), outline=GOLD+(255,), width=3)
    # photo well with cooler grade
    well=[px+22, py+22, px+pw-22, py+int(ph*0.78)]
    rd.rectangle(well, fill=(186,178,166,255))
    # draw face into a temp then paste? just draw centered in well
    fcx=(well[0]+well[2])//2; fcy=well[1]+int((well[3]-well[1])*0.52)
    fs=int(S*0.92)
    face(right, fcx, fcy, fs, skin=(200,170,152), hair=(28,22,22), lip=(140,65,75), eye=(35,32,38), shirt=(28,40,62))
    # cool overlay only on the photo well
    mask=Image.new('RGBA',right.size,(0,0,0,0)); md=ImageDraw.Draw(mask)
    md.rectangle(well, fill=(30,55,90,50))
    right=Image.alpha_composite(right, mask)
    right=grain(right, 5, 7)
    rd=ImageDraw.Draw(right)
    # nameplate under the photo, inside the yearbook card
    ny=py+int(ph*0.84)
    rd.text((cx, ny), "CLASS OF  '97", font=F('SemiBold', int(S*0.20)), fill=NAVY, anchor='mm')
    rd.text((cx, ny+int(S*0.28)), "น้องมายด์", font=F('Medium', int(S*0.18)), fill=INK, anchor='mm')

    im=right.copy(); im.paste(left.crop((0,0,m,H)),(0,0))
    ov=Image.new('RGBA',(W,H),(0,0,0,0)); od=ImageDraw.Draw(ov); gh=int(H*0.42)
    for i in range(gh): od.line([(0,H-gh+i),(W,H-gh+i)], fill=(18,14,10,int(245*(i/gh)**1.2)))
    im=Image.alpha_composite(im,ov); d=ImageDraw.Draw(im)
    d.rectangle([m-3,0,m+3,H], fill='white')
    cy2=int(H*0.32); d.ellipse([m-34,cy2-34,m+34,cy2+34], fill='white', outline=(0,0,0,60), width=2)
    d.text((m-14,cy2),'◀',font=F('Regular',26),fill=(40,40,40),anchor='mm'); d.text((m+14,cy2),'▶',font=F('Regular',26),fill=(40,40,40),anchor='mm')
    def pill(x,y,t,bgc,fg,font,anchor):
        b=d.textbbox((x,y),t,font=font,anchor=anchor); p=14
        d.rounded_rectangle([b[0]-p*1.6,b[1]-p,b[2]+p*1.6,b[3]+p], radius=40, fill=bgc); d.text((x,y),t,font=font,fill=fg,anchor=anchor)
    top=int(H*0.10) if port else 120
    pill(m//2,top,'BEFORE',(0,0,0,170),'white',F('SemiBold',34),'mm')
    pill(m+m//2,top,'AFTER',AMBER+(255,),(30,20,0),F('SemiBold',34),'mm')
    pill(W//2,52,'AI วันละแอป · แจกฟรี / Free',(255,255,255,235),(25,25,25),F('Medium',32),'mm')
    chip_y=int(H*(0.60 if port else 0.585))
    pill(m//2,chip_y,'เซลฟี่ธรรมดา',(0,0,0,150),'white',F('Medium',28),'mm')
    pill(m+m//2,chip_y,'ยุค 90s · คะแนน 88 เข้าสุด',(255,255,255,240),(40,30,10),F('Medium',25),'mm')
    pill(m+m//2,chip_y+70,"Class of '97",GOLD+(255,),NAVY,F('SemiBold',29),'mm')
    s=1.0 if port else 0.85
    y=H-int(60*s)
    d.text((W//2,y),'One selfie → 80s / 90s / Y2K yearbook look',font=F('Regular',int(40*s)),fill=(235,230,220),anchor='ms'); y-=int(76*s)
    d.text((W//2,y),'เซลฟี่เดียว กลายเป็นรูปรุ่นยุค 90s',font=F('SemiBold',int(52*s)),fill=(255,205,90),anchor='ms'); y-=int(100*s)
    d.text((W//2,y),'YearbookMe',font=F('Bold',int(110*s)),fill='white',anchor='ms',stroke_width=2,stroke_fill=(0,0,0))
    im.convert('RGB').save(name)

make(1080,1350,'cover_1080x1350.png'); make(1080,1080,'cover_1080x1080.png')
