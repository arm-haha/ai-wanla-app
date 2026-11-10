"""Generate ../schemas.json + ../examples.json and validate every example."""
import json, os, jsonschema
from parkpin import *
from fixtures import *

S="https://json-schema.org/draft/2020-12/schema"
s={"type":"string"}; b={"type":"boolean"}; n0={"type":"number","minimum":0}
u={"type":"number","minimum":0,"maximum":1}; i0={"type":"integer","minimum":0}; i1={"type":"integer","minimum":1}
pct={"type":"integer","minimum":0,"maximum":100}
mall={"enum":list(MALLS)}; fl={"enum":FLOOR_KINDS}; col={"enum":COLORS}

def obj(req, props, **kw):
    return {"type":"object","required":req,"properties":props,"additionalProperties":False, **kw}
def arr(i, **kw):
    return {"type":"array","items":i, **kw}

defs = {
 "Person": obj(["id","name_th","age"], {
    "id":{"type":"string","pattern":"^u[0-9]{2}$"},"name_th":s,"name_en":s,"age":i1,"city_th":s,"goal_th":s}),
 "PinPhoto": obj(["id","px_w","px_h","mall_id","floor","zone","color","pillar","glare","blur","tilt","sign_fill","confidence","has_plate"], {
    "id":{"type":"string","pattern":"^p[0-9]{2}$"},"px_w":i1,"px_h":i1,"mall_id":mall,"floor":fl,"zone":s,
    "color":col,"pillar":s,"glare":u,"blur":u,"tilt":u,"sign_fill":u,"confidence":u,"has_plate":b}),
 "ScanQuality": obj(["score","ok","tips_th"], {"score":pct,"ok":b,"tips_th":arr(s)}),
 "PinScan": obj(["photo_id","mall_id","mall_th","floor","zone","color","color_th","pillar","quality","ok","uncertain","message_th","has_plate","disclaimer_th"], {
    "photo_id":s,"mall_id":mall,"mall_th":s,"floor":fl,"zone":s,"color":col,"color_th":s,"pillar":s,
    "quality":{"$ref":"#/$defs/ScanQuality"},"ok":b,"uncertain":b,"message_th":s,"has_plate":b,"disclaimer_th":s}),
 "Pipeline": obj(["photo_id","steps"], {"photo_id":s,"steps":arr(s,minItems=1)}),
 "MallInfo": obj(["id","name_th","close_hhmm","grace_min","per_hour_thb","cap_thb","lost_ticket_thb","landmarks_th"], {
    "id":{"type":"string","pattern":"^m[0-9]{2}$"},"name_th":s,"close_hhmm":s,"grace_min":i0,"per_hour_thb":i0,
    "cap_thb":i0,"lost_ticket_thb":i0,"landmarks_th":arr(s)}),
 "FeeEstimate": obj(["mall_id","mall_th","minutes","hours_billed","fee_thb","cap_thb","per_hour_thb","grace_min","next_jump_min","next_fee_thb","lost_ticket_thb","disclaimer_th"], {
    "mall_id":mall,"mall_th":s,"minutes":i0,"hours_billed":i0,"fee_thb":i0,"cap_thb":i0,"per_hour_thb":i0,
    "grace_min":i0,"next_jump_min":{"type":["integer","null"],"minimum":0},"next_fee_thb":i0,"lost_ticket_thb":i0,"disclaimer_th":s}),
 "CloseReminder": obj(["mall_id","close_hhmm","minutes_left","status","message_th","disclaimer_th"], {
    "mall_id":mall,"close_hhmm":s,"minutes_left":{"type":"integer"},"status":{"enum":["ok","soon","after_close"]},
    "message_th":s,"disclaimer_th":s}),
 "WalkStep": obj(["n","text_th"], {"n":i1,"text_th":s}),
 "WalkbackGuide": obj(["mall_th","floor","zone","color","color_th","pillar","steps","disclaimer_th"], {
    "mall_th":s,"floor":fl,"zone":s,"color":col,"color_th":s,"pillar":s,
    "steps":arr({"$ref":"#/$defs/WalkStep"},minItems=1),"disclaimer_th":s}),
 "SavedPin": obj(["id","person_id","photo_id","mall_id","mall_th","floor","zone","color","pillar","parked_at","hint_th","needs_plate_blur","on_device"], {
    "id":s,"person_id":s,"photo_id":s,"mall_id":mall,"mall_th":s,"floor":fl,"zone":s,"color":col,"pillar":s,
    "parked_at":s,"hint_th":s,"needs_plate_blur":b,"on_device":b}),
 "LostCar": obj(["pin_id","mall_th","floor","zone","pillar","minutes","fee_thb","walkback","message_th","disclaimer_th"], {
    "pin_id":s,"mall_th":s,"floor":fl,"zone":s,"pillar":s,"minutes":i0,"fee_thb":i0,
    "walkback":{"$ref":"#/$defs/WalkbackGuide"},"message_th":s,"disclaimer_th":s}),
 "FamilyShare": obj(["title_th","name_th","mall_th","floor","zone","pillar","minutes","fee_thb","steps_count","note_th","line_share_url","disclaimer_th"], {
    "title_th":s,"name_th":s,"mall_th":s,"floor":fl,"zone":s,"pillar":s,"minutes":i0,"fee_thb":i0,
    "steps_count":i1,"note_th":s,"line_share_url":{"type":"string","pattern":"^https://line\\.me/R/share\\?text="},"disclaimer_th":s}),
 "HistoryStats": obj(["count","malls","last_parked_at","top_mall"], {
    "count":i0,"malls":i0,"last_parked_at":{"type":["string","null"]},"top_mall":{"type":["string","null"]}}),
 "ShareCard": obj(["title_th","headline_th","hook_th","floor","layout","sizes","watermark","cta_th"], {
    "title_th":s,"headline_th":s,"hook_th":s,"floor":fl,"layout":{"enum":["pin_card"]},
    "sizes":arr({"enum":["1080x1350","1080x1920","1080x1080"]}),"watermark":s,"cta_th":s}),
 "Quota": obj(["allowed","left_after","paywall"], {"allowed":i0,"left_after":{"type":["integer","null"],"minimum":0},"paywall":b}),
 "SafetyGuard": obj(["level","message_th"], {"level":{"enum":["ok","warn"]},"message_th":s}),
}
schema={"$schema":S,"$id":"https://example.com/parkpin.schema.json","title":"ParkPin","$defs":defs}

def ref(n):
    return {"$ref":f"#/$defs/{n}","$defs":defs}

ex=[]
def add(n,v,note=""):
    ex.append({"def":n,"note":note,"value":v})

for p in PEOPLE:
    add("Person", p, p["name_th"])
for ph in PHOTOS:
    add("PinPhoto", ph, ph["id"])
    add("PinScan", pin_scan(ph), ph["id"])
    add("Pipeline", {"photo_id":ph["id"],"steps":pipeline_steps(ph)}, ph["id"])
for mid in MALLS:
    add("MallInfo", mall_info(mid), mid)

fee_jay = fee_estimate("fictomall_bangna", PARKED, NOW)
add("FeeEstimate", fee_jay, "jay 2h30")
add("FeeEstimate", fee_estimate("fictomall_bangna", PARKED, "2026-11-17T14:30:00"), "grace")
add("FeeEstimate", fee_estimate("fictomall_bangna", "2026-11-17T00:00:00", "2026-11-17T20:00:00"), "cap")
add("FeeEstimate", fee_estimate("fictopark_airport", "2026-11-17T10:00:00", "2026-11-17T12:00:00"), "airport")
add("FeeEstimate", fee_estimate("fictoworld_chiangmai", "2026-11-17T14:00:00", "2026-11-17T14:20:00"), "cnx grace")
add("CloseReminder", close_reminder("fictomall_bangna", NOW), "ok")
add("CloseReminder", close_reminder("fictomall_bangna", "2026-11-17T21:40:00"), "soon")
add("CloseReminder", close_reminder("fictomall_bangna", "2026-11-17T22:10:00"), "after")
add("CloseReminder", close_reminder("fictoplex_siri", "2026-11-17T21:00:00"), "siri soon")

walk = walkback_guide(JAY_PHOTO, JAY_HINT)
add("WalkbackGuide", walk, "jay")
add("WalkbackGuide", walkback_guide(PHOTOS[1], "ใกล้ลิฟต์แก้ว"), "cnx")
pin = save_pin("pin01", "u01", JAY_PHOTO, PARKED, JAY_HINT)
add("SavedPin", pin, "jay")
add("SavedPin", save_pin("pin08", "u01", PHOTOS[7], PARKED, JAY_HINT), "plate flag")
add("LostCar", lost_car(pin, NOW, JAY_PHOTO), "jay")
add("FamilyShare", family_share(JAY, pin, fee_jay, walk, JAY_NOTE), "jay")
pins=[save_pin(*e[:2], e[2], e[3], e[4]) for e in HISTORY]
for p in pins:
    add("SavedPin", p, p["id"]+" hist")
add("HistoryStats", history_stats(pins), "jay hist")
add("HistoryStats", history_stats([]), "empty")
add("ShareCard", share_card(JAY["name_th"], pin, fee_jay), "jay")
add("Quota", quota(1,1), "free")
add("Quota", quota(3,1), "exhausted")
add("Quota", quota(0,5,pro=True), "pro")
add("SafetyGuard", safety_guard(False), "ok")
add("SafetyGuard", safety_guard(True), "plate")

for e in ex:
    jsonschema.validate(e["value"], ref(e["def"]))
d=os.path.dirname(os.path.abspath(__file__))+"/.."
json.dump(schema, open(d+"/schemas.json","w"), ensure_ascii=False, indent=1)
json.dump({"examples":ex}, open(d+"/examples.json","w"), ensure_ascii=False, indent=1)
print(len(defs),"defs,",len(ex),"examples, all valid")
