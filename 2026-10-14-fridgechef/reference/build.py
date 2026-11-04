"""Build ../examples.json and ../schemas.json from the reference engine, then validate."""
import json, pathlib, jsonschema
import fridge as F, fixtures as X
from schema import ROOT

OUT = pathlib.Path(__file__).resolve().parent.parent
COLORS = {"bg": "#F7FAFC", "ink": "#0F172A", "ice": "#38BDF8", "tomato": "#EF4444", "basil": "#22C55E", "yolk": "#FBBF24", "card": "#FFFFFF"}

inv = F.build_inventory(X.DETECTIONS, X.TODAY)
top3 = F.menu_match(inv)
allm = F.menu_match(inv, {"max_missing": 3}, top_n=0)
inv_lime = F.build_inventory(X.DETECTIONS, X.TODAY, confirmed_keys=["lime"])
lime_all = F.menu_match(inv_lime, top_n=0)
radar = F.use_first_radar(inv)
cm = F.cook_mode(top3[0]["recipe_id"])
prog = [F.cook_progress(cm["recipe_id"], 0, s) for s in (0, 120, 180)] + [F.cook_progress(cm["recipe_id"], 1, 0)]
plan_ids = ["kai_pad_kaprao", "pad_kalam_pli", "yum_sai_krok"]
plan = [m for m in lime_all if m["recipe_id"] in plan_ids]
shop = F.shopping_list(plan)
dice_pool = F.menu_match(inv, {"max_missing": 0}, top_n=0)
dice = F.menu_dice(dice_pool, X.DICE_SEED)
today_log = F.cook_log_entry(top3[0], X.TODAY)
history = X.HISTORY + [today_log]
wrapped = F.waste_wrapped(history, "2026-10")
filters_examples = [
    {"filters": {"diet": ["not_spicy"]}, "top3": [m["recipe_id"] for m in F.menu_match(inv, {"diet": ["not_spicy"]})]},
    {"filters": {"time_max": 8}, "top3": [m["recipe_id"] for m in F.menu_match(inv, {"time_max": 8})]},
    {"filters": {"diet": ["vegetarian"]}, "top3": [m["recipe_id"] for m in F.menu_match(inv, {"diet": ["vegetarian"]})]},
    {"filters": {"diet": ["no_pork"], "max_missing": 1}, "top3": [m["recipe_id"] for m in F.menu_match(inv, {"diet": ["no_pork"]})]},
]
t = top3[0]
share_cards = [
    {"kind": "rescue", "size": "1080x1920", "title_th": "ตู้เย็นรอดแล้ว! 🧊",
     "lines_th": [f"{t['emoji']} {t['name_th']}", f"ช่วยของใกล้เสีย {len(t['rescues'])} อย่าง", f"ประหยัด ฿{t['rescue_value_thb']}", f"เวลาทำ {t['time_min']} นาที"],
     "bg": COLORS["bg"], "accent": COLORS["tomato"], "footer": "ทำด้วย FridgeChef · AI วันละแอป"},
    {"kind": "wrapped", "size": "1080x1920", "title_th": "ตุลาคมของปุ๊ก 🍳",
     "lines_th": [f"ทำกินเอง {wrapped['meals_cooked']} มื้อ", f"ช่วยของรอด {wrapped['items_rescued']} อย่าง", f"ประหยัด ฿{wrapped['value_saved_thb']}",
                  f"เมนูประจำ: {wrapped['top_recipe_name_th']}", f"ทำติดกันสูงสุด {wrapped['best_streak_days']} วัน"],
     "bg": COLORS["ink"], "accent": COLORS["yolk"], "footer": "ทำด้วย FridgeChef · AI วันละแอป"},
    {"kind": "menu", "size": "1080x1080", "title_th": "ตู้เย็นฉันทำได้ 3 เมนู",
     "lines_th": [f"{m['emoji']} {m['name_th']} · {m['match_pct']}%" for m in top3], "bg": COLORS["bg"], "accent": COLORS["ice"], "footer": "FridgeChef"},
]
expect_locked = {
    "today": X.TODAY, "detections": len(X.DETECTIONS), "confirmed_chips": sum(i["confirmed"] for i in inv),
    "unconfirmed": [i["key"] for i in inv if not i["confirmed"]],
    "radar_today": radar["groups"]["today"], "radar_at_risk_count": radar["at_risk_count"], "radar_at_risk_value_thb": radar["at_risk_value_thb"],
    "top3": [m["recipe_id"] for m in top3], "top3_scores": [m["score"] for m in top3],
    "top1_rescues": t["rescues"], "top1_rescue_value_thb": t["rescue_value_thb"],
    "cook_steps": len(cm["steps"]), "cook_total_timer_s": cm["total_timer_s"],
    "after_confirm_lime_new_menus": sorted({m["recipe_id"] for m in lime_all} - {m["recipe_id"] for m in F.menu_match(inv, top_n=0)}),
    "shopping_total_thb": shop["total_thb"], "dice_pick": dice["pick"],
    "wrapped_meals": wrapped["meals_cooked"], "wrapped_items": wrapped["items_rescued"], "wrapped_value_thb": wrapped["value_saved_thb"],
    "wrapped_top": wrapped["top_recipe_id"], "wrapped_streak": wrapped["best_streak_days"],
}
catalog = [{"key": k, "name_th": v[0], "emoji": v[1], "category": v[2], "shelf_life_days": v[3], "unit_th": v[4], "price_thb": v[5], "store": v[6]} for k, v in F.CATALOG.items()]
ui = {
    "home_title": "วันนี้ตู้เย็นทำอะไรได้บ้าง?", "scan_cta": "📸 ถ่ายตู้เย็น", "demo_cta": "ลองข้อมูลตัวอย่าง (ตู้เย็นปุ๊ก)",
    "scanning": "กำลังส่องตู้เย็น…", "chips_title": "เจอ {n} อย่าง แตะเพื่อแก้", "chip_unsure": "{name} ใช่ไหม?",
    "radar_today": "ใช้วันนี้", "radar_soon": "ใช้เร็ว", "radar_ok": "สบาย", "radar_check": "เช็กก่อนกิน",
    "menu_title": "ทำได้เลย {n} เมนู", "badge_ready": "ทำได้เลย ✅", "badge_missing": "ขาดอีก {n} อย่าง",
    "rescue_pill": "ช่วยของใกล้เสีย ฿{v}", "cook_start": "เริ่มทำเลย 👩‍🍳", "timer_done": "ครบเวลา! ไปขั้นต่อไป",
    "list_title": "ของที่ต้องซื้อเพิ่ม", "list_share": "ส่งเข้า LINE", "dice_cta": "🎲 กินอะไรดี สุ่มเลย",
    "wrapped_cta": "ดูสรุปเดือนนี้", "share_cta": "แชร์การ์ด", "empty_fridge": "ตู้เย็นว่างจัง… ลองพิมพ์ของที่มีแทนได้นะ",
    "safety_note": "วันหมดอายุเป็นค่าประมาณ ดม/ดูก่อนกินเสมอ", "allergy_note": "เช็กส่วนผสมถ้าแพ้อาหาร",
}
reel = [
    {"t": "0–3s", "shot": "เปิดตู้เย็นรก ๆ กล้องมือถือ POV", "text": "ตู้เย็นแบบนี้… ทำอะไรกินได้?"},
    {"t": "3–7s", "shot": "กดถ่าย → กรอบสแกนวิ่งบนรูป → chips 12 อย่างเด้งเข้าถาด", "text": "ถ่ายรูปเดียว AI นับให้ 12 อย่าง"},
    {"t": "7–11s", "shot": "Use-First Radar วงแดง 4 อย่าง ‘ใช้วันนี้’", "text": "หมูสับ กะเพรา ข้าว ต้นหอม ต้องใช้วันนี้!"},
    {"t": "11–16s", "shot": "การ์ด 3 เมนูสไลด์ขึ้น ‘กะเพราหมูสับไข่ดาว 100%’ + pill ‘ช่วยของ ฿60’", "text": "ได้ 3 เมนู ไม่ต้องออกไปซื้อ"},
    {"t": "16–23s", "shot": "Cook Mode จับเวลาไข่ดาว 3:00 → ตัดเสียงฉ่า ผัดกะเพรา", "text": "มีจับเวลาทุกขั้น"},
    {"t": "23–27s", "shot": "แตะ ‘มะนาว ใช่ไหม?’ → เมนูยำโผล่ / ลิสต์ซื้อของส่ง LINE / ลูกเต๋าสุ่ม", "text": "+ลิสต์ซื้อของ +สุ่มเมนู"},
    {"t": "27–30s", "shot": "จานกะเพราจริง + การ์ด Wrapped ‘ประหยัด ฿225’", "text": "คอมเมนต์ ‘ตู้เย็น’ รับลิงก์ฟรี"},
]
tv = [
    {"id": "tv01", "fn": "expiry_status", "input": [1], "expect": "today"},
    {"id": "tv02", "fn": "expiry_status", "input": [3], "expect": "soon"},
    {"id": "tv03", "fn": "expiry_status", "input": [-1], "expect": "check"},
    {"id": "tv04", "fn": "build_inventory.days_left[pork_minced]", "input": {"added_on": "2026-10-12", "today": X.TODAY}, "expect": 1},
    {"id": "tv05", "fn": "build_inventory.confirmed[lime]", "input": {"confidence": 0.41}, "expect": False},
    {"id": "tv06", "fn": "menu_match.top3", "input": "demo", "expect": expect_locked["top3"]},
    {"id": "tv07", "fn": "menu_match.top3.scores", "input": "demo", "expect": expect_locked["top3_scores"]},
    {"id": "tv08", "fn": "match_recipe[kai_pad_kaprao].missing_required", "input": "demo", "expect": ["chicken"]},
    {"id": "tv09", "fn": "use_first_radar.at_risk_value_thb", "input": "demo", "expect": radar["at_risk_value_thb"]},
    {"id": "tv10", "fn": "cook_mode.total_timer_s", "input": cm["recipe_id"], "expect": cm["total_timer_s"]},
    {"id": "tv11", "fn": "cook_progress", "input": [cm["recipe_id"], 0, 120], "expect": {"remaining_s": 60, "timer_done": False}},
    {"id": "tv12", "fn": "confirm lime → new menus", "input": "demo", "expect": expect_locked["after_confirm_lime_new_menus"]},
    {"id": "tv13", "fn": "shopping_list.total_thb", "input": plan_ids, "expect": shop["total_thb"]},
    {"id": "tv14", "fn": "menu_dice.pick", "input": X.DICE_SEED, "expect": dice["pick"]},
    {"id": "tv15", "fn": "waste_wrapped", "input": "2026-10", "expect": {k: wrapped[k] for k in ("meals_cooked","items_rescued","value_saved_thb","best_streak_days")}},
    {"id": "tv16", "fn": "menu_match filter not_spicy excludes spicy", "input": {"diet": ["not_spicy"]}, "expect": filters_examples[0]["top3"]},
]
examples = {
    "meta": {"app": "FridgeChef", "app_th": "ตู้เย็นเชฟ", "date": X.TODAY, "channel": "AI วันละแอป", "version": 1,
             "note": "ทุกตัวเลขมาจาก reference/fridge.py (deterministic) · persona สมมติ"},
    "colors": COLORS, "persona": X.PERSONA, "staples": F.STAPLES, "catalog": catalog, "recipes": F.RECIPES,
    "demo_input": {"today": X.TODAY, "detections": X.DETECTIONS, "dice_seed": X.DICE_SEED},
    "expect_locked": expect_locked, "inventory": inv, "radar": radar, "menu_top3": top3, "menu_all": allm,
    "confirm_lime_rerun": {"confirmed_keys": ["lime"], "menus": lime_all}, "filters_examples": filters_examples,
    "cook_mode": cm, "cook_progress": prog, "shopping_plan_ids": plan_ids, "shopping_list": shop,
    "dice_pool": [m["recipe_id"] for m in dice_pool], "dice": dice,
    "history": history, "wrapped": wrapped, "share_cards": share_cards,
    "local_store_example": {"version": 1, "inventory": inv[:3], "history": history[-2:], "shopping": shop,
                            "settings": {"staples": F.STAPLES, "diet": [], "household": 1, "stove": "electric_1", "ai_vision": False},
                            "last_scan_at": "2026-10-14T18:05:00+07:00"},
    "ai_examples": {
        "vision_request": {"image_base64": "<base64 jpeg ≤1MB>", "allowed_keys": list(F.CATALOG), "locale": "th-TH"},
        "vision_response": {"detections": [{"key": d["key"], "qty": d["qty"], "confidence": d["confidence"], "bbox": d["bbox"]} for d in X.DETECTIONS[:3]],
                            "unknown_items_th": ["ซอสในขวดสีแดง (อ่านฉลากไม่ออก)"]},
        "recipe_request": {"have": sorted(F.usable_keys(inv)), "staples": F.STAPLES, "diet": [], "time_max": 15},
        "recipe_response": {"recipes": [F.RECIPE_BY_ID["khai_jiao_moo_sap"]], "disclaimer_th": "สูตรจาก AI ตรวจความสุกของเนื้อสัตว์ก่อนกิน"},
    },
    "ui_copy_th": ui, "reel_script": reel, "test_vectors": tv,
}
schema = ROOT
jsonschema.Draft202012Validator.check_schema(schema)
v = jsonschema.Draft202012Validator(schema)
def chk(path, inst, defname):
    errs = list(jsonschema.Draft202012Validator({"$ref": f"#/$defs/{defname}", "$defs": schema["$defs"]}).iter_errors(inst))
    assert not errs, (path, errs[0].message)
errs = list(v.iter_errors(examples)); assert not errs, errs[0].message
for i in inv: chk("inventory", i, "InventoryItem")
for m in allm + lime_all: chk("menu", m, "MenuMatch")
for r in F.RECIPES: chk("recipe", r, "Recipe")
for c in catalog: chk("catalog", c, "CatalogItem")
for d in X.DETECTIONS: chk("det", d, "Detection")
for c in share_cards: chk("card", c, "ShareCard")
for p in prog: chk("prog", p, "CookProgress")
for h in history: chk("hist", h, "CookLogEntry")
chk("cm", cm, "CookMode"); chk("radar", radar, "Radar"); chk("shop", shop, "ShoppingList"); chk("dice", dice, "DiceResult")
chk("wrapped", wrapped, "Wrapped"); chk("store", examples["local_store_example"], "LocalStore")
for k, d in [("vision_request","AiVisionRequest"),("vision_response","AiVisionResponse"),("recipe_request","AiRecipeRequest"),("recipe_response","AiRecipeResponse")]:
    chk(k, examples["ai_examples"][k], d)
for t_ in tv: chk("tv", t_, "TestVector")
(OUT / "examples.json").write_text(json.dumps(examples, ensure_ascii=False, indent=2))
(OUT / "schemas.json").write_text(json.dumps(schema, ensure_ascii=False, indent=2))
print("OK defs=", len(schema["$defs"]), "tv=", len(tv))
print(json.dumps(expect_locked, ensure_ascii=False, indent=1))
print(json.dumps(filters_examples, ensure_ascii=False))
print(shop["line_text"]); print(dice); print(wrapped)
