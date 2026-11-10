"""Generate ../schemas.json + ../examples.json and validate every example."""
import json, os, jsonschema
from specstry import *
from fixtures import *

S = "https://json-schema.org/draft/2020-12/schema"
s={"type":"string"}; b={"type":"boolean"}; n0={"type":"number","minimum":0}
u={"type":"number","minimum":0,"maximum":1}; i0={"type":"integer","minimum":0}; i1={"type":"integer","minimum":1}
pct={"type":"integer","minimum":0,"maximum":100}
date={"type":"string","format":"date","pattern":"^[0-9]{4}-[0-9]{2}-[0-9]{2}$"}
fid={"enum":list(FRAMES)}; shape={"enum":FACE_SHAPES}; life={"enum":LIFESTYLES}
region={"enum":list(REGION_MULT)}; under={"enum":UNDERTONES}; lens={"enum":list(LENS_TYPES)}
mat={"enum":MATERIALS}

def obj(req, props, **kw):
    return {"type":"object","required":req,"properties":props,"additionalProperties":False, **kw}
def arr(i, **kw):
    return {"type":"array","items":i, **kw}

defs = {
 "Person": obj(["id","name_th","age","region","lifestyle"], {
    "id":{"type":"string","pattern":"^u[0-9]{2}$"},"name_th":s,"name_en":s,"age":i1,"city_th":s,"goal_th":s,
    "region":region,"lifestyle":life}),
 "Measures": obj(["length_mm","forehead_mm","cheek_mm","jaw_mm"], {
    "length_mm":n0,"forehead_mm":n0,"cheek_mm":n0,"jaw_mm":n0}),
 "FacePhoto": obj(["id","px_w","px_h","glare","blur","tilt","face_fill","eyes_visible","undertone","face_confidence","pd_mm","measures"], {
    "id":{"type":"string","pattern":"^p[0-9]{2}$"},"px_w":i1,"px_h":i1,"glare":u,"blur":u,"tilt":u,
    "face_fill":u,"eyes_visible":u,"undertone":under,"face_confidence":u,"pd_mm":n0,
    "measures":{"$ref":"#/$defs/Measures"}}),
 "ScanQuality": obj(["score","ok","tips_th"], {"score":pct,"ok":b,"tips_th":arr(s)}),
 "FaceShape": obj(["shape","shape_th","length_mm","forehead_mm","cheek_mm","jaw_mm","length_to_width","advice_th"], {
    "shape":shape,"shape_th":s,"length_mm":n0,"forehead_mm":n0,"cheek_mm":n0,"jaw_mm":n0,
    "length_to_width":n0,"advice_th":s}),
 "FaceScan": obj(["photo_id","quality","undertone","pd_mm","face","uncertain","ok","message_th"], {
    "photo_id":s,"quality":{"$ref":"#/$defs/ScanQuality"},"undertone":under,"pd_mm":n0,
    "face":{"anyOf":[{"$ref":"#/$defs/FaceShape"},{"type":"null"}]},"uncertain":b,"ok":b,"message_th":s}),
 "Pipeline": obj(["photo_id","steps"], {"photo_id":s,"steps":arr(s,minItems=1)}),
 "FrameInfo": obj(["id","name_th","name_en","shape","material","material_th","lens_width","bridge","temple","color","base_thb","best_shapes","lifestyle","front_mm"], {
    "id":fid,"name_th":s,"name_en":s,"shape":s,"material":mat,"material_th":s,"lens_width":i1,"bridge":i1,
    "temple":i1,"color":s,"base_thb":i0,"best_shapes":arr(shape),"lifestyle":arr(life),"front_mm":i1}),
 "PdStatus": obj(["pd_mm","verdict","message_th","disclaimer_th"], {
    "pd_mm":n0,"verdict":{"enum":["typical","check","out_of_range"]},"message_th":s,"disclaimer_th":s}),
 "SizeCheck": obj(["frame_id","pd_mm","pd_verdict","face_width_mm","frame_front_mm","lens_width","bridge","temple","delta_mm","verdict","fit_th","centres_mm","center_offset_mm","message_th","disclaimer_th"], {
    "frame_id":fid,"pd_mm":n0,"pd_verdict":{"enum":["typical","check","out_of_range"]},"face_width_mm":n0,
    "frame_front_mm":n0,"lens_width":i1,"bridge":i1,"temple":i1,"delta_mm":{"type":"number"},
    "verdict":{"enum":["ok","too_narrow","too_wide"]},"fit_th":s,"centres_mm":n0,
    "center_offset_mm":{"type":"number"},"message_th":s,"disclaimer_th":s}),
 "FitScore": obj(["frame_id","score","face_pts","size_pts","contrast_pts","lifestyle_pts","reasons_th"], {
    "frame_id":fid,"score":pct,"face_pts":i0,"size_pts":i0,"contrast_pts":i0,"lifestyle_pts":i0,"reasons_th":arr(s)}),
 "TryOn": obj(["photo_id","frame_id","name_th","shape","material","color","face_shape","face_shape_th","pd_mm","size_verdict","fit_score","quality","watermark","disclaimer_th"], {
    "photo_id":s,"frame_id":fid,"name_th":s,"shape":s,"material":mat,"color":s,"face_shape":shape,"face_shape_th":s,
    "pd_mm":n0,"size_verdict":{"enum":["ok","too_narrow","too_wide"]},"fit_score":pct,
    "quality":{"$ref":"#/$defs/ScanQuality"},"watermark":s,"disclaimer_th":s}),
 "TryOnGrid": obj(["photo_id","count","ranked","top_id"], {
    "photo_id":s,"count":i1,"ranked":arr({"$ref":"#/$defs/TryOn"},minItems=1),"top_id":fid}),
 "CompareGrid": obj(["photo_id","frames","count"], {
    "photo_id":s,"frames":arr({"$ref":"#/$defs/TryOn"},minItems=2),"count":{"type":"integer","minimum":2,"maximum":4}}),
 "PriceRange": obj(["frame_id","name_th","region","lens","lens_th","mid_thb","min_thb","max_thb","currency","disclaimer_th"], {
    "frame_id":fid,"name_th":s,"region":region,"lens":lens,"lens_th":s,"mid_thb":i0,"min_thb":i0,"max_thb":i0,
    "currency":{"const":"THB"},"disclaimer_th":s}),
 "QuoteCheck": obj(["quote_thb","min_thb","max_thb","mid_thb","verdict","message_th","questions_th","disclaimer_th"], {
    "quote_thb":i0,"min_thb":i0,"max_thb":i0,"mid_thb":i0,"verdict":{"enum":["low","fair","high","very_high"]},
    "message_th":s,"questions_th":arr(s,minItems=1),"disclaimer_th":s}),
 "LensAdvice": obj(["lens","name_th","add_thb","notes_th","warnings_th","lifestyle","disclaimer_th"], {
    "lens":lens,"name_th":s,"add_thb":i0,"notes_th":s,"warnings_th":arr(s),"lifestyle":life,"disclaimer_th":s}),
 "OpticianCard": obj(["title_th","name_th","face_shape","face_shape_th","frame_id","frame_th","lens_width","bridge","temple","pd_mm","fit_score","size_verdict","budget_min_thb","budget_max_thb","note_th","line_share_url","disclaimer_th"], {
    "title_th":s,"name_th":s,"face_shape":shape,"face_shape_th":s,"frame_id":fid,"frame_th":s,
    "lens_width":i1,"bridge":i1,"temple":i1,"pd_mm":n0,"fit_score":pct,
    "size_verdict":{"enum":["ok","too_narrow","too_wide"]},"budget_min_thb":i0,"budget_max_thb":i0,
    "note_th":s,"line_share_url":{"type":"string","pattern":"^https://line\\.me/R/share\\?text="},"disclaimer_th":s}),
 "DiaryEntry": obj(["id","person_id","date","frame_id","shop_th","cost_thb","status","on_device"], {
    "id":s,"person_id":s,"date":date,"frame_id":fid,"shop_th":s,"cost_thb":i0,
    "status":{"enum":["wishlist","tried","bought"]},"on_device":b}),
 "DiaryStats": obj(["count","total_thb","avg_thb","last_date","top_frame"], {
    "count":i0,"total_thb":i0,"avg_thb":i0,"last_date":{"type":["string","null"]},"top_frame":{"type":["string","null"]}}),
 "ShareCard": obj(["title_th","headline_th","hook_th","frame_id","face_shape","layout","sizes","watermark","cta_th"], {
    "title_th":s,"headline_th":s,"hook_th":s,"frame_id":fid,"face_shape":shape,"layout":{"enum":["tryon_result"]},
    "sizes":arr({"enum":["1080x1350","1080x1920","1080x1080"]}),"watermark":s,"cta_th":s}),
 "Quota": obj(["allowed","left_after","paywall"], {"allowed":i0,"left_after":{"type":["integer","null"],"minimum":0},"paywall":b}),
 "SafetyGuard": obj(["level","message_th"], {"level":{"enum":["ok","stop"]},"message_th":s}),
}
schema={"$schema":S,"$id":"https://example.com/specstry.schema.json","title":"SpecsTry","$defs":defs}

def ref(n):
    return {"$ref":f"#/$defs/{n}","$defs":defs}

ex=[]; 
def add(n,v,note=""):
    ex.append({"def":n,"note":note,"value":v})

for p in PEOPLE:
    add("Person", p, p["name_th"])
for ph in PHOTOS:
    add("FacePhoto", ph, ph["id"])
    add("FaceScan", face_scan(ph), ph["id"])
    add("Pipeline", {"photo_id":ph["id"],"steps":pipeline_steps(ph)}, ph["id"])

for sh, mm in (("oval",(185,132,136,125)),("round",(160,134,136,132)),("square",(168,138,140,138)),
               ("heart",(180,140,138,120)),("oblong",(200,130,130,128)),("diamond",(180,124,140,124))):
    add("FaceShape", face_shape(*mm), sh)

for fid_ in FRAMES:
    add("FrameInfo", frame_info(fid_), fid_)

add("PdStatus", pd_status(62), "typical")
add("PdStatus", pd_status(54), "check")
add("PdStatus", pd_status(50), "out of range")

sz = size_check(62, 136, "f01")
add("SizeCheck", sz, "gale ok")
add("SizeCheck", size_check(62, 136, "f10"), "too narrow")
add("SizeCheck", size_check(62, 136, "f11"), "too wide")
add("SizeCheck", size_check(50, 136, "f01"), "odd pd")

add("FitScore", fit_score("oval","f01",sz,"cool","office"), "gale f01")
add("FitScore", fit_score("round","f08", size_check(64,136,"f08"), "warm","fashion"), "mismatch")

t_gale = overlay_tryon(GALE_PHOTO, "f01", "office")
add("TryOn", t_gale, "gale f01")
add("TryOn", overlay_tryon(GALE_PHOTO, "f02", "office"), "gale f02")
add("TryOn", overlay_tryon(PHOTOS[1], "f02", "office"), "bom rectangle")
add("TryOn", overlay_tryon(PHOTOS[3], "f03", "fashion"), "mind cateye")
add("TryOn", overlay_tryon(PHOTOS[1], "f04", "office"), "bom titanium")
add("TryOn", overlay_tryon(PHOTOS[3], "f07", "office"), "mind rimless")
add("TryOn", overlay_tryon(PHOTOS[4], "f05", "casual"), "oblong browline")
add("TryOn", overlay_tryon(PHOTOS[5], "f03", "fashion"), "diamond cateye")
add("SizeCheck", size_check(62, 136, "f02"), "f02")
add("SizeCheck", size_check(62, 136, "f07"), "f07")
add("SizeCheck", size_check(62, 136, "f12"), "f12")
add("FitScore", fit_score("oval","f02", size_check(62,136,"f02"), "cool","office"), "gale f02")
add("FitScore", fit_score("oval","f07", size_check(62,136,"f07"), "cool","office"), "gale f07")
add("PriceRange", price_range("f12","bkk","single"), "f12")
add("PriceRange", price_range("f10","bkk","single"), "f10")

add("TryOnGrid", tryon_grid(GALE_PHOTO, GALE_GRID, "office"), "gale 6")
add("CompareGrid", compare_grid(GALE_PHOTO, ["f01","f07","f02"], "office"), "top3")

pr = price_range("f01","bkk","single")
add("PriceRange", pr, "gale")
add("PriceRange", price_range("f01","province","single"), "province")
add("PriceRange", price_range("f01","bkk","progressive"), "progressive")
add("PriceRange", price_range("f04","tourist","blue_light"), "tourist titanium")
add("QuoteCheck", quote_check(3200,"f01","bkk"), "fair")
add("QuoteCheck", quote_check(1800,"f01","bkk"), "low")
add("QuoteCheck", quote_check(3900,"f01","bkk"), "high")
add("QuoteCheck", quote_check(8000,"f01","bkk"), "very high")

for L in LENS_TYPES:
    add("LensAdvice", lens_advice(L, 26 if L!="progressive" else 58, "office" if L!="sun" else "outdoor"), L)

add("OpticianCard", optician_card(GALE, face_scan(GALE_PHOTO), t_gale, pr, sz, GALE_NOTE), "gale")
entries=[diary_entry(*e) for e in DIARY]
for e in entries:
    add("DiaryEntry", e, e["id"])
add("DiaryStats", diary_stats(entries), "gale diary")
add("DiaryStats", diary_stats([]), "empty")
add("ShareCard", share_card(GALE["name_th"], t_gale), "gale")
add("Quota", quota(1,1), "free")
add("Quota", quota(3,1), "exhausted")
add("Quota", quota(0,5,pro=True), "pro")
add("SafetyGuard", safety_guard(True), "ok")
add("SafetyGuard", safety_guard(False), "stop")

for e in ex:
    jsonschema.validate(e["value"], ref(e["def"]))
d=os.path.dirname(os.path.abspath(__file__))+"/.."
json.dump(schema, open(d+"/schemas.json","w"), ensure_ascii=False, indent=1)
json.dump({"examples":ex}, open(d+"/examples.json","w"), ensure_ascii=False, indent=1)
print(len(defs),"defs,",len(ex),"examples, all valid")
