# ⚡ Quick Start - เริ่มใช้งานด่วน V2.0

## ขั้นตอนเร็ว (10 นาที)

### 1️⃣ ติดตั้ง Dependencies
```bash
py -m pip install -r requirements_v2.txt
```

### 2️⃣ ตั้งค่า Supabase

1. สมัคร: https://supabase.com (ฟรี)
2. สร้าง Project (Region: Singapore)
3. คัดลอก URL + API Key จาก Settings > API
4. รัน SQL: `setup_database_v2.sql` ใน SQL Editor
5. แก้ไขไฟล์ `.streamlit/secrets.toml`:
```toml
SUPABASE_URL = "your-url-here"
SUPABASE_KEY = "your-key-here"
```

### 3️⃣ เตรียมไฟล์

**ใน Google Drive:**
1. สร้างโฟลเดอร์ใหม่
2. อัพโหลดไฟล์ PDF (ต้องแยกเป็นไฟล์เดี่ยวแล้ว)
   - ตั้งชื่อ: 1.pdf, 2.pdf, 3.pdf, ...
3. แชร์โฟลเดอร์: "Anyone with the link" → Viewer
4. คัดลอกลิงค์โฟลเดอร์

**ไฟล์ Excel:**
1. ดาวน์โหลด Template จากระบบ
2. กรอกรายชื่อ (ลำดับต้องตรงกับชื่อไฟล์ PDF)

### 4️⃣ เพิ่มกิจกรรม (Admin)

```bash
# รันหน้า Admin
py -m streamlit run admin_app.py
```

1. Login: `admin` / `admin123`
2. คลิก "เพิ่มกิจกรรมใหม่"
3. กรอกชื่อกิจกรรม
4. Paste ลิงค์โฟลเดอร์ Google Drive
5. อัพโหลดไฟล์ Excel
6. คลิก "สร้างกิจกรรม"

### 5️⃣ ทดสอบ (User)

```bash
# รันหน้า User
py -m streamlit run user_app.py
```

1. เลือกกิจกรรม
2. ใส่ชื่อค้นหา
3. คลิก "ดาวน์โหลด"

---

## 🎯 ข้อมูลสำคัญ

| รายการ | ข้อมูล |
|--------|--------|
| Admin Username | `admin` |
| Admin Password | `admin123` |
| หน้า Admin | http://localhost:8501 (admin_app.py) |
| หน้า User | http://localhost:8501 (user_app.py) |
| คู่มือฉบับเต็ม | `COMPLETE_USER_GUIDE_V2.md` |

---

## ⚠️ สิ่งที่ต้องจำ

1. ไฟล์ PDF **ต้องแยกเป็นไฟล์เดี่ยวก่อน**
2. ชื่อไฟล์ต้องเป็นตัวเลข (1.pdf, 2.pdf, ...)
3. ลำดับใน Excel ต้องตรงกับชื่อไฟล์
4. จำนวนแถวใน Excel = จำนวนไฟล์ PDF
5. โฟลเดอร์ Google Drive ต้องแชร์เป็น Public

---

## 🆘 เจอปัญหา?

อ่าน: `COMPLETE_USER_GUIDE_V2.md` (คู่มือฉบับเต็ม)

---

**พร้อมใช้งาน!** 🚀
