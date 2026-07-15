"""
Opal Language - AST Nodes / عقد شجرة النحو المجرد

Defines all AST node types used by the parser and interpreter.
يعرّف جميع أنواع عقد شجرة النحو المجرد
"""

# ==============================================================
# Base Node / العقدة الأساسية
# ==============================================================

class ASTNode:
    """العقدة الأساسية لجميع عقد AST / Base class for all AST nodes"""

    def __init__(self, line=0, column=0):
        self.line = line
        self.column = column

    def __repr__(self):
        attrs = ', '.join(f"{k}={v!r}" for k, v in self.__dict__.items()
                          if k not in ('line', 'column'))
        return f"{self.__class__.__name__}({attrs})"


# ==============================================================
# Expressions / التعبيرات
# ==============================================================

class NumberLiteral(ASTNode):
    """رقم حرفي - 123 or 3.14"""
    def __init__(self, value, line=0, column=0):
        super().__init__(line, column)
        self.value = value


class StringLiteral(ASTNode):
    """نص حرفي - "hello" """
    def __init__(self, value, line=0, column=0):
        super().__init__(line, column)
        self.value = value


class BooleanLiteral(ASTNode):
    """قيمة منطقية - true/false or صحيح/خطأ"""
    def __init__(self, value, line=0, column=0):
        super().__init__(line, column)
        self.value = value


class NullLiteral(ASTNode):
    """قيمة فارغة - null/فراغ"""
    def __init__(self, line=0, column=0):
        super().__init__(line, column)
        self.value = None


class ListLiteral(ASTNode):
    """قائمة - [1, 2, 3]"""
    def __init__(self, elements, line=0, column=0):
        super().__init__(line, column)
        self.elements = elements


class Identifier(ASTNode):
    """اسم متغير - variable name"""
    def __init__(self, name, line=0, column=0):
        super().__init__(line, column)
        self.name = name


class BinaryOp(ASTNode):
    """عملية ثنائية - a + b, a > b, etc."""
    def __init__(self, op, left, right, line=0, column=0):
        super().__init__(line, column)
        self.op = op      # TokenType
        self.left = left
        self.right = right


class UnaryOp(ASTNode):
    """عملية أحادية - -x, not x, ليس x"""
    def __init__(self, op, operand, line=0, column=0):
        super().__init__(line, column)
        self.op = op
        self.operand = operand


class Assignment(ASTNode):
    """إسناد - x = value"""
    def __init__(self, name, value, line=0, column=0):
        super().__init__(line, column)
        self.name = name
        self.value = value


class Call(ASTNode):
    """استدعاء دالة - function(args)"""
    def __init__(self, callee, args, line=0, column=0):
        super().__init__(line, column)
        self.callee = callee    # The function expression
        self.args = args        # List of argument expressions


class IndexAccess(ASTNode):
    """وصول لعنصر - list[index]"""
    def __init__(self, obj, index, line=0, column=0):
        super().__init__(line, column)
        self.obj = obj
        self.index = index


class MemberAccess(ASTNode):
    """وصول لعضو - object.property"""
    def __init__(self, obj, member, line=0, column=0):
        super().__init__(line, column)
        self.obj = obj
        self.member = member


class Range(ASTNode):
    """نطاق - 1..10"""
    def __init__(self, start, end, line=0, column=0):
        super().__init__(line, column)
        self.start = start
        self.end = end


# ==============================================================
# Statements / الجمل
# ==============================================================

class VarDecl(ASTNode):
    """تعريف متغير - var x = value / متغير س = قيمة"""
    def __init__(self, name, value, is_const=False, line=0, column=0):
        super().__init__(line, column)
        self.name = name
        self.value = value
        self.is_const = is_const


class EchoStmt(ASTNode):
    """طباعة - echo value / اطبع قيمة"""
    def __init__(self, expressions, line=0, column=0):
        super().__init__(line, column)
        self.expressions = expressions  # list of expressions to print


class ExprStmt(ASTNode):
    """جملة تعبير - expression as statement"""
    def __init__(self, expression, line=0, column=0):
        super().__init__(line, column)
        self.expression = expression


class Block(ASTNode):
    """كتلة كود - { ... }"""
    def __init__(self, statements, line=0, column=0):
        super().__init__(line, column)
        self.statements = statements


class IfStmt(ASTNode):
    """جملة شرطية - if/elif/else"""
    def __init__(self, condition, then_block, elif_branches=None, else_block=None, line=0, column=0):
        super().__init__(line, column)
        self.condition = condition
        self.then_block = then_block
        self.elif_branches = elif_branches or []  # list of (condition, block)
        self.else_block = else_block


class WhileStmt(ASTNode):
    """حلقة while - while condition { ... }"""
    def __init__(self, condition, body, line=0, column=0):
        super().__init__(line, column)
        self.condition = condition
        self.body = body


class ForStmt(ASTNode):
    """حلقة for - for i in range { ... }"""
    def __init__(self, var_name, iterable, body, line=0, column=0):
        super().__init__(line, column)
        self.var_name = var_name
        self.iterable = iterable
        self.body = body


class FuncDecl(ASTNode):
    """تعريف دالة - function name(params) { ... }"""
    def __init__(self, name, params, body, line=0, column=0):
        super().__init__(line, column)
        self.name = name
        self.params = params    # list of parameter names
        self.body = body


class ReturnStmt(ASTNode):
    """إرجاع - return value / ارجع قيمة"""
    def __init__(self, value=None, line=0, column=0):
        super().__init__(line, column)
        self.value = value


class BreakStmt(ASTNode):
    """توقف - break / توقف"""
    def __init__(self, line=0, column=0):
        super().__init__(line, column)


class ContinueStmt(ASTNode):
    """اكمال - continue / اكمل"""
    def __init__(self, line=0, column=0):
        super().__init__(line, column)


class ImportStmt(ASTNode):
    """استيراد مكتبة - import math / استورد math"""
    def __init__(self, module_name, line=0, column=0):
        super().__init__(line, column)
        self.module_name = module_name


class FromImportStmt(ASTNode):
    """استيراد محدد - from strings import uppercase"""
    def __init__(self, module_name, names, line=0, column=0):
        super().__init__(line, column)
        self.module_name = module_name
        self.names = names  # list of names to import


class Program(ASTNode):
    """البرنامج الكامل / The complete program"""
    def __init__(self, statements, line=0, column=0):
        super().__init__(line, column)
        self.statements = statements
