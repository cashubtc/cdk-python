#!/bin/bash
set -euo pipefail

echo "Generating Python bindings for macOS ARM64 (Apple Silicon)..."

# Get absolute path to this script's directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Navigate to CDK repository (check both ./cdk for CI and ../cdk for local dev)
CDK_PATH="$PROJECT_DIR/cdk"
if [ ! -d "$CDK_PATH" ]; then
    CDK_PATH="$PROJECT_DIR/../cdk"
    if [ ! -d "$CDK_PATH" ]; then
        echo "Error: CDK repository not found at $PROJECT_DIR/cdk or $PROJECT_DIR/../cdk"
        exit 1
    fi
fi

# Convert to absolute path
CDK_PATH="$(cd "$CDK_PATH" && pwd)"
echo "Using CDK at: $CDK_PATH"

# Set Rust target
TARGET="aarch64-apple-darwin"
echo "Adding Rust target: $TARGET"
rustup target add $TARGET

# Build cdk-ffi
echo "Building cdk-ffi for $TARGET..."
cd "$CDK_PATH/crates/cdk-ffi"
cargo build --profile release-smaller --target $TARGET

# Generate Python bindings
echo "Generating Python bindings..."
LIB_PATH="$CDK_PATH/target/$TARGET/release-smaller/libcdk_ffi.dylib"
if [ ! -f "$LIB_PATH" ]; then
    echo "Error: Library not found at $LIB_PATH"
    exit 1
fi

OUT_DIR="$PROJECT_DIR/src/cdk"
# Run uniffi-bindgen on the host architecture
CURRENT_ARCH=$(uname -m)
if [ "$CURRENT_ARCH" = "arm64" ]; then
    UNIFFI_TARGET="aarch64-apple-darwin"
else
    UNIFFI_TARGET="x86_64-apple-darwin"
fi
echo "Running uniffi-bindgen with target: $UNIFFI_TARGET"
cargo run --target $UNIFFI_TARGET --bin uniffi-bindgen generate \
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
