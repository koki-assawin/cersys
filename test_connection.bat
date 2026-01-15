@echo off
echo ====================================================
echo Testing Supabase Connection
echo ====================================================
echo.

REM Check if Python is installed
echo [1/3] Checking Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found
    echo.
    echo Please install Python from:
    echo https://www.python.org/downloads/
    echo.
    echo IMPORTANT: Select "Add Python to PATH" during installation!
    pause
    exit /b 1
)
echo OK: Python found
python --version
echo.

REM Check if dependencies are installed
echo [2/3] Checking Dependencies...
python -c "import supabase" >nul 2>&1
if %errorlevel% neq 0 (
    echo Dependencies not found. Installing...
    echo.
    echo This may take 2-3 minutes. Please wait...
    echo.

    REM Use easy installation method
    pip install --quiet --upgrade pip
    pip install --quiet streamlit pandas openpyxl pypdf python-dotenv httpx
    pip install --quiet --prefer-binary supabase

    if %errorlevel% neq 0 (
        echo.
        echo ERROR: Installation failed
        echo.
        echo Please try running: install_easy.bat
        echo Or read: FIX_INSTALLATION_ERROR.md
        pause
        exit /b 1
    )
    echo.
    echo OK: Dependencies installed successfully
) else (
    echo OK: Dependencies ready
)
echo.

REM Run connection test
echo [3/3] Testing connection...
echo.
python check_connection.py
echo.

echo ====================================================
echo Test completed
echo ====================================================
echo.
pause
