"""
ลบข้อมูลเก่าทั้งหมด (เฉพาะ events และ certificates)
"""
import os
from supabase import create_client, Client

# อ่านค่า config
config_file = ".streamlit/secrets.toml"
if os.path.exists(config_file):
    import toml
    secrets = toml.load(config_file)
    SUPABASE_URL = secrets.get("SUPABASE_URL", "")
    SUPABASE_KEY = secrets.get("SUPABASE_KEY", "")
else:
    print("ERROR: Cannot find .streamlit/secrets.toml")
    exit(1)

# เชื่อมต่อ Supabase
print("="*70)
print("Clean Database (Delete All Events and Certificates)")
print("="*70)
print()

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("OK: Connected to Supabase")
except Exception as e:
    print(f"ERROR: Cannot connect: {e}")
    exit(1)

# ถามยืนยัน
print()
print("WARNING: This will delete ALL events and certificates!")
print("Admin users will NOT be deleted.")
print()
confirm = input("Are you sure? Type 'YES' to confirm: ")

if confirm != "YES":
    print("\nCancelled.")
    exit(0)

print()
print("Deleting all certificates...")
try:
    # ลบ certificates ทั้งหมด
    result = supabase.table('certificates').delete().neq('id', 0).execute()
    print("OK: Deleted all certificates")
except Exception as e:
    print(f"ERROR: {e}")

print()
print("Deleting all events...")
try:
    # ลบ events ทั้งหมด
    result = supabase.table('events').delete().neq('id', 0).execute()
    print("OK: Deleted all events")
except Exception as e:
    print(f"ERROR: {e}")

print()
print("="*70)
print("Database Cleaned!")
print("="*70)
print()
print("Next steps:")
print("  1. Run: run_admin.bat")
print("  2. Login with admin/admin123")
print("  3. Download Template from menu")
print("  4. Fill in File IDs (from Google Drive)")
print("  5. Create new event with Excel file")
print()
