"""FridgeChef reference engine (deterministic). Port 1:1 to TypeScript (lib/fridge.ts).
All numbers in examples.json are produced by this file. No randomness except seeded dice.
"""
from __future__ import annotations
from datetime import date

CONFIDENCE_MIN = 0.60          # chips below this are shown as "ใช่ไหม?" and excluded until confirmed
STAPLES = ["fish_sauce", "soy_sauce", "oyster_sauce", "sugar", "oil", "salt", "pepper"]

# key: (name_th, emoji, category, shelf_life_days, unit_th, price_thb_per_pack, store)
CATALOG = {
    "egg":          ("ไข่ไก่", "🥚", "protein", 21, "ฟอง", 5, "7-Eleven"),
    "pork_minced":  ("หมูสับ", "🥩", "protein", 3, "กรัม", 40, "ตลาด"),
    "chicken":      ("อกไก่", "🍗", "protein", 2, "กรัม", 45, "ตลาด"),
    "sausage":      ("ไส้กรอก", "🌭", "protein", 14, "ชิ้น", 39, "7-Eleven"),
    "egg_tofu":     ("เต้าหู้ไข่", "🧈", "protein", 10, "หลอด", 12, "7-Eleven"),
    "holy_basil":   ("ใบกะเพรา", "🌿", "herb", 4, "กำ", 10, "ตลาด"),
    "spring_onion": ("ต้นหอม", "🧅", "herb", 5, "ต้น", 10, "ตลาด"),
    "chili":        ("พริกขี้หนู", "🌶️", "herb", 7, "กำ", 5, "ตลาด"),
    "garlic":       ("กระเทียม", "🧄", "herb", 30, "หัว", 10, "ตลาด"),
    "lime":         ("มะนาว", "🍋", "herb", 14, "ลูก", 5, "ตลาด"),
    "tomato":       ("มะเขือเทศ", "🍅", "veg", 7, "ลูก", 10, "ตลาด"),
    "carrot":       ("แครอท", "🥕", "veg", 14, "หัว", 8, "ตลาด"),
    "cabbage":      ("กะหล่ำปลี", "🥬", "veg", 10, "หัว", 25, "ตลาด"),
    "onion":        ("หอมใหญ่", "🧅", "veg", 30, "หัว", 10, "ตลาด"),
    "cooked_rice":  ("ข้าวสวย", "🍚", "carb", 2, "ถ้วย", 10, "7-Eleven"),
    "glass_noodle": ("วุ้นเส้น", "🍜", "carb", 180, "ห่อ", 12, "7-Eleven"),
    "milk":         ("นมจืด", "🥛", "dairy", 7, "กล่อง", 25, "7-Eleven"),
}

RECIPES = [
    {"id": "kaprao_moo_kai_dao", "name_th": "กะเพราหมูสับไข่ดาว", "emoji": "🍳", "time_min": 12, "tags": ["spicy", "pork"],
     "required": ["pork_minced", "holy_basil", "chili", "garlic", "cooked_rice"], "optional": ["egg"],
     "steps": [["ทอดไข่ดาวให้ขอบกรอบ", 180], ["โขลกพริก+กระเทียมหยาบ ๆ", 0], ["ผัดพริกกระเทียมให้หอม ใส่หมูสับผัดจนสุก", 240],
               ["ปรุงซอสหอยฯ ซีอิ๊ว น้ำปลา น้ำตาลนิด", 0], ["ปิดไฟ ใส่ใบกะเพรา คลุกเร็ว ๆ", 30], ["ตักราดข้าว วางไข่ดาว", 0]]},
    {"id": "khao_pad_sausage", "name_th": "ข้าวผัดไส้กรอก", "emoji": "🍛", "time_min": 10, "tags": ["pork", "kid_friendly"],
     "required": ["cooked_rice", "sausage", "egg", "garlic"], "optional": ["tomato", "spring_onion", "carrot", "onion"],
     "steps": [["หั่นไส้กรอก แครอท มะเขือเทศ", 0], ["เจียวกระเทียม ใส่ไส้กรอกผัด", 120], ["ตอกไข่ ยีให้สุก", 60],
               ["ใส่ข้าว ผัดให้ร่วน ปรุงซีอิ๊ว", 180], ["โรยต้นหอม", 0]]},
    {"id": "tom_jued_tofu_moo", "name_th": "ต้มจืดเต้าหู้หมูสับ", "emoji": "🍲", "time_min": 15, "tags": ["pork", "not_spicy", "kid_friendly"],
     "required": ["egg_tofu", "pork_minced", "garlic"], "optional": ["spring_onion", "carrot", "cabbage", "glass_noodle"],
     "steps": [["ต้มน้ำให้เดือด ใส่กระเทียมทุบ", 240], ["ปั้นหมูสับเป็นก้อน ใส่ลงหม้อ", 180],
               ["ใส่แครอท เต้าหู้ไข่หั่นแว่น", 180], ["ปรุงซีอิ๊ว+น้ำปลา โรยต้นหอม", 0]]},
    {"id": "khai_jiao_moo_sap", "name_th": "ไข่เจียวหมูสับฟู ๆ", "emoji": "🥚", "time_min": 8, "tags": ["pork", "not_spicy", "kid_friendly"],
     "required": ["egg", "pork_minced"], "optional": ["spring_onion", "tomato", "onion"],
     "steps": [["ตีไข่+หมูสับ+น้ำปลา ให้ขึ้นฟอง", 60], ["น้ำมันร้อนจัด เทไข่สูง ๆ", 90], ["กลับด้าน ทอดอีกนิด", 60], ["ตักพักสะเด็ดน้ำมัน", 0]]},
    {"id": "khai_tun_nom", "name_th": "ไข่ตุ๋นนมสด (ไมโครเวฟ)", "emoji": "🍮", "time_min": 10, "tags": ["not_spicy", "vegetarian", "microwave_ok", "kid_friendly"],
     "required": ["egg", "milk"], "optional": ["spring_onion", "carrot"],
     "steps": [["ตีไข่ 2 ฟอง + นม ครึ่งแก้ว + ซีอิ๊วนิด", 0], ["กรองใส่ถ้วย ปิดฟิล์มเจาะรู", 0], ["ไมโครเวฟไฟกลาง", 240], ["พัก 1 นาทีให้เซ็ตตัว", 60]]},
    {"id": "khai_pad_makheua_thet", "name_th": "ไข่ผัดมะเขือเทศ", "emoji": "🍅", "time_min": 8, "tags": ["not_spicy", "vegetarian"],
     "required": ["egg", "tomato", "garlic"], "optional": ["spring_onion", "onion"],
     "steps": [["ผัดไข่ให้สุกครึ่ง ๆ ตักพัก", 60], ["ผัดกระเทียม+มะเขือเทศให้นุ่ม", 120], ["ใส่ไข่กลับ ปรุงซอสหอยฯ+น้ำตาลนิด", 30], ["โรยต้นหอม", 0]]},
    {"id": "khao_tom_moo", "name_th": "ข้าวต้มหมูสับ", "emoji": "🥣", "time_min": 12, "tags": ["pork", "not_spicy"],
     "required": ["cooked_rice", "pork_minced", "garlic"], "optional": ["spring_onion", "egg"],
     "steps": [["เจียวกระเทียมพักไว้", 60], ["ต้มน้ำ ใส่หมูสับปั้นก้อน", 180], ["ใส่ข้าวสวย ต้มต่อ", 240], ["ปรุง ตอกไข่ โรยต้นหอม+กระเทียมเจียว", 60]]},
    {"id": "yum_woon_sen", "name_th": "ยำวุ้นเส้นหมูสับ", "emoji": "🥗", "time_min": 15, "tags": ["spicy", "pork"],
     "required": ["glass_noodle", "pork_minced", "tomato", "chili", "lime"], "optional": ["onion", "spring_onion"],
     "steps": [["แช่วุ้นเส้นให้นิ่ม ลวกพัก", 120], ["ลวกหมูสับให้สุก", 90], ["ผสมน้ำยำ มะนาว น้ำปลา น้ำตาล พริก", 0], ["คลุกทุกอย่าง ชิมรสจัด ๆ", 0]]},
    {"id": "yum_sai_krok", "name_th": "ยำไส้กรอกแซ่บ", "emoji": "🌭", "time_min": 10, "tags": ["spicy", "pork"],
     "required": ["sausage", "tomato", "chili", "lime", "onion"], "optional": ["spring_onion"],
     "steps": [["ทอด/ลวกไส้กรอก หั่นเฉียง", 120], ["หั่นหอมใหญ่ มะเขือเทศ", 0], ["ผสมน้ำยำ", 0], ["คลุกให้เข้ากัน", 0]]},
    {"id": "pad_kalam_pli", "name_th": "กะหล่ำปลีผัดน้ำปลา", "emoji": "🥬", "time_min": 8, "tags": ["not_spicy", "vegetarian"],
     "required": ["cabbage", "garlic"], "optional": ["carrot"],
     "steps": [["ฉีกกะหล่ำเป็นชิ้น", 0], ["เจียวกระเทียมจนเหลือง", 60], ["ไฟแรง ใส่กะหล่ำ+แครอท ผัด", 120], ["ปรุงน้ำปลา+น้ำตาล", 0]]},
    {"id": "kai_pad_kaprao", "name_th": "กะเพราไก่", "emoji": "🍗", "time_min": 12, "tags": ["spicy"],
     "required": ["chicken", "holy_basil", "chili", "garlic", "cooked_rice"], "optional": ["egg"],
     "steps": [["สับไก่", 0], ["ผัดพริกกระเทียม ใส่ไก่", 240], ["ปรุง ใส่กะเพรา", 30]]},
    {"id": "sausage_omelet_roll", "name_th": "ไข่ม้วนไส้กรอก", "emoji": "🌯", "time_min": 10, "tags": ["pork", "not_spicy", "kid_friendly"],
     "required": ["egg", "sausage"], "optional": ["spring_onion", "carrot"],
     "steps": [["ตีไข่ ใส่ต้นหอม+แครอทซอย", 0], ["เทไข่บาง ๆ วางไส้กรอก ม้วน", 120], ["เทไข่ชั้นสองม้วนต่อ", 120], ["หั่นเฉียงจัดจาน", 0]]},
]
RECIPE_BY_ID = {r["id"]: r for r in RECIPES}


def _d(s: str) -> date:
    return date.fromisoformat(s)


def expiry_status(days_left: int) -> str:
    if days_left < 0:
        return "check"      # เช็กก่อนกิน (ไม่แนะนำในเมนู)
    if days_left <= 1:
        return "today"      # ใช้วันนี้ (แดง)
    if days_left <= 3:
        return "soon"       # ใช้เร็ว (เหลือง)
    return "ok"             # สบาย (เขียว)


def build_inventory(detections: list[dict], today: str, confirmed_keys: list[str] | None = None,
                    removed_keys: list[str] | None = None) -> list[dict]:
    """detections: [{key, qty, added_on, confidence}] from vision (or demo). Returns inventory sorted by days_left asc then key."""
    confirmed_keys = confirmed_keys or []
    removed_keys = removed_keys or []
    t = _d(today)
    inv = []
    for det in detections:
        k = det["key"]
        if k not in CATALOG or k in removed_keys:
            continue
        name, emoji, cat, shelf, unit, price, store = CATALOG[k]
        conf = det.get("confidence", 1.0)
        confirmed = conf >= CONFIDENCE_MIN or k in confirmed_keys
        days_left = shelf - (t - _d(det["added_on"])).days
        inv.append({"key": k, "name_th": name, "emoji": emoji, "category": cat, "qty": det["qty"], "unit_th": unit,
                    "added_on": det["added_on"], "shelf_life_days": shelf, "days_left": days_left,
                    "status": expiry_status(days_left), "confidence": conf, "confirmed": confirmed,
                    "price_thb": price})
    inv.sort(key=lambda x: (x["days_left"], x["key"]))
    return inv


def usable_keys(inv: list[dict]) -> set[str]:
    return {i["key"] for i in inv if i["confirmed"] and i["status"] != "check"}


def rescue_bonus(days_left: int) -> int:
    if days_left <= 1:
        return 12
    if days_left <= 3:
        return 6
    return 0


def match_recipe(recipe: dict, inv: list[dict]) -> dict:
    have = usable_keys(inv)
    by_key = {i["key"]: i for i in inv}
    req_have = [k for k in recipe["required"] if k in have]
    req_missing = [k for k in recipe["required"] if k not in have]
    opt_have = [k for k in recipe["optional"] if k in have]
    opt_missing = [k for k in recipe["optional"] if k not in have]
    match_pct = round(100 * len(req_have) / len(recipe["required"]))
    used = req_have + opt_have
    bonus = sum(rescue_bonus(by_key[k]["days_left"]) for k in used)
    rescued = [k for k in used if by_key[k]["days_left"] <= 2]
    score = match_pct + bonus + 2 * len(opt_have) - len(req_missing) * 25 - round(recipe["time_min"] * 0.5)
    return {"recipe_id": recipe["id"], "name_th": recipe["name_th"], "emoji": recipe["emoji"],
            "time_min": recipe["time_min"], "tags": recipe["tags"], "match_pct": match_pct,
            "uses": used, "missing_required": req_missing, "missing_optional": opt_missing,
            "rescues": rescued, "rescue_value_thb": sum(by_key[k]["price_thb"] for k in rescued),
            "score": score,
            "badge_th": "ทำได้เลย ✅" if not req_missing else f"ขาดอีก {len(req_missing)} อย่าง"}


def menu_match(inv: list[dict], filters: dict | None = None, top_n: int = 3) -> list[dict]:
    """filters: {max_missing:int=1, time_max:int|None, diet:[not_spicy|no_pork|vegetarian]}"""
    f = {"max_missing": 1, "time_max": None, "diet": []}
    f.update(filters or {})
    out = []
    for r in RECIPES:
        if f["time_max"] is not None and r["time_min"] > f["time_max"]:
            continue
        if "not_spicy" in f["diet"] and "spicy" in r["tags"]:
            continue
        if "no_pork" in f["diet"] and "pork" in r["tags"]:
            continue
        if "vegetarian" in f["diet"] and "vegetarian" not in r["tags"]:
            continue
        m = match_recipe(r, inv)
        if len(m["missing_required"]) > f["max_missing"]:
            continue
        out.append(m)
    out.sort(key=lambda m: (-m["score"], m["time_min"], m["recipe_id"]))
    return out[:top_n] if top_n else out


def cook_mode(recipe_id: str) -> dict:
    r = RECIPE_BY_ID[recipe_id]
    steps = [{"n": i + 1, "text_th": s, "timer_s": t} for i, (s, t) in enumerate(r["steps"])]
    return {"recipe_id": recipe_id, "name_th": r["name_th"], "steps": steps,
            "total_timer_s": sum(s["timer_s"] for s in steps), "timer_steps": sum(1 for s in steps if s["timer_s"] > 0)}


def cook_progress(recipe_id: str, step_index: int, elapsed_in_step_s: int) -> dict:
    cm = cook_mode(recipe_id)
    st = cm["steps"][step_index]
    remaining = max(0, st["timer_s"] - elapsed_in_step_s) if st["timer_s"] else 0
    done = st["timer_s"] > 0 and remaining == 0
    return {"recipe_id": recipe_id, "step_n": st["n"], "of": len(cm["steps"]), "remaining_s": remaining,
            "timer_done": done, "next_hint_th": ("ไปขั้นต่อไปได้เลย 👉" if (done or st["timer_s"] == 0) else "รอจับเวลา ⏱️")}


def use_first_radar(inv: list[dict]) -> dict:
    groups = {"today": [], "soon": [], "ok": [], "check": []}
    for i in inv:
        if i["confirmed"]:
            groups[i["status"]].append(i["key"])
    at_risk = groups["today"] + groups["soon"]
    return {"groups": groups, "at_risk_count": len(at_risk),
            "at_risk_value_thb": sum(i["price_thb"] for i in inv if i["key"] in at_risk),
            "headline_th": f"ของใกล้เสีย {len(groups['today'])} อย่างต้องใช้วันนี้"}


def shopping_list(matches: list[dict], include_optional: int = 1) -> dict:
    need: list[str] = []
    for m in matches:
        for k in m["missing_required"] + m["missing_optional"][:include_optional]:
            if k not in need:
                need.append(k)
    by_store: dict[str, list[dict]] = {}
    for k in need:
        name, emoji, _c, _s, unit, price, store = CATALOG[k]
        by_store.setdefault(store, []).append({"key": k, "name_th": name, "emoji": emoji, "price_thb": price})
    stores = [{"store": s, "items": by_store[s], "subtotal_thb": sum(x["price_thb"] for x in by_store[s])}
              for s in sorted(by_store)]
    total = sum(s["subtotal_thb"] for s in stores)
    lines = ["🛒 ของที่ต้องซื้อเพิ่ม (FridgeChef)"]
    for s in stores:
        lines.append(f"[{s['store']}]")
        lines += [f"- {x['emoji']} {x['name_th']} ~฿{x['price_thb']}" for x in s["items"]]
    lines.append(f"รวมประมาณ ฿{total}")
    return {"stores": stores, "total_thb": total, "line_text": "\n".join(lines)}


def menu_dice(candidates: list[dict], seed: int) -> dict:
    """LCG (numerical recipes) — same in TS with Math.imul/unsigned. Returns pick + 6 spin frames."""
    x = seed & 0xFFFFFFFF
    frames = []
    for _ in range(6):
        x = (1664525 * x + 1013904223) & 0xFFFFFFFF
        frames.append(candidates[x % len(candidates)]["recipe_id"])
    return {"seed": seed, "frames": frames, "pick": frames[-1]}


def cook_log_entry(match: dict, cooked_on: str) -> dict:
    return {"date": cooked_on, "recipe_id": match["recipe_id"], "rescued": match["rescues"],
            "rescued_value_thb": match["rescue_value_thb"]}


def waste_wrapped(history: list[dict], month: str) -> dict:
    rows = [h for h in history if h["date"].startswith(month)]
    value = sum(h["rescued_value_thb"] for h in rows)
    items = sum(len(h["rescued"]) for h in rows)
    counts: dict[str, int] = {}
    for h in rows:
        counts[h["recipe_id"]] = counts.get(h["recipe_id"], 0) + 1
    top = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[0][0] if counts else None
    days = sorted({h["date"] for h in rows})
    # streak = longest run of consecutive cooked days
    best = cur = 0
    prev = None
    for d in days:
        cur = cur + 1 if prev and (_d(d) - _d(prev)).days == 1 else 1
        best = max(best, cur)
        prev = d
    return {"month": month, "meals_cooked": len(rows), "items_rescued": items, "value_saved_thb": value,
            "top_recipe_id": top, "top_recipe_name_th": RECIPE_BY_ID[top]["name_th"] if top else None,
            "best_streak_days": best,
            "headline_th": f"เดือนนี้ช่วยของในตู้เย็นรอด {items} อย่าง ประหยัด ฿{value}"}
