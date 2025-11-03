#!/usr/bin/env just --justfile

# Default recipe to display help information
default:
    @just --list

# CDK repository path
cdk_path := "../cdk"

# Display project information
info:
    @echo "CDK Python Bindings"
    @echo "==================="
    @echo "Python version: $(python --version)"
    @echo "CDK path: {{cdk_path}}"
    @echo "Rust version: $(rustc --version)"

# Check that CDK repository exists
check-cdk:
    @test -d {{cdk_path}} || (echo "Error: CDK repository not found at {{cdk_path}}" && exit 1)
    @echo "CDK repository found at {{cdk_path}}"

# Install development dependencies
install-dev:
    pip install -r requirements-dev.txt

# Generate Python bindings for current platform
generate: check-cdk
    @echo "Detecting platform and generating bindings..."
    @if [[ "$OSTYPE" == "darwin"* ]]; then \
        if [[ $(uname -m) == "arm64" ]]; then \
            ./scripts/generate-macos-arm64.sh; \
        else \
            ./scripts/generate-macos-x86_64.sh; \
        fi \
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then \
        if [[ $(uname -m) == "aarch64" ]]; then \
            ./scripts/generate-linux-aarch64.sh; \
        else \
            ./scripts/generate-linux-x86_64.sh; \
        fi \
    elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then \
        ./scripts/generate-windows-x86_64.sh; \
    else \
        echo "Unsupported platform: $OSTYPE"; \
        exit 1; \
    fi

# Generate bindings for macOS ARM64 (Apple Silicon)
generate-macos-arm64: check-cdk
    ./scripts/generate-macos-arm64.sh

# Generate bindings for macOS x86_64 (Intel)
generate-macos-x86_64: check-cdk
    ./scripts/generate-macos-x86_64.sh

# Generate bindings for Linux x86_64
generate-linux-x86_64: check-cdk
    ./scripts/generate-linux-x86_64.sh

# Generate bindings for Linux ARM64
generate-linux-aarch64: check-cdk
    ./scripts/generate-linux-aarch64.sh

# Generate bindings for Windows x86_64
generate-windows-x86_64: check-cdk
    ./scripts/generate-windows-x86_64.sh

# Build Python package (requires generated bindings)
build:
    python -m build

# Install package in development mode
install: generate
    pip install -e .

# Run all tests
test:
    PYTHONPATH=src venv/bin/pytest tests/ -v

# Run tests with coverage
test-cov:
    PYTHONPATH=src venv/bin/pytest tests/ -v --cov=cdk --cov-report=html --cov-report=term

# Run specific test file
test-file FILE:
    PYTHONPATH=src venv/bin/pytest tests/{{FILE}} -v

# Run tests matching pattern
test-pattern PATTERN:
    PYTHONPATH=src venv/bin/pytest tests/ -v -k "{{PATTERN}}"

# Format code with black
format:
    black src/ tests/
    isort src/ tests/

# Check code formatting
format-check:
    black --check src/ tests/
    isort --check-only src/ tests/

# Lint code
lint:
    flake8 src/ tests/
    pylint src/cdk/ tests/
    mypy src/cdk/

# Run all code quality checks
check: format-check lint test

# Clean build artifacts
clean:
    rm -rf build/
    rm -rf dist/
    rm -rf *.egg-info/
    rm -rf .pytest_cache/
    rm -rf .mypy_cache/
    rm -rf .coverage
    rm -rf htmlcov/
    find . -type d -name __pycache__ -exec rm -rf {} +
    find . -type f -name "*.pyc" -delete
    find . -type f -name "*.pyo" -delete
    find . -type f -name "*.so" -delete
    find . -type f -name "*.dylib" -delete
    find . -type f -name "*.dll" -delete

# Clean generated bindings
clean-bindings:
    rm -f src/cdk/cdk.py
    rm -f src/cdk/libcdk_ffi.*
    rm -f src/cdk/cdk_ffi.dll

# Clean everything including Rust build artifacts in CDK
clean-all: clean clean-bindings
    cd {{cdk_path}} && cargo clean

# Build wheel for distribution
wheel: build
    @echo "Wheel created in dist/"
    @ls -lh dist/*.whl

# Build source distribution
sdist: build
    @echo "Source distribution created in dist/"
    @ls -lh dist/*.tar.gz

# Upload to PyPI (requires TWINE_USERNAME and TWINE_PASSWORD)
publish: clean build
    twine check dist/*
    twine upload dist/*

# Upload to Test PyPI
publish-test: clean build
    twine check dist/*
    twine upload --repository testpypi dist/*

# Start Python REPL with cdk imported
repl: generate
    python -c "import sys; sys.path.insert(0, 'src'); import cdk; print('CDK module loaded. Try: dir(cdk)'); import code; code.interact(local=dict(globals(), **locals()))"

# Run a simple test to verify bindings work
verify: generate
    python -c "import sys; sys.path.insert(0, 'src'); import cdk; print('✓ CDK Python bindings loaded successfully'); print(f'Available: {[x for x in dir(cdk) if not x.startswith(\"_\")][:10]}...')"

# Create new release (tag and push)
release VERSION:
    @echo "Creating release {{VERSION}}"
    @git tag -a v{{VERSION}} -m "Release v{{VERSION}}"
    @git push origin v{{VERSION}}
    @echo "Release v{{VERSION}} created and pushed"

# Open repository in browser
repo:
    @open https://github.com/cashubtc/cdk-python || xdg-open https://github.com/cashubtc/cdk-python
