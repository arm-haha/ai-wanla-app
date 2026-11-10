"""Generate ../schemas.json + ../examples.json and validate every example."""
import json, os, jsonschema
from contractlens import *
from fixtures import *

S="https://json-schema.org/draft/2020-12/schema"
s={"type":"string"}; b={"type":"boolean"}; n0={"type":"number","minimum":0}
u={"type":"number","minimum":0,"maximum":1}; i0={"type":"integer","minimum":0}; i1={"type":"integer","minimum":1}
pct={"type":"integer","minimum":0,"maximum":100}
date={"type":"string","format":"date","pattern":"^[0-9]{4}-[0-9]{2}-[0-9]{2}$"}
kind={"enum":KINDS}; level={"enum":list(LEVELS)}; ck={"enum":list(CLAUSES)}

def obj(req, props, **kw):
    return {"type":"object","required":req,"properties":props,"additionalProperties":False, **kw}
def arr(i, **kw):
    return {"type":"array","items":i, **kw}

defs = {
 "Person": obj(["id","name_th","age","region"], {
    "id":{"type":"string","pattern":"^u[0-9]{2}$"},"name_th":s,"name_en":s,"age":i1,"city_th":s,"goal_th":s,
    "region":{"enum":list(REGION_MULT)}}),
 "Detection": obj(["clause","confidence"], {"clause":ck,"confidence":u,"excerpt_th":s}),
 "ContractPhoto": obj(["id","px_w","px_h","kind","glare","blur","tilt","text_fill","detections"], {
    "id":{"type":"string","pattern":"^p[0-9]{2}$"},"px_w":i1,"px_h":i1,"kind":kind,"glare":u,"blur":u,"tilt":u,
    "text_fill":u,"detections":arr({"$ref":"#/$defs/Detection"})}),
 "ScanQuality": obj(["score","ok","tips_th"], {"score":pct,"ok":b,"tips_th":arr(s)}),
 "IdentifiedClause": obj(["clause","name_th","confidence"], {"clause":ck,"name_th":s,"confidence":u,"excerpt_th":s}),
 "ContractScan": obj(["photo_id","kind","kind_th","quality","clauses","uncertain","clause_count","ok","disclaimer_th"], {
    "photo_id":s,"kind":kind,"kind_th":s,"quality":{"$ref":"#/$defs/ScanQuality"},
    "clauses":arr({"$ref":"#/$defs/IdentifiedClause"}),"uncertain":arr(ck),"clause_count":i0,"ok":b,"disclaimer_th":s}),
 "Pipeline": obj(["photo_id","steps"], {"photo_id":s,"steps":arr(s,minItems=1)}),
 "ClauseInfo": obj(["id","key","name_th","kind","default_level","meaning_th","why_th","ask_th"], {
    "id":{"type":"string","pattern":"^c[0-9]{2}$"},"key":ck,"name_th":s,"kind":{"enum":["rental","loan","both"]},
    "default_level":level,"meaning_th":s,"why_th":s,"ask_th":arr(s)}),
 "RiskItem": obj(["clause","name_th","level","meaning_th","why_th","ask_th"], {
    "clause":ck,"name_th":s,"level":level,"meaning_th":s,"why_th":s,"ask_th":arr(s)}),
 "RiskHighlights": obj(["kind","level","score","count","items","red_count","yellow_count","headline_th","disclaimer_th"], {
    "kind":kind,"level":level,"score":pct,"count":i0,"items":arr({"$ref":"#/$defs/RiskItem"}),
    "red_count":i0,"yellow_count":i0,"headline_th":s,"disclaimer_th":s}),
 "PlainSummary": obj(["kind","kind_th","level","bullets_th","headline_th","plain_th","disclaimer_th"], {
    "kind":kind,"kind_th":s,"level":level,"bullets_th":arr(s),"headline_th":s,"plain_th":s,"disclaimer_th":s}),
 "RentalFees": obj(["kind","rent_thb","deposit_thb","advance_thb","extras_thb","move_in_thb","late_fee_per_day_thb","late_30d_thb","breakdown_th","disclaimer_th"], {
    "kind":{"const":"rental"},"rent_thb":i0,"deposit_thb":i0,"advance_thb":i0,"extras_thb":i0,"move_in_thb":i0,
    "late_fee_per_day_thb":i0,"late_30d_thb":i0,"breakdown_th":arr(s),"disclaimer_th":s}),
 "LoanFees": obj(["kind","principal_thb","interest_total_thb","total_payable_thb","installment_thb","term_months","method_th","disclaimer_th"], {
    "kind":{"const":"loan"},"principal_thb":i0,"interest_total_thb":i0,"total_payable_thb":i0,"installment_thb":i0,
    "term_months":i1,"method_th":s,"disclaimer_th":s}),
 "Questions": obj(["questions_th","count","disclaimer_th"], {"questions_th":arr(s,minItems=1),"count":i1,"disclaimer_th":s}),
 "CheckItem": obj(["key","text_th","done"], {"key":s,"text_th":s,"done":b}),
 "SignChecklist": obj(["kind","items","done_count","total","missing","ready_to_sign","message_th","disclaimer_th"], {
    "kind":kind,"items":arr({"$ref":"#/$defs/CheckItem"},minItems=1),"done_count":i0,"total":i1,
    "missing":arr(s),"ready_to_sign":b,"message_th":s,"disclaimer_th":s}),
 "FamilyCard": obj(["title_th","name_th","kind","kind_th","level","score","headline_th","money_th","note_th","line_share_url","disclaimer_th"], {
    "title_th":s,"name_th":s,"kind":kind,"kind_th":s,"level":level,"score":pct,"headline_th":s,"money_th":s,
    "note_th":s,"line_share_url":{"type":"string","pattern":"^https://line\\.me/R/share\\?text="},"disclaimer_th":s}),
 "DiaryEntry": obj(["id","person_id","date","kind","title_th","level","on_device"], {
    "id":s,"person_id":s,"date":date,"kind":kind,"title_th":s,"level":level,"on_device":b}),
 "DiaryStats": obj(["count","red","last_date","top_kind"], {
    "count":i0,"red":i0,"last_date":{"type":["string","null"]},"top_kind":{"type":["string","null"]}}),
 "ShareCard": obj(["title_th","headline_th","hook_th","level","score","layout","sizes","watermark","cta_th"], {
    "title_th":s,"headline_th":s,"hook_th":s,"level":level,"score":pct,"layout":{"enum":["risk_result"]},
    "sizes":arr({"enum":["1080x1350","1080x1920","1080x1080"]}),"watermark":s,"cta_th":s}),
 "Quota": obj(["allowed","left_after","paywall"], {"allowed":i0,"left_after":{"type":["integer","null"],"minimum":0},"paywall":b}),
 "SafetyGuard": obj(["level","message_th"], {"level":{"enum":["ok","warn","stop"]},"message_th":s}),
}
schema={"$schema":S,"$id":"https://example.com/contractlens.schema.json","title":"ContractLens","$defs":defs}

def ref(n):
    return {"$ref":f"#/$defs/{n}","$defs":defs}

ex=[]
def add(n,v,note=""):
    ex.append({"def":n,"note":note,"value":v})

for p in PEOPLE:
    add("Person", p, p["name_th"])
for ph in PHOTOS:
    add("ContractPhoto", ph, ph["id"])
    add("ContractScan", contract_scan(ph), ph["id"])
    add("Pipeline", {"photo_id":ph["id"],"steps":pipeline_steps(ph)}, ph["id"])
for k in CLAUSES:
    add("ClauseInfo", clause_info(k), k)

h_benz = risk_highlights("rental", BENZ_PHOTO["detections"], BENZ_TERMS)
add("RiskHighlights", h_benz, "benz")
add("RiskHighlights", risk_highlights("loan", PHOTOS[1]["detections"], LOAN_TERMS), "ohm loan")
add("RiskHighlights", risk_highlights("rental", PHOTOS[2]["detections"], CLEAN_RENT), "blanks")
add("RiskHighlights", risk_highlights("rental", PHOTOS[3]["detections"], CLEAN_RENT), "utility")
add("RiskHighlights", risk_highlights("rental", [], CLEAN_RENT), "green")
add("RiskHighlights", risk_highlights("rental", [], dict(BENZ_TERMS, deposit_months=3)), "numeric deposit")
add("PlainSummary", plain_summary("rental", BENZ_TERMS, h_benz), "benz")
add("PlainSummary", plain_summary("loan", LOAN_TERMS, risk_highlights("loan", PHOTOS[1]["detections"], LOAN_TERMS)), "loan")
fees_b = fee_calc("rental", BENZ_TERMS)
add("RentalFees", fees_b, "benz")
add("RentalFees", fee_calc("rental", CLEAN_RENT), "clean")
add("LoanFees", fee_calc("loan", LOAN_TERMS), "ohm")
add("LoanFees", fee_calc("loan", {"principal_thb":50000,"interest_pct_month":0.8,"term_months":6}), "mild")
add("Questions", questions_to_ask(h_benz), "benz")
add("Questions", questions_to_ask(risk_highlights("loan", PHOTOS[1]["detections"], LOAN_TERMS)), "loan")
add("SignChecklist", sign_checklist("rental", BENZ_CHECKED), "incomplete")
add("SignChecklist", sign_checklist("rental", [k for k,_ in CHECKLIST_RENTAL]), "complete rental")
add("SignChecklist", sign_checklist("loan", []), "empty loan")
add("SignChecklist", sign_checklist("loan", [k for k,_ in CHECKLIST_LOAN]), "complete loan")
add("FamilyCard", family_card(BENZ, contract_scan(BENZ_PHOTO), h_benz, fees_b, BENZ_NOTE), "benz")
add("FamilyCard", family_card(PEOPLE[1], contract_scan(PHOTOS[1]), risk_highlights("loan", PHOTOS[1]["detections"], LOAN_TERMS), fee_calc("loan", LOAN_TERMS), "ให้ทนายอ่านก่อน"), "ohm")
for e in [diary_entry(*x) for x in DIARY]:
    add("DiaryEntry", e, e["id"])
add("DiaryStats", diary_stats([diary_entry(*x) for x in DIARY]), "benz")
add("DiaryStats", diary_stats([]), "empty")
add("ShareCard", share_card(BENZ["name_th"], h_benz), "benz")
add("Quota", quota(1,1), "free")
add("Quota", quota(3,1), "exhausted")
add("Quota", quota(0,5,pro=True), "pro")
for lv in ("green","yellow","red"):
    add("SafetyGuard", safety_guard(lv), lv)

for e in ex:
    jsonschema.validate(e["value"], ref(e["def"]))
d=os.path.dirname(os.path.abspath(__file__))+"/.."
json.dump(schema, open(d+"/schemas.json","w"), ensure_ascii=False, indent=1)
json.dump({"examples":ex}, open(d+"/examples.json","w"), ensure_ascii=False, indent=1)
print(len(defs),"defs,",len(ex),"examples, all valid")
