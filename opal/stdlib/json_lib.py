"""
Opal Standard Library - JSON / مكتبة JSON

JSON parsing and serialization functions.
دوال تحليل وتسلسل JSON
"""

import json as _json


def get_module():
    """إرجاع دوال مكتبة JSON / Return JSON module functions"""
    return {
        'parse': _json_parse,
        'تحليل': _json_parse,
        'stringify': _json_stringify,
        'تسلسل': _json_stringify,
        'to_json': _json_stringify,
        'إلى_json': _json_stringify,
        'from_json': _json_parse,
        'من_json': _json_parse,
    }


def _json_parse(str_value):
    """تحليل نص JSON إلى كائن / Parse JSON string to object"""
    try:
        return _json.loads(str(str_value))
    except Exception as e:
        return None


def _json_stringify(value, indent=None):
    """تحويل كائن إلى نص JSON / Convert object to JSON string"""
    try:
        # Handle None, True, False as JSON null/true/false
        if value is None:
            return "null"
        if value is True:
            return "true"
        if value is False:
            return "false"
        return _json.dumps(_convert_opal(value), ensure_ascii=False,
                          indent=indent if indent else None)
    except Exception as e:
        return None


def _convert_opal(value):
    """تحويل قيم أوبال إلى قيم Python للـ JSON / Convert Opal values for JSON"""
    if isinstance(value, dict):
        return {k: _convert_opal(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_convert_opal(v) for v in value]
    return value
