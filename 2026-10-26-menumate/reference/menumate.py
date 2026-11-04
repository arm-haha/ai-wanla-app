"""MenuMate (อ่านเมนูไม่ออก) — deterministic reference logic.

The AI (vision LLM) does: read menu photo -> MenuItem list (original text, Thai name,
description, price, spice, allergens). Everything below is plain code so the app
stays predictable, testable and cheap: currency, safety flags, budget order
builder, point-to-order card, bill check, trip wrapped.
"""
from __future__ import annotations
import math

SAFE, WARN, AVOID = "safe", "warn", "avoid"

# Diet rules: pref key -> ingredient tags that break it
DIET_RULES = {
    "no_pork": {"pork", "lard"},
    "no_beef": {"beef"},
    "halal": {"pork", "lard", "alcohol"},
    "vegetarian": {"pork", "beef", "chicken", "seafood", "fish", "lard"},
}

def to_thb(amount_local: float, rate_thb_per_unit: float) -> int:
    """Convert to baht, rounded to nearest baht."""
    if rate_thb_per_unit <= 0:
        raise ValueError("rate must be > 0")
    return int(math.floor(amount_local * rate_thb_per_unit + 0.5))

def flag_item(item: dict, prefs: dict) -> dict:
    """Return {'level': safe|warn|avoid, 'reasons': [...]} for one menu item."""
    reasons, level = [], SAFE
    tags = set(item.get("ingredients", [])) | set(item.get("allergens", []))
    for a in prefs.get("allergies", []):
        if a in tags:
            reasons.append(f"แพ้{a}"); level = AVOID
    for d in prefs.get("diets", []):
        hit = DIET_RULES.get(d, set()) & tags
        if hit:
            reasons.append(f"{d}: มี {', '.join(sorted(hit))}"); level = AVOID
    if level != AVOID:
        tol = prefs.get("spice_tolerance", 3)
        if item.get("spice_level", 0) > tol:
            reasons.append(f"เผ็ดระดับ {item['spice_level']} เกินที่รับได้ ({tol})"); level = WARN
        if item.get("confidence", 1.0) < 0.6:
            reasons.append("AI อ่านไม่ชัด ถามพนักงานก่อน"); level = WARN
    return {"level": level, "reasons": reasons}

def build_order(items: list[dict], budget_local: float, party_size: int, prefs: dict) -> dict:
    """Greedy budget plan: 1 main per person (highest must_try first), then add
    sides/drinks by must_try while staying within budget. Only SAFE items."""
    if party_size < 1:
        raise ValueError("party_size >= 1")
    safe = [i for i in items if flag_item(i, prefs)["level"] == SAFE]
    by_score = lambda i: (-i.get("must_try", 0), i["price"], i["id"])
    mains = sorted([i for i in safe if i["category"] == "main"], key=by_score)
    others = sorted([i for i in safe if i["category"] != "main"], key=by_score)
    picks, total = [], 0
    for m in mains:
        if len([p for p in picks if p["category"] == "main"]) >= party_size:
            break
        if total + m["price"] <= budget_local:
            picks.append(m); total += m["price"]
    for o in others:
        if total + o["price"] <= budget_local:
            picks.append(o); total += o["price"]
    return {
        "budget_local": budget_local,
        "party_size": party_size,
        "pick_ids": [p["id"] for p in picks],
        "total_local": total,
        "left_local": budget_local - total,
        "per_person_local": round(total / party_size, 2),
        "mains_covered": len([p for p in picks if p["category"] == "main"]) >= party_size,
    }

POINT_HEADERS = {
    "ja": ("こちらをお願いします", "個", "ありがとうございます"),
    "ko": ("이거 주세요", "개", "감사합니다"),
    "zh": ("我要点这些", "份", "谢谢"),
    "en": ("I'd like to order these, please", "x", "Thank you"),
}

def point_card(items: list[dict], order: dict, lang: str, note_local: str | None = None) -> dict:
    """Show-the-waiter card in the menu's own language (original names, never AI translation)."""
    head, unit, thanks = POINT_HEADERS.get(lang, POINT_HEADERS["en"])
    idx = {i["id"]: i for i in items}
    counts: dict[str, int] = {}
    for pid in order["pick_ids"]:
        counts[pid] = counts.get(pid, 0) + 1
    lines = [{"original_name": idx[k]["original_name"], "qty": v,
              "line": f"{idx[k]['original_name']} × {v}{unit if lang != 'en' else ''}"}
             for k, v in counts.items()]
    return {"lang": lang, "header": head, "lines": lines,
            "note_local": note_local, "footer": thanks}

def bill_check(order_items: list[dict], receipt_lines: list[dict],
               tax_rate: float = 0.0, service_rate: float = 0.0) -> dict:
    """Compare what we ordered vs receipt. Flags extra lines, missing lines, and math gap."""
    ordered = {}
    for i in order_items:
        ordered[i["original_name"]] = ordered.get(i["original_name"], 0) + i["price"]
    billed = {}
    for r in receipt_lines:
        billed[r["name"]] = billed.get(r["name"], 0) + r["amount"]
    extra = sorted(k for k in billed if k not in ordered)
    missing = sorted(k for k in ordered if k not in billed)
    price_diff = sorted(k for k in ordered if k in billed and billed[k] != ordered[k])
    subtotal = sum(ordered.values())
    expected = int(math.floor(subtotal * (1 + tax_rate + service_rate) + 0.5))
    receipt_total = sum(billed.values())
    ok = not extra and not price_diff and receipt_total <= expected
    return {"expected_total": expected, "receipt_total": receipt_total,
            "gap": receipt_total - expected, "extra_lines": extra,
            "missing_lines": missing, "price_mismatch": price_diff, "ok": ok}

def split_even(total_local: float, people: int, rate: float) -> dict:
    per = round(total_local / people, 2)
    return {"per_person_local": per, "per_person_thb": to_thb(per, rate)}

def trip_wrapped(meals: list[dict], rate: float) -> dict:
    """meals: [{city, total_local, items_tried, avoided}] -> shareable stats."""
    spent = sum(m["total_local"] for m in meals)
    tried = sum(m["items_tried"] for m in meals)
    avoided = sum(m["avoided"] for m in meals)
    top = max(meals, key=lambda m: m["total_local"]) if meals else None
    return {"meals": len(meals), "dishes_tried": tried, "allergy_dodged": avoided,
            "spent_local": spent, "spent_thb": to_thb(spent, rate),
            "biggest_meal_city": top["city"] if top else None}
