#!/bin/bash
set -euo pipefail

echo "Generating Python bindings for macOS ARM64 (Apple Silicon)..."

# Get absolute path to this script's directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Navigate to CDK repository
CDK_PATH="$PROJECT_DIR/../cdk"
if [ ! -d "$CDK_PATH" ]; then
    echo "Error: CDK repository not found at $CDK_PATH"
    exit 1
fi

# Convert to absolute path
CDK_PATH="$(cd "$CDK_PATH" && pwd)"

# Set Rust target
TARGET="aarch64-apple-darwin"
echo "Adding Rust target: $TARGET"
rustup target add $TARGET

# Build cdk-ffi with postgres support
echo "Building cdk-ffi for $TARGET..."
cd "$CDK_PATH/crates/cdk-ffi"
cargo build --profile release-smaller --target $TARGET --features postgres

# Generate Python bindings
echo "Generating Python bindings..."
LIB_PATH="$CDK_PATH/target/$TARGET/release-smaller/libcdk_ffi.dylib"
if [ ! -f "$LIB_PATH" ]; then
    echo "Error: Library not found at $LIB_PATH"
    exit 1
fi

OUT_DIR="$PROJECT_DIR/src/cdk"
cargo run --bin uniffi-bindgen generate \
    --library "$LIB_PATH" \
    --language python \
    --out-dir "$OUT_DIR"

# Copy the native library
echo "Copying native library..."
cp "$LIB_PATH" "$OUT_DIR/"

# Rename cdk_ffi.py to cdk.py
if [ -f "$OUT_DIR/cdk_ffi.py" ]; then
    mv "$OUT_DIR/cdk_ffi.py" "$OUT_DIR/cdk.py"
fi

echo "✓ Python bindings generated successfully for macOS ARM64"
echo "✓ Files created:"
echo "  - src/cdk/cdk.py"
echo "  - src/cdk/libcdk_ffi.dylib"
