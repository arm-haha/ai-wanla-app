# PoseMate (โพสท่าไม่เป็น) — ชุดส่งมอบเช้า (AI วันละแอป)

**วันที่:** 2026-10-23 (Asia/Bangkok) · **ช่อง:** AI วันละแอป · **สถานะ:** พร้อม gen วันนี้
**ฮุค Reel:** ไปคาเฟ่ทีไรยืนแข็งทุกที? ถ่ายฉาก 1 รูป AI ส่งท่ามาให้ 3 ท่า แล้วซ้อนเงาให้ยืนตาม รูปจาก 30 → 94

เดโมน้ำหวาน (สมมติ): ฉากริมหน้าต่างคาเฟ่ แสงหน้าต่าง 100 → การ์ด 3 ท่า (จิบกาแฟ / พิงขอบหน้าต่าง / เท้าคาง) → ยืนตามเงาพิงหน้าต่าง **65% → 94%** → Friend Mode "ระดับอก · 1x · 1.5 ม." → รูปก่อน **30** (ย้อนแสง เอียง 6° หัวโล่ง) → หลัง **94** ปังมาก 🔥 → แคปชันไทย 3 อัน → เสื้อครีมบนกำแพงครีม 16 จม vs สีอิฐ 64 เด้ง → ฟีด 9 ช่อง balance 90

## ไฟล์
| ไฟล์ | ใช้ทำอะไร |
|---|---|
| `prd.md` | ปัญหา ไวรัล persona 10 ฟีเจอร์ สูตรคอร์ หน้าจอ เทค ความเป็นส่วนตัว acceptance แผนวันเดียว |
| `prompts.md` | Prompt A–J (codegen ทั้งแอปทีละส่วน, QA, /reel-demo) + runtime K–M (อ่านฉาก, แคปชัน, แคปชัน Reel) |
| `schemas.json` | JSON Schema draft 2020-12, 25 defs (Pose, Scene, PoseCard, PoseMatch, AngleCoach, ShotScore, GlowUp, CaptionPack, GridPlan, OutfitPop, LocalStore, Ai*) |
| `examples.json` | คลังท่า 12 ท่า · preset มุมกล้อง · ฉาก · การ์ด · match ก่อน/หลัง · คะแนนก่อน/หลัง · glow-up · angle coach 3 แบบ · แคปชัน · grid · outfit pop · การ์ดกลุ่ม · ตัวอย่าง AI · UI copy ไทย · สคริปต์ Reel · expect_locked (validate 42 objects 0 error) |
| `reference/` | `posemate.py` (คอร์ deterministic) · `fixtures.py` · `schema.py` · `build.py` · `tests.py` (21 tests ผ่าน) |

ใช้งาน: วาง Prompt A + แนบ `prd.md`, `schemas.json`, `examples.json`, `reference/posemate.py` → ส่ง Prompt B–J ต่อทีละอัน
ตรวจซ้ำ: `cd reference && python3 build.py && python3 tests.py`

## ฟีเจอร์
**Must-have:** ① Spot Scan → Scene Read ② Pose Cards + Ghost Overlay (⭐ wow) ③ Angle Coach + Friend Mode ④ Shot Score + Glow-up Card ⑤ Caption Pack ไทย
**Nice-to-have:** ⑥ Outfit × Spot Pop ⑦ Group Pose 2–4 คน ⑧ Photo Dump Grid 9 ช่อง ⑨ Pose Library ⑩ Streak + History

## สี UI
`#FFF7EE` cream · `#1F1A2E` ink · `#FF6B5A` coral · `#FFB347` sunset · `#B8A4FF` lavender · `#3DDC97` mint · `#7DF9FF` ghost · `#F43F5E` warn

## กับดัก
- **Pose tracking กระตุก/แสงน้อย:** รัน MediaPipe บนเครื่อง ลดเฟรมวิเคราะห์เหลือ ~7fps แต่กล้องลื่น ถ้าหา landmarks ไม่เจอ ให้ใช้การ์ด cue อย่างเดียว
- **คะแนนรูป = เรื่องอ่อนไหว:** วัดแค่มุมกล้อง/องค์ประกอบ ห้ามคะแนนหน้าตา หุ่น สีผิว ไม่มีฟิลเตอร์ปรับหุ่น
- **ความเป็นส่วนตัว:** รูปคนไม่ออกจากเครื่อง ส่งแค่รูปฉากเปล่า
- **ท่าซ้ำจนเบื่อ:** คลังท่าต้องโตได้ (JSON) อัปเดตท่าใหม่ตามเทรนด์เป็นคอนเทนต์ต่อเนื่อง
- **ความปลอดภัย:** ไม่แนะนำท่าริมที่สูง/กลางถนน ใส่คำเตือนในจุดเสี่ยง
- **ร้าน/สถานที่จริงในคลิป:** ขออนุญาตร้านก่อนถ่าย ชื่อร้านในเดโมเป็นร้านสมมติ

> บุคคล ร้าน และตัวเลขในเดโมทั้งหมดเป็นตัวอย่างสมมติ
