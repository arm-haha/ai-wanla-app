"""HomeworkHero deterministic logic (no AI calls). Hints, scripts and practice items are app-chosen examples — not an official curriculum, and never a key that gives the child's homework answer in the hint path."""
import urllib.parse as _up
from copy import deepcopy

MIN_CONF = 0.6
FREE_SCANS_PER_DAY = 3
WATERMARK = "Made with HomeworkHero · hints only, not the answer"
SAFETY_DISCLAIMER_TH = "HomeworkHero ให้คำใบ้และวิธีคิดทีละขั้น ไม่บอกคำตอบของการบ้านลูกในหน้าหลัก เป็นเครื่องมือช่วยผู้ปกครองสอน ไม่ใช่ครู ไม่ใช่หลักสูตร สพฐ. อย่างเป็นทางการ และไม่ใช้ทำงานให้ลูก"
LEVELS = ["p1","p2","p3","p4","p5","p6","m1","m2","m3","m4","m5","m6"]
LEVEL_TH = {f"p{i}": f"ประถมศึกษาปีที่ {i}" for i in range(1,7)}
LEVEL_TH.update({f"m{i}": f"มัธยมศึกษาปีที่ {i}" for i in range(1,7)})
SUBJECTS = ["math","thai","sci","eng"]
SUB_TH = {"math":"คณิตศาสตร์","thai":"ภาษาไทย","sci":"วิทยาศาสตร์","eng":"ภาษาอังกฤษ"}
HINT_LEVELS = (1, 2, 3)

def _templates():
    # Built as data + callables below.
    return TEMPLATES

def _hint_percent(f):
    return [
        "โจทย์ถามหาราคาที่ต้องจ่ายหลังลดแล้ว ไม่ใช่จำนวนเงินที่ลดเพียงอย่างเดียว",
        "ร้อยละในโจทย์แปลว่า 'กี่ส่วนใน 100' ลองคิดเป็นเศษส่วนอย่างง่าย หรือหารร้อยก่อน แล้วคูณกับราคาเดิม เพื่อหาเงินที่ลด",
        f"วิธี: เงินที่ลด = ราคาเดิม × (ร้อยละ ÷ 100) แล้วราคาที่จ่าย = ราคาเดิม − เงินที่ลด แทนตัวเลขจากโจทย์ในช่องว่าง: เงินที่ลด = {f['price']} × ({f['percent']} ÷ 100) = ____ จากนั้น ราคาที่จ่าย = {f['price']} − ____ = ____",
    ]

def _ans_percent(f):
    off = f["price"] * f["percent"] / 100
    pay = f["price"] - off
    # keep integer if exact
    if off == int(off) and pay == int(pay):
        off, pay = int(off), int(pay)
    return {"discount": off, "pay": pay, "display_th": f"ราคาที่จ่าย {pay} บาท"}

def _sim_percent(seed):
    pairs = [(1200, 20), (500, 10), (2000, 15), (450, 20), (360, 25)]
    p, pct = pairs[seed % len(pairs)]
    return {"price": p, "percent": pct}

def _hint_area(f):
    return [
        "โจทย์ถามพื้นที่ ซึ่งเป็นเนื้อที่ในรูป ไม่ใช่ความยาวรอบรูป",
        "รูปสี่เหลี่ยมมุมฉาก หาพื้นที่ด้วยด้านคู่ยาวคูณด้านคู่กว้าง ดูหน่วยให้ตรงกันก่อนคูณ",
        f"วิธี: พื้นที่ = ยาว × กว้าง แทนตัวเลข: {f['length']} × {f['width']} = ____ ตาราง{f['unit']}",
    ]

def _ans_area(f):
    a = f["length"] * f["width"]
    if a == int(a):
        a = int(a)
    return {"area": a, "display_th": f"พื้นที่ {a} ตาราง{f['unit']}"}

def _sim_area(seed):
    pairs = [(12, 7, "เมตร"), (8, 5, "เซนติเมตร"), (15, 4, "เมตร"), (9, 9, "เซนติเมตร")]
    L, W, u = pairs[seed % len(pairs)]
    return {"length": L, "width": W, "unit": u}

def _hint_fraction(f):
    return [
        "โจทย์ถามว่า 'เศษส่วนของจำนวน' คือการแบ่งจำนวนออกเป็นส่วนเท่า ๆ แล้วเอาบางส่วน",
        "ตัวส่วนบอกว่าแบ่งกี่ส่วน ตัวเศษบอกว่าเอาไปกี่ส่วน ลองแบ่งจำนวนออกเป็นส่วนเท่ากับตัวส่วนก่อน",
        f"วิธี: ค่าที่ขอ = จำนวน × (เศษ ÷ ส่วน) = {f['whole']} × ({f['num']} ÷ {f['den']}) ทำในวงเล็บก่อน แล้วคูณ ได้ ____",
    ]

def _ans_fraction(f):
    v = f["whole"] * f["num"] / f["den"]
    if v == int(v):
        v = int(v)
    return {"value": v, "display_th": f"ได้ {v}"}

def _sim_fraction(seed):
    triples = [(24, 1, 3), (18, 2, 3), (40, 3, 5), (30, 1, 2)]
    w, n, d = triples[seed % len(triples)]
    return {"whole": w, "num": n, "den": d}

def _hint_unitrate(f):
    return [
        "โจทย์ให้ของหลายชิ้นกับราคารวม แล้วถามราคาต่อหน่วย หรือจำนวนที่ซื้อได้ในงบ",
        "หา 'ต่อ 1 หน่วย' ก่อนเสมอ โดยเอาปริมาณไปหารยอดรวม แล้วค่อยนำไปใช้ต่อ",
        f"วิธี: ราคาต่อหน่วย = ราคารวม ÷ จำนวน = {f['total']} ÷ {f['qty']} = ____ บาท/หน่วย",
    ]

def _ans_unitrate(f):
    r = f["total"] / f["qty"]
    if r == int(r):
        r = int(r)
    return {"rate": r, "display_th": f"หน่วยละ {r} บาท"}

def _sim_unitrate(seed):
    pairs = [(120, 5), (360, 6), (250, 10), (480, 8)]
    t, q = pairs[seed % len(pairs)]
    return {"total": t, "qty": q}

def _hint_average(f):
    return [
        "ค่าเฉลี่ยคือค่ากลางที่ได้จากการรวมข้อมูลแล้วหารด้วยจำนวนครั้ง/จำนวนตัว",
        "อย่าลืมหารด้วยจำนวนตัวทั้งหมด ไม่ใช่หารด้วยตัวใดตัวหนึ่ง",
        f"วิธี: ค่าเฉลี่ย = ({' + '.join(str(x) for x in f['values'])}) ÷ {len(f['values'])} = ____",
    ]

def _ans_average(f):
    v = sum(f["values"]) / len(f["values"])
    if v == int(v):
        v = int(v)
    return {"average": v, "display_th": f"ค่าเฉลี่ย {v}"}

def _sim_average(seed):
    sets = [[8, 10, 12], [5, 7, 9, 11], [20, 30, 40], [6, 6, 9]]
    return {"values": list(sets[seed % len(sets)])}

def _hint_decimal_add(f):
    return [
        "การบวกทศนิยมต้องให้จุดทศนิยมอยู่ตรงแนวเดียวกันก่อน แล้วบวกทีละหลัก",
        "ถ้าจำนวนหลักหลังจุดไม่เท่ากัน ให้เติมศูนย์ให้เท่ากันจะบวกง่ายขึ้น",
        f"วิธี: จัดแนวจุดทศนิยมแล้วบวก {f['a']} + {f['b']} = ____",
    ]

def _ans_decimal(f):
    v = round(f["a"] + f["b"], 4)
    if v == int(v):
        v = int(v)
    return {"sum": v, "display_th": f"ผลบวก {v}"}

def _sim_decimal(seed):
    pairs = [(1.25, 2.5), (0.8, 1.35), (3.07, 0.9), (12.5, 4.75)]
    a, b = pairs[seed % len(pairs)]
    return {"a": a, "b": b}

def _hint_classifier(f):
    return [
        "โจทย์ถามคำราชาศัพท์หรือคำสุภาพที่ใช้กับคำนามในประโยค ไม่ใช่แปลทั้งประโยค",
        "ดูว่าคำนามในโจทย์เป็นคน สัตว์ สิ่งของ หรือสิ่งที่เป็นทางการ แล้วเลือกคำที่เข้าชุดกับคำนามนั้น",
        f"วิธี: หาคำนามหลักในประโยค «{f['sentence']}» แล้วเลือกคำที่โจทย์ให้มาซึ่งใช้คู่กับคำนามนั้น คำตอบคือช่องว่าง ____",
    ]

def _ans_classifier(f):
    return {"word": f["answer"], "display_th": f"คำที่ใช้คือ «{f['answer']}»"}

def _sim_classifier(seed):
    items = [
        {"sentence": "คุณครู____หนังสือให้เพื่อน", "answer": "แจก", "choices": ["แจก", "พระราชทาน", "ป้อน"]},
        {"sentence": "แม่____ข้าวให้ลูก", "answer": "ตัก", "choices": ["ตัก", "ริน", "ฉัน"]},
    ]
    return dict(items[seed % len(items)])

def _hint_cycle(f):
    return [
        "โจทย์วิทยาศาสตร์เรื่องวัฏจักรน้ำถาม 'กระบวนการ' ไม่ใช่ชื่อก้อนเมฆอย่างเดียว",
        "ไล่ตามลำดับ: น้ำเปลี่ยนเป็นไอ ขึ้นไปบนฟ้า แล้วกลายเป็นน้ำอีกครั้ง",
        f"วิธี: จากคำใบ้ «{f['clue']}» เลือกชื่อกระบวนการที่ตรงที่สุดจากบทเรียน ช่องว่างคือ ____",
    ]

def _ans_cycle(f):
    return {"process": f["answer"], "display_th": f"กระบวนการคือ {f['answer']}"}

def _sim_cycle(seed):
    items = [
        {"clue": "น้ำในทะเลกลายเป็นไอเมื่อโดนความร้อน", "answer": "การระเหย"},
        {"clue": "ไอน้ำเย็นตัวแล้วรวมเป็นหยดน้ำในเมฆ", "answer": "การควบแน่น"},
        {"clue": "หยดน้ำในเมฆหนักจนตกลงมา", "answer": "หยาดน้ำฟ้า"},
    ]
    return dict(items[seed % len(items)])

def _hint_tense(f):
    return [
        "ดูคำบอกเวลาในประโยคภาษาอังกฤษ ว่าเหตุการณ์จบแล้ว กำลังทำ หรือทำเป็นประจำ",
        "คำว่า yesterday / last ... มักใช้รูปอดีต คำว่า every / always มักใช้ปัจจุบันง่าย",
        f"วิธี: ประโยค «{f['sentence']}» มีคำบอกเวลาคือ «{f['time_word']}» เลือกกริยารูปที่เข้ากับคำนั้น ช่องว่างคือ ____",
    ]

def _ans_tense(f):
    return {"verb": f["answer"], "display_th": f"ใช้ «{f['answer']}»"}

def _sim_tense(seed):
    items = [
        {"sentence": "She ____ to school every day.", "time_word": "every day", "answer": "goes", "choices": ["goes", "went", "going"]},
        {"sentence": "They ____ football yesterday.", "time_word": "yesterday", "answer": "played", "choices": ["play", "played", "playing"]},
    ]
    return dict(items[seed % len(items)])

def _hint_linear(f):
    return [
        "สมการถามค่าของตัวไม่ทราบค่า เป้าหมายคือทำให้ตัวแปรอยู่คนละข้างกับตัวเลข",
        "ทำค้างกับเครื่องหมายที่เห็น: มีบวกให้ลบออก ทั้งสองข้าง มีคูณให้หารทั้งสองข้าง",
        f"วิธี: จาก {f['a']}x + {f['b']} = {f['c']} ลบ {f['b']} ทั้งสองข้าง ได้ {f['a']}x = ____ แล้วหารทั้งสองข้างด้วย {f['a']} ได้ x = ____",
    ]

def _ans_linear(f):
    x = (f["c"] - f["b"]) / f["a"]
    if x == int(x):
        x = int(x)
    return {"x": x, "display_th": f"x = {x}"}

def _sim_linear(seed):
    triples = [(2, 3, 11), (3, 5, 20), (4, 1, 21), (5, 0, 15)]
    a, b, c = triples[seed % len(triples)]
    return {"a": a, "b": b, "c": c}

TEMPLATES = {
    "percent_discount": {
        "id": "t01", "subject": "math", "level": "p4", "name_th": "โจทย์ปัญหาร้อยละ (ลดราคา)",
        "skill_th": "จำนวนและการดำเนินการ · ร้อยละ", "fields": ("price", "percent"),
        "hints": _hint_percent, "answer": _ans_percent, "similar": _sim_percent,
        "mistakes_th": ["คิดแค่เงินที่ลดแล้วยกเป็นคำตอบ", "คูณร้อยละโดยไม่หาร 100", "ลืมลบออกจากราคาเดิม"],
        "parent_th": [
            "ถามว่า 'โจทย์อยากได้ราคาที่จ่าย หรือเงินที่ลด'",
            "อย่าบอกตัวเลขสุดท้าย ชวนวาดแท่ง 100 ส่วน หรือใช้ของจริงในครัว",
            "ถ้าติดที่คูณร้อยละ ให้ถามว่า 25 ใน 100 คือกี่ส่วนจาก 4 ส่วน",
        ],
    },
    "area_rect": {
        "id": "t02", "subject": "math", "level": "p3", "name_th": "พื้นที่สี่เหลี่ยมมุมฉาก",
        "skill_th": "การวัด · พื้นที่", "fields": ("length", "width", "unit"),
        "hints": _hint_area, "answer": _ans_area, "similar": _sim_area,
        "mistakes_th": ["หาความยาวรอบรูปแทนพื้นที่", "คูณแล้วใส่หน่วยเป็นเซนติเมตรแทนตารางหน่วย"],
        "parent_th": ["ถามความต่างระหว่าง 'รอบรูป' กับ 'พื้นที่'", "ให้ลูกชี้ด้านยาวและด้านกว้างบนรูปก่อนคูณ"],
    },
    "fraction_of": {
        "id": "t03", "subject": "math", "level": "p5", "name_th": "เศษส่วนของจำนวน",
        "skill_th": "จำนวนและการดำเนินการ · เศษส่วน", "fields": ("whole", "num", "den"),
        "hints": _hint_fraction, "answer": _ans_fraction, "similar": _sim_fraction,
        "mistakes_th": ["คูณตัวเศษอย่างเดียวแล้วหารด้วยจำนวน", "สลับเศษกับส่วน"],
        "parent_th": ["ให้แบ่งของจริง (เช่น ลูกอม) เป็นส่วนเท่า ๆ ตามตัวส่วน แล้วนับตามตัวเศษ"],
    },
    "unit_rate": {
        "id": "t04", "subject": "math", "level": "p6", "name_th": "ราคาต่อหน่วย",
        "skill_th": "อัตราส่วนและร้อยละ · ราคาต่อหน่วย", "fields": ("total", "qty"),
        "hints": _hint_unitrate, "answer": _ans_unitrate, "similar": _sim_unitrate,
        "mistakes_th": ["เอาจำนวนไปหารราคาผิดทาง", "ลืมหน่วยต่อชิ้น"],
        "parent_th": ["ถามว่า 'ถ้าของ 1 ชิ้นจะราคาเท่าไร' ก่อนโจทย์ข้อต่อไป"],
    },
    "average": {
        "id": "t05", "subject": "math", "level": "p5", "name_th": "ค่าเฉลี่ยเลขคณิต",
        "skill_th": "สถิติ · ค่ากลาง", "fields": ("values",),
        "hints": _hint_average, "answer": _ans_average, "similar": _sim_average,
        "mistakes_th": ["รวมแล้วไม่หาร", "หารด้วยจำนวนตัวที่ผิด"],
        "parent_th": ["ให้ลูกนับว่ามีข้อมูลกี่ตัวก่อนหาร"],
    },
    "decimal_add": {
        "id": "t06", "subject": "math", "level": "p4", "name_th": "บวกทศนิยม",
        "skill_th": "จำนวนและการดำเนินการ · ทศนิยม", "fields": ("a", "b"),
        "hints": _hint_decimal_add, "answer": _ans_decimal, "similar": _sim_decimal,
        "mistakes_th": ["ไม่จัดแนวจุดทศนิยม", "เติมศูนย์ผิดหลัก"],
        "parent_th": ["ให้เขียนแนวตั้ง จุดทศนิยมต้องอยู่ตรงกัน แล้วค่อยบวก"],
    },
    "thai_word_choice": {
        "id": "t07", "subject": "thai", "level": "p4", "name_th": "เลือกคำให้เหมาะกับคำนาม",
        "skill_th": "หลักการใช้ภาษา · คำและชนิดของคำ", "fields": ("sentence", "answer", "choices"),
        "hints": _hint_classifier, "answer": _ans_classifier, "similar": _sim_classifier,
        "mistakes_th": ["เลือกคำสุภาพเกินไปหรือน้อยไปโดยไม่ดูคำนาม"],
        "parent_th": ["อ่านประโยคดัง ๆ แล้วถามว่าใครทำอะไรกับอะไร อย่าชี้นิ้วที่ตัวเลือกทันที"],
    },
    "water_cycle": {
        "id": "t08", "subject": "sci", "level": "p5", "name_th": "กระบวนการในวัฏจักรน้ำ",
        "skill_th": "วิทยาศาสตร์กายภาพ · น้ำและอากาศ", "fields": ("clue", "answer"),
        "hints": _hint_cycle, "answer": _ans_cycle, "similar": _sim_cycle,
        "mistakes_th": ["สับสนการระเหยกับการควบแน่น"],
        "parent_th": ["ชวนนึกถึงหม้อน้ำเดือดและฝาหม้อเป็นไอค้าง อย่าบอกชื่อกระบวนการก่อน"],
    },
    "eng_tense": {
        "id": "t09", "subject": "eng", "level": "m1", "name_th": "เลือกกาลของกริยา",
        "skill_th": "English · verb tense", "fields": ("sentence", "time_word", "answer", "choices"),
        "hints": _hint_tense, "answer": _ans_tense, "similar": _sim_tense,
        "mistakes_th": ["ดูประธานอย่างเดียวแล้วลืมคำบอกเวลา"],
        "parent_th": ["ชี้คำบอกเวลาให้ลูกอ่านก่อนเลือกกริยา อย่าแปลทั้งประโยคให้"],
    },
    "linear_eq": {
        "id": "t10", "subject": "math", "level": "m2", "name_th": "สมการเชิงเส้นตัวแปรเดียว",
        "skill_th": "พีชคณิต · สมการ", "fields": ("a", "b", "c"),
        "hints": _hint_linear, "answer": _ans_linear, "similar": _sim_linear,
        "mistakes_th": ["ย้ายข้างแล้วไม่เปลี่ยนเครื่องหมาย", "หารแค่ข้างเดียว"],
        "parent_th": ["ให้ลูกพูดว่า 'ทำเหมือนกันทั้งสองข้าง' ทุกครั้งที่ย้ายค่า"],
    },
}

# Default fields for the "scanned homework" demo items live in fixtures.
# ------------------- quality / scan -------------------

def scan_quality(glare, blur, tilt, text_fill):
    for v in (glare, blur, tilt, text_fill):
        if not 0 <= v <= 1:
            raise ValueError("quality inputs must be 0..1")
    score = round(100 * (1 - (0.30 * glare + 0.35 * blur + 0.20 * tilt + 0.15 * (1 - text_fill))))
    tips = []
    if glare > 0.5:
        tips.append("แสงสะท้อนบนกระดาษ เอียงมือถือหรือปิดไฟด้านบน")
    if blur > 0.4:
        tips.append("ตัวอักษรเบลอ ถ่ายใกล้ขึ้นและแตะโฟกัสที่โจทย์")
    if tilt > 0.4:
        tips.append("ถ่ายเอียงเกินไป วางสมุดราบแล้วถ่ายจากด้านบน")
    if text_fill < 0.5:
        tips.append("โจทย์ไม่เต็มกรอบ ขยับกล้องให้อยู่ทั้งข้อ")
    ok = score >= 60 and text_fill >= 0.5
    if not ok and not tips:
        tips.append("ถ่ายใหม่ให้โจทย์ชัด ทั้งข้อ แสงนุ่ม")
    return {"score": score, "ok": ok, "tips_th": tips}

def identify_problem(photo, min_conf=MIN_CONF):
    tid = photo["template"]
    if tid not in TEMPLATES:
        raise ValueError("unknown template " + tid)
    if photo["confidence"] < min_conf:
        return {"ok": False, "template": tid, "uncertain": True, "message_th": "ยังอ่านโจทย์ไม่ชัด ถ่ายใหม่หรือเลือกวิชา/ระดับเอง"}
    t = TEMPLATES[tid]
    return {"ok": True, "template": tid, "uncertain": False, "subject": t["subject"], "level": t["level"], "message_th": ""}

def homework_scan(photo):
    q = scan_quality(photo["glare"], photo["blur"], photo["tilt"], photo["text_fill"])
    ident = identify_problem(photo)
    t = TEMPLATES[photo["template"]]
    return {
        "photo_id": photo["id"], "quality": q, "template": photo["template"],
        "name_th": t["name_th"], "subject": t["subject"], "subject_th": SUB_TH[t["subject"]],
        "level": t["level"], "level_th": LEVEL_TH[t["level"]], "skill_th": t["skill_th"],
        "fields": photo["fields"], "ok": q["ok"] and ident["ok"],
        "uncertain": ident["uncertain"], "message_th": ident["message_th"],
        "disclaimer_th": SAFETY_DISCLAIMER_TH,
    }

def pipeline_steps(photo):
    s = ["page_detect"]
    if photo["glare"] > 0.5:
        s.append("deglare")
    if photo["tilt"] > 0.4:
        s.append("deskew")
    s += ["ocr_block", "template_match", "hint_tree", "parent_script", "practice"]
    return s

def _require_template(tid, fields):
    if tid not in TEMPLATES:
        raise ValueError("unknown template " + tid)
    t = TEMPLATES[tid]
    missing = [k for k in t["fields"] if k not in fields]
    if missing:
        raise ValueError("missing fields " + ",".join(missing))
    return t

def _answer_strings(ans):
    out = set()
    for v in ans.values():
        if isinstance(v, bool):
            continue
        out.add(str(v))
        if isinstance(v, float) and v == int(v):
            out.add(str(int(v)))
    return {x for x in out if x and x not in ("display_th",)}

def step_hints(tid, fields, upto=3):
    t = _require_template(tid, fields)
    if upto not in HINT_LEVELS:
        raise ValueError("upto must be 1, 2 or 3")
    texts = t["hints"](fields)
    items = [{"n": i + 1, "text_th": texts[i], "reveals_answer": False} for i in range(upto)]
    # Guard: first two hints must not contain the final answer tokens.
    ans = t["answer"](fields)
    banned = set()
    for k, v in ans.items():
        if k == "display_th":
            continue
        if isinstance(v, (int, float)):
            banned.add(str(int(v)) if v == int(v) else str(v))
        elif isinstance(v, str) and len(v) >= 2:
            banned.add(v)
    for it in items:
        if it["n"] <= 2:
            low = it["text_th"]
            for b in banned:
                if b and b in low:
                    raise ValueError(f"hint {it['n']} leaked answer token {b}")
    return {"template": tid, "upto": upto, "hints": items, "disclaimer_th": "คำใบ้ไม่ใช่คำตอบของการบ้าน ลูกควรคิดช่องว่างเอง"}

def parent_script(tid, fields):
    t = _require_template(tid, fields)
    steps = [{"n": i + 1, "text_th": s} for i, s in enumerate(t["parent_th"])]
    return {
        "template": tid, "title_th": "สคริปต์ผู้ปกครอง",
        "intro_th": "อย่าทำข้อให้ลูก ใช้คำถามด้านล่าง แล้วรอคำตอบของลูกก่อนให้คำใบ้ข้อถัดไป",
        "steps": steps, "mistakes_th": list(t["mistakes_th"]),
        "disclaimer_th": SAFETY_DISCLAIMER_TH,
    }

def parent_reveal(tid, fields):
    """Parent-only gate. Do not show this on the child's hint screen."""
    t = _require_template(tid, fields)
    ans = t["answer"](fields)
    return {
        "template": tid, "gated": True, "audience": "parent",
        "answer": ans, "display_th": ans["display_th"],
        "warning_th": "โชว์เฉพาะผู้ปกครอง อย่าอ่านออกเสียงถ้าลูกยังคิดอยู่",
        "disclaimer_th": SAFETY_DISCLAIMER_TH,
    }

def similar_practice(tid, seed=0, count=3):
    t = _require_template(tid, TEMPLATES[tid]["similar"](0) if tid in TEMPLATES else {})
    # re-require after similar default: call similar for each
    items = []
    for i in range(count):
        fields = TEMPLATES[tid]["similar"](seed + i)
        method = TEMPLATES[tid]["hints"](fields)[2]
        items.append({
            "n": i + 1, "fields": fields, "method_th": method,
            "answer_key": TEMPLATES[tid]["answer"](fields),  # parent side
        })
    return {"template": tid, "count": count, "items": items,
            "note_th": "ข้อฝึกเป็นคนละตัวเลขกับงานที่สแกน คำตอบอยู่ใน answer_key สำหรับผู้ปกครองเท่านั้น",
            "disclaimer_th": SAFETY_DISCLAIMER_TH}

def common_mistakes(tid):
    if tid not in TEMPLATES:
        raise ValueError("unknown template " + tid)
    t = TEMPLATES[tid]
    return {"template": tid, "mistakes_th": list(t["mistakes_th"])}

def timebox(minutes, used_minutes, hints_used):
    if minutes <= 0 or used_minutes < 0 or hints_used < 0:
        raise ValueError("bad timebox")
    left = max(0, minutes - used_minutes)
    encourage = "เก่งมากที่พยายามเอง" if hints_used <= 1 else "พักครึ่งนาที แล้วลองคำใบ้ถัดไป"
    if left == 0:
        encourage = "หมดเวลาที่ตั้งไว้ พักได้ แล้วค่อยกลับมาทำข้อฝึกคล้ายกัน"
    return {"minutes": minutes, "used_minutes": used_minutes, "left_minutes": left,
            "hints_used": hints_used, "encourage_th": encourage}

def progress_entry(eid, child_id, date, tid, hints_used, minutes, self_solved, on_device=True):
    if hints_used < 0 or minutes < 0:
        raise ValueError("bad progress")
    return {"id": eid, "child_id": child_id, "date": date, "template": tid,
            "hints_used": hints_used, "minutes": minutes, "self_solved": bool(self_solved),
            "on_device": on_device}

def progress_stats(entries):
    if not entries:
        return {"count": 0, "solved": 0, "avg_hints": 0, "avg_minutes": 0, "last_date": None, "top_template": None}
    solved = sum(1 for e in entries if e["self_solved"])
    avg_h = round(sum(e["hints_used"] for e in entries) / len(entries), 2)
    avg_m = round(sum(e["minutes"] for e in entries) / len(entries), 2)
    last = max(entries, key=lambda e: e["date"])["date"]
    from collections import Counter
    top = Counter(e["template"] for e in entries).most_common(1)[0][0]
    return {"count": len(entries), "solved": solved, "avg_hints": avg_h, "avg_minutes": avg_m,
            "last_date": last, "top_template": top}

def teacher_note(person, scan, hints_used, note_th=""):
    text = (
        f"HomeworkHero — บันทึกถึงครู/ผู้ปกครอง\n"
        f"{person['name_th']} ช่วยดูงาน{scan['subject_th']} {scan['level_th']}\n"
        f"เรื่อง: {scan['name_th']}\n"
        f"ใช้คำใบ้ {hints_used} ระดับ (ไม่เปิดคำตอบในหน้าหลัก)\n"
        f"{note_th}".strip()
    )
    return {
        "title_th": "บันทึกถึงครู",
        "name_th": person["name_th"],
        "subject_th": scan["subject_th"],
        "level_th": scan["level_th"],
        "topic_th": scan["name_th"],
        "hints_used": hints_used,
        "note_th": note_th,
        "line_share_url": "https://line.me/R/share?text=" + _up.quote(text),
        "disclaimer_th": SAFETY_DISCLAIMER_TH,
    }

def share_card(name_th, scan):
    return {
        "title_th": f"HomeworkHero — {name_th}",
        "headline_th": f"{scan['subject_th']} {scan['level_th']} · {scan['name_th']}",
        "hook_th": "ถ่ายการบ้าน ได้วิธีสอนทีละขั้น ไม่บอกคำตอบ",
        "subject": scan["subject"], "level": scan["level"], "layout": "hint_session",
        "sizes": ["1080x1350", "1080x1920", "1080x1080"], "watermark": WATERMARK,
        "cta_th": "คอมเมนต์ HINT รับแพ็กฟรี",
    }

def quota(used_today, want, pro=False):
    if pro:
        return {"allowed": want, "left_after": None, "paywall": False}
    left = max(0, FREE_SCANS_PER_DAY - used_today)
    allowed = min(want, left)
    return {"allowed": allowed, "left_after": left - allowed, "paywall": allowed < want}

def safety_guard(revealed=False):
    if revealed:
        return {"level": "warn", "message_th": "กำลังเปิดคำตอบฝั่งผู้ปกครอง อย่าอ่านให้ลูกฟังถ้ายังคิดอยู่ " + SAFETY_DISCLAIMER_TH}
    return {"level": "ok", "message_th": SAFETY_DISCLAIMER_TH}

def template_info(tid):
    if tid not in TEMPLATES:
        raise ValueError("unknown template " + tid)
    t = TEMPLATES[tid]
    return {"id": t["id"], "template": tid, "name_th": t["name_th"], "subject": t["subject"],
            "subject_th": SUB_TH[t["subject"]], "level": t["level"], "level_th": LEVEL_TH[t["level"]],
            "skill_th": t["skill_th"], "fields": list(t["fields"])}

def level_catalog():
    return [{"level": k, "level_th": LEVEL_TH[k]} for k in LEVELS]
