"""
Opal Standard Library - I/O / مكتبة الإدخال والإخراج

Input/Output functions for Opal.
دوال الإدخال والإخراج للغة أوبال
"""

import sys


def get_module():
    """إرجاع دوال مكتبة الإدخال والإخراج / Return I/O module functions"""
    return {
        'print': _print,
        'طباعة': _print,
        'input': _input,
        'إدخال': _input,
        'read': _input,
        'read_file': _read_file,
        'اقرأ_ملف': _read_file,
        'write_file': _write_file,
        'اكتب_ملف': _write_file,
        'readlines': _readlines,
        'lines': _readlines,
    }


def _print(*args):
    """طباعة بدون سطر جديد / Print without newline"""
    print(*args, end='')
    return None


def _input(prompt=""):
    """إدخال من المستخدم / Read input from user"""
    return input(prompt)


def _read_file(path):
    """قراءة ملف / Read file contents"""
    try:
        with open(str(path), 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return None


def _write_file(path, content):
    """كتابة ملف / Write to file"""
    try:
        with open(str(path), 'w', encoding='utf-8') as f:
            f.write(str(content))
        return True
    except Exception as e:
        return False


def _readlines(path):
    """قراءة أسطر ملف / Read file lines as list"""
    try:
        with open(str(path), 'r', encoding='utf-8') as f:
            return f.read().splitlines()
    except Exception as e:
        return []
