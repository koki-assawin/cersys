@echo off
echo ====================================================
echo Certificate Download System - Cloud Version
echo ====================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found
    echo.
    echo Please install Python from:
    echo https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check secrets.toml
if not exist ".streamlit\secrets.toml" (
    echo ERROR: .streamlit\secrets.toml not found
    echo.
    echo Please create the file and add your Supabase keys:
    echo   copy .streamlit\secrets.toml.example .streamlit\secrets.toml
    echo   Then edit the file with your URL and KEY
    pause
    exit /b 1
)

echo OK: secrets.toml found
echo.

REM Check Dependencies
echo Checking Dependencies...
python -c "import streamlit, supabase" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing dependencies...
    pip install -r requirements_cloud.txt
)

echo.
echo ====================================================
echo Starting application...
echo ====================================================
echo.
echo Open browser at: http://localhost:8501
echo Press Ctrl+C to stop
echo.

streamlit run app_cloud.py
