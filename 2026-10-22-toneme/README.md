# ToneMe (สีไหนใช่เรา) — ชุดส่งมอบเช้า (AI วันละแอป)

**วันที่:** 2026-10-22 (Asia/Bangkok) · **ช่อง:** AI วันละแอป · **สถานะ:** พร้อม gen วันนี้
**ฮุค Reel:** ใส่ชมพูแล้วหน้าโทรม? เซลฟี่ 10 วิ AI บอกว่าเราเป็นซีซั่นสีไหน แล้วทาบผ้าให้ดูกันจะจะ ส้ม 96 vs ชมพู 0

เดโมมายด์ (สมมติ): เซลฟี่ + quiz → **True Autumn 🍂** (warmth 21 · lightness 48 · contrast 59 · มั่นใจ 78%) → Drape ส้มฟักทอง **96** vs ชมพูบาร์บี้ **0** → ชุดวันนี้ 50 → เปลี่ยนเสื้อเป็นเทียล **96** → ลิปโทนอิฐ → สแกนเสื้อเทียลในร้าน 91 ใช่ → ตู้เสื้อผ้าเข้ากับเรา 50% → แก๊ง 4 คนได้สีกลาง ครีมอูฐ 85

## ไฟล์
| ไฟล์ | ใช้ทำอะไร |
|---|---|
| `prd.md` | ปัญหา ไวรัล persona 10 ฟีเจอร์ สูตรคอร์ หน้าจอ เทค ความเป็นส่วนตัว acceptance แผนวันเดียว |
| `prompts.md` | Prompt A–J (codegen ทั้งแอปทีละส่วน, QA, /reel-demo) + runtime K–M (vision หา region, stylist caption, แคปชัน Reel) |
| `schemas.json` | JSON Schema draft 2020-12, 28 defs (ScanSample, Profile, DrapeBattle, PaletteCard, OutfitCheck, Makeup, ShopScan, ClosetAudit, FriendCompare, LocalStore, Ai*) |
| `examples.json` | พาเลตต์ 4 ซีซั่น (12 ใช่ + 4 เลี่ยง) · profile มายด์ + ตัวอย่าง 5 ซีซั่นย่อย · drape · การ์ด · ชุดก่อน/หลัง · makeup · shop · closet · hair · แก๊ง · ตัวอย่าง AI · UI copy ไทย · สคริปต์ Reel · expect_locked (validate 21 objects 0 error) |
| `reference/` | `toneme.py` (คอร์ deterministic) · `fixtures.py` · `schema.py` · `build.py` · `tests.py` (23 tests ผ่าน) |

ใช้งาน: วาง Prompt A + แนบ `prd.md`, `schemas.json`, `examples.json`, `reference/toneme.py` → ส่ง Prompt B–J ต่อทีละอัน
ตรวจซ้ำ: `cd reference && python3 build.py && python3 tests.py`

## ฟีเจอร์
**Must-have:** ① Selfie Tone Scan → Season Reveal ② Drape Battle A/B (⭐ wow) ③ Palette Card วอลเปเปอร์ ④ Outfit Check + สีแนะนำ ⑤ Makeup Shade Finder
**Nice-to-have:** ⑥ Shop Scan ในร้าน ⑦ Closet Audit ⑧ Hair Color Guide ⑨ Friend Group Color ⑩ AI Stylist Caption

## สี UI
`#FBF7F2` linen · `#2B2238` ink · `#E8879B` rose · `#F6B48F` peach · `#8FB8A0` sage · `#8DB6E8` sky · `#D4A64A` gold · `#E5484D` no

## กับดัก
- **แสง/กล้องเพี้ยน = ผลเพี้ยน:** บังคับ light check, แนะนำแสงหน้าต่าง ไม่แต่งหน้า ปิดฟิลเตอร์ ถ้าไม่ผ่านไม่ให้ผล
- **ประเด็นสีผิว (colorism):** ห้ามคำ "ผิวขาวดีกว่า" ไม่มีฟิลเตอร์ทำผิวขาว ย้ำว่าทุกโทนสวยในสีของตัวเอง
- **ช่างดูสีตัวจริงแย้ง:** วางตัวเป็น "ไกด์สนุกๆ ฉบับเร็ว" ไม่ใช่การวิเคราะห์มืออาชีพ ผลก้ำกึ่งบอกตรงๆ
- **เซลฟี่ = ข้อมูลชีวมิติ:** อ่านสีแล้วลบทันที ไม่เก็บรูป ไม่ส่งรูปเพื่อน
- **สีจอไม่ตรงผ้าจริง:** บอกให้เทียบกับผ้าจริงในแสงกลางวันก่อนซื้อ
- **ชื่อแบรนด์เครื่องสำอาง:** ให้แค่กลุ่มสี + hex เลี่ยงการรับรองสินค้า

> บุคคล ประวัติ และตัวเลขในเดโมทั้งหมดเป็นตัวอย่างสมมติ
