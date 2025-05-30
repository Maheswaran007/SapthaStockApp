@echo off
echo === Cleaning old builds ===
rmdir /s /q dist
rmdir /s /q build
del /q app.spec

echo === Building new EXE ===
pyinstaller --onefile --noconsole --add-data "modules;modules" app.py

IF NOT EXIST "dist\app.exe" (
    echo Build failed. Exiting.
    exit /b 1
)

echo === Compiling Patch Installer ===
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" patch.iss

echo === Done ===
pause
