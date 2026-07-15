"""
Opal Language - Interpreter / المفسر

Tree-walking interpreter that executes the AST.
مفسر يمشي على شجرة النحو وينفذها

This is the heart of Opal - it evaluates expressions and executes statements.
هذا هو قلب أوبال - يقيم التعبيرات وينفذ الجمل
"""

from .tokens import TokenType
from .ast_nodes import (
    NumberLiteral, StringLiteral, BooleanLiteral, NullLiteral,
    ListLiteral, Identifier, BinaryOp, UnaryOp, Assignment,
    Call, IndexAccess, MemberAccess, Range,
    VarDecl, EchoStmt, ExprStmt, Block, IfStmt, WhileStmt, ForStmt,
    FuncDecl, ReturnStmt, BreakStmt, ContinueStmt,
    ImportStmt, FromImportStmt, Program
)
from .environment import Environment
from .stdlib import load_module, module_exists


# ==============================================================
# Control Flow Signals / إشارات التحكم في التدفق
# Used to handle return, break, continue
# ==============================================================

class ReturnSignal(Exception):
    """إشارة الإرجاع / Return signal"""
    def __init__(self, value):
        self.value = value


class BreakSignal(Exception):
    """إشارة التوقف / Break signal"""
    pass


class ContinueSignal(Exception):
    """إشارة الإكمال / Continue signal"""
    pass


# ==============================================================
# Opal Function / دالة أوبال
# Represents a user-defined function
# ==============================================================

class OpalFunction:
    """دالة معرفة من قبل المستخدم / User-defined function"""

    def __init__(self, name, params, body, closure):
        self.name = name
        self.params = params
        self.body = body
        self.closure = closure  # النطاق المحيط / Enclosing scope

    def __call__(self, *args):
        """استدعاء الدالة / Call the function"""
        return self.interpreter.call_function(self, list(args))

    def __repr__(self):
        return f"<function {self.name}({', '.join(self.params)})>"


# ==============================================================
# Built-in Functions / الدوال المدمجة
# ==============================================================

class BuiltinFunction:
    """دالة مدمجة / Built-in function wrapper"""

    def __init__(self, name, func):
        self.name = name
        self.func = func

    def __call__(self, *args):
        return self.func(*args)

    def __repr__(self):
        return f"<builtin {self.name}>"


# ==============================================================
# Interpreter / المفسر
# ==============================================================

class OpalError(Exception):
    """خطأ في وقت التشغيل / Runtime error"""
    pass


class Interpreter:
    """مفسر أوبال - ينفذ AST / Opal interpreter - executes AST"""

    def __init__(self):
        self.global_env = Environment()
        self.setup_builtins()
        self.max_iterations = 10_000_000  # منع الحلقات اللانهائية / prevent infinite loops
        self.iteration_count = 0

    def setup_builtins(self):
        """تعريف الدوال المدمجة / Setup built-in functions"""

        # Print function / دالة الطباعة
        self.global_env.define('print', BuiltinFunction('print', self._builtin_print))
        self.global_env.define('طباعة', BuiltinFunction('طباعة', self._builtin_print))

        # Length function / دالة الطول
        self.global_env.define('len', BuiltinFunction('len', len))
        self.global_env.define('طول', BuiltinFunction('طول', len))

        # Type function / دالة النوع
        def _type_of(value):
            if value is None:
                return "null"
            if isinstance(value, bool):
                return "boolean"
            if isinstance(value, int):
                return "int"
            if isinstance(value, float):
                return "float"
            if isinstance(value, str):
                return "string"
            if isinstance(value, list):
                return "list"
            if isinstance(value, (OpalFunction, BuiltinFunction)):
                return "function"
            return "unknown"

        self.global_env.define('typeof', BuiltinFunction('typeof', _type_of))
        self.global_env.define('نوع', BuiltinFunction('نوع', _type_of))

        # String conversion / تحويل لنص
        def _to_str(value):
            return self.opal_to_string(value)

        self.global_env.define('str', BuiltinFunction('str', _to_str))
        self.global_env.define('نص', BuiltinFunction('نص', _to_str))

        # Number conversion / تحويل لرقم
        def _to_num(value):
            try:
                if isinstance(value, str):
                    if '.' in value:
                        return float(value)
                    return int(value)
                return int(value)
            except (ValueError, TypeError):
                return None

        self.global_env.define('number', BuiltinFunction('number', _to_num))
        self.global_env.define('رقم', BuiltinFunction('رقم', _to_num))

        # Input function / دالة الإدخال
        def _input(prompt=""):
            return input(str(prompt) if prompt else "")

        self.global_env.define('input', BuiltinFunction('input', _input))
        self.global_env.define('إدخال', BuiltinFunction('إدخال', _input))

        # Range function / دالة النطاق
        def _range(start, end=None, step=1):
            if end is None:
                return list(range(int(start)))
            return list(range(int(start), int(end), int(step)))

        self.global_env.define('range', BuiltinFunction('range', _range))
        self.global_env.define('نطاق', BuiltinFunction('نطاق', _range))

        # Auto-import common modules / استيراد تلقائي للوحدات الشائعة
        for mod_name in ['math', 'strings', 'lists', 'types']:
            mod = load_module(mod_name)
            if mod:
                for fname, fval in mod.items():
                    if callable(fval) or not fname.startswith('_'):
                        self.global_env.define(fname, fval)

    def _builtin_print(self, *args):
        """دالة الطباعة المدمجة / Built-in print function"""
        parts = [self.opal_to_string(arg) for arg in args]
        print(' '.join(parts))
        return None

    def interpret(self, program):
        """تفسير البرنامج كاملاً / Interpret the entire program"""
        try:
            for stmt in program.statements:
                self.execute(stmt, self.global_env)
        except ReturnSignal:
            pass  # Top-level return is OK
        return None

    # ==========================================================
    # Statement Execution / تنفيذ الجمل
    # ==========================================================

    def execute(self, node, env):
        """تنفيذ عقدة / Execute a node"""
        method_name = f'exec_{type(node).__name__}'
        method = getattr(self, method_name, None)
        if method is None:
            raise OpalError(f"لا يمكن تنفيذ: {type(node).__name__} - Cannot execute: {type(node).__name__}")
        return method(node, env)

    def exec_Program(self, node, env):
        """تنفيذ البرنامج / Execute program"""
        for stmt in node.statements:
            self.execute(stmt, env)

    def exec_VarDecl(self, node, env):
        """تنفيذ تعريف متغير / Execute variable declaration"""
        value = self.evaluate(node.value, env)
        env.define(node.name, value, node.is_const)

    def exec_EchoStmt(self, node, env):
        """تنفيذ الطباعة / Execute echo"""
        parts = []
        for expr in node.expressions:
            value = self.evaluate(expr, env)
            parts.append(self.opal_to_string(value))
        print(' '.join(parts))
        return None

    def exec_ExprStmt(self, node, env):
        """تنفيذ جملة تعبير / Execute expression statement"""
        return self.evaluate(node.expression, env)

    def exec_Block(self, node, env):
        """تنفيذ كتلة / Execute block"""
        block_env = Environment(env)
        for stmt in node.statements:
            self.execute(stmt, block_env)

    def exec_IfStmt(self, node, env):
        """تنفيذ جملة شرطية / Execute if statement"""
        condition = self.evaluate(node.condition, env)
        if self.is_truthy(condition):
            self.execute(node.then_block, env)
        else:
            for elif_cond, elif_block in node.elif_branches:
                if self.is_truthy(self.evaluate(elif_cond, env)):
                    self.execute(elif_block, env)
                    return
            if node.else_block is not None:
                self.execute(node.else_block, env)

    def exec_WhileStmt(self, node, env):
        """تنفيذ حلقة while / Execute while loop"""
        self.iteration_count = 0
        while self.is_truthy(self.evaluate(node.condition, env)):
            self.iteration_count += 1
            if self.iteration_count > self.max_iterations:
                raise OpalError(
                    f"تجاوز عدد التكرارات الحد الأقصى ({self.max_iterations}) - "
                    f"Maximum iterations exceeded"
                )
            try:
                self.execute(node.body, env)
            except BreakSignal:
                break
            except ContinueSignal:
                continue

    def exec_ForStmt(self, node, env):
        """تنفيذ حلقة for / Execute for loop"""
        iterable_val = self.evaluate(node.iterable, env)

        # Make it iterable / جعله قابل للتكرار
        if isinstance(iterable_val, list):
            items = iterable_val
        elif isinstance(iterable_val, str):
            items = list(iterable_val)
        elif isinstance(iterable_val, (int, float)):
            items = list(range(int(iterable_val)))
        elif isinstance(iterable_val, Range):
            items = list(range(
                int(self.evaluate(iterable_val.start, env)),
                int(self.evaluate(iterable_val.end, env)) + 1
            ))
        else:
            raise OpalError(
                f"لا يمكن التكرار على: {type(iterable_val).__name__} - "
                f"Cannot iterate over: {type(iterable_val).__name__}"
            )

        self.iteration_count = 0
        for item in items:
            self.iteration_count += 1
            if self.iteration_count > self.max_iterations:
                raise OpalError("تجاوز عدد التكرارات - Maximum iterations exceeded")

            loop_env = Environment(env)
            loop_env.define(node.var_name, item)
            try:
                self.execute(node.body, loop_env)
            except BreakSignal:
                break
            except ContinueSignal:
                continue

    def exec_FuncDecl(self, node, env):
        """تنفيذ تعريف دالة / Execute function declaration"""
        func = OpalFunction(node.name, node.params, node.body, env)
        env.define(node.name, func)

    def exec_ReturnStmt(self, node, env):
        """تنفيذ إرجاع / Execute return"""
        value = None
        if node.value is not None:
            value = self.evaluate(node.value, env)
        raise ReturnSignal(value)

    def exec_BreakStmt(self, node, env):
        """تنفيذ توقف / Execute break"""
        raise BreakSignal()

    def exec_ContinueStmt(self, node, env):
        """تنفيذ اكمال / Execute continue"""
        raise ContinueSignal()

    def exec_ImportStmt(self, node, env):
        """تنفيذ استيراد / Execute import"""
        mod = load_module(node.module_name)
        if mod is None:
            raise OpalError(
                f"المكتبة '{node.module_name}' غير موجودة - "
                f"Module '{node.module_name}' not found"
            )
        # Import all names into current environment
        for name, value in mod.items():
            env.define(name, value)

    def exec_FromImportStmt(self, node, env):
        """تنفيذ استيراد محدد / Execute from import"""
        mod = load_module(node.module_name)
        if mod is None:
            raise OpalError(
                f"المكتبة '{node.module_name}' غير موجودة - "
                f"Module '{node.module_name}' not found"
            )
        for name in node.names:
            if name in mod:
                env.define(name, mod[name])
            else:
                raise OpalError(
                    f"'{name}' غير موجود في '{node.module_name}' - "
                    f"'{name}' not found in '{node.module_name}'"
                )

    # ==========================================================
    # Expression Evaluation / تقييم التعبيرات
    # ==========================================================

    def evaluate(self, node, env):
        """تقييم عقدة / Evaluate a node"""
        method_name = f'eval_{type(node).__name__}'
        method = getattr(self, method_name, None)
        if method is None:
            raise OpalError(f"لا يمكن تقييم: {type(node).__name__} - Cannot evaluate: {type(node).__name__}")
        return method(node, env)

    def eval_NumberLiteral(self, node, env):
        return node.value

    def eval_StringLiteral(self, node, env):
        return node.value

    def eval_BooleanLiteral(self, node, env):
        return node.value

    def eval_NullLiteral(self, node, env):
        return None

    def eval_ListLiteral(self, node, env):
        return [self.evaluate(elem, env) for elem in node.elements]

    def eval_Identifier(self, node, env):
        return env.get(node.name)

    def eval_Range(self, node, env):
        """تقييم نطاق - يستخدم لاحقاً في for / Evaluate range"""
        start = self.evaluate(node.start, env)
        end = self.evaluate(node.end, env)
        return list(range(int(start), int(end) + 1))

    def eval_BinaryOp(self, node, env):
        """تقييم عملية ثنائية / Evaluate binary operation"""
        # Short-circuit evaluation for and/or / تقييم مختصر لـ and/or
        if node.op.type == TokenType.AND:
            left = self.evaluate(node.left, env)
            if not self.is_truthy(left):
                return left
            return self.evaluate(node.right, env)

        if node.op.type == TokenType.OR:
            left = self.evaluate(node.left, env)
            if self.is_truthy(left):
                return left
            return self.evaluate(node.right, env)

        left = self.evaluate(node.left, env)
        right = self.evaluate(node.right, env)

        op = node.op.type

        if op == TokenType.PLUS:
            # String concatenation or number addition
            if isinstance(left, str) or isinstance(right, str):
                return self.opal_to_string(left) + self.opal_to_string(right)
            if isinstance(left, list) and isinstance(right, list):
                return left + right
            return left + right

        if op == TokenType.MINUS:
            return left - right

        if op == TokenType.STAR:
            return left * right

        if op == TokenType.SLASH or op == TokenType.DIVIDE:
            if right == 0:
                raise OpalError("القسمة على صفر - Division by zero")
            return left / right

        if op == TokenType.POWER:
            return left ** right

        if op == TokenType.MODULO:
            return left % right

        if op == TokenType.EQ:
            return left == right

        if op == TokenType.NEQ:
            return left != right

        if op == TokenType.LT:
            return left < right

        if op == TokenType.GT:
            return left > right

        if op == TokenType.LTE:
            return left <= right

        if op == TokenType.GTE:
            return left >= right

        raise OpalError(f"عملية غير معروفة: {op} - Unknown operator: {op}")

    def eval_UnaryOp(self, node, env):
        """تقييم عملية أحادية / Evaluate unary operation"""
        operand = self.evaluate(node.operand, env)

        if node.op.type == TokenType.MINUS:
            return -operand
        if node.op.type == TokenType.NOT:
            return not self.is_truthy(operand)

        raise OpalError(f"عملية أحادية غير معروفة: {node.op.type} - Unknown unary operator")

    def eval_Assignment(self, node, env):
        """تقييم إسناد / Evaluate assignment"""
        value = self.evaluate(node.value, env)
        env.set(node.name, value)
        return value

    def eval_Call(self, node, env):
        """تقييم استدعاء دالة / Evaluate function call"""
        callee = self.evaluate(node.callee, env)

        # Evaluate arguments / تقييم الوسائط
        args = [self.evaluate(arg, env) for arg in node.args]

        # Call the function / استدعاء الدالة
        if isinstance(callee, OpalFunction):
            return self.call_function(callee, args)
        elif isinstance(callee, BuiltinFunction):
            return callee(*args)
        elif callable(callee):
            try:
                return callee(*args)
            except Exception as e:
                raise OpalError(f"خطأ في استدعاء الدالة - Error calling function: {e}")
        else:
            raise OpalError(
                f"هذا ليس دالة: {type(callee).__name__} - "
                f"This is not a function: {type(callee).__name__}"
            )

    def call_function(self, func, args):
        """استدعاء دالة أوبال / Call an Opal function"""
        # Create new scope from closure / إنشاء نطاق جديد من الإغلاق
        func_env = Environment(func.closure)

        # Bind parameters / ربط البارامترات
        if len(args) != len(func.params):
            # Allow fewer args with null defaults / السماح بوسائط أقل
            for i, param in enumerate(func.params):
                if i < len(args):
                    func_env.define(param, args[i])
                else:
                    func_env.define(param, None)
        else:
            for param, arg in zip(func.params, args):
                func_env.define(param, arg)

        # Execute body / تنفيذ الجسم
        try:
            self.execute(func.body, func_env)
        except ReturnSignal as r:
            return r.value

        return None  # Default return if no return statement

    def eval_IndexAccess(self, node, env):
        """تقييم وصول لعنصر / Evaluate index access"""
        obj = self.evaluate(node.obj, env)
        index = self.evaluate(node.index, env)

        if isinstance(obj, list):
            idx = int(index)
            # Support negative indices / دعم الفهارس السالبة
            if idx < 0:
                idx = len(obj) + idx
            if 0 <= idx < len(obj):
                return obj[idx]
            raise OpalError(f"الفهرس خارج النطاق: {idx} - Index out of range: {idx}")

        if isinstance(obj, str):
            idx = int(index)
            if idx < 0:
                idx = len(obj) + idx
            if 0 <= idx < len(obj):
                return obj[idx]
            raise OpalError(f"الفهرس خارج النطاق: {idx} - Index out of range: {idx}")

        if isinstance(obj, dict):
            return obj.get(index)

        raise OpalError(
            f"لا يمكن الفهرسة على: {type(obj).__name__} - "
            f"Cannot index into: {type(obj).__name__}"
        )

    def eval_MemberAccess(self, node, env):
        """تقييم وصول لعضو / Evaluate member access"""
        obj = self.evaluate(node.obj, env)

        member = node.member

        # If it's a dict / إذا كان قاموس
        if isinstance(obj, dict):
            if member in obj:
                return obj[member]
            raise OpalError(f"'{member}' غير موجود - '{member}' not found")

        # If it's a list, provide built-in methods / إذا كان قائمة
        if isinstance(obj, list):
            if member == 'length' or member == 'طول':
                return len(obj)
            if member == 'push' or member == 'أضف':
                return BuiltinFunction('push', lambda item: obj.append(item) or obj)
            if member == 'pop':
                return BuiltinFunction('pop', lambda: obj.pop() if obj else None)
            if member == 'reverse' or member == 'عكس':
                return BuiltinFunction('reverse', lambda: list(reversed(obj)))
            if member == 'sort' or member == 'رتب':
                return BuiltinFunction('sort', lambda: sorted(obj))

        # If it's a string, provide built-in methods / إذا كان نص
        if isinstance(obj, str):
            if member == 'length' or member == 'طول':
                return len(obj)
            if member == 'upper' or member == 'كبير':
                return BuiltinFunction('upper', lambda: obj.upper())
            if member == 'lower' or member == 'صغير':
                return BuiltinFunction('lower', lambda: obj.lower())
            if member == 'reverse' or member == 'عكس':
                return BuiltinFunction('reverse', lambda: obj[::-1])
            if member == 'trim' or member == 'نظف':
                return BuiltinFunction('trim', lambda: obj.strip())

        raise OpalError(
            f"'{member}' غير موجود في {type(obj).__name__} - "
            f"'{member}' not found in {type(obj).__name__}"
        )

    # ==========================================================
    # Helpers / دوال مساعدة
    # ==========================================================

    def is_truthy(self, value):
        """تحقق من أن القيمة صحيحة / Check if value is truthy"""
        if value is None:
            return False
        if isinstance(value, bool):
            return value
        if isinstance(value, (int, float)):
            return value != 0
        if isinstance(value, str):
            return len(value) > 0
        if isinstance(value, list):
            return len(value) > 0
        return True

    def opal_to_string(self, value):
        """تحويل قيمة إلى نص / Convert value to string for display"""
        if value is None:
            return "null"
        if value is True:
            return "true"
        if value is False:
            return "false"
        if isinstance(value, list):
            return '[' + ', '.join(self.opal_to_string(v) for v in value) + ']'
        if isinstance(value, OpalFunction):
            return f"<function {value.name}>"
        if isinstance(value, BuiltinFunction):
            return f"<builtin {value.name}>"
        return str(value)
