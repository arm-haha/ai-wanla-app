"""Demo fixture: พี่ต้อม (Tom) practises an original ScaleRun in C. Fictional only — no copyrighted songs or lyrics."""
TODAY = "2026-12-02"

TOM = {
    "id": "u01", "name_th": "พี่ต้อม", "name_en": "Tom", "age": 27, "city_th": "กรุงเทพฯ",
    "goal_th": "อยากฮัมสเกลรันบันไดเสียง C แล้วรู้คะแนนเสียงกับจังหวะ และแข่งการ์ดกับเพื่อน",
}
NINA = {
    "id": "u02", "name_th": "น้องนีน่า", "name_en": "Nina", "age": 26, "city_th": "เชียงใหม่",
    "goal_th": "แข่งการ์ดดูเอทกับพี่ต้อมจากคะแนนฝึก",
}
BEE = {
    "id": "u03", "name_th": "พี่บี", "name_en": "Bee", "age": 33, "city_th": "ขอนแก่น",
    "goal_th": "วอร์มอัพแล้วลากสระอา",
}

TOM_TAKE = {
    "id": "t01", "exercise": "scale_run_c", "mean_cents_off": 36, "mean_ms_off": 52,
    "confidence": 0.95, "notes": ["C","D","E","F","G","A","B","C"],
}
NINA_TAKE = {
    "id": "t02", "exercise": "scale_run_c", "mean_cents_off": 50, "mean_ms_off": 64,
    "confidence": 0.92, "notes": ["C","D","E","F","G","A","B","C"],
}
# nina: pitch 100-25=75, timing 100-32=68, combined 0.6*75+0.4*68=45+27.2=72.2→72
BEE_TAKE = {
    "id": "t03", "exercise": "vowel_hold", "mean_cents_off": 20, "mean_ms_off": 20,
    "confidence": 0.90, "notes": ["A","A","A"],
}
LOWCONF_TAKE = {
    "id": "t04", "exercise": "scale_run_c", "mean_cents_off": 36, "mean_ms_off": 52,
    "confidence": 0.41, "notes": ["C"],
}

PEOPLE = [TOM, NINA, BEE]
