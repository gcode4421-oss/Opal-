"""
Opal Standard Library - TUI (Terminal User Interface)
مكتبة واجهات الطرفية - ارسم واجهات حقيقية في الطرفية

Draw real interfaces in the terminal - boxes, menus, progress bars, etc.
ارسم واجهات حقيقية في الطرفية - صناديق، قوائم، أشرطة تقدم، إلخ

Features / المميزات:
- Boxes and borders / صناديق وحدود
- Menus / قوائم
- Progress bars / أشرطة تقدم
- Tables / جداول
- ASCII art / فن ASCII
- Screen control / تحكم بالشاشة
- Input forms / نماذج إدخال
- Animations / حركات

Works on Termux, Linux, macOS, Windows
يعمل على Termux، Linux، macOS، Windows
"""

import os
import sys
import shutil
import time


# Get terminal size / الحصول على حجم الطرفية
def _get_terminal_size():
    """الحصول على حجم الطرفية / Get terminal size"""
    try:
        size = shutil.get_terminal_size()
        return size.columns, size.lines
    except:
        return 80, 24


# Box drawing characters / رموز الرسم
class BoxChars:
    """رموز رسم الصناديق / Box drawing characters"""
    # Single line / خط واحد
    TOP_LEFT = '┌'
    TOP_RIGHT = '┐'
    BOTTOM_LEFT = '└'
    BOTTOM_RIGHT = '┘'
    HORIZONTAL = '─'
    VERTICAL = '│'
    CROSS = '┼'
    T_DOWN = '┬'
    T_UP = '┴'
    T_LEFT = '├'
    T_RIGHT = '┤'

    # Double line / خط مزدوج
    D_TOP_LEFT = '╔'
    D_TOP_RIGHT = '╗'
    D_BOTTOM_LEFT = '╚'
    D_BOTTOM_RIGHT = '╝'
    D_HORIZONTAL = '═'
    D_VERTICAL = '║'

    # Rounded / مدور
    R_TOP_LEFT = '╭'
    R_TOP_RIGHT = '╮'
    R_BOTTOM_LEFT = '╰'
    R_BOTTOM_RIGHT = '╯'

    # Filled / ممتلئ
    FULL_BLOCK = '█'
    LIGHT_SHADE = '░'
    MEDIUM_SHADE = '▒'
    DARK_SHADE = '▓'

    # Progress / تقدم
    PROGRESS_FULL = '█'
    PROGRESS_EMPTY = '░'


class OpalScreen:
    """شاشة طرفية / Terminal screen"""

    def __init__(self, width=None, height=None):
        if width is None or height is None:
            w, h = _get_terminal_size()
            self.width = width or w
            self.height = height or h
        else:
            self.width = width
            self.height = height
        # Initialize buffer / تهيئة المخزن
        self.buffer = [[' '] * self.width for _ in range(self.height)]
        self.colors = [[None] * self.width for _ in range(self.height)]

    def clear(self):
        """مسح الشاشة / Clear screen"""
        self.buffer = [[' '] * self.width for _ in range(self.height)]
        self.colors = [[None] * self.width for _ in range(self.height)]

    def set_pixel(self, x, y, char, color=None):
        """تعيين بكسل / Set pixel at position"""
        if 0 <= y < self.height and 0 <= x < self.width:
            self.buffer[y][x] = char[0] if char else ' '
            self.colors[y][x] = color

    def draw_text(self, x, y, text, color=None):
        """رسم نص / Draw text"""
        for i, ch in enumerate(text):
            self.set_pixel(x + i, y, ch, color)

    def draw_box(self, x, y, w, h, style='single', color=None):
        """رسم صندوق / Draw box"""
        if style == 'double':
            tl, tr, bl, br = BoxChars.D_TOP_LEFT, BoxChars.D_TOP_RIGHT, BoxChars.D_BOTTOM_LEFT, BoxChars.D_BOTTOM_RIGHT
            h_char, v_char = BoxChars.D_HORIZONTAL, BoxChars.D_VERTICAL
        elif style == 'rounded':
            tl, tr, bl, br = BoxChars.R_TOP_LEFT, BoxChars.R_TOP_RIGHT, BoxChars.R_BOTTOM_LEFT, BoxChars.R_BOTTOM_RIGHT
            h_char, v_char = BoxChars.HORIZONTAL, BoxChars.VERTICAL
        else:  # single
            tl, tr, bl, br = BoxChars.TOP_LEFT, BoxChars.TOP_RIGHT, BoxChars.BOTTOM_LEFT, BoxChars.BOTTOM_RIGHT
            h_char, v_char = BoxChars.HORIZONTAL, BoxChars.VERTICAL

        # Top / الأعلى
        self.set_pixel(x, y, tl, color)
        for i in range(1, w - 1):
            self.set_pixel(x + i, y, h_char, color)
        self.set_pixel(x + w - 1, y, tr, color)

        # Sides / الجوانب
        for i in range(1, h - 1):
            self.set_pixel(x, y + i, v_char, color)
            self.set_pixel(x + w - 1, y + i, v_char, color)

        # Bottom / الأسفل
        self.set_pixel(x, y + h - 1, bl, color)
        for i in range(1, w - 1):
            self.set_pixel(x + i, y + h - 1, h_char, color)
        self.set_pixel(x + w - 1, y + h - 1, br, color)

    def draw_hline(self, x, y, length, char='─', color=None):
        """رسم خط أفقي / Draw horizontal line"""
        for i in range(length):
            self.set_pixel(x + i, y, char, color)

    def draw_vline(self, x, y, length, char='│', color=None):
        """رسم خط عمودي / Draw vertical line"""
        for i in range(length):
            self.set_pixel(x, y + i, char, color)

    def fill_rect(self, x, y, w, h, char=' ', color=None):
        """ملء مستطيل / Fill rectangle"""
        for j in range(h):
            for i in range(w):
                self.set_pixel(x + i, y + j, char, color)

    def render(self):
        """عرض الشاشة / Render the screen"""
        # Clear terminal / مسح الطرفية
        print('\033[2J\033[H', end='')

        for y in range(self.height):
            line = []
            current_color = None
            for x in range(self.width):
                color = self.colors[y][x]
                if color != current_color:
                    if color:
                        line.append(str(color))
                    else:
                        line.append('\033[0m')
                    current_color = color
                line.append(self.buffer[y][x])
            print(''.join(line))

        # Reset colors / إعادة تعيين الألوان
        print('\033[0m', end='')


def get_module():
    """إرجاع دوال مكتبة TUI / Return TUI module functions"""
    return {
        # Screen functions / دوال الشاشة
        'screen': _create_screen,
        'شاشة': _create_screen,
        'clear': _clear_screen,
        'امسح': _clear_screen,
        'terminal_size': _terminal_size,
        'حجم_الطرفية': _terminal_size,

        # Box drawing / رسم الصناديق
        'box': _draw_box,
        'صندوق': _draw_box,
        'hline': _draw_hline,
        'vline': _draw_vline,
        'rect': _draw_rect,

        # Text / النصوص
        'print_at': _print_at,
        'اطبع_في': _print_at,
        'center_text': _center_text,
        'نص_منسق': _center_text,

        # Progress / التقدم
        'progress_bar': _progress_bar,
        'شريط_تقدم': _progress_bar,

        # Menus / القوائم
        'menu': _show_menu,
        'قائمة': _show_menu,

        # Tables / الجداول
        'table': _draw_table,
        'جدول': _draw_table,

        # Input / الإدخال
        'input_box': _input_box,
        'مربع_إدخال': _input_box,

        # Animation / الحركات
        'loading': _loading,
        'تحميل': _loading,
        'spinner': _spinner,

        # ASCII art / فن ASCII
        'banner': _banner,
        'لافتة': _banner,
        'art': _ascii_art,

        # Notification / الإشعارات
        'alert': _alert,
        'تنبيه': _alert,
        'confirm': _confirm,
        'تأكيد': _confirm,

        # Cursor / المؤشر
        'move_cursor': _move_cursor,
        'save_cursor': _save_cursor,
        'restore_cursor': _restore_cursor,
        'hide_cursor': _hide_cursor,
        'show_cursor': _show_cursor,

        # Constants / ثوابت
        'BOX_CHARS': {
            'top_left': BoxChars.TOP_LEFT,
            'top_right': BoxChars.TOP_RIGHT,
            'bottom_left': BoxChars.BOTTOM_LEFT,
            'bottom_right': BoxChars.BOTTOM_RIGHT,
            'horizontal': BoxChars.HORIZONTAL,
            'vertical': BoxChars.VERTICAL,
            'cross': BoxChars.CROSS,
            'full_block': BoxChars.FULL_BLOCK,
            'light_shade': BoxChars.LIGHT_SHADE,
            'medium_shade': BoxChars.MEDIUM_SHADE,
            'dark_shade': BoxChars.DARK_SHADE,
        },
    }


def _create_screen(width=None, height=None):
    """إنشاء شاشة / Create screen"""
    return OpalScreen(width, height)


def _clear_screen():
    """مسح الشاشة / Clear screen"""
    print('\033[2J\033[H', end='')


def _terminal_size():
    """حجم الطرفية / Terminal size"""
    w, h = _get_terminal_size()
    return {'width': w, 'height': h, 'عرض': w, 'ارتفاع': h}


def _draw_box(x, y, w, h, style='single'):
    """رسم صندوق في الطرفية / Draw box in terminal"""
    if style == 'double':
        tl, tr, bl, br = BoxChars.D_TOP_LEFT, BoxChars.D_TOP_RIGHT, BoxChars.D_BOTTOM_LEFT, BoxChars.D_BOTTOM_RIGHT
        hc, vc = BoxChars.D_HORIZONTAL, BoxChars.D_VERTICAL
    elif style == 'rounded':
        tl, tr, bl, br = BoxChars.R_TOP_LEFT, BoxChars.R_TOP_RIGHT, BoxChars.R_BOTTOM_LEFT, BoxChars.R_BOTTOM_RIGHT
        hc, vc = BoxChars.HORIZONTAL, BoxChars.VERTICAL
    else:
        tl, tr, bl, br = BoxChars.TOP_LEFT, BoxChars.TOP_RIGHT, BoxChars.BOTTOM_LEFT, BoxChars.BOTTOM_RIGHT
        hc, vc = BoxChars.HORIZONTAL, BoxChars.VERTICAL

    # Move cursor and draw / تحريك المؤشر والرسم
    # Top / الأعلى
    print(f'\033[{y};{x}H{tl}{hc * (w - 2)}{tr}', end='')
    # Sides / الجوانب
    for i in range(1, h - 1):
        print(f'\033[{y+i};{x}H{vc}', end='')
        print(f'\033[{y+i};{x+w-1}H{vc}', end='')
    # Bottom / الأسفل
    print(f'\033[{y+h-1};{x}H{bl}{hc * (w - 2)}{br}', end='')
    print(f'\033[{y+h-1};{x+w-1}H', end='')
    sys.stdout.flush()


def _draw_hline(x, y, length, char='─'):
    """رسم خط أفقي / Draw horizontal line"""
    print(f'\033[{y};{x}H{char * length}', end='')
    sys.stdout.flush()


def _draw_vline(x, y, length, char='│'):
    """رسم خط عمودي / Draw vertical line"""
    for i in range(length):
        print(f'\033[{y+i};{x}H{char}', end='')
    sys.stdout.flush()


def _draw_rect(x, y, w, h, char='█'):
    """رسم مستطيل ممتلئ / Draw filled rectangle"""
    for j in range(h):
        print(f'\033[{y+j};{x}H{char * w}', end='')
    sys.stdout.flush()


def _print_at(x, y, text):
    """طباعة نص في موضع / Print text at position"""
    print(f'\033[{y};{x}H{text}', end='')
    sys.stdout.flush()


def _center_text(y, text):
    """توسيط نص / Center text"""
    w, _ = _get_terminal_size()
    x = (w - len(text)) // 2
    print(f'\033[{y};{x}H{text}', end='')
    sys.stdout.flush()


def _progress_bar(x, y, width, percent, filled='█', empty='░'):
    """رسم شريط تقدم / Draw progress bar"""
    filled_len = int(width * percent / 100)
    bar = filled * filled_len + empty * (width - filled_len)
    print(f'\033[{y};{x}H[{bar}] {percent}%', end='')
    sys.stdout.flush()


def _show_menu(title, items, x=2, y=2):
    """عرض قائمة / Show menu"""
    _clear_screen()
    width = max(len(title), max(len(str(i)) for i in items)) + 4

    _print_at(x, y, '╔' + '═' * width + '╗')
    _print_at(x, y + 1, f'║ {title}' + ' ' * (width - len(title) - 1) + '║')
    _print_at(x, y + 2, '╠' + '═' * width + '╣')

    for i, item in enumerate(items):
        _print_at(x, y + 3 + i, f'║ {i+1}. {item}' + ' ' * (width - len(str(item)) - 4) + '║')

    _print_at(x, y + 3 + len(items), '╚' + '═' * width + '╝')
    sys.stdout.flush()

    try:
        choice = input(f'\n\033[{y+4+len(items)};{x}Hاختر رقم: / Choose number: ')
        return int(choice) - 1
    except (ValueError, EOFError):
        return -1


def _draw_table(headers, rows, x=2, y=2):
    """رسم جدول / Draw table"""
    _clear_screen()

    # Calculate column widths / حساب عرض الأعمدة
    col_widths = [len(str(h)) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            if i < len(col_widths):
                col_widths[i] = max(col_widths[i], len(str(cell)))

    # Top border / الحد العلوي
    top = '┌' + '┬'.join('─' * (w + 2) for w in col_widths) + '┐'
    _print_at(x, y, top)

    # Headers / العناوين
    header_line = '│'
    for i, h in enumerate(headers):
        header_line += f' {str(h):<{col_widths[i]}} │'
    _print_at(x, y + 1, header_line)

    # Header separator / فاصل العناوين
    sep = '├' + '┼'.join('─' * (w + 2) for w in col_widths) + '┤'
    _print_at(x, y + 2, sep)

    # Rows / الصفوف
    for i, row in enumerate(rows):
        row_line = '│'
        for j, cell in enumerate(row):
            if j < len(col_widths):
                row_line += f' {str(cell):<{col_widths[j]}} │'
        _print_at(x, y + 3 + i, row_line)

    # Bottom border / الحد السفلي
    bottom = '└' + '┴'.join('─' * (w + 2) for w in col_widths) + '┘'
    _print_at(x, y + 3 + len(rows), bottom)

    # Move cursor below table / تحريك المؤشر أسفل الجدول
    print(f'\033[{y + 4 + len(rows)};1H', end='')
    sys.stdout.flush()


def _input_box(x, y, width, label=''):
    """مربع إدخال / Input box"""
    _draw_box(x, y, width, 3)
    _print_at(x + 1, y + 1, label)
    sys.stdout.flush()
    try:
        return input(f'\033[{y+1};{x+len(label)+2}H')
    except EOFError:
        return ''


def _loading(message, duration=2):
    """عرض تحميل / Show loading"""
    spinners = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        print(f'\r{spinners[i % len(spinners)]} {message}...', end='')
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    print(f'\r✓ {message}')


def _spinner(message, callback):
    """عرض spinner أثناء تنفيذ callback / Show spinner during callback"""
    spinners = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    import threading

    result = [None]
    done = [False]

    def run():
        try:
            result[0] = callback()
        finally:
            done[0] = True

    thread = threading.Thread(target=run)
    thread.start()

    i = 0
    while not done[0]:
        print(f'\r{spinners[i % len(spinners)]} {message}...', end='')
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1

    thread.join()
    print(f'\r✓ {message}')
    return result[0]


def _banner(text, style='big'):
    """عرض لافتة كبيرة / Display big banner"""
    if style == 'simple':
        w, _ = _get_terminal_size()
        line = '═' * (len(text) + 6)
        print(f'\n{line}')
        print(f'║ {text} ║')
        print(f'{line}\n')
    else:
        # ASCII art style / نمط فن ASCII
        w, _ = _get_terminal_size()
        padding = (w - len(text) - 4) // 2
        print('\n' + ' ' * padding + '╔' + '═' * (len(text) + 2) + '╗')
        print(' ' * padding + f'║ {text} ║')
        print(' ' * padding + '╚' + '═' * (len(text) + 2) + '╝\n')


def _ascii_art(text):
    """فن ASCII / ASCII art"""
    fonts = {
        'A': ['  ▄▀█  ', ' █▀▀█  ', ' █  █  '],
        'B': ['  █▀▄  ', '  █▀▄  ', '  ▀▀   '],
        'O': ['  ▄▀▄  ', '  █ █  ', '  ▀▄▀  '],
    }
    for ch in text.upper():
        if ch in fonts:
            for line in fonts[ch]:
                print(line)
        else:
            print(f'  {ch}  ')


def _alert(message, title='تنبيه / Alert'):
    """عرض تنبيه / Show alert"""
    w = max(len(message), len(title)) + 4
    _draw_box(2, 2, w, 5)
    _print_at(4, 3, title)
    _print_at(4, 4, message)
    sys.stdout.flush()
    try:
        input(f'\n\033[7;2Hاضغط Enter للمتابعة... / Press Enter to continue...')
    except EOFError:
        pass


def _confirm(message):
    """تأكيد / Confirm dialog"""
    try:
        response = input(f'{message} (y/n): ')
        return response.lower() in ('y', 'yes', 'نعم')
    except EOFError:
        return False


def _move_cursor(x, y):
    """تحريك المؤشر / Move cursor"""
    print(f'\033[{y};{x}H', end='')
    sys.stdout.flush()


def _save_cursor():
    """حفظ المؤشر / Save cursor"""
    print('\033[s', end='')
    sys.stdout.flush()


def _restore_cursor():
    """استعادة المؤشر / Restore cursor"""
    print('\033[u', end='')
    sys.stdout.flush()


def _hide_cursor():
    """إخفاء المؤشر / Hide cursor"""
    print('\033[?25l', end='')
    sys.stdout.flush()


def _show_cursor():
    """إظهار المؤشر / Show cursor"""
    print('\033[?25h', end='')
    sys.stdout.flush()
