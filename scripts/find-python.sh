#!/bin/bash
# Helper script to find the correct Python binary in manylinux containers
# Usage: ./find-python.sh 3.10
# Returns: Path to Python binary

set -euo pipefail

if [ $# -ne 1 ]; then
    echo "Usage: $0 <python-version>" >&2
    echo "Example: $0 3.10" >&2
    exit 1
fi

PYTHON_VERSION="$1"
PYVER=$(echo "$PYTHON_VERSION" | tr -d .)

# Try the standard manylinux path first
PYTHON_BIN="/opt/python/cp${PYVER}-cp${PYVER}/bin/python"

# If exact path doesn't exist, try glob pattern (for different build variants)
if [ ! -f "$PYTHON_BIN" ]; then
    # Find Python binaries matching the version, excluding debug builds
    PYTHON_BIN=$(ls /opt/python/cp${PYVER}-cp${PYVER}*/bin/python 2>/dev/null | grep -v "t/bin/python" | head -n1 || true)

    # If still not found, try system Python as fallback
    if [ -z "$PYTHON_BIN" ] || [ ! -f "$PYTHON_BIN" ]; then
        if command -v python${PYTHON_VERSION} &> /dev/null; then
            PYTHON_BIN=$(command -v python${PYTHON_VERSION})
        elif command -v python3 &> /dev/null; then
            # Check if system python3 matches requested version
            SYSTEM_VERSION=$(python3 --version 2>&1 | grep -oP '\d+\.\d+' | head -1)
            if [ "$SYSTEM_VERSION" = "$PYTHON_VERSION" ]; then
                PYTHON_BIN=$(command -v python3)
            fi
        fi
    fi
fi

# Validate the Python binary was found
if [ -z "$PYTHON_BIN" ] || [ ! -f "$PYTHON_BIN" ]; then
    echo "Error: Python $PYTHON_VERSION not found" >&2
    echo "Searched paths:" >&2
    echo "  - /opt/python/cp${PYVER}-cp${PYVER}/bin/python" >&2
    echo "  - /opt/python/cp${PYVER}-cp${PYVER}*/bin/python" >&2
    echo "  - python${PYTHON_VERSION} (system)" >&2
    exit 1
fi

# Verify the Python version matches what we expect
ACTUAL_VERSION=$($PYTHON_BIN --version 2>&1 | grep -oP '\d+\.\d+' | head -1)
if [ "$ACTUAL_VERSION" != "$PYTHON_VERSION" ]; then
    echo "Warning: Python version mismatch. Expected $PYTHON_VERSION, got $ACTUAL_VERSION" >&2
fi

echo "$PYTHON_BIN"