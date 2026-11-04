"""JSON Schema (draft 2020-12) for ToneMe. build.py writes it to ../schemas.json."""
import toneme as T
S = lambda **k: dict(type="string", **k)
I = lambda **k: dict(type="integer", **k)
HEX = S(pattern=r"^#[0-9A-Fa-f]{6}$")
ref = lambda n: {"$ref": f"#/$defs/{n}"}
arr = lambda x, **k: dict(type="array", items=x, **k)
score = I(minimum=0, maximum=100)
def obj(props, req=None):
    return {"type": "object", "properties": props, "required": req if req is not None else list(props), "additionalProperties": False}
swatch = lambda key: obj({key: S(), "hex": HEX})
D = {
    "Hex": HEX, "Season": {"enum": list(T.PALETTES)}, "Sub": {"enum": list(T.SUB_TH)},
    "Vein": {"enum": list(T.VEIN)}, "Metal": {"enum": list(T.METAL)}, "Slot": {"enum": list(T.SLOT_TH)},
    "Verdict": {"enum": ["yes", "maybe", "no"]},
    "Swatch": swatch("name_th"),
    "ScanSample": obj({"skin": ref("Hex"), "hair": ref("Hex"), "eyes": ref("Hex"), "vein": ref("Vein"), "metal": ref("Metal"), "light_ok": {"type": "boolean"}},
                      ["skin", "hair", "eyes", "vein", "metal"]),
    "Profile": obj({"season": ref("Season"), "sub": ref("Sub"), "label": S(), "label_th": S(), "warmth": I(), "lightness": score, "contrast": score,
                    "undertone": {"enum": ["warm", "cool"]}, "depth": {"enum": ["light", "deep"]}, "chroma": {"enum": ["clear", "soft"]},
                    "confidence": I(minimum=50, maximum=95), "metal": {"enum": ["gold", "silver"]}}),
    "DrapeSide": obj({"hex": ref("Hex"), "score": score, "near_th": S()}),
    "DrapeBattle": obj({"a": ref("DrapeSide"), "b": ref("DrapeSide"), "winner": {"enum": ["a", "b"]}, "gap": score, "line_th": S()}),
    "PaletteCard": obj({"name": S(), "label": S(), "label_th": S(), "best": arr(ref("Swatch"), minItems=12, maxItems=12), "avoid": arr(ref("Swatch"), minItems=4, maxItems=4),
                        "metal": {"enum": ["gold", "silver"]}, "size_px": {"const": [1080, 1920]}, "watermark": {"const": "ToneMe · AI วันละแอป"}}),
    "OutfitItemInput": obj({"slot": ref("Slot"), "hex": ref("Hex")}),
    "OutfitRow": obj({"slot": ref("Slot"), "hex": ref("Hex"), "score": score, "verdict_th": S(), "verdict": ref("Verdict"), "swap_hex": ref("Hex"), "swap_th": S()}),
    "OutfitCheck": obj({"overall": score, "verdict_th": S(), "items": arr(ref("OutfitRow"), maxItems=7), "tip_th": S(maxLength=80)}),
    "Makeup": obj({"lip": arr(swatch("family_th"), minItems=1), "blush": arr(swatch("family_th"), minItems=1), "shadow": arr(swatch("family_th"), minItems=1), "note_th": S()}),
    "ShopScan": obj({"hex": ref("Hex"), "score": score, "verdict": ref("Verdict"), "verdict_th": S(), "near_th": S(), "near_hex": ref("Hex")}),
    "ClosetItem": obj({"id": S(), "name_th": S(minLength=1, maxLength=40), "hex": ref("Hex")}),
    "ClosetRow": obj({"id": S(), "name_th": S(), "hex": ref("Hex"), "score": score, "verdict": ref("Verdict"), "verdict_th": S(), "near_th": S(), "near_hex": ref("Hex")}),
    "ClosetAudit": obj({"total": I(minimum=0), "yes": I(minimum=0), "maybe": I(minimum=0), "no": I(minimum=0), "match_pct": score,
                        "items": arr(ref("ClosetRow")), "buy_next_th": arr(S(), maxItems=3)}),
    "Friend": obj({"name": S(), "season": ref("Season")}),
    "FriendCompare": obj({"members": arr(ref("Friend"), minItems=2, maxItems=8), "count": {"type": "object", "propertyNames": ref("Season"), "additionalProperties": I(minimum=1)},
                          "group_color_th": S(), "group_color_hex": ref("Hex"), "avg_score": score, "line_th": S()}),
    "LocalStore": obj({"version": {"const": 1}, "name": S(), "profile": ref("Profile"), "closet": arr(ref("ClosetItem"), maxItems=200),
                       "friends": arr(ref("Friend")), "settings": obj({"keep_selfie": {"const": False}, "show_avoid": {"type": "boolean"}})}),
    "AiScanRequest": obj({"image": S(description="base64 JPEG ≤ 1024px, ส่งเฉพาะตอนสแกน ไม่เก็บ"), "white_ref": {"type": "boolean"}}),
    "AiScanResponse": obj({"face_found": {"type": "boolean"}, "light_ok": {"type": "boolean"}, "light_issue": {"enum": ["none", "too_dark", "yellow_cast", "filter", "backlight", "makeup_heavy"]},
                           "regions": obj({k: arr({"type": "number", "minimum": 0, "maximum": 1}, minItems=4, maxItems=4) for k in ("cheek_l", "cheek_r", "forehead", "hair", "iris")}),
                           "note_th": S(maxLength=100)}),
    "AiStylistRequest": obj({"profile": ref("Profile"), "outfit": ref("OutfitCheck"), "vibe": {"enum": ["office", "date", "cafe", "wedding_guest"]}}),
    "AiStylistResponse": obj({"caption_th": S(maxLength=90)}),
}
ROOT = {"$schema": "https://json-schema.org/draft/2020-12/schema", "$id": "https://example.invalid/toneme/schemas.json",
        "title": "ToneMe (สีไหนใช่เรา) data contracts", "$defs": D}
