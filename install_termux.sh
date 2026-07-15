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

# Check if running on Termux / التحقق من Termux
if [ ! -d "/data/data/com.termux" ]; then
    echo "Warning: This script is designed for Termux."
    echo "تحذير: هذا السكريبت مصمم لـ Termux."
    echo "Continuing anyway... / المتابعة على أي حال..."
fi

# Update packages / تحديث الحزم
echo "[1/6] Updating packages / تحديث الحزم..."
pkg update -y >/dev/null 2>&1 || true
pkg install -y python python-pip git >/dev/null 2>&1 || {
    echo "Installing python... / تثبيت بايثون..."
    pkg install -y python
    pkg install -y python-pip
}

# Check python / التحقق من بايثون
echo "[2/6] Checking Python / التحقق من بايثون..."
if ! command -v python &>/dev/null; then
    echo "Error: Python not found / خطأ: بايثون غير موجود"
    exit 1
fi

PYTHON_VERSION=$(python --version 2>&1)
echo "Found: $PYTHON_VERSION"

# Install pip if missing / تثبيت pip إذا لم يكن موجوداً
echo "[3/6] Ensuring pip is available / التأكد من توفر pip..."
python -m pip --version >/dev/null 2>&1 || {
    echo "Installing pip... / تثبيت pip..."
    pkg install -y python-pip
}

# Clone or update repository / استنساخ أو تحديث المستودع
INSTALL_DIR="$HOME/opal"
echo "[4/6] Downloading Opal / تنزيل أوبال..."
if [ -d "$INSTALL_DIR" ]; then
    echo "Updating existing installation... / تحديث التثبيت الحالي..."
    cd "$INSTALL_DIR"
    git pull >/dev/null 2>&1 || true
else
    git clone https://github.com/gcode4421-oss/Opal-.git "$INSTALL_DIR" 2>/dev/null || {
        echo "Failed to clone repository / فشل استنساخ المستودع"
        echo "Please download manually from: https://github.com/gcode4421-oss/Opal-"
        exit 1
    }
fi

cd "$INSTALL_DIR"

# Install Opal / تثبيت أوبال
echo "[5/6] Installing Opal / تثبيت أوبال..."
python -m pip install -e . --break-system-packages 2>/dev/null || \
python -m pip install -e . --user 2>/dev/null || \
python -m pip install -e .

# Create symlink / إنشاء رابط رمزي
echo "[6/6] Setting up opal command / إعداد أمر opal..."
TERMUX_BIN="$PREFIX/bin"
if [ -d "$TERMUX_BIN" ] && [ -w "$TERMUX_BIN" ]; then
    ln -sf "$INSTALL_DIR/opal/main.py" "$TERMUX_BIN/opal"
    chmod +x "$TERMUX_BIN/opal"
fi

# Also create user-level symlink / رابط على مستوى المستخدم
USER_BIN="$HOME/.local/bin"
mkdir -p "$USER_BIN"
cat > "$USER_BIN/opal" << 'EOF'
#!/bin/bash
exec python3 "$HOME/opal/opal/main.py" "$@"
EOF
chmod +x "$USER_BIN/opal"

# Add to PATH if not there / إضافة إلى PATH
if [[ ":$PATH:" != *":$USER_BIN:"* ]]; then
    echo ""
    echo "Adding ~/.local/bin to PATH in ~/.bashrc"
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
    export PATH="$USER_BIN:$PATH"
fi

# Verify installation / التحقق من التثبيت
echo ""
echo "============================================"
echo "  Installation Complete! / اكتمل التثبيت!"
echo "============================================"
echo ""

if command -v opal &>/dev/null; then
    echo "Opal version: $(opal --version 2>&1)"
    echo ""
    echo "Usage / الاستخدام:"
    echo "  opal file.op              Run an Opal file / تشغيل ملف"
    echo "  opal --repl               Interactive REPL / واجهة تفاعلية"
    echo "  opal --help               Show help / عرض المساعدة"
    echo ""
    echo "Quick test / اختبار سريع:"
    echo '  echo "مرحبا بالعالم!" > test.op'
    echo "  opal test.op"
    echo ""
    echo "Enjoy Opal! / استمتع بأوبال!"
else
    echo "To use opal, run: source ~/.bashrc"
    echo "Or use: python3 ~/opal/opal/main.py file.op"
fi
