"""
Opal Standard Library - Lists / مكتبة القوائم

List/array manipulation functions for Opal.
دوال معالجة القوائم للغة أوبال
"""


def get_module():
    """إرجاع دوال مكتبة القوائم / Return list module functions"""
    return {
        'length': len,
        'طول': len,
        'size': len,
        'push': _push,
        'أضف': _push,
        'pop': _pop,
        'pop': _pop,
        'shift': _shift,
        'unshift': _unshift,
        'insert': _insert,
        'أدرج': _insert,
        'remove': _remove,
        'احذف': _remove,
        'remove_at': _remove_at,
        'contains': lambda lst, item: item in lst,
        'يحتوي': lambda lst, item: item in lst,
        'index_of': _index_of,
        'موضع': _index_of,
        'reverse': _reverse,
        'عكس': _reverse,
        'sort': _sort,
        'رتب': _sort,
        'sum': sum,
        'مجموع': sum,
        'min': min,
        'الأصغر': min,
        'max': max,
        'الأكبر': max,
        'map': _map,
        'filter': _filter,
        'reduce': _reduce,
        'range': lambda n: list(range(int(n))),
        'نطاق': lambda n: list(range(int(n))),
        'flatten': _flatten,
        'سطح': _flatten,
        'slice': lambda lst, start, end: lst[int(start):int(end)],
        'شريحة': lambda lst, start, end: lst[int(start):int(end)],
        'zip': lambda a, b: list(zip(a, b)),
        'concat': lambda a, b: list(a) + list(b),
        'دمج_قوائم': lambda a, b: list(a) + list(b),
    }


def _push(lst, item):
    """إضافة عنصر للنهاية / Add item to end"""
    lst.append(item)
    return lst


def _pop(lst):
    """حذف من النهاية / Remove from end"""
    if lst:
        return lst.pop()
    return None


def _shift(lst):
    """حذف من البداية / Remove from beginning"""
    if lst:
        return lst.pop(0)
    return None


def _unshift(lst, item):
    """إضافة للبداية / Add to beginning"""
    lst.insert(0, item)
    return lst


def _insert(lst, index, item):
    """إدراج في موضع / Insert at position"""
    lst.insert(int(index), item)
    return lst


def _remove(lst, item):
    """حذف عنصر / Remove item"""
    try:
        lst.remove(item)
    except ValueError:
        pass
    return lst


def _remove_at(lst, index):
    """حذف من موضع / Remove at position"""
    idx = int(index)
    if 0 <= idx < len(lst):
        return lst.pop(idx)
    return None


def _index_of(lst, item):
    """موضع عنصر / Index of item"""
    try:
        return lst.index(item)
    except ValueError:
        return -1


def _reverse(lst):
    """عكس قائمة أو نص / Reverse a list or string"""
    if isinstance(lst, str):
        return lst[::-1]
    if isinstance(lst, list):
        return list(reversed(lst))
    return lst


def _sort(lst, key=None):
    """ترتيب قائمة / Sort a list"""
    return sorted(lst)


def _map(func, lst):
    """تطبيق دالة على كل عنصر / Apply function to each element"""
    return [func(item) for item in lst]


def _filter(func, lst):
    """تصفية قائمة / Filter a list"""
    return [item for item in lst if func(item)]


def _reduce(func, lst, initial=None):
    """تقليل قائمة / Reduce a list"""
    result = initial
    for item in lst:
        if result is None:
            result = item
        else:
            result = func(result, item)
    return result


def _flatten(lst):
    """تسطيح قائمة / Flatten nested list"""
    result = []
    for item in lst:
        if isinstance(item, list):
            result.extend(item)
        else:
            result.append(item)
    return result
