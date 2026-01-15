"""
สร้าง Template Google Sheet ตัวอย่าง
"""
import pandas as pd

# สร้าง DataFrame ตัวอย่าง
data = {
    'ลำดับที่': [1, 2, 3],
    'ชื่อ-สกุล': [
        'นายสมชาย ใจดี',
        'นางสาวสมหญิง รักดี',
        'นายทดสอบ ระบบ'
    ],
    'URL': [
        'https://drive.google.com/file/d/1UP4SLbS2fDN2jx_0Di8iD9KzhTG_oljU/view',
        'https://drive.google.com/file/d/1ABC123DEF456GHI789JKL012MNO345/view',
        'https://drive.google.com/file/d/1XYZ789PQR456STU123VWX890ABC567/view'
    ]
}

df = pd.DataFrame(data)

# บันทึกเป็น CSV (สำหรับอัพโหลดไปเป็น Google Sheet)
output_file = 'template_google_sheet.csv'
df.to_csv(output_file, index=False, encoding='utf-8-sig')

print("="*70)
print("Google Sheet Template Created")
print("="*70)
print()
print(f"File: {output_file}")
print()
print("Template structure:")
print(df)
print()
print("="*70)
print("How to use:")
print("="*70)
print()
print("1. Open Google Drive")
print("2. Click 'New' -> Google Sheets -> Blank spreadsheet")
print("3. File -> Import -> Upload -> Select template_google_sheet.csv")
print("4. Replace URLs with your actual PDF URLs")
print("5. Share -> Anyone with the link can VIEW")
print("6. Copy the Google Sheet URL")
print("7. Use this URL in Admin page")
print()
print("Google Sheet URL format:")
print("  https://docs.google.com/spreadsheets/d/SHEET_ID/edit")
print()
print("="*70)
