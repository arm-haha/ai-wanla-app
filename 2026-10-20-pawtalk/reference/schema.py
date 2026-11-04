"""JSON Schema (draft 2020-12) for PawTalk. build.py writes it to ../schemas.json."""
import pawtalk as P
ALL_CUES = sorted({c for t in P.CUES.values() for c in t})
S = lambda **k: dict(type="string", **k)
I = lambda **k: dict(type="integer", **k)
date_ = S(format="date", pattern=r"^\d{4}-\d{2}-\d{2}$")
hhmm = S(pattern=r"^([01]\d|2[0-3]):[0-5]\d$")
ref = lambda n: {"$ref": f"#/$defs/{n}"}
arr = lambda x, **k: dict(type="array", items=x, **k)
def obj(props, req=None, extra=False):
    return {"type": "object", "properties": props, "required": req if req is not None else list(props), "additionalProperties": extra}
D = {
    "Species": {"enum": ["cat", "dog"]},
    "Mood": {"enum": P.MOODS},
    "Persona": {"enum": P.PERSONAS},
    "CueId": {"enum": ALL_CUES},
    "SymptomId": {"enum": list(P.SYMPTOMS)},
    "TriageLevel": {"enum": ["emergency", "soon", "watch", "ok"]},
    "CareKind": {"enum": ["deworm", "flea", "vaccine", "nail", "bath", "heartworm", "grooming", "litter", "custom"]},
    "CareStatusEnum": {"enum": ["overdue", "due_soon", "ok"]},
    "Pet": obj({"id": S(minLength=1), "name": S(minLength=1, maxLength=24), "species": ref("Species"), "breed_th": S(),
                "sex": {"enum": ["male", "female", "unknown"]}, "age_years": {"type": "number", "minimum": 0, "maximum": 30},
                "weight_kg": {"type": "number", "exclusiveMinimum": 0, "maximum": 100}, "neutered": {"type": "boolean"},
                "size": {"enum": ["small", "medium", "large"]}, "persona": ref("Persona"), "meal_times": arr(hhmm, maxItems=6),
                "goal": {"enum": ["weight_loss"]}, "photo_id": S()},
               ["id", "name", "species", "age_years", "weight_kg", "neutered", "persona", "meal_times"]),
    "SnapInput": obj({"pet_id": S(), "at": hhmm, "cues": arr(ref("CueId"), minItems=1, maxItems=8, uniqueItems=True),
                      "source": {"enum": ["ai_suggested", "user_picked", "demo"]}, "photo_id": S()}, ["pet_id", "at", "cues", "source"]),
    "MoodShare": obj({"mood": ref("Mood"), "points": I(minimum=1), "pct": I(minimum=0, maximum=100), "label_th": S(), "emoji": S()}),
    "MoodResult": obj({"species": ref("Species"), "cues": arr(ref("CueId")), "meal_bonus": {"type": "boolean"},
                       "minutes_to_meal": {"type": ["integer", "null"], "minimum": 0, "maximum": 1439},
                       "moods": arr(ref("MoodShare")), "top_mood": ref("Mood"), "vibe_score": I(minimum=0, maximum=100),
                       "vibe_label": {"enum": ["ฟินมาก", "โอเค", "ระวังนะ"]}, "safety_hint": {"type": ["string", "null"]}}),
    "ThoughtBubble": obj({"pet_id": S(), "mood": ref("Mood"), "persona": ref("Persona"), "persona_th": S(), "template_index": I(minimum=0, maximum=2),
                          "text_th": S(minLength=1, maxLength=80), "emoji": S(), "badge_th": S(), "disclaimer_th": S()}),
    "DuetLine": obj({"pet_id": S(), "text_th": S(maxLength=80)}),
    "Duet": arr(ref("DuetLine"), minItems=3, maxItems=3),
    "CareItem": obj({"id": S(), "pet_id": S(), "kind": ref("CareKind"), "label_th": S(), "last_done": date_, "interval_days": I(minimum=1, maximum=730)}),
    "CareStatus": obj({"task_id": S(), "pet_id": S(), "kind": ref("CareKind"), "label_th": S(), "due_on": date_, "days_left": I(), "status": ref("CareStatusEnum")}),
    "NextMeal": obj({"at": hhmm, "in_min": I(minimum=0, maximum=1439)}),
    "SymptomHit": obj({"id": ref("SymptomId"), "level": ref("TriageLevel"), "label_th": S()}),
    "HealthResult": obj({"pet_id": S(), "symptoms": arr(ref("SymptomHit")), "level": ref("TriageLevel"), "level_th": S(),
                         "escalated": {"type": "boolean"}, "show_vet_finder": {"type": "boolean"}, "disclaimer_th": S()}),
    "FoodPlan": obj({"pet_id": S(), "stage": {"enum": ["young", "neutered", "intact", "weight_loss"]}, "rer_kcal": I(minimum=1), "factor": {"type": "number"},
                     "kcal_per_day": I(minimum=1), "grams_per_day": I(minimum=1), "meals_per_day": I(minimum=1, maximum=6), "grams_per_meal": I(minimum=1), "note_th": S()}),
    "HumanAge": obj({"pet_id": S(), "pet_years": {"type": "number"}, "human_years": I(minimum=0), "note_th": S()}),
    "LogEntry": obj({"on": date_, "kind": {"enum": list(P.XP)}, "pet_id": S(), "mood": ref("Mood")}, ["on", "kind", "pet_id"]),
    "Progress": obj({"xp": I(minimum=0), "level": I(minimum=1), "streak_days": I(minimum=0)}),
    "Wrapped": obj({"pet_id": S(), "month": S(pattern=r"^\d{4}-\d{2}$"), "snaps": I(minimum=0), "mood_counts": {"type": "object", "additionalProperties": I(minimum=1)},
                    "top_mood": {"anyOf": [ref("Mood"), {"type": "null"}]}, "happy_pct": I(minimum=0, maximum=100),
                    "grumpiest_weekday": {"type": ["string", "null"]}, "care_done": I(minimum=0)}),
    "PetIdCard": obj({"pet_id": S(), "title_th": S(), "lines_th": arr(S(), minItems=3, maxItems=6), "human_age": I(), "persona_th": S(),
                      "top_mood_emoji": S(), "size_px": {"const": [1080, 1350]}, "watermark": {"const": "PawTalk · AI วันละแอป"}}),
    "MemeCard": obj({"pet_id": S(), "bubble": ref("ThoughtBubble"), "size_px": {"const": [1080, 1920]}, "layout": {"enum": ["bubble_top", "bubble_side", "duet_chat"]},
                     "watermark": {"const": "PawTalk · AI วันละแอป"}}),
    "LocalStore": obj({"version": {"const": 1}, "owner_name": S(), "pets": arr(ref("Pet"), maxItems=10), "care": arr(ref("CareItem")),
                       "log": arr(ref("LogEntry")), "settings": obj({"notify": {"type": "boolean"}, "lang": {"enum": ["th", "en"]}})}),
    "AiCueRequest": obj({"species": ref("Species"), "image": S(description="base64 JPEG ≤ 1024px"), "allowed_cues": arr(ref("CueId"))}),
    "AiCueResponse": obj({"species_seen": {"enum": ["cat", "dog", "other", "none"]}, "cues": arr(obj({"cue": ref("CueId"), "confidence": {"type": "number", "minimum": 0, "maximum": 1}}), maxItems=8),
                          "is_pet_photo": {"type": "boolean"}, "note_th": S(maxLength=120)}),
    "AiCaptionRequest": obj({"bubble": ref("ThoughtBubble"), "pet_name": S(), "max_chars": I(maximum=80)}),
    "AiCaptionResponse": obj({"text_th": S(maxLength=80), "kept_mood": ref("Mood")}),
}
ROOT = {"$schema": "https://json-schema.org/draft/2020-12/schema", "$id": "https://example.invalid/pawtalk/schemas.json",
        "title": "PawTalk (แมวหมาพูดได้) data contracts", "$defs": D}
