import json, math
from mood import analyze, LEXICON, QUAD, jsround
from history import HISTORY

TZ="+07:00"
def iso(d,t): return f"{d}T{t}:00{TZ}"
THEME_TH={"work":"งาน","sleep":"การนอน","body":"ร่างกาย","pet":"สัตว์เลี้ยง","friends":"เพื่อน","family":"ครอบครัว",
 "money":"เงิน","commute":"การเดินทาง","exercise":"ออกกำลังกาย","food":"ของกิน","love":"แฟน/ความรัก","self":"ตัวเอง","feeling":"ความรู้สึก"}
THEME_EMOJI={"work":"💼","sleep":"😴","body":"🫀","pet":"🐱","friends":"🫂","family":"🏠","money":"💸","commute":"🚗",
 "exercise":"🏃","food":"🍜","love":"💗","self":"🪞","feeling":"💭"}

def entry_id(i): return f"vm_{i+1:03d}"
entries=[]
for i,(d,t,x) in enumerate(HISTORY):
    a=analyze(x)
    entries.append({"id":entry_id(i),"date":d,"created_at":iso(d,t),"text":x,"a":a})

def analysis_obj(e, summary=None, engine="lexicon_v1"):
    a=e["a"]
    return {
      "entry_id":e["id"],"engine":engine,"lexicon_version":"th-2026.10",
      "valence_sum":a["valence_sum"],"energy_sum":a["energy_sum"],
      "valence":a["valence"],"energy":a["energy"],"score":a["score"],
      "quadrant":a["quadrant"],"label_th":a["label_th"],"weather":a["weather"],
      "aura":{"primary":a["aura"]["primary"],"secondary":a["aura"]["secondary"],"glow_intensity":round(min(1,0.35+abs(a["valence"])/8*0.65),2),
              "motion":"pulse_slow" if a["energy"]<6 else "swirl_fast"},
      "themes":[{"key":k,"label_th":THEME_TH[k],"emoji":THEME_EMOJI[k]} for k in a["themes"]],
      "matched_terms":[{k:m[k] for k in ("term","index","valence","energy","theme","negated")} for m in a["matched_terms"]],
      "summary_th": summary or "",
      "safety":{"risk_level":"none","matched":[]}
    }

# day aggregation
from collections import OrderedDict
days=OrderedDict()
for e in entries: days.setdefault(e["date"],[]).append(e)
def day_obj(d,es):
    return {"date":d,"entry_ids":[e["id"] for e in es],"score":jsround(sum(e["a"]["score"] for e in es)/len(es)),
            "quadrant":es[-1]["a"]["quadrant"],"color":es[-1]["a"]["aura"]["primary"],"weather_emoji":es[-1]["a"]["weather"]["emoji"]}

# triggers
def triggers(es, min_with=3):
    out=[]
    allt=[]
    for e in es:
        for th in e["a"]["themes"]:
            if th not in allt: allt.append(th)
    for th in allt:
        w=[e["a"]["score"] for e in es if th in e["a"]["themes"]]
        wo=[e["a"]["score"] for e in es if th not in e["a"]["themes"]]
        if len(w)<min_with or len(wo)<1: continue
        aw=round(sum(w)/len(w),1); awo=round(sum(wo)/len(wo),1); delta=round(sum(w)/len(w)-sum(wo)/len(wo),1)
        out.append({"theme":th,"label_th":THEME_TH[th],"emoji":THEME_EMOJI[th],"entries_with":len(w),"entries_without":len(wo),
                    "avg_score_with":aw,"avg_score_without":awo,"delta":delta,
                    "direction":"lifts" if delta>=5 else ("drains" if delta<=-5 else "neutral")})
    out.sort(key=lambda x:-abs(x["delta"]))
    return out
trig=triggers(entries)
def trig_text(t):
    n=jsround(abs(t["delta"]))
    if t["direction"]=="lifts": return f"วันที่มีเรื่อง{t['label_th']} {t['emoji']} ใจคุณดีกว่าปกติ +{n} คะแนน"
    if t["direction"]=="drains": return f"วันที่มีเรื่อง{t['label_th']} {t['emoji']} ใจคุณต่ำกว่าปกติ −{n} คะแนน"
    return f"เรื่อง{t['label_th']} {t['emoji']} ไม่ค่อยเปลี่ยนอารมณ์คุณ"
for t in trig: t["text_th"]=trig_text(t)

demo_before=entries[13]; demo_after=entries[14]
SUM_BEFORE="วันนี้งานกดดันหนัก ทั้งประชุมด่วนและงานโดนแก้ซ้ำ บวกรถติดจนหมดแรง แต่ช่วงท้ายมีแมวช่วยให้ใจเบาลงนิดหนึ่ง"
SUM_AFTER="หลังหายใจช้าๆ คุณบอกว่าสบายใจขึ้น และขอบคุณตัวเองที่ผ่านวันนี้มาได้"

lex=[{"term":t,"valence":v,"energy":e,"theme":th} for t,v,e,th in LEXICON]

ex={}
ex["_meta"]={"app":"VoiceMood","pack_date":"2026-10-07","timezone":"Asia/Bangkok","channel":"AI วันละแอป","day":"8/10",
  "note_th":"ข้อมูลทั้งหมดเป็นตัวละครสมมติ ('น้ำหวาน' + แมว 'ข้าวตู') คะแนนทุกตัวคำนวณซ้ำด้วยกติกา lexicon_v1 (prd.md §8) แล้วตรงกัน",
  "verified":{"schema_errors":0,"rules_recomputed":True}}
ex["demo_persona"]={"nickname":"น้ำหวาน","age_band":"25-29","job_th":"กราฟิกดีไซเนอร์ออฟฟิศ กรุงเทพฯ","pet_name":"ข้าวตู","fictional":True}
ex["lexicon_th"]=lex
ex["mood_rules"]={
  "match":"เรียง term ยาวไปสั้น หา occurrence แรกที่ไม่ทับช่วงที่ใช้ไปแล้ว นับครั้งเดียวต่อ term",
  "negation":"ถ้า 3 ตัวอักษรก่อน term คือ 'ไม่' และ term ไม่ได้ขึ้นต้นด้วย 'ไม่' → valence กลับเครื่องหมาย, energy = 0",
  "valence":"v = clamp(Σvalence, -8, 8)","energy":"energy = round((clamp(Σenergy, -8, 8) + 8) / 16 * 10)  // 0–10",
  "score":"score = round((v + 8) / 16 * 100)  // 0–100, round = floor(x + 0.5)",
  "quadrant":"v == 0 → neutral · v > 0 → (energy ≥ 6 ? bright : calm) · v < 0 → (energy ≥ 6 ? tense : low)",
  "weather":[{"min":80,"key":"sunny","emoji":"☀️","label_th":"แดดจ้า"},{"min":60,"key":"clear","emoji":"⛅","label_th":"ฟ้าโปร่ง"},
             {"min":41,"key":"cloudy","emoji":"☁️","label_th":"เมฆครึ้ม"},{"min":21,"key":"drizzle","emoji":"🌧️","label_th":"ฝนพรำ"},
             {"min":0,"key":"storm","emoji":"⛈️","label_th":"พายุเข้า"}],
  "quadrant_palette":{k:{"label_th":v[0],"primary":v[1],"secondary":v[2]} for k,v in QUAD.items()},
  "themes":"themes = theme ของ term ที่เจอ (ไม่รวม feeling) เรียงตามตำแหน่งแรกที่เจอ ไม่ซ้ำ",
  "day":"คะแนนวัน = round(ค่าเฉลี่ย score ทุก entry ของวันนั้น) · สีวัน = quadrant ของ entry ล่าสุด",
  "triggers":"สำหรับแต่ละ theme ที่มี entries_with ≥ 3 และ entries_without ≥ 1: delta = avg(score ที่มี theme) − avg(score ที่ไม่มี) · ≥ +5 lifts · ≤ −5 drains · เรียงตาม |delta|",
  "safety_first":"ตรวจ safety_terms ก่อนทุกอย่าง ถ้าเจอ → ไม่คำนวณคะแนน ไม่โชว์อากาศ ไม่ให้แชร์ เปิด Support Sheet"
}
ex["voice_input_example"]={"id":"in_014","source":"mic","lang":"th-TH","started_at":iso("2026-10-07","19:47"),"duration_sec":28,
  "transcript_raw":demo_before["text"],"transcript_edited":None,"interim_chunks":[
   "วันนี้หัวหน้าเรียกประชุมด่วน","ตอนห้าโมงเย็น งานโดนแก้รอบที่สามแล้ว","เหนื่อยมาก รถติดอีก","กลับถึงห้องก็ไม่อยากทำอะไรเลย","แต่พอแมวมานอนตักก็ดีขึ้นนิดนึง"],
  "audio_kept":False,"stt_engine":"web_speech"}
ex["analysis_example"]=analysis_obj(demo_before,SUM_BEFORE)
ex["comfort_card_example"]={"entry_id":demo_before["id"],"engine":"template_v1","quadrant":"low",
  "validate_th":"วันแบบนี้ใครเจอก็หมดแรง งานโดนแก้ซ้ำๆ ไม่ได้แปลว่าคุณทำได้ไม่ดี",
  "reframe_th":"คุณยังเห็นช่วงเล็กๆ ที่ใจเบาลงตอนข้าวตูมานอนตัก แปลว่าคุณยังมีที่พักใจอยู่",
  "tiny_action":{"type":"breathe","text_th":"หายใจตามวงกลม 60 วินาที","minutes":1,"cta_th":"เริ่มหายใจ"},
  "alt_actions":[{"type":"gratitude","text_th":"เขียน 3 อย่างเล็กๆ ที่ยังดีวันนี้","minutes":2,"cta_th":"เขียนเลย"},
                 {"type":"rest","text_th":"วางมือถือ ไปอาบน้ำอุ่นก่อนนอน","minutes":15,"cta_th":"โอเค"}],
  "disclaimer_th":"VoiceMood เป็นสมุดบันทึกอารมณ์ ไม่ใช่การวินิจฉัยทางการแพทย์"}
ex["breath_session_example"]={"id":"br_007","entry_id":demo_before["id"],"pattern":"4-4-6","cycles":4,"duration_sec":56,
  "started_at":iso("2026-10-07","19:49"),"completed":True,"orb_from":"#818CF8","orb_to":"#34D399","haptics":True}
ex["recheck_example"]={"before_entry_id":demo_before["id"],"after_entry_id":demo_after["id"],"input_after":{
   "id":"in_015","source":"mic","lang":"th-TH","started_at":iso("2026-10-07","19:51"),"duration_sec":9,"transcript_raw":demo_after["text"],
   "transcript_edited":None,"interim_chunks":[demo_after["text"]],"audio_kept":False,"stt_engine":"web_speech"},
  "analysis_after":analysis_obj(demo_after,SUM_AFTER),
  "before_score":demo_before["a"]["score"],"after_score":demo_after["a"]["score"],
  "delta":demo_after["a"]["score"]-demo_before["a"]["score"],
  "caption_th":f"ก่อน {demo_before['a']['score']} {demo_before['a']['weather']['emoji']} → หลัง {demo_after['a']['score']} {demo_after['a']['weather']['emoji']} (จากคำที่คุณเล่าเอง)"}

# history entries
hist=[]
summ={}
for e in entries:
    hist.append({"id":e["id"],"date":e["date"],"created_at":e["created_at"],"transcript":e["text"],
      "score":e["a"]["score"],"energy":e["a"]["energy"],"quadrant":e["a"]["quadrant"],"weather_emoji":e["a"]["weather"]["emoji"],
      "themes":e["a"]["themes"],"color":e["a"]["aura"]["primary"]})
ex["history_entries"]=hist

# garden Oct
import calendar
oct_days=[]
for dnum in range(1,32):
    d=f"2026-10-{dnum:02d}"
    if d in days: oct_days.append(day_obj(d,days[d]))
    else: oct_days.append({"date":d,"entry_ids":[],"score":None,"quadrant":None,"color":None,"weather_emoji":None})
ex["garden_example"]={"month":"2026-10","style":"orbs","first_weekday":"mon","days":oct_days,
  "filled_days":sum(1 for x in oct_days if x["entry_ids"]),"streak_days":14}
ex["trigger_insights_example"]={"window":{"from":"2026-09-24","to":"2026-10-07"},"entry_count":len(entries),"min_entries_with":3,"insights":trig}
week=[e for e in entries if e["date"]>="2026-10-01"]
wk_scores=[e["a"]["score"] for e in week]
from collections import Counter
qc=Counter(e["a"]["quadrant"] for e in week)
best=max(week,key=lambda e:e["a"]["score"]); worst=min(week,key=lambda e:e["a"]["score"])
ex["mood_wrapped_example"]={"id":"wr_2026w40","period":{"from":"2026-10-01","to":"2026-10-07"},"entries":len(week),
  "avg_score":round(sum(wk_scores)/len(wk_scores),1),"top_quadrant":qc.most_common(1)[0][0],"quadrant_counts":dict(qc),
  "best_day":{"date":best["date"],"score":best["a"]["score"]},"hardest_day":{"date":worst["date"],"score":worst["a"]["score"]},
  "top_lift":next(t for t in trig if t["direction"]=="lifts"),"top_drain":next(t for t in trig if t["direction"]=="drains"),
  "minutes_spoken":round(sum([30,26,24,32,28,26,28,9])/60,1),"streak_days":14,
  "slides_th":[f"สัปดาห์นี้คุณเล่าเรื่องใจ {len(week)} ครั้ง","สีที่เจอบ่อยสุด: สดใส มีพลัง 💛",f"วันที่ใจฟูสุด: {int(best['date'][-2:])} ต.ค. ({best['a']['score']} ⛅)","สิ่งที่ชาร์จใจคุณ: ออกกำลังกาย 🏃","สิ่งที่ดูดพลัง: งาน 💼","สตรีค 14 วัน 🔥 เก่งมาก"]}
ex["gratitude_example"]={"id":"gr_007","date":"2026-10-07","items_th":["ข้าวตูมานอนตัก","ได้กลับห้องแล้ว","พรุ่งนี้วันพฤหัส อีกนิดเดียว"],"created_at":iso("2026-10-07","19:53")}
ex["time_capsule_example"]={"id":"tc_001","created_at":iso("2026-10-07","19:55"),"open_at":"2027-01-07T20:00:00+07:00",
  "text_th":"ถึงน้ำหวานอีก 3 เดือนข้างหน้า วันนี้เหนื่อยมาก แต่เราผ่านมาได้นะ","audio_kept":False,"opened":False}
ex["reminder_example"]={"id":"rm_01","enabled":True,"time_local":"21:30","days":["mon","tue","wed","thu","fri","sat","sun"],
  "text_th":"วันนี้ใจคุณสีอะไร? พูดสัก 30 วิ 🎙️","channel":"web_push"}
ex["share_card_example"]={"id":"sc_014","entry_id":demo_before["id"],"variant":"aura_story","size":{"w":1080,"h":1920},
  "show_transcript":False,"show_score":True,"show_themes":True,"headline_th":"ใจฉันวันนี้ 🌧️ ฝนพรำ","sub_th":"หม่น เหนื่อยล้า · แต่มีแมวช่วย 🐱",
  "after_badge_th":"หายใจ 1 นาที → ⛅ 75","watermark_th":"VoiceMood · AI วันละแอป","colors":{"bg":"#14112B","aura_1":"#818CF8","aura_2":"#34D399"},
  "file_name":"voicemood_2026-10-07.png"}
SAFETY_TERMS=["อยากตาย","ไม่อยากอยู่แล้ว","ฆ่าตัวตาย","ทำร้ายตัวเอง","จบชีวิต"]
RES=[{"name_th":"สายด่วนสุขภาพจิต กรมสุขภาพจิต","phone":"1323","hours_th":"24 ชั่วโมง ฟรี","verify_before_launch":True},
     {"name_th":"เจ็บป่วยฉุกเฉิน (สพฉ.)","phone":"1669","hours_th":"24 ชั่วโมง","verify_before_launch":True}]
ex["safety_terms_th"]=SAFETY_TERMS
ex["safety_check_examples"]=[
  {"input_text":demo_before["text"],"risk_level":"none","matched":[],"action":"continue","resources":[]},
  {"input_text":"(ตัวอย่างทดสอบ) เหนื่อยจนไม่อยากอยู่แล้ว","risk_level":"urgent","matched":["ไม่อยากอยู่แล้ว"],"action":"show_support_sheet",
   "message_th":"ขอบคุณที่เล่าให้ฟังนะ ตอนนี้คุณไม่ต้องอยู่กับความรู้สึกนี้คนเดียว คุยกับคนที่พร้อมรับฟังได้เลย","resources":RES}]
ex["settings_example"]={"lang":"th","stt_engine":"web_speech","ai_engine":"lexicon_v1","keep_audio":False,"pin_lock":False,
  "reminder_id":"rm_01","sound":True,"haptics":True,"theme":"night","share_defaults":{"show_transcript":False,"show_score":True}}
ex["local_store_example"]={"version":1,"key":"voicemood:v1","settings":ex["settings_example"],
  "entry_ids":[e["id"] for e in entries],"last_opened":iso("2026-10-07","19:56"),"streak":{"current":14,"best":14,"last_date":"2026-10-07"}}
ex["analytics_examples"]=[
  {"event":"record_start","ts":iso("2026-10-07","19:47"),"props":{"source":"mic"}},
  {"event":"analysis_done","ts":iso("2026-10-07","19:48"),"props":{"engine":"lexicon_v1","score":25,"quadrant":"low","ms":2600}},
  {"event":"breath_done","ts":iso("2026-10-07","19:50"),"props":{"duration_sec":56}},
  {"event":"recheck_done","ts":iso("2026-10-07","19:51"),"props":{"delta":50}},
  {"event":"share_card_export","ts":iso("2026-10-07","19:54"),"props":{"variant":"aura_story","show_transcript":False}}]
ex["feature_checklist_example"]={"must_have":[
  {"id":"voice_to_aura","name_th":"Voice Vent → Mood Aura","done":True},
  {"id":"comfort_card","name_th":"Comfort Card + หายใจ 60 วิ + เช็กใจอีกรอบ","done":True},
  {"id":"mood_garden","name_th":"Mood Garden ปฏิทินลูกแก้วอารมณ์","done":True},
  {"id":"triggers","name_th":"Mood Triggers อะไรชาร์จ/ดูดพลัง","done":True},
  {"id":"share_card","name_th":"Share Aura Card (ซ่อนข้อความค่าเริ่ม)","done":True}],
 "nice_to_have":[{"id":"mood_wrapped","name_th":"Mood Wrapped รายสัปดาห์","done":False},{"id":"gratitude","name_th":"ขอบคุณ 3 อย่าง","done":False},
  {"id":"time_capsule","name_th":"จดหมายถึงตัวเองในอนาคต","done":False},{"id":"reminder","name_th":"เตือนเช็กใจ 21:30","done":False},
  {"id":"pin_lock","name_th":"ล็อก PIN","done":False},{"id":"typed_mode","name_th":"โหมดพิมพ์แทนพูด","done":False},{"id":"export_txt","name_th":"ส่งออกบันทึก .txt","done":False}],
 "min_features_rule":5,"must_count":5}
ex["ui_copy_th"]={
 "home_title":"วันนี้ใจคุณสีอะไร?","home_sub":"กดค้าง แล้วเล่าให้ฟังสัก 30 วิ","mic_hold":"กดค้างเพื่อพูด","mic_listening":"กำลังฟังอยู่นะ…",
 "mic_denied":"ยังไม่ได้อนุญาตไมค์ — พิมพ์เล่าแทนได้เลย","analyzing":"กำลังอ่านสีใจคุณ…","result_score":"คะแนนใจวันนี้",
 "score_note":"คะแนนจากคำที่คุณเล่าเอง ไม่ใช่การวัดทางการแพทย์","breathe_cta":"หายใจตามวงกลม 60 วิ","breathe_in":"หายใจเข้า…","breathe_hold":"ค้างไว้…","breathe_out":"ผ่อนออกช้าๆ…",
 "recheck_cta":"เช็กใจอีกรอบ","garden_title":"สวนอารมณ์เดือนนี้","triggers_title":"อะไรชาร์จใจ / ดูดพลังคุณ","triggers_need_more":"เล่าอีก {n} วัน แอปจะเริ่มเห็นแพทเทิร์น",
 "share_cta":"แชร์สีใจวันนี้","share_privacy":"ข้อความที่พูดจะไม่ถูกใส่ในการ์ด (เปิดได้ถ้าต้องการ)","demo_cta":"ลองข้อมูลตัวอย่าง (น้ำหวาน)",
 "privacy_badge":"เก็บในเครื่องคุณเท่านั้น · ไม่เก็บไฟล์เสียง","disclaimer":"VoiceMood เป็นสมุดบันทึกอารมณ์ ไม่ใช่การวินิจฉัยหรือการรักษา",
 "support_title":"คุณไม่ได้อยู่คนเดียวนะ","support_call":"โทร 1323 (สายด่วนสุขภาพจิต)","nav":["เล่า","สวนอารมณ์","แพทเทิร์น","ตั้งค่า"]}
ex["reel_script_th"]={"length_sec":30,"caption_th":"พูดระบายแค่ 30 วิ… AI บอกว่าวันนี้ใจคุณสีอะไร 🔮 คอมเมนต์ \"สีใจ\" รับลิงก์ฟรี",
 "shots":[
  {"t":"0-3","shot":"หน้าตรง เหนื่อยๆ ในห้องมืด ถือมือถือ","overlay":"วันนี้ใจฉันสีอะไร?","audio":"ถอนหายใจ"},
  {"t":"3-6","shot":"หน้าจอโค้ด/AI gen แอป speed-ramp","overlay":"ให้ AI สร้างแอปให้ใน 1 คืน","audio":"beat drop"},
  {"t":"6-12","shot":"กดค้างไมค์ พูดเรื่องวันนี้ คำลอยขึ้นเป็นตัวหนังสือ วงคลื่นเต้น","overlay":"เล่าให้ฟัง 30 วิ","audio":"เสียงพูดจริง (ข้อมูลน้ำหวาน)"},
  {"t":"12-16","shot":"คำถูกดูดเข้าลูกแก้ว → ลูกแก้วเปลี่ยนเป็นสีม่วงฟ้า + 🌧️ 25","overlay":"วันนี้ใจคุณ: ฝนพรำ 🌧️","audio":"whoosh + ding"},
  {"t":"16-21","shot":"Comfort Card เลื่อนขึ้น → หายใจตามลูกแก้วที่พองยุบ → เช็กใจอีกรอบ 25 → 75 ⛅ สีเปลี่ยนเป็นเขียวมิ้นต์","overlay":"หายใจ 1 นาที ใจเปลี่ยนสี","audio":"chime"},
  {"t":"21-25","shot":"สวนอารมณ์ 14 วัน ลูกแก้วสีๆ เด้งเรียงทีละวัน → การ์ดแพทเทิร์น 'ออกกำลังกาย +17 · งาน −21'","overlay":"แอปรู้ว่าอะไรชาร์จใจคุณ","audio":"pop pop pop"},
  {"t":"25-30","shot":"การ์ดแชร์สตอรี่ aura สวยๆ + โลโก้ช่อง","overlay":"คอมเมนต์ \"สีใจ\" รับลิงก์ฟรี","audio":"outro"}]}
ex["alt_reel_ideas_th"]=["ให้แฟน/เพื่อนพูดแล้วเทียบสีใจกัน 2 คน","เช็กใจทุกคืน 7 วันแล้วเปิด Mood Wrapped ตอนจบ","พูดเรื่องเดียวกันแบบบ่น vs แบบมองบวก แล้วดูสีเปลี่ยน","สวนอารมณ์ทั้งเดือนตุลา time-lapse"]

from mood import analyze as _an
ex["unit_test_vectors"]=[{"text":t,"expect":{k:_an(t)[k] for k in ("score","energy","quadrant","valence_sum","energy_sum")}} for t in ["วันนี้ไม่สบายใจเลย","วันนี้กินข้าวแล้ว","วันนี้เหนื่อยมากแต่ดีใจที่ได้เจอเพื่อน"]]
json.dump(ex,open('../examples.json','w'),ensure_ascii=False,indent=2)
print(json.dumps({k:ex[k] for k in ["recheck_example"]},ensure_ascii=False)[:300])
print([ (t["theme"],t["delta"],t["direction"]) for t in trig])
print(ex["mood_wrapped_example"]["avg_score"],ex["mood_wrapped_example"]["top_quadrant"],ex["mood_wrapped_example"]["quadrant_counts"],ex["mood_wrapped_example"]["best_day"],len(week))
