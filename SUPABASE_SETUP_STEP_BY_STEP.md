# 🚀 คู่มือตั้งค่า Supabase ทีละขั้นตอน

## ⏱️ เวลาที่ใช้: ประมาณ 10-15 นาที

---

## 📋 สิ่งที่ต้องเตรียม
- [ ] อีเมล (Gmail, GitHub account)
- [ ] เบราว์เซอร์ (Chrome, Firefox, Edge)
- [ ] เปิดไฟล์นี้ไว้ข้างๆ เพื่อทำตาม

---

## ขั้นตอนที่ 1: สมัครบัญชี Supabase 🆓

### 1.1 เปิดเว็บไซต์ Supabase
1. เปิดเบราว์เซอร์ไปที่: **https://supabase.com**
2. คลิกปุ่ม **"Start your project"** หรือ **"Sign Up"** (มุมขวาบน)

### 1.2 เลือกวิธีสมัคร
คุณมี 3 ทางเลือก:
- ✅ **GitHub** (แนะนำ - ง่ายที่สุด)
- Google
- Email/Password

**คลิกเลือกวิธีที่สะดวก** → ทำตามขั้นตอนการสมัครจนเสร็จ

### 1.3 ยืนยันอีเมล (ถ้าใช้ Email)
- เช็คอีเมลและคลิก Verify
- Login เข้าสู่ระบบ

✅ **เสร็จขั้นตอนที่ 1!** คุณจะเห็นหน้า Dashboard ของ Supabase

---

## ขั้นตอนที่ 2: สร้าง Organization (ครั้งแรก)

### 2.1 ถ้าเป็นครั้งแรก
1. ระบบจะถามให้ **สร้าง Organization**
2. กรอกข้อมูล:
   - **Organization name**: ชื่ออะไรก็ได้ เช่น `my-org` หรือ `certificate-system`
3. คลิก **"Create organization"**

✅ **เสร็จขั้นตอนที่ 2!**

---

## ขั้นตอนที่ 3: สร้าง Project ใหม่ 🎯

### 3.1 คลิกสร้าง Project
1. คลิกปุ่ม **"New Project"** (สีเขียว)
2. เลือก Organization ที่สร้างไว้

### 3.2 กรอกข้อมูล Project
กรอกข้อมูลตามนี้:

#### **Name** (ชื่อโปรเจค):
```
certificate-system
```
หรือชื่ออื่นที่ชอบก็ได้ (ภาษาอังกฤษ, ไม่เว้นวรรค)

#### **Database Password**:
```
สร้างรหัสผ่านที่แข็งแรง เช่น: CertSys2026!@#$
```
⚠️ **สำคัญมาก**:
- **คัดลอกรหัสผ่านนี้ไว้ในที่ปลอดภัย!** (Notepad, Notes app)
- จะใช้ตอนเชื่อมต่อ Database ภายหลัง

#### **Region** (เลือกเซิร์ฟเวอร์):
```
Southeast Asia (Singapore)
```
✅ เลือก **Singapore** เพราะใกล้ไทยที่สุด = เร็วที่สุด

#### **Pricing Plan**:
```
Free (ฟรี)
```
✅ เลือก Free plan (500MB DB + 1GB Storage)

### 3.3 สร้าง Project
1. ตรวจสอบข้อมูลให้ครบ
2. คลิก **"Create new project"**
3. รอ **1-2 นาที** (จะมี Progress bar)

✅ **เสร็จขั้นตอนที่ 3!** รอจนกว่า Project พร้อมใช้งาน (สถานะเป็น Active)

---

## ขั้นตอนที่ 4: คัดลอก API Keys 🔑

### 4.1 เข้าสู่หน้า API Settings
1. คลิกที่ **⚙️ Settings** (เมนูซ้ายล่าง)
2. เลือก **"API"** ในเมนูย่อย

### 4.2 คัดลอกข้อมูล 2 อย่างนี้

#### 🔹 Project URL:
ดูในส่วน **"Project URL"**
```
https://xxxxxxxxxxxxx.supabase.co
```
**✏️ คัดลอกและบันทึกไว้**

#### 🔹 API Key (anon/public):
ดูในส่วน **"Project API keys"** → หา **"anon" "public"**
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZ...
(ตัวอักษรยาวมาก)
```
**✏️ คัดลอกและบันทึกไว้**

⚠️ **สำคัญ**:
- คัดลอกทั้ง 2 ค่านี้ไปเก็บไว้ใน Notepad หรือที่ปลอดภัย
- จะใช้ตอนตั้งค่าโปรเจค

✅ **เสร็จขั้นตอนที่ 4!**

---

## ขั้นตอนที่ 5: สร้าง Database Tables 📊

### 5.1 เข้าสู่ SQL Editor
1. คลิกที่ **🗄️ SQL Editor** (เมนูซ้าย)
2. คลิก **"+ New query"** (มุมขวาบน)

### 5.2 คัดลอก SQL นี้
คัดลอก SQL ด้านล่างนี้ **ทั้งหมด**:

```sql
-- ลบตารางเก่าถ้ามี (สำหรับทดสอบใหม่)
DROP TABLE IF EXISTS certificates CASCADE;
DROP TABLE IF EXISTS events CASCADE;

-- สร้างตาราง events (รายการกิจกรรม/โครงการ)
CREATE TABLE events (
    id BIGSERIAL PRIMARY KEY,
    event_name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- สร้างตาราง certificates (เกียรติบัตรของแต่ละคน)
CREATE TABLE certificates (
    id BIGSERIAL PRIMARY KEY,
    event_id BIGINT NOT NULL REFERENCES events(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    file_path TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- สร้าง Index เพื่อเพิ่มความเร็วในการค้นหา
CREATE INDEX idx_certificates_event_id ON certificates(event_id);
CREATE INDEX idx_certificates_name ON certificates(name);

-- เพิ่มข้อมูลตัวอย่าง (ทดสอบ)
INSERT INTO events (event_name) VALUES ('โครงการอบรมทดสอบ');

-- แสดงผลลัพธ์
SELECT 'สร้างตารางสำเร็จ!' as status;
SELECT * FROM events;
```

### 5.3 รัน SQL
1. **Paste** (Ctrl+V) SQL ลงในช่อง
2. คลิกปุ่ม **"Run"** (หรือกด F5)
3. รอสักครู่

### 5.4 ตรวจสอบผลลัพธ์
ควรเห็น:
```
✅ Success. 1 rows returned
```
และมีข้อมูล 1 แถวแสดงว่า:
```
id | event_name           | created_at
1  | โครงการอบรมทดสอบ      | 2026-01-15...
```

✅ **เสร็จขั้นตอนที่ 5!** Database พร้อมใช้งานแล้ว

---

## ขั้นตอนที่ 6: สร้าง Storage Bucket 📦

### 6.1 เข้าสู่หน้า Storage
1. คลิกที่ **📦 Storage** (เมนูซ้าย)

### 6.2 สร้าง Bucket ใหม่
1. คลิกปุ่ม **"New bucket"**
2. กรอกข้อมูล:

#### **Name**:
```
certificates
```
⚠️ **สำคัญ**: ต้องเป็น **"certificates"** ตรงตัว (ตัวพิมพ์เล็กทั้งหมด)

#### **Public bucket**:
```
✅ เลือก (คลิก checkbox)
```
เพราะต้องการให้ผู้ใช้ดาวน์โหลดไฟล์ได้

3. คลิก **"Create bucket"**

### 6.3 ตรวจสอบ
ควรเห็น Bucket ชื่อ **"certificates"** ในรายการ

✅ **เสร็จขั้นตอนที่ 6!** Storage พร้อมเก็บไฟล์แล้ว

---

## ขั้นตอนที่ 7: ตั้งค่า Storage Policies (สำคัญ!) 🔒

### 7.1 เข้าไปในหน้า Policies
1. คลิกที่ **Storage** (ถ้ายังไม่ได้เปิดไว้)
2. คลิกที่ **Bucket "certificates"**
3. คลิกแท็บ **"Policies"** (ด้านบน)

### 7.2 สร้าง Policy สำหรับอ่านไฟล์ (Read)
1. คลิกปุ่ม **"New Policy"**
2. เลือก **"For full customization"** → คลิก **"Create policy"**
3. กรอกข้อมูล:

**Policy name:**
```
Public Read Access
```

**Allowed operation:**
```
✅ SELECT (อ่านได้)
```

**Target roles:**
```
public
```

**WITH CHECK:**
```
bucket_id = 'certificates'
```

**USING expression:**
```
bucket_id = 'certificates'
```

หรือ **ใช้วิธีง่ายกว่า**: กลับไป SQL Editor และรัน:

```sql
-- Policy สำหรับอ่านไฟล์ (ดาวน์โหลด)
CREATE POLICY "Allow public read access"
ON storage.objects FOR SELECT
TO public
USING (bucket_id = 'certificates');

-- Policy สำหรับเขียนไฟล์ (อัพโหลด)
CREATE POLICY "Allow public upload"
ON storage.objects FOR INSERT
TO public
WITH CHECK (bucket_id = 'certificates');

-- Policy สำหรับอัพเดตไฟล์
CREATE POLICY "Allow public update"
ON storage.objects FOR UPDATE
TO public
USING (bucket_id = 'certificates');

SELECT 'สร้าง Storage Policies สำเร็จ!' as status;
```

✅ **เสร็จขั้นตอนที่ 7!** ตอนนี้ระบบสามารถอัพโหลดและดาวน์โหลดไฟล์ได้แล้ว

---

## ขั้นตอนที่ 8: ตั้งค่าโปรเจคบนเครื่อง 💻

### 8.1 สร้างไฟล์ Secrets
เปิด Terminal/Command Prompt ในโฟลเดอร์โปรเจค:

```bash
# Windows
cd C:\xampp\htdocs\cersys

# หรือ Linux/Mac
cd ~/path/to/cersys
```

สร้างไฟล์:
```bash
# Windows
copy .streamlit\secrets.toml.example .streamlit\secrets.toml

# Linux/Mac
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

### 8.2 แก้ไขไฟล์ secrets.toml
เปิดไฟล์ `.streamlit/secrets.toml` ด้วย Text Editor และแก้ไข:

```toml
SUPABASE_URL = "ใส่ Project URL ที่คัดลอกไว้"
SUPABASE_KEY = "ใส่ anon key ที่คัดลอกไว้"
```

**ตัวอย่าง:**
```toml
SUPABASE_URL = "https://abcdefghijk.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSI..."
```

⚠️ **ระวัง**:
- ใส่ URL และ Key ที่ถูกต้อง
- มี เครื่องหมาย `"` ครบ
- ไม่มีช่องว่างนำหน้า

**บันทึกไฟล์**

✅ **เสร็จขั้นตอนที่ 8!**

---

## ขั้นตอนที่ 9: ทดสอบการเชื่อมต่อ 🧪

### 9.1 ติดตั้ง Dependencies
```bash
pip install -r requirements_cloud.txt
```

### 9.2 รันโปรแกรม
```bash
streamlit run app_cloud.py
```

### 9.3 ตรวจสอบ
เปิดเบราว์เซอร์ที่ **http://localhost:8501**

**ถ้าเห็น**:
- ✅ หน้าเว็บโหลดได้ปกติ
- ✅ ไม่มี Error สีแดง
- ✅ สามารถเลือกกิจกรรมได้ (จะมี "โครงการอบรมทดสอบ")

**แสดงว่าเชื่อมต่อสำเร็จ!** 🎉

### 9.4 ทดสอบอัพโหลด (Admin)
1. ไปที่แท็บ **"Admin"**
2. ลองสร้างกิจกรรมใหม่
3. อัพโหลดไฟล์ Excel + PDF ทดสอบ
4. ดูว่าระบบทำงานได้ไหม

✅ **เสร็จขั้นตอนที่ 9!** ระบบพร้อมใช้งาน

---

## 🎉 สรุป: คุณได้อะไรบ้าง?

เมื่อทำครบทุกขั้นตอนแล้ว คุณจะมี:

✅ บัญชี Supabase (ฟรี)
✅ Project พร้อมใช้งาน
✅ Database Tables (events, certificates)
✅ Storage Bucket (certificates)
✅ API Keys สำหรับเชื่อมต่อ
✅ โปรเจคบนเครื่องพร้อมใช้
✅ ระบบทดสอบการทำงานแล้ว

---

## 🆘 แก้ปัญหา (ถ้าเจอ Error)

### ❌ Error: "Connection failed"
**วิธีแก้:**
1. ตรวจสอบ `secrets.toml` ว่า URL และ Key ถูกต้อง
2. ตรวจสอบว่า Project ใน Supabase ยัง Active อยู่ (ไม่ถูก Pause)

### ❌ Error: "Bucket not found"
**วิธีแก้:**
1. เช็คว่าสร้าง Bucket ชื่อ **"certificates"** แล้ว (ตัวพิมพ์เล็กทั้งหมด)
2. เช็คว่า Bucket เป็น Public

### ❌ Error: "Permission denied"
**วิธีแก้:**
1. รัน SQL ในขั้นตอนที่ 7 อีกครั้ง (Storage Policies)
2. เช็คว่า Policies ถูกสร้างแล้วใน Storage → Policies

### ❌ Error: "Table not found"
**วิธีแก้:**
1. รัน SQL ในขั้นตอนที่ 5 อีกครั้ง
2. ตรวจสอบใน Table Editor ว่ามีตาราง events และ certificates

---

## 📞 ต้องการความช่วยเหลือ?

ถ้ายังติดปัญหา:
1. ดู Error message ใน Terminal
2. ดู Logs ใน Supabase Dashboard
3. ถ่ายภาพหน้าจอ Error มาถาม

**พร้อมช่วยแก้ปัญหาเสมอครับ!** 🚀

---

## ✅ Checklist ก่อนไป Deploy

ก่อนจะ Deploy บน Cloud ให้เช็คว่า:

- [ ] Supabase Project สร้างแล้ว
- [ ] Database Tables มีอยู่แล้ว (events, certificates)
- [ ] Storage Bucket "certificates" มีแล้ว
- [ ] Storage Policies ตั้งค่าแล้ว
- [ ] ทดสอบบนเครื่อง Local ผ่านแล้ว
- [ ] อัพโหลด + ดาวน์โหลดไฟล์ได้
- [ ] API Keys ถูกต้อง

**ถ้าครบทุกข้อ → พร้อม Deploy แล้ว!** 🎊
