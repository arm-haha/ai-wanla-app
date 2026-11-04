"""Demo fixture "ปุ๊ก" (fictional) — dorm fridge, Wed 2026-10-14."""
TODAY = "2026-10-14"
PERSONA = {"name": "ปุ๊ก", "age": 21, "context": "นักศึกษาอยู่หอ มีตู้เย็นเล็ก เตาไฟฟ้า 1 หัว + ไมโครเวฟ งบกินวันละ ~150"}
DETECTIONS = [  # simulated vision output for demo photo assets/demo-fridge.jpg
    {"key": "egg", "qty": 4, "added_on": "2026-10-08", "confidence": 0.97, "bbox": [0.08, 0.62, 0.30, 0.78]},
    {"key": "pork_minced", "qty": 200, "added_on": "2026-10-12", "confidence": 0.91, "bbox": [0.36, 0.40, 0.62, 0.55]},
    {"key": "holy_basil", "qty": 1, "added_on": "2026-10-11", "confidence": 0.88, "bbox": [0.66, 0.40, 0.92, 0.56]},
    {"key": "chili", "qty": 1, "added_on": "2026-10-10", "confidence": 0.84, "bbox": [0.70, 0.80, 0.86, 0.90]},
    {"key": "garlic", "qty": 1, "added_on": "2026-10-01", "confidence": 0.93, "bbox": [0.52, 0.80, 0.66, 0.92]},
    {"key": "tomato", "qty": 2, "added_on": "2026-10-09", "confidence": 0.95, "bbox": [0.10, 0.80, 0.30, 0.94]},
    {"key": "spring_onion", "qty": 3, "added_on": "2026-10-10", "confidence": 0.79, "bbox": [0.30, 0.60, 0.70, 0.66]},
    {"key": "cooked_rice", "qty": 1, "added_on": "2026-10-13", "confidence": 0.86, "bbox": [0.08, 0.20, 0.34, 0.36]},
    {"key": "egg_tofu", "qty": 1, "added_on": "2026-10-07", "confidence": 0.90, "bbox": [0.40, 0.20, 0.70, 0.30]},
    {"key": "milk", "qty": 1, "added_on": "2026-10-10", "confidence": 0.98, "bbox": [0.76, 0.06, 0.94, 0.36]},
    {"key": "sausage", "qty": 3, "added_on": "2026-10-05", "confidence": 0.92, "bbox": [0.38, 0.62, 0.62, 0.74]},
    {"key": "carrot", "qty": 1, "added_on": "2026-10-03", "confidence": 0.81, "bbox": [0.72, 0.62, 0.94, 0.76]},
    {"key": "lime", "qty": 1, "added_on": "2026-10-09", "confidence": 0.41, "bbox": [0.88, 0.82, 0.96, 0.90]},
]
DICE_SEED = 20261014
# earlier cook log this month (fictional) — today's kaprao is appended by build.py
HISTORY = [
    {"date": "2026-10-03", "recipe_id": "khai_jiao_moo_sap", "rescued": ["pork_minced"], "rescued_value_thb": 40},
    {"date": "2026-10-04", "recipe_id": "khao_pad_sausage", "rescued": ["cooked_rice"], "rescued_value_thb": 10},
    {"date": "2026-10-05", "recipe_id": "khai_tun_nom", "rescued": ["milk"], "rescued_value_thb": 25},
    {"date": "2026-10-08", "recipe_id": "khai_pad_makheua_thet", "rescued": ["tomato", "spring_onion"], "rescued_value_thb": 20},
    {"date": "2026-10-09", "recipe_id": "tom_jued_tofu_moo", "rescued": ["pork_minced", "spring_onion"], "rescued_value_thb": 50},
    {"date": "2026-10-10", "recipe_id": "khao_tom_moo", "rescued": ["cooked_rice"], "rescued_value_thb": 10},
    {"date": "2026-10-12", "recipe_id": "khai_jiao_moo_sap", "rescued": [], "rescued_value_thb": 0},
    {"date": "2026-10-13", "recipe_id": "khao_pad_sausage", "rescued": ["cooked_rice"], "rescued_value_thb": 10},
]
