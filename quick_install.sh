#!/bin/bash
# ============================================================
# Opal Language - One-Line Installer
# مثبّت لغة أوبال بأمر واحد
# ============================================================
# 
# Usage / الاستخدام:
#   curl -sL https://raw.githubusercontent.com/gcode4421-oss/Opal-/main/quick_install.sh | bash
#   أو: bash quick_install.sh
#
# This script installs Opal from GitHub (no PyPI needed!)
# هذا السكريبت يثبّت أوبال من GitHub (بدون حاجة لـ PyPI!)
# ============================================================

set -e

echo "============================================"
echo "  Installing Opal Language v2.1.0"
echo "  تثبيت لغة أوبال 2.1.0"
echo "============================================"
echo ""

# Detect Python / كشف بايثون
detect_python() {
    if command -v python3 &>/dev/null; then
        echo "python3"
    elif command -v python &>/dev/null; then
        echo "python"
    else
        echo ""
    fi
}

PYTHON_CMD=$(detect_python)
if [ -z "$PYTHON_CMD" ]; then
    echo "❌ Python 3 not found / خطأ: بايثون 3 غير موجود"
    echo "Please install Python 3.8+ from https://python.org"
    exit 1
fi

echo "Python: $($PYTHON_CMD --version 2>&1)"
echo ""

# Install pip if needed / تثبيت pip إذا لزم
if ! $PYTHON_CMD -m pip --version >/dev/null 2>&1; then
    echo "Installing pip... / تثبيت pip..."
    $PYTHON_CMD -m ensurepip --user 2>/dev/null || true
fi

echo "[1/3] Installing Opal from GitHub / تثبيت أوبال من GitHub..."
echo ""

# Try multiple installation methods / تجربة طرق تثبيت متعددة
INSTALL_SUCCESS=false

# Method 1: Direct from GitHub / الطريقة 1: مباشرة من GitHub
if ! $INSTALL_SUCCESS; then
    echo "  Trying: pip install from GitHub..."
    if $PYTHON_CMD -m pip install "git+https://github.com/gcode4421-oss/Opal-.git" 2>/dev/null; then
        INSTALL_SUCCESS=true
        echo "  ✓ Installed from GitHub"
    fi
fi

# Method 2: From release wheel / الطريقة 2: من ملف الـ wheel المنشور
if ! $INSTALL_SUCCESS; then
    echo "  Trying: install from release wheel..."
    WHEEL_URL="https://github.com/gcode4421-oss/Opal-/releases/download/v2.1.0/opal_lang-2.1.0-py3-none-any.whl"
    if $PYTHON_CMD -m pip install "$WHEEL_URL" 2>/dev/null; then
        INSTALL_SUCCESS=true
        echo "  ✓ Installed from release wheel"
    fi
fi

# Method 3: With --user flag / الطريقة 3: مع --user
if ! $INSTALL_SUCCESS; then
    echo "  Trying: install with --user..."
    WHEEL_URL="https://github.com/gcode4421-oss/Opal-/releases/download/v2.1.0/opal_lang-2.1.0-py3-none-any.whl"
    if $PYTHON_CMD -m pip install "$WHEEL_URL" --user 2>/dev/null; then
        INSTALL_SUCCESS=true
        echo "  ✓ Installed with --user"
    fi
fi

# Method 4: With --break-system-packages / الطريقة 4: مع --break-system-packages
if ! $INSTALL_SUCCESS; then
    echo "  Trying: install with --break-system-packages..."
    WHEEL_URL="https://github.com/gcode4421-oss/Opal-/releases/download/v2.1.0/opal_lang-2.1.0-py3-none-any.whl"
    if $PYTHON_CMD -m pip install "$WHEEL_URL" --break-system-packages 2>/dev/null; then
        INSTALL_SUCCESS=true
        echo "  ✓ Installed with --break-system-packages"
    fi
fi

# Method 5: Download and install / الطريقة 5: تحميل وتثبيت
if ! $INSTALL_SUCCESS; then
    echo "  Trying: download and install..."
    TMPDIR=$(mktemp -d)
    if curl -sL -o "$TMPDIR/opal.whl" "https://github.com/gcode4421-oss/Opal-/releases/download/v2.1.0/opal_lang-2.1.0-py3-none-any.whl"; then
        if $PYTHON_CMD -m pip install "$TMPDIR/opal.whl" 2>/dev/null; then
            INSTALL_SUCCESS=true
            echo "  ✓ Installed from downloaded wheel"
        fi
    fi
    rm -rf "$TMPDIR"
fi

if [ "$INSTALL_SUCCESS" != true ]; then
    echo ""
    echo "❌ Installation failed / فشل التثبيت"
    echo ""
    echo "Manual installation / التثبيت اليدوي:"
    echo "  git clone https://github.com/gcode4421-oss/Opal-.git"
    echo "  cd Opal-"
    echo "  pip install ."
    exit 1
fi

echo ""

# Setup opal command / إعداد أمر opal
echo "[2/3] Setting up opal command / إعداد أمر opal..."
USER_BIN="$HOME/.local/bin"
mkdir -p "$USER_BIN"

# Try to create symlink to opal command / محاولة إنشاء رابط لأمر opal
OPAL_SCRIPT=$($PYTHON_CMD -c "import opal; import os; print(os.path.join(os.path.dirname(os.path.dirname(opal.__file__)), 'bin', 'opal'))" 2>/dev/null)

if [ -z "$OPAL_SCRIPT" ] || [ ! -f "$OPAL_SCRIPT" ]; then
    # Find opal executable / البحث عن ملف opal القابل للتنفيذ
    OPAL_PATH=$($PYTHON_CMD -c "
import subprocess, sys
result = subprocess.run([sys.executable, '-m', 'pip', 'show', '-f', 'opal-lang'], 
                       capture_output=True, text=True)
for line in result.stdout.split('\n'):
    if 'bin/opal' in line or 'opal_cli' in line:
        print(line.strip())
        break
" 2>/dev/null)
fi

# Create a simple wrapper if needed / إنشاء wrapper بسيط إذا لزم
if ! command -v opal &>/dev/null; then
    cat > "$USER_BIN/opal" << EOF
#!/bin/bash
exec $PYTHON_CMD -m opal.main "\$@"
EOF
    chmod +x "$USER_BIN/opal"
    echo "  ✓ Created opal wrapper"
fi

# Add to PATH if needed / إضافة إلى PATH إذا لزم
if [[ ":$PATH:" != *":$USER_BIN:"* ]]; then
    SHELL_RC=""
    [ -f "$HOME/.bashrc" ] && SHELL_RC="$HOME/.bashrc"
    [ -f "$HOME/.zshrc" ] && SHELL_RC="$HOME/.zshrc"
    if [ -n "$SHELL_RC" ]; then
        echo "export PATH=\"$USER_BIN:\$PATH\"" >> "$SHELL_RC"
        echo "  ✓ Added to PATH in $SHELL_RC"
    fi
    export PATH="$USER_BIN:$PATH"
fi

echo ""

# Verify installation / التحقق من التثبيت
echo "[3/3] Verifying installation / التحقق من التثبيت..."
if command -v opal &>/dev/null; then
    VERSION=$(opal --version 2>&1)
    echo "  ✓ $VERSION"
else
    # Try direct python call / محاولة استدعاء مباشر
    if $PYTHON_CMD -m opal.main --version >/dev/null 2>&1; then
        VERSION=$($PYTHON_CMD -m opal.main --version 2>&1)
        echo "  ✓ $VERSION (via python -m)"
    else
        echo "  ⚠️  opal command not in PATH yet"
        echo "     Run: export PATH=\"$USER_BIN:\$PATH\""
    fi
fi

echo ""
echo "============================================"
echo "  🎉 Installation Complete!"
echo "  اكتمل التثبيت!"
echo "============================================"
echo ""
echo "Usage / الاستخدام:"
echo "  opal --version              Show version / عرض الإصدار"
echo "  opal file.op                Run a file / تشغيل ملف"
echo "  opal --repl                 Interactive REPL / واجهة تفاعلية"
echo "  opal --help                 Show help / عرض المساعدة"
echo "  opal file.op --compile-c    Convert to C / تحويل إلى C"
echo "  opal file.op --color=always Force colors / إجبار الألوان"
echo ""
echo "Quick test / اختبار سريع:"
echo "  echo 'echo \"Hello, Opal!\"' > test.op"
echo "  opal test.op"
echo ""
echo "Documentation: https://github.com/gcode4421-oss/Opal-"
echo "Enjoy Opal! / استمتع بأوبال! 🚀"
echo ""
