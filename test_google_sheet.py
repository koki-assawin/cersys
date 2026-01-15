"""
ทดสอบการอ่าน Google Sheet
"""
import pandas as pd
import requests
from io import StringIO
import re

def extract_google_sheet_id(link):
    """ดึง Sheet ID จาก Google Sheet link"""
    patterns = [
        r'docs\.google\.com/spreadsheets/d/([a-zA-Z0-9_-]+)',
    ]
    for pattern in patterns:
        match = re.search(pattern, link)
        if match:
            return match.group(1)
    return None

def read_google_sheet(sheet_url):
    """อ่านข้อมูลจาก Google Sheet (public)"""
    try:
        # ดึง Sheet ID
        sheet_id = extract_google_sheet_id(sheet_url)
        if not sheet_id:
            return None, "Cannot extract Sheet ID"

        # สร้าง CSV export URL
        csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

        print(f"Trying to read: {csv_url}")

        # ดาวน์โหลดข้อมูล
        response = requests.get(csv_url, timeout=10)

        if response.status_code == 200:
            # อ่านเป็น DataFrame
            df = pd.read_csv(StringIO(response.text))
            return df, None
        else:
            return None, f"Cannot access Google Sheet (Status: {response.status_code})"

    except Exception as e:
        return None, f"Error: {str(e)}"

# ทดสอบ
print("="*70)
print("Google Sheet Reader Test")
print("="*70)
print()

# ให้ผู้ใช้ใส่ URL
sheet_url = input("Enter Google Sheet URL: ").strip()

if not sheet_url:
    print("\nUsing example URL...")
    sheet_url = "https://docs.google.com/spreadsheets/d/1EXAMPLE/edit"
    print(f"URL: {sheet_url}")

print()
print("Reading Google Sheet...")
print()

df, error = read_google_sheet(sheet_url)

if error:
    print(f"ERROR: {error}")
    print()
    print("Make sure:")
    print("  1. Google Sheet is shared as 'Anyone with the link can VIEW'")
    print("  2. URL is from Google Sheets (not Google Drive)")
    print("  3. Format: https://docs.google.com/spreadsheets/d/SHEET_ID/edit")
else:
    print("SUCCESS: Read Google Sheet")
    print()
    print(f"Total rows: {len(df)}")
    print(f"Columns: {', '.join(df.columns.tolist())}")
    print()
    print("Data preview:")
    print(df)
    print()

    # ตรวจสอบคอลัมน์ที่จำเป็น
    required_columns = ['ลำดับที่', 'ชื่อ-สกุล', 'URL']
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        print("WARNING: Missing required columns:")
        print(f"  {', '.join(missing_columns)}")
        print()
        print("Required columns: ลำดับที่, ชื่อ-สกุล, URL")
    else:
        print("OK: All required columns found")

print()
print("="*70)
