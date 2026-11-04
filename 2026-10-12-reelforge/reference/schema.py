"""Generate schemas.json (draft 2020-12) and validate examples.json."""
import json
from pathlib import Path
from jsonschema import Draft202012Validator

R = lambda n: {"$ref": f"#/$defs/{n}"}
def obj(props, req=None, extra=False):
    return {"type": "object", "properties": props,
            "required": req if req is not None else list(props),
            "additionalProperties": extra}
S = {"type": "string"}; N = {"type": "number"}; I = {"type": "integer"}; B = {"type": "boolean"}
NS = {"type": ["string", "null"]}
NN = {"type": ["number", "null"]}
NI = {"type": ["integer", "null"]}
arr = lambda x, **k: {"type": "array", "items": x, **k}

STYLE_ENUM = ["soft_sell_before_after", "teach_3_steps", "storytime", "unboxing", "soft_sell"]
CAT_ENUM = ["snacks", "beauty", "study", "fashion", "drink", "fitness", "tech", "gift", "other"]
ROLE_ENUM = ["hook", "problem", "product_reveal", "howto", "cta", "step", "setup", "twist",
             "lesson", "box", "details", "benefit", "proof"]

D = {
 "HexColor": {"type": "string", "pattern": "^#[0-9A-Fa-f]{6}$"},
 "DateLocal": {"type": "string", "pattern": "^\\d{4}-\\d{2}-\\d{2}$"},
 "DateTime": {"type": "string", "pattern": "^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}(\\+07:00|Z)$"},
 "StyleId": {"type": "string", "enum": STYLE_ENUM},
 "CategoryKey": {"type": "string", "enum": CAT_ENUM},
 "Channel": {"type": ["string", "null"], "enum": ["LINE", "IG", "TikTok", "Shopee", "Lazada", "Facebook", None]},
 "ShotRole": {"type": "string", "enum": ROLE_ENUM},
 "HookAngle": {"type": "string", "enum": ["contrast", "transformation", "product_pain", "curiosity", "howto", "story"]},
 "HookScores": obj({
    "curiosity": {"type": "integer", "minimum": 0, "maximum": 100},
    "clarity": {"type": "integer", "minimum": 0, "maximum": 100},
    "emotion": {"type": "integer", "minimum": 0, "maximum": 100},
    "total": {"type": "integer", "minimum": 0, "maximum": 300},
 }),
 "ParsedIdea": obj({
    "raw": S, "normalized": S, "product": S, "category": R("CategoryKey"),
    "category_label_th": S, "emoji": S, "matched_keyword": NS,
    "price_unit": NN, "price_set": NN, "set_qty": NI,
    "channel": R("Channel"), "area": NS, "cta_keyword": S, "lang": {"const": "th"},
 }),
 "HookCandidate": obj({
    "id": S, "text_th": S, "angle": R("HookAngle"),
    "scores": R("HookScores"), "rank": I, "is_winner": B,
 }),
 "HookSelected": obj({
    "id": S, "text_th": S, "angle": R("HookAngle"),
    "scores": R("HookScores"), "rank": I,
 }),
 "Shot": obj({
    "n": I, "shot_id": S, "beat_id": S, "role": R("ShotRole"),
    "start_s": I, "duration_s": I, "end_s": I,
    "title_th": S, "overlay_th": S, "vo_th": S, "prompt_th": S, "camera_th": S,
 }),
 "Blueprint": obj({
    "blueprint_id": S, "idea": R("ParsedIdea"), "style": R("StyleId"),
    "style_label_th": S, "style_emoji": S,
    "duration_target_s": I, "duration_total_s": I,
    "bgm_mood": S, "bgm_mood_th": S,
    "hook": R("HookSelected"), "hooks_ranked": arr(R("HookCandidate"), minItems=3, maxItems=3),
    "shots": arr(R("Shot"), minItems=3, maxItems=8),
    "shot_count": I, "cta_keyword": S, "created_from": S,
 }),
 "CaptionPack": obj({
    "caption_short_th": S, "caption_long_th": S,
    "hashtags": arr(S, minItems=8, maxItems=12),
    "comment_cta_keyword": S, "comment_cta_line_th": S,
    "lang": {"const": "th"}, "char_count_short": I, "char_count_long": I,
 }),
 "OverlayLine": obj({
    "shot_id": S, "n": I, "overlay_th": S, "font_hint": S,
    "safe_zone": S, "max_chars": I,
 }),
 "CoverVariant": obj({
    "id": S, "variant": {"enum": ["contrast", "product", "cta"]},
    "size": arr(I, minItems=2, maxItems=2),
    "title_th": S, "subtitle_th": S, "badge_th": S,
    "bg": R("HexColor"), "accent": R("HexColor"),
 }),
 "OverlaysPack": obj({
    "per_shot": arr(R("OverlayLine")), "covers": arr(R("CoverVariant"), minItems=3, maxItems=3),
    "hook_line_th": S, "export_format": {"const": "png"},
    "export_size": arr(I, minItems=2, maxItems=2),
 }),
 "FilmProgress": obj({
    "total_s": N, "elapsed_s": N, "remaining_s": N, "done": B,
    "shot_index": I, "shot_n": I, "shot_id": S,
    "shot_elapsed_s": N, "shot_remaining_s": N,
    "shot_progress": N, "overall_progress": N,
    "prompt_th": S, "overlay_th": S,
 }),
 "StyleTemplate": obj({
    "id": R("StyleId"), "label_th": S, "emoji": S,
    "bgm_mood": S, "bgm_mood_th": S, "beat_count": I,
    "beat_roles": arr(R("ShotRole")), "default_weights": arr(I),
 }),
 "CategoryRule": obj({
    "keywords": arr(S, minItems=1), "category": R("CategoryKey"),
    "label_th": S, "emoji": S, "cta_keyword_default": S,
 }),
 "TrendAngle": obj({
    "id": S, "title_th": S, "desc_th": S, "style": R("StyleId"),
 }),
 "ShareCard": obj({
    "id": S, "variant": {"enum": ["blueprint_story", "cover_story", "hook_square"]},
    "size": arr(I, minItems=2, maxItems=2),
    "title_th": S, "subtitle_th": S, "lines_th": arr(S, maxItems=6),
    "footer_th": S, "theme": S, "show_product": B,
    "bg": R("HexColor"), "accent": R("HexColor"),
 }),
 "ExportPack": obj({
    "zip_name": S,
    "files": arr(obj({"name": S, "desc_th": S})),
    "includes_ai": B,
 }),
 "Streak": obj({"days": I, "last_date": R("DateLocal"), "label_th": S}),
 "HistoryItem": obj({
    "blueprint_id": S, "title_th": S, "created_at": R("DateTime"), "duration_s": I,
 }),
 "Settings": obj({
    "lang": {"enum": ["th", "en"]}, "default_style": R("StyleId"),
    "default_duration_s": I, "ai_assist": {"enum": ["off", "hooks", "captions", "full"]},
    "haptics": B, "keep_history": B, "auto_advance_film": B, "countdown_beep": B,
    "export_includes_json": B, "theme": S,
 }),
 "LocalStore": obj({
    "key": {"const": "reelforge:v1"}, "version": {"const": 1},
    "settings": R("Settings"), "blueprint_count": I,
    "streak": R("Streak"), "last_blueprint_id": S, "note": S,
 }),
 "Persona": obj({"name": S, "role_th": S, "note_th": S}),
 "ReelBeat": obj({"t": S, "shot": S, "overlay": S, "vo": S}),
 "FeatureItem": obj({"key": S, "label": S, "done": B}),
 "FeatureChecklist": obj({
    "must_have": arr(R("FeatureItem"), minItems=5),
    "nice_to_have": arr(R("FeatureItem")),
 }),
 "AnalyticsEvent": obj({
    "name": {"enum": [
        "idea_submitted", "blueprint_built", "film_mode_started", "hook_swapped",
        "cover_exported", "share_card_exported", "demo_loaded", "export_zip",
    ]},
    "at": R("DateTime"), "props": {"type": "object"},
 }, req=["name", "at"]),
 "TestVector": obj({"name": S, "fn": S, "input": {"type": "object"}, "expect": {"type": "object"}},
                   req=["name", "fn", "expect"]),
 "ExpectLocked": obj({
    "product": S, "category": R("CategoryKey"), "price_unit": N, "price_set": N,
    "set_qty": I, "channel": S, "area": S, "cta_keyword": S,
    "shot_count": I, "durations": arr(I), "hook_winner_id": S,
    "hook_winner_contains": arr(S), "cover_count": I, "hooks_count": I,
 }),
 "Colors": obj({
    "bg": R("HexColor"), "magenta": R("HexColor"), "violet": R("HexColor"),
    "cream": R("HexColor"), "gold": R("HexColor"),
 }),
 "Meta": obj({
    "app": {"const": "ReelForge"}, "pack_date": R("DateLocal"),
    "day_in_queue": S, "channel": S, "persona_note": S,
    "timezone": {"const": "Asia/Bangkok"}, "today": R("DateLocal"),
    "hook_line_th": S, "colors": R("Colors"),
 }),
 "DemoInput": obj({
    "raw_idea": S, "style": R("StyleId"), "duration_target_s": I, "source": S,
 }),
 "ExtraIdea": obj({
    "id": S, "idea": R("ParsedIdea"),
    "blueprint_summary": obj({
        "blueprint_id": S, "style": R("StyleId"), "duration_total_s": I,
        "shot_count": I, "hook_th": S, "cta_keyword": S, "durations": arr(I),
    }),
 }),
 "HookLab": obj({
    "hooks": arr(R("HookCandidate"), minItems=3, maxItems=3),
    "winner_id": S,
    "swap_example": obj({
        "selected": S, "after_hook_id": S, "after_shot1_overlay": S, "duration_still_s": I,
    }),
 }),
 "FilmModeExamples": obj({
    "at_0s": R("FilmProgress"), "at_3s": R("FilmProgress"), "at_10s": R("FilmProgress"),
    "at_29s": R("FilmProgress"), "at_30s_done": R("FilmProgress"),
    "rewind_to_shot3": R("FilmProgress"),
 }),
 # runtime AI contracts
 "AiHooksRequest": obj({
    "idea_normalized": S, "product": S, "category": R("CategoryKey"),
    "style": R("StyleId"), "existing_hooks": arr(S),
 }, req=["idea_normalized", "product", "style"]),
 "AiHooksResponse": obj({
    "hooks": arr(obj({"text_th": S, "angle": S}, req=["text_th"]), minItems=1, maxItems=5),
    "note_th": S,
 }),
 "AiCaptionRequest": obj({
    "blueprint_id": S, "product": S, "hook_th": S, "cta_keyword": S, "tone": S,
 }, req=["product", "hook_th", "cta_keyword"]),
 "AiCaptionResponse": obj({
    "caption_short_th": S, "caption_long_th": S, "hashtags": arr(S),
 }),
 "AiAngleRequest": obj({"idea_normalized": S, "category": R("CategoryKey")}, req=["idea_normalized"]),
 "AiAngleResponse": obj({"angles": arr(obj({"title_th": S, "desc_th": S, "style": R("StyleId")}))}),
}

schema = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://ai-wanla-app.local/reelforge/schemas.json",
    "title": "ReelForge examples.json root",
    "description": "Demo fixture + UI copy + test vectors for ReelForge (AI วันละแอป Day 10/10)",
    "$defs": D,
    "type": "object",
    "required": [
        "meta", "persona", "demo_input", "idea_parsed", "style_library",
        "blueprint_example", "caption_pack_example", "overlays_example",
        "hook_lab_example", "film_mode_examples", "ui_copy_th", "reel_script_th",
        "test_vectors", "feature_checklist_example", "expect_locked",
    ],
    "properties": {
        "meta": R("Meta"),
        "persona": R("Persona"),
        "demo_input": R("DemoInput"),
        "idea_parsed": R("ParsedIdea"),
        "style_library": arr(R("StyleTemplate"), minItems=5),
        "category_rules": arr(R("CategoryRule")),
        "blueprint_example": R("Blueprint"),
        "caption_pack_example": R("CaptionPack"),
        "overlays_example": R("OverlaysPack"),
        "hook_lab_example": R("HookLab"),
        "film_mode_examples": R("FilmModeExamples"),
        "trend_angles_example": arr(R("TrendAngle")),
        "extra_ideas": arr(R("ExtraIdea")),
        "history_example": arr(R("HistoryItem")),
        "streak_example": R("Streak"),
        "share_card_example": R("ShareCard"),
        "export_pack_example": R("ExportPack"),
        "settings_example": R("Settings"),
        "local_store_example": R("LocalStore"),
        "ui_copy_th": {"type": "object", "additionalProperties": S},
        "reel_script_th": arr(R("ReelBeat"), minItems=6),
        "test_vectors": arr(R("TestVector"), minItems=10),
        "feature_checklist_example": R("FeatureChecklist"),
        "analytics_events_example": arr(R("AnalyticsEvent")),
        "expect_locked": R("ExpectLocked"),
    },
    "additionalProperties": True,
}

root = Path(__file__).resolve().parent.parent
schema_path = root / "schemas.json"
schema_path.write_text(json.dumps(schema, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("wrote", schema_path, "defs", len(D), "bytes", schema_path.stat().st_size)

examples_path = root / "examples.json"
if examples_path.exists():
    examples = json.loads(examples_path.read_text(encoding="utf-8"))
    v = Draft202012Validator(schema)
    errors = sorted(v.iter_errors(examples), key=lambda e: list(e.path))
    if errors:
        print("SCHEMA ERRORS", len(errors))
        for e in errors[:20]:
            print(" -", "/".join(str(p) for p in e.path), e.message)
    else:
        print("schema validate: 0 errors")
else:
    print("examples.json missing — run build.py first")
