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
from . import json_lib
from . import http_lib
from . import time_lib
from . import system_lib
from . import file_lib
from . import lowlevel_lib
from . import colors_lib
from . import tui_lib
from . import hardware_lib


# Registry of available modules / سجل الوحدات المتاحة
MODULES = {
    # English module names
    'math': math_lib.get_module,
    'strings': string_lib.get_module,
    'string': string_lib.get_module,
    'io': io_lib.get_module,
    'lists': list_lib.get_module,
    'list': list_lib.get_module,
    'types': type_lib.get_module,
    'json': json_lib.get_module,
    'http': http_lib.get_module,
    'web': http_lib.get_module,
    'time': time_lib.get_module,
    'system': system_lib.get_module,
    'os': system_lib.get_module,
    'file': file_lib.get_module,
    'files': file_lib.get_module,
    'filesystem': file_lib.get_module,
    'fs': file_lib.get_module,
    'lowlevel': lowlevel_lib.get_module,
    'low_level': lowlevel_lib.get_module,
    'memory': lowlevel_lib.get_module,
    'mem': lowlevel_lib.get_module,
    'sys': lowlevel_lib.get_module,
    'colors': colors_lib.get_module,
    'color': colors_lib.get_module,
    'terminal': colors_lib.get_module,
    'term': colors_lib.get_module,
    'tui': tui_lib.get_module,
    'ui': tui_lib.get_module,
    'gui': tui_lib.get_module,
    'hardware': hardware_lib.get_module,
    'hw': hardware_lib.get_module,
    'device': hardware_lib.get_module,

    # Arabic module names
    'رياضيات': math_lib.get_module,
    'نصوص': string_lib.get_module,
    'إدخال_إخراج': io_lib.get_module,
    'قوائم': list_lib.get_module,
    'أنواع': type_lib.get_module,
    'وقت': time_lib.get_module,
    'تاريخ': time_lib.get_module,
    'نظام': system_lib.get_module,
    'ملفات': file_lib.get_module,
    'ملف': file_lib.get_module,
    'منخفض': lowlevel_lib.get_module,
    'ذاكرة': lowlevel_lib.get_module,
    'ألوان': colors_lib.get_module,
    'لون': colors_lib.get_module,
    'طرفية': colors_lib.get_module,
    'واجهة': tui_lib.get_module,
    'هاردوير': hardware_lib.get_module,
    'جهاز': hardware_lib.get_module,
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
