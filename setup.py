"""
Opal Language - Setup / إعداد التثبيت

Install Opal globally with: pip install -e .
بعد التثبيت يمكنك استخدام: opal file.op
"""

from setuptools import setup, find_packages

setup(
    name="opal-lang",
    version="1.0.0",
    description="Opal - A beginner-friendly programming language with Arabic and English support",
    long_description="""
Opal Language / لغة أوبال

A simple, powerful programming language designed for beginners.
Supports both Arabic and English keywords.

لغة برمجة بسيطة وقوية مصممة للمبتدئين.
تدعم الكلمات المفتاحية بالعربية والإنجليزية.

Usage / الاستخدام:
    opal file.op
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
        "Programming Language :: Other",  # Opal itself
        "Intended Audience :: Education",
        "Topic :: Education",
        "Operating System :: OS Independent",
    ],
)
