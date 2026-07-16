#!/bin/bash
# ============================================================
# Opal Language - Termux Installation Script
# سكريبت تثبيت لغة أوبال على Termux
# ============================================================
# Usage / الاستخدام:
#   curl -sL https://raw.githubusercontent.com/gcode4421-oss/Opal-/main/install_termux.sh | bash
#   أو: bash install_termux.sh
# ============================================================

set -e

echo "============================================"
echo "  Installing Opal Language on Termux"
echo "  تثبيت لغة أوبال على Termux"
echo "============================================"
echo ""

# Detect Python command (prefer python3, fall back to python)
# كشف أمر بايثون (تفضيل python3، الرجوع إلى python)
detect_python() {
    if command -v python3 &>/dev/null; then
        echo "python3"
    elif command -v python &>/dev/null; then
        echo "python"
    else
        echo ""
    fi
}

# Check if running on Termux / التحقق من Termux
IS_TERMUX=false
if [ -n "$PREFIX" ] && [[ "$PREFIX" == *com.termux* ]]; then
    IS_TERMUX=true
elif [ -d "/data/data/com.termux" ]; then
    IS_TERMUX=true
fi

if [ "$IS_TERMUX" = true ]; then
    echo "Detected: Termux environment / بيئة Termux مكتشفة"
else
    echo "Warning: This script is designed for Termux."
    echo "تحذير: هذا السكريبت مصمم لـ Termux."
    echo "Continuing anyway... / المتابعة على أي حال..."
fi
echo ""

# Step 1: Install Python if missing / تثبيت بايثون إذا لم يكن موجوداً
echo "[1/7] Installing Python / تثبيت بايثون..."
if [ "$IS_TERMUX" = true ]; then
    pkg update -y >/dev/null 2>&1 || true
    pkg install -y python git >/dev/null 2>&1 || {
        echo "Failed to install python via pkg / فشل تثبيت بايثون عبر pkg"
        exit 1
    }
fi

# Detect Python again after install / كشف بايثون مرة أخرى بعد التثبيت
PYTHON_CMD=$(detect_python)
if [ -z "$PYTHON_CMD" ]; then
    echo "Error: Python not found / خطأ: بايثون غير موجود"
    echo "Please install Python 3 manually / يرجى تثبيت بايثون 3 يدوياً"
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1)
echo "Found: $PYTHON_VERSION (using: $PYTHON_CMD)"
echo ""

# Step 2: Ensure pip is available / التأكد من توفر pip
echo "[2/7] Checking pip / التحقق من pip..."
if ! $PYTHON_CMD -m pip --version >/dev/null 2>&1; then
    echo "Installing pip... / تثبيت pip..."
    if [ "$IS_TERMUX" = true ]; then
        pkg install -y python-pip >/dev/null 2>&1 || true
    fi
    # Try ensurepip as fallback
    $PYTHON_CMD -m ensurepip --default-pip >/dev/null 2>&1 || true
fi

if $PYTHON_CMD -m pip --version >/dev/null 2>&1; then
    echo "pip is available / pip متاح"
else
    echo "Warning: pip not available / تحذير: pip غير متاح"
fi
echo ""

# Step 3: Install git if missing / تثبيت git إذا لم يكن موجوداً
echo "[3/7] Checking git / التحقق من git..."
if ! command -v git &>/dev/null; then
    if [ "$IS_TERMUX" = true ]; then
        pkg install -y git >/dev/null 2>&1 || true
    fi
fi
if command -v git &>/dev/null; then
    echo "git is available / git متاح"
else
    echo "Warning: git not available / تحذير: git غير متاح"
    echo "Will try to download without git / سأحاول التنزيل بدون git"
fi
echo ""

# Step 4: Clone or update repository / استنساخ أو تحديث المستودع
INSTALL_DIR="$HOME/opal"
echo "[4/7] Downloading Opal / تنزيل أوبال..."
if [ -d "$INSTALL_DIR/.git" ]; then
    echo "Updating existing installation... / تحديث التثبيت الحالي..."
    cd "$INSTALL_DIR"
    git pull >/dev/null 2>&1 || echo "Warning: git pull failed, continuing / تحذير: فشل git pull، المتابعة"
elif [ -d "$INSTALL_DIR" ]; then
    echo "Directory exists but not a git repo. Removing... / المجلد موجود لكنه ليس مستودع git. حذف..."
    rm -rf "$INSTALL_DIR"
    git clone https://github.com/gcode4421-oss/Opal-.git "$INSTALL_DIR" 2>/dev/null || {
        echo "Failed to clone repository / فشل استنساخ المستودع"
        echo "Please download manually from: https://github.com/gcode4421-oss/Opal-"
        exit 1
    }
else
    if command -v git &>/dev/null; then
        git clone https://github.com/gcode4421-oss/Opal-.git "$INSTALL_DIR" 2>/dev/null || {
            echo "Failed to clone repository / فشل استنساخ المستودع"
            exit 1
        }
    else
        echo "Error: git is required to download Opal / خطأ: git مطلوب لتنزيل أوبال"
        exit 1
    fi
fi

cd "$INSTALL_DIR"
echo ""

# Step 5: Install Opal package / تثبيت حزمة أوبال
echo "[5/7] Installing Opal package / تثبيت حزمة أوبال..."
INSTALL_SUCCESS=false

# Try multiple installation methods / تجربة طرق تثبيت متعددة
# Method 1: --user (preferred, works on most systems)
if ! $INSTALL_SUCCESS; then
    $PYTHON_CMD -m pip install -e . --user >/dev/null 2>&1 && INSTALL_SUCCESS=true
fi

# Method 2: --break-system-packages (newer pip on externally-managed systems)
if ! $INSTALL_SUCCESS; then
    $PYTHON_CMD -m pip install -e . --break-system-packages >/dev/null 2>&1 && INSTALL_SUCCESS=true
fi

# Method 3: plain install
if ! $INSTALL_SUCCESS; then
    $PYTHON_CMD -m pip install -e . >/dev/null 2>&1 && INSTALL_SUCCESS=true
fi

if [ "$INSTALL_SUCCESS" = true ]; then
    echo "Package installed successfully / تم تثبيت الحزمة بنجاح"
else
    echo "Warning: pip install failed, will use direct script / تحذير: فشل تثبيت pip، سيستخدم سكريبت مباشر"
fi
echo ""

# Step 6: Create the opal command / إنشاء أمر opal
echo "[6/7] Setting up opal command / إعداد أمر opal..."

# Make sure main.py is executable / التأكد من أن main.py قابل للتنفيذ
chmod +x "$INSTALL_DIR/opal/main.py"
chmod +x "$INSTALL_DIR/opal_cli"
chmod +x "$INSTALL_DIR/bin/opal"

# Create the opal wrapper script that uses the correct Python
# إنشاء سكريبت opal wrapper الذي يستخدم بايثون الصحيح
OPAL_WRAPPER="$HOME/.local/bin/opal"
mkdir -p "$(dirname "$OPAL_WRAPPER")"

cat > "$OPAL_WRAPPER" << 'EOFCMD'
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Opal Language - Universal CLI Wrapper
مشغل لغة أوبال الشامل - يعمل من أي مكان
"""
import sys
import os

def find_opal_main():
    """ابحث عن opal.main / Find opal.main"""
    # Try direct import
    try:
        from opal.main import main
        return main
    except ImportError:
        pass

    # Search common locations
    search_paths = [
        os.path.expanduser('~/.local/lib'),
        '/usr/lib/python3/dist-packages',
        '/usr/local/lib/python3/dist-packages',
    ]

    # Find all python3.X site-packages
    for lib_dir in ['/usr/lib', '/usr/local/lib', os.path.expanduser('~/.local/lib'),
                    '/data/data/com.termux/files/usr/lib']:
        if os.path.isdir(lib_dir):
            for entry in os.listdir(lib_dir):
                if entry.startswith('python3'):
                    sp = os.path.join(lib_dir, entry, 'site-packages')
                    if os.path.isdir(sp) and sp not in search_paths:
                        search_paths.append(sp)

    for path in search_paths:
        if path and os.path.isdir(path) and path not in sys.path:
            sys.path.insert(0, path)
            try:
                from opal.main import main
                return main
            except ImportError:
                continue

    # Try home opal installation
    home_opal = os.path.expanduser('~/opal')
    if os.path.isdir(home_opal) and home_opal not in sys.path:
        sys.path.insert(0, home_opal)
        try:
            from opal.main import main
            return main
        except ImportError:
            pass

    return None


def main():
    main_func = find_opal_main()
    if main_func is None:
        print("❌ Error: Opal language not found!", file=sys.stderr)
        print("خطأ: لغة أوبال غير موجودة!", file=sys.stderr)
        print("", file=sys.stderr)
        print("To install Opal:", file=sys.stderr)
        print("  pip install opal-lang", file=sys.stderr)
        print("  # أو:", file=sys.stderr)
        print("  pip install git+https://github.com/gcode4421-oss/Opal-.git", file=sys.stderr)
        sys.exit(1)
    sys.exit(main_func())


if __name__ == '__main__':
    main()
EOFCMD
chmod +x "$OPAL_WRAPPER"

# Also try to install to Termux's bin (if accessible)
# أيضاً محاولة التثبيت في مجلد bin الخاص بـ Termux (إذا كان متاحاً)
TERMUX_BIN=""
if [ -n "$PREFIX" ] && [ -d "$PREFIX/bin" ] && [ -w "$PREFIX/bin" ]; then
    TERMUX_BIN="$PREFIX/bin"
elif [ -w "/data/data/com.termux/files/usr/bin" ]; then
    TERMUX_BIN="/data/data/com.termux/files/usr/bin"
fi

if [ -n "$TERMUX_BIN" ]; then
    cp "$OPAL_WRAPPER" "$TERMUX_BIN/opal"
    chmod +x "$TERMUX_BIN/opal"
    echo "Installed to: $TERMUX_BIN/opal"
fi

echo "Installed to: $OPAL_WRAPPER"
echo ""

# Step 7: Update PATH / تحديث PATH
echo "[7/7] Updating PATH / تحديث PATH..."
USER_BIN="$HOME/.local/bin"
NEEDS_PATH_UPDATE=false
if [[ ":$PATH:" != *":$USER_BIN:"* ]]; then
    NEEDS_PATH_UPDATE=true
fi

if [ "$NEEDS_PATH_UPDATE" = true ]; then
    # Detect shell config file / كشف ملف إعداد الشيل
    SHELL_RC=""
    if [ -f "$HOME/.bashrc" ]; then
        SHELL_RC="$HOME/.bashrc"
    elif [ -f "$HOME/.zshrc" ]; then
        SHELL_RC="$HOME/.zshrc"
    elif [ -n "$BASH_VERSION" ]; then
        SHELL_RC="$HOME/.bashrc"
    fi

    if [ -n "$SHELL_RC" ]; then
        echo "Adding $USER_BIN to PATH in $SHELL_RC"
        echo "export PATH=\"$USER_BIN:\$PATH\"" >> "$SHELL_RC"
    fi
    export PATH="$USER_BIN:$PATH"
fi
echo ""

# Verify installation / التحقق من التثبيت
echo "============================================"
echo "  Installation Complete! / اكتمل التثبيت!"
echo "============================================"
echo ""

# Test the installation / اختبار التثبيت
echo "Testing installation... / اختبار التثبيت..."
if "$OPAL_WRAPPER" --version >/dev/null 2>&1; then
    OPAL_VERSION=$("$OPAL_WRAPPER" --version 2>&1)
    echo "✓ $OPAL_VERSION"
else
    echo "✗ Warning: opal command test failed / تحذير: فشل اختبار أمر opal"
    echo "  Trying direct Python invocation... / محاولة استدعاء بايثون مباشرة..."
    if $PYTHON_CMD "$INSTALL_DIR/opal/main.py" --version >/dev/null 2>&1; then
        echo "✓ Direct invocation works / الاستدعاء المباشر يعمل"
    else
        echo "✗ Error: Installation verification failed / خطأ: فشل التحقق من التثبيت"
        exit 1
    fi
fi

echo ""
echo "Usage / الاستخدام:"
echo "  opal file.op              Run an Opal file / تشغيل ملف"
echo "  opal --repl               Interactive REPL / واجهة تفاعلية"
echo "  opal --help               Show help / عرض المساعدة"
echo "  opal file.op --compile-c  Transpile to C / تحويل إلى C"
echo ""

if [ "$NEEDS_PATH_UPDATE" = true ]; then
    echo "⚠️  Important / مهم:"
    echo "   Run this command to use opal immediately:"
    echo "   شغل هذا الأمر لاستخدام opal فوراً:"
    echo ""
    echo "   export PATH=\"$USER_BIN:\$PATH\""
    echo ""
    echo "   Or restart your terminal / أو أعد تشغيل الطرفية"
    echo ""
fi

echo "Quick test / اختبار سريع:"
echo '  echo "مرحبا بالعالم!" > test.op'
echo "  opal test.op"
echo ""
echo "Enjoy Opal! / استمتع بأوبال!"
echo ""
echo "Repository: https://github.com/gcode4421-oss/Opal-"
