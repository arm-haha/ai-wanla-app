"""Generate ../schemas.json + ../examples.json and validate every example."""
import json, os, jsonschema
from labellens import *
from fixtures import *
S = "https://json-schema.org/draft/2020-12/schema"
light = {"enum":[GREEN,AMBER,RED]}
nut = {"type":"object","required":["kcal","sugar_g","fat_g","sodium_mg"],"properties":{k:{"type":"number","minimum":0} for k in ("kcal","sugar_g","fat_g","sodium_mg")}}
defs = {
 "UserProfile":{"type":"object","required":["name","allergies","goal"],"properties":{"name":{"type":"string"},
   "allergies":{"type":"array","items":{"enum":sorted(ALLERGENS)}},"goal":{"enum":["cut_sugar","cut_salt","balanced","kid_mode"]},
   "daily_limits":{"type":"object","properties":{k:{"type":"number","exclusiveMinimum":0} for k in DAILY}}}},
 "Nutrients":nut,
 "Label":{"type":"object","required":["id","name_th","category","form","serving_size","servings_per_pack","per_serving","ingredients_th"],"properties":{
   "id":{"type":"string"},"name_th":{"type":"string","minLength":1},"category":{"type":"string"},"form":{"enum":["drink","solid"]},
   "serving_size":{"type":"number","exclusiveMinimum":0},"servings_per_pack":{"type":"number","exclusiveMinimum":0},
   "per_serving":{"$ref":"#/$defs/Nutrients"},"price_thb":{"type":"number","minimum":0},"ingredients_th":{"type":"string"},
   "additives":{"type":"array","items":{"type":"string","pattern":"^E[0-9]{3,4}[a-z]?$"}},"barcode":{"type":"string"},
   "ocr_confidence":{"type":"number","minimum":0,"maximum":1}}},
 "PackTotals":nut,
 "SugarSpoons":{"type":"object","required":["sugar_g","tsp"],"properties":{"sugar_g":{"type":"number"},"tsp":{"type":"number","minimum":0}}},
 "Grade":{"type":"object","required":["score","grade","lights"],"properties":{"score":{"type":"integer","minimum":0,"maximum":100},
   "grade":{"enum":list("ABCDE")},"lights":{"type":"object","required":["sugar_g","fat_g","sodium_mg"],"properties":{k:light for k in ("sugar_g","fat_g","sodium_mg")}}}},
 "AllergenCheck":{"type":"object","required":["safe","hits"],"properties":{"safe":{"type":"boolean"},"hits":{"type":"array","items":{"type":"object","required":["allergen","matched"],"properties":{"allergen":{"type":"string"},"matched":{"type":"string"}}}}}},
 "Additive":{"type":"object","required":["code","name_th","level"],"properties":{"code":{"type":"string"},"name_th":{"type":"string"},"level":{"enum":["info","caution","unknown"]}}},
 "Battle":{"type":"object","required":["a","b","score_a","score_b","winner","sugar_diff_tsp","price_diff_thb"],"properties":{"a":{"type":"string"},"b":{"type":"string"},
   "score_a":{"type":"integer"},"score_b":{"type":"integer"},"winner":{"type":"string"},"sugar_diff_tsp":{"type":"number","minimum":0},"price_diff_thb":{"type":"number","minimum":0}}},
 "Swap":{"type":["object","null"],"required":["from","to","score_gain","sugar_saved_tsp"],"properties":{"from":{"type":"string"},"to":{"type":"string"},"score_gain":{"type":"integer","exclusiveMinimum":0},"sugar_saved_tsp":{"type":"number"}}},
 "BudgetDay":{"type":"object","required":["totals","pct","over","sugar_tsp","items"],"properties":{"totals":nut,"pct":{"type":"object"},
   "over":{"type":"array","items":{"enum":sorted(DAILY)}},"sugar_tsp":{"type":"number"},"items":{"type":"integer","minimum":0}}},
 "Streak":{"type":"object","required":["streak","badge"],"properties":{"streak":{"type":"integer","minimum":0},"badge":{"type":["string","null"]}}},
 "ReelCard":{"type":"object","required":["kind","title_th","big_stat","sub_th"],"properties":{"kind":{"enum":["sugar_spoons","battle","day_total","swap","streak"]},
   "title_th":{"type":"string"},"big_stat":{"type":"string"},"sub_th":{"type":"string"},"disclaimer_th":{"type":"string"}}},
}
schema = {"$schema":S,"$id":"labellens.schemas.json","title":"LabelLens schemas","$defs":defs}
T = lambda l: pack_totals(l)
DIS = "ข้อมูลสมมติ ประมาณการจากฉลาก ไม่ใช่คำแนะนำทางการแพทย์"
ex = {
 "UserProfile":[USER,{"name":"แม่ต้น","allergies":["peanut"],"goal":"kid_mode","daily_limits":{"sugar_g":16}}],
 "Nutrients":[l["per_serving"] for l in CANDIDATES],
 "Label":CANDIDATES,
 "PackTotals":[T(l) for l in CANDIDATES],
 "SugarSpoons":[{"sugar_g":T(l)["sugar_g"],"tsp":sugar_spoons(T(l)["sugar_g"])} for l in CANDIDATES],
 "Grade":[grade(l) for l in CANDIDATES],
 "AllergenCheck":[allergen_hits(l["ingredients_th"],USER["allergies"]) for l in (CHIPS,NOODLE,GREENTEA0)],
 "Additive":decode_additives(["621","E951","ins 102","E999","E955"]),
 "Battle":[battle(GREENTEA,GREENTEA0),battle(CHIPS,NOODLE),battle(GREENTEA_LITE,GREENTEA_LITE)],
 "Swap":[swap_suggest(GREENTEA,CANDIDATES),swap_suggest(GREENTEA0,CANDIDATES)],
 "BudgetDay":[budget_day(DAY),budget_day([])],
 "Streak":[week_streak(WEEK),week_streak([])],
 "ReelCard":[
  {"kind":"sugar_spoons","title_th":"ชาเขียว 1 ขวด = น้ำตาล 10 ช้อนชา","big_stat":"10 ช้อน","sub_th":"เกินโควตาทั้งวัน 167%","disclaimer_th":DIS},
  {"kind":"battle","title_th":"หวาน vs ไม่หวาน ราคาเท่ากัน","big_stat":"50 vs 100","sub_th":"ต่างกัน 10 ช้อนชา จ่ายเท่าเดิม","disclaimer_th":DIS},
  {"kind":"day_total","title_th":"ของว่างวันนี้ 3 อย่าง","big_stat":"15 ช้อน","sub_th":"น้ำตาล 250% ของทั้งวัน","disclaimer_th":DIS},
  {"kind":"swap","title_th":"สลับขวดเดียว","big_stat":"-10 ช้อน","sub_th":"คะแนน +50","disclaimer_th":DIS},
  {"kind":"streak","title_th":"หวานน้อยติดกัน","big_stat":"6 วัน","sub_th":"อีก 1 วันได้ badge 7 วัน","disclaimer_th":DIS}],
}
for k,v in ex.items():
    for o in v: jsonschema.validate(o,{"$schema":S,"$defs":defs,"$ref":f"#/$defs/{k}"})
d=os.path.dirname(os.path.abspath(__file__))+"/.."
json.dump(schema,open(d+"/schemas.json","w"),ensure_ascii=False,indent=1)
json.dump(ex,open(d+"/examples.json","w"),ensure_ascii=False,indent=1)
print(len(defs),"defs,",sum(map(len,ex.values())),"examples valid")
