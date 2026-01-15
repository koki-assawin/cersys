# คู่มือ Deploy ไป Streamlit Cloud

## ขั้นตอนที่ 1: สร้าง GitHub Repository

1. เข้า https://github.com/new
2. ตั้งชื่อ Repository: `cersys` หรือ `certificate-system`
3. เลือก **Public** (Streamlit Cloud ฟรีต้องเป็น Public)
4. **อย่าเลือก** Add README, .gitignore หรือ license
5. คลิก **Create repository**

## ขั้นตอนที่ 2: Push Code ไป GitHub

หลังจากสร้าง repo แล้ว ให้รันคำสั่งใน Command Prompt:

```bash
cd C:\xampp\htdocs\cersys
git remote add origin https://github.com/YOUR_USERNAME/cersys.git
git branch -M main
git push -u origin main
```

**เปลี่ยน YOUR_USERNAME เป็น username GitHub ของคุณ**

## ขั้นตอนที่ 3: Deploy บน Streamlit Cloud

1. เข้า https://share.streamlit.io
2. คลิก **Sign in with GitHub**
3. คลิก **New app**
4. เลือก:
   - Repository: `YOUR_USERNAME/cersys`
   - Branch: `main`
   - Main file path: `user_app.py`
5. คลิก **Advanced settings**
6. ในส่วน **Secrets** ให้ใส่:

```toml
SUPABASE_URL = "https://ajohgfktalotqyhnwbdu.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFqb2hnZmt0YWxvdHF5aG53YmR1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njg0NTAxNjIsImV4cCI6MjA4NDAyNjE2Mn0.3LpcsdbQPaAKaMZuCrn61QQKH0pIIQZ17uIcDbi4eBQ"
```

7. คลิก **Deploy!**

## ขั้นตอนที่ 4: Deploy Admin App (ทำซ้ำขั้นตอน 3)

1. คลิก **New app** อีกครั้ง
2. เลือก:
   - Repository: `YOUR_USERNAME/cersys`
   - Branch: `main`
   - Main file path: `admin_app.py`
3. ใส่ Secrets เหมือนเดิม
4. คลิก **Deploy!**

## URL ที่จะได้

หลัง deploy สำเร็จจะได้ URL ประมาณนี้:
- User App: `https://YOUR_USERNAME-cersys-user-app-xxxxx.streamlit.app`
- Admin App: `https://YOUR_USERNAME-cersys-admin-app-xxxxx.streamlit.app`

## หมายเหตุ

- Streamlit Cloud ฟรีต้องเป็น **Public repository**
- ถ้าต้องการ Private ต้องจ่ายเงิน
- ห้าม commit ไฟล์ `.streamlit/secrets.toml` ไป GitHub (มันอยู่ใน .gitignore แล้ว)

---
Copyright 2026 นายอัศวิน จุลมูล - โรงเรียนเตรียมอุดมศึกษาภาคใต้
