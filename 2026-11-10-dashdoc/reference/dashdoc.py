"""DashDoc deterministic logic (no AI calls). Costs, km limits, intervals are app-chosen example values — not mechanic advice or real quotes."""
import datetime as _dt
import urllib.parse as _up

LEVELS = {"red": "แดง · จอดเดี๋ยวนี้", "yellow": "เหลือง · ขับระวังไปอู่", "green": "เขียว/ฟ้า · ข้อมูลเฉย ๆ"}
LEVEL_RANK = {"green": 1, "yellow": 2, "red": 3}
COLORS = ["red", "yellow", "green", "blue"]
SYMPTOMS = {
    "none": "ไม่มีอาการอื่น", "smoke": "มีควัน", "burning_smell": "กลิ่นไหม้", "overheating": "เข็มความร้อนพุ่ง",
    "knocking": "เสียงเคาะ/กระแทกในเครื่อง", "brake_soft": "เบรกนิ่ม/ลึกผิดปกติ", "steering_heavy": "พวงมาลัยหนักผิดปกติ",
    "shaking": "รถสั่นมาก", "power_loss": "รถไม่มีแรง/ดับ", "fluid_leak": "มีของเหลวรั่วใต้รถ",
}
SEVERE_SYMPTOMS = ["smoke", "burning_smell", "overheating", "knocking", "brake_soft", "power_loss", "fluid_leak"]
CAR_CLASSES = {"eco": 1.0, "sedan": 1.15, "suv_pickup": 1.35}
REGION_MULT = {"bkk": 1.0, "province": 0.85, "tourist": 1.2}
FUELS = ["petrol", "diesel", "hybrid"]
FLASH_ESCALATE = ["check_engine"]
MIN_CONF = 0.6

# Warning-light library: urgency is the *steady* state. drive_km / drive_days / max_speed are example guardrails.
LIGHTS = {
    "check_engine": {"id": "w01", "name_th": "ไฟเช็กเครื่องยนต์", "name_en": "Check engine", "color": "yellow", "drive_km": 100, "drive_days": 3, "max_speed": 90,
        "meaning_th": "ระบบควบคุมเครื่องยนต์/ไอเสียตรวจเจอความผิดปกติ", "checks": ["gas_cap", "oil_level"], "fixes": ["f18", "f01", "f02", "f03"]},
    "oil_pressure": {"id": "w02", "name_th": "ไฟแรงดันน้ำมันเครื่อง", "name_en": "Oil pressure", "color": "red", "drive_km": 0, "drive_days": 0, "max_speed": 0,
        "meaning_th": "น้ำมันเครื่องน้อยหรือแรงดันตก เครื่องอาจพังภายในไม่กี่นาที", "checks": ["oil_level"], "fixes": ["f09", "f10"]},
    "coolant_temp": {"id": "w03", "name_th": "ไฟความร้อนเครื่องยนต์สูง", "name_en": "Engine overheating", "color": "red", "drive_km": 0, "drive_days": 0, "max_speed": 0,
        "meaning_th": "น้ำหล่อเย็นน้อยหรือระบบระบายความร้อนมีปัญหา", "checks": ["coolant_level"], "fixes": ["f11", "f12"]},
    "battery_charge": {"id": "w04", "name_th": "ไฟแบตเตอรี่/ระบบชาร์จ", "name_en": "Battery / charging", "color": "red", "drive_km": 0, "drive_days": 0, "max_speed": 0,
        "meaning_th": "ไดชาร์จหรือแบตมีปัญหา รถอาจดับกลางทางเมื่อแบตหมด", "checks": ["battery_terminals"], "fixes": ["f07", "f08"]},
    "brake_system": {"id": "w05", "name_th": "ไฟระบบเบรก", "name_en": "Brake system", "color": "red", "drive_km": 0, "drive_days": 0, "max_speed": 0,
        "meaning_th": "น้ำมันเบรกต่ำ หรือระบบเบรกผิดปกติ (เช็กก่อนว่าปลดเบรกมือแล้ว)", "checks": ["parking_brake", "brake_fluid"], "fixes": ["f13", "f14"]},
    "parking_brake": {"id": "w06", "name_th": "ไฟเบรกมือ", "name_en": "Parking brake", "color": "red", "drive_km": 0, "drive_days": 0, "max_speed": 0,
        "meaning_th": "เบรกมือยังดึงอยู่ ปลดแล้วไฟยังไม่ดับให้เช็กระบบเบรก", "checks": ["parking_brake"], "fixes": ["f13"]},
    "abs": {"id": "w07", "name_th": "ไฟ ABS", "name_en": "ABS", "color": "yellow", "drive_km": 150, "drive_days": 5, "max_speed": 80,
        "meaning_th": "เบรกธรรมดายังใช้ได้ แต่ ABS ช่วยกันล้อล็อกไม่ทำงาน", "checks": [], "fixes": ["f14", "f18"]},
    "airbag": {"id": "w08", "name_th": "ไฟถุงลมนิรภัย (SRS)", "name_en": "Airbag (SRS)", "color": "yellow", "drive_km": 100, "drive_days": 2, "max_speed": 80,
        "meaning_th": "ถุงลมอาจไม่ทำงานเมื่อเกิดอุบัติเหตุ ควรรีบตรวจ", "checks": [], "fixes": ["f18"]},
    "tpms": {"id": "w09", "name_th": "ไฟลมยางอ่อน (TPMS)", "name_en": "Low tire pressure", "color": "yellow", "drive_km": 50, "drive_days": 1, "max_speed": 80,
        "meaning_th": "ลมยางอย่างน้อย 1 เส้นต่ำกว่าที่กำหนด ยางอาจรั่วหรือลมตกตามอากาศ", "checks": ["tire_visual"], "fixes": ["f04", "f05", "f06"]},
    "low_fuel": {"id": "w10", "name_th": "ไฟน้ำมันใกล้หมด", "name_en": "Low fuel", "color": "yellow", "drive_km": 50, "drive_days": 1, "max_speed": 110,
        "meaning_th": "น้ำมันเหลือน้อย รีบเติมก่อนรถดับ (ดีเซลระวังอากาศเข้าระบบ)", "checks": [], "fixes": []},
    "power_steering": {"id": "w11", "name_th": "ไฟพวงมาลัยพาวเวอร์ (EPS)", "name_en": "Power steering", "color": "yellow", "drive_km": 30, "drive_days": 1, "max_speed": 60,
        "meaning_th": "พวงมาลัยอาจหนักขึ้นกะทันหัน ขับช้าและเว้นระยะห่างมาก ๆ", "checks": [], "fixes": ["f18"]},
    "dpf": {"id": "w12", "name_th": "ไฟกรองไอเสียดีเซล (DPF)", "name_en": "Diesel particulate filter", "color": "yellow", "drive_km": 80, "drive_days": 3, "max_speed": 90,
        "meaning_th": "ตัวกรองเขม่าเริ่มตัน ลองวิ่งทางตรงรอบสม่ำเสมอเพื่อเผาเขม่า", "checks": [], "fixes": ["f16", "f18"]},
    "esc": {"id": "w13", "name_th": "ไฟควบคุมการทรงตัว (ESC)", "name_en": "Stability control", "color": "yellow", "drive_km": 150, "drive_days": 5, "max_speed": 80,
        "meaning_th": "ไฟค้างแปลว่าระบบอาจปิดทำงานหรือมีเซนเซอร์เสีย (กะพริบตอนลื่น = ระบบกำลังทำงาน ปกติ)", "checks": [], "fixes": ["f14", "f18"]},
    "washer": {"id": "w14", "name_th": "ไฟน้ำฉีดกระจกต่ำ", "name_en": "Washer fluid low", "color": "green", "drive_km": None, "drive_days": 14, "max_speed": None,
        "meaning_th": "น้ำฉีดกระจกใกล้หมด เติมเมื่อสะดวก", "checks": [], "fixes": []},
    "service_due": {"id": "w15", "name_th": "ไฟถึงเวลาเช็กระยะ", "name_en": "Service due", "color": "green", "drive_km": None, "drive_days": 30, "max_speed": None,
        "meaning_th": "ถึงรอบเช็กระยะตามที่ตั้งไว้ ไม่ใช่อาการเสีย", "checks": [], "fixes": ["f09"]},
    "high_beam": {"id": "w16", "name_th": "ไฟสูงเปิดอยู่", "name_en": "High beam on", "color": "blue", "drive_km": None, "drive_days": None, "max_speed": None,
        "meaning_th": "เปิดไฟสูงอยู่ อย่าลืมหรี่เมื่อมีรถสวน", "checks": [], "fixes": []},
    "seat_belt": {"id": "w17", "name_th": "ไฟเตือนเข็มขัดนิรภัย", "name_en": "Seat belt", "color": "red", "drive_km": None, "drive_days": None, "max_speed": None,
        "meaning_th": "มีคนยังไม่คาดเข็มขัด คาดแล้วไฟดับเอง (ไม่ต้องจอดฉุกเฉิน)", "checks": [], "fixes": [], "minor": True},
}
LIGHT_BY_ID = {v["id"]: k for k, v in LIGHTS.items()}

FIXES = {
    "f01": {"name_th": "ฝาถังน้ำมันหลวม/เสื่อม", "min": 0, "max": 150, "ask_th": ["ลองปิดฝาถังให้แน่นแล้วขับ 1–2 วัน ไฟดับไหม"]},
    "f02": {"name_th": "เปลี่ยนเซนเซอร์ออกซิเจน (O2)", "min": 1500, "max": 4500, "ask_th": ["รหัสที่อ่านได้คืออะไร", "ขอดูอะไหล่เก่า"]},
    "f03": {"name_th": "เปลี่ยนหัวเทียน/คอยล์จุดระเบิด", "min": 1200, "max": 5500, "ask_th": ["ต้องเปลี่ยนทั้งชุดหรือเฉพาะสูบที่เสีย", "รับประกันกี่เดือน"]},
    "f04": {"name_th": "เติมลม/ปะยางรั่ว", "min": 50, "max": 400, "ask_th": ["เป็นแผลรั่วจากตะปูหรือที่ขอบยาง ปะได้ไหม"]},
    "f05": {"name_th": "เปลี่ยนยาง 1 เส้น", "min": 2000, "max": 4500, "ask_th": ["ยางเส้นอื่นสึกเท่าไร ต้องเปลี่ยนคู่ไหม", "ราคารวมถ่วงล้อและศูนย์ล้อหรือยัง"]},
    "f06": {"name_th": "เปลี่ยนเซนเซอร์ลมยาง (TPMS)", "min": 800, "max": 2500, "ask_th": ["ต้องรีเซ็ตระบบด้วยไหม"]},
    "f07": {"name_th": "เปลี่ยนแบตเตอรี่", "min": 1800, "max": 4500, "ask_th": ["ขนาด/ปีผลิตของแบตที่เปลี่ยน", "ขอดูผลวัดแบตและไดชาร์จก่อนเปลี่ยน"]},
    "f08": {"name_th": "ซ่อม/เปลี่ยนไดชาร์จ", "min": 4500, "max": 12000, "ask_th": ["ซ่อมได้ไหม หรือต้องเปลี่ยนเป็นของใหม่/บิ้ว", "ขอผลวัดแรงดันชาร์จ"]},
    "f09": {"name_th": "เปลี่ยนน้ำมันเครื่อง+กรอง", "min": 1000, "max": 2500, "ask_th": ["เบอร์น้ำมันเครื่องและยี่ห้อ", "ปริมาณที่ใส่กี่ลิตร"]},
    "f10": {"name_th": "เปลี่ยนเซนเซอร์/ปั๊มน้ำมันเครื่อง", "min": 600, "max": 9000, "ask_th": ["วัดแรงดันจริงแล้วหรือยัง ว่าเซนเซอร์เสียหรือปั๊มเสีย", "มีความเสียหายในเครื่องหรือไม่"]},
    "f11": {"name_th": "เติมน้ำหล่อเย็น/เปลี่ยนเทอร์โมสตัท", "min": 500, "max": 3500, "ask_th": ["รั่วจุดไหน ทดสอบแรงดันระบบหรือยัง"]},
    "f12": {"name_th": "เปลี่ยนหม้อน้ำ/ปั๊มน้ำ", "min": 3500, "max": 9000, "ask_th": ["เปลี่ยนสายพานไทม์มิ่งพร้อมกันไหม", "รับประกันงานกี่เดือน"]},
    "f13": {"name_th": "เปลี่ยนผ้าเบรก/จานเบรก", "min": 1500, "max": 4000, "ask_th": ["ผ้าเบรกเหลือกี่มิลลิเมตร", "จานต้องเจียหรือเปลี่ยน"]},
    "f14": {"name_th": "เซนเซอร์ ABS/เติม-เปลี่ยนน้ำมันเบรก", "min": 800, "max": 3500, "ask_th": ["เซนเซอร์ล้อไหน", "น้ำมันเบรกชนิด DOT อะไร"]},
    "f16": {"name_th": "ล้าง/เผา DPF", "min": 3000, "max": 9000, "ask_th": ["ลองรีเจนเนอเรทก่อนไหม", "ถ้าเปลี่ยนใหม่ราคาเท่าไร"]},
    "f18": {"name_th": "ต่อเครื่องอ่านรหัส (OBD) วิเคราะห์", "min": 300, "max": 800, "ask_th": ["ขอรหัส P0xxx ที่อ่านได้และใบสรุป", "ค่าตรวจหักออกจากค่าซ่อมได้ไหม"]},
}

# Aftercare / service intervals (app-chosen examples). km=None → date-only.
SERVICE_ITEMS = {
    "engine_oil": {"label_th": "น้ำมันเครื่อง", "km": 10000, "months": 6},
    "tire_rotate": {"label_th": "สลับยาง/ถ่วงล้อ", "km": 10000, "months": 6},
    "tire_replace": {"label_th": "เปลี่ยนยาง", "km": 40000, "months": 48},
    "battery": {"label_th": "แบตเตอรี่", "km": None, "months": 30},
    "brake_fluid": {"label_th": "น้ำมันเบรก", "km": 40000, "months": 24},
    "coolant": {"label_th": "น้ำหล่อเย็น", "km": 40000, "months": 24},
    "air_filter": {"label_th": "กรองอากาศ", "km": 20000, "months": 12},
    "act": {"label_th": "พ.ร.บ.", "km": None, "months": 12},
    "tax": {"label_th": "ภาษีรถประจำปี", "km": None, "months": 12},
    "insurance": {"label_th": "ประกันภัย", "km": None, "months": 12},
}
SOON_KM, DUE_KM = 1500, 500
SOON_DAYS, DUE_DAYS = 30, 14
FREE_SCANS_PER_DAY = 3
WATERMARK = "Made with DashDoc · estimate only, not a mechanic"
SAFETY_DISCLAIMER_TH = "DashDoc เป็นคำแนะนำเบื้องต้น ไม่ใช่ช่างและไม่ใช่การวินิจฉัยจริง ไฟสีแดง = จอดในที่ปลอดภัยทันที ถ้าไม่แน่ใจให้เรียกช่าง/ประกันภัย"
PRICE_DISCLAIMER_TH = "ราคาเป็นช่วงประมาณการ ไม่ใช่ราคาจริงของอู่ ขึ้นกับรุ่นรถ อะไหล่ และพื้นที่"

HOTLINES = [
    {"key": "police", "label_th": "ตำรวจ", "number": "191", "kind": "public", "note_th": "เช็กเบอร์จากแหล่งทางการก่อนใช้งานจริง"},
    {"key": "highway_police", "label_th": "ตำรวจทางหลวง", "number": "1193", "kind": "public", "note_th": "เช็กเบอร์จากแหล่งทางการก่อนใช้งานจริง"},
    {"key": "medical", "label_th": "การแพทย์ฉุกเฉิน", "number": "1669", "kind": "public", "note_th": "เช็กเบอร์จากแหล่งทางการก่อนใช้งานจริง"},
    {"key": "insurer", "label_th": "สายด่วนประกันภัยของคุณ", "number": None, "kind": "placeholder", "note_th": "ใส่เบอร์จากกรมธรรม์"},
    {"key": "tow", "label_th": "รถยกที่ไว้ใจ", "number": None, "kind": "placeholder", "note_th": "ใส่เบอร์ร้าน/ศูนย์ที่คุ้นเคย"},
    {"key": "garage", "label_th": "อู่ประจำ", "number": None, "kind": "placeholder", "note_th": "ใส่เบอร์อู่"},
]
GUIDES = {
    "flat_tire": {"title_th": "ยางแบน", "tools_th": ["แม่แรง", "ประแจถอดล้อ", "ยางอะไหล่", "ไฟฉาย"], "steps_th": [
        "เปิดไฟฉุกเฉิน จอดบนพื้นเรียบนอกถนน ดึงเบรกมือ", "วางป้ายสามเหลี่ยมห่างท้ายรถ ผู้โดยสารลงไปยืนในที่ปลอดภัย",
        "คลายน็อตล้อให้หลวมก่อนยกรถ", "ยกรถตามจุดแม่แรงในคู่มือ ถอดล้อ", "ใส่ล้ออะไหล่ ขันน็อตแบบไขว้ ลดแม่แรง ขันให้แน่น",
        "ขับช้า ไม่เกิน 80 กม./ชม. ไปร้านยางทันที (ยางอะไหล่ขนาดเล็กห้ามขับไกล)"]},
    "jump_start": {"title_th": "แบตหมด จั๊มสตาร์ท", "tools_th": ["สายพ่วงแบต", "รถคันช่วย"], "steps_th": [
        "จอดสองคันใกล้กันแต่ไม่ชนกัน ดับเครื่องทั้งสองคัน", "แดงต่อ + แบตเสีย → + แบตดี", "ดำต่อ − แบตดี → โลหะเปลือยบนตัวถังรถคันเสีย (ห่างแบต)",
        "สตาร์ทคันช่วย รอ 3–5 นาที แล้วสตาร์ทคันเสีย", "ถอดสายย้อนลำดับ ขับต่อ 30 นาทีให้ชาร์จ แล้วให้ร้านวัดแบต/ไดชาร์จ"]},
    "overheating": {"title_th": "เครื่องร้อนจัด", "tools_th": ["น้ำเปล่า", "ผ้าหนา"], "steps_th": [
        "เปิดไฟฉุกเฉิน จอดข้างทางที่ปลอดภัย ดับเครื่อง", "เปิดฝากระโปรงเพื่อระบายความร้อน แต่ห้ามเปิดฝาหม้อน้ำตอนร้อน",
        "รออย่างน้อย 30 นาทีจนเครื่องเย็น", "เช็กระดับน้ำหล่อเย็นในถังพัก เติมได้เมื่อเย็นแล้ว", "ถ้าไฟยังติด/น้ำรั่ว ให้เรียกรถยก ไม่ขับต่อ"]},
}
KIT_ITEMS = ["ป้ายสามเหลี่ยมสะท้อนแสง", "สายพ่วงแบตเตอรี่", "ไฟฉาย", "ที่สูบลมไฟฟ้า/ปั๊มลม", "เสื้อสะท้อนแสง", "ผ้าเช็ดมือ+ถุงมือ", "น้ำดื่ม", "สำเนากรมธรรม์/พ.ร.บ."]

CHECK_TEXT = {
    "gas_cap": "ลองเปิดแล้วปิดฝาถังน้ำมันให้แน่นจนได้ยินเสียงคลิก",
    "oil_level": "จอดบนพื้นเรียบ รอ 5–10 นาที ดึงก้านวัดน้ำมันเครื่องเช็ดแล้วจุ่มใหม่ ดูว่าอยู่ระหว่างขีด MIN–MAX",
    "coolant_level": "รอจนเครื่องเย็น (≥30 นาที) ดูระดับน้ำหล่อเย็นที่ถังพัก ห้ามเปิดฝาหม้อน้ำตอนร้อน",
    "battery_terminals": "ดูขั้วแบตว่าหลวมหรือมีขี้เกลือสีขาว/เขียว",
    "parking_brake": "ตรวจว่าปลดเบรกมือสุดแล้ว",
    "brake_fluid": "ดูระดับน้ำมันเบรกที่กระปุกใต้ฝากระโปรง ต่ำกว่า MIN หรือเบรกนิ่ม = ห้ามขับต่อ",
    "tire_visual": "เดินดูยางทั้ง 4 เส้น มีเส้นไหนแบน มีตะปู หรือยางบวมไหม แล้วเติมลมตามขอบประตูรถ",
}

# ---------- Photo scan ----------
def scan_quality(glare, blur, tilt, n_lights):
    for v in (glare, blur, tilt):
        if not 0 <= v <= 1:
            raise ValueError("glare/blur/tilt must be 0..1")
    score = round(100 * (1 - (0.40 * glare + 0.35 * blur + 0.25 * tilt)))
    if n_lights == 0:
        score = max(0, score - 30)
    tips = []
    if glare > 0.5:
        tips.append("แสงสะท้อนบนหน้าปัดเยอะ ลองเอียงมือถือหรือบังแดด")
    if blur > 0.4:
        tips.append("ภาพเบลอ ถือมือถือนิ่ง ๆ แตะโฟกัสที่ไฟเตือน")
    if tilt > 0.4:
        tips.append("ถ่ายเอียงเกินไป ถ่ายตรงหน้าปัด")
    if n_lights == 0:
        tips.append("ไม่เจอไฟเตือน ติดเครื่องแล้วถ่ายตอนไฟยังติดอยู่")
    return {"score": score, "ok": score >= 60 and n_lights >= 1, "tips_th": tips}

def identify_lights(photo, min_conf=MIN_CONF):
    lights, uncertain = [], []
    for d in photo["detections"]:
        sym = d["symbol"]
        if sym not in LIGHTS:
            raise ValueError("unknown symbol " + sym)
        if d["confidence"] < min_conf:
            uncertain.append(sym)
            continue
        base = LIGHTS[sym]["color"]
        sev = "red" if base == "red" else "yellow" if base == "yellow" else "green"
        if sym in FLASH_ESCALATE and d.get("flashing"):
            sev = "red"
        elif base == "yellow" and d["color_seen"] == "red":
            sev = "red"
        if LIGHTS[sym].get("minor"):
            sev = "green"
        lights.append({"symbol": sym, "name_th": LIGHTS[sym]["name_th"], "name_en": LIGHTS[sym]["name_en"], "color_seen": d["color_seen"],
                       "flashing": bool(d.get("flashing")), "confidence": d["confidence"], "severity": sev})
    lights.sort(key=lambda x: (-LEVEL_RANK[x["severity"]], x["symbol"]))
    return {"photo_id": photo["id"], "lights": lights, "uncertain": uncertain}

def light_scan(photo):
    q = scan_quality(photo["glare"], photo["blur"], photo["tilt"], len(photo["detections"]))
    ident = identify_lights(photo)
    return {"photo_id": photo["id"], "quality": q, "lights": ident["lights"], "uncertain": ident["uncertain"], "light_count": len(ident["lights"])}

def pipeline_steps(photo):
    s = ["panel_detect"]
    if photo["glare"] > 0.5:
        s.append("deglare")
    if photo["tilt"] > 0.4:
        s.append("deskew")
    s += ["symbol_classify", "color_check", "urgency", "price_range"]
    return s

# ---------- Urgency meter + verdict ----------
BASE_SCORE = {"red": 85, "yellow": 40, "green": 8}

def urgency_score(lights, symptoms=()):
    sevs = [l["severity"] for l in lights]
    if not sevs:
        return 0
    top = max(sevs, key=lambda s: LEVEL_RANK[s])
    score = BASE_SCORE[top]
    score += 8 * (sum(1 for s in sevs if s == top) - 1)
    if any(l["flashing"] and l["symbol"] in FLASH_ESCALATE for l in lights):
        score = max(score, 92)
    sev = [x for x in symptoms if x in SEVERE_SYMPTOMS]
    if sev:
        score = max(score, 75) + 5 * (len(sev) - 1)
    if "steering_heavy" in symptoms or "shaking" in symptoms:
        score += 12
    return min(100, score)

def level_of(score):
    return "red" if score >= 70 else "yellow" if score >= 30 else "green"

def drive_verdict(lights, symptoms=("none",)):
    """Plain-Thai 'ขับต่อได้ไหม' answer."""
    if not lights:
        raise ValueError("no lights")
    score = urgency_score(lights, symptoms)
    level = level_of(score)
    active = [l for l in lights if LEVEL_RANK[l["severity"]] >= 2]
    if level == "red":
        why = [l["name_th"] for l in lights if l["severity"] == "red"]
        why += [SYMPTOMS[x] for x in symptoms if x in SEVERE_SYMPTOMS]
        return {"level": "red", "score": score, "can_drive": False, "max_km": 0, "max_speed_kmh": 0, "within_days": 0,
                "headline_th": "จอดเดี๋ยวนี้", "answer_th": "ไม่ควรขับต่อ จอดในที่ปลอดภัย ดับเครื่อง แล้วเรียกช่าง/รถยก", "reasons_th": why}
    if level == "yellow":
        kms = [LIGHTS[l["symbol"]]["drive_km"] for l in active if LIGHTS[l["symbol"]]["drive_km"] is not None]
        days = [LIGHTS[l["symbol"]]["drive_days"] for l in active if LIGHTS[l["symbol"]]["drive_days"] is not None]
        spd = [LIGHTS[l["symbol"]]["max_speed"] for l in active if LIGHTS[l["symbol"]]["max_speed"]]
        km, dd, sp = min(kms), min(days), min(spd)
        return {"level": "yellow", "score": score, "can_drive": True, "max_km": km, "max_speed_kmh": sp, "within_days": dd,
                "headline_th": f"ขับต่อได้ ~{km} กม.", "answer_th": f"ขับต่อได้ไม่เกิน ~{km} กม. ความเร็วไม่เกิน {sp} กม./ชม. ไปอู่ใกล้สุดภายใน {dd} วัน",
                "reasons_th": [l["name_th"] for l in active]}
    return {"level": "green", "score": score, "can_drive": True, "max_km": None, "max_speed_kmh": None, "within_days": None,
            "headline_th": "ขับต่อได้ตามปกติ", "answer_th": "ไม่ใช่อาการเสีย ขับต่อได้ แล้วจัดการตามข้อมูลของไฟเมื่อสะดวก", "reasons_th": [l["name_th"] for l in lights]}

def do_now_steps(level, symbols):
    steps = []
    if level == "red":
        keys = [("hazard", "เปิดไฟฉุกเฉิน ลดความเร็วช้า ๆ"), ("pull_over", "จอดในที่ปลอดภัยนอกเลนวิ่ง (ไหล่ทาง/ปั๊ม) ห้ามจอดกลางทางโค้ง"),
                ("engine_off", "ดับเครื่อง ดึงเบรกมือ ให้ทุกคนลงจากรถไปยืนที่ปลอดภัย")]
    elif level == "yellow":
        keys = [("slow", "ลดความเร็ว หลีกเลี่ยงเร่งแรง/บรรทุกหนัก/ทางไกล"), ("avoid_night_highway", "เลี่ยงทางด่วนและทางไกล เลือกเส้นที่มีปั๊ม/อู่ระหว่างทาง")]
    else:
        keys = [("continue", "ขับต่อได้ตามปกติ")]
    out = [{"n": i + 1, "key": k, "text_th": t} for i, (k, t) in enumerate(keys)]
    seen = set()
    for sym in symbols:
        for c in LIGHTS[sym]["checks"]:
            if c not in seen:
                seen.add(c)
                out.append({"n": len(out) + 1, "key": c, "text_th": CHECK_TEXT[c]})
    if level == "red":
        out.append({"n": len(out) + 1, "key": "call_help", "text_th": "โทรประกัน/รถยก ห้ามสตาร์ทซ้ำถ้าไฟน้ำมันเครื่อง/ความร้อนติด"})
    elif level == "yellow":
        out.append({"n": len(out) + 1, "key": "go_garage", "text_th": "ส่งการ์ดให้ช่างทาง LINE แล้วขับไปอู่ใกล้สุด"})
    return out

# ---------- Fair price ----------
def price_range(fix_id, region="bkk", car_class="eco"):
    f = FIXES[fix_id]
    m = REGION_MULT[region] * CAR_CLASSES[car_class]
    return {"fix_id": fix_id, "name_th": f["name_th"], "min_thb": int(round(f["min"] * m / 50.0) * 50), "max_thb": int(round(f["max"] * m / 50.0) * 50)}

def likely_fixes(symbols, region="bkk", car_class="eco", limit=4):
    out, seen = [], set()
    for sym in symbols:
        for fid in LIGHTS[sym]["fixes"]:
            if fid not in seen:
                seen.add(fid)
                r = price_range(fid, region, car_class)
                r["for_symbol"] = sym
                out.append(r)
    return out[:limit]

def quote_check(fix_id, quote_thb, region="bkk", car_class="eco"):
    if quote_thb < 0:
        raise ValueError("quote < 0")
    r = price_range(fix_id, region, car_class)
    if quote_thb < r["min_thb"] * 0.8:
        v, msg = "low", "ถูกกว่าช่วงปกติ ถามว่าเป็นอะไหล่เกรดไหน/รับประกันไหม"
    elif quote_thb <= r["max_thb"]:
        v, msg = "fair", "อยู่ในช่วงที่สมเหตุสมผล"
    elif quote_thb <= r["max_thb"] * 1.3:
        v, msg = "high", "สูงกว่าช่วงปกติเล็กน้อย ขอรายละเอียดค่าอะไหล่/ค่าแรง"
    else:
        v, msg = "very_high", "สูงกว่าช่วงปกติมาก ขอใบเสนอราคาเป็นลายลักษณ์อักษรและลองถามอู่อื่น"
    return {"fix_id": fix_id, "quote_thb": quote_thb, "min_thb": r["min_thb"], "max_thb": r["max_thb"], "verdict": v, "message_th": msg,
            "questions_th": FIXES[fix_id]["ask_th"] + ["ขอดูอะไหล่เก่า/ภาพถ่ายจุดที่เสีย"], "disclaimer_th": PRICE_DISCLAIMER_TH}

# ---------- Mechanic card ----------
def mechanic_card(person, car, verdict, symbols, symptoms, fixes, extra_note_th=""):
    names = " + ".join(LIGHTS[s]["name_th"] for s in symbols)
    sym_txt = "ไม่มีอาการอื่น" if list(symptoms) in (["none"], []) else ", ".join(SYMPTOMS[x] for x in symptoms)
    lo = sum(f["min_thb"] for f in fixes[:2])
    hi = sum(f["max_thb"] for f in fixes[:2])
    title = f"การ์ดส่งช่าง — {car['model_th']}"
    lines = [f"รถ: {car['model_th']} ปี {car['year']} เลขไมล์ {car['odometer_km']:,} กม.", f"ไฟเตือน: {names}", f"อาการ: {sym_txt}",
             f"ความเร่งด่วน: {LEVELS[verdict['level']]}"]
    if lo or hi:
        lines.append(f"ช่วงงบที่คาดไว้ ~฿{lo:,}–{hi:,} (ประมาณเอง)")
    if extra_note_th:
        lines.append(extra_note_th)
    lines.append(f"ฝากช่วยเช็กให้หน่อยครับ/ค่ะ — {person['name_th']}")
    text = "\n".join(lines)
    return {"title_th": title, "name_th": person["name_th"], "car_model_th": car["model_th"], "odometer_km": car["odometer_km"], "symbols": symbols,
            "symptoms": list(symptoms), "level": verdict["level"], "budget_min_thb": lo, "budget_max_thb": hi, "note_th": text,
            "line_share_url": "https://line.me/R/share?text=" + _up.quote(text), "disclaimer_th": PRICE_DISCLAIMER_TH}

# ---------- Car diary + reminders ----------
def _add_months(d, m):
    y, mo = divmod(d.month - 1 + m, 12)
    y += d.year
    mo += 1
    day = min(d.day, [31, 29 if y % 4 == 0 and (y % 100 or y % 400 == 0) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][mo - 1])
    return _dt.date(y, mo, day)

def service_entry(eid, car_id, date, odometer_km, item, cost_thb, shop_th):
    if item not in SERVICE_ITEMS:
        raise ValueError("unknown item")
    return {"id": eid, "car_id": car_id, "date": date, "odometer_km": odometer_km, "item": item, "cost_thb": cost_thb, "shop_th": shop_th, "on_device": True}

def next_due(entry):
    it = SERVICE_ITEMS[entry["item"]]
    d = _add_months(_dt.date.fromisoformat(entry["date"]), it["months"])
    return {"item": entry["item"], "label_th": it["label_th"], "due_km": None if it["km"] is None else entry["odometer_km"] + it["km"], "due_date": d.isoformat()}

def reminder_status(entry, now_km, today):
    nd = next_due(entry)
    t = _dt.date.fromisoformat(today)
    days_left = (_dt.date.fromisoformat(nd["due_date"]) - t).days
    km_left = None if nd["due_km"] is None else nd["due_km"] - now_km
    over = days_left < 0 or (km_left is not None and km_left < 0)
    due = days_left <= DUE_DAYS or (km_left is not None and km_left <= DUE_KM)
    soon = days_left <= SOON_DAYS or (km_left is not None and km_left <= SOON_KM)
    status = "overdue" if over else "due" if due else "soon" if soon else "ok"
    return {"item": entry["item"], "label_th": nd["label_th"], "status": status, "days_left": days_left, "km_left": km_left,
            "due_km": nd["due_km"], "due_date": nd["due_date"]}

def diary_stats(entries):
    if not entries:
        return {"count": 0, "total_thb": 0, "avg_thb": 0, "last_odometer_km": None, "top_item": None}
    tot = sum(e["cost_thb"] for e in entries)
    cnt = {}
    for e in entries:
        cnt[e["item"]] = cnt.get(e["item"], 0) + 1
    top = sorted(cnt.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]
    return {"count": len(entries), "total_thb": tot, "avg_thb": int(round(tot / len(entries))),
            "last_odometer_km": max(e["odometer_km"] for e in entries), "top_item": top}

# ---------- Emergency kit ----------
def emergency_kit(profile):
    contacts = []
    for h in HOTLINES:
        c = dict(h)
        if h["key"] == "insurer" and profile.get("insurer_hotline"):
            c.update(number=profile["insurer_hotline"], kind="user", label_th=f"ประกัน {profile.get('insurer_th', '')}".strip())
        if h["key"] == "tow" and profile.get("tow_phone"):
            c.update(number=profile["tow_phone"], kind="user")
        if h["key"] == "garage" and profile.get("garage_phone"):
            c.update(number=profile["garage_phone"], kind="user")
        contacts.append(c)
    missing = [c["key"] for c in contacts if c["number"] is None]
    return {"contacts": contacts, "missing": missing, "kit_items_th": list(KIT_ITEMS), "guides": sorted(GUIDES)}

def guide(key):
    g = GUIDES[key]
    return {"key": key, "title_th": g["title_th"], "tools_th": g["tools_th"],
            "steps": [{"n": i + 1, "text_th": t} for i, t in enumerate(g["steps_th"])], "disclaimer_th": SAFETY_DISCLAIMER_TH}

# ---------- Share + quota ----------
def share_card(name_th, symbols, verdict):
    names = " + ".join(LIGHTS[s]["name_en"] for s in symbols)
    return {"title_th": f"DashDoc — {name_th}", "headline_th": verdict["headline_th"], "hook_th": "ไฟโชว์หน้าปัด ขับต่อได้ไหม? ถ่ายรูปเดียวรู้ใน 3 วิ",
            "symbols": symbols, "level": verdict["level"], "score": verdict["score"], "layout": "scan_result", "sizes": ["1080x1350", "1080x1920", "1080x1080"],
            "watermark": WATERMARK, "cta_th": f"ไฟเตือน {names} · ลอง DashDoc ฟรี"}

def quota(used_today, want, pro=False):
    if pro:
        return {"allowed": want, "left_after": None, "paywall": False}
    left = max(0, FREE_SCANS_PER_DAY - used_today)
    allowed = min(want, left)
    return {"allowed": allowed, "left_after": left - allowed, "paywall": allowed < want}

def safety_guard(level):
    if level == "red":
        return {"level": "stop", "message_th": "ไฟแดง/อาการรุนแรง: จอดในที่ปลอดภัย อย่าฝืนขับ " + SAFETY_DISCLAIMER_TH}
    if level == "yellow":
        return {"level": "warn", "message_th": "ถ้าอาการแย่ลงระหว่างทาง ให้จอดทันที " + SAFETY_DISCLAIMER_TH}
    return {"level": "ok", "message_th": SAFETY_DISCLAIMER_TH}
