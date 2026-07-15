"""
Opal Language - Parser / المحلل النحوي

Converts tokens into an Abstract Syntax Tree (AST).
يحول الرموز إلى شجرة نحو مجرد

Uses recursive descent parsing with proper precedence.
يستخدم التحليل النحوي التنازلي Recursive Descent
"""

from .tokens import TokenType, Token
from .ast_nodes import (
    NumberLiteral, StringLiteral, BooleanLiteral, NullLiteral,
    ListLiteral, Identifier, BinaryOp, UnaryOp, Assignment,
    Call, IndexAccess, MemberAccess, Range,
    VarDecl, EchoStmt, ExprStmt, Block, IfStmt, WhileStmt, ForStmt,
    FuncDecl, ReturnStmt, BreakStmt, ContinueStmt,
    ImportStmt, FromImportStmt, Program
)


class ParseError(Exception):
    """خطأ نحوي / Parse error"""

    def __init__(self, message, line=0, column=0):
        super().__init__(f"خطأ نحوي (ParseError) عند السطر {line}: {message}")
        self.line = line
        self.column = column


class Parser:
    """المحلل النحوي - يحول الرموز إلى AST / Parser - tokens to AST"""

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def parse(self):
        """يحلل كل البرنامج / Parse entire program"""
        statements = []
        self.skip_newlines()

        while not self.is_at_end():
            # Skip newlines between statements
            if self.check(TokenType.NEWLINE):
                self.advance()
                continue
            stmt = self.statement()
            if stmt is not None:
                statements.append(stmt)
            self.skip_newlines()

        return Program(statements)

    # ==========================================================
    # Helper methods / دوال مساعدة
    # ==========================================================

    def peek(self, offset=0):
        """ينظر للرمز الحالي / Peek current token"""
        idx = self.pos + offset
        if idx >= len(self.tokens):
            return self.tokens[-1]  # EOF
        return self.tokens[idx]

    def advance(self):
        """يتقدم رمز واحد / Advance one token"""
        if not self.is_at_end():
            self.pos += 1
        return self.tokens[self.pos - 1]

    def check(self, type):
        """يتحقق من نوع الرمز الحالي / Check current token type"""
        return self.peek().type == type

    def match(self, *types):
        """يتحقق من أنواع متعددة / Check multiple types"""
        for type in types:
            if self.check(type):
                return self.advance()
        return None

    def is_at_end(self):
        """هل وصلنا للنهاية / Are we at end"""
        return self.peek().type == TokenType.EOF

    def skip_newlines(self):
        """تخطي الأسطر الجديدة / Skip newlines"""
        while self.check(TokenType.NEWLINE):
            self.advance()

    def expect(self, type, message=None):
        """يتوقع رمز محدد / Expect a specific token"""
        if self.check(type):
            return self.advance()
        token = self.peek()
        if message is None:
            message = f"Expected {type.name}, got {token.type.name}"
        raise ParseError(f"{message} (وجد: '{token.value}')", token.line, token.column)

    # ==========================================================
    # Statements / الجمل
    # ==========================================================

    def statement(self):
        """يحلل جملة واحدة / Parse a single statement"""
        self.skip_newlines()

        # Variable declaration / تعريف متغير
        if self.check(TokenType.VAR) or self.check(TokenType.CONST):
            return self.var_declaration()

        # Echo/print / طباعة
        if self.check(TokenType.ECHO):
            return self.echo_statement()

        # If statement / جملة شرطية
        if self.check(TokenType.IF):
            return self.if_statement()

        # While loop / حلقة while
        if self.check(TokenType.WHILE):
            return self.while_statement()

        # For loop / حلقة for
        if self.check(TokenType.FOR):
            return self.for_statement()

        # Function declaration / تعريف دالة
        if self.check(TokenType.FUNCTION):
            return self.func_declaration()

        # Return / إرجاع
        if self.check(TokenType.RETURN):
            return self.return_statement()

        # Break / توقف
        if self.check(TokenType.BREAK):
            self.advance()
            self.consume_terminator()
            return BreakStmt()

        # Continue / اكمال
        if self.check(TokenType.CONTINUE):
            self.advance()
            self.consume_terminator()
            return ContinueStmt()

        # Import / استيراد
        if self.check(TokenType.IMPORT):
            return self.import_statement()

        # From import / استيراد محدد
        if self.check(TokenType.FROM):
            return self.from_import_statement()

        # Otherwise it's an expression statement / وإلا فهي جملة تعبير
        return self.expression_statement()

    def var_declaration(self):
        """var name = value / متغير اسم = قيمة"""
        is_const = self.check(TokenType.CONST)
        self.advance()  # consume var/const

        name_token = self.expect(TokenType.IDENTIFIER,
                                 "Expected variable name after 'var'/متغير")
        name = name_token.value

        self.expect(TokenType.ASSIGN,
                    "Expected '=' in variable declaration")

        value = self.expression()
        self.consume_terminator()

        return VarDecl(name, value, is_const)

    def echo_statement(self):
        """echo expr1, expr2, ... / اطبع"""
        self.advance()  # consume echo

        expressions = []
        expressions.append(self.expression())

        while self.match(TokenType.COMMA):
            expressions.append(self.expression())

        self.consume_terminator()
        return EchoStmt(expressions)

    def if_statement(self):
        """if cond { ... } elif cond { ... } else { ... }"""
        self.advance()  # consume if
        condition = self.expression()
        self.expect(TokenType.LBRACE, "Expected '{' after if condition")
        then_block = self.block()

        elif_branches = []
        else_block = None

        self.skip_newlines()

        # elif branches / فروع elif
        while self.check(TokenType.ELIF):
            self.advance()
            elif_cond = self.expression()
            self.expect(TokenType.LBRACE, "Expected '{' after elif condition")
            elif_block = self.block()
            elif_branches.append((elif_cond, elif_block))
            self.skip_newlines()

        # else branch / فرع else
        if self.check(TokenType.ELSE):
            self.advance()
            self.expect(TokenType.LBRACE, "Expected '{' after else")
            else_block = self.block()

        return IfStmt(condition, then_block, elif_branches, else_block)

    def while_statement(self):
        """while condition { ... }"""
        self.advance()  # consume while
        condition = self.expression()
        self.expect(TokenType.LBRACE, "Expected '{' after while condition")
        body = self.block()
        return WhileStmt(condition, body)

    def for_statement(self):
        """for var in iterable { ... }"""
        self.advance()  # consume for
        var_name = self.expect(TokenType.IDENTIFIER,
                                "Expected variable name after 'for'").value
        self.expect(TokenType.IN, "Expected 'in' in for loop")
        iterable = self.expression()
        self.expect(TokenType.LBRACE, "Expected '{' in for loop")
        body = self.block()
        return ForStmt(var_name, iterable, body)

    def func_declaration(self):
        """function name(params) { ... } / دالة اسم(بارامترات) { ... }"""
        self.advance()  # consume function/fun

        name = self.expect(TokenType.IDENTIFIER,
                           "Expected function name").value

        self.expect(TokenType.LPAREN, "Expected '(' after function name")

        params = []
        if not self.check(TokenType.RPAREN):
            params.append(self.expect(TokenType.IDENTIFIER,
                                      "Expected parameter name").value)
            while self.match(TokenType.COMMA):
                params.append(self.expect(TokenType.IDENTIFIER,
                                          "Expected parameter name").value)

        self.expect(TokenType.RPAREN, "Expected ')' after parameters")
        self.expect(TokenType.LBRACE, "Expected '{' before function body")

        body = self.block()
        return FuncDecl(name, params, body)

    def return_statement(self):
        """return value / ارجع قيمة"""
        self.advance()  # consume return

        # Check if there's a value / تحقق إذا كانت هناك قيمة
        if self.check(TokenType.NEWLINE) or self.check(TokenType.SEMICOLON) or \
           self.check(TokenType.RBRACE) or self.check(TokenType.EOF):
            self.consume_terminator()
            return ReturnStmt(None)

        value = self.expression()
        self.consume_terminator()
        return ReturnStmt(value)

    def import_statement(self):
        """import module / استورد وحدة"""
        self.advance()  # consume import
        module_name = self.expect(TokenType.IDENTIFIER,
                                  "Expected module name after 'import'").value
        self.consume_terminator()
        return ImportStmt(module_name)

    def from_import_statement(self):
        """from module import name1, name2 / من وحدة استورد اسم1، اسم2"""
        self.advance()  # consume from
        module_name = self.expect(TokenType.IDENTIFIER,
                                  "Expected module name after 'from'").value
        self.expect(TokenType.IMPORT, "Expected 'import' after module name")

        names = []
        names.append(self.expect(TokenType.IDENTIFIER,
                                 "Expected name to import").value)
        while self.match(TokenType.COMMA):
            names.append(self.expect(TokenType.IDENTIFIER,
                                     "Expected name to import").value)

        self.consume_terminator()
        return FromImportStmt(module_name, names)

    def expression_statement(self):
        """جملة تعبير / Expression as statement"""
        expr = self.expression()
        self.consume_terminator()
        return ExprStmt(expr)

    def block(self):
        """{ statements } / كتلة كود"""
        statements = []
        self.skip_newlines()

        while not self.check(TokenType.RBRACE) and not self.is_at_end():
            self.skip_newlines()
            if self.check(TokenType.RBRACE):
                break
            stmt = self.statement()
            if stmt is not None:
                statements.append(stmt)
            self.skip_newlines()

        self.expect(TokenType.RBRACE, "Expected '}' to close block")
        return Block(statements)

    def consume_terminator(self):
        """يستهلك نهاية الجملة / Consume statement terminator"""
        if self.check(TokenType.NEWLINE) or self.check(TokenType.SEMICOLON):
            self.advance()
        # Also OK if followed by RBRACE or EOF

    # ==========================================================
    # Expressions / التعبيرات (with precedence / مع الأولوية)
    # ==========================================================

    def expression(self):
        """التعبير الرئيسي / Main expression entry point"""
        return self.assignment_expr()

    def assignment_expr(self):
        """x = value / إسناد"""
        left = self.or_expr()

        if self.check(TokenType.ASSIGN):
            self.advance()
            right = self.assignment_expr()

            if not isinstance(left, Identifier):
                raise ParseError("Invalid assignment target",
                                 self.peek().line, self.peek().column)

            return Assignment(left.name, right)

        return left

    def or_expr(self):
        """a or b / a أو b"""
        left = self.and_expr()

        while self.check(TokenType.OR):
            op = self.advance()
            right = self.and_expr()
            left = BinaryOp(op, left, right, op.line, op.column)

        return left

    def and_expr(self):
        """a and b / a و b"""
        left = self.equality_expr()

        while self.check(TokenType.AND):
            op = self.advance()
            right = self.equality_expr()
            left = BinaryOp(op, left, right, op.line, op.column)

        return left

    def equality_expr(self):
        """a == b, a != b"""
        left = self.comparison_expr()

        while self.check(TokenType.EQ) or self.check(TokenType.NEQ):
            op = self.advance()
            right = self.comparison_expr()
            left = BinaryOp(op, left, right, op.line, op.column)

        return left

    def comparison_expr(self):
        """a < b, a > b, a <= b, a >= b"""
        left = self.range_expr()

        while self.check(TokenType.LT) or self.check(TokenType.GT) or \
              self.check(TokenType.LTE) or self.check(TokenType.GTE):
            op = self.advance()
            right = self.range_expr()
            left = BinaryOp(op, left, right, op.line, op.column)

        return left

    def range_expr(self):
        """a..b / نطاق"""
        left = self.addition_expr()

        if self.check(TokenType.DOTDOT):
            op = self.advance()
            right = self.addition_expr()
            left = Range(left, right, op.line, op.column)

        return left

    def addition_expr(self):
        """a + b, a - b"""
        left = self.multiplication_expr()

        while self.check(TokenType.PLUS) or self.check(TokenType.MINUS):
            op = self.advance()
            right = self.multiplication_expr()
            left = BinaryOp(op, left, right, op.line, op.column)

        return left

    def multiplication_expr(self):
        """a * b, a / b, a ÷ b, a % b"""
        left = self.power_expr()

        while self.check(TokenType.STAR) or self.check(TokenType.SLASH) or \
              self.check(TokenType.DIVIDE) or self.check(TokenType.MODULO):
            op = self.advance()
            right = self.power_expr()
            left = BinaryOp(op, left, right, op.line, op.column)

        return left

    def power_expr(self):
        """a ^ b"""
        left = self.unary_expr()

        while self.check(TokenType.POWER):
            op = self.advance()
            right = self.unary_expr()  # right-associative
            left = BinaryOp(op, left, right, op.line, op.column)

        return left

    def unary_expr(self):
        """-x, not x, ليس x"""
        if self.check(TokenType.MINUS):
            op = self.advance()
            operand = self.unary_expr()
            return UnaryOp(op, operand, op.line, op.column)

        if self.check(TokenType.NOT):
            op = self.advance()
            operand = self.unary_expr()
            return UnaryOp(op, operand, op.line, op.column)

        return self.postfix_expr()

    def postfix_expr(self):
        """function calls, index access, member access"""
        expr = self.primary()

        while True:
            if self.check(TokenType.LPAREN):
                # Function call / استدعاء دالة
                self.advance()
                args = []
                if not self.check(TokenType.RPAREN):
                    args.append(self.expression())
                    while self.match(TokenType.COMMA):
                        args.append(self.expression())
                self.expect(TokenType.RPAREN, "Expected ')' after arguments")
                expr = Call(expr, args)

            elif self.check(TokenType.LBRACKET):
                # Index access / وصول لعنصر
                self.advance()
                index = self.expression()
                self.expect(TokenType.RBRACKET, "Expected ']' after index")
                expr = IndexAccess(expr, index)

            elif self.check(TokenType.DOT):
                # Member access / وصول لعضو
                self.advance()
                member = self.expect(TokenType.IDENTIFIER,
                                     "Expected member name after '.'").value
                expr = MemberAccess(expr, member)

            else:
                break

        return expr

    def primary(self):
        """القيم الأساسية / Primary expressions"""
        # Number / رقم
        if self.check(TokenType.NUMBER):
            token = self.advance()
            return NumberLiteral(token.value, token.line, token.column)

        # String / نص
        if self.check(TokenType.STRING):
            token = self.advance()
            return StringLiteral(token.value, token.line, token.column)

        # Boolean / منطقي
        if self.check(TokenType.TRUE):
            token = self.advance()
            return BooleanLiteral(True, token.line, token.column)

        if self.check(TokenType.FALSE):
            token = self.advance()
            return BooleanLiteral(False, token.line, token.column)

        # Null / فارغ
        if self.check(TokenType.NULL):
            token = self.advance()
            return NullLiteral(token.line, token.column)

        # Identifier / معرف
        if self.check(TokenType.IDENTIFIER):
            token = self.advance()
            return Identifier(token.value, token.line, token.column)

        # Parenthesized expression / تعبير بين أقواس
        if self.check(TokenType.LPAREN):
            self.advance()
            expr = self.expression()
            self.expect(TokenType.RPAREN, "Expected ')' after expression")
            return expr

        # List literal / قائمة
        if self.check(TokenType.LBRACKET):
            self.advance()
            elements = []
            self.skip_newlines()
            if not self.check(TokenType.RBRACKET):
                elements.append(self.expression())
                while self.match(TokenType.COMMA):
                    self.skip_newlines()
                    elements.append(self.expression())
            self.skip_newlines()
            self.expect(TokenType.RBRACKET, "Expected ']' after list elements")
            return ListLiteral(elements)

        token = self.peek()
        raise ParseError(
            f"Unexpected token: {token.type.name} ('{token.value}')",
            token.line, token.column
        )
