"""
Opal Language - Environment / نظام النطاقات

Manages variable scopes and bindings.
يدير نطاقات المتغيرات وارتباطاتها
"""


class Environment:
    """نطاق المتغيرات / Variable scope environment"""

    def __init__(self, parent=None):
        """إنشاء نطاق جديد / Create a new scope"""
        self.parent = parent    # النطاق الأب / Parent scope
        self.vars = {}          # المتغيرات / Variable bindings
        self.consts = set()     # الثوابت / Constants

    def define(self, name, value, is_const=False):
        """تعريف متغير جديد في هذا النطاق / Define a variable in current scope"""
        self.vars[name] = value
        if is_const:
            self.consts.add(name)

    def get(self, name):
        """الحصول على قيمة متغير / Get a variable value"""
        if name in self.vars:
            return self.vars[name]

        if self.parent is not None:
            return self.parent.get(name)

        raise NameError(
            f"المتغير '{name}' غير معرف - Variable '{name}' is not defined"
        )

    def set(self, name, value):
        """تعديل قيمة متغير موجود / Update an existing variable"""
        # Check if constant in current scope
        if name in self.consts:
            raise RuntimeError(
                f"لا يمكن تعديل الثابت '{name}' - Cannot reassign constant '{name}'"
            )

        if name in self.vars:
            self.vars[name] = value
            return

        if self.parent is not None:
            self.parent.set(name, value)
            return

        raise NameError(
            f"المتغير '{name}' غير معرف - Variable '{name}' is not defined"
        )

    def has(self, name):
        """تحقق من وجود متغير / Check if variable exists"""
        if name in self.vars:
            return True
        if self.parent is not None:
            return self.parent.has(name)
        return False

    def get_const_names(self):
        """الحصول على أسماء الثوابت / Get constant names"""
        all_consts = set(self.consts)
        if self.parent:
            all_consts.update(self.parent.get_const_names())
        return all_consts
