#!/usr/bin/env python3
"""
Opal Package Installer (opi) / مثبّت حزم أوبال

Package manager for Opal - like pip but for Opal packages.
مدير حزم لأوبال - مثل pip لكن لحزم أوبال

Usage / الاستخدام:
    opi install <package>      Install a package / تثبيت حزمة
    opi uninstall <package>    Remove a package / إزالة حزمة
    opi list                   List installed packages / قائمة الحزم
    opi search <query>         Search packages / البحث عن حزم
    opi info <package>         Show package info / معلومات حزمة
    opi update <package>       Update a package / تحديث حزمة
    opi update --all           Update all packages / تحديث كل الحزم
    opi init                   Initialize new package / إنشاء حزمة جديدة
    opi publish                Publish package / نشر حزمة
    opi repo list              List repositories / قائمة المستودعات
    opi repo add <url>         Add repository / إضافة مستودع
    opi --version              Show version / عرض الإصدار
    opi --help                 Show help / عرض المساعدة
"""

import sys
import os
import json
import urllib.request
import urllib.error
import subprocess
import shutil
from pathlib import Path


# Version / الإصدار
OPI_VERSION = "1.0.0"

# Opal packages directory / مجلد حزم أوبال
OPAL_HOME = os.environ.get('OPAL_HOME', os.path.expanduser('~/.opal'))
OPAL_PACKAGES_DIR = os.path.join(OPAL_HOME, 'packages')
OPAL_CONFIG_FILE = os.path.join(OPAL_HOME, 'config.json')
OPAL_REGISTRY_FILE = os.path.join(OPAL_HOME, 'registry.json')

# Default registry (Opal Package Repository) / المستودع الافتراضي
DEFAULT_REGISTRY = "https://raw.githubusercontent.com/gcode4421-oss/opal-packages/main/registry.json"


def ensure_dirs():
    """التأكد من وجود المجلدات / Ensure directories exist"""
    os.makedirs(OPAL_PACKAGES_DIR, exist_ok=True)
    if not os.path.exists(OPAL_CONFIG_FILE):
        # Write directly to avoid recursion / كتابة مباشرة لتجنب الحلقة
        config = {
            'version': OPI_VERSION,
            'repositories': [DEFAULT_REGISTRY],
            'installed': {}
        }
        try:
            with open(OPAL_CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except:
            pass


def load_config():
    """تحميل الإعدادات / Load configuration"""
    ensure_dirs()
    try:
        with open(OPAL_CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {
            'version': OPI_VERSION,
            'repositories': [DEFAULT_REGISTRY],
            'installed': {}
        }


def save_config(config):
    """حفظ الإعدادات / Save configuration"""
    os.makedirs(OPAL_HOME, exist_ok=True)
    os.makedirs(OPAL_PACKAGES_DIR, exist_ok=True)
    try:
        with open(OPAL_CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    except:
        pass


def fetch_registry():
    """جلب سجل الحزم من المستودع / Fetch package registry"""
    config = load_config()
    all_packages = {}

    for repo_url in config.get('repositories', [DEFAULT_REGISTRY]):
        try:
            req = urllib.request.Request(repo_url)
            req.add_header('User-Agent', 'opi-package-manager')
            with urllib.request.urlopen(req, timeout=30) as response:
                data = json.loads(response.read().decode('utf-8'))
                if 'packages' in data:
                    for pkg in data['packages']:
                        all_packages[pkg['name']] = pkg
        except Exception as e:
            print(f"  ⚠️  تعذر جلب المستودع / Could not fetch repo: {repo_url}")
            print(f"     {e}")

    return all_packages


def install_package(package_name, version=None):
    """تثبيت حزمة / Install a package"""
    print(f"📦 تثبيت حزمة / Installing: {package_name}")

    # Fetch registry / جلب السجل
    print("  جارٍ جلب سجل الحزم... / Fetching package registry...")
    registry = fetch_registry()

    if package_name not in registry:
        print(f"❌ الحزمة '{package_name}' غير موجودة / Package not found")
        print(f"   استخدم 'opi search {package_name}' للبحث / Use search to find packages")
        return False

    pkg = registry[package_name]

    if version and pkg.get('version') != version:
        print(f"⚠️  الإصدار المطلوب {version} غير متاح، المتاح: {pkg.get('version')}")

    print(f"  الحزمة: {pkg['name']} v{pkg.get('version', '1.0.0')}")
    print(f"  الوصف: {pkg.get('description', 'No description')}")

    # Download package / تحميل الحزمة
    download_url = pkg.get('download_url') or pkg.get('url')
    if not download_url:
        print(f"❌ لا يوجد رابط تحميل / No download URL")
        return False

    pkg_dir = os.path.join(OPAL_PACKAGES_DIR, package_name)
    os.makedirs(pkg_dir, exist_ok=True)

    print(f"  جارٍ التحميل... / Downloading...")
    try:
        req = urllib.request.Request(download_url)
        req.add_header('User-Agent', 'opi-package-manager')
        with urllib.request.urlopen(req, timeout=60) as response:
            content = response.read()

        # Save package file / حفظ ملف الحزمة
        pkg_file = os.path.join(pkg_dir, f"{package_name}.op")
        with open(pkg_file, 'wb') as f:
            f.write(content)

        # Save metadata / حفظ البيانات الوصفية
        meta = {
            'name': pkg['name'],
            'version': pkg.get('version', '1.0.0'),
            'description': pkg.get('description', ''),
            'author': pkg.get('author', ''),
            'installed_at': str(__import__('datetime').datetime.now()),
        }
        with open(os.path.join(pkg_dir, 'package.json'), 'w', encoding='utf-8') as f:
            json.dump(meta, f, indent=2, ensure_ascii=False)

        # Update config / تحديث الإعدادات
        config = load_config()
        config['installed'][package_name] = meta
        save_config(config)

        print(f"✅ تم تثبيت {package_name} بنجاح! / Installed successfully!")
        print(f"   المسار: {pkg_dir}")
        return True

    except Exception as e:
        print(f"❌ فشل التحميل / Download failed: {e}")
        return False


def uninstall_package(package_name):
    """إزالة حزمة / Uninstall a package"""
    print(f"🗑️  إزالة حزمة / Removing: {package_name}")

    config = load_config()
    if package_name not in config.get('installed', {}):
        print(f"❌ الحزمة '{package_name}' غير مثبتة / Package not installed")
        return False

    pkg_dir = os.path.join(OPAL_PACKAGES_DIR, package_name)
    if os.path.exists(pkg_dir):
        shutil.rmtree(pkg_dir)

    del config['installed'][package_name]
    save_config(config)

    print(f"✅ تم إزالة {package_name} / Removed successfully!")
    return True


def list_packages():
    """قائمة الحزم المثبتة / List installed packages"""
    config = load_config()
    installed = config.get('installed', {})

    if not installed:
        print("📭 لا توجد حزم مثبتة / No packages installed")
        print("   استخدم 'opi install <package>' للتثبيت")
        return

    print(f"📋 الحزم المثبتة ({len(installed)}) / Installed packages:")
    print()
    for name, meta in installed.items():
        version = meta.get('version', '?')
        desc = meta.get('description', '')
        print(f"  {name} v{version}")
        if desc:
            print(f"    {desc}")
    print()


def search_packages(query):
    """البحث عن حزم / Search packages"""
    print(f"🔍 البحث عن: '{query}' / Searching for: '{query}'")
    print()

    registry = fetch_registry()
    results = []

    query_lower = query.lower()
    for name, pkg in registry.items():
        if query_lower in name.lower() or query_lower in pkg.get('description', '').lower():
            results.append((name, pkg))

    if not results:
        print("❌ لا توجد نتائج / No results found")
        return

    print(f" Found {len(results)} packages / تم العثور على {len(results)} حزمة:")
    print()
    for name, pkg in results:
        version = pkg.get('version', '?')
        desc = pkg.get('description', 'No description')
        print(f"  {name} v{version}")
        print(f"    {desc}")
    print()


def package_info(package_name):
    """معلومات حزمة / Show package info"""
    registry = fetch_registry()

    if package_name not in registry:
        # Check if installed / تحقق إذا كانت مثبتة
        config = load_config()
        if package_name in config.get('installed', {}):
            print(f"📦 {package_name} (installed / مثبتة)")
            meta = config['installed'][package_name]
            for k, v in meta.items():
                print(f"  {k}: {v}")
            return
        print(f"❌ الحزمة '{package_name}' غير موجودة / Package not found")
        return

    pkg = registry[package_name]
    print(f"📦 {pkg['name']}")
    print(f"   Version: {pkg.get('version', '?')}")
    print(f"   Description: {pkg.get('description', 'No description')}")
    print(f"   Author: {pkg.get('author', 'Unknown')}")
    print(f"   License: {pkg.get('license', 'MIT')}")
    print(f"   Homepage: {pkg.get('homepage', 'N/A')}")
    print(f"   Download: {pkg.get('download_url', pkg.get('url', 'N/A'))}")

    config = load_config()
    if package_name in config.get('installed', {}):
        print(f"   Status: ✅ مثبتة / Installed")
    else:
        print(f"   Status: ❌ غير مثبتة / Not installed")


def update_package(package_name=None):
    """تحديث حزمة أو كل الحزم / Update a package or all"""
    config = load_config()
    installed = config.get('installed', {})

    if not installed:
        print("📭 لا توجد حزم مثبتة / No packages installed")
        return

    if package_name == '--all' or package_name is None:
        print(f"🔄 تحديث كل الحزم ({len(installed)}) / Updating all packages...")
        for name in list(installed.keys()):
            print()
            uninstall_package(name)
            install_package(name)
    else:
        if package_name not in installed:
            print(f"❌ الحزمة '{package_name}' غير مثبتة / Package not installed")
            return
        print(f"🔄 تحديث {package_name} / Updating...")
        uninstall_package(package_name)
        install_package(package_name)


def init_package():
    """إنشاء حزمة جديدة / Initialize new package"""
    print("📦 إنشاء حزمة أوبال جديدة / Create new Opal package")
    print()

    try:
        name = input("اسم الحزمة / Package name: ").strip()
        if not name:
            print("❌ الاسم مطلوب / Name required")
            return

        description = input("الوصف / Description: ").strip()
        author = input("المؤلف / Author: ").strip()
        version = input("الإصدار [1.0.0] / Version [1.0.0]: ").strip() or "1.0.0"
        license_choice = input("الترخيص [MIT] / License [MIT]: ").strip() or "MIT"
    except (EOFError, KeyboardInterrupt):
        print("\n❌ تم الإلغاء / Cancelled")
        return

    # Create package directory / إنشاء مجلد الحزمة
    pkg_dir = os.path.join(os.getcwd(), name)
    if os.path.exists(pkg_dir):
        print(f"❌ المجلد '{name}' موجود / Directory exists")
        return

    os.makedirs(pkg_dir)

    # Create package.json / إنشاء package.json
    package_json = {
        'name': name,
        'version': version,
        'description': description,
        'author': author,
        'license': license_choice,
        'main': f'{name}.op',
        'dependencies': [],
    }

    with open(os.path.join(pkg_dir, 'package.json'), 'w', encoding='utf-8') as f:
        json.dump(package_json, f, indent=2, ensure_ascii=False)

    # Create main .op file / إنشاء الملف الرئيسي
    main_content = f"""// {name} - {description}
// {author}
// v{version}

// Example function / دالة مثال
function hello() {{
    return "Hello from {name}!"
}}
"""
    with open(os.path.join(pkg_dir, f'{name}.op'), 'w', encoding='utf-8') as f:
        f.write(main_content)

    # Create README / إنشاء README
    readme = f"""# {name}

{description}

## Installation / التثبيت
```bash
opi install {name}
```

## Usage / الاستخدام
```opal
import {name}
echo hello()
```

## Author / المؤلف
{author}

## License / الترخيص
{license_choice}
"""
    with open(os.path.join(pkg_dir, 'README.md'), 'w', encoding='utf-8') as f:
        f.write(readme)

    print(f"\n✅ تم إنشاء الحزمة! / Package created!")
    print(f"   المسار: {pkg_dir}")
    print(f"   الملفات: package.json, {name}.op, README.md")
    print()
    print("   للنشر: / To publish:")
    print(f"   cd {name}")
    print("   opi publish")


def show_help():
    """عرض المساعدة / Show help"""
    print(f"""
Opal Package Installer (opi) v{OPI_VERSION}
مثبّت حزم أوبال

Usage / الاستخدام:
    opi install <package>      تثبيت حزمة / Install a package
    opi uninstall <package>    إزالة حزمة / Remove a package
    opi list                   قائمة الحزم / List installed packages
    opi search <query>         البحث / Search packages
    opi info <package>         معلومات / Show package info
    opi update [package]       تحديث / Update package(s)
    opi update --all           تحديث الكل / Update all packages
    opi init                   حزمة جديدة / Create new package
    opi publish                نشر / Publish package
    opi repo list              المستودعات / List repositories
    opi repo add <url>         إضافة مستودع / Add repository
    opi repo remove <url>      حذف مستودع / Remove repository
    opi --version              الإصدار / Show version
    opi --help                 المساعدة / Show help

Examples / أمثلة:
    opi install utils
    opi install math-lib@2.0
    opi search "math"
    opi list
    opi info utils

Package directory: {OPAL_PACKAGES_DIR}
""")


def main():
    """نقطة الدخول الرئيسية / Main entry point"""
    if len(sys.argv) < 2:
        show_help()
        sys.exit(0)

    command = sys.argv[1]
    args = sys.argv[2:]

    if command in ('--help', '-h', 'help'):
        show_help()
    elif command in ('--version', '-v', 'version'):
        print(f"opi v{OPI_VERSION}")
    elif command == 'install':
        if not args:
            print("❌ استخدم: opi install <package>")
            sys.exit(1)
        install_package(args[0])
    elif command in ('uninstall', 'remove'):
        if not args:
            print("❌ استخدم: opi uninstall <package>")
            sys.exit(1)
        uninstall_package(args[0])
    elif command == 'list':
        list_packages()
    elif command == 'search':
        if not args:
            print("❌ استخدم: opi search <query>")
            sys.exit(1)
        search_packages(args[0])
    elif command == 'info':
        if not args:
            print("❌ استخدم: opi info <package>")
            sys.exit(1)
        package_info(args[0])
    elif command == 'update':
        if not args or args[0] == '--all':
            update_package('--all')
        else:
            update_package(args[0])
    elif command == 'init':
        init_package()
    elif command == 'repo':
        if not args:
            print("استخدم: opi repo list|add|remove")
            sys.exit(1)
        subcmd = args[0]
        config = load_config()
        if subcmd == 'list':
            print("📋 المستودعات / Repositories:")
            for repo in config.get('repositories', []):
                print(f"  - {repo}")
        elif subcmd == 'add' and len(args) > 1:
            if args[1] not in config['repositories']:
                config['repositories'].append(args[1])
                save_config(config)
                print(f"✅ تمت الإضافة / Added: {args[1]}")
        elif subcmd == 'remove' and len(args) > 1:
            if args[1] in config['repositories']:
                config['repositories'].remove(args[1])
                save_config(config)
                print(f"✅ تم الحذف / Removed: {args[1]}")
    elif command == 'publish':
        print("📦 النشر غير متاح بعد / Publishing not yet available")
        print("   سيتم إضافته في الإصدار القادم / Coming soon")
    else:
        print(f"❌ أمر غير معروف: {command}")
        show_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
