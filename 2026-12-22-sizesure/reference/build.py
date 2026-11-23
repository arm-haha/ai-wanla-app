"""Generate ../schemas.json + ../examples.json and validate every example."""
import json, os, jsonschema
from sizesure import *
from fixtures import *

S = "https://json-schema.org/draft/2020-12/schema"
s = {"type": "string"}; b = {"type": "boolean"}; ns = {"type": ["string", "null"]}
u = {"type": "number", "minimum": 0, "maximum": 1}; num = {"type": "number"}; pos = {"type": "number", "exclusiveMinimum": 0}
i0 = {"type": "integer", "minimum": 0}; i1 = {"type": "integer", "minimum": 1}
pct = {"type": "integer", "minimum": 0, "maximum": 100}
date = {"type": "string", "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}$"}
arr = lambda x, **k: dict({"type": "array", "items": x}, **k)
R = lambda n: {"$ref": "#/$defs/" + n}
rng = arr(num, minItems=2, maxItems=2)


def obj(props, req=None, extra=False):
    return {"type": "object", "required": req if req is not None else list(props), "properties": props, "additionalProperties": extra}


area = {"enum": list(CIRC)}; cloth = {"enum": list(CLOTH_EASE)}
cmmap = obj({k: pos for k in CIRC + ("shoulder", "inseam", "sleeve")})
circmap = obj({k: pos for k in CIRC})
defs = {
    "Person": obj({"id": s, "name_th": s, "name_en": s, "age": {"type": "integer", "minimum": 1, "maximum": 110}, "height_cm": {"type": "number", "minimum": 50, "maximum": 230},
                   "city_th": s, "updated": date}),
    "BodyPhoto": obj({"id": s, "light": u, "full_body": {"enum": [0, 1]}, "pose_ok": {"enum": [0, 1]}, "clothing": cloth, "ref_visible": {"enum": [0, 1]}}),
    "PhotoCheck": obj({"score": pct, "ok": b, "tips_th": arr(s)}),
    "AiBodyMeasure": obj({"front": obj({k: pos for k in ("height_px", "shoulder_px", "chest_px", "waist_px", "hip_px", "inseam_px", "arm_px")}),
                          "side": obj({k: pos for k in ("height_px", "chest_px", "waist_px", "hip_px")}),
                          "a4_px": {"type": ["number", "null"], "exclusiveMinimum": 0}, "clothing": cloth, "people": i0, "nudity": b, "pose_ok": b, "confidence": u}),
    "Measurements": obj({"height_cm": num, "cm": cmmap, "margin_cm": pos, "clothing": cloth, "warnings": arr({"enum": ["scale_mismatch", "loose_clothes"]}),
                         "scale_note_th": ns, "source": {"enum": ["photo", "tape", "mixed"]}}),
    "AiChartRead": obj({"shop_th": s, "unit": {"enum": ["cm", "inch"]}, "method": {"enum": ["body", "garment", "flat"]},
                        "rows": arr(obj({"label": s, "values": {"type": "object", "additionalProperties": {"oneOf": [pos, arr(pos, minItems=2, maxItems=2)]}}}), minItems=1)},
                       ["unit", "method", "rows"]),
    "SizeChart": obj({"shop_th": s, "kind": {"enum": ["body", "garment"]}, "rows": arr(obj({"label": s, "cm": {"type": "object", "additionalProperties": rng}})),
                      "converted": b, "note_th": ns}),
    "AreaFit": obj({"area": area, "body_cm": num, "range_cm": rng, "ease_cm": num, "label": {"enum": ["good", "tight", "loose"]}}),
    "SizeRecommendation": obj({"best": s, "second": ns, "fit": arr(R("AreaFit"), minItems=1), "between_sizes": b, "confidence": {"enum": ["high", "medium", "low"]},
                               "advice_th": s, "kind": {"enum": list(KINDS)}, "fit_pref": {"enum": ["slim", "regular", "oversize"]}, "stretch": {"enum": list(STRETCH)}}),
    "ShoeSize": obj({"foot_cm": pos, "shoe_cm": pos, "eu": num, "us_women": num, "us_men": num, "uk": num, "width": {"enum": ["narrow", "regular", "wide", None]},
                     "approx": {"const": True}, "note_th": ns}),
    "SizePassport": obj({"name_th": s, "updated": s, "top": {"enum": list(GENERIC)}, "jeans_waist_in": i1, "cm": circmap, "inch": circmap,
                         "shoe_eu": {"type": ["number", "null"]}, "margin_cm": pos, "share_numbers": b}),
    "GiftPick": obj({"for_th": s, "kind": {"enum": ["top", "bottom", "shoes"]}, "size": s, "jeans_waist_in": {"type": ["integer", "null"]},
                     "shoe_eu": {"type": ["number", "null"]}, "tip_th": s}),
    "ReturnRisk": obj({"level": {"enum": ["low", "medium", "high"]}, "points": i0, "reasons_th": arr(s), "tip_th": s}),
    "LogEntry": obj({"date": date, "cm": circmap}),
    "LogSummary": obj({"today": date, "entries": i0, "last_date": {"type": ["string", "null"]}, "days_since": {"type": ["integer", "null"]},
                       "change_cm": {"type": "object", "additionalProperties": num}, "hidden": b, "remeasure": b, "note_th": s}),
    "ShareCard": obj({"layout": {"enum": ["size_card", "before_after", "fit_meter"]}, "size": {"const": "1080x1350"}, "shows_numbers": {"const": False},
                      "top": s, "shoe_eu": {"type": ["number", "null"]}, "watermark": s, "badge_th": s}),
    "ReelShot": obj({"kind": {"enum": [k for k, _ in REEL_SHOTS]}, "start": {"type": "number", "minimum": 0}, "end": num, "caption_th": s}),
    "ReelPlan": obj({"seconds": {"type": "integer", "minimum": 15, "maximum": 30}, "ratio": {"const": "9:16"}, "bpm": i1, "shots": arr(R("ReelShot"), minItems=3), "watermark": s}),
    "Quota": obj({"plan": {"enum": ["free", "plus"]}, "measures_per_day": i1, "used": i0, "left": i0, "blocked": b}),
    "PrivacyCheck": obj({"allowed": b, "level": {"enum": ["ok", "warn", "stop"]}, "flags": arr({"enum": [k for k in GUARD if k]}), "messages_th": arr(s, minItems=1), "manual_entry_ok": b}),
    "SafetyGuard": obj({"flag": {"type": ["string", "null"]}, "level": {"enum": ["ok", "warn", "stop"]}, "message_th": s, "block": b}),
}
schema = {"$schema": S, "$id": "https://github.com/arm-haha/ai-wanla-app/2026-12-22-sizesure/schemas.json", "title": "SizeSure", "$defs": defs}
ref = lambda n: {"$schema": S, "$defs": defs, "$ref": "#/$defs/" + n}

ex = []
add = lambda d, v, note="": ex.append({"def": d, "note": note, "value": v})
for p in PEOPLE: add("Person", p, p["name_en"])
for ph in PHOTOS:
    add("BodyPhoto", ph, ph["id"]); add("PhotoCheck", photo_check(*[ph[k] for k in ("light", "full_body", "pose_ok", "clothing", "ref_visible")]), ph["id"])
for a in ((0.8, 1, 1, "normal", 1), (0.95, 1, 0, "fitted", 1), (0.5, 1, 1, "loose", 1)): add("PhotoCheck", photo_check(*a), str(a))
add("AiBodyMeasure", AI_PRAEW, "praew"); add("AiBodyMeasure", AI_OAT, "oat loose"); add("AiBodyMeasure", dict(AI_PRAEW, a4_px=None), "no A4")
add("Measurements", M_PRAEW, "praew"); add("Measurements", M_OAT, "oat")
add("Measurements", measure_body(dict(AI_PRAEW, clothing="normal"), 160), "praew normal clothes")
add("Measurements", measure_body(dict(AI_PRAEW, a4_px=None), 160), "no A4")
add("Measurements", override(M_PRAEW, {"chest": 85, "waist": 68.5, "hip": 94}), "tape")
add("Measurements", override(M_OAT, {"waist": 84}), "mixed")
for c in (CHART_SHIRT, CHART_DRESS, CHART_JEANS): add("AiChartRead", c, c["shop_th"])
CHART_KIDS = {"shop_th": "ร้านชุดนอน (สมมติ)", "unit": "cm", "method": "garment", "rows": [{"label": "F", "values": {"chest": 104, "length": 66}}, {"label": "XL", "values": {"chest": 112, "length": 70}}]}
add("AiChartRead", CHART_KIDS, "garment cm")
for c in (N_SHIRT, N_DRESS, N_JEANS, normalize_chart(CHART_KIDS)): add("SizeChart", c, c["shop_th"])
gen = {"shop_th": "ตารางมาตรฐานในแอป", "kind": "body", "rows": [{"label": k, "cm": v} for k, v in GENERIC.items()], "converted": False, "note_th": None}
add("SizeChart", gen, "generic")
recs = [(REC_SHIRT, "shirt regular"), (REC_DRESS, "dress"), (REC_JEANS, "jeans slim some-stretch"),
        (recommend(M_PRAEW, N_SHIRT, "top", "slim"), "shirt slim"), (recommend(M_PRAEW, N_SHIRT, "top", "oversize"), "shirt oversize"),
        (recommend(M_PRAEW, N_JEANS, "bottom", "slim", "none"), "jeans no stretch"), (recommend(M_OAT, gen, "top"), "oat generic low conf"),
        (recommend(M_PRAEW, gen, "top"), "praew generic"), (recommend(M_PRAEW, normalize_chart(CHART_KIDS), "top", "oversize"), "pajama oversize"),
        (recommend(override(M_PRAEW, {"chest": 85, "waist": 68.5, "hip": 94}), N_DRESS, "dress", "regular", "high"), "dress stretch tape")]
for r, note in recs: add("SizeRecommendation", r, note)
for r, note in recs:
    for a in r["fit"]: add("AreaFit", a, note + " " + a["area"])
for a in ((940, 1188, 360), (1080, 1188, 450), (1000, 1188, 330), (700, 1188, None), (1160, 1188, 440)): add("ShoeSize", shoe_size(*a), str(a))
add("SizePassport", PP_PRAEW, "praew")
add("SizePassport", passport(PEOPLE[1], M_OAT, shoe_size(1160, 1188, 440)), "oat")
add("SizePassport", passport(PEOPLE[2], override(M_PRAEW, {"chest": 92, "waist": 80, "hip": 98})), "nuan tape no shoe")
for a in ((PP_PRAEW,), (PP_PRAEW, "top", "oversize"), (PP_PRAEW, "bottom"), (PP_PRAEW, "shoes")): add("GiftPick", gift_pick(*a), str(a[1:]))
for r, c, rv in ((REC_SHIRT, True, None), (REC_DRESS, False, "runs_small"), (REC_JEANS, True, "true_to_size"), (recs[6][0], False, None), (REC_SHIRT, True, "runs_large")):
    add("ReturnRisk", return_risk(r, c, rv), str(rv))
for e in LOG: add("LogEntry", e, e["date"])
add("LogSummary", log_summary(LOG, TODAY)); add("LogSummary", log_summary(LOG, TODAY, True), "hidden"); add("LogSummary", log_summary(LOG[:1], TODAY), "remeasure")
add("LogSummary", log_summary([], TODAY), "empty")
for lay in ("size_card", "before_after", "fit_meter"): add("ShareCard", share_card(PP_PRAEW, lay), lay)
for sec in (15, 20, 30): add("ReelPlan", reel_plan(sec), str(sec))
for sh in reel_plan(24)["shots"]: add("ReelShot", sh, sh["kind"])
for a in ((0,), (2,), (3,), (10, "plus")): add("Quota", quota(*a), str(a))
for a in ((28, True), (15, True), (30, False), (30, True, ("nudity",)), (30, True, ("loose_clothes",)), (40, True, ("multiple_people",))):
    add("PrivacyCheck", privacy_check(*a), str(a))
for f in GUARD: add("SafetyGuard", safety_guard(f), str(f))

for x in ex: jsonschema.validate(x["value"], ref(x["def"]))
d = os.path.dirname(os.path.abspath(__file__)) + "/.."
json.dump(schema, open(d + "/schemas.json", "w"), ensure_ascii=False, indent=1)
json.dump({"examples": ex}, open(d + "/examples.json", "w"), ensure_ascii=False, indent=1)
print(len(defs), "defs,", len(ex), "examples, all valid")
