# 🎓 ระบบดาวน์โหลดเกียรติบัตร - Cloud Version

## 📌 สิ่งที่เปลี่ยนแปลง

### ❌ เวอร์ชันเดิม (app.py):
- ใช้ SQLite (ข้อมูลหายเมื่อ restart)
- เก็บไฟล์ในโฟลเดอร์ (ไฟล์หายเมื่อ restart)
- ✅ **ใช้ได้ดีบนเครื่อง Local เท่านั้น**

### ✅ เวอร์ชันใหม่ (app_cloud.py):
- ใช้ Supabase PostgreSQL (ข้อมูลถาวร)
- เก็บไฟล์ใน Supabase Storage (ไฟล์ถาวร)
- ✅ **ใช้ได้บน Cloud ไม่มีข้อมูลหาย**

---

## 🚀 เริ่มต้นใช้งานด่วน (Quick Start)

### 1. ติดตั้ง Dependencies
```bash
pip install -r requirements_cloud.txt
```

### 2. สร้างบัญชี Supabase (ฟรี)
- ไปที่: https://supabase.com
- สร้าง Project และคัดลอก API Keys

### 3. ตั้งค่า Secrets
สร้างไฟล์ `.streamlit/secrets.toml`:
```toml
SUPABASE_URL = "https://xxxxx.supabase.co"
SUPABASE_KEY = "your-anon-key"
```

### 4. สร้างตารางใน Supabase
คัดลอก SQL นี้ไปรันใน Supabase SQL Editor:
```sql
CREATE TABLE events (
    id BIGSERIAL PRIMARY KEY,
    event_name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE certificates (
    id BIGSERIAL PRIMARY KEY,
    event_id BIGINT REFERENCES events(id),
    name TEXT NOT NULL,
    file_path TEXT NOT NULL
);
```

### 5. สร้าง Storage Bucket
- ไปที่ Storage ใน Supabase Dashboard
- สร้าง Bucket ชื่อ `certificates` (แบบ Public)

### 6. รันทดสอบ
```bash
streamlit run app_cloud.py
```

---

## 📚 เอกสารแนะนำ

- **คู่มือครบวงจร**: อ่าน `CLOUD_DEPLOYMENT_GUIDE.md`
- **ตัวอย่าง Secrets**: ดู `.streamlit/secrets.toml.example`

---

## 💰 ค่าใช้จ่าย

### Supabase Free Tier (ฟรี):
- Database: 500 MB
- Storage: 1 GB
- เหมาะกับ: ~2,000-5,000 เกียรติบัตร

### Streamlit Community Cloud (ฟรี):
- Apps: ไม่จำกัด
- RAM: 1 GB
- เหมาะกับ: ระบบขนาดเล็ก-กลาง

---

## 🔒 ความปลอดภัย

⚠️ **สำคัญมาก**:
1. ห้าม commit ไฟล์ `.streamlit/secrets.toml` ขึ้น Git
2. ใช้ `.gitignore` ที่มีให้
3. ควรเพิ่มระบบ Login สำหรับ Admin

---

## 🆚 เปรียบเทียบ Local vs Cloud

| ฟีเจอร์ | Local (app.py) | Cloud (app_cloud.py) |
|---------|----------------|----------------------|
| ข้อมูลหายเมื่อ restart | ❌ ใช่ | ✅ ไม่ |
| ใช้งานบน Streamlit Cloud | ❌ ไม่ได้ | ✅ ได้ |
| ความเร็ว | ⚡ เร็วมาก | 🚀 เร็ว |
| การตั้งค่า | ✅ ง่าย | ⚠️ ต้องตั้งค่า Supabase |
| ค่าใช้จ่าย | ฟรี | ฟรี (มี limit) |
| เหมาะกับ | ทดสอบ/ใช้ส่วนตัว | Production |

---

## ❓ คำถามที่พบบ่อย (FAQ)

### Q: ข้อมูลจะหายไหมถ้าใช้ Cloud version?
A: **ไม่หาย** เพราะเก็บใน Supabase (Database + Storage แบบถาวร)

### Q: ต้องเสียเงินไหม?
A: **ไม่ต้อง** ถ้าใช้ Free tier ของ Supabase + Streamlit Cloud (เพียงพอสำหรับใช้งานทั่วไป)

### Q: ถ้าเกิน Free tier จะเกิดอะไร?
A: ระบบจะ limit การใช้งาน ต้องอัพเกรดเป็น Pro Plan ($25/เดือน สำหรับ Supabase)

### Q: ฉันควรใช้ version ไหน?
A:
- **Local (app.py)**: ถ้ารันบนเครื่องตัวเอง ไม่ต้องการออนไลน์
- **Cloud (app_cloud.py)**: ถ้าต้องการให้คนอื่นเข้าถึงผ่าน Internet

---

## 📁 โครงสร้างไฟล์

```
cersys/
├── app.py                          # เวอร์ชัน Local
├── app_cloud.py                    # ⭐ เวอร์ชัน Cloud (ใช้อันนี้)
├── requirements.txt                # สำหรับ Local
├── requirements_cloud.txt          # สำหรับ Cloud
├── CLOUD_DEPLOYMENT_GUIDE.md       # คู่มือครบวงจร
├── README_CLOUD.md                 # ไฟล์นี้
├── .gitignore                      # ป้องกัน commit secrets
└── .streamlit/
    └── secrets.toml.example        # ตัวอย่างการตั้งค่า
```

---

## 🎉 พร้อมใช้งาน!

หากทำตามขั้นตอนครบแล้ว ระบบของคุณพร้อม Deploy บน Cloud และใช้งานได้ถาวรโดยไม่ต้องกังวลเรื่องข้อมูลหาย!

**ขอให้โชคดี! 🚀**
