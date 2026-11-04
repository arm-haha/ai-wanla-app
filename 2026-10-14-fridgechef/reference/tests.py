"""Run: python3 tests.py — re-computes every test vector in ../examples.json from fridge.py."""
import json, pathlib
import fridge as F, fixtures as X
ex = json.loads((pathlib.Path(__file__).resolve().parent.parent / "examples.json").read_text())
E = ex["expect_locked"]
inv = F.build_inventory(X.DETECTIONS, X.TODAY)
n = 0
def ok(cond, msg):
    global n; assert cond, msg; n += 1
ok(F.expiry_status(1) == "today" and F.expiry_status(3) == "soon" and F.expiry_status(-1) == "check" and F.expiry_status(4) == "ok", "status")
by = {i["key"]: i for i in inv}
ok(by["pork_minced"]["days_left"] == 1, "pork days_left")
ok(by["lime"]["confirmed"] is False, "lime unconfirmed")
top = F.menu_match(inv)
ok([m["recipe_id"] for m in top] == E["top3"], "top3")
ok([m["score"] for m in top] == E["top3_scores"], "scores")
ok(F.match_recipe(F.RECIPE_BY_ID["kai_pad_kaprao"], inv)["missing_required"] == ["chicken"], "kai missing")
ok(F.use_first_radar(inv)["at_risk_value_thb"] == E["radar_at_risk_value_thb"], "radar value")
ok(F.cook_mode(E["top3"][0])["total_timer_s"] == E["cook_total_timer_s"], "timer total")
p = F.cook_progress(E["top3"][0], 0, 120); ok(p["remaining_s"] == 60 and not p["timer_done"], "progress")
inv2 = F.build_inventory(X.DETECTIONS, X.TODAY, confirmed_keys=["lime"])
new = sorted({m["recipe_id"] for m in F.menu_match(inv2, top_n=0)} - {m["recipe_id"] for m in F.menu_match(inv, top_n=0)})
ok(new == E["after_confirm_lime_new_menus"], "lime rerun")
plan = [m for m in F.menu_match(inv2, top_n=0) if m["recipe_id"] in ex["shopping_plan_ids"]]
ok(F.shopping_list(plan)["total_thb"] == E["shopping_total_thb"], "shopping")
ok(F.menu_dice(F.menu_match(inv, {"max_missing": 0}, top_n=0), X.DICE_SEED)["pick"] == E["dice_pick"], "dice")
w = F.waste_wrapped(ex["history"], "2026-10")
ok((w["meals_cooked"], w["items_rescued"], w["value_saved_thb"], w["best_streak_days"]) == (E["wrapped_meals"], E["wrapped_items"], E["wrapped_value_thb"], E["wrapped_streak"]), "wrapped")
ok(all("spicy" not in m["tags"] for m in F.menu_match(inv, {"diet": ["not_spicy"]}, top_n=0)), "not_spicy filter")
ok(all("pork" not in m["tags"] for m in F.menu_match(inv, {"diet": ["no_pork"]}, top_n=0)), "no_pork filter")
ok(F.build_inventory([{"key": "milk", "qty": 1, "added_on": "2026-10-01", "confidence": 0.9}], X.TODAY)[0]["status"] == "check", "expired milk")
ok(not F.menu_match(F.build_inventory([], X.TODAY), {"max_missing": 0}), "empty fridge")
print(f"ALL {n} TESTS PASS")
