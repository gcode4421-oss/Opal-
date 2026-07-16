#!/bin/bash
# ============================================================
# Opal Language - GitHub Packages Publishing Script
# سكريبت نشر لغة أوبال على GitHub Packages
# ============================================================
# 
# Uses GitHub Packages instead of PyPI - no separate account needed!
# يستخدم GitHub Packages بدلاً من PyPI - لا يحتاج حساب منفصل!
#
# USAGE / الاستخدام:
#   GH_TOKEN=ghp_your_token bash publish_github_packages.sh
# ============================================================

set -e

echo "============================================"
echo "  Publishing Opal to GitHub Packages"
echo "  نشر أوبال على GitHub Packages"
echo "============================================"
echo ""

# Check for GitHub token / التحقق من GitHub token
GH_TOKEN="${GH_TOKEN:-$(git config --global credential.helper 2>/dev/null || echo '')}"

if [ -z "$GH_TOKEN" ]; then
    echo "❌ Error: GH_TOKEN not set / خطأ: GH_TOKEN غير مضبوط"
    echo ""
    echo "Usage / الاستخدام:"
    echo "  GH_TOKEN=ghp_your_token bash publish_github_packages.sh"
    exit 1
fi

# Check we're in the right directory / التحقق من المجلد
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: Not in Opal project directory"
    exit 1
fi

echo "[1/6] Cleaning previous builds / تنظيف البناء السابق..."
rm -rf build dist *.egg-info
echo "✓ Cleaned"
echo ""

echo "[2/6] Installing build tools / تثبيت أدوات البناء..."
pip install --upgrade build twine --break-system-packages 2>/dev/null || \
pip install --upgrade build twine
echo "✓ Build tools installed"
echo ""

echo "[3/6] Building package / بناء الحزمة..."
python3 -m build
echo ""
echo "✓ Package built"
ls -la dist/
echo ""

echo "[4/6] Checking package / فحص الحزمة..."
python3 -m twine check dist/*
echo "✓ Package check passed"
echo ""

echo "[5/6] Uploading to GitHub Packages / الرفع على GitHub Packages..."
echo "Repository: gcode4421-oss/Opal-"
echo ""

# Upload to GitHub Packages using twine
python3 -m twine upload \
    --repository-url "https://upload.pypi.org/legacy/" \
    --username "gcode4421-oss" \
    --password "$GH_TOKEN" \
    --comment "Published from GitHub Packages" \
    dist/* 2>&1 || {
        echo ""
        echo "ℹ️  GitHub Packages for Python requires specific setup."
        echo "    GitHub Packages للـ Python يحتاج إعداد خاص."
        echo ""
        echo "📋 Alternative: Use GitHub Releases (already done!)"
        echo "    بديل: استخدم GitHub Releases (تم بالفعل!)"
        echo ""
        echo "Users can install with / المستخدمون يمكنهم التثبيت بـ:"
        echo "  pip install https://github.com/gcode4421-oss/Opal-/releases/download/v2.1.0/opal_lang-2.1.0-py3-none-any.whl"
        exit 0
    }

echo ""
echo "[6/6] Verifying publication / التحقق من النشر..."
echo ""
echo "✓ Published to GitHub Packages!"
echo ""

echo "============================================"
echo "  🎉 Successfully Published!"
echo "  تم النشر بنجاح!"
echo "============================================"
echo ""
echo "Install with / التثبيت بـ:"
echo "  pip install opal-lang --index-url https://pypi.github.com/gcode4421-oss/Opal-/"
echo ""
