#!/bin/bash
# ============================================================
# Opal Language - Linux/macOS Installation Script
# سكريبت تثبيت لغة أوبال على لينكس وماك
# ============================================================
# Usage / الاستخدام:
#   curl -sL https://raw.githubusercontent.com/gcode4421-oss/Opal-/main/install.sh | bash
#   أو: bash install.sh
# ============================================================

set -e

echo "============================================"
echo "  Installing Opal Language"
echo "  تثبيت لغة أوبال"
echo "============================================"
echo ""

# Detect OS / كشف نظام التشغيل
OS="unknown"
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
fi

echo "Detected OS: $OS / نظام التشغيل: $OS"
echo ""

# Check Python 3 / التحقق من بايثون 3
echo "[1/5] Checking Python 3 / التحقق من بايثون 3..."
if command -v python3 &>/dev/null; then
    PYTHON_CMD="python3"
elif command -v python &>/dev/null; then
    PYTHON_CMD="python"
else
    echo "Python 3 not found. Installing... / بايثون 3 غير موجود. جاري التثبيت..."
    if [ "$OS" = "macos" ]; then
        if command -v brew &>/dev/null; then
            brew install python
        else
            echo "Please install Python 3 first: https://www.python.org/downloads/"
            exit 1
        fi
    else
        # Try various package managers / تجربة مديري الحزم
        sudo apt-get update -y >/dev/null 2>&1 && sudo apt-get install -y python3 python3-pip >/dev/null 2>&1 || \
        sudo yum install -y python3 python3-pip >/dev/null 2>&1 || \
        sudo dnf install -y python3 python3-pip >/dev/null 2>&1 || \
        sudo pacman -S --noconfirm python python-pip >/dev/null 2>&1 || {
            echo "Could not install Python automatically / تعذر تثبيت بايثون تلقائياً"
            echo "Please install Python 3 manually / يرجى تثبيت بايثون 3 يدوياً"
            exit 1
        }
    fi
    PYTHON_CMD="python3"
fi

echo "Python: $($PYTHON_CMD --version 2>&1)"

# Ensure pip is available / التأكد من توفر pip
echo ""
echo "[2/5] Checking pip / التحقق من pip..."
$PYTHON_CMD -m pip --version >/dev/null 2>&1 || {
    echo "Installing pip... / تثبيت pip..."
    if [ "$OS" = "macos" ]; then
        curl https://bootstrap.pypa.io/get-pip.py -o /tmp/get-pip.py
        $PYTHON_CMD /tmp/get-pip.py --user
    else
        sudo apt-get install -y python3-pip >/dev/null 2>&1 || \
        sudo yum install -y python3-pip >/dev/null 2>&1 || true
    fi
}

# Install git if missing / تثبيت git إذا لم يكن موجوداً
echo ""
echo "[3/5] Checking git / التحقق من git..."
if ! command -v git &>/dev/null; then
    echo "Installing git... / تثبيت git..."
    if [ "$OS" = "macos" ]; then
        brew install git >/dev/null 2>&1 || true
    else
        sudo apt-get install -y git >/dev/null 2>&1 || \
        sudo yum install -y git >/dev/null 2>&1 || true
    fi
fi

# Clone repository / استنساخ المستودع
INSTALL_DIR="$HOME/opal"
echo ""
echo "[4/5] Downloading Opal / تنزيل أوبال..."
if [ -d "$INSTALL_DIR" ]; then
    echo "Updating existing installation... / تحديث التثبيت الحالي..."
    cd "$INSTALL_DIR"
    git pull >/dev/null 2>&1 || true
else
    git clone https://github.com/gcode4421-oss/Opal-.git "$INSTALL_DIR" 2>/dev/null || {
        echo "Failed to clone repository / فشل استنساخ المستودع"
        exit 1
    }
fi

cd "$INSTALL_DIR"

# Make all entry points executable / جعل جميع نقاط الدخول قابلة للتنفيذ
chmod +x opal/main.py opal_cli bin/opal install.sh install_termux.sh install_universal.sh 2>/dev/null || true

# Install / التثبيت
echo ""
echo "[5/5] Installing Opal package / تثبيت حزمة أوبال..."
$PYTHON_CMD -m pip install -e . --user 2>/dev/null || \
$PYTHON_CMD -m pip install -e . --break-system-packages 2>/dev/null || \
$PYTHON_CMD -m pip install -e .

# Setup user bin / إعداد مجلد المستخدم
USER_BIN="$HOME/.local/bin"
mkdir -p "$USER_BIN"

# Copy the universal wrapper from bin/opal
# نسخ المشغل الشامل من bin/opal
cp "$INSTALL_DIR/bin/opal" "$USER_BIN/opal"
chmod +x "$USER_BIN/opal"

# Try system-wide install / محاولة التثبيت على مستوى النظام
if [ -w "/usr/local/bin" ]; then
    cp "$USER_BIN/opal" "/usr/local/bin/opal"
    chmod +x "/usr/local/bin/opal"
fi

# Add to PATH / إضافة إلى PATH
if [[ ":$PATH:" != *":$USER_BIN:"* ]]; then
    SHELL_NAME=$(basename "$SHELL")
    if [ "$SHELL_NAME" = "bash" ]; then
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
    elif [ "$SHELL_NAME" = "zsh" ]; then
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.zshrc"
    fi
    export PATH="$USER_BIN:$PATH"
fi

# Verify / التحقق
echo ""
echo "============================================"
echo "  Installation Complete! / اكتمل التثبيت!"
echo "============================================"

if command -v opal &>/dev/null; then
    echo ""
    echo "Opal version: $(opal --version 2>&1)"
    echo ""
    echo "Quick test / اختبار سريع:"
    echo '  echo "Hello, Opal!" > test.op && opal test.op'
else
    echo ""
    echo "Please restart your terminal or run: source ~/.bashrc"
    echo "ثم جرب: opal --version"
fi

echo ""
echo "Documentation: https://github.com/gcode4421-oss/Opal-"
echo "Enjoy Opal! / استمتع بأوبال!"
