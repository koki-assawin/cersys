"""
ทดสอบการเชื่อมต่อและ Schema V2.0
"""

import os
import sys

print("=" * 60)
print("Test Supabase V2.0 Connection")
print("=" * 60)
print()

# [1] ตรวจสอบ dependencies
print("[1/6] Checking dependencies...")
try:
    import streamlit
    import pandas
    import openpyxl
    from supabase import create_client, Client
    print("OK: All dependencies installed")
except ImportError as e:
    print(f"ERROR: Missing dependency: {e}")
    sys.exit(1)

# [2] อ่าน config
print()
print("[2/6] Reading configuration...")
config_file = ".streamlit/secrets.toml"
if not os.path.exists(config_file):
    print(f"ERROR: {config_file} not found")
    sys.exit(1)

import toml
secrets = toml.load(config_file)
SUPABASE_URL = secrets.get("SUPABASE_URL", "")
SUPABASE_KEY = secrets.get("SUPABASE_KEY", "")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("ERROR: SUPABASE_URL or SUPABASE_KEY not set")
    sys.exit(1)

print(f"OK: SUPABASE_URL = {SUPABASE_URL[:40]}...")
print(f"OK: SUPABASE_KEY = {SUPABASE_KEY[:30]}...")

# [3] เชื่อมต่อ Supabase
print()
print("[3/6] Connecting to Supabase...")
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("OK: Connected to Supabase")
except Exception as e:
    print(f"ERROR: Cannot connect: {e}")
    sys.exit(1)

# [4] ตรวจสอบตาราง V2
print()
print("[4/6] Checking V2.0 database schema...")

tables_to_check = {
    'admin_users': ['username', 'password_hash', 'full_name'],
    'events': ['event_name', 'google_drive_folder_link'],
    'certificates': ['name', 'order_number', 'google_drive_file_link']
}

all_tables_ok = True

for table_name, expected_columns in tables_to_check.items():
    try:
        result = supabase.table(table_name).select("*").limit(1).execute()

        # ตรวจสอบว่าตารางมีอยู่
        print(f"OK: Table '{table_name}' exists")

        # ตรวจสอบจำนวน rows
        count_result = supabase.table(table_name).select("*", count="exact").execute()
        row_count = count_result.count if hasattr(count_result, 'count') else len(count_result.data)
        print(f"    - {row_count} rows")

    except Exception as e:
        print(f"ERROR: Table '{table_name}' check failed: {e}")
        all_tables_ok = False

# [5] ตรวจสอบ Admin User
print()
print("[5/6] Checking admin user...")
try:
    result = supabase.table('admin_users').select("username, full_name").execute()
    if result.data and len(result.data) > 0:
        admin = result.data[0]
        print(f"OK: Admin user found")
        print(f"    - Username: {admin['username']}")
        print(f"    - Full name: {admin['full_name']}")
    else:
        print("WARNING: No admin user found")
        print("         Default admin should be created by SQL")
except Exception as e:
    print(f"ERROR: Cannot check admin user: {e}")
    all_tables_ok = False

# [6] ตรวจสอบ Google Drive columns
print()
print("[6/6] Checking Google Drive integration...")
try:
    # ตรวจสอบว่า events มี google_drive_folder_link
    result = supabase.table('events').select("google_drive_folder_link").limit(1).execute()
    print("OK: Events table has 'google_drive_folder_link' column")

    # ตรวจสอบว่า certificates มี google_drive_file_link
    result = supabase.table('certificates').select("google_drive_file_link, order_number").limit(1).execute()
    print("OK: Certificates table has Google Drive columns")
    print("    - google_drive_file_link")
    print("    - order_number")
except Exception as e:
    print(f"ERROR: Google Drive columns check failed: {e}")
    all_tables_ok = False

# สรุปผล
print()
print("=" * 60)
print("Summary")
print("=" * 60)

if all_tables_ok:
    print("SUCCESS: V2.0 database schema is ready!")
    print()
    print("Next steps:")
    print("  1. Run admin app: run_admin.bat")
    print("  2. Login with: admin / admin123")
    print("  3. Add your first event")
    print()
    sys.exit(0)
else:
    print("FAILED: Some checks failed")
    print()
    print("Please run setup_database_v2.sql in Supabase SQL Editor")
    print("See: setup_step_by_step.md for instructions")
    print()
    sys.exit(1)
