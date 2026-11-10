"""Generate ../schemas.json + ../examples.json and validate every example."""
import json, os, jsonschema
from fitdeck import *
from fixtures import *

S="https://json-schema.org/draft/2020-12/schema"
s={"type":"string"}; b={"type":"boolean"}; u={"type":"number","minimum":0,"maximum":1}
n0={"type":"number","minimum":0}; i0={"type":"integer","minimum":0}; i1={"type":"integer","minimum":1}
pct={"type":"integer","minimum":0,"maximum":100}
def obj(req, props, **kw):
    return {"type":"object","required":req,"properties":props,"additionalProperties":False, **kw}
def arr(i, **kw):
    return {"type":"array","items":i, **kw}

defs = {
 "Person": obj(["id","name_th","age"], {"id":{"type":"string","pattern":"^u[0-9]{2}$"},"name_th":s,"name_en":s,"age":i1,"city_th":s,"goal_th":s}),
 "Detection": obj(["key","value","confidence"], {"key":s,"value":True,"confidence":u}),
 "GearPhoto": obj(["id","px_w","px_h","glare","blur","crop","detections"], {"id":{"type":"string","pattern":"^s[0-9]{2}$"},"px_w":i1,"px_h":i1,"glare":u,"blur":u,"crop":u,"detections":arr({"$ref":"#/$defs/Detection"})}),
 "ScanQuality": obj(["score","ok","tips_th"], {"score":pct,"ok":b,"tips_th":arr(s)}),
 "GearScan": obj(["shot_id","quality","ok","keys","weight_kg","count","message_th"], {"shot_id":s,"quality":{"$ref":"#/$defs/ScanQuality"},"ok":b,"keys":arr(s),"weight_kg":{"type":["number","null"],"minimum":0},"count":i0,"message_th":s}),
 "Move": obj(["n","key","id","name_th","sec","minutes","muscles","safety_th","need"], {"n":i1,"key":s,"id":s,"name_th":s,"sec":i1,"minutes":n0,"muscles":arr(s),"safety_th":s,"need":arr(s)}),
 "Plan": obj(["level","keys","weight_kg","moves","count","total_sec","total_min","headline_th","disclaimer_th"], {"level":{"enum":["beginner","intermediate"]},"keys":arr(s),"weight_kg":{"type":["number","null"]},"moves":arr({"$ref":"#/$defs/Move"}),"count":i0,"total_sec":i0,"total_min":n0,"headline_th":s,"disclaimer_th":s}),
 "TimerCard": obj(["n","key","name_th","sec","start_sec","end_sec","safety_th","cue_th"], {"n":i1,"key":s,"name_th":s,"sec":i1,"start_sec":i0,"end_sec":i1,"safety_th":s,"cue_th":s}),
 "TimerDeck": obj(["cards","count","total_sec","headline_th"], {"cards":arr({"$ref":"#/$defs/TimerCard"}),"count":i0,"total_sec":i0,"headline_th":s}),
 "LogRow": obj(["date","level","planned","completed","total_sec","feeling","stopped"], {"date":s,"level":s,"planned":i1,"completed":i0,"total_sec":i0,"feeling":{"enum":["easy","ok","hard","stop"]},"stopped":b}),
 "SessionLog": obj(["rows","count","finished_sessions","headline_th"], {"rows":arr({"$ref":"#/$defs/LogRow"}),"count":i0,"finished_sessions":i0,"headline_th":s}),
 "ShareCard": obj(["title_th","headline_th","hook_th","total_min","count","level","layout","sizes","watermark","cta_th"], {"title_th":s,"headline_th":s,"hook_th":s,"total_min":n0,"count":i1,"level":s,"layout":{"enum":["fit_card"]},"sizes":arr({"enum":["1080x1350","1080x1920","1080x1080"]}),"watermark":s,"cta_th":s}),
 "Quota": obj(["allowed","left_after","paywall"], {"allowed":i0,"left_after":{"type":["integer","null"],"minimum":0},"paywall":b}),
 "SafetyGuard": obj(["level","message_th"], {"level":{"enum":["ok","warn","stop"]},"message_th":s}),
}
schema={"$schema":S,"$id":"https://example.com/fitdeck.schema.json","title":"FitDeck","$defs":defs}
def ref(n): return {"$ref":f"#/$defs/{n}","$defs":defs}
ex=[]; add=lambda n,v,note="": ex.append({"def":n,"note":note,"value":v})

for p in PEOPLE: add("Person", p, p["name_th"])
for sh in (GIFT_SHOT, BEE_SHOT, TON_SHOT, BAD_SHOT, EMPTY_SHOT, LOWCONF_SHOT):
    add("GearPhoto", sh, sh["id"])
    add("GearScan", parse_gear(sh), sh["id"])
    add("ScanQuality", scan_quality(sh["glare"], sh["blur"], sh["crop"], len(sh["detections"])), sh["id"])
    for d in sh["detections"][:2]:
        add("Detection", d, sh["id"]+" "+str(d["key"]))

gift=parse_gear(GIFT_SHOT)
for level, note, g in (("beginner","gift beg", gift), ("intermediate","gift int", gift),
                       ("beginner","bee", parse_gear(BEE_SHOT)), ("intermediate","ton", parse_gear(TON_SHOT)),
                       ("beginner","low", parse_gear(LOWCONF_SHOT))):
    plan=make_plan(g, level)
    add("Plan", plan, note)
    for m in plan["moves"]:
        add("Move", m, note+" "+m["key"])
    deck=timer_cards(plan)
    add("TimerDeck", deck, note)
    for c in deck["cards"][:4]:
        add("TimerCard", c, note+" t"+str(c["n"]))

plan=make_plan(gift,"beginner")
log=log_session([], TODAY, plan, 7, "ok")
add("SessionLog", log, "complete")
add("LogRow", log["rows"][0], "complete row")
log2=log_session(log["rows"], "2026-12-02", plan, 2, "stop")
add("SessionLog", log2, "then stop")
add("LogRow", log2["rows"][1], "stop row")
add("ShareCard", share_card("พี่กิ๊ฟ", plan), "gift")
add("Quota", quota(1,1), "free"); add("Quota", quota(3,1), "exh"); add("Quota", quota(0,5,pro=True), "pro")
add("SafetyGuard", safety_guard(), "ok")
add("SafetyGuard", safety_guard(pain=True), "pain")
add("SafetyGuard", safety_guard(dizzy=True), "dizzy")
add("SafetyGuard", safety_guard(cleared=False), "not cleared")

for e in ex:
    jsonschema.validate(e["value"], ref(e["def"]))
d=os.path.dirname(os.path.abspath(__file__))+"/.."
json.dump(schema, open(d+"/schemas.json","w"), ensure_ascii=False, indent=1)
json.dump({"examples": ex}, open(d+"/examples.json","w"), ensure_ascii=False, indent=1)
print(len(defs), "defs,", len(ex), "examples, all valid")
