"""
Opal Standard Library - Time & Date / مكتبة الوقت والتاريخ

Time and date functions.
دوال الوقت والتاريخ
"""

import time as _time
import datetime as _datetime


def get_module():
    """إرجاع دوال مكتبة الوقت / Return time module functions"""
    return {
        'now': _now,
        'الآن': _now,
        'timestamp': lambda: _time.time(),
        'الطابع_الزمني': lambda: _time.time(),
        'sleep': lambda seconds: _time.sleep(float(seconds)),
        'نم': lambda seconds: _time.sleep(float(seconds)),
        'format_time': _format_time,
        'تنسيق_الوقت': _format_time,
        'date': _date,
        'تاريخ': _date,
        'year': lambda: _datetime.datetime.now().year,
        'سنة': lambda: _datetime.datetime.now().year,
        'month': lambda: _datetime.datetime.now().month,
        'شهر': lambda: _datetime.datetime.now().month,
        'day': lambda: _datetime.datetime.now().day,
        'يوم': lambda: _datetime.datetime.now().day,
        'hour': lambda: _datetime.datetime.now().hour,
        'ساعة': lambda: _datetime.datetime.now().hour,
        'minute': lambda: _datetime.datetime.now().minute,
        'دقيقة': lambda: _datetime.datetime.now().minute,
        'second': lambda: _datetime.datetime.now().second,
        'ثانية': lambda: _datetime.datetime.now().second,
    }


def _now():
    """الوقت الحالي بالثواني / Current time in seconds"""
    return _time.time()


def _format_time(timestamp=None, fmt="%Y-%m-%d %H:%M:%S"):
    """تنسيق الوقت / Format time"""
    if timestamp is None:
        timestamp = _time.time()
    try:
        return _time.strftime(fmt, _time.localtime(float(timestamp)))
    except Exception:
        return str(timestamp)


def _date():
    """التاريخ الحالي / Current date string"""
    return _time.strftime("%Y-%m-%d")
