"""Run: python3 tests.py — locks the demo numbers the Reel shows."""
import scam as S, fixtures as X
R = {m["id"]: S.scan(m["text"], m["sender"], m["channel"]) for m in X.INBOX}
def t_inbox_scores(): assert {k: v["score"] for k, v in R.items()} == {"m1": 90, "m2": 85, "m3": 55, "m4": 0}
def t_levels(): assert [R[k]["level"] for k in ("m1", "m2", "m3", "m4")] == ["scam", "scam", "risky", "low"]
def t_m1_flags(): assert [f["rule_id"] for f in R["m1"]["flags"]] == ["urgency", "credential", "link", "brand_mismatch", "bad_tld"]
def t_combo(): assert (R["m1"]["raw_score"], R["m1"]["combo_bonus"]) == (80, 10) and R["m3"]["combo_bonus"] == 0
def t_real_site(): assert R["m1"]["links"][0]["real_site"] == "kasikornbank.com" and R["m2"]["links"][0]["real_site"] == "thailandpost.co.th"
def t_shortener_hidden(): assert R["m3"]["links"][0]["verdict"] == "hidden"
def t_official(): x = S.link_xray("https://www.kasikornbank.com"); assert x["verdict"] == "official" and not x["flags"]
def t_ip_punycode():
    assert set(S.link_xray("http://192.168.10.5/scb")["flags"]) == {"no_https", "ip_link"}
    assert "punycode" in S.link_xray("https://xn--krngthai-ke9a.com/otp")["flags"]
def t_th_sld(): assert S.registered_domain("track.thailandpost.co.th") == "thailandpost.co.th" and S.registered_domain("a.b.kbank-x.top") == "kbank-x.top"
def t_highlights_no_overlap():
    for r in R.values():
        hs = r["highlights"]; assert all(a["end"] <= b["start"] for a, b in zip(hs, hs[1:]))
        assert all(r["text"][h["start"]:h["end"]] == h["text"] for h in hs)
def t_friend_safe(): assert R["m4"]["flags"] == [] and R["m4"]["actions"]["safe_reply_th"] is None
def t_quiz_engine_agrees():
    for c in X.QUIZ_DECK:
        s = S.scan(c["text"], c["sender"], c["channel"])["score"]
        assert (s >= 25) == (c["truth"] == "scam"), (c["id"], s)
def t_quiz_round():
    ids = S.quiz_round(X.QUIZ_DECK, X.QUIZ_SEED); assert ids == ["q08", "q06", "q01", "q02", "q04"]
    g = S.quiz_grade(X.QUIZ_DECK, ids, X.QUIZ_ANSWERS); assert (g["right"], g["badge_th"]) == (4, "👀 เกือบแล้ว")
def t_streak(): assert S.quiz_streak(X.QUIZ_DAYS) == 5 and S.quiz_streak(["2026-10-01", "2026-10-03"]) == 1
def t_call(): c = S.call_shield(X.CALL_TICKED); assert (c["score"], c["level"]) == (80, "scam")
def t_family_card():
    c = S.family_card(R["m1"], "มิ้นท์", "แม่"); assert c["title_th"] == "แม่ ระวังข้อความนี้นะ" and "90/100" in c["lines_th"][0]
def t_wrapped():
    h = X.HISTORY + [S.history_entry(R[i], X.TODAY) for i in ("m1", "m2", "m3", "m4")]
    w = S.shield_wrapped(h, "2026-10", X.QUIZ_DAYS)
    assert (w["checked"], w["flagged"], w["low"], w["top_rule_id"], w["most_faked_brand"], w["quiz_streak_days"]) == (8, 6, 2, "credential", "kbank", 5)
def t_score_capped(): assert S.scan("ด่วน OTP โอน คืนภาษี ตำรวจ แอดไลน์ กสิกร http://kbank-x.top bit.ly/a")["score"] == 100
if __name__ == "__main__":
    ts = [(k, v) for k, v in dict(globals()).items() if k.startswith("t_")]
    for k, f in ts: f()
    print(f"{len(ts)} tests passed")
