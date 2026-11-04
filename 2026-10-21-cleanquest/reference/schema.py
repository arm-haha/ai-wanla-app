"""JSON Schema (draft 2020-12) for CleanQuest. build.py writes it to ../schemas.json."""
import cleanquest as C
S = lambda **k: dict(type="string", **k)
I = lambda **k: dict(type="integer", **k)
date_ = S(format="date", pattern=r"^\d{4}-\d{2}-\d{2}$")
ref = lambda n: {"$ref": f"#/$defs/{n}"}
arr = lambda x, **k: dict(type="array", items=x, **k)
score = I(minimum=0, maximum=100)
def obj(props, req=None, extra=False):
    return {"type": "object", "properties": props, "required": req if req is not None else list(props), "additionalProperties": extra}
D = {
    "HotspotId": {"enum": list(C.HOTSPOTS)},
    "Zone": {"enum": ["bed", "desk", "floor"]},
    "Severity": {"enum": [1, 2, 3]},
    "Mode": {"enum": list(C.MODES)},
    "Decision": {"enum": ["keep", "sell", "donate", "trash"]},
    "Condition": {"enum": list(C.COND_F)},
    "HotspotInput": obj({"id": ref("HotspotId"), "severity": ref("Severity")}),
    "ScanInput": obj({"room_id": S(), "at": S(format="date-time"), "hotspots": arr(ref("HotspotInput"), maxItems=13),
                      "source": {"enum": ["ai_suggested", "user_picked", "demo"]}, "photo_id": S()}, ["room_id", "hotspots", "source"]),
    "HotspotPin": obj({"id": ref("HotspotId"), "severity": ref("Severity"), "label_th": S(), "severity_th": S(), "points": I(minimum=1), "emoji": S(),
                       "box": arr({"type": "number", "minimum": 0, "maximum": 1}, minItems=4, maxItems=4)}, ["id", "severity", "label_th", "severity_th", "points", "emoji"]),
    "MessScore": obj({"clean_score": score, "mess_points": I(minimum=0), "label_th": {"enum": [t for _, t in C.LABELS]},
                      "worst_zone": {"anyOf": [ref("Zone"), {"type": "null"}]}, "zone_points": {"type": "object", "propertyNames": ref("Zone"), "additionalProperties": I(minimum=1)},
                      "hotspots": arr(ref("HotspotPin")), "est_minutes": I(minimum=0)}),
    "Quest": obj({"id": S(pattern=r"^q\d+$"), "hotspot": ref("HotspotId"), "title_th": S(maxLength=60), "emoji": S(), "minutes": I(minimum=1),
                  "xp": I(minimum=1), "quick_win": {"type": "boolean"}, "score_after": score}),
    "Sprint": obj({"n": I(minimum=1), "quest_ids": arr(S(), minItems=1), "minutes": I(minimum=1)}),
    "QuestPlan": obj({"mode": ref("Mode"), "mode_th": S(), "quests": arr(ref("Quest")), "sprints": arr(ref("Sprint")),
                      "total_minutes": I(minimum=0), "score_before": score, "score_after": score}),
    "TimerState": obj({"live_score": score, "xp_gained": I(minimum=0), "done": I(minimum=0), "left": I(minimum=0),
                       "next_quest": {"type": ["string", "null"]}, "sprint": {"type": ["integer", "null"]}, "remaining_sec": I(minimum=0), "finished": {"type": "boolean"}}),
    "GlowUpCard": obj({"name": S(), "before": score, "after": score, "delta": I(minimum=-100, maximum=100), "minutes": I(minimum=0), "quests_done": I(minimum=0),
                       "title_th": S(), "headline_th": S(), "size_px": {"const": [1080, 1920]}, "layout": {"enum": ["split_before_after", "slider"]},
                       "watermark": {"const": "CleanQuest · AI วันละแอป"}}),
    "DeclutterItem": obj({"id": S(), "name_th": S(minLength=1, maxLength=40), "condition": ref("Condition"), "last_used_months": I(minimum=0, maximum=240),
                          "paid_thb": I(minimum=0), "sentimental": {"type": "boolean"}, "duplicate": {"type": "boolean"}, "photo_id": S()},
                         ["id", "name_th", "condition", "last_used_months"]),
    "DeclutterResult": obj({"item_id": S(), "name_th": S(), "decision": ref("Decision"), "reason_th": S(), "resale_thb": I(minimum=0), "listing_th": S(maxLength=140)},
                           ["item_id", "name_th", "decision", "reason_th", "resale_thb"]),
    "ChoreShare": obj({"person": S(), "quest_ids": arr(S()), "minutes": I(minimum=0)}),
    "LogEntry": obj({"on": date_, "kind": {"enum": list(C.XP)}, "xp": I(minimum=0)}, ["on", "kind"]),
    "Progress": obj({"xp": I(minimum=0), "level": I(minimum=1), "streak_days": I(minimum=0)}),
    "Session": obj({"on": date_, "before": score, "after": score, "minutes": I(minimum=0), "hotspots": arr(ref("HotspotId"))}),
    "WeeklyReset": obj({"next_reset": date_, "days_left": I(minimum=0, maximum=6), "done_this_week": {"type": "boolean"}}),
    "Wrapped": obj({"month": S(pattern=r"^\d{4}-\d{2}$"), "sessions": I(minimum=0), "minutes": I(minimum=0), "avg_delta": I(), "best_delta": I(),
                    "top_hotspot": {"anyOf": [ref("HotspotId"), {"type": "null"}]}, "hotspot_counts": {"type": "object", "propertyNames": ref("HotspotId"), "additionalProperties": I(minimum=1)}}),
    "LocalStore": obj({"version": {"const": 1}, "name": S(), "roommates": arr(S(), maxItems=6), "sessions": arr(ref("Session")), "items": arr(ref("DeclutterItem")),
                       "log": arr(ref("LogEntry")), "settings": obj({"reset_weekday": I(minimum=0, maximum=6), "notify": {"type": "boolean"}, "sound": {"type": "boolean"}})}),
    "AiScanRequest": obj({"image": S(description="base64 JPEG ≤ 1280px"), "allowed_hotspots": arr(ref("HotspotId"))}),
    "AiScanResponse": obj({"is_room_photo": {"type": "boolean"}, "hotspots": arr(obj({"id": ref("HotspotId"), "severity": ref("Severity"),
                           "confidence": {"type": "number", "minimum": 0, "maximum": 1}, "box": arr({"type": "number", "minimum": 0, "maximum": 1}, minItems=4, maxItems=4)}), maxItems=13),
                           "note_th": S(maxLength=120)}),
    "AiPepTalkRequest": obj({"quest": ref("Quest"), "live_score": score, "style": {"enum": ["coach", "bestie", "army"]}}),
    "AiPepTalkResponse": obj({"text_th": S(maxLength=60)}),
}
ROOT = {"$schema": "https://json-schema.org/draft/2020-12/schema", "$id": "https://example.invalid/cleanquest/schemas.json",
        "title": "CleanQuest (ห้องรกหาย) data contracts", "$defs": D}
