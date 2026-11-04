# ตัวอย่างข้อมูลสมมติ (example data) ไม่ใช่ฉลากของแบรนด์จริง
GREENTEA = {"id":"greentea_sweet","name_th":"ชาเขียวขวด (หวาน) 420 ml","category":"tea","form":"drink","serving_size":210,"servings_per_pack":2,
  "per_serving":{"kcal":90,"sugar_g":20,"fat_g":0,"sodium_mg":40},"price_thb":20,
  "ingredients_th":"น้ำ, น้ำตาล, ใบชาเขียว 0.3%, วิตามินซี, กลิ่นธรรมชาติ, E330","additives":["E330"]}
GREENTEA0 = {"id":"greentea_zero","name_th":"ชาเขียวขวด (ไม่หวาน) 420 ml","category":"tea","form":"drink","serving_size":210,"servings_per_pack":2,
  "per_serving":{"kcal":0,"sugar_g":0,"fat_g":0,"sodium_mg":20},"price_thb":20,
  "ingredients_th":"น้ำ, ใบชาเขียว 0.5%, วิตามินซี","additives":[]}
GREENTEA_LITE = {"id":"greentea_lite","name_th":"ชาเขียวขวด (หวานน้อย) 420 ml","category":"tea","form":"drink","serving_size":210,"servings_per_pack":2,
  "per_serving":{"kcal":45,"sugar_g":10,"fat_g":0,"sodium_mg":30},"price_thb":20,
  "ingredients_th":"น้ำ, น้ำตาล, ใบชาเขียว, ซูคราโลส","additives":["E955"]}
CHIPS = {"id":"chips_seaweed","name_th":"มันฝรั่งทอดรสสาหร่าย 75 g","category":"snack","form":"solid","serving_size":25,"servings_per_pack":3,
  "per_serving":{"kcal":130,"sugar_g":1,"fat_g":8,"sodium_mg":190},"price_thb":35,
  "ingredients_th":"มันฝรั่ง, น้ำมันปาล์ม, ผงปรุงรสสาหร่าย (เกลือ, น้ำตาล, ผงชูรส E621, นมผง, ถั่วเหลือง)","additives":["E621"]}
NOODLE = {"id":"noodle_tomyum","name_th":"บะหมี่กึ่งสำเร็จรูปต้มยำ 60 g","category":"noodle","form":"solid","serving_size":60,"servings_per_pack":1,
  "per_serving":{"kcal":280,"sugar_g":4,"fat_g":12,"sodium_mg":1300},"price_thb":7,
  "ingredients_th":"แป้งสาลี, น้ำมันปาล์ม, เกลือ, กุ้งแห้ง, ผงชูรส E621","additives":["E621"]}
MILK = {"id":"milk_choc","name_th":"นมช็อกโกแลต UHT 180 ml","category":"milk","form":"drink","serving_size":180,"servings_per_pack":1,
  "per_serving":{"kcal":130,"sugar_g":17,"fat_g":4,"sodium_mg":110},"price_thb":14,
  "ingredients_th":"นมโคสด, น้ำตาล, ผงโกโก้, E471","additives":["E471"]}
CANDIDATES = [GREENTEA, GREENTEA0, GREENTEA_LITE, CHIPS, NOODLE, MILK]
USER = {"name":"มิว","allergies":["shrimp","milk"],"goal":"cut_sugar"}
DAY = [{"label":GREENTEA,"packs":1},{"label":CHIPS,"packs":1},{"label":MILK,"packs":1}]
WEEK = [{"date":"2026-10-%02d"%d,"sugar_tsp":t} for d,t in zip(range(22,29),[9,5,4,6,3,5,2])]
