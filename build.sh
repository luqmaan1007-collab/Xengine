#!/bin/bash
# Simple Xengine Build Script

echo "╔═══════════════════════════════════════╗"
echo "║   Building Xengine Game Engine        ║"
echo "╚═══════════════════════════════════════╝"
echo ""

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Create build directory
echo "[1/4] Creating build directory..."
mkdir -p build
cd build

# Run CMake
echo "[2/4] Running CMake..."
cmake .. -DCMAKE_BUILD_TYPE=Release

if [ $? -ne 0 ]; then
    echo "❌ CMake failed!"
    exit 1
fi

# Build
echo "[3/4] Building..."
cmake --build . --config Release

if [ $? -ne 0 ]; then
    echo "❌ Build failed!"
    exit 1
fi

# Run demo
echo "[4/4] Running demo..."
echo ""
./xengine_demo

echo ""
echo "╔═══════════════════════════════════════╗"
echo "║   ✓ Build Complete!                    ║"
echo "╚═══════════════════════════════════════╝"
echo ""
echo "Executable: build/xengine_demo"
echo "Library: build/libxengine.a"
echo ""
