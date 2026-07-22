"""
Opal Language - Logo / شعار اللغة

ASCII art logo for Opal Language.
شعار فني ASCII للغة أوبال

Usage / الاستخدام:
    from opal.logo import print_logo, get_logo, print_small_logo
    print_logo()  # Print big logo / طباعة الشعار الكبير
"""

# Big logo / الشعار الكبير
LOGO_BIG = r"""
   ___  _ ___ _    _    
  / _ \| | __| |  | |   
 | (_) | | _|| |__| |__ 
  \___/|_|___|____|____|
                        
  لغة أوبال - Opal Language
"""

# Medium logo / شعار متوسط  
LOGO_MEDIUM = r"""
  ___  _ ___ _    _    
 / _ \| | __| |  | |   
| (_) | | _|| |__| |__ 
 \___/|_|___|____|____|
"""

# Small logo / شعار صغير
LOGO_SMALL = r"""
  ___  _ ___ 
 / _ \| | __|
| (_) | | _|
 \___/|_|___|
"""

# Gem-style logo (opal is a gem) / شعار على شكل جوهرة
LOGO_GEM = r"""
       .-*---*-.
      / .---. \
     | /     \ |
     | |     | |
     | \     / |
      \ *---* /
       -*--*-*
    OPAL LANGUAGE
"""

# Diamond/gem logo / شعار جوهرة
LOGO_DIAMOND = r"""
      /\
     /  \
    /____\
    \    /
     \  /
      \/
   OPAL LANG
"""

# Boxed logo / شعار في صندوق
LOGO_BOXED = r"""
╔═══════════════════════════╗
║                           ║
║   ___  _ ___ _    _       ║
║  / _ \| | __| |  | |      ║
║ | (_) | | _|| |__| |__    ║
║  \___/|_|___|____|____|   ║
║                           ║
║     لغة أوبال             ║
║     Opal Language         ║
║                           ║
╚═══════════════════════════╝
"""

# Arabic logo / شعار عربي
LOGO_ARABIC = r"""
   ╔═══════════════════════╗
   ║                       ║
   ║    ◆  أوبال  ◆       ║
   ║                       ║
   ║   لغة البرمجة         ║
   ║   Opal Language       ║
   ║                       ║
   ╚═══════════════════════╝
"""

# Animated logo frames / إطارات الشعار المتحرك
LOGO_FRAMES = [
    r"   ◆          ",
    r"   ◇◆         ",
    r"   ◆◇◆        ",
    r"  ◆◇◆◇◆       ",
    r" ◆◇◆◇◆◇◆      ",
    r"◆◇◆ OPAL ◇◆◇◆",
]


def get_logo(style='medium'):
    """الحصول على الشعار / Get logo"""
    logos = {
        'big': LOGO_BIG,
        'medium': LOGO_MEDIUM,
        'small': LOGO_SMALL,
        'gem': LOGO_GEM,
        'diamond': LOGO_DIAMOND,
        'boxed': LOGO_BOXED,
        'arabic': LOGO_ARABIC,
    }
    return logos.get(style, LOGO_MEDIUM)


def print_logo(style='medium', with_colors=True):
    """طباعة الشعار / Print logo"""
    logo = get_logo(style)
    
    if with_colors:
        # Try to use colors / محاولة استخدام الألوان
        try:
            from .stdlib.colors_lib import CYAN, BOLD, RESET, BLUE, MAGENTA
            print(f"{BOLD}{CYAN}{logo}{RESET}")
        except:
            print(logo)
    else:
        print(logo)


def print_small_logo():
    """طباعة الشعار الصغير / Print small logo"""
    print_logo('small')


def print_animated_logo(frames=6, delay=0.2):
    """طباعة شعار متحرك / Print animated logo"""
    import time
    import sys
    
    for i in range(frames):
        # Clear line / مسح السطر
        sys.stdout.write('\r\033[K')
        frame = LOGO_FRAMES[i % len(LOGO_FRAMES)]
        
        try:
            from .stdlib.colors_lib import CYAN, BOLD, RESET
            sys.stdout.write(f'{BOLD}{CYAN}{frame}{RESET}')
        except:
            sys.stdout.write(frame)
            
        sys.stdout.flush()
        time.sleep(delay)
    
    sys.stdout.write('\n')


def get_banner(text="OPAL", width=40):
    """إنشاء لافتة / Create banner"""
    padding = (width - len(text) - 4) // 2
    if padding < 0:
        padding = 0
    line = '═' * width
    spaces = ' ' * padding
    return f"""
╔{line}╗
║{spaces}  ◆ {text} ◆  {spaces}║
╚{line}╝
"""
