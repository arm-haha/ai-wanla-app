"""Generate ../schemas.json + ../examples.json and validate every example."""
import json, os, jsonschema
from homeworkhero import *
from fixtures import *

S="https://json-schema.org/draft/2020-12/schema"
s={"type":"string"}; b={"type":"boolean"}; n={"type":"number"}; n0={"type":"number","minimum":0}
u={"type":"number","minimum":0,"maximum":1}; i0={"type":"integer","minimum":0}; i1={"type":"integer","minimum":1}
pct={"type":"integer","minimum":0,"maximum":100}
date={"type":"string","format":"date","pattern":"^[0-9]{4}-[0-9]{2}-[0-9]{2}$"}
tid={"enum":list(TEMPLATES)}; sub={"enum":SUBJECTS}; lev={"enum":LEVELS}

def obj(req, props, **kw):
    return {"type":"object","required":req,"properties":props,"additionalProperties":False, **kw}
def arr(i, **kw):
    return {"type":"array","items":i, **kw}

defs = {
 "Person": obj(["id","name_th","age","child_grade"], {
    "id":{"type":"string","pattern":"^u[0-9]{2}$"},"name_th":s,"name_en":s,"age":i1,"city_th":s,"goal_th":s,"child_grade":lev}),
 "HomeworkPhoto": obj(["id","px_w","px_h","glare","blur","tilt","text_fill","template","confidence","fields"], {
    "id":{"type":"string","pattern":"^p[0-9]{2}$"},"px_w":i1,"px_h":i1,"glare":u,"blur":u,"tilt":u,"text_fill":u,
    "template":tid,"confidence":u,"fields":{"type":"object"}}),
 "ScanQuality": obj(["score","ok","tips_th"], {"score":pct,"ok":b,"tips_th":arr(s)}),
 "HomeworkScan": obj(["photo_id","quality","template","name_th","subject","subject_th","level","level_th","skill_th","fields","ok","uncertain","message_th","disclaimer_th"], {
    "photo_id":s,"quality":{"$ref":"#/$defs/ScanQuality"},"template":tid,"name_th":s,"subject":sub,"subject_th":s,
    "level":lev,"level_th":s,"skill_th":s,"fields":{"type":"object"},"ok":b,"uncertain":b,"message_th":s,"disclaimer_th":s}),
 "Pipeline": obj(["photo_id","steps"], {"photo_id":s,"steps":arr(s,minItems=1)}),
 "TemplateInfo": obj(["id","template","name_th","subject","subject_th","level","level_th","skill_th","fields"], {
    "id":{"type":"string","pattern":"^t[0-9]{2}$"},"template":tid,"name_th":s,"subject":sub,"subject_th":s,
    "level":lev,"level_th":s,"skill_th":s,"fields":arr(s)}),
 "LevelInfo": obj(["level","level_th"], {"level":lev,"level_th":s}),
 "Hint": obj(["n","text_th","reveals_answer"], {"n":i1,"text_th":s,"reveals_answer":b}),
 "StepHints": obj(["template","upto","hints","disclaimer_th"], {
    "template":tid,"upto":{"enum":[1,2,3]},"hints":arr({"$ref":"#/$defs/Hint"},minItems=1),"disclaimer_th":s}),
 "ParentScript": obj(["template","title_th","intro_th","steps","mistakes_th","disclaimer_th"], {
    "template":tid,"title_th":s,"intro_th":s,
    "steps":arr(obj(["n","text_th"],{"n":i1,"text_th":s}),minItems=1),"mistakes_th":arr(s),"disclaimer_th":s}),
 "ParentReveal": obj(["template","gated","audience","answer","display_th","warning_th","disclaimer_th"], {
    "template":tid,"gated":{"const":True},"audience":{"const":"parent"},"answer":{"type":"object"},
    "display_th":s,"warning_th":s,"disclaimer_th":s}),
 "PracticeItem": obj(["n","fields","method_th","answer_key"], {
    "n":i1,"fields":{"type":"object"},"method_th":s,"answer_key":{"type":"object"}}),
 "SimilarPractice": obj(["template","count","items","note_th","disclaimer_th"], {
    "template":tid,"count":i1,"items":arr({"$ref":"#/$defs/PracticeItem"},minItems=1),"note_th":s,"disclaimer_th":s}),
 "CommonMistakes": obj(["template","mistakes_th"], {"template":tid,"mistakes_th":arr(s,minItems=1)}),
 "Timebox": obj(["minutes","used_minutes","left_minutes","hints_used","encourage_th"], {
    "minutes":i1,"used_minutes":i0,"left_minutes":i0,"hints_used":i0,"encourage_th":s}),
 "ProgressEntry": obj(["id","child_id","date","template","hints_used","minutes","self_solved","on_device"], {
    "id":s,"child_id":s,"date":date,"template":tid,"hints_used":i0,"minutes":i0,"self_solved":b,"on_device":b}),
 "ProgressStats": obj(["count","solved","avg_hints","avg_minutes","last_date","top_template"], {
    "count":i0,"solved":i0,"avg_hints":n0,"avg_minutes":n0,
    "last_date":{"type":["string","null"]},"top_template":{"type":["string","null"]}}),
 "TeacherNote": obj(["title_th","name_th","subject_th","level_th","topic_th","hints_used","note_th","line_share_url","disclaimer_th"], {
    "title_th":s,"name_th":s,"subject_th":s,"level_th":s,"topic_th":s,"hints_used":i0,"note_th":s,
    "line_share_url":{"type":"string","pattern":"^https://line\\.me/R/share\\?text="},"disclaimer_th":s}),
 "ShareCard": obj(["title_th","headline_th","hook_th","subject","level","layout","sizes","watermark","cta_th"], {
    "title_th":s,"headline_th":s,"hook_th":s,"subject":sub,"level":lev,"layout":{"enum":["hint_session"]},
    "sizes":arr({"enum":["1080x1350","1080x1920","1080x1080"]}),"watermark":s,"cta_th":s}),
 "Quota": obj(["allowed","left_after","paywall"], {"allowed":i0,"left_after":{"type":["integer","null"],"minimum":0},"paywall":b}),
 "SafetyGuard": obj(["level","message_th"], {"level":{"enum":["ok","warn"]},"message_th":s}),
}
schema={"$schema":S,"$id":"https://example.com/homeworkhero.schema.json","title":"HomeworkHero","$defs":defs}

def ref(n):
    return {"$ref":f"#/$defs/{n}","$defs":defs}

ex=[]
def add(n,v,note=""):
    ex.append({"def":n,"note":note,"value":v})

for p in PEOPLE:
    add("Person", p, p["name_th"])
for ph in PHOTOS:
    add("HomeworkPhoto", ph, ph["id"])
    add("HomeworkScan", homework_scan(ph), ph["id"])
    add("Pipeline", {"photo_id":ph["id"],"steps":pipeline_steps(ph)}, ph["id"])
for tid_ in TEMPLATES:
    add("TemplateInfo", template_info(tid_), tid_)
for lv in level_catalog():
    add("LevelInfo", lv, lv["level"])

add("StepHints", step_hints("percent_discount", NOON_FIELDS, 1), "noon 1")
add("StepHints", step_hints("percent_discount", NOON_FIELDS, 2), "noon 2")
add("StepHints", step_hints("percent_discount", NOON_FIELDS, 3), "noon 3")
for ph in PHOTOS[1:6]:
    add("StepHints", step_hints(ph["template"], ph["fields"], 3), ph["id"])
add("StepHints", step_hints("decimal_add", PHOTOS[7]["fields"], 3), "p08")

for ph in [NOON_PHOTO, PHOTOS[1], PHOTOS[3], PHOTOS[4]]:
    add("ParentScript", parent_script(ph["template"], ph["fields"]), ph["id"])
    add("ParentReveal", parent_reveal(ph["template"], ph["fields"]), ph["id"])
add("ParentReveal", parent_reveal("fraction_of", PHOTOS[2]["fields"]), "fraction")
add("ParentReveal", parent_reveal("water_cycle", PHOTOS[5]["fields"]), "cycle")

for tid_ in ("percent_discount","area_rect","linear_eq","eng_tense","average"):
    add("SimilarPractice", similar_practice(tid_, 0, 3), tid_)
for tid_ in TEMPLATES:
    add("CommonMistakes", common_mistakes(tid_), tid_)

add("Timebox", timebox(20,7,1), "noon mid")
add("Timebox", timebox(20,5,2), "more hints")
add("Timebox", timebox(20,20,3), "done")
entries=[progress_entry(*e) for e in PROGRESS]
for e in entries:
    add("ProgressEntry", e, e["id"])
add("ProgressStats", progress_stats(entries), "noon")
add("ProgressStats", progress_stats([]), "empty")
add("TeacherNote", teacher_note(NOON, homework_scan(NOON_PHOTO), 2, NOON_NOTE), "noon")
add("ShareCard", share_card(NOON["name_th"], homework_scan(NOON_PHOTO)), "noon")
add("Quota", quota(1,1), "free")
add("Quota", quota(3,1), "exhausted")
add("Quota", quota(0,5,pro=True), "pro")
add("SafetyGuard", safety_guard(False), "ok")
add("SafetyGuard", safety_guard(True), "warn")

for e in ex:
    jsonschema.validate(e["value"], ref(e["def"]))
d=os.path.dirname(os.path.abspath(__file__))+"/.."
json.dump(schema, open(d+"/schemas.json","w"), ensure_ascii=False, indent=1)
json.dump({"examples":ex}, open(d+"/examples.json","w"), ensure_ascii=False, indent=1)
print(len(defs),"defs,",len(ex),"examples, all valid")
