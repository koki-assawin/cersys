# 📘 คู่มือการติดตั้งและ Deploy ระบบเกียรติบัตรบน Cloud

## 🎯 สรุปการปรับปรุง

### ✅ สิ่งที่แก้ไขแล้ว:
1. **เปลี่ยนจาก SQLite → Supabase PostgreSQL** (Database แบบ Cloud)
2. **เปลี่ยนจากโฟลเดอร์ Local → Supabase Storage** (File Storage แบบ Cloud)
3. **เพิ่มการจัดการ Secrets** สำหรับ API Keys

### 📁 ไฟล์ในระบบ:
- `app.py` - เวอร์ชันเดิม (ใช้กับ Local เท่านั้น)
- `app_cloud.py` - ⭐ **เวอร์ชันใหม่** (ใช้กับ Cloud ได้)
- `requirements_cloud.txt` - Dependencies สำหรับ Cloud version

---

## 🚀 ขั้นตอนการติดตั้งและ Deploy (แบบละเอียด)

### 📋 Step 1: ตั้งค่า Supabase (ฟรี)

#### 1.1 สมัครบัญชี Supabase
1. ไปที่ https://supabase.com
2. คลิก **"Start your project"** และสมัครด้วย GitHub หรือ Email
3. สร้าง **Organization** (ถ้ายังไม่มี)

#### 1.2 สร้าง Project ใหม่
1. คลิก **"New Project"**
2. กรอกข้อมูล:
   - **Project Name**: `certificate-system` (หรือชื่ออื่นตามใจชอบ)
   - **Database Password**: สร้าง Password ที่แข็งแรง (เก็บไว้ด้วย)
   - **Region**: เลือก **Singapore** (ใกล้ไทยที่สุด)
3. คลิก **"Create new project"** และรอประมาณ 1-2 นาที

#### 1.3 คัดลอก API Keys
1. ไปที่ **Settings** (เมนูซ้ายล่าง)
2. คลิก **API**
3. คัดลอกค่า 2 อย่างนี้:
   - **Project URL** (เช่น `https://xxxxx.supabase.co`)
   - **anon public** key (ตัวยาวๆ ที่ขึ้นต้นด้วย `eyJ...`)

#### 1.4 สร้าง Database Tables
1. ไปที่ **SQL Editor** (เมนูซ้าย)
2. คลิก **"New Query"**
3. คัดลอก SQL นี้และรัน:

```sql
-- สร้างตาราง events (รายการกิจกรรม)
CREATE TABLE IF NOT EXISTS events (
    id BIGSERIAL PRIMARY KEY,
    event_name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- สร้างตาราง certificates (เกียรติบัตรแต่ละใบ)
CREATE TABLE IF NOT EXISTS certificates (
    id BIGSERIAL PRIMARY KEY,
    event_id BIGINT REFERENCES events(id),
    name TEXT NOT NULL,
    file_path TEXT NOT NULL
);

-- สร้าง Index เพื่อเพิ่มความเร็วในการค้นหา
CREATE INDEX IF NOT EXISTS idx_certificates_event_id ON certificates(event_id);
CREATE INDEX IF NOT EXISTS idx_certificates_name ON certificates(name);
```

4. คลิก **Run** (หรือกด F5)
5. ตรวจสอบว่าแสดงข้อความ "Success. No rows returned"

#### 1.5 สร้าง Storage Bucket
1. ไปที่ **Storage** (เมนูซ้าย)
2. คลิก **"New Bucket"**
3. กรอกข้อมูล:
   - **Name**: `certificates`
   - **Public bucket**: ✅ เลือก (เพื่อให้ดาวน์โหลดได้)
4. คลิก **"Create bucket"**

---

### 💻 Step 2: ติดตั้งโปรแกรมบนเครื่อง (ทดสอบก่อน Deploy)

#### 2.1 Clone หรือดาวน์โหลดโค้ด
```bash
# ถ้ามี Git
git clone <your-repo-url>
cd cersys

# หรือดาวน์โหลดไฟล์มาแล้ว extract
```

#### 2.2 ติดตั้ง Dependencies
```bash
pip install -r requirements_cloud.txt
```

#### 2.3 ตั้งค่า Secrets
1. สร้างไฟล์ `.streamlit/secrets.toml`:
```bash
# Windows
mkdir .streamlit
copy .streamlit\secrets.toml.example .streamlit\secrets.toml

# Linux/Mac
mkdir -p .streamlit
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

2. แก้ไขไฟล์ `.streamlit/secrets.toml`:
```toml
SUPABASE_URL = "https://xxxxx.supabase.co"  # ← ใส่ URL ของคุณ
SUPABASE_KEY = "eyJ..."  # ← ใส่ anon key ของคุณ
```

#### 2.4 รันทดสอบบนเครื่อง
```bash
streamlit run app_cloud.py
```

เปิดเบราว์เซอร์ที่ http://localhost:8501 และทดสอบระบบ

---

### ☁️ Step 3: Deploy บน Streamlit Community Cloud (ฟรี)

#### 3.1 อัพโหลดโค้ดขึ้น GitHub
1. สร้าง Repository ใหม่บน GitHub (Public หรือ Private ก็ได้)
2. Push โค้ดขึ้นไป:

```bash
git init
git add .
git commit -m "Initial commit - Certificate System"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

⚠️ **สำคัญ**: อย่า push ไฟล์ `secrets.toml` ขึ้น GitHub!

#### 3.2 สร้าง .gitignore
สร้างไฟล์ `.gitignore` เพื่อป้องกันไม่ให้ secrets โดนอัพโหลด:

```
.streamlit/secrets.toml
*.sqlite
__pycache__/
*.pyc
.env
```

#### 3.3 Deploy บน Streamlit Cloud
1. ไปที่ https://share.streamlit.io
2. คลิก **"New app"**
3. กรอกข้อมูล:
   - **Repository**: เลือก repo ของคุณ
   - **Branch**: `main`
   - **Main file path**: `app_cloud.py`
4. คลิก **"Advanced settings"**
5. ในส่วน **Secrets**, คัดลอกจากไฟล์ `secrets.toml` ของคุณ:
```toml
SUPABASE_URL = "https://xxxxx.supabase.co"
SUPABASE_KEY = "eyJ..."
```
6. คลิก **"Deploy!"**
7. รอประมาณ 2-3 นาที

---

### ☁️ Step 4 (ทางเลือก): Deploy บน Railway.app

หากต้องการประสิทธิภาพและความเสถียรที่ดีกว่า (มีค่าใช้จ่ายเล็กน้อย):

#### 4.1 สมัครบัญชี Railway
1. ไปที่ https://railway.app
2. สมัครด้วย GitHub

#### 4.2 สร้าง Project
1. คลิก **"New Project"**
2. เลือก **"Deploy from GitHub repo"**
3. เลือก repository ของคุณ

#### 4.3 ตั้งค่า Environment Variables
1. ไปที่ **Variables** tab
2. เพิ่มตัวแปร:
   - `SUPABASE_URL`: ใส่ URL ของคุณ
   - `SUPABASE_KEY`: ใส่ anon key ของคุณ

#### 4.4 ตั้งค่า Start Command
1. ไปที่ **Settings** tab
2. ในส่วน **Deploy** → **Start Command** ใส่:
```bash
streamlit run app_cloud.py --server.port $PORT --server.address 0.0.0.0
```

3. คลิก **Deploy** และรอประมาณ 2-3 นาที

---

## 🔒 ความปลอดภัย (Security Best Practices)

### ⚠️ สิ่งที่ต้องระวัง:
1. **ห้าม commit secrets.toml ขึ้น GitHub**
2. **ใช้ Environment Variables บน Production**
3. **เปลี่ยน Supabase Password เป็นระยะ**
4. **ควรเพิ่มระบบ Authentication สำหรับหน้า Admin**

### 🔐 เพิ่มความปลอดภัยหน้า Admin (แนะนำ):

แก้ไข `app_cloud.py` เพิ่มรหัสผ่านสำหรับ Admin:

```python
# เพิ่มที่ด้านบนของ tab2 (Admin section)
with tab2:
    st.header("จัดการข้อมูลเกียรติบัตร")

    # เพิ่มระบบ Login Admin
    if 'admin_logged_in' not in st.session_state:
        st.session_state.admin_logged_in = False

    if not st.session_state.admin_logged_in:
        password = st.text_input("รหัสผ่าน Admin", type="password")
        if st.button("เข้าสู่ระบบ"):
            if password == "your-strong-password":  # ⚠️ เปลี่ยนรหัสผ่านนี้!
                st.session_state.admin_logged_in = True
                st.rerun()
            else:
                st.error("รหัสผ่านไม่ถูกต้อง")
        st.stop()

    # ... โค้ดส่วน Admin ที่เหลือ ...
```

---

## 📊 ข้อจำกัดของ Free Tier

### Supabase Free Tier:
- ✅ Database: 500 MB
- ✅ Storage: 1 GB
- ✅ Bandwidth: 5 GB/เดือน
- ⚠️ เกินนี้ต้องอัพเกรดเป็น Pro ($25/เดือน)

### Streamlit Community Cloud:
- ✅ Apps: ไม่จำกัด (Public repos)
- ✅ RAM: 1 GB
- ✅ CPU: 0.78 cores
- ⚠️ App จะ sleep หากไม่มีผู้ใช้งานหลายวัน

---

## 🔧 การแก้ปัญหา (Troubleshooting)

### ปัญหา: "Connection to Supabase failed"
**วิธีแก้:**
1. ตรวจสอบ URL และ Key ว่าคัดลอกถูกต้อง
2. ตรวจสอบว่า Project ยังไม่ถูก Pause (Free tier pause หาก idle นาน)

### ปัญหา: "Bucket not found"
**วิธีแก้:**
1. ตรวจสอบว่าสร้าง Bucket ชื่อ `certificates` แล้ว
2. ตรวจสอบว่า Bucket เป็น Public

### ปัญหา: "Permission denied"
**วิธีแก้:**
1. ไปที่ Supabase Dashboard → Authentication → Policies
2. สร้าง Policy สำหรับ Storage:
```sql
-- อนุญาตให้ทุกคนอ่านได้
CREATE POLICY "Public Access"
ON storage.objects FOR SELECT
TO public
USING (bucket_id = 'certificates');

-- อนุญาตให้ทุกคนเขียนได้ (ถ้าไม่มี Auth)
CREATE POLICY "Public Upload"
ON storage.objects FOR INSERT
TO public
WITH CHECK (bucket_id = 'certificates');
```

---

## 📞 ติดต่อและสนับสนุน

หากมีปัญหาหรือข้อสงสัย:
1. อ่าน Troubleshooting ด้านบน
2. ตรวจสอบ Logs บน Streamlit Cloud Dashboard
3. ดู Documentation: https://docs.supabase.com

---

## ✅ Checklist ก่อน Deploy

- [ ] สร้าง Supabase Project แล้ว
- [ ] รัน SQL สร้างตารางแล้ว
- [ ] สร้าง Storage Bucket `certificates` แล้ว
- [ ] ทดสอบบนเครื่อง Local ผ่านแล้ว
- [ ] สร้าง .gitignore และไม่ commit secrets.toml
- [ ] Push โค้ดขึ้น GitHub แล้ว
- [ ] ตั้งค่า Secrets บน Streamlit Cloud แล้ว
- [ ] Deploy และทดสอบการอัพโหลด + ดาวน์โหลดผ่านแล้ว

---

**สร้างโดย:** Claude Code
**เวอร์ชัน:** 2.0 Cloud Edition
**อัพเดตล่าสุด:** 2026-01-15
