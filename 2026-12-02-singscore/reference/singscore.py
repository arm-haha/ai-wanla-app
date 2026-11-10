"""SingScore deterministic logic (no AI calls).
Scoring uses app-chosen formulas on pitch/timing numbers — not a vocal coach or ENT doctor.
No copyrighted lyrics or commercial karaoke tracks are bundled. Users bring their own audio.
"""
FREE_SCANS_PER_DAY = 3
MIN_CONF = 0.6
WATERMARK = "Made with SingScore · practice only, no bundled lyrics"
SAFETY_DISCLAIMER_TH = "SingScore เป็นคะแนนฝึกซ้อมจากระดับเสียงและจังหวะ ไม่ใช่ครูสอนร้องและไม่ใช่แพทย์ แพ็กนี้ไม่มีเนื้อเพลงลิขสิทธิ์ ผู้ใช้ต้องใช้เสียงฮัมหรือแทร็กของตนเอง และอย่าร้องจนเจ็บคอ"

# Original practice pieces only — not commercial songs.
EXERCISES = {
    "scale_run_c": {"id": "ex01", "name_th": "สเกลรันบันไดเสียง C", "name_en": "ScaleRun in C", "tonic": "C", "mode": "major", "notes": ["C","D","E","F","G","A","B","C"]},
    "scale_run_g": {"id": "ex02", "name_th": "สเกลรันบันไดเสียง G", "name_en": "ScaleRun in G", "tonic": "G", "mode": "major", "notes": ["G","A","B","C","D","E","F#","G"]},
    "scale_run_f": {"id": "ex03", "name_th": "สเกลรันบันไดเสียง F", "name_en": "ScaleRun in F", "tonic": "F", "mode": "major", "notes": ["F","G","A","Bb","C","D","E","F"]},
    "breath_pulse": {"id": "ex04", "name_th": "พัลส์ลมหายใจ", "name_en": "BreathPulse", "tonic": "C", "mode": "drone", "notes": ["C","C","C","C"]},
    "hum_fifth": {"id": "ex05", "name_th": "ฮัมช่วงห้า", "name_en": "HumFifth", "tonic": "C", "mode": "fifth", "notes": ["C","G","C"]},
    "vowel_hold": {"id": "ex06", "name_th": "ลากสระอา", "name_en": "VowelHold Ah", "tonic": "A", "mode": "drone", "notes": ["A","A","A"]},
}

WARMUPS = {
    "lip_trill": {"id": "wu01", "name_th": "ลิปทริลล์", "sec": 30, "how_th": "ปิดปากเบา ๆ แล้วเป่าลมให้ริมฝีปากสั่น เลื่อนเสียงขึ้นลงช้า ๆ"},
    "siren": {"id": "wu02", "name_th": "ไซเรนฮัม", "sec": 30, "how_th": "ฮัมจากเสียงต่ำไปสูงแล้วกลับลง เหมือนไซเรน คอยผ่อน"},
    "hum_five": {"id": "wu03", "name_th": "ฮัมโด–ซอล", "sec": 20, "how_th": "ฮัมโน้ตหลักแล้วกระโดดขึ้นช่วงห้า แล้วกลับมา"},
    "vowel_slide": {"id": "wu04", "name_th": "ลากสระอี–อา", "sec": 20, "how_th": "เปลี่ยนจากสระอีเป็นอาบนโน้ตเดียว โดยไม่เกร็งคอ"},
}

PC = ["C","C#","D","Eb","E","F","F#","G","Ab","A","Bb","B"]
# Simple major / minor pitch-class sets from tonic
def _pcs(tonic, mode):
    i = PC.index(tonic)
    if mode == "major":
        steps = [0,2,4,5,7,9,11]
    elif mode == "minor":
        steps = [0,2,3,5,7,8,10]
    elif mode == "fifth":
        steps = [0,7]
    else:  # drone
        steps = [0]
    return {(PC[(i+s)%12]) for s in steps}


def pitch_score(mean_cents_off):
    if mean_cents_off is None:
        raise ValueError("mean_cents_off required")
    if mean_cents_off < 0:
        raise ValueError("mean_cents_off must be >= 0")
    return max(0, min(100, round(100 - 0.5 * mean_cents_off)))


def timing_score(mean_ms_off):
    if mean_ms_off is None:
        raise ValueError("mean_ms_off required")
    if mean_ms_off < 0:
        raise ValueError("mean_ms_off must be >= 0")
    return max(0, min(100, round(100 - 0.5 * mean_ms_off)))


def combined_score(pitch, timing):
    return int(round(0.6 * pitch + 0.4 * timing))


def score_take(take):
    if take.get("confidence", 1) < MIN_CONF:
        return {"ok": False, "pitch": None, "timing": None, "combined": None,
                "band": None, "message_th": "สัญญาณเสียงไม่ชัด ลองฮัมใหม่ในที่เงียบ"}
    p = pitch_score(take["mean_cents_off"])
    t = timing_score(take["mean_ms_off"])
    c = combined_score(p, t)
    if c >= 85:
        band, msg = "great", "ใกล้เคียงมาก คงจังหวะนี้ไว้"
    elif c >= 70:
        band, msg = "good", "ดีแล้ว เกลาเสียงให้นิ่งขึ้นอีกนิด"
    elif c >= 50:
        band, msg = "ok", "ผ่านเบื้องต้น ลองวอร์มอัพแล้วย้อนสเกลอีกครั้ง"
    else:
        band, msg = "try_again", "ยังหลุดค่อนข้างมาก ลองฮัมเบา ๆ ช้าลง"
    return {"ok": True, "pitch": p, "timing": t, "combined": c, "band": band,
            "cents": take["mean_cents_off"], "ms": take["mean_ms_off"],
            "exercise": take.get("exercise"),
            "headline_th": f"คะแนนรวม {c} · เสียง {p} · จังหวะ {t}",
            "message_th": msg, "disclaimer_th": SAFETY_DISCLAIMER_TH}


def key_finder(notes, hinted_exercise=None):
    clean = [n for n in notes if n in PC]
    if not clean:
        raise ValueError("no notes")
    # If an official exercise is hinted and notes are a subset of it, use that.
    if hinted_exercise:
        if hinted_exercise not in EXERCISES:
            raise ValueError("unknown exercise " + hinted_exercise)
        ex = EXERCISES[hinted_exercise]
        return {"tonic": ex["tonic"], "mode": ex["mode"], "exercise": hinted_exercise,
                "name_th": ex["name_th"], "notes": list(ex["notes"]),
                "headline_th": f"คีย์ {ex['tonic']} {ex['mode']} · {ex['name_th']}",
                "source": "exercise"}
    # Otherwise score tonic+mode by how many notes land in the scale.
    best = None
    for tonic in PC:
        for mode in ("major", "minor"):
            s = _pcs(tonic, mode)
            hit = sum(1 for n in clean if n in s)
            key = (hit, -len(s), tonic, mode)  # more hits better
            if best is None or key[:2] > best[:2] or (key[:2]==best[:2] and (tonic, mode) < (best[2], best[3])):
                # deterministic tie-break: higher hit, then tonic/mode name
                if best is None or hit > best[0] or (hit == best[0] and (tonic, mode) < (best[2], best[3])):
                    best = (hit, len(s), tonic, mode)
    tonic, mode = best[2], best[3]
    return {"tonic": tonic, "mode": mode, "exercise": None, "name_th": None,
            "notes": clean, "headline_th": f"คีย์โดยประมาณ {tonic} {mode}",
            "source": "notes", "hit": best[0], "total": len(clean)}


def warmups(keys=None):
    use = keys or list(WARMUPS)
    out = []
    total = 0
    for k in use:
        if k not in WARMUPS:
            raise ValueError("unknown warmup " + k)
        w = WARMUPS[k]
        total += w["sec"]
        out.append({"key": k, **w})
    return {"items": out, "count": len(out), "total_sec": total,
            "headline_th": f"วอร์มอัพ {len(out)} ท่า · {total} วินาที",
            "disclaimer_th": "วอร์มอัพเบา ๆ ถ้าเจ็บคอให้หยุด"}


def duet_battle(name_a, score_a, name_b, score_b):
    if score_a is None or score_b is None:
        raise ValueError("both scores required")
    if score_a == score_b:
        verdict, winner, msg = "tie", None, "เสมอกัน ทั้งคู่ฝึกต่อได้"
    elif score_a > score_b:
        verdict, winner, msg = "a", name_a, f"{name_a} นำ {score_a - score_b} แต้ม"
    else:
        verdict, winner, msg = "b", name_b, f"{name_b} นำ {score_b - score_a} แต้ม"
    return {"name_a": name_a, "score_a": score_a, "name_b": name_b, "score_b": score_b,
            "verdict": verdict, "winner": winner, "margin": abs(score_a - score_b),
            "headline_th": msg, "disclaimer_th": "เป็นการ์ดแข่งสนุกจากคะแนนฝึก ไม่ใช่การประกวดจริง"}


def practice_log(log, date, exercise, combined, feeling="ok"):
    if feeling not in ("easy", "ok", "hard", "stop"):
        raise ValueError("unknown feeling")
    if exercise not in EXERCISES:
        raise ValueError("unknown exercise " + exercise)
    row = {"date": date, "exercise": exercise, "name_th": EXERCISES[exercise]["name_th"],
           "combined": combined, "feeling": feeling}
    rows = list(log) + [row]
    best = max(r["combined"] for r in rows)
    return {"rows": rows, "count": len(rows), "best": best,
            "headline_th": f"ฝึก {len(rows)} ครั้ง · คะแนนดีสุด {best}"}


def share_card(name_th, result, key):
    return {"title_th": f"SingScore — {name_th}",
            "headline_th": result["headline_th"],
            "hook_th": "ร้องคาราโอเกะให้คะแนน + โค้ชเสียง",
            "combined": result["combined"], "pitch": result["pitch"], "timing": result["timing"],
            "key_th": key["headline_th"] if key else None,
            "layout": "sing_card", "sizes": ["1080x1350", "1080x1920", "1080x1080"],
            "watermark": WATERMARK, "cta_th": "คอมเมนต์ SING รับแพ็กฟรี"}


def quota(used_today, want, pro=False):
    if pro:
        return {"allowed": want, "left_after": None, "paywall": False}
    left = max(0, FREE_SCANS_PER_DAY - used_today)
    allowed = min(want, left)
    return {"allowed": allowed, "left_after": left - allowed, "paywall": allowed < want}


def safety_guard(sore_throat=False, strain=False):
    if sore_throat or strain:
        return {"level": "stop", "message_th": "หยุดร้องถ้าเจ็บคอหรือฝืนเสียง แล้วพักน้ำ " + SAFETY_DISCLAIMER_TH}
    return {"level": "ok", "message_th": SAFETY_DISCLAIMER_TH}
