# How to Test Supabase Connection

## Fixed: Batch File Encoding Error

The `.bat` files had Thai characters which caused encoding errors in Windows Command Prompt.
**All files have been updated to use English only.**

---

## Quick Test Steps

### Method 1: Using Batch File (Easiest)

**Double-click this file:**
```
test_connection.bat
```

This will:
1. Check if Python is installed
2. Install dependencies automatically
3. Test your Supabase connection
4. Show results

---

### Method 2: Using Python Script Directly

**Open Command Prompt** in this folder and run:

```bash
# Install dependencies (only once)
pip install -r requirements_cloud.txt

# Run test
python check_connection.py
```

**Expected output:**
```
============================================================
Supabase Connection Test
============================================================

[1/5] Checking dependencies...
OK: supabase library found

[2/5] Reading configuration...
OK: Found .streamlit/secrets.toml
OK: SUPABASE_URL = https://ajohgfktalotqyhnwbdu.supabas...
OK: SUPABASE_KEY = eyJhbGciOiJIUzI1NiIsInR5cCI6Ik...

[3/5] Connecting to Supabase...
OK: Connected to Supabase

[4/5] Checking database tables...
OK: Table 'events' found (2 rows)
OK: Table 'certificates' found (3 rows)

[5/5] Checking storage bucket...
OK: Bucket 'certificates' found

============================================================
Summary
============================================================
SUCCESS: All checks passed!

You can now run the application:
  streamlit run app_cloud.py

Or double-click: run_app.bat
============================================================
```

---

## If You See Errors

### Error: "Python not found"

**Solution:**
1. Install Python from: https://www.python.org/downloads/
2. Choose Python 3.11 or 3.12
3. **IMPORTANT:** Check "Add Python to PATH" during installation
4. Restart Command Prompt
5. Test: `python --version`

---

### Error: "Table 'events' not found"

**Solution:**
1. Go to Supabase Dashboard
2. Click **SQL Editor**
3. Copy all content from file: `setup_database.sql`
4. Paste and click **Run**

---

### Error: "Bucket 'certificates' not found"

**Solution:**
1. Go to Supabase Dashboard
2. Click **Storage**
3. Click **New Bucket**
4. Name: `certificates`
5. Select **Public bucket**
6. Click **Create bucket**
7. Then run SQL from: `setup_storage_policies.sql`

---

### Error: "secrets.toml not found"

**Solution:**
1. Copy the example file:
   ```bash
   copy .streamlit\secrets.toml.example .streamlit\secrets.toml
   ```
2. Edit `.streamlit\secrets.toml` and add your keys:
   ```toml
   SUPABASE_URL = "https://xxxxx.supabase.co"
   SUPABASE_KEY = "your-anon-key"
   ```

---

## Run the Application

After all tests pass, you can run the app:

**Method 1: Double-click**
```
run_app.bat
```

**Method 2: Command line**
```bash
streamlit run app_cloud.py
```

Then open browser at: **http://localhost:8501**

---

## Checklist Before Testing

Make sure you completed these steps in Supabase:

- [ ] Created a Supabase Project
- [ ] Copied API URL and Key to `secrets.toml`
- [ ] Ran SQL from `setup_database.sql`
- [ ] Created Storage Bucket named `certificates`
- [ ] Ran SQL from `setup_storage_policies.sql`

---

## Need Help?

If you still have issues:
1. Take a screenshot of the error
2. Copy the full error message
3. Check which step failed

I'm here to help! 🚀
