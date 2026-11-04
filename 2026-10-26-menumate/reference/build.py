"""Generate schemas.json + examples.json and validate every example."""
import json, os, jsonschema
from menumate import *
from fixtures import *
S = "https://json-schema.org/draft/2020-12/schema"
lvl = {"enum": ["safe","warn","avoid"]}
defs = {
 "UserPrefs": {"type":"object","required":["allergies","diets","spice_tolerance","home_currency"],"properties":{
   "allergies":{"type":"array","items":{"enum":["shrimp","crab","shellfish","peanut","tree_nut","egg","milk","soy","wheat","fish","sesame"]}},
   "diets":{"type":"array","items":{"enum":list(DIET_RULES)}},
   "spice_tolerance":{"type":"integer","minimum":0,"maximum":3},
   "home_currency":{"const":"THB"},"ui_lang":{"enum":["th","en"]}}},
 "ExchangeRate": {"type":"object","required":["currency","thb_per_unit","source","updated_at"],"properties":{
   "currency":{"enum":["JPY","KRW","CNY","TWD","HKD","SGD","VND","USD","EUR"]},
   "thb_per_unit":{"type":"number","exclusiveMinimum":0},
   "source":{"enum":["user_set","api"]},"updated_at":{"type":"string","format":"date-time"}}},
 "MenuItem": {"type":"object","required":["id","original_name","thai_name","price","category","spice_level","ingredients","allergens","must_try","confidence"],"properties":{
   "id":{"type":"string"},"original_name":{"type":"string","minLength":1},"romanized":{"type":"string"},
   "thai_name":{"type":"string"},"thai_desc":{"type":"string"},
   "price":{"type":"number","minimum":0},"category":{"enum":["main","side","drink","dessert","set"]},
   "spice_level":{"type":"integer","minimum":0,"maximum":3},
   "ingredients":{"type":"array","items":{"type":"string"}},
   "allergens":{"type":"array","items":{"type":"string"}},
   "must_try":{"type":"integer","minimum":0,"maximum":100},
   "emoji":{"type":"string"},"confidence":{"type":"number","minimum":0,"maximum":1},
   "bbox":{"type":"array","items":{"type":"number"},"minItems":4,"maxItems":4}}},
 "MenuScan": {"type":"object","required":["scan_id","lang","currency","items"],"properties":{
   "scan_id":{"type":"string"},"lang":{"enum":["ja","ko","zh","en","vi"]},
   "currency":{"$ref":"#/$defs/ExchangeRate/properties/currency"},
   "shop_name_local":{"type":["string","null"]},"city":{"type":["string","null"]},
   "items":{"type":"array","minItems":1,"items":{"$ref":"#/$defs/MenuItem"}},
   "unreadable_regions":{"type":"integer","minimum":0}}},
 "ItemFlag": {"type":"object","required":["level","reasons"],"properties":{"level":lvl,"reasons":{"type":"array","items":{"type":"string"}}}},
 "OrderPlan": {"type":"object","required":["budget_local","party_size","pick_ids","total_local","left_local","per_person_local","mains_covered"],"properties":{
   "budget_local":{"type":"number","minimum":0},"party_size":{"type":"integer","minimum":1},
   "pick_ids":{"type":"array","items":{"type":"string"}},"total_local":{"type":"number"},
   "left_local":{"type":"number","minimum":0},"per_person_local":{"type":"number"},"mains_covered":{"type":"boolean"}}},
 "PointCard": {"type":"object","required":["lang","header","lines","footer"],"properties":{
   "lang":{"type":"string"},"header":{"type":"string"},"note_local":{"type":["string","null"]},"footer":{"type":"string"},
   "lines":{"type":"array","items":{"type":"object","required":["original_name","qty","line"],"properties":{
     "original_name":{"type":"string"},"qty":{"type":"integer","minimum":1},"line":{"type":"string"}}}}}},
 "AllergyCard": {"type":"object","required":["lang","text_local","text_th","allergens"],"properties":{
   "lang":{"type":"string"},"text_local":{"type":"string"},"text_th":{"type":"string"},"allergens":{"type":"array","items":{"type":"string"}}}},
 "ReceiptLine": {"type":"object","required":["name","amount"],"properties":{"name":{"type":"string"},"amount":{"type":"number"}}},
 "BillCheck": {"type":"object","required":["expected_total","receipt_total","gap","extra_lines","missing_lines","price_mismatch","ok"],"properties":{
   "expected_total":{"type":"number"},"receipt_total":{"type":"number"},"gap":{"type":"number"},
   "extra_lines":{"type":"array","items":{"type":"string"}},"missing_lines":{"type":"array","items":{"type":"string"}},
   "price_mismatch":{"type":"array","items":{"type":"string"}},"ok":{"type":"boolean"}}},
 "SplitResult": {"type":"object","required":["per_person_local","per_person_thb"],"properties":{"per_person_local":{"type":"number"},"per_person_thb":{"type":"integer"}}},
 "Phrase": {"type":"object","required":["id","situation_th","text_local","romanized"],"properties":{
   "id":{"type":"string"},"situation_th":{"type":"string"},"text_local":{"type":"string"},"romanized":{"type":"string"},"lang":{"type":"string"}}},
 "TripWrapped": {"type":"object","required":["meals","dishes_tried","allergy_dodged","spent_local","spent_thb","biggest_meal_city"],"properties":{
   "meals":{"type":"integer"},"dishes_tried":{"type":"integer"},"allergy_dodged":{"type":"integer"},
   "spent_local":{"type":"number"},"spent_thb":{"type":"integer"},"biggest_meal_city":{"type":["string","null"]}}},
 "ReelCard": {"type":"object","required":["kind","title_th","before","after"],"properties":{
   "kind":{"enum":["menu_flip","order_win","bill_catch","wrapped"]},"title_th":{"type":"string"},
   "before":{"type":"string"},"after":{"type":"string"},"stat":{"type":"string"}}},
}
schema = {"$schema":S,"$id":"menumate.schemas.json","title":"MenuMate schemas","$defs":defs}
order = build_order(MENU, BUDGET, PARTY, PREFS)
picked = [i for i in MENU if i["id"] in order["pick_ids"]]
ex = {
 "UserPrefs":[{**PREFS,"home_currency":"THB","ui_lang":"th"}],
 "ExchangeRate":[{"currency":"JPY","thb_per_unit":RATE,"source":"user_set","updated_at":"2026-10-26T08:00:00+07:00"}],
 "MenuItem":MENU,
 "MenuScan":[{"scan_id":"scan_osaka_01","lang":"ja","currency":"JPY","shop_name_local":"らーめん 例屋","city":"Osaka","items":MENU,"unreadable_regions":1}],
 "ItemFlag":[flag_item(i, PREFS) for i in MENU],
 "OrderPlan":[order, build_order(MENU,1000,2,PREFS)],
 "PointCard":[point_card(MENU, order, "ja", "エビアレルギーがあります")],
 "AllergyCard":[{"lang":"ja","text_local":"私はエビアレルギーです。エビが入っていない料理を教えてください。","text_th":"ฉันแพ้กุ้ง ช่วยบอกเมนูที่ไม่มีกุ้งให้หน่อย","allergens":["shrimp"]}],
 "ReceiptLine":RECEIPT,
 "BillCheck":[bill_check(picked, RECEIPT)],
 "SplitResult":[split_even(order["total_local"], PARTY, RATE)],
 "Phrase":[
  {"id":"p1","situation_th":"ขอน้ำเปล่า","text_local":"お水をください","romanized":"omizu o kudasai","lang":"ja"},
  {"id":"p2","situation_th":"ไม่เผ็ดได้ไหม","text_local":"辛くしないでください","romanized":"karaku shinaide kudasai","lang":"ja"},
  {"id":"p3","situation_th":"เช็กบิล","text_local":"お会計お願いします","romanized":"okaikei onegaishimasu","lang":"ja"},
  {"id":"p4","situation_th":"รับบัตรไหม","text_local":"カードは使えますか","romanized":"kādo wa tsukaemasu ka","lang":"ja"}],
 "TripWrapped":[trip_wrapped(MEALS, RATE)],
 "ReelCard":[
  {"kind":"menu_flip","title_th":"เมนูญี่ปุ่นล้วน → ไทยใน 3 วิ","before":"อ่านไม่ออกสักตัว","after":"8 เมนูภาษาไทย + ราคาบาท","stat":"8 เมนู"},
  {"kind":"order_win","title_th":"งบ ¥3,000 สองคน","before":"กลัวสั่งเกินงบ","after":f"สั่งได้ 4 อย่าง เหลือ ¥{order['left_local']}","stat":f"¥{order['total_local']} ≈ ฿{to_thb(order['total_local'],RATE)}"},
  {"kind":"bill_catch","title_th":"บิลเกินมา ¥200","before":"จ่ายไปแบบงงๆ","after":"เจอ ライス ที่ไม่ได้สั่ง","stat":"+¥200"},
  {"kind":"wrapped","title_th":"ทริปญี่ปุ่นกินอะไรไปบ้าง","before":"จำไม่ได้","after":"12 เมนู หลบกุ้งได้ 3 ครั้ง","stat":"฿2,054"}],
}
n=0
for k, arr in ex.items():
    sub = {"$schema":S,"$defs":defs,"$ref":f"#/$defs/{k}"}
    for o in arr: jsonschema.validate(o, sub); n+=1
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
json.dump(schema, open(f"{root}/schemas.json","w"), ensure_ascii=False, indent=2)
json.dump({"_note":"Example data (fictional shop, example exchange rate 0.23 THB/JPY). Generated by reference/build.py","examples":ex}, open(f"{root}/examples.json","w"), ensure_ascii=False, indent=2)
print(len(defs), "defs,", n, "examples valid; order", order)
