"""
Opal Language - Token Definitions
تعريفات الرموز في لغة أوبال

This file defines all token types and keyword mappings for both
Arabic and English language support.
هذا الملف يعرّف جميع أنواع الرموز وكلمات اللغة المفتاحية بالعربية والإنجليزية
"""

from enum import Enum, auto


class TokenType(Enum):
    """جميع أنواع الرموز في لغة أوبال / All token types in Opal"""

    # Literals / القيم الحرفية
    NUMBER = auto()        # 123, 3.14
    STRING = auto()        # "hello", 'world'
    IDENTIFIER = auto()    # variable names / أسماء المتغيرات
    TRUE = auto()          # true / صحيح
    FALSE = auto()         # false / خطأ
    NULL = auto()          # null / فراغ

    # Keywords - English / الكلمات المفتاحية - إنجليزي
    VAR = auto()           # var
    CONST = auto()         # const
    IF = auto()            # if
    ELSE = auto()          # else
    ELIF = auto()          # elif
    WHILE = auto()         # while
    FOR = auto()           # for
    IN = auto()            # in
    FUNCTION = auto()      # function
    RETURN = auto()        # return
    BREAK = auto()         # break
    CONTINUE = auto()      # continue
    IMPORT = auto()        # import
    FROM = auto()          # from
    ECHO = auto()          # echo (print)
    AND = auto()           # and / و
    OR = auto()            # or / أو
    NOT = auto()           # not / ليس

    # Operators / العمليات
    PLUS = auto()          # +
    MINUS = auto()         # -
    STAR = auto()          # *
    SLASH = auto()         # /
    DIVIDE = auto()        # ÷ (Arabic-friendly division)
    POWER = auto()         # ^
    MODULO = auto()        # %

    ASSIGN = auto()        # =
    EQ = auto()            # ==
    NEQ = auto()           # !=
    LT = auto()            # <
    GT = auto()            # >
    LTE = auto()           # <=
    GTE = auto()           # >=

    # Delimiters / الفواصل
    LPAREN = auto()        # (
    RPAREN = auto()        # )
    LBRACE = auto()        # {
    RBRACE = auto()        # }
    LBRACKET = auto()      # [
    RBRACKET = auto()      # ]
    COMMA = auto()         # ,
    DOT = auto()           # .
    DOTDOT = auto()        # ..
    COLON = auto()         # :
    SEMICOLON = auto()     # ;
    ARROW = auto()         # ->

    # Special / خاصة
    NEWLINE = auto()
    EOF = auto()


# ==============================================================
# Keyword Mappings / جدول الكلمات المفتاحية
# Supports both English and Arabic keywords
# يدعم الكلمات المفتاحية بالإنجليزية والعربية
# ==============================================================

KEYWORDS = {
    # English keywords / كلمات إنجليزية
    'var': TokenType.VAR,
    'const': TokenType.CONST,
    'if': TokenType.IF,
    'else': TokenType.ELSE,
    'elif': TokenType.ELIF,
    'while': TokenType.WHILE,
    'for': TokenType.FOR,
    'in': TokenType.IN,
    'function': TokenType.FUNCTION,
    'return': TokenType.RETURN,
    'break': TokenType.BREAK,
    'continue': TokenType.CONTINUE,
    'import': TokenType.IMPORT,
    'from': TokenType.FROM,
    'echo': TokenType.ECHO,
    'and': TokenType.AND,
    'or': TokenType.OR,
    'not': TokenType.NOT,
    'true': TokenType.TRUE,
    'false': TokenType.FALSE,
    'null': TokenType.NULL,
    'fun': TokenType.FUNCTION,  # shortcut / اختصار

    # Arabic keywords / كلمات عربية
    'متغير': TokenType.VAR,
    'ثابت': TokenType.CONST,
    'اذا': TokenType.IF,
    'إذا': TokenType.IF,
    'والا': TokenType.ELSE,
    'وإلا': TokenType.ELSE,
    'وإذا': TokenType.ELIF,
    'واذا': TokenType.ELIF,
    'بينما': TokenType.WHILE,
    'لكل': TokenType.FOR,
    'في': TokenType.IN,
    'دالة': TokenType.FUNCTION,
    'داله': TokenType.FUNCTION,
    'ارجع': TokenType.RETURN,
    'أرجع': TokenType.RETURN,
    'توقف': TokenType.BREAK,
    'اكمل': TokenType.CONTINUE,
    'أكمل': TokenType.CONTINUE,
    'استورد': TokenType.IMPORT,
    'من': TokenType.FROM,
    'اطبع': TokenType.ECHO,
    'و': TokenType.AND,
    'أو': TokenType.OR,
    'او': TokenType.OR,
    'ليس': TokenType.NOT,
    'صحيح': TokenType.TRUE,
    'خطأ': TokenType.FALSE,
    'خطا': TokenType.FALSE,
    'فراغ': TokenType.NULL,
    'عدم': TokenType.NULL,
}


class Token:
    """رمز واحد في الكود المصدري / A single token in the source code"""

    def __init__(self, type, value, line, column):
        self.type = type      # TokenType
        self.value = value    # The actual text
        self.line = line      # Line number (1-based)
        self.column = column  # Column number (1-based)

    def __repr__(self):
        return f"Token({self.type.name}, {self.value!r}, line={self.line})"

    def __str__(self):
        return f"{self.type.name}('{self.value}')"


# ==============================================================
# Helper: Check if a character is a valid identifier character
# دالة مساعدة: التحقق من أن الحرف صالح لأسماء المتغيرات
# ==============================================================

def is_arabic_char(ch):
    """Check if character is Arabic / التحقق من أن الحرف عربي"""
    if not ch:
        return False
    code = ord(ch)
    # Arabic main range + Arabic Supplement + Arabic Presentation Forms
    return (0x0600 <= code <= 0x06FF) or \
           (0x0750 <= code <= 0x077F) or \
           (0xFB50 <= code <= 0xFDFF) or \
           (0xFE70 <= code <= 0xFEFF)


def is_arabic_punctuation(ch):
    """Check if character is Arabic punctuation / تحقق من أن الحرف علامة ترقيم عربية"""
    if not ch:
        return False
    code = ord(ch)
    # Arabic punctuation marks to exclude from identifiers
    # علامات الترقيم العربية المستثناة من أسماء المتغيرات
    arabic_punct = {
        0x060C,  # ، Arabic comma / الفاصلة العربية
        0x060D,  # Arabic date separator
        0x061B,  # ؛ Arabic semicolon / الفاصلة المنقوطة
        0x061C,  # Arabic letter mark
        0x061E,  # Arabic triple dot punctuation mark
        0x061F,  # ؟ Arabic question mark / علامة الاستفهام
        0x066A,  # ٪ Arabic percent sign
        0x066B,  # Arabic decimal separator
        0x066C,  # Arabic thousands separator
        0x066D,  # Arabic five pointed star
        0x066E,  # Arabic letter dotless beh
        0x066F,  # Arabic letter dotless qaf
        0x0640,  # ـ Arabic tatweel (letter extension - exclude for simplicity)
        0x06D4,  # ۔ Arabic full stop
    }
    return code in arabic_punct


def is_identifier_start(ch):
    """Check if character can start an identifier / يمكن أن يبدأ اسم متغير"""
    return (ch.isalpha() or ch == '_' or is_arabic_char(ch)) and not is_arabic_punctuation(ch)


def is_identifier_char(ch):
    """Check if character can be in an identifier / يمكن أن يكون في اسم متغير"""
    return (ch.isalnum() or ch == '_' or is_arabic_char(ch)) and not is_arabic_punctuation(ch)


def is_digit(ch):
    """Check if character is a digit / التحقق من أن الحرف رقم"""
    return ch.isdigit()
