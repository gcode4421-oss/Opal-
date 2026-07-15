"""
Opal Standard Library - Loader / محمل المكتبات

Loads standard library modules for Opal.
يحمل وحدات المكتبة القياسية للغة أوبال
"""

from . import math_lib
from . import string_lib
from . import io_lib
from . import list_lib
from . import type_lib


# Registry of available modules / سجل الوحدات المتاحة
MODULES = {
    'math': math_lib.get_module,
    'رياضيات': math_lib.get_module,
    'strings': string_lib.get_module,
    'نصوص': string_lib.get_module,
    'string': string_lib.get_module,
    'io': io_lib.get_module,
    'إدخال_إخراج': io_lib.get_module,
    'lists': list_lib.get_module,
    'قوائم': list_lib.get_module,
    'list': list_lib.get_module,
    'types': type_lib.get_module,
    'أنواع': type_lib.get_module,
}


def load_module(name):
    """تحميل وحدة بالاسم / Load a module by name"""
    if name in MODULES:
        return MODULES[name]()
    return None


def module_exists(name):
    """تحقق من وجود وحدة / Check if module exists"""
    return name in MODULES


def list_modules():
    """قائمة جميع الوحدات / List all available modules"""
    return list(MODULES.keys())
