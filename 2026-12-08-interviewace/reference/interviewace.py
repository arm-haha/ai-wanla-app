"""InterviewAce deterministic logic (no AI calls). Interview practice — not a job offer or hiring decision."""
FILLERS = ("อ่า", "เอ่อ", "คือ", "ก็", "แบบ")
STAR_KEYS = {
    "S": ("สถานการณ์", "ตอนนั้น", "ครั้งหนึ่ง", "ช่วงนั้น"),
    "T": ("งานที่", "หน้าที่", "ได้รับมอบ", "โจทย์คือ"),
    "A": ("ฉันจึง", "เลยทำ", "สิ่งที่ทำ", "เลยลงมือ"),
    "R": ("ผลคือ", "ผลลัพธ์", "ได้ยอด", "เพิ่มขึ้น", "เสร็จตาม"),
}
ROLES = {
    "marketing": {
        "id": "r01", "name_th": "งานการตลาด", "name_en": "Marketing",
        "seniority": "junior",
        "questions": [
            "เล่าตอนที่ต้องทำงานเป็นทีมแล้วมีปัญหา",
            "เคยทำแคมเปญแล้ววัดผลอย่างไร",
            "ถ้างบน้อย แต่ต้องเห็นผลใน 2 สัปดาห์ จะเริ่มตรงไหน",
            "เล่าครั้งที่รับฟีดแบ็กแล้วปรับงาน",
        ],
    },
    "engineer": {
        "id": "r02", "name_th": "งานวิศวกร / นักพัฒนา", "name_en": "Engineer",
        "seniority": "mid",
        "questions": [
            "เล่าบั๊กที่ยากที่สุดที่เคยแก้",
            "เคยไม่เห็นด้วยกับแนวทางในทีม แล้วทำอย่างไร",
            "อธิบายโปรเจกต์ที่ภูมิใจแบบคนไม่ใช่สายเทคนิคฟังรู้เรื่อง",
            "ถ้าเดดไลน์ใกล้แต่คุณภาพยังไม่พร้อม จะตัดสินใจอย่างไร",
        ],
    },
    "nurse": {
        "id": "r03", "name_th": "งานพยาบาล", "name_en": "Nurse",
        "seniority": "junior",
        "questions": [
            "เล่าตอนที่ต้องสื่อสารกับญาติคนไข้ในสถานการณ์ตึงเครียด",
            "เคยเจอเหตุไม่คาดคิดระหว่างเวร แล้วจัดการอย่างไร",
            "ทำงานเป็นทีมกับแพทย์และเพื่อนร่วมเวรอย่างไร",
            "ดูแลตัวเองอย่างไรหลังเวรหนัก",
        ],
    },
    "teacher": {
        "id": "r04", "name_th": "งานครู / ติวเตอร์", "name_en": "Teacher",
        "seniority": "junior",
        "questions": [
            "เล่าตอนที่สอนแล้วเด็กไม่เข้าใจ แล้วปรับอย่างไร",
            "เคยจัดการห้องที่สมาธิหลุด แล้วทำอะไร",
            "ออกแบบคาบเรียนใหม่ให้ใน 3 ประโยค",
            "รับฟีดแบ็กจากผู้ปกครองอย่างไร",
        ],
    },
    "sales": {
        "id": "r05", "name_th": "งานขาย", "name_en": "Sales",
        "seniority": "mid",
        "questions": [
            "เล่าตอนที่เกือบเสียดีล แล้วพลิกกลับมาได้อย่างไร",
            "ทำความรู้จักลูกค้าใหม่ใน 5 นาทีแรกอย่างไร",
            "เคยถูกปฏิเสธซ้ำ ๆ แล้วยังเดินต่อได้เพราะอะไร",
            "ตั้งเป้าและติดตามผลของตัวเองอย่างไร",
        ],
    },
    "fresh_grad": {
        "id": "r06", "name_th": "จบใหม่ / ยังไม่มีประสบการณ์งาน", "name_en": "Fresh graduate",
        "seniority": "entry",
        "questions": [
            "เล่าโครงงานหรือกิจกรรมที่เคยทำเป็นทีม",
            "ทำไมสนใจตำแหน่งนี้",
            "เคยล้มเหลวในงานกลุ่ม แล้วเรียนรู้อะไร",
            "ใน 90 วันแรก จะเรียนรู้งานอย่างไร",
        ],
    },
}
ROLE_IDS = list(ROLES)
FREE_GENS_PER_DAY = 3
WATERMARK = "Made with InterviewAce · practice only, not a hiring decision"
SAFETY_DISCLAIMER_TH = "InterviewAce เป็นเครื่องมือซ้อมสัมภาษณ์เท่านั้น ไม่ใช่การรับรองว่าจะได้งาน ไม่ใช่คะแนนจากผู้สัมภาษณ์จริง และไม่ใช่คำแนะนำด้านอาชีพเฉพาะบุคคล คะแนนในแอปเป็นค่าตัวอย่างจากสูตรที่ตั้งเอง"

def role_info(role):
    if role not in ROLES:
        raise ValueError("unknown role")
    r = ROLES[role]
    return {"id": r["id"], "role": role, "name_th": r["name_th"], "name_en": r["name_en"],
            "seniority": r["seniority"], "questions": list(r["questions"]), "count": len(r["questions"])}


def question_card(role, index):
    info = role_info(role)
    if index not in range(info["count"]):
        raise ValueError("question index out of range")
    return {"role": role, "index": index, "prompt_th": info["questions"][index],
            "role_th": info["name_th"], "ideal_sec": 75, "ideal_words": 100}


def tokenize(transcript):
    if not isinstance(transcript, str) or not transcript.strip():
        raise ValueError("transcript required")
    return transcript.split()


def word_count(transcript):
    return len(tokenize(transcript))


def filler_count(transcript):
    toks = tokenize(transcript)
    counts = {f: toks.count(f) for f in FILLERS}
    total = sum(counts.values())
    words = len(toks)
    ratio = round(total / words, 4) if words else 0.0
    return {"counts": counts, "total": total, "word_count": words, "ratio": ratio,
            "label_th": f"คำเติม {total} จาก {words} คำ"}


def star_flags(transcript):
    flags = {}
    for part, keys in STAR_KEYS.items():
        flags[part] = any(k in transcript for k in keys)
    return flags


def star_score(flags):
    return int(round(25 * sum(1 for v in flags.values() if v)))


def length_score(words, duration_sec=None):
    # peak 100 at 100 words; 1.5 points off per word away, clamped
    score = 100 - abs(words - 100) * 1.5
    if duration_sec is not None:
        if duration_sec < 0:
            raise ValueError("duration must be >= 0")
        # also peak at 75s; blend 50/50 if provided
        dscore = 100 - abs(duration_sec - 75) * 1.2
        score = 0.5 * score + 0.5 * dscore
    return max(0, min(100, int(round(score))))


def clarity_score(ratio):
    return max(0, min(100, int(round(100 - ratio * 400))))


def structure_score(flags, words):
    star = star_score(flags)
    body = 100 if words >= 40 else int(round(words * 2.5))
    return int(round(0.8 * star + 0.2 * body))


def score_answer(transcript, duration_sec=None):
    fill = filler_count(transcript)
    flags = star_flags(transcript)
    words = fill["word_count"]
    length = length_score(words, duration_sec)
    clarity = clarity_score(fill["ratio"])
    star = star_score(flags)
    structure = structure_score(flags, words)
    overall = int(round(0.25 * structure + 0.25 * clarity + 0.20 * length + 0.30 * star))
    band = "พร้อมมาก" if overall >= 85 else "พร้อมปานกลาง" if overall >= 65 else "ต้องซ้อมอีก"
    return {
        "overall": overall, "structure": structure, "clarity": clarity, "length": length, "star": star,
        "band_th": band, "word_count": words, "filler_total": fill["total"], "filler_ratio": fill["ratio"],
        "star_flags": flags, "duration_sec": duration_sec,
        "headline_th": f"คะแนนรวม {overall} · {band}",
        "disclaimer_th": SAFETY_DISCLAIMER_TH,
    }


def star_rewrite(situation, task, action, result):
    parts = [situation.strip(), task.strip(), action.strip(), result.strip()]
    if any(not p for p in parts):
        raise ValueError("all STAR parts required")
    text = (
        f"สถานการณ์: {parts[0]} "
        f"งานที่ได้รับ: {parts[1]} "
        f"สิ่งที่ทำ: {parts[2]} "
        f"ผลลัพธ์: {parts[3]}"
    )
    return {"situation_th": parts[0], "task_th": parts[1], "action_th": parts[2], "result_th": parts[3],
            "text_th": text, "char_count": len(text), "tip_th": "จบด้วยผลที่วัดได้ จะจำง่ายขึ้นตอนสัมภาษณ์"}


def confidence_report(score, name_th, role_th):
    tips = []
    if score["star"] < 80:
        missing = [k for k, v in score["star_flags"].items() if not v]
        label = {"S": "สถานการณ์", "T": "งานที่ได้รับ", "A": "สิ่งที่ทำ", "R": "ผลลัพธ์"}
        if missing:
            tips.append("เติมส่วน " + " ".join(label[m] for m in missing) + " ให้ครบ และ ideally จบด้วยตัวเลข")
        else:
            tips.append("โครง STAR ครบแล้ว ลองย่อให้กระชับขึ้น")
    if score["clarity"] < 75:
        tips.append("ลดคำเติมอย่าง อ่า เอ่อ แบบ จะฟังชัดขึ้น")
    if score["length"] < 75:
        tips.append("จับเวลาให้อยู่ราว 45–90 วินาที หรือประมาณ 80–120 คำ")
    if not tips:
        tips.append("คะแนนดีแล้ว ซ้อมอีก 1–2 รอบให้คล่องปาก")
    return {
        "name_th": name_th, "role_th": role_th, "overall": score["overall"], "band_th": score["band_th"],
        "structure": score["structure"], "clarity": score["clarity"], "length": score["length"], "star": score["star"],
        "tips_th": tips, "headline_th": score["headline_th"], "disclaimer_th": SAFETY_DISCLAIMER_TH,
    }


def drill(weakest):
    bank = {
        "star": "เล่าคำตอบเดิมใหม่ โดยพูดสี่ประโยคตาม สถานการณ์ / งานที่ได้รับ / สิ่งที่ทำ / ผลลัพธ์",
        "clarity": "อัดคลิป 30 วินาทีโดยห้ามใช้คำว่า อ่า เอ่อ แบบ",
        "length": "ตั้งเวลา 75 วินาที แล้วเล่าให้จบพอดี ไม่เร็วไม่ช้า",
        "structure": "เขียนโครงสามบรรทัด เปิด-เนื้อ-ปิด ก่อนพูด",
    }
    if weakest not in bank:
        raise ValueError("unknown drill")
    return {"focus": weakest, "task_th": bank[weakest], "minutes": 5}


def share_card(name_th, overall, band_th, role_th):
    return {
        "title_th": f"InterviewAce — {name_th}",
        "headline_th": f"คะแนนรวม {overall} · {band_th}",
        "hook_th": "ซ้อมสัมภาษณ์งานกับ AI",
        "role_th": role_th, "overall": overall,
        "layout": "score_report", "sizes": ["1080x1350", "1080x1920", "1080x1080"],
        "watermark": WATERMARK,
        "cta_th": f"คอมเมนต์ ACE รับแพ็กฟรี · {band_th}",
        "disclaimer_th": SAFETY_DISCLAIMER_TH,
    }


def quota(used_today, want, pro=False):
    if pro:
        return {"allowed": want, "left_after": None, "paywall": False}
    left = max(0, FREE_GENS_PER_DAY - used_today)
    allowed = min(want, left)
    return {"allowed": allowed, "left_after": left - allowed, "paywall": allowed < want}


def safety_guard(ok=True):
    if not ok:
        return {"level": "stop", "message_th": "ยังให้คะแนนไม่ได้ " + SAFETY_DISCLAIMER_TH}
    return {"level": "ok", "message_th": SAFETY_DISCLAIMER_TH}
