"""ScamScan (มิจฉาสแกน) — deterministic core. AI is optional garnish; every score here is rule-based and reproducible.
Disclaimer baked in: the score is a risk signal, never a guarantee. Always verify via the official number you look up yourself."""
import re, random
from urllib.parse import urlsplit

VERSION = "scamscan-rules-1"

# ---- Red-flag rules (id, weight, label_th, explain_th, patterns) ----
RULES = [
    ("urgency", 15, "เร่งให้รีบ", "มิจฉาชอบขู่ให้รีบ จะได้ไม่มีเวลาคิดหรือถามใคร",
     [r"ด่วน", r"ภายใน\s?\d+\s?(ชม|ชั่วโมง|นาที)", r"ภายในวันนี้", r"ทันที", r"ถูกระงับ", r"ระงับ", r"หมดอายุ", r"ล่าสุดวันนี้", r"หมดไว"]),
    ("credential", 20, "ขอรหัส/OTP/ข้อมูลส่วนตัว", "ธนาคารและหน่วยงานจริงจะไม่ขอ OTP รหัส หรือเลขบัตรผ่านลิงก์/แชต",
     [r"OTP", r"รหัสผ่าน", r"รหัส\s?PIN", r"PIN", r"เลขบัตรประชาชน", r"ยืนยันตัวตน", r"กรอกข้อมูล"]),
    ("money", 15, "ขอให้โอน/จ่ายเงิน", "ขอค่าธรรมเนียม มัดจำ หรือให้โอนก่อน = สัญญาณอันตราย",
     [r"โอน(เงิน)?", r"ค่าธรรมเนียม", r"ชำระ", r"มัดจำ", r"ค่าส่ง(เพิ่ม)?", r"ค่าปรับ"]),
    ("too_good", 15, "ดีเกินจริง", "ได้รางวัล เงินคืน รายได้ง่าย ๆ ที่ไม่เคยสมัคร มักเป็นเหยื่อล่อ",
     [r"ได้รับรางวัล", r"ถูกรางวัล", r"เงินคืน", r"คืนภาษี", r"รายได้วันละ", r"กำไร\s?\d+", r"ฟรี!", r"ลด\S*\s?[7-9]\d\s?%"]),
    ("authority", 15, "อ้างเป็นเจ้าหน้าที่", "อ้างตำรวจ ศาล DSI ปปง. หรือหมายจับ เพื่อให้กลัว",
     [r"ตำรวจ", r"DSI", r"ดีเอสไอ", r"ปปง", r"หมายจับ", r"ศาล", r"คดี(ฟอกเงิน)?"]),
    ("off_platform", 20, "ให้แอดไลน์/ลงแอปนอกสโตร์", "ให้แอดไลน์แปลก ๆ หรือโหลดแอป/ไฟล์ .apk อาจโดนดูดเงินจากมือถือ",
     [r"แอดไลน์", r"add\s?line", r"ติดตั้งแอป", r"ดาวน์โหลดแอป", r"\.apk\b", r"@\w+\s?\(ไลน์\)"]),
    ("link", 10, "มีลิงก์ให้กด", "ลิงก์ในข้อความที่ไม่ได้ขอ = ตรวจด้วย Link X-Ray ก่อนกดเสมอ", []),
    ("brand_mismatch", 25, "อ้างแบรนด์ แต่ลิงก์ไม่ใช่เว็บทางการ", "ชื่อในข้อความกับโดเมนจริงไม่ตรงกัน = ลิงก์ปลอมเลียนแบบ", []),
    ("shortener", 10, "ลิงก์ย่อซ่อนปลายทาง", "ลิงก์ย่อทำให้มองไม่เห็นว่าพาไปเว็บไหน", []),
    ("bad_tld", 10, "นามสกุลเว็บแปลก", "หน่วยงานไทยใช้ .co.th .go.th .or.th หรือ .com ของตัวเอง ไม่ใช่ .top .xyz .icu", []),
    ("no_https", 5, "ลิงก์ไม่เข้ารหัส (http)", "เว็บที่ให้กรอกข้อมูลต้องเป็น https อย่างน้อย", []),
    ("punycode", 15, "โดเมนตัวอักษรหลอกตา", "xn-- คือโดเมนที่ใช้ตัวอักษรหน้าตาเหมือน แต่ไม่ใช่ตัวจริง", []),
    ("ip_link", 15, "ลิงก์เป็นเลข IP", "เว็บจริงไม่ส่งลิงก์เป็นตัวเลข IP", []),
]
RULE = {r[0]: r for r in RULES}

BRANDS = {  # verify this allowlist against each organization's own site before launch
    "kbank":    {"name_th": "ธนาคารกสิกรไทย", "text": ["กสิกร", "kbank", "K PLUS"], "host": ["kbank", "kasikorn", "kasikornbank"], "official": ["kasikornbank.com"]},
    "scb":      {"name_th": "ธนาคารไทยพาณิชย์", "text": ["ไทยพาณิชย์", "SCB"], "host": ["scb", "scbeasy"], "official": ["scb.co.th"]},
    "ktb":      {"name_th": "ธนาคารกรุงไทย", "text": ["กรุงไทย", "Krungthai"], "host": ["krungthai", "ktb"], "official": ["krungthai.com"]},
    "krungsri": {"name_th": "ธนาคารกรุงศรีอยุธยา", "text": ["กรุงศรี", "Krungsri"], "host": ["krungsri"], "official": ["krungsri.com"]},
    "bbl":      {"name_th": "ธนาคารกรุงเทพ", "text": ["ธนาคารกรุงเทพ", "Bangkok Bank", "บัวหลวง"], "host": ["bangkokbank", "bualuang"], "official": ["bangkokbank.com"]},
    "thaipost": {"name_th": "ไปรษณีย์ไทย", "text": ["ไปรษณีย์", "Thailand Post"], "host": ["thaipost", "thailandpost"], "official": ["thailandpost.co.th"]},
    "revenue":  {"name_th": "กรมสรรพากร", "text": ["สรรพากร", "คืนภาษี"], "host": ["rd", "revenue"], "official": ["rd.go.th"]},
    "pea":      {"name_th": "การไฟฟ้าส่วนภูมิภาค", "text": ["การไฟฟ้า", "PEA", "ค่าไฟ"], "host": ["pea"], "official": ["pea.co.th"]},
}
SHORTENERS = {"bit.ly", "tinyurl.com", "cutt.ly", "t.ly", "s.id", "shorturl.at", "rb.gy", "is.gd"}
BAD_TLDS = {"top", "xyz", "icu", "click", "cc", "live", "shop", "buzz", "sbs", "cfd"}
TH_SLD = {"co", "or", "go", "in", "ac", "net", "mi"}
URL_RE = re.compile(r"(?:(?:https?://)|(?:www\.))[^\s<>\"'ก-๙]+|\b[a-z0-9-]+(?:\.[a-z0-9-]+)*\.(?:com|net|org|th|top|xyz|icu|click|cc|live|shop|ly|id|gd|at|me|buzz|sbs|cfd)(?:/[^\s<>\"'ก-๙]*)?", re.I)

LEVELS = [  # (min_score, level, label_th, color, emoji)
    (75, "scam", "เข้าข่ายมิจฉาสูงมาก", "#DC2626", "🚨"),
    (50, "risky", "เสี่ยงสูง อย่าเพิ่งกด", "#F97316", "⚠️"),
    (25, "caution", "น่าสงสัย ตรวจก่อน", "#FACC15", "🤔"),
    (0,  "low", "ยังไม่เจอสัญญาณอันตราย", "#16A34A", "✅"),
]

def level_of(score):
    for mn, lv, lab, col, emo in LEVELS:
        if score >= mn:
            return {"level": lv, "label_th": lab, "color": col, "emoji": emo}

def registered_domain(host):
    parts = host.lower().strip(".").split(".")
    if len(parts) >= 3 and parts[-1] == "th" and parts[-2] in TH_SLD:
        return ".".join(parts[-3:])
    return ".".join(parts[-2:]) if len(parts) >= 2 else host

def extract_links(text):
    out = []
    for m in URL_RE.finditer(text):
        raw = m.group(0).rstrip(".,)!")
        out.append({"raw": raw, "start": m.start(), "end": m.start() + len(raw)})
    return out

def claimed_brands(text):
    t = text.lower()
    return sorted(b for b, v in BRANDS.items() if any(k.lower() in t for k in v["text"]))

def link_xray(raw, text_brands=()):
    u = raw if re.match(r"https?://", raw, re.I) else "http://" + raw
    has_scheme = bool(re.match(r"https?://", raw, re.I))
    sp = urlsplit(u)
    host = (sp.hostname or "").lower()
    is_ip = bool(re.fullmatch(r"\d{1,3}(\.\d{1,3}){3}", host))
    reg = host if is_ip else registered_domain(host)
    tld = "" if is_ip else host.rsplit(".", 1)[-1]
    tokens = [t for t in re.split(r"[.\-]", host) if t]
    host_brands = sorted(b for b, v in BRANDS.items() if any(tok in v["host"] for tok in tokens))
    official_of = sorted(b for b, v in BRANDS.items() if reg in v["official"])
    brands = sorted(set(host_brands) | set(text_brands))
    flags = []
    if reg in SHORTENERS: flags.append("shortener")
    if tld in BAD_TLDS: flags.append("bad_tld")
    if has_scheme and sp.scheme.lower() == "http": flags.append("no_https")
    if "xn--" in host: flags.append("punycode")
    if is_ip: flags.append("ip_link")
    mismatch = [b for b in brands if b not in official_of]
    if mismatch and reg not in SHORTENERS: flags.append("brand_mismatch")
    if official_of and not mismatch and not flags:
        verdict, verdict_th = "official", f"ตรงกับเว็บทางการของ {BRANDS[official_of[0]]['name_th']} (ยังควรพิมพ์เข้าเว็บเองดีกว่ากดลิงก์)"
    elif "brand_mismatch" in flags:
        verdict, verdict_th = "fake_lookalike", f"ปลอมตัวเป็น {BRANDS[mismatch[0]]['name_th']} — เว็บจริงคือ {BRANDS[mismatch[0]]['official'][0]}"
    elif "shortener" in flags:
        verdict, verdict_th = "hidden", "ลิงก์ย่อ มองไม่เห็นปลายทาง อย่ากด"
    elif flags:
        verdict, verdict_th = "suspicious", "มีจุดน่าสงสัย อย่ากรอกข้อมูล"
    else:
        verdict, verdict_th = "unknown", "ไม่รู้จักเว็บนี้ ถ้าไม่ได้ขอเอง อย่ากด"
    return {"raw": raw, "scheme": sp.scheme.lower() if has_scheme else "none", "host": host, "registered_domain": reg, "tld": tld,
            "host_tokens": tokens, "claimed_brands": brands, "official_match": official_of, "flags": flags,
            "verdict": verdict, "verdict_th": verdict_th,
            "real_site": BRANDS[mismatch[0]]["official"][0] if "brand_mismatch" in flags else None}

def scan(text, sender="", channel="sms"):
    """Return ScanResult: score 0-100, level, fired rules with highlights, links x-ray, actions."""
    fired, highlights = {}, []
    for rid, w, lab, exp, pats in RULES:
        for p in pats:
            for m in re.finditer(p, text, re.I):
                highlights.append({"start": m.start(), "end": m.end(), "text": m.group(0), "rule_id": rid})
                fired.setdefault(rid, 0); fired[rid] += 1
    links = extract_links(text)
    tb = claimed_brands(text + " " + sender)
    xr = [link_xray(l["raw"], tb) for l in links]
    for l in links:
        highlights.append({"start": l["start"], "end": l["end"], "text": l["raw"], "rule_id": "link"})
    if links: fired["link"] = len(links)
    for x in xr:
        for f in x["flags"]:
            fired[f] = fired.get(f, 0) + 1
    # dedupe overlapping highlights: keep earliest start, longest span
    highlights.sort(key=lambda h: (h["start"], -(h["end"] - h["start"])))
    clean, last_end = [], -1
    for h in highlights:
        if h["start"] >= last_end:
            clean.append(h); last_end = h["end"]
    order = [r[0] for r in RULES]
    flags = [{"rule_id": rid, "weight": RULE[rid][1], "label_th": RULE[rid][2], "explain_th": RULE[rid][3], "hits": fired[rid]}
             for rid in order if rid in fired]
    raw_score = sum(f["weight"] for f in flags)
    # combo bonus: a link + (credential or money) is the classic phishing shape
    combo = bool(links) and ("credential" in fired or "money" in fired)
    score = min(100, raw_score + (10 if combo else 0))
    lv = level_of(score)
    return {"engine": VERSION, "channel": channel, "sender": sender, "text": text, "score": score, "raw_score": raw_score, "combo_bonus": 10 if combo else 0,
            **lv, "flags": flags, "highlights": clean, "links": xr, "claimed_brands": tb,
            "actions": action_plan(lv["level"], [f["rule_id"] for f in flags], tb),
            "disclaimer_th": "คะแนนนี้เป็นสัญญาณเตือน ไม่ใช่คำตัดสิน ถ้าไม่แน่ใจ โทรถามเบอร์ทางการที่หาเอง"}

AOC = {"name_th": "ศูนย์ AOC รับแจ้งภัยออนไลน์", "phone": "1441"}  # verify before launch

def action_plan(level, rule_ids, brands):
    steps = []
    if level in ("scam", "risky"):
        steps += [{"icon": "🛑", "text_th": "อย่ากดลิงก์ อย่าโอน อย่าบอก OTP"},
                  {"icon": "📞", "text_th": ("โทรถาม" + BRANDS[brands[0]]["name_th"] + " ด้วยเบอร์หลังบัตร/ในแอปทางการ") if brands else "โทรถามหน่วยงานด้วยเบอร์ที่หาเองจากเว็บทางการ"},
                  {"icon": "🚫", "text_th": "บล็อกผู้ส่ง แล้วลบข้อความ"},
                  {"icon": "📣", "text_th": f"ถ้าเผลอกด/โอนแล้ว: ติดต่อธนาคารทันที แล้วแจ้ง {AOC['name_th']} {AOC['phone']}"}]
    elif level == "caution":
        steps += [{"icon": "🔍", "text_th": "อย่าเพิ่งกด ตรวจลิงก์ด้วย Link X-Ray"},
                  {"icon": "📞", "text_th": "ถามคนส่งผ่านช่องทางอื่นที่รู้จักอยู่แล้ว"},
                  {"icon": "👨‍👩‍👧", "text_th": "ส่งการ์ดถามลูกหลานก่อนก็ได้"}]
    else:
        steps += [{"icon": "✅", "text_th": "ยังไม่เจอสัญญาณอันตรายชัด ๆ"},
                  {"icon": "🧠", "text_th": "ถ้ามีคนขอเงินหรือ OTP ทีหลัง ให้สแกนใหม่"}]
    if "off_platform" in rule_ids:
        steps.insert(1, {"icon": "📵", "text_th": "อย่าติดตั้งแอปหรือไฟล์ที่ส่งมาทางแชต"})
    reply = None
    if level in ("scam", "risky", "caution"):
        reply = "ขอบคุณค่ะ เดี๋ยวติดต่อหน่วยงานผ่านเบอร์ทางการเองนะคะ"
    return {"steps": steps, "safe_reply_th": reply, "best_reply_th": "ไม่ตอบเลย ดีที่สุด" if level in ("scam", "risky") else None}

def family_card(result, from_name, to_name):
    ex = result["text"][:60] + ("…" if len(result["text"]) > 60 else "")
    lines = [f"{result['emoji']} {result['label_th']} · {result['score']}/100",
             f"\"{ex}\""] + [f"• {f['label_th']}" for f in result["flags"][:3]] + [result["actions"]["steps"][0]["text_th"]]
    return {"kind": "family_alert", "size": "1080x1350", "to_th": to_name, "from_th": from_name,
            "title_th": f"{to_name} ระวังข้อความนี้นะ" if result["level"] in ("scam", "risky") else f"{to_name} ข้อความนี้ต้องเช็กก่อนนะ",
            "lines_th": lines, "accent": result["color"], "bg": "#0B1220", "footer": "เช็กด้วย ScamScan · AI วันละแอป",
            "line_text_th": f"{to_name} 🙏 ข้อความที่ได้มา ScamScan บอกว่า {result['label_th']} ({result['score']}/100) — {result['actions']['steps'][0]['text_th']}"}

# ---- Quiz: จริงหรือหลอก ----
def quiz_round(deck, seed, n=5):
    rng = random.Random(seed)
    ids = [c["id"] for c in deck]
    rng.shuffle(ids)
    return ids[:n]

def quiz_grade(deck, round_ids, answers):
    by = {c["id"]: c for c in deck}
    res = [{"id": i, "answer": a, "correct": by[i]["truth"] == a} for i, a in zip(round_ids, answers)]
    right = sum(r["correct"] for r in res)
    badge = "🛡️ สายตาเหยี่ยว" if right == len(res) else "👀 เกือบแล้ว" if right >= len(res) - 1 else "📚 ฝึกอีกนิด"
    return {"results": res, "right": right, "of": len(res), "badge_th": badge}

def quiz_streak(days_played):
    """days_played: sorted list of YYYY-MM-DD; streak = consecutive days ending at last item."""
    from datetime import date, timedelta
    ds = sorted({date.fromisoformat(d) for d in days_played})
    if not ds: return 0
    s, cur = 1, ds[-1]
    for d in reversed(ds[:-1]):
        if cur - d == timedelta(days=1): s += 1; cur = d
        else: break
    return s

# ---- Call Shield: ระหว่างคุยโทรศัพท์ ----
CALL_SIGNS = [
    ("cs_authority", 20, "อ้างเป็นตำรวจ/DSI/ศาล/ปปง."),
    ("cs_your_case", 20, "บอกว่าบัญชีเราพัวพันคดี/ฟอกเงิน"),
    ("cs_transfer_check", 25, "ให้โอนเงินไป 'ตรวจสอบ' หรือ 'บัญชีปลอดภัย'"),
    ("cs_secret", 15, "ห้ามบอกใคร ห้ามวางสาย"),
    ("cs_video_uniform", 10, "วิดีโอคอลโชว์เครื่องแบบ/บัตร/ห้องสถานี"),
    ("cs_app_install", 20, "ให้ติดตั้งแอปหรือแชร์หน้าจอ"),
    ("cs_otp", 20, "ขอ OTP หรือรหัส"),
    ("cs_parcel", 10, "อ้างพัสดุผิดกฎหมายติดชื่อเรา"),
]
def call_shield(ticked):
    w = {c[0]: c for c in CALL_SIGNS}
    score = min(100, sum(w[t][1] for t in ticked))
    lv = level_of(score)
    return {"ticked": ticked, "score": score, **lv,
            "say_th": "ขอวางสายก่อนนะคะ เดี๋ยวโทรกลับสถานี/ธนาคารด้วยเบอร์ทางการเอง",
            "rule_th": "หน่วยงานจริงไม่ให้โอนเงินไปตรวจสอบ และไม่ห้ามวางสาย"}

# ---- History & Wrapped ----
def history_entry(result, on):
    return {"on": on, "score": result["score"], "level": result["level"], "top_rule": result["flags"][0]["rule_id"] if result["flags"] else None,
            "brands": result["claimed_brands"], "preview_th": result["text"][:40]}

def shield_wrapped(history, month, quiz_days):
    hs = [h for h in history if h["on"].startswith(month)]
    flagged = [h for h in hs if h["level"] in ("scam", "risky")]
    from collections import Counter
    rc = Counter(h["top_rule"] for h in flagged if h["top_rule"])
    bc = Counter(b for h in flagged for b in h["brands"])
    top_rule = sorted(rc.items(), key=lambda kv: (-kv[1], kv[0]))[0][0] if rc else None
    top_brand = sorted(bc.items(), key=lambda kv: (-kv[1], kv[0]))[0][0] if bc else None
    return {"month": month, "checked": len(hs), "flagged": len(flagged), "low": sum(h["level"] == "low" for h in hs),
            "top_rule_id": top_rule, "top_rule_th": RULE[top_rule][2] if top_rule else None,
            "most_faked_brand": top_brand, "most_faked_brand_th": BRANDS[top_brand]["name_th"] if top_brand else None,
            "quiz_streak_days": quiz_streak([d for d in quiz_days if d.startswith(month)])}
