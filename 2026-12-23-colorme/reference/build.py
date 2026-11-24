"""Generate ../schemas.json + ../examples.json and validate every example."""
import json, os, jsonschema
from colorme import *
from fixtures import *

S = "https://json-schema.org/draft/2020-12/schema"
s = {"type": "string"}; b = {"type": "boolean"}; ns = {"type": ["string", "null"]}
u = {"type": "number", "minimum": 0, "maximum": 1}; num = {"type": "number"}; pos = {"type": "number", "exclusiveMinimum": 0}
i0 = {"type": "integer", "minimum": 0}; i1 = {"type": "integer", "minimum": 1}
pct = {"type": "integer", "minimum": 0, "maximum": 100}
date = {"type": "string", "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}$"}
hexc = {"type": "string", "pattern": "^#[0-9A-F]{6}$"}
arr = lambda x, **k: dict({"type": "array", "items": x}, **k)
R = lambda n: {"$ref": "#/$defs/" + n}
crayon = {"enum": KEYS}; level = {"enum": list(LEVELS)}


def obj(props, req=None, extra=False):
    return {"type": "object", "required": req if req is not None else list(props), "properties": props, "additionalProperties": extra}


rgb = arr({"type": "integer", "minimum": 0, "maximum": 255}, minItems=3, maxItems=3)
defs = {
    "Child": obj({"id": s, "name_th": s, "name_en": s, "age": {"type": "integer", "minimum": 3, "maximum": 120}, "city_th": s}),
    "Crayon": obj({"key": crayon, "name_th": s, "name_en": s, "hex": hexc}),
    "Level": obj({"key": level, "name_th": s, "ages": arr(i1, minItems=2, maxItems=2), "max_colors": i1, "min_area": i1, "max_regions": i1,
                  "line_px": i1, "numbers": b, "dots": i1}),
    "PhotoInput": obj({"id": s, "light": u, "sharp": u, "subject": u, "busy": u, "w": i1, "h": i1}),
    "PhotoCheck": obj({"score": pct, "ok": b, "tips_th": arr(s)}),
    "AiPhotoClean": obj({"subject_th": s, "background": {"enum": ["keep", "simplify", "remove"]}, "people": i0, "child_faces": i0, "nudity": b,
                         "id_document": b, "violent": b, "copyright_character": b, "suggested_title_th": s, "confidence": u}),
    "Palette": obj({"level": level, "keys": arr(crayon, minItems=1, maxItems=13)}),
    "LegendItem": obj({"num": i1, "key": crayon, "name_th": s, "hex": hexc, "regions": i1}),
    "RegionLabel": obj({"region": i1, "num": i1, "x": i0, "y": i0, "fits": b}),
    "ColoringPage": obj({"level": level, "mode": {"enum": list(MODES)}, "w": i1, "h": i1, "colors": i1, "regions": i1, "min_area": i1,
                         "simplify_passes": i0, "line_px": i1, "show_numbers": b, "edge_ratio": u, "legend": arr(R("LegendItem"), minItems=1),
                         "labels": arr(R("RegionLabel"))}),
    "Dot": obj({"num": i1, "x": num, "y": num}),
    "DotPage": obj({"level": level, "dots": arr(R("Dot"), minItems=3), "perimeter": pos, "spacing": pos, "closed": {"const": True}}),
    "Booklet": obj({"title_th": s, "pages": {"type": "integer", "minimum": 2, "maximum": 13}, "sheets_double_sided": i1, "paper": {"const": "A4"},
                    "dpi": {"const": 300}, "px": arr(i1, minItems=2, maxItems=2), "ink_saver": b, "line_px": i1, "ink_pct": {"type": "number", "minimum": 0, "maximum": 35},
                    "has_answer_key": b}),
    "Progress": obj({"coverage_pct": pct, "in_lines_pct": pct, "match_pct": {"type": ["integer", "null"], "minimum": 0, "maximum": 100},
                     "stars": {"type": "integer", "minimum": 1, "maximum": 3}, "favorite": {"enum": KEYS + [None]}, "praise_th": s, "done": b}),
    "Quest": obj({"date": date, "theme_th": {"enum": THEMES}, "streak": i0, "done_today": b, "new_sticker": {"enum": list(STICKERS.values()) + [None]}}),
    "GalleryEntry": obj({"date": date, "title_th": s, "stars": {"type": "integer", "minimum": 1, "maximum": 3}, "favorite": {"enum": KEYS + [None]}}),
    "GallerySummary": obj({"month": {"type": "string", "pattern": "^[0-9]{4}-[0-9]{2}$"}, "pages": i0, "stars": i0, "favorite_th": ns, "art_book_ready": b, "note_th": s}),
    "ShareCard": obj({"layout": {"enum": ["before_after", "reveal", "booklet"]}, "size": {"const": "1080x1350"}, "child_face_hidden": {"const": True},
                      "stars": {"type": ["integer", "null"]}, "level_th": s, "watermark": s, "badge_th": s}),
    "ReelShot": obj({"kind": {"enum": [k for k, _ in REEL_SHOTS]}, "start": {"type": "number", "minimum": 0}, "end": num, "caption_th": s}),
    "ReelPlan": obj({"seconds": {"type": "integer", "minimum": 15, "maximum": 30}, "ratio": {"const": "9:16"}, "bpm": i1, "shots": arr(R("ReelShot"), minItems=3), "watermark": s}),
    "Quota": obj({"plan": {"enum": ["free", "plus"]}, "pages_per_day": i1, "used": i0, "left": i0, "blocked": b}),
    "PrivacyCheck": obj({"allowed": b, "level": {"enum": ["ok", "warn", "stop"]}, "flags": arr({"enum": [k for k in GUARD if k]}), "messages_th": arr(s, minItems=1),
                         "parent_mode": b, "share_allowed": b}),
    "SafetyGuard": obj({"flag": {"type": ["string", "null"]}, "level": {"enum": ["ok", "warn", "stop"]}, "message_th": s, "block": b}),
}
schema = {"$schema": S, "$id": "https://github.com/arm-haha/ai-wanla-app/2026-12-23-colorme/schemas.json", "title": "ColorMe", "$defs": defs}
ref = lambda n: {"$schema": S, "$defs": defs, "$ref": "#/$defs/" + n}

ex = []
add = lambda d, v, note="": ex.append({"def": d, "note": note, "value": v})
for k in KIDS: add("Child", k, k["name_en"])
for c in CRAYONS: add("Crayon", {"key": c[0], "name_th": c[1], "name_en": c[2], "hex": "#%02X%02X%02X" % c[3]}, c[0])
for k, v in LEVELS.items(): add("Level", dict(key=k, **{kk: (list(vv) if kk == "ages" else vv) for kk, vv in v.items()}), k)
PHOTOS = [{"id": "p01", "light": 0.9, "sharp": 0.85, "subject": 0.6, "busy": 0.3, "w": W, "h": H},
          {"id": "p02", "light": 0.6, "sharp": 0.7, "subject": 0.25, "busy": 0.5, "w": 96, "h": 120},
          {"id": "p03", "light": 0.4, "sharp": 0.3, "subject": 0.2, "busy": 0.8, "w": 96, "h": 72}]
for p in PHOTOS:
    add("PhotoInput", p, p["id"]); add("PhotoCheck", photo_check(p["light"], p["sharp"], p["subject"], p["busy"]), p["id"])
AI = [{"subject_th": "แมวส้มนั่งบนสนามหญ้า", "background": "simplify", "people": 0, "child_faces": 0, "nudity": False, "id_document": False, "violent": False,
       "copyright_character": False, "suggested_title_th": "น้องส้มจี๊ดอาบแดด", "confidence": 0.93},
      {"subject_th": "เด็กสองคนเล่นทราย", "background": "remove", "people": 2, "child_faces": 2, "nudity": False, "id_document": False, "violent": False,
       "copyright_character": False, "suggested_title_th": "ปิดเทอมที่ทะเล", "confidence": 0.81},
      {"subject_th": "ตุ๊กตาการ์ตูนหมีสีน้ำตาล", "background": "keep", "people": 0, "child_faces": 0, "nudity": False, "id_document": False, "violent": False,
       "copyright_character": True, "suggested_title_th": "ตุ๊กตาหมีตัวโปรด", "confidence": 0.77},
      {"subject_th": "บัตรประจำตัว", "background": "keep", "people": 1, "child_faces": 0, "nudity": False, "id_document": True, "violent": False,
       "copyright_character": False, "suggested_title_th": "-", "confidence": 0.9}]
for a in AI: add("AiPhotoClean", a, a["subject_th"])
for age in (4, 6, 10, 36): add("Palette", {"level": level_for_age(age), "keys": pick_palette(PIC, LEVELS[level_for_age(age)]["max_colors"])}, str(age))
stripes = [[(230, 57, 70) if (x // 2) % 2 else (120, 190, 240) for x in range(40)] for _ in range(30)]
pages = [(PAGE_TINY, "tiny 4y"), (PAGE_KID, "kid 6y numbers"), (PAGE_BIG, "big 10y"), (PAGE_CALM, "calm adult"), (PAGE_LINE, "kid lineart"),
         (make_page(stripes, 4), "stripes auto-simplify"), (make_page(PIC, 12, "lineart"), "big lineart")]
for p, note in pages: add("ColoringPage", page_public(p), note)
for l in PAGE_KID["legend"] + PAGE_CALM["legend"]: add("LegendItem", l, l["key"])
for l in PAGE_KID["labels"]: add("RegionLabel", l, "region %d" % l["region"])
for age in (4, 6, 10, 36): add("DotPage", dot_to_dot(CAT_OUTLINE, age), str(age))
for d in dot_to_dot(CAT_OUTLINE, 4)["dots"][:5]: add("Dot", d, str(d["num"]))
for a, note in (((PAGE_KID, PAGE_TINY, PAGE_BIG), "3 pages"), ((PAGE_KID,), "1 page"), ((PAGE_LINE,) * 12, "12 pages")):
    add("Booklet", booklet(list(a), "น้องข้าวปั้น"), note)
add("Booklet", booklet([PAGE_CALM, PAGE_BIG], "คุณแม่ฝน", True), "ink saver")
scans = [(PAGE_KID, SCAN_DONE, "done"), (PAGE_KID, SCAN_HALF, "half, some other colours"), (PAGE_KID, SCAN_START, "just started"),
         (PAGE_KID, scan_of(PAGE_KID, 1.0, spill=30), "over the line"), (PAGE_LINE, scan_of(PAGE_LINE, 1.0), "lineart free colours"),
         (PAGE_KID, [[None] * PAGE_KID["w"] for _ in range(PAGE_KID["h"])], "blank")]
for p, sc, note in scans: add("Progress", progress_check(p, sc), note)
for d, h in ((TODAY, HISTORY), ("2026-12-24", HISTORY), ("2026-12-25", HISTORY), ("2026-12-30", ["2026-12-%02d" % i for i in range(24, 31)])):
    add("Quest", quest(d, h), d)
for g in GALLERY: add("GalleryEntry", g, g["title_th"])
add("GallerySummary", gallery_summary(GALLERY, "2026-12"), "8 pages"); add("GallerySummary", gallery_summary(GALLERY[:5], "2026-12"), "5 pages")
add("GallerySummary", gallery_summary(GALLERY, "2026-11"), "empty")
done = progress_check(PAGE_KID, SCAN_DONE)
for lay in ("before_after", "reveal", "booklet"): add("ShareCard", share_card(PAGE_KID, done if lay != "booklet" else None, lay), lay)
for sec in (15, 20, 30): add("ReelPlan", reel_plan(sec), str(sec))
for sh in reel_plan(24)["shots"]: add("ReelShot", sh, sh["kind"])
for a in ((0,), (3,), (5,), (12, "plus")): add("Quota", quota(*a), str(a))
for a in ((True, True), (True, False), (False, True), (True, True, ("copyright_character",)), (True, True, ("id_document",)), (True, True, ("nudity",))):
    add("PrivacyCheck", privacy_check(*a), str(a))
for f in GUARD: add("SafetyGuard", safety_guard(f), str(f))

for x in ex: jsonschema.validate(x["value"], ref(x["def"]))
d = os.path.dirname(os.path.abspath(__file__)) + "/.."
json.dump(schema, open(d + "/schemas.json", "w"), ensure_ascii=False, indent=1)
json.dump({"examples": ex}, open(d + "/examples.json", "w"), ensure_ascii=False, indent=1)
print(len(defs), "defs,", len(ex), "examples, all valid")
