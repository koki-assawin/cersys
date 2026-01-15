# 🧪 วิธีทดสอบการเชื่อมต่อ Supabase (Manual)

## ⚠️ สำคัญ: ต้องติดตั้ง Python ก่อน

ระบบตรวจพบว่าคุณยังไม่ได้ติดตั้ง Python หรือยังไม่ได้ตั้งค่า PATH

### 📥 ติดตั้ง Python (ถ้ายังไม่มี)

1. ดาวน์โหลด Python จาก: **https://www.python.org/downloads/**
2. เลือกเวอร์ชัน **Python 3.11** หรือ **3.12**
3. เมื่อติดตั้ง **เลือก "Add Python to PATH"** (สำคัญมาก!)
4. คลิก **Install Now**
5. รีสตาร์ท Command Prompt

---

## 🚀 วิธีทดสอบ (เมื่อติดตั้ง Python แล้ว)

### วิธีที่ 1: ใช้สคริปต์ทดสอบอัตโนมัติ

เปิด Command Prompt ในโฟลเดอร์โปรเจค แล้วรัน:

```bash
# 1. ติดตั้ง Dependencies
pip install -r requirements_cloud.txt

# 2. รันสคริปต์ทดสอบ
python check_connection.py
```

ถ้าเห็น:
```
✅ เชื่อมต่อ Supabase สำเร็จ!
✅ ตาราง 'events' พร้อมใช้งาน
✅ ตาราง 'certificates' พร้อมใช้งาน
✅ พบ Bucket 'certificates'
```

**แสดงว่าสำเร็จ!** พร้อมรันโปรแกรมหลักได้

---

### วิธีที่ 2: ทดสอบด้วยตนเอง (Manual Test)

#### ขั้นที่ 1: ติดตั้ง Dependencies
```bash
pip install streamlit pandas openpyxl pypdf supabase python-dotenv
```

#### ขั้นที่ 2: รันโปรแกรม
```bash
streamlit run app_cloud.py
```

#### ขั้นที่ 3: ตรวจสอบผลลัพธ์
เปิดเบราว์เซอร์ที่ **http://localhost:8501**

**ถ้าเห็น:**
- ✅ หน้าเว็บโหลดขึ้นมา (ไม่มี Error สีแดง)
- ✅ มี Dropdown เลือกกิจกรรมได้
- ✅ ในแท็บ User มีกิจกรรมให้เลือก

**แสดงว่าการเชื่อมต่อสำเร็จ!**

---

### วิธีที่ 3: ทดสอบผ่าน Python Shell

เปิด Python Shell แล้วรัน:

```python
import os
os.environ['SUPABASE_URL'] = 'https://ajohgfktalotqyhnwbdu.supabase.co'
os.environ['SUPABASE_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFqb2hnZmt0YWxvdHF5aG53YmR1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njg0NTAxNjIsImV4cCI6MjA4NDAyNjE2Mn0.3LpcsdbQPaAKaMZuCrn61QQKH0pIIQZ17uIcDbi4eBQ'

from supabase import create_client

supabase = create_client(
    os.environ['SUPABASE_URL'],
    os.environ['SUPABASE_KEY']
)

# ทดสอบอ่านตาราง events
response = supabase.table('events').select("*").execute()
print(f"✅ พบ {len(response.data)} กิจกรรม")
print(response.data)
```

**ถ้าเห็น:**
```
✅ พบ 2 กิจกรรม
[{'id': 1, 'event_name': 'โครงการอบรมทดสอบระบบ', ...}, ...]
```

**แสดงว่าเชื่อมต่อสำเร็จ!**

---

## 🎯 Checklist การทดสอบ

ให้ทำการทดสอบทุกข้อนี้:

### ✅ ส่วนที่ 1: การเชื่อมต่อพื้นฐาน
- [ ] ติดตั้ง Python แล้ว (`python --version` ใช้ได้)
- [ ] ติดตั้ง Dependencies แล้ว (`pip list | grep supabase`)
- [ ] ไฟล์ `secrets.toml` มี URL และ Key ถูกต้อง

### ✅ ส่วนที่ 2: Database
- [ ] สร้างตาราง `events` แล้ว (รัน SQL ใน Supabase)
- [ ] สร้างตาราง `certificates` แล้ว
- [ ] มีข้อมูลทดสอบในตาราง

### ✅ ส่วนที่ 3: Storage
- [ ] สร้าง Bucket `certificates` แล้ว
- [ ] Bucket เป็น Public
- [ ] ตั้งค่า Storage Policies แล้ว (รัน SQL)

### ✅ ส่วนที่ 4: ทดสอบการทำงาน
- [ ] รัน `streamlit run app_cloud.py` ได้
- [ ] หน้าเว็บเปิดที่ localhost:8501
- [ ] ไม่มี Error แสดง
- [ ] เลือกกิจกรรมได้ในหน้า User

---

## 🔍 ตรวจสอบปัญหา

### ❌ Error: "No module named 'supabase'"
**วิธีแก้:**
```bash
pip install supabase
```

### ❌ Error: "Connection refused"
**วิธีแก้:**
1. เช็คว่า `SUPABASE_URL` ถูกต้อง
2. เช็คว่า `SUPABASE_KEY` ถูกต้อง
3. เช็คว่า Supabase Project ไม่ถูก Pause (ไปเช็คใน Dashboard)

### ❌ Error: "Table 'events' does not exist"
**วิธีแก้:**
1. ไปที่ Supabase Dashboard > SQL Editor
2. รัน SQL ในไฟล์ `setup_database.sql`

### ❌ Error: "Bucket 'certificates' not found"
**วิธีแก้:**
1. ไปที่ Supabase Dashboard > Storage
2. คลิก New Bucket
3. ตั้งชื่อว่า `certificates` (ตัวพิมพ์เล็กทั้งหมด)
4. เลือก Public

### ❌ Error: "Permission denied"
**วิธีแก้:**
1. ไปที่ Supabase Dashboard > SQL Editor
2. รัน SQL ในไฟล์ `setup_storage_policies.sql`

---

## 📊 ตัวอย่างผลลัพธ์ที่ถูกต้อง

### เมื่อรัน check_connection.py:
```
🔍 ตรวจสอบการเชื่อมต่อ Supabase...
--------------------------------------------------
✅ พบ SUPABASE_URL: https://ajohgfktalotqyhnwb...
✅ พบ SUPABASE_KEY: eyJhbGciOiJIUzI1NiIsIn...

🔌 กำลังเชื่อมต่อ Supabase...
✅ เชื่อมต่อ Supabase สำเร็จ!

📊 ตรวจสอบ Database Tables...
✅ ตาราง 'events' พร้อมใช้งาน (มี 2 รายการ)
✅ ตาราง 'certificates' พร้อมใช้งาน (มี 3 รายการ)

📦 ตรวจสอบ Storage Bucket...
✅ พบ Bucket 'certificates'

==================================================
📋 สรุปผลการตรวจสอบ:
==================================================
✅ = พร้อมใช้งาน
❌ = ต้องแก้ไข

ถ้าพร้อมทั้งหมด สามารถรันคำสั่งนี้ได้:
   streamlit run app_cloud.py
==================================================
```

### เมื่อรัน streamlit run app_cloud.py:
```
You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.1.x:8501
```

---

## ✅ ถ้าทดสอบผ่านทุกข้อ

**ยินดีด้วย!** ระบบของคุณพร้อมใช้งานแล้ว! 🎉

ขั้นตอนต่อไป:
1. ทดสอบอัพโหลดเกียรติบัตรในแท็บ Admin
2. ทดสอบค้นหาและดาวน์โหลดในแท็บ User
3. เมื่อทดสอบเสร็จ พร้อม Deploy บน Cloud!

---

## 📞 ต้องการความช่วยเหลือ?

ถ้ายังติดปัญหา:
1. ถ่ายภาพหน้าจอ Error message
2. คัดลอก Error ทั้งหมดจาก Terminal
3. บอกว่าติดตรงขั้นตอนไหน

**พร้อมช่วยเหลือเสมอ!** 💪
