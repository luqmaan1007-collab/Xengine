#!/bin/bash
# Xengine Installation Diagnostic Script
# This will show exactly what's failing

set -e  # Exit on error

echo "======================================"
echo "Xengine Installation Diagnostic"
echo "======================================"
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check dependencies
echo "[1/8] Checking dependencies..."
MISSING=""

if ! command_exists cmake; then
    MISSING="${MISSING}cmake "
fi

if ! command_exists ninja; then
    if ! command_exists make; then
        MISSING="${MISSING}ninja/make "
    fi
fi

if ! command_exists python3; then
    MISSING="${MISSING}python3 "
fi

if ! command_exists git; then
    MISSING="${MISSING}git "
fi

if ! command_exists g++; then
    if ! command_exists clang++; then
        MISSING="${MISSING}g++/clang++ "
    fi
fi

if [ -n "$MISSING" ]; then
    echo "ERROR: Missing dependencies: $MISSING"
    echo ""
    echo "Install them with:"
    echo "  Ubuntu/Debian: sudo apt-get install build-essential cmake ninja-build python3 git"
    echo "  macOS: brew install cmake ninja python3 git"
    exit 1
fi

echo "✓ All dependencies found"
echo ""

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
XENGINE_DIR="$(dirname "$SCRIPT_DIR")"

echo "[2/8] Xengine directory: $XENGINE_DIR"
cd "$XENGINE_DIR"
echo ""

# Create build directory
echo "[3/8] Creating build directory..."
mkdir -p build
cd build
echo "✓ Build directory created"
echo ""

# Run CMake (this is where it might fail)
echo "[4/8] Running CMake configuration..."
if command_exists ninja; then
    BUILD_SYSTEM="Ninja"
else
    BUILD_SYSTEM="Unix Makefiles"
fi

echo "Using build system: $BUILD_SYSTEM"

# Try CMake with verbose output
if cmake .. -G "$BUILD_SYSTEM" -DCMAKE_BUILD_TYPE=Release 2>&1 | tee cmake_output.log; then
    echo "✓ CMake configuration successful"
else
    echo ""
    echo "=========================================="
    echo "ERROR: CMake configuration failed!"
    echo "=========================================="
    echo ""
    echo "Last 20 lines of output:"
    tail -20 cmake_output.log
    echo ""
    echo "Full log saved to: build/cmake_output.log"
    echo ""
    echo "Common fixes:"
    echo "1. Missing OpenGL: sudo apt-get install libgl1-mesa-dev"
    echo "2. Missing X11: sudo apt-get install libx11-dev"
    echo "3. Wrong CMake version: sudo apt-get install cmake"
    exit 1
fi
echo ""

# Build
echo "[5/8] Building Xengine..."
if command_exists ninja; then
    if ninja 2>&1 | tee build_output.log; then
        echo "✓ Build successful"
    else
        echo ""
        echo "=========================================="
        echo "ERROR: Build failed!"
        echo "=========================================="
        echo ""
        echo "Last 30 lines of output:"
        tail -30 build_output.log
        echo ""
        echo "Full log saved to: build/build_output.log"
        exit 1
    fi
else
    if make -j$(nproc) 2>&1 | tee build_output.log; then
        echo "✓ Build successful"
    else
        echo ""
        echo "=========================================="
        echo "ERROR: Build failed!"
        echo "=========================================="
        echo ""
        echo "Last 30 lines of output:"
        tail -30 build_output.log
        echo ""
        echo "Full log saved to: build/build_output.log"
        exit 1
    fi
fi
echo ""

# Make CLI tool executable
echo "[6/8] Setting up CLI tools..."
chmod +x ../tools/*.py
echo "✓ CLI tools ready"
echo ""

# Create symlink (optional)
echo "[7/8] Creating xengine command..."
INSTALL_DIR="$HOME/.local/bin"
mkdir -p "$INSTALL_DIR"

cat > "$INSTALL_DIR/xengine" << 'EOF'
#!/bin/bash
XENGINE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
python3 "$XENGINE_ROOT/tools/xengine-cli.py" "$@"
EOF

chmod +x "$INSTALL_DIR/xengine"

# Check if in PATH
if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
    echo ""
    echo "NOTE: Add $INSTALL_DIR to your PATH:"
    echo "  echo 'export PATH=\"\$HOME/.local/bin:\$PATH\"' >> ~/.bashrc"
    echo "  source ~/.bashrc"
fi

echo "✓ xengine command installed"
echo ""

# Test
echo "[8/8] Testing installation..."
if [ -f "libxengine.a" ] || [ -f "xengine" ] || ls *.so >/dev/null 2>&1 || ls *.a >/dev/null 2>&1; then
    echo "✓ Xengine library built successfully"
else
    echo "⚠ Warning: No library files found, but build completed"
fi
echo ""

echo "======================================"
echo "✓ Installation Complete!"
echo "======================================"
echo ""
echo "Next steps:"
echo "  1. Create a new game: xengine create mygame"
echo "  2. Build a game: cd mygame && xengine build"
echo "  3. Run a game: xengine run"
echo ""
echo "For Android APK:"
echo "  xengine build --platform android"
echo ""
echo "Documentation: $XENGINE_DIR/docs/getting-started.md"
echo ""
