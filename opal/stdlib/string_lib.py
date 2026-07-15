"""
Opal Standard Library - Strings / مكتبة النصوص

String manipulation functions for Opal.
دوال معالجة النصوص للغة أوبال
"""


def get_module():
    """إرجاع دوال مكتبة النصوص / Return string module functions"""
    return {
        'length': len,
        'طول': len,
        'upper': lambda s: str(s).upper(),
        'كبير': lambda s: str(s).upper(),
        'lower': lambda s: str(s).lower(),
        'صغير': lambda s: str(s).lower(),
        'reverse': _reverse,
        'عكس': _reverse,
        'repeat': lambda s, n: str(s) * int(n),
        'كرر': lambda s, n: str(s) * int(n),
        'contains': lambda s, sub: str(sub) in str(s),
        'يحتوي': lambda s, sub: str(sub) in str(s),
        'replace': lambda s, old, new: str(s).replace(str(old), str(new)),
        'استبدل': lambda s, old, new: str(s).replace(str(old), str(new)),
        'split': lambda s, sep: str(s).split(str(sep)),
        'قسم': lambda s, sep: str(s).split(str(sep)),
        'join': _join,
        'دمج': _join,
        'trim': lambda s: str(s).strip(),
        'نظف': lambda s: str(s).strip(),
        'substring': lambda s, start, end: str(s)[int(start):int(end)],
        'جزء': lambda s, start, end: str(s)[int(start):int(end)],
        'startswith': lambda s, prefix: str(s).startswith(str(prefix)),
        'endswith': lambda s, suffix: str(s).endswith(str(suffix)),
        'find': _find,
        'بحث': _find,
        'to_number': _to_number,
        'إلى_رقم': _to_number,
        'format': _format,
        'تنسيق': _format,
    }


def _reverse(s):
    """عكس نص أو قائمة / Reverse a string or list"""
    if isinstance(s, str):
        return s[::-1]
    if isinstance(s, list):
        return list(reversed(s))
    return s


def _join(lst, sep=""):
    """دمج قائمة / Join a list"""
    return str(sep).join(str(x) for x in lst)


def _find(s, sub):
    """البحث عن موضع / Find position"""
    result = str(s).find(str(sub))
    return result  # -1 if not found


def _to_number(s):
    """تحويل نص إلى رقم / Convert string to number"""
    try:
        if '.' in str(s):
            return float(s)
        return int(s)
    except ValueError:
        return None


def _format(template, *args):
    """تنسيق نص / Format a string"""
    return str(template)
    # Simple format: replaces {} with args
    result = str(template)
    for arg in args:
        result = result.replace('{}', str(arg), 1)
    return result
