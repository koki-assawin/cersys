# ⚡ Quick Start - ตั้งค่าระบบเร็ว 10 นาที

## 📌 สำหรับคนไม่อยากอ่านเยอะ

### ✅ Checklist สั้นๆ

```
☐ 1. สมัคร Supabase (https://supabase.com)
☐ 2. สร้าง Project (Region: Singapore)
☐ 3. คัดลอก API Keys (Settings > API)
☐ 4. รัน SQL สร้าง Database (ใช้ไฟล์ setup_database.sql)
☐ 5. สร้าง Bucket "certificates" (Storage > New bucket > Public)
☐ 6. รัน SQL ตั้งค่า Storage (ใช้ไฟล์ setup_storage_policies.sql)
☐ 7. แก้ไข .streamlit/secrets.toml (ใส่ URL + Key)
☐ 8. รันโปรแกรม: streamlit run app_cloud.py
```

---

## 🎯 คำสั่งด่วน

### 1. ติดตั้ง Dependencies
```bash
pip install -r requirements_cloud.txt
```

### 2. สร้างไฟล์ Secrets
```bash
# Windows
copy .streamlit\secrets.toml.example .streamlit\secrets.toml

# Linux/Mac
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

### 3. แก้ไข secrets.toml
```toml
SUPABASE_URL = "ใส่ URL ของคุณ"
SUPABASE_KEY = "ใส่ Key ของคุณ"
```

### 4. รันโปรแกรม
```bash
streamlit run app_cloud.py
```

---

## 📂 ไฟล์ที่ต้องใช้

| ไฟล์ | ใช้ทำอะไร |
|------|-----------|
| `setup_database.sql` | สร้าง Database Tables |
| `setup_storage_policies.sql` | ตั้งค่า Storage Permissions |
| `.streamlit/secrets.toml` | เก็บ API Keys |

---

## 🆘 เจอปัญหา?

อ่านคู่มือฉบับเต็ม:
- **ละเอียด**: `SUPABASE_SETUP_STEP_BY_STEP.md`
- **ครบวงจร**: `CLOUD_DEPLOYMENT_GUIDE.md`

---

## ✅ ทดสอบว่าสำเร็จหรือไม่

เปิด http://localhost:8501 แล้วดูว่า:
- [ ] หน้าเว็บโหลดได้
- [ ] ไม่มี Error สีแดง
- [ ] เลือกกิจกรรมได้ (จะมี "โครงการอบรมทดสอบระบบ")

**ถ้าครบทั้ง 3 ข้อ = สำเร็จ!** 🎉

---

## 🚀 พร้อม Deploy?

Deploy บน Streamlit Cloud:
1. Push โค้ดขึ้น GitHub
2. ไปที่ https://share.streamlit.io
3. เลือก Repo > ตั้งค่า Secrets
4. Deploy!

**เสร็จแล้ว!** 🎊
