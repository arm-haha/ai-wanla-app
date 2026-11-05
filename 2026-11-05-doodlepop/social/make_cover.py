"""Procedural cover: left = crayon drawing on paper (BEFORE), right = clean animated character (AFTER). Fictional art only."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np, random, math
G='/usr/share/fonts/truetype/sand-box/google/'
F=lambda w,s: ImageFont.truetype(G+'Kanit/Kanit-'+w+'.ttf',s,layout_engine=ImageFont.Layout.RAQM)
M=lambda w,s: ImageFont.truetype(G+'Mali/Mali-'+w+'.ttf',s,layout_engine=ImageFont.Layout.RAQM)
PINK=(244,114,182); PINK_L=(251,207,232); PURPLE=(109,40,217); YEL=(250,204,21); GREEN=(34,197,94); RED=(239,68,68); BLUE=(56,189,248)
def ell(cx,cy,rx,ry,n=90,a0=0,a1=2*math.pi): return [(cx+rx*math.cos(a0+(a1-a0)*i/n),cy+ry*math.sin(a0+(a1-a0)*i/n)) for i in range(n+1)]
def dino(S,cx,cy,raised):
    """Return dict of shape polygons (pixel coords) for the dino at scale S."""
    P=lambda x,y:(cx+x*S,cy+y*S)
    sh={}
    sh['tail']=[P(-0.22,0.12),P(-0.62,0.42),P(-0.18,0.38)]
    sh['body']=ell(*P(0,0.15),0.30*S,0.33*S)
    sh['belly']=ell(*P(0.02,0.2),0.17*S,0.22*S)
    sh['head']=ell(*P(0.02,-0.33),0.23*S,0.19*S)
    sh['legL']=[P(-0.17,0.4),P(-0.05,0.4),P(-0.05,0.62),P(-0.19,0.62)]
    sh['legR']=[P(0.06,0.4),P(0.18,0.4),P(0.2,0.62),P(0.06,0.62)]
    sh['armL']=[P(-0.24,-0.02),P(-0.46,0.14),P(-0.42,0.2),P(-0.2,0.08)]
    sh['armR']=[P(0.22,-0.02),P(0.44,-0.3),P(0.5,-0.26),P(0.26,0.08)] if raised else [P(0.24,-0.02),P(0.46,0.14),P(0.42,0.2),P(0.2,0.08)]
    sh['crown']=[P(-0.12,-0.48),P(-0.14,-0.66),P(-0.06,-0.56),P(0.02,-0.7),P(0.09,-0.56),P(0.17,-0.66),P(0.15,-0.48)]
    sp=[]
    for i,(x,y) in enumerate([(-0.3,-0.12),(-0.33,0.06),(-0.32,0.24)]):
        sp.append([P(x+0.03,y-0.06),P(x-0.1,y),P(x+0.03,y+0.06)])
    sh['spikes']=sp
    return sh,P
def paper(W,H):
    rng=np.random.default_rng(5); a=np.ones((H,W,3))*np.array([250,246,236])/255
    a+=rng.normal(0,0.018,(H,W,1))
    yy,xx=np.mgrid[0:H,0:W]; a*=1-0.22*np.exp(-((xx-W*0.05)**2+(yy-H*0.15)**2)/(2*(W*0.28)**2))[...,None]  # hand shadow
    a*=1-0.12*np.clip(xx/W-0.0,0,1)[...,None]*0
    im=Image.fromarray((np.clip(a,0,1)*255).astype('uint8'))
    d=ImageDraw.Draw(im)
    for y in range(int(H*0.08),H,int(H*0.045)): d.line([(0,y),(W,y)],fill=(200,215,235),width=1)
    return im
def crayon_poly(d,pts,color,w,rnd,passes=3,closed=True):
    pts=list(pts)+([pts[0]] if closed else [])
    for k in range(passes):
        j=[(x+rnd.uniform(-5,5),y+rnd.uniform(-5,5)) for x,y in pts]
        d.line(j,fill=color+(rnd.randint(150,230),),width=w+rnd.randint(-2,2),joint='curve')
def crayon_fill(base,poly,color,rnd,density=9,angle=0.6):
    W,H=base.size; mask=Image.new('L',(W,H),0); ImageDraw.Draw(mask).polygon(poly,fill=255)
    lay=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(lay)
    xs=[p[0] for p in poly]; ys=[p[1] for p in poly]; x0,x1,y0,y1=min(xs),max(xs),min(ys),max(ys); L=(x1-x0)+(y1-y0)
    t=-L
    while t<L:
        cx0=x0+t; d.line([(cx0,y0),(cx0+(y1-y0)*angle,y1)],fill=color+(rnd.randint(120,200),),width=rnd.randint(5,9)); t+=density+rnd.uniform(-3,3)
    lay=lay.filter(ImageFilter.GaussianBlur(0.8)); a=np.minimum(np.asarray(lay.split()[3]),np.asarray(mask.filter(ImageFilter.GaussianBlur(3))))
    lay.putalpha(Image.fromarray(a.astype('uint8'))); base.alpha_composite(lay)
def before(W,H,S,cx,cy):
    rnd=random.Random(11); im=paper(W,H).convert('RGBA'); sh,P=dino(S,cx,cy,False)
    # sun + grass scribbles
    d=ImageDraw.Draw(im)
    crayon_fill(im,ell(W*0.13,H*0.3,70,70),YEL,rnd); d=ImageDraw.Draw(im); crayon_poly(d,ell(W*0.13,H*0.3,70,70,30),(234,179,8),6,rnd)
    for i in range(10): a=i*math.pi/5; crayon_poly(d,[(W*0.13+95*math.cos(a),H*0.3+95*math.sin(a)),(W*0.13+130*math.cos(a),H*0.3+130*math.sin(a))],(234,179,8),6,rnd,2,False)
    gy=P(0,0.63)[1]
    for x in range(0,W,22): crayon_poly(d,[(x,gy+40),(x+8,gy-5),(x+16,gy+40)],GREEN,5,rnd,1,False)
    for k in ['tail','legL','legR','armL','armR','body','head']: crayon_fill(im,sh[k],PINK,rnd)
    crayon_fill(im,sh['belly'],(253,224,71),rnd,12); crayon_fill(im,sh['crown'],YEL,rnd,8)
    for sp in sh['spikes']: crayon_fill(im,sp,(167,139,250),rnd,7)
    d=ImageDraw.Draw(im)
    for k in ['tail','legL','legR','armL','armR','body','head']: crayon_poly(d,sh[k],PURPLE,7,rnd)
    crayon_poly(d,sh['crown'],(202,138,4),6,rnd)
    for sp in sh['spikes']: crayon_poly(d,sp,PURPLE,6,rnd)
    for ex in (-0.07,0.11): x,y=P(ex,-0.36); d.ellipse([x-13,y-16,x+13,y+16],fill=(30,30,30)); 
    crayon_poly(d,ell(*P(0.02,-0.3),0.1*S,0.07*S,20,0.2,math.pi-0.2),RED,6,rnd,2,False)
    d.text((40,gy-60),'ใบเตย 5 ขวบ',font=M('Bold',int(S*0.1)),fill=(37,99,235,210),anchor='ls')
    return im
def after(W,H,S,cx,cy):
    a=np.zeros((H,W,3)); yy,xx=np.mgrid[0:H,0:W]; t=(yy/H)[...,None]
    a=(1-t)*np.array([255,236,179])+t*np.array([251,182,206]); im=Image.fromarray(a.astype('uint8')).convert('RGBA')
    d=ImageDraw.Draw(im); rnd=random.Random(4)
    for _ in range(70):
        x=rnd.randint(0,W); y=rnd.randint(0,H); r=rnd.randint(5,12); c=rnd.choice([RED,YEL,BLUE,GREEN,PURPLE,(255,255,255)])
        d.rounded_rectangle([x,y,x+r*2,y+r],radius=4,fill=c+(200,))
    lift=-0.07; sh,P=dino(S,cx,cy+lift*S,True)
    fx,fy=P(0,0.63); fy-=lift*S; d.ellipse([fx-S*0.3,fy+5,fx+S*0.3,fy+45],fill=(120,40,90,70))
    OUT=(76,29,149); lw=max(6,int(S*0.018))
    def shape(poly,fill): d.polygon(poly,fill=fill); d.line(list(poly)+[poly[0]],fill=OUT,width=lw,joint='curve')
    for k in ['tail','legL','legR','armL','armR','body']: shape(sh[k],PINK)
    for sp in sh['spikes']: shape(sp,(167,139,250))
    shape(sh['head'],PINK); shape(sh['belly'],(254,240,138)); shape(sh['crown'],YEL)
    for k,c in [((-0.06,-0.6),RED),((0.03,-0.63),BLUE),((0.12,-0.6),GREEN)]: x,y=P(*k); d.ellipse([x-9,y-9,x+9,y+9],fill=c)
    for ex in (-0.07,0.11):
        x,y=P(ex,-0.36); d.ellipse([x-15,y-19,x+15,y+19],fill=(25,25,35)); d.ellipse([x-6,y-12,x+3,y-3],fill='white')
    for ex in (-0.15,0.19): x,y=P(ex,-0.27); d.ellipse([x-16,y-8,x+16,y+8],fill=(251,113,133,180))
    d.arc([*P(-0.06,-0.36),*P(0.1,-0.22)],20,160,fill=OUT,width=lw)
    # motion arcs near raised arm + sparkles
    hx,hy=P(0.48,-0.3)
    for r in (50,80,110): d.arc([hx-r,hy-r,hx+r,hy+r],-80,10,fill=(255,255,255,230),width=7)
    for sx,sy,r in [(0.62,-0.55,26),(0.75,0.05,18),(0.4,-0.72,16),(0.68,0.35,22)]:
        x,y=P(sx,sy); d.polygon([(x,y-r),(x+r*0.28,y-r*0.28),(x+r,y),(x+r*0.28,y+r*0.28),(x,y+r),(x-r*0.28,y+r*0.28),(x-r,y),(x-r*0.28,y-r*0.28)],fill=(255,255,255,240))
    # pose chips
    return im
def make(W,H,name):
    S=int(min(W,H)*(0.5 if H>W else 0.42)); cx=W//2; cy=int(H*(0.46 if H>W else 0.41))
    bef=before(W,H,S,cx,cy); im=after(W,H,S,cx,cy); m=W//2
    im.paste(bef.crop((0,0,m,H)),(0,0))
    ov=Image.new('RGBA',(W,H),(0,0,0,0)); od=ImageDraw.Draw(ov)
    gh=int(H*0.40)
    for i in range(gh): od.line([(0,H-gh+i),(W,H-gh+i)],fill=(20,10,30,int(235*(i/gh)**1.3)))
    im=Image.alpha_composite(im,ov); d=ImageDraw.Draw(im)
    d.rectangle([m-3,0,m+3,H],fill='white')
    cy2=int(H*0.40); d.ellipse([m-34,cy2-34,m+34,cy2+34],fill='white',outline=(0,0,0,60),width=2)
    d.text((m-14,cy2),'◀',font=F('Regular',26),fill=(40,40,40),anchor='mm'); d.text((m+14,cy2),'▶',font=F('Regular',26),fill=(40,40,40),anchor='mm')
    def pill(x,y,t,bg,fg,font,anchor):
        b=d.textbbox((x,y),t,font=font,anchor=anchor); p=14
        d.rounded_rectangle([b[0]-p*1.6,b[1]-p,b[2]+p*1.6,b[3]+p],radius=40,fill=bg); d.text((x,y),t,font=font,fill=fg,anchor=anchor)
    top=int(H*0.12) if H>W else 120
    pill(m-150,top,'BEFORE',(0,0,0,170),'white',F('SemiBold',34),'mm')
    pill(m+150,top,'AFTER',(255,196,64,255),(30,20,0),F('SemiBold',34),'mm')
    pill(W//2,52,'AI วันละแอป · แจกฟรี / Free',(255,255,255,235),(25,25,25),F('Medium',32),'mm')
    s=1.0 if H>W else 0.85
    y=H-int(60*s)
    d.text((W//2,y),"Bring your kid's drawing to life",font=F('Regular',int(44*s)),fill=(235,235,235),anchor='ms'); y-=int(76*s)
    d.text((W//2,y),'รูปวาดลูก ขยับได้',font=F('SemiBold',int(64*s)),fill=(255,205,90),anchor='ms'); y-=int(100*s)
    d.text((W//2,y),'DoodlePop',font=F('Bold',int(120*s)),fill='white',anchor='ms',stroke_width=2,stroke_fill=(0,0,0))
    im.convert('RGB').save(name)
make(1080,1350,'cover_1080x1350.png'); make(1080,1080,'cover_1080x1080.png')
