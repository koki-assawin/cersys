@echo off
echo ====================================================
echo Opening Setup Files
echo ====================================================
echo.

REM เปิดไฟล์คำแนะนำ
echo Opening NEXT_STEP.txt...
start notepad NEXT_STEP.txt

REM รอ 1 วินาที
timeout /t 1 /nobreak >nul

REM เปิดไฟล์ SQL
echo Opening setup_database_v2.sql...
start notepad setup_database_v2.sql

echo.
echo Files opened in Notepad.
echo Please follow the instructions in NEXT_STEP.txt
echo.
pause
