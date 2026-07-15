# Opal Language / لغة أوبال

<div dir="rtl">

# لغة أوبال - لغة برمجة قوية وسهلة للمبتدئين

![Opal Logo](https://img.shields.io/badge/Opal-1.0.0-blue) ![Python](https://img.shields.io/badge/Python-3.8+-green) ![License](https://img.shields.io/badge/License-MIT-yellow)

## ما هي لغة أوبال؟

أوبال هي لغة برمجة حديثة مصممة خصيصاً للمبتدئين، تدعم الكلمات المفتاحية باللغتين **العربية** و**الإنجليزية** بالكامل. تم تصميمها لتكون سهلة التعلم والاستخدام، مع الحفاظ على القوة والمرونة.

### المميزات الرئيسية:

- ✅ **دعم كامل للعربية والإنجليزية** - اكتب الكود بأي لغة
- ✅ **سهلة للمبتدئين** - صياغة بسيطة وواضحة
- ✅ **مكتبة قياسية غنية** - رياضيات، نصوص، قوائم، إدخال/إخراج
- ✅ **دوال وحلقات وجمل شرطية** - كل ما تحتاجه
- ✅ **مفتوحة المصدر** - مجانية بالكامل

</div>

---

## What is Opal?

Opal is a modern programming language designed specifically for beginners, with full support for both **Arabic** and **English** keywords. It's designed to be easy to learn and use, while remaining powerful and flexible.

### Key Features:

- ✅ **Full Arabic and English support** - Write code in either language
- ✅ **Beginner-friendly** - Simple, clear syntax
- ✅ **Rich standard library** - Math, strings, lists, I/O
- ✅ **Functions, loops, conditionals** - Everything you need
- ✅ **Open source** - Completely free

---

## Installation / التثبيت

```bash
# Clone the repository
git clone https://github.com/gcode4421-oss/Opal-.git
cd Opal-

# Install Opal
pip install -e .

# Verify installation
opal --version
```

## Quick Start / البداية السريعة

Create a file `hello.op`:

```
// English
echo "Hello, World!"

// Arabic
اطبع "مرحبا بالعالم!"

// Variables
var name = "Opal"
متغير اسم = "أوبال"

echo "Welcome to " + name
اطبع "مرحبا بك في " + اسم
```

Run it:
```bash
opal hello.op
```

---

## Language Syntax / صياغة اللغة

### Variables / المتغيرات

```
// English
var name = "Opal"
var age = 25
var is_active = true
const PI = 3.14159

// Arabic
متغير الاسم = "أوبال"
متغير العمر = 25
متغير نشط = صحيح
ثابت باي = 3.14159
```

### Printing / الطباعة

```
// English
echo "Hello"
echo "Name:", name
echo "Sum:", 5 + 3

// Arabic
اطبع "مرحبا"
اطبع "الاسم:", الاسم
اطبع "المجموع:", 5 + 3
```

### Conditionals / الجمل الشرطية

```
// English
if age >= 18 {
    echo "Adult"
} elif age >= 13 {
    echo "Teenager"
} else {
    echo "Child"
}

// Arabic
اذا العمر >= 18 {
    اطبع "بالغ"
} واذا العمر >= 13 {
    اطبع "مراهق"
} والا {
    اطبع "طفل"
}
```

### Loops / الحلقات

```
// While loop
var i = 0
while i < 5 {
    echo i
    i = i + 1
}

// For loop with range
for i in 1..10 {
    echo i
}

// For loop over list
var fruits = ["apple", "banana", "cherry"]
for fruit in fruits {
    echo fruit
}

// Arabic loops
متغير س = 0
بينما س < 5 {
    اطبع س
    س = س + 1
}

لكل رقم في 1..10 {
    اطبع رقم
}
```

### Functions / الدوال

```
// English
function add(a, b) {
    return a + b
}

echo add(5, 3)  // Output: 8

// Recursive function
function factorial(n) {
    if n <= 1 {
        return 1
    }
    return n * factorial(n - 1)
}

echo factorial(5)  // Output: 120

// Arabic
دالة جمع(أ، ب) {
    ارجع أ + ب
}

اطبع جمع(5، 3)  // النتيجة: 8
```

### Lists / القوائم

```
var numbers = [1, 2, 3, 4, 5]
echo numbers[0]      // First element
echo numbers.length   // Length: 5

var mixed = [1, "hello", true, 3.14]

// List operations
push(numbers, 6)     // Add to end
pop(numbers)         // Remove from end
echo reverse(numbers) // Reverse
echo sort(numbers)    // Sort
```

### Operators / العمليات

| English | Arabic | Description |
|---------|--------|-------------|
| `+` | `+` | Addition / الجمع |
| `-` | `-` | Subtraction / الطرح |
| `*` | `*` | Multiplication / الضرب |
| `/` or `÷` | `/` or `÷` | Division / القسمة |
| `^` | `^` | Power / الأس |
| `%` | `%` | Modulo / باقي القسمة |
| `==` | `==` | Equal / يساوي |
| `!=` | `!=` | Not equal / لا يساوي |
| `<` | `<` | Less than / أصغر من |
| `>` | `>` | Greater than / أكبر من |
| `and` | `و` | Logical AND / و |
| `or` | `أو` | Logical OR / أو |
| `not` | `ليس` | Logical NOT | ليس |

---

## Standard Library / المكتبة القياسية

### Math Library / مكتبة الرياضيات

```
import math

// Constants
echo pi          // 3.14159...
echo e           // 2.71828...

// Functions
echo sqrt(16)    // 4.0
echo abs(-5)     // 5
echo power(2, 3) // 8
echo floor(3.7)  // 3
echo ceil(3.2)   // 4
echo round(3.5)  // 4
echo min(5, 3)   // 3
echo max(5, 3)   // 5
echo random()    // Random 0-1
echo randint(1, 100) // Random int

// Arabic
استورد رياضيات
echo باي
echo الجذر(25)
echo القيمة_المطلقة(-10)
echo أس(2، 5)
```

### String Library / مكتبة النصوص

```
import strings

echo length("Hello")       // 5
echo upper("hello")        // HELLO
echo lower("WORLD")        // world
echo reverse("Opal")       // lapO
echo contains("Hello", "ell") // true
echo replace("Hello", "H", "J") // Jello
echo split("a,b,c", ",")   // [a, b, c]

// Arabic
استورد نصوص
echo طول("أوبال")
echo عكس("مرحبا")
echo كبير("abc")
```

### List Library / مكتبة القوائم

```
import lists

var nums = [3, 1, 4, 1, 5, 9, 2, 6]

echo length(nums)    // 8
echo sort(nums)      // [1, 1, 2, 3, 4, 5, 6, 9]
echo reverse(nums)   // [6, 2, 9, 5, 1, 4, 1, 3]
echo sum(nums)       // 31
echo min(nums)       // 1
echo max(nums)       // 9
echo contains(nums, 5) // true
```

### Selective Import / استيراد محدد

```
from strings import upper, lower, length
from math import sqrt, pi

echo upper("hello")
echo sqrt(16)
echo pi
```

---

## Complete Example / مثال كامل

```
// ==========================================
// Opal Language - Complete Demo
// ==========================================

import math
import strings

// Variables
var name = "Opal"
var version = 1.0

echo "=== " + name + " " + version + " ==="

// Function definition
function fibonacci(n) {
    if n <= 1 {
        return n
    }
    return fibonacci(n - 1) + fibonacci(n - 2)
}

// Generate Fibonacci sequence
echo "\nFibonacci:"
for i in 0..10 {
    echo "  fib(" + i + ") =", fibonacci(i)
}

// List operations
var numbers = [5, 2, 8, 1, 9, 3]
echo "\nOriginal:", numbers
echo "Sorted:", sort(numbers)
echo "Sum:", sum(numbers)
echo "Average:", sum(numbers) / length(numbers))

// Arabic section
متغير أسماء = ["أحمد", "فاطمة", "علي"]
اطبع "\nالأسماء:"
لكل اسم في أسماء {
    اطبع "  -", اسم
}
```

---

## Running Opal / تشغيل أوبال

```bash
# Run a file
opal file.op

# Run with verbose output
opal file.op --verbose

# Interactive REPL
opal --repl

# Show version
opal --version

# Show help
opal --help
```

---

## File Extension / امتداد الملف

Opal files use the `.op` extension:
- `hello.op`
- `math_demo.op`
- `arabic_demo.op`

---

## Project Structure / بنية المشروع

```
Opal-/
├── opal/
│   ├── __init__.py        # Package init
│   ├── tokens.py          # Token definitions
│   ├── lexer.py           # Lexer (tokenizer)
│   ├── ast_nodes.py       # AST node definitions
│   ├── parser.py          # Parser
│   ├── environment.py     # Variable scopes
│   ├── interpreter.py     # Interpreter (executor)
│   ├── main.py            # CLI entry point
│   └── stdlib/            # Standard library
│       ├── __init__.py    # Library loader
│       ├── math_lib.py    # Math functions
│       ├── string_lib.py  # String functions
│       ├── list_lib.py    # List functions
│       ├── io_lib.py      # I/O functions
│       └── type_lib.py    # Type functions
├── examples/              # Example programs
│   ├── hello.op
│   ├── math_demo.op
│   ├── functions.op
│   ├── conditionals.op
│   ├── lists_strings.op
│   ├── arabic_demo.op
│   └── import_demo.op
├── setup.py               # Installation script
├── README.md              # This file
└── opal                   # CLI launcher
```

---

## License / الترخيص

MIT License - Free to use, modify, and distribute.

---

<div dir="rtl">

## شكر وتقدير

لغة أوبال مصممة لتكون سهلة وقوية في نفس الوقت. شكراً لاستخدامك أوبال!

**استمتع بالبرمجة! 🚀**

</div>
