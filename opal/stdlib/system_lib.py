"""
Opal Standard Library - System / مكتبة النظام

System and OS-related functions.
دوال النظام ونظام التشغيل
"""

import os as _os
import sys as _sys
import platform as _platform
import subprocess as _subprocess


def get_module():
    """إرجاع دوال مكتبة النظام / Return system module functions"""
    return {
        'os': _get_os,
        'نظام': _get_os,
        'platform': _get_platform,
        'منصة': _get_platform,
        'cwd': _os.getcwd,
        'المجلد_الحالي': _os.getcwd,
        'chdir': _os.chdir,
        'تغيير_المجلد': _os.chdir,
        'list_dir': _list_dir,
        'list_files': _list_dir,
        'قائمة_الملفات': _list_dir,
        'exists': _os.path.exists,
        'موجود': _os.path.exists,
        'is_file': _os.path.isfile,
        'is_dir': _os.path.isdir,
        'mkdir': _os.mkdir,
        'أنشئ_مجلد': _os.mkdir,
        'remove': _os.remove,
        'احذف_ملف': _os.remove,
        'rmdir': _os.rmdir,
        'env': _os.getenv,
        'متغير_البيئة': _os.getenv,
        'exit': _sys.exit,
        'خروج': _sys.exit,
        'run': _run_command,
        'نفذ': _run_command,
        'python_version': _sys.version,
        'machine': _platform.machine,
    }


def _get_os():
    """اسم نظام التشغيل / Get OS name"""
    return _platform.system()


def _get_platform():
    """معلومات المنصة / Get platform info"""
    return {
        'system': _platform.system(),
        'release': _platform.release(),
        'version': _platform.version(),
        'machine': _platform.machine(),
        'processor': _platform.processor(),
        'python_version': _platform.python_version(),
    }


def _list_dir(path="."):
    """قائمة محتويات مجلد / List directory contents"""
    try:
        return _os.listdir(str(path))
    except Exception:
        return []


def _run_command(cmd):
    """تنفيذ أمر نظام / Run a system command"""
    try:
        result = _subprocess.run(
            str(cmd),
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        return {
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode,
        }
    except Exception as e:
        return {
            'stdout': '',
            'stderr': str(e),
            'returncode': -1,
        }
