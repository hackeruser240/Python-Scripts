@echo off

cd C:\Users\HP\OneDrive\Documents\pythonScripts\Py_scripts\latex_cv_template

echo =====================
echo Clean Previous Builds
echo =====================
rmdir /s /q build
rmdir /s /q dist

echo ===========================
echo Activate Python Environment
echo ===========================
call C:\Users\HP\OneDrive\Documents\pythonScripts\Py_scripts\python-env\Scripts\activate.bat


echo =====================
echo Build Executable File
echo =====================
pyinstaller --onefile --noconsole --name "CV Template Deployer" src\gui.py

echo ✅ Build complete!
pause