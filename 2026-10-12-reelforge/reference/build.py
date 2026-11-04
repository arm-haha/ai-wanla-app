"""Build examples.json from deterministic engine + fixtures."""
import json
from pathlib import Path
from reel import (
    STYLES, STYLE_IDS, CATEGORY_RULES, parse_idea, build_blueprint,
    build_caption_pack, build_overlays, rank_hooks, film_progress,
    film_rewind, swap_hook, suggest_trend_angles, allocate_durations,
)
from fixtures import (
    TODAY, PERSONA, DEMO_IDEA_RAW, DEMO_STYLE, DEMO_DURATION, EXPECT,
    EXTRA_IDEAS, HISTORY_META, STREAK, COLORS,
)

TZ = "+07:00"

idea = parse_idea(DEMO_IDEA_RAW)
bp = build_blueprint(idea, DEMO_STYLE, DEMO_DURATION)
caps = build_caption_pack(bp)
ovs = build_overlays(bp)
angles = suggest_trend_angles(idea)

# film mode samples
film_t0 = film_progress(bp["shots"], 0)
film_t3 = film_progress(bp["shots"], 3.0)  # start of shot 2
film_t10 = film_progress(bp["shots"], 10.0)  # into shot 3 (3+6=9, so 1s into shot 3)
film_t29 = film_progress(bp["shots"], 29.0)
film_done = film_progress(bp["shots"], 30.0)
film_rew = film_rewind(bp["shots"], 2)  # rewind to shot index 2 (3rd shot)

# hook swap example: swap to hook_b
bp_swapped = swap_hook(bp, "hook_b")

# style library
style_library = []
for sid in STYLE_IDS:
    st = STYLES[sid]
    style_library.append({
        "id": sid,
        "label_th": st["label_th"],
        "emoji": st["emoji"],
        "bgm_mood": st["bgm_mood"],
        "bgm_mood_th": st["bgm_mood_th"],
        "beat_count": len(st["beats"]),
        "beat_roles": [b[1] for b in st["beats"]],
        "default_weights": [b[2] for b in st["beats"]],
    })

# extra blueprints
extra_bps = []
for ex in EXTRA_IDEAS:
    ei = parse_idea(ex["raw"])
    ebp = build_blueprint(ei, ex["style"], ex["duration"])
    extra_bps.append({
        "id": ex["id"],
        "idea": ei,
        "blueprint_summary": {
            "blueprint_id": ebp["blueprint_id"],
            "style": ebp["style"],
            "duration_total_s": ebp["duration_total_s"],
            "shot_count": ebp["shot_count"],
            "hook_th": ebp["hook"]["text_th"],
            "cta_keyword": ebp["cta_keyword"],
            "durations": [s["duration_s"] for s in ebp["shots"]],
        },
    })

# share blueprint card
share_card = {
    "id": "share_bp_cookie",
    "variant": "blueprint_story",
    "size": [1080, 1920],
    "title_th": "ชุดถ่าย 30 วิ พร้อมแล้ว",
    "subtitle_th": f"{idea['product']} · {bp['style_label_th']}",
    "lines_th": [
        f"ฮุค: {bp['hook']['text_th'][:36]}…",
        f"{bp['shot_count']} ช็อต · {bp['duration_total_s']} วิ",
        f"BGM: {bp['bgm_mood_th']}",
        f"CTA: 「{bp['cta_keyword']}」",
    ],
    "footer_th": "ReelForge · AI วันละแอป",
    "theme": "cinema_neon",
    "show_product": True,
    "bg": COLORS["bg"],
    "accent": COLORS["magenta"],
}

# export pack manifest
export_pack = {
    "zip_name": "reelforge-cookie-30s.zip",
    "files": [
        {"name": "blueprint.json", "desc_th": "โครงสร้างช็อต + เวลา + VO"},
        {"name": "captions.txt", "desc_th": "แคปชันสั้น/ยาว + แฮชแท็ก"},
        {"name": "overlays/", "desc_th": "PNG overlay รายช็อต + 3 ปก"},
        {"name": "README_th.txt", "desc_th": "วิธีถ่ายตาม Film Mode"},
    ],
    "includes_ai": False,
}

# category rules export
cat_rules = [
    {"keywords": kws, "category": cat, "label_th": lab, "emoji": em, "cta_keyword_default": cta}
    for kws, cat, lab, em, cta in CATEGORY_RULES
]

# UI copy Thai
ui_copy_th = {
    "home_title": "ReelForge",
    "home_sub": "โยนไอเดีย → ได้ชุดถ่ายพร้อมจับเวลา",
    "idea_placeholder": "เช่น ขายคุกกี้เนยสด ส่ง LINE ชิ้นละ 45…",
    "idea_cta": "สร้าง Blueprint",
    "demo_cta": "ลองข้อมูลตัวอย่าง · เจี๊ยบ",
    "voice_cta": "วางข้อความจาก voice note",
    "style_picker_title": "สไตล์คลิป",
    "duration_label": "ความยาวเป้าหมาย",
    "blueprint_ready": "ชุดถ่ายพร้อมแล้ว 🎬",
    "film_mode_cta": "เข้า Film Mode",
    "film_next": "ช็อตถัดไป",
    "film_rewind": "ถ่ายช็อตนี้อีกครั้ง",
    "film_done": "ครบทุกช็อต · เก่งมาก!",
    "caption_tab": "แคปชัน",
    "overlay_tab": "Overlay & ปก",
    "hooks_tab": "Hook A/B Lab",
    "swap_hook": "ใช้ฮุคนี้",
    "winner_badge": "ชนะ · แนะนำ",
    "export_cta": "ส่งออกแพ็ก ZIP",
    "share_cta": "แชร์การ์ด Blueprint",
    "cover_export": "บันทึกปก PNG",
    "privacy_badge": "ทำงานในเครื่อง · ไม่บังคับล็อกอิน",
    "streak_label": "สตรีคสร้างคลิป",
    "history_title": "Blueprint ล่าสุด",
    "trend_title": "มุมคลิปแนะนำ",
    "bgm_label": "มู้ด BGM",
    "cta_hint": "คำคอมเมนต์ CTA",
    "empty_idea": "วางไอเดียก่อนนะ จะได้สร้างชุดถ่ายให้",
    "toast_copied": "คัดลอกแล้ว",
    "toast_hook_swapped": "สลับฮุคแล้ว · ช็อต 1 อัปเดต",
    "disclaimer": "ตัวอย่างสมมติจากช่อง AI วันละแอป · ไม่ใช่คำแนะนำการตลาด",
}

# reel script for the channel's own Reel about this app
reel_script_th = [
    {"t": "0–3s", "shot": "มือถือเปิดหน้าโฮม ReelForge พื้นมืด + นีออน", "overlay": "ไอเดียในหัว แต่ไม่รู้จะเปิดคลิปยังไง?", "vo": "ไอเดียในหัวแต่ไม่รู้จะเปิดคลิปยังไง?"},
    {"t": "3–7s", "shot": "พิมพ์ไอเดียคุกกี้ / กดลองข้อมูลตัวอย่าง", "overlay": "โยนไอเดียเข้าไป 10 วิ", "vo": "โยนเข้าแอปนี้สิบวิ"},
    {"t": "7–12s", "shot": "Blueprint โผล่ 5 ช็อตพร้อมเวลา", "overlay": "ได้ชุดถ่าย · ฮุค · CTA", "vo": "ได้ชุดถ่ายพร้อมจับเวลาเลย"},
    {"t": "12–18s", "shot": "Film Mode นับถอยหลัง + การ์ดพรอมป์", "overlay": "Film Mode · ช็อต 1/5", "vo": "เข้าโหมดถ่าย มีตัวจับเวลาและข้อความบนจอ"},
    {"t": "18–22s", "shot": "Caption Pack + hashtags โผล่", "overlay": "แคปชันไทย · คอมเมนต์ คุกกี้", "vo": "แคปชันไทยพร้อมคำคอมเมนต์"},
    {"t": "22–26s", "shot": "Hook A/B Lab สลับฮุค / ปก 3 แบบ", "overlay": "ฮุค A/B + ปก 3 แบบ", "vo": "ทดลองฮุคสามแบบ เลือกอันที่แรงสุด"},
    {"t": "26–30s", "shot": "การ์ดแชร์ Blueprint + โลโก้ช่อง", "overlay": "คอมเมนต์ 「รีล」 รับลิงก์", "vo": "คอมเมนต์คำว่ารีล รับลิงก์ฟรี"},
]

# test vectors
test_vectors = [
    {
        "name": "parse_demo_cookie",
        "fn": "parse_idea",
        "input": {"raw": DEMO_IDEA_RAW},
        "expect": {
            "product": EXPECT["product"],
            "category": EXPECT["category"],
            "price_unit": EXPECT["price_unit"],
            "price_set": EXPECT["price_set"],
            "set_qty": EXPECT["set_qty"],
            "channel": EXPECT["channel"],
            "area": EXPECT["area"],
            "cta_keyword": EXPECT["cta_keyword"],
        },
    },
    {
        "name": "blueprint_30s_five_shots",
        "fn": "build_blueprint",
        "input": {"raw": DEMO_IDEA_RAW, "style": DEMO_STYLE, "duration_target": 30},
        "expect": {
            "shot_count": 5,
            "duration_total_s": 30,
            "durations": [3, 6, 8, 8, 5],
            "hook_id": "hook_a",
            "cta_keyword": "คุกกี้",
            "bgm_mood": "warm_upbeat",
        },
    },
    {
        "name": "hook_a_is_rank1",
        "fn": "rank_hooks",
        "input": {"raw": DEMO_IDEA_RAW, "style": DEMO_STYLE},
        "expect": {"winner_id": "hook_a", "hooks_count": 3, "winner_rank": 1},
    },
    {
        "name": "caption_has_cta_cookie",
        "fn": "build_caption_pack",
        "input": {"raw": DEMO_IDEA_RAW, "style": DEMO_STYLE, "duration_target": 30},
        "expect": {
            "comment_cta_keyword": "คุกกี้",
            "hashtag_min": 8,
            "short_contains": "คุกกี้",
        },
    },
    {
        "name": "overlays_three_covers",
        "fn": "build_overlays",
        "input": {"raw": DEMO_IDEA_RAW, "style": DEMO_STYLE, "duration_target": 30},
        "expect": {"cover_count": 3, "per_shot_count": 5, "cover_ids": ["cover_a", "cover_b", "cover_c"]},
    },
    {
        "name": "film_progress_at_0",
        "fn": "film_progress",
        "input": {"elapsed_s": 0},
        "expect": {"shot_n": 1, "done": False, "overall_progress": 0.0},
    },
    {
        "name": "film_progress_at_10",
        "fn": "film_progress",
        "input": {"elapsed_s": 10},
        "expect": {"shot_n": 3, "done": False},  # 3+6=9, so at 10s -> shot 3
    },
    {
        "name": "film_progress_done",
        "fn": "film_progress",
        "input": {"elapsed_s": 30},
        "expect": {"done": True, "remaining_s": 0},
    },
    {
        "name": "allocate_30_soft_sell",
        "fn": "allocate_durations",
        "input": {"weights": [3, 6, 8, 8, 5], "target": 30},
        "expect": {"durations": [3, 6, 8, 8, 5], "sum": 30},
    },
    {
        "name": "allocate_15_equalish",
        "fn": "allocate_durations",
        "input": {"weights": [3, 6, 8, 8, 5], "target": 15},
        "expect": {"sum": 15, "min_each": 1},
    },
    {
        "name": "swap_to_hook_b",
        "fn": "swap_hook",
        "input": {"hook_id": "hook_b"},
        "expect": {"hook_id": "hook_b", "duration_total_s": 30, "shot_count": 5},
    },
    {
        "name": "parse_beauty_serum",
        "fn": "parse_idea",
        "input": {"raw": EXTRA_IDEAS[0]["raw"]},
        "expect": {"category": "beauty", "channel": "Shopee", "price_unit": 390.0},
    },
    {
        "name": "parse_study_bio",
        "fn": "parse_idea",
        "input": {"raw": EXTRA_IDEAS[1]["raw"]},
        "expect": {"category": "study"},
    },
    {
        "name": "trend_angles_snacks_first",
        "fn": "suggest_trend_angles",
        "input": {"raw": DEMO_IDEA_RAW},
        "expect": {"first_id": "angle_before_after", "count": 5},
    },
]

# settings
settings_example = {
    "lang": "th",
    "default_style": "soft_sell_before_after",
    "default_duration_s": 30,
    "ai_assist": "off",
    "haptics": True,
    "keep_history": True,
    "auto_advance_film": True,
    "countdown_beep": True,
    "export_includes_json": True,
    "theme": "cinema_neon",
}

local_store = {
    "key": "reelforge:v1",
    "version": 1,
    "settings": settings_example,
    "blueprint_count": 3,
    "streak": STREAK,
    "last_blueprint_id": bp["blueprint_id"],
    "note": "local-first · IndexedDB blueprints + localStorage settings",
}

feature_checklist = {
    "must_have": [
        {"key": "idea_drop_blueprint", "label": "Idea Drop → Reel Blueprint", "done": True},
        {"key": "shot_list_film_mode", "label": "Shot List + Film Mode Timer", "done": True},
        {"key": "caption_pack", "label": "Caption Pack (Thai)", "done": True},
        {"key": "overlay_cover_forge", "label": "Overlay & Cover Forge", "done": True},
        {"key": "hook_ab_lab", "label": "Hook A/B Lab", "done": True},
    ],
    "nice_to_have": [
        {"key": "style_templates", "label": "Style Templates library", "done": True},
        {"key": "voice_to_idea", "label": "Voice → Idea (transcript paste)", "done": True},
        {"key": "trend_angles", "label": "Trend Angle Suggest", "done": True},
        {"key": "export_zip", "label": "Export Pack ZIP", "done": True},
        {"key": "streak_history", "label": "Streak / History", "done": True},
        {"key": "share_card", "label": "Share Blueprint Card", "done": True},
    ],
}

analytics_events = [
    {"name": "idea_submitted", "at": f"{TODAY}T08:00:00{TZ}", "props": {"source": "demo", "category": "snacks"}},
    {"name": "blueprint_built", "at": f"{TODAY}T08:00:02{TZ}", "props": {"style": DEMO_STYLE, "duration_s": 30, "shots": 5}},
    {"name": "film_mode_started", "at": f"{TODAY}T08:00:20{TZ}", "props": {"blueprint_id": bp["blueprint_id"]}},
    {"name": "hook_swapped", "at": f"{TODAY}T08:01:00{TZ}", "props": {"from": "hook_a", "to": "hook_b"}},
    {"name": "cover_exported", "at": f"{TODAY}T08:01:30{TZ}", "props": {"cover_id": "cover_a"}},
    {"name": "share_card_exported", "at": f"{TODAY}T08:02:00{TZ}", "props": {"variant": "blueprint_story"}},
    {"name": "demo_loaded", "at": f"{TODAY}T07:58:00{TZ}", "props": {"persona": "เจี๊ยบ"}},
]

# film mode strip for UI (serialize without nested huge shot dup)
def slim_film(fp):
    return {
        "total_s": fp["total_s"],
        "elapsed_s": fp["elapsed_s"],
        "remaining_s": fp["remaining_s"],
        "done": fp["done"],
        "shot_index": fp["shot_index"],
        "shot_n": fp["shot"]["n"],
        "shot_id": fp["shot"]["shot_id"],
        "shot_elapsed_s": fp["shot_elapsed_s"],
        "shot_remaining_s": fp["shot_remaining_s"],
        "shot_progress": fp["shot_progress"],
        "overall_progress": fp["overall_progress"],
        "prompt_th": fp["shot"]["prompt_th"],
        "overlay_th": fp["shot"]["overlay_th"],
    }

examples = {
    "meta": {
        "app": "ReelForge",
        "pack_date": TODAY,
        "day_in_queue": "10/10",
        "channel": "AI วันละแอป",
        "persona_note": PERSONA["note_th"],
        "timezone": "Asia/Bangkok",
        "today": TODAY,
        "hook_line_th": "ไอเดียในหัวแต่ไม่รู้จะเปิดคลิปยังไง? โยนเข้าแอปนี้ 10 วิ… ได้ชุดถ่ายพร้อมจับเวลาเลย 🎬",
        "colors": COLORS,
    },
    "persona": PERSONA,
    "demo_input": {
        "raw_idea": DEMO_IDEA_RAW,
        "style": DEMO_STYLE,
        "duration_target_s": DEMO_DURATION,
        "source": "demo_fixture",
    },
    "idea_parsed": idea,
    "style_library": style_library,
    "category_rules": cat_rules,
    "blueprint_example": bp,
    "caption_pack_example": caps,
    "overlays_example": ovs,
    "hook_lab_example": {
        "hooks": bp["hooks_ranked"],
        "winner_id": bp["hook"]["id"],
        "swap_example": {
            "selected": "hook_b",
            "after_hook_id": bp_swapped["hook"]["id"],
            "after_shot1_overlay": bp_swapped["shots"][0]["overlay_th"],
            "duration_still_s": bp_swapped["duration_total_s"],
        },
    },
    "film_mode_examples": {
        "at_0s": slim_film(film_t0),
        "at_3s": slim_film(film_t3),
        "at_10s": slim_film(film_t10),
        "at_29s": slim_film(film_t29),
        "at_30s_done": slim_film(film_done),
        "rewind_to_shot3": slim_film(film_rew),
    },
    "trend_angles_example": angles,
    "extra_ideas": extra_bps,
    "history_example": HISTORY_META,
    "streak_example": STREAK,
    "share_card_example": share_card,
    "export_pack_example": export_pack,
    "settings_example": settings_example,
    "local_store_example": local_store,
    "ui_copy_th": ui_copy_th,
    "reel_script_th": reel_script_th,
    "test_vectors": test_vectors,
    "feature_checklist_example": feature_checklist,
    "analytics_events_example": analytics_events,
    "expect_locked": EXPECT,
}

out = Path(__file__).resolve().parent.parent / "examples.json"

# --- enrichment (retention / reel depth) ---
examples["voice_transcript_example"] = {
  "source": "paste",
  "transcript_th": "เอ่อ วันนี้อยากลองขายคุกกี้เนยสดในไลน์ ส่งทั่วกรุงเทพ ชิ้นละสี่สิบห้าบาท ถ้าเซ็ตหกชิ้นสองร้อยสี่สิบ ช่วยทำคลิปรีลให้หน่อย",
  "normalized_idea": DEMO_IDEA_RAW,
  "note_th": "ผู้ใช้วางข้อความจาก voice note / speech-to-text แล้วแอป parse_idea ต่อ",
}
examples["before_after_demo"] = {
  "persona": "เจี๊ยบ",
  "before_th": "โพสต์ข้อความอย่างเดียวใน LINE / IG สตอรี่ — มียอดดู แต่คนทักน้อย",
  "after_th": "Reel 30 วิ ตาม Blueprint: ฮุค contrast → โชว์คุกกี้ → สั่ง LINE → CTA 「คุกกี้」",
  "metric_story_th": "ก่อน: ข้อความนิ่ง / หลัง: คลิปพร้อมถ่าย 5 ช็อต จับเวลา 30 วิ",
  "shot_durations": [3, 6, 8, 8, 5],
}
examples["shot_storyboard"] = [
  {"n": 1, "duration_s": 3, "visual_th": "เจี๊ยบมองกล้อง ยิ้ม พูดฮุค", "prop_th": "มือถือตั้งฝั่งตรงข้าม"},
  {"n": 2, "duration_s": 6, "visual_th": "โชว์หน้าจอโพสต์ข้อความเก่า (เบลอชื่อลูกค้า)", "prop_th": "มือถือเครื่องที่สอง"},
  {"n": 3, "duration_s": 8, "visual_th": "ยกกล่องคุกกี้เนยสด หมุนให้เห็นเนื้อ", "prop_th": "คุกกี้บนจานไม้"},
  {"n": 4, "duration_s": 8, "visual_th": "ชี้ไอคอน LINE / พิมพ์ตัวอย่างข้อความสั่ง", "prop_th": "หน้าจอแชทตัวอย่าง"},
  {"n": 5, "duration_s": 5, "visual_th": "ชี้คอมเมนต์ ยิ้ม พูดคำว่าคุกกี้", "prop_th": "—"},
]
examples["caption_variants_extra"] = {
  "alt_short_th": "คุกกี้เนยสดชิ้นละ 45฿ ส่ง LINE ทั้งกรุงเทพ — เปิดคลิป 30 วิ แล้วทักได้เลย คอมเมนต์ 「คุกกี้」",
  "alt_long_th": "เคยโพสต์ข้อความอย่างเดียวแล้วเงียบไหม?\nลองถ่ายคลิปสั้น 30 วิ โชว์ของจริง บอกทางสั่ง ปิดด้วยคำคอมเมนต์\nคุกกี้เนยสดอบใหม่ · ชิ้นละ 45 · เซ็ต 6 ชิ้น 240\nส่งทั่วกรุงเทพทาง LINE\n\nคอมเมนต์ 「คุกกี้」 รับเมนูวันนี้",
}
examples["ui_copy_th"].update({
  "film_countdown": "เตรียมตัว", "film_recording": "กำลังถ่าย…",
  "hook_curiosity": "ความอยากรู้", "hook_clarity": "ความชัด", "hook_emotion": "อารมณ์",
  "duration_15": "15 วิ", "duration_30": "30 วิ", "duration_45": "45 วิ", "duration_60": "60 วิ",
  "template_soft_sell_ba": "ก่อน/หลัง · Soft sell", "template_teach": "สอน 3 ขั้น",
  "template_story": "Storytime", "template_unbox": "Unboxing", "template_soft": "Soft sell",
  "onboarding_1": "วางไอเดียหรือเลือกเทมเพลต", "onboarding_2": "ได้ Blueprint + ฮุค + ช็อต",
  "onboarding_3": "เข้า Film Mode แล้วถ่ายตามจับเวลา",
  "safe_zone_hint": "ตัวอักษรอยู่โซนกลางบน ปลอดภัยจาก UI IG",
  "export_done": "แพ็กพร้อมดาวน์โหลด",
  "history_empty": "ยังไม่มี Blueprint — ลองข้อมูลตัวอย่างได้เลย",
})
examples["ai_runtime_examples"] = {
  "hooks_request": {
    "idea_normalized": idea["normalized"], "product": idea["product"],
    "category": idea["category"], "style": DEMO_STYLE,
    "existing_hooks": [h["text_th"] for h in bp["hooks_ranked"]],
  },
  "hooks_response_sample": {
    "hooks": [{"text_th": "หยุดโพสต์นิ่งๆ — เปิดกล้อง 30 วิ แล้วดูยอดทัก", "angle": "transformation"}],
    "note_th": "ทางเลือกเสริม — คะแนนยังต้องผ่าน rank_hooks ในเครื่อง",
  },
  "caption_request": {
    "blueprint_id": bp["blueprint_id"], "product": idea["product"],
    "hook_th": bp["hook"]["text_th"], "cta_keyword": "คุกกี้", "tone": "friendly_seller",
  },
}

out.write_text(json.dumps(examples, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("wrote", out, "bytes", out.stat().st_size)
print("shots", [s["duration_s"] for s in bp["shots"]], "hook", bp["hook"]["id"], "cta", bp["cta_keyword"])
print("covers", [c["title_th"] for c in ovs["covers"]])
print("test_vectors", len(test_vectors))
