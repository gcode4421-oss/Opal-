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
OPAL_VERSION = "2.0.0"


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
    opal <file.op>          تشغيل ملف أوبال / Run an Opal file
    opal <file.op> --verbose تشغيل مع التفاصيل / Run with verbose output
    opal --repl             واجهة تفاعلية / Start interactive REPL
    opal --version          عرض الإصدار / Show version
    opal --help             عرض هذه المساعدة / Show this help

Examples / أمثلة:
    opal hello.op
    opal examples/math_demo.op
    opal --repl

Features / المميزات:
    ✓ Support for Arabic and English keywords
    ✓ دعم الكلمات المفتاحية بالعربية والإنجليزية
    ✓ Easy syntax for beginners
    ✓ صياغة سهلة للمبتدئين
    ✓ Standard library (math, strings, lists, io, types)
    ✓ مكتبة قياسية شاملة
    ✓ Functions, loops, conditionals
    ✓ دوال، حلقات، جمل شرطية
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
    filepath = None

    for arg in args:
        if arg == '--help' or arg == '-h':
            show_help()
            sys.exit(0)
        elif arg == '--version' or arg == '-v':
            print(f"Opal {OPAL_VERSION}")
            sys.exit(0)
        elif arg == '--repl' or arg == '-r':
            use_repl = True
        elif arg == '--verbose':
            verbose = True
        elif arg.startswith('--'):
            print(f"خيار غير معروف: {arg} - Unknown option: {arg}")
            sys.exit(1)
        else:
            filepath = arg

    if use_repl:
        repl()
    elif filepath:
        run_file(filepath, verbose)
    else:
        show_help()


if __name__ == '__main__':
    main()
