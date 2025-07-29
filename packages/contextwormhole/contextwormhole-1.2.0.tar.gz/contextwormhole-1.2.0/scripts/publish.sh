#!/bin/bash
# publish.sh - Build and publish package to PyPI
# =============================================

# Exit on error
set -e

# Clean up previous builds
echo "Cleaning up previous builds..."
rm -rf build/ dist/ *.egg-info/

# Build the package
echo "Building package..."
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade build twine
python3 -m build

# Check the package
echo "Checking package..."
python3 -m twine check dist/*

# Publish to PyPI
echo "Ready to publish to PyPI"
echo "------------------------"
echo "This will publish the package directly to PyPI (not TestPyPI)"
echo "Command that will be executed: python -m twine upload dist/*"
echo ""

# Ask for confirmation
read -p "Do you want to publish to PyPI? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python3 -m twine upload dist/*
    echo "Published to PyPI!"
    echo "To install from PyPI, run:"
    echo "pip3 install contextwormhole"
fi

echo "Done!"