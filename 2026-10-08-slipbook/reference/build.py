import json, copy
from slip import *
from fixtures import *

TZ = "+07:00"
def iso(d, t): return f"{d}T{t}:00{TZ}"
mem = {norm_key(k): v for k, v in MEMORY.items()}

# ---------- parse + import demo batch ----------
parsed, seen, batch_rows = [], {}, []
for sid, fname, tpl, txt in SLIPS:
    p = parse_slip(txt, OWNER_NAMES)
    cat, src, cconf = categorize(p["counterparty"], p["direction"], mem)
    key = dedupe_key(p)
    dup_of = seen.get(key)
    reasons = []
    if p["confidence"] < 0.85: reasons.append("missing_fields")
    if cconf < 0.6: reasons.append("who_is_this")
    if dup_of: reasons = []
    row = {"slip_id": sid, "file_name": fname, "template_hint": tpl, "parse_engine": "regex_th_v1",
           "amount": p["amount"], "currency": "THB", "date": p["date"], "time": p["time"], "ref": p["ref"],
           "counterparty": p["counterparty"], "counterparty_account_masked": p["counterparty_account_masked"],
           "direction": p["direction"], "bank": p["bank"], "parse_confidence": p["confidence"],
           "missing_fields": p["missing"], "dedupe_key": key,
           "category_guess": {"category": cat, "source": src, "confidence": cconf},
           "status": "duplicate" if dup_of else ("needs_review" if reasons else "ok"),
           "duplicate_of": dup_of, "review_reasons": reasons}
    if not dup_of: seen[key] = sid
    parsed.append(row)

added = [r for r in parsed if r["status"] != "duplicate"]
batch = {"batch_id": "imp_20261008_0812", "created_at": iso(TODAY, "08:12"), "files_dropped": len(SLIPS),
         "parsed_ok": sum(1 for r in parsed if r["parse_confidence"] >= 0.85),
         "duplicates_skipped": sum(1 for r in parsed if r["status"] == "duplicate"),
         "needs_review": sum(1 for r in parsed if r["status"] == "needs_review"),
         "added": len(added),
         "out_total": round(sum(r["amount"] for r in added if r["direction"] == "out"), 2),
         "in_total": round(sum(r["amount"] for r in added if r["direction"] == "in"), 2),
         "duration_ms_target": 3000, "slip_ids": [r["slip_id"] for r in parsed]}

# user confirms s07 -> friends, learns memory
mem_after = dict(mem); mem_after[norm_key("น.ส. แพรวา ส.")] = "friends"

# ---------- ledger ----------
ledger = []
for i, (d, t, cp, amt, cat) in enumerate(HISTORY):
    ledger.append({"id": f"tx_{i+1:03d}", "date": d, "time": t, "created_at": iso(d, t), "counterparty": cp,
                   "amount": amt, "currency": "THB", "direction": "out", "category": cat, "category_source": "user",
                   "source": "slip", "slip_id": None, "ref": None, "note": "", "tags": []})
n = len(ledger)
for r in added:
    n += 1
    cat = r["category_guess"]["category"]; src = r["category_guess"]["source"]
    if r["slip_id"] == "s07": src = "user"
    ledger.append({"id": f"tx_{n:03d}", "date": r["date"], "time": r["time"], "created_at": iso(r["date"], r["time"]),
                   "counterparty": r["counterparty"], "amount": r["amount"], "currency": "THB", "direction": r["direction"],
                   "category": cat, "category_source": src, "source": "slip", "slip_id": r["slip_id"], "ref": r["ref"],
                   "note": "หารหมูกระทะ" if r["slip_id"] == "s07" else ("คืนค่าตั๋วหนัง" if r["slip_id"] == "s18" else ""), "tags": []})

dash_oct = dashboard(ledger, "2026-10"); dash_sep = dashboard(ledger, "2026-09")
for dsh in (dash_oct, dash_sep):
    mx = max(x["amount"] for x in dsh["daily"])
    for x in dsh["daily"]: x["heat"] = heat_level(x["amount"], mx)
bud = budget_status(dash_oct, BUDGETS_OCT, TODAY)
subs = subscriptions(ledger)

# ---------- wrapped (Sep) ----------
sep_out = [t for t in ledger if t["date"].startswith("2026-09") and t["direction"] == "out"]
days_with = {t["date"] for t in sep_out}
no_spend = 30 - len(days_with)
cnt = {}
for t in sep_out: cnt.setdefault(t["counterparty"], [0, 0.0]); cnt[t["counterparty"]][0] += 1; cnt[t["counterparty"]][1] += t["amount"]
fav = sorted(cnt.items(), key=lambda kv: (-kv[1][0], -kv[1][1]))[0]
big_day = sorted(dash_sep["daily"], key=lambda x: (-x["amount"], x["date"]))[0]
top_cat = dash_sep["by_category"][0]
plates = int(fav[1][1] // 60)
sub_year = round(sum(s["yearly_cost"] for s in subs), 2)
wrapped = {"month": "2026-09", "title_th": "สลิปบุ๊ก แรป · กันยายน 2026", "spent_total": dash_sep["spent_total"],
  "txn_count": dash_sep["txn_count"], "slides": [
   {"n":1,"kind":"total","headline_th":f"เดือนนี้เงินออกไป ฿{dash_sep['spent_total']:,.0f}","sub_th":f"จาก {dash_sep['txn_count']} สลิป"},
   {"n":2,"kind":"top_category","headline_th":f"หมวดที่กินเงินที่สุด {top_cat['emoji']} {top_cat['label_th']}","sub_th":f"฿{top_cat['amount']:,.0f} · {top_cat['percent']}%"},
   {"n":3,"kind":"favorite_place","headline_th":f"ขาประจำ: {fav[0]}","sub_th":f"{fav[1][0]} ครั้ง · ฿{fav[1][1]:,.0f} ≈ ข้าวมันไก่ {plates} จาน"},
   {"n":4,"kind":"biggest_day","headline_th":f"วันที่ใช้หนักสุด {big_day['date']}","sub_th":f"฿{big_day['amount']:,.0f}"},
   {"n":5,"kind":"no_spend_days","headline_th":f"วันที่ไม่จ่ายอะไรเลย {no_spend} วัน","sub_th":"เก่งมาก 👏"},
   {"n":6,"kind":"subscriptions","headline_th":f"ตัดทุกเดือน {len(subs)} รายการ","sub_th":f"ปีละ ฿{sub_year:,.0f} — ยังใช้ครบไหม?"}],
  "favorite": {"name": fav[0], "count": fav[1][0], "amount": round(fav[1][1], 2), "compare_th": f"≈ ข้าวมันไก่ {plates} จาน"},
  "no_spend_days": no_spend, "biggest_day": big_day}

CAT_LIST = [CAT[k] for k in CAT]
examples = {
 "meta": {"app": "SlipBook", "pack_date": "2026-10-08", "day_in_queue": "9/10", "channel": "AI วันละแอป",
          "persona_note": "ต้นกล้า เป็นตัวละครสมมติ ทุกชื่อ/เลขบัญชี/เลขอ้างอิงในไฟล์นี้แต่งขึ้น",
          "currency": "THB", "timezone": "Asia/Bangkok", "today": TODAY},
 "categories": CAT_LIST,
 "category_rules": [{"keyword": k, "category": c} for k, c in RULES],
 "merchant_memory_before": mem, "merchant_memory_after": mem_after,
 "settings_example": {"owner_names": OWNER_NAMES, "lang": "th", "ocr_engine": "tesseract_tha_eng", "ai_parse": "off",
    "keep_images": False, "mask_accounts": True, "hide_amounts_on_share": False, "month_start_day": 1,
    "pin_lock": False, "reminder": {"enabled": True, "time": "21:00"}, "currency": "THB"},
 "budgets": {"month": "2026-10", "by_category": BUDGETS_OCT},
 "slips_raw": [{"slip_id": s, "file_name": f, "template_hint": t, "ocr_text": x} for s, f, t, x in SLIPS],
 "parsed_slips": parsed,
 "import_batch_example": batch,
 "review_edit_example": {"slip_id": "s07", "question_th": "น.ส. แพรวา ส. คือใคร?", "options": ["family", "friends", "other"],
    "chosen": "friends", "remember": True, "memory_key": norm_key("น.ส. แพรวา ส."), "note": "หารหมูกระทะ"},
 "ledger": ledger,
 "dashboard_oct": dash_oct, "dashboard_sep": dash_sep,
 "budget_status_oct": bud,
 "subscriptions": subs,
 "wrapped_sep": wrapped,
}

# share cards
examples["share_cards"] = [
 {"id": "card_wrapped_sep", "variant": "wrapped_story", "size": [1080, 1920], "month": "2026-09",
  "show_amounts": True, "show_counterparties": False, "headline_th": wrapped["slides"][0]["headline_th"],
  "lines_th": [s["headline_th"] for s in wrapped["slides"][1:4]], "footer_th": "ทำบัญชีจากสลิปใน 10 วิ · SlipBook", "theme": "mint"},
 {"id": "card_month_square", "variant": "donut_square", "size": [1080, 1080], "month": "2026-10",
  "show_amounts": False, "show_counterparties": False, "headline_th": "ต.ค. เงินไหลไปไหน?",
  "lines_th": [f"{c['emoji']} {c['label_th']} {c['percent']}%" for c in dash_oct["by_category"][:4]],
  "footer_th": "ทำบัญชีจากสลิปใน 10 วิ · SlipBook", "theme": "mint"}]

examples["search_example"] = {"query": "Café Amazon", "range": ["2026-09-01", "2026-10-08"],
  "matches": sum(1 for t in ledger if "café amazon" in norm_key(t["counterparty"])),
  "total": round(sum(t["amount"] for t in ledger if "café amazon" in norm_key(t["counterparty"])), 2)}

examples["ui_copy_th"] = {
 "home_title": "สลิปเต็มแกลเลอรี่?", "home_sub": "โยนเข้ามาเลย เดี๋ยวทำบัญชีให้", "drop_cta": "เลือกสลิปจากแกลเลอรี่",
 "demo_cta": "ลองข้อมูลตัวอย่าง (ต้นกล้า)", "privacy_badge": "อ่านสลิปในเครื่อง · ไม่เก็บรูป · ปิดเลขบัญชีให้อัตโนมัติ",
 "importing": "กำลังอ่าน {done}/{total} สลิป…", "import_done": "เพิ่ม {added} รายการ · ข้ามสลิปซ้ำ {dup} · รอเช็ก {review}",
 "dup_chip": "สลิปซ้ำ — ข้ามให้แล้ว", "review_missing": "อ่านไม่ครบ ช่วยเช็กหน่อย", "review_who": "{name} คือใคร?",
 "remember_toggle": "จำไว้ ครั้งหน้าจัดให้เลย", "dashboard_title": "{month} เงินไหลไปไหน?",
 "safe_per_day": "ใช้ได้อีกวันละ ฿{amount}", "jar_warn": "{emoji} {label} ใช้ไป {percent}% แล้ว",
 "jar_over": "{emoji} {label} เกินงบ ฿{over}", "subs_title": "ตัดเงินทุกเดือน", "subs_line": "{name} ฿{amount}/เดือน = ฿{yearly}/ปี",
 "wrapped_cta": "ดูสรุปเดือนนี้", "share_cta": "แชร์การ์ด", "hide_amounts": "ซ่อนตัวเลขเงิน",
 "empty_month": "ยังไม่มีสลิปเดือนนี้ — ลองโยนเข้ามาสัก 3 ใบ",
 "disclaimer": "SlipBook ช่วยจดรายจ่ายจากสลิป ไม่ได้ตรวจสอบว่าสลิปจริงหรือปลอม และไม่เชื่อมบัญชีธนาคาร"}

top3 = dash_oct["by_category"][:3]
examples["reel_script_th"] = [
 {"t":"0-3s","shot":"เลื่อนแกลเลอรี่ที่มีแต่สลิปโอนเงิน (ใช้สลิปตัวอย่าง)","overlay":"สลิปเต็มเครื่อง แต่ไม่รู้เงินหายไปไหน 😵","vo":"ใครแกลเลอรี่เป็นแบบนี้บ้าง"},
 {"t":"3-7s","shot":"สั่ง AI สร้างแอป: จอ prompt + โค้ดวิ่ง (speed ramp)","overlay":"ให้ AI เขียนแอปให้ 1 วัน","vo":"วันนี้ให้ AI ทำแอปเปลี่ยนสลิปเป็นบัญชี"},
 {"t":"7-13s","shot":"เลือก 18 สลิป → สลิปบินเข้ากองแล้วแตกเป็นแถวรายการ ตัวเลขนับขึ้น","overlay":f"18 สลิป → บัญชีใน 3 วิ · ข้ามสลิปซ้ำ 1","vo":"โยนเข้าไปทีเดียว 18 ใบ"},
 {"t":"13-17s","shot":"โดนัทหมวดหมู่หมุนเข้า","overlay":f"ต.ค. ใช้ไป ฿{dash_oct['spent_total']:,.0f} · {top3[0]['emoji']} {top3[0]['label_th']} {top3[0]['percent']}%","vo":"รู้เลยเงินไปไหน"},
 {"t":"17-21s","shot":"แตะชิป 'น.ส. แพรวา ส. คือใคร?' → เลือกเพื่อน → จำไว้","overlay":"สอนครั้งเดียว ครั้งหน้าจัดให้เอง","vo":""},
 {"t":"21-25s","shot":"Budget jars + ป้าย 'ใช้ได้อีกวันละ'","overlay":f"ใช้ได้อีกวันละ ฿{bud['safe_per_day']:,}","vo":"แถมบอกว่าวันนี้ใช้ได้อีกเท่าไหร่"},
 {"t":"25-28s","shot":"การ์ดตัดทุกเดือน + Wrapped สไลด์","overlay":f"ตัดทุกเดือน ปีละ ฿{sub_year:,.0f} 😳","vo":""},
 {"t":"28-30s","shot":"หน้าผู้พูด + การ์ดแชร์","overlay":"คอมเมนต์「สลิป」รับลิงก์ฟรี","vo":"อยากได้คอมเมนต์คำว่า สลิป"}]

examples["test_vectors"] = [
 {"name":"parse_s01_template_A","input_slip":"s01","expect":{"amount":89.0,"date":"2026-10-01","time":"08:12","ref":"0126274A0812KP01","direction":"out","category":"food"}},
 {"name":"parse_s03_template_C_buddhist_slash","input_slip":"s03","expect":{"amount":200.0,"date":"2026-10-01","time":"18:45","category":"transport"}},
 {"name":"thousand_separator","input_slip":"s08","expect":{"amount":1284.5,"category":"bills"}},
 {"name":"duplicate_same_ref","input_slip":"s09","expect":{"status":"duplicate","duplicate_of":"s08"}},
 {"name":"person_unknown_asks","input_slip":"s07","expect":{"category":"friends","source":"person_default","status":"needs_review","counterparty_account_masked":"xxx-x-x5190-x"}},
 {"name":"memory_family","input_slip":"s13","expect":{"category":"family","source":"memory"}},
 {"name":"missing_ref_fingerprint","input_slip":"s14","expect":{"ref":None,"parse_confidence":0.8,"status":"needs_review","dedupe_key":"fp:2026-10-06|12:40|120.00|ร้านส้มตำนัว"}},
 {"name":"incoming_by_owner_name","input_slip":"s18","expect":{"direction":"in","counterparty":"นาย ภูมิ ใจดี","category":"income"}},
 {"name":"batch_counts","expect":{"files_dropped":batch["files_dropped"],"duplicates_skipped":batch["duplicates_skipped"],"needs_review":batch["needs_review"],"added":batch["added"],"out_total":batch["out_total"],"in_total":batch["in_total"]}},
 {"name":"dashboard_oct","expect":{"spent_total":dash_oct["spent_total"],"income_total":dash_oct["income_total"],"txn_count":dash_oct["txn_count"],"top3":[[c["category"],c["amount"],c["percent"]] for c in top3]}},
 {"name":"budget_oct_today","expect":{"remaining_days_incl_today":bud["remaining_days_incl_today"],"left_total":bud["left_total"],"safe_per_day":bud["safe_per_day"],"warn_or_over":[j["category"] for j in bud["jars"] if j["state"]!="ok"]}},
 {"name":"subscriptions","expect":[[s["counterparty"],s["amount"],s["yearly_cost"]] for s in subs]},
 {"name":"wrapped_sep","expect":{"spent_total":dash_sep["spent_total"],"txn_count":dash_sep["txn_count"],"favorite":wrapped["favorite"],"no_spend_days":no_spend}},
]
examples["feature_checklist_example"] = {"must_have": [
  {"key":"slip_drop","label":"Slip Drop → Auto Book","done":True},
  {"key":"smart_category","label":"Smart Category + Merchant Memory","done":True},
  {"key":"month_dashboard","label":"Month Dashboard (โดนัท + ปฏิทินร้อน + ท็อปผู้รับ)","done":True},
  {"key":"budget_jars","label":"Budget Jars + ใช้ได้อีกวันละ","done":True},
  {"key":"share_wrapped","label":"Money Wrapped + Share Card","done":True}],
 "nice_to_have": [
  {"key":"subscription_spotter","label":"ตัดเงินทุกเดือน","done":True},
  {"key":"search","label":"ค้นหา/กรอง","done":False},{"key":"split_link","label":"ส่งต่อ SplitBill","done":False},
  {"key":"export_csv","label":"ส่งออก CSV/Sheets","done":False},{"key":"pin_lock","label":"ล็อก PIN","done":False},
  {"key":"reminder","label":"เตือน 21:00 โยนสลิปวันนี้","done":False},{"key":"quick_add","label":"เพิ่มเงินสดด้วยมือ","done":False}]}
examples["analytics_events_example"] = [
 {"name":"import_completed","at":iso(TODAY,"08:12"),"props":{"files":18,"added":17,"dup":1,"review":2,"ms":2400}},
 {"name":"category_corrected","at":iso(TODAY,"08:13"),"props":{"from_source":"person_default","to":"friends","remember":True}},
 {"name":"share_card_exported","at":iso(TODAY,"08:15"),"props":{"variant":"wrapped_story","show_amounts":True}}]
examples["local_store_example"] = {"key":"slipbook:v1","version":1,"settings":examples["settings_example"],
  "budgets":[examples["budgets"]],"merchant_memory":mem_after,"txn_count":len(ledger),"last_import_batch":batch["batch_id"],
  "seen_dedupe_keys_count":len(seen),"note":"transactions อยู่ใน IndexedDB store 'txns' (ดู ledger) — localStorage เก็บแค่ค่าตั้ง/งบ/memory"}

json.dump(examples, open("../examples.json","w"), ensure_ascii=False, indent=2)
print(json.dumps({k: examples[k] for k in ["import_batch_example"]}, ensure_ascii=False))
print("OCT", dash_oct["spent_total"], dash_oct["income_total"], dash_oct["txn_count"], [(c["category"],c["amount"],c["percent"]) for c in dash_oct["by_category"]])
print("SEP", dash_sep["spent_total"], dash_sep["txn_count"], [(c["category"],c["amount"],c["percent"]) for c in dash_sep["by_category"]][:4])
print("BUD", {k:bud[k] for k in bud if k!="jars"}); print([(j["category"],j["spent"],j["percent"],j["state"]) for j in bud["jars"]])
print("SUBS", subs); print("WRAP", wrapped["favorite"], no_spend, big_day, sub_year)
print("SEARCH", examples["search_example"])
