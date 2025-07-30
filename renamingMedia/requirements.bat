@echo off
REM Activate your virtual environment first
REM Example: call path\to\your\venv\Scripts\activate

echo ===========================================
echo Installing required Python packages...
echo ===========================================

pip install pandas
pip install pyinstaller

echo ===========================================
echo All packages installed.
echo ===========================================
pause