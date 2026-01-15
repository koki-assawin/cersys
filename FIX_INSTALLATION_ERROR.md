# Fix: Microsoft Visual C++ Error

## Problem

When running `test_connection.bat`, you got this error:
```
error: Microsoft Visual C++ 14.0 or greater is required.
ERROR: Failed building wheel for pyroaring
```

## Why This Happens

The `supabase` library needs `pyroaring` which requires compiling C++ code.
Windows needs **Microsoft C++ Build Tools** (~6GB download) to compile it.

---

## ✅ Solution: Easy Installation (Recommended)

### Method 1: Use Easy Installer (Fastest) ⭐

**Just double-click this file:**
```
install_easy.bat
```

This will:
- Install all packages with pre-built binaries
- Skip problematic compilation
- Take only 2-3 minutes

---

### Method 2: Manual Installation

Open **Command Prompt** in this folder and run:

```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Install core packages
pip install streamlit pandas openpyxl pypdf python-dotenv httpx

# Install supabase (use pre-built binaries)
pip install --prefer-binary supabase
```

---

### Method 3: Install One by One

**Double-click:**
```
install_dependencies.bat
```

This installs packages one by one with detailed progress.

---

## After Installation

Test if it works:

```bash
python check_connection.py
```

Expected output:
```
[1/5] Checking dependencies...
OK: supabase library found
...
SUCCESS: All checks passed!
```

---

## Alternative: Install C++ Build Tools (Not Recommended)

If you really want to install the C++ compiler (takes ~6GB space):

1. Download: https://visualstudio.microsoft.com/visual-cpp-build-tools/
2. Install "Desktop development with C++"
3. Restart computer
4. Run: `pip install -r requirements_cloud.txt`

**Note:** This is overkill for our app. Use Method 1 instead.

---

## Troubleshooting

### "pip is not recognized"
```bash
python -m pip install --upgrade pip
```

### "Permission denied"
Run Command Prompt as Administrator:
1. Search "cmd" in Start menu
2. Right-click → Run as administrator
3. Navigate to project folder
4. Run the commands again

### Still not working?
Try installing Python again:
1. Uninstall current Python
2. Download from: https://www.python.org/downloads/
3. During installation:
   - Check "Add Python to PATH"
   - Choose "Customize installation"
   - Check all optional features
4. Install and restart computer

---

## Quick Fix Summary

1. **Double-click:** `install_easy.bat`
2. Wait for installation (2-3 minutes)
3. Run: `python check_connection.py`
4. If success, run: `python check_connection.py` or `run_app.bat`

---

## Need Help?

If you're still stuck:
1. Take a screenshot of the error
2. Copy the full error message
3. Let me know which method you tried

I'm here to help! 🚀
