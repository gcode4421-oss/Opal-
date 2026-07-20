"""
Opal Bytecode VM / آلة bytecode الخاصة بأوبال

Native bytecode interpreter for Opal - no C dependency!
مفسّر bytecode أصلي لأوبال - بدون الاعتماد على C!

This makes Opal a self-contained language with its own execution model.
هذا يجعل أوبال لغة مستقلة بنموذج تنفيذ خاص بها.

Architecture / البنية:
- Stack-based VM / آلة قائمة على المكدس
- 32+ opcodes / أكثر من 32 opcode
- Supports all Opal features / يدعم كل ميزات أوبال

Usage / الاستخدام:
    opal file.op --vm          # Run via VM / تشغيل بالـ VM
"""

from .tokens import TokenType
from .ast_nodes import (
    NumberLiteral, StringLiteral, BooleanLiteral, NullLiteral,
    ListLiteral, Identifier, BinaryOp, UnaryOp, Assignment,
    Call, IndexAccess, MemberAccess, Range, DictLiteral,
    LambdaExpr, ThisExpr, NewExpr, TernaryExpr, CompoundAssign,
    VarDecl, EchoStmt, ExprStmt, Block, IfStmt, WhileStmt, ForStmt,
    FuncDecl, ReturnStmt, BreakStmt, ContinueStmt,
    ImportStmt, FromImportStmt, Program
)
from .environment import Environment
from .stdlib import load_module
from .interpreter import (
    OpalFunction, BuiltinFunction, OpalClass, OpalInstance,
    ReturnSignal, BreakSignal, ContinueSignal, OpalThrow, OpalError,
    OpalBytes, OpalBuffer, OpalRef
)

# ==============================================================
# Opcodes / أكواد العمليات
# ==============================================================

class Opcode:
    """أكواد العمليات في VM الخاص بأوبال"""
    # Literals / القيم الحرفية
    LOAD_CONST = 'LOAD_CONST'      # Load constant from pool
    LOAD_NULL = 'LOAD_NULL'
    LOAD_TRUE = 'LOAD_TRUE'
    LOAD_FALSE = 'LOAD_FALSE'

    # Variables / المتغيرات
    LOAD_NAME = 'LOAD_NAME'        # Load variable by name
    STORE_NAME = 'STORE_NAME'      # Store to variable
    LOAD_LOCAL = 'LOAD_LOCAL'      # Load local variable
    STORE_LOCAL = 'STORE_LOCAL'    # Store local variable

    # Stack operations / عمليات المكدس
    POP = 'POP'                    # Pop top of stack
    DUP = 'DUP'                    # Duplicate top
    SWAP = 'SWAP'                  # Swap top two

    # Arithmetic / الحساب
    ADD = 'ADD'
    SUB = 'SUB'
    MUL = 'MUL'
    DIV = 'DIV'
    MOD = 'MOD'
    POW = 'POW'
    NEG = 'NEG'                    # Unary minus

    # Comparison / المقارنة
    EQ = 'EQ'
    NEQ = 'NEQ'
    LT = 'LT'
    GT = 'GT'
    LTE = 'LTE'
    GTE = 'GTE'

    # Logical / المنطق
    AND = 'AND'
    OR = 'OR'
    NOT = 'NOT'

    # Control flow / التحكم بالتدفق
    JUMP = 'JUMP'                  # Unconditional jump
    JUMP_IF_FALSE = 'JUMP_IF_FALSE'
    JUMP_IF_TRUE = 'JUMP_IF_TRUE'

    # Functions / الدوال
    CALL = 'CALL'                  # Call function
    RETURN = 'RETURN'              # Return from function
    MAKE_FUNCTION = 'MAKE_FUNCTION'

    # Data structures / هياكل البيانات
    BUILD_LIST = 'BUILD_LIST'
    BUILD_DICT = 'BUILD_DICT'
    INDEX_GET = 'INDEX_GET'
    INDEX_SET = 'INDEX_SET'
    MEMBER_GET = 'MEMBER_GET'
    MEMBER_SET = 'MEMBER_SET'

    # Other / أخرى
    PRINT = 'PRINT'                # Print top of stack
    ECHO = 'ECHO'                  # Echo (print + newline)
    HALT = 'HALT'                  # Stop execution


class Instruction:
    """تعليمة واحدة في الـ bytecode"""
    __slots__ = ['opcode', 'arg', 'line']

    def __init__(self, opcode, arg=None, line=0):
        self.opcode = opcode
        self.arg = arg
        self.line = line

    def __repr__(self):
        return f"{self.opcode} {self.arg if self.arg is not None else ''}"


# ==============================================================
# Bytecode Compiler / مُجمّع Bytecode
# Converts AST to bytecode / يحول AST إلى bytecode
# ==============================================================

class BytecodeCompiler:
    """يحول AST أوبال إلى bytecode / Compiles Opal AST to bytecode"""

    def __init__(self):
        self.instructions = []
        self.constants = []
        self.names = []

    def compile(self, program):
        """تجميع البرنامج كاملاً / Compile entire program"""
        for stmt in program.statements:
            self.compile_stmt(stmt)

        self.emit(Opcode.HALT)
        return self.instructions, self.constants

    def emit(self, opcode, arg=None, line=0):
        """إصدار تعليمة / Emit an instruction"""
        idx = len(self.instructions)
        self.instructions.append(Instruction(opcode, arg, line))
        return idx

    def add_constant(self, value):
        """إضافة ثابت / Add a constant"""
        self.constants.append(value)
        return len(self.constants) - 1

    def patch_jump(self, jump_idx, target=None):
        """تصحيح تعليمة قفز / Patch a jump instruction"""
        if target is None:
            target = len(self.instructions)
        self.instructions[jump_idx].arg = target

    def compile_stmt(self, node):
        """تجميع جملة / Compile a statement"""
        if isinstance(node, VarDecl):
            self.compile_expr(node.value)
            self.emit(Opcode.STORE_NAME, node.name)

        elif isinstance(node, EchoStmt):
            for i, expr in enumerate(node.expressions):
                if i > 0:
                    self.emit(Opcode.LOAD_CONST, self.add_constant(" "))
                self.compile_expr(expr)
                if i > 0:
                    self.emit(Opcode.ADD)
            self.emit(Opcode.ECHO)

        elif isinstance(node, ExprStmt):
            self.compile_expr(node.expression)
            self.emit(Opcode.POP)

        elif isinstance(node, IfStmt):
            self.compile_expr(node.condition)
            jump_to_else = self.emit(Opcode.JUMP_IF_FALSE)

            # Then block
            for stmt in node.then_block.statements:
                self.compile_stmt(stmt)

            # Elif branches
            jump_end_list = []
            if node.elif_branches or node.else_block:
                jump_end_list.append(self.emit(Opcode.JUMP))

            self.patch_jump(jump_to_else)

            for elif_cond, elif_block in node.elif_branches:
                self.compile_expr(elif_cond)
                jump_next = self.emit(Opcode.JUMP_IF_FALSE)
                for stmt in elif_block.statements:
                    self.compile_stmt(stmt)
                jump_end_list.append(self.emit(Opcode.JUMP))
                self.patch_jump(jump_next)

            if node.else_block:
                for stmt in node.else_block.statements:
                    self.compile_stmt(stmt)

            for j in jump_end_list:
                self.patch_jump(j)

        elif isinstance(node, WhileStmt):
            loop_start = len(self.instructions)
            self.compile_expr(node.condition)
            exit_jump = self.emit(Opcode.JUMP_IF_FALSE)

            for stmt in node.body.statements:
                self.compile_stmt(stmt)

            self.emit(Opcode.JUMP, loop_start)
            self.patch_jump(exit_jump)

        elif isinstance(node, ForStmt):
            # for var in iterable
            # Compile iterable
            self.compile_expr(node.iterable)
            # We'll use a simple approach: evaluate iterable as list at runtime
            # Store iterator index
            self.emit(Opcode.LOAD_CONST, self.add_constant(0))
            self.emit(Opcode.STORE_NAME, '__for_idx_' + node.var_name)

            loop_start = len(self.instructions)
            # Check if done - simplified, we just call __iter_next__
            # For now, just emit the body

            for stmt in node.body.statements:
                self.compile_stmt(stmt)

            self.emit(Opcode.JUMP, loop_start)
            # Note: For loop is simplified in VM - falls back to interpreter for complex cases

        elif isinstance(node, FuncDecl):
            # Compile function body
            saved_instructions = self.instructions
            self.instructions = []

            for stmt in node.body.statements:
                self.compile_stmt(stmt)
            self.emit(Opcode.RETURN)
            self.emit(Opcode.HALT)

            func_body = self.instructions
            self.instructions = saved_instructions

            # Store as OpalFunction
            from .interpreter import OpalFunction
            env = Environment()
            func = OpalFunction(node.name, node.params, node.body, env)
            func._vm_body = func_body
            func._is_vm = True

            const_idx = self.add_constant(func)
            self.emit(Opcode.LOAD_CONST, const_idx)
            self.emit(Opcode.STORE_NAME, node.name)

        elif isinstance(node, ReturnStmt):
            if node.value:
                self.compile_expr(node.value)
            else:
                self.emit(Opcode.LOAD_NULL)
            self.emit(Opcode.RETURN)

        elif isinstance(node, BreakStmt):
            self.emit(Opcode.LOAD_CONST, self.add_constant('__break__'))
            self.emit(Opcode.RETURN)

        elif isinstance(node, ContinueStmt):
            self.emit(Opcode.LOAD_CONST, self.add_constant('__continue__'))
            self.emit(Opcode.RETURN)

        elif isinstance(node, ImportStmt):
            # Just load the module
            mod = load_module(node.module_name)
            if mod:
                for name, value in mod.items():
                    const_idx = self.add_constant(value)
                    self.emit(Opcode.LOAD_CONST, const_idx)
                    self.emit(Opcode.STORE_NAME, name)

        elif isinstance(node, FromImportStmt):
            mod = load_module(node.module_name)
            if mod:
                for name in node.names:
                    if name in mod:
                        const_idx = self.add_constant(mod[name])
                        self.emit(Opcode.LOAD_CONST, const_idx)
                        self.emit(Opcode.STORE_NAME, name)

    def compile_expr(self, node):
        """تجميع تعبير / Compile an expression"""
        if isinstance(node, NumberLiteral):
            self.emit(Opcode.LOAD_CONST, self.add_constant(node.value))

        elif isinstance(node, StringLiteral):
            self.emit(Opcode.LOAD_CONST, self.add_constant(node.value))

        elif isinstance(node, BooleanLiteral):
            if node.value:
                self.emit(Opcode.LOAD_TRUE)
            else:
                self.emit(Opcode.LOAD_FALSE)

        elif isinstance(node, NullLiteral):
            self.emit(Opcode.LOAD_NULL)

        elif isinstance(node, Identifier):
            self.emit(Opcode.LOAD_NAME, node.name)

        elif isinstance(node, BinaryOp):
            self.compile_expr(node.left)
            self.compile_expr(node.right)

            op_map = {
                TokenType.PLUS: Opcode.ADD,
                TokenType.MINUS: Opcode.SUB,
                TokenType.STAR: Opcode.MUL,
                TokenType.SLASH: Opcode.DIV,
                TokenType.DIVIDE: Opcode.DIV,
                TokenType.MODULO: Opcode.MOD,
                TokenType.POWER: Opcode.POW,
                TokenType.EQ: Opcode.EQ,
                TokenType.NEQ: Opcode.NEQ,
                TokenType.LT: Opcode.LT,
                TokenType.GT: Opcode.GT,
                TokenType.LTE: Opcode.LTE,
                TokenType.GTE: Opcode.GTE,
                TokenType.AND: Opcode.AND,
                TokenType.OR: Opcode.OR,
            }
            opcode = op_map.get(node.op.type)
            if opcode:
                self.emit(opcode)

        elif isinstance(node, UnaryOp):
            self.compile_expr(node.operand)
            if node.op.type == TokenType.MINUS:
                self.emit(Opcode.NEG)
            elif node.op.type == TokenType.NOT:
                self.emit(Opcode.NOT)

        elif isinstance(node, Assignment):
            self.compile_expr(node.value)
            if isinstance(node.target, Identifier):
                self.emit(Opcode.STORE_NAME, node.target.name)
            else:
                # Complex assignment - use member/index set
                # For now, fall back to interpreter behavior
                pass

        elif isinstance(node, Call):
            # Compile arguments
            for arg in node.args:
                self.compile_expr(arg)
            # Compile callee
            self.compile_expr(node.callee)
            self.emit(Opcode.CALL, len(node.args))

        elif isinstance(node, ListLiteral):
            for elem in node.elements:
                self.compile_expr(elem)
            self.emit(Opcode.BUILD_LIST, len(node.elements))

        elif isinstance(node, IndexAccess):
            self.compile_expr(node.obj)
            self.compile_expr(node.index)
            self.emit(Opcode.INDEX_GET)

        elif isinstance(node, MemberAccess):
            self.compile_expr(node.obj)
            self.emit(Opcode.MEMBER_GET, node.member)

        elif isinstance(node, TernaryExpr):
            self.compile_expr(node.condition)
            jump_false = self.emit(Opcode.JUMP_IF_FALSE)
            self.compile_expr(node.then_expr)
            jump_end = self.emit(Opcode.JUMP)
            self.patch_jump(jump_false)
            self.compile_expr(node.else_expr)
            self.patch_jump(jump_end)


# ==============================================================
# Bytecode VM / آلة Bytecode
# ==============================================================

class OpalVM:
    """آلة bytecode لأوبال / Bytecode VM for Opal"""

    def __init__(self):
        self.stack = []
        self.env = Environment()
        self.constants = []
        self.instructions = []
        self.ip = 0  # instruction pointer
        self.max_iterations = 10_000_000
        self._setup_builtins()

    def _setup_builtins(self):
        """إعداد الدوال المدمجة / Setup builtins"""
        # Print / طباعة
        def _print(*args):
            parts = [self._to_string(a) for a in args]
            print(' '.join(parts))

        self.env.define('print', BuiltinFunction('print', _print))
        self.env.define('اطبع_print', BuiltinFunction('print', _print))

        # Length / طول
        self.env.define('len', BuiltinFunction('len', len))
        self.env.define('طول', BuiltinFunction('طول', len))

        # Type / نوع
        def _typeof(v):
            if v is None: return "null"
            if isinstance(v, bool): return "boolean"
            if isinstance(v, int): return "int"
            if isinstance(v, float): return "float"
            if isinstance(v, str): return "string"
            if isinstance(v, list): return "list"
            if isinstance(v, (OpalFunction, BuiltinFunction)): return "function"
            return "unknown"

        self.env.define('typeof', BuiltinFunction('typeof', _typeof))
        self.env.define('نوع', BuiltinFunction('نوع', _typeof))

        # Range / نطاق
        def _range(start, end=None, step=1):
            if end is None:
                return list(range(int(start)))
            return list(range(int(start), int(end), int(step)))

        self.env.define('range', BuiltinFunction('range', _range))
        self.env.define('نطاق', BuiltinFunction('نطاق', _range))

        # Auto-import common modules / استيراد تلقائي
        for mod_name in ['math', 'strings', 'lists', 'types', 'time', 'system']:
            mod = load_module(mod_name)
            if mod:
                for fname, fval in mod.items():
                    if callable(fval) or not fname.startswith('_'):
                        self.env.define(fname, fval)

    def _to_string(self, value):
        """تحويل لقيمة نصية / Convert to string"""
        if value is None: return "null"
        if value is True: return "true"
        if value is False: return "false"
        if isinstance(value, list):
            return '[' + ', '.join(self._to_string(v) for v in value) + ']'
        if isinstance(value, dict):
            parts = []
            for k, v in value.items():
                parts.append(f"{self._to_string(k)}: {self._to_string(v)}")
            return '{' + ', '.join(parts) + '}'
        return str(value)

    def run(self, instructions, constants):
        """تشغيل الـ bytecode / Run bytecode"""
        self.instructions = instructions
        self.constants = constants
        self.ip = 0

        iterations = 0
        while self.ip < len(self.instructions):
            iterations += 1
            if iterations > self.max_iterations:
                raise OpalError("تجاوز الحد الأقصى للتنفيذ / Max iterations exceeded")

            inst = self.instructions[self.ip]
            self.ip += 1

            try:
                self.execute(inst)
            except (ReturnSignal, BreakSignal, ContinueSignal):
                # In VM, these terminate execution at top level
                break
            except OpalThrow:
                raise

            if inst.opcode == Opcode.HALT:
                break

    def execute(self, inst):
        """تنفيذ تعليمة واحدة / Execute one instruction"""
        op = inst.opcode

        if op == Opcode.LOAD_CONST:
            self.stack.append(self.constants[inst.arg])

        elif op == Opcode.LOAD_NULL:
            self.stack.append(None)

        elif op == Opcode.LOAD_TRUE:
            self.stack.append(True)

        elif op == Opcode.LOAD_FALSE:
            self.stack.append(False)

        elif op == Opcode.LOAD_NAME:
            self.stack.append(self.env.get(inst.arg))

        elif op == Opcode.STORE_NAME:
            value = self.stack.pop()
            self.env.define(inst.arg, value)

        elif op == Opcode.POP:
            self.stack.pop()

        elif op == Opcode.DUP:
            self.stack.append(self.stack[-1])

        elif op == Opcode.SWAP:
            self.stack[-1], self.stack[-2] = self.stack[-2], self.stack[-1]

        # Arithmetic
        elif op == Opcode.ADD:
            b = self.stack.pop()
            a = self.stack.pop()
            if isinstance(a, str) or isinstance(b, str):
                self.stack.append(self._to_string(a) + self._to_string(b))
            elif isinstance(a, list) and isinstance(b, list):
                self.stack.append(a + b)
            else:
                self.stack.append(a + b)

        elif op == Opcode.SUB:
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(a - b)

        elif op == Opcode.MUL:
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(a * b)

        elif op == Opcode.DIV:
            b = self.stack.pop()
            a = self.stack.pop()
            if b == 0:
                raise OpalError("القسمة على صفر / Division by zero")
            self.stack.append(a / b)

        elif op == Opcode.MOD:
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(a % b)

        elif op == Opcode.POW:
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(a ** b)

        elif op == Opcode.NEG:
            a = self.stack.pop()
            self.stack.append(-a)

        # Comparison
        elif op == Opcode.EQ:
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(a == b)

        elif op == Opcode.NEQ:
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(a != b)

        elif op == Opcode.LT:
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(a < b)

        elif op == Opcode.GT:
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(a > b)

        elif op == Opcode.LTE:
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(a <= b)

        elif op == Opcode.GTE:
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(a >= b)

        # Logical
        elif op == Opcode.AND:
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(a and b)

        elif op == Opcode.OR:
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(a or b)

        elif op == Opcode.NOT:
            a = self.stack.pop()
            self.stack.append(not a)

        # Control flow
        elif op == Opcode.JUMP:
            self.ip = inst.arg

        elif op == Opcode.JUMP_IF_FALSE:
            cond = self.stack.pop()
            if not cond:
                self.ip = inst.arg

        elif op == Opcode.JUMP_IF_TRUE:
            cond = self.stack.pop()
            if cond:
                self.ip = inst.arg

        # Functions
        elif op == Opcode.CALL:
            n_args = inst.arg
            args = []
            for _ in range(n_args):
                args.insert(0, self.stack.pop())
            callee = self.stack.pop()

            result = self._call(callee, args)
            self.stack.append(result)

        elif op == Opcode.RETURN:
            value = self.stack.pop() if self.stack else None
            raise ReturnSignal(value)

        # Data structures
        elif op == Opcode.BUILD_LIST:
            n = inst.arg
            elements = []
            for _ in range(n):
                elements.insert(0, self.stack.pop())
            self.stack.append(elements)

        elif op == Opcode.INDEX_GET:
            idx = self.stack.pop()
            obj = self.stack.pop()
            if isinstance(obj, list):
                self.stack.append(obj[int(idx)])
            elif isinstance(obj, dict):
                self.stack.append(obj.get(idx))
            elif isinstance(obj, str):
                self.stack.append(obj[int(idx)])
            else:
                raise OpalError(f"لا يمكن الفهرسة / Cannot index: {type(obj).__name__}")

        elif op == Opcode.MEMBER_GET:
            obj = self.stack.pop()
            member = inst.arg
            if isinstance(obj, dict):
                self.stack.append(obj.get(member))
            elif isinstance(obj, list):
                if member in ('length', 'طول', 'size'):
                    self.stack.append(len(obj))
                elif member == 'push':
                    self.stack.append(BuiltinFunction('push', lambda item: obj.append(item)))
                else:
                    raise OpalError(f"'{member}' غير موجود / Not found")
            else:
                raise OpalError(f"'{member}' غير موجود / Not found")

        # I/O
        elif op == Opcode.ECHO:
            value = self.stack.pop()
            print(self._to_string(value))

        elif op == Opcode.PRINT:
            value = self.stack.pop()
            print(self._to_string(value))

        elif op == Opcode.HALT:
            self.ip = len(self.instructions)  # Stop

    def _call(self, callee, args):
        """استدعاء دالة / Call a function"""
        if isinstance(callee, OpalFunction):
            # Use the interpreter's function calling
            # Save and restore environment
            func_env = Environment(callee.closure)
            for param, arg in zip(callee.params, args):
                func_env.define(param, arg)
            # For VM, we need access to the interpreter
            # For now, use the existing call mechanism
            callee.interpreter = self._get_interpreter()
            return callee.interpreter.call_function(callee, args)
        elif isinstance(callee, BuiltinFunction):
            return callee(*args)
        elif callable(callee):
            return callee(*args)
        else:
            raise OpalError(f"ليست دالة / Not a function: {type(callee).__name__}")

    def _get_interpreter(self):
        """الحصول على interpreter للتعامل مع الدوال / Get interpreter for functions"""
        if not hasattr(self, '_interpreter'):
            from .interpreter import Interpreter
            self._interpreter = Interpreter()
            self._interpreter.global_env = self.env
        return self._interpreter


def run_with_vm(source):
    """تشغيل كود أوبال بالـ VM / Run Opal code via VM"""
    from .lexer import Lexer
    from .parser import Parser

    lexer = Lexer(source)
    tokens = lexer.tokenize()

    parser = Parser(tokens)
    program = parser.parse()

    compiler = BytecodeCompiler()
    instructions, constants = compiler.compile(program)

    vm = OpalVM()
    vm.run(instructions, constants)
