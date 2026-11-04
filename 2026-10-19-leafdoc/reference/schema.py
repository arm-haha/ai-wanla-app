"""JSON Schema (draft 2020-12) for LeafDoc. build.py writes ../schemas.json and validates every example against it."""
import leaf as L
S = "string"; I = "integer"; N = "number"; B = "boolean"
def obj(props, req=None, extra=False):
    return {"type": "object", "properties": props, "required": req if req is not None else list(props), "additionalProperties": extra}
def arr(items, **kw):
    d = {"type": "array", "items": items}; d.update(kw); return d
def ref(n): return {"$ref": f"#/$defs/{n}"}
NUL = lambda t: {"type": [t, "null"]}
def enum(xs): return {"type": S, "enum": list(xs)}

DEFS = {
    "DateLocal": {"type": S, "pattern": r"^\d{4}-\d{2}-\d{2}$"},
    "HexColor": {"type": S, "pattern": "^#[0-9A-Fa-f]{6}$"},
    "SpeciesId": enum(L.SPECIES), "SymptomId": enum(L.SYMPTOMS), "CauseId": enum(L.CAUSES),
    "Light": enum(L.LIGHT_ORDER), "Pot": enum(L.POT_FACTOR), "Season": enum(L.SEASON_FACTOR), "Soil": enum(["wet", "moist", "dry"]),
    "Grade": {"type": S, "enum": [g[1] for g in L.GRADES], "description": "thriving ≥80 · fussy 60–79 · sick 40–59 · critical <40"},
    "Species": obj({"id": ref("SpeciesId"), "name_th": {"type": S}, "name_en": {"type": S}, "base_water_days": {"type": I, "minimum": 1},
                    "light_need": ref("Light"), "pet_toxic": {"type": B}, "humidity_lover": {"type": B}, "emoji": {"type": S}, "verified": {"type": B}}),
    "Symptom": obj({"id": ref("SymptomId"), "label_th": {"type": S}, "severity": {"type": I, "minimum": 1, "maximum": 40}}),
    "Cause": obj({"id": ref("CauseId"), "label_th": {"type": S}, "emoji": {"type": S}, "weights": {"type": "object", "additionalProperties": {"type": I}},
                  "explain_th": {"type": S}, "plan_th": arr({"type": S}, minItems=7, maxItems=7)}),
    "Plant": obj({"id": {"type": S, "pattern": "^p\\d+$"}, "nickname_th": {"type": S, "maxLength": 20}, "species": ref("SpeciesId"), "light": ref("Light"),
                  "pot": ref("Pot"), "last_watered": ref("DateLocal"), "added_on": ref("DateLocal"), "spot_th": {"type": S}, "photo_key": NUL(S)},
                 ["id", "nickname_th", "species", "light", "pot", "last_watered", "added_on"]),
    "CheckupContext": obj({"soil": ref("Soil"), "light": ref("Light"), "days_since_water": {"type": I, "minimum": 0}, "ac_room": {"type": B},
                           "months_since_feed": {"type": I, "minimum": 0}}, ["soil", "light", "days_since_water"]),
    "CheckupInput": obj({"plant_id": {"type": S}, "on": ref("DateLocal"), "symptoms": arr(ref("SymptomId"), uniqueItems=True), "ctx": ref("CheckupContext"),
                         "source": enum(["chips", "ai_vision", "demo"])}),
    "CauseScore": obj({"cause_id": ref("CauseId"), "label_th": {"type": S}, "emoji": {"type": S}, "points": {"type": I, "minimum": 1},
                       "confidence_pct": {"type": I, "minimum": 0, "maximum": 100}, "evidence": arr(ref("SymptomId"), minItems=1), "explain_th": {"type": S}}),
    "Diagnosis": obj({"engine": {"type": S}, "plant_id": {"type": S}, "species": ref("SpeciesId"), "on": ref("DateLocal"), "symptoms": arr(ref("SymptomId")),
                      "symptoms_th": arr({"type": S}), "health_score": {"type": I, "minimum": 5, "maximum": 100}, "grade": ref("Grade"), "grade_th": {"type": S},
                      "emoji": {"type": S}, "color": ref("HexColor"), "causes": arr(ref("CauseScore"), maxItems=3),
                      "top_cause": {"anyOf": [ref("CauseId"), {"type": "null"}]}, "disclaimer_th": {"type": S}}),
    "WaterStatus": obj({"interval_days": {"type": I, "minimum": 1}, "days_since": {"type": I}, "due_on": ref("DateLocal"), "days_left": {"type": I},
                        "status": enum(["overdue", "today", "soon", "ok"]), "status_th": {"type": S}, "season": ref("Season"),
                        "next_dates": arr(ref("DateLocal"), minItems=4, maxItems=4), "finger_test_th": {"type": S}}),
    "PlanDay": obj({"day": {"type": I, "minimum": 1, "maximum": 7}, "on": ref("DateLocal"), "task_th": {"type": S}, "done": {"type": B}, "extra_th": {"type": S}},
                   ["day", "on", "task_th", "done"]),
    "RescuePlan": obj({"plant_id": {"type": S}, "cause_id": {"anyOf": [ref("CauseId"), {"type": "null"}]}, "title_th": {"type": S}, "start_on": ref("DateLocal"),
                       "days": arr(ref("PlanDay"), minItems=7, maxItems=7), "recheck_on": ref("DateLocal")}),
    "PlanProgress": obj({"done": {"type": I}, "of": {"type": I}, "pct": {"type": I, "minimum": 0, "maximum": 100}}),
    "LightReading": obj({"lux_est": {"type": I, "minimum": 0}, "band": ref("Light"), "band_th": {"type": S}, "fits": arr(ref("SpeciesId")), "note_th": {"type": S}}),
    "PetCheck": obj({"species": ref("SpeciesId"), "pet_toxic": {"type": B}, "badge_th": {"type": S}, "verified": {"type": B}, "source_note": {"type": S}}),
    "RoomQuiz": obj({"light": ref("Light"), "ac_room": {"type": B}, "pets": {"type": B}, "forgetful": {"type": B}}),
    "RoomMatch": arr(obj({"species": ref("SpeciesId"), "name_th": {"type": S}, "emoji": {"type": S}, "fit": {"type": I, "minimum": 0, "maximum": 100}}), maxItems=3),
    "GlowUpCard": obj({"kind": {"const": "glow_up"}, "size": enum(["1080x1920", "1080x1350"]), "plant_id": {"type": S}, "before_on": ref("DateLocal"),
                       "after_on": ref("DateLocal"), "days": {"type": I}, "before_score": {"type": I}, "after_score": {"type": I}, "delta": {"type": I},
                       "new_leaves": {"type": I, "minimum": 0}, "headline_th": {"type": S}, "sub_th": {"type": S}, "bg": ref("HexColor"), "accent": ref("HexColor"), "footer": {"type": S}}),
    "JungleLevel": obj({"xp": {"type": I}, "level": {"type": I, "minimum": 1, "maximum": 5}, "title_th": {"type": S}, "next_at": NUL(I)}),
    "LogEntry": obj({"on": ref("DateLocal"), "kind": enum(["water", "checkup", "feed", "repot", "photo"]), "plant_id": {"type": S}, "on_time": {"type": B},
                     "top_cause": {"anyOf": [ref("CauseId"), {"type": "null"}]}, "delta": {"type": I}, "score": {"type": I}}, ["on", "kind", "plant_id"]),
    "Wrapped": obj({"month": {"type": S, "pattern": r"^\d{4}-\d{2}$"}, "waterings": {"type": I}, "on_time_pct": {"type": I}, "checkups": {"type": I},
                    "top_cause": {"anyOf": [ref("CauseId"), {"type": "null"}]}, "top_cause_th": NUL(S), "best_glow_plant": NUL(S), "best_delta": {"type": I}}),
    "Settings": obj({"reminder_time": {"type": S, "pattern": r"^\d{2}:\d{2}$"}, "has_pets": {"type": B}, "ac_room": {"type": B}, "ai_vision": {"type": B}}),
    "LocalStore": obj({"version": {"const": 1}, "settings": ref("Settings"), "plants": arr(ref("Plant"), maxItems=100), "diagnoses": arr(ref("Diagnosis")),
                       "plans": arr(ref("RescuePlan")), "log": arr(ref("LogEntry"), maxItems=2000), "care_days": arr(ref("DateLocal"))},
                      ["version", "settings", "plants", "log"]),
    "AiVisionRequest": obj({"image_b64_jpeg": {"type": S, "description": "≤ 1024px long side"}, "known_species": NUL(S)}),
    "AiVisionResponse": obj({"species_guess": {"anyOf": [ref("SpeciesId"), {"const": "unknown"}]}, "species_confidence": {"type": N, "minimum": 0, "maximum": 1},
                             "symptoms": arr(ref("SymptomId"), uniqueItems=True, maxItems=6), "leaf_boxes": arr(obj({"x": {"type": N}, "y": {"type": N}, "w": {"type": N}, "h": {"type": N}, "symptom": ref("SymptomId")}), maxItems=8),
                             "note_th": {"type": S, "maxLength": 120}}, ["species_guess", "species_confidence", "symptoms"]),
    "AiCareChatResponse": obj({"answer_th": {"type": S, "maxLength": 400}, "never_change_score": {"const": True}}),
}
ROOT = {"$schema": "https://json-schema.org/draft/2020-12/schema", "$id": "https://ai-wanla-app.local/leafdoc/schemas.json", "title": "LeafDoc schemas", "$defs": DEFS}
