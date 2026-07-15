"""
Opal Standard Library - Math / مكتبة الرياضيات

Mathematical functions for Opal.
دوال رياضية للغة أوبال
"""

import math as _math


def get_module():
    """إرجاع دوال مكتبة الرياضيات / Return math module functions"""
    return {
        # Constants / ثوابت
        'pi': _math.pi,
        'e': _math.e,
        'infinity': _math.inf,
        'باي': _math.pi,
        'هـ': _math.e,

        # Functions / دوال
        'abs': abs,
        'القيمة_المطلقة': abs,
        'sqrt': _math.sqrt,
        'الجذر': _math.sqrt,
        'power': pow,
        'أس': pow,
        'floor': _math.floor,
        'ceil': _math.ceil,
        'round': round,
        'تقريب': round,
        'min': min,
        'الأصغر': min,
        'max': max,
        'الأكبر': max,
        'sin': _math.sin,
        'cos': _math.cos,
        'tan': _math.tan,
        'log': _math.log,
        'log10': _math.log10,
        'exp': _math.exp,
        'random': _random,
        'عشوائي': _random,
        'randint': _randint,
        'عشوائي_بين': _randint,
    }


def _random():
    """رقم عشوائي بين 0 و 1 / Random number between 0 and 1"""
    import random
    return random.random()


def _randint(a, b):
    """رقم صحيح عشوائي بين a و b / Random integer between a and b"""
    import random
    return random.randint(int(a), int(b))
