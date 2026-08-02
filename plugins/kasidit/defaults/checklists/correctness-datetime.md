# Date / Time Correctness Checklist

## Parsing
- [ ] `new Date('2026-03-02')` ใน JS ตีความเป็น UTC midnight แต่ `.getDay()` อ่านเป็น local
      -> ในโซน UTC ติดลบ (ทวีปอเมริกาทั้งหมด) ทุกวันเลื่อนถอย 1 วัน
      ใช้ `Date.UTC` + `getUTC*` ให้ตลอด หรือใช้ Temporal / date library
- [ ] วันที่ไม่มีจริง (2026-02-30) ถูกจับหรือถูกม้วนเงียบๆ — ต้อง roundtrip check

## เลขคณิต
- [ ] บวกวันด้วย +86400000ms พังข้าม DST ถ้าอยู่ใน local time
- [ ] ปลายช่วง inclusive หรือ exclusive — เขียนไว้ให้ชัด
- [ ] วันหยุดที่ตรงกับสุดสัปดาห์ ต้องไม่ถูกหักซ้ำ

## ทดสอบ
- [ ] รัน test suite ซ้ำใต้ TZ ที่ offset ติดลบ (`TZ=America/Santiago`)
      และ TZ ที่มี DST — ไม่ใช่ UTC อย่างเดียว
