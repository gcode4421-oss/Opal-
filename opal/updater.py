"""
Opal Language - Update Checker / مدقق التحديثات

Checks for updates from GitHub repository.
يتحقق من وجود تحديثات من مستودع GitHub

Features / المميزات:
- Check latest version from GitHub releases
- Compare with installed version
- Auto-update notification
- Update installation
"""

import os
import sys
import json
import urllib.request
import urllib.error
import subprocess
from . import __version__ as CURRENT_VERSION

# GitHub repository info / معلومات المستودع
GITHUB_REPO = "gcode4421-oss/Opal-"
GITHUB_API = f"https://api.github.com/repos/{GITHUB_REPO}"
GITHUB_RELEASES_URL = f"{GITHUB_API}/releases/latest"
GITHUB_REPO_URL = f"https://github.com/{GITHUB_REPO}"
GITHUB_RAW_URL = f"https://raw.githubusercontent.com/{GITHUB_REPO}/main"


def get_latest_version():
    """الحصول على أحدث إصدار من GitHub / Get latest version from GitHub"""
    try:
        req = urllib.request.Request(GITHUB_RELEASES_URL)
        req.add_header('User-Agent', 'Opal-Language-Update-Checker')
        req.add_header('Accept', 'application/vnd.github+json')

        # Use GITHUB_TOKEN if available to avoid rate limits
        # استخدم GITHUB_TOKEN إذا كان متاحاً لتجنب حدود المعدل
        github_token = os.environ.get('GITHUB_TOKEN') or os.environ.get('GH_TOKEN')
        if github_token:
            req.add_header('Authorization', f'token {github_token}')

        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            tag = data.get('tag_name', '').lstrip('v')
            return {
                'version': tag,
                'name': data.get('name', ''),
                'published_at': data.get('published_at', ''),
                'html_url': data.get('html_url', ''),
                'body': data.get('body', ''),
                'tarball_url': data.get('tarball_url', ''),
                'zipball_url': data.get('zipball_url', ''),
            }
    except urllib.error.HTTPError as e:
        if e.code == 403:
            return {'error': 'rate limit exceeded - حاول لاحقاً أو استخدم GITHUB_TOKEN'}
        return {'error': f'HTTP {e.code}: {e.reason}'}
    except urllib.error.URLError as e:
        return {'error': f'Network error: {str(e.reason)}'}
    except Exception as e:
        return {'error': str(e)}


def get_local_version():
    """الحصول على الإصدار المحلي / Get installed version"""
    return CURRENT_VERSION


def is_newer(remote_version, local_version):
    """مقارنة الإصدارات / Compare versions"""
    try:
        def parse(v):
            return [int(x) for x in v.split('.')]
        remote = parse(remote_version)
        local = parse(local_version)
        # Pad with zeros / إضافة أصفار
        while len(remote) < len(local):
            remote.append(0)
        while len(local) < len(remote):
            local.append(0)
        return remote > local
    except (ValueError, AttributeError):
        return False


def check_for_updates(silent=False):
    """التحقق من التحديثات / Check for updates"""
    local = get_local_version()

    if not silent:
        print(f"الإصدار الحالي: {local} / Current version: {local}")
        print(f"جارٍ التحقق من التحديثات... / Checking for updates...")

    result = get_latest_version()

    if 'error' in result:
        if not silent:
            print(f"❌ تعذر التحقق من التحديثات / Could not check for updates")
            print(f"   {result['error']}")
        return {
            'has_update': False,
            'error': result['error'],
            'local': local,
        }

    remote = result['version']

    if not remote:
        if not silent:
            print("❌ لا يوجد إصدار منشور / No release found")
        return {
            'has_update': False,
            'error': 'No release found',
            'local': local,
        }

    has_update = is_newer(remote, local)

    if not silent:
        print(f"الإصدار الأحدث: {remote} / Latest version: {remote}")
        print(f"تاريخ النشر: {result['published_at']}")
        print()

        if has_update:
            print("🎉 يوجد تحديث جديد! / Update available!")
            print(f"   {local} → {remote}")
            print()
            print("للتحديث / To update:")
            print(f"  opal update")
            print()
            print(f"التفاصيل: {result['html_url']}")
        else:
            print("✓ لديك أحدث إصدار / You have the latest version")

    return {
        'has_update': has_update,
        'local': local,
        'remote': remote,
        'info': result,
    }


def perform_update():
    """تثبيت التحديث / Perform the update"""
    print("============================================")
    print("  تحديث لغة أوبال / Update Opal Language")
    print("============================================")
    print()

    # First check if update is available / التحقق من وجود تحديث
    check = check_for_updates()

    if check.get('error') and 'Network' in str(check.get('error', '')):
        print("❌ لا يمكن الاتصال بالإنترنت / Cannot connect to internet")
        return False

    if not check.get('has_update'):
        print()
        print("✓ لديك أحدث إصدار بالفعل / Already up to date")
        return True

    print()
    print("جارٍ التحديث... / Updating...")
    print()

    # Try multiple update methods / تجربة طرق تحديث متعددة

    # Method 1: pip install from GitHub / الطريقة 1: من GitHub
    print("[1/3] محاولة التحديث من GitHub / Trying update from GitHub...")
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'install',
             f'git+https://github.com/{GITHUB_REPO}.git',
             '--upgrade', '--force-reinstall'],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode == 0:
            print("✓ تم التحديث بنجاح! / Update successful!")
            print()
            # Verify new version / التحقق من الإصدار الجديد
            try:
                # Re-import to get new version
                import importlib
                import opal
                importlib.reload(opal)
                new_version = opal.__version__
            except:
                new_version = check['remote']
            print(f"الإصدار الجديد: {new_version} / New version: {new_version}")
            return True
        else:
            print(f"  فشل: {result.stderr[:200]}")
    except Exception as e:
        print(f"  فشل: {e}")

    # Method 2: pip install with --break-system-packages / الطريقة 2
    print("[2/3] محاولة مع --break-system-packages / Trying with --break-system-packages...")
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'install',
             f'git+https://github.com/{GITHUB_REPO}.git',
             '--upgrade', '--force-reinstall', '--break-system-packages'],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode == 0:
            print("✓ تم التحديث بنجاح! / Update successful!")
            return True
        else:
            print(f"  فشل: {result.stderr[:200]}")
    except Exception as e:
        print(f"  فشل: {e}")

    # Method 3: From release wheel / الطريقة 3: من ملف الـ wheel
    print("[3/3] محاولة من ملف الـ wheel / Trying from release wheel...")
    try:
        wheel_url = f"https://github.com/{GITHUB_REPO}/releases/download/v{check['remote']}/opal_lang-{check['remote']}-py3-none-any.whl"
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'install',
             wheel_url, '--force-reinstall'],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode == 0:
            print("✓ تم التحديث بنجاح! / Update successful!")
            return True
        else:
            print(f"  فشل: {result.stderr[:200]}")
    except Exception as e:
        print(f"  فشل: {e}")

    print()
    print("❌ فشل التحديث التلقائي / Auto-update failed")
    print()
    print("التحديث اليدوي / Manual update:")
    print(f"  pip install --upgrade git+https://github.com/{GITHUB_REPO}.git")
    print()
    print(f"أو حمّل من: {check['info'].get('html_url', GITHUB_REPO_URL)}")
    return False


def show_version_info():
    """عرض معلومات الإصدار / Show version information"""
    local = get_local_version()
    print()
    print("============================================")
    print("  معلومات إصدار أوبال / Opal Version Info")
    print("============================================")
    print()
    print(f"الإصدار الحالي / Current: {local}")
    print(f"المستودع / Repository: {GITHUB_REPO_URL}")
    print()

    print("جارٍ التحقق من أحدث إصدار... / Checking latest...")
    result = get_latest_version()

    if 'error' in result:
        print(f"❌ تعذر التحقق / Could not check: {result['error']}")
        return

    remote = result.get('version', 'غير معروف')
    print(f"الإصدار الأحدث / Latest: {remote}")

    if remote and is_newer(remote, local):
        print()
        print("🎉 يوجد تحديث جديد! / Update available!")
        print(f"   {local} → {remote}")
        print(f"   للتحديث / To update: opal update")
    elif remote == local:
        print()
        print("✓ لديك أحدث إصدار / You have the latest version")
    else:
        print()
        print(f"ℹ️  الإصدار المحلي أحدث من المنشور / Local is newer than published")
        print(f"   المحلي: {local}")
        print(f"   المنشور: {remote}")

    print()
    if result.get('published_at'):
        print(f"تاريخ النشر / Published: {result['published_at']}")
    if result.get('html_url'):
        print(f"الرابط / URL: {result['html_url']}")
    print()


def auto_check_update():
    """فحص تلقائي صامت - يُستدعى عند بدء التشغيل / Silent check on startup"""
    try:
        check = check_for_updates(silent=True)
        if check.get('has_update'):
            local = check['local']
            remote = check['remote']
            print()
            print("┌─────────────────────────────────────────────┐")
            print("│  🎉 تحديث جديد متاح! / Update available!    │")
            print(f"│  {local} → {remote}                          │")
            print("│  شغّل / Run: opal update                     │")
            print("└─────────────────────────────────────────────┘")
            print()
    except Exception:
        # Silent fail - don't interrupt user / فشل صامت
        pass
