"""Generate ../schemas.json + ../examples.json and validate every example."""
import json, os, jsonschema
from partypop import *
from fixtures import *

S = "https://json-schema.org/draft/2020-12/schema"
s = {"type": "string"}; b = {"type": "boolean"}; ns = {"type": ["string", "null"]}
u = {"type": "number", "minimum": 0, "maximum": 1}; num = {"type": "number"}; nn = {"type": "number", "minimum": 0}
i0 = {"type": "integer", "minimum": 0}; i1 = {"type": "integer", "minimum": 1}
date = {"type": "string", "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}$"}
dtm = {"type": "string", "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}$"}
hexc = {"type": "string", "pattern": "^#[0-9A-F]{6}$"}
arr = lambda x, **k: dict({"type": "array", "items": x}, **k)
R = lambda n: {"$ref": "#/$defs/" + n}
theme = {"enum": THEME_KEYS}; style = {"enum": list(MENU_STYLES)}; zone = {"enum": sorted({v[1] for v in DECOR.values()})}
flags = {"enum": [k for k in GUARD if k]}
lvl = {"enum": ["ok", "warn", "stop"]}


def obj(props, req=None, extra=False):
    return {"type": "object", "required": req if req is not None else list(props), "properties": props, "additionalProperties": extra}


defs = {
    "User": obj({"id": s, "name_th": s, "name_en": s, "age": {"type": "integer", "minimum": 8, "maximum": 120}, "city_th": s}),
    "Theme": obj({"key": theme, "name_th": s, "name_en": s, "palette": arr(hexc, minItems=6, maxItems=6), "dress_th": s}),
    "DecorItem": obj({"key": {"enum": list(DECOR)}, "name_th": s, "zone": zone, "price": i1, "pack_th": s, "priority": i1,
                      "themes": arr(theme, minItems=1), "qty_rule": s}),
    "AiRoomScan": obj({"room_type": {"enum": ["living", "studio", "office", "dining", "garden", "rooftop"]},
                       "width_m": {"type": "number", "minimum": 1.5, "maximum": 20}, "depth_m": {"type": "number", "minimum": 1.5, "maximum": 20},
                       "tables": i0, "has_balcony": b, "rental": b, "zones": arr({"enum": ["wall", "sofa", "table", "window", "ceiling", "bed", "floor"]}),
                       "light": {"enum": ["warm", "cool", "dim"]}, "clutter": u, "confidence": u}),
    "Room": obj({"room_type": s, "width_m": nn, "depth_m": nn, "area_m2": nn, "wall_m": nn, "tables": i1, "has_balcony": b, "rental": b}),
    "Capacity": obj({"guests": i1, "seated_max": i0, "standing_max": i0, "status": {"enum": ["comfy", "mingle", "over"]},
                     "exit_path_cm": {"const": 80}, "tip_th": s, "flag": {"enum": [None, "over_capacity"]}}),
    "BudgetSplit": obj({"total": i1, "decor": i0, "food": i0, "drinks": i0, "games_gifts": i0, "reserve": i0, "per_head": i0,
                        "food_per_guest": nn, "potluck": b, "tip_th": s}),
    "DecoPick": obj({"key": {"enum": list(DECOR)}, "name_th": s, "zone": zone, "packs": i1, "pack_th": s, "unit_price": i1, "cost": i1, "no_nails": {"const": True}}),
    "DecoPlan": obj({"theme": theme, "theme_th": s, "budget": i0, "spent": i0, "left": i0, "items": arr(R("DecoPick")),
                     "skipped": arr({"enum": list(DECOR)}), "zones": arr(zone), "palette": arr(hexc, minItems=6, maxItems=6)}),
    "RenderPrompt": obj({"keep_layout": {"const": True}, "theme": theme, "palette": arr(hexc), "items_th": s, "forbid": arr(s, minItems=4), "size": {"const": "1080x1350"}}),
    "MenuItem": obj({"key": {"enum": list(FOOD)}, "name_th": s, "need": nn, "unit": s, "buy_qty": nn, "packs": i1, "cost": i0, "section_th": s}),
    "MenuPlan": obj({"style": style, "style_th": s, "adults": i1, "kids": i0, "hours": {"type": "number", "minimum": 1, "maximum": 12},
                     "guest_eq": nn, "items": arr(R("MenuItem"), minItems=1), "total": i0, "allergy_labels": arr(s), "flag": {"enum": [None, "food_allergy"]}}),
    "MenuTrim": obj({"style": style, "total": i0, "potluck_dishes": i0, "changed": b}),
    "ShoppingList": obj({"rows": arr(obj({"name_th": s, "qty_th": s, "section_th": s, "cost": i0, "checked": b}), minItems=1),
                         "sections": arr(obj({"section_th": s, "cost": i0})), "total": i0, "budget": i1, "over_by": i0, "fits": b}),
    "Timeline": obj({"start": dtm, "end": dtm, "tasks": arr(obj({"key": {"enum": [t[1] for t in TASKS]}, "at": dtm, "text_th": s, "done": b}), minItems=3),
                     "flag": {"enum": [None, "noise_late"]}}),
    "GamePlan": obj({"players": i1, "mode": {"enum": ["family", "office", "friends"]}, "kids": i0, "minutes": i0,
                     "games": arr(obj({"key": {"enum": list(GAME)}, "name_th": s, "minutes": i1, "props_th": s, "kid_ok": b})), "drinking_games": {"const": False}}),
    "GiftSwap": obj({"people": {"type": "integer", "minimum": 3}, "seed": {"type": "integer"}, "budget_cap": i1,
                     "pairs": arr(obj({"giver": s, "receiver": s, "code": {"type": "string", "pattern": "^[0-9A-F]{4}$"}}), minItems=3),
                     "secret": {"const": True}, "rule_th": s}),
    "Invite": obj({"host_th": s, "title_th": s, "date_th": s, "time_th": s, "theme": theme, "dress_th": s, "place_th": s, "address_th": ns,
                   "address_hidden": b, "rsvp_by": date, "palette": arr(hexc, minItems=3, maxItems=3), "watermark": s}),
    "CostSplit": obj({"total": i0, "host_pays": i0, "payers": i1, "kids_free": i0, "each": i0, "collected": i0, "extra": i0}),
    "Countdown": obj({"date": date, "days_to_new_year": i1, "be_year": i1, "weekday_th": s}),
    "ShareCard": obj({"kind": {"enum": ["before_after", "invite", "shopping"]}, "size": {"const": "1080x1350"}, "theme": theme,
                      "faces_blurred": {"const": True}, "address_hidden": {"const": True}, "watermark": s}),
    "ReelPlan": obj({"seconds": {"type": "integer", "minimum": 15, "maximum": 30}, "ratio": {"const": "9:16"}, "bpm": i1,
                     "shots": arr(obj({"kind": {"enum": [k for k, _, _ in REEL_SHOTS]}, "start": nn, "end": num, "caption_th": s}), minItems=3), "watermark": s}),
    "Quota": obj({"plan": {"enum": ["free", "plus"]}, "renders_per_day": i1, "used": i0, "left": i0, "blocked": b}),
    "PrivacyCheck": obj({"allowed": b, "level": lvl, "flags": arr(flags), "messages_th": arr(s, minItems=1), "share_allowed": b}),
    "SafetyGuard": obj({"flag": {"type": ["string", "null"]}, "level": lvl, "message_th": s, "block": b}),
}
schema = {"$schema": S, "$id": "https://github.com/arm-haha/ai-wanla-app/2026-12-25-partypop/schemas.json", "title": "PartyPop", "$defs": defs}
ref = lambda n: {"$schema": S, "$defs": defs, "$ref": "#/$defs/" + n}

ex = []
add = lambda dd, v, note="": ex.append({"def": dd, "note": note, "value": v})
for x in (USER, OFFICE, KID): add("User", x, x["name_en"])
for k, (th, en, pal) in THEMES.items(): add("Theme", {"key": k, "name_th": th, "name_en": en, "palette": pal, "dress_th": DRESS[k]}, k)
for k, v in DECOR.items():
    add("DecorItem", {"key": k, "name_th": v[0], "zone": v[1], "price": v[2], "pack_th": v[3], "priority": v[4],
                      "themes": THEME_KEYS if v[5] == "*" else v[5].split(","), "qty_rule": v[6]}, k)
SCANS = (("ห้องนั่งเล่นคุณแพร", SCAN), ("สตูดิโอ", SCAN_SMALL), ("ออฟฟิศ", SCAN_OFFICE))
for n, sc in SCANS: add("AiRoomScan", sc, n); add("Room", room_from_scan(sc), n)
RM = room_from_scan(SCAN)
r_small, r_off = room_from_scan(SCAN_SMALL), room_from_scan(SCAN_OFFICE)
for rm, a, k, n in ((RM, ADULTS, KIDS, "fixture 12"), (RM, 6, 0, "6"), (r_small, 12, 0, "studio 12"), (r_off, 30, 0, "office 30"), (r_small, 4, 1, "studio 5")):
    add("Capacity", capacity(rm, a, k), n)
for tot, a, k in ((BUDGET, ADULTS, KIDS), (1500, ADULTS, KIDS), (12000, 30, 0), (2500, 4, 2)): add("BudgetSplit", budget_split(tot, a, k), "%d/%d+%d" % (tot, a, k))
B = budget_split(BUDGET, ADULTS, KIDS)
PLANS = [deco_plan(RM, THEME, B["decor"], 12)] + [deco_plan(rm, th, bud, g) for rm, th, bud, g in
         ((RM, "cozy_xmas", 1500, 12), (r_small, "pastel_pop", 600, 5), (r_off, "neon_disco", 3000, 30), (RM, "thai_fair", 1200, 12),
          (RM, "minimal_white", 800, 8), (RM, "countdown_gold", 0, 12))]
for p in PLANS: add("DecoPlan", p, "%s %d" % (p["theme"], p["budget"]))
for it in PLANS[0]["items"]: add("DecoPick", it, it["key"])
for p in PLANS[:4]: add("RenderPrompt", render_prompt(RM, p), p["theme"])
MENUS = [menu_plan("suki", ADULTS, KIDS, HOURS), menu_plan("buffet", ADULTS, KIDS, HOURS), menu_plan("snack", ADULTS, KIDS, HOURS),
         menu_plan("buffet", 30, 0, 4), menu_plan("suki", 4, 2, 3, ["กุ้ง"])]
for m in MENUS: add("MenuPlan", m, "%s %d+%d" % (m["style"], m["adults"], m["kids"]))
for it in MENUS[0]["items"]: add("MenuItem", it, it["key"])
for fb in (2480, 1500, 800): add("MenuTrim", trim_menu("suki", ADULTS, KIDS, HOURS, fb), str(fb))
add("ShoppingList", shopping_list(PLANS[0], MENUS[0], B), "fixture fits")
b2 = budget_split(1800, ADULTS, KIDS); add("ShoppingList", shopping_list(deco_plan(RM, THEME, b2["decor"], 12), MENUS[0], b2), "1800 over")
add("Timeline", timeline(START, END, alcohol=True), "new year"); add("Timeline", timeline("2026-12-26T17:00", "2026-12-26T21:00"), "office evening")
add("Timeline", timeline("2026-12-24T18:00", "2026-12-24T22:00"), "christmas eve")
for a in ((12, "family", 3, 60), (30, "office", 0, 60), (8, "friends", 0, 45), (5, "family", 2, 30)): add("GamePlan", game_plan(*a), str(a))
add("GiftSwap", gift_swap(GUESTS, 2027, 300, COUPLES), "fixture"); add("GiftSwap", gift_swap(["ต้น", "ฝน", "บี", "นุ่น", "เจ"], 7, 200), "office 5")
add("Invite", invite("แพร", START, THEME, "คอนโดริมน้ำ นนทบุรี", "ห้อง 1205"), "public")
add("Invite", invite("แพร", START, THEME, "คอนโดริมน้ำ นนทบุรี", "ห้อง 1205", public=False), "private")
add("Invite", invite("ต้น", "2026-12-26T17:00", "neon_disco", "ห้องประชุมชั้น 8", "อาคารสมมติ ชั้น 8"), "office")
S_ = shopping_list(PLANS[0], MENUS[0], B)
add("CostSplit", cost_split(S_["total"], ADULTS, KIDS, PLANS[0]["spent"]), "host pays decor"); add("CostSplit", cost_split(S_["total"], ADULTS, KIDS), "all share")
for dt in ("2026-12-25", "2026-12-31", "2026-11-26"): add("Countdown", countdown(dt), dt)
for k in ("before_after", "invite", "shopping"): add("ShareCard", share_card(k), k)
for sec in (15, 20, 24, 30): add("ReelPlan", reel_plan(sec), str(sec))
for a in ((0,), (2,), (3,), (5, "plus")): add("Quota", quota(*a), str(a))
for a in (((), 32), (("alcohol_minor",), 32), ((), 11), ((), 11, True), (("drink_drive", "noise_late"), 32),
          (tuple(party_flags(kids=3, alcohol=True, driving_guests=2, end_after_midnight=True)), 32), (("photo_of_others",), 32)):
    add("PrivacyCheck", privacy_check(*a), str(a))
for f in GUARD: add("SafetyGuard", safety_guard(f), str(f))

for x in ex: jsonschema.validate(x["value"], ref(x["def"]))
dd = os.path.dirname(os.path.abspath(__file__)) + "/.."
json.dump(schema, open(dd + "/schemas.json", "w"), ensure_ascii=False, indent=1)
json.dump({"examples": ex}, open(dd + "/examples.json", "w"), ensure_ascii=False, indent=1)
print(len(defs), "defs,", len(ex), "examples, all valid")
