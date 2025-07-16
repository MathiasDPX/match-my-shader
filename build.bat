@echo off
cd game

echo Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install requirements.
    pause
    exit /b 1
)

pyinstaller ^
    -D main.py ^
    -n match_my_shader ^
    --add-data "challenges;challenges" ^
    --add-data "docs;docs" ^
    --add-data "icon.ico;." ^
    --icon "icon.ico" ^
    --noconsole ^
    --clean

echo Build complete!
pause