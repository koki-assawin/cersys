@echo off
echo ====================================================
echo Easy Installation (Skipping problematic packages)
echo ====================================================
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found
    pause
    exit /b 1
)

echo Installing core packages...
pip install --upgrade pip
pip install streamlit pandas openpyxl pypdf python-dotenv httpx

echo.
echo Installing supabase (without optional dependencies)...
pip install --prefer-binary supabase

echo.
echo ====================================================
echo Installation Complete!
echo ====================================================
echo.
echo Testing connection...
python check_connection.py
pause
