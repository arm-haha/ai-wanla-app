from datetime import date
TODAY = date(2026, 10, 27)
OWNED = ["screwdriver"]
FAUCET = {"issue_id":"faucet_drip","title_th":"ก๊อกน้ำซิงก์หยด","symptom_th":"น้ำหยดตลอดแม้ปิดสุด ประมาณ 1 หยด/วินาที",
          "category":"plumbing","confidence":0.88,"difficulty":2,"minutes":20,"hazard_tags":[],
          "causes":[{"cause_th":"ยางรองวาล์ว (washer) เสื่อม","p":0.71},{"cause_th":"เซรามิกวาล์วสึก","p":0.22},{"cause_th":"น็อตหลวม","p":0.07}]}
FAUCET_PARTS = [{"id":"washer","name_th":"ยางรองก๊อก 1/2\"","search_kw":"ยางรองก๊อกน้ำ 1/2 นิ้ว","price_thb":25,"qty":1}]
FAUCET_TOOLS = [{"id":"screwdriver","name_th":"ไขควง","price_thb":60},{"id":"adj_wrench","name_th":"ประแจเลื่อน 8\"","price_thb":120}]
FAUCET_STEPS = [{"id":"s1","text_th":"ปิดวาล์วน้ำใต้ซิงก์ แล้วเปิดก๊อกปล่อยน้ำค้าง","minutes":2},
                {"id":"s2","text_th":"แกะฝาครอบ ไขสกรูด้ามจับ","minutes":3},
                {"id":"s3","text_th":"ใช้ประแจคลายตัววาล์ว (ทวนเข็ม)","minutes":4},
                {"id":"s4","text_th":"เปลี่ยนยางรองใหม่ ขนาดเดิม","minutes":5},
                {"id":"s5","text_th":"ประกอบกลับ เปิดวาล์ว เช็กว่าไม่หยด 1 นาที","minutes":6}]
TOILET = {"issue_id":"toilet_running","title_th":"ชักโครกน้ำไหลไม่หยุด","symptom_th":"มีเสียงน้ำไหลลงโถตลอด","category":"plumbing",
          "confidence":0.81,"difficulty":2,"minutes":15,"hazard_tags":[],"causes":[{"cause_th":"ลูกยางปิดน้ำ (flapper) เสื่อม","p":0.8},{"cause_th":"ลูกลอยตั้งสูง","p":0.2}]}
TOILET_PARTS = [{"id":"flapper","name_th":"ลูกยางชักโครก","search_kw":"ลูกยางชักโครก flapper","price_thb":120,"qty":1}]
OUTLET = {"issue_id":"outlet_burn","title_th":"ปลั๊กไฟมีรอยไหม้","symptom_th":"เต้ารับดำ มีกลิ่นไหม้","category":"electrical",
          "confidence":0.9,"difficulty":4,"minutes":30,"hazard_tags":["burn_mark"],"causes":[{"cause_th":"ขั้วหลวม/โหลดเกิน","p":0.85}]}
AIRCON = {"issue_id":"aircon_drip","title_th":"แอร์น้ำหยด","symptom_th":"น้ำหยดจากใต้ตัวแอร์ในห้อง","category":"appliance",
          "confidence":0.55,"difficulty":2,"minutes":25,"hazard_tags":["ladder_over_2m"],"causes":[{"cause_th":"ฟิลเตอร์ตัน","p":0.5},{"cause_th":"ท่อน้ำทิ้งตัน","p":0.5}]}
CARE = [{"id":"ac_filter","title_th":"ล้างฟิลเตอร์แอร์","every_days":30,"last_done":"2026-09-10"},
        {"id":"ac_service","title_th":"ล้างแอร์ใหญ่ (ช่าง)","every_days":180,"last_done":"2026-06-01"},
        {"id":"drain","title_th":"เทน้ำร้อน+เบกกิ้งโซดาท่อซิงก์","every_days":30,"last_done":"2026-10-20"},
        {"id":"smoke","title_th":"กดเทสต์เครื่องตรวจควัน","every_days":90,"last_done":"2026-08-15"}]
