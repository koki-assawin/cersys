"""
ตรวจสอบข้อมูลในฐานข้อมูล
"""
import os
from supabase import create_client, Client
import pandas as pd

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
print("Database Content Check")
print("="*70)
print()

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("OK: Connected to Supabase")
except Exception as e:
    print(f"ERROR: Cannot connect: {e}")
    exit(1)

# ตรวจสอบ Events
print()
print("-"*70)
print("EVENTS TABLE")
print("-"*70)
try:
    result = supabase.table('events').select("*").execute()
    if result.data:
        df = pd.DataFrame(result.data)
        print(f"\nTotal events: {len(df)}\n")
        for idx, row in df.iterrows():
            print(f"ID: {row['id']}")
            print(f"  Name: {row['event_name']}")
            print(f"  Folder Link: {row.get('google_drive_folder_link', 'N/A')}")
            print(f"  Created: {row.get('created_at', 'N/A')[:10]}")
            print()
    else:
        print("No events found")
except Exception as e:
    print(f"ERROR: {e}")

# ตรวจสอบ Certificates
print("-"*70)
print("CERTIFICATES TABLE")
print("-"*70)
try:
    result = supabase.table('certificates').select("*").execute()
    if result.data:
        df = pd.DataFrame(result.data)
        print(f"\nTotal certificates: {len(df)}\n")
        for idx, row in df.iterrows():
            print(f"ID: {row['id']} | Event: {row['event_id']} | Order: {row['order_number']}")
            print(f"  Name: {row['name']}")
            print(f"  File Link: {row.get('google_drive_file_link', 'N/A')}")
            print(f"  File Name: {row.get('file_name', 'N/A')}")
            print()
    else:
        print("No certificates found")
except Exception as e:
    print(f"ERROR: {e}")

print("="*70)
print("Check Complete")
print("="*70)
print()
print("If you see folder links (not file links), you need to:")
print("  1. Delete old data")
print("  2. Create new event with proper File IDs")
print("  3. Use the new Template with File ID column")
print()
