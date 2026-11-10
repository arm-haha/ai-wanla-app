"""TripStitch deterministic logic (no AI calls). Hours, travel times and costs are app-chosen examples — not live data or a booking."""
import datetime as _dt
import urllib.parse as _up

SOURCES = ["ig", "maps", "tiktok", "web", "note"]
TYPES = ["cafe", "food", "temple", "market", "viewpoint", "photo", "activity", "stay"]
SLOTS = ["morning", "afternoon", "evening"]
CLIMATES = ["hot", "cool_morning", "rain_possible", "cold"]
MIN_CONF = 0.6
FREE_SCANS_PER_DAY = 3
WATERMARK = "Made with TripStitch · plan only, not a booking"
SAFETY_DISCLAIMER_TH = "TripStitch เป็นแผนเที่ยวเบื้องต้นจากแคปจอ ไม่ใช่ข้อมูลเวลาเปิด-ปิดหรือราคาจริง ตรวจกับแหล่งทางการก่อนเดินทาง และห้ามแชร์ตำแหน่งบ้านของผู้อื่น"
PRICE_DISCLAIMER_TH = "ตัวเลขงบเป็นค่าประมาณการที่ตั้งเอง ไม่ใช่ราคาจองจริง"

# Example travel minutes between area pairs (undirected).
AREA_MIN = {
    frozenset(("nimman", "old_city")): 15,
    frozenset(("nimman", "doi_suthep")): 40,
    frozenset(("nimman", "mae_rim")): 35,
    frozenset(("old_city", "doi_suthep")): 30,
    frozenset(("old_city", "mae_rim")): 45,
    frozenset(("doi_suthep", "mae_rim")): 50,
    frozenset(("nimman", "airport")): 25,
    frozenset(("old_city", "airport")): 30,
    frozenset(("silom", "thonglor")): 20,
    frozenset(("silom", "old_town")): 25,
    frozenset(("thonglor", "old_town")): 30,
    frozenset(("chiang_khan_walk", "mekong")): 10,
    frozenset(("chiang_khan_walk", "hill")): 20,
    frozenset(("mekong", "hill")): 25,
}
SLOT_PREF = {
    "cafe": "morning", "temple": "morning", "photo": "afternoon", "viewpoint": "afternoon",
    "food": "afternoon", "activity": "afternoon", "market": "evening", "stay": "evening",
}
# Per-visit example costs, mid used in budget.
VISIT_COST = {
    "cafe": (100, 200), "food": (80, 180), "temple": (0, 100), "market": (100, 300),
    "viewpoint": (0, 80), "photo": (0, 50), "activity": (200, 800), "stay": (0, 0),
}
STAY_PER_NIGHT = 900  # example mid-range room THB
FOOD_PER_PAX_DAY = 300
TRANSPORT_PER_DAY = 150
BUFFER_RATE = 0.125

PACK_BASE = ["ยาประจำตัว", "ที่ชาร์จและแบตสำรอง", "เอกสาร/บัตรประชาชน", "เงินสดเล็กน้อยและบัตร"]
PACK_BY_CLIMATE = {
    "hot": ["เสื้อระบายอากาศ", "ครีมกันแดด", "หมวกหรือร่มกันแดด", "ขวดน้ำ"],
    "cool_morning": ["เสื้อคลุมบาง", "กางเกงขายาว 1 ตัวสำหรับเช้า"],
    "rain_possible": ["ร่มพับหรือเสื้อกันฝนบาง", "ถุงซิปล็อคกันชื้น"],
    "cold": ["เสื้อกันหนาว", "กางเกงขายาว", "ถุงเท้า"],
}
PACK_BY_TYPE = {
    "temple": ["ชุดสุภาพคลุมไหล่-เข่า สำหรับเข้าวัด"],
    "cafe": ["กล้องหรือมือถือพร้อมที่ชาร์จ"],
    "market": ["กระเป๋าสะพายปิดซิป", "รองเท้าเดินสบาย"],
    "viewpoint": ["รองเท้ากันลื่น"],
    "activity": ["ขวดน้ำเพิ่ม"],
}

def travel_min(a, b):
    if a == b:
        return 10
    return AREA_MIN.get(frozenset((a, b)), 40)

def scan_quality(glare, blur, crop, n_places):
    for v in (glare, blur, crop):
        if not 0 <= v <= 1:
            raise ValueError("glare/blur/crop must be 0..1")
    score = round(100 * (1 - (0.35 * glare + 0.40 * blur + 0.25 * crop)))
    if n_places == 0:
        score = max(0, score - 30)
    tips = []
    if glare > 0.5:
        tips.append("แสงสะท้อนบนจอเยอะ ลดความสว่างจอหรือถ่ายในที่ร่ม")
    if blur > 0.4:
        tips.append("ภาพเบลอ แคปจอใหม่จากแอปต้นทางจะคมกว่าการถ่ายหน้าจอ")
    if crop > 0.45:
        tips.append("ชื่อสถานที่ถูกครอป เลื่อนแคปให้อยู่ครบทั้งชื่อและพิกัด/ย่าน")
    if n_places == 0:
        tips.append("ไม่เจอชื่อสถานที่ ลองแคปจอที่มีชื่อร้านหรือหมุดแผนที่ชัด ๆ")
    return {"score": score, "ok": score >= 60 and n_places >= 1, "tips_th": tips, "place_hint_count": n_places}

def extract_places(shot, min_conf=MIN_CONF):
    found, uncertain = [], []
    for d in shot["detections"]:
        if d["type"] not in TYPES:
            raise ValueError("unknown type " + d["type"])
        if d["confidence"] < min_conf:
            uncertain.append(d["name_th"])
            continue
        found.append({
            "id": d["id"], "name_th": d["name_th"], "name_en": d.get("name_en", d["name_th"]),
            "area": d["area"], "type": d["type"], "source": d.get("source", "note"),
            "confidence": d["confidence"], "open_hour": d.get("open_hour"), "close_hour": d.get("close_hour"),
            "closed_dow": list(d.get("closed_dow") or []), "ticket_thb": int(d.get("ticket_thb") or 0),
            "note_th": d.get("note_th") or "",
        })
    q = scan_quality(shot["glare"], shot["blur"], shot["crop"], len(shot["detections"]))
    return {"shot_id": shot["id"], "quality": q, "places": found, "uncertain": uncertain, "place_count": len(found)}

def pipeline_steps(shot):
    s = ["screen_detect"]
    if shot["glare"] > 0.5:
        s.append("deglare")
    if shot["crop"] > 0.45:
        s.append("recrop")
    s += ["ocr_name", "area_match", "dedupe", "day_plan", "budget"]
    return s

def stitch_places(shots):
    by_id, uncertain, shot_ids = {}, [], []
    for sh in shots:
        r = extract_places(sh)
        shot_ids.append(sh["id"])
        uncertain.extend(r["uncertain"])
        for p in r["places"]:
            if p["id"] not in by_id or p["confidence"] > by_id[p["id"]]["confidence"]:
                by_id[p["id"]] = p
    places = sorted(by_id.values(), key=lambda p: (p["area"], p["name_th"]))
    return {"shot_ids": shot_ids, "places": places, "place_count": len(places), "uncertain": uncertain,
            "areas": sorted({p["area"] for p in places})}

def _slot_rank(place):
    pref = SLOT_PREF[place["type"]]
    return SLOTS.index(pref)

def plan_days(places, start_date, nights, pax=2):
    if not places:
        raise ValueError("no places")
    if nights < 1:
        raise ValueError("nights < 1")
    days_n = nights + 1  # days on the ground (arrive day 1, leave after last night)
    start = _dt.date.fromisoformat(start_date)
    # cluster by area, larger clusters first, then name
    areas = {}
    for p in places:
        areas.setdefault(p["area"], []).append(p)
    clusters = sorted(areas.values(), key=lambda c: (-len(c), c[0]["area"]))
    # assign whole clusters to days, cycling if more clusters than days
    day_places = [[] for _ in range(days_n)]
    for i, cluster in enumerate(clusters):
        day_places[i % days_n].extend(cluster)
    # if a day is empty, pull one place from the fullest day
    for i, dp in enumerate(day_places):
        if not dp:
            src = max(range(days_n), key=lambda j: len(day_places[j]))
            if day_places[src]:
                dp.append(day_places[src].pop())
    itinerary = []
    prev_area = None
    for i, dp in enumerate(day_places):
        ordered = sorted(dp, key=lambda p: (_slot_rank(p), p["name_th"]))
        stops, last = [], prev_area
        used_slots = set()
        for p in ordered:
            slot = SLOT_PREF[p["type"]]
            # if slot taken, bump to next available
            if slot in used_slots:
                for alt in SLOTS:
                    if alt not in used_slots:
                        slot = alt
                        break
            used_slots.add(slot)
            travel = 0 if last is None else travel_min(last, p["area"])
            stops.append({
                "n": len(stops) + 1, "place_id": p["id"], "name_th": p["name_th"], "area": p["area"],
                "type": p["type"], "slot": slot, "travel_min": travel,
                "open_hour": p["open_hour"], "close_hour": p["close_hour"],
            })
            last = p["area"]
        d = start + _dt.timedelta(days=i)
        itinerary.append({
            "day": i + 1, "date": d.isoformat(), "dow": d.strftime("%A").lower(),
            "stops": stops, "stop_count": len(stops),
            "areas": sorted({s["area"] for s in stops}),
            "total_travel_min": sum(s["travel_min"] for s in stops),
        })
        prev_area = last
    return {"start_date": start_date, "nights": nights, "days": days_n, "pax": pax,
            "itinerary": itinerary, "place_count": len(places)}

def closed_warnings(plan, places):
    by_id = {p["id"]: p for p in places}
    out = []
    for day in plan["itinerary"]:
        # Python Monday=0; our closed_dow uses 0=Mon ... 6=Sun
        dow = _dt.date.fromisoformat(day["date"]).weekday()
        for s in day["stops"]:
            p = by_id[s["place_id"]]
            if dow in p["closed_dow"]:
                out.append({
                    "day": day["day"], "date": day["date"], "place_id": p["id"], "name_th": p["name_th"],
                    "message_th": f"{p['name_th']} ปิดวันนั้น ลองย้ายไปวันอื่นหรือเลือกแผนสำรอง",
                })
    return out

def rain_plan(plan, places):
    indoor = [p for p in places if p["type"] in ("cafe", "food", "market", "activity")]
    tips = ["เช็กฝนเช้าวันนั้น ถ้าฝนตกหนักสลับคาเฟ่/ร้านอาหารในร่มก่อน", "พกร่มพับและถุงกันชื้นให้กล้อง"]
    alts = [{"name_th": p["name_th"], "area": p["area"], "type": p["type"]} for p in indoor[:4]]
    return {"tips_th": tips, "indoor_alts": alts, "disclaimer_th": SAFETY_DISCLAIMER_TH}

def _round50(n):
    return int(round(n / 50.0) * 50)

def budget_split(places, nights, pax, budget_thb, stay_thb=None):
    if pax < 1 or nights < 1 or budget_thb < 0:
        raise ValueError("bad budget inputs")
    stay = stay_thb if stay_thb is not None else STAY_PER_NIGHT * nights
    food = FOOD_PER_PAX_DAY * pax * (nights + 1)
    transport = TRANSPORT_PER_DAY * (nights + 1)
    tickets = sum(p["ticket_thb"] * pax for p in places)
    extras = 0
    for p in places:
        lo, hi = VISIT_COST[p["type"]]
        extras += int(round((lo + hi) / 2)) * pax
    # cafe/food visit costs already partly overlap daily food — count only cafe/activity/market extras at 50%
    extras = 0
    for p in places:
        if p["type"] in ("cafe", "market", "activity", "viewpoint"):
            lo, hi = VISIT_COST[p["type"]]
            extras += int(round((lo + hi) / 2)) * pax
    planned = stay + food + transport + tickets + extras
    buffer = _round50(max(budget_thb * BUFFER_RATE, planned * BUFFER_RATE))
    # If the demo budget is meant to include buffer, keep planned+buffer vs budget
    total = planned + buffer
    per_pax = int(round(total / pax))
    if budget_thb <= 0:
        verdict, msg = "unknown", "ยังไม่ได้ตั้งงบ"
    elif total <= budget_thb * 0.85:
        verdict, msg = "under", "ต่ำกว่างบที่ตั้งไว้ มีเหลือสำหรับของฝากหรือมื้อพิเศษ"
    elif total <= budget_thb:
        verdict, msg = "fit", "อยู่ในงบที่ตั้งไว้"
    elif total <= budget_thb * 1.15:
        verdict, msg = "tight", "ตึงงบเล็กน้อย ลดมื้อพิเศษหรือเลือกที่พักถูกลงได้"
    else:
        verdict, msg = "over", "เกินงบที่ตั้งไว้ ลองลดคืนที่พัก หรือตัดสถานที่ที่เสียค่าเข้า"
    lines = [
        {"key": "stay", "label_th": "ที่พัก", "thb": stay},
        {"key": "food", "label_th": "อาหาร", "thb": food},
        {"key": "transport", "label_th": "เดินทาง", "thb": transport},
        {"key": "tickets", "label_th": "ค่าเข้า/ตั๋ว", "thb": tickets},
        {"key": "extras", "label_th": "คาเฟ่และของจิปาถะ", "thb": extras},
        {"key": "buffer", "label_th": "เผื่อเหลือ", "thb": buffer},
    ]
    return {"budget_thb": budget_thb, "planned_thb": planned, "buffer_thb": buffer, "total_thb": total,
            "per_pax_thb": per_pax, "pax": pax, "nights": nights, "lines": lines,
            "verdict": verdict, "message_th": msg, "disclaimer_th": PRICE_DISCLAIMER_TH}

def packing_list(nights, climates, types):
    if nights < 1:
        raise ValueError("nights < 1")
    days = nights + 1
    items = [{"key": "tees", "text_th": f"เสื้อยืดหรือเสื้อสบาย {days} ตัว", "group": "clothes"},
             {"key": "pants", "text_th": f"กางเกง/กระโปรง {max(2, days - 1)} ตัว", "group": "clothes"},
             {"key": "underwear", "text_th": f"ชุดชั้นในและถุงเท้า {days} ชุด", "group": "clothes"}]
    seen = set()
    for c in climates:
        if c not in CLIMATES:
            raise ValueError("unknown climate")
        for t in PACK_BY_CLIMATE[c]:
            if t not in seen:
                seen.add(t)
                items.append({"key": f"climate_{len(seen)}", "text_th": t, "group": "weather"})
    for typ in types:
        for t in PACK_BY_TYPE.get(typ, []):
            if t not in seen:
                seen.add(t)
                items.append({"key": f"type_{len(seen)}", "text_th": t, "group": "activity"})
    for i, t in enumerate(PACK_BASE):
        items.append({"key": f"base_{i}", "text_th": t, "group": "essentials"})
    return {"nights": nights, "days": days, "climates": list(climates), "count": len(items), "items": items}

def share_card(title_th, dest_th, plan, budget):
    days = ", ".join(f"วันที่ {d['day']} {len(d['stops'])} จุด" for d in plan["itinerary"])
    return {"title_th": title_th, "headline_th": dest_th,
            "hook_th": "แคปจอที่เที่ยวเก็บไว้ กลายเป็นทริปพร้อมเที่ยว",
            "days_th": days, "total_thb": budget["total_thb"], "verdict": budget["verdict"],
            "layout": "trip_card", "sizes": ["1080x1350", "1080x1920", "1080x1080"],
            "watermark": WATERMARK, "offline": True,
            "cta_th": f"งบประมาณ ~฿{budget['total_thb']:,} · คอมเมนต์ TRIP รับแพ็กฟรี"}

def quota(used_today, want, pro=False):
    if pro:
        return {"allowed": want, "left_after": None, "paywall": False}
    left = max(0, FREE_SCANS_PER_DAY - used_today)
    allowed = min(want, left)
    return {"allowed": allowed, "left_after": left - allowed, "paywall": allowed < want}

def safety_guard(has_places, warnings=0):
    if not has_places:
        return {"level": "warn", "message_th": "ยังไม่มีสถานที่พอสำหรับวางแผน " + SAFETY_DISCLAIMER_TH}
    if warnings:
        return {"level": "warn", "message_th": "มีร้านที่ปิดในวันที่วางไว้ ตรวจอีกครั้งก่อนเดินทาง " + SAFETY_DISCLAIMER_TH}
    return {"level": "ok", "message_th": SAFETY_DISCLAIMER_TH}
