"""JSON Schema (draft 2020-12) for ScamScan. build.py writes ../schemas.json and validates every example against it."""
S = "string"; I = "integer"; N = "number"; B = "boolean"
def obj(props, req=None, extra=False):
    return {"type": "object", "properties": props, "required": req if req is not None else list(props), "additionalProperties": extra}
def arr(items, **kw):
    d = {"type": "array", "items": items}; d.update(kw); return d
def ref(n): return {"$ref": f"#/$defs/{n}"}
NUL = lambda t: {"type": [t, "null"]}

DEFS = {
    "DateLocal": {"type": S, "pattern": r"^\d{4}-\d{2}-\d{2}$"},
    "HexColor": {"type": S, "pattern": "^#[0-9A-Fa-f]{6}$"},
    "Channel": {"type": S, "enum": ["sms", "line", "messenger", "email", "call", "other"]},
    "RuleId": {"type": S, "enum": ["urgency","credential","money","too_good","authority","off_platform","link","brand_mismatch","shortener","bad_tld","no_https","punycode","ip_link"]},
    "LinkFlag": {"type": S, "enum": ["brand_mismatch","shortener","bad_tld","no_https","punycode","ip_link"]},
    "BrandId": {"type": S, "enum": ["kbank","scb","ktb","krungsri","bbl","thaipost","revenue","pea"]},
    "Level": {"type": S, "enum": ["scam","risky","caution","low"], "description": "scam ≥75 · risky 50–74 · caution 25–49 · low 0–24"},
    "Truth": {"type": S, "enum": ["scam","real"]},
    "ScanInput": obj({"text": {"type": S, "minLength": 1, "maxLength": 2000}, "sender": {"type": S}, "channel": ref("Channel"),
                      "source": {"type": S, "enum": ["paste","share_sheet","screenshot_ocr","demo"]}}, ["text","channel"]),
    "Rule": obj({"id": ref("RuleId"), "weight": {"type": I, "minimum": 0, "maximum": 50}, "label_th": {"type": S}, "explain_th": {"type": S},
                 "patterns": arr({"type": S})}),
    "Brand": obj({"id": ref("BrandId"), "name_th": {"type": S}, "text": arr({"type": S}), "host": arr({"type": S}),
                  "official": arr({"type": S}, minItems=1), "verified": {"type": B, "description": "set true only after checking the org's own site"}}),
    "Flag": obj({"rule_id": ref("RuleId"), "weight": {"type": I}, "label_th": {"type": S}, "explain_th": {"type": S}, "hits": {"type": I, "minimum": 1}}),
    "Highlight": obj({"start": {"type": I, "minimum": 0}, "end": {"type": I, "minimum": 1}, "text": {"type": S}, "rule_id": ref("RuleId")}),
    "LinkXray": obj({"raw": {"type": S}, "scheme": {"type": S, "enum": ["http","https","none"]}, "host": {"type": S}, "registered_domain": {"type": S},
                     "tld": {"type": S}, "host_tokens": arr({"type": S}), "claimed_brands": arr(ref("BrandId")), "official_match": arr(ref("BrandId")),
                     "flags": arr(ref("LinkFlag")), "verdict": {"type": S, "enum": ["official","fake_lookalike","hidden","suspicious","unknown"]},
                     "verdict_th": {"type": S}, "real_site": NUL(S)}),
    "ActionStep": obj({"icon": {"type": S}, "text_th": {"type": S}}),
    "ActionPlan": obj({"steps": arr(ref("ActionStep"), minItems=1), "safe_reply_th": NUL(S), "best_reply_th": NUL(S)}),
    "ScanResult": obj({"engine": {"type": S}, "channel": ref("Channel"), "sender": {"type": S}, "text": {"type": S},
                       "score": {"type": I, "minimum": 0, "maximum": 100}, "raw_score": {"type": I, "minimum": 0}, "combo_bonus": {"type": I, "enum": [0, 10]},
                       "level": ref("Level"), "label_th": {"type": S}, "color": ref("HexColor"), "emoji": {"type": S},
                       "flags": arr(ref("Flag")), "highlights": arr(ref("Highlight")), "links": arr(ref("LinkXray")),
                       "claimed_brands": arr(ref("BrandId")), "actions": ref("ActionPlan"), "disclaimer_th": {"type": S}}),
    "FamilyCard": obj({"kind": {"const": "family_alert"}, "size": {"type": S, "enum": ["1080x1350","1080x1920"]}, "to_th": {"type": S}, "from_th": {"type": S},
                       "title_th": {"type": S}, "lines_th": arr({"type": S}, minItems=2), "accent": ref("HexColor"), "bg": ref("HexColor"),
                       "footer": {"type": S}, "line_text_th": {"type": S, "description": "plain text for LINE share URL scheme"}}),
    "QuizCard": obj({"id": {"type": S, "pattern": "^q\\d{2}$"}, "truth": ref("Truth"), "channel": ref("Channel"), "sender": {"type": S}, "text": {"type": S}}),
    "QuizGrade": obj({"results": arr(obj({"id": {"type": S}, "answer": ref("Truth"), "correct": {"type": B}})), "right": {"type": I}, "of": {"type": I}, "badge_th": {"type": S}}),
    "CallSign": obj({"id": {"type": S, "pattern": "^cs_"}, "weight": {"type": I}, "label_th": {"type": S}}),
    "CallShield": obj({"ticked": arr({"type": S, "pattern": "^cs_"}), "score": {"type": I, "minimum": 0, "maximum": 100}, "level": ref("Level"),
                       "label_th": {"type": S}, "color": ref("HexColor"), "emoji": {"type": S}, "say_th": {"type": S}, "rule_th": {"type": S}}),
    "HistoryEntry": obj({"on": ref("DateLocal"), "score": {"type": I}, "level": ref("Level"), "top_rule": {"anyOf": [ref("RuleId"), {"type": "null"}]},
                         "brands": arr(ref("BrandId")), "preview_th": {"type": S, "maxLength": 40}}),
    "Wrapped": obj({"month": {"type": S, "pattern": r"^\d{4}-\d{2}$"}, "checked": {"type": I}, "flagged": {"type": I}, "low": {"type": I},
                    "top_rule_id": {"anyOf": [ref("RuleId"), {"type": "null"}]}, "top_rule_th": NUL(S),
                    "most_faked_brand": {"anyOf": [ref("BrandId"), {"type": "null"}]}, "most_faked_brand_th": NUL(S), "quiz_streak_days": {"type": I}}),
    "Settings": obj({"big_text": {"type": B}, "read_aloud": {"type": B, "description": "Web Speech API th-TH"}, "family": arr(obj({"name_th": {"type": S}, "relation_th": {"type": S}})),
                     "share_history_with_family": {"type": B}, "ai_explain": {"type": B}}),
    "LocalStore": obj({"version": {"const": 1}, "settings": ref("Settings"), "history": arr(ref("HistoryEntry"), maxItems=500),
                       "quiz_days": arr(ref("DateLocal")), "custom_brands": arr(ref("Brand")), "blocked_senders": arr({"type": S})},
                      ["version","settings","history","quiz_days"]),
    "AiExplainRequest": obj({"text": {"type": S}, "flags": arr(ref("RuleId")), "level": ref("Level"), "audience": {"type": S, "enum": ["elder","teen","general"]}}),
    "AiExplainResponse": obj({"summary_th": {"type": S, "maxLength": 200}, "why_th": arr({"type": S}, maxItems=3), "never_change_score": {"const": True}}),
    "AiOcrResponse": obj({"text": {"type": S}, "sender_guess": NUL(S), "channel_guess": ref("Channel"), "confidence": {"type": N, "minimum": 0, "maximum": 1}}),
}
ROOT = {"$schema": "https://json-schema.org/draft/2020-12/schema", "$id": "https://ai-wanla-app.local/scamscan/schemas.json", "title": "ScamScan schemas", "$defs": DEFS}
