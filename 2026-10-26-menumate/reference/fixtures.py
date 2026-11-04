"""Demo fixture: เจน + เพื่อน 2 คน ร้านราเมงโอซาก้า. Example data, not a real shop.
Rate is an EXAMPLE rate (0.23 THB/JPY); the app must let the user set today's rate."""
RATE = 0.23
PREFS = {"allergies": ["shrimp"], "diets": [], "spice_tolerance": 1}
MENU = [
 {"id":"m1","original_name":"豚骨ラーメン","romanized":"tonkotsu rāmen","thai_name":"ราเมงน้ำซุปกระดูกหมู","thai_desc":"น้ำซุปข้นขาว หมูชาชู ไข่ต้มยางมะตูม","price":980,"category":"main","spice_level":0,"ingredients":["pork","egg","wheat"],"allergens":["egg","wheat"],"must_try":95,"emoji":"🍜","confidence":0.97},
 {"id":"m2","original_name":"辛味噌ラーメン","romanized":"kara miso rāmen","thai_name":"ราเมงมิโสะเผ็ด","thai_desc":"มิโสะพริก เผ็ดกลาง ใส่หมูสับ","price":1080,"category":"main","spice_level":2,"ingredients":["pork","soy","wheat"],"allergens":["soy","wheat"],"must_try":88,"emoji":"🌶️","confidence":0.95},
 {"id":"m3","original_name":"海老塩ラーメン","romanized":"ebi shio rāmen","thai_name":"ราเมงซุปเกลือกุ้ง","thai_desc":"ซุปใส กลิ่นกุ้งหวาน","price":1150,"category":"main","spice_level":0,"ingredients":["shrimp","wheat"],"allergens":["shrimp","wheat"],"must_try":90,"emoji":"🦐","confidence":0.93},
 {"id":"m4","original_name":"醤油ラーメン","romanized":"shōyu rāmen","thai_name":"ราเมงโชยุ","thai_desc":"ซุปซีอิ๊วใส คลาสสิก","price":880,"category":"main","spice_level":0,"ingredients":["chicken","soy","wheat"],"allergens":["soy","wheat"],"must_try":80,"emoji":"🍥","confidence":0.96},
 {"id":"s1","original_name":"餃子（6個）","romanized":"gyōza","thai_name":"เกี๊ยวซ่าทอด 6 ชิ้น","thai_desc":"ไส้หมูกะหล่ำ","price":450,"category":"side","spice_level":0,"ingredients":["pork","wheat"],"allergens":["wheat"],"must_try":85,"emoji":"🥟","confidence":0.98},
 {"id":"s2","original_name":"唐揚げ","romanized":"karaage","thai_name":"ไก่ทอดคาราอาเกะ","thai_desc":"ไก่หมักโชยุทอดกรอบ","price":520,"category":"side","spice_level":0,"ingredients":["chicken","soy","wheat"],"allergens":["soy","wheat"],"must_try":70,"emoji":"🍗","confidence":0.97},
 {"id":"s3","original_name":"替玉","romanized":"kaedama","thai_name":"เส้นเติม","thai_desc":"สั่งเส้นเพิ่มใส่ซุปเดิม","price":150,"category":"side","spice_level":0,"ingredients":["wheat"],"allergens":["wheat"],"must_try":60,"emoji":"➕","confidence":0.55},
 {"id":"d1","original_name":"ウーロン茶","romanized":"ūron cha","thai_name":"ชาอูหลง","thai_desc":"ชาเย็นไม่หวาน","price":250,"category":"drink","spice_level":0,"ingredients":[],"allergens":[],"must_try":40,"emoji":"🍵","confidence":0.99},
]
BUDGET = 3000
PARTY = 2
RECEIPT = [
 {"name":"豚骨ラーメン","amount":980},{"name":"醤油ラーメン","amount":880},
 {"name":"餃子（6個）","amount":450},{"name":"唐揚げ","amount":520},
 {"name":"ライス","amount":200},
]
MEALS = [
 {"city":"Osaka","total_local":2830,"items_tried":4,"avoided":1},
 {"city":"Kyoto","total_local":4200,"items_tried":5,"avoided":0},
 {"city":"Osaka","total_local":1900,"items_tried":3,"avoided":2},
]
