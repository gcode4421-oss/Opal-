#!/bin/bash
# Test install_termux.sh in simulated limited environment
# اختبار install_termux.sh في بيئة محدودة محاكاة

set -e

echo "=========================================="
echo "  Simulating Termux installation"
echo "  محاكاة تثبيت Termux"
echo "=========================================="

# Create clean test environment
TEST_HOME="/tmp/opal_termux_test"
rm -rf "$TEST_HOME"
mkdir -p "$TEST_HOME/usr/bin"  # simulated $PREFIX/bin
mkdir -p "$TEST_HOME/.local/bin"

# Set environment to simulate Termux
export HOME="$TEST_HOME"
export PREFIX="$TEST_HOME/usr"
export PATH="$TEST_HOME/usr/bin:$TEST_HOME/.local/bin:/usr/bin:/bin"

# Pre-install python3 in simulated PREFIX (symlink to system python3)
ln -sf "$(which python3)" "$TEST_HOME/usr/bin/python3"
ln -sf "$(which python3)" "$TEST_HOME/usr/bin/python"
ln -sf "$(which git)" "$TEST_HOME/usr/bin/git"

# Make sure we have pip
python3 -m pip --version >/dev/null 2>&1 || {
    echo "Setup error: pip not available"
    exit 1
}

echo ""
echo "=== Running install_termux.sh ==="
echo ""

# Run the actual install script
bash /home/z/my-project/download/opal/install_termux.sh

echo ""
echo "=== Post-install verification ==="
echo ""

# Test 1: Check wrapper exists
if [ -f "$TEST_HOME/.local/bin/opal" ]; then
    echo "PASS: Wrapper script exists"
else
    echo "FAIL: Wrapper script not found"
    exit 1
fi

# Test 2: Check wrapper is executable
if [ -x "$TEST_HOME/.local/bin/opal" ]; then
    echo "PASS: Wrapper is executable"
else
    echo "FAIL: Wrapper is not executable"
    exit 1
fi

# Test 3: Check wrapper shebang
WRAPPER_SHEBANG=$(head -1 "$TEST_HOME/.local/bin/opal")
if [[ "$WRAPPER_SHEBANG" == "#!/bin/bash" ]]; then
    echo "PASS: Wrapper has bash shebang"
else
    echo "FAIL: Wrong shebang: $WRAPPER_SHEBANG"
    exit 1
fi

# Test 4: Check no CRLF in wrapper
if file "$TEST_HOME/.local/bin/opal" | grep -q CRLF; then
    echo "FAIL: Wrapper has CRLF line endings"
    exit 1
else
    echo "PASS: Wrapper has LF line endings"
fi

# Test 5: Check main.py is executable
if [ -x "$TEST_HOME/opal/opal/main.py" ]; then
    echo "PASS: main.py is executable"
else
    echo "FAIL: main.py is not executable"
    exit 1
fi

# Test 6: Check main.py shebang
MAIN_SHEBANG=$(head -1 "$TEST_HOME/opal/opal/main.py")
if [[ "$MAIN_SHEBANG" == "#!/usr/bin/env python3" ]]; then
    echo "PASS: main.py has correct shebang"
else
    echo "FAIL: Wrong shebang: $MAIN_SHEBANG"
    exit 1
fi

# Test 7: Actually run opal --version
echo ""
echo "=== Running opal commands ==="
VERSION_OUTPUT=$("$TEST_HOME/.local/bin/opal" --version 2>&1)
if echo "$VERSION_OUTPUT" | grep -q "Opal"; then
    echo "PASS: opal --version works: $VERSION_OUTPUT"
else
    echo "FAIL: opal --version failed: $VERSION_OUTPUT"
    exit 1
fi

# Test 8: Run a test file
TEST_FILE="$TEST_HOME/test.op"
echo 'echo "Hello from Termux test!"' > "$TEST_FILE"
echo 'var x = 5' >> "$TEST_FILE"
echo 'var y = 10' >> "$TEST_FILE"
echo 'echo "Sum:", x + y' >> "$TEST_FILE"

FILE_OUTPUT=$("$TEST_HOME/.local/bin/opal" "$TEST_FILE" 2>&1)
if echo "$FILE_OUTPUT" | grep -q "Sum: 15"; then
    echo "PASS: opal test.op works"
    echo "  Output: $FILE_OUTPUT"
else
    echo "FAIL: opal test.op failed"
    echo "  Output: $FILE_OUTPUT"
    exit 1
fi

# Test 9: Test Arabic support
echo 'اطبع "مرحبا من تيرمكس"' > "$TEST_FILE"
ARABIC_OUTPUT=$("$TEST_HOME/.local/bin/opal" "$TEST_FILE" 2>&1)
if echo "$ARABIC_OUTPUT" | grep -q "مرحبا"; then
    echo "PASS: Arabic support works"
else
    echo "FAIL: Arabic support failed"
    exit 1
fi

# Test 10: Test compile-c
echo 'echo "Hello C!"' > "$TEST_FILE"
COMPILE_OUTPUT=$("$TEST_HOME/.local/bin/opal" "$TEST_FILE" --compile-c -o "$TEST_FILE.c" 2>&1)
if [ -f "$TEST_FILE.c" ] && grep -q "main" "$TEST_FILE.c"; then
    echo "PASS: --compile-c works"
else
    echo "FAIL: --compile-c failed: $COMPILE_OUTPUT"
    exit 1
fi

# Cleanup
rm -rf "$TEST_HOME"

echo ""
echo "=========================================="
echo "  ALL INSTALLATION TESTS PASSED!"
echo "  كل اختبارات التثبيت نجحت!"
echo "=========================================="
