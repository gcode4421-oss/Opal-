"""
Opal Standard Library - File System / مكتبة نظام الملفات

File and directory operations.
عمليات الملفات والمجلدات
"""

import os as _os
import shutil as _shutil


def get_module():
    """إرجاع دوال مكتبة الملفات / Return file system module functions"""
    return {
        # Reading / القراءة
        'read': _read_file,
        'اقرأ': _read_file,
        'read_file': _read_file,
        'read_lines': _read_lines,
        'اقرأ_أسطر': _read_lines,
        'read_text': _read_file,
        'read_bytes': _read_bytes,

        # Writing / الكتابة
        'write': _write_file,
        'اكتب': _write_file,
        'write_file': _write_file,
        'write_text': _write_file,
        'append': _append_file,
        'أضف': _append_file,
        'append_file': _append_file,

        # File info / معلومات الملف
        'size': _file_size,
        'حجم': _file_size,
        'file_size': _file_size,
        'modified': _modified_time,
        'معدل': _modified_time,
        'abspath': lambda p: _os.path.abspath(str(p)),
        'مسار_مطلق': lambda p: _os.path.abspath(str(p)),
        'basename': lambda p: _os.path.basename(str(p)),
        'اسم_الملف': lambda p: _os.path.basename(str(p)),
        'dirname': lambda p: _os.path.dirname(str(p)),
        'اسم_المجلد': lambda p: _os.path.dirname(str(p)),
        'splitext': lambda p: list(_os.path.splitext(str(p))),

        # Directory operations / عمليات المجلد
        'list_dir': _list_dir,
        'list_files': _list_dir,
        'قائمة': _list_dir,
        'walk': _walk,
        'تجول': _walk,
        'mkdir': _make_dir,
        'أنشئ_مجلد': _make_dir,
        'makedirs': lambda p: _os.makedirs(str(p), exist_ok=True),
        'rmdir': lambda p: _os.rmdir(str(p)),
        'rmtree': lambda p: _shutil.rmtree(str(p), ignore_errors=True),

        # Copy/Move / نسخ/نقل
        'copy': _copy,
        'نسخ': _copy,
        'copy_file': _copy,
        'move': _move,
        'انقل': _move,
        'rename': _move,
        'أعد_تسمية': _move,

        # Existence / الوجود
        'exists': lambda p: _os.path.exists(str(p)),
        'موجود': lambda p: _os.path.exists(str(p)),
        'is_file': lambda p: _os.path.isfile(str(p)),
        'is_dir': lambda p: _os.path.isdir(str(p)),
        'is_directory': lambda p: _os.path.isdir(str(p)),

        # Path operations / عمليات المسار
        'join': _path_join,
        'دمج_المسار': _path_join,
        'separator': _os.sep,
        'فاصل': _os.sep,
    }


def _read_file(path, encoding='utf-8'):
    """قراءة ملف / Read file contents"""
    try:
        with open(str(path), 'r', encoding=encoding) as f:
            return f.read()
    except Exception as e:
        return None


def _read_lines(path, encoding='utf-8'):
    """قراءة أسطر ملف / Read file as lines"""
    try:
        with open(str(path), 'r', encoding=encoding) as f:
            return f.read().splitlines()
    except Exception:
        return []


def _read_bytes(path):
    """قراءة ملف كبايتات / Read file as bytes"""
    try:
        with open(str(path), 'rb') as f:
            return f.read()
    except Exception:
        return None


def _write_file(path, content, encoding='utf-8'):
    """كتابة ملف / Write to file"""
    try:
        with open(str(path), 'w', encoding=encoding) as f:
            f.write(str(content))
        return True
    except Exception:
        return False


def _append_file(path, content, encoding='utf-8'):
    """إضافة لمحتوى ملف / Append to file"""
    try:
        with open(str(path), 'a', encoding=encoding) as f:
            f.write(str(content))
        return True
    except Exception:
        return False


def _file_size(path):
    """حجم الملف بالبايت / File size in bytes"""
    try:
        return _os.path.getsize(str(path))
    except Exception:
        return -1


def _modified_time(path):
    """وقت آخر تعديل / Last modified time"""
    try:
        return _os.path.getmtime(str(path))
    except Exception:
        return 0


def _list_dir(path='.'):
    """قائمة محتويات مجلد / List directory contents"""
    try:
        return _os.listdir(str(path))
    except Exception:
        return []


def _walk(path):
    """التجول في شجرة المجلدات / Walk directory tree"""
    result = []
    try:
        for root, dirs, files in _os.walk(str(path)):
            for f in files:
                result.append(_os.path.join(root, f))
    except Exception:
        pass
    return result


def _make_dir(path):
    """إنشاء مجلد / Create directory"""
    try:
        _os.mkdir(str(path))
        return True
    except Exception:
        return False


def _copy(src, dst):
    """نسخ ملف / Copy file"""
    try:
        _shutil.copy2(str(src), str(dst))
        return True
    except Exception:
        return False


def _move(src, dst):
    """نقل/إعادة تسمية / Move/rename"""
    try:
        _shutil.move(str(src), str(dst))
        return True
    except Exception:
        return False


def _path_join(*parts):
    """دمج أجزاء المسار / Join path parts"""
    return _os.path.join(*[str(p) for p in parts])
