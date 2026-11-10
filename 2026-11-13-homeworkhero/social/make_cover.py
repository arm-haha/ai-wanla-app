from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
K='/usr/share/fonts/truetype/sand-box/google/Kanit/Kanit-'
F=lambda w,s: ImageFont.truetype(K+w+'.ttf',s,layout_engine=ImageFont.Layout.RAQM)
AMBER=(255,205,90)
YELLOW=(231,176,12)
BLUE=(43,108,176)
PINK=(249,197,209)
PAPER=(250,248,240)
INK=(27,36,48)

def bg(W,H,top,bot,noise=3,seed=7):
    yy=np.linspace(0,1,H).reshape(H,1,1)
    a=np.array(top)*(1-yy)+np.array(bot)*yy
    a=np.repeat(a,W,axis=1)
    a+=np.random.default_rng(seed).normal(0,noise,(H,W,1))
    return Image.fromarray(np.clip(a,0,255).astype('uint8')).convert('RGBA')

def sheet(im, cx, cy, w, h, hinted=False):
    d=ImageDraw.Draw(im)
    x0,y0=cx-w//2, cy-h//2
    # shadow
    d.rounded_rectangle([x0+12,y0+16,x0+w+12,y0+h+16], radius=18, fill=(20,30,20,80))
    d.rounded_rectangle([x0,y0,x0+w,y0+h], radius=18, fill=PAPER+(255,), outline=(210,205,190,255), width=3)
    # margin line
    d.line([(x0+int(w*0.14), y0+20),(x0+int(w*0.14), y0+h-20)], fill=(230,160,160,255), width=3)
    # header
    d.text((cx, y0+int(h*0.10)), 'คณิตศาสตร์ ป.4', font=F('SemiBold', max(22, w//14)), fill=BLUE+(255,), anchor='mm')
    # problem lines
    lines=[
        'สินค้าชิ้นหนึ่งราคา 800 บาท',
        'ลด 25%  เหลือกี่บาท ?',
        'ตอบ  ________  บาท',
    ]
    y=y0+int(h*0.28)
    for i,t in enumerate(lines):
        d.text((x0+int(w*0.20), y), t, font=F('Medium', max(18, w//16)), fill=INK+(255,), anchor='lm')
        y += int(h*0.16)
    if hinted:
        # sticky hint card overlapping bottom
        hx,hy=x0+int(w*0.10), y0+int(h*0.62)
        hw,hh=int(w*0.80), int(h*0.32)
        d.rounded_rectangle([hx+6,hy+8,hx+hw+6,hy+hh+8], radius=16, fill=(0,0,0,40))
        d.rounded_rectangle([hx,hy,hx+hw,hy+hh], radius=16, fill=PINK+(255,))
        d.text((hx+hw//2, hy+int(hh*0.22)), 'คำใบ้ 3 · วิธีคิด', font=F('SemiBold', max(18,w//16)), fill=(120,40,60,255), anchor='mm')
        d.text((hx+hw//2, hy+int(hh*0.52)), '800 × (25 ÷ 100) = ____', font=F('Bold', max(18,w//15)), fill=INK+(255,), anchor='mm')
        d.text((hx+hw//2, hy+int(hh*0.78)), 'ไม่บอกคำตอบ', font=F('Medium', max(16,w//18)), fill=(120,40,60,255), anchor='mm')
    else:
        d.text((cx, y0+int(h*0.82)), 'ยังไม่รู้จะเริ่มตรงไหน', font=F('Medium', max(18,w//16)), fill=(120,110,100,255), anchor='mm')
    return im

def make(W,H,name):
    port=H>W; m=W//2
    left=bg(W,H,(210,222,208),(170,188,168),3,1)
    right=bg(W,H,(214,226,216),(168,190,176),2,2)
    cy=int(H*(0.40 if port else 0.42))
    sw=int(m*0.78); sh=int(sw*1.25)
    sheet(left, m//2, cy, sw, sh, hinted=False)
    sheet(right, m+m//2, cy, sw, sh, hinted=True)
    im=right.copy(); im.paste(left.crop((0,0,m,H)),(0,0))
    ov=Image.new('RGBA',(W,H),(0,0,0,0)); od=ImageDraw.Draw(ov); gh=int(H*0.42)
    for i in range(gh):
        od.line([(0,H-gh+i),(W,H-gh+i)],fill=(12,18,16,int(245*(i/gh)**1.2)))
    im=Image.alpha_composite(im,ov); d=ImageDraw.Draw(im)
    d.rectangle([m-3,0,m+3,H],fill='white')
    cy2=int(H*0.28); d.ellipse([m-34,cy2-34,m+34,cy2+34],fill='white',outline=(0,0,0,60),width=2)
    d.text((m-14,cy2),'◀',font=F('Regular',26),fill=(40,40,40),anchor='mm')
    d.text((m+14,cy2),'▶',font=F('Regular',26),fill=(40,40,40),anchor='mm')
    def pill(x,y,t,bgc,fg,font,anchor):
        b=d.textbbox((x,y),t,font=font,anchor=anchor); p=14
        d.rounded_rectangle([b[0]-p*1.6,b[1]-p,b[2]+p*1.6,b[3]+p],radius=40,fill=bgc); d.text((x,y),t,font=font,fill=fg,anchor=anchor)
    top=int(H*0.10) if port else 120
    pill(m//2,top,'BEFORE',(0,0,0,170),'white',F('SemiBold',34),'mm')
    pill(m+m//2,top,'AFTER',YELLOW+(255,),(30,20,0),F('SemiBold',34),'mm')
    pill(W//2,52,'AI วันละแอป · แจกฟรี / Free',(255,255,255,235),(25,25,25),F('Medium',32),'mm')
    chip_y=int(H*(0.62 if port else 0.60))
    pill(m//2,chip_y,'โจทย์ร้อยละ · ติดแล้ว',(0,0,0,150),'white',F('Medium',26),'mm')
    pill(m+m//2,chip_y,'คณิต ป.4 · คำใบ้ทีละขั้น',(255,255,255,240),(20,40,30),F('Medium',24),'mm')
    pill(m+m//2,chip_y+70,'ไม่บอกคำตอบ',YELLOW+(255,),(30,20,0),F('SemiBold',28),'mm')
    sc=1.0 if port else 0.85
    y=H-int(60*sc)
    d.text((W//2,y),'Step hints for parents — never the answer',font=F('Regular',int(38*sc)),fill=(235,240,232),anchor='ms'); y-=int(76*sc)
    d.text((W//2,y),'ถ่ายการบ้าน ได้วิธีสอนทีละขั้น',font=F('SemiBold',int(52*sc)),fill=AMBER,anchor='ms'); y-=int(100*sc)
    d.text((W//2,y),'HomeworkHero',font=F('Bold',int(92*sc)),fill='white',anchor='ms',stroke_width=2,stroke_fill=(0,0,0))
    im.convert('RGB').save(name)

if __name__=='__main__':
    make(1080,1350,'cover_1080x1350.png'); make(1080,1080,'cover_1080x1080.png')
    print('covers written')
