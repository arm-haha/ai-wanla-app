# Reference implementation of VoiceMood mood rules (mirror of lib/mood.ts)
LEXICON = [
 # term, valence, energy, theme
 ("ประชุมด่วน",-1,2,"work"),("โดนแก้",-1,1,"work"),("เดดไลน์",-1,2,"work"),("หัวหน้าชม",2,1,"work"),
 ("งานเสร็จ",2,1,"work"),("ทำโอที",-1,-1,"work"),
 ("นอนน้อย",-1,-2,"sleep"),("นอนไม่หลับ",-2,-1,"sleep"),("ได้นอนเต็มอิ่ม",2,2,"sleep"),
 ("เหนื่อย",-2,-3,"body"),("ปวดหัว",-1,-1,"body"),("สดชื่น",2,2,"body"),
 ("แมว",1,0,"pet"),
 ("เจอเพื่อน",2,2,"friends"),("เพื่อนเท",-2,0,"friends"),("หัวเราะ",2,1,"friends"),
 ("โทรหาแม่",1,0,"family"),("ทะเลาะกับที่บ้าน",-3,2,"family"),
 ("เงินเดือนออก",2,2,"money"),("เงินไม่พอ",-2,1,"money"),
 ("รถติด",-1,1,"commute"),
 ("ไปวิ่ง",2,2,"exercise"),("โยคะ",1,1,"exercise"),
 ("ชาบู",1,1,"food"),("ชานม",1,1,"food"),
 ("แฟน",1,1,"love"),
 ("เครียด",-2,2,"feeling"),("กังวล",-2,1,"feeling"),("เหงา",-2,-1,"feeling"),("เบื่อ",-1,-2,"feeling"),
 ("โกรธ",-3,3,"feeling"),("ดีใจ",3,2,"feeling"),("มีความสุข",3,1,"feeling"),("สบายใจ",2,-1,"feeling"),
 ("ภูมิใจ",3,1,"feeling"),("ไม่อยากทำอะไร",-1,-3,"feeling"),("ดีขึ้น",1,1,"feeling"),
 ("ขอบคุณ",1,0,"feeling"),("ผ่อนคลาย",2,-2,"feeling"),
]
QUAD = {
 "bright":("สดใส มีพลัง","#FACC15","#FDE68A"),
 "calm":("สงบ สบายใจ","#34D399","#A7F3D0"),
 "tense":("เครียด ร้อนรน","#FB7185","#FDA4AF"),
 "low":("หม่น เหนื่อยล้า","#818CF8","#C7D2FE"),
 "neutral":("กลางๆ เรื่อยๆ","#C4B5FD","#EDE9FE"),
}
def jsround(x):
    import math
    return math.floor(x+0.5)
def clamp(x,a,b): return max(a,min(b,x))
def weather(score):
    if score>=80: return ("sunny","แดดจ้า","☀️")
    if score>=60: return ("clear","ฟ้าโปร่ง","⛅")
    if score>=41: return ("cloudy","เมฆครึ้ม","☁️")
    if score>=21: return ("drizzle","ฝนพรำ","🌧️")
    return ("storm","พายุเข้า","⛈️")
def analyze(text):
    used=[False]*len(text)
    matched=[]
    for term,v,e,th in sorted(LEXICON,key=lambda t:-len(t[0])):
        start=0
        while True:
            i=text.find(term,start)
            if i<0: break
            if not any(used[i:i+len(term)]):
                neg = (not term.startswith("ไม่")) and text[max(0,i-3):i]=="ไม่"
                for k in range(i,i+len(term)): used[k]=True
                vv = -v if neg else v
                ee = 0 if neg else e
                matched.append({"term":term,"index":i,"valence":vv,"energy":ee,"theme":th,"negated":neg})
                break
            start=i+1
    matched.sort(key=lambda m:m["index"])
    sv=sum(m["valence"] for m in matched); se=sum(m["energy"] for m in matched)
    v=clamp(sv,-8,8); e=clamp(se,-8,8)
    score=jsround((v+8)/16*100); energy=jsround((e+8)/16*10)
    if v==0: q="neutral"
    elif v>0: q="bright" if energy>=6 else "calm"
    else: q="tense" if energy>=6 else "low"
    themes=[]
    for m in matched:
        if m["theme"]!="feeling" and m["theme"] not in themes: themes.append(m["theme"])
    w=weather(score)
    lab,c1,c2=QUAD[q]
    return {"valence_sum":sv,"energy_sum":se,"valence":v,"energy":energy,"score":score,"quadrant":q,
            "label_th":lab,"weather":{"key":w[0],"label_th":w[1],"emoji":w[2]},
            "aura":{"primary":c1,"secondary":c2},"themes":themes,"matched_terms":matched}
