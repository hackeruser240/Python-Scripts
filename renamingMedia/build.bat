@echo off

rem Delete existing build and dist folders if they exist
echo ===========================================
echo Cleaning previous build artifacts...
rmdir /S /Q "build" 2>nul
rmdir /S /Q "dist" 2>nul
echo Cleaning complete.
echo ===========================================

rem Run PyInstaller command
pyinstaller --clean --onefile --noconsole --name="Renaming Media" --add-binary "C:\Users\HP\AppData\Local\Programs\Python\Python312\DLLs\pyexpat.pyd;." --add-data "app_icon.ico;." renamingMedia.py

echo ===========================================
echo Build process finished
echo ===========================================