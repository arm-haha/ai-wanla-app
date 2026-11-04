"""Generate ../schemas.json + ../examples.json and validate every example."""
import json, os, jsonschema
from fixmate import *
from fixtures import *
S = "https://json-schema.org/draft/2020-12/schema"
hz = {"enum": sorted(STOP_TAGS | CAUTION_TAGS)}
defs = {
 "HomeProfile": {"type":"object","required":["home_type","owned_tools","skill_level"],"properties":{
   "home_type":{"enum":["condo","house","dorm","townhouse"]},"owned_tools":{"type":"array","items":{"type":"string"}},
   "skill_level":{"type":"integer","minimum":1,"maximum":5},"province":{"type":"string"}}},
 "Cause": {"type":"object","required":["cause_th","p"],"properties":{"cause_th":{"type":"string"},"p":{"type":"number","minimum":0,"maximum":1}}},
 "Diagnosis": {"type":"object","required":["issue_id","title_th","symptom_th","category","confidence","difficulty","minutes","hazard_tags","causes"],"properties":{
   "issue_id":{"type":"string"},"title_th":{"type":"string","minLength":1},"symptom_th":{"type":"string"},
   "category":{"enum":["plumbing","electrical","appliance","furniture","wall_floor","door_window"]},
   "confidence":{"type":"number","minimum":0,"maximum":1},"difficulty":{"type":"integer","minimum":1,"maximum":5},
   "minutes":{"type":"integer","minimum":1},"hazard_tags":{"type":"array","items":hz},
   "causes":{"type":"array","minItems":1,"items":{"$ref":"#/$defs/Cause"}},
   "pins":{"type":"array","items":{"type":"object","required":["label_th","xy"],"properties":{"label_th":{"type":"string"},"xy":{"type":"array","items":{"type":"number","minimum":0,"maximum":1},"minItems":2,"maxItems":2}}}}}},
 "SafetyGate": {"type":"object","required":["level","reasons","allow_diy"],"properties":{
   "level":{"enum":[OK,CAUTION,STOP]},"reasons":{"type":"array","items":{"type":"string"}},"allow_diy":{"type":"boolean"}}},
 "Part": {"type":"object","required":["id","name_th","search_kw","price_thb"],"properties":{
   "id":{"type":"string"},"name_th":{"type":"string"},"search_kw":{"type":"string"},
   "price_thb":{"type":"number","minimum":0},"qty":{"type":"integer","minimum":1},"price_source":{"enum":["user_set","example"]}}},
 "Tool": {"type":"object","required":["id","name_th","price_thb"],"properties":{"id":{"type":"string"},"name_th":{"type":"string"},"price_thb":{"type":"number","minimum":0}}},
 "FixStep": {"type":"object","required":["id","text_th","minutes"],"properties":{
   "id":{"type":"string"},"text_th":{"type":"string"},"minutes":{"type":"integer","minimum":1},
   "arrow_xy":{"type":"array","items":{"type":"number"},"minItems":2,"maxItems":2},"warn_th":{"type":"string"}}},
 "Verdict": {"type":"object","required":["verdict","safety","diy_total_thb","pro_quote_thb","minutes","save_thb","missing_tools"],"properties":{
   "verdict":{"enum":["diy","call_pro","need_photo"]},"safety":{"enum":[OK,CAUTION,STOP]},"diy_total_thb":{"type":"number"},
   "pro_quote_thb":{"type":"number","exclusiveMinimum":0},"minutes":{"type":"integer"},"save_thb":{"type":"number","minimum":0},
   "missing_tools":{"type":"array","items":{"type":"string"}}}},
 "DripWaste": {"type":"object","required":["liters_month","buckets_10l"],"properties":{"liters_month":{"type":"integer","minimum":0},"buckets_10l":{"type":"integer","minimum":0}}},
 "StepProgress": {"type":"object","required":["done","total","pct","minutes_left","next_step"],"properties":{
   "done":{"type":"integer"},"total":{"type":"integer"},"pct":{"type":"integer","minimum":0,"maximum":100},
   "minutes_left":{"type":"integer"},"next_step":{"type":["string","null"]}}},
 "CareItem": {"type":"object","required":["id","title_th","next_due","overdue_days","due_in_days"],"properties":{
   "id":{"type":"string"},"title_th":{"type":"string"},"next_due":{"type":"string","format":"date"},
   "overdue_days":{"type":"integer","minimum":0},"due_in_days":{"type":"integer","minimum":0}}},
 "SavingsTally": {"type":"object","required":["fixes","saved_thb","minutes","badge"],"properties":{
   "fixes":{"type":"integer"},"saved_thb":{"type":"number"},"minutes":{"type":"integer"},"badge":{"type":["string","null"]}}},
 "ProMessage": {"type":"object","required":["channel","text_th","photos"],"properties":{"channel":{"enum":["line","sms","copy"]},"text_th":{"type":"string"},"photos":{"type":"integer","minimum":0}}},
 "ReelCard": {"type":"object","required":["kind","title_th","before","after"],"properties":{
   "kind":{"enum":["fix_glowup","saved_money","safety_stop","care_streak"]},"title_th":{"type":"string"},
   "before":{"type":"string"},"after":{"type":"string"},"stat":{"type":"string"}}},
}
schema = {"$schema":S,"$id":"fixmate.schemas.json","title":"FixMate schemas","$defs":defs}
fixes = [{"verdict":"diy","status":"fixed","save_thb":355,"minutes":20},{"verdict":"diy","status":"fixed","save_thb":480,"minutes":15}]
ex = {
 "HomeProfile":[{"home_type":"condo","owned_tools":OWNED,"skill_level":1,"province":"กรุงเทพฯ"},{"home_type":"house","owned_tools":["screwdriver","adj_wrench","drill"],"skill_level":3}],
 "Diagnosis":[FAUCET,TOILET,OUTLET,AIRCON],
 "SafetyGate":[safety_gate(d) for d in (FAUCET,TOILET,OUTLET,AIRCON)],
 "Part":[{**p,"price_source":"example"} for p in FAUCET_PARTS+TOILET_PARTS],
 "Tool":FAUCET_TOOLS,
 "FixStep":FAUCET_STEPS,
 "Verdict":[verdict(FAUCET,FAUCET_PARTS,FAUCET_TOOLS,OWNED,500),verdict(TOILET,TOILET_PARTS,[],OWNED,600),verdict(OUTLET,[],[],OWNED,400),verdict(AIRCON,[],[],OWNED,800)],
 "DripWaste":[drip_waste(60),drip_waste(20)],
 "StepProgress":[step_progress(FAUCET_STEPS,set()),step_progress(FAUCET_STEPS,{"s1","s2"}),step_progress(FAUCET_STEPS,{s["id"] for s in FAUCET_STEPS})],
 "CareItem":care_schedule(CARE,TODAY),
 "SavingsTally":[savings_tally(fixes),savings_tally([])],
 "ProMessage":[{"channel":"line","text_th":pro_message(OUTLET,"ห้องนอน คอนโดชั้น 12",2),"photos":2}],
 "ReelCard":[{"kind":"fix_glowup","title_th":"ก๊อกหยดมา 3 เดือน ซ่อมเอง 20 นาที","before":"หยด 60 ครั้ง/นาที ≈ 130 ลิตร/เดือน","after":"0 หยด","stat":"ประหยัดค่าช่าง ฿355 (ราคาตัวอย่าง)"},
             {"kind":"saved_money","title_th":"เดือนนี้ซ่อมเอง 2 งาน","before":"ช่าง ฿1,100","after":"ซ่อมเอง ฿265","stat":"เก็บไว้ ฿835"},
             {"kind":"safety_stop","title_th":"อันนี้อย่าซ่อมเอง!","before":"ปลั๊กมีรอยไหม้","after":"ตัดเบรกเกอร์ + ส่งข้อความหาช่างใน 1 แตะ"}],
}
v = jsonschema.Draft202012Validator; n = 0
v.check_schema(schema)
for k, items in ex.items():
    for it in items:
        jsonschema.validate(it, {"$schema":S,"$defs":defs,"$ref":f"#/$defs/{k}"}); n += 1
os.chdir(os.path.dirname(os.path.abspath(__file__)))
json.dump(schema, open("../schemas.json","w"), ensure_ascii=False, indent=1)
json.dump(ex, open("../examples.json","w"), ensure_ascii=False, indent=1)
print(f"{len(defs)} defs, {n} examples valid")
