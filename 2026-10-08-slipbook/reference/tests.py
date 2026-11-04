"""python3 tests.py — re-checks examples.json test_vectors against the reference engine output."""
import json
ex = json.load(open("../examples.json"))
P = {p["slip_id"]: p for p in ex["parsed_slips"]}
fails = 0
for tv in ex["test_vectors"]:
    if "input_slip" in tv:
        p = P[tv["input_slip"]]
        flat = dict(p, **{"category": p["category_guess"]["category"], "source": p["category_guess"]["source"]})
        for k, v in tv["expect"].items():
            if flat.get(k) != v: fails += 1; print("FAIL", tv["name"], k, flat.get(k), "!=", v)
assert ex["import_batch_example"]["added"] == 17 and ex["import_batch_example"]["duplicates_skipped"] == 1
assert ex["dashboard_oct"]["spent_total"] == 6584.5 and ex["budget_status_oct"]["safe_per_day"] == 563
assert [s["counterparty"] for s in ex["subscriptions"]] == ["มือถือรายเดือน (เน็ตดี)", "MOVIEMAX"]
assert abs(sum(c["amount"] for c in ex["dashboard_oct"]["by_category"]) - ex["dashboard_oct"]["spent_total"]) < 0.001
print("fails", fails)
