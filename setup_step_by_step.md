# 🚀 ขั้นตอนติดตั้งระบบ V2.0 ทีละขั้น

## ✅ ขั้นที่ 1: ติดตั้ง Dependencies (เสร็จแล้ว)

- [x] Python packages ติดตั้งเรียบร้อยแล้ว
- [x] Supabase client พร้อมใช้งาน

---

## 📋 ขั้นที่ 2: อัพเดทฐานข้อมูล Supabase

**วิธีทำ:**

1. เปิด Supabase Dashboard: https://supabase.com/dashboard
2. เลือก Project ของคุณ
3. คลิกที่ **SQL Editor** (เมนูด้านซ้าย)
4. คลิก **New Query**
5. เปิดไฟล์ `setup_database_v2.sql` ในโฟลเดอร์นี้
6. **คัดลอกโค้ด SQL ทั้งหมด** วางใน SQL Editor
7. คลิก **Run** (หรือกด Ctrl+Enter)
8. รอจนเห็นข้อความ "Success"

**ผลลัพธ์ที่คาดหวัง:**
```
Database V2 setup completed successfully!
Created 1 admin users
Created 1 events
Default admin username: admin
Default admin password: admin123
Please change the password after first login!
```

⚠️ **คำเตือน:** SQL จะลบข้อมูลเก่าทั้งหมดและสร้างใหม่

---

## ✅ ขั้นที่ 3: ทดสอบการเชื่อมต่อ

หลังจากรัน SQL แล้ว กลับมารันคำสั่งนี้:

```bash
run_test_v2.bat
```

หรือ

```bash
py test_v2_connection.py
```

ควรเห็นผลลัพธ์:
- ✓ Database V2 schema detected
- ✓ Admin user found
- ✓ Events table ready

---

## 🎯 ขั้นที่ 4: ทดสอบระบบ Admin

```bash
run_admin.bat
```

1. เปิดเบราว์เซอร์: http://localhost:8501
2. Login:
   - Username: `admin`
   - Password: `admin123`
3. ทดสอบเพิ่มกิจกรรม

---

## 👥 ขั้นที่ 5: ทดสอบระบบ User

```bash
run_user.bat
```

1. เปิดเบราว์เซอร์: http://localhost:8501
2. เลือกกิจกรรมที่สร้างไว้
3. ทดสอบค้นหาชื่อ

---

## 📚 เอกสารเพิ่มเติม

- **คู่มือฉบับเต็ม:** `COMPLETE_USER_GUIDE_V2.md`
- **คู่มือด่วน:** `QUICK_START_V2.md`

---

## 🆘 แก้ปัญหา

### ปัญหา: ไม่พบตาราง admin_users

**สาเหตุ:** ยังไม่ได้รัน SQL

**วิธีแก้:** ทำตามขั้นที่ 2 ข้างต้น

### ปัญหา: Login ไม่ได้

**สาเหตุ:** รหัสผ่านผิดหรือยังไม่ได้สร้าง admin

**วิธีแก้:** ตรวจสอบว่ารัน SQL เรียบร้อยแล้ว

---

**พร้อมแล้ว! เริ่มใช้งานได้เลย** 🎊
