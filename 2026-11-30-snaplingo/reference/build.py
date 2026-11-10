"""Generate ../schemas.json + ../examples.json and validate every example."""
import json, os, jsonschema
from snaplingo import *
from fixtures import *

S="https://json-schema.org/draft/2020-12/schema"
s={"type":"string"}; b={"type":"boolean"}; u={"type":"number","minimum":0,"maximum":1}
i0={"type":"integer","minimum":0}; i1={"type":"integer","minimum":1}
pct={"type":"integer","minimum":0,"maximum":100}
def obj(req, props, **kw):
    return {"type":"object","required":req,"properties":props,"additionalProperties":False, **kw}
def arr(i, **kw):
    return {"type":"array","items":i, **kw}

defs = {
 "Person": obj(["id","name_th","age"], {"id":{"type":"string","pattern":"^u[0-9]{2}$"},"name_th":s,"name_en":s,"age":i1,"city_th":s,"role":s,"goal_th":s,"parent_id":s}),
 "Detection": obj(["key","value","confidence"], {"key":s,"value":True,"confidence":u}),
 "ScenePhoto": obj(["id","px_w","px_h","glare","blur","crop","detections"], {"id":{"type":"string","pattern":"^s[0-9]{2}$"},"px_w":i1,"px_h":i1,"glare":u,"blur":u,"crop":u,"detections":arr({"$ref":"#/$defs/Detection"})}),
 "ScanQuality": obj(["score","ok","tips_th"], {"score":pct,"ok":b,"tips_th":arr(s)}),
 "SceneScan": obj(["shot_id","quality","ok","keys","count","message_th"], {"shot_id":s,"quality":{"$ref":"#/$defs/ScanQuality"},"ok":b,"keys":arr(s),"count":i0,"message_th":s}),
 "LabelCard": obj(["key","id","name_th","name_en","ipa_en","th_en","name_zh","pinyin","th_zh","topic","headline_th","en_line_th","zh_line_th"], {
    "key":s,"id":s,"name_th":s,"name_en":s,"ipa_en":s,"th_en":s,"name_zh":s,"pinyin":s,"th_zh":s,"topic":s,"headline_th":s,"en_line_th":s,"zh_line_th":s}),
 "LabelSet": obj(["cards","count","headline_th"], {"cards":arr({"$ref":"#/$defs/LabelCard"}),"count":i0,"headline_th":s}),
 "FlashCard": obj(["key","lang","front_th","back","say_th"], {"key":s,"lang":{"enum":["en","zh"]},"front_th":s,"back":s,"say_th":s}),
 "FlashDeck": obj(["lang","cards","count"], {"lang":{"enum":["en","zh"]},"cards":arr({"$ref":"#/$defs/FlashCard"}),"count":i0}),
 "Choice": obj(["key","text","correct"], {"key":s,"text":s,"correct":b}),
 "QuizQuestion": obj(["n","key","prompt_th","choices","answer","correct"], {"n":i1,"key":s,"prompt_th":s,"choices":arr({"$ref":"#/$defs/Choice"}),"answer":{"type":["string","null"]},"correct":{"type":["boolean","null"]}}),
 "MiniQuiz": obj(["lang","questions","count","answered","right","score_pct","headline_th"], {"lang":{"enum":["en","zh"]},"questions":arr({"$ref":"#/$defs/QuizQuestion"}),"count":i1,"answered":i0,"right":i0,"score_pct":pct,"headline_th":s}),
 "Reward": obj(["at","key","name_th"], {"at":i1,"key":s,"name_th":s}),
 "Progress": obj(["date","passed","streak","prev_streak","score_pct","right","answered","rewards","reward_count","headline_th"], {
    "date":{"type":["string","null"]},"passed":b,"streak":i0,"prev_streak":i0,"score_pct":pct,"right":i0,"answered":i1,
    "rewards":arr({"$ref":"#/$defs/Reward"}),"reward_count":i0,"headline_th":s}),
 "ShareCard": obj(["title_th","headline_th","hook_th","parent_th","child_th","count","streak","layout","sizes","watermark","cta_th"], {
    "title_th":s,"headline_th":s,"hook_th":s,"parent_th":s,"child_th":s,"count":i0,"streak":i0,
    "layout":{"enum":["lingo_card"]},"sizes":arr({"enum":["1080x1350","1080x1920","1080x1080"]}),"watermark":s,"cta_th":s}),
 "Quota": obj(["allowed","left_after","paywall"], {"allowed":i0,"left_after":{"type":["integer","null"],"minimum":0},"paywall":b}),
 "SafetyGuard": obj(["level","message_th"], {"level":{"enum":["ok","warn","stop"]},"message_th":s}),
}
schema={"$schema":S,"$id":"https://example.com/snaplingo.schema.json","title":"SnapLingo","$defs":defs}
def ref(n): return {"$ref":f"#/$defs/{n}","$defs":defs}
ex=[]; add=lambda n,v,note="": ex.append({"def":n,"note":note,"value":v})

for p in PEOPLE: add("Person", p, p["name_th"])
for sh in (KITCHEN, ROOM, BAD_SHOT, EMPTY_SHOT, LOWCONF_SHOT):
    add("ScenePhoto", sh, sh["id"])
    add("SceneScan", parse_scene(sh), sh["id"])
    add("ScanQuality", scan_quality(sh["glare"], sh["blur"], sh["crop"], len(sh["detections"])), sh["id"])
    for d in sh["detections"][:2]:
        add("Detection", d, sh["id"]+" "+d["key"])

keys=parse_scene(KITCHEN)["keys"]
labs=labels(keys)
add("LabelSet", labs, "kitchen")
for c in labs["cards"]:
    add("LabelCard", c, c["key"])
for k in list(WORDS):
    if k not in keys:
        add("LabelCard", label_card(k), k)
for lang in ("en","zh"):
    deck=flashcards(keys, lang)
    add("FlashDeck", deck, lang)
    for c in deck["cards"]:
        add("FlashCard", c, lang+" "+c["key"])
q0=mini_quiz(keys,"en")
q1=mini_quiz(keys,"en", answers=["kettle","kettle","spoon"])
q2=mini_quiz(keys,"en", answers=["cup","cup","cup"])
q3=mini_quiz(["kettle"],"zh", answers=["kettle"])
for q,note in ((q0,"unanswered"),(q1,"tao 2/3"),(q2,"fail"),(q3,"zh one")):
    add("MiniQuiz", q, note)
    add("QuizQuestion", q["questions"][0], note+" q1")
    for ch in q["questions"][0]["choices"]:
        add("Choice", ch, note+" "+ch["key"])
p3=progress(2,q1,TODAY); p4=progress(3,q1,TODAY); pfail=progress(4,q2,TODAY)
add("Progress", p3, "star"); add("Progress", p4, "streak4"); add("Progress", pfail, "reset")
for p in (p3,):
    for r in p["rewards"]:
        add("Reward", r, r["key"])
add("Progress", progress(6,q1,TODAY), "sun")
add("Progress", progress(13,q1), "rainbow")
add("Progress", progress(29,q1), "trophy")
add("ShareCard", share_card("พี่แอน","น้องเต้า",labs,p4), "tao")
add("ShareCard", share_card("พี่แอน","น้องเต้า",labs,None), "no prog")
add("Quota", quota(1,1), "free"); add("Quota", quota(3,1), "exh"); add("Quota", quota(0,5,pro=True), "pro")
add("SafetyGuard", safety_guard(), "ok")
add("SafetyGuard", safety_guard(True, True), "warn")
add("SafetyGuard", safety_guard(True, False), "stop")
room=labels(parse_scene(ROOM)["keys"]); add("LabelSet", room, "room")
for lang in ("en","zh"):
    deck=flashcards(parse_scene(ROOM)["keys"], lang); add("FlashDeck", deck, "room "+lang)


for e in ex:
    jsonschema.validate(e["value"], ref(e["def"]))
d=os.path.dirname(os.path.abspath(__file__))+"/.."
json.dump(schema, open(d+"/schemas.json","w"), ensure_ascii=False, indent=1)
json.dump({"examples": ex}, open(d+"/examples.json","w"), ensure_ascii=False, indent=1)
print(len(defs), "defs,", len(ex), "examples, all valid")
