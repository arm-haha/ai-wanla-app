"""python3 tests.py — re-check examples.json test_vectors against reference engine."""
import json
from pathlib import Path
from reel import (
    parse_idea, build_blueprint, build_caption_pack, build_overlays,
    rank_hooks, film_progress, swap_hook, allocate_durations, suggest_trend_angles,
)
from fixtures import DEMO_IDEA_RAW, DEMO_STYLE, DEMO_DURATION, EXPECT

ex = json.load(open(Path(__file__).resolve().parent.parent / "examples.json", encoding="utf-8"))
fails = 0

def check(name, cond, detail=""):
    global fails
    if not cond:
        fails += 1
        print("FAIL", name, detail)

# locked expect
idea = parse_idea(DEMO_IDEA_RAW)
bp = build_blueprint(idea, DEMO_STYLE, DEMO_DURATION)
caps = build_caption_pack(bp)
ovs = build_overlays(bp)

check("product", idea["product"] == EXPECT["product"], idea["product"])
check("category", idea["category"] == EXPECT["category"])
check("price_unit", idea["price_unit"] == EXPECT["price_unit"])
check("price_set", idea["price_set"] == EXPECT["price_set"])
check("set_qty", idea["set_qty"] == EXPECT["set_qty"])
check("channel", idea["channel"] == EXPECT["channel"])
check("area", idea["area"] == EXPECT["area"])
check("cta", idea["cta_keyword"] == EXPECT["cta_keyword"])
check("shot_count", bp["shot_count"] == 5)
durs = [s["duration_s"] for s in bp["shots"]]
check("durations", durs == [3, 6, 8, 8, 5], durs)
check("sum30", sum(durs) == 30)
check("hook_a", bp["hook"]["id"] == "hook_a")
check("hook_vs", "vs" in bp["hook"]["text_th"] and "30 วิ" in bp["hook"]["text_th"])
check("cta_in_short", "คุกกี้" in caps["caption_short_th"] and caps["comment_cta_keyword"] == "คุกกี้")
check("covers3", len(ovs["covers"]) == 3)
check("hooks3", len(bp["hooks_ranked"]) == 3 and bp["hooks_ranked"][0]["rank"] == 1)
check("winner_is_a", bp["hooks_ranked"][0]["id"] == "hook_a" and bp["hooks_ranked"][0]["is_winner"])

# examples.json mirrors engine
check("ex_durations", [s["duration_s"] for s in ex["blueprint_example"]["shots"]] == durs)
check("ex_hook", ex["blueprint_example"]["hook"]["id"] == "hook_a")
check("ex_cta", ex["caption_pack_example"]["comment_cta_keyword"] == "คุกกี้")
check("ex_locked", ex["expect_locked"]["durations"] == [3, 6, 8, 8, 5])

# run each test_vector
for tv in ex["test_vectors"]:
    fn = tv["fn"]
    inp = tv["input"]
    exp = tv["expect"]
    if fn == "parse_idea":
        got = parse_idea(inp["raw"])
        for k, v in exp.items():
            check(tv["name"] + "." + k, got.get(k) == v, f"{got.get(k)} != {v}")
    elif fn == "build_blueprint":
        got = build_blueprint(parse_idea(inp["raw"]), inp["style"], inp["duration_target"])
        check(tv["name"] + ".shot_count", got["shot_count"] == exp["shot_count"])
        check(tv["name"] + ".duration", got["duration_total_s"] == exp["duration_total_s"])
        check(tv["name"] + ".durs", [s["duration_s"] for s in got["shots"]] == exp["durations"])
        check(tv["name"] + ".hook", got["hook"]["id"] == exp["hook_id"])
        check(tv["name"] + ".cta", got["cta_keyword"] == exp["cta_keyword"])
        check(tv["name"] + ".bgm", got["bgm_mood"] == exp["bgm_mood"])
    elif fn == "rank_hooks":
        got_bp = build_blueprint(parse_idea(inp["raw"]), inp["style"], 30)
        ranked = got_bp["hooks_ranked"]
        check(tv["name"] + ".winner", ranked[0]["id"] == exp["winner_id"])
        check(tv["name"] + ".count", len(ranked) == exp["hooks_count"])
        check(tv["name"] + ".rank", ranked[0]["rank"] == exp["winner_rank"])
    elif fn == "build_caption_pack":
        got = build_caption_pack(build_blueprint(parse_idea(inp["raw"]), inp["style"], inp["duration_target"]))
        check(tv["name"] + ".cta", got["comment_cta_keyword"] == exp["comment_cta_keyword"])
        check(tv["name"] + ".tags", len(got["hashtags"]) >= exp["hashtag_min"])
        check(tv["name"] + ".short", exp["short_contains"] in got["caption_short_th"])
    elif fn == "build_overlays":
        got = build_overlays(build_blueprint(parse_idea(inp["raw"]), inp["style"], inp["duration_target"]))
        check(tv["name"] + ".covers", len(got["covers"]) == exp["cover_count"])
        check(tv["name"] + ".per", len(got["per_shot"]) == exp["per_shot_count"])
        check(tv["name"] + ".ids", [c["id"] for c in got["covers"]] == exp["cover_ids"])
    elif fn == "film_progress":
        got = film_progress(bp["shots"], inp["elapsed_s"])
        if "shot_n" in exp:
            check(tv["name"] + ".shot_n", got["shot"]["n"] == exp["shot_n"], got["shot"]["n"])
        if "done" in exp:
            check(tv["name"] + ".done", got["done"] == exp["done"])
        if "overall_progress" in exp:
            check(tv["name"] + ".prog", got["overall_progress"] == exp["overall_progress"])
        if "remaining_s" in exp:
            check(tv["name"] + ".rem", got["remaining_s"] == exp["remaining_s"])
    elif fn == "allocate_durations":
        got = allocate_durations(inp["weights"], inp["target"])
        if "durations" in exp:
            check(tv["name"] + ".durs", got == exp["durations"], got)
        if "sum" in exp:
            check(tv["name"] + ".sum", sum(got) == exp["sum"])
        if "min_each" in exp:
            check(tv["name"] + ".min", all(x >= exp["min_each"] for x in got))
    elif fn == "swap_hook":
        got = swap_hook(bp, inp["hook_id"])
        check(tv["name"] + ".hook", got["hook"]["id"] == exp["hook_id"])
        check(tv["name"] + ".dur", got["duration_total_s"] == exp["duration_total_s"])
        check(tv["name"] + ".shots", got["shot_count"] == exp["shot_count"])
    elif fn == "suggest_trend_angles":
        got = suggest_trend_angles(parse_idea(inp["raw"]))
        check(tv["name"] + ".first", got[0]["id"] == exp["first_id"])
        check(tv["name"] + ".count", len(got) == exp["count"])
    else:
        check(tv["name"], False, "unknown fn " + fn)

# feature checklist
check("must5", len(ex["feature_checklist_example"]["must_have"]) >= 5)
check("must_all_done", all(f["done"] for f in ex["feature_checklist_example"]["must_have"]))

print("fails", fails)
raise SystemExit(1 if fails else 0)
