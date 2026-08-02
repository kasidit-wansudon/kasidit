# Locale / i18n Correctness Checklist

## Encoding
- [ ] I/O boundary (DB connection, HTTP response, file read/write) ประกาศ UTF-8 ชัดเจน ไม่ปล่อยให้ default ของ driver/OS ตัดสิน
- [ ] ทดสอบด้วยข้อความที่มี multi-byte / emoji / combining characters (ภาษาไทยมีสระ/วรรณยุกต์ซ้อน) ผ่าน round-trip เก็บ-อ่านโดยไม่เพี้ยน
- [ ] ความยาวสตริงที่ใช้ตัดคำ/truncate นับหน่วยถูกต้อง (grapheme cluster ไม่ใช่ byte หรือ UTF-16 code unit) — ตัดกลางสระไทย/emoji แล้วเพี้ยน

## การเรียงลำดับ (Collation)
- [ ] เรียงชื่อ/คำภาษาไทยด้วย locale-aware collation ไม่ใช่ byte-order เปรียบเทียบตรง (ผลลัพธ์เพี้ยนจากที่คนไทยคาดหวัง)
- [ ] เปรียบเทียบสตริงแบบ case-insensitive คำนึงถึง locale (ตัวอย่างคลาสสิก: ตุรกี `I`/`ı` เพี้ยนถ้าใช้ default locale)

## ตัวเลข / วันที่ / สกุลเงินตามภาษา
- [ ] ตัวคั่นทศนิยม/หลักพัน format ตาม locale ผู้ใช้ (`1,234.56` vs `1.234,56`) ไม่ hardcode
- [ ] รูปแบบวันที่แสดงผลตาม locale (DD/MM vs MM/DD) แยกจากรูปแบบที่เก็บใน DB (ต้องเก็บเป็น ISO 8601 เสมอ ดู [[correctness-datetime]])
- [ ] ปีพ.ศ./ค.ศ. ถ้า UI แสดงปีพ.ศ. ต้อง convert ที่ display layer เท่านั้น ไม่ปนกับค่าที่คำนวณ/เก็บ

## RTL (ถ้ารองรับอาหรับ/ฮีบรู)
- [ ] Layout ใช้ logical properties (`margin-inline-start` ไม่ใช่ `margin-left`) ไม่ hardcode ทิศทาง
- [ ] Icon ที่มีทิศทาง (ลูกศร, ปุ่มย้อนกลับ) ถูก mirror เมื่อ `dir="rtl"`
- [ ] ข้อความผสม (ตัวเลข/โค้ดแทรกในประโยค RTL) ไม่กลับด้านผิดที่ (bidi bug)

## ฟอนต์
- [ ] ฟอนต์ที่ใช้ครอบคลุมอักษรทุกภาษาที่รองรับจริง (ภาษาไทยต้องการสระบน/ล่าง วรรณยุกต์ — ฟอนต์ละตินล้วนเรนเดอร์เป็นกล่อง/สระหลุด)
- [ ] Fallback font chain ประกาศไว้ ไม่ปล่อยให้ระบบเลือกเอง (ผลต่างกันระหว่าง OS)

## ทดสอบ
- [ ] รัน UI/ทดสอบ pseudo-locale หรือภาษาที่ยาวกว่าอังกฤษ ~30-40% (เยอรมัน/ไทย) เพื่อจับปัญหา layout ล้น
- [ ] สลับ locale ของเครื่องทดสอบจริง ไม่ใช่แค่เปลี่ยนไฟล์แปล — บาง bug (ตัวคั่นทศนิยม, collation) มาจาก system locale ไม่ใช่ i18n library
