#!/bin/bash
set -euo pipefail

echo "Generating Python bindings for Linux ARM64 (Native)..."

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

# Detect current architecture
CURRENT_ARCH=$(uname -m)
echo "Current architecture: $CURRENT_ARCH"

# Set Rust target
TARGET="aarch64-unknown-linux-gnu"
echo "Adding Rust target: $TARGET"
rustup target add $TARGET

# Build cdk-ffi
echo "Building cdk-ffi for $TARGET..."
cd $CDK_PATH/crates/cdk-ffi
cargo build --profile release-smaller --target $TARGET

# Generate Python bindings
echo "Generating Python bindings..."
LIB_PATH="../../target/$TARGET/release-smaller/libcdk_ffi.so"
if [ ! -f "$LIB_PATH" ]; then
    echo "Error: Library not found at $LIB_PATH"
    exit 1
fi

# When running natively on aarch64, use the native target for uniffi-bindgen
if [ "$CURRENT_ARCH" = "aarch64" ]; then
    echo "Running uniffi-bindgen natively on ARM64"
    cargo run --target aarch64-unknown-linux-gnu --bin uniffi-bindgen generate \
        --library $LIB_PATH \
        --language python \
        --out-dir ../../cdk-python/src/cdk/
else
    echo "Running uniffi-bindgen with cross-compilation from $CURRENT_ARCH"
    cargo run --target x86_64-unknown-linux-gnu --bin uniffi-bindgen generate \
        --library $LIB_PATH \
        --language python \
        --out-dir ../../cdk-python/src/cdk/
fi

# Copy the native library
echo "Copying native library..."
cd -
cp $CDK_PATH/target/$TARGET/release-smaller/libcdk_ffi.so src/cdk/

echo "✓ Python bindings generated successfully for Linux ARM64"
echo "✓ Files created:"
echo "  - src/cdk/cdk.py"
echo "  - src/cdk/libcdk_ffi.so"