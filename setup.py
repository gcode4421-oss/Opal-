"""
Opal Language - Setup / إعداد التثبيت

Install Opal globally with: pip install -e .
بعد التثبيت يمكنك استخدام: opal file.op
"""

from setuptools import setup, find_packages

setup(
    name="opal-lang",
    version="2.1.0",
    description="Opal - A powerful beginner-friendly programming language with Arabic and English support, colors, and C transpiler",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
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
