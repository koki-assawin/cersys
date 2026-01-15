"""
Complete System Test
Test all functionalities of the certificate system
"""

import os
import sys

print("=" * 70)
print("Certificate System - Complete Test")
print("=" * 70)
print()

# Test 1: Import all required libraries
print("[1/6] Testing dependencies...")
try:
    import streamlit as st
    import pandas as pd
    from pypdf import PdfReader
    from supabase import create_client, Client
    print("OK: All dependencies imported successfully")
except ImportError as e:
    print(f"ERROR: Missing dependency: {e}")
    sys.exit(1)

print()

# Test 2: Read configuration
print("[2/6] Reading configuration...")
SUPABASE_URL = ""
SUPABASE_KEY = ""

secrets_file = ".streamlit/secrets.toml"
if os.path.exists(secrets_file):
    try:
        with open(secrets_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('SUPABASE_URL'):
                    SUPABASE_URL = line.split('=')[1].strip().strip('"').strip("'")
                elif line.startswith('SUPABASE_KEY'):
                    SUPABASE_KEY = line.split('=')[1].strip().strip('"').strip("'")
        print(f"OK: Configuration loaded")
        print(f"    URL: {SUPABASE_URL[:40]}...")
    except Exception as e:
        print(f"ERROR: Error reading config: {e}")
        sys.exit(1)
else:
    print(f"ERROR: {secrets_file} not found")
    sys.exit(1)

print()

# Test 3: Connect to Supabase
print("[3/6] Connecting to Supabase...")
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("OK: Connected successfully")
except Exception as e:
    print(f"ERROR: Connection failed: {e}")
    sys.exit(1)

print()

# Test 4: Test Database Operations
print("[4/6] Testing database operations...")
try:
    # Test reading events
    response = supabase.table('events').select("*").limit(5).execute()
    event_count = len(response.data)
    print(f"OK: Events table accessible ({event_count} events)")

    if event_count > 0:
        print(f"    Sample event: {response.data[0].get('event_name', 'N/A')}")

    # Test reading certificates
    response = supabase.table('certificates').select("*").limit(5).execute()
    cert_count = len(response.data)
    print(f"OK: Certificates table accessible ({cert_count} certificates)")

except Exception as e:
    print(f"ERROR: Database test failed: {e}")

print()

# Test 5: Test Storage (optional - may fail but app still works)
print("[5/6] Testing storage bucket...")
try:
    buckets = supabase.storage.list_buckets()
    bucket_names = [b.name for b in buckets]

    if 'certificates' in bucket_names:
        print("OK: Bucket 'certificates' found")

        # Try to list files (should be empty initially)
        try:
            files = supabase.storage.from_('certificates').list()
            print(f"    Files in bucket: {len(files)}")
        except:
            print("    Note: Cannot list files (may need to upload first)")
    else:
        print(f"WARNING: Bucket 'certificates' not found in list")
        print(f"    Available: {bucket_names}")
        print("    Note: This may be a list API issue. Upload/download might still work.")

except Exception as e:
    print(f"WARNING: Storage test warning: {str(e)}")
    print("    Note: Upload/download functionality may still work")

print()

# Test 6: Check Streamlit app
print("[6/6] Checking Streamlit app...")
try:
    import subprocess
    result = subprocess.run(['netstat', '-an'], capture_output=True, text=True, timeout=5)
    if ':8501' in result.stdout:
        print("OK: Streamlit app is running at http://localhost:8501")
    else:
        print("WARNING: Streamlit not detected on port 8501")
        print("    Start it with: py -m streamlit run app_cloud.py")
except:
    print("WARNING: Cannot check if Streamlit is running")
    print("    Try opening: http://localhost:8501")

print()
print("=" * 70)
print("Test Summary")
print("=" * 70)
print()
print("OK      = Working correctly")
print("WARNING = Warning (may still work)")
print("ERROR   = Critical error")
print()
print("Next steps:")
print("1. Open browser: http://localhost:8501")
print("2. Try the User tab (search for certificates)")
print("3. Try the Admin tab (upload certificates)")
print()
print("If you see the app interface, the system is ready to use!")
print("=" * 70)
