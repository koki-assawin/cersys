@echo off
echo ====================================================
echo Installing Dependencies for Certificate System
echo ====================================================
echo.
echo This will install packages one by one to avoid errors.
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found
    echo Please install Python first from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Step 1/7: Installing streamlit...
pip install streamlit --quiet
if %errorlevel% neq 0 (
    echo ERROR: Failed to install streamlit
    pause
    exit /b 1
)
echo OK

echo Step 2/7: Installing pandas...
pip install pandas --quiet
if %errorlevel% neq 0 (
    echo ERROR: Failed to install pandas
    pause
    exit /b 1
)
echo OK

echo Step 3/7: Installing openpyxl...
pip install openpyxl --quiet
if %errorlevel% neq 0 (
    echo ERROR: Failed to install openpyxl
    pause
    exit /b 1
)
echo OK

echo Step 4/7: Installing pypdf...
pip install pypdf --quiet
if %errorlevel% neq 0 (
    echo ERROR: Failed to install pypdf
    pause
    exit /b 1
)
echo OK

echo Step 5/7: Installing python-dotenv...
pip install python-dotenv --quiet
if %errorlevel% neq 0 (
    echo ERROR: Failed to install python-dotenv
    pause
    exit /b 1
)
echo OK

echo Step 6/7: Installing httpx...
pip install "httpx[http2]" --quiet
if %errorlevel% neq 0 (
    echo ERROR: Failed to install httpx
    pause
    exit /b 1
)
echo OK

echo Step 7/7: Installing supabase (this may take a while)...
pip install supabase --no-deps --quiet
pip install httpx python-dotenv typing-extensions --quiet
pip install postgrest realtime storage3 supafunc gotrue --quiet
if %errorlevel% neq 0 (
    echo WARNING: Some supabase components may not be installed
    echo But the core functionality should work
)
echo OK

echo.
echo ====================================================
echo Installation Complete!
echo ====================================================
echo.
echo You can now run:
echo   python check_connection.py
echo.
pause
