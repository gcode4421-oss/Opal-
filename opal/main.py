#!/usr/bin/env python3
"""
Opal Language - Main Entry Point / نقطة الدخول الرئيسية

CLI interface for running Opal files.
واجهة سطر الأوامر لتشغيل ملفات أوبال

Usage / الاستخدام:
    opal file.op
    opal file.op --verbose
    opal --version
    opal --help
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from opal.lexer import Lexer, LexError
from opal.parser import Parser, ParseError
from opal.interpreter import Interpreter, OpalError


# Version / الإصدار
OPAL_VERSION = "2.3.0"


def run_file(filepath, verbose=False):
    """تشغيل ملف أوبال / Run an Opal file"""
    if not os.path.exists(filepath):
        print(f"خطأ: الملف '{filepath}' غير موجود - Error: File '{filepath}' not found")
        sys.exit(1)

    if not filepath.endswith('.op'):
        print(f"تحذير: الملف لا ينتهي بـ .op - Warning: file doesn't end with .op")

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            source = f.read()
    except Exception as e:
        print(f"خطأ في قراءة الملف - Error reading file: {e}")
        sys.exit(1)

    run_source(source, filepath, verbose)


def run_source(source, filepath="<stdin>", verbose=False):
    """تشغيل كود أوبال / Run Opal source code"""
    # Change to file's directory for relative imports
    if filepath != "<stdin>":
        old_cwd = os.getcwd()
        file_dir = os.path.dirname(os.path.abspath(filepath))
        os.chdir(file_dir)

    try:
        # Step 1: Lexing / التحليل اللغوي
        if verbose:
            print("--- Lexing (التحليل اللغوي) ---")

        lexer = Lexer(source)
        tokens = lexer.tokenize()

        if verbose:
            print(f"Generated {len(tokens)} tokens")

        # Step 2: Parsing / التحليل النحوي
        if verbose:
            print("--- Parsing (التحليل النحوي) ---")

        parser = Parser(tokens)
        program = parser.parse()

        if verbose:
            print(f"Parsed {len(program.statements)} statements")

        # Step 3: Interpretation / التفسير
        if verbose:
            print("--- Running (التشغيل) ---")

        interpreter = Interpreter()
        interpreter.interpret(program)

    except LexError as e:
        print(f"\n❌ {e}", file=sys.stderr)
        _show_error_context(source, filepath, e.line)
        sys.exit(1)
    except ParseError as e:
        print(f"\n❌ {e}", file=sys.stderr)
        _show_error_context(source, filepath, e.line)
        sys.exit(1)
    except OpalError as e:
        print(f"\n❌ خطأ في وقت التشغيل (Runtime Error): {e}", file=sys.stderr)
        sys.exit(1)
    except ReturnSignal:
        pass
    except Exception as e:
        print(f"\n❌ خطأ غير متوقع (Unexpected Error): {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        if filepath != "<stdin>":
            os.chdir(old_cwd)


def run_with_vm(filepath, verbose=False):
    """تشغيل ملف أوبال بالـ VM الخاص / Run Opal file with native VM"""
    if not os.path.exists(filepath):
        print(f"خطأ: الملف '{filepath}' غير موجود - Error: File '{filepath}' not found")
        sys.exit(1)

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            source = f.read()
    except Exception as e:
        print(f"خطأ في قراءة الملف - Error reading file: {e}")
        sys.exit(1)

    try:
        from opal.vm import run_with_vm as vm_run

        if verbose:
            print("--- Running with Opal Bytecode VM ---")
            print("--- التشغيل بـ VM الخاص بأوبال ---")

        vm_run(source)

    except (LexError, ParseError, OpalError) as e:
        print(f"\n❌ {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ خطأ غير متوقع (Unexpected Error): {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


def _show_error_context(source, filepath, line_num):
    """عرض السياق حول الخطأ / Show context around error"""
    lines = source.split('\n')
    if 1 <= line_num <= len(lines):
        print(f"\n  {filepath}:{line_num}", file=sys.stderr)
        # Show lines around the error
        start = max(0, line_num - 2)
        end = min(len(lines), line_num + 1)
        for i in range(start, end):
            marker = " >>> " if (i + 1) == line_num else "     "
            print(f"  {marker}{i+1:4d} | {lines[i]}", file=sys.stderr)


# Re-import for error handling
from opal.interpreter import ReturnSignal


def repl():
    """REPL - واجهة تفاعلية / Interactive REPL"""
    print(f"""
╔══════════════════════════════════════╗
║   Opal Language v{OPAL_VERSION}            ║
║   لغة أوبال - REPL تفاعلي           ║
╚══════════════════════════════════════╝

اكتب 'خروج' أو 'exit' للخروج
Type 'exit' to quit
""")

    interpreter = Interpreter()

    while True:
        try:
            line = input('opal> ')
            if line.strip().lower() in ('exit', 'quit', 'خروج'):
                print("وداعاً! / Goodbye!")
                break
            if not line.strip():
                continue

            # Lex and parse
            lexer = Lexer(line)
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            program = parser.parse()

            # Execute
            try:
                interpreter.interpret(program)
            except ReturnSignal as r:
                if r.value is not None:
                    print(interpreter.opal_to_string(r.value))

        except (LexError, ParseError, OpalError) as e:
            print(f"خطأ: {e}")
        except KeyboardInterrupt:
            print("\nوداعاً! / Goodbye!")
            break
        except Exception as e:
            print(f"خطأ: {e}")


def show_help():
    """عرض المساعدة / Show help"""
    print(f"""
Opal Language v{OPAL_VERSION} - لغة أوبال للبرمجة

Usage / الاستخدام:
    opal <file.op>              تشغيل ملف أوبال / Run an Opal file
    opal <file.op> --verbose    تشغيل مع التفاصيل / Run with verbose output
    opal <file.op> --compile-c  تحويل إلى C / Transpile to C code
    opal <file.op> --compile-c -o out.c  تحديد ملف الإخراج
    opal --repl                 واجهة تفاعلية / Start interactive REPL
    opal --version              عرض الإصدار مع فحص التحديثات / Show version + check updates
    opal version                نفس الأمر / Same as --version
    opal up                     التحقق من التحديثات / Check for updates
    opal update                 تثبيت أحدث إصدار / Install latest version
    opal --help                 عرض هذه المساعدة / Show this help
    opal --no-update-check      تخطي فحص التحديث التلقائي / Skip auto update check

Examples / أمثلة:
    opal hello.op
    opal examples/math_demo.op
    opal --repl
    opal program.op --compile-c
    opal up                     فحص التحديثات
    opal update                 تحديث اللغة

Features / المميزات:
    ✓ Support for Arabic and English keywords
    ✓ دعم الكلمات المفتاحية بالعربية والإنجليزية
    ✓ Easy syntax for beginners
    ✓ صياغة سهلة للمبتدئين
    ✓ Object-Oriented Programming (classes, inheritance)
    ✓ البرمجة الكائنية (صفوف، وراثة)
    ✓ Error handling (try/catch/finally)
    ✓ معالجة الأخطاء
    ✓ Lambda functions, dictionaries, switch
    ✓ الدوال المجهولة، القواميس، التبديل
    ✓ Standard library (math, strings, lists, io, json, http, file, time, system, lowlevel)
    ✓ مكتبة قياسية شاملة
    ✓ C transpiler for systems programming
    ✓ مولّد كود C لبرمجة الأنظمة
""")


def main():
    """نقطة الدخول الرئيسية / Main entry point"""
    args = sys.argv[1:]

    if len(args) == 0:
        show_help()
        sys.exit(0)

    # Parse arguments
    verbose = False
    use_repl = False
    compile_c = False
    use_vm = False
    output_path = None
    filepath = None
    color_mode = None  # None = auto, 'always', 'never'

    i = 0
    while i < len(args):
        arg = args[i]
        if arg == '--help' or arg == '-h':
            show_help()
            sys.exit(0)
        elif arg == '--version' or arg == '-v' or arg == 'version':
            # Show version info with update check / عرض معلومات الإصدار مع فحص التحديث
            from opal.updater import show_version_info
            show_version_info()
            sys.exit(0)
        elif arg == 'up' or arg == 'update-check' or arg == '--check-update':
            # Check for updates / التحقق من التحديثات
            from opal.updater import check_for_updates
            check_for_updates()
            sys.exit(0)
        elif arg == 'update' or arg == 'upgrade':
            # Perform update / تنفيذ التحديث
            from opal.updater import perform_update
            perform_update()
            sys.exit(0)
        elif arg == '--no-update-check':
            # Skip auto update check / تخطي الفحص التلقائي
            pass  # Handled below
        elif arg == '--repl' or arg == '-r':
            use_repl = True
        elif arg == '--verbose':
            verbose = True
        elif arg == '--compile-c' or arg == '--cc':
            compile_c = True
        elif arg == '--vm' or arg == '--bytecode':
            use_vm = True
        elif arg == '--color':
            i += 1
            if i < len(args):
                color_mode = args[i]
        elif arg == '--color=always':
            color_mode = 'always'
        elif arg == '--color=never':
            color_mode = 'never'
        elif arg == '--color=auto':
            color_mode = 'auto'
        elif arg == '-o':
            i += 1
            if i < len(args):
                output_path = args[i]
        elif arg.startswith('--'):
            print(f"خيار غير معروف: {arg} - Unknown option: {arg}")
            sys.exit(1)
        else:
            filepath = arg
        i += 1

    # Apply color mode / تطبيق وضع الألوان
    if color_mode == 'always':
        import os
        os.environ['FORCE_COLOR'] = '1'
    elif color_mode == 'never':
        import os
        os.environ['NO_COLOR'] = '1'

    # Auto update check (silent) - skip if disabled
    # فحص تلقائي للتحديثات (صامت) - يتخطى إذا كان معطلاً
    if '--no-update-check' not in args:
        try:
            from opal.updater import auto_check_update
            auto_check_update()
        except Exception:
            pass  # Silent fail / فشل صامت

    if use_repl:
        repl()
    elif filepath:
        if compile_c:
            # Compile to C / تحويل إلى C
            from opal.c_transpiler import compile_file
            compile_file(filepath, output_path)
        elif use_vm:
            # Run via Opal Bytecode VM / تشغيل عبر VM الخاص بأوبال
            run_with_vm(filepath, verbose)
        else:
            run_file(filepath, verbose)
    else:
        show_help()


if __name__ == '__main__':
    main()
