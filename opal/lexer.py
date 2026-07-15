"""
Opal Language - Lexer / المحلل اللغوي

Converts source code text into a stream of tokens.
يحول الكود المصدري إلى سلسلة من الرموز

Supports:
- Arabic and English identifiers and keywords
- Numbers (integers and floats)
- Strings (single and double quotes)
- Comments (// and #)
- All operators and delimiters
"""

from .tokens import (
    TokenType, Token, KEYWORDS,
    is_identifier_start, is_identifier_char, is_digit, is_arabic_char
)


class LexError(Exception):
    """خطأ في التحليل اللغوي / Lexical error"""

    def __init__(self, message, line, column):
        super().__init__(f"خطأ لغوي (LexError) عند السطر {line}, العمود {column}: {message}")
        self.line = line
        self.column = column


class Lexer:
    """المحلل اللغوي - يحول النص إلى رموز / Tokenizer"""

    def __init__(self, source):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens = []

    def error(self, message):
        raise LexError(message, self.line, self.column)

    def peek(self, offset=0):
        """ينظر للحرف الحالي أو القادم بدون تحرك / Peek at current or next char"""
        idx = self.pos + offset
        if idx >= len(self.source):
            return '\0'
        return self.source[idx]

    def advance(self):
        """يتقدم حرف واحد ويعيده / Advance one character"""
        ch = self.peek()
        self.pos += 1
        if ch == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return ch

    def match(self, expected):
        """يتحقق من الحرف التالي ويتقدم إذا طابق / Match next char"""
        if self.peek() == expected:
            self.advance()
            return True
        return False

    def tokenize(self):
        """يحول كل الكود إلى رموز / Tokenize entire source"""
        while self.pos < len(self.source):
            ch = self.peek()

            # Skip whitespace / تخطي المسافات
            if ch in ' \t\r':
                self.advance()
                continue

            # Arabic comma → treat as regular comma / الفاصلة العربية كفاصلة عادية
            if ch == '\u060c':
                self.advance()
                self.add_token(TokenType.COMMA, ',')
                continue

            # Arabic semicolon → treat as regular semicolon / الفاصلة المنقوطة العربية
            if ch == '\u061b':
                self.advance()
                self.add_token(TokenType.SEMICOLON, ';')
                continue

            # Arabic question mark → skip / علامة الاستفهام العربية
            if ch in '\u061f\u061b':
                self.advance()
                continue

            # Skip newlines (but track them) / تخطي الأسطر الجديدة
            if ch == '\n':
                self.add_token(TokenType.NEWLINE, '\\n')
                self.advance()
                continue

            # Comments / التعليقات
            if ch == '/' and self.peek(1) == '/':
                self.skip_comment()
                continue
            if ch == '#':
                self.skip_comment()
                continue
            # Block comments /* ... */ / تعليقات متعددة الأسطر
            if ch == '/' and self.peek(1) == '*':
                self.skip_block_comment()
                continue

            # Numbers / الأرقام
            if is_digit(ch):
                self.read_number()
                continue

            # Strings / النصوص
            if ch == '"' or ch == "'":
                self.read_string(ch)
                continue

            # Identifiers and keywords / المعرفات والكلمات المفتاحية
            if is_identifier_start(ch):
                self.read_identifier()
                continue

            # Operators and delimiters / العمليات والفواصل
            self.read_operator()

        self.add_token(TokenType.EOF, None)
        return self.tokens

    def add_token(self, type, value):
        """يضيف رمز جديد / Add a token"""
        self.tokens.append(Token(type, value, self.line, self.column))

    def skip_comment(self):
        """تخطي التعليق حتى نهاية السطر / Skip comment to end of line"""
        while self.peek() != '\n' and self.peek() != '\0':
            self.advance()

    def skip_block_comment(self):
        """تخطي تعليق متعدد الأسطر / Skip block comment /* ... */"""
        self.advance()  # consume /
        self.advance()  # consume *
        while True:
            if self.peek() == '\0':
                break
            if self.peek() == '*' and self.peek(1) == '/':
                self.advance()  # consume *
                self.advance()  # consume /
                break
            self.advance()

    def read_number(self):
        """يقرأ رقم (صحيح أو عشري) / Read a number (int or float)"""
        start_col = self.column
        num_str = ''

        while is_digit(self.peek()):
            num_str += self.advance()

        # Handle decimal point / النقطة العشرية
        if self.peek() == '.' and is_digit(self.peek(1)):
            num_str += self.advance()  # consume '.'
            while is_digit(self.peek()):
                num_str += self.advance()

        # Convert to int or float
        if '.' in num_str:
            value = float(num_str)
        else:
            value = int(num_str)

        self.add_token(TokenType.NUMBER, value)

    def read_string(self, quote):
        """يقرأ نص بين علامتي اقتباس / Read a string literal"""
        start_line = self.line
        start_col = self.column
        self.advance()  # consume opening quote
        string_value = ''

        while self.peek() != quote and self.peek() != '\0':
            if self.peek() == '\n':
                self.error("النص غير مغلق - String not closed")

            # Escape sequences / تسلسلات الهروب
            if self.peek() == '\\':
                self.advance()
                escape_char = self.advance()
                if escape_char == 'n':
                    string_value += '\n'
                elif escape_char == 't':
                    string_value += '\t'
                elif escape_char == 'r':
                    string_value += '\r'
                elif escape_char == '\\':
                    string_value += '\\'
                elif escape_char == quote:
                    string_value += quote
                elif escape_char == '0':
                    string_value += '\0'
                else:
                    string_value += escape_char
            else:
                string_value += self.advance()

        if self.peek() == '\0':
            self.error("النص غير مغلق - String not closed")

        self.advance()  # consume closing quote
        self.add_token(TokenType.STRING, string_value)

    def read_identifier(self):
        """يقرأ معرف أو كلمة مفتاحية / Read identifier or keyword"""
        start_line = self.line
        start_col = self.column
        ident = ''

        while is_identifier_char(self.peek()):
            ident += self.advance()

        # Check if it's a keyword / تحقق إذا كانت كلمة مفتاحية
        token_type = KEYWORDS.get(ident)
        if token_type is not None:
            self.add_token(token_type, ident)
        else:
            self.add_token(TokenType.IDENTIFIER, ident)

    def read_operator(self):
        """يقرأ عامل أو فاصلة / Read operator or delimiter"""
        ch = self.peek()

        # Three-character operators / عوامل من 3 أحرف
        three_char = ch + self.peek(1) + self.peek(2)

        if three_char == '...':
            # Could be spread, but we'll treat as DOTDOT for now
            pass

        # Two-character operators / عوامل من حرفين
        two_char = ch + self.peek(1)

        if two_char == '==':
            self.advance(); self.advance()
            self.add_token(TokenType.EQ, '==')
            return
        if two_char == '!=':
            self.advance(); self.advance()
            self.add_token(TokenType.NEQ, '!=')
            return
        if two_char == '<=':
            self.advance(); self.advance()
            self.add_token(TokenType.LTE, '<=')
            return
        if two_char == '>=':
            self.advance(); self.advance()
            self.add_token(TokenType.GTE, '>=')
            return
        if two_char == '..':
            self.advance(); self.advance()
            self.add_token(TokenType.DOTDOT, '..')
            return
        if two_char == '->':
            self.advance(); self.advance()
            self.add_token(TokenType.ARROW, '->')
            return
        if two_char == '+=':
            self.advance(); self.advance()
            self.add_token(TokenType.PLUS_ASSIGN, '+=')
            return
        if two_char == '-=':
            self.advance(); self.advance()
            self.add_token(TokenType.MINUS_ASSIGN, '-=')
            return
        if two_char == '*=':
            self.advance(); self.advance()
            self.add_token(TokenType.STAR_ASSIGN, '*=')
            return
        if two_char == '/=':
            self.advance(); self.advance()
            self.add_token(TokenType.SLASH_ASSIGN, '/=')
            return
        if two_char == '//':
            self.advance(); self.advance()
            self.add_token(TokenType.FLOOR_DIV, '//')
            return

        # Single-character operators / عوامل من حرف واحد
        single = {
            '+': TokenType.PLUS,
            '-': TokenType.MINUS,
            '*': TokenType.STAR,
            '/': TokenType.SLASH,
            '÷': TokenType.DIVIDE,
            '^': TokenType.POWER,
            '%': TokenType.MODULO,
            '=': TokenType.ASSIGN,
            '<': TokenType.LT,
            '>': TokenType.GT,
            '(': TokenType.LPAREN,
            ')': TokenType.RPAREN,
            '{': TokenType.LBRACE,
            '}': TokenType.RBRACE,
            '[': TokenType.LBRACKET,
            ']': TokenType.RBRACKET,
            ',': TokenType.COMMA,
            '.': TokenType.DOT,
            ':': TokenType.COLON,
            ';': TokenType.SEMICOLON,
            '?': TokenType.QUESTION,
        }

        if ch in single:
            self.advance()
            self.add_token(single[ch], ch)
            return

        # Unknown character / حرف غير معروف
        self.error(f"حرف غير معروف: '{ch}' - Unknown character: '{ch}'")
