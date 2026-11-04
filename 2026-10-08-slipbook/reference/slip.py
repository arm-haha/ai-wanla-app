"""SlipBook reference engine (pure, deterministic). Mirror in lib/parse.ts, lib/categorize.ts, lib/money.ts."""
import re, calendar

def jsround(x):
    import math
    return math.floor(x + 0.5)

TH_MONTHS = {"ม.ค.":1,"ก.พ.":2,"มี.ค.":3,"เม.ย.":4,"พ.ค.":5,"มิ.ย.":6,"ก.ค.":7,"ส.ค.":8,"ก.ย.":9,"ต.ค.":10,"พ.ย.":11,"ธ.ค.":12}
EN_MONTHS = {m:i for i,m in enumerate(["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],1)}

def _year(y):
    y = int(y)
    if y < 100:            # "69" = พ.ศ. 2569 ; "26" = ค.ศ. 2026
        y = y + 2500 if y >= 50 else y + 2000
    if y > 2400: y -= 543   # พ.ศ. -> ค.ศ.
    return y

RE_AMOUNT = [
    re.compile(r"(?:จำนวนเงิน|จำนวน|ยอดเงิน|Amount)\s*[:：]?\s*(?:฿|THB)?\s*([\d,]+\.\d{2})"),
    re.compile(r"฿\s*([\d,]+\.\d{2})"),
    re.compile(r"([\d,]+\.\d{2})\s*(?:บาท|THB)"),
]
RE_DATE_TH = re.compile(r"(\d{1,2})\s*(ม\.ค\.|ก\.พ\.|มี\.ค\.|เม\.ย\.|พ\.ค\.|มิ\.ย\.|ก\.ค\.|ส\.ค\.|ก\.ย\.|ต\.ค\.|พ\.ย\.|ธ\.ค\.)\s*(\d{2,4})")
RE_DATE_SLASH = re.compile(r"(\d{1,2})/(\d{1,2})/(\d{2,4})")
RE_DATE_EN = re.compile(r"(\d{1,2})\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d{2,4})")
RE_TIME = re.compile(r"(\d{1,2}):(\d{2})(?::\d{2})?\s*(?:น\.)?")
RE_REF = re.compile(r"(?:รหัสอ้างอิง|เลขที่รายการ|หมายเลขอ้างอิง|Ref(?:erence)?\s*No\.?|Transaction ID)\s*[:：]?\s*([A-Za-z0-9]{8,30})")
RE_TO = re.compile(r"^(?:ไปยัง|ถึง|ผู้รับ|To)\s*[:：]?\s*(.+)$", re.M)
RE_FROM = re.compile(r"^(?:จาก|ผู้โอน|From)\s*[:：]?\s*(.+)$", re.M)
RE_ACCT = re.compile(r"[xX\*]{2,}[-\d xX\*]*\d{3,4}[-\d xX\*]*")
INCOMING = ["รับเงิน", "เงินเข้า", "ได้รับเงิน", "Received"]
BANK_HINTS = {"KBANK":["K PLUS","กสิกร"],"SCB":["SCB","ไทยพาณิชย์"],"KTB":["Krungthai","กรุงไทย"],
              "BBL":["Bangkok Bank","กรุงเทพ"],"BAY":["krungsri","กรุงศรี"],"TTB":["ttb","ทีทีบี"],
              "GSB":["MyMo","ออมสิน"],"TRUEMONEY":["TrueMoney","ทรูมันนี่"]}

def _line_after(label_re, text):
    m = label_re.search(text)
    if not m: return None
    v = m.group(1).strip()
    return v or None

def parse_slip(text, owner_names=()):
    """OCR text -> ParsedSlip dict. Never guesses: missing field => None + lower confidence.
    owner_names: the user's own names (Settings). If the "to" line contains one, the slip is incoming."""
    out = {"amount": None, "date": None, "time": None, "ref": None, "counterparty": None,
           "counterparty_account_masked": None, "direction": "out", "bank": None, "confidence": 0.0, "missing": []}
    for r in RE_AMOUNT:
        m = r.search(text)
        if m:
            out["amount"] = float(m.group(1).replace(",", "")); break
    m = RE_DATE_TH.search(text)
    if m: d, mo, y = int(m.group(1)), TH_MONTHS[m.group(2)], _year(m.group(3))
    else:
        m = RE_DATE_EN.search(text)
        if m: d, mo, y = int(m.group(1)), EN_MONTHS[m.group(2)], _year(m.group(3))
        else:
            m = RE_DATE_SLASH.search(text)
            if m: d, mo, y = int(m.group(1)), int(m.group(2)), _year(m.group(3))
    if m: out["date"] = f"{y:04d}-{mo:02d}-{d:02d}"
    m = RE_TIME.search(text)
    if m: out["time"] = f"{int(m.group(1)):02d}:{m.group(2)}"
    out["ref"] = _line_after(RE_REF, text)
    to_line = _line_after(RE_TO, text) or ""
    incoming = any(k in text for k in INCOMING) or any(n and n in to_line for n in owner_names)
    out["direction"] = "in" if incoming else "out"
    cp = _line_after(RE_FROM, text) if incoming else (to_line or None)
    if cp:
        acct = RE_ACCT.search(cp)
        if acct:
            out["counterparty_account_masked"] = acct.group(0).strip()
            cp = cp[:acct.start()].strip(" -·|")
        out["counterparty"] = cp
    for code, hints in BANK_HINTS.items():
        if any(h.lower() in text.lower() for h in hints): out["bank"] = code; break
    weights = {"amount": .35, "date": .2, "time": .1, "ref": .2, "counterparty": .15}
    conf = 0
    for k, w in weights.items():
        if out[k] is None: out["missing"].append(k)
        else: conf += w
    out["confidence"] = round(conf, 2)
    return out

# ---------- categorize ----------
CATEGORIES = [
 ("food","ของกิน","🍜","#F97316"),("cafe","คาเฟ่/เครื่องดื่ม","☕","#A16207"),("transport","เดินทาง","🚕","#0EA5E9"),
 ("shopping","ช้อปปิ้ง","🛍️","#EC4899"),("bills","บิล/ค่าน้ำไฟเน็ต","🧾","#64748B"),("subscription","สมาชิกรายเดือน","🔁","#8B5CF6"),
 ("family","ครอบครัว","🏠","#10B981"),("friends","โอนเพื่อน/หารบิล","🫂","#F59E0B"),("health","สุขภาพ","💊","#EF4444"),
 ("fun","บันเทิง","🎬","#6366F1"),("other","อื่นๆ","📦","#94A3B8")]
CAT = {c[0]: {"key":c[0],"label_th":c[1],"emoji":c[2],"color":c[3]} for c in CATEGORIES}

# ordered keyword rules (case-insensitive contains). first match wins.
RULES = [
 ("7-eleven","food"),("เซเว่น","food"),("lotus","food"),("ข้าว","food"),("ก๋วยเตี๋ยว","food"),("ส้มตำ","food"),
 ("หมูกระทะ","food"),("line man","food"),("grab food","food"),("foodpanda","food"),("ร้านอาหาร","food"),
 ("café","cafe"),("cafe","cafe"),("coffee","cafe"),("กาแฟ","cafe"),("ชานม","cafe"),
 ("grab","transport"),("bolt","transport"),("แรบบิท","transport"),("bts","transport"),("mrt","transport"),("ปตท","transport"),("เติมน้ำมัน","transport"),
 ("shopee","shopping"),("lazada","shopping"),("tiktok shop","shopping"),
 ("การไฟฟ้า","bills"),("การประปา","bills"),("ค่าเน็ต","bills"),("มือถือรายเดือน","bills"),("internet","bills"),
 ("moviemax","subscription"),("netflix","subscription"),("spotify","subscription"),("youtube","subscription"),("icloud","subscription"),
 ("โรงพยาบาล","health"),("คลินิก","health"),("ร้านยา","health"),("ฟิตเนส","health"),
 ("โรงหนัง","fun"),("คอนเสิร์ต","fun"),("ตั๋ว","fun"),
]
PERSON_PREFIX = re.compile(r"^(นาย|นาง|น\.ส\.|นางสาว|ด\.ช\.|ด\.ญ\.|คุณ|MR\.?|MRS\.?|MS\.?)\s*", re.I)

def norm_key(name):
    return re.sub(r"\s+", " ", (name or "").strip().lower())

def categorize(counterparty, direction="out", memory=None):
    """returns (category, source, confidence). memory: {norm_key: category} learned from user edits."""
    memory = memory or {}
    if direction == "in": return ("income", "direction", 1.0)
    k = norm_key(counterparty)
    if k in memory: return (memory[k], "memory", 1.0)
    for kw, cat in RULES:
        if kw in k: return (cat, "rule", 0.9)
    if PERSON_PREFIX.match(counterparty or ""): return ("friends", "person_default", 0.5)
    return ("other", "fallback", 0.3)

# ---------- import / dedupe ----------
def dedupe_key(p):
    if p["ref"]: return "ref:" + p["ref"]
    return f"fp:{p['date']}|{p['time']}|{p['amount']:.2f}|{norm_key(p['counterparty'])}"

# ---------- money math ----------
def month_days(ym):
    y, m = map(int, ym.split("-")); return calendar.monthrange(y, m)[1]

def dashboard(txns, ym):
    out_t = [t for t in txns if t["date"].startswith(ym) and t["direction"] == "out"]
    in_t = [t for t in txns if t["date"].startswith(ym) and t["direction"] == "in"]
    spent = round(sum(t["amount"] for t in out_t), 2)
    by = {}
    for t in out_t: by[t["category"]] = round(by.get(t["category"], 0) + t["amount"], 2)
    cats = sorted(by.items(), key=lambda kv: (-kv[1], kv[0]))
    by_cat = [{"category":k,"label_th":CAT[k]["label_th"],"emoji":CAT[k]["emoji"],"color":CAT[k]["color"],"amount":v,
               "percent": round(v/spent*100, 1),"count": sum(1 for t in out_t if t["category"]==k)} for k,v in cats]
    daily = {}
    for t in out_t: daily[t["date"]] = round(daily.get(t["date"], 0) + t["amount"], 2)
    peers = {}
    for t in out_t:
        k = t["counterparty"]; peers.setdefault(k, [0, 0.0]); peers[k][0] += 1; peers[k][1] = round(peers[k][1] + t["amount"], 2)
    top = sorted(peers.items(), key=lambda kv: (-kv[1][1], kv[0]))[:5]
    return {"month": ym, "spent_total": spent, "income_total": round(sum(t["amount"] for t in in_t), 2),
            "txn_count": len(out_t), "by_category": by_cat,
            "daily": [{"date": d, "amount": a} for d, a in sorted(daily.items())],
            "top_counterparties": [{"name": k, "count": v[0], "amount": v[1]} for k, v in top]}

def heat_level(amount, max_amount):
    if amount <= 0: return 0
    r = amount / max_amount
    return 1 if r <= .25 else 2 if r <= .5 else 3 if r <= .75 else 4

def budget_status(dash, budgets, today):
    ym = dash["month"]; nd = month_days(ym); day = int(today[-2:]); remaining_days = nd - day + 1
    spent_by = {c["category"]: c["amount"] for c in dash["by_category"]}
    jars = []
    for k, b in budgets.items():
        s = spent_by.get(k, 0.0); pct = jsround(s / b * 100) if b else 0
        state = "over" if s > b else "warn" if pct >= 80 else "ok"
        jars.append({"category": k, "label_th": CAT[k]["label_th"], "emoji": CAT[k]["emoji"], "budget": b, "spent": s,
                     "left": round(b - s, 2), "percent": pct, "state": state})
    tb = sum(budgets.values()); ts = round(sum(spent_by.get(k, 0) for k in budgets) + sum(v for k, v in spent_by.items() if k not in budgets), 2)
    left = round(tb - ts, 2)
    per_day = jsround(left / remaining_days) if left > 0 else 0
    return {"month": ym, "today": today, "days_in_month": nd, "remaining_days_incl_today": remaining_days,
            "budget_total": tb, "spent_total": ts, "left_total": left, "safe_per_day": per_day,
            "expected_percent_by_today": jsround(day / nd * 100), "jars": jars}

RECURRING_ELIGIBLE = {"subscription", "bills", "health", "fun", "other"}

def subscriptions(txns):
    """same normalized counterparty, out, category in RECURRING_ELIGIBLE, exactly once per month in >=2 distinct months,
    every amount within ±5% of the first. (everyday spots like coffee/food/transport/family are excluded on purpose)"""
    groups = {}
    for t in sorted(txns, key=lambda t: (t["date"], t["time"])):
        if t["direction"] != "out" or t["category"] not in RECURRING_ELIGIBLE: continue
        groups.setdefault(norm_key(t["counterparty"]), []).append(t)
    out = []
    for k, ts in groups.items():
        months = sorted({t["date"][:7] for t in ts})
        if len(months) < 2: continue
        base = ts[0]["amount"]
        if not all(abs(t["amount"] - base) <= base * 0.05 for t in ts): continue
        if len(ts) != len(months): continue   # exactly once per month
        dom = [int(t["date"][-2:]) for t in ts]
        out.append({"counterparty": ts[0]["counterparty"], "amount": base, "months": months,
                    "day_of_month": jsround(sum(dom)/len(dom)), "yearly_cost": round(base * 12, 2),
                    "category": ts[-1]["category"]})
    return sorted(out, key=lambda s: -s["amount"])
