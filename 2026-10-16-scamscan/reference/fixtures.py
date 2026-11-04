"""Demo fixtures — all people, senders, domains and messages are FICTIONAL examples for the Reel demo."""
TODAY = "2026-10-16"
PERSONA = {"name_th": "ป้าแดง", "age": 62, "helper_th": "มิ้นท์", "helper_role_th": "ลูกสาว"}
# ป้าแดง's inbox this morning (demo)
INBOX = [
    {"id": "m1", "channel": "sms", "sender": "KBank-TH",
     "text": "แจ้งเตือน: บัญชี K PLUS ของท่านถูกระงับ กรุณายืนยันตัวตนภายใน 24 ชม. ที่ https://kbank-verify-th.top/login แล้วกรอก OTP"},
    {"id": "m2", "channel": "sms", "sender": "ThaiPost",
     "text": "ไปรษณีย์: พัสดุของคุณค้างส่งเนื่องจากที่อยู่ไม่ครบ ชำระค่าส่งเพิ่ม 18 บาท ที่ thaipost-delivery.cc/pay ด่วน"},
    {"id": "m3", "channel": "line", "sender": "เพื่อนใหม่ในไลน์",
     "text": "ยินดีด้วยค่ะ คุณได้รับเงินคืนภาษี 4,280 บาท กดรับที่ bit.ly/rd-kuen แล้วแอดไลน์ @refund-th เพื่อยืนยัน"},
    {"id": "m4", "channel": "line", "sender": "มิ้นท์",
     "text": "แม่ เย็นนี้มิ้นท์กลับไปกินข้าวบ้านนะ ซื้อขนมครกไปฝาก"},
]
LINK_CHECKS = ["https://kbank-verify-th.top/login", "https://www.kasikornbank.com", "http://192.168.10.5/scb", "https://xn--krngthai-ke9a.com/otp"]
CALL_TICKED = ["cs_authority", "cs_your_case", "cs_secret", "cs_transfer_check"]
QUIZ_SEED = 20261016
QUIZ_DECK = [
    {"id": "q01", "truth": "scam", "channel": "sms", "sender": "PEA", "text": "การไฟฟ้า: ค้างชำระค่าไฟ จะถูกตัดไฟภายในวันนี้ ชำระที่ pea-bill.xyz"},
    {"id": "q02", "truth": "real", "channel": "sms", "sender": "SCB", "text": "SCB: เงินเข้าบัญชี x1234 จำนวน 1,500.00 บ. คงเหลือ 8,240.15 บ."},
    {"id": "q03", "truth": "scam", "channel": "line", "sender": "งานออนไลน์", "text": "รับสมัครงานกดไลก์ รายได้วันละ 1,500 บาท แอดไลน์ @job-easy ด่วน รับจำนวนจำกัด"},
    {"id": "q04", "truth": "real", "channel": "line", "sender": "หลานต้น", "text": "ยาย พรุ่งนี้ต้นไปรับไปหาหมอ 9 โมงนะ"},
    {"id": "q05", "truth": "scam", "channel": "sms", "sender": "Krungsri", "text": "กรุงศรี: มีการเข้าสู่ระบบผิดปกติ ยืนยันตัวตนทันที krungsri-secure.icu"},
    {"id": "q06", "truth": "scam", "channel": "messenger", "sender": "ร้านกระเป๋าแบรนด์", "text": "ลดล้างสต็อก 90% โอนมัดจำก่อน 500 บาท ของหมดไว"},
    {"id": "q07", "truth": "real", "channel": "sms", "sender": "7-Eleven", "text": "สมาชิกALL: แต้มของคุณจะหมดอายุสิ้นเดือนนี้ ตรวจได้ในแอป ALL member"},
    {"id": "q08", "truth": "scam", "channel": "line", "sender": "เจ้าหน้าที่ DSI", "text": "บัญชีของท่านพัวพันคดีฟอกเงิน ติดต่อกลับด่วน ห้ามบอกผู้อื่น ติดตั้งแอปตรวจสอบ dsi-check.apk"},
    {"id": "q09", "truth": "real", "channel": "line", "sender": "กลุ่มบ้าน", "text": "วันอาทิตย์ทำบุญบ้านนะ 7 โมงเช้า ใครว่างมาช่วยจัดของหน่อย"},
    {"id": "q10", "truth": "scam", "channel": "sms", "sender": "Lucky", "text": "ยินดีด้วย! คุณถูกรางวัล iPhone ชำระค่าธรรมเนียมจัดส่ง 99 บาท tinyurl.com/get-ip"},
]
QUIZ_ANSWERS = ["scam", "real", "scam", "real", "real"]  # demo user's taps for the seeded 5-card round
QUIZ_DAYS = ["2026-10-12", "2026-10-13", "2026-10-14", "2026-10-15", "2026-10-16"]
HISTORY = [  # earlier checks this month (pre-computed shape, fictional)
    {"on": "2026-10-03", "score": 85, "level": "scam", "top_rule": "credential", "brands": ["kbank"], "preview_th": "บัญชีถูกระงับ ยืนยันตัวตน…"},
    {"on": "2026-10-05", "score": 10, "level": "low", "top_rule": None, "brands": [], "preview_th": "แม่ ส่งรูปหลานให้ดู"},
    {"on": "2026-10-08", "score": 70, "level": "risky", "top_rule": "money", "brands": ["thaipost"], "preview_th": "พัสดุค้างส่ง ชำระค่าส่ง…"},
    {"on": "2026-10-11", "score": 90, "level": "scam", "top_rule": "credential", "brands": ["scb"], "preview_th": "SCB แจ้งเปลี่ยนเบอร์ กรอก OTP…"},
]
