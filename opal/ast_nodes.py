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
    """إسناد - x = value (or this.field = value, obj.prop = value)"""
    def __init__(self, target, value, line=0, column=0):
        super().__init__(line, column)
        self.target = target  # can be Identifier, MemberAccess, or IndexAccess
        self.name = target.name if isinstance(target, Identifier) else None
        self.value = value


class CompoundAssign(ASTNode):
    """إسناد مركب - x += 5 (or this.field += 5)"""
    def __init__(self, target, op, value, line=0, column=0):
        super().__init__(line, column)
        self.target = target
        self.name = target.name if isinstance(target, Identifier) else None
        self.op = op  # TokenType
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


class DictLiteral(ASTNode):
    """قاموس - {key: value, key2: value2}"""
    def __init__(self, pairs, line=0, column=0):
        super().__init__(line, column)
        self.pairs = pairs  # list of (key_expr, value_expr)


class LambdaExpr(ASTNode):
    """دالة مجهولة - fn(x) -> x * 2"""
    def __init__(self, params, body, line=0, column=0):
        super().__init__(line, column)
        self.params = params
        self.body = body


class ThisExpr(ASTNode):
    """this - الإشارة للكائن الحالي"""
    def __init__(self, line=0, column=0):
        super().__init__(line, column)


class NewExpr(ASTNode):
    """new ClassName(args) - إنشاء كائن جديد"""
    def __init__(self, class_name, args, line=0, column=0):
        super().__init__(line, column)
        self.class_name = class_name
        self.args = args


class TernaryExpr(ASTNode):
    """عملية ثلاثية - cond ? a : b"""
    def __init__(self, condition, then_expr, else_expr, line=0, column=0):
        super().__init__(line, column)
        self.condition = condition
        self.then_expr = then_expr
        self.else_expr = else_expr


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


class TryStmt(ASTNode):
    """try/catch/finally - حاول/امسك/أخيرا"""
    def __init__(self, try_block, catch_param, catch_block, finally_block=None, line=0, column=0):
        super().__init__(line, column)
        self.try_block = try_block
        self.catch_param = catch_param  # variable name for caught error
        self.catch_block = catch_block
        self.finally_block = finally_block


class ThrowStmt(ASTNode):
    """throw expr - رمي خطأ"""
    def __init__(self, value, line=0, column=0):
        super().__init__(line, column)
        self.value = value


class ClassDecl(ASTNode):
    """class definition - تعريف صف"""
    def __init__(self, name, methods, parent=None, line=0, column=0):
        super().__init__(line, column)
        self.name = name
        self.methods = methods  # list of FuncDecl
        self.parent = parent    # parent class name


class SwitchStmt(ASTNode):
    """switch/case/default - بدل/حالة/افتراضي"""
    def __init__(self, expr, cases, default_block=None, line=0, column=0):
        super().__init__(line, column)
        self.expr = expr
        self.cases = cases  # list of (value_expr, block)
        self.default_block = default_block


class DoUntilStmt(ASTNode):
    """do { } until (cond) - افعل {} حتى ()"""
    def __init__(self, body, condition, line=0, column=0):
        super().__init__(line, column)
        self.body = body
        self.condition = condition


class Program(ASTNode):
    """البرنامج الكامل / The complete program"""
    def __init__(self, statements, line=0, column=0):
        super().__init__(line, column)
        self.statements = statements
