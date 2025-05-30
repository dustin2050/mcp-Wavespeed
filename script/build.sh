#!/bin/bash

set -e

# change to project root
cd "$(dirname "$0")/.." || exit 1

# show current directory and version
echo "current directory: $(pwd)"
VERSION=$(grep -m 1 "version =" pyproject.toml | cut -d '"' -f2)
echo "build version: $VERSION"

# clean old build files
echo "clean old build files..."
rm -rf dist/ build/ *.egg-info/

# install build tools
echo "install/upgrade build tools..."
pip install --upgrade build twine

# build package
echo "build distribution package..."
python -m build

# list built files
echo "built files:"
ls -l dist/

# confirm upload
read -p "upload to PyPI? (y/n): " UPLOAD
if [[ "$UPLOAD" == "y" || "$UPLOAD" == "Y" ]]; then
    echo "upload to PyPI..."
    python -m twine upload dist/*
    echo "upload completed!"
else
    echo "skip upload."
fi

echo "build process completed."
