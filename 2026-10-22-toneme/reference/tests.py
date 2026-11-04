"""Run: python3 tests.py — locks the demo numbers the Reel shows."""
import toneme as T, fixtures as X
P = T.analyze(**X.SAMPLE)
def t_profile(): assert (P["label"], P["warmth"], P["lightness"], P["contrast"], P["confidence"]) == ("True Autumn", 21, 48, 59, 78)
def t_traits(): assert (P["undertone"], P["depth"], P["chroma"], P["metal"]) == ("warm", "deep", "clear", "gold")
def t_quiz_flips(): q = T.analyze(**{**X.SAMPLE, "vein": "blue", "metal": "silver"}); assert q["warmth"] == 21 - 36 and q["season"] == "winter"
def t_light_spring(): assert T.analyze(skin="#F5D5C0", hair="#7A5A3A", eyes="#5A3E2B")["label"] == "Light Spring"
def t_summer(): assert T.analyze(skin="#E9C9B9", hair="#1B1B1B", eyes="#1E1410")["label"] == "True Summer"
def t_winter(): assert T.analyze(skin="#C49A8E", hair="#121212", eyes="#140E0C", vein="blue", metal="silver")["label"] == "True Winter"
def t_sub_valid():
    for s in ["#F5D5C0", "#E9C9B9", "#C49A8E", "#8D5524", "#D9A27E"]:
        for v in T.VEIN:
            r = T.analyze(skin=s, hair="#2B1D14", eyes="#3A2618", vein=v); assert r["sub"] in T.SUBS[r["season"]] and 50 <= r["confidence"] <= 95
def t_bad_light():
    try: T.analyze(**X.SAMPLE, light_ok=False); assert False
    except ValueError as e: assert str(e) == "bad_light"
def t_bad_quiz():
    try: T.analyze(skin="#D9A27E", hair="#2B1D14", eyes="#3A2618", vein="purple"); assert False
    except ValueError: pass
def t_deterministic(): assert T.analyze(**X.SAMPLE) == P
def t_drape(): d = T.drape_battle(P, *X.DRAPE); assert (d["a"]["score"], d["b"]["score"], d["winner"], d["gap"]) == (96, 0, "a", 96)
def t_drape_swap_sides(): d = T.drape_battle(P, X.DRAPE[1], X.DRAPE[0]); assert d["winner"] == "b"
def t_palette_card(): c = T.palette_card(P, X.NAME); assert len(c["best"]) == 12 and len(c["avoid"]) == 4 and c["best"][0]["name_th"] == "เทอร์ราคอตตา"
def t_palette_exact_100():
    for s, v in T.PALETTES.items():
        for _, h in v["best"]: assert T.color_score(s, h)[0] >= 90, (s, h)
def t_avoid_low():
    for s, v in T.PALETTES.items():
        for _, h in v["avoid"]: assert T.color_score(s, h)[0] < 50, (s, h)
def t_outfit(): f = T.outfit_check(P, X.OUTFIT); assert (f["overall"], f["items"][0]["swap_th"]) == (50, "เทียล") and "เทียล" in f["tip_th"]
def t_outfit_swap(): assert T.outfit_check(P, X.OUTFIT_SWAP)["overall"] == 96
def t_outfit_empty(): assert T.outfit_check(P, [])["overall"] == 0
def t_makeup(): m = T.makeup(P); assert m["lip"][0]["family_th"] == "อิฐ" and m["blush"][0]["hex"] == "#D27D5C"
def t_shop(): s = T.shop_scan(P, X.SHOP); assert (s["score"], s["verdict"], s["near_th"]) == (91, "yes", "เทียล")
def t_audit(): a = T.closet_audit(P, X.CLOSET); assert (a["yes"], a["maybe"], a["no"], a["match_pct"], a["buy_next_th"]) == (4, 0, 4, 50, ["เทอร์ราคอตตา", "ส้มฟักทอง", "เทียล"])
def t_hair(): assert [h["name_th"] for h in T.hair_guide(P)] == ["น้ำตาลช็อกโกแลต", "แดงทองแดง"]
def t_friends(): g = T.friend_compare(X.FRIENDS); assert (g["group_color_th"], g["avg_score"], g["count"]) == ("ครีมอูฐ", 85, {"spring": 1, "summer": 1, "autumn": 2})
if __name__ == "__main__":
    ts = [(k, v) for k, v in dict(globals()).items() if k.startswith("t_")]
    for k, f in ts: f(); print("ok", k)
    print(f"{len(ts)} tests passed")
