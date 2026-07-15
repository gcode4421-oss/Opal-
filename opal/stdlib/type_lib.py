"""
Opal Standard Library - Type & Convert / مكتبة الأنواع والتحويل

Type checking and conversion functions.
دوال فحص الأنواع والتحويل بينها
"""


def get_module():
    """إرجاع دوال الأنواع / Return type module functions"""
    return {
        'is_number': lambda x: isinstance(x, (int, float)) and not isinstance(x, bool),
        'هو_رقم': lambda x: isinstance(x, (int, float)) and not isinstance(x, bool),
        'is_string': lambda x: isinstance(x, str),
        'هو_نص': lambda x: isinstance(x, str),
        'is_bool': lambda x: isinstance(x, bool),
        'هو_منطقي': lambda x: isinstance(x, bool),
        'is_list': lambda x: isinstance(x, list),
        'هو_قائمة': lambda x: isinstance(x, list),
        'is_null': lambda x: x is None,
        'هو_فارغ': lambda x: x is None,
        'is_function': callable,
        'هو_دالة': callable,
        'to_string': _to_string,
        'إلى_نص': _to_string,
        'to_number': _to_number,
        'إلى_رقم': _to_number,
        'to_int': lambda x: int(x),
        'إلى_صحيح': lambda x: int(x),
        'to_float': lambda x: float(x),
        'إلى_عشري': lambda x: float(x),
        'type_of': _type_of,
        'نوع': _type_of,
    }


def _to_string(value):
    """تحويل إلى نص / Convert to string"""
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    return str(value)


def _to_number(value):
    """تحويل إلى رقم / Convert to number"""
    if isinstance(value, (int, float)):
        return value
    try:
        if '.' in str(value):
            return float(value)
        return int(value)
    except (ValueError, TypeError):
        return None


def _type_of(value):
    """الحصول على نوع القيمة / Get type name"""
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int):
        return "int"
    if isinstance(value, float):
        return "float"
    if isinstance(value, str):
        return "string"
    if isinstance(value, list):
        return "list"
    if callable(value):
        return "function"
    return "unknown"
