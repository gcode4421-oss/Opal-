#!/bin/bash
# ============================================================
# Opal Language - PyPI Publishing Script
# سكريبت نشر لغة أوبال على PyPI
# ============================================================
# 
# USAGE / الاستخدام:
#   1. Get PyPI token from: https://pypi.org/manage/account/token/
#      احصل على PyPI token من الرابط أعلاه
#
#   2. Run this script / شغل هذا السكريبت:
#      PYPI_TOKEN=your_token_here bash publish_pypi.sh
#
#   3. Or set token first / أو ضع الـ token أولاً:
#      export PYPI_TOKEN=your_token_here
#      bash publish_pypi.sh
# ============================================================

set -e

echo "============================================"
echo "  Publishing Opal to PyPI"
echo "  نشر أوبال على PyPI"
echo "============================================"
echo ""

# Check for PyPI token / التحقق من PyPI token
if [ -z "$PYPI_TOKEN" ]; then
    echo "❌ Error: PYPI_TOKEN not set / خطأ: PYPI_TOKEN غير مضبوط"
    echo ""
    echo "Get your token from: https://pypi.org/manage/account/token/"
    echo "احصل على الـ token من الرابط أعلاه"
    echo ""
    echo "Then run / ثم شغل:"
    echo "  PYPI_TOKEN=your_token_here bash publish_pypi.sh"
    exit 1
fi

# Check we're in the right directory / التحقق من المجلد الصحيح
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: Not in Opal project directory"
    echo "خطأ: لست في مجلد مشروع أوبال"
    echo "Run from: /home/z/my-project/download/opal"
    exit 1
fi

echo "[1/5] Cleaning previous builds / تنظيف البناء السابق..."
rm -rf build dist *.egg-info
echo "✓ Cleaned"
echo ""

echo "[2/5] Installing build tools / تثبيت أدوات البناء..."
pip install --upgrade build twine --break-system-packages 2>/dev/null || \
pip install --upgrade build twine
echo "✓ Build tools installed"
echo ""

echo "[3/5] Building package / بناء الحزمة..."
python3 -m build
echo ""
echo "✓ Package built"
ls -la dist/
echo ""

echo "[4/5] Checking package / فحص الحزمة..."
python3 -m twine check dist/*
echo "✓ Package check passed"
echo ""

echo "[5/5] Uploading to PyPI / الرفع على PyPI..."
python3 -m twine upload dist/* \
    -u "__token__" \
    -p "$PYPI_TOKEN" \
    --non-interactive
echo ""
echo "✓ Uploaded to PyPI!"
echo ""

echo "============================================"
echo "  🎉 Successfully Published!"
echo "  تم النشر بنجاح!"
echo "============================================"
echo ""
echo "Package URL: https://pypi.org/project/opal-lang/"
echo ""
echo "Users can now install with / يمكن للمستخدمين التثبيت بـ:"
echo "  pip install opal-lang"
echo ""
echo "Verify installation / تحقق من التثبيت:"
echo "  opal --version"
echo ""
