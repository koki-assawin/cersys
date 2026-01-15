@echo off
echo ====================================================
echo Fix 404 Error and Setup New Data
echo ====================================================
echo.
echo This script will:
echo   1. Show current database contents
echo   2. Clean old data (if you want)
echo   3. Create test data with correct File IDs
echo.
echo ====================================================
echo.

echo Step 1: Checking current database...
echo.
py CHECK_DATABASE.py
echo.

echo ====================================================
echo.
echo Do you want to clean all old data and start fresh?
echo.
set /p CLEAN="Type YES to clean, or press Enter to skip: "

if /i "%CLEAN%"=="YES" (
    echo.
    echo Cleaning database...
    py CLEAN_DATABASE.py
    echo.
)

echo ====================================================
echo.
echo Setup Complete!
echo.
echo Next steps:
echo   1. Run: run_admin.bat
echo   2. Login: admin / admin123
echo   3. Download Template
echo   4. Fill in your real File IDs
echo   5. Create new event
echo.
echo For detailed instructions, see: FIX_404_ERROR.md
echo.
pause
