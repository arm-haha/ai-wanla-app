"""Generate ../schemas.json + ../examples.json and validate every example."""
import json, os, jsonschema
from handfont import *
from fixtures import *

S = "https://json-schema.org/draft/2020-12/schema"
s = {"type": "string"}; b = {"type": "boolean"}; ns = {"type": ["string", "null"]}
u = {"type": "number", "minimum": 0, "maximum": 1}; num = {"type": "number"}
i0 = {"type": "integer", "minimum": 0}; i1 = {"type": "integer", "minimum": 1}
pct = {"type": "integer", "minimum": 0, "maximum": 100}
hexc = {"type": "string", "pattern": "^#[0-9A-F]{6}$"}
date = {"type": "string", "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}$"}
arr = lambda x, **k: dict({"type": "array", "items": x}, **k)
R = lambda n: {"$ref": "#/$defs/" + n}


def obj(props, req=None, extra=False):
    return {"type": "object", "required": req if req is not None else list(props), "properties": props, "additionalProperties": extra}


tmpl = {"enum": list(TEMPLATES)}; setn = {"enum": list(SETS)}
defs = {
    "Person": obj({"id": s, "name_th": s, "name_en": s, "age": {"type": "integer", "minimum": 5, "maximum": 110}, "city_th": s, "use_th": s}),
    "SheetPhoto": obj({"id": s, "light": u, "blur": u, "skew_deg": {"type": "number", "minimum": -45, "maximum": 45}, "ink_contrast": u}),
    "ScanQuality": obj({"score": pct, "ok": b, "tips_th": arr(s)}),
    "SheetScan": obj({"photo_id": s, "quality": R("ScanQuality")}),
    "TemplateSheet": obj({"template": tmpl, "name_th": s, "cells": i1, "pages": i1, "sets": arr(setn, minItems=1), "guide": s, "tips_th": arr(s)}),
    "AiGlyphExtract": obj({"sheet_id": s, "corners_found": b, "cells": arr(R("GlyphCell")), "signature_like": b, "personal_data": b,
                           "handwriting_style": {"enum": ["round", "loopless", "cursive", "print", "mixed"]}, "confidence": u, "notes_th": s},
                          ["sheet_id", "corners_found", "cells", "signature_like", "personal_data", "handwriting_style", "confidence"]),
    "GlyphCell": obj({"char": {"type": "string", "minLength": 1, "maxLength": 1}, "ink": u, "touches_border": b, "extra_blobs": i0}),
    "GlyphCheck": obj({"char": s, "status": {"enum": ["ok", "empty", "too_faint", "overflow", "messy"]}, "usable": b, "fix_th": ns}),
    "Coverage": obj({"template": tmpl, "total": i1, "usable": i0, "percent": pct, "core_percent": pct, "missing": arr(s, maxItems=40), "can_build": b, "fallback_th": ns}),
    "ConsentCheck": obj({"allowed": b, "level": {"enum": ["ok", "warn", "stop"]}, "flags": arr({"enum": [k for k in GUARD if k]}), "messages_th": arr(s, minItems=1)}),
    "MarkPlacement": obj({"base": s, "cut_descender": b, "marks": arr(obj({"mark": s, "kind": {"enum": ["upper_vowel", "lower_vowel", "tone"]},
                                                                            "dx": {"type": "integer"}, "dy": {"type": "integer"}, "note_th": ns}))}),
    "StyleParams": obj({"weight": {"enum": list(WEIGHTS)}, "stroke": i1, "slant": {"type": "number", "minimum": -15, "maximum": 15},
                        "roughness": {"enum": list(ROUGH)}, "rough": u, "tracking": {"type": "number", "minimum": -50, "maximum": 100},
                        "baseline_jitter": i0, "alternates": {"type": "integer", "minimum": 1, "maximum": 3}}),
    "FontBuild": obj({"ok": b, "family": {"type": "string", "pattern": "^HandFont-[A-Za-z0-9]+$"}, "format": {"enum": list(EXPORTS)},
                      "glyphs": i0, "alternates": i0, "size_kb": i0, "reason_th": ns}),
    "TextPreview": obj({"text": s, "size_pt": i1, "lines": arr(s), "line_count": i0, "clusters": i0, "alternates_used": i1}),
    "CardLayout": obj({"kind": {"enum": list(CARDS)}, "name_th": s, "size": {"enum": ["A5", "A6", "A7"]}, "paper": {"enum": list(PAPERS)},
                       "paper_hex": hexc, "ink": {"enum": list(INKS)}, "ink_hex": hexc, "chars": i0, "max_chars": i1, "fits": b,
                       "font_pt": {"enum": [18, 22, 28]}, "warning_th": ns}),
    "StickerExport": obj({"text": s, "format": {"const": "png_sticker"}, "ink_hex": hexc, "outline": b, "width_px": i1, "height_px": i1, "transparent": b}),
    "PracticeSheet": obj({"text": s, "rows": {"type": "integer", "minimum": 1, "maximum": 12}, "mode": {"enum": ["trace", "copy", "free"]},
                          "guide_lines": {"enum": [3, 4]}, "opacity": u, "paper": {"const": "A4"}}),
    "PracticeSample": obj({"height_var": u, "baseline_var": u, "spacing_var": u, "slant_var": u}),
    "PracticeScore": obj({"samples": i1, "score": pct, "grade": {"enum": ["A", "B", "C", "D"]},
                          "focus": {"enum": ["height_var", "baseline_var", "spacing_var", "slant_var"]}, "tip_th": s}),
    "ReelShot": obj({"kind": {"enum": [k for k, _ in REEL_SHOTS]}, "start": {"type": "number", "minimum": 0}, "end": num, "caption_th": s}),
    "ReelPlan": obj({"family": s, "seconds": {"type": "integer", "minimum": 15, "maximum": 30}, "ratio": {"const": "9:16"}, "bpm": i1,
                     "shots": arr(R("ReelShot"), minItems=3), "watermark": s}),
    "DiaryEntry": obj({"date": date, "kind": {"enum": ["build", "card", "sticker", "practice"]}, "version": i1, "score": pct}, ["date", "kind"]),
    "DiarySummary": obj({"today": date, "fonts_built": i0, "cards_made": i0, "stickers_made": i0, "practice_streak": i0,
                         "best_score": {"type": ["integer", "null"]}, "improvement": {"type": "integer"}, "latest_version": i0}),
    "ShareCard": obj({"family": s, "sample_text": s, "layout": {"enum": ["before_after", "alphabet_grid", "typed_note"]}, "size": {"const": "1080x1350"},
                      "watermark": s, "badge_th": s}),
    "Quota": obj({"plan": {"enum": ["free", "plus"]}, "builds_per_day": i1, "used": i0, "left": i0, "blocked": b}),
    "SafetyGuard": obj({"flag": {"type": ["string", "null"]}, "level": {"enum": ["ok", "warn", "stop"]}, "message_th": s, "block": b}),
}
schema = {"$schema": S, "$id": "https://github.com/arm-haha/ai-wanla-app/2026-12-18-handfont/schemas.json", "title": "HandFont", "$defs": defs}
ref = lambda n: {"$schema": S, "$defs": defs, "$ref": "#/$defs/" + n}

ex = []
add = lambda d, v, note="": ex.append({"def": d, "note": note, "value": v})
for p in PEOPLE: add("Person", p, p["name_en"])
for ph in PHOTOS: add("SheetPhoto", ph, ph["id"]); add("SheetScan", sheet_scan(ph), ph["id"])
for lt, bl, sk, ic in ((0.9, 0.0, 0, 1.0), (0.65, 0.35, -9, 0.55), (0.75, 0.1, 5, 0.3)): add("ScanQuality", scan_quality(lt, bl, sk, ic), f"{lt},{bl},{sk},{ic}")
for t in TEMPLATES: add("TemplateSheet", template_sheet(t), t)
add("AiGlyphExtract", {"sheet_id": "s01", "corners_found": True, "cells": CELLS[:6], "signature_like": False, "personal_data": False,
                       "handwriting_style": "round", "confidence": 0.93, "notes_th": "ลายมือกลมมน เส้นสม่ำเสมอ"}, "mint")
add("AiGlyphExtract", {"sheet_id": "s09", "corners_found": False, "cells": [], "signature_like": True, "personal_data": True,
                       "handwriting_style": "cursive", "confidence": 0.41}, "signature-ish")
for c in CELLS[:12] + [c for c in CELLS if c["char"] in "ฃฬๆ"]: add("GlyphCell", c, c["char"])
for c in CHECKS[:12] + [c for c in CHECKS if not c["usable"]]: add("GlyphCheck", c, c["char"])
add("GlyphCheck", glyph_check({"char": "A", "ink": 0.6, "touches_border": False, "extra_blobs": 0}), "messy-ink")
add("Coverage", COV, "mint quick")
add("Coverage", coverage("english", [glyph_check({"char": c, "ink": 0.1, "touches_border": False, "extra_blobs": 0}) for c in LAT_UPPER + LAT_LOWER]), "english no digits")
add("Coverage", coverage("thai_quick", [glyph_check(dict(c, ink=0.0)) if i % 2 else glyph_check(c) for i, c in enumerate(CELLS)]), "half")
for a, kw in ((27, {}), (11, {}), (11, {"parent_ok": True}), (30, {"signature": True}), (25, {"purpose": "forgery"}), (33, {"purpose": "resale"})):
    add("ConsentCheck", consent_check(a, True, **kw), f"{a} {kw}")
add("ConsentCheck", consent_check(40, False), "someone else")
for w in ("ก่", "ที่", "ปี่", "ฟื้", "ฎุ", "ญู", "ฐุ", "ป๋", "สั้", "กึ๋"): add("MarkPlacement", mark_placement(w[0], list(w[1:])), w)
for st in (("thin", 0, "clean", 0), ("regular", 4, "natural", 10), ("bold", -6, "sketchy", 30), ("regular", 12, "natural", -20)):
    add("StyleParams", style_params(*st), str(st))
add("FontBuild", BUILD, "mint ttf")
for f in ("otf", "woff2"): add("FontBuild", font_build(PEOPLE[0], "thai_quick", COV, STYLE, f), f)
add("FontBuild", font_build(PEOPLE[1], "thai_quick", COV, style_params("bold", 0, "clean"), "ttf"), "boss clean")
add("FontBuild", font_build(PEOPLE[2], "thai_quick", coverage("thai_quick", [glyph_check(dict(c, ink=0.0)) if i % 2 else glyph_check(c) for i, c in enumerate(CELLS)]), STYLE), "blocked")
for t, mw in ((MSG, 80), ("สุขสันต์วันเกิดนะเพื่อนรัก", 90), ("Happy birthday my dear friend see you soon", 60), ("ขอบคุณที่อุดหนุนนะคะ 🙏", 80), ("รักนะ", 80), ("Thank you for your order!", 50)):
    add("TextPreview", text_preview(t, STYLE, 24, mw), t[:16])
msgs = {"birthday": "สุขสันต์วันเกิดนะแก ขอให้ปีนี้ปังทุกเรื่อง", "thank_you": "ขอบคุณที่ช่วยเหลือกันมาตลอดนะครับ", "love_note": "วันนี้ก็คิดถึงเหมือนเดิม",
        "wedding": "ขอให้รักกันตลอดไป ดูแลกันและกันจนแก่เฒ่า ยินดีด้วยนะทั้งคู่", "new_year": "สวัสดีปีใหม่ 2570 ขอให้สุขภาพแข็งแรงนะหลาน",
        "teacher": MSG, "shop_note": "ขอบคุณที่อุดหนุนนะคะ ใช้แล้วรีวิวด้วยน้า"}
for k, m in msgs.items(): add("CardLayout", card_layout(k, m), k)
add("CardLayout", card_layout("shop_note", "ขอบคุณ" * 20), "too long")
add("CardLayout", card_layout("birthday", "HBD!", "notebook_blue", "white_on_dark"), "custom")
for t, ink in (("555 ขำมาก", "black"), ("ฝันดีนะ", "blue_pen"), ("SALE วันนี้วันเดียว ลด 50% ทั้งร้าน", "red_pen"), ("ok", "pencil")): add("StickerExport", sticker_export(t, ink), t)
for a in (("กขค", 6, "trace"), ("สวัสดีครับ", 8, "copy"), ("abc", 4, "free"), ("ก ไก่ ข ไข่", 12, "trace")): add("PracticeSheet", practice_sheet(*a), a[0])
for sm in SAMPLES: add("PracticeSample", sm)
for sm in (SAMPLES, [{"height_var": 0.05, "baseline_var": 0.05, "spacing_var": 0.1, "slant_var": 0.05}],
           [{"height_var": 0.6, "baseline_var": 0.5, "spacing_var": 0.3, "slant_var": 0.2}], [{"height_var": 0.3, "baseline_var": 0.6, "spacing_var": 0.3, "slant_var": 0.4}]):
    add("PracticeScore", practice_score(sm))
for sec in (15, 20, 30):
    r = reel_plan("HandFont-Mint", sec); add("ReelPlan", r, str(sec))
for sh in reel_plan("HandFont-Mint", 24)["shots"]: add("ReelShot", sh, sh["kind"])
for e in DIARY: add("DiaryEntry", e, e["kind"])
for d in ("2026-12-22", "2026-12-24"): add("DiarySummary", diary_summary(DIARY, d), d)
add("DiarySummary", diary_summary([{"date": TODAY, "kind": "build", "version": 1}], TODAY), "first day")
for lay in ("before_after", "alphabet_grid", "typed_note"): add("ShareCard", share_card("HandFont-Mint", MSG, lay), lay)
for a in ((0,), (1,), (2,), (5, "plus")): add("Quota", quota(*a), str(a))
for f in GUARD: add("SafetyGuard", safety_guard(f), str(f))

for x in ex: jsonschema.validate(x["value"], ref(x["def"]))
d = os.path.dirname(os.path.abspath(__file__)) + "/.."
json.dump(schema, open(d + "/schemas.json", "w"), ensure_ascii=False, indent=1)
json.dump({"examples": ex}, open(d + "/examples.json", "w"), ensure_ascii=False, indent=1)
print(len(defs), "defs,", len(ex), "examples, all valid")
