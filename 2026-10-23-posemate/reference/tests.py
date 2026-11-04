"""Run: python3 tests.py — locks the demo numbers the Reel shows."""
import posemate as T, fixtures as X
SC = T.scene_read(**X.SCENE); LIVE = T.pose_match("p_window_lean", X.LIVE_KP)
B = T.shot_score(**X.BEFORE); A = T.shot_score(**X.AFTER, pose=LIVE["match"])
def raises(f, msg):
    try: f(); assert False
    except ValueError as e: assert str(e) == msg
def t_scene(): assert (SC["light_score"], SC["tip_th"]) == (100, "ถ่ายได้เลย แสงสวย")
def t_scene_back(): assert T.scene_read("street_wall", "back")["tip_th"].startswith("ย้ายมุม")
def t_bad_inputs(): raises(lambda: T.scene_read("moon", "side"), "bad_spot"); raises(lambda: T.scene_read("beach", "neon"), "bad_light"); raises(lambda: T.scene_read("beach", "side", 5), "bad_people")
def t_cards(): assert [c["id"] for c in T.pose_cards(SC)] == ["p_cup_sip", "p_window_lean", "p_chin_rest"]
def t_cards_people_match():
    for s in T.SPOTS:
        for n in range(1, 5):
            cs = T.pose_cards(T.scene_read(s, "side", n)); assert 1 <= len(cs) <= 3 and all(T.P[c["id"]]["people"] == n for c in cs)
def t_match_live(): assert LIVE == {"pose_id": "p_window_lean", "match": 94, "worst_th": "เท้าขวา"}
def t_match_stiff(): assert T.pose_match("p_window_lean", X.STIFF_KP)["match"] == 65
def t_match_self_100():
    for p in T.POSES:
        if p["kp"]: assert T.pose_match(p["id"], p["kp"])["match"] == 100
def t_match_scale_invariant(): kp = [[.1 + x * .5, .1 + y * .5] for x, y in X.LIVE_KP]; assert T.pose_match("p_window_lean", kp)["match"] == 94
def t_match_no_ghost(): raises(lambda: T.pose_match("g_jump", X.LIVE_KP), "no_ghost")
def t_before(): assert (B["total"], B["grade_th"], B["parts"]["light"]) == (30, "ลองใหม่ 😅", 35) and B["fixes_th"][0].startswith("เว้นหัว")
def t_after(): assert (A["total"], A["grade_th"], A["fixes_th"]) == (94, "ปังมาก 🔥", [])
def t_glow(): g = T.glow_up(B, A); assert (g["delta"], g["line_th"]) == (64, "จาก 30 → 94 แค่ทำตามแอป")
def t_weights(): assert abs(sum(T.W.values()) - 1) < 1e-9
def t_angle(): a = T.angle_coach("p_wall_lean"); assert (a["lens"], a["tilt"], a["friend_cues_th"][1]) == ("0.5x", -10, "ก้มกล้องลง 10°")
def t_caption(): c = T.caption_pack("cafe_window"); assert len(c["captions_th"]) == 3 and "#AIวันละแอป" in c["hashtags"]
def t_grid(): g = T.grid_plan(X.PHOTOS); assert (g["order"][0], g["balance"], sorted(g["order"]) == sorted(p["id"] for p in X.PHOTOS)) == ("ph1", 90, True)
def t_grid_need_9(): raises(lambda: T.grid_plan(X.PHOTOS[:8]), "need_9")
def t_outfit(): a, b = (T.outfit_pop(*o) for o in X.OUTFIT_BG); assert (a["score"], a["verdict"], b["score"], b["verdict"]) == (16, "blend", 64, "pop")
def t_outfit_gray(): assert T.outfit_pop("#000000", "#FFFFFF")["score"] == 60
def t_deterministic(): assert T.shot_score(**X.BEFORE) == B
if __name__ == "__main__":
    ts = [(k, v) for k, v in dict(globals()).items() if k.startswith("t_")]
    for k, f in ts: f(); print("ok", k)
    print(f"{len(ts)} tests passed")
