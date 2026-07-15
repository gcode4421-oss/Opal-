# Opal Language v2.0 / لغة أوبال 2.0

<div dir="rtl">

# لغة أوبال - لغة برمجة قوية وسهلة للمبتدئين والمحترفين

![Opal](https://img.shields.io/badge/Opal-2.0.0-blue) ![Python](https://img.shields.io/badge/Python-3.8+-green) ![License](https://img.shields.io/badge/License-MIT-yellow) ![Platform](https://img.shields.io/badge/Platform-All-success)

## ما الجديد في الإصدار 2.0؟

🚀 **تحديثات ضخمة:**
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

## What's New in v2.0?

🚀 **Massive Updates:**
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
```

Save as `hello.op` and run / احفظ باسم `hello.op` وشغل:
```bash
opal hello.op
```

---

## Language Features / مميزات اللغة

### 1. Variables & Constants / المتغيرات والثوابت

```opal
var name = "Opal"          // English
const PI = 3.14159

متغير الاسم = "أوبال"      // Arabic
ثابت باي = 3.14159
```

### 2. Data Types / أنواع البيانات

```opal
var num = 42               // Integer
var float = 3.14           // Float
var str = "Hello"          // String
var bool = true            // Boolean
var nothing = null         // Null
var list = [1, 2, 3]       // List
var dict = {"a": 1, "b": 2}  // Dictionary (NEW!)
```

### 3. Object-Oriented Programming / البرمجة الكائنية (جديد!)

```opal
// English
class Animal {
    function init(name, sound) {
        this.name = name
        this.sound = sound
    }

    function speak() {
        echo this.name + " says " + this.sound
    }
}

class Dog : Animal {  // Inheritance
    function fetch() {
        echo this.name + " fetches the ball!"
    }
}

var dog = new Dog("Rex", "Woof")
dog.speak()
dog.fetch()

// Arabic
صف حيوان {
    دالة init(الاسم، الصوت) {
        هذا.الاسم = الاسم
        هذا.الصوت = الصوت
    }

    دالة تكلم() {
        اطبع هذا.الاسم + " يقول " + هذا.الصوت
    }
}

متغير كلب = جديد حيوان("ريكس"، "هو هو")
كلب.تكلم()
```

### 4. Error Handling / معالجة الأخطاء (جديد!)

```opal
try {
    var result = 10 / 0
} catch (error) {
    echo "Caught error:", error
} finally {
    echo "Cleanup"
}

// Custom errors
function check_age(age) {
    if age < 18 {
        throw "Too young!"
    }
    return "OK"
}

// Arabic
حاول {
    متغير نتيجة = 10 ÷ 0
} أمسك (خطأ) {
    اطبع "تم الإمساك بالخطأ:", خطأ
} أخيرا {
    اطبع "تنظيف"
}
```

### 5. Lambda Functions / الدوال المجهولة (جديد!)

```opal
var double = fn(x) -> x * 2
echo double(5)  // 10

var greet = fn(name) {
    return "Hello, " + name
}

// Using with map
var nums = [1, 2, 3, 4, 5]
var doubled = map(fn(x) -> x * 2, nums)
echo doubled  // [2, 4, 6, 8, 10]
```

### 6. Dictionaries / القواميس (جديد!)

```opal
var person = {
    "name": "Alice",
    "age": 30,
    "skills": ["Python", "Opal"]
}

echo person["name"]      // Alice
person["age"] = 31       // Update
person["city"] = "Cairo" // Add new
```

### 7. Switch / جملة التبديل (جديد!)

```opal
var day = 3
switch (day) {
    case 1: { echo "Monday" }
    case 2: { echo "Tuesday" }
    case 3: { echo "Wednesday" }
    default: { echo "Other" }
}
```

### 8. Ternary Operator / العملية الثلاثية (جديد!)

```opal
var age = 20
var status = age >= 18 ? "Adult" : "Minor"
echo status  // Adult

// Nested
var temp = 25
var weather = temp > 30 ? "Hot" : temp > 20 ? "Warm" : "Cool"
```

### 9. Compound Assignment / الإسناد المركب (جديد!)

```opal
var x = 10
x += 5   // x = 15
x -= 3   // x = 12
x *= 2   // x = 24
x /= 4   // x = 6
```

### 10. Do-Until Loop / حلقة افعل-حتى (جديد!)

```opal
var i = 0
do {
    echo i
    i += 1
} until (i >= 3)
```

### 11. Block Comments / التعليقات المتعددة (جديد!)

```opal
// Single line comment
# Also a comment

/* Multi-line
   comment
   تعليق متعدد
   الأسطر */
```

---

## Standard Library / المكتبة القياسية

### Math / رياضيات

```opal
import math

echo pi              // 3.14159...
echo sqrt(16)        // 4.0
echo power(2, 10)    // 1024
echo random()        // Random 0-1
echo randint(1, 100) // Random int
```

### Strings / نصوص

```opal
import strings

echo length("Hello")     // 5
echo upper("hello")      // HELLO
echo reverse("Opal")     // lapO
echo split("a,b,c", ",") // [a, b, c]
```

### Lists / قوائم

```opal
import lists

var nums = [3, 1, 4, 1, 5]
echo sort(nums)      // [1, 1, 3, 4, 5]
echo sum(nums)       // 14
echo max(nums)       // 5
echo reverse(nums)   // [5, 1, 4, 1, 3]
```

### JSON (جديد!)

```opal
import json

var data = {"name": "Opal", "version": 2.0}
var str = stringify(data)
echo str  // {"name": "Opal", "version": 2.0}

var parsed = parse(str)
echo parsed["name"]  // Opal
```

### HTTP / ويب (جديد!)

```opal
import http

var response = get("https://httpbin.org/get")
echo response["status"]
echo response["body"]

var post_response = post("https://httpbin.org/post", {"key": "value"})
echo post_response["status"]

echo url_encode("Hello World")  // Hello%20World
```

### File System / نظام الملفات (جديد!)

```opal
import file

// Read/Write
write("test.txt", "Hello, Opal!")
var content = read("test.txt")
echo content

// File info
echo exists("test.txt")  // true
echo size("test.txt")    // file size in bytes

// Directory
echo list_dir(".")       // list current directory
mkdir("new_folder")
```

### Time & Date / الوقت والتاريخ (جديد!)

```opal
import time

echo now()           // current timestamp
echo date()          // current date string
echo year()          // current year
echo hour()          // current hour
sleep(2)             // sleep 2 seconds
```

### System / نظام (جديد!)

```opal
import system

echo os()            // Operating system name
echo cwd()           // Current working directory
echo list_dir(".")   // List files
echo env("PATH")     // Environment variable
```

---

## Operators / العمليات

| Operator | Arabic | Description |
|----------|--------|-------------|
| `+` | `+` | Addition / الجمع |
| `-` | `-` | Subtraction / الطرح |
| `*` | `*` | Multiplication / الضرب |
| `/` or `÷` | `/` or `÷` | Division / القسمة |
| `^` | `^` | Power / الأس |
| `%` | `%` | Modulo / باقي القسمة |
| `==` | `==` | Equal / يساوي |
| `!=` | `!=` | Not equal / لا يساوي |
| `<` `>` `<=` `>=` | same | Comparison / مقارنة |
| `and` | `و` | Logical AND |
| `or` | `أو` | Logical OR |
| `not` | `ليس` | Logical NOT |
| `+=` `-=` `*=` `/=` | same | Compound assign (NEW!) |
| `? :` | `? :` | Ternary (NEW!) |

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
| `in` | `في` | In (for loop) |
| `function` | `دالة` | Function declaration |
| `return` | `ارجع` | Return |
| `break` | `توقف` | Break |
| `continue` | `اكمل` | Continue |
| `import` | `استورد` | Import module |
| `from` | `من` | From import |
| `echo` | `اطبع` | Print |
| `true` | `صحيح` | Boolean true |
| `false` | `خطأ` | Boolean false |
| `null` | `فراغ` | Null |
| `and` | `و` | Logical AND |
| `or` | `أو` | Logical OR |
| `not` | `ليس` | Logical NOT |
| `try` | `حاول` | Try (NEW!) |
| `catch` | `امسك` | Catch (NEW!) |
| `finally` | `اخيرا` | Finally (NEW!) |
| `throw` | `ارمي` | Throw (NEW!) |
| `class` | `صف` | Class (NEW!) |
| `this` | `هذا` | This (NEW!) |
| `new` | `جديد` | New instance (NEW!) |
| `fn` | - | Lambda (NEW!) |
| `switch` | `بدل` | Switch (NEW!) |
| `case` | `حالة` | Case (NEW!) |
| `default` | `افتراضي` | Default (NEW!) |
| `do` | `افعل` | Do (NEW!) |
| `until` | `حتى` | Until (NEW!) |

---

## Running Opal / تشغيل أوبال

```bash
# Run a file / تشغيل ملف
opal file.op

# Verbose output / تفاصيل أكثر
opal file.op --verbose

# Interactive REPL / واجهة تفاعلية
opal --repl

# Version / الإصدار
opal --version

# Help / المساعدة
opal --help
```

---

## Examples / أمثلة

See the `examples/` directory for complete examples:
- `hello.op` - Basic hello world
- `math_demo.op` - Math library
- `functions.op` - Functions and recursion
- `conditionals.op` - Conditionals and loops
- `lists_strings.op` - Lists and strings
- `arabic_demo.op` - Full Arabic example
- `import_demo.op` - Import system
- `oop_demo.op` - Object-oriented programming (NEW!)
- `arabic_oop_demo.op` - Arabic OOP (NEW!)
- `advanced_features.op` - All advanced features (NEW!)
- `web_json_demo.op` - Web and JSON (NEW!)
- `advanced_demo.op` - Complete showcase

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
│   ├── main.py            # CLI entry point
│   └── stdlib/
│       ├── __init__.py    # Library loader
│       ├── math_lib.py    # Math functions
│       ├── string_lib.py  # String functions
│       ├── list_lib.py    # List functions
│       ├── io_lib.py      # I/O functions
│       ├── type_lib.py    # Type functions
│       ├── json_lib.py    # JSON (NEW!)
│       ├── http_lib.py    # HTTP (NEW!)
│       ├── file_lib.py    # File system (NEW!)
│       ├── time_lib.py    # Time (NEW!)
│       └── system_lib.py  # System (NEW!)
├── examples/              # Example programs
├── install.sh             # Linux/macOS installer
├── install_termux.sh      # Termux installer
├── install_windows.bat    # Windows installer
├── install_universal.sh   # Universal installer
├── setup.py               # Python package setup
├── README.md              # This file
└── opal                   # CLI launcher
```

---

## License / الترخيص

MIT License - Free to use, modify, and distribute.

---

<div dir="rtl">

## شكر وتقدير

لغة أوبال v2.0 - أقوى وأسرع وأسهل من أي وقت مضى!

**استمتع بالبرمجة! 🚀**

</div>
