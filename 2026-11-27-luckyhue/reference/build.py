"""Generate ../schemas.json + ../examples.json and validate every example."""
import json, os, jsonschema
from luckyhue import *
from fixtures import *

S = "https://json-schema.org/draft/2020-12/schema"
s={"type":"string"}; b={"type":"boolean"}; u={"type":"number","minimum":0,"maximum":1}
n0={"type":"number","minimum":0}; i0={"type":"integer","minimum":0}; i1={"type":"integer","minimum":1}
pct={"type":"integer","minimum":0,"maximum":100}
def obj(req, props, **kw):
    return {"type":"object","required":req,"properties":props,"additionalProperties":False, **kw}
def arr(i, **kw):
    return {"type":"array","items":i, **kw}

defs = {
 "Person": obj(["id","name_th","age"], {"id":{"type":"string","pattern":"^u[0-9]{2}$"},"name_th":s,"name_en":s,"age":i1,"city_th":s,"birth_iso":s,"birth_weekday":{"type":["string","null"]},"goal_th":s}),
 "ClosetItem": obj(["id","name_th","category","color_key","color_th"], {"id":s,"name_th":s,"category":{"enum":CATEGORY_ORDER},"color_key":s,"color_th":s}),
 "ClosetPhoto": obj(["id","px_w","px_h","glare","blur","crop","items"], {"id":{"type":"string","pattern":"^s[0-9]{2}$"},"px_w":i1,"px_h":i1,"glare":u,"blur":u,"crop":u,"items":arr({"$ref":"#/$defs/ClosetItem"})}),
 "ScanQuality": obj(["score","ok","tips_th"], {"score":pct,"ok":b,"tips_th":arr(s)}),
 "ClosetScan": obj(["shot_id","quality","ok","items","count","message_th"], {"shot_id":s,"quality":{"$ref":"#/$defs/ScanQuality"},"ok":b,"items":arr({"$ref":"#/$defs/ClosetItem"}),"count":i0,"message_th":s}),
 "LuckyColor": obj(["weekday","name_th","color_th","color_en","hex","accent","is_birth_day","today_is_birth_day","night_mode","headline_th","blessing_th","disclaimer_th"], {
    "weekday":s,"name_th":s,"color_th":s,"color_en":s,"hex":s,"accent":s,"is_birth_day":b,
    "today_is_birth_day":{"type":["boolean","null"]},"night_mode":b,"headline_th":s,"blessing_th":s,"disclaimer_th":s}),
 "OutfitMix": obj(["items","count","lucky_n","neutral_n","other_n","score","verdict","headline_th","color_th","hex","disclaimer_th"], {
    "items":arr({"$ref":"#/$defs/ClosetItem"}),"count":i0,"lucky_n":i0,"neutral_n":i0,"other_n":i0,"score":pct,
    "verdict":{"enum":["match","clash","no_match"]},"headline_th":s,"color_th":s,"hex":s,"disclaimer_th":s}),
 "Wallpaper": obj(["size","weekday","color_th","hex","palette","blessing_th","title_th","watermark","disclaimer_th"], {
    "size":{"enum":["1080x1920","1080x1080","1170x2532"]},"weekday":s,"color_th":s,"hex":s,"palette":arr(s),"blessing_th":s,"title_th":s,"watermark":s,"disclaimer_th":s}),
 "CalendarDay": obj(["iso","weekday","name_th","color_th","hex","is_birth_day"], {"iso":s,"weekday":s,"name_th":s,"color_th":s,"hex":s,"is_birth_day":b}),
 "WeeklyCalendar": obj(["start_iso","birth_weekday","days","count","headline_th","disclaimer_th"], {"start_iso":s,"birth_weekday":s,"days":arr({"$ref":"#/$defs/CalendarDay"}),"count":i1,"headline_th":s,"disclaimer_th":s}),
 "ShareCard": obj(["title_th","headline_th","hook_th","color_th","hex","outfit_score","layout","sizes","watermark","cta_th"], {
    "title_th":s,"headline_th":s,"hook_th":s,"color_th":s,"hex":s,"outfit_score":{"type":["integer","null"],"minimum":0,"maximum":100},
    "layout":{"enum":["hue_card"]},"sizes":arr({"enum":["1080x1350","1080x1920","1080x1080"]}),"watermark":s,"cta_th":s}),
 "Quota": obj(["allowed","left_after","paywall"], {"allowed":i0,"left_after":{"type":["integer","null"],"minimum":0},"paywall":b}),
 "SafetyGuard": obj(["level","message_th"], {"level":{"enum":["ok","warn","stop"]},"message_th":s}),
 "ColorInfo": obj(["key","id","name_th","color_th","color_en","hex","accent"], {"key":s,"id":s,"name_th":s,"color_th":s,"color_en":s,"hex":s,"accent":s}),
}
schema={"$schema":S,"$id":"https://example.com/luckyhue.schema.json","title":"LuckyHue","$defs":defs}
def ref(n): return {"$ref":f"#/$defs/{n}","$defs":defs}
ex=[]
def add(n,v,note=""): ex.append({"def":n,"note":note,"value":v})

for p in PEOPLE: add("Person", p, p["name_th"])
shots=[MAY_CLOSET, BAD_SHOT, EMPTY_SHOT]
for sh in shots:
    add("ClosetPhoto", sh, sh["id"])
    add("ClosetScan", parse_closet(sh), sh["id"])
    add("ScanQuality", scan_quality(sh["glare"], sh["blur"], sh["crop"], len(sh["items"])), sh["id"])
    for it in sh["items"][:3]:
        add("ClosetItem", it, it["id"])
for k in WEEKDAYS:
    add("LuckyColor", lucky_color(k, TODAY), k)
add("LuckyColor", lucky_color("wednesday", use_wednesday_night=True), "wed night")
lucky=lucky_color("friday", TODAY); closet=parse_closet(MAY_CLOSET)
for pick, note in ((MAY_PICK,"may match"), (None,"auto"), (CLASH_PICK,"clash"), (["i01","i03"],"no match red via sunday later"), ([], "empty")):
    if note.startswith("no match"):
        add("OutfitMix", outfit_mix(closet, lucky_color("sunday"), pick=pick), "no match")
    else:
        add("OutfitMix", outfit_mix(closet, lucky, pick=pick), note)
# extra mixes across weekdays
for k in WEEKDAYS:
    add("OutfitMix", outfit_mix(closet, lucky_color(k)), "auto "+k)
    add("Wallpaper", wallpaper(lucky_color(k)), "wp "+k)
add("Wallpaper", wallpaper(lucky), "friday phone")
add("Wallpaper", wallpaper(lucky, "1080x1080"), "square")
add("Wallpaper", wallpaper(lucky_color("sunday"), "1170x2532"), "sunday")
cal=weekly_calendar(TODAY,"friday")
add("WeeklyCalendar", cal, "may week")
for d in cal["days"]:
    add("CalendarDay", d, d["weekday"])
add("WeeklyCalendar", weekly_calendar("2026-11-25","sunday"), "midweek start")
add("ShareCard", share_card("พี่เมย์", lucky, outfit_mix(closet, lucky, pick=MAY_PICK)), "may")
add("ShareCard", share_card("พี่เมย์", lucky, None), "no mix")
add("Quota", quota(1,1), "free"); add("Quota", quota(3,1), "exhausted"); add("Quota", quota(0,5,pro=True), "pro")
add("SafetyGuard", safety_guard(), "ok"); add("SafetyGuard", safety_guard(True), "warn")
for k,v in WEEKDAYS.items():
    add("ColorInfo", {"key":k,"id":v["id"],"name_th":v["name_th"],"color_th":v["color_th"],"color_en":v["color_en"],"hex":v["hex"],"accent":v["accent"]}, k)
for k in WEEKDAYS:
    add("WeeklyCalendar", weekly_calendar(TODAY, k), "week "+k)
for g,bl,c,n in ((0.1,0.1,0.1,3),(0.3,0.2,0.2,2),(0.5,0.4,0.3,1),(0.0,0.0,0.0,4),(0.2,0.3,0.1,5),(0.4,0.1,0.2,2),(0.6,0.2,0.1,1),(0.1,0.6,0.1,2),(0.2,0.2,0.6,1),(0.05,0.05,0.05,8)):
    add("ScanQuality", scan_quality(g,bl,c,n), f"{g}-{bl}-{c}-{n}")

for e in ex:
    jsonschema.validate(e["value"], ref(e["def"]))
d=os.path.dirname(os.path.abspath(__file__))+"/.."
json.dump(schema, open(d+"/schemas.json","w"), ensure_ascii=False, indent=1)
json.dump({"examples": ex}, open(d+"/examples.json","w"), ensure_ascii=False, indent=1)
print(len(defs), "defs,", len(ex), "examples, all valid")
