"""Generate ../schemas.json + ../examples.json and validate every example."""
import json, os, jsonschema
from posterpop import *
from fixtures import *

S = "https://json-schema.org/draft/2020-12/schema"
s = {"type": "string"}
b = {"type": "boolean"}
i0 = {"type": "integer", "minimum": 0}
i1 = {"type": "integer", "minimum": 1}
tmpl = {"enum": list(TEMPLATES)}
sz = {"enum": list(SIZES)}

def obj(req, props, **kw):
    return {"type": "object", "required": req, "properties": props, "additionalProperties": False, **kw}

def arr(i, **kw):
    return {"type": "array", "items": i, **kw}

defs = {
 "Person": obj(["id", "name_th", "age", "shop_th"], {
    "id": {"type": "string", "pattern": "^u[0-9]{2}$"}, "name_th": s, "name_en": s, "age": i1,
    "city_th": s, "shop_th": s, "role_th": s}),
 "TemplateInfo": obj(["id", "template", "name_th", "name_en", "mood_th", "zones", "default_palette"], {
    "id": {"type": "string", "pattern": "^t[0-9]{2}$"}, "template": tmpl, "name_th": s, "name_en": s,
    "mood_th": s, "zones": arr(s, minItems=1), "default_palette": arr(s, minItems=2)}),
 "SizeInfo": obj(["id", "size_id", "w", "h", "label_th", "kind"], {
    "id": {"type": "string", "pattern": "^s[0-9]{2}$"}, "size_id": sz, "w": i1, "h": i1, "label_th": s,
    "kind": {"enum": ["social", "print"]}}),
 "ContrastCheck": obj(["fg", "bg", "kind", "ratio", "need", "ok", "level_th", "tip_th"], {
    "fg": s, "bg": s, "kind": {"enum": ["body", "large"]}, "ratio": {"type": "number", "minimum": 1},
    "need": {"type": "number"}, "ok": b, "level_th": s, "tip_th": s}),
 "BrandKit": obj(["name_th", "colors", "heading_font", "body_font", "contrast", "tip_th"], {
    "name_th": s, "colors": arr(s, minItems=2), "heading_font": s, "body_font": s,
    "contrast": {"$ref": "#/$defs/ContrastCheck"}, "tip_th": s}),
 "QrBlock": obj(["url", "position", "size_px", "label_th", "kind"], {
    "url": s, "position": {"enum": ["footer_right", "footer_left", "footer_center"]},
    "size_px": i1, "label_th": s, "kind": {"const": "qr"}}),
 "MenuRow": obj(["name_th", "price_thb", "price_label_th"], {"name_th": s, "price_thb": i0, "price_label_th": s}),
 "MenuGrid": obj(["rows", "count", "cols"], {
    "rows": arr({"$ref": "#/$defs/MenuRow"}, minItems=1), "count": i1, "cols": i1}),
 "Zone": obj(["id", "y", "h"], {"id": s, "y": {"type": "number"}, "h": {"type": "number"}}),
 "PosterLayout": obj(["template", "size_id", "w", "h", "title_th", "title_px", "colors", "zones", "ok_contrast", "disclaimer_th"], {
    "template": tmpl, "size_id": sz, "w": i1, "h": i1, "title_th": s, "subtitle_th": s, "details_th": s,
    "date_th": s, "place_th": s, "cta_th": s, "title_px": i1, "heading_font": s, "body_font": s,
    "colors": arr(s), "zones": arr({"$ref": "#/$defs/Zone"}), "qr": {"type": ["object", "null"]},
    "title_contrast": {"$ref": "#/$defs/ContrastCheck"}, "body_contrast": {"$ref": "#/$defs/ContrastCheck"},
    "headline_th": s, "ok_contrast": b, "disclaimer_th": s}),
 "Pipeline": obj(["steps"], {"steps": arr(s, minItems=1), "template": tmpl}),
 "ShareCard": obj(["title_th", "headline_th", "hook_th", "template", "size_id", "layout", "sizes", "watermark", "cta_th"], {
    "title_th": s, "headline_th": s, "hook_th": s, "template": tmpl, "size_id": sz,
    "layout": {"enum": ["poster_preview"]}, "sizes": arr({"enum": ["1080x1350", "1080x1920", "1080x1080"]}),
    "watermark": s, "cta_th": s}),
 "Quota": obj(["allowed", "left_after", "paywall"], {"allowed": i0, "left_after": {"type": ["integer", "null"], "minimum": 0}, "paywall": b}),
 "SafetyGuard": obj(["level", "message_th"], {"level": {"enum": ["ok", "warn", "stop"]}, "message_th": s}),
}
schema = {"$schema": S, "$id": "https://example.com/posterpop.schema.json", "title": "PosterPop", "$defs": defs}

def ref(n):
    return {"$ref": f"#/$defs/{n}", "$defs": defs}

ex = []
def add(n, v, note=""):
    ex.append({"def": n, "note": note, "value": v})

for p in PEOPLE:
    add("Person", {k: p[k] for k in p}, p["name_th"])
for tid in TEMPLATE_IDS:
    add("TemplateInfo", template_info(tid), tid)
for sid in SIZE_IDS:
    add("SizeInfo", size_info(sid), sid)

add("ContrastCheck", contrast_check("#4A2C2A", "#F8F1E3", "large"), "jay large")
add("ContrastCheck", contrast_check("#4A2C2A", "#F8F1E3", "body"), "jay body")
add("ContrastCheck", contrast_check("#F8F1E3", "#F8F1E3", "body"), "fail")
add("ContrastCheck", contrast_check("#8A8A8A", "#FFFFFF", "large"), "grey large")
add("ContrastCheck", contrast_check("#8A8A8A", "#FFFFFF", "body"), "grey body")
add("ContrastCheck", contrast_check("#000000", "#FFFFFF", "body"), "max")

jay_brand = brand_kit(JAY_BRAND["name_th"], JAY_BRAND["colors"])
morn_brand = brand_kit(MORN_BRAND["name_th"], MORN_BRAND["colors"])
add("BrandKit", jay_brand, "jay")
add("BrandKit", morn_brand, "morn")
add("BrandKit", brand_kit("Ficto Clinic", ["#1A1A1A", "#FFFFFF", "#2563EB"]), "clinic")

for url, pos in ((JAY_BRIEF["qr_url"], "footer_right"), (MORN_BRIEF["qr_url"], "footer_center"),
                 ("https://example.com/menu", "footer_left")):
    add("QrBlock", qr_block(url, pos), pos)

add("MenuRow", menu_grid(JAY_MENU)["rows"][0], "latte")
add("MenuGrid", menu_grid(JAY_MENU), "4 items")
add("MenuGrid", menu_grid(JAY_MENU + JAY_MENU + JAY_MENU[:1]), "9 items")
add("MenuGrid", menu_grid([{"name_th": "น้ำเปล่า", "price_thb": 0}]), "free water")

jay_qr = qr_block(JAY_BRIEF["qr_url"])
jay_lay = auto_layout("sale", "ig_portrait", JAY_BRIEF["title"], JAY_BRIEF["subtitle"], JAY_BRIEF["details"],
                      JAY_BRIEF["date_th"], JAY_BRIEF["place_th"], JAY_BRIEF["cta_th"], jay_brand, jay_qr)
add("PosterLayout", jay_lay, "jay ig")
add("PosterLayout", auto_layout("sale", "a4", JAY_BRIEF["title"], JAY_BRIEF["subtitle"], JAY_BRIEF["details"],
                                JAY_BRIEF["date_th"], JAY_BRIEF["place_th"], JAY_BRIEF["cta_th"], jay_brand, jay_qr), "jay a4")
add("PosterLayout", auto_layout("sale", "ig_story", JAY_BRIEF["title"], JAY_BRIEF["subtitle"], JAY_BRIEF["details"],
                                JAY_BRIEF["date_th"], JAY_BRIEF["place_th"], JAY_BRIEF["cta_th"], jay_brand, jay_qr), "jay story")
add("PosterLayout", auto_layout("event", "fb_post", MORN_BRIEF["title"], MORN_BRIEF["subtitle"], MORN_BRIEF["details"],
                                MORN_BRIEF["date_th"], MORN_BRIEF["place_th"], MORN_BRIEF["cta_th"], morn_brand,
                                qr_block(MORN_BRIEF["qr_url"])), "morn event")
add("PosterLayout", auto_layout("menu", "a4", "เมนู Ficto Café", "เครื่องดื่มและขนม", "", "", "", "ยินดีต้อนรับ", jay_brand, None), "menu a4")
for z in jay_lay["zones"]:
    add("Zone", z, z["id"])

for tid, qr, ok in (("sale", True, True), ("event", True, True), ("menu", False, False)):
    add("Pipeline", {"template": tid, "steps": pipeline_steps(tid, has_qr=qr, contrast_ok=ok)}, tid)

add("ShareCard", share_card("พี่เจ", "โปรศุกร์ 1 แถม 1", "sale", "ig_portrait"), "jay")
add("ShareCard", share_card("พี่มอ", "ตลาดนัดยามเย็น", "event", "fb_post"), "morn")
add("Quota", quota(1, 1), "free")
add("Quota", quota(3, 1), "exhausted")
add("Quota", quota(0, 5, pro=True), "pro")
add("SafetyGuard", safety_guard(True), "ok")
add("SafetyGuard", safety_guard(False), "stop")

# extra layouts for size coverage
for sid in ("ig_square", "a3"):
    add("PosterLayout", auto_layout("sale", sid, JAY_BRIEF["title"], JAY_BRIEF["subtitle"], JAY_BRIEF["details"],
                                    JAY_BRIEF["date_th"], JAY_BRIEF["place_th"], JAY_BRIEF["cta_th"], jay_brand, jay_qr), sid)


pairs = [("#1E3A5F","#F4EFE6","large"), ("#1E3A5F","#F4EFE6","body"),
         ("#2C1810","#FFF8EE","body"), ("#E8772E","#F8F1E3","large"),
         ("#E8772E","#F8F1E3","body"), ("#FFFFFF","#4A2C2A","large"),
         ("#C4A574","#1E3A5F","large"), ("#2563EB","#FFFFFF","body"),
         ("#111111","#FFFF00","large"), ("#FF0000","#FFFFFF","body")]
for fg,bg,k in pairs:
    add("ContrastCheck", contrast_check(fg,bg,k), f"{fg} {k}")

for name, cols in (("Ficto Books", ["#111827","#FFF7ED","#B45309"]),
                   ("Ficto Gym", ["#14532D","#ECFDF5","#F59E0B"]),
                   ("Ficto Salon", ["#4C0519","#FFF1F2","#E11D48"])):
    bk = brand_kit(name, cols)
    add("BrandKit", bk, name)
    lay = auto_layout("sale", "ig_portrait", "เปิดแล้ววันนี้", "ลด 20%", "เปิด 10:00–20:00",
                      "เปิดทุกวัน", "ซอยสมมติ 1", "แวะมาได้เลย", bk,
                      qr_block("https://example.com/"+name.split()[-1].lower()))
    add("PosterLayout", lay, name)
    add("ShareCard", share_card(name, "เปิดแล้ววันนี้", "sale", "ig_portrait"), name)
    add("QrBlock", qr_block("https://example.com/"+name.split()[-1].lower(), "footer_right"), name)

for items in (
    [{"name_th": "ข้าวกะเพรา", "price_thb": 60}, {"name_th": "ข้าวผัด", "price_thb": 55}, {"name_th": "ชาเย็น", "price_thb": 40}],
    [{"name_th": f"รายการ {i}", "price_thb": 20+i*5} for i in range(1, 8)],
):
    add("MenuGrid", menu_grid(items), f"n{len(items)}")
    for r in items[:3]:
        add("MenuRow", menu_grid([r])["rows"][0], r["name_th"])

for e in ex:
    jsonschema.validate(e["value"], ref(e["def"]))

d = os.path.dirname(os.path.abspath(__file__)) + "/.."
json.dump(schema, open(d + "/schemas.json", "w"), ensure_ascii=False, indent=1)
json.dump({"examples": ex}, open(d + "/examples.json", "w"), ensure_ascii=False, indent=1)
print(len(defs), "defs,", len(ex), "examples, all valid")
