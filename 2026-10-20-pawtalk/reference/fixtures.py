"""Demo fixture: บ้านแพรว (สมมติ) — แมวส้ม 'ส้มฉุน' + หมาชิบะ 'ข้าวปั้น'. Today 2026-10-20 (Tue)."""
TODAY = "2026-10-20"
OWNER = "แพรว"
PETS = [
    {"id": "cat1", "name": "ส้มฉุน", "species": "cat", "breed_th": "แมวส้มไทย", "sex": "male", "age_years": 3,
     "weight_kg": 4.5, "neutered": True, "persona": "boss", "meal_times": ["07:30", "19:00"]},
    {"id": "dog1", "name": "ข้าวปั้น", "species": "dog", "breed_th": "ชิบะอินุ", "sex": "female", "age_years": 2,
     "weight_kg": 9.0, "neutered": True, "size": "medium", "persona": "sweet", "meal_times": ["08:00", "18:00"]},
]
FOOD = {"cat1": {"kcal_per_100g": 380, "meals": 2}, "dog1": {"kcal_per_100g": 350, "meals": 2}}
# Reel scene 1: 07:05, ส้มฉุน staring at bowl, loud meow, tail flick (breakfast at 07:30 → meal bonus)
SNAPS = {
    "cat1": {"at": "07:05", "cues": ["staring_at_bowl", "meow_loud", "tail_flick"]},
    "dog1": {"at": "07:05", "cues": ["tail_wag_loose", "play_bow", "bringing_toy"]},
}
# second scene for vibe contrast: ส้มฉุน after breakfast
CAT_AFTER = {"at": "08:10", "cues": ["slow_blink", "loaf", "purr"]}
CARE = [
    {"id": "t1", "pet_id": "cat1", "kind": "deworm", "label_th": "ถ่ายพยาธิ", "last_done": "2026-07-15", "interval_days": 90},
    {"id": "t2", "pet_id": "cat1", "kind": "flea", "label_th": "หยดเห็บหมัด", "last_done": "2026-09-22", "interval_days": 30},
    {"id": "t3", "pet_id": "cat1", "kind": "vaccine", "label_th": "วัคซีนรวมประจำปี", "last_done": "2025-11-02", "interval_days": 365},
    {"id": "t4", "pet_id": "dog1", "kind": "nail", "label_th": "ตัดเล็บ", "last_done": "2026-10-10", "interval_days": 14},
    {"id": "t5", "pet_id": "dog1", "kind": "bath", "label_th": "อาบน้ำ", "last_done": "2026-10-04", "interval_days": 14},
    {"id": "t6", "pet_id": "dog1", "kind": "heartworm", "label_th": "ยาป้องกันพยาธิหนอนหัวใจ", "last_done": "2026-09-21", "interval_days": 30},
]
HEALTH = {"cat1": ["hairball", "vomit_once"], "dog1": ["scratching_more"]}
HEALTH_RED = {"cat1": ["straining_no_urine", "hairball"]}   # shown in the 'what if' safety beat
LOG = (
    [{"on": d, "kind": "snap", "pet_id": "cat1", "mood": m} for d, m in [
        ("2026-10-01", "hungry"), ("2026-10-03", "annoyed"), ("2026-10-07", "annoyed"), ("2026-10-08", "chill"),
        ("2026-10-10", "hungry"), ("2026-10-12", "chill"), ("2026-10-14", "annoyed"), ("2026-10-15", "hungry"),
        ("2026-10-16", "happy"), ("2026-10-17", "hungry"), ("2026-10-18", "needy"), ("2026-10-19", "hungry")]]
    + [{"on": d, "kind": "snap", "pet_id": "dog1", "mood": m} for d, m in [
        ("2026-10-17", "playful"), ("2026-10-18", "happy"), ("2026-10-19", "playful")]]
    + [{"on": "2026-10-04", "kind": "care_done", "pet_id": "dog1"}, {"on": "2026-10-10", "kind": "care_done", "pet_id": "dog1"},
       {"on": "2026-10-19", "kind": "health_check", "pet_id": "cat1"}]
)
