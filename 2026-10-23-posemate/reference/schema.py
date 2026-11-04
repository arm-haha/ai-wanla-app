"""JSON Schema (draft 2020-12) for PoseMate. build.py writes it to ../schemas.json."""
import posemate as T
S = lambda **k: dict(type="string", **k)
I = lambda **k: dict(type="integer", **k)
N = lambda **k: dict(type="number", **k)
HEX = S(pattern=r"^#[0-9A-Fa-f]{6}$")
ref = lambda n: {"$ref": f"#/$defs/{n}"}
arr = lambda x, **k: dict(type="array", items=x, **k)
score = I(minimum=0, maximum=100)
unit = N(minimum=0, maximum=1)
def obj(props, req=None):
    return {"type": "object", "properties": props, "required": req if req is not None else list(props), "additionalProperties": False}
D = {
    "Hex": HEX, "Spot": {"enum": list(T.SPOTS)}, "Light": {"enum": list(T.LIGHT)}, "Shot": {"enum": list(T.ANGLE)},
    "Point": arr(unit, minItems=2, maxItems=2), "Keypoints": arr(ref("Point"), minItems=9, maxItems=9, description="ลำดับ " + ", ".join(T.KP)),
    "Pose": obj({"id": S(), "name_th": S(), "spots": arr(ref("Spot"), minItems=1), "people": I(minimum=1, maximum=4), "shot": ref("Shot"),
                 "difficulty": I(minimum=1, maximum=3), "cue_th": S(maxLength=80), "kp": {"anyOf": [ref("Keypoints"), {"type": "null"}]}}),
    "Scene": obj({"spot": ref("Spot"), "spot_th": S(), "light": ref("Light"), "light_th": S(), "light_score": score, "people": I(minimum=1, maximum=4),
                  "clutter": I(minimum=0), "tip_th": S()}),
    "PoseCard": obj({"id": S(), "name_th": S(), "cue_th": S(), "shot": ref("Shot"), "difficulty": I(minimum=1, maximum=3), "ghost": {"type": "boolean"}}),
    "PoseCards": arr(ref("PoseCard"), minItems=1, maxItems=3),
    "PoseMatch": obj({"pose_id": S(), "match": score, "worst_th": S()}),
    "AngleCoach": obj({"pose_id": S(), "shot": ref("Shot"), "height_th": S(), "tilt": I(minimum=-30, maximum=30), "lens": {"enum": ["0.5x", "1x", "2x"]},
                       "distance_m": N(minimum=0.3, maximum=10), "tip_th": S(), "friend_cues_th": arr(S(maxLength=40), minItems=3, maxItems=6)}),
    "ShotInput": obj({"tilt_deg": N(minimum=-45, maximum=45), "subject_xy": ref("Point"), "headroom": unit, "light": ref("Light"), "clutter": I(minimum=0, maximum=10),
                      "pose": score}, ["tilt_deg", "subject_xy", "headroom", "light", "clutter"]),
    "ShotScore": obj({"total": score, "grade_th": S(), "parts": obj({k: score for k in T.W}), "fixes_th": arr(S(), maxItems=3)}),
    "GlowUp": obj({"before": score, "after": score, "delta": I(minimum=-100, maximum=100), "line_th": S()}),
    "CaptionPack": obj({"spot": ref("Spot"), "captions_th": arr(S(maxLength=60), minItems=3, maxItems=3), "hashtags": arr(S(pattern="^#"), maxItems=8),
                        "place_tag": {"type": ["string", "null"]}}),
    "GridPhoto": obj({"id": S(), "kind": {"enum": ["person", "detail", "scene"]}, "hue": N(minimum=0, maximum=360)}),
    "GridPlan": obj({"order": arr(S(), minItems=9, maxItems=9), "clashes": I(minimum=0), "balance": score}),
    "OutfitPop": obj({"outfit": ref("Hex"), "bg": ref("Hex"), "contrast": N(minimum=1, maximum=21), "hue_gap": I(minimum=0, maximum=180), "score": score,
                      "verdict": {"enum": ["pop", "ok", "blend"]}, "verdict_th": S()}),
    "Session": obj({"id": S(), "date": S(format="date"), "scene": ref("Scene"), "pose_id": S(), "before": score, "after": score}),
    "LocalStore": obj({"version": {"const": 1}, "name": S(), "saved_poses": arr(S()), "sessions": arr(ref("Session"), maxItems=500), "streak_days": I(minimum=0),
                       "settings": obj({"keep_photos": {"const": False}, "grid_lines": {"type": "boolean"}, "sound": {"type": "boolean"}})}),
    "AiSceneRequest": obj({"image": S(description="base64 JPEG ≤ 768px ของฉาก (ไม่ต้องมีคน) ไม่เก็บ")}),
    "AiSceneResponse": obj({"spot": ref("Spot"), "light": ref("Light"), "clutter": I(minimum=0, maximum=10), "horizon_tilt_deg": N(minimum=-45, maximum=45),
                            "bg_hex": ref("Hex"), "note_th": S(maxLength=100)}),
    "AiCaptionRequest": obj({"spot": ref("Spot"), "pose_name_th": S(), "mood": {"enum": ["chill", "cute", "cool", "funny"]}}),
    "AiCaptionResponse": obj({"captions_th": arr(S(maxLength=60), minItems=3, maxItems=3)}),
}
ROOT = {"$schema": "https://json-schema.org/draft/2020-12/schema", "$id": "https://example.invalid/posemate/schemas.json",
        "title": "PoseMate (โพสท่าไม่เป็น) data contracts", "$defs": D}
