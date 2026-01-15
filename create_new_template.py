"""
สร้าง Template Excel ใหม่ที่มีคอลัมน์ File ID
"""
import pandas as pd

# สร้าง DataFrame ตัวอย่าง
data = {
    'ลำดับ': [1, 2, 3],
    'ชื่อ-นามสกุล': ['สมชาย ใจดี', 'สมหญิง รักดี', 'ทดสอบ ระบบ'],
    'File ID': ['1abc123def456', '1ghi789jkl012', '1mno345pqr678'],
    'หมายเหตุ': ['', '', '']
}

df = pd.DataFrame(data)

# บันทึกเป็นไฟล์ Excel
output_file = 'template_รายชื่อ_v2.xlsx'
df.to_excel(output_file, index=False, engine='openpyxl')

print(f"OK - Created {output_file} successfully")
print("\nTemplate structure:")
print(df)
print("\n" + "="*60)
print("How to use:")
print("1. Fill order number (must match PDF filename)")
print("2. Fill name")
print("3. Fill File ID from Google Drive")
print("   - Open file in Google Drive")
print("   - URL format: https://drive.google.com/file/d/FILE_ID/view")
print("   - Copy FILE_ID and paste here")
print("4. Notes (optional)")
print("="*60)
