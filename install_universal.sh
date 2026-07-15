#!/bin/bash
# ============================================================
# Opal Language - Universal Installation Script (Auto-detect OS)
# سكريبت تثبيت شامل (كشف تلقائي للنظام)
# ============================================================
# This script automatically detects your operating system
# and installs Opal accordingly.
# هذا السكريبت يكتشف نظام التشغيل تلقائياً ويثبت أوبال
# ============================================================

set -e

echo "============================================"
echo "  Opal Language - Universal Installer"
echo "  المثبت الشامل للغة أوبال"
echo "============================================"
echo ""

# Detect operating system / كشف نظام التشغيل
detect_os() {
    if [ -d "/data/data/com.termux" ]; then
        echo "termux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "linux"
    elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
        echo "windows"
    else
        echo "unknown"
    fi
}

OS=$(detect_os)
echo "Detected system: $OS / النظام المكتشف: $OS"
echo ""

case "$OS" in
    termux)
        echo "Running Termux installer... / تشغيل مثبت Termux..."
        bash "$(dirname "$0")/install_termux.sh"
        ;;
    linux|macos)
        echo "Running Unix installer... / تشغيل مثبت Unix..."
        bash "$(dirname "$0")/install.sh"
        ;;
    windows)
        echo "On Windows, please run: install_windows.bat"
        echo "على ويندوز، يرجى تشغيل: install_windows.bat"
        exit 1
        ;;
    *)
        echo "Unknown operating system: $OSTYPE"
        echo "نظام تشغيل غير معروف: $OSTYPE"
        echo ""
        echo "Please install manually / يرجى التثبيت يدوياً:"
        echo "  1. Install Python 3.8+ / تثبيت بايثون 3.8+"
        echo "  2. git clone https://github.com/gcode4421-oss/Opal-.git"
        echo "  3. cd Opal-"
        echo "  4. pip install -e ."
        exit 1
        ;;
esac
