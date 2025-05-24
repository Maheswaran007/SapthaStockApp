@echo off
REM Step 1: Build app.exe with PyInstaller
pyinstaller --onedir --windowed app.py

REM Step 2: Build installer with Inno Setup
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" SapthaStockAppInstaller.iss

echo Build completed! Installer is in output folder.
pause
