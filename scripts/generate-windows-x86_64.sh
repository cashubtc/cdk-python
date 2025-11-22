#!/bin/bash
set -euo pipefail

echo "Generating Python bindings for Windows x86_64..."

# Navigate to CDK repository (check both ./cdk for CI and ../cdk for local dev)
CDK_PATH="./cdk"
if [ ! -d "$CDK_PATH" ]; then
    CDK_PATH="../cdk"
    if [ ! -d "$CDK_PATH" ]; then
        echo "Error: CDK repository not found at ./cdk or ../cdk"
        exit 1
    fi
fi

echo "Using CDK at: $CDK_PATH"

# Set Rust target
TARGET="x86_64-pc-windows-msvc"
echo "Adding Rust target: $TARGET"
rustup target add $TARGET

# Build cdk-ffi
echo "Building cdk-ffi for $TARGET..."
cd $CDK_PATH/crates/cdk-ffi
cargo build --profile release-smaller --target $TARGET

# Generate Python bindings
echo "Generating Python bindings..."
LIB_PATH="../../target/$TARGET/release-smaller/cdk_ffi.dll"
if [ ! -f "$LIB_PATH" ]; then
    echo "Error: Library not found at $LIB_PATH"
    exit 1
fi

# Detect current architecture and use appropriate uniffi-bindgen target
CURRENT_ARCH=$(uname -m)
if [ "$CURRENT_ARCH" = "x86_64" ] || [ "$CURRENT_ARCH" = "AMD64" ]; then
    UNIFFI_TARGET="x86_64-pc-windows-msvc"
elif [ "$CURRENT_ARCH" = "aarch64" ] || [ "$CURRENT_ARCH" = "ARM64" ]; then
    UNIFFI_TARGET="aarch64-pc-windows-msvc"
else
    # Fallback to x86_64 for unknown architectures
    UNIFFI_TARGET="x86_64-pc-windows-msvc"
fi

echo "Running uniffi-bindgen with target: $UNIFFI_TARGET"
cargo run --target $UNIFFI_TARGET --bin uniffi-bindgen generate \
    --library $LIB_PATH \
    --language python \
    --out-dir ../../cdk-python/src/cdk/

# Copy the native library
echo "Copying native library..."
cd -
cp $CDK_PATH/target/$TARGET/release-smaller/cdk_ffi.dll src/cdk/

echo "✓ Python bindings generated successfully for Windows x86_64"
echo "✓ Files created:"
echo "  - src/cdk/cdk.py"
echo "  - src/cdk/cdk_ffi.dll"
