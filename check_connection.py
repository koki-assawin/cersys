"""
Supabase Connection Test Script
Test if Supabase configuration is correct
"""

import os
import sys

print("=" * 60)
print("Supabase Connection Test")
print("=" * 60)
print()

# Step 1: Check if dependencies are installed
print("[1/5] Checking dependencies...")
try:
    from supabase import create_client, Client
    print("OK: supabase library found")
except ImportError:
    print("ERROR: supabase library not found")
    print()
    print("Please run: pip install -r requirements_cloud.txt")
    sys.exit(1)

print()

# Step 2: Read configuration from secrets.toml
print("[2/5] Reading configuration...")

SUPABASE_URL = ""
SUPABASE_KEY = ""

# Try to read from .streamlit/secrets.toml
secrets_file = ".streamlit/secrets.toml"
if os.path.exists(secrets_file):
    print(f"OK: Found {secrets_file}")
    try:
        with open(secrets_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('SUPABASE_URL'):
                    SUPABASE_URL = line.split('=')[1].strip().strip('"').strip("'")
                elif line.startswith('SUPABASE_KEY'):
                    SUPABASE_KEY = line.split('=')[1].strip().strip('"').strip("'")
    except Exception as e:
        print(f"ERROR: Cannot read secrets.toml: {e}")
        sys.exit(1)
else:
    print(f"ERROR: {secrets_file} not found")
    print()
    print("Please create the file:")
    print(f"  copy .streamlit\\secrets.toml.example .streamlit\\secrets.toml")
    sys.exit(1)

# Validate configuration
if not SUPABASE_URL or not SUPABASE_KEY:
    print("ERROR: SUPABASE_URL or SUPABASE_KEY is empty")
    print()
    print("Please edit .streamlit/secrets.toml and add:")
    print('  SUPABASE_URL = "https://xxxxx.supabase.co"')
    print('  SUPABASE_KEY = "your-anon-key"')
    sys.exit(1)

print(f"OK: SUPABASE_URL = {SUPABASE_URL[:40]}...")
print(f"OK: SUPABASE_KEY = {SUPABASE_KEY[:30]}...")
print()

# Step 3: Connect to Supabase
print("[3/5] Connecting to Supabase...")
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("OK: Connected to Supabase")
except Exception as e:
    print(f"ERROR: Cannot connect to Supabase")
    print(f"  {str(e)}")
    sys.exit(1)

print()

# Step 4: Check Database Tables
print("[4/5] Checking database tables...")

tables_ok = True

# Check events table
try:
    response = supabase.table('events').select("*").limit(1).execute()
    count = len(response.data)
    print(f"OK: Table 'events' found ({count} rows)")
except Exception as e:
    print(f"ERROR: Table 'events' not found or not accessible")
    print(f"  {str(e)}")
    print()
    print("Please run SQL in Supabase SQL Editor:")
    print("  File: setup_database.sql")
    tables_ok = False

# Check certificates table
try:
    response = supabase.table('certificates').select("*").limit(1).execute()
    count = len(response.data)
    print(f"OK: Table 'certificates' found ({count} rows)")
except Exception as e:
    print(f"ERROR: Table 'certificates' not found or not accessible")
    print(f"  {str(e)}")
    print()
    print("Please run SQL in Supabase SQL Editor:")
    print("  File: setup_database.sql")
    tables_ok = False

print()

# Step 5: Check Storage Bucket
print("[5/5] Checking storage bucket...")

storage_ok = True

try:
    buckets = supabase.storage.list_buckets()
    bucket_names = [b.name for b in buckets]

    if 'certificates' in bucket_names:
        print("OK: Bucket 'certificates' found")
    else:
        print("ERROR: Bucket 'certificates' not found")
        print(f"  Available buckets: {bucket_names}")
        print()
        print("Please create bucket in Supabase Dashboard:")
        print("  1. Go to Storage")
        print("  2. Click 'New Bucket'")
        print("  3. Name: certificates")
        print("  4. Public: Yes")
        storage_ok = False
except Exception as e:
    print(f"WARNING: Cannot check storage buckets")
    print(f"  {str(e)}")
    storage_ok = False

print()
print("=" * 60)
print("Summary")
print("=" * 60)

if tables_ok and storage_ok:
    print("SUCCESS: All checks passed!")
    print()
    print("You can now run the application:")
    print("  streamlit run app_cloud.py")
    print()
    print("Or double-click: run_app.bat")
else:
    print("FAILED: Some checks failed")
    print()
    print("Please fix the issues above and run this script again")
    sys.exit(1)

print("=" * 60)
