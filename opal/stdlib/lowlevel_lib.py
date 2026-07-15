"""
Opal Standard Library - Low-Level Types / الأنواع منخفضة المستوى

Low-level types and memory operations for systems programming.
أنواع منخفضة المستوى وعمليات ذاكرة لبرمجة الأنظمة

This module provides:
- Fixed-size integer types (int8, int16, int32, int64, uint8, etc.)
- Byte arrays
- Pointer-like references (simulated)
- Bit operations
- Memory buffer operations

يوفر هذا الموديول:
- أنواع أعداد صحيحة بحجم ثابت
- مصفوفات بايتات
- مراجع شبيهة بالمؤشرات
- عمليات البت
- عمليات مخازن الذاكرة

NOTE: These are simulated in Python for safety. For true OS development,
use the C transpiler (opal --compile-c file.op) to generate C code.
ملاحظة: هذه محاكاة في بايثون للأمان. لتطوير أنظمة حقيقية، استخدم مولّد C.
"""

import struct as _struct
import ctypes as _ctypes


def get_module():
    """إرجاع دوال الأنواع المنخفضة / Return low-level types module"""
    return {
        # Fixed-size integer types / أنواع صحيحة بحجم ثابت
        'int8': lambda x: _ctypes.c_int8(int(x)).value,
        'int16': lambda x: _ctypes.c_int16(int(x)).value,
        'int32': lambda x: _ctypes.c_int32(int(x)).value,
        'int64': lambda x: _ctypes.c_int64(int(x)).value,
        'uint8': lambda x: _ctypes.c_uint8(int(x)).value,
        'uint16': lambda x: _ctypes.c_uint16(int(x)).value,
        'uint32': lambda x: _ctypes.c_uint32(int(x)).value,
        'uint64': lambda x: _ctypes.c_uint64(int(x)).value,

        # Float types / أنواع عشرية
        'float32': lambda x: _struct.unpack('f', _struct.pack('f', float(x)))[0],
        'float64': lambda x: float(x),

        # Byte type / نوع البايت
        'byte': lambda x: int(x) & 0xFF,
        'بايت': lambda x: int(x) & 0xFF,

        # Byte array / مصفوفة بايتات
        'bytes': _make_bytes,
        'بايتات': _make_bytes,
        'bytearray': _make_bytearray,
        'مصفوفة_بايتات': _make_bytearray,

        # Bit operations / عمليات البت
        'bit_and': lambda a, b: int(a) & int(b),
        'bit_or': lambda a, b: int(a) | int(b),
        'bit_xor': lambda a, b: int(a) ^ int(b),
        'bit_not': lambda a: ~int(a),
        'shift_left': lambda a, n: int(a) << int(n),
        'shift_right': lambda a, n: int(a) >> int(n),
        'bit_and_و': lambda a, b: int(a) & int(b),
        'bit_or_أو': lambda a, b: int(a) | int(b),

        # Memory buffer / مخزن الذاكرة
        'buffer': _make_buffer,
        'مخزن': _make_buffer,
        'alloc': _alloc,
        'حجز': _alloc,

        # Type sizes / أحجام الأنواع
        'sizeof': _sizeof,
        'حجم_النوع': _sizeof,
        'size_of': _sizeof,

        # Conversion / تحويل
        'to_bytes': _to_bytes,
        'إلى_بايتات': _to_bytes,
        'from_bytes': _from_bytes,
        'من_بايتات': _from_bytes,

        # Pointer-like reference (simulated) / مرجع شبيه بالمؤشر (محاكاة)
        'ref': _make_ref,
        'مرجع': _make_ref,
        'deref': _deref,
        'تحليلة': _deref,

        # Constants / ثوابت
        'INT8_MIN': -128,
        'INT8_MAX': 127,
        'INT16_MIN': -32768,
        'INT16_MAX': 32767,
        'INT32_MIN': -2147483648,
        'INT32_MAX': 2147483647,
        'UINT8_MAX': 255,
        'UINT16_MAX': 65535,
        'UINT32_MAX': 4294967295,
        'UINT64_MAX': 18446744073709551615,
    }


# ==============================================================
# Byte array implementation / تنفيذ مصفوفة البايتات
# ==============================================================

class OpalBytes:
    """مصفوفة بايتات / Byte array"""

    def __init__(self, size_or_data):
        if isinstance(size_or_data, int):
            self.data = bytearray(size_or_data)
        elif isinstance(size_or_data, (list, tuple)):
            self.data = bytearray(int(x) & 0xFF for x in size_or_data)
        elif isinstance(size_or_data, str):
            self.data = bytearray(size_or_data, 'utf-8')
        elif isinstance(size_or_data, (bytes, bytearray)):
            self.data = bytearray(size_or_data)
        else:
            self.data = bytearray()

    def __getitem__(self, idx):
        if isinstance(idx, slice):
            return OpalBytes(self.data[idx])
        return self.data[idx]

    def __setitem__(self, idx, value):
        self.data[idx] = int(value) & 0xFF

    def __len__(self):
        return len(self.data)

    def __repr__(self):
        return f"<bytes size={len(self.data)}>"

    def to_string(self, encoding='utf-8'):
        """تحويل إلى نص / Convert to string"""
        try:
            return self.data.decode(encoding)
        except Exception:
            return ""

    def to_list(self):
        """تحويل إلى قائمة / Convert to list"""
        return list(self.data)

    def append(self, byte):
        """إضافة بايت / Append a byte"""
        self.data.append(int(byte) & 0xFF)

    def extend(self, other):
        """إضافة عدة بايتات / Extend with more bytes"""
        if isinstance(other, OpalBytes):
            self.data.extend(other.data)
        elif isinstance(other, (list, tuple)):
            self.data.extend(int(x) & 0xFF for x in other)


# ==============================================================
# Buffer implementation / تنفيذ المخزن
# ==============================================================

class OpalBuffer:
    """مخزن ذاكرة / Memory buffer"""

    def __init__(self, size):
        self.size = size
        self.data = bytearray(size)
        self.position = 0

    def write(self, value, offset=None):
        """كتابة قيمة / Write a value"""
        if offset is None:
            offset = self.position

        if isinstance(value, int):
            # Write as 4-byte int / كتابة كعدد 4 بايت
            packed = _struct.pack('<i', value & 0xFFFFFFFF)
            for i, b in enumerate(packed):
                if offset + i < self.size:
                    self.data[offset + i] = b
            self.position = offset + len(packed)
        elif isinstance(value, str):
            encoded = value.encode('utf-8')
            for i, b in enumerate(encoded):
                if offset + i < self.size:
                    self.data[offset + i] = b
            self.position = offset + len(encoded)
        elif isinstance(value, (list, tuple)):
            for i, v in enumerate(value):
                if offset + i < self.size:
                    self.data[offset + i] = int(v) & 0xFF
            self.position = offset + len(value)

    def read(self, offset, length):
        """قراءة بايتات / Read bytes"""
        result = []
        for i in range(length):
            if offset + i < self.size:
                result.append(self.data[offset + i])
            else:
                result.append(0)
        return result

    def read_int(self, offset):
        """قراءة عدد صحيح / Read an integer"""
        if offset + 4 <= self.size:
            return _struct.unpack('<i', bytes(self.data[offset:offset+4]))[0]
        return 0

    def read_string(self, offset, length):
        """قراءة نص / Read a string"""
        try:
            return bytes(self.data[offset:offset+length]).decode('utf-8')
        except Exception:
            return ""

    def clear(self):
        """مسح المخزن / Clear buffer"""
        self.data = bytearray(self.size)
        self.position = 0

    def __getitem__(self, idx):
        return self.data[idx]

    def __setitem__(self, idx, value):
        self.data[idx] = int(value) & 0xFF

    def __len__(self):
        return self.size

    def __repr__(self):
        return f"<buffer size={self.size}>"


# ==============================================================
# Reference (simulated pointer) / مرجع (محاكاة مؤشر)
# ==============================================================

class OpalRef:
    """مرجع شبيه بالمؤشر / Pointer-like reference"""

    def __init__(self, value=None):
        self.value = value

    def get(self):
        """الحصول على القيمة / Get value"""
        return self.value

    def set(self, value):
        """تعيين القيمة / Set value"""
        self.value = value

    def __repr__(self):
        return f"<ref value={self.value!r}>"


# ==============================================================
# Helper functions / دوال مساعدة
# ==============================================================

def _make_bytes(size_or_data):
    """إنشاء مصفوفة بايتات / Create byte array"""
    return OpalBytes(size_or_data)


def _make_bytearray(size_or_data):
    """إنشاء مصفوفة بايتات قابلة للتعديل / Create mutable byte array"""
    return OpalBytes(size_or_data)


def _make_buffer(size):
    """إنشاء مخزن ذاكرة / Create memory buffer"""
    return OpalBuffer(int(size))


def _alloc(size, init_value=0):
    """حجز ذاكرة وتعبئتها / Allocate memory"""
    buf = OpalBuffer(int(size))
    if init_value != 0:
        for i in range(int(size)):
            buf.data[i] = int(init_value) & 0xFF
    return buf


def _sizeof(type_name):
    """حجم نوع بالبايت / Size of a type in bytes"""
    sizes = {
        'int8': 1, 'uint8': 1, 'byte': 1,
        'int16': 2, 'uint16': 2,
        'int32': 4, 'uint32': 4,
        'int64': 8, 'uint64': 8,
        'float32': 4, 'float64': 8,
        'pointer': 8, 'ptr': 8,
    }
    return sizes.get(str(type_name).lower(), 0)


def _to_bytes(value, size=4):
    """تحويل عدد إلى بايتات / Convert number to bytes"""
    try:
        if size == 1:
            return OpalBytes([int(value) & 0xFF])
        elif size == 2:
            return OpalBytes(list(_struct.pack('<H', int(value) & 0xFFFF)))
        elif size == 4:
            return OpalBytes(list(_struct.pack('<I', int(value) & 0xFFFFFFFF)))
        elif size == 8:
            return OpalBytes(list(_struct.pack('<Q', int(value) & 0xFFFFFFFFFFFFFFFF)))
    except Exception:
        return OpalBytes(0)
    return OpalBytes(0)


def _from_bytes(byte_list):
    """تحويل بايتات إلى عدد / Convert bytes to number"""
    try:
        if isinstance(byte_list, OpalBytes):
            byte_list = list(byte_list.data)
        elif isinstance(byte_list, (bytes, bytearray)):
            byte_list = list(byte_list)

        size = len(byte_list)
        if size == 1:
            return byte_list[0]
        elif size == 2:
            return _struct.unpack('<H', bytes(byte_list))[0]
        elif size == 4:
            return _struct.unpack('<I', bytes(byte_list))[0]
        elif size == 8:
            return _struct.unpack('<Q', bytes(byte_list))[0]
        else:
            # Convert as big-endian number / تحويل كرقم big-endian
            result = 0
            for b in byte_list:
                result = (result << 8) | (b & 0xFF)
            return result
    except Exception:
        return 0


def _make_ref(value=None):
    """إنشاء مرجع / Create a reference"""
    return OpalRef(value)


def _deref(ref):
    """تحليل مرجع / Dereference a reference"""
    if isinstance(ref, OpalRef):
        return ref.value
    return ref
