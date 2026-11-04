import json
R=lambda n:{"$ref":f"#/$defs/{n}"}
S={"type":"string"}; I={"type":"integer"}; N={"type":"number"}; B={"type":"boolean"}
def obj(props,req=None,extra=False,desc=None):
    o={"type":"object","properties":props,"required":req if req is not None else list(props.keys()),"additionalProperties":extra}
    if desc: o["description"]=desc
    return o
def arr(x,**k): return {"type":"array","items":x,**k}
def nul(x): return {"anyOf":[x,{"type":"null"}]}
D={}
D["Lang"]={"type":"string","enum":["th","en"]}
D["Quadrant"]={"type":"string","enum":["bright","calm","tense","low","neutral"],"description":"Valence × energy quadrant"}
D["WeatherKey"]={"type":"string","enum":["sunny","clear","cloudy","drizzle","storm"]}
D["ThemeKey"]={"type":"string","enum":["work","sleep","body","pet","friends","family","money","commute","exercise","food","love","self","feeling"]}
D["HexColor"]={"type":"string","pattern":"^#[0-9A-Fa-f]{6}$"}
D["DateLocal"]={"type":"string","pattern":"^\\d{4}-\\d{2}-\\d{2}$"}
D["DateTime"]={"type":"string","format":"date-time","pattern":"\\+07:00$|Z$"}
D["AiEngine"]={"type":"string","enum":["lexicon_v1","llm_api","template_v1"]}
D["SttEngine"]={"type":"string","enum":["web_speech","server_whisper","typed"]}
D["LexiconTerm"]=obj({"term":{"type":"string","minLength":1},"valence":{"type":"integer","minimum":-3,"maximum":3},
   "energy":{"type":"integer","minimum":-3,"maximum":3},"theme":R("ThemeKey")})
D["VoiceInput"]=obj({"id":S,"source":{"enum":["mic","upload","typed"]},"lang":{"enum":["th-TH","en-US"]},"started_at":R("DateTime"),
   "duration_sec":{"type":"integer","minimum":0,"maximum":180},"transcript_raw":{"type":"string","maxLength":2000},
   "transcript_edited":nul({"type":"string","maxLength":2000}),"interim_chunks":arr(S),"audio_kept":B,"stt_engine":R("SttEngine")},
   desc="One recording/typing session. Audio blob is NOT stored unless audio_kept=true (IndexedDB).")
D["MatchedTerm"]=obj({"term":S,"index":{"type":"integer","minimum":0},"valence":{"type":"integer","minimum":-3,"maximum":3},
   "energy":{"type":"integer","minimum":-3,"maximum":3},"theme":R("ThemeKey"),"negated":B})
D["Weather"]=obj({"key":R("WeatherKey"),"label_th":S,"emoji":S})
D["Aura"]=obj({"primary":R("HexColor"),"secondary":R("HexColor"),"glow_intensity":{"type":"number","minimum":0,"maximum":1},
   "motion":{"enum":["pulse_slow","swirl_fast"]}})
D["ThemeChip"]=obj({"key":R("ThemeKey"),"label_th":S,"emoji":S})
D["SafetyFlag"]=obj({"risk_level":{"enum":["none","elevated","urgent"]},"matched":arr(S)})
D["MoodAnalysis"]=obj({"entry_id":S,"engine":R("AiEngine"),"lexicon_version":S,"valence_sum":I,"energy_sum":I,
   "valence":{"type":"integer","minimum":-8,"maximum":8},"energy":{"type":"integer","minimum":0,"maximum":10},
   "score":{"type":"integer","minimum":0,"maximum":100},"quadrant":R("Quadrant"),"label_th":S,"weather":R("Weather"),
   "aura":R("Aura"),"themes":arr(R("ThemeChip")),"matched_terms":arr(R("MatchedTerm")),"summary_th":{"type":"string","maxLength":200},
   "safety":R("SafetyFlag")},desc="Output of lib/mood.ts (lexicon_v1) or LLM (llm_api, re-scored with same formulas).")
D["TinyAction"]=obj({"type":{"enum":["breathe","gratitude","rest","walk","message_friend","water","journal"]},"text_th":S,
   "minutes":{"type":"integer","minimum":1,"maximum":30},"cta_th":S})
D["ComfortCard"]=obj({"entry_id":S,"engine":R("AiEngine"),"quadrant":R("Quadrant"),"validate_th":{"type":"string","maxLength":140},
   "reframe_th":{"type":"string","maxLength":160},"tiny_action":R("TinyAction"),"alt_actions":arr(R("TinyAction"),maxItems=3),"disclaimer_th":S})
D["BreathSession"]=obj({"id":S,"entry_id":nul(S),"pattern":{"enum":["4-4-6","4-7-8","box_4"]},"cycles":{"type":"integer","minimum":1,"maximum":10},
   "duration_sec":I,"started_at":R("DateTime"),"completed":B,"orb_from":R("HexColor"),"orb_to":R("HexColor"),"haptics":B})
D["Recheck"]=obj({"before_entry_id":S,"after_entry_id":S,"input_after":R("VoiceInput"),"analysis_after":R("MoodAnalysis"),
   "before_score":I,"after_score":I,"delta":I,"caption_th":S},desc="Second short check-in after Comfort/Breathe. Self-report only.")
D["HistoryEntry"]=obj({"id":S,"date":R("DateLocal"),"created_at":R("DateTime"),"transcript":S,"score":{"type":"integer","minimum":0,"maximum":100},
   "energy":{"type":"integer","minimum":0,"maximum":10},"quadrant":R("Quadrant"),"weather_emoji":S,"themes":arr(R("ThemeKey")),"color":R("HexColor")},
   desc="Flattened MoodEntry for lists/garden. Full entry = VoiceInput + MoodAnalysis + ComfortCard.")
D["MoodEntry"]=obj({"id":S,"date":R("DateLocal"),"created_at":R("DateTime"),"input":R("VoiceInput"),"analysis":R("MoodAnalysis"),
   "comfort":nul(R("ComfortCard")),"breath_id":nul(S),"recheck_of":nul(S),"note":nul(S)},req=["id","date","created_at","input","analysis"])
D["GardenDay"]=obj({"date":R("DateLocal"),"entry_ids":arr(S),"score":nul({"type":"integer","minimum":0,"maximum":100}),
   "quadrant":nul(R("Quadrant")),"color":nul(R("HexColor")),"weather_emoji":nul(S)})
D["MoodGarden"]=obj({"month":{"type":"string","pattern":"^\\d{4}-\\d{2}$"},"style":{"enum":["orbs","flowers","pixels"]},"first_weekday":{"enum":["mon","sun"]},
   "days":arr(R("GardenDay"),minItems=28,maxItems=31),"filled_days":I,"streak_days":I})
D["TriggerInsight"]=obj({"theme":R("ThemeKey"),"label_th":S,"emoji":S,"entries_with":{"type":"integer","minimum":3},"entries_without":{"type":"integer","minimum":1},
   "avg_score_with":N,"avg_score_without":N,"delta":N,"direction":{"enum":["lifts","drains","neutral"]},"text_th":S})
D["TriggerReport"]=obj({"window":obj({"from":R("DateLocal"),"to":R("DateLocal")}),"entry_count":I,"min_entries_with":I,"insights":arr(R("TriggerInsight"))})
D["MoodWrapped"]=obj({"id":S,"period":obj({"from":R("DateLocal"),"to":R("DateLocal")}),"entries":I,"avg_score":N,"top_quadrant":R("Quadrant"),
   "quadrant_counts":{"type":"object","propertyNames":R("Quadrant"),"additionalProperties":I},
   "best_day":obj({"date":R("DateLocal"),"score":I}),"hardest_day":obj({"date":R("DateLocal"),"score":I}),
   "top_lift":R("TriggerInsight"),"top_drain":R("TriggerInsight"),"minutes_spoken":N,"streak_days":I,"slides_th":arr(S,minItems=3,maxItems=8)})
D["Gratitude"]=obj({"id":S,"date":R("DateLocal"),"items_th":arr({"type":"string","maxLength":80},minItems=1,maxItems=3),"created_at":R("DateTime")})
D["TimeCapsule"]=obj({"id":S,"created_at":R("DateTime"),"open_at":R("DateTime"),"text_th":S,"audio_kept":B,"opened":B})
D["Reminder"]=obj({"id":S,"enabled":B,"time_local":{"type":"string","pattern":"^\\d{2}:\\d{2}$"},
   "days":arr({"enum":["mon","tue","wed","thu","fri","sat","sun"]}),"text_th":S,"channel":{"enum":["web_push","local_notification"]}})
D["ShareCard"]=obj({"id":S,"entry_id":S,"variant":{"enum":["aura_story","garden_square","wrapped_story","duo_compare"]},
   "size":obj({"w":I,"h":I}),"show_transcript":B,"show_score":B,"show_themes":B,"headline_th":S,"sub_th":S,"after_badge_th":nul(S),
   "watermark_th":S,"colors":obj({"bg":R("HexColor"),"aura_1":R("HexColor"),"aura_2":R("HexColor")}),"file_name":S})
D["SupportResource"]=obj({"name_th":S,"phone":S,"hours_th":S,"verify_before_launch":B})
D["SafetyCheck"]=obj({"input_text":S,"risk_level":{"enum":["none","elevated","urgent"]},"matched":arr(S),
   "action":{"enum":["continue","soft_check_in","show_support_sheet"]},"message_th":S,"resources":arr(R("SupportResource"))},
   req=["input_text","risk_level","matched","action","resources"])
D["Settings"]=obj({"lang":R("Lang"),"stt_engine":R("SttEngine"),"ai_engine":{"enum":["lexicon_v1","llm_api"]},"keep_audio":B,"pin_lock":B,
   "reminder_id":nul(S),"sound":B,"haptics":B,"theme":{"enum":["night","dawn"]},"share_defaults":obj({"show_transcript":B,"show_score":B})})
D["LocalStore"]=obj({"version":{"const":1},"key":{"const":"voicemood:v1"},"settings":R("Settings"),"entry_ids":arr(S),"last_opened":R("DateTime"),
   "streak":obj({"current":I,"best":I,"last_date":R("DateLocal")})},desc="localStorage index. Entries themselves live in IndexedDB store 'entries'.")
D["AnalyticsEvent"]=obj({"event":{"enum":["app_open","demo_load","record_start","record_stop","analysis_done","comfort_view","breath_done","recheck_done",
   "garden_view","triggers_view","wrapped_view","share_card_export","safety_sheet_shown","settings_change"]},"ts":R("DateTime"),"props":{"type":"object"}})
D["FeatureItem"]=obj({"id":S,"name_th":S,"done":B})
D["FeatureChecklist"]=obj({"must_have":arr(R("FeatureItem"),minItems=5),"nice_to_have":arr(R("FeatureItem")),"min_features_rule":{"const":5},"must_count":{"type":"integer","minimum":5}})
D["ExamplesFile"]={"type":"object","description":"Shape of examples.json","required":["_meta","lexicon_th","analysis_example","history_entries","garden_example","trigger_insights_example"]}

SCHEMA={"$schema":"https://json-schema.org/draft/2020-12/schema","$id":"https://ai-wanla-app.example/voicemood/schemas.json",
 "title":"VoiceMood data contracts","description":"VoiceMood (AI วันละแอป Day 8/10, 2026-10-07). Types for lib/mood.ts, comfort, garden, triggers, wrapped, share, safety, storage.",
 "$defs":D}
json.dump(SCHEMA,open('../schemas.json','w'),ensure_ascii=False,indent=2)

# validate
from jsonschema import Draft202012Validator
ex=json.load(open('../examples.json'))
M={"lexicon_th":("LexiconTerm",True),"voice_input_example":("VoiceInput",False),"analysis_example":("MoodAnalysis",False),
 "comfort_card_example":("ComfortCard",False),"breath_session_example":("BreathSession",False),"recheck_example":("Recheck",False),
 "history_entries":("HistoryEntry",True),"garden_example":("MoodGarden",False),"trigger_insights_example":("TriggerReport",False),
 "mood_wrapped_example":("MoodWrapped",False),"gratitude_example":("Gratitude",False),"time_capsule_example":("TimeCapsule",False),
 "reminder_example":("Reminder",False),"share_card_example":("ShareCard",False),"safety_check_examples":("SafetyCheck",True),
 "settings_example":("Settings",False),"local_store_example":("LocalStore",False),"analytics_examples":("AnalyticsEvent",True),
 "feature_checklist_example":("FeatureChecklist",False)}
errs=0
for k,(d,isarr) in M.items():
    sch={"$schema":SCHEMA["$schema"],"$defs":D, **({"type":"array","items":R(d)} if isarr else R(d))}
    v=Draft202012Validator(sch)
    for e in v.iter_errors(ex[k]):
        errs+=1; print(k,list(e.path),e.message[:150])
print("defs",len(D),"errors",errs)
