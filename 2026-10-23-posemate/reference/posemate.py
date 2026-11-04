"""PoseMate (โพสท่าไม่เป็น) — deterministic core. AI only reads the scene/keypoints; every score comes from here."""
import math
SPOTS = {"cafe_window": "ริมหน้าต่างคาเฟ่", "street_wall": "กำแพงสีริมถนน", "stairs": "บันได", "beach": "ทะเล", "nature": "สวน/ธรรมชาติ", "mirror": "กระจก"}
LIGHT = {"side": 100, "window": 100, "front": 75, "shade": 70, "top": 45, "back": 35}
LIGHT_TH = {"side": "แสงข้าง", "window": "แสงหน้าต่าง", "front": "แสงหน้าตรง", "shade": "ร่มเงา", "top": "แดดเที่ยงตรงหัว", "back": "ย้อนแสง"}
KP = ["head", "neck", "l_sh", "r_sh", "l_hand", "r_hand", "hip", "l_foot", "r_foot"]
# keypoints normalised to frame [x,y]
POSES = [
    {"id": "p_window_lean", "name_th": "พิงขอบหน้าต่าง มองนอก", "spots": ["cafe_window"], "people": 1, "shot": "half", "difficulty": 1,
     "cue_th": "เอนไหล่แตะกระจก มือนึงถือแก้ว มองออกนอกหน้าต่าง", "kp": [[.55, .2], [.55, .3], [.48, .33], [.62, .33], [.47, .52], [.66, .46], [.55, .62], [.5, .95], [.6, .95]]},
    {"id": "p_cup_sip", "name_th": "จิบกาแฟ เผลอยิ้ม", "spots": ["cafe_window"], "people": 1, "shot": "close", "difficulty": 1,
     "cue_th": "ยกแก้วระดับคาง ก้มหน้านิดๆ ยิ้มมุมปาก", "kp": [[.5, .25], [.5, .38], [.42, .42], [.58, .42], [.48, .3], [.55, .3], [.5, .75], [.45, .98], [.55, .98]]},
    {"id": "p_chin_rest", "name_th": "เท้าคาง เหม่อ", "spots": ["cafe_window"], "people": 1, "shot": "half", "difficulty": 2,
     "cue_th": "ศอกวางโต๊ะ มือแตะคางเบาๆ หันหน้า 45° เข้าหาแสง", "kp": [[.52, .22], [.52, .32], [.44, .36], [.6, .36], [.5, .27], [.66, .55], [.52, .65], [.47, .97], [.57, .97]]},
    {"id": "p_walk_away", "name_th": "เดินผ่าน หันกลับมามอง", "spots": ["street_wall", "nature", "beach"], "people": 1, "shot": "full", "difficulty": 2,
     "cue_th": "ก้าวขาไขว้ เดินช้าๆ หันไหล่กลับมาครึ่งเดียว", "kp": [[.5, .12], [.5, .2], [.44, .23], [.56, .23], [.4, .42], [.6, .4], [.5, .5], [.44, .92], [.58, .9]]},
    {"id": "p_wall_lean", "name_th": "พิงกำแพง ขาไขว้", "spots": ["street_wall"], "people": 1, "shot": "full", "difficulty": 1,
     "cue_th": "หลังพิงกำแพง ขาหน้าไขว้ มือล้วงกระเป๋า", "kp": [[.5, .12], [.5, .2], [.43, .23], [.57, .23], [.44, .45], [.58, .45], [.5, .5], [.52, .92], [.48, .92]]},
    {"id": "p_stair_sit", "name_th": "นั่งบันได ศอกวางเข่า", "spots": ["stairs"], "people": 1, "shot": "full", "difficulty": 1,
     "cue_th": "นั่งขั้นที่ 3 เข่าชิด ศอกวางเข่า มองเลยกล้อง", "kp": [[.5, .3], [.5, .4], [.43, .43], [.57, .43], [.44, .6], [.56, .6], [.5, .66], [.45, .9], [.55, .9]]},
    {"id": "p_hair_wind", "name_th": "จับผมโดนลม", "spots": ["beach", "nature"], "people": 1, "shot": "half", "difficulty": 2,
     "cue_th": "หันข้างให้ลม มือนึงปัดผมหลังหู หลับตาครึ่งนึง", "kp": [[.5, .2], [.5, .3], [.43, .33], [.57, .33], [.46, .2], [.6, .55], [.5, .62], [.46, .97], [.55, .97]]},
    {"id": "p_mirror_tilt", "name_th": "มิเรอร์เซลฟี่ บิดเอว", "spots": ["mirror"], "people": 1, "shot": "full", "difficulty": 1,
     "cue_th": "มือถือบังครึ่งหน้า บิดเอวเข้า ย่อเข่าหน้า", "kp": [[.5, .12], [.5, .2], [.43, .23], [.57, .23], [.48, .18], [.6, .45], [.48, .5], [.47, .92], [.56, .9]]},
    {"id": "g_back_to_back", "name_th": "ยืนหันหลังชนกัน", "spots": ["street_wall", "nature", "beach", "stairs"], "people": 2, "shot": "full", "difficulty": 1,
     "cue_th": "หลังชนกัน กอดอก หันหน้ามาทางกล้องครึ่งเดียว", "kp": None},
    {"id": "g_cafe_cheers", "name_th": "ชนแก้วข้ามโต๊ะ", "spots": ["cafe_window"], "people": 2, "shot": "half", "difficulty": 1,
     "cue_th": "นั่งตรงข้าม ยกแก้วชนกลางเฟรม หัวเราะใส่กัน", "kp": None},
    {"id": "g_step_ladder", "name_th": "ยืนไล่ขั้นบันได", "spots": ["stairs"], "people": 3, "shot": "full", "difficulty": 1,
     "cue_th": "แต่ละคนยืนคนละขั้น หันคนละมุม คนบนสุดชี้ฟ้า", "kp": None},
    {"id": "g_jump", "name_th": "กระโดดพร้อมกัน", "spots": ["beach", "nature", "street_wall"], "people": 4, "shot": "full", "difficulty": 3,
     "cue_th": "นับ 1-2-3 กระโดด เปิดโหมดถ่ายรัว", "kp": None},
]
P = {p["id"]: p for p in POSES}
ANGLE = {"full": {"height_th": "ระดับเอว", "tilt": -10, "lens": "0.5x", "distance_m": 2.5, "tip_th": "ถือต่ำระดับเอว ก้มกล้องลง 10° เท้าชิดขอบล่าง ขาจะยาวขึ้น"},
         "half": {"height_th": "ระดับอก", "tilt": 0, "lens": "1x", "distance_m": 1.5, "tip_th": "กล้องระดับอก ถือตรง เว้นหัว 1 นิ้ว ไม่ตัดข้อมือ"},
         "close": {"height_th": "ระดับตา", "tilt": 5, "lens": "2x", "distance_m": 1.0, "tip_th": "ซูม 2x ถอยออก หน้าไม่บาน ถือสูงกว่าตานิดเดียว"}}
W = {"level": .15, "thirds": .2, "headroom": .1, "light": .2, "clutter": .1, "pose": .25}
FIX_TH = {"level": "เอียงกล้องให้เส้นขอบฟ้าตรง (เปิดเส้นตาราง)", "thirds": "ขยับคนไปเส้น 1/3 ไม่ต้องอยู่กลางเป๊ะ", "headroom": "เว้นหัวพอดี ไม่ชิดขอบ ไม่โล่งเกิน",
          "light": "หันหน้าเข้าหาแสง/ย้ายไปแสงข้าง", "clutter": "เก็บของเกะกะออกจากฉากหลัง", "pose": "ทำท่าตามเงาให้ตรงขึ้น"}

def scene_read(spot, light, people=1, clutter=0):
    if spot not in SPOTS: raise ValueError("bad_spot")
    if light not in LIGHT: raise ValueError("bad_light")
    if not 1 <= people <= 4: raise ValueError("bad_people")
    tip = "ถ่ายได้เลย แสงสวย" if LIGHT[light] >= 90 else ("ย้ายมุม 90° ให้แสงเข้าข้างหน้า" if LIGHT[light] < 50 else "โอเค ถ้าหันเข้าหาแสงอีกนิดจะดีขึ้น")
    return {"spot": spot, "spot_th": SPOTS[spot], "light": light, "light_th": LIGHT_TH[light], "light_score": LIGHT[light], "people": people, "clutter": clutter, "tip_th": tip}

def pose_cards(scene, n=3):
    c = [p for p in POSES if scene["spot"] in p["spots"] and p["people"] == scene["people"]]
    if len(c) < n: c += [p for p in POSES if p["people"] == scene["people"] and p not in c]
    c = sorted(c, key=lambda p: (scene["spot"] not in p["spots"], p["difficulty"], p["id"]))[:n]
    return [{"id": p["id"], "name_th": p["name_th"], "cue_th": p["cue_th"], "shot": p["shot"], "difficulty": p["difficulty"], "ghost": p["kp"] is not None} for p in c]

def _norm(kp):
    hx, hy = kp[6]; nx, ny = kp[1]; s = math.dist((hx, hy), (nx, ny)) or 1
    return [((x - hx) / s, (y - hy) / s) for x, y in kp]

def pose_match(pose_id, kp):
    t = P[pose_id]["kp"]
    if t is None: raise ValueError("no_ghost")
    if len(kp) != 9: raise ValueError("bad_kp")
    a, b = _norm(t), _norm(kp)
    d = [math.dist(x, y) for x, y in zip(a, b)]
    worst = KP[d.index(max(d))]
    return {"pose_id": pose_id, "match": max(0, round(100 - 250 * sum(d) / len(d))), "worst_th": {"head": "หัว", "neck": "คอ", "l_sh": "ไหล่ซ้าย", "r_sh": "ไหล่ขวา", "l_hand": "มือซ้าย", "r_hand": "มือขวา", "hip": "สะโพก", "l_foot": "เท้าซ้าย", "r_foot": "เท้าขวา"}[worst]}

def angle_coach(pose_id):
    a = ANGLE[P[pose_id]["shot"]]
    return {"pose_id": pose_id, "shot": P[pose_id]["shot"], **a,
            "friend_cues_th": [f"ถือกล้อง{a['height_th']}", ("ก้มกล้องลง " if a["tilt"] < 0 else "เงยกล้องขึ้น " if a["tilt"] > 0 else "ถือตรง ") + (f"{abs(a['tilt'])}°" if a["tilt"] else "ไม่เอียง"),
                               f"ใช้เลนส์ {a['lens']}", f"ยืนห่าง {a['distance_m']} เมตร", "กดถ่ายรัว 5 รูป"]}

def shot_score(tilt_deg, subject_xy, headroom, light, clutter, pose):
    x, y = subject_xy
    d = min(math.dist((x, y), (tx, ty)) for tx in (1/3, 2/3) for ty in (1/3, 2/3))
    off = 0 if .06 <= headroom <= .15 else min(abs(headroom - .06), abs(headroom - .15))
    parts = {"level": max(0, round(100 - abs(tilt_deg) * 12)), "thirds": max(0, round(100 - d * 400)), "headroom": max(0, round(100 - off * 600)),
             "light": LIGHT[light], "clutter": max(0, 100 - clutter * 20), "pose": pose}
    total = round(sum(parts[k] * W[k] for k in W))
    fixes = [FIX_TH[k] for k, _ in sorted(((k, v) for k, v in parts.items() if v < 70), key=lambda kv: (kv[1], kv[0]))][:3]
    grade = "ปังมาก 🔥" if total >= 85 else "ดีแล้ว 👍" if total >= 70 else "ยังได้อีก" if total >= 50 else "ลองใหม่ 😅"
    return {"total": total, "grade_th": grade, "parts": parts, "fixes_th": fixes}

def glow_up(before, after):
    return {"before": before["total"], "after": after["total"], "delta": after["total"] - before["total"], "line_th": f"จาก {before['total']} → {after['total']} แค่ทำตามแอป"}

CAP = {"cafe_window": ["กาแฟแก้วนี้ไม่ได้ช่วยให้ตื่น แต่ช่วยให้รูปสวย ☕", "แสงหน้าต่างทำงานแทนฟิลเตอร์", "วันนี้ขอช้าๆ แบบนี้"],
       "street_wall": ["กำแพงสวย คนก็ต้องไม่แพ้", "เดินผ่านแค่นี้ ไม่ได้ตั้งใจ (ตั้งใจมาก)", "สีนี้ต้องมีรูป"],
       "stairs": ["ขึ้นทีละขั้น ช้าแต่ชิค", "บันไดนี้คือสตูดิโอฟรี", "นั่งพักแป๊บ ถ่ายรูปนาน"],
       "beach": ["ลมทะเลจัดทรงผมให้แล้ว", "ส่งคลื่นไปบอกงานว่าไม่ว่าง 🌊", "เค็มนิดๆ ชิลหน่อยๆ"],
       "nature": ["ต้นไม้ไม่ถามว่ารอบนี้ถ่ายกี่รูป", "ออกมาชาร์จแบตแบบธรรมชาติ", "เขียวแบบนี้ใจสงบ"],
       "mirror": ["กระจกไม่โกหก แต่มุมช่วยได้", "ชุดวันนี้ขอเก็บไว้หน่อย", "OOTD ก่อนออกบ้าน"]}
TAGS = {"cafe_window": ["#คาเฟ่", "#cafehopping"], "street_wall": ["#streetstyle", "#ootd"], "stairs": ["#ootd", "#posing"], "beach": ["#ทะเล", "#beachvibes"], "nature": ["#ธรรมชาติ", "#weekend"], "mirror": ["#mirrorselfie", "#ootd"]}
def caption_pack(spot, place=None):
    tags = TAGS[spot] + ["#PoseMate", "#AIวันละแอป"]
    return {"spot": spot, "captions_th": CAP[spot], "hashtags": tags, "place_tag": place}

def _warm(h): return h < 70 or h >= 300
def grid_plan(photos):
    if len(photos) != 9: raise ValueError("need_9")
    left, out = sorted(photos, key=lambda p: p["id"]), []
    while left:
        prev = out[-1] if out else None; up = out[-3] if len(out) >= 3 else None
        def cost(p): return (prev is not None and p["kind"] == prev["kind"]) + (up is not None and p["kind"] == up["kind"]) + (prev is not None and _warm(p["hue"]) == _warm(prev["hue"]))
        best = min(left, key=lambda p: (cost(p), p["id"])); out.append(best); left.remove(best)
    clash = sum(1 for i in range(9) for j in (i + 1, i + 3) if j < 9 and (j != i + 1 or i % 3 != 2) and out[i]["kind"] == out[j]["kind"])
    return {"order": [p["id"] for p in out], "clashes": clash, "balance": max(0, 100 - clash * 10)}

def _lum(h):
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (1, 3, 5))
    f = lambda c: c / 12.92 if c <= .03928 else ((c + .055) / 1.055) ** 2.4
    return .2126 * f(r) + .7152 * f(g) + .0722 * f(b)
def _hue(h):
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)); mx, mn = max(r, g, b), min(r, g, b)
    if mx == mn: return None
    d = mx - mn
    hh = ((g - b) / d) % 6 if mx == r else (b - r) / d + 2 if mx == g else (r - g) / d + 4
    return hh * 60
def outfit_pop(outfit_hex, bg_hex):
    l1, l2 = sorted((_lum(outfit_hex), _lum(bg_hex)), reverse=True); ratio = (l1 + .05) / (l2 + .05)
    h1, h2 = _hue(outfit_hex), _hue(bg_hex); hd = 0 if h1 is None or h2 is None else min(abs(h1 - h2), 360 - abs(h1 - h2))
    s = min(100, round(min(ratio, 4) / 4 * 60 + hd / 180 * 40))
    return {"outfit": outfit_hex, "bg": bg_hex, "contrast": round(ratio, 2), "hue_gap": round(hd), "score": s,
            "verdict": "pop" if s >= 60 else "ok" if s >= 35 else "blend", "verdict_th": "ชุดเด้งจากฉาก ✨" if s >= 60 else "พอได้" if s >= 35 else "ชุดจมไปกับฉาก ลองย้ายมุม"}
