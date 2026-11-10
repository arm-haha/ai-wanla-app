"""ContractLens deterministic logic (no AI calls). Risk flags, fees and checklists are app-chosen example values — not legal advice, not a lawyer, and not a statement of Thai law."""
import urllib.parse as _up

MIN_CONF = 0.6
FREE_SCANS_PER_DAY = 3
WATERMARK = "Made with ContractLens · not legal advice"
SAFETY_DISCLAIMER_TH = "ContractLens เป็นเครื่องมือช่วยอ่านเบื้องต้น ไม่ใช่คำปรึกษาทางกฎหมาย ไม่ใช่ทนาย และไม่ใช่ข้อความกฎหมาย ก่อนเซ็นควรปรึกษาทนายหรือหน่วยงานที่เชื่อถือได้"
FEE_DISCLAIMER_TH = "ตัวเลขค่าใช้จ่ายเป็นแบบจำลองจากตัวเลขในสัญญาที่กรอก ไม่ใช่ใบแจ้งหนี้และไม่ใช่ค่าธรรมเนียมตามกฎหมาย"
KINDS = ["rental", "loan"]
KIND_TH = {"rental": "สัญญาเช่า", "loan": "สัญญากู้ยืม / สินเชื่อ"}
LEVELS = {"red": "แดง · ควรชะลอการเซ็น", "yellow": "เหลือง · ควรถามให้ชัด", "green": "เขียว · ดูแล้วไม่พบธงตามกฎตัวอย่าง"}
LEVEL_RANK = {"green": 1, "yellow": 2, "red": 3}
REGION_MULT = {"bkk": 1.0, "province": 0.85, "tourist": 1.1}

# Example risk rules chosen by the app — not legal thresholds.
CLAUSES = {
    "auto_renew": {"id": "c01", "name_th": "ต่อสัญญาอัตโนมัติ", "kind": "both", "default_level": "red",
        "meaning_th": "สัญญาอาจต่อเองเมื่อครบกำหนด ถ้าไม่บอกเลิกตามเวลาที่กำหนด",
        "why_th": "อาจถูกผูกต่ออีกช่วงยาวโดยไม่ตั้งใจ",
        "ask_th": ["ต้องบอกเลิกล่วงหน้ากี่วัน และบอกอย่างไรจึงถือว่าถึง", "ถ้าย้ายก่อนครบต่ออัตโนมัติ มีค่าปรับไหม"]},
    "excess_deposit": {"id": "c02", "name_th": "มัดจำสูง (กฎตัวอย่าง > 2 เดือน)", "kind": "rental", "default_level": "red",
        "meaning_th": "แอปตั้งตัวอย่างให้เตือนเมื่อมัดจำรวมเกิน 2 เดือนของค่าเช่า",
        "why_th": "เงินก้อนใหญ่ถูกถือไว้ และเงื่อนไขคืนอาจกำกวม",
        "ask_th": ["มัดจำคืนเมื่อไร หักอะไรได้บ้าง ต้องมีใบเสร็จไหม", "มีเพดานการหักค่าเสื่อมไหม"]},
    "heavy_penalty": {"id": "c03", "name_th": "ค่าปรับ/เบี้ยปรับสูง", "kind": "both", "default_level": "red",
        "meaning_th": "มีค่าปรับเลิกสัญญาก่อนครบ หรือค่าปรับรายวันที่สูงมากเมื่อเทียบกับค่าเช่า/ค่างวด",
        "why_th": "อาจจ่ายเพิ่มจนไม่คุ้มถ้าต้องย้ายหรือผ่อนไม่ทัน",
        "ask_th": ["คำนวณค่าปรับอย่างไร เป็นจำนวนคงที่หรือร้อยละ", "มีเพดานค่าปรับรวมไหม"]},
    "entry_no_notice": {"id": "c04", "name_th": "เข้าห้องโดยไม่บอกล่วงหน้า", "kind": "rental", "default_level": "red",
        "meaning_th": "ผู้ให้เช่าหรือตัวแทนเข้าห้องได้โดยไม่ต้องแจ้งล่วงหน้า",
        "why_th": "กระทบความเป็นส่วนตัวและความปลอดภัย",
        "ask_th": ["จะแจ้งล่วงหน้าอย่างน้อยกี่ชั่วโมง ยกเว้นกรณีฉุกเฉินอะไรบ้าง"]},
    "hidden_fee": {"id": "c05", "name_th": "ค่าใช้จ่ายแฝง / ไม่ระบุชัด", "kind": "both", "default_level": "yellow",
        "meaning_th": "มีค่าส่วนกลาง ค่าธรรมเนียม ค่าประกัน หรือค่าดำเนินการที่ระบุคลุมเครือ",
        "why_th": "ยอดจริงอาจสูงกว่าตัวเลขที่คุยกันตอนแรก",
        "ask_th": ["ขอรายการค่าใช้จ่ายทั้งหมดเป็นตัวเลขบาทต่อเดือน/ต่อปี", "รายการไหนปรับได้โดยไม่ต้องแจ้ง"]},
    "utility_unclear": {"id": "c06", "name_th": "ค่าน้ำค่าไฟไม่ชัด", "kind": "rental", "default_level": "yellow",
        "meaning_th": "อัตราค่าน้ำไฟหรือวิธีแบ่งมิเตอร์ไม่ระบุตัวเลข",
        "why_th": "อาจถูกคิดสูงกว่าอัตราที่คาด",
        "ask_th": ["อัตราต่อหน่วยเท่าไร มิเตอร์แยกหรือรวม ขอดูบิลตัวอย่าง"]},
    "repair_all": {"id": "c07", "name_th": "ผู้เช่าซ่อมทุกอย่าง", "kind": "rental", "default_level": "yellow",
        "meaning_th": "ผู้เช่ารับผิดชอบซ่อมทั้งของที่สึกหรอตามปกติและของที่เสียจากโครงสร้าง",
        "why_th": "ค่าซ่อมใหญ่ควรคุยให้ชัดว่าใครจ่าย",
        "ask_th": ["ของที่สึกหรอตามปกติ (แอร์ เครื่องทำน้ำอุ่น) ใครซ่อม", "มีวงเงินซ่อมที่ผู้เช่าต้องจ่ายเองไหม"]},
    "interest_high": {"id": "c08", "name_th": "ดอกเบี้ยสูง (กฎตัวอย่าง ≥ 1.5%/เดือน)", "kind": "loan", "default_level": "red",
        "meaning_th": "แอปตั้งตัวอย่างให้เตือนเมื่อดอกเบี้ยระบุ ≥ 1.5% ต่อเดือน หรือเทียบเท่า",
        "why_th": "ภาระรวมอาจสูงกว่าที่คิดจากค่างวด",
        "ask_th": ["อัตรานี้คิดแบบลดต้นลดดอกหรือดอกคงที่", "มีดอกปรับล่าช้าเท่าไร และคิดทบต้นไหม"]},
    "early_termination": {"id": "c09", "name_th": "เลิกสัญญาก่อนครบยาก/แพง", "kind": "both", "default_level": "yellow",
        "meaning_th": "ไม่มีช่องเลิกก่อนครบ หรือมีค่าปรับเกือบเท่าสัญญาที่เหลือ",
        "why_th": "ถ้าแผนเปลี่ยน อาจออกไม่ได้โดยไม่เสียเงินก้อน",
        "ask_th": ["เลิกก่อนครบได้ไหม ต้องบอกล่วงหน้ากี่วัน และเสียเท่าไร"]},
    "no_receipt": {"id": "c10", "name_th": "ไม่ระบุว่าต้องออกใบเสร็จ", "kind": "both", "default_level": "yellow",
        "meaning_th": "สัญญาไม่พูดถึงหลักฐานการชำระเงิน",
        "why_th": "ถ้าไม่มีใบเสร็จ การพิสูจน์ว่าจ่ายแล้วจะยาก",
        "ask_th": ["ขอให้เขียนในสัญญาว่าต้องออกใบเสร็จ/สลิปทุกงวด"]},
    "seizure": {"id": "c11", "name_th": "ยึดทรัพย์หรือเข้าถึงบัญชีได้ง่าย", "kind": "loan", "default_level": "red",
        "meaning_th": "มีข้อความให้ยึดทรัพย์หรือหักบัญชีได้ทันทีเมื่อผิดนัด โดยไม่ผ่านขั้นตอนที่อธิบายชัด",
        "why_th": "ความเสี่ยงสูง ควรให้ทนายอ่านก่อน",
        "ask_th": ["ขั้นตอนเมื่อผิดนัดเป็นอย่างไร มีระยะผ่อนผันกี่วัน", "ทรัพย์อะไรอยู่ในหลักประกันบ้าง"]},
    "blank_terms": {"id": "c12", "name_th": "ช่องว่าง / ข้อความที่แก้ได้ภายหลัง", "kind": "both", "default_level": "red",
        "meaning_th": "มีช่องว่าง ตัวเลขไม่กรอก หรืออนุญาตให้อีกฝ่ายแก้เงื่อนไขได้ฝ่ายเดียว",
        "why_th": "เงื่อนไขอาจเปลี่ยนหลังเซ็น",
        "ask_th": ["ขอให้เติมตัวเลขให้ครบและขีดฆ่าช่องว่างก่อนเซ็น", "การแก้ไขต้องมีลายเซ็นทั้งสองฝ่ายใช่ไหม"]},
}

# example deposit months threshold
DEPOSIT_RED_MONTHS = 2
INTEREST_RED_MONTH = 1.5  # percent per month, example only
PENALTY_RED_RATIO = 1.0  # penalty >= 1 month rent or 1 installment → red if also marked

CHECKLIST_RENTAL = [
    ("parties", "ชื่อและที่อยู่ทั้งสองฝ่ายตรงกับบัตรและห้องจริง"),
    ("address", "ที่อยู่ห้อง เลขห้อง และทรัพย์ที่เช่าระบุครบ"),
    ("term", "วันเริ่ม-วันสิ้นสุด และเงื่อนไขต่อสัญญาเขียนชัด"),
    ("rent", "ค่าเช่า วันจ่าย ช่องทางจ่าย ระบุเป็นตัวเลขบาท"),
    ("deposit", "จำนวนมัดจำ เงื่อนไขคืน และรายการที่หักได้"),
    ("fees", "ค่าส่วนกลาง ค่าน้ำไฟ ค่าอื่น ๆ เป็นตัวเลข"),
    ("repair", "ใครซ่อมอะไร วงเงินและความรับผิดชอบ"),
    ("exit", "การบอกเลิก ย้ายออก และสภาพห้องตอนคืน"),
    ("receipt", "มีข้อความว่าต้องออกหลักฐานการชำระเงิน"),
    ("blanks", "ไม่มีช่องว่าง และไม่ยอมให้แก้ฝ่ายเดียวหลังเซ็น"),
]
CHECKLIST_LOAN = [
    ("parties", "ชื่อผู้กู้ ผู้ให้กู้ และผู้ค้ำ (ถ้ามี) ตรงกับบัตร"),
    ("principal", "เงินต้นที่ได้รับจริง (หลังหักค่าธรรมเนียม) ระบุชัด"),
    ("rate", "อัตราดอกเบี้ย วิธีคิด และดอกปรับล่าช้า"),
    ("payment", "ค่างวด วันจ่าย จำนวนงวด และตารางผ่อน"),
    ("fees", "ค่าธรรมเนียม ค่าประกัน และค่าอื่นที่ต้องจ่ายเพิ่ม"),
    ("collateral", "หลักประกันคืออะไร และเงื่อนไขการยึด"),
    ("prepay", "จ่ายก่อนครบได้ไหม มีค่าปรับปิดบัญชีไหม"),
    ("default", "ผิดนัดแล้วเกิดอะไร ระยะผ่อนผันกี่วัน"),
    ("receipt", "มีหลักฐานการชำระทุกงวด"),
    ("blanks", "ไม่มีช่องว่าง และไม่ให้แก้ฝ่ายเดียวหลังเซ็น"),
]

def scan_quality(glare, blur, tilt, text_fill):
    for v in (glare, blur, tilt, text_fill):
        if not 0 <= v <= 1:
            raise ValueError("quality inputs must be 0..1")
    score = round(100 * (1 - (0.30 * glare + 0.35 * blur + 0.20 * tilt + 0.15 * (1 - text_fill))))
    tips = []
    if glare > 0.5:
        tips.append("แสงสะท้อนบนกระดาษ ปิดแฟลชหรือหันออกจากไฟ")
    if blur > 0.4:
        tips.append("ตัวอักษรเบลอ ถ่ายให้ตรงและแตะโฟกัสที่ข้อความ")
    if tilt > 0.4:
        tips.append("ถ่ายเอียงเกินไป วางเอกสารราบแล้วถ่ายจากด้านบน")
    if text_fill < 0.5:
        tips.append("เอกสารไม่เต็มกรอบ ถ่ายให้เห็นทั้งหน้า รวมหัวสัญญา")
    ok = score >= 60 and text_fill >= 0.5
    if not ok and not tips:
        tips.append("ถ่ายใหม่ให้ตัวอักษรชัด ทั้งหน้า แสงนุ่ม")
    return {"score": score, "ok": ok, "tips_th": tips}

def clause_info(key):
    if key not in CLAUSES:
        raise ValueError("unknown clause " + key)
    c = dict(CLAUSES[key])
    c["key"] = key
    return c

def identify_clauses(photo, min_conf=MIN_CONF):
    found, uncertain = [], []
    for d in photo["detections"]:
        k = d["clause"]
        if k not in CLAUSES:
            raise ValueError("unknown clause " + k)
        if d["confidence"] < min_conf:
            uncertain.append(k)
            continue
        found.append({"clause": k, "name_th": CLAUSES[k]["name_th"], "confidence": d["confidence"],
                      "excerpt_th": d.get("excerpt_th", "")})
    return {"clauses": found, "uncertain": uncertain}

def contract_scan(photo):
    if photo["kind"] not in KINDS:
        raise ValueError("kind must be rental or loan")
    q = scan_quality(photo["glare"], photo["blur"], photo["tilt"], photo["text_fill"])
    ident = identify_clauses(photo)
    return {
        "photo_id": photo["id"], "kind": photo["kind"], "kind_th": KIND_TH[photo["kind"]],
        "quality": q, "clauses": ident["clauses"], "uncertain": ident["uncertain"],
        "clause_count": len(ident["clauses"]), "ok": q["ok"],
        "disclaimer_th": SAFETY_DISCLAIMER_TH,
    }

def pipeline_steps(photo):
    s = ["page_detect"]
    if photo["glare"] > 0.5:
        s.append("deglare")
    if photo["tilt"] > 0.4:
        s.append("deskew")
    s += ["ocr_block", "clause_tag", "risk_highlight", "fee_calc", "checklist"]
    return s

def _escalate_with_numbers(key, terms):
    """Apply example numeric guardrails on top of a detected clause."""
    level = CLAUSES[key]["default_level"]
    if key == "excess_deposit":
        dep = terms.get("deposit_months")
        if dep is not None and dep > DEPOSIT_RED_MONTHS:
            level = "red"
        elif dep is not None and dep == DEPOSIT_RED_MONTHS:
            level = "yellow"
    if key == "interest_high":
        rate = terms.get("interest_pct_month")
        if rate is not None and rate >= INTEREST_RED_MONTH:
            level = "red"
        elif rate is not None and rate >= 1.0:
            level = "yellow"
    if key == "heavy_penalty":
        ratio = terms.get("penalty_months")
        if ratio is not None and ratio >= PENALTY_RED_RATIO:
            level = "red"
    return level

def risk_highlights(kind, detections, terms):
    if kind not in KINDS:
        raise ValueError("bad kind")
    items = []
    seen = set()
    for d in detections:
        if d.get("confidence", 1) < MIN_CONF:
            continue
        k = d["clause"]
        if k in seen:
            continue
        if CLAUSES[k]["kind"] not in ("both", kind):
            continue
        seen.add(k)
        level = _escalate_with_numbers(k, terms)
        items.append({
            "clause": k, "name_th": CLAUSES[k]["name_th"], "level": level,
            "meaning_th": CLAUSES[k]["meaning_th"], "why_th": CLAUSES[k]["why_th"],
            "ask_th": list(CLAUSES[k]["ask_th"]),
        })
    # numeric-only flags even if OCR missed the clause label
    if kind == "rental" and terms.get("deposit_months", 0) > DEPOSIT_RED_MONTHS and "excess_deposit" not in seen:
        items.append({
            "clause": "excess_deposit", "name_th": CLAUSES["excess_deposit"]["name_th"], "level": "red",
            "meaning_th": CLAUSES["excess_deposit"]["meaning_th"], "why_th": CLAUSES["excess_deposit"]["why_th"],
            "ask_th": list(CLAUSES["excess_deposit"]["ask_th"]),
        })
    if kind == "loan" and terms.get("interest_pct_month", 0) >= INTEREST_RED_MONTH and "interest_high" not in seen:
        items.append({
            "clause": "interest_high", "name_th": CLAUSES["interest_high"]["name_th"], "level": "red",
            "meaning_th": CLAUSES["interest_high"]["meaning_th"], "why_th": CLAUSES["interest_high"]["why_th"],
            "ask_th": list(CLAUSES["interest_high"]["ask_th"]),
        })
    items.sort(key=lambda x: (-LEVEL_RANK[x["level"]], x["clause"]))
    if not items:
        top, score = "green", 8
    else:
        top = max(items, key=lambda x: LEVEL_RANK[x["level"]])["level"]
        score = {"green": 8, "yellow": 45, "red": 78}[top]
        score = min(100, score + 8 * (sum(1 for i in items if i["level"] == top) - 1))
    reds = [i["name_th"] for i in items if i["level"] == "red"]
    if top == "red":
        headline_th = "พบจุดแดง " + str(len(reds)) + " ข้อ ควรชะลอการเซ็นแล้วถามให้ชัด"
    elif top == "yellow":
        headline_th = "พบจุดที่ควรถามเพิ่ม ยังไม่ควรเซ็นเร็ว"
    else:
        headline_th = "ไม่พบธงตามกฎตัวอย่างของแอป ยังควรอ่านทั้งฉบับและปรึกษาผู้รู้ก่อนเซ็น"
    return {
        "kind": kind, "level": top, "score": score, "count": len(items), "items": items,
        "red_count": sum(1 for i in items if i["level"] == "red"),
        "yellow_count": sum(1 for i in items if i["level"] == "yellow"),
        "headline_th": headline_th, "disclaimer_th": SAFETY_DISCLAIMER_TH,
    }

def plain_summary(kind, terms, highlights):
    if kind == "rental":
        bits = [
            f"ค่าเช่า ฿{terms['rent_thb']:,} ต่อเดือน",
            f"มัดจำ {terms.get('deposit_months', 0)} เดือน (฿{terms['rent_thb'] * terms.get('deposit_months', 0):,})",
            f"ระยะสัญญา {terms.get('term_months', 0)} เดือน",
        ]
        if terms.get("advance_months"):
            bits.append(f"จ่ายล่วงหน้า {terms['advance_months']} เดือน")
    else:
        bits = [
            f"เงินต้น ฿{terms['principal_thb']:,}",
            f"ดอกเบี้ยตัวอย่าง {terms.get('interest_pct_month', 0)}% ต่อเดือน",
            f"ระยะ {terms.get('term_months', 0)} เดือน",
        ]
    if highlights["red_count"]:
        bits.append("มีจุดแดงที่ควรชะลอการเซ็น " + str(highlights["red_count"]) + " ข้อ")
    return {
        "kind": kind, "kind_th": KIND_TH[kind], "level": highlights["level"],
        "bullets_th": bits, "headline_th": highlights["headline_th"],
        "plain_th": "สรุปแบบภาษาคน: " + " · ".join(bits),
        "disclaimer_th": SAFETY_DISCLAIMER_TH,
    }

def _round50(x):
    return int(round(x / 50.0) * 50)

def fee_calc(kind, terms):
    if kind == "rental":
        rent = terms["rent_thb"]
        dep = terms.get("deposit_months", 0) * rent
        adv = terms.get("advance_months", 0) * rent
        extras = terms.get("extras_thb", 0)
        late = terms.get("late_fee_per_day_thb", 0)
        move_in = rent + dep + adv + extras  # first payment if first month included as rent or advance
        # If advance_months includes first month, callers set it that way.
        return {
            "kind": kind, "rent_thb": rent, "deposit_thb": dep, "advance_thb": adv,
            "extras_thb": extras, "move_in_thb": move_in,
            "late_fee_per_day_thb": late, "late_30d_thb": late * 30,
            "breakdown_th": [
                f"ค่าเช่าเดือนแรก ฿{rent:,}",
                f"มัดจำ ฿{dep:,}",
                f"จ่ายล่วงหน้า ฿{adv:,}",
                f"ค่าอื่นที่ระบุ ฿{extras:,}",
            ],
            "disclaimer_th": FEE_DISCLAIMER_TH + " " + SAFETY_DISCLAIMER_TH,
        }
    principal = terms["principal_thb"]
    rate = terms.get("interest_pct_month", 0) / 100.0
    months = terms.get("term_months", 1)
    # example flat-interest illustration (not a real amortization): total interest = principal * rate * months
    interest = int(round(principal * rate * months))
    total = principal + interest
    installment = int(round(total / months)) if months else total
    return {
        "kind": kind, "principal_thb": principal, "interest_total_thb": interest,
        "total_payable_thb": total, "installment_thb": installment, "term_months": months,
        "method_th": "ตัวอย่างคิดดอกแบบคงที่ตลอดสัญญา (ไม่ใช่ตารางลดต้นลดดอกจริง)",
        "disclaimer_th": FEE_DISCLAIMER_TH + " " + SAFETY_DISCLAIMER_TH,
    }

def questions_to_ask(highlights):
    qs, seen = [], set()
    for it in highlights["items"]:
        for q in it["ask_th"]:
            if q not in seen:
                seen.add(q)
                qs.append(q)
    qs.append("ขอยกสัญญาไปอ่านและปรึกษาผู้รู้อย่างน้อย 1 คืนได้ไหม")
    return {"questions_th": qs, "count": len(qs), "disclaimer_th": SAFETY_DISCLAIMER_TH}

def sign_checklist(kind, checked):
    source = CHECKLIST_RENTAL if kind == "rental" else CHECKLIST_LOAN
    items = []
    for key, text in source:
        items.append({"key": key, "text_th": text, "done": key in checked})
    missing = [i["key"] for i in items if not i["done"]]
    ready = len(missing) == 0
    return {
        "kind": kind, "items": items, "done_count": len(items) - len(missing),
        "total": len(items), "missing": missing, "ready_to_sign": ready,
        "message_th": "ครบตามเช็กลิสต์ตัวอย่างแล้ว แต่ยังไม่ใช่คำแนะนำให้เซ็น" if ready else "ยังไม่ครบเช็กลิสต์ตัวอย่าง อย่ารีบเซ็น",
        "disclaimer_th": SAFETY_DISCLAIMER_TH,
    }

def family_card(person, scan, highlights, fees, note_th=""):
    if scan["kind"] == "rental":
        money = f"ย้ายเข้าประมาณ ฿{fees['move_in_thb']:,}"
    else:
        money = f"ยอดที่ต้องจ่ายรวมตัวอย่าง ฿{fees['total_payable_thb']:,}"
    text = (
        f"ContractLens — สรุปก่อนเซ็น (ไม่ใช่คำกฎหมาย)\n"
        f"{person['name_th']} · {scan['kind_th']}\n"
        f"{highlights['headline_th']}\n"
        f"{money}\n"
        f"{note_th}".strip()
    )
    return {
        "title_th": "การ์ดส่งครอบครัว",
        "name_th": person["name_th"],
        "kind": scan["kind"],
        "kind_th": scan["kind_th"],
        "level": highlights["level"],
        "score": highlights["score"],
        "headline_th": highlights["headline_th"],
        "money_th": money,
        "note_th": note_th,
        "line_share_url": "https://line.me/R/share?text=" + _up.quote(text),
        "disclaimer_th": SAFETY_DISCLAIMER_TH,
    }

def share_card(name_th, highlights):
    return {
        "title_th": f"ContractLens — {name_th}",
        "headline_th": highlights["headline_th"],
        "hook_th": "ถ่ายสัญญา เจอจุดอันตรายก่อนเซ็น",
        "level": highlights["level"], "score": highlights["score"],
        "layout": "risk_result",
        "sizes": ["1080x1350", "1080x1920", "1080x1080"],
        "watermark": WATERMARK, "cta_th": "คอมเมนต์ CLAUSE รับแพ็กฟรี",
    }

def quota(used_today, want, pro=False):
    if pro:
        return {"allowed": want, "left_after": None, "paywall": False}
    left = max(0, FREE_SCANS_PER_DAY - used_today)
    allowed = min(want, left)
    return {"allowed": allowed, "left_after": left - allowed, "paywall": allowed < want}

def safety_guard(level):
    if level == "red":
        return {"level": "stop", "message_th": "พบจุดแดง ควรชะลอการเซ็น " + SAFETY_DISCLAIMER_TH}
    if level == "yellow":
        return {"level": "warn", "message_th": "ยังมีข้อที่ควรถามให้ชัด " + SAFETY_DISCLAIMER_TH}
    return {"level": "ok", "message_th": SAFETY_DISCLAIMER_TH}

def diary_entry(eid, person_id, date, kind, title_th, level, on_device=True):
    if kind not in KINDS:
        raise ValueError("bad kind")
    return {"id": eid, "person_id": person_id, "date": date, "kind": kind,
            "title_th": title_th, "level": level, "on_device": on_device}

def diary_stats(entries):
    if not entries:
        return {"count": 0, "red": 0, "last_date": None, "top_kind": None}
    red = sum(1 for e in entries if e["level"] == "red")
    last = max(entries, key=lambda e: e["date"])["date"]
    from collections import Counter
    top = Counter(e["kind"] for e in entries).most_common(1)[0][0]
    return {"count": len(entries), "red": red, "last_date": last, "top_kind": top}
