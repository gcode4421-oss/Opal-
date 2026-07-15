# Opal Language v2.1.0 / لغة أوبال 2.1.0

<div dir="rtl">

# لغة أوبال - لغة برمجة قوية وسهلة للمبتدئين والمحترفين

![Opal](https://img.shields.io/badge/Opal-2.1.0-blue) ![Python](https://img.shields.io/badge/Python-3.8+-green) ![License](https://img.shields.io/badge/License-MIT-yellow) ![Platform](https://img.shields.io/badge/Platform-All-success) ![Tests](https://img.shields.io/badge/Tests-9%2F9%20pass-brightgreen)

[![PyPI version](https://badge.fury.io/py/opal-lang.svg)](https://badge.fury.io/py/opal-lang)
[![GitHub release](https://img.shields.io/github/v/release/gcode4421-oss/Opal-)](https://github.com/gcode4421-oss/Opal-/releases)
[![Install](https://img.shields.io/badge/pip%20install-opal--lang-blue)](https://pypi.org/project/opal-lang/)

## Install / تثبيت

```bash
# From GitHub / من GitHub (works now / يعمل الآن)
pip install git+https://github.com/gcode4421-oss/Opal-.git

# From release wheel / من ملف الـ wheel المنشور
pip install https://github.com/gcode4421-oss/Opal-/releases/download/v2.1.0/opal_lang-2.1.0-py3-none-any.whl

# From PyPI (after publishing) / من PyPI (بعد النشر)
pip install opal-lang
```

## ما الجديد في الإصدار 2.1.0؟

🚀 **تحديثات ضخمة:**
- ✅ **مكتبة الألوان (Colors)** - دعم كامل لـ ANSI colors بالعربية والإنجليزية
- ✅ **الأنواع منخفضة المستوى (Low-level types)** - int8, int16, int32, int64, bytes, buffers
- ✅ **مولّد كود C (C Transpiler)** - `opal file.op --compile-c` لتحويل الكود إلى C
- ✅ **دعم العربية المحسّن** - تشكيل عربي، BiDi، علامات RTL/LTR
- ✅ **تثبيت من أي مجلد** - `opal` يعمل من أي مسار بعد التثبيت
- ✅ **--color=always/never/auto** - تحكم كامل في الألوان
- ✅ **البرمجة الكائنية (OOP)** - صفوف، كائنات، وراثة، `this`
- ✅ **معالجة الأخطاء** - `try/catch/finally` و `throw`
- ✅ **الدوال المجهولة (Lambda)** - `fn(x) -> x * 2`
- ✅ **القواميس (Dictionaries)** - `{"key": value}`
- ✅ **جملة التبديل (Switch)** - `switch/case/default`
- ✅ **العملية الثلاثية (Ternary)** - `cond ? a : b`
- ✅ **الإسناد المركب** - `+=`, `-=`, `*=`, `/=`
- ✅ **حلقة افعل-حتى (Do-Until)** - `do { } until (cond)`
- ✅ **مكتبة JSON** - تحليل وتسلسل JSON
- ✅ **مكتبة HTTP** - طلبات الويب
- ✅ **مكتبة الملفات** - قراءة/كتابة/نسخ/نقل
- ✅ **مكتبة الوقت** - الوقت والتاريخ
- ✅ **مكتبة النظام** - معلومات نظام التشغيل
- ✅ **التعليقات متعددة الأسطر** - `/* ... */`
- ✅ **دعم Termux** - تثبيت سهل على الهاتف

</div>

---

## What's New in v2.1.0?

🚀 **Massive Updates:**
- ✅ **Colors Library** - Full ANSI color support with Arabic and English names
- ✅ **Low-level types** - int8, int16, int32, int64, bytes, buffers, references
- ✅ **C Transpiler** - `opal file.op --compile-c` to convert Opal to C code
- ✅ **Improved Arabic support** - Arabic reshaping, BiDi, RTL/LTR marks
- ✅ **System-wide installation** - `opal` works from any directory
- ✅ **--color=always/never/auto** - Full color control
- ✅ **Object-Oriented Programming (OOP)** - classes, objects, inheritance, `this`
- ✅ **Error Handling** - `try/catch/finally` and `throw`
- ✅ **Lambda Functions** - `fn(x) -> x * 2`
- ✅ **Dictionaries** - `{"key": value}`
- ✅ **Switch Statements** - `switch/case/default`
- ✅ **Ternary Operator** - `cond ? a : b`
- ✅ **Compound Assignment** - `+=`, `-=`, `*=`, `/=`
- ✅ **Do-Until Loop** - `do { } until (cond)`
- ✅ **JSON Library** - parse and stringify JSON
- ✅ **HTTP Library** - web requests
- ✅ **File Library** - read/write/copy/move
- ✅ **Time Library** - time and date functions
- ✅ **System Library** - OS information
- ✅ **Block Comments** - `/* ... */`
- ✅ **Termux Support** - easy install on mobile

---

## Installation / التثبيت

### Termux (Android) / أندرويد

```bash
# Quick install / تثبيت سريع
pkg install git python
git clone https://github.com/gcode4421-oss/Opal-.git
cd Opal-
bash install_termux.sh
```

### Linux / macOS

```bash
# Clone and install / استنساخ وتثبيت
git clone https://github.com/gcode4421-oss/Opal-.git
cd Opal-
bash install.sh
```

### Windows

```cmd
:: Download and run / تحميل وتشغيل
git clone https://github.com/gcode4421-oss/Opal-.git
cd Opal-
install_windows.bat
```

### pip (any platform / أي نظام)

```bash
pip install opal-lang
```

بعد التثبيت، `opal` يعمل من **أي مجلد**:
```bash
cd /any/directory
opal myfile.op
```

---

## Quick Start / البداية السريعة

```opal
// English / إنجليزي
echo "Hello, World!"
var name = "Opal"
echo "Welcome to " + name

// Arabic / عربي
اطبع "مرحبا بالعالم!"
متغير اسم = "أوبال"
اطبع "مرحبا بك في " + اسم

// Colors / الألوان
import colors
echo RED + "Error!" + RESET
echo أخضر + "نص أخضر بالعربية" + إعادة
echo BOLD + BLUE + "Bold Blue" + RESET
```

Save as `hello.op` and run / احفظ باسم `hello.op` وشغل:
```bash
opal hello.op

# With forced colors / مع إجبار الألوان
opal hello.op --color=always
```

---

## Standard Library / المكتبة القياسية (12 مكتبة)

| Library | Arabic Name | Description |
|---------|-------------|-------------|
| `math` | `رياضيات` | Math functions |
| `strings` | `نصوص` | String manipulation |
| `lists` | `قوائم` | List operations |
| `io` | `إدخال_إخراج` | Input/output |
| `types` | `أنواع` | Type checking |
| `json` | - | JSON parse/stringify |
| `http` | - | HTTP requests |
| `file` | `ملفات` | File system operations |
| `time` | `وقت` | Time and date |
| `system` | `نظام` | OS information |
| `lowlevel` | `منخفض` | Low-level types (int8, bytes, buffers) |
| `colors` | `ألوان` | ANSI colors with Arabic support (NEW!) |

### Colors Library Example / مثال مكتبة الألوان

```opal
import colors

// English colors
echo RED + "Red text" + RESET
echo GREEN + "Green text" + RESET
echo BLUE + "Blue text" + RESET

// Arabic colors
echo أحمر + "نص أحمر" + إعادة
echo أخضر + "نص أخضر" + إعادة
echo أزرق + "نص أزرق" + إعادة

// Styles
echo BOLD + "Bold text" + RESET
echo UNDERLINE + "Underlined" + RESET
echo عريض + "نص عريض" + إعادة

// RGB custom colors
echo rgb("Custom purple", 128, 0, 128)

// Status messages
echo GREEN + "[SUCCESS] " + RESET + "Operation completed"
echo RED + "[ERROR] " + RESET + "Something went wrong"
echo YELLOW + "[WARNING] " + RESET + "Be careful"
```

---

## C Transpiler / مولّد كود C

```bash
# Convert Opal to C / تحويل أوبال إلى C
opal program.op --compile-c -o program.c

# Compile with gcc / ترجمة بـ gcc
gcc program.c -o program -lm

# Run / تشغيل
./program
```

يدعم: variables, functions, recursion, if/elif/else, while, for, all operators, ternary, compound assignment, string concatenation.

---

## Examples / أمثلة

### Beginner Examples (examples/preview/)
- `hello.op` - Hello World (English + Arabic)
- `calculator.op` - Simple calculator
- `guessing_game.op` - Number guessing game
- `temperature_converter.op` - Temperature converter
- `colors_demo.op` - Colors showcase (English)
- `arabic_colors_demo.op` - Colors + Arabic showcase

### Advanced Examples (examples/)
- `oop_demo.op` - Object-oriented programming
- `arabic_oop_demo.op` - OOP in Arabic
- `advanced_features.op` - All advanced features
- `web_json_demo.op` - Web and JSON
- `lowlevel_demo.op` - Low-level types
- `math_demo.op`, `functions.op`, `conditionals.op`, etc.

### Test Suite (tests/)
- 9 test suites - all passing
- `test_01_variables.op` through `test_08_imports.op`
- `test_c_complex.op` - C transpiler verification

---

## Running Opal / تشغيل أوبال

```bash
# Run a file / تشغيل ملف
opal file.op

# With colors forced / مع إجبار الألوان
opal file.op --color=always

# Disable colors / تعطيل الألوان
opal file.op --color=never

# Verbose output / تفاصيل أكثر
opal file.op --verbose

# Compile to C / تحويل إلى C
opal file.op --compile-c -o output.c

# Interactive REPL / واجهة تفاعلية
opal --repl

# Version / الإصدار
opal --version

# Help / المساعدة
opal --help
```

---

## Keyword Reference / مرجع الكلمات المفتاحية

| English | Arabic | Description |
|---------|--------|-------------|
| `var` | `متغير` | Variable declaration |
| `const` | `ثابت` | Constant declaration |
| `if` | `اذا` | If statement |
| `elif` | `واذا` | Else if |
| `else` | `والا` | Else |
| `while` | `بينما` | While loop |
| `for` | `لكل` | For loop |
| `function` | `دالة` | Function declaration |
| `return` | `ارجع` | Return |
| `break` | `توقف` | Break |
| `continue` | `اكمل` | Continue |
| `import` | `استورد` | Import module |
| `from` | `من` | From import |
| `echo` | `اطبع` | Print |
| `try` | `حاول` | Try |
| `catch` | `امسك` | Catch |
| `finally` | `اخيرا` | Finally |
| `throw` | `ارمي` | Throw |
| `class` | `صف` | Class |
| `this` | `هذا` | This |
| `new` | `جديد` | New instance |
| `switch` | `بدل` | Switch |
| `case` | `حالة` | Case |
| `do` | `افعل` | Do |
| `until` | `حتى` | Until |
| `fn` | - | Lambda |

---

## Project Structure / بنية المشروع

```
Opal-/
├── opal/
│   ├── __init__.py
│   ├── tokens.py          # Token definitions
│   ├── lexer.py           # Lexer
│   ├── ast_nodes.py       # AST nodes
│   ├── parser.py          # Parser
│   ├── environment.py     # Variable scopes
│   ├── interpreter.py     # Interpreter
│   ├── c_transpiler.py    # C code generator
│   ├── main.py            # CLI entry point
│   └── stdlib/
│       ├── __init__.py    # Library loader
│       ├── math_lib.py    # Math functions
│       ├── string_lib.py  # String functions
│       ├── list_lib.py    # List functions
│       ├── io_lib.py      # I/O functions
│       ├── type_lib.py    # Type functions
│       ├── json_lib.py    # JSON
│       ├── http_lib.py    # HTTP
│       ├── file_lib.py    # File system
│       ├── time_lib.py    # Time
│       ├── system_lib.py  # System
│       ├── lowlevel_lib.py # Low-level types
│       └── colors_lib.py  # Colors (NEW!)
├── examples/
│   ├── preview/           # Beginner examples
│   └── *.op               # Advanced examples
├── tests/                 # Test suites (9 tests)
├── install.sh             # Linux/macOS installer
├── install_termux.sh      # Termux installer
├── install_windows.bat    # Windows installer
├── install_universal.sh   # Universal installer
├── setup.py               # Python package setup
├── README.md              # This file
└── opal_cli               # CLI launcher
```

---

## Test Results / نتائج الاختبارات

| Test | Status |
|------|--------|
| test_01_variables | ✅ PASS |
| test_02_control_flow | ✅ PASS |
| test_03_functions | ✅ PASS |
| test_04_oop | ✅ PASS |
| test_05_error_handling | ✅ PASS |
| test_06_advanced | ✅ PASS |
| test_07_stdlib | ✅ PASS |
| test_08_imports | ✅ PASS |
| test_c_complex | ✅ PASS |
| **Total** | **9/9 PASS** |

---

## License / الترخيص

MIT License - Free to use, modify, and distribute.

---

<div dir="rtl">

## شكر وتقدير

لغة أوبال v2.1.0 - أقوى وأسرع وأسهل من أي وقت مضى!

**استمتع بالبرمجة! 🚀**

</div>

---

## Links / روابط

- **Repository**: https://github.com/gcode4421-oss/Opal-
- **Releases**: https://github.com/gcode4421-oss/Opal-/releases
- **Issues**: https://github.com/gcode4421-oss/Opal-/issues
