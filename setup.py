"""
Opal Language - Setup / إعداد التثبيت

Install Opal globally with: pip install -e .
بعد التثبيت يمكنك استخدام: opal file.op
"""

from setuptools import setup, find_packages

setup(
    name="opal-lang",
    version="2.1.0",
    description="Opal - A powerful beginner-friendly programming language with Arabic and English support",
    long_description="""
Opal Language v2.0 / لغة أوبال 2.0

A powerful, simple programming language designed for beginners and experts alike.
Supports both Arabic and English keywords natively.

لغة برمجة قوية وبسيطة مصممة للمبتدئين والمحترفين.
تدعم الكلمات المفتاحية بالعربية والإنجليزية بشكل أصلي.

Features / المميزات:
- Full Arabic and English support / دعم كامل للعربية والإنجليزية
- Object-Oriented Programming (classes, inheritance) / البرمجة الكائنية
- Error handling (try/catch/finally) / معالجة الأخطاء
- Lambda functions / الدوال المجهولة
- Dictionaries / القواميس
- Switch statements / جمل التبديل
- Ternary operator / العملية الثلاثية
- Compound assignments (+=, -=, etc.) / الإسناد المركب
- Rich standard library (math, strings, lists, JSON, HTTP, files, time, system)
- مكتبة قياسية غنية
- Cross-platform (Linux, macOS, Windows, Termux)
- يعمل على جميع الأنظمة

Usage / الاستخدام:
    opal file.op
    opal --repl
""",
    author="Opal Team",
    author_email="opal@example.com",
    url="https://github.com/gcode4421-oss/Opal-",
    packages=find_packages(),
    python_requires=">=3.8",
    entry_points={
        'console_scripts': [
            'opal=opal.main:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Other",
        "Intended Audience :: Education",
        "Topic :: Education",
        "Topic :: Software Development :: Interpreters",
        "Operating System :: OS Independent",
    ],
)
