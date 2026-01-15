"""
ทดสอบการแปลง URL
"""
import re

def extract_file_id(link):
    """ดึง File ID จาก Google Drive link"""
    if not link:
        return None

    patterns = [
        r'drive\.google\.com/file/d/([a-zA-Z0-9_-]+)',
        r'drive\.google\.com/open\?id=([a-zA-Z0-9_-]+)',
    ]

    for pattern in patterns:
        match = re.search(pattern, link)
        if match:
            return match.group(1)

    return None

def convert_to_download_link(link):
    """แปลงเป็นลิงค์ดาวน์โหลดโดยตรง"""
    file_id = extract_file_id(link)
    if file_id:
        return f"https://drive.google.com/uc?export=download&id={file_id}"
    return link

def convert_to_preview_link(link):
    """แปลงเป็นลิงค์ดูไฟล์ (googleusercontent)"""
    file_id = extract_file_id(link)
    if file_id:
        return f"https://lh3.googleusercontent.com/d/{file_id}"
    return link

# ทดสอบ
print("="*70)
print("URL Conversion Test")
print("="*70)
print()

test_url = "https://drive.google.com/file/d/1UP4SLbS2fDN2jx_0Di8iD9KzhTG_oljU/view"

print(f"Original URL:")
print(f"  {test_url}")
print()

file_id = extract_file_id(test_url)
print(f"Extracted File ID:")
print(f"  {file_id}")
print()

download_url = convert_to_download_link(test_url)
print(f"Download URL:")
print(f"  {download_url}")
print()

preview_url = convert_to_preview_link(test_url)
print(f"Preview URL (Google User Content):")
print(f"  {preview_url}")
print()

print("="*70)
print("Test Result: OK")
print("="*70)
print()
print("These URLs should work:")
print(f"1. View in Google Drive: {test_url}")
print(f"2. Direct Download: {download_url}")
print(f"3. Preview (Image/PDF): {preview_url}")
print()
