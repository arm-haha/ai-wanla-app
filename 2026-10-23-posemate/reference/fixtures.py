"""Demo fixture — fictional: น้ำหวาน + เพื่อน ปิ่น, คาเฟ่ริมหน้าต่าง. All values are example data."""
NAME = "น้ำหวาน"; TODAY = "2026-10-23"
SCENE = dict(spot="cafe_window", light="window", people=1, clutter=1)
BEFORE = dict(tilt_deg=6, subject_xy=(0.5, 0.55), headroom=0.30, light="back", clutter=3, pose=40)
LIVE_KP = [[.56, .21], [.55, .31], [.48, .34], [.62, .33], [.46, .54], [.67, .47], [.55, .63], [.5, .95], [.61, .95]]
STIFF_KP = [[.5, .15], [.5, .25], [.42, .28], [.58, .28], [.38, .5], [.62, .5], [.5, .55], [.45, .95], [.55, .95]]
OUTFIT_BG = [("#F2E6D8", "#EFE3D3"), ("#B5523B", "#EFE3D3")]  # เสื้อครีม vs กำแพงครีม, เสื้อสีอิฐ
PHOTOS = [{"id": f"ph{i}", "kind": k, "hue": h} for i, (k, h) in enumerate([("person", 30), ("person", 35), ("person", 200), ("detail", 25), ("detail", 180),
          ("scene", 210), ("scene", 40), ("detail", 20), ("person", 190)], 1)]
AFTER = dict(tilt_deg=0, subject_xy=(0.66, 0.36), headroom=0.10, light="window", clutter=1)  # pose = live match
