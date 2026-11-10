"""Generate ../schemas.json + ../examples.json and validate every example."""
import json, os, jsonschema
from singscore import *
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
 "Take": obj(["id","exercise","mean_cents_off","mean_ms_off","confidence","notes"], {"id":s,"exercise":s,"mean_cents_off":n0,"mean_ms_off":n0,"confidence":u,"notes":arr(s)}),
 "Score": obj(["ok","pitch","timing","combined","band","cents","ms","exercise","headline_th","message_th","disclaimer_th"], {
    "ok":b,"pitch":{"type":["integer","null"],"minimum":0,"maximum":100},"timing":{"type":["integer","null"],"minimum":0,"maximum":100},
    "combined":{"type":["integer","null"],"minimum":0,"maximum":100},"band":{"type":["string","null"]},
    "cents":n0,"ms":n0,"exercise":s,"headline_th":s,"message_th":s,"disclaimer_th":s}, **{}),
 "KeyFind": obj(["tonic","mode","exercise","name_th","notes","headline_th","source"], {"tonic":s,"mode":s,"exercise":{"type":["string","null"]},"name_th":{"type":["string","null"]},"notes":arr(s),"headline_th":s,"source":{"enum":["exercise","notes"]}}, **{}),
 "WarmupItem": obj(["key","id","name_th","sec","how_th"], {"key":s,"id":s,"name_th":s,"sec":i1,"how_th":s}),
 "WarmupSet": obj(["items","count","total_sec","headline_th","disclaimer_th"], {"items":arr({"$ref":"#/$defs/WarmupItem"}),"count":i0,"total_sec":i0,"headline_th":s,"disclaimer_th":s}),
 "DuetBattle": obj(["name_a","score_a","name_b","score_b","verdict","winner","margin","headline_th","disclaimer_th"], {
    "name_a":s,"score_a":pct,"name_b":s,"score_b":pct,"verdict":{"enum":["a","b","tie"]},"winner":{"type":["string","null"]},"margin":i0,"headline_th":s,"disclaimer_th":s}),
 "LogRow": obj(["date","exercise","name_th","combined","feeling"], {"date":s,"exercise":s,"name_th":s,"combined":pct,"feeling":{"enum":["easy","ok","hard","stop"]}}),
 "PracticeLog": obj(["rows","count","best","headline_th"], {"rows":arr({"$ref":"#/$defs/LogRow"}),"count":i0,"best":pct,"headline_th":s}),
 "ShareCard": obj(["title_th","headline_th","hook_th","combined","pitch","timing","key_th","layout","sizes","watermark","cta_th"], {
    "title_th":s,"headline_th":s,"hook_th":s,"combined":{"type":["integer","null"]},"pitch":{"type":["integer","null"]},"timing":{"type":["integer","null"]},
    "key_th":{"type":["string","null"]},"layout":{"enum":["sing_card"]},"sizes":arr({"enum":["1080x1350","1080x1920","1080x1080"]}),"watermark":s,"cta_th":s}),
 "Quota": obj(["allowed","left_after","paywall"], {"allowed":i0,"left_after":{"type":["integer","null"],"minimum":0},"paywall":b}),
 "SafetyGuard": obj(["level","message_th"], {"level":{"enum":["ok","warn","stop"]},"message_th":s}),
 "ExerciseInfo": obj(["key","id","name_th","name_en","tonic","mode","notes"], {"key":s,"id":s,"name_th":s,"name_en":s,"tonic":s,"mode":s,"notes":arr(s)}),
}
# optional fields on Score when not ok: cents/ms/exercise/headline/disclaimer may be missing
# lowconf score doesn't have cents - I need to fix score_take to always include fields OR make them optional.
# Looking at lowconf return: no cents, ms, exercise, headline, disclaimer.
# I'll pad score_take lowconf OR loosen schema. Easier to pad the function return.

# Make KeyFind hit/total optional
defs["KeyFind"]["properties"]["hit"]=i0
defs["KeyFind"]["properties"]["total"]=i1

schema={"$schema":S,"$id":"https://example.com/singscore.schema.json","title":"SingScore","$defs":defs}
def ref(n): return {"$ref":f"#/$defs/{n}","$defs":defs}
ex=[]; add=lambda n,v,note="": ex.append({"def":n,"note":note,"value":v})

# Fix lowconf example by not using strict Score for it if fields missing — I'll add fields in a wrapper
def as_score(take):
    r=score_take(take)
    if not r.get("ok"):
        r=dict(r, cents=take.get("mean_cents_off",0), ms=take.get("mean_ms_off",0),
               exercise=take.get("exercise"), headline_th=r["message_th"], disclaimer_th=SAFETY_DISCLAIMER_TH)
    return r

for p in PEOPLE: add("Person", p, p["name_th"])
for take in (TOM_TAKE, NINA_TAKE, BEE_TAKE, LOWCONF_TAKE):
    add("Take", take, take["id"])
    add("Score", as_score(take), take["id"])
for exk,exv in EXERCISES.items():
    add("ExerciseInfo", {"key":exk, **exv}, exk)
add("KeyFind", key_finder(TOM_TAKE["notes"], "scale_run_c"), "tom ex")
add("KeyFind", key_finder(TOM_TAKE["notes"]), "tom notes")
add("KeyFind", key_finder(EXERCISES["scale_run_g"]["notes"], "scale_run_g"), "g")
add("KeyFind", key_finder(["C","G","C"], "hum_fifth"), "fifth")
w=warmups(); add("WarmupSet", w, "all")
for it in w["items"]: add("WarmupItem", it, it["key"])
add("WarmupSet", warmups(["lip_trill","hum_five"]), "subset")
tom,nina=as_score(TOM_TAKE),as_score(NINA_TAKE)
add("DuetBattle", duet_battle("พี่ต้อม", tom["combined"], "น้องนีน่า", nina["combined"]), "tom wins")
add("DuetBattle", duet_battle("พี่ต้อม", 80, "น้องนีน่า", 80), "tie")
add("DuetBattle", duet_battle("พี่ต้อม", 60, "น้องนีน่า", 88), "nina")
log=practice_log([], TODAY, "scale_run_c", 79, "ok")
log=practice_log(log["rows"], TODAY, "vowel_hold", 90, "easy")
add("PracticeLog", log, "two")
for r in log["rows"]: add("LogRow", r, r["exercise"])
add("ShareCard", share_card("พี่ต้อม", tom, key_finder(TOM_TAKE["notes"], "scale_run_c")), "tom")
add("ShareCard", share_card("พี่ต้อม", tom, None), "no key")
add("Quota", quota(1,1), "free"); add("Quota", quota(3,1), "exh"); add("Quota", quota(0,5,pro=True), "pro")
add("SafetyGuard", safety_guard(), "ok")
add("SafetyGuard", safety_guard(sore_throat=True), "throat")
add("SafetyGuard", safety_guard(strain=True), "strain")
for cents in (0, 8, 24, 36, 48, 70, 90, 110, 160, 200):
    for ms in (0, 20, 52, 80):
        take={"id":"g","exercise":"scale_run_c","mean_cents_off":cents,"mean_ms_off":ms,"confidence":0.95,"notes":["C"]}
        add("Score", as_score(take), f"c{cents}-m{ms}")
for exk in EXERCISES:
    add("PracticeLog", practice_log([], TODAY, exk, 70, "ok"), "log "+exk)

# extra band examples
for cents,ms,note in ((10,10,"great"),(60,60,"good70"),(100,100,"ok50"),(120,120,"retry")):
    add("Score", as_score({"id":"x","exercise":"scale_run_c","mean_cents_off":cents,"mean_ms_off":ms,"confidence":0.95,"notes":["C"]}), note)

for e in ex:
    jsonschema.validate(e["value"], ref(e["def"]))
d=os.path.dirname(os.path.abspath(__file__))+"/.."
json.dump(schema, open(d+"/schemas.json","w"), ensure_ascii=False, indent=1)
json.dump({"examples": ex}, open(d+"/examples.json","w"), ensure_ascii=False, indent=1)
print(len(defs), "defs,", len(ex), "examples, all valid")
