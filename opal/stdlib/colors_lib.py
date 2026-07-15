"""
Opal Standard Library - Colors & Terminal / مكتبة الألوان والطرفية

Provides ANSI color codes and terminal control for colored output.
توفر رموز ANSI للألوان والتحكم بالطرفية للمخرجات الملونة

Features / المميزات:
- Foreground colors (16 colors + 256 colors + RGB)
- Background colors
- Text styles (bold, italic, underline, etc.)
- Terminal control (clear, cursor, etc.)
- Arabic text support helpers
- RTL text helpers

ملاحظة: الألوان تعمل على معظم الطرفيات الحديثة
Note: Colors work on most modern terminals
"""

import os
import sys

# Detect if colors are supported / كشف دعم الألوان
def _supports_color():
    """تحقق من دعم الطرفية للألوان / Check if terminal supports colors"""
    # Check for force color environment variables
    # التحقق من متغيرات بيئة إجبار الألوان
    if os.environ.get('FORCE_COLOR') or os.environ.get('CLICOLOR_FORCE'):
        return True
    
    # Check for NO_COLOR (disables colors)
    if os.environ.get('NO_COLOR'):
        return False
    
    if sys.platform == 'win32':
        # Windows 10+ supports ANSI
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
            handle = kernel32.GetStdHandle(-11)
            mode = ctypes.c_uint32()
            kernel32.GetConsoleMode(handle, ctypes.byref(mode))
            kernel32.SetConsoleMode(handle, mode.value | ENABLE_VIRTUAL_TERMINAL_PROCESSING)
            return True
        except:
            return False
    
    # Unix-like: check if stdout is a tty
    if hasattr(sys.stdout, 'isatty') and sys.stdout.isatty():
        term = os.environ.get('TERM', '')
        if term and term != 'dumb':
            return True
    return False


_COLOR_SUPPORTED = _supports_color()


def _is_color_supported():
    """تحقق ديناميكي من دعم الألوان / Dynamic check for color support"""
    # Re-check environment each time (allows runtime changes)
    # إعادة التحقق من البيئة في كل مرة (يسمح بالتغييرات أثناء التشغيل)
    if os.environ.get('FORCE_COLOR') or os.environ.get('CLICOLOR_FORCE'):
        return True
    if os.environ.get('NO_COLOR'):
        return False
    return _COLOR_SUPPORTED


def enable_colors():
    """إجبار تفعيل الألوان / Force enable colors"""
    global _COLOR_SUPPORTED
    _COLOR_SUPPORTED = True
    os.environ['FORCE_COLOR'] = '1'


def disable_colors():
    """تعطيل الألوان / Disable colors"""
    global _COLOR_SUPPORTED
    _COLOR_SUPPORTED = False
    os.environ['NO_COLOR'] = '1'


# ==============================================================
# ANSI Color Codes / رموز ANSI للألوان
# These are computed dynamically based on color support
# تُحسب ديناميكياً بناءً على دعم الألوان
# ==============================================================

def _c(code):
    """يُرجع كود ANSI إذا كانت الألوان مدعومة، وإلا نص فارغ / Return ANSI code if colors supported"""
    return code if _is_color_supported() else ''


class _ColorCode:
    """كود لون ديناميكي / Dynamic color code"""
    def __init__(self, code):
        self._code = code
    def __str__(self):
        return self._code if _is_color_supported() else ''
    def __repr__(self):
        return self.__str__()
    def __add__(self, other):
        return str(self) + str(other)
    def __radd__(self, other):
        return str(other) + str(self)
    def __mul__(self, n):
        return str(self) * n


# Reset / إعادة تعيين
RESET = _ColorCode('\033[0m')
RESET_ALL = RESET

# Text styles / أنماط النص
BOLD = _ColorCode('\033[1m')
DIM = _ColorCode('\033[2m')
ITALIC = _ColorCode('\033[3m')
UNDERLINE = _ColorCode('\033[4m')
BLINK = _ColorCode('\033[5m')
REVERSE = _ColorCode('\033[7m')
HIDDEN = _ColorCode('\033[8m')
STRIKETHROUGH = _ColorCode('\033[9m')

# Foreground colors (standard 16) / ألوان النص الأمامية
BLACK = _ColorCode('\033[30m')
RED = _ColorCode('\033[31m')
GREEN = _ColorCode('\033[32m')
YELLOW = _ColorCode('\033[33m')
BLUE = _ColorCode('\033[34m')
MAGENTA = _ColorCode('\033[35m')
CYAN = _ColorCode('\033[36m')
WHITE = _ColorCode('\033[37m')

# Bright foreground colors / ألوان أمامية فاتحة
BRIGHT_BLACK = _ColorCode('\033[90m')
BRIGHT_RED = _ColorCode('\033[91m')
BRIGHT_GREEN = _ColorCode('\033[92m')
BRIGHT_YELLOW = _ColorCode('\033[93m')
BRIGHT_BLUE = _ColorCode('\033[94m')
BRIGHT_MAGENTA = _ColorCode('\033[95m')
BRIGHT_CYAN = _ColorCode('\033[96m')
BRIGHT_WHITE = _ColorCode('\033[97m')

# Background colors / ألوان الخلفية
BG_BLACK = _ColorCode('\033[40m')
BG_RED = _ColorCode('\033[41m')
BG_GREEN = _ColorCode('\033[42m')
BG_YELLOW = _ColorCode('\033[43m')
BG_BLUE = _ColorCode('\033[44m')
BG_MAGENTA = _ColorCode('\033[45m')
BG_CYAN = _ColorCode('\033[46m')
BG_WHITE = _ColorCode('\033[47m')

# Bright background colors / ألوان خلفية فاتحة
BG_BRIGHT_BLACK = _ColorCode('\033[100m')
BG_BRIGHT_RED = _ColorCode('\033[101m')
BG_BRIGHT_GREEN = _ColorCode('\033[102m')
BG_BRIGHT_YELLOW = _ColorCode('\033[103m')
BG_BRIGHT_BLUE = _ColorCode('\033[104m')
BG_BRIGHT_MAGENTA = _ColorCode('\033[105m')
BG_BRIGHT_CYAN = _ColorCode('\033[106m')
BG_BRIGHT_WHITE = _ColorCode('\033[107m')

# Arabic names for colors / أسماء عربية للألوان
أسود = BLACK
أحمر = RED
أخضر = GREEN
أصفر = YELLOW
أزرق = BLUE
أرجواني = MAGENTA
سماوي = CYAN
أبيض = WHITE
أسود_فاتح = BRIGHT_BLACK
أحمر_فاتح = BRIGHT_RED
أخضر_فاتح = BRIGHT_GREEN
أصفر_فاتح = BRIGHT_YELLOW
أزرق_فاتح = BRIGHT_BLUE
أرجواني_فاتح = BRIGHT_MAGENTA
سماوي_فاتح = BRIGHT_CYAN
أبيض_فاتح = BRIGHT_WHITE

# Additional Arabic color names / أسماء ألوان عربية إضافية
برتقالي = BRIGHT_RED  # orange approximated as bright red
بنفسجي = MAGENTA
نيلي = BLUE
رمادي = BRIGHT_BLACK
فضي = BRIGHT_WHITE
ذهبي = YELLOW
وردي = BRIGHT_MAGENTA
بني = YELLOW
كهرماني = YELLOW

# Arabic style names / أسماء عربية للأنماط
عريض = BOLD
خافت = DIM
مائل = ITALIC
تحته_خط = UNDERLINE
وميض = BLINK
معكوس = REVERSE
مخفي = HIDDEN
إعادة_تعيين = RESET

# ==============================================================
# Terminal Control / تحكم الطرفية
# ==============================================================

CLEAR_SCREEN = '\033[2J' if _COLOR_SUPPORTED else ''
CLEAR_LINE = '\033[2K' if _COLOR_SUPPORTED else ''
CURSOR_HOME = '\033[H' if _COLOR_SUPPORTED else ''
CURSOR_UP = '\033[A' if _COLOR_SUPPORTED else ''
CURSOR_DOWN = '\033[B' if _COLOR_SUPPORTED else ''
CURSOR_FORWARD = '\033[C' if _COLOR_SUPPORTED else ''
CURSOR_BACK = '\033[D' if _COLOR_SUPPORTED else ''
SAVE_CURSOR = '\033[s' if _COLOR_SUPPORTED else ''
RESTORE_CURSOR = '\033[u' if _COLOR_SUPPORTED else ''
HIDE_CURSOR = '\033[?25l' if _COLOR_SUPPORTED else ''
SHOW_CURSOR = '\033[?25h' if _COLOR_SUPPORTED else ''

# New line / سطر جديد
NEWLINE = '\n'
TAB = '\t'


def get_module():
    """إرجاع دوال مكتبة الألوان / Return colors module functions"""
    return {
        # Color constants / ثوابت الألوان
        'RESET': RESET,
        'reset': RESET,
        'إعادة': RESET,

        # Styles / الأنماط
        'BOLD': BOLD,
        'bold': BOLD,
        'عريض': BOLD,
        'DIM': DIM,
        'dim': DIM,
        'ITALIC': ITALIC,
        'italic': ITALIC,
        'مائل': ITALIC,
        'UNDERLINE': UNDERLINE,
        'underline': UNDERLINE,
        'تحته_خط': UNDERLINE,
        'BLINK': BLINK,
        'REVERSE': REVERSE,
        'معكوس': REVERSE,

        # Foreground colors / ألوان النص
        'BLACK': BLACK,
        'black': BLACK,
        'أسود': BLACK,
        'RED': RED,
        'red': RED,
        'أحمر': RED,
        'GREEN': GREEN,
        'green': GREEN,
        'أخضر': GREEN,
        'YELLOW': YELLOW,
        'yellow': YELLOW,
        'أصفر': YELLOW,
        'BLUE': BLUE,
        'blue': BLUE,
        'أزرق': BLUE,
        'MAGENTA': MAGENTA,
        'magenta': MAGENTA,
        'أرجواني': MAGENTA,
        'CYAN': CYAN,
        'cyan': CYAN,
        'سماوي': CYAN,
        'WHITE': WHITE,
        'white': WHITE,
        'أبيض': WHITE,

        # Bright colors / ألوان فاتحة
        'BRIGHT_BLACK': BRIGHT_BLACK,
        'BRIGHT_RED': BRIGHT_RED,
        'BRIGHT_GREEN': BRIGHT_GREEN,
        'BRIGHT_YELLOW': BRIGHT_YELLOW,
        'BRIGHT_BLUE': BRIGHT_BLUE,
        'BRIGHT_CYAN': BRIGHT_CYAN,
        'BRIGHT_MAGENTA': BRIGHT_MAGENTA,
        'BRIGHT_WHITE': BRIGHT_WHITE,

        # Additional Arabic color names / أسماء ألوان عربية إضافية
        'برتقالي': BRIGHT_RED,
        'بنفسجي': MAGENTA,
        'نيلي': BLUE,
        'رمادي': BRIGHT_BLACK,
        'فضي': BRIGHT_WHITE,
        'ذهبي': YELLOW,
        'وردي': BRIGHT_MAGENTA,
        'بني': YELLOW,
        'كهرماني': YELLOW,
        'أسود_فاتح': BRIGHT_BLACK,
        'أحمر_فاتح': BRIGHT_RED,
        'أخضر_فاتح': BRIGHT_GREEN,
        'أصفر_فاتح': BRIGHT_YELLOW,
        'أزرق_فاتح': BRIGHT_BLUE,
        'أرجواني_فاتح': BRIGHT_MAGENTA,
        'سماوي_فاتح': BRIGHT_CYAN,
        'أبيض_فاتح': BRIGHT_WHITE,

        # Background colors / ألوان الخلفية
        'BG_BLACK': BG_BLACK,
        'BG_RED': BG_RED,
        'BG_GREEN': BG_GREEN,
        'BG_YELLOW': BG_YELLOW,
        'BG_BLUE': BG_BLUE,
        'BG_CYAN': BG_CYAN,
        'BG_WHITE': BG_WHITE,
        'BG_MAGENTA': BG_MAGENTA,

        # Terminal control / تحكم الطرفية
        'CLEAR': CLEAR_SCREEN,
        'clear': CLEAR_SCREEN,
        'مسح': CLEAR_SCREEN,
        'CLEAR_LINE': CLEAR_LINE,
        'NEWLINE': NEWLINE,
        'TAB': TAB,

        # Functions / دوال
        'color': _color,
        'لون': _color,
        'rgb': _rgb,
        'bg_rgb': _bg_rgb,
        'style': _style,
        'نمط': _style,
        'colorize': _colorize,
        'ملون': _colorize,
        'strip_color': _strip_color,
        'إزالة_اللون': _strip_color,
        'supports_color': _supports_color_fn,
        'يدعم_الألوان': _supports_color_fn,
        'enable_colors': enable_colors,
        'disable_colors': disable_colors,
        'clear_screen': _clear_screen,
        'امسح_الشاشة': _clear_screen,
        'move_cursor': _move_cursor,
        'حرّك_المؤشر': _move_cursor,

        # Arabic text helpers / مساعدات النص العربي
        'rtl': _rtl,
        'ltr': _ltr,
        'bidi': _bidi,
        'reshape_arabic': _reshape_arabic,
        'تشكيل_عربي': _reshape_arabic,
    }


# ==============================================================
# Helper Functions / دوال مساعدة
# ==============================================================

def _color(text, color_name):
    """تلوين نص بلون محدد / Color text with specified color"""
    colors = {
        'black': BLACK, 'red': RED, 'green': GREEN, 'yellow': YELLOW,
        'blue': BLUE, 'magenta': MAGENTA, 'cyan': CYAN, 'white': WHITE,
        'أسود': BLACK, 'أحمر': RED, 'أخضر': GREEN, 'أصفر': YELLOW,
        'أزرق': BLUE, 'أرجواني': MAGENTA, 'سماوي': CYAN, 'أبيض': WHITE,
    }
    c = colors.get(str(color_name).lower(), RESET)
    return f"{c}{text}{RESET}"


def _rgb(text, r, g, b):
    """تلوين نص بـ RGB / Color text with RGB"""
    if not _COLOR_SUPPORTED:
        return str(text)
    return f"\033[38;2;{int(r)};{int(g)};{int(b)}m{text}{RESET}"


def _bg_rgb(text, r, g, b):
    """لون خلفية بـ RGB / Background color with RGB"""
    if not _COLOR_SUPPORTED:
        return str(text)
    return f"\033[48;2;{int(r)};{int(g)};{int(b)}m{text}{RESET}"


def _style(text, *styles):
    """تطبيق أنماط متعددة على نص / Apply multiple styles to text"""
    if not _COLOR_SUPPORTED:
        return str(text)
    style_map = {
        'bold': BOLD, 'dim': DIM, 'italic': ITALIC, 'underline': UNDERLINE,
        'blink': BLINK, 'reverse': REVERSE, 'hidden': HIDDEN,
        'عريض': BOLD, 'خافت': DIM, 'مائل': ITALIC, 'تحته_خط': UNDERLINE,
        'وميض': BLINK, 'معكوس': REVERSE, 'مخفي': HIDDEN,
    }
    prefix = ''.join(style_map.get(str(s).lower(), '') for s in styles)
    return f"{prefix}{text}{RESET}"


def _colorize(text, color=None, bg=None, bold=False, italic=False, underline=False):
    """تلوين نص مع خيارات متعددة / Colorize text with multiple options"""
    if not _COLOR_SUPPORTED:
        return str(text)

    color_map = {
        'black': BLACK, 'red': RED, 'green': GREEN, 'yellow': YELLOW,
        'blue': BLUE, 'magenta': MAGENTA, 'cyan': CYAN, 'white': WHITE,
    }
    bg_map = {
        'black': BG_BLACK, 'red': BG_RED, 'green': BG_GREEN, 'yellow': BG_YELLOW,
        'blue': BG_BLUE, 'magenta': BG_MAGENTA, 'cyan': BG_CYAN, 'white': BG_WHITE,
    }

    prefix = ''
    if bold:
        prefix += BOLD
    if italic:
        prefix += ITALIC
    if underline:
        prefix += UNDERLINE
    if color and str(color).lower() in color_map:
        prefix += color_map[str(color).lower()]
    if bg and str(bg).lower() in bg_map:
        prefix += bg_map[str(bg).lower()]

    return f"{prefix}{text}{RESET}"


def _strip_color(text):
    """إزالة جميع أكواد ANSI من نص / Strip all ANSI codes from text"""
    import re
    ansi_escape = re.compile(r'\033\[[0-9;]*m')
    return ansi_escape.sub('', str(text))


def _supports_color_fn():
    """تحقق من دعم الألوان / Check color support"""
    return _COLOR_SUPPORTED


def _clear_screen():
    """مسح الشاشة / Clear screen"""
    if _COLOR_SUPPORTED:
        print(CLEAR_SCREEN + CURSOR_HOME, end='')
    return None


def _move_cursor(row, col):
    """تحريك المؤشر لموضع / Move cursor to position"""
    if _COLOR_SUPPORTED:
        print(f"\033[{int(row)};{int(col)}H", end='')
    return None


# ==============================================================
# Arabic Text Helpers / مساعدات النص العربي
# ==============================================================

def _rtl(text):
    """وضع علامة RTL للنص / Add RTL mark for text"""
    # RLM (Right-to-Left Mark)
    return '\u200F' + str(text)


def _ltr(text):
    """وضع علامة LTR للنص / Add LTR mark for text"""
    # LRM (Left-to-Right Mark)
    return '\u200E' + str(text)


def _bidi(text):
    """تطبيق خوارزمية BiDi للنص / Apply BiDi algorithm to text"""
    try:
        # Try to use python-bidi if available
        try:
            from bidi.algorithm import get_display
            return get_display(str(text))
        except ImportError:
            # Fallback: just return the text with RTL mark
            return '\u202B' + str(text) + '\u202C'
    except Exception:
        return str(text)


def _reshape_arabic(text):
    """تشكيل النص العربي للعرض / Reshape Arabic text for display"""
    try:
        # Try to use arabic-reshaper if available
        try:
            import arabic_reshaper
            return arabic_reshaper.reshape(str(text))
        except ImportError:
            # Fallback: return text as-is
            return str(text)
    except Exception:
        return str(text)
