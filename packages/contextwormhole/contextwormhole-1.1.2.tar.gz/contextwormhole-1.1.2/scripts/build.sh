#!/bin/bash
# build.sh - Build the package
# ===========================

# Exit on error
set -e

# Clean up previous builds
echo "Cleaning up previous builds..."
rm -rf build/ dist/ *.egg-info/

# Install build dependencies
echo "Installing build dependencies..."
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade build twine

# Build the package
echo "Building package..."
python3 -m build

# Check the package
echo "Checking package..."
python3 -m twine check dist/*

echo "Build completed successfully!"
echo "Distribution files are in the 'dist/' directory."
echo ""
echo "To install the package locally, run:"
echo "pip3 install dist/*.whl"
echo ""
echo "To publish to PyPI, use the publish.sh script."