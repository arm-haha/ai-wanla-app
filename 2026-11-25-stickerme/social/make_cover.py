"""Procedural cover: left = illustrated selfie (BEFORE), right = 16-sticker chibi grid (AFTER).
Fictional illustration only — no real faces, not a LINE product."""
from PIL import Image, ImageDraw, ImageFont
import numpy as np
G='/usr/share/fonts/truetype/sand-box/google/'
F=lambda w,s: ImageFont.truetype(G+'Kanit/Kanit-'+w+'.ttf',s,layout_engine=ImageFont.Layout.RAQM)
NAVY=(31,41,55); PINK=(251,113,133); YELLOW=(251,191,36)
CREAM=(255,247,237); WHITE=(255,255,255); LINE=(31,41,55)
SKIN=(255,214,186); HAIR=(60,40,32); BLUSH=(255,160,160)

def bg(W,H,top,bot,noise,seed):
    yy=np.linspace(0,1,H)[:,None,None]; a=np.array(top)*(1-yy)+np.array(bot)*yy; a=np.repeat(a,W,axis=1)
    a+=np.random.default_rng(seed).normal(0,noise,(H,W,1))
    return Image.fromarray(np.clip(a,0,255).astype('uint8')).convert('RGBA')

def pill(d,x,y,t,bgc,fg,font,anchor):
    b=d.textbbox((x,y),t,font=font,anchor=anchor); p=14
    d.rounded_rectangle([b[0]-p*1.6,b[1]-p,b[2]+p*1.6,b[3]+p], radius=40, fill=bgc); d.text((x,y),t,font=font,fill=fg,anchor=anchor)

def chibi(im, cx, cy, r, mood="happy"):
    """Simple geometric character — clearly a drawing, not a photograph."""
    d=ImageDraw.Draw(im)
    # head
    d.ellipse([cx-r, cy-r, cx+r, cy+int(r*1.05)], fill=SKIN, outline=LINE, width=max(3, r//10))
    # hair bangs
    d.pieslice([cx-r, cy-int(r*1.25), cx+r, cy+int(r*0.2)], 200, 340, fill=HAIR, outline=LINE, width=max(2, r//12))
    d.ellipse([cx-int(r*0.85), cy-int(r*1.15), cx+int(r*0.85), cy-int(r*0.15)], fill=HAIR)
    # blush
    br=max(4, r//6)
    d.ellipse([cx-int(r*0.62)-br, cy+int(r*0.18), cx-int(r*0.62)+br, cy+int(r*0.18)+br], fill=BLUSH)
    d.ellipse([cx+int(r*0.62)-br, cy+int(r*0.18), cx+int(r*0.62)+br, cy+int(r*0.18)+br], fill=BLUSH)
    # eyes
    er=max(3, r//7)
    ey=cy-int(r*0.08)
    if mood in ("happy","laugh","love","ok","thumbs","celebrate","wink"):
        # happy curves or open
        if mood=="wink":
            d.ellipse([cx-int(r*0.35)-er, ey-er, cx-int(r*0.35)+er, ey+er], fill=LINE)
            d.arc([cx+int(r*0.35)-er-2, ey-er, cx+int(r*0.35)+er+2, ey+er], 200, 340, fill=LINE, width=max(3, r//10))
        elif mood=="laugh":
            d.arc([cx-int(r*0.35)-er, ey-er, cx-int(r*0.35)+er, ey+er], 200, 340, fill=LINE, width=max(3, r//10))
            d.arc([cx+int(r*0.35)-er, ey-er, cx+int(r*0.35)+er, ey+er], 200, 340, fill=LINE, width=max(3, r//10))
        elif mood=="love":
            for sx in (-1, 1):
                hx=cx+sx*int(r*0.35); hy=ey
                d.polygon([(hx,hy+er),(hx-er,hy-er//2),(hx+er,hy-er//2)], fill=PINK)
        else:
            d.ellipse([cx-int(r*0.35)-er, ey-er, cx-int(r*0.35)+er, ey+er], fill=LINE)
            d.ellipse([cx+int(r*0.35)-er, ey-er, cx+int(r*0.35)+er, ey+er], fill=LINE)
            # shine
            d.ellipse([cx-int(r*0.35)-er//2, ey-er, cx-int(r*0.35), ey-er//3], fill=WHITE)
            d.ellipse([cx+int(r*0.35)-er//2, ey-er, cx+int(r*0.35), ey-er//3], fill=WHITE)
    elif mood in ("sad","cry","sorry","tired"):
        d.arc([cx-int(r*0.35)-er, ey-er//2, cx-int(r*0.35)+er, ey+er], 20, 160, fill=LINE, width=max(3, r//10))
        d.arc([cx+int(r*0.35)-er, ey-er//2, cx+int(r*0.35)+er, ey+er], 20, 160, fill=LINE, width=max(3, r//10))
        if mood=="cry":
            d.ellipse([cx-int(r*0.35)-3, ey+er, cx-int(r*0.35)+3, ey+er+int(r*0.35)], fill=(56,189,248))
    elif mood=="angry":
        d.line([(cx-int(r*0.55), ey-er), (cx-int(r*0.18), ey-er//2)], fill=LINE, width=max(3, r//10))
        d.line([(cx+int(r*0.55), ey-er), (cx+int(r*0.18), ey-er//2)], fill=LINE, width=max(3, r//10))
        d.ellipse([cx-int(r*0.35)-er, ey-er//2, cx-int(r*0.35)+er, ey+er], fill=LINE)
        d.ellipse([cx+int(r*0.35)-er, ey-er//2, cx+int(r*0.35)+er, ey+er], fill=LINE)
    elif mood=="shocked":
        d.ellipse([cx-int(r*0.38)-er-2, ey-er-2, cx-int(r*0.38)+er+2, ey+er+2], fill=WHITE, outline=LINE, width=2)
        d.ellipse([cx+int(r*0.38)-er-2, ey-er-2, cx+int(r*0.38)+er+2, ey+er+2], fill=WHITE, outline=LINE, width=2)
        d.ellipse([cx-int(r*0.38)-er//2, ey-er//2, cx-int(r*0.38)+er//2, ey+er//2], fill=LINE)
        d.ellipse([cx+int(r*0.38)-er//2, ey-er//2, cx+int(r*0.38)+er//2, ey+er//2], fill=LINE)
    else:
        d.ellipse([cx-int(r*0.35)-er, ey-er, cx-int(r*0.35)+er, ey+er], fill=LINE)
        d.ellipse([cx+int(r*0.35)-er, ey-er, cx+int(r*0.35)+er, ey+er], fill=LINE)
    # mouth
    my=cy+int(r*0.42)
    if mood in ("happy","ok","thumbs","wink"):
        d.arc([cx-int(r*0.35), my-int(r*0.25), cx+int(r*0.35), my+int(r*0.22)], 20, 160, fill=LINE, width=max(3, r//9))
    elif mood=="laugh" or mood=="celebrate":
        d.pieslice([cx-int(r*0.32), my-int(r*0.2), cx+int(r*0.32), my+int(r*0.32)], 10, 170, fill=(180,40,50), outline=LINE, width=2)
    elif mood=="love":
        d.ellipse([cx-int(r*0.12), my-int(r*0.06), cx+int(r*0.12), my+int(r*0.16)], fill=(180,40,50))
    elif mood in ("sad","cry","sorry","tired"):
        d.arc([cx-int(r*0.28), my-int(r*0.1), cx+int(r*0.28), my+int(r*0.28)], 200, 340, fill=LINE, width=max(3, r//9))
    elif mood=="angry":
        d.line([(cx-int(r*0.2), my+int(r*0.05)), (cx+int(r*0.2), my+int(r*0.05))], fill=LINE, width=max(3, r//9))
    elif mood=="shocked":
        d.ellipse([cx-int(r*0.14), my-int(r*0.08), cx+int(r*0.14), my+int(r*0.22)], fill=(40,20,20), outline=LINE, width=2)
    else:
        d.arc([cx-int(r*0.28), my-int(r*0.2), cx+int(r*0.28), my+int(r*0.16)], 20, 160, fill=LINE, width=max(3, r//9))

def make(W,H,name):
    port=H>W; m=W//2; S=int(W*(0.20 if port else 0.16))
    left=bg(W,H,(255,236,220),(255,214,200),3,11)
    # phone frame with illustrated selfie
    pw,ph=int(S*2.05), int(S*(3.05 if port else 2.85))
    px,py=m//2-pw//2, int(H*(0.16 if port else 0.18))
    ld=ImageDraw.Draw(left)
    ld.rounded_rectangle([px,py,px+pw,py+ph], radius=36, fill=(30,30,36,255), outline=(80,80,90,255), width=5)
    ld.rounded_rectangle([px+10,py+10,px+pw-10,py+ph-10], radius=28, fill=(255,240,230,255))
    cx, cy, r = m//2, py+int(ph*0.48), int(S*0.62)
    chibi(left, cx, cy, r, "happy")
    ld.text((m//2, py+int(ph*0.88)), "เซลฟี่ 1 รูป", font=F('SemiBold', int(S*0.16)), fill=NAVY, anchor='mm')

    right=bg(W,H,(255,250,240),(255,228,230),2,12)
    rd=ImageDraw.Draw(right)
    moods=["happy","laugh","love","wink","ok","sad","angry","shocked"]
    labels=["ยิ้ม","ฮา","รัก","ขยิบ","โอเค","เศร้า","โกรธ","ตกใจ"]
    bub=["เข้าใจแล้ว","สุดยอด!","รักนะ","เดี๋ยวมา","","","",""]
    cols, rows = 4, 2
    grid_w=int(m*0.88); grid_h=int(H*(0.42 if port else 0.38))
    gx0=m+(m-grid_w)//2; gy0=int(H*(0.16 if port else 0.18))
    gap=10; cw=(grid_w-gap*(cols-1))//cols; ch=(grid_h-gap*(rows-1))//rows
    for i,mood in enumerate(moods):
        r0,c0=divmod(i, cols) if False else (i//cols, i%cols)
        x=gx0+c0*(cw+gap); y=gy0+r0*(ch+gap)
        rd.rounded_rectangle([x,y,x+cw,y+ch], radius=16, fill=WHITE+(255,), outline=(253,186,116,255), width=3)
        # draw on a crop? just draw at cell center
        cr=int(min(cw,ch)*0.28)
        chibi(right, x+cw//2, y+int(ch*0.42), cr, mood)
        if bub[i]:
            rd.rounded_rectangle([x+6, y+ch-int(ch*0.32), x+cw-6, y+ch-6], radius=10, fill=PINK+(255,))
            rd.text((x+cw//2, y+ch-int(ch*0.16)-3), bub[i], font=F('SemiBold', max(14, int(S*0.09))), fill=WHITE, anchor='mm')
        else:
            rd.text((x+cw//2, y+ch-int(ch*0.16)), labels[i], font=F('Medium', max(14, int(S*0.10))), fill=NAVY, anchor='mm')

    im=right.copy(); im.paste(left.crop((0,0,m,H)),(0,0))
    ov=Image.new('RGBA',(W,H),(0,0,0,0)); od=ImageDraw.Draw(ov); gh=int(H*0.40)
    for i in range(gh): od.line([(0,H-gh+i),(W,H-gh+i)], fill=(40,20,24,int(235*(i/gh)**1.2)))
    im=Image.alpha_composite(im,ov); d=ImageDraw.Draw(im)
    d.rectangle([m-3,0,m+3,H], fill='white')
    cy2=int(H*0.30); d.ellipse([m-34,cy2-34,m+34,cy2+34], fill='white', outline=(0,0,0,60), width=2)
    d.text((m-14,cy2),'◀',font=F('Regular',26),fill=(40,40,40),anchor='mm'); d.text((m+14,cy2),'▶',font=F('Regular',26),fill=(40,40,40),anchor='mm')
    top=int(H*0.09) if port else 100
    pill(d,m//2,top,'BEFORE',(0,0,0,170),'white',F('SemiBold',34),'mm')
    pill(d,m+m//2,top,'AFTER',YELLOW+(255,),(30,20,0),F('SemiBold',34),'mm')
    pill(d,W//2,48,'AI วันละแอป · แจกฟรี / Free',(255,255,255,235),(25,25,25),F('Medium',32),'mm')
    chip_y = max(py+ph, gy0+grid_h) + (48 if port else 38)
    pill(d,m//2,chip_y,'เซลฟี่ใบเดียว',(0,0,0,170),'white',F('Medium',24),'mm')
    pill(d,m+m//2,chip_y,'ชุด 16 อารมณ์ + ข้อความไทย',(255,255,255,240),NAVY,F('Medium',24),'mm')
    pill(d,m+m//2,chip_y+(58 if port else 52),'พร้อมส่ง Creators 370×320',PINK+(255,),WHITE,F('SemiBold',22),'mm')
    s=1.0 if port else 0.85
    y=H-int(56*s)
    d.text((W//2,y),'One selfie → a LINE sticker set of your face',font=F('Regular',int(32*s)),fill=(255,230,230),anchor='ms'); y-=int(72*s)
    d.text((W//2,y),'เซลฟี่เดียว ได้สติกเกอร์หน้าตัวเองทั้งเซ็ต',font=F('SemiBold',int(40*s)),fill=(255,205,90),anchor='ms'); y-=int(92*s)
    d.text((W//2,y),'StickerMe',font=F('Bold',int(100*s)),fill='white',anchor='ms',stroke_width=2,stroke_fill=(0,0,0))
    im.convert('RGB').save(name)

make(1080,1350,'cover_1080x1350.png'); make(1080,1080,'cover_1080x1080.png')
print("covers written")
