"""Demo fixture: แม่แพร + น้องใบเตย (5 ขวบ) + พี่ภูผา (8 ขวบ). Fictional example data only."""
TODAY = "2026-11-05"
PARENT = {"id": "u01", "name_th": "แพร", "role": "mom"}
KIDS = [
 {"id": "k01", "name_th": "น้องใบเตย", "birth": "2021-06-15", "avatar": "dino"},
 {"id": "k02", "name_th": "พี่ภูผา", "birth": "2018-03-02", "avatar": "robot"},
]
DRAWINGS = [
 {"id": "d01", "kid_id": "k01", "title_th": "แมวส้มของหนู", "subject": "animal", "drawn_on": "2025-07-10", "px_w": 2480, "px_h": 1860, "colors": 3, "strokes": 60,
  "parts": {"head": 1, "body": 1, "arms": 0, "legs": 4, "tail": 1, "wings": 0}, "scan": {"shadow": 0.5, "blur": 0.2, "tilt": 0.3, "crop_cut": 0.0}},
 {"id": "d02", "kid_id": "k01", "title_th": "ซานต้าใจดี", "subject": "person", "drawn_on": "2025-12-25", "px_w": 1860, "px_h": 2480, "colors": 4, "strokes": 110,
  "parts": {"head": 1, "body": 1, "arms": 2, "legs": 2, "tail": 0, "wings": 0}, "scan": {"shadow": 0.2, "blur": 0.1, "tilt": 0.1, "crop_cut": 0.0}},
 {"id": "d03", "kid_id": "k01", "title_th": "ช้างเล่นสงกรานต์", "subject": "animal", "drawn_on": "2026-04-13", "px_w": 2480, "px_h": 1860, "colors": 5, "strokes": 150,
  "parts": {"head": 1, "body": 1, "arms": 0, "legs": 4, "tail": 1, "wings": 0}, "scan": {"shadow": 0.3, "blur": 0.1, "tilt": 0.0, "crop_cut": 0.1}},
 {"id": "d04", "kid_id": "k02", "title_th": "หุ่นยนต์ไฟฟ้า", "subject": "robot", "drawn_on": "2026-08-20", "px_w": 2480, "px_h": 3300, "colors": 6, "strokes": 260,
  "parts": {"head": 1, "body": 1, "arms": 2, "legs": 2, "tail": 0, "wings": 0}, "scan": {"shadow": 0.1, "blur": 0.0, "tilt": 0.0, "crop_cut": 0.0}},
 {"id": "d05", "kid_id": "k01", "title_th": "ปลาวาฬบินได้", "subject": "animal", "drawn_on": "2026-10-01", "px_w": 2480, "px_h": 1860, "colors": 4, "strokes": 120,
  "parts": {"head": 1, "body": 1, "arms": 0, "legs": 0, "tail": 1, "wings": 0}, "scan": {"shadow": 0.9, "blur": 0.7, "tilt": 0.2, "crop_cut": 0.4}},
 {"id": "d06", "kid_id": "k01", "title_th": "ไดโนชมพูใส่มงกุฎ", "subject": "animal", "drawn_on": "2026-11-04", "px_w": 2480, "px_h": 3300, "colors": 6, "strokes": 210,
  "parts": {"head": 1, "body": 1, "arms": 2, "legs": 2, "tail": 1, "wings": 0}, "scan": {"shadow": 0.4, "blur": 0.1, "tilt": 0.2, "crop_cut": 0.0}},
]
PROMPT_HISTORY = [("2026-11-01", "ช้างกินไอศกรีม"), ("2026-11-03", "มังกรตัวจิ๋ว"), ("2026-09-01", "ไดโนเสาร์ใส่หมวก")]
