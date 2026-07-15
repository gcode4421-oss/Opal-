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
    Call, IndexAccess, MemberAccess, Range, DictLiteral, LambdaExpr,
    ThisExpr, NewExpr, TernaryExpr, CompoundAssign,
    VarDecl, EchoStmt, ExprStmt, Block, IfStmt, WhileStmt, ForStmt,
    FuncDecl, ReturnStmt, BreakStmt, ContinueStmt,
    ImportStmt, FromImportStmt, Program, TryStmt, ThrowStmt,
    ClassDecl, SwitchStmt, DoUntilStmt
)
from .environment import Environment
from .stdlib import load_module, module_exists


# ==============================================================
# Control Flow Signals / إشارات التحكم في التدفق
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


class OpalThrow(Exception):
    """خطأ مرمي من throw / An error thrown by throw statement"""
    def __init__(self, value):
        self.value = value
        super().__init__(str(value))


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
# Opal Class & Instance / الصف والكائن في أوبال
# ==============================================================

class OpalClass:
    """صف معرف من قبل المستخدم / User-defined class"""

    def __init__(self, name, methods, parent=None):
        self.name = name
        self.methods = methods  # dict: name -> OpalFunction
        self.parent = parent    # parent OpalClass (or None)

    def find_method(self, name):
        """يبحث عن دالة بالاسم / Find method by name"""
        if name in self.methods:
            return self.methods[name]
        if self.parent is not None:
            return self.parent.find_method(name)
        return None

    def __repr__(self):
        return f"<class {self.name}>"


class OpalInstance:
    """كائن من صف / An instance of an Opal class"""

    def __init__(self, opal_class):
        self.opal_class = opal_class
        self.fields = {}  # متغيرات الكائن / Instance fields

    def get_field(self, name):
        if name in self.fields:
            return self.fields[name]
        method = self.opal_class.find_method(name)
        if method is not None:
            return method
        return None

    def __repr__(self):
        return f"<{self.opal_class.name} instance>"


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
        for mod_name in ['math', 'strings', 'lists', 'types', 'time', 'system']:
            mod = load_module(mod_name)
            if mod:
                for fname, fval in mod.items():
                    if callable(fval) or not fname.startswith('_'):
                        self.global_env.define(fname, fval)

        # Make JSON and HTTP available but not auto-loaded (need explicit import)
        # JSON و HTTP متاحان لكن يحتاجان استيراد صريح

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

    def exec_TryStmt(self, node, env):
        """تنفيذ try/catch/finally / تنفيذ حاول/امسك/أخيرا"""
        try:
            self.execute(node.try_block, env)
        except (OpalThrow, OpalError) as thrown:
            # Get the value from the error
            if isinstance(thrown, OpalThrow):
                err_value = thrown.value
            else:
                err_value = str(thrown)

            if node.catch_block is not None:
                catch_env = Environment(env)
                if node.catch_param is not None:
                    catch_env.define(node.catch_param, err_value)
                try:
                    self.execute(node.catch_block, catch_env)
                except ReturnSignal:
                    raise
            else:
                raise
        finally:
            if node.finally_block is not None:
                self.execute(node.finally_block, env)

    def exec_ThrowStmt(self, node, env):
        """تنفيذ throw / تنفيذ ارمي"""
        value = self.evaluate(node.value, env)
        raise OpalThrow(value)

    def exec_ClassDecl(self, node, env):
        """تنفيذ تعريف صف / Execute class declaration"""
        parent_class = None
        if node.parent is not None:
            parent_class = env.get(node.parent)
            if not isinstance(parent_class, OpalClass):
                raise OpalError(
                    f"'{node.parent}' ليس صف - '{node.parent}' is not a class"
                )

        # Build method dict
        methods = {}
        for method in node.methods:
            func = OpalFunction(method.name, method.params, method.body, env)
            func.interpreter = self
            methods[method.name] = func

        opal_class = OpalClass(node.name, methods, parent_class)
        env.define(node.name, opal_class)

    def exec_SwitchStmt(self, node, env):
        """تنفيذ switch / تنفيذ بدل"""
        expr_val = self.evaluate(node.expr, env)
        for case_value_expr, case_block in node.cases:
            case_val = self.evaluate(case_value_expr, env)
            if expr_val == case_val:
                self.execute(case_block, env)
                return
        if node.default_block is not None:
            self.execute(node.default_block, env)

    def exec_DoUntilStmt(self, node, env):
        """تنفيذ do-until / تنفيذ افعل-حتى
        تكرر الجسم حتى يصبح الشرط صحيحاً (تتوقف عند الصحة)
        Repeat body UNTIL condition is true (stop when true)
        """
        self.iteration_count = 0
        while True:
            self.iteration_count += 1
            if self.iteration_count > self.max_iterations:
                raise OpalError("تجاوز عدد التكرارات - Maximum iterations exceeded")
            try:
                for stmt in node.body.statements:
                    self.execute(stmt, env)
            except BreakSignal:
                break
            except ContinueSignal:
                pass
            # Check condition AFTER body / فحص الشرط بعد الجسم
            # until: stop when condition becomes TRUE / حتى: توقف عند صحة الشرط
            if self.is_truthy(self.evaluate(node.condition, env)):
                break

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

    def eval_DictLiteral(self, node, env):
        """تقييم قاموس / Evaluate dict literal"""
        result = {}
        for key_expr, value_expr in node.pairs:
            key = self.evaluate(key_expr, env)
            value = self.evaluate(value_expr, env)
            result[key] = value
        return result

    def eval_LambdaExpr(self, node, env):
        """تقييم دالة مجهولة / Evaluate lambda"""
        func = OpalFunction("<lambda>", node.params, node.body, env)
        func.interpreter = self
        return func

    def eval_ThisExpr(self, node, env):
        """تقييم this / Evaluate this"""
        if env.has("this"):
            return env.get("this")
        raise OpalError("'this' غير متاح هنا - 'this' is not available here")

    def eval_NewExpr(self, node, env):
        """تقييم new ClassName(args) / إنشاء كائن جديد"""
        opal_class = env.get(node.class_name)
        if not isinstance(opal_class, OpalClass):
            raise OpalError(
                f"'{node.class_name}' ليس صف - '{node.class_name}' is not a class"
            )

        instance = OpalInstance(opal_class)
        args = [self.evaluate(arg, env) for arg in node.args]

        # Call constructor if exists / استدعاء المنشئ إذا وجد
        constructor = opal_class.find_method("init") or \
                      opal_class.find_method("constructor") or \
                      opal_class.find_method("__init__")
        if constructor is not None:
            constructor.interpreter = self
            self.call_method(constructor, instance, args)

        return instance

    def call_method(self, method, instance, args):
        """استدعاء دالة على كائن / Call a method on an instance"""
        method_env = Environment(method.closure)
        method_env.define("this", instance)
        if len(args) != len(method.params):
            for i, param in enumerate(method.params):
                method_env.define(param, args[i] if i < len(args) else None)
        else:
            for param, arg in zip(method.params, args):
                method_env.define(param, arg)
        try:
            self.execute(method.body, method_env)
        except ReturnSignal as r:
            return r.value
        return None

    def eval_TernaryExpr(self, node, env):
        """تقييم عملية ثلاثية / Evaluate ternary"""
        cond = self.evaluate(node.condition, env)
        if self.is_truthy(cond):
            return self.evaluate(node.then_expr, env)
        return self.evaluate(node.else_expr, env)

    def eval_CompoundAssign(self, node, env):
        """تقييم إسناد مركب / Evaluate compound assignment (+=, etc.)"""
        # Get current value based on target type
        if isinstance(node.target, Identifier):
            current = env.get(node.target.name)
        elif isinstance(node.target, MemberAccess):
            # Use member access logic
            temp_access = MemberAccess(node.target.obj, node.target.member)
            current = self.eval_MemberAccess(temp_access, env)
        elif isinstance(node.target, IndexAccess):
            temp_access = IndexAccess(node.target.obj, node.target.index)
            current = self.eval_IndexAccess(temp_access, env)
        else:
            raise OpalError("هدف إسناد غير صالح - Invalid compound assignment target")

        right = self.evaluate(node.value, env)

        if node.op.type == TokenType.PLUS_ASSIGN:
            if isinstance(current, str) or isinstance(right, str):
                new_val = self.opal_to_string(current) + self.opal_to_string(right)
            else:
                new_val = current + right
        elif node.op.type == TokenType.MINUS_ASSIGN:
            new_val = current - right
        elif node.op.type == TokenType.STAR_ASSIGN:
            new_val = current * right
        elif node.op.type == TokenType.SLASH_ASSIGN:
            if right == 0:
                raise OpalError("القسمة على صفر - Division by zero")
            new_val = current / right
        else:
            raise OpalError(f"عملية إسناد غير معروفة - Unknown compound assignment")

        # Set new value based on target type
        if isinstance(node.target, Identifier):
            env.set(node.target.name, new_val)
        elif isinstance(node.target, MemberAccess):
            obj = self.evaluate(node.target.obj, env)
            if isinstance(obj, OpalInstance):
                obj.fields[node.target.member] = new_val
            elif isinstance(obj, dict):
                obj[node.target.member] = new_val
        elif isinstance(node.target, IndexAccess):
            obj = self.evaluate(node.target.obj, env)
            index = self.evaluate(node.target.index, env)
            if isinstance(obj, list):
                idx = int(index)
                while idx >= len(obj):
                    obj.append(None)
                obj[idx] = new_val
            elif isinstance(obj, dict):
                obj[index] = new_val

        return new_val

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

        # Simple variable assignment / إسناد متغير بسيط
        if isinstance(node.target, Identifier):
            env.set(node.target.name, value)
            return value

        # Member assignment: this.field = value / obj.prop = value / إسناد لعضو
        if isinstance(node.target, MemberAccess):
            obj = self.evaluate(node.target.obj, env)
            member = node.target.member

            # Instance field / حقل كائن
            if isinstance(obj, OpalInstance):
                obj.fields[member] = value
                return value

            # Dict / قاموس
            if isinstance(obj, dict):
                obj[member] = value
                return value

            raise OpalError(
                f"لا يمكن الإسناد إلى عضو في {type(obj).__name__} - "
                f"Cannot assign to member of {type(obj).__name__}"
            )

        # Index assignment: list[i] = value / dict[key] = value
        if isinstance(node.target, IndexAccess):
            obj = self.evaluate(node.target.obj, env)
            index = self.evaluate(node.target.index, env)

            if isinstance(obj, list):
                idx = int(index)
                if idx < 0:
                    idx = len(obj) + idx
                while idx >= len(obj):
                    obj.append(None)
                obj[idx] = value
                return value

            if isinstance(obj, dict):
                obj[index] = value
                return value

            raise OpalError(
                f"لا يمكن الإسناد إلى فهرس في {type(obj).__name__} - "
                f"Cannot assign to index of {type(obj).__name__}"
            )

        raise OpalError("هدف إسناد غير صالح - Invalid assignment target")

    def eval_Call(self, node, env):
        """تقييم استدعاء دالة / Evaluate function call"""
        # Handle method calls on instances - need to set 'this'
        if isinstance(node.callee, MemberAccess):
            obj = self.evaluate(node.callee.obj, env)
            member = node.callee.member

            # Method call on instance / استدعاء دالة على كائن
            if isinstance(obj, OpalInstance):
                method = obj.opal_class.find_method(member)
                if method is None:
                    raise OpalError(
                        f"الدالة '{member}' غير موجودة - Method '{member}' not found"
                    )
                method.interpreter = self
                args = [self.evaluate(arg, env) for arg in node.args]
                return self.call_method(method, obj, args)

        callee = self.evaluate(node.callee, env)

        # Evaluate arguments / تقييم الوسائط
        args = [self.evaluate(arg, env) for arg in node.args]

        # Call the function / استدعاء الدالة
        if isinstance(callee, OpalFunction):
            callee.interpreter = self
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

        # If it's an OpalInstance / إذا كان كائن من صف
        if isinstance(obj, OpalInstance):
            if member in obj.fields:
                return obj.fields[member]
            method = obj.opal_class.find_method(member)
            if method is not None:
                return method
            raise OpalError(
                f"'{member}' غير موجود في الصف '{obj.opal_class.name}' - "
                f"'{member}' not found in class '{obj.opal_class.name}'"
            )

        # If it's an OpalClass (static access) / إذا كان صف
        if isinstance(obj, OpalClass):
            method = obj.find_method(member)
            if method is not None:
                return method
            raise OpalError(
                f"'{member}' غير موجود في الصف '{obj.name}' - "
                f"'{member}' not found in class '{obj.name}'"
            )

        # If it's a dict / إذا كان قاموس
        if isinstance(obj, dict):
            if member in obj:
                return obj[member]
            # Also support string key access
            raise OpalError(f"'{member}' غير موجود - '{member}' not found")

        # If it's a list, provide built-in methods / إذا كان قائمة
        if isinstance(obj, list):
            if member == 'length' or member == 'طول' or member == 'size':
                return len(obj)
            if member == 'push' or member == 'أضف':
                return BuiltinFunction('push', lambda item: obj.append(item) or obj)
            if member == 'pop':
                return BuiltinFunction('pop', lambda: obj.pop() if obj else None)
            if member == 'reverse' or member == 'عكس':
                return BuiltinFunction('reverse', lambda: list(reversed(obj)))
            if member == 'sort' or member == 'رتب':
                return BuiltinFunction('sort', lambda: sorted(obj))
            if member == 'join' or member == 'دمج':
                return BuiltinFunction('join', lambda sep="": sep.join(str(x) for x in obj))
            if member == 'contains' or member == 'يحتوي':
                return BuiltinFunction('contains', lambda item: item in obj)
            if member == 'index_of' or member == 'موضع':
                return BuiltinFunction('index_of', lambda item: obj.index(item) if item in obj else -1)

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
            if member == 'contains' or member == 'يحتوي':
                return BuiltinFunction('contains', lambda sub: sub in obj)
            if member == 'replace' or member == 'استبدل':
                return BuiltinFunction('replace', lambda old, new: obj.replace(old, new))
            if member == 'split' or member == 'قسم':
                return BuiltinFunction('split', lambda sep: obj.split(sep))

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
        if isinstance(value, dict):
            parts = []
            for k, v in value.items():
                parts.append(f"{self.opal_to_string(k)}: {self.opal_to_string(v)}")
            return '{' + ', '.join(parts) + '}'
        if isinstance(value, OpalFunction):
            return f"<function {value.name}>"
        if isinstance(value, BuiltinFunction):
            return f"<builtin {value.name}>"
        if isinstance(value, OpalClass):
            return f"<class {value.name}>"
        if isinstance(value, OpalInstance):
            # Check for __str or toString method
            str_method = value.opal_class.find_method("__str") or \
                         value.opal_class.find_method("toString") or \
                         value.opal_class.find_method("to_string")
            if str_method is not None:
                str_method.interpreter = self
                result = self.call_method(str_method, value, [])
                if isinstance(result, str):
                    return result
            return f"<{value.opal_class.name} instance>"
        return str(value)
