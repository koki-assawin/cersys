"""
สคริปต์สร้างข้อมูลทดสอบในฐานข้อมูล
พร้อม URL ที่ถูกต้องของแต่ละไฟล์
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
print("="*60)
print("Create Test Data with Real Google Drive URLs")
print("="*60)
print()

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("OK: Connected to Supabase")
except Exception as e:
    print(f"ERROR: Cannot connect: {e}")
    exit(1)

# ข้อมูลตัวอย่าง (ใช้ File ID ที่คุณให้มา)
test_file_id = "1UP4SLbS2fDN2jx_0Di8iD9KzhTG_oljU"  # ตัวอย่างจากผู้ใช้

print()
print("Creating test event...")

# สร้าง event ทดสอบ
try:
    event_data = {
        "event_name": "กิจกรรมทดสอบระบบ V2",
        "description": "ทดสอบการดาวน์โหลดและดูไฟล์",
        "google_drive_folder_link": "https://drive.google.com/drive/folders/test",
        "created_by": "system"
    }

    result = supabase.table('events').insert(event_data).execute()

    if result.data:
        event_id = result.data[0]['id']
        print(f"OK: Created event ID: {event_id}")

        # สร้างเกียรติบัตรทดสอบ 3 ใบ
        print()
        print("Creating test certificates...")

        certificates = [
            {
                "event_id": event_id,
                "name": "สมชาย ใจดี",
                "order_number": 1,
                "google_drive_file_link": f"https://drive.google.com/file/d/{test_file_id}/view",
                "file_name": "1.pdf"
            },
            {
                "event_id": event_id,
                "name": "สมหญิง รักดี",
                "order_number": 2,
                "google_drive_file_link": f"https://drive.google.com/file/d/{test_file_id}/view",
                "file_name": "2.pdf"
            },
            {
                "event_id": event_id,
                "name": "ทดสอบ ระบบ",
                "order_number": 3,
                "google_drive_file_link": f"https://drive.google.com/file/d/{test_file_id}/view",
                "file_name": "3.pdf"
            }
        ]

        for cert in certificates:
            try:
                supabase.table('certificates').insert(cert).execute()
                print(f"OK: Created certificate for {cert['name']}")
            except Exception as e:
                print(f"ERROR: Cannot create certificate: {e}")

        print()
        print("="*60)
        print("Test Data Created Successfully!")
        print("="*60)
        print()
        print(f"Event ID: {event_id}")
        print(f"Event Name: {event_data['event_name']}")
        print(f"Certificates: {len(certificates)}")
        print()
        print("Test URLs:")
        for cert in certificates:
            print(f"  - {cert['name']}: {cert['google_drive_file_link']}")
        print()
        print("Next steps:")
        print("  1. Run: run_user.bat")
        print("  2. Search for: สมชาย")
        print("  3. Click download or view button")
        print()

    else:
        print("ERROR: Cannot create event")

except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
