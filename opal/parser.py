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
    Call, IndexAccess, MemberAccess, Range, DictLiteral, LambdaExpr,
    ThisExpr, NewExpr, TernaryExpr, CompoundAssign,
    VarDecl, EchoStmt, ExprStmt, Block, IfStmt, WhileStmt, ForStmt,
    FuncDecl, ReturnStmt, BreakStmt, ContinueStmt,
    ImportStmt, FromImportStmt, Program, TryStmt, ThrowStmt,
    ClassDecl, SwitchStmt, DoUntilStmt
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

        # Do-until loop / حلقة افعل-حتى
        if self.check(TokenType.DO):
            return self.do_until_statement()

        # Function declaration / تعريف دالة
        if self.check(TokenType.FUNCTION):
            return self.func_declaration()

        # Class declaration / تعريف صف
        if self.check(TokenType.CLASS):
            return self.class_declaration()

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

        # Try/catch / حاول/امسك
        if self.check(TokenType.TRY):
            return self.try_statement()

        # Throw / رمي
        if self.check(TokenType.THROW):
            return self.throw_statement()

        # Switch / بدل
        if self.check(TokenType.SWITCH):
            return self.switch_statement()

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

    def try_statement(self):
        """try { } catch (e) { } finally { } / حاول {} أمسك (هـ) {} أخيرا {}"""
        self.advance()  # consume try
        self.expect(TokenType.LBRACE, "Expected '{' after try")
        try_block = self.block()

        catch_param = None
        catch_block = None
        finally_block = None

        self.skip_newlines()

        if self.check(TokenType.CATCH):
            self.advance()
            if self.check(TokenType.LPAREN):
                self.advance()
                catch_param = self.expect(TokenType.IDENTIFIER,
                                          "Expected error variable name").value
                self.expect(TokenType.RPAREN, "Expected ')' after catch variable")
            self.expect(TokenType.LBRACE, "Expected '{' after catch")
            catch_block = self.block()

        self.skip_newlines()

        if self.check(TokenType.FINALLY):
            self.advance()
            self.expect(TokenType.LBRACE, "Expected '{' after finally")
            finally_block = self.block()

        return TryStmt(try_block, catch_param, catch_block, finally_block)

    def throw_statement(self):
        """throw expr / ارمي قيمة"""
        self.advance()  # consume throw
        value = self.expression()
        self.consume_terminator()
        return ThrowStmt(value)

    def class_declaration(self):
        """class Name { methods } / صف اسم { دوال }"""
        self.advance()  # consume class
        name = self.expect(TokenType.IDENTIFIER,
                           "Expected class name").value

        parent = None
        # Optional inheritance: class Name extends Parent / صف اسم يرث أب
        if self.match(TokenType.COLON):
            parent = self.expect(TokenType.IDENTIFIER,
                                 "Expected parent class name").value

        self.expect(TokenType.LBRACE, "Expected '{' after class name")

        methods = []
        self.skip_newlines()
        while not self.check(TokenType.RBRACE) and not self.is_at_end():
            self.skip_newlines()
            if self.check(TokenType.RBRACE):
                break
            # Each method is a function declaration
            if self.check(TokenType.FUNCTION):
                methods.append(self.func_declaration())
            else:
                # Allow method without 'function' keyword
                method_name = self.expect(TokenType.IDENTIFIER,
                                          "Expected method name").value
                self.expect(TokenType.LPAREN, "Expected '('")
                params = []
                if not self.check(TokenType.RPAREN):
                    params.append(self.expect(TokenType.IDENTIFIER).value)
                    while self.match(TokenType.COMMA):
                        params.append(self.expect(TokenType.IDENTIFIER).value)
                self.expect(TokenType.RPAREN, "Expected ')'")
                self.expect(TokenType.LBRACE, "Expected '{'")
                body = self.block()
                methods.append(FuncDecl(method_name, params, body))
            self.skip_newlines()

        self.expect(TokenType.RBRACE, "Expected '}' to close class")
        return ClassDecl(name, methods, parent)

    def switch_statement(self):
        """switch (expr) { case v: { } default: { } } / بدل (تعبير) {}"""
        self.advance()  # consume switch
        self.expect(TokenType.LPAREN, "Expected '(' after switch")
        expr = self.expression()
        self.expect(TokenType.RPAREN, "Expected ')' after switch expression")
        self.expect(TokenType.LBRACE, "Expected '{' for switch body")

        cases = []
        default_block = None
        self.skip_newlines()

        while not self.check(TokenType.RBRACE) and not self.is_at_end():
            self.skip_newlines()
            if self.check(TokenType.RBRACE):
                break

            if self.check(TokenType.CASE):
                self.advance()
                case_value = self.expression()
                self.expect(TokenType.COLON, "Expected ':' after case value")
                case_block = self.block_or_stmts()
                cases.append((case_value, case_block))
            elif self.check(TokenType.DEFAULT):
                self.advance()
                self.expect(TokenType.COLON, "Expected ':' after default")
                default_block = self.block_or_stmts()
            else:
                raise ParseError("Expected 'case' or 'default' in switch",
                                 self.peek().line, self.peek().column)
            self.skip_newlines()

        self.expect(TokenType.RBRACE, "Expected '}' to close switch")
        return SwitchStmt(expr, cases, default_block)

    def block_or_stmts(self):
        """Parse either a block { } or statements until next case/default/}"""
        if self.check(TokenType.LBRACE):
            self.advance()
            return self.block()
        # Read statements until next case/default/}
        statements = []
        while not self.check(TokenType.CASE) and not self.check(TokenType.DEFAULT) \
              and not self.check(TokenType.RBRACE) and not self.is_at_end():
            self.skip_newlines()
            if self.check(TokenType.CASE) or self.check(TokenType.DEFAULT) \
               or self.check(TokenType.RBRACE):
                break
            stmt = self.statement()
            if stmt is not None:
                statements.append(stmt)
            self.skip_newlines()
        return Block(statements)

    def do_until_statement(self):
        """do { } until (cond) / افعل {} حتى ()"""
        self.advance()  # consume do
        self.expect(TokenType.LBRACE, "Expected '{' after do")
        body = self.block()
        self.expect(TokenType.UNTIL, "Expected 'until' after do block")
        self.expect(TokenType.LPAREN, "Expected '(' after until")
        condition = self.expression()
        self.expect(TokenType.RPAREN, "Expected ')' after until condition")
        self.consume_terminator()
        return DoUntilStmt(body, condition)

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
        return self.ternary_expr()

    def ternary_expr(self):
        """cond ? a : b / شرط ? أ : ب"""
        cond = self.assignment_expr()
        if self.check(TokenType.QUESTION):
            self.advance()
            then_expr = self.ternary_expr()
            self.expect(TokenType.COLON, "Expected ':' in ternary expression")
            else_expr = self.ternary_expr()
            return TernaryExpr(cond, then_expr, else_expr)
        return cond

    def assignment_expr(self):
        """x = value / إسناد"""
        left = self.or_expr()

        # Regular assignment / إسناد عادي
        if self.check(TokenType.ASSIGN):
            self.advance()
            right = self.assignment_expr()
            return Assignment(left, right)

        # Compound assignments / إسناد مركب
        if self.check(TokenType.PLUS_ASSIGN) or self.check(TokenType.MINUS_ASSIGN) \
           or self.check(TokenType.STAR_ASSIGN) or self.check(TokenType.SLASH_ASSIGN):
            op = self.advance()
            right = self.assignment_expr()
            return CompoundAssign(left, op, right)

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

        # this / هذا
        if self.check(TokenType.THIS):
            token = self.advance()
            return ThisExpr(token.line, token.column)

        # Lambda / fn(params) -> expr | { block } / دالة مجهولة
        if self.check(TokenType.LAMBDA):
            return self.lambda_expr()

        # new ClassName(args) / جديد اسم الصف(وسائط)
        if self.check(TokenType.NEW):
            self.advance()
            class_name = self.expect(TokenType.IDENTIFIER,
                                     "Expected class name after 'new'").value
            self.expect(TokenType.LPAREN, "Expected '(' after class name")
            args = []
            if not self.check(TokenType.RPAREN):
                args.append(self.expression())
                while self.match(TokenType.COMMA):
                    args.append(self.expression())
            self.expect(TokenType.RPAREN, "Expected ')' after arguments")
            return NewExpr(class_name, args)

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

        # Dict literal / قاموس {key: value, ...}
        # Must be careful: { could start a block. In expression context, treat as dict.
        if self.check(TokenType.LBRACE):
            return self.dict_literal()

        token = self.peek()
        raise ParseError(
            f"Unexpected token: {token.type.name} ('{token.value}')",
            token.line, token.column
        )

    def lambda_expr(self):
        """fn(params) -> expr or { block } / دالة مجهولة"""
        self.advance()  # consume fn/lambda

        self.expect(TokenType.LPAREN, "Expected '(' after lambda")
        params = []
        if not self.check(TokenType.RPAREN):
            params.append(self.expect(TokenType.IDENTIFIER, "Expected parameter").value)
            while self.match(TokenType.COMMA):
                params.append(self.expect(TokenType.IDENTIFIER, "Expected parameter").value)
        self.expect(TokenType.RPAREN, "Expected ')' after lambda params")

        # Optional arrow / السهم الاختياري
        if self.check(TokenType.ARROW):
            self.advance()

        # Body: either expression or block
        if self.check(TokenType.LBRACE):
            self.advance()
            body = self.block()
        else:
            body = Block([ReturnStmt(self.expression())])

        return LambdaExpr(params, body)

    def dict_literal(self):
        """{key: value, key2: value2} / قاموس"""
        self.advance()  # consume {
        pairs = []
        self.skip_newlines()

        if not self.check(TokenType.RBRACE):
            # Parse first pair / أول زوج
            key = self.expression()
            self.expect(TokenType.COLON, "Expected ':' after dict key")
            value = self.expression()
            pairs.append((key, value))

            while self.match(TokenType.COMMA):
                self.skip_newlines()
                if self.check(TokenType.RBRACE):
                    break
                key = self.expression()
                self.expect(TokenType.COLON, "Expected ':' after dict key")
                value = self.expression()
                pairs.append((key, value))

        self.skip_newlines()
        self.expect(TokenType.RBRACE, "Expected '}' to close dict")
        return DictLiteral(pairs)
