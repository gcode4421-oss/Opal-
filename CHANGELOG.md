# Changelog / سجل التغييرات

All notable changes to Opal Language are documented here.
يتم توثيق كل التغييرات المهمة في لغة أوبال هنا.

## [2.1.0] - 2026-07-15

### Added / مضاف
- **Colors Library** (`colors_lib.py`): Full ANSI color support
  - 16 standard colors (RED, GREEN, BLUE, etc.)
  - 8 bright colors (BRIGHT_RED, BRIGHT_GREEN, etc.)
  - 8 background colors (BG_RED, BG_GREEN, etc.)
  - Text styles (BOLD, ITALIC, UNDERLINE, BLINK, REVERSE)
  - Arabic color names (أحمر، أخضر، أزرق، أصفر، etc.)
  - Additional colors (برتقالي، بنفسجي، نيلي، ذهبي، وردي)
  - RGB color support: `rgb()`, `bg_rgb()`
  - Terminal control: clear_screen, move_cursor
  - Arabic text helpers: `rtl()`, `ltr()`, `bidi()`, `reshape_arabic()`
- **Low-level types** (`lowlevel_lib.py`):
  - Fixed-size integers: int8, int16, int32, int64, uint8-64
  - Byte arrays (OpalBytes)
  - Memory buffers (OpalBuffer)
  - References (OpalRef - simulated pointers)
  - Bit operations (bit_and, bit_or, bit_xor, shifts)
  - Type sizes (sizeof)
  - Type constants (INT8_MAX, etc.)
- **C Transpiler** (`c_transpiler.py`):
  - Transpiles Opal code to C
  - Dynamic Value type with union
  - Supports: functions, recursion, if/else, while, for, all operators
  - String concatenation with type coercion
  - Command: `opal file.op --compile-c -o output.c`
- **CLI options**:
  - `--color=always/never/auto` for color control
  - `--compile-c` / `--cc` for C transpilation
  - `-o` for output file specification
- **Examples**:
  - `examples/preview/colors_demo.op` - Colors showcase (English)
  - `examples/preview/arabic_colors_demo.op` - Colors + Arabic
  - `examples/lowlevel_demo.op` - Low-level types
- **Test suites**: 9 test files covering all features
- **Install scripts**: Termux, Linux/macOS, Windows, Universal

### Changed / تغيير
- `opal` command now works from any directory (system-wide symlink)
- Dynamic color support detection (respects FORCE_COLOR, NO_COLOR, TERM)
- Improved Arabic support with bidi and reshaping helpers

### Fixed / إصلاح
- Parser: Arabic catch variable rejected (خطأ is FALSE keyword)
  - Fixed by allowing FALSE/TRUE/NULL as catch variable names
- CLI entry points: All have correct `#!/usr/bin/env python3` shebangs
- All files use LF line endings (no CRLF)
- All entry files have executable permissions

## [2.0.0] - 2026-07-15

### Added / مضاف
- **Object-Oriented Programming (OOP)**: classes, inheritance, `this`, `new`
- **Error Handling**: `try/catch/finally` and `throw`
- **Lambda Functions**: `fn(x) -> x * 2`
- **Dictionaries**: `{"key": value}`
- **Switch Statements**: `switch/case/default`
- **Ternary Operator**: `cond ? a : b`
- **Compound Assignment**: `+=`, `-=`, `*=`, `/=`
- **Do-Until Loop**: `do { } until (cond)`
- **Block Comments**: `/* ... */`
- **Standard Libraries**:
  - JSON: parse and stringify
  - HTTP: GET/POST web requests
  - File: read/write/copy/move
  - Time: time and date functions
  - System: OS information

## [1.0.0] - 2026-07-15

### Added / مضاف
- Initial release of Opal Language
- Arabic and English keyword support
- Variables, constants, functions
- Control flow: if/elif/else, while, for
- Lists, strings, numbers, booleans
- Standard libraries: math, strings, lists, io, types
- Import system: `import` and `from...import`
- REPL mode
- CLI: `opal file.op`
