# 🚀 START HERE - Complete Setup Guide

## Current Status: Python Not Installed

Your system needs Python to run this application.

---

## Step 1: Install Python (5 minutes)

### Download Python:
1. Go to: **https://www.python.org/downloads/**
2. Click the big yellow button: **Download Python 3.12.x**
3. Save the installer file

### Install Python:
1. **Double-click** the downloaded installer
2. ⚠️ **IMPORTANT:** Check the box **"Add Python to PATH"** (at the bottom)
3. Click **"Install Now"**
4. Wait for installation to complete
5. Click **"Close"**

### Verify Installation:
1. Open **Command Prompt** (search "cmd" in Start menu)
2. Type: `python --version`
3. You should see: `Python 3.12.x`

---

## Step 2: Setup Supabase (10-15 minutes)

Before running the app, you need to setup Supabase (free cloud database).

### Quick Checklist:
```
☐ Go to https://supabase.com and create account
☐ Create new project (Region: Singapore)
☐ Copy Project URL and API Key (Settings > API)
☐ Save keys to .streamlit/secrets.toml
☐ Run SQL: setup_database.sql (in SQL Editor)
☐ Create Storage Bucket: "certificates" (Public)
☐ Run SQL: setup_storage_policies.sql
```

**Detailed guide:** See `SUPABASE_SETUP_STEP_BY_STEP.md`

---

## Step 3: Test Connection

After installing Python and setting up Supabase:

### Option A: Double-click
```
test_connection.bat
```

### Option B: Command line
```bash
python check_connection.py
```

**Expected result:**
```
SUCCESS: All checks passed!
```

---

## Step 4: Run the Application

### Option A: Double-click
```
run_app.bat
```

### Option B: Command line
```bash
streamlit run app_cloud.py
```

**Then open:** http://localhost:8501

---

## Troubleshooting

### "Python not found"
- You didn't check "Add Python to PATH" during installation
- Solution: Reinstall Python and check that box

### "secrets.toml not found"
- You didn't create the secrets file
- Solution:
  ```bash
  copy .streamlit\secrets.toml.example .streamlit\secrets.toml
  ```
  Then edit the file with your Supabase keys

### "Table not found"
- You didn't run the SQL setup
- Solution: Run SQL from `setup_database.sql` in Supabase SQL Editor

### "Bucket not found"
- You didn't create the Storage bucket
- Solution: Create bucket "certificates" in Supabase Storage

---

## Files Overview

| File | Purpose |
|------|---------|
| `START_HERE.md` | ⭐ This file - Read first! |
| `SUPABASE_SETUP_STEP_BY_STEP.md` | Detailed Supabase setup guide |
| `HOW_TO_TEST.md` | Testing instructions |
| `test_connection.bat` | Test Supabase connection |
| `run_app.bat` | Run the application |
| `check_connection.py` | Connection test script |
| `setup_database.sql` | Database setup SQL |
| `setup_storage_policies.sql` | Storage permissions SQL |

---

## Quick Start (If you already have everything)

1. Install dependencies:
   ```bash
   pip install -r requirements_cloud.txt
   ```

2. Test connection:
   ```bash
   python check_connection.py
   ```

3. Run app:
   ```bash
   streamlit run app_cloud.py
   ```

---

## Need Help?

Read the detailed guides:
- Supabase Setup: `SUPABASE_SETUP_STEP_BY_STEP.md`
- Testing: `HOW_TO_TEST.md`
- Deployment: `CLOUD_DEPLOYMENT_GUIDE.md`

---

**Let's get started! Follow Step 1 above.** 🎉
