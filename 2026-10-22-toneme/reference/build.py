"""Build ../examples.json and ../schemas.json from the engine, then validate every object."""
import json, pathlib, jsonschema
import toneme as T, fixtures as X
from schema import ROOT
OUT = pathlib.Path(__file__).resolve().parent.parent
COLORS = {"linen": "#FBF7F2", "ink": "#2B2238", "rose": "#E8879B", "peach": "#F6B48F", "sage": "#8FB8A0", "sky": "#8DB6E8", "gold": "#D4A64A", "no": "#E5484D"}
p = T.analyze(**X.SAMPLE)
drape = T.drape_battle(p, *X.DRAPE)
card = T.palette_card(p, X.NAME)
fit, fit2 = T.outfit_check(p, X.OUTFIT), T.outfit_check(p, X.OUTFIT_SWAP)
mk, shop, audit, hair, grp = T.makeup(p), T.shop_scan(p, X.SHOP), T.closet_audit(p, X.CLOSET), T.hair_guide(p), T.friend_compare(X.FRIENDS)
season_demos = {k: T.analyze(**v) for k, v in {
    "light_spring": dict(skin="#F5D5C0", hair="#7A5A3A", eyes="#5A3E2B"), "bright_spring": dict(skin="#F2D2BD", hair="#3B2A20", eyes="#3A2618"),
    "true_summer": dict(skin="#E9C9B9", hair="#1B1B1B", eyes="#1E1410"), "true_winter": dict(skin="#C49A8E", hair="#121212", eyes="#140E0C", vein="blue", metal="silver"), "true_autumn": X.SAMPLE}.items()}
store = {"version": 1, "name": X.NAME, "profile": p, "closet": X.CLOSET, "friends": X.FRIENDS, "settings": {"keep_selfie": False, "show_avoid": True}}
ai_scan = {"face_found": True, "light_ok": True, "light_issue": "none",
           "regions": {"cheek_l": [0.30, 0.48, 0.10, 0.08], "cheek_r": [0.60, 0.48, 0.10, 0.08], "forehead": [0.42, 0.22, 0.16, 0.08], "hair": [0.20, 0.05, 0.60, 0.10], "iris": [0.40, 0.38, 0.04, 0.03]},
           "note_th": "แสงหน้าต่างด้านข้าง สม่ำเสมอดี ไม่เห็นฟิลเตอร์"}
stylist = {"office": "ออทัมน์สายทำงาน เทียล+ครีมอูฐ ดูแพงแบบไม่ต้องพยายาม", "date": "ลิปอิฐ+เสื้อส้มฟักทอง หน้าฉ่ำแบบไม่ต้องปัดเพิ่ม"}
ui = {"home_title": "สีไหนใช่เรา? ให้ AI ดูให้ใน 10 วิ", "scan_cta": "🤳 สแกนหน้า (แสงกลางวัน)", "light_tip": "หันหน้าเข้าหน้าต่าง ไม่แต่งหน้า ปิดฟิลเตอร์",
      "bad_light": "แสงเหลือง/มืดไป ผลอาจเพี้ยน ลองย้ายไปริมหน้าต่างนะ", "quiz_vein": "เส้นเลือดที่ข้อมือเป็นสีอะไร?", "quiz_metal": "ใส่ทองหรือเงินแล้วหน้าดูดีกว่า?",
      "reveal": "คุณคือ… {label_th}", "drape_cta": "ลองทาบผ้า 2 สี ⚔️", "palette_save": "เซฟพาเลตต์เป็นวอลเปเปอร์", "outfit_cta": "📸 เช็กชุดวันนี้",
      "shop_cta": "สแกนสีในร้าน", "closet_title": "ตู้เสื้อผ้าเข้ากับเราแค่ไหน", "friends_cta": "ชวนแก๊งหาสีกลาง",
      "privacy": "เซลฟี่ไม่ถูกเก็บ อ่านแค่สีแล้วลบทันที", "disclaimer": "ผลนี้เป็นไกด์สนุกๆ ไม่มีสีผิวไหนดีกว่ากัน ทุกโทนสวยในสีของตัวเอง"}
reel = [{"t": "0–3s", "shot": "ถือเสื้อชมพูบาร์บี้ทาบหน้า หน้าหมอง", "overlay_th": "ทำไมใส่สีนี้แล้วหน้าโทรม…"},
        {"t": "3–7s", "shot": "speed-ramp gen แอปด้วย AI", "overlay_th": "เลยให้ AI สร้างแอปหาสีที่ใช่"},
        {"t": "7–12s", "shot": "เซลฟี่ → จุดสีเด้งบนแก้ม/ผม/ตา → เปิดการ์ด True Autumn 🍂", "overlay_th": "เราคือ ออทัมน์ 🍂"},
        {"t": "12–17s", "shot": "Drape Battle สลับผ้า ส้มฟักทอง 96 vs ชมพูบาร์บี้ 0", "overlay_th": "ส้ม 96 · ชมพู 0 💀"},
        {"t": "17–23s", "shot": "เช็กชุด เสื้อฟ้า 50 → เปลี่ยนเป็นเทียล 96", "overlay_th": "แค่เปลี่ยนเสื้อ 50 → 96"},
        {"t": "23–27s", "shot": "แวบ ลิป/บลัช + ตู้เสื้อผ้า 50% + แก๊ง 4 คนสีครีมอูฐ", "overlay_th": "ลิป ตู้เสื้อผ้า เพื่อนทั้งแก๊ง"},
        {"t": "27–30s", "shot": "พาเลตต์เป็นวอลเปเปอร์มือถือ", "overlay_th": "คอมเมนต์ 'สี' เดี๋ยวส่งลิงก์ฟรี"}]
expect = {"profile": [p["label"], p["warmth"], p["lightness"], p["contrast"], p["confidence"]], "drape": [drape["a"]["score"], drape["b"]["score"], drape["winner"]],
          "outfit": [fit["overall"], fit2["overall"]], "shop": [shop["score"], shop["verdict"]], "audit": [audit["match_pct"], audit["buy_next_th"]],
          "group": [grp["group_color_th"], grp["avg_score"]], "season_demos": {k: v["label"] for k, v in season_demos.items()}}
EX = {"_note": "ข้อมูลทั้งหมดเป็นตัวอย่างสมมติ (มายด์) สร้างโดย reference/build.py", "today": X.TODAY, "colors": COLORS,
      "palettes": {s: {k: [{"name_th": n, "hex": h} for n, h in v[k]] for k in v} for s, v in T.PALETTES.items()},
      "scan_sample": {**X.SAMPLE, "light_ok": True}, "profile": p, "season_demos": season_demos, "drape_battle": drape, "palette_card": card,
      "outfit_before": fit, "outfit_after_swap": fit2, "makeup": mk, "shop_scan": shop, "closet_audit": audit, "hair_guide": hair,
      "friend_compare": grp, "local_store": store, "ai_scan_response_example": ai_scan, "ai_stylist_examples": stylist, "ui_copy_th": ui,
      "reel_script": reel, "expect_locked": expect}
CHECK = [("ScanSample", EX["scan_sample"]), ("Profile", p)] + [("Profile", v) for v in season_demos.values()] + [("DrapeBattle", drape), ("PaletteCard", card),
         ("OutfitCheck", fit), ("OutfitCheck", fit2), ("Makeup", mk), ("ShopScan", shop), ("ClosetAudit", audit), ("FriendCompare", grp), ("LocalStore", store),
         ("AiScanResponse", ai_scan)] + [("Swatch", h) for h in hair] + [("AiStylistResponse", {"caption_th": c}) for c in stylist.values()]
if __name__ == "__main__":
    errs = 0
    for name, o in CHECK:
        v = jsonschema.Draft202012Validator({**ROOT, "$ref": f"#/$defs/{name}"}, format_checker=jsonschema.FormatChecker())
        for e in v.iter_errors(o): errs += 1; print(name, e.message)
    (OUT / "schemas.json").write_text(json.dumps(ROOT, ensure_ascii=False, indent=2))
    (OUT / "examples.json").write_text(json.dumps(EX, ensure_ascii=False, indent=2))
    print(f"validated {len(CHECK)} objects, {errs} errors, {len(ROOT['$defs'])} defs")
    raise SystemExit(1 if errs else 0)
