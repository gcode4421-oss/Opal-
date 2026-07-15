@echo off
REM ============================================================
REM Opal Language - Windows Installation Script
REM سكريبت تثبيت لغة أوبال على ويندوز
REM ============================================================
REM Usage: Run this file in Command Prompt or PowerShell
REM الاستخدام: شغل هذا الملف في موجه الأوامر أو PowerShell
REM ============================================================

echo ============================================
echo   Installing Opal Language
echo   تثبيت لغة أوبال
echo ============================================
echo.

REM Check Python / التحقق من بايثون
echo [1/4] Checking Python / التحقق من بايثون...
python --version >nul 2>&1
if errorlevel 1 (
    echo Python not found! Please install Python 3.8+ from: https://www.python.org/downloads/
    echo بايثون غير موجود! يرجى تثبيت بايثون 3.8+ من: https://www.python.org/downloads/
    pause
    exit /b 1
)

python --version

REM Check pip / التحقق من pip
echo.
echo [2/4] Checking pip / التحقق من pip...
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo Installing pip... / تثبيت pip...
    python -m ensurepip --default-pip
)

REM Check git / التحقق من git
echo.
echo [3/4] Checking git / التحقق من git...
git --version >nul 2>&1
if errorlevel 1 (
    echo Git not found! Please install Git from: https://git-scm.com/download/win
    echo Git غير موجود! يرجى تثبيت Git من: https://git-scm.com/download/win
    pause
    exit /b 1
)

REM Clone or update / استنساخ أو تحديث
echo.
echo [4/4] Downloading Opal / تنزيل أوبال...
set INSTALL_DIR=%USERPROFILE%\opal

if exist "%INSTALL_DIR%" (
    echo Updating existing installation... / تحديث التثبيت الحالي...
    cd "%INSTALL_DIR%"
    git pull
) else (
    git clone https://github.com/gcode4421-oss/Opal-.git "%INSTALL_DIR%"
)

cd "%INSTALL_DIR%"

REM Install / التثبيت
echo.
echo Installing Opal package / تثبيت حزمة أوبال...
python -m pip install -e .

REM Create opal.bat in user directory / إنشاء ملف تشغيل
echo @echo off > "%USERPROFILE%\opal.bat"
echo python "%INSTALL_DIR%\opal\main.py" %%* >> "%USERPROFILE%\opal.bat"

REM Also try to create in a PATH directory / محاولة وضعه في مسار PATH
echo @echo off > "opal.bat"
echo python "%INSTALL_DIR%\opal\main.py" %%* >> "opal.bat"

echo.
echo ============================================
echo   Installation Complete! / اكتمل التثبيت!
echo ============================================
echo.
echo To use Opal / لاستخدام أوبال:
echo   opal file.op
echo   opal --repl
echo   opal --help
echo.
echo Quick test / اختبار سريع:
echo   echo "Hello, Opal!" ^> test.op
echo   opal test.op
echo.
echo Enjoy Opal! / استمتع بأوبال!
pause
