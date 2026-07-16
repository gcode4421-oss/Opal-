# Installing Opal Language / تثبيت لغة أوبال

## Option 1: Install from GitHub (Recommended) / الطريقة الأولى: من GitHub (موصى بها)

### Using pip directly / باستخدام pip مباشرة
```bash
pip install git+https://github.com/gcode4421-oss/Opal-.git
```

### From release wheel / من ملف الـ wheel المنشور
```bash
# Download the wheel file / تحميل ملف الـ wheel
curl -L -o opal_lang-2.1.0-py3-none-any.whl \
  https://github.com/gcode4421-oss/Opal-/releases/download/v2.1.0/opal_lang-2.1.0-py3-none-any.whl

# Install it / تثبيته
pip install opal_lang-2.1.0-py3-none-any.whl
```

### From source / من المصدر
```bash
git clone https://github.com/gcode4421-oss/Opal-.git
cd Opal-
pip install .
```

## Option 2: Install from PyPI / الطريقة الثانية: من PyPI

> **Note**: Once published to PyPI, you can install with:
> **ملاحظة**: بعد النشر على PyPI، يمكنك التثبيت بـ:
```bash
pip install opal-lang
```

## Option 3: Manual Installation / الطريقة الثالثة: تثبيت يدوي

### Termux (Android)
```bash
pkg install git python
git clone https://github.com/gcode4421-oss/Opal-.git
cd Opal-
bash install_termux.sh
```

### Linux / macOS
```bash
git clone https://github.com/gcode4421-oss/Opal-.git
cd Opal-
bash install.sh
```

### Windows
```cmd
git clone https://github.com/gcode4421-oss/Opal-.git
cd Opal-
install_windows.bat
```

## Verification / التحقق

After installation, verify it works / بعد التثبيت، تحقق من عمله:

```bash
opal --version
# Should output: Opal 2.1.0

opal --help
# Shows help

# Create test file / إنشاء ملف اختبار
echo 'echo "Hello, Opal!"' > test.op
opal test.op
# Should output: Hello, Opal!

# Test Arabic / اختبار العربية
echo 'اطبع "مرحبا بالعالم!"' > test.op
opal test.op
# Should output: مرحبا بالعالم!

# Test colors / اختبار الألوان
echo 'import colors
echo RED + "Red text" + RESET
echo أخضر + "نص أخضر" + إعادة' > test.op
opal test.op --color=always
```

## Upgrading / التحديث

```bash
pip install --upgrade opal-lang
# Or from GitHub:
pip install --upgrade --force-reinstall git+https://github.com/gcode4421-oss/Opal-.git
```

## Uninstalling / إزالة التثبيت

```bash
pip uninstall opal-lang
```

## Troubleshooting / حل المشاكل

### `opal: command not found` / أمر opal غير موجود

Add pip's bin directory to PATH / أضف مجلد bin الخاص بـ pip إلى PATH:

```bash
# Linux/macOS
export PATH="$HOME/.local/bin:$PATH"
# Add to ~/.bashrc or ~/.zshrc to make permanent

# Termux
export PATH="$PREFIX/bin:$PATH"
```

### Colors not showing / الألوان لا تظهر

Force colors with / إجبار الألوان بـ:
```bash
opal file.op --color=always
# Or set environment variable:
export FORCE_COLOR=1
opal file.op
```

### Arabic text not displaying correctly / النص العربي لا يظهر بشكل صحيح

Make sure your terminal supports UTF-8 / تأكد من أن طرفيتك تدعم UTF-8:
```bash
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
```

## Package Information / معلومات الحزمة

- **Package name**: `opal-lang`
- **Version**: 2.1.0
- **Python requirement**: >= 3.8
- **License**: MIT
- **Dependencies**: arabic-reshaper, python-bidi

## Links / روابط

- **GitHub Repository**: https://github.com/gcode4421-oss/Opal-
- **Releases**: https://github.com/gcode4421-oss/Opal-/releases
- **Latest Release**: https://github.com/gcode4421-oss/Opal-/releases/tag/v2.1.0
- **Documentation**: https://github.com/gcode4421-oss/Opal-#readme
- **Changelog**: https://github.com/gcode4421-oss/Opal-/blob/main/CHANGELOG.md
- **Issues**: https://github.com/gcode4421-oss/Opal-/issues
