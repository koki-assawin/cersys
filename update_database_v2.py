"""
สคริปต์อัพเดทฐานข้อมูล Supabase เป็น V2.0
"""

import os
from supabase import create_client, Client
import streamlit as st

# อ่านค่า config
config_file = ".streamlit/secrets.toml"
if os.path.exists(config_file):
    import toml
    secrets = toml.load(config_file)
    SUPABASE_URL = secrets.get("SUPABASE_URL", "")
    SUPABASE_KEY = secrets.get("SUPABASE_KEY", "")
else:
    print("ERROR: ไม่พบไฟล์ .streamlit/secrets.toml")
    exit(1)

# เชื่อมต่อ Supabase
print("=" * 60)
print("Supabase Database Update V2.0")
print("=" * 60)
print()

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✓ เชื่อมต่อ Supabase สำเร็จ")
except Exception as e:
    print(f"ERROR: ไม่สามารถเชื่อมต่อ Supabase: {e}")
    exit(1)

# อ่านไฟล์ SQL
print()
print("กำลังอ่านไฟล์ setup_database_v2.sql...")

with open("setup_database_v2.sql", "r", encoding="utf-8") as f:
    sql_content = f.read()

# แบ่ง SQL เป็น statements
sql_statements = []
current_statement = []

for line in sql_content.split('\n'):
    # ข้าม comments และบรรทัดว่าง
    line = line.strip()
    if not line or line.startswith('--'):
        continue

    current_statement.append(line)

    # ถ้าจบด้วย ; แปลว่าจบ statement
    if line.endswith(';'):
        sql_statements.append(' '.join(current_statement))
        current_statement = []

print(f"✓ พบ {len(sql_statements)} SQL statements")
print()

# รัน SQL ทีละ statement
print("กำลังอัพเดทฐานข้อมูล...")
print("-" * 60)

success_count = 0
error_count = 0

for i, sql in enumerate(sql_statements, 1):
    try:
        # ใช้ rpc หรือ execute ขึ้นกับประเภทของ SQL
        if sql.strip().upper().startswith('SELECT'):
            # Query ที่ต้องการผลลัพธ์
            result = supabase.rpc('exec_sql', {'query': sql}).execute()
            print(f"[{i}/{len(sql_statements)}] ✓ {sql[:50]}...")
            if hasattr(result, 'data') and result.data:
                print(f"         Result: {result.data}")
        else:
            # DDL/DML statements
            # ใช้ PostgREST's rpc ถ้ามี หรือใช้ raw SQL
            supabase.postgrest.session.post(
                f"{SUPABASE_URL}/rest/v1/rpc/exec_sql",
                json={"query": sql},
                headers={
                    "apikey": SUPABASE_KEY,
                    "Authorization": f"Bearer {SUPABASE_KEY}"
                }
            )
            print(f"[{i}/{len(sql_statements)}] ✓ {sql[:50]}...")

        success_count += 1

    except Exception as e:
        error_msg = str(e)
        # ข้าม error ที่ไม่สำคัญ
        if 'does not exist' in error_msg or 'already exists' in error_msg:
            print(f"[{i}/{len(sql_statements)}] ⚠ {sql[:50]}... (skipped)")
        else:
            print(f"[{i}/{len(sql_statements)}] ✗ ERROR: {e}")
            error_count += 1

print("-" * 60)
print()
print(f"สำเร็จ: {success_count} statements")
if error_count > 0:
    print(f"ERROR: {error_count} statements")
print()

# ตรวจสอบผลลัพธ์
print("กำลังตรวจสอบตาราง...")
try:
    # ตรวจสอบ admin_users
    result = supabase.table('admin_users').select("*").execute()
    print(f"✓ ตาราง admin_users: {len(result.data)} รายการ")

    # ตรวจสอบ events
    result = supabase.table('events').select("*").execute()
    print(f"✓ ตาราง events: {len(result.data)} รายการ")

    # ตรวจสอบ certificates
    result = supabase.table('certificates').select("*").execute()
    print(f"✓ ตาราง certificates: {len(result.data)} รายการ")

except Exception as e:
    print(f"ERROR: ไม่สามารถตรวจสอบตาราง: {e}")

print()
print("=" * 60)
print("อัพเดทฐานข้อมูลเสร็จสิ้น!")
print("=" * 60)
print()
print("ข้อมูล Admin เริ่มต้น:")
print("  Username: admin")
print("  Password: admin123")
print()
print("⚠ โปรดเปลี่ยนรหัสผ่านหลังจาก Login ครั้งแรก!")
print()
