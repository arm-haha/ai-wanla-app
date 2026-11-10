from PIL import Image, ImageDraw, ImageFont
import numpy as np
K='/usr/share/fonts/truetype/sand-box/google/Kanit/Kanit-'
F=lambda w,s: ImageFont.truetype(K+w+'.ttf',s,layout_engine=ImageFont.Layout.RAQM)
AMBER=(255,205,90)
RED=(220,38,38)
GOLD=(201,163,106)
PAPER=(250,247,238)
INK=(26,26,26)

def bg(W,H,top,bot,noise=3,seed=7):
    yy=np.linspace(0,1,H).reshape(H,1,1)
    a=np.array(top)*(1-yy)+np.array(bot)*yy
    a=np.repeat(a,W,axis=1)
    a+=np.random.default_rng(seed).normal(0,noise,(H,W,1))
    return Image.fromarray(np.clip(a,0,255).astype('uint8')).convert('RGBA')

def contract(im, cx, cy, w, h, marked=False):
    d=ImageDraw.Draw(im)
    x0,y0=cx-w//2, cy-h//2
    d.rounded_rectangle([x0+10,y0+14,x0+w+10,y0+h+14], radius=8, fill=(30,20,10,70))
    d.rounded_rectangle([x0,y0,x0+w,y0+h], radius=8, fill=PAPER+(255,), outline=(200,190,170,255), width=2)
    d.text((cx, y0+int(h*0.08)), 'สัญญาเช่าห้องชุด (จำลอง)', font=F('SemiBold', max(16,w//16)), fill=INK+(255,), anchor='mm')
    lines=[
        'ผู้เช่าตกลงชำระค่าเช่า เดือนละ 18,000 บาท',
        'วางมัดจำสามเดือน คืนเมื่อย้ายออกตามเงื่อนไข',
        'หากไม่บอกเลิกก่อน 30 วัน ให้ต่อสัญญาอีก 12 เดือน',
        'ค่าส่วนกลางและค่าอื่นตามที่ผู้ให้เช่ากำหนด',
        'ผู้เช่าลงลายมือชื่อ ____________________',
    ]
    y=y0+int(h*0.20)
    fs=max(14, w//22)
    for i,t in enumerate(lines):
        if marked and i in (1, 2):
            bbox=d.textbbox((x0+int(w*0.08), y), t, font=F('Medium', fs))
            d.rectangle([bbox[0]-6,bbox[1]-4,min(x0+w-12,bbox[2]+6),bbox[3]+4], fill=(254,226,226,255))
        d.text((x0+int(w*0.08), y), t, font=F('Medium', fs), fill=INK+(255,), anchor='lm')
        y += int(h*0.12)
    if marked:
        # verdict card
        vx,vy=x0+int(w*0.08), y0+int(h*0.78)
        vw,vh=int(w*0.84), int(h*0.18)
        d.rounded_rectangle([vx,vy,vx+vw,vy+vh], radius=14, fill=(255,255,255,245), outline=RED+(255,), width=4)
        d.text((vx+vw//2, vy+int(vh*0.32)), 'ความเสี่ยง 86 / 100', font=F('SemiBold', max(16,w//18)), fill=RED+(255,), anchor='mm')
        d.text((vx+vw//2, vy+int(vh*0.70)), 'จุดแดง 2 ข้อ · ควรชะลอ', font=F('Bold', max(16,w//16)), fill=INK+(255,), anchor='mm')
    return im

def make(W,H,name):
    port=H>W; m=W//2
    left=bg(W,H,(60,52,46),(24,20,18),3,1)
    right=bg(W,H,(58,48,48),(22,16,16),2,2)
    cy=int(H*(0.40 if port else 0.42))
    sw=int(m*0.84); sh=int(sw*1.28)
    contract(left, m//2, cy, sw, sh, marked=False)
    contract(right, m+m//2, cy, sw, sh, marked=True)
    im=right.copy(); im.paste(left.crop((0,0,m,H)),(0,0))
    ov=Image.new('RGBA',(W,H),(0,0,0,0)); od=ImageDraw.Draw(ov); gh=int(H*0.42)
    for i in range(gh):
        od.line([(0,H-gh+i),(W,H-gh+i)],fill=(10,8,8,int(245*(i/gh)**1.2)))
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
    pill(m+m//2,top,'AFTER',RED+(255,),'white',F('SemiBold',34),'mm')
    pill(W//2,52,'AI วันละแอป · แจกฟรี / Free',(255,255,255,235),(25,25,25),F('Medium',32),'mm')
    chip_y=int(H*(0.62 if port else 0.60))
    pill(m//2,chip_y,'สัญญาบางตา · จะเซ็นอยู่แล้ว',(0,0,0,150),'white',F('Medium',24),'mm')
    pill(m+m//2,chip_y,'มัดจำ 3 เดือน + ต่ออัตโนมัติ',(255,255,255,240),(80,10,10),F('Medium',22),'mm')
    pill(m+m//2,chip_y+70,'ไม่ใช่คำกฎหมาย',GOLD+(255,),(30,20,0),F('SemiBold',26),'mm')
    sc=1.0 if port else 0.85
    y=H-int(60*sc)
    d.text((W//2,y),'Spot the risky clauses before you sign',font=F('Regular',int(40*sc)),fill=(235,230,224),anchor='ms'); y-=int(76*sc)
    d.text((W//2,y),'ถ่ายสัญญา เจอจุดอันตรายก่อนเซ็น',font=F('SemiBold',int(52*sc)),fill=AMBER,anchor='ms'); y-=int(100*sc)
    d.text((W//2,y),'ContractLens',font=F('Bold',int(92*sc)),fill='white',anchor='ms',stroke_width=2,stroke_fill=(0,0,0))
    im.convert('RGB').save(name)

if __name__=='__main__':
    make(1080,1350,'cover_1080x1350.png'); make(1080,1080,'cover_1080x1080.png')
    print('covers written')
